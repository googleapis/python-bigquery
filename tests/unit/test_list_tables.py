from .helpers import make_connection, dataset_polymorphic
import google.cloud.bigquery.dataset
import mock
import pytest


@dataset_polymorphic
def test_list_tables_empty_w_timeout(
    make_dataset, get_reference, client, PROJECT, DS_ID
):
    path = "/projects/{}/datasets/{}/tables".format(PROJECT, DS_ID)
    conn = client._connection = make_connection({})

    dataset = make_dataset(PROJECT, DS_ID)
    iterator = client.list_tables(dataset, timeout=7.5)
    assert iterator.dataset is get_reference(dataset)
    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        page = next(iterator.pages)

    final_attributes.assert_called_once_with({"path": path}, client, None)
    tables = list(page)
    token = iterator.next_page_token

    assert tables == []
    assert token is None
    conn.api_request.assert_called_once_with(
        method="GET", path=path, query_params={}, timeout=7.5
    )


@dataset_polymorphic
def test_list_tables_defaults(make_dataset, get_reference, client, PROJECT, DS_ID):
    from google.cloud.bigquery.table import TableListItem

    TABLE_1 = "table_one"
    TABLE_2 = "table_two"
    PATH = "projects/%s/datasets/%s/tables" % (PROJECT, DS_ID)
    TOKEN = "TOKEN"
    DATA = {
        "nextPageToken": TOKEN,
        "tables": [
            {
                "kind": "bigquery#table",
                "id": "%s:%s.%s" % (PROJECT, DS_ID, TABLE_1),
                "tableReference": {
                    "tableId": TABLE_1,
                    "datasetId": DS_ID,
                    "projectId": PROJECT,
                },
                "type": "TABLE",
            },
            {
                "kind": "bigquery#table",
                "id": "%s:%s.%s" % (PROJECT, DS_ID, TABLE_2),
                "tableReference": {
                    "tableId": TABLE_2,
                    "datasetId": DS_ID,
                    "projectId": PROJECT,
                },
                "type": "TABLE",
            },
        ],
    }

    conn = client._connection = make_connection(DATA)
    dataset = make_dataset(PROJECT, DS_ID)

    iterator = client.list_tables(dataset)
    assert iterator.dataset is dataset
    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        page = next(iterator.pages)

    final_attributes.assert_called_once_with({"path": "/%s" % PATH}, client, None)
    tables = list(page)
    token = iterator.next_page_token

    assert len(tables) == len(DATA["tables"])
    for found, expected in zip(tables, DATA["tables"]):
        assert isinstance(found, TableListItem)
        assert found.full_table_id == expected["id"]
        assert found.table_type == expected["type"]
    assert token == TOKEN

    conn.api_request.assert_called_once_with(
        method="GET", path="/%s" % PATH, query_params={}, timeout=None
    )


def test_list_tables_explicit(client, PROJECT, DS_ID):
    from google.cloud.bigquery.table import TableListItem

    TABLE_1 = "table_one"
    TABLE_2 = "table_two"
    PATH = "projects/%s/datasets/%s/tables" % (PROJECT, DS_ID)
    TOKEN = "TOKEN"
    DATA = {
        "tables": [
            {
                "kind": "bigquery#dataset",
                "id": "%s:%s.%s" % (PROJECT, DS_ID, TABLE_1),
                "tableReference": {
                    "tableId": TABLE_1,
                    "datasetId": DS_ID,
                    "projectId": PROJECT,
                },
                "type": "TABLE",
            },
            {
                "kind": "bigquery#dataset",
                "id": "%s:%s.%s" % (PROJECT, DS_ID, TABLE_2),
                "tableReference": {
                    "tableId": TABLE_2,
                    "datasetId": DS_ID,
                    "projectId": PROJECT,
                },
                "type": "TABLE",
            },
        ]
    }

    conn = client._connection = make_connection(DATA)
    dataset = google.cloud.bigquery.dataset.DatasetReference(PROJECT, DS_ID)

    iterator = client.list_tables(
        # Test with string for dataset ID.
        DS_ID,
        max_results=3,
        page_token=TOKEN,
    )
    assert iterator.dataset == dataset
    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        page = next(iterator.pages)

    final_attributes.assert_called_once_with({"path": "/%s" % PATH}, client, None)
    tables = list(page)
    token = iterator.next_page_token

    assert len(tables) == len(DATA["tables"])
    for found, expected in zip(tables, DATA["tables"]):
        assert isinstance(found, TableListItem)
        assert found.full_table_id == expected["id"]
        assert found.table_type == expected["type"]
    assert token is None

    conn.api_request.assert_called_once_with(
        method="GET",
        path="/%s" % PATH,
        query_params={"maxResults": 3, "pageToken": TOKEN},
        timeout=None,
    )


def test_list_tables_wrong_type(client):
    with pytest.raises(TypeError):
        client.list_tables(42)
