"""Unit tests for EnLang Modular Target Code Emitters."""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.emitters.python_emitter import PythonEmitter
from enlang_core.emitters.html_emitter import HTMLEmitter
from enlang_core.emitters.css_emitter import CSSEmitter
from enlang_core.emitters.js_emitter import JSEmitter
from enlang_core.emitters.sql_emitter import SQLEmitter
from enlang_core.parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, LiteralNode, VariableNode,
    CreateElementNode, StyleNode, TableNode
)

class TestModularEmitters(unittest.TestCase):
    def test_python_emitter(self):
        prog = ProgramNode([
            AssignmentNode(VariableNode("x"), LiteralNode(100, "number")),
            DisplayNode(VariableNode("x"))
        ])
        py = PythonEmitter().emit(prog)
        self.assertIn("x = 100", py)
        self.assertIn("print(x)", py)

    def test_html_emitter(self):
        node = CreateElementNode("button", name="Click Me", attributes={"class": "btn", "id": "myBtn"})
        html = HTMLEmitter().emit(node)
        self.assertIn("<button", html)
        self.assertIn('class="btn"', html)
        self.assertIn("Click Me</button>", html)

    def test_css_emitter(self):
        node = StyleNode(".hero", rules={"background": "#000", "padding": "20px"})
        css = CSSEmitter().emit(node)
        self.assertIn(".hero {", css)
        self.assertIn("background: #000;", css)

    def test_js_emitter(self):
        node = AssignmentNode(VariableNode("msg"), LiteralNode("Hello", "string"))
        js = JSEmitter().emit(node)
        self.assertIn('let msg = "Hello";', js)

    def test_sql_emitter(self):
        node = TableNode("users", columns=[("id", "integer"), ("name", "text")])
        sql = SQLEmitter().emit(node)
        self.assertIn("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT);", sql)

if __name__ == "__main__":
    unittest.main()
