import ast
from autogen.scripts.microgenerator.generate import CodeAnalyzer


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
