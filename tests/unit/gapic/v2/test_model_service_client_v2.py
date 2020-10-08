# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Unit tests."""

import mock
import pytest

from google.cloud import bigquery_v2
from google.cloud.bigquery_v2.proto import model_pb2
from google.protobuf import empty_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestModelServiceClient(object):
    def test_get_model(self):
        # Setup Expected Response
        etag = "etag3123477"
        creation_time = 1932333101
        last_modified_time = 671513446
        description = "description-1724546052"
        friendly_name = "friendlyName1451097503"
        expiration_time = 767170141
        location = "location1901043637"
        expected_response = {
            "etag": etag,
            "creation_time": creation_time,
            "last_modified_time": last_modified_time,
            "description": description,
            "friendly_name": friendly_name,
            "expiration_time": expiration_time,
            "location": location,
        }
        expected_response = model_pb2.Model(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"

        response = client.get_model(project_id, dataset_id, model_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = model_pb2.GetModelRequest(
            project_id=project_id, dataset_id=dataset_id, model_id=model_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"

        with pytest.raises(CustomException):
            client.get_model(project_id, dataset_id, model_id)

    def test_list_models(self):
        # Setup Expected Response
        next_page_token = "nextPageToken-1530815211"
        expected_response = {"next_page_token": next_page_token}
        expected_response = model_pb2.ListModelsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"

        response = client.list_models(project_id, dataset_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = model_pb2.ListModelsRequest(
            project_id=project_id, dataset_id=dataset_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_models_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"

        with pytest.raises(CustomException):
            client.list_models(project_id, dataset_id)

    def test_patch_model(self):
        # Setup Expected Response
        etag = "etag3123477"
        creation_time = 1932333101
        last_modified_time = 671513446
        description = "description-1724546052"
        friendly_name = "friendlyName1451097503"
        expiration_time = 767170141
        location = "location1901043637"
        expected_response = {
            "etag": etag,
            "creation_time": creation_time,
            "last_modified_time": last_modified_time,
            "description": description,
            "friendly_name": friendly_name,
            "expiration_time": expiration_time,
            "location": location,
        }
        expected_response = model_pb2.Model(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"
        model = {}

        response = client.patch_model(project_id, dataset_id, model_id, model)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = model_pb2.PatchModelRequest(
            project_id=project_id, dataset_id=dataset_id, model_id=model_id, model=model
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_patch_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"
        model = {}

        with pytest.raises(CustomException):
            client.patch_model(project_id, dataset_id, model_id, model)

    def test_delete_model(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"

        client.delete_model(project_id, dataset_id, model_id)

        assert len(channel.requests) == 1
        expected_request = model_pb2.DeleteModelRequest(
            project_id=project_id, dataset_id=dataset_id, model_id=model_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_model_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigquery_v2.ModelServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        dataset_id = "datasetId-2115646910"
        model_id = "modelId-619038223"

        with pytest.raises(CustomException):
            client.delete_model(project_id, dataset_id, model_id)
