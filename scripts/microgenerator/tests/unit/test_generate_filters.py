import pytest
from scripts.microgenerator.generate import (
    _should_include_class,
    _should_include_method,
)


# Tests for _should_include_class
@pytest.mark.parametrize(
    "class_name, filters, expected",
    [
        ("MyClass", {}, True),  # No filters
        (
            "DatasetClient",
            {"include_suffixes": ["Client", "Service"]},
            True,
        ),  # Include suffix match
        (
            "MyClass",
            {"include_suffixes": ["Client", "Service"]},
            False,
        ),  # Include suffix no match
        (
            "MyBase",
            {"exclude_suffixes": ["Base", "Util"]},
            False,
        ),  # Exclude suffix match
        (
            "MyClass",
            {"exclude_suffixes": ["Base", "Util"]},
            True,
        ),  # Exclude suffix no match
        (
            "DatasetClient",
            {"include_suffixes": ["Client"], "exclude_suffixes": ["BaseClient"]},
            True,
        ),  # Mix include/exclude
        (
            "BaseClient",
            {"include_suffixes": ["Client"], "exclude_suffixes": ["BaseClient"]},
            False,
        ),  # Mix include/exclude
        (
            "MyClass",
            {"include_suffixes": [], "exclude_suffixes": []},
            True,
        ),  # Empty filters
    ],
)
def test_should_include_class(class_name, filters, expected):
    assert _should_include_class(class_name, filters) is expected


# Tests for _should_include_method
@pytest.mark.parametrize(
    "method_name, filters, expected",
    [
        ("my_method", {}, True),  # No filters
        (
            "get_dataset",
            {"include_prefixes": ["get_", "list_"]},
            True,
        ),  # Include prefix match
        (
            "list_jobs",
            {"include_prefixes": ["get_", "list_"]},
            True,
        ),  # Include prefix match
        (
            "create_dataset",
            {"include_prefixes": ["get_", "list_"]},
            False,
        ),  # Include prefix no match
        (
            "_private_method",
            {"exclude_prefixes": ["_", "internal_"]},
            False,
        ),  # Exclude prefix match
        (
            "internal_helper",
            {"exclude_prefixes": ["_", "internal_"]},
            False,
        ),  # Exclude prefix match
        (
            "get_dataset",
            {"exclude_prefixes": ["_", "internal_"]},
            True,
        ),  # Exclude prefix no match
        (
            "get_dataset",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            True,
        ),  # Mix include/exclude
        (
            "get_internal_status",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            False,
        ),  # Mix include/exclude
        (
            "list_datasets",
            {"include_prefixes": ["get_"], "exclude_prefixes": ["get_internal_"]},
            False,
        ),  # Mix include/exclude
        (
            "my_method",
            {"include_prefixes": [], "exclude_prefixes": []},
            True,
        ),  # Empty filters
    ],
)
def test_should_include_method(method_name, filters, expected):
    assert _should_include_method(method_name, filters) is expected
