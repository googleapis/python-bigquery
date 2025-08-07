import ast
import os
from collections import defaultdict

from config_helper import (
    CLASSES_TO_INCLUDE,
    # CLASSES_TO_EXCLUDE, # Not currently being used.
    METHODS_TO_INCLUDE,
    METHODS_TO_EXCLUDE,
)
from template_utils import load_template

# Constants
BASE_DIR = "google/cloud/bigquery_v2/services"
FILES_TO_PARSE = [
    os.path.join(root, file)
    for root, _, files in os.walk(BASE_DIR)
    for file in files
    if file.endswith(".py")
]


def create_tree(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    return tree


def _extract_classes(tree):
    """Extracts class nodes from an AST."""
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith(
            *CLASSES_TO_INCLUDE
        ):  # TODO: currently this is variable includes only one class. Refactor if necessary
            classes.append(node)
    return classes


def _extract_methods(class_node):
    """Extracts method nodes from a class node."""
    return (m for m in class_node.body if isinstance(m, ast.FunctionDef))


def _process_method(method, class_name, parsed_data):
    """Processes a single method and updates parsed_data."""
    method_name = method.name
    if any(method_name.startswith(prefix) for prefix in METHODS_TO_INCLUDE) and not any(
        method_name.startswith(prefix) for prefix in METHODS_TO_EXCLUDE
    ):
        parameters = [arg.arg for arg in method.args.args + method.args.kwonlyargs]
        parsed_data[class_name][method_name] = parameters


def parse_files(file_paths):
    """
    Parse a list of Python files and extract information about classes,
    methods, and parameters.

    Args:
        file_paths (list): List of file paths to parse.

    Returns:
        Defaultdict with zero or more entries.
    """

    parsed_data = defaultdict(dict)

    for file_path in file_paths:
        tree = create_tree(file_path)

        for class_ in _extract_classes(tree):
            class_name = class_.name
            parsed_data[class_name]

            for method in _extract_methods(class_):
                _process_method(method, class_name, parsed_data)

    return parsed_data


def _format_args(method_args):
    """Formats method arguments for use in creating a method definition
    and a method call.
    """
    args_for_def = ", ".join(method_args)
    args_for_call = ", ".join([f"{arg}={arg}" for arg in method_args if arg != "self"])
    return args_for_def, args_for_call


def _format_class_name(method_name, suffix="Request"):
    """Formats a class name from a method name.

    Example:
        list_datasets -> ListDatasetsRequest
    """
    return "".join(word.capitalize() for word in method_name.split("_")) + suffix


def generate_client_class_source(data):
    """
    Generates the BigQueryClient source code using a Jinja2 template.

    Args:
        data: A dictionary where keys are *ServiceClient class names and
              values are dictionaries of methods for that client.

    Returns:
        A string containing the complete, formatted Python source code
        for the BigQueryClient class.
    """

    template = load_template("bigqueryclient.py.j2")

    # Prepare the context for the template.
    # We transform the input data into a flat list of methods
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

    # Render the template with the context.
    generated_code = template.render(methods=methods_context)

    return generated_code


if __name__ == "__main__":
    data = parse_files(FILES_TO_PARSE)

    final_code = generate_client_class_source(data)
    # TODO: write final code to file.

    print(final_code)

    # Ensure black gets called on the generated source files as a final step.
