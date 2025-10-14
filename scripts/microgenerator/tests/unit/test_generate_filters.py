import pytest
from scripts.microgenerator.generate import (
    _should_include_class,
    _should_include_method,
)


# Tests for _should_include_class
@pytest.mark.parametrize(
    "class_name, filters, expected",
    [
        pytest.param("MyClass", {}, True, id="No filters"),
        pytest.param(
            "DatasetClient",
            {"include_suffixes": ["Client", "Service"]},
            True,
            id="Include suffix match",
        ),
        pytest.param(
            "MyClass",
            {"include_suffixes": ["Client", "Service"]},
            False,
            id="Include suffix no match",
        ),
        pytest.param(
            "MyBase",
            {"exclude_suffixes": ["Base", "Util"]},
            False,
            id="Exclude suffix match",
        ),
        pytest.param(
            "MyClass",
            {"exclude_suffixes": ["Base", "Util"]},
            True,
            id="Exclude suffix no match",
        ),
        pytest.param(
            "DatasetClient",
            {"include_suffixes": ["Client"], "exclude_suffixes": ["BaseClient"]},
            True,
            id="Mix include/exclude match",
        ),
        pytest.param(
            "BaseClient",
            {"include_suffixes": ["Client"], "exclude_suffixes": ["BaseClient"]},
            False,
            id="Mix include/exclude no match",
        ),
        pytest.param(
            "MyClass",
            {"include_suffixes": [], "exclude_suffixes": []},
            True,
            id="Empty filters",
        ),
    ],
)
def test_should_include_class(class_name, filters, expected):
    assert _should_include_class(class_name, filters) is expected


# Tests for _should_include_method
@pytest.mark.parametrize(
    "method_name, filters, expected",
    [
        pytest.param("my_method", {}, True, id="No filters"),
        pytest.param(
            "get_dataset",
            {"include_prefixes": ["get_", "list_"]},
            True,
            id="Include prefix match (get)",
        ),
        pytest.param(
            "list_jobs",
            {"include_prefixes": ["get_", "list_"]},
            True,
            id="Include prefix match (list)",
        ),
        pytest.param(
            "create_dataset",
            {"include_prefixes": ["get_", "list_"]},
            False,
            id="Include prefix no match",
        ),
        pytest.param(
            "_private_method",
            {"exclude_prefixes": ["_", "internal_"]},
            False,
            id="Exclude prefix match (private)",
        ),
        pytest.param(
            "internal_helper",
            {"exclude_prefixes": ["_", "internal_"]},
            False,
            id="Exclude prefix match (internal)",
        ),
        pytest.param(
            "get_dataset",
            {"exclude_prefixes": ["_", "internal_"]},
            True,
            id="Exclude prefix no match",
        ),
        pytest.param(
            "get_dataset",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            True,
            id="Mix include/exclude match",
        ),
        pytest.param(
            "get_internal_status",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            False,
            id="Mix include/exclude no match (exclude wins)",
        ),
        pytest.param(
            "list_datasets",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            False,
            id="Mix include/exclude no match (include fails)",
        ),
        pytest.param(
            "my_method",
            {"include_prefixes": [], "exclude_prefixes": []},
            True,
            id="Empty filters",
        ),
    ],
)
def test_should_include_method(method_name, filters, expected):
    assert _should_include_method(method_name, filters) is expected
