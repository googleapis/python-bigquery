<!--
Copyright 2020 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# 3.0.0 Migration Guide

## New Required Dependencies

Some of the previously optional dependencies are now *required* in `3.x` versions of the
library, namely
[google-cloud-bigquery-storage](https://pypi.org/project/google-cloud-bigquery-storage/)
(minimum version `2.0.0`) and [pyarrow](https://pypi.org/project/pyarrow/) (minimum
version `3.0.0`).

The behavior of some of the package "extras" has thus also changed:
 * The `pandas` extra now requires the [db-types](https://pypi.org/project/db-dtypes/)
   package.
 * The `bqstorage` extra has been preserved for comaptibility reasons, but it is now a
   no-op and should be omitted when installing the BigQuery client library.

   **Before:**
   ```
   $ pip install google-cloud-bigquery[bqstorage]
   ```

   **After:**
   ```
   $ pip install google-cloud-bigquery
   ```

 * The `bignumeric_type` extra has been removed, as `BIGNUMERIC` type is now
   automatically supported. That extra should thus not be used.

   **Before:**
   ```
   $ pip install google-cloud-bigquery[bignumeric_type]
   ```

   **After:**
   ```
   $ pip install google-cloud-bigquery
   ```

## Re-organized Types

The auto-generated parts of the library has been removed, and proto-based types formerly
found in `google.cloud.bigquery_v2` have been replaced by the new implementation (but
see the [section](#legacy-types) below).

For example, the standard SQL data types should new be imported from a new location:

**Before:**
```py
from google.cloud.bigquery_v2 import StandardSqlDataType
from google.cloud.bigquery_v2.types import StandardSqlField
from google.cloud.bigquery_v2.types.standard_sql import StandardSqlStructType
```

**After:**
```py
from google.cloud.bigquery import StandardSqlDataType
from google.cloud.bigquery.standard_sql import StandardSqlField
from google.cloud.bigquery.standard_sql import StandardSqlStructType
```

The `TypeKind` enum defining all possible SQL types for schema fields has been renamed
and is not nested anymore under `StandardSqlDataType`:


**Before:**
```py
from google.cloud.bigquery_v2 import StandardSqlDataType

if field_type == StandardSqlDataType.TypeKind.STRING:
    ...
```

**After:**
```py

from google.cloud.bigquery import StandardSqlTypeNames

if field_type == StandardSqlTypeNames.STRING:
    ...
```


<a name="legacy-types"></a>
## Legacy Types

For compatibility reasons, the legacy proto-based types still exists as static code
and can be imported:

```py
from google.cloud.bigquery_v2 import StandardSqlDataType  # a sublcass of proto.Message
```

Mind, however, that importing them will issue a warning, because aside from being
importable, these types **are not maintained anymore** in any way. They may differ both
from the types in `google.cloud.bigquery`, and from the types supported on the backend.

Unless you have a very specific situation that warrants using them, you should instead
use the actively maintained types from `google.cloud.bigquery`.


## Destination Table is Preserved on Query Jobs

When the BigQuery client creates a `QueryJob`, it no longer removes the destination
table from the job's configuration. Destination table for the query can thus be
explicitly defined by the user.


## Changed Default Inferred Type for Naive `datetime` Instances.

In the absence of schema information, columns with naive `datetime.datetime` values,
i.e. without timezone information, are recognized and loaded using the `DATETIME` type.
On the other hand, for columns with timezone-aware `datetime.dateime` values, the
`TIMESTAMP` type is continued to be used.


## Destination Table is Preserved on Query Jobs

When the BigQuery client creates a `QueryJob`, it no longer removes the destination
table from the job's configuration. Destination table for the query can thus be
explicitly defined by the user.


## Type Annotations

The library is now type-annotated and declares itself as such. If you use a static
type checker such as `mypy`, you might start getting errors in places where
`google-cloud-bigquery` package is used.

It is recommended to update your code and/or type annotations to fix these errors, but
if this is not feasible in the short term, you can temporarily ignore type annotations
in `google-cloud-bigquery`, for example by using a special `# type: ignore` comment:

```py
from google.cloud import bigquery  # type: ignore
```

But again, this is only recommended as a possible short-term workaround if immediately
fixing the type check errors in your project is not feasible.


# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-bigquery` client drops support for Python
versions below 3.6. The client surface itself has not changed, but the 1.x series
will not be receiving any more feature updates or bug fixes. You are thus
encouraged to upgrade to the 2.x series.

If you experience issues or have questions, please file an
[issue](https://github.com/googleapis/python-bigquery/issues).


## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Supported BigQuery Storage Clients

The 2.0.0 release requires BigQuery Storage `>= 2.0.0`, which dropped support
for `v1beta1` and `v1beta2` versions of the BigQuery Storage API. If you want to
use a BigQuery Storage client, it must be the one supporting the `v1` API version.


## Changed GAPIC Enums Path

> **WARNING**: Breaking change

Generated GAPIC enum types have been moved under `types`. Import paths need to be
adjusted.

**Before:**
```py
from google.cloud.bigquery_v2.gapic import enums

distance_type = enums.Model.DistanceType.COSINE
```

**After:**
```py
from google.cloud.bigquery_v2 import types

distance_type = types.Model.DistanceType.COSINE
```
