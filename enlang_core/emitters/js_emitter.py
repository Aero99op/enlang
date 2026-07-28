"""JavaScript ES6+ Target Emitter (.enlgs)."""
from .base_emitter import BaseEmitter
from ..parser.ast_nodes import AssignmentNode, DisplayNode, LiteralNode, VariableNode

class JSEmitter(BaseEmitter):
    """Emits ES6+ JavaScript code from AST nodes."""
    def emit(self, ast_node):
        self.output = []
        if isinstance(ast_node, AssignmentNode):
            target_str = ast_node.target.name if isinstance(ast_node.target, VariableNode) else str(ast_node.target)
            val_str = ast_node.value.value if isinstance(ast_node.value, LiteralNode) else str(ast_node.value)
            if isinstance(val_str, str) and not val_str.isdigit():
                val_str = f'"{val_str}"'
            self.emit_line(f"let {target_str} = {val_str};")
        elif isinstance(ast_node, DisplayNode):
            val_str = ast_node.expression.name if isinstance(ast_node.expression, VariableNode) else str(ast_node.expression)
            self.emit_line(f"console.log({val_str});")
        return "\n".join(self.output)
