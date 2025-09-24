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
import glob
import logging
import re
from collections import defaultdict
from typing import List, Dict, Any, Iterator

from . import name_utils
from . import utils

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
        self.imports: set[str] = set()
        self.types: set[str] = set()
        self._current_class_info: Dict[str, Any] | None = None
        self._is_in_method: bool = False

    def _get_type_str(self, node: ast.AST | None) -> str | None:
        """Recursively reconstructs a type annotation string from an AST node."""
        if node is None:
            return None
        # Handles simple names like 'str', 'int', 'HttpRequest'
        if isinstance(node, ast.Name):
            return node.id
        # Handles dotted names like 'service.GetDatasetRequest'
        if isinstance(node, ast.Attribute):
            # Attempt to reconstruct the full dotted path
            parts = []
            curr = node
            while isinstance(curr, ast.Attribute):
                parts.append(curr.attr)
                curr = curr.value
            if isinstance(curr, ast.Name):
                parts.append(curr.id)
                return ".".join(reversed(parts))
        # Handles subscripted types like 'list[str]', 'Optional[...]'
        if isinstance(node, ast.Subscript):
            value_str = self._get_type_str(node.value)
            slice_str = self._get_type_str(node.slice)
            return f"{value_str}[{slice_str}]"
        # Handles tuples inside subscripts, e.g., 'dict[str, int]'
        if isinstance(node, ast.Tuple):
            return ", ".join(
                [s for s in (self._get_type_str(e) for e in node.elts) if s]
            )
        # Handles forward references as strings, e.g., '"Dataset"'
        if isinstance(node, ast.Constant):
            return repr(node.value)
        return None  # Fallback for unhandled types

    def _collect_types_from_node(self, node: ast.AST | None) -> None:
        """Recursively traverses an annotation node to find and collect all type names."""
        if node is None:
            return

        if isinstance(node, ast.Name):
            self.types.add(node.id)
        elif isinstance(node, ast.Attribute):
            type_str = self._get_type_str(node)
            if type_str:
                self.types.add(type_str)
        elif isinstance(node, ast.Subscript):
            self._collect_types_from_node(node.value)
            self._collect_types_from_node(node.slice)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                self._collect_types_from_node(elt)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            self.types.add(node.value)
        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, ast.BitOr
        ):  # For | union type
            self._collect_types_from_node(node.left)
            self._collect_types_from_node(node.right)

    def visit_Import(self, node: ast.Import) -> None:
        """Catches 'import X' and 'import X as Y' statements."""
        for alias in node.names:
            if alias.asname:
                self.imports.add(f"import {alias.name} as {alias.asname}")
            else:
                self.imports.add(f"import {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Catches 'from X import Y' statements."""
        module = node.module or ""
        if not module:
            module = "." * node.level
        else:
            module = "." * node.level + module

        names = []
        for alias in node.names:
            if alias.asname:
                names.append(f"{alias.name} as {alias.asname}")
            else:
                names.append(alias.name)

        if names:
            self.imports.add(f"from {module} import {', '.join(names)}")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visits a class definition node."""
        class_info = {
            "class_name": node.name,
            "methods": [],
            "attributes": [],
        }

        # Extract class-level attributes (for proto.Message classes)
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attr_name = item.target.id
                type_str = self._get_type_str(item.annotation)
                class_info["attributes"].append({"name": attr_name, "type": type_str})

        self.structure.append(class_info)
        self._current_class_info = class_info
        self.generic_visit(node)
        self._current_class_info = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visits a function/method definition node."""
        if self._current_class_info:  # This is a method
            args_info = []

            # Get default values
            defaults = [self._get_type_str(d) for d in node.args.defaults]
            num_defaults = len(defaults)
            num_args = len(node.args.args)

            for i, arg in enumerate(node.args.args):
                arg_data = {"name": arg.arg, "type": self._get_type_str(arg.annotation)}

                # Match defaults to arguments from the end
                default_index = i - (num_args - num_defaults)
                if default_index >= 0:
                    arg_data["default"] = defaults[default_index]

                args_info.append(arg_data)
                self._collect_types_from_node(arg.annotation)

            # Collect return type
            return_type = self._get_type_str(node.returns)
            self._collect_types_from_node(node.returns)

            method_info = {
                "method_name": node.name,
                "args": args_info,
                "return_type": return_type,
            }
            self._current_class_info["methods"].append(method_info)

            # Visit nodes inside the method to find instance attributes.
            self._is_in_method = True
            self.generic_visit(node)
            self._is_in_method = False

    def _add_attribute(self, attr_name: str, attr_type: str | None = None):
        """Adds a unique attribute to the current class context.

        Assumes self._current_class_info is not None, as this method
        is only called from within visit_Assign and visit_AnnAssign
        after checking for an active class context.
        """
        # Create a list of attribute names for easy lookup
        attr_names = [
            attr.get("name") for attr in self._current_class_info["attributes"]
        ]
        if attr_name not in attr_names:
            self._current_class_info["attributes"].append(
                {"name": attr_name, "type": attr_type}
            )

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
                self._add_attribute(target.attr, self._get_type_str(node.annotation))
            # Class attribute: x: int = ...
            # We identify it as a class attribute if the assignment happens
            # directly within the class body, not inside a method.
            elif isinstance(target, ast.Name) and not self._is_in_method:
                self._add_attribute(target.id, self._get_type_str(node.annotation))
        self.generic_visit(node)


def parse_code(code: str) -> tuple[List[Dict[str, Any]], set[str], set[str]]:
    """
    Parses a string of Python code into a structured list of classes, a set of imports,
    and a set of all type annotations found.

    Args:
        code: A string containing Python code.

    Returns:
        A tuple containing:
        - A list of dictionaries, where each dictionary represents a class.
        - A set of strings, where each string is an import statement.
        - A set of strings, where each string is a type annotation.
    """
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure, analyzer.imports, analyzer.types


def parse_file(file_path: str) -> tuple[List[Dict[str, Any]], set[str], set[str]]:
    """
    Parses a Python file into a structured list of classes, a set of imports,
    and a set of all type annotations found.

    Args:
        file_path: The absolute path to the Python file.

    Returns:
        A tuple containing the class structure, a set of import statements,
        and a set of type annotations.
    """
    with open(file_path, "r", encoding="utf-8") as source:
        code = source.read()
    return parse_code(code)


def list_code_objects(
    path: str,
    show_methods: bool = False,
    show_attributes: bool = False,
    show_arguments: bool = False,
) -> Any:
    """
    Lists classes and optionally their methods, attributes, and arguments
    from a given Python file or directory.

    This function consolidates the functionality of the various `list_*` functions.

    Args:
        path (str): The absolute path to a Python file or directory.
        show_methods (bool): Whether to include methods in the output.
        show_attributes (bool): Whether to include attributes in the output.
        show_arguments (bool): If True, includes method arguments. Implies show_methods.

    Returns:
        - If `show_methods` and `show_attributes` are both False, returns a
          sorted `List[str]` of class names (mimicking `list_classes`).
        - Otherwise, returns a `Dict[str, Dict[str, Any]]` containing the
          requested details about each class.
    """
    # If show_arguments is True, we must show methods.
    if show_arguments:
        show_methods = True

    results = defaultdict(dict)
    all_class_keys = []

    def process_structure(
        structure: List[Dict[str, Any]], file_name: str | None = None
    ):
        """Populates the results dictionary from the parsed AST structure."""
        for class_info in structure:
            key = class_info["class_name"]
            if file_name:
                key = f"{key} (in {file_name})"

            all_class_keys.append(key)

            if show_attributes:
                results[key]["attributes"] = sorted(class_info["attributes"])

            if show_methods:
                if show_arguments:
                    method_details = {}
                    # Sort methods by name for consistent output
                    for method in sorted(
                        class_info["methods"], key=lambda m: m["method_name"]
                    ):
                        method_details[method["method_name"]] = method["args"]
                    results[key]["methods"] = method_details
                else:
                    results[key]["methods"] = sorted(
                        [m["method_name"] for m in class_info["methods"]]
                    )

    # Determine if the path is a file or directory and process accordingly
    if os.path.isfile(path) and path.endswith(".py"):
        structure, _, _ = parse_file(path)
        process_structure(structure)
    elif os.path.isdir(path):
        # This assumes `utils.walk_codebase` is defined elsewhere.
        for file_path in utils.walk_codebase(path):
            structure, _, _ = parse_file(file_path)
            process_structure(structure, file_name=os.path.basename(file_path))

    # Return the data in the desired format based on the flags
    if not show_methods and not show_attributes:
        return sorted(all_class_keys)
    else:
        return dict(results)


# =============================================================================
# Section 2: Source file data gathering
# =============================================================================


def _should_include_class(class_name: str, class_filters: Dict[str, Any]) -> bool:
    """Checks if a class should be included based on filter criteria."""
    if class_filters.get("include_suffixes"):
        if not class_name.endswith(tuple(class_filters["include_suffixes"])):
            return False
    if class_filters.get("exclude_suffixes"):
        if class_name.endswith(tuple(class_filters["exclude_suffixes"])):
            return False
    return True


def _should_include_method(method_name: str, method_filters: Dict[str, Any]) -> bool:
    """Checks if a method should be included based on filter criteria."""
    if method_filters.get("include_prefixes"):
        if not any(
            method_name.startswith(p) for p in method_filters["include_prefixes"]
        ):
            return False
    if method_filters.get("exclude_prefixes"):
        if any(method_name.startswith(p) for p in method_filters["exclude_prefixes"]):
            return False
    return True


def _build_request_arg_schema(
    source_files: List[str], project_root: str
) -> Dict[str, List[str]]:
    """Parses type files to build a schema of request classes and their _id arguments."""
    request_arg_schema: Dict[str, List[str]] = {}
    for file_path in source_files:
        if "/types/" not in file_path:
            continue

        # Correctly determine the module name from the file path
        relative_path = os.path.relpath(file_path, project_root)
        module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, ".")

        try:
            structure, _, _ = parse_file(file_path)
            if not structure:
                continue

            for class_info in structure:
                class_name = class_info.get("class_name", "Unknown")
                if class_name.endswith("Request"):
                    full_class_name = f"{module_name}.{class_name}"
                    id_args = [
                        attr["name"]
                        for attr in class_info.get("attributes", [])
                        if attr.get("name", "").endswith("_id")
                    ]
                    if id_args:
                        request_arg_schema[full_class_name] = id_args
        except Exception as e:
            logging.warning(f"Failed to parse {file_path}: {e}")
    return request_arg_schema


