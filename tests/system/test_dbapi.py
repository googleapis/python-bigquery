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

import datetime
import operator
import itertools
import uuid

from google.cloud._helpers import UTC
import psutil
import pytest

from google.cloud.bigquery import dbapi
from . import helpers

try:
    from google.cloud import bigquery_storage
except ImportError:  # pragma: NO COVER
    bigquery_storage = None

try:
    import pyarrow
    import pyarrow.types
except ImportError:  # pragma: NO COVER
    pyarrow = None


@pytest.fixture(scope="session")
def connection(bigquery_client):
    return dbapi.connect(bigquery_client)


@pytest.fixture
def cursor(connection):
    return connection.cursor()


@pytest.mark.parametrize(("sql", "expected"), helpers.STANDARD_SQL_EXAMPLES)
def test_w_standard_sql_types(sql, expected, cursor):
    cursor.execute(sql)
    assert cursor.rowcount == 1
    row = cursor.fetchone()
    assert len(row) == 1
    assert row[0] == expected
    row = cursor.fetchone()
    assert row is None


def test_fetchall(cursor):
    query = "SELECT * FROM UNNEST([(1, 2), (3, 4), (5, 6)])"
    for arraysize in itertools.chain((None,), range(1, 5)):
        cursor.execute(query)
        assert cursor.rowcount == 3
        cursor.arraysize = arraysize
        rows = cursor.fetchall()
        row_tuples = [r.values() for r in rows]
        assert row_tuples == [(1, 2), (3, 4), (5, 6)]


def test_fetchall_from_script(cursor):
    query = """
    CREATE TEMP TABLE Example
    (
      x INT64,
      y STRING
    );

    INSERT INTO Example
    VALUES (5, 'foo'),
    (6, 'bar'),
    (7, 'baz');

    SELECT *
    FROM Example
    ORDER BY x ASC;
    """

    cursor.execute(query)
    assert cursor.rowcount == 3
    rows = cursor.fetchall()
    row_tuples = [r.values() for r in rows]
    assert row_tuples == [(5, "foo"), (6, "bar"), (7, "baz")]


def test_create_view(cursor, dataset_id):
    query = f"""
    CREATE VIEW {dataset_id}.dbapi_create_view
    AS SELECT name, SUM(number) AS total
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    GROUP BY name;
    """

    cursor.execute(query)
    assert cursor.rowcount == 0


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_fetch_w_bqstorage_client_large_result_set(bigquery_client, bqstorage_client):
    cursor = dbapi.connect(bigquery_client, bqstorage_client).cursor()

    cursor.execute(
        """
        SELECT id, `by`, time_ts
        FROM `bigquery-public-data.hacker_news.comments`
        ORDER BY `id` ASC
        LIMIT 100000
        """
    )

    result_rows = [cursor.fetchone(), cursor.fetchone(), cursor.fetchone()]

    field_name = operator.itemgetter(0)
    fetched_data = [sorted(row.items(), key=field_name) for row in result_rows]

    # Since DB API is not thread safe, only a single result stream should be
    # requested by the BQ storage client, meaning that results should arrive
    # in the sorted order.
    expected_data = [
        [
            ("by", "sama"),
            ("id", 15),
            ("time_ts", datetime.datetime(2006, 10, 9, 19, 51, 1, tzinfo=UTC)),
        ],
        [
            ("by", "pg"),
            ("id", 17),
            ("time_ts", datetime.datetime(2006, 10, 9, 19, 52, 45, tzinfo=UTC)),
        ],
        [
            ("by", "pg"),
            ("id", 22),
            ("time_ts", datetime.datetime(2006, 10, 10, 2, 18, 22, tzinfo=UTC)),
        ],
    ]
    assert fetched_data == expected_data


def test_dry_run_query(cursor):
    from google.cloud.bigquery.job import QueryJobConfig

    query = """
        SELECT country_name
        FROM `bigquery-public-data.utility_us.country_code_iso`
        WHERE country_name LIKE 'U%'
    """

    cursor.execute(query, job_config=QueryJobConfig(dry_run=True))
    assert cursor.rowcount == 0

    rows = cursor.fetchall()
    assert list(rows) == []


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_connection_does_not_leak_sockets():
    current_process = psutil.Process()
    conn_count_start = len(current_process.connections())

    # Provide no explicit clients, so that the connection will create and own them.
    connection = dbapi.connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, `by`, time_ts
        FROM `bigquery-public-data.hacker_news.comments`
        ORDER BY `id` ASC
        LIMIT 100000
    """
    )
    rows = cursor.fetchall()
    assert len(rows) == 100000

    connection.close()
    conn_count_end = len(current_process.connections())
    assert conn_count_end <= conn_count_start


def test_w_dml(bigquery_client, cursor, dataset_id):
    table_id = "dbapi_test_w_dml"
    bigquery_client.load_table_from_json(
        [{"greeting": "こんにちは"}, {"greeting": "Hello World"}, {"greeting": "Howdy!"}],
        f"{dataset_id}.{table_id}",
    ).result()

    query = f"""UPDATE {dataset_id}.{table_id}
        SET greeting = 'Guten Tag'
        WHERE greeting = 'Hello World'
        """
    cursor.execute(
        query, job_id="test_w_dml_{}".format(str(uuid.uuid4())),
    )
    assert cursor.rowcount == 1


@pytest.mark.parametrize(
    ("sql", "expected", "query_parameters"),
    [
        ("SELECT %(boolval)s", True, {"boolval": True},),
        ('SELECT %(a "very" weird `name`)s', True, {'a "very" weird `name`': True},),
        ("SELECT %(select)s", True, {"select": True},),  # this name is a keyword
        ("SELECT %s", False, [False]),
        ("SELECT %(intval)s", 123, {"intval": 123},),
        ("SELECT %s", -123456789, [-123456789],),
        ("SELECT %(floatval)s", 1.25, {"floatval": 1.25},),
        ("SELECT LOWER(%(strval)s)", "i am a string", {"strval": "I Am A String"},),
        (
            "SELECT DATE_SUB(%(dateval)s, INTERVAL 1 DAY)",
            datetime.date(2017, 4, 1),
            {"dateval": datetime.date(2017, 4, 2)},
        ),
        (
            "SELECT TIME_ADD(%(timeval)s, INTERVAL 4 SECOND)",
            datetime.time(12, 35, 0),
            {"timeval": datetime.time(12, 34, 56)},
        ),
        (
            ("SELECT DATETIME_ADD(%(datetimeval)s, INTERVAL 53 SECOND)"),
            datetime.datetime(2012, 3, 4, 5, 7, 0),
            {"datetimeval": datetime.datetime(2012, 3, 4, 5, 6, 7)},
        ),
        (
            "SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)",
            datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            {"zoned": datetime.datetime(2012, 3, 4, 5, 6, 7, tzinfo=UTC)},
        ),
        (
            "SELECT TIMESTAMP_TRUNC(%(zoned)s, MINUTE)",
            datetime.datetime(2012, 3, 4, 5, 6, 0, tzinfo=UTC),
            {"zoned": datetime.datetime(2012, 3, 4, 5, 6, 7, 250000, tzinfo=UTC)},
        ),
    ],
)
def test_w_query_parameters(cursor, sql, query_parameters, expected):
    cursor.execute(sql, query_parameters)

    assert cursor.rowcount == 1
    row = cursor.fetchone()
    assert len(row) == 1
    assert row[0] == expected
    row = cursor.fetchone()
    assert row is None
