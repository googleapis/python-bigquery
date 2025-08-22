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

"""
A dual-purpose module for Python code analysis and BigQuery client generation.

When run as a script, it generates the BigQueryClient source code.
When imported, it provides utility functions for parsing and exploring
any Python codebase using the `ast` module.
"""

import ast
import os
import argparse
import glob
from collections import defaultdict
from typing import List, Dict, Any, Iterator

import utils

# =============================================================================
# Section 1: Generic AST Analysis Utilities
# =============================================================================

class CodeAnalyzer(ast.NodeVisitor):
    """
    A node visitor to traverse an AST and extract structured information
    about classes, methods, and their arguments.
    """

    def __init__(self):
        self.structure: List[Dict[str, Any]] = []
        self._current_class_info: Dict[str, Any] | None = None
        self._is_in_method: bool = False

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visits a class definition node."""
        class_info = {
            "class_name": node.name,
            "methods": [],
            "attributes": [],
        }
        self.structure.append(class_info)
        self._current_class_info = class_info
        self.generic_visit(node)
        self._current_class_info = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visits a function/method definition node."""
        if self._current_class_info:  # This is a method
            method_info = {
                "method_name": node.name,
                "args": [arg.arg for arg in node.args.args],
            }
            self._current_class_info["methods"].append(method_info)

            # Visit nodes inside the method to find instance attributes
            self._is_in_method = True
            self.generic_visit(node)
            self._is_in_method = False

    def _add_attribute(self, attr_name: str):
        """Adds a unique attribute to the current class context."""
        if self._current_class_info:
            if attr_name not in self._current_class_info["attributes"]:
                self._current_class_info["attributes"].append(attr_name)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Handles attribute assignments: `x = ...` and `self.x = ...`."""
        if self._current_class_info:
            for target in node.targets:
                # Instance attribute: self.x = ...
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    self._add_attribute(target.attr)
                # Class attribute: x = ... (only if not inside a method)
                elif isinstance(target, ast.Name) and not self._is_in_method:
                    self._add_attribute(target.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Handles annotated assignments: `x: int = ...` and `self.x: int = ...`."""
        if self._current_class_info:
            target = node.target
            # Instance attribute: self.x: int = ...
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                self._add_attribute(target.attr)
            # Class attribute: x: int = ... (only if not inside a method)
            elif isinstance(target, ast.Name) and not self._is_in_method:
                self._add_attribute(target.id)
        self.generic_visit(node)


def parse_code(code: str) -> List[Dict[str, Any]]:
    """
    Parses a string of Python code into a structured list of classes.

    Args:
        code: A string containing Python code.

    Returns:
        A list of dictionaries, where each dictionary represents a class.
    """
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure


def parse_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses a Python file into a structured list of classes.

    Args:
        file_path: The absolute path to the Python file.

    Returns:
        A list of dictionaries representing the classes in the file.
    """
    with open(file_path, "r", encoding="utf-8") as source:
        code = source.read()
    return parse_code(code)


def list_classes(path: str) -> List[str]:
    """Lists all classes in a given Python file or directory."""
    class_names = []
    if os.path.isfile(path) and path.endswith(".py"):
        structure = parse_file(path)
        for class_info in structure:
            class_names.append(class_info["class_name"])
    elif os.path.isdir(path):
        for file_path in utils.walk_codebase(path):
            structure = parse_file(file_path)
            for class_info in structure:
                class_names.append(
                    f"{class_info['class_name']} (in {os.path.basename(file_path)})"
                )
    return sorted(class_names)


def list_classes_and_methods(path: str) -> Dict[str, List[str]]:
    """Lists all classes and their methods in a given Python file or directory."""
    results = defaultdict(list)

    def process_structure(structure, file_name=None):
        for class_info in structure:
            key = class_info["class_name"]
            if file_name:
                key = f"{key} (in {file_name})"

            results[key] = sorted([m["method_name"] for m in class_info["methods"]])

    if os.path.isfile(path) and path.endswith(".py"):
        process_structure(parse_file(path))
    elif os.path.isdir(path):
        for file_path in utils.walk_codebase(path):
            process_structure(
                parse_file(file_path), file_name=os.path.basename(file_path)
            )

    return results


def list_classes_methods_and_attributes(path: str) -> Dict[str, Dict[str, List[str]]]:
    """Lists classes, methods, and attributes in a file or directory."""
    results = defaultdict(lambda: defaultdict(list))

    def process_structure(structure, file_name=None):
        for class_info in structure:
            key = class_info["class_name"]
            if file_name:
                key = f"{key} (in {file_name})"

            results[key]["attributes"] = sorted(class_info["attributes"])
            results[key]["methods"] = sorted(
                [m["method_name"] for m in class_info["methods"]]
            )

    if os.path.isfile(path) and path.endswith(".py"):
        process_structure(parse_file(path))
    elif os.path.isdir(path):
        for file_path in utils.walk_codebase(path):
            process_structure(
                parse_file(file_path), file_name=os.path.basename(file_path)
            )

    return results


def list_classes_methods_attributes_and_arguments(
    path: str,
) -> Dict[str, Dict[str, Any]]:
    """Lists classes, methods, attributes, and arguments in a file or directory."""
    results = defaultdict(lambda: defaultdict(list))

    def process_structure(structure, file_name=None):
        for class_info in structure:
            key = class_info["class_name"]
            if file_name:
                key = f"{key} (in {file_name})"

            results[key]["attributes"] = sorted(class_info["attributes"])
            method_details = {}
            # Sort methods by name for consistent output
            for method in sorted(class_info["methods"], key=lambda m: m["method_name"]):
                method_details[method["method_name"]] = method["args"]
            results[key]["methods"] = method_details

    if os.path.isfile(path) and path.endswith(".py"):
        process_structure(parse_file(path))
    elif os.path.isdir(path):
        for file_path in utils.walk_codebase(path):
            process_structure(
                parse_file(file_path), file_name=os.path.basename(file_path)
            )

    return results


# =============================================================================
# Section 2: Generic Code Generation Logic
# =============================================================================

def analyze_source_files(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes source files as per the configuration to extract class and method info.

    Args:
        config: The generator's configuration dictionary.

    Returns:
        A dictionary containing the data needed for template rendering.
    """
    parsed_data = defaultdict(dict)
    source_patterns = config.get("source_files", [])
    filter_rules = config.get("filter", {})
    class_filters = filter_rules.get("classes", {})
    method_filters = filter_rules.get("methods", {})

    source_files = []
    for pattern in source_patterns:
        source_files.extend(glob.glob(pattern, recursive=True))

    for file_path in source_files:
        structure = parse_file(file_path)

        for class_info in structure:
            class_name = class_info["class_name"]
            # Apply class filters
            if class_filters.get("include_suffixes"):
                if not class_name.endswith(tuple(class_filters["include_suffixes"])):
                    continue

            parsed_data[class_name]  # Ensure class is in dict

            for method in class_info["methods"]:
                method_name = method["method_name"]
                # Apply method filters
                if method_filters.get("include_prefixes"):
                    if not any(
                        method_name.startswith(p)
                        for p in method_filters["include_prefixes"]
                    ):
                        continue
                if method_filters.get("exclude_prefixes"):
                    if any(
                        method_name.startswith(p)
                        for p in method_filters["exclude_prefixes"]
                    ):
                        continue
                parsed_data[class_name][method_name] = method["args"]
    return parsed_data


def _format_args(method_args: List[str]) -> tuple[str, str]:
    """Formats method arguments for use in creating a method definition and a method call."""
    args_for_def = ", ".join(method_args)
    args_for_call = ", ".join([f"{arg}={arg}" for arg in method_args if arg != "self"])
    return args_for_def, args_for_call


def _format_class_name(method_name: str, suffix: str = "Request") -> str:
    """Formats a class name from a method name."""
    return "".join(word.capitalize() for word in method_name.split("_")) + suffix


def generate_code(config: Dict[str, Any], data: Dict[str, Any]) -> None:
    """
    Generates source code files using Jinja2 templates.
    """
    templates_config = config.get("templates", [])
    for item in templates_config:
        template_path = item["template"]
        output_path = item["output"]

        print(f"Processing template: {template_path}.")

        template = utils.load_template(template_path)
        methods_context = []
        for class_name, methods in data.items():
            for method_name, method_args in methods.items():
                args_for_def, args_for_call = _format_args(method_args)
                request_class_name = _format_class_name(method_name)
                methods_context.append(
                    {
                        "name": method_name,
                        "class_name": class_name,
                        "args_for_def": args_for_def,
                        "args_for_call": args_for_call,
                        "request_class_name": request_class_name,
                    }
                )
        
        print(f"Found {len(methods_context)} methods to generate.")

        final_code = template.render(
            service_name=config.get("service_name"),
            methods=methods_context
        )

        utils.write_code_to_file(output_path, final_code)


# =============================================================================
# Section 3: Main Execution
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A generic Python code generator for clients."
    )
    parser.add_argument(
        "config", help="Path to the YAML configuration file."
    )
    args = parser.parse_args()

    config = utils.load_config(args.config)
    data = analyze_source_files(config)
    generate_code(config, data)

    # TODO: Ensure blacken gets called on the generated source files as a final step.