def _process_service_clients(
    source_files: List[str], class_filters: Dict, method_filters: Dict
) -> tuple[defaultdict, set, set]:
    """Parses service client files to extract class and method information."""
    parsed_data = defaultdict(dict)
    all_imports: set[str] = set()
    all_types: set[str] = set()

    for file_path in source_files:
        if "/services/" not in file_path:
            continue

        structure, imports, types = parse_file(file_path)
        all_imports.update(imports)
        all_types.update(types)

        for class_info in structure:
            class_name = class_info["class_name"]
            if not _should_include_class(class_name, class_filters):
                continue

            parsed_data[class_name]  # Ensure class is in dict

            for method in class_info["methods"]:
                method_name = method["method_name"]
                if not _should_include_method(method_name, method_filters):
                    continue
                parsed_data[class_name][method_name] = method
    return parsed_data, all_imports, all_types


def analyze_source_files(
    config: Dict[str, Any],
) -> tuple[Dict[str, Any], set[str], set[str], Dict[str, List[str]]]:
    """
    Analyzes source files per the configuration to extract class and method info,
    as well as information on imports and typehints.

    Args:
        config: The generator's configuration dictionary.

    Returns:
        A tuple containing:
        - A dictionary containing the data needed for template rendering.
        - A set of all import statements required by the parsed methods.
        - A set of all type annotations found in the parsed methods.
        - A dictionary mapping request class names to their `_id` arguments.
    """
    project_root = config["project_root"]
    source_patterns_dict = config.get("source_files", {})
    filter_rules = config.get("filter", {})
    class_filters = filter_rules.get("classes", {})
    method_filters = filter_rules.get("methods", {})

    source_files = []
    for group in source_patterns_dict.values():
        for pattern in group:
            # Make the pattern absolute
            absolute_pattern = os.path.join(project_root, pattern)
            source_files.extend(glob.glob(absolute_pattern, recursive=True))

    # PASS 1: Build the request argument schema from the types files.
    request_arg_schema = _build_request_arg_schema(source_files, project_root)

    # PASS 2: Process the service client files.
    parsed_data, all_imports, all_types = _process_service_clients(
        source_files, class_filters, method_filters
    )

    return parsed_data, all_imports, all_types, request_arg_schema


