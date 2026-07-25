"""
EnLang Syntax Checker & Linter
==============================
Performs static analysis and linting on EnLang source files (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb)
without executing them.

Checks:
  1. Indentation & Block boundary formatting (4-space rule)
  2. Trailing colon (:) on block headers
  3. Matched block closures (end match, end interface)
  4. Unclosed string literals
  5. Unsupported or ambiguous phrase warnings (e.g., 'is bigger than')
"""

import re
import os

class Diagnostic:
    def __init__(self, line_no: int, message: str, level: str = "ERROR", suggestion: str = ""):
        self.line_no = line_no
        self.message = message
        self.level = level  # ERROR, WARNING, INFO
        self.suggestion = suggestion

    def __str__(self):
        prefix = f"[{self.level}] Line {self.line_no}: {self.message}"
        if self.suggestion:
            prefix += f" (Suggestion: {self.suggestion})"
        return prefix

def check_syntax(code: str, file_path: str = "main.enlg") -> list:
    diagnostics = []
    lines = code.splitlines()

    in_match = False
    in_interface = False
    in_native_block = False

    block_headers = (
        r'^\s*(?:if|otherwise\s+if|elif|else|repeat|for|while|until|function|func|action|task|procedure|process|class|interface|match|switch|try|except|finally|style|on\s+screen|animate)\b'
    )

    invalid_phrases = [
        (r'\bis bigger than\b', "Use 'is greater than' instead of 'is bigger than'"),
        (r'\bis same as\b', "Use 'is equal to' instead of 'is same as'"),
        (r'\bassign\b.+\bto\b', "Use 'set <var> to <val>' or 'store <val> in <var>'"),
        (r'\bput\b.+\binside\b', "Use 'store <val> in <var>'"),
    ]

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        lstripped = raw_line.lstrip()
        indent_len = len(raw_line) - len(lstripped)

        # Check 1: Indentation (Must be multiple of 4 spaces if indented)
        if indent_len % 4 != 0:
            diagnostics.append(Diagnostic(
                idx,
                f"Indentation is {indent_len} spaces. EnLang requires multiples of 4 spaces.",
                level="WARNING",
                suggestion=f"Adjust indentation to {(indent_len // 4 + 1) * 4} spaces"
            ))

        # Check 2: Unclosed string literal
        double_quotes = line.count('"') - line.count('\\"')
        single_quotes = line.count("'") - line.count("\\'")
        if double_quotes % 2 != 0 or single_quotes % 2 != 0:
            diagnostics.append(Diagnostic(
                idx,
                "Unclosed string literal detected.",
                level="ERROR",
                suggestion="Ensure string quotes are closed properly"
            ))

        # Check 3: Block header missing trailing colon
        if re.search(block_headers, raw_line, re.IGNORECASE):
            if not line.endswith(":") and not re.search(r'\b(?:then|do)\b', line, re.IGNORECASE):
                diagnostics.append(Diagnostic(
                    idx,
                    "Block header missing trailing colon ':'.",
                    level="ERROR",
                    suggestion="Add a colon ':' at the end of the line"
                ))

        # Check 4: Unsupported English phrases
        for pattern, sugg in invalid_phrases:
            if re.search(pattern, line, re.IGNORECASE):
                diagnostics.append(Diagnostic(
                    idx,
                    f"Unsupported natural phrase detected in statement.",
                    level="ERROR",
                    suggestion=sugg
                ))

        # Block tracking
        if re.match(r'^\s*(?:match|switch)\b', line, re.IGNORECASE):
            in_match = True
        elif re.match(r'^\s*end\s+match\b', line, re.IGNORECASE):
            in_match = False

        if re.match(r'^\s*interface\b', line, re.IGNORECASE):
            in_interface = True
        elif re.match(r'^\s*end\s+interface\b', line, re.IGNORECASE):
            in_interface = False

    if in_match:
        diagnostics.append(Diagnostic(
            len(lines),
            "Unclosed 'match' block. Missing 'end match'.",
            level="ERROR",
            suggestion="Add 'end match' at the end of the match block"
        ))

    if in_interface:
        diagnostics.append(Diagnostic(
            len(lines),
            "Unclosed 'interface' block. Missing 'end interface'.",
            level="ERROR",
            suggestion="Add 'end interface' at the end of the interface block"
        ))

    return diagnostics

def check_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"[ERROR] File '{file_path}' not found.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    diagnostics = check_syntax(code, file_path)

    print("=" * 65)
    print(f"  EnLang Syntax Checker & Linter  —  {file_path}")
    print("=" * 65)

    if not diagnostics:
        print("  [PASS] No syntax errors or warnings found! Clean file.")
        print("=" * 65)
        return True

    errors = [d for d in diagnostics if d.level == "ERROR"]
    warnings = [d for d in diagnostics if d.level == "WARNING"]

    for d in diagnostics:
        print(f"  {d}")

    print("=" * 65)
    print(f"  Result: {len(errors)} Error(s), {len(warnings)} Warning(s)")
    print("=" * 65)
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_file(sys.argv[1])
    else:
        print("Usage: python -m enlang_core.checker <filename.enlg>")
