"""AST to Intermediate Representation (IR) Builder."""
from .ir_nodes import IRInstruction, IRBlock, IRFunction
from ..parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, LiteralNode, VariableNode,
    FunctionDefNode, FunctionCallNode, BinaryExpressionNode, ReturnNode
)

class IRBuilder:
    """Converts AST nodes into backend-agnostic IR blocks and instructions."""
    def __init__(self):
        self.temp_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"%t{self.temp_counter}"

    def build_program(self, program_node):
        main_block = IRBlock(label="main")
        for stmt in program_node.statements:
            self._build_stmt(stmt, main_block)
        return main_block

    def _build_stmt(self, node, block):
        if isinstance(node, AssignmentNode):
            val_reg = self._build_expr(node.value, block)
            target_name = node.target.name if isinstance(node.target, VariableNode) else str(node.target)
            block.append(IRInstruction("STORE", dest=target_name, arg1=val_reg))
        elif isinstance(node, DisplayNode):
            val_reg = self._build_expr(node.expression, block)
            block.append(IRInstruction("PRINT", arg1=val_reg))
        elif isinstance(node, ReturnNode):
            if node.expression:
                val_reg = self._build_expr(node.expression, block)
                block.append(IRInstruction("RET", arg1=val_reg))
            else:
                block.append(IRInstruction("RET"))
        else:
            self._build_expr(node, block)

    def _build_expr(self, node, block):
        if isinstance(node, LiteralNode):
            res_reg = self.new_temp()
            block.append(IRInstruction("LOAD_VAL", dest=res_reg, arg1=node.value))
            return res_reg
        elif isinstance(node, VariableNode):
            res_reg = self.new_temp()
            block.append(IRInstruction("LOAD_VAR", dest=res_reg, arg1=node.name))
            return res_reg
        elif isinstance(node, BinaryExpressionNode):
            left_reg = self._build_expr(node.left, block)
            right_reg = self._build_expr(node.right, block)
            res_reg = self.new_temp()
            block.append(IRInstruction("BIN_OP", dest=res_reg, arg1=left_reg, arg2=f"{node.operator}:{right_reg}"))
            return res_reg
        return str(node)