# =============================================================================
# Section 3: Code Generation
# =============================================================================

def _generate_import_statement(
    context: List[Dict[str, Any]], key: str, path: str
) -> str:
    """Generates a formatted import statement from a list of context dictionaries.

    Args:
        context: A list of dictionaries containing the data.
        key: The key to extract from each dictionary in the context.
        path: The base import path (e.g., "google.cloud.bigquery_v2.services").

    Returns:
        A formatted, multi-line import statement string.
    """
    names = sorted(list(set([item[key] for item in context])))
    names_str = ",\n    ".join(names)
    return f"from {path} import (\n    {names_str}\n)"


def generate_code(config: Dict[str, Any], analysis_results: tuple) -> None:
    """
    Generates source code files using Jinja2 templates.
    """
    data, all_imports, all_types, request_arg_schema = analysis_results
    project_root = config["project_root"]
    config_dir = config["config_dir"]

    templates_config = config.get("templates", [])
    for item in templates_config:
        template_path = os.path.join(config_dir, item["template"])
        output_path = os.path.join(project_root, item["output"])

        template = utils.load_template(template_path)
        methods_context = []
        for class_name, methods in data.items():
            for method_name, method_info in methods.items():
                context = {
                    "name": method_name,
                    "class_name": class_name,
                    "return_type": method_info["return_type"],
                }

                # Infer the request class and find its schema.
                inferred_request_name = name_utils.method_to_request_class_name(
                    method_name
                )

                # Check for a request class name override in the config.
                method_overrides = (
                    config.get("filter", {}).get("methods", {}).get("overrides", {})
                )
                if method_name in method_overrides:
                    inferred_request_name = method_overrides[method_name].get(
                        "request_class_name", inferred_request_name
                    )

                fq_request_name = ""
                for key in request_arg_schema.keys():
                    if key.endswith(f".{inferred_request_name}"):
                        fq_request_name = key
                        break

                # If found, augment the method context.
                if fq_request_name:
                    context["request_class_full_name"] = fq_request_name
                    context["request_id_args"] = request_arg_schema[fq_request_name]

                methods_context.append(context)

        # Prepare imports for the template
        services_context = []
        client_class_names = sorted(
            list(set([m["class_name"] for m in methods_context]))
        )

        for class_name in client_class_names:
            service_name_cluster = name_utils.generate_service_names(class_name)
            services_context.append(service_name_cluster)

        # Also need to update methods_context to include the service_name and module_name
        # so the template knows which client to use for each method.
        class_to_service_map = {s["service_client_class"]: s for s in services_context}
        for method in methods_context:
            service_info = class_to_service_map.get(method["class_name"])
            if service_info:
                method["service_name"] = service_info["service_name"]
                method["service_module_name"] = service_info["service_module_name"]

        # Prepare new imports
        service_imports = [
            _generate_import_statement(
                services_context,
                "service_module_name",
                "google.cloud.bigquery_v2.services",
            )
        ]

        # Prepare type imports
        type_imports = [
            _generate_import_statement(
                services_context, "service_name", "google.cloud.bigquery_v2.types"
            )
        ]

        final_code = template.render(
            service_name=config.get("service_name"),
            methods=methods_context,
            services=services_context,
            service_imports=service_imports,
            type_imports=type_imports,
            request_arg_schema=request_arg_schema,
        )

        utils.write_code_to_file(output_path, final_code)
