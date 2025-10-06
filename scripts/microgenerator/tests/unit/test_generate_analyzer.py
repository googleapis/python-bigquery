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
from scripts.microgenerator.generate import parse_code, CodeAnalyzer


# --- Mock Types ---
class MyClass:
    pass


class AnotherClass:
    pass


class YetAnotherClass:
    pass


def test_codeanalyzer_finds_class():
    code = """
class MyClass:
    pass
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 1
    assert analyzer.structure[0]["class_name"] == "MyClass"


def test_codeanalyzer_finds_multiple_classes():
    code = """
class ClassA:
    pass


class ClassB:
    pass
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 2
    class_names = sorted([c["class_name"] for c in analyzer.structure])
    assert class_names == ["ClassA", "ClassB"]


def test_codeanalyzer_finds_method():
    code = """
class MyClass:
    def my_method(self):
        pass
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 1
    assert len(analyzer.structure[0]["methods"]) == 1
    assert analyzer.structure[0]["methods"][0]["method_name"] == "my_method"


def test_codeanalyzer_finds_multiple_methods():
    code = """
class MyClass:
    def method_a(self):
        pass

    def method_b(self):
        pass
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 1
    method_names = sorted([m["method_name"] for m in analyzer.structure[0]["methods"]])
    assert method_names == ["method_a", "method_b"]


def test_codeanalyzer_no_classes():
    code = """
def top_level_function():
    pass
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 0


def test_codeanalyzer_class_with_no_methods():
    code = """
class MyClass:
    attribute = 123
"""
    analyzer = CodeAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    assert len(analyzer.structure) == 1
    assert analyzer.structure[0]["class_name"] == "MyClass"
    assert len(analyzer.structure[0]["methods"]) == 0


# --- Test Data for Parameterization ---
TYPE_TEST_CASES = [
    pytest.param(
        """class TestClass:
    def func(self, a: int, b: str) -> bool: return True""",
        [("a", "int"), ("b", "str")],
        "bool",
        id="simple_types",
    ),
    pytest.param(
        """from typing import Optional
class TestClass:
    def func(self, a: Optional[int]) -> str | None: return 'hello'""",
        [("a", "Optional[int]")],
        "str | None",
        id="optional_union_none",
    ),
    pytest.param(
        """from typing import Union
class TestClass:
    def func(self, a: int | float, b: Union[str, bytes]) -> None: pass""",
        [("a", "int | float"), ("b", "Union[str, bytes]")],
        "None",
        id="union_types",
    ),
    pytest.param(
        """from typing import List, Dict, Tuple
class TestClass:
    def func(self, a: List[int], b: Dict[str, float]) -> Tuple[int, str]: return (1, 'a')""",
        [("a", "List[int]"), ("b", "Dict[str, float]")],
        "Tuple[int, str]",
        id="generic_types",
    ),
    pytest.param(
        """import datetime
from scripts.microgenerator.tests.unit.test_generate_analyzer import MyClass
class TestClass:
    def func(self, a: datetime.date, b: MyClass) -> MyClass: return b""",
        [("a", "datetime.date"), ("b", "MyClass")],
        "MyClass",
        id="imported_types",
    ),
    pytest.param(
        """from scripts.microgenerator.tests.unit.test_generate_analyzer import AnotherClass, YetAnotherClass
class TestClass:
    def func(self, a: 'AnotherClass') -> 'YetAnotherClass': return AnotherClass()""",
        [("a", "'AnotherClass'")],
        "'YetAnotherClass'",
        id="forward_refs",
    ),
    pytest.param(
        """class TestClass:
    def func(self, a, b): return a + b""",
        [("a", None), ("b", None)],  # No annotations means type is None
        None,
        id="no_annotations",
    ),
    pytest.param(
        """from typing import List, Optional, Dict, Union, Any
class TestClass:
    def func(self, a: List[Optional[Dict[str, Union[int, str]]]]) -> Dict[str, Any]: return {}""",
        [("a", "List[Optional[Dict[str, Union[int, str]]]]")],
        "Dict[str, Any]",
        id="complex_nested",
    ),
    pytest.param(
        """from typing import Literal
class TestClass:
    def func(self, a: Literal['one', 'two']) -> Literal[True]: return True""",
        [("a", "Literal['one', 'two']")],
        "Literal[True]",
        id="literal_type",
    ),
]


class TestCodeAnalyzerArgsReturns:
    @pytest.mark.parametrize(
        "code_snippet, expected_args, expected_return", TYPE_TEST_CASES
    )
    def test_type_extraction(self, code_snippet, expected_args, expected_return):
        structure, imports, types = parse_code(code_snippet)

        assert len(structure) == 1, "Should parse one class"
        class_info = structure[0]
        assert class_info["class_name"] == "TestClass"

        assert len(class_info["methods"]) == 1, "Should find one method"
        method_info = class_info["methods"][0]
        assert method_info["method_name"] == "func"

        # Extract args, skipping 'self'
        extracted_args = []
        for arg in method_info.get("args", []):
            if arg["name"] == "self":
                continue
            extracted_args.append((arg["name"], arg["type"]))

        assert extracted_args == expected_args
        assert method_info.get("return_type") == expected_return
