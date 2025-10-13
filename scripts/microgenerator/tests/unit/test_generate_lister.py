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

import os
import pytest
from unittest import mock

from scripts.microgenerator import generate

# Mock data to be returned by parse_file
MOCK_ANALYZED_CLASSES = [
    {
        "class_name": "MyClass",
        "methods": [
            {
                "method_name": "my_method",
                "args": [{"name": "self"}, {"name": "a", "type": "int"}],
                "return_type": "None",
            },
            {
                "method_name": "another_method",
                "args": [{"name": "self"}],
                "return_type": "str",
            },
        ],
        "attributes": [{"name": "my_attr", "type": "str"}],
    },
    {
        "class_name": "AnotherClass",
        "methods": [],
        "attributes": [],
    },
]

MOCK_ANALYZED_CLASSES_B = [
    {
        "class_name": "ClassB",
        "methods": [],
        "attributes": [],
    }
]


@pytest.fixture
def temp_py_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_file.py"
    p.write_text("class TestClass:\n    pass")
    return str(p)


@pytest.fixture
def temp_py_dir(tmp_path):
    d = tmp_path / "dir"
    d.mkdir()
    p1 = d / "file1.py"
    p1.write_text("class File1Class:\n    pass")
    p2 = d / "file2.py"
    p2.write_text("class File2Class:\n    pass")
    return str(d)


@pytest.fixture
def temp_empty_py_file(tmp_path):
    p = tmp_path / "empty.py"
    p.write_text("")
    return str(p)


@pytest.fixture
def temp_no_classes_py_file(tmp_path):
    p = tmp_path / "no_classes.py"
    p.write_text("def some_function():\n    pass")
    return str(p)


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_classes_only(mock_parse_file, temp_py_file):
    mock_parse_file.return_value = (MOCK_ANALYZED_CLASSES, set(), set())
    # show_methods, show_attributes, show_arguments default to False so only classes show up
    result = generate.list_code_objects(temp_py_file)
    assert result == ["AnotherClass", "MyClass"]
    mock_parse_file.assert_called_once_with(temp_py_file)


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_show_methods(mock_parse_file, temp_py_file):
    mock_parse_file.return_value = (MOCK_ANALYZED_CLASSES, set(), set())
    # show_attributes, show_arguments default to False and do not show up
    result = generate.list_code_objects(temp_py_file, show_methods=True)
    assert "MyClass" in result
    assert "AnotherClass" in result
    assert result["MyClass"]["methods"] == ["another_method", "my_method"]
    assert result["AnotherClass"]["methods"] == []


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_show_attributes(mock_parse_file, temp_py_file):
    mock_parse_file.return_value = (MOCK_ANALYZED_CLASSES, set(), set())
    # show_methods, show_arguments default to False and do not show up
    result = generate.list_code_objects(temp_py_file, show_attributes=True)
    assert "MyClass" in result
    assert result["MyClass"]["attributes"] == [{"name": "my_attr", "type": "str"}]
    assert "AnotherClass" in result
    assert result["AnotherClass"]["attributes"] == []


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_show_arguments(mock_parse_file, temp_py_file):
    mock_parse_file.return_value = (MOCK_ANALYZED_CLASSES, set(), set())
    # show_arguments=True implies show_methods=True; show_attributes defaults to False.
    result = generate.list_code_objects(temp_py_file, show_arguments=True)
    assert "MyClass" in result
    assert "methods" in result["MyClass"]
    assert result["MyClass"]["methods"]["my_method"] == [
        {"name": "self"},
        {"name": "a", "type": "int"},
    ]
    assert result["MyClass"]["methods"]["another_method"] == [{"name": "self"}]


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_all_flags(mock_parse_file, temp_py_file):
    mock_parse_file.return_value = (MOCK_ANALYZED_CLASSES, set(), set())
    # all show_* parameters are set to True, so if present in the code all elements will show up
    result = generate.list_code_objects(
        temp_py_file, show_methods=True, show_attributes=True, show_arguments=True
    )
    assert "MyClass" in result
    assert "methods" in result["MyClass"]
    assert "attributes" in result["MyClass"]
    assert result["MyClass"]["methods"]["my_method"] == [
        {"name": "self"},
        {"name": "a", "type": "int"},
    ]
    assert result["MyClass"]["attributes"] == [{"name": "my_attr", "type": "str"}]


@mock.patch("scripts.microgenerator.utils.walk_codebase")
@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_directory(mock_parse_file, mock_walk_codebase, temp_py_dir):
    file1 = os.path.join(temp_py_dir, "file1.py")
    file2 = os.path.join(temp_py_dir, "file2.py")
    mock_walk_codebase.return_value = [file1, file2]

    def side_effect(path):
        if path == file1:
            return (MOCK_ANALYZED_CLASSES, set(), set())
        if path == file2:
            return (MOCK_ANALYZED_CLASSES_B, set(), set())
        return ([], set(), set())

    mock_parse_file.side_effect = side_effect
    # show_methods, show_attributes, show_arguments default to False so only classes show up
    result = generate.list_code_objects(temp_py_dir)
    assert sorted(result) == [
        "AnotherClass (in file1.py)",
        "ClassB (in file2.py)",
        "MyClass (in file1.py)",
    ]


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_empty_file(mock_parse_file, temp_empty_py_file):
    mock_parse_file.return_value = ([], set(), set())
    # empty file, nothing should be returned
    result = generate.list_code_objects(temp_empty_py_file)
    assert result == []
    # empty file, nothing should be returned
    result_dict = generate.list_code_objects(temp_empty_py_file, show_methods=True)
    assert result_dict == {}


@mock.patch("scripts.microgenerator.generate.parse_file")
def test_list_code_objects_no_classes(mock_parse_file, temp_no_classes_py_file):
    mock_parse_file.return_value = ([], set(), set())
    # file has no classes, nothing should be returned
    result = generate.list_code_objects(temp_no_classes_py_file)
    assert result == []
    # file has no classes, nothing should be returned
    result_dict = generate.list_code_objects(
        temp_no_classes_py_file, show_attributes=True
    )
    assert result_dict == {}
