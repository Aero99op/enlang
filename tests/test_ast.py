"""Unit tests for EnLang Universal AST Nodes."""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, LiteralNode, VariableNode,
    FunctionDefNode, FunctionCallNode, BinaryExpressionNode, LoopNode, ReturnNode
)

class TestASTNodes(unittest.TestCase):
    def test_assignment_ast(self):
        target = VariableNode("x", line_num=1)
        val = LiteralNode(10, "number", line_num=1)
        node = AssignmentNode(target, val, line_num=1)
        d = node.to_dict()
        self.assertEqual(d["type"], "AssignmentNode")
        self.assertEqual(d["target"]["name"], "x")
        self.assertEqual(d["value"]["value"], 10)

    def test_function_def_ast(self):
        params = [VariableNode("a"), VariableNode("b")]
        body = [ReturnNode(BinaryExpressionNode(VariableNode("a"), "+", VariableNode("b")))]
        func = FunctionDefNode("add", params=params, body=body, line_num=5)
        d = func.to_dict()
        self.assertEqual(d["type"], "FunctionDefNode")
        self.assertEqual(d["name"], "add")
        self.assertEqual(len(d["params"]), 2)
        self.assertEqual(d["body"][0]["type"], "ReturnNode")

    def test_program_ast(self):
        prog = ProgramNode([
            AssignmentNode(VariableNode("name"), LiteralNode("EnLang", "string")),
            DisplayNode(VariableNode("name"))
        ])
        d = prog.to_dict()
        self.assertEqual(d["type"], "ProgramNode")
        self.assertEqual(len(d["statements"]), 2)
        self.assertEqual(d["statements"][0]["type"], "AssignmentNode")
        self.assertEqual(d["statements"][1]["type"], "DisplayNode")

if __name__ == "__main__":
    unittest.main()
