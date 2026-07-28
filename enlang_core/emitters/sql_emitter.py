"""SQLite SQL Target Emitter (.enlgdb)."""
from .base_emitter import BaseEmitter
from ..parser.ast_nodes import TableNode

class SQLEmitter(BaseEmitter):
    """Emits SQLite schema queries from Table AST nodes."""
    def emit(self, ast_node):
        self.output = []
        if isinstance(ast_node, TableNode):
            cols_str = ", ".join([f"{c[0]} {c[1].upper()}" for c in ast_node.columns])
            self.emit_line(f"CREATE TABLE IF NOT EXISTS {ast_node.name} ({cols_str});")
        return "\n".join(self.output)
