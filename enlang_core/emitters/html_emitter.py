"""HTML5 Markup Target Emitter (.enlgf)."""
from .base_emitter import BaseEmitter
from ..parser.ast_nodes import CreateElementNode

class HTMLEmitter(BaseEmitter):
    """Emits clean semantic HTML5 markup from frontend AST nodes."""
    def emit(self, ast_node):
        self.output = []
        if isinstance(ast_node, CreateElementNode):
            tag_map = {
                "hero": "section", "nav": "nav", "button": "button",
                "form": "form", "table": "table", "card": "div", "footer": "footer"
            }
            html_tag = tag_map.get(ast_node.tag.lower(), "div")
            attr_str = ""
            for k, v in ast_node.attributes.items():
                attr_str += f' {k}="{v}"'
            self.emit_line(f"<{html_tag}{attr_str}>{ast_node.name or ''}</{html_tag}>")
        return "\n".join(self.output)
