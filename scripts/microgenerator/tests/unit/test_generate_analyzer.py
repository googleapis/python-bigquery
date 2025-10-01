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
