# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

import mock

try:
    from google.cloud import bigquery_storage_v1beta1
except ImportError:  # pragma: NO COVER
    bigquery_storage_v1beta1 = None


class TestConnection(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dbapi import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _mock_client(self):
        from google.cloud.bigquery import client

        mock_client = mock.create_autospec(client.Client)
        return mock_client

    def _mock_bqstorage_client(self):
        from google.cloud.bigquery_storage_v1beta1 import client

        mock_client = mock.create_autospec(client.BigQueryStorageClient)
        return mock_client

    def test_ctor_wo_bqstorage_client(self):
        from google.cloud.bigquery.dbapi import Connection

        mock_client = self._mock_client()
        connection = self._make_one(client=mock_client)
        self.assertIsInstance(connection, Connection)
        self.assertIs(connection._client, mock_client)
        self.assertIsNone(connection._bqstorage_client)

    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_ctor_w_bqstorage_client(self):
        from google.cloud.bigquery.dbapi import Connection

        mock_client = self._mock_client()
        mock_bqstorage_client = self._mock_bqstorage_client()
        connection = self._make_one(
            client=mock_client, bqstorage_client=mock_bqstorage_client,
        )
        self.assertIsInstance(connection, Connection)
        self.assertIs(connection._client, mock_client)
        self.assertIs(connection._bqstorage_client, mock_bqstorage_client)

    @mock.patch("google.cloud.bigquery.Client", autospec=True)
    def test_connect_wo_client(self, mock_client):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import Connection

        connection = connect()
        self.assertIsInstance(connection, Connection)
        self.assertIsNotNone(connection._client)
        self.assertIsNone(connection._bqstorage_client)

    def test_connect_w_client(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import Connection

        mock_client = self._mock_client()
        connection = connect(client=mock_client)
        self.assertIsInstance(connection, Connection)
        self.assertIs(connection._client, mock_client)
        self.assertIsNone(connection._bqstorage_client)

    @unittest.skipIf(
        bigquery_storage_v1beta1 is None, "Requires `google-cloud-bigquery-storage`"
    )
    def test_connect_w_both_clients(self):
        from google.cloud.bigquery.dbapi import connect
        from google.cloud.bigquery.dbapi import Connection

        mock_client = self._mock_client()
        mock_bqstorage_client = self._mock_bqstorage_client()
        connection = connect(
            client=mock_client, bqstorage_client=mock_bqstorage_client,
        )
        self.assertIsInstance(connection, Connection)
        self.assertIs(connection._client, mock_client)
        self.assertIs(connection._bqstorage_client, mock_bqstorage_client)

    def test_close(self):
        connection = self._make_one(client=self._mock_client())
        # close() is a no-op, there is nothing to test.
        connection.close()

    def test_commit(self):
        connection = self._make_one(client=self._mock_client())
        # commit() is a no-op, there is nothing to test.
        connection.commit()

    def test_cursor(self):
        from google.cloud.bigquery.dbapi import Cursor

        connection = self._make_one(client=self._mock_client())
        cursor = connection.cursor()
        self.assertIsInstance(cursor, Cursor)
        self.assertIs(cursor.connection, connection)
