"""Hierarchical Symbol Table for EnLang Scope Management."""

class Symbol:
    """Represents a symbol (variable or function) in the symbol table."""
    def __init__(self, name, sym_type="variable", declared_line=0):
        self.name = name
        self.sym_type = sym_type  # 'variable', 'function'
        self.declared_line = declared_line

class Scope:
    """Represents a lexical scope containing symbols and parent reference."""
    def __init__(self, name="global", parent=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        curr = self
        while curr is not None:
            if name in curr.symbols:
                return curr.symbols[name]
            curr = curr.parent
        return None

class SymbolTable:
    """Manages hierarchical scope stack during semantic analysis."""
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope

    def push_scope(self, name):
        self.current_scope = Scope(name, parent=self.current_scope)
        return self.current_scope

    def pop_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    def define(self, name, sym_type="variable", line=0):
        sym = Symbol(name, sym_type, line)
        self.current_scope.define(sym)
        return sym

    def lookup(self, name):
        return self.current_scope.lookup(name)
