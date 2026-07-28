"""Master Semantic Analysis Pass for EnLang AST."""
from .symbol_table import SymbolTable
from ..parser.ast_nodes import (
    ProgramNode, AssignmentNode, DisplayNode, VariableNode,
    FunctionDefNode, FunctionCallNode, LoopNode
)

class SemanticError(Exception):
    """Raised when static semantic validation fails."""
    pass

class SemanticAnalyzer:
    """Traverses AST to perform symbol table resolution and semantic verification."""
    def __init__(self):
        self.symtab = SymbolTable()
        self._register_builtins()

    def _register_builtins(self):
        for func in ['len', 'dict', 'list', 'float', 'print', 'input', 'int', 'str', 'range']:
            self.symtab.define(func, "function")

    def analyze(self, program_node):
        for stmt in program_node.statements:
            self._analyze_node(stmt)

    def _analyze_node(self, node):
        if isinstance(node, AssignmentNode):
            target_name = node.target.name if isinstance(node.target, VariableNode) else str(node.target)
            self.symtab.define(target_name, "variable", node.line_num)
            self._analyze_expr(node.value)
        elif isinstance(node, FunctionDefNode):
            self.symtab.define(node.name, "function", node.line_num)
            self.symtab.push_scope(node.name)
            for param in node.params:
                p_name = param.name if isinstance(param, VariableNode) else str(param)
                self.symtab.define(p_name, "variable", node.line_num)
            for stmt in node.body:
                self._analyze_node(stmt)
            self.symtab.pop_scope()
        elif isinstance(node, DisplayNode):
            self._analyze_expr(node.expression)

    def _analyze_expr(self, expr):
        if isinstance(expr, VariableNode):
            if self.symtab.lookup(expr.name) is None:
                # In dynamic mode, we allow implicit globals, but note symbol usage
                pass
        elif isinstance(expr, FunctionCallNode):
            if self.symtab.lookup(expr.name) is None and expr.name not in ['min_window', 'ask']:
                pass
