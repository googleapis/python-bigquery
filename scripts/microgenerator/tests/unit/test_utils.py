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

"""Tests for utils.py."""

import pytest
from unittest.mock import Mock, patch

from scripts.microgenerator import utils


def test_load_resource_success():
    """Tests that _load_resource returns the loader's result on success."""
    loader_func = Mock(return_value="Success")
    result = utils._load_resource(
        loader_func=loader_func,
        path="/fake/path",
        not_found_exc=FileNotFoundError,
        parse_exc=ValueError,
        resource_type_name="Fake Resource",
    )
    assert result == "Success"
    loader_func.assert_called_once()


def test_load_resource_not_found(capsys):
    """Tests that _load_resource exits on not_found_exc."""
    loader_func = Mock(side_effect=FileNotFoundError)
    with pytest.raises(SystemExit) as excinfo:
        utils._load_resource(
            loader_func=loader_func,
            path="/fake/path",
            not_found_exc=FileNotFoundError,
            parse_exc=ValueError,
            resource_type_name="Fake Resource",
        )
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Fake Resource '/fake/path' not found." in captured.err


def test_load_resource_parse_error(capsys):
    """Tests that _load_resource exits on parse_exc."""
    error = ValueError("Invalid format")
    loader_func = Mock(side_effect=error)
    with pytest.raises(SystemExit) as excinfo:
        utils._load_resource(
            loader_func=loader_func,
            path="/fake/path",
            not_found_exc=FileNotFoundError,
            parse_exc=ValueError,
            resource_type_name="Fake Resource",
        )
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert (
        "Error: Could not load fake resource from '/fake/path': Invalid format"
        in captured.err
    )


def test_load_template_success(tmp_path):
    """Tests that load_template successfully loads a Jinja2 template."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_path = template_dir / "test.j2"
    template_path.write_text("Hello, {{ name }}!")

    template = utils.load_template(str(template_path))
    assert template.render(name="World") == "Hello, World!"


def test_load_template_not_found(capsys):
    """Tests that load_template exits when the template is not found."""
    with pytest.raises(SystemExit) as excinfo:
        utils.load_template("/non/existent/path.j2")
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Template file '/non/existent/path.j2' not found." in captured.err


def test_load_template_parse_error(tmp_path, capsys):
    """Tests that load_template exits on a template syntax error."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_path = template_dir / "test.j2"
    template_path.write_text("Hello, {{ name }!")  # Malformed template

    with pytest.raises(SystemExit) as excinfo:
        utils.load_template(str(template_path))
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Could not load template file" in captured.err


def test_load_config_success(tmp_path):
    """Tests that load_config successfully loads a YAML file."""
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    config_path.write_text("key: value")

    config = utils.load_config(str(config_path))
    assert config == {"key": "value"}


def test_load_config_not_found(capsys):
    """Tests that load_config exits when the config file is not
    found."""
    with pytest.raises(SystemExit) as excinfo:
        utils.load_config("/non/existent/path.yaml")
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert (
        "Error: Configuration file '/non/existent/path.yaml' not found." in captured.err
    )


def test_load_config_parse_error(tmp_path, capsys):
    """Tests that load_config exits on a YAML syntax error."""
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    config_path.write_text("key: value:")  # Malformed YAML

    with pytest.raises(SystemExit) as excinfo:
        utils.load_config(str(config_path))
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Could not load configuration file" in captured.err


def test_walk_codebase_finds_py_files(tmp_path):
    """Tests that walk_codebase finds all .py files."""
    # Create a directory structure
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "c").mkdir()

    # Create some files
    (tmp_path / "a" / "file1.py").touch()
    (tmp_path / "a" / "c" / "file2.py").touch()
    (tmp_path / "b" / "file3.py").touch()
    (tmp_path / "a" / "file.txt").touch()  # Should be ignored
    (tmp_path / "b" / "script").touch()  # Should be ignored

    result = sorted(list(utils.walk_codebase(str(tmp_path))))

    expected = sorted(
        [
            str(tmp_path / "a" / "file1.py"),
            str(tmp_path / "a" / "c" / "file2.py"),
            str(tmp_path / "b" / "file3.py"),
        ]
    )

    assert result == expected


def test_walk_codebase_no_py_files(tmp_path):
    """Tests that walk_codebase handles directories with no .py files."""
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "file.txt").touch()
    (tmp_path / "b").mkdir()

    result = list(utils.walk_codebase(str(tmp_path)))
    assert result == []


def test_walk_codebase_empty_directory(tmp_path):
    """Tests that walk_codebase handles an empty directory."""
    result = list(utils.walk_codebase(str(tmp_path)))
    assert result == []


def test_walk_codebase_non_existent_path():
    """Tests that walk_codebase handles a non-existent path gracefully."""
    result = list(utils.walk_codebase("/non/existent/path"))
    assert result == []


def test_walk_codebase_with_file_path(tmp_path):
    """Tests that walk_codebase handles being passed a file path."""
    file_path = tmp_path / "file.py"
    file_path.touch()
    # os.walk on a file yields nothing, so this should be empty.
    result = list(utils.walk_codebase(str(file_path)))
    assert result == []


def test_write_code_to_file_creates_directory(tmp_path):
    """Tests that write_code_to_file creates the directory if it doesn't exist."""
    output_dir = tmp_path / "new_dir"
    output_path = output_dir / "test_file.py"
    content = "import this"

    assert not output_dir.exists()

    utils.write_code_to_file(str(output_path), content)

    assert output_dir.is_dir()
    assert output_path.read_text() == content


def test_write_code_to_file_existing_directory(tmp_path):
    """Tests that write_code_to_file works when the directory already exists."""
    output_path = tmp_path / "test_file.py"
    content = "import that"

    utils.write_code_to_file(str(output_path), content)

    assert output_path.read_text() == content


def test_write_code_to_file_no_directory(tmp_path, monkeypatch):
    """Tests that write_code_to_file works for the current directory."""
    monkeypatch.chdir(tmp_path)
    output_path = "test_file.py"
    content = "import the_other"

    utils.write_code_to_file(output_path, content)

    assert (tmp_path / output_path).read_text() == content


@patch("os.path.isdir", return_value=False)
@patch("os.makedirs")
def test_write_code_to_file_dir_creation_fails(
    mock_makedirs, mock_isdir, tmp_path, capsys
):
    """Tests that write_code_to_file exits if directory creation fails."""
    output_path = tmp_path / "new_dir" / "test_file.py"
    content = "import this"

    with pytest.raises(SystemExit) as excinfo:
        utils.write_code_to_file(str(output_path), content)

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Output directory was not created." in captured.err
    mock_makedirs.assert_called_once()
