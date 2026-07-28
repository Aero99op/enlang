"""CSS3 Stylesheet Target Emitter (.enlgd)."""
from .base_emitter import BaseEmitter
from ..parser.ast_nodes import StyleNode

class CSSEmitter(BaseEmitter):
    """Emits CSS3 stylesheet rules from styling AST nodes."""
    def emit(self, ast_node):
        self.output = []
        if isinstance(ast_node, StyleNode):
            self.emit_line(f"{ast_node.selector} {{")
            self.indent_level += 1
            for k, v in ast_node.rules.items():
                self.emit_line(f"{k}: {v};")
            self.indent_level -= 1
            self.emit_line("}")
        return "\n".join(self.output)
