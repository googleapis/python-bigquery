# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Classes for query jobs."""

import concurrent.futures
import copy
import re
import typing
from typing import Any, Dict, Optional, Union

from google.api_core import exceptions
from google.api_core.future import polling as polling_future
import requests

from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetListItem
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration
from google.cloud.bigquery.enums import KeyResultStatementKind
from google.cloud.bigquery.external_config import ExternalConfig
from google.cloud.bigquery import _helpers
from google.cloud.bigquery.query import _query_param_from_api_repr
from google.cloud.bigquery.query import ArrayQueryParameter
from google.cloud.bigquery.query import ScalarQueryParameter
from google.cloud.bigquery.query import StructQueryParameter
from google.cloud.bigquery.query import UDFResource
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.routine import RoutineReference
from google.cloud.bigquery.table import _EmptyRowIterator
from google.cloud.bigquery.table import RangePartitioning
from google.cloud.bigquery.table import _table_arg_to_table_ref
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import TimePartitioning
from google.cloud.bigquery._tqdm_helpers import wait_for_query

from google.cloud.bigquery.job.base import _AsyncJob
from google.cloud.bigquery.job.base import _JobConfig
from google.cloud.bigquery.job.base import _JobReference

if typing.TYPE_CHECKING:  # pragma: NO COVER
    # Assumption: type checks are only used by library developers and CI environments
    # that have all optional dependencies installed, thus no conditional imports.
    import pandas
    import pyarrow
    from google.api_core import retry as retries
    from google.cloud import bigquery_storage
    from google.cloud.bigquery.table import RowIterator


_CONTAINS_ORDER_BY = re.compile(r"ORDER\s+BY", re.IGNORECASE)
_TIMEOUT_BUFFER_SECS = 0.1


def _contains_order_by(query):
    """Do we need to preserve the order of the query results?

    This function has known false positives, such as with ordered window
    functions:

    .. code-block:: sql

       SELECT SUM(x) OVER (
           window_name
           PARTITION BY...
           ORDER BY...
           window_frame_clause)
       FROM ...

    This false positive failure case means the behavior will be correct, but
    downloading results with the BigQuery Storage API may be slower than it
    otherwise would. This is preferable to the false negative case, where
    results are expected to be in order but are not (due to parallel reads).
    """
    return query and _CONTAINS_ORDER_BY.search(query)


def _from_api_repr_query_parameters(resource):
    return [_query_param_from_api_repr(mapping) for mapping in resource]


def _to_api_repr_query_parameters(value):
    return [query_parameter.to_api_repr() for query_parameter in value]


def _from_api_repr_udf_resources(resource):
    udf_resources = []
    for udf_mapping in resource:
        for udf_type, udf_value in udf_mapping.items():
            udf_resources.append(UDFResource(udf_type, udf_value))
    return udf_resources


def _to_api_repr_udf_resources(value):
    return [{udf_resource.udf_type: udf_resource.value} for udf_resource in value]


def _from_api_repr_table_defs(resource):
    return {k: ExternalConfig.from_api_repr(v) for k, v in resource.items()}


def _to_api_repr_table_defs(value):
    return {k: ExternalConfig.to_api_repr(v) for k, v in value.items()}


class ScriptOptions:
    """Options controlling the execution of scripts.

    https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#ScriptOptions
    """

    def __init__(
        self,
        statement_timeout_ms: Optional[int] = None,
        statement_byte_budget: Optional[int] = None,
        key_result_statement: Optional[KeyResultStatementKind] = None,
    ):
        self._properties = {}
        self.statement_timeout_ms = statement_timeout_ms
        self.statement_byte_budget = statement_byte_budget
        self.key_result_statement = key_result_statement

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "ScriptOptions":
        """Factory: construct instance from the JSON repr.

        Args:
            resource(Dict[str: Any]):
                ScriptOptions representation returned from API.

        Returns:
            google.cloud.bigquery.ScriptOptions:
                ScriptOptions sample parsed from ``resource``.
        """
        entry = cls()
        entry._properties = copy.deepcopy(resource)
        return entry

    def to_api_repr(self) -> Dict[str, Any]:
        """Construct the API resource representation."""
        return copy.deepcopy(self._properties)

    @property
    def statement_timeout_ms(self) -> Union[int, None]:
        """Timeout period for each statement in a script."""
        return _helpers._int_or_none(self._properties.get("statementTimeoutMs"))

    @statement_timeout_ms.setter
    def statement_timeout_ms(self, value: Union[int, None]):
        if value is not None:
            value = str(value)
        self._properties["statementTimeoutMs"] = value

    @property
    def statement_byte_budget(self) -> Union[int, None]:
        """Limit on the number of bytes billed per statement.

        Exceeding this budget results in an error.
        """
        return _helpers._int_or_none(self._properties.get("statementByteBudget"))

    @statement_byte_budget.setter
    def statement_byte_budget(self, value: Union[int, None]):
        if value is not None:
            value = str(value)
        self._properties["statementByteBudget"] = value

    @property
    def key_result_statement(self) -> Union[KeyResultStatementKind, None]:
        """Determines which statement in the script represents the "key result".

        This is used to populate the schema and query results of the script job.
        Default is ``KeyResultStatementKind.LAST``.
        """
        return self._properties.get("keyResultStatement")

    @key_result_statement.setter
    def key_result_statement(self, value: Union[KeyResultStatementKind, None]):
        self._properties["keyResultStatement"] = value


