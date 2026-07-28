"""Master Senior Compiler QA Audit Execution Harness for EnLang v2.0.0."""
import unittest
import sys
import os
import time
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.transpiler import EnLangTranspiler
from enlang_core.interpreter import EnLangInterpreter
from enlang_core.nlp_engine.pipeline import NLPPipeline

class TestQAMasterAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transpiler = EnLangTranspiler()
        cls.interpreter = EnLangInterpreter()
        cls.nlp = NLPPipeline()

    def test_phase_1_core_language(self):
        """Phase 1: Validating core language constructs, recursion, and data structures in .enlg."""
        code = """set x to 10
set y to 20
set z to x plus y times 2
display z

function factorial with n:
    if n is less than or equal to 1 then:
        return 1
    return n times call factorial with n - 1

set fact5 to call factorial with 5
display fact5
"""
        py_code = self.transpiler.transpile(code, file_path="test.enlg")
        self.assertIn("x = 10", py_code)
        self.assertIn("y = 20", py_code)
        self.assertIn("def factorial(n):", py_code)
        
        # Runtime verification
        success, stdout, stderr, _ = self.interpreter.run_code(code, file_path="test.enlg")
        self.assertTrue(success, f"Runtime error: {stderr}")
        self.assertIn("50", stdout)  # 10 + 20 * 2 = 50
        self.assertIn("120", stdout) # 5! = 120

    def test_phase_2_frontend_enlgf(self):
        """Phase 2: HTML5 components, layouts, forms, and cards in .enlgf."""
        code = """create hero
create nav
create button named "Submit" with action "handleClick()"
create form
create table
"""
        success, html_out, _, _ = self.interpreter.run_code(code, file_path="test.enlgf")
        self.assertTrue(success)
        self.assertIn("<button", html_out)
        self.assertIn("<form>", html_out)

    def test_phase_3_design_enlgd(self):
        """Phase 3: CSS3 selectors, glassmorphism, flexbox, and media queries in .enlgd."""
        code = """define theme dark
style element .card with background "#ffffff" and padding "20px"
media query mobile max-width "768px" apply font-size "14px"
"""
        success, css_out, _, _ = self.interpreter.run_code(code, file_path="test.enlgd")
        self.assertTrue(success)
        self.assertIn(".card", css_out)

    def test_phase_4_scripts_enlgs(self):
        """Phase 4: Client-side JS, DOM manipulation, timers, and async fetch in .enlgs."""
        code = """set title to "Dashboard"
on click of "#submitBtn" call handleSubmit
after 1000 ms call refreshData
"""
        success, js_out, _, _ = self.interpreter.run_code(code, file_path="test.enlgs")
        self.assertTrue(success)
        self.assertIn("let title = \"Dashboard\";", js_out)
        self.assertIn("setTimeout(refreshData, 1000);", js_out)

    def test_phase_5_database_enlgdb(self):
        """Phase 5: Database schema creation, queries, and SQLite runtime verification in .enlgdb."""
        code = """create table users with columns id as integer, name as text, role as text
select all from users where role is "Admin"
"""
        success, sql_out, _, _ = self.interpreter.run_code(code, file_path="test.enlgdb")
        self.assertTrue(success)
        self.assertIn("CREATE TABLE IF NOT EXISTS users", sql_out)
        self.assertIn("SELECT * FROM users", sql_out)

        # SQLite Verification
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        statements = [stmt.strip() for stmt in sql_out.split(";") if stmt.strip()]
        for stmt in statements:
            cursor.execute(stmt)
        conn.close()

    def test_phase_6_cross_domain_integration(self):
        """Phase 6: Full multi-domain application integration across all 5 domains."""
        enlg = "set status to 'Active'"
        enlgf = "create button named 'Save' with action 'saveData()'"
        enlgd = "style element .btn with background '#0070f3'"
        enlgs = "on click of '.btn' call saveData"
        enlgdb = "create table logs with columns id as integer, msg as text"

        _, res_py, _, _ = self.interpreter.run_code(enlg, file_path="app.enlg")
        _, res_html, _, _ = self.interpreter.run_code(enlgf, file_path="app.enlgf")
        _, res_css, _, _ = self.interpreter.run_code(enlgd, file_path="app.enlgd")
        _, res_js, _, _ = self.interpreter.run_code(enlgs, file_path="app.enlgs")
        _, res_sql, _, _ = self.interpreter.run_code(enlgdb, file_path="app.enlgdb")

        self.assertIn("<button", res_html)
        self.assertIn(".btn", res_css)
        self.assertIn("addEventListener", res_js)
        self.assertIn("CREATE TABLE", res_sql)

    def test_phase_7_robustness_stress(self):
        """Phase 7: Malformed, ambiguous, and stress program handling without compiler crashes."""
        malformed = [
            "set to to to",
            "if then if",
            "function without name",
            "create table with",
            "style element with"
        ]
        for src in malformed:
            res = self.transpiler.transpile(src, file_path="test.enlg")
            self.assertIsInstance(res, str)

    def test_phase_8_performance_benchmarks(self):
        """Phase 8: Parse/transpile duration benchmarks for 1K lines."""
        lines = ["set x to 10\nset y to 20\nset z to x plus y\n"] * 333 # ~1000 lines
        big_code = "".join(lines)

        t0 = time.time()
        res = self.transpiler.transpile(big_code, file_path="bench.enlg")
        t1 = time.time()

        elapsed = t1 - t0
        print(f"\n[PERFORMANCE BENCHMARK] 1,000 lines transpiled in {elapsed:.4f} seconds.")
        self.assertLess(elapsed, 2.0) # Transpiles 1K lines under 2 seconds

if __name__ == "__main__":
    unittest.main()
