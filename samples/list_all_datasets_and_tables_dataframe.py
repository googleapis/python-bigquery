# Copyright 2022 Cedarwood Insights Limited
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

import typing

if typing.TYPE_CHECKING:
    import pandas

def list_all_datasets_and_tables_df() -> "pandas.DataFrame":
    """
    List all Datasets and Tables for a GCP Project
    Return the results in a Pandas DataFrame
    """
    # [START bigquery_list_all_datasets_and_tables]

    import pandas
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()
    project = client.project

    # Create empty Python lists
    dataset_list = []
    final_table_list = []

    # Grab the Datasets for the Project
    datasets = list(client.list_datasets())  # Make an API request.

    if datasets:

        # Generate Python list of datasets
        for dataset in datasets:
            dataset_list.append(dataset.dataset_id)
        print (dataset_list)

        # Grab the Tables for the Dataset
        for dataset_id in dataset_list:
            full_dataset_id = f"{project}.{dataset_id}"
            tables = list(client.list_tables(full_dataset_id))  # Make an API request.

            if tables:

                for table in tables:
                    # Create dictionary for each table
                    table_dict = {
                        'project_id': table.project,
                        'dataset_id': table.dataset_id,
                        'table_id': table.table_id}
                    # Append dictionary to final table list
                    final_table_list.append(table_dict)

            else:
                table_dict = {
                    'project_id': project,
                    'dataset_id': dataset_id,
                    'table_id': '[NO TABLES]'}
                # Append dictionary to final table list
                final_table_list.append(table_dict)

    else:
        table_dict = {
            'project_id': project,
            'dataset_id': '[NO DATASETS]',
            'table_id': '[NO TABLES]'}
        # Append dictionary to final table list
        final_table_list.append(table_dict)

    # Load resulting list of tables into a dataframe
    dataset_tables_df = pandas.DataFrame(final_table_list)
    print("Datasets and Tables in project {}:".format(project))
    print (dataset_tables_df)

    # [END bigquery_list_all_datasets_and_tables]
    return dataset_tables_df
