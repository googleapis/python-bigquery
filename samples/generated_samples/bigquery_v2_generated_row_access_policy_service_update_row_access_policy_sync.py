# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for UpdateRowAccessPolicy
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-bigquery


# [START bigquery_v2_generated_RowAccessPolicyService_UpdateRowAccessPolicy_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import bigquery_v2


def sample_update_row_access_policy():
    # Create a client
    client = bigquery_v2.RowAccessPolicyServiceClient()

    # Initialize request argument(s)
    row_access_policy = bigquery_v2.RowAccessPolicy()
    row_access_policy.row_access_policy_reference.project_id = "project_id_value"
    row_access_policy.row_access_policy_reference.dataset_id = "dataset_id_value"
    row_access_policy.row_access_policy_reference.table_id = "table_id_value"
    row_access_policy.row_access_policy_reference.policy_id = "policy_id_value"
    row_access_policy.filter_predicate = "filter_predicate_value"

    request = bigquery_v2.UpdateRowAccessPolicyRequest(
        project_id="project_id_value",
        dataset_id="dataset_id_value",
        table_id="table_id_value",
        policy_id="policy_id_value",
        row_access_policy=row_access_policy,
    )

    # Make the request
    response = client.update_row_access_policy(request=request)

    # Handle the response
    print(response)


# [END bigquery_v2_generated_RowAccessPolicyService_UpdateRowAccessPolicy_sync]
