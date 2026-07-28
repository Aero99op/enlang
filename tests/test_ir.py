"""Unit tests for EnLang Intermediate Representation (IR) Layer."""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.ir.ir_builder import IRBuilder
from enlang_core.parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, LiteralNode, VariableNode,
    BinaryExpressionNode, ReturnNode
)

class TestIRLayer(unittest.TestCase):
    def test_ir_build_program(self):
        prog = ProgramNode([
            AssignmentNode(VariableNode("x"), LiteralNode(10, "number")),
            AssignmentNode(VariableNode("y"), BinaryExpressionNode(VariableNode("x"), "+", LiteralNode(5, "number"))),
            DisplayNode(VariableNode("y"))
        ])
        builder = IRBuilder()
        block = builder.build_program(prog)
        self.assertEqual(block.label, "main")
        self.assertGreater(len(block.instructions), 0)
        # Verify STORE instruction generated for variable assignment
        store_ops = [i for i in block.instructions if i.op == "STORE"]
        self.assertEqual(len(store_ops), 2)
        print_ops = [i for i in block.instructions if i.op == "PRINT"]
        self.assertEqual(len(print_ops), 1)

if __name__ == "__main__":
    unittest.main()
