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

import pytest
from unittest import mock
import textwrap as tw

from scripts.microgenerator import generate


# --- Tests for parse_code() ---
def test_parse_code_empty():
    analyzed_classes, imports, types = generate.parse_code("")
    assert analyzed_classes == []
    assert imports == set()
    assert types == set()


def test_parse_code_simple_class():
    code = tw.dedent(
        """
        class MyClass:
            pass
    """
    )
    analyzed_classes, _, _ = generate.parse_code(code)
    assert len(analyzed_classes) == 1
    assert analyzed_classes[0]["class_name"] == "MyClass"


def test_parse_code_simple_function():
    code = tw.dedent(
        """
        def my_function():
            pass
    """
    )

    # In the microgenerator, the focus is parsing major classes (and their
    # associated methods in the GAPIC generated code, not parsing top-level
    # functions. Thus we do not expect it to capture this top-level function.
    analyzed_classes, _, _ = generate.parse_code(code)
    assert len(analyzed_classes) == 0


def test_parse_code_invalid_syntax():
    with pytest.raises(SyntaxError):
        # incorrect indentation and missing trailing colon on func definition.
        code = tw.dedent(
            """
            class MyClass:
                pass
              def func()
                pass
        """
        )
        generate.parse_code(code)


def test_parse_code_with_imports_and_types():
    code = tw.dedent(
        """
        import os
        import sys as system
        from typing import List, Optional, Dict
        from . import my_module

        class MyClass:
            attr: Dict[str, int]
            def method(self, x: List[str]) -> Optional[int]:
                return None
            def method2(self, y: 'MyClass') -> None:
                pass
    """
    )
    analyzed_classes, imports, types = generate.parse_code(code)

    expected_imports = {
        "import os",
        "import sys as system",
        "from typing import List, Optional, Dict",
        "from . import my_module",
    }
    assert imports == expected_imports

    expected_types = {
        "Dict",
        "str",
        "int",
        "List",
        "Optional",
        "MyClass",
        "None",
    }
    assert types == expected_types
    assert len(analyzed_classes) == 1


# --- Tests for parse_file() ---
# parse_file() wraps parse_code() and simply reads in content from a file
# as a string using the built in open() function and passes the string intact
# to parse_code().
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_parse_file_reads_and_parses(mock_file):
    read_data = tw.dedent(
        """
        class TestClass:
            pass
    """
    )
    mock_file.return_value.read.return_value = read_data
    analyzed_classes, _, _ = generate.parse_file("dummy/path/file.py")
    mock_file.assert_called_once_with("dummy/path/file.py", "r", encoding="utf-8")
    assert len(analyzed_classes) == 1
    assert analyzed_classes[0]["class_name"] == "TestClass"


@mock.patch("builtins.open", side_effect=FileNotFoundError)
def test_parse_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        generate.parse_file("nonexistent.py")
    mock_file.assert_called_once_with("nonexistent.py", "r", encoding="utf-8")


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_parse_file_syntax_error(mock_file):
    mock_file.return_value.read.return_value = "a = ("
    with pytest.raises(SyntaxError):
        generate.parse_file("syntax_error.py")
    mock_file.assert_called_once_with("syntax_error.py", "r", encoding="utf-8")


@mock.patch(
    "scripts.microgenerator.generate.parse_code", return_value=([], set(), set())
)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_parse_file_calls_parse_code(mock_file, mock_parse_code):
    """This test simply confirms that parse_code() gets called internally.

    Other parse_code tests ensure that it works as expected.
    """
    read_data = "some code"
    mock_file.return_value.read.return_value = read_data
    generate.parse_file("some_file.py")
    mock_parse_code.assert_called_once_with(read_data)
