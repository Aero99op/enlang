"""Python 3 Target Code Emitter (.enlg)."""
from .base_emitter import BaseEmitter
from ..parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, LiteralNode, VariableNode,
    FunctionDefNode, FunctionCallNode, BinaryExpressionNode, ReturnNode
)

class PythonEmitter(BaseEmitter):
    """Emits native Python 3 source code from AST."""
    def emit(self, ast_node):
        self.output = []
        if isinstance(ast_node, ProgramNode):
            for stmt in ast_node.statements:
                self._emit_stmt(stmt)
        return "\n".join(self.output)

    def _emit_stmt(self, node):
        if isinstance(node, AssignmentNode):
            val_str = self._emit_expr(node.value)
            target_str = node.target.name if isinstance(node.target, VariableNode) else str(node.target)
            self.emit_line(f"{target_str} = {val_str}")
        elif isinstance(node, DisplayNode):
            val_str = self._emit_expr(node.expression)
            self.emit_line(f"print({val_str})")
        elif isinstance(node, FunctionDefNode):
            params_str = ", ".join([p.name if isinstance(p, VariableNode) else str(p) for p in node.params])
            prefix = "async def" if node.is_async else "def"
            self.emit_line(f"{prefix} {node.name}({params_str}):")
            self.indent_level += 1
            if not node.body:
                self.emit_line("pass")
            else:
                for b_stmt in node.body:
                    self._emit_stmt(b_stmt)
            self.indent_level -= 1
        elif isinstance(node, ReturnNode):
            val_str = self._emit_expr(node.expression) if node.expression else ""
            self.emit_line(f"return {val_str}".strip())

    def _emit_expr(self, node):
        if isinstance(node, LiteralNode):
            if node.type_tag == "string":
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, VariableNode):
            return node.name
        elif isinstance(node, BinaryExpressionNode):
            left_str = self._emit_expr(node.left)
            right_str = self._emit_expr(node.right)
            return f"{left_str} {node.operator} {right_str}"
        return str(node)
