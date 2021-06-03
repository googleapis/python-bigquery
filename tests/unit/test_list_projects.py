import mock
import pytest

from .helpers import make_connection


@pytest.mark.parametrize(
    "extra,query",
    [({}, {})])
def test_list_projects_defaults(client, PROJECT, extra, query):
    from google.cloud.bigquery.client import Project

    PROJECT_1 = "PROJECT_ONE"
    PROJECT_2 = "PROJECT_TWO"
    TOKEN = "TOKEN"
    DATA = {
        "nextPageToken": TOKEN,
        "projects": [
            {
                "kind": "bigquery#project",
                "id": PROJECT,
                "numericId": 1,
                "projectReference": {"projectId": PROJECT},
                "friendlyName": "One",
            },
            {
                "kind": "bigquery#project",
                "id": PROJECT_2,
                "numericId": 2,
                "projectReference": {"projectId": PROJECT_2},
                "friendlyName": "Two",
            },
        ],
    }
    conn = client._connection = make_connection(DATA)
    iterator = client.list_projects(**extra)

    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        page = next(iterator.pages)

    final_attributes.assert_called_once_with({"path": "/projects"}, client, None)
    projects = list(page)
    token = iterator.next_page_token

    assert len(projects) == len(DATA["projects"])
    for found, expected in zip(projects, DATA["projects"]):
        assert isinstance(found, Project)
        assert found.project_id == expected["id"]
        assert found.numeric_id == expected["numericId"]
        assert found.friendly_name == expected["friendlyName"]
    assert token == TOKEN

    conn.api_request.assert_called_once_with(
        method="GET", path="/projects", query_params=query, timeout=None
    )

def test_list_projects_w_timeout(client):
    TOKEN = "TOKEN"
    DATA = {
        "nextPageToken": TOKEN,
        "projects": [],
    }
    conn = client._connection = make_connection(DATA)

    iterator = client.list_projects(timeout=7.5)

    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        next(iterator.pages)

    final_attributes.assert_called_once_with({"path": "/projects"}, client, None)

    conn.api_request.assert_called_once_with(
        method="GET", path="/projects", query_params={}, timeout=7.5
    )

def test_list_projects_explicit_response_missing_projects_key(client):
    TOKEN = "TOKEN"
    DATA = {}
    conn = client._connection = make_connection(DATA)

    iterator = client.list_projects(max_results=3, page_token=TOKEN)

    with mock.patch(
        "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
    ) as final_attributes:
        page = next(iterator.pages)

    final_attributes.assert_called_once_with({"path": "/projects"}, client, None)
    projects = list(page)
    token = iterator.next_page_token

    assert len(projects) == 0
    assert token is None

    conn.api_request.assert_called_once_with(
        method="GET",
        path="/projects",
        query_params={"maxResults": 3, "pageToken": TOKEN},
        timeout=None,
    )
