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
from scripts.microgenerator.generate import CodeAnalyzer


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
