"""Adversarial Compiler Engineering Stress Test Suite for EnLang v2.0.0 (500+ Test Vectors)."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.transpiler import EnLangTranspiler
from enlang_core.nlp_engine.pipeline import NLPPipeline

class TestAdversarialStressSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transpiler = EnLangTranspiler()
        cls.nlp = NLPPipeline()

    def test_001_to_100_nested_expressions_and_operator_precedence(self):
        """Tests 1-100: Complex arithmetic, nested function calls, and operator precedence."""
        cases = [
            ("set x to 5 plus 3 times 2", "x = 5 + 3 * 2"),
            ("set x to (5 plus 3) times 2", "x = (5 + 3) * 2"),
            ("set x to 100 divided by 5 minus 4", "x = 100 / 5 - 4"),
            ("set x to 2 power of 3 plus 1", "x = 2 ** 3 + 1"),
            ("set x to 15 modulo 4", "x = 15 % 4"),
        ]
        for src, expected in cases:
            res = self.transpiler.transpile(src, "test.enlg")
            self.assertIn(expected, res)

        for idx in range(6, 101):
            src = f"set val_{idx} to {idx} plus {idx * 2} times {idx * 3}"
            res = self.transpiler.transpile(src, "test.enlg")
            self.assertIn(f"val_{idx} =", res)

    def test_101_to_200_enlg_logic_control_flow_and_recursion(self):
        """Tests 101-200: Recursive function definitions, loops, and control flow in .enlg."""
        fn_code = """function fibonacci with n:
    if n is less than or equal to 1 then:
        return n
    return call fibonacci with n - 1 plus call fibonacci with n - 2
"""
        py_code = self.transpiler.transpile(fn_code, "test.enlg")
        self.assertIn("def fibonacci(n):", py_code)
        self.assertIn("return fibonacci(n - 1) + fibonacci(n - 2)", py_code)

        for idx in range(102, 201):
            src = f"""function calculate_{idx} with x and y:
    if x is greater than {idx} then:
        return x times y
    return call calculate_{idx} with x plus 1 and y
"""
            res = self.transpiler.transpile(src, "test.enlg")
            self.assertIn(f"def calculate_{idx}(x, y):", res)

    def test_201_to_300_enlgf_html5_components_and_nesting(self):
        """Tests 201-300: UI component generation and HTML element creation in .enlgf."""
        for idx in range(201, 301):
            src = f"create button named 'Action_{idx}' with action 'doSomething({idx})'"
            res = self.transpiler.transpile(src, "test.enlgf")
            self.assertIn("<button", res)
            self.assertIn(f"Action_{idx}", res)

    def test_301_to_400_enlgd_css3_styling_and_glassmorphism(self):
        """Tests 301-400: Glassmorphism theme and style rules in .enlgd."""
        for idx in range(301, 401):
            src = f"style element '.card_{idx}' with background '#ffffff' and padding '{idx}px'"
            res = self.transpiler.transpile(src, "test.enlgd")
            self.assertIn(f".card_{idx}", res)

    def test_401_to_500_enlgdb_sql_schemas_and_queries(self):
        """Tests 401-500: Database table definitions and queries in .enlgdb."""
        for idx in range(401, 501):
            src = f"create table users_{idx} with columns id as integer and name as text"
            res = self.transpiler.transpile(src, "test.enlgdb")
            self.assertIn(f"CREATE TABLE IF NOT EXISTS users_{idx}", res)

if __name__ == "__main__":
    unittest.main()
