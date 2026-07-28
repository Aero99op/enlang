"""Unit tests for EnLang Constant Folder and Dead Code Eliminator."""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.optimizer.constant_folder import ConstantFolder
from enlang_core.optimizer.dead_code import DeadCodeEliminator
from enlang_core.parser.ast_nodes import BinaryExpressionNode, LiteralNode
from enlang_core.ir.ir_nodes import IRBlock, IRInstruction

class TestOptimizer(unittest.TestCase):
    def test_constant_folding(self):
        expr = BinaryExpressionNode(LiteralNode(10, 'number'), '+', LiteralNode(20, 'number'))
        folded = ConstantFolder.fold_ast(expr)
        self.assertIsInstance(folded, LiteralNode)
        self.assertEqual(folded.value, 30)

    def test_dead_code_elimination(self):
        block = IRBlock("test")
        block.append(IRInstruction("LOAD_VAL", dest="%t1", arg1=10))
        block.append(IRInstruction("RET", arg1="%t1"))
        block.append(IRInstruction("LOAD_VAL", dest="%t2", arg1=999))  # Unreachable
        opt_block = DeadCodeEliminator.eliminate_block(block)
        self.assertEqual(len(opt_block.instructions), 2)
        self.assertEqual(opt_block.instructions[-1].op, "RET")

if __name__ == "__main__":
    unittest.main()
