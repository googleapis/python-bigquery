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

import ast
import pytest
from scripts.microgenerator.generate import CodeAnalyzer

# --- Tests CodeAnalyzer handling of Imports ---


class TestCodeAnalyzerImports:
    @pytest.mark.parametrize(
        "code_snippet, expected_imports",
        [
            pytest.param(
                "import os\nimport sys",
                ["import os", "import sys"],
                id="simple_imports",
            ),
            pytest.param(
                "import numpy as np",
                ["import numpy as np"],
                id="aliased_import",
            ),
            pytest.param(
                "from collections import defaultdict, OrderedDict",
                ["from collections import defaultdict, OrderedDict"],
                id="from_import_multiple",
            ),
            pytest.param(
                "from typing import List as L",
                ["from typing import List as L"],
                id="from_import_aliased",
            ),
            pytest.param(
                "from math import *",
                ["from math import *"],
                id="from_import_wildcard",
            ),
            pytest.param(
                "import os.path",
                ["import os.path"],
                id="dotted_import",
            ),
            pytest.param(
                "from google.cloud import bigquery",
                ["from google.cloud import bigquery"],
                id="from_dotted_module",
            ),
            pytest.param(
                "",
                [],
                id="no_imports",
            ),
            pytest.param(
                "class MyClass:\n    import json # Should not be picked up",
                [],
                id="import_inside_class",
            ),
            pytest.param(
                "def my_func():\n    from time import sleep # Should not be picked up",
                [],
                id="import_inside_function",
            ),
        ],
    )
    def test_import_extraction(self, code_snippet, expected_imports):
        analyzer = CodeAnalyzer()
        tree = ast.parse(code_snippet)
        analyzer.visit(tree)

        # Normalize for comparison
        extracted = sorted(list(analyzer.imports))
        expected = sorted(expected_imports)

        assert extracted == expected


# --- Tests CodeAnalyzer handling of Attributes ---


class TestCodeAnalyzerAttributes:
    @pytest.mark.parametrize(
        "code_snippet, expected_analyzed_classes",
        [
            pytest.param(
                """
class MyClass:
    CLASS_VAR = 123
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [],
                        "attributes": [{"name": "CLASS_VAR", "type": None}],
                    }
                ],
                id="class_var_assign",
            ),
            pytest.param(
                """
class MyClass:
    class_var: int = 456
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [],
                        "attributes": [{"name": "class_var", "type": "int"}],
                    }
                ],
                id="class_var_annassign",
            ),
            pytest.param(
                """
class MyClass:
    class_var: int
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [],
                        "attributes": [{"name": "class_var", "type": "int"}],
                    }
                ],
                id="class_var_annassign_no_value",
            ),
            pytest.param(
                """
class MyClass:
    def __init__(self):
        self.instance_var = 789
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [
                            {
                                "method_name": "__init__",
                                "args": [{"name": "self", "type": None}],
                                "return_type": None,
                            }
                        ],
                        "attributes": [{"name": "instance_var", "type": None}],
                    }
                ],
                id="instance_var_assign",
            ),
            pytest.param(
                """
class MyClass:
    def __init__(self):
        self.instance_var: str = 'hello'
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [
                            {
                                "method_name": "__init__",
                                "args": [{"name": "self", "type": None}],
                                "return_type": None,
                            }
                        ],
                        "attributes": [{"name": "instance_var", "type": "str"}],
                    }
                ],
                id="instance_var_annassign",
            ),
            pytest.param(
                """
class MyClass:
    def __init__(self):
        self.instance_var: str
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [
                            {
                                "method_name": "__init__",
                                "args": [{"name": "self", "type": None}],
                                "return_type": None,
                            }
                        ],
                        "attributes": [{"name": "instance_var", "type": "str"}],
                    }
                ],
                id="instance_var_annassign_no_value",
            ),
            pytest.param(
                """
class MyClass:
    VAR_A = 1
    var_b: int = 2
    def __init__(self):
        self.var_c = 3
        self.var_d: float = 4.0
""",
                [
                    {
                        "class_name": "MyClass",
                        "methods": [
                            {
                                "method_name": "__init__",
                                "args": [{"name": "self", "type": None}],
                                "return_type": None,
                            }
                        ],
                        "attributes": [
                            {"name": "VAR_A", "type": None},
                            {"name": "var_b", "type": "int"},
                            {"name": "var_c", "type": None},
                            {"name": "var_d", "type": "float"},
                        ],
                    }
                ],
                id="mixed_attributes",
            ),
            pytest.param(
                "a = 123 # Module level",
                [],
                id="module_level_assign",
            ),
            pytest.param(
                "b: int = 456 # Module level",
                [],
                id="module_level_annassign",
            ),
        ],
    )
    def test_attribute_extraction(
        self, code_snippet: str, expected_analyzed_classes: list
    ):
        """Tests the extraction of class and instance attributes."""
        analyzer = CodeAnalyzer()
        tree = ast.parse(code_snippet)
        analyzer.visit(tree)

        extracted = analyzer.analyzed_classes
        # Normalize attributes for order-independent comparison
        for item in extracted:
            if "attributes" in item:
                item["attributes"].sort(key=lambda x: x["name"])
        for item in expected_analyzed_classes:
            if "attributes" in item:
                item["attributes"].sort(key=lambda x: x["name"])

        assert extracted == expected_analyzed_classes
