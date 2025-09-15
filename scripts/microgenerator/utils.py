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

"""Utility functions for the microgenerator."""

import os
import sys
import yaml
import jinja2
from typing import Dict, Any, Iterator, Callable


def _load_resource(
    loader_func: Callable,
    path: str,
    not_found_exc: type,
    parse_exc: type,
    resource_type_name: str,
) -> Any:
    """
    Generic resource loader with common error handling.

    Args:
        loader_func: A callable that performs the loading and returns the resource.
                     It should raise appropriate exceptions on failure.
        path: The path/name of the resource for use in error messages.
        not_found_exc: The exception type to catch for a missing resource.
        parse_exc: The exception type to catch for a malformed resource.
        resource_type_name: A human-readable name for the resource type.
    """
    try:
        return loader_func()
    except not_found_exc:
        print(f"Error: {resource_type_name} '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    except parse_exc as e:
        print(
            f"Error: Could not load {resource_type_name.lower()} from '{path}': {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def load_template(template_path: str) -> jinja2.Template:
    """
    Loads a Jinja2 template from a given file path.
    """
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)

    def _loader() -> jinja2.Template:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir or "."),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return env.get_template(template_name)

    return _load_resource(
        loader_func=_loader,
        path=template_path,
        not_found_exc=jinja2.exceptions.TemplateNotFound,
        parse_exc=jinja2.exceptions.TemplateError,
        resource_type_name="Template file",
    )


def load_config(config_path: str) -> Dict[str, Any]:
    """Loads the generator's configuration from a YAML file."""

    def _loader() -> Dict[str, Any]:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    return _load_resource(
        loader_func=_loader,
        path=config_path,
        not_found_exc=FileNotFoundError,
        parse_exc=yaml.YAMLError,
        resource_type_name="Configuration file",
    )


def walk_codebase(path: str) -> Iterator[str]:
    """Yields all .py file paths in a directory."""
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def write_code_to_file(output_path: str, content: str):
    """Ensures the output directory exists and writes content to the file."""
    output_dir = os.path.dirname(output_path)

    # An empty output_dir means the file is in the current directory.
    if output_dir:
        print(f"  Ensuring output directory exists: {os.path.abspath(output_dir)}")
        os.makedirs(output_dir, exist_ok=True)
        if not os.path.isdir(output_dir):
            print(f"  Error: Output directory was not created.", file=sys.stderr)
            sys.exit(1)

    print(f"  Writing generated code to: {os.path.abspath(output_path)}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {output_path}")