class QueryJobConfig(_JobConfig):
    """Configuration options for query jobs.

    All properties in this class are optional. Values which are :data:`None` ->
    server defaults. Set properties on the constructed configuration by using
    the property name as the name of a keyword argument.
    """

    def __init__(self, **kwargs):
        super(QueryJobConfig, self).__init__("query", **kwargs)

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.encryption_configuration.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.destination_encryption_configuration
        """
        prop = self._get_sub_prop("destinationEncryptionConfiguration")
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @destination_encryption_configuration.setter
    def destination_encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop("destinationEncryptionConfiguration", api_repr)

    @property
    def allow_large_results(self):
        """bool: Allow large query results tables (legacy SQL, only)

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.allow_large_results
        """
        return self._get_sub_prop("allowLargeResults")

    @allow_large_results.setter
    def allow_large_results(self, value):
        self._set_sub_prop("allowLargeResults", value)

    @property
    def create_disposition(self):
        """google.cloud.bigquery.job.CreateDisposition: Specifies behavior
        for creating tables.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.create_disposition
        """
        return self._get_sub_prop("createDisposition")

    @create_disposition.setter
    def create_disposition(self, value):
        self._set_sub_prop("createDisposition", value)

    @property
    def default_dataset(self):
        """google.cloud.bigquery.dataset.DatasetReference: the default dataset
        to use for unqualified table names in the query or :data:`None` if not
        set.

        The ``default_dataset`` setter accepts:

        - a :class:`~google.cloud.bigquery.dataset.Dataset`, or
        - a :class:`~google.cloud.bigquery.dataset.DatasetReference`, or
        - a :class:`str` of the fully-qualified dataset ID in standard SQL
          format. The value must included a project ID and dataset ID
          separated by ``.``. For example: ``your-project.your_dataset``.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.default_dataset
        """
        prop = self._get_sub_prop("defaultDataset")
        if prop is not None:
            prop = DatasetReference.from_api_repr(prop)
        return prop

    @default_dataset.setter
    def default_dataset(self, value):
        if value is None:
            self._set_sub_prop("defaultDataset", None)
            return

        if isinstance(value, str):
            value = DatasetReference.from_string(value)

        if isinstance(value, (Dataset, DatasetListItem)):
            value = value.reference

        resource = value.to_api_repr()
        self._set_sub_prop("defaultDataset", resource)

    @property
    def destination(self):
        """google.cloud.bigquery.table.TableReference: table where results are
        written or :data:`None` if not set.

        The ``destination`` setter accepts:

        - a :class:`~google.cloud.bigquery.table.Table`, or
        - a :class:`~google.cloud.bigquery.table.TableReference`, or
        - a :class:`str` of the fully-qualified table ID in standard SQL
          format. The value must included a project ID, dataset ID, and table
          ID, each separated by ``.``. For example:
          ``your-project.your_dataset.your_table``.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.destination_table
        """
        prop = self._get_sub_prop("destinationTable")
        if prop is not None:
            prop = TableReference.from_api_repr(prop)
        return prop

    @destination.setter
    def destination(self, value):
        if value is None:
            self._set_sub_prop("destinationTable", None)
            return

        value = _table_arg_to_table_ref(value)
        resource = value.to_api_repr()
        self._set_sub_prop("destinationTable", resource)

    @property
    def dry_run(self):
        """bool: :data:`True` if this query should be a dry run to estimate
        costs.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfiguration.FIELDS.dry_run
        """
        return self._properties.get("dryRun")

    @dry_run.setter
    def dry_run(self, value):
        self._properties["dryRun"] = value

    @property
    def flatten_results(self):
        """bool: Flatten nested/repeated fields in results. (Legacy SQL only)

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.flatten_results
        """
        return self._get_sub_prop("flattenResults")

    @flatten_results.setter
    def flatten_results(self, value):
        self._set_sub_prop("flattenResults", value)

    @property
    def maximum_billing_tier(self):
        """int: Deprecated. Changes the billing tier to allow high-compute
        queries.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.maximum_billing_tier
        """
        return self._get_sub_prop("maximumBillingTier")

    @maximum_billing_tier.setter
    def maximum_billing_tier(self, value):
        self._set_sub_prop("maximumBillingTier", value)

    @property
    def maximum_bytes_billed(self):
        """int: Maximum bytes to be billed for this job or :data:`None` if not set.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.maximum_bytes_billed
        """
        return _helpers._int_or_none(self._get_sub_prop("maximumBytesBilled"))

    @maximum_bytes_billed.setter
    def maximum_bytes_billed(self, value):
        self._set_sub_prop("maximumBytesBilled", str(value))

    @property
    def priority(self):
        """google.cloud.bigquery.job.QueryPriority: Priority of the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.priority
        """
        return self._get_sub_prop("priority")

    @priority.setter
    def priority(self, value):
        self._set_sub_prop("priority", value)

    @property
    def query_parameters(self):
        """List[Union[google.cloud.bigquery.query.ArrayQueryParameter, \
        google.cloud.bigquery.query.ScalarQueryParameter, \
        google.cloud.bigquery.query.StructQueryParameter]]: list of parameters
        for parameterized query (empty by default)

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.query_parameters
        """
        prop = self._get_sub_prop("queryParameters", default=[])
        return _from_api_repr_query_parameters(prop)

    @query_parameters.setter
    def query_parameters(self, values):
        self._set_sub_prop("queryParameters", _to_api_repr_query_parameters(values))

    @property
    def range_partitioning(self):
        """Optional[google.cloud.bigquery.table.RangePartitioning]:
        Configures range-based partitioning for destination table.

        .. note::
            **Beta**. The integer range partitioning feature is in a
            pre-release state and might change or have limited support.

        Only specify at most one of
        :attr:`~google.cloud.bigquery.job.LoadJobConfig.time_partitioning` or
        :attr:`~google.cloud.bigquery.job.LoadJobConfig.range_partitioning`.

        Raises:
            ValueError:
                If the value is not
                :class:`~google.cloud.bigquery.table.RangePartitioning` or
                :data:`None`.
        """
        resource = self._get_sub_prop("rangePartitioning")
        if resource is not None:
            return RangePartitioning(_properties=resource)

    @range_partitioning.setter
    def range_partitioning(self, value):
        resource = value
        if isinstance(value, RangePartitioning):
            resource = value._properties
        elif value is not None:
            raise ValueError(
                "Expected value to be RangePartitioning or None, got {}.".format(value)
            )
        self._set_sub_prop("rangePartitioning", resource)

    @property
    def udf_resources(self):
        """List[google.cloud.bigquery.query.UDFResource]: user
        defined function resources (empty by default)

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.user_defined_function_resources
        """
        prop = self._get_sub_prop("userDefinedFunctionResources", default=[])
        return _from_api_repr_udf_resources(prop)

    @udf_resources.setter
    def udf_resources(self, values):
        self._set_sub_prop(
            "userDefinedFunctionResources", _to_api_repr_udf_resources(values)
        )

    @property
    def use_legacy_sql(self):
        """bool: Use legacy SQL syntax.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.use_legacy_sql
        """
        return self._get_sub_prop("useLegacySql")

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        self._set_sub_prop("useLegacySql", value)

    @property
    def use_query_cache(self):
        """bool: Look for the query result in the cache.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.use_query_cache
        """
        return self._get_sub_prop("useQueryCache")

    @use_query_cache.setter
    def use_query_cache(self, value):
        self._set_sub_prop("useQueryCache", value)

    @property
    def write_disposition(self):
        """google.cloud.bigquery.job.WriteDisposition: Action that occurs if
        the destination table already exists.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.write_disposition
        """
        return self._get_sub_prop("writeDisposition")

    @write_disposition.setter
    def write_disposition(self, value):
        self._set_sub_prop("writeDisposition", value)

    @property
    def table_definitions(self):
        """Dict[str, google.cloud.bigquery.external_config.ExternalConfig]:
        Definitions for external tables or :data:`None` if not set.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.external_table_definitions
        """
        prop = self._get_sub_prop("tableDefinitions")
        if prop is not None:
            prop = _from_api_repr_table_defs(prop)
        return prop

    @table_definitions.setter
    def table_definitions(self, values):
        self._set_sub_prop("tableDefinitions", _to_api_repr_table_defs(values))

    @property
    def time_partitioning(self):
        """Optional[google.cloud.bigquery.table.TimePartitioning]: Specifies
        time-based partitioning for the destination table.

        Only specify at most one of
        :attr:`~google.cloud.bigquery.job.LoadJobConfig.time_partitioning` or
        :attr:`~google.cloud.bigquery.job.LoadJobConfig.range_partitioning`.

        Raises:
            ValueError:
                If the value is not
                :class:`~google.cloud.bigquery.table.TimePartitioning` or
                :data:`None`.
        """
        prop = self._get_sub_prop("timePartitioning")
        if prop is not None:
            prop = TimePartitioning.from_api_repr(prop)
        return prop

    @time_partitioning.setter
    def time_partitioning(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop("timePartitioning", api_repr)

    @property
    def clustering_fields(self):
        """Optional[List[str]]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           BigQuery supports clustering for both partitioned and
           non-partitioned tables.
        """
        prop = self._get_sub_prop("clustering")
        if prop is not None:
            return list(prop.get("fields", ()))

    @clustering_fields.setter
    def clustering_fields(self, value):
        """Optional[List[str]]: Fields defining clustering for the table

        (Defaults to :data:`None`).
        """
        if value is not None:
            self._set_sub_prop("clustering", {"fields": value})
        else:
            self._del_sub_prop("clustering")

    @property
    def schema_update_options(self):
        """List[google.cloud.bigquery.job.SchemaUpdateOption]: Specifies
        updates to the destination table schema to allow as a side effect of
        the query job.
        """
        return self._get_sub_prop("schemaUpdateOptions")

    @schema_update_options.setter
    def schema_update_options(self, values):
        self._set_sub_prop("schemaUpdateOptions", values)

    @property
    def script_options(self) -> ScriptOptions:
        """Connection properties which can modify the query behavior.

        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#scriptoptions
        """
        prop = self._get_sub_prop("scriptOptions")
        if prop is not None:
            prop = ScriptOptions.from_api_repr(prop)
        return prop

    @script_options.setter
    def script_options(self, value: Union[ScriptOptions, None]):
        if value is not None:
            value = value.to_api_repr()
        self._set_sub_prop("scriptOptions", value)

    def to_api_repr(self) -> dict:
        """Build an API representation of the query job config.

        Returns:
            Dict: A dictionary in the format used by the BigQuery API.
        """
        resource = copy.deepcopy(self._properties)

        # Query parameters have an addition property associated with them
        # to indicate if the query is using named or positional parameters.
        query_parameters = resource["query"].get("queryParameters")
        if query_parameters:
            if query_parameters[0].get("name") is None:
                resource["query"]["parameterMode"] = "POSITIONAL"
            else:
                resource["query"]["parameterMode"] = "NAMED"

        return resource


class QueryJob(_AsyncJob):
    """Asynchronous job: query tables.

    Args:
        job_id (str): the job's ID, within the project belonging to ``client``.

        query (str): SQL query string.

        client (google.cloud.bigquery.client.Client):
            A client which holds credentials and project configuration
            for the dataset (which requires a project).

        job_config (Optional[google.cloud.bigquery.job.QueryJobConfig]):
            Extra configuration options for the query job.
    """

    _JOB_TYPE = "query"
    _UDF_KEY = "userDefinedFunctionResources"

    def __init__(self, job_id, query, client, job_config=None):
        super(QueryJob, self).__init__(job_id, client)

        if job_config is None:
            job_config = QueryJobConfig()
        if job_config.use_legacy_sql is None:
            job_config.use_legacy_sql = False

        self._properties["configuration"] = job_config._properties
        self._configuration = job_config

        if query:
            _helpers._set_sub_prop(
                self._properties, ["configuration", "query", "query"], query
            )

        self._query_results = None
        self._done_timeout = None
        self._transport_timeout = None

    @property
    def allow_large_results(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.allow_large_results`.
        """
        return self._configuration.allow_large_results

    @property
    def create_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.create_disposition`.
        """
        return self._configuration.create_disposition

    @property
    def default_dataset(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.default_dataset`.
        """
        return self._configuration.default_dataset

    @property
    def destination(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.destination`.
        """
        return self._configuration.destination

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.encryption_configuration.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.destination_encryption_configuration`.
        """
        return self._configuration.destination_encryption_configuration

    @property
    def dry_run(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.dry_run`.
        """
        return self._configuration.dry_run

    @property
    def flatten_results(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.flatten_results`.
        """
        return self._configuration.flatten_results

    @property
    def priority(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.priority`.
        """
        return self._configuration.priority

    @property
    def query(self):
        """str: The query text used in this query job.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery.FIELDS.query
        """
        return _helpers._get_sub_prop(
            self._properties, ["configuration", "query", "query"]
        )

    @property
    def query_parameters(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.query_parameters`.
        """
        return self._configuration.query_parameters

    @property
    def udf_resources(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.udf_resources`.
        """
        return self._configuration.udf_resources

    @property
    def use_legacy_sql(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.use_legacy_sql`.
        """
        return self._configuration.use_legacy_sql

    @property
    def use_query_cache(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.use_query_cache`.
        """
        return self._configuration.use_query_cache

    @property
    def write_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.write_disposition`.
        """
        return self._configuration.write_disposition

    @property
    def maximum_billing_tier(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.maximum_billing_tier`.
        """
        return self._configuration.maximum_billing_tier

    @property
    def maximum_bytes_billed(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.maximum_bytes_billed`.
        """
        return self._configuration.maximum_bytes_billed

    @property
    def range_partitioning(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.range_partitioning`.
        """
        return self._configuration.range_partitioning

    @property
    def table_definitions(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.table_definitions`.
        """
        return self._configuration.table_definitions

    @property
    def time_partitioning(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.time_partitioning`.
        """
        return self._configuration.time_partitioning

    @property
    def clustering_fields(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.clustering_fields`.
        """
        return self._configuration.clustering_fields

    @property
    def schema_update_options(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.schema_update_options`.
        """
        return self._configuration.schema_update_options

    def to_api_repr(self):
        """Generate a resource for :meth:`_begin`."""
        # Use to_api_repr to allow for some configuration properties to be set
        # automatically.
        configuration = self._configuration.to_api_repr()
        return {
            "jobReference": self._properties["jobReference"],
            "configuration": configuration,
        }

    @classmethod
    def from_api_repr(cls, resource: dict, client) -> "QueryJob":
        """Factory:  construct a job given its API representation

        Args:
            resource (Dict): dataset job representation returned from the API

            client (google.cloud.bigquery.client.Client):
                Client which holds credentials and project
                configuration for the dataset.

        Returns:
            google.cloud.bigquery.job.QueryJob: Job parsed from ``resource``.
        """
        cls._check_resource_config(resource)
        job_ref = _JobReference._from_api_repr(resource["jobReference"])
        job = cls(job_ref, None, client=client)
        job._set_properties(resource)
        return job

    @property
    def query_plan(self):
        """Return query plan from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.query_plan

        Returns:
            List[google.cloud.bigquery.job.QueryPlanEntry]:
                mappings describing the query plan, or an empty list
                if the query has not yet completed.
        """
        plan_entries = self._job_statistics().get("queryPlan", ())
        return [QueryPlanEntry.from_api_repr(entry) for entry in plan_entries]

    @property
    def timeline(self):
        """List(TimelineEntry): Return the query execution timeline
        from job statistics.
        """
        raw = self._job_statistics().get("timeline", ())
        return [TimelineEntry.from_api_repr(entry) for entry in raw]

    @property
    def total_bytes_processed(self):
        """Return total bytes processed from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.total_bytes_processed

        Returns:
            Optional[int]:
                Total bytes processed by the job, or None if job is not
                yet complete.
        """
        result = self._job_statistics().get("totalBytesProcessed")
        if result is not None:
            result = int(result)
        return result

    @property
    def total_bytes_billed(self):
        """Return total bytes billed from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.total_bytes_billed

        Returns:
            Optional[int]:
                Total bytes processed by the job, or None if job is not
                yet complete.
        """
        result = self._job_statistics().get("totalBytesBilled")
        if result is not None:
            result = int(result)
        return result

    @property
    def billing_tier(self):
        """Return billing tier from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.billing_tier

        Returns:
            Optional[int]:
                Billing tier used by the job, or None if job is not
                yet complete.
        """
        return self._job_statistics().get("billingTier")

    @property
    def cache_hit(self):
        """Return whether or not query results were served from cache.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.cache_hit

        Returns:
            Optional[bool]:
                whether the query results were returned from cache, or None
                if job is not yet complete.
        """
        return self._job_statistics().get("cacheHit")

    @property
    def ddl_operation_performed(self):
        """Optional[str]: Return the DDL operation performed.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.ddl_operation_performed

        """
        return self._job_statistics().get("ddlOperationPerformed")

    @property
    def ddl_target_routine(self):
        """Optional[google.cloud.bigquery.routine.RoutineReference]: Return the DDL target routine, present
            for CREATE/DROP FUNCTION/PROCEDURE  queries.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.ddl_target_routine
        """
        prop = self._job_statistics().get("ddlTargetRoutine")
        if prop is not None:
            prop = RoutineReference.from_api_repr(prop)
        return prop

    @property
    def ddl_target_table(self):
        """Optional[google.cloud.bigquery.table.TableReference]: Return the DDL target table, present
            for CREATE/DROP TABLE/VIEW queries.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.ddl_target_table
        """
        prop = self._job_statistics().get("ddlTargetTable")
        if prop is not None:
            prop = TableReference.from_api_repr(prop)
        return prop

    @property
    def num_dml_affected_rows(self):
        """Return the number of DML rows affected by the job.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.num_dml_affected_rows

        Returns:
            Optional[int]:
                number of DML rows affected by the job, or None if job is not
                yet complete.
        """
        result = self._job_statistics().get("numDmlAffectedRows")
        if result is not None:
            result = int(result)
        return result

    @property
    def slot_millis(self):
        """Union[int, None]: Slot-milliseconds used by this query job."""
        return _helpers._int_or_none(self._job_statistics().get("totalSlotMs"))

    @property
    def statement_type(self):
        """Return statement type from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.statement_type

        Returns:
            Optional[str]:
                type of statement used by the job, or None if job is not
                yet complete.
        """
        return self._job_statistics().get("statementType")

    @property
    def referenced_tables(self):
        """Return referenced tables from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.referenced_tables

        Returns:
            List[Dict]:
                mappings describing the query plan, or an empty list
                if the query has not yet completed.
        """
        tables = []
        datasets_by_project_name = {}

        for table in self._job_statistics().get("referencedTables", ()):

            t_project = table["projectId"]

            ds_id = table["datasetId"]
            t_dataset = datasets_by_project_name.get((t_project, ds_id))
            if t_dataset is None:
                t_dataset = DatasetReference(t_project, ds_id)
                datasets_by_project_name[(t_project, ds_id)] = t_dataset

            t_name = table["tableId"]
            tables.append(t_dataset.table(t_name))

        return tables

    @property
    def undeclared_query_parameters(self):
        """Return undeclared query parameters from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.undeclared_query_parameters

        Returns:
            List[Union[ \
                google.cloud.bigquery.query.ArrayQueryParameter, \
                google.cloud.bigquery.query.ScalarQueryParameter, \
                google.cloud.bigquery.query.StructQueryParameter \
            ]]:
                Undeclared parameters, or an empty list if the query has
                not yet completed.
        """
        parameters = []
        undeclared = self._job_statistics().get("undeclaredQueryParameters", ())

        for parameter in undeclared:
            p_type = parameter["parameterType"]

            if "arrayType" in p_type:
                klass = ArrayQueryParameter
            elif "structTypes" in p_type:
                klass = StructQueryParameter
            else:
                klass = ScalarQueryParameter

            parameters.append(klass.from_api_repr(parameter))

        return parameters

    @property
    def estimated_bytes_processed(self):
        """Return the estimated number of bytes processed by the query.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobStatistics2.FIELDS.estimated_bytes_processed

        Returns:
            Optional[int]:
                number of DML rows affected by the job, or None if job is not
                yet complete.
        """
        result = self._job_statistics().get("estimatedBytesProcessed")
        if result is not None:
            result = int(result)
        return result

    def _blocking_poll(self, timeout=None, **kwargs):
        self._done_timeout = timeout
        self._transport_timeout = timeout
        super(QueryJob, self)._blocking_poll(timeout=timeout, **kwargs)

    @staticmethod
    def _format_for_exception(query, job_id):
        """Format a query for the output in exception message.

        Args:
            query (str): The SQL query to format.
            job_id (str): The ID of the job that ran the query.

        Returns:
            str: A formatted query text.
        """
        template = "\n\n(job ID: {job_id})\n\n{header}\n\n{ruler}\n{body}\n{ruler}"

        lines = query.splitlines()
        max_line_len = max(len(line) for line in lines)

        header = "-----Query Job SQL Follows-----"
        header = "{:^{total_width}}".format(header, total_width=max_line_len + 5)

        # Print out a "ruler" above and below the SQL so we can judge columns.
        # Left pad for the line numbers (4 digits plus ":").
        ruler = "    |" + "    .    |" * (max_line_len // 10)

        # Put line numbers next to the SQL.
        body = "\n".join(
            "{:4}:{}".format(n, line) for n, line in enumerate(lines, start=1)
        )

        return template.format(job_id=job_id, header=header, ruler=ruler, body=body)

    def _begin(self, client=None, retry=DEFAULT_RETRY, timeout=None):
        """API call:  begin the job via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert

        Args:
            client (Optional[google.cloud.bigquery.client.Client]):
                The client to use. If not passed, falls back to the ``client``
                associated with the job object or``NoneType``.
            retry (Optional[google.api_core.retry.Retry]):
                How to retry the RPC.
            timeout (Optional[float]):
                The number of seconds to wait for the underlying HTTP transport
                before using ``retry``.

        Raises:
            ValueError: If the job has already begun.
        """

        try:
            super(QueryJob, self)._begin(client=client, retry=retry, timeout=timeout)
        except exceptions.GoogleAPICallError as exc:
            exc.message += self._format_for_exception(self.query, self.job_id)
            exc.query_job = self
            raise

    def _reload_query_results(
        self, retry: "retries.Retry" = DEFAULT_RETRY, timeout: float = None
    ):
        """Refresh the cached query results.

        Args:
            retry (Optional[google.api_core.retry.Retry]):
                How to retry the call that retrieves query results.
            timeout (Optional[float]):
                The number of seconds to wait for the underlying HTTP transport
                before using ``retry``.
        """
        if self._query_results and self._query_results.complete:
            return

        # Since the API to getQueryResults can hang up to the timeout value
        # (default of 10 seconds), set the timeout parameter to ensure that
        # the timeout from the futures API is respected. See:
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/4135
        timeout_ms = None
        if self._done_timeout is not None:
            # Subtract a buffer for context switching, network latency, etc.
            api_timeout = self._done_timeout - _TIMEOUT_BUFFER_SECS
            api_timeout = max(min(api_timeout, 10), 0)
            self._done_timeout -= api_timeout
            self._done_timeout = max(0, self._done_timeout)
            timeout_ms = int(api_timeout * 1000)

        # If an explicit timeout is not given, fall back to the transport timeout
        # stored in _blocking_poll() in the process of polling for job completion.
        transport_timeout = timeout if timeout is not None else self._transport_timeout

        self._query_results = self._client._get_query_results(
            self.job_id,
            retry,
            project=self.project,
            timeout_ms=timeout_ms,
            location=self.location,
            timeout=transport_timeout,
        )

    def _done_or_raise(self, retry=DEFAULT_RETRY, timeout=None):
        """Check if the query has finished running and raise if it's not.

        If the query has finished, also reload the job itself.
        """
        # If an explicit timeout is not given, fall back to the transport timeout
        # stored in _blocking_poll() in the process of polling for job completion.
        transport_timeout = timeout if timeout is not None else self._transport_timeout

        try:
            self._reload_query_results(retry=retry, timeout=transport_timeout)
        except exceptions.GoogleAPIError as exc:
            # Reloading also updates error details on self, thus no need for an
            # explicit self.set_exception() call if reloading succeeds.
            try:
                self.reload(retry=retry, timeout=transport_timeout)
            except exceptions.GoogleAPIError:
                # Use the query results reload exception, as it generally contains
                # much more useful error information.
                self.set_exception(exc)
            finally:
                return

        # Only reload the job once we know the query is complete.
        # This will ensure that fields such as the destination table are
        # correctly populated.
        if not self._query_results.complete:
            raise polling_future._OperationNotComplete()
        else:
            try:
                self.reload(retry=retry, timeout=transport_timeout)
            except exceptions.GoogleAPIError as exc:
                self.set_exception(exc)

    def result(
        self,
        page_size: int = None,
        max_results: int = None,
        retry: "retries.Retry" = DEFAULT_RETRY,
        timeout: float = None,
        start_index: int = None,
    ) -> Union["RowIterator", _EmptyRowIterator]:
        """Start the job and wait for it to complete and get the result.

        Args:
            page_size (Optional[int]):
                The maximum number of rows in each page of results from this
                request. Non-positive values are ignored.
            max_results (Optional[int]):
                The maximum total number of rows from this request.
            retry (Optional[google.api_core.retry.Retry]):
                How to retry the call that retrieves rows. If the job state is
                ``DONE``, retrying is aborted early even if the results are not
                available, as this will not change anymore.
            timeout (Optional[float]):
                The number of seconds to wait for the underlying HTTP transport
                before using ``retry``.
                If multiple requests are made under the hood, ``timeout``
                applies to each individual request.
            start_index (Optional[int]):
                The zero-based index of the starting row to read.

        Returns:
            google.cloud.bigquery.table.RowIterator:
                Iterator of row data
                :class:`~google.cloud.bigquery.table.Row`-s. During each
                page, the iterator will have the ``total_rows`` attribute
                set, which counts the total number of rows **in the result
                set** (this is distinct from the total number of rows in the
                current page: ``iterator.page.num_items``).

                If the query is a special query that produces no results, e.g.
                a DDL query, an ``_EmptyRowIterator`` instance is returned.

        Raises:
            google.cloud.exceptions.GoogleAPICallError:
                If the job failed.
            concurrent.futures.TimeoutError:
                If the job did not complete in the given timeout.
        """
        try:
            super(QueryJob, self).result(retry=retry, timeout=timeout)

            # Since the job could already be "done" (e.g. got a finished job
            # via client.get_job), the superclass call to done() might not
            # set the self._query_results cache.
            self._reload_query_results(retry=retry, timeout=timeout)
        except exceptions.GoogleAPICallError as exc:
            exc.message += self._format_for_exception(self.query, self.job_id)
            exc.query_job = self
            raise
        except requests.exceptions.Timeout as exc:
            raise concurrent.futures.TimeoutError from exc

        # If the query job is complete but there are no query results, this was
        # special job, such as a DDL query. Return an empty result set to
        # indicate success and avoid calling tabledata.list on a table which
        # can't be read (such as a view table).
        if self._query_results.total_rows is None:
            return _EmptyRowIterator()

        rows = self._client._list_rows_from_query_results(
            self.job_id,
            self.location,
            self.project,
            self._query_results.schema,
            total_rows=self._query_results.total_rows,
            destination=self.destination,
            page_size=page_size,
            max_results=max_results,
            start_index=start_index,
            retry=retry,
            timeout=timeout,
        )
        rows._preserve_order = _contains_order_by(self.query)
        return rows

    # If changing the signature of this method, make sure to apply the same
    # changes to table.RowIterator.to_arrow()
    def to_arrow(
        self,
        progress_bar_type: str = None,
        bqstorage_client: "bigquery_storage.BigQueryReadClient" = None,
        create_bqstorage_client: bool = True,
    ) -> "pyarrow.Table":
        """[Beta] Create a class:`pyarrow.Table` by loading all pages of a
        table or query.

        Args:
            progress_bar_type (Optional[str]):
                If set, use the `tqdm <https://tqdm.github.io/>`_ library to
                display a progress bar while the data downloads. Install the
                ``tqdm`` package to use this feature.

                Possible values of ``progress_bar_type`` include:

                ``None``
                  No progress bar.
                ``'tqdm'``
                  Use the :func:`tqdm.tqdm` function to print a progress bar
                  to :data:`sys.stderr`.
                ``'tqdm_notebook'``
                  Use the :func:`tqdm.tqdm_notebook` function to display a
                  progress bar as a Jupyter notebook widget.
                ``'tqdm_gui'``
                  Use the :func:`tqdm.tqdm_gui` function to display a
                  progress bar as a graphical dialog box.
            bqstorage_client (Optional[google.cloud.bigquery_storage_v1.BigQueryReadClient]):
                A BigQuery Storage API client. If supplied, use the faster
                BigQuery Storage API to fetch rows from BigQuery. This API
                is a billable API.

                This method requires the ``pyarrow`` and
                ``google-cloud-bigquery-storage`` libraries.

                Reading from a specific partition or snapshot is not
                currently supported by this method.
            create_bqstorage_client (Optional[bool]):
                If ``True`` (default), create a BigQuery Storage API client
                using the default API settings. The BigQuery Storage API
                is a faster way to fetch rows from BigQuery. See the
                ``bqstorage_client`` parameter for more information.

                This argument does nothing if ``bqstorage_client`` is supplied.

                ..versionadded:: 1.24.0

        Returns:
            pyarrow.Table
                A :class:`pyarrow.Table` populated with row data and column
                headers from the query results. The column headers are derived
                from the destination table's schema.

        Raises:
            ValueError:
                If the :mod:`pyarrow` library cannot be imported.

        ..versionadded:: 1.17.0
        """
        query_result = wait_for_query(self, progress_bar_type)
        return query_result.to_arrow(
            progress_bar_type=progress_bar_type,
            bqstorage_client=bqstorage_client,
            create_bqstorage_client=create_bqstorage_client,
        )

    # If changing the signature of this method, make sure to apply the same
    # changes to table.RowIterator.to_dataframe()
    def to_dataframe(
        self,
        bqstorage_client: "bigquery_storage.BigQueryReadClient" = None,
        dtypes: Dict[str, Any] = None,
        progress_bar_type: str = None,
        create_bqstorage_client: bool = True,
        date_as_object: bool = True,
    ) -> "pandas.DataFrame":
        """Return a pandas DataFrame from a QueryJob

        Args:
            bqstorage_client (Optional[google.cloud.bigquery_storage_v1.BigQueryReadClient]):
                A BigQuery Storage API client. If supplied, use the faster
                BigQuery Storage API to fetch rows from BigQuery. This
                API is a billable API.

                This method requires the ``fastavro`` and
                ``google-cloud-bigquery-storage`` libraries.

                Reading from a specific partition or snapshot is not
                currently supported by this method.

            dtypes (Optional[Map[str, Union[str, pandas.Series.dtype]]]):
                A dictionary of column names pandas ``dtype``s. The provided
                ``dtype`` is used when constructing the series for the column
                specified. Otherwise, the default pandas behavior is used.

            progress_bar_type (Optional[str]):
                If set, use the `tqdm <https://tqdm.github.io/>`_ library to
                display a progress bar while the data downloads. Install the
                ``tqdm`` package to use this feature.

                See
                :func:`~google.cloud.bigquery.table.RowIterator.to_dataframe`
                for details.

                ..versionadded:: 1.11.0
            create_bqstorage_client (Optional[bool]):
                If ``True`` (default), create a BigQuery Storage API client
                using the default API settings. The BigQuery Storage API
                is a faster way to fetch rows from BigQuery. See the
                ``bqstorage_client`` parameter for more information.

                This argument does nothing if ``bqstorage_client`` is supplied.

                ..versionadded:: 1.24.0

            date_as_object (Optional[bool]):
                If ``True`` (default), cast dates to objects. If ``False``, convert
                to datetime64[ns] dtype.

                ..versionadded:: 1.26.0

        Returns:
            A :class:`~pandas.DataFrame` populated with row data and column
            headers from the query results. The column headers are derived
            from the destination table's schema.

        Raises:
            ValueError: If the `pandas` library cannot be imported.
        """
        query_result = wait_for_query(self, progress_bar_type)
        return query_result.to_dataframe(
            bqstorage_client=bqstorage_client,
            dtypes=dtypes,
            progress_bar_type=progress_bar_type,
            create_bqstorage_client=create_bqstorage_client,
            date_as_object=date_as_object,
        )

    def __iter__(self):
        return iter(self.result())


class QueryPlanEntryStep(object):
    """Map a single step in a query plan entry.

    Args:
        kind (str): step type.
        substeps (List): names of substeps.
    """

    def __init__(self, kind, substeps):
        self.kind = kind
        self.substeps = list(substeps)

    @classmethod
    def from_api_repr(cls, resource: dict) -> "QueryPlanEntryStep":
        """Factory: construct instance from the JSON repr.

        Args:
            resource (Dict): JSON representation of the entry.

        Returns:
            google.cloud.bigquery.job.QueryPlanEntryStep:
                New instance built from the resource.
        """
        return cls(kind=resource.get("kind"), substeps=resource.get("substeps", ()))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.kind == other.kind and self.substeps == other.substeps


class QueryPlanEntry(object):
    """QueryPlanEntry represents a single stage of a query execution plan.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#ExplainQueryStage
    for the underlying API representation within query statistics.
    """

    def __init__(self):
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource: dict) -> "QueryPlanEntry":
        """Factory: construct instance from the JSON repr.

        Args:
            resource(Dict[str: object]):
                ExplainQueryStage representation returned from API.

        Returns:
            google.cloud.bigquery.job.QueryPlanEntry:
                Query plan entry parsed from ``resource``.
        """
        entry = cls()
        entry._properties = resource
        return entry

    @property
    def name(self):
        """Optional[str]: Human-readable name of the stage."""
        return self._properties.get("name")

    @property
    def entry_id(self):
        """Optional[str]: Unique ID for the stage within the plan."""
        return self._properties.get("id")

    @property
    def start(self):
        """Optional[Datetime]: Datetime when the stage started."""
        if self._properties.get("startMs") is None:
            return None
        return _helpers._datetime_from_microseconds(
            int(self._properties.get("startMs")) * 1000.0
        )

    @property
    def end(self):
        """Optional[Datetime]: Datetime when the stage ended."""
        if self._properties.get("endMs") is None:
            return None
        return _helpers._datetime_from_microseconds(
            int(self._properties.get("endMs")) * 1000.0
        )

    @property
    def input_stages(self):
        """List(int): Entry IDs for stages that were inputs for this stage."""
        if self._properties.get("inputStages") is None:
            return []
        return [
            _helpers._int_or_none(entry)
            for entry in self._properties.get("inputStages")
        ]

    @property
    def parallel_inputs(self):
        """Optional[int]: Number of parallel input segments within
        the stage.
        """
        return _helpers._int_or_none(self._properties.get("parallelInputs"))

    @property
    def completed_parallel_inputs(self):
        """Optional[int]: Number of parallel input segments completed."""
        return _helpers._int_or_none(self._properties.get("completedParallelInputs"))

    @property
    def wait_ms_avg(self):
        """Optional[int]: Milliseconds the average worker spent waiting to
        be scheduled.
        """
        return _helpers._int_or_none(self._properties.get("waitMsAvg"))

    @property
    def wait_ms_max(self):
        """Optional[int]: Milliseconds the slowest worker spent waiting to
        be scheduled.
        """
        return _helpers._int_or_none(self._properties.get("waitMsMax"))

    @property
    def wait_ratio_avg(self):
        """Optional[float]: Ratio of time the average worker spent waiting
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get("waitRatioAvg")

    @property
    def wait_ratio_max(self):
        """Optional[float]: Ratio of time the slowest worker spent waiting
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get("waitRatioMax")

    @property
    def read_ms_avg(self):
        """Optional[int]: Milliseconds the average worker spent reading
        input.
        """
        return _helpers._int_or_none(self._properties.get("readMsAvg"))

    @property
    def read_ms_max(self):
        """Optional[int]: Milliseconds the slowest worker spent reading
        input.
        """
        return _helpers._int_or_none(self._properties.get("readMsMax"))

    @property
    def read_ratio_avg(self):
        """Optional[float]: Ratio of time the average worker spent reading
        input, relative to the longest time spent by any worker in any stage
        of the overall plan.
        """
        return self._properties.get("readRatioAvg")

    @property
    def read_ratio_max(self):
        """Optional[float]: Ratio of time the slowest worker spent reading
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get("readRatioMax")

    @property
    def compute_ms_avg(self):
        """Optional[int]: Milliseconds the average worker spent on CPU-bound
        processing.
        """
        return _helpers._int_or_none(self._properties.get("computeMsAvg"))

    @property
    def compute_ms_max(self):
        """Optional[int]: Milliseconds the slowest worker spent on CPU-bound
        processing.
        """
        return _helpers._int_or_none(self._properties.get("computeMsMax"))

    @property
    def compute_ratio_avg(self):
        """Optional[float]: Ratio of time the average worker spent on
        CPU-bound processing, relative to the longest time spent by any
        worker in any stage of the overall plan.
        """
        return self._properties.get("computeRatioAvg")

    @property
    def compute_ratio_max(self):
        """Optional[float]: Ratio of time the slowest worker spent on
        CPU-bound processing, relative to the longest time spent by any
        worker in any stage of the overall plan.
        """
        return self._properties.get("computeRatioMax")

    @property
    def write_ms_avg(self):
        """Optional[int]: Milliseconds the average worker spent writing
        output data.
        """
        return _helpers._int_or_none(self._properties.get("writeMsAvg"))

    @property
    def write_ms_max(self):
        """Optional[int]: Milliseconds the slowest worker spent writing
        output data.
        """
        return _helpers._int_or_none(self._properties.get("writeMsMax"))

    @property
    def write_ratio_avg(self):
        """Optional[float]: Ratio of time the average worker spent writing
        output data, relative to the longest time spent by any worker in any
        stage of the overall plan.
        """
        return self._properties.get("writeRatioAvg")

    @property
    def write_ratio_max(self):
        """Optional[float]: Ratio of time the slowest worker spent writing
        output data, relative to the longest time spent by any worker in any
        stage of the overall plan.
        """
        return self._properties.get("writeRatioMax")

    @property
    def records_read(self):
        """Optional[int]: Number of records read by this stage."""
        return _helpers._int_or_none(self._properties.get("recordsRead"))

    @property
    def records_written(self):
        """Optional[int]: Number of records written by this stage."""
        return _helpers._int_or_none(self._properties.get("recordsWritten"))

    @property
    def status(self):
        """Optional[str]: status of this stage."""
        return self._properties.get("status")

    @property
    def shuffle_output_bytes(self):
        """Optional[int]: Number of bytes written by this stage to
        intermediate shuffle.
        """
        return _helpers._int_or_none(self._properties.get("shuffleOutputBytes"))

    @property
    def shuffle_output_bytes_spilled(self):
        """Optional[int]: Number of bytes written by this stage to
        intermediate shuffle and spilled to disk.
        """
        return _helpers._int_or_none(self._properties.get("shuffleOutputBytesSpilled"))

    @property
    def steps(self):
        """List(QueryPlanEntryStep): List of step operations performed by
        each worker in the stage.
        """
        return [
            QueryPlanEntryStep.from_api_repr(step)
            for step in self._properties.get("steps", [])
        ]


class TimelineEntry(object):
    """TimelineEntry represents progress of a query job at a particular
    point in time.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#querytimelinesample
    for the underlying API representation within query statistics.
    """

    def __init__(self):
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct instance from the JSON repr.

        Args:
            resource(Dict[str: object]):
                QueryTimelineSample representation returned from API.

        Returns:
            google.cloud.bigquery.TimelineEntry:
                Timeline sample parsed from ``resource``.
        """
        entry = cls()
        entry._properties = resource
        return entry

    @property
    def elapsed_ms(self):
        """Optional[int]: Milliseconds elapsed since start of query
        execution."""
        return _helpers._int_or_none(self._properties.get("elapsedMs"))

    @property
    def active_units(self):
        """Optional[int]: Current number of input units being processed
        by workers, reported as largest value since the last sample."""
        return _helpers._int_or_none(self._properties.get("activeUnits"))

    @property
    def pending_units(self):
        """Optional[int]: Current number of input units remaining for
        query stages active at this sample time."""
        return _helpers._int_or_none(self._properties.get("pendingUnits"))

    @property
    def completed_units(self):
        """Optional[int]: Current number of input units completed by
        this query."""
        return _helpers._int_or_none(self._properties.get("completedUnits"))

    @property
    def slot_millis(self):
        """Optional[int]: Cumulative slot-milliseconds consumed by
        this query."""
        return _helpers._int_or_none(self._properties.get("totalSlotMs"))
