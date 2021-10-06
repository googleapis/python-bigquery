# Copyright 2021 Google LLC
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

import concurrent.futures
import datetime
import decimal

import pytest

from google.cloud import bigquery
from google.cloud.bigquery.query import ScalarQueryParameter

# from google.cloud.bigquery.query import ArrayQueryParameter
# from google.cloud.bigquery.query import ScalarQueryParameterType
# from google.cloud.bigquery.query import StructQueryParameter
# from google.cloud.bigquery.query import StructQueryParameterType


@pytest.fixture(params=["INSERT", "QUERY"])
def query_api_method(request):
    return request.param


@pytest.fixture(scope="session")
def table_with_9999_columns_10_rows(bigquery_client, project_id, dataset_id):
    """Generate a table of maximum width via CREATE TABLE AS SELECT.

    The first column is named 'rowval', and has a value from 1..rowcount
    Subsequent columns are named col_<N> and contain the value N*rowval, where
    N is between 1 and 9999 inclusive.
    """
    table_id = "many_columns"
    row_count = 10
    col_projections = ",".join([f"r * {n} as col_{n}" for n in range(1, 10000)])
    sql = f"""
    CREATE TABLE `{project_id}.{dataset_id}.{table_id}`
    AS
    SELECT
        r as rowval,
        {col_projections}
    FROM
      UNNEST(GENERATE_ARRAY(1,{row_count},1)) as r
    """
    query_job = bigquery_client.query(sql)
    query_job.result()

    return f"{project_id}.{dataset_id}.{table_id}"


def test_query_many_columns(
    bigquery_client, table_with_9999_columns_10_rows, query_api_method
):
    # Test working with the widest schema BigQuery supports, 10k columns.
    query_job = bigquery_client.query(
        f"SELECT * FROM `{table_with_9999_columns_10_rows}`",
        api_method=query_api_method,
    )
    rows = list(query_job)
    assert len(rows) == 10

    # check field representations adhere to expected values.
    for row in rows:
        rowval = row["rowval"]
        for column in range(1, 10000):
            assert row[f"col_{column}"] == rowval * column


def test_query_w_timeout(bigquery_client, query_api_method):
    job_config = bigquery.QueryJobConfig()
    job_config.use_query_cache = False

    query_job = bigquery_client.query(
        "SELECT * FROM `bigquery-public-data.github_repos.commits`;",
        location="US",
        job_config=job_config,
        api_method=query_api_method,
    )

    with pytest.raises(concurrent.futures.TimeoutError):
        query_job.result(timeout=1)

    # Even though the query takes >1 second, the call to getQueryResults
    # should succeed.
    assert not query_job.done(timeout=1)
    assert bigquery_client.cancel_job(query_job) is not None


def test_query_statistics(bigquery_client, query_api_method):
    """
    A system test to exercise some of the extended query statistics.

    Note:  We construct a query that should need at least three stages by
    specifying a JOIN query.  Exact plan and stats are effectively
    non-deterministic, so we're largely interested in confirming values
    are present.
    """

    job_config = bigquery.QueryJobConfig()
    job_config.use_query_cache = False

    query_job = bigquery_client.query(
        """
        SELECT
          COUNT(1)
        FROM
        (
          SELECT
            year,
            wban_number
          FROM `bigquery-public-data.samples.gsod`
          LIMIT 1000
        ) lside
        INNER JOIN
        (
          SELECT
            year,
            state
          FROM `bigquery-public-data.samples.natality`
          LIMIT 1000
        ) rside
        ON
        lside.year = rside.year
        """,
        location="US",
        job_config=job_config,
        api_method=query_api_method,
    )

    # run the job to completion
    query_job.result()

    # Must reload job to get stats if jobs.query was used.
    if query_api_method == "QUERY":
        query_job.reload()

    # Assert top-level stats
    assert not query_job.cache_hit
    assert query_job.destination is not None
    assert query_job.done
    assert not query_job.dry_run
    assert query_job.num_dml_affected_rows is None
    assert query_job.priority == "INTERACTIVE"
    assert query_job.total_bytes_billed > 1
    assert query_job.total_bytes_processed > 1
    assert query_job.statement_type == "SELECT"
    assert query_job.slot_millis > 1

    # Make assertions on the shape of the query plan.
    plan = query_job.query_plan
    assert len(plan) >= 3
    first_stage = plan[0]
    assert first_stage.start is not None
    assert first_stage.end is not None
    assert first_stage.entry_id is not None
    assert first_stage.name is not None
    assert first_stage.parallel_inputs > 0
    assert first_stage.completed_parallel_inputs > 0
    assert first_stage.shuffle_output_bytes > 0
    assert first_stage.status == "COMPLETE"

    # Query plan is a digraph.  Ensure it has inter-stage links,
    # but not every stage has inputs.
    stages_with_inputs = 0
    for entry in plan:
        if len(entry.input_stages) > 0:
            stages_with_inputs = stages_with_inputs + 1
    assert stages_with_inputs > 0
    assert len(plan) > stages_with_inputs


