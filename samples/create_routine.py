# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def create_routine(routine_id):

    # [START bigquery_create_routine]
    from google.cloud import bigquery
    from google.cloud import bigquery_v2

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Choose a fully-qualified ID for the routine.
    # routine_id = "my-project.my_dataset.my_routine"

    routine = bigquery.Routine(
        routine_id,
        type_="SCALAR_FUNCTION",
        language="SQL",
        body="x * 3",
        arguments=[
            bigquery.RoutineArgument(
                name="x",
                data_type=bigquery_v2.types.StandardSqlDataType(
                    type_kind=bigquery_v2.types.StandardSqlDataType.TypeKind.INT64
                ),
            )
        ],
    )

    routine = client.create_routine(routine)  # Make an API request.

    print("Created routine {}".format(routine.reference))
    # [END bigquery_create_routine]
    return routine
