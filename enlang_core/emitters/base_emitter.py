"""Abstract Base Interface for EnLang Target Code Emitters."""

class BaseEmitter:
    """Abstract emitter interface for converting AST/IR to target backend code."""
    def __init__(self):
        self.indent_level = 0
        self.output = []

    def indent(self):
        return "    " * self.indent_level

    def emit_line(self, line=""):
        if line:
            self.output.append(self.indent() + line)
        else:
            self.output.append("")

    def emit(self, ast_or_ir):
        raise NotImplementedError("Each emitter must implement the emit() method.")