@pytest.mark.parametrize(
    ("sql", "expected", "query_parameters"),
    (
        (
            "SELECT @question",
            "What is the answer to life, the universe, and everything?",
            [
                ScalarQueryParameter(
                    name="question",
                    type_="STRING",
                    value="What is the answer to life, the universe, and everything?",
                )
            ],
        ),
        (
            "SELECT @answer",
            42,
            [ScalarQueryParameter(name="answer", type_="INT64", value=42)],
        ),
        (
            "SELECT @pi",
            3.1415926,
            [ScalarQueryParameter(name="pi", type_="FLOAT64", value=3.1415926)],
        ),
        (
            "SELECT @pi_numeric_param",
            decimal.Decimal("3.141592654"),
            [
                ScalarQueryParameter(
                    name="pi_numeric_param",
                    type_="NUMERIC",
                    value=decimal.Decimal("3.141592654"),
                )
            ],
        ),
        (
            "SELECT @bignum_param",
            decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
            [
                ScalarQueryParameter(
                    name="bignum_param",
                    type_="BIGNUMERIC",
                    value=decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
                )
            ],
        ),
        (
            "SELECT @truthy",
            True,
            [ScalarQueryParameter(name="truthy", type_="BOOL", value=True)],
        ),
        (
            "SELECT @beef",
            b"DEADBEEF",
            [ScalarQueryParameter(name="beef", type_="BYTES", value=b"DEADBEEF")],
        ),
        (
            "SELECT @naive",
            datetime.datetime(2016, 12, 5, 12, 41, 9),
            [
                ScalarQueryParameter(
                    name="naive",
                    type_="DATETIME",
                    value=datetime.datetime(2016, 12, 5, 12, 41, 9),
                )
            ],
        ),
        (
            "SELECT @naive_date",
            datetime.date(2016, 12, 5),
            [
                ScalarQueryParameter(
                    name="naive_date", type_="DATE", value=datetime.date(2016, 12, 5)
                )
            ],
        ),
        (
            "SELECT @naive_time",
            datetime.time(12, 41, 9, 62500),
            [
                ScalarQueryParameter(
                    name="naive_time",
                    type_="TIME",
                    value=datetime.time(12, 41, 9, 62500),
                )
            ],
        ),
        (
            "SELECT @zoned",
            datetime.datetime(2016, 12, 5, 12, 41, 9, tzinfo=datetime.timezone.utc),
            [
                ScalarQueryParameter(
                    name="zoned",
                    type_="TIMESTAMP",
                    value=datetime.datetime(
                        2016, 12, 5, 12, 41, 9, tzinfo=datetime.timezone.utc
                    ),
                )
            ],
        ),
        # (
        #    "SELECT @array_param",
        #    [1, 2],
        #    [array_param],
        # ),
        # (
        #    "SELECT (@hitchhiker.question, @hitchhiker.answer)",
        #    ({"_field_1": question, "_field_2": answer}),
        #    [struct_param],
        # ),
        # (
        #    "SELECT "
        #    "((@rectangle.bottom_right.x - @rectangle.top_left.x) "
        #    "* (@rectangle.top_left.y - @rectangle.bottom_right.y))",
        #    100,
        #    [rectangle_param],
        # ),
        # (
        #    "SELECT ?",
        #    [
        #        {"name": phred_name, "age": phred_age},
        #        {"name": bharney_name, "age": bharney_age},
        #    ],
        #    [characters_param],
        # ),
        # (
        #    "SELECT @empty_array_param",
        #    [],
        #    [empty_struct_array_param],
        # ),
        # (
        #    "SELECT @roles",
        #    (
        #        "hero": {"name": phred_name, "age": phred_age},
        #        "sidekick": {"name": bharney_name, "age": bharney_age},
        #    ),
        #    [roles_param],
        # ),
        # (
        #    "SELECT ?",
        #    {"friends": [phred_name, bharney_name]},
        #    [with_friends_param],
        # ),
        # (
        #    "SELECT @bignum_param",
        #    bignum,
        #    [bignum_param],
        # ),
    ),
)
def test_query_parameters(
    bigquery_client, query_api_method, sql, expected, query_parameters
):
    # array_param = ArrayQueryParameter(
    #    name="array_param", array_type="INT64", values=[1, 2]
    # )
    # struct_param = StructQueryParameter("hitchhiker", question_param, answer_param)
    # phred_name = "Phred Phlyntstone"
    # phred_name_param = ScalarQueryParameter(
    #    name="name", type_="STRING", value=phred_name
    # )
    # phred_age = 32
    # phred_age_param = ScalarQueryParameter(
    #    name="age", type_="INT64", value=phred_age
    # )
    # phred_param = StructQueryParameter(None, phred_name_param, phred_age_param)
    # bharney_name = "Bharney Rhubbyl"
    # bharney_name_param = ScalarQueryParameter(
    #    name="name", type_="STRING", value=bharney_name
    # )
    # bharney_age = 31
    # bharney_age_param = ScalarQueryParameter(
    #    name="age", type_="INT64", value=bharney_age
    # )
    # bharney_param = StructQueryParameter(
    #    None, bharney_name_param, bharney_age_param
    # )
    # characters_param = ArrayQueryParameter(
    #    name=None, array_type="RECORD", values=[phred_param, bharney_param]
    # )
    # empty_struct_array_param = ArrayQueryParameter(
    #    name="empty_array_param",
    #    values=[],
    #    array_type=StructQueryParameterType(
    #        ScalarQueryParameterType(name="foo", type_="INT64"),
    #        ScalarQueryParameterType(name="bar", type_="STRING"),
    #    ),
    # )
    # hero_param = StructQueryParameter("hero", phred_name_param, phred_age_param)
    # sidekick_param = StructQueryParameter(
    #    "sidekick", bharney_name_param, bharney_age_param
    # )
    # roles_param = StructQueryParameter("roles", hero_param, sidekick_param)
    # friends_param = ArrayQueryParameter(
    #    name="friends", array_type="STRING", values=[phred_name, bharney_name]
    # )
    # with_friends_param = StructQueryParameter(None, friends_param)
    # top_left_param = StructQueryParameter(
    #    "top_left",
    #    ScalarQueryParameter("x", "INT64", 12),
    #    ScalarQueryParameter("y", "INT64", 102),
    # )
    # bottom_right_param = StructQueryParameter(
    #    "bottom_right",
    #    ScalarQueryParameter("x", "INT64", 22),
    #    ScalarQueryParameter("y", "INT64", 92),
    # )
    # rectangle_param = StructQueryParameter(
    #    "rectangle", top_left_param, bottom_right_param
    # )

    jconfig = bigquery.QueryJobConfig()
    jconfig.query_parameters = query_parameters
    query_job = bigquery_client.query(
        sql, job_config=jconfig, api_method=query_api_method,
    )
    rows = list(query_job.result())
    assert len(rows) == 1
    assert len(rows[0]) == 1
    assert rows[0][0] == expected
