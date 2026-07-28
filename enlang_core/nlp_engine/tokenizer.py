"""Lexical Tokenizer and String Literal Protector for Preprocessing."""
import re

class PreprocessTokenizer:
    """Protects string literals and extracts normalized tokens."""
    def __init__(self):
        self.strings = []

    def protect_strings(self, text):
        self.strings = []
        def save_str(m):
            self.strings.append(m.group(0))
            return f"__STR_{len(self.strings)-1}__"
        return re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', save_str, text)

    def restore_strings(self, text):
        for idx, s in enumerate(self.strings):
            text = text.replace(f"__STR_{idx}__", s)
        return text
