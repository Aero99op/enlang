"""
EnLang Syntax Checker & Linter — UPGRADED v2.2.7
==================================================
Performs BOTH static analysis AND transpile-compile validation on EnLang source files.

Phase 1: Static Analysis (indentation, block closure, unclosed strings, invalid phrases)
Phase 2: Transpile + Python compile() dry-run (catches ALL runtime transpiler/syntax errors)
"""

import sys
import re
import os

# Fix Windows cp1252 terminal — allow full Unicode output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class Diagnostic:
    def __init__(self, line_no: int, message: str, level: str = "ERROR", suggestion: str = ""):
        self.line_no = line_no
        self.message = message
        self.level = level  # ERROR, WARNING, INFO
        self.suggestion = suggestion

    def __str__(self):
        prefix = f"[{self.level}] Line {self.line_no}: {self.message}"
        if self.suggestion:
            prefix += f"\n         -> Suggestion: {self.suggestion}"
        return prefix

def _check_line(idx: int, raw_line: str, line: str, diagnostics: list):
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
    block_headers = (
        r'^\s*(?:if|otherwise\s+if|elif|else|repeat|for|while|until|function|func|action|task|procedure|process|class|interface|match|switch|try|except|finally|style|on\s+screen|animate)\b'
    )
    if re.search(block_headers, raw_line, re.IGNORECASE):
        if not line.endswith(":") and not re.search(r'\b(?:then|do)\b', line, re.IGNORECASE):
            diagnostics.append(Diagnostic(
                idx,
                "Block header missing trailing colon ':'.",
                level="ERROR",
                suggestion="Add a colon ':' at the end of the line"
            ))

    # Check 4: Unsupported English phrases
    invalid_phrases = [
        (r'\bis bigger than\b', "Use 'is greater than' instead of 'is bigger than'"),
        (r'\bis same as\b', "Use 'is equal to' instead of 'is same as'"),
        (r'\bassign\b.+\bto\b', "Use 'set <var> to <val>' or 'store <val> in <var>'"),
        (r'\bput\b.+\binside\b', "Use 'store <val> in <var>'"),
        # Hallucination patterns — phrases AI generates that aren't supported
        (r'\binsert\b.+\bat\s+the\s+beginning\s+of\b', None),  # valid now, skip
    ]
    for pattern, sugg in invalid_phrases:
        if sugg is None:
            continue  # valid syntax, skip warning
        if re.search(pattern, line, re.IGNORECASE):
            diagnostics.append(Diagnostic(
                idx,
                "Unsupported natural phrase detected in statement.",
                level="ERROR",
                suggestion=sugg
            ))

    # Check 5: Bare Action/Function Call Ambiguity
    m_bare = re.match(r'^\s*([a-zA-Z_]\w*)\s+((["\'].+?["\'])|([a-zA-Z_]\w*|\d+))\s*$', line, re.IGNORECASE)
    if m_bare:
        action_word = m_bare.group(1)
        arg_val = m_bare.group(2)
        valid_keywords = {
            'set', 'store', 'save', 'put', 'get', 'call', 'run', 'execute', 'start', 'return',
            'import', 'from', 'create', 'define', 'let', 'var', 'if', 'else', 'elif', 'while',
            'for', 'repeat', 'function', 'func', 'class', 'match', 'switch', 'case', 'default',
            'try', 'except', 'finally', 'display', 'print', 'show', 'log', 'say', 'output',
            'write', 'connect', 'include', 'use', 'page', 'theme', 'style', 'animate',
            'add', 'append', 'push', 'insert', 'place', 'remove', 'sort', 'reverse',
            'increment', 'decrement', 'convert', 'cast', 'join', 'split', 'trim',
            'check', 'fetch', 'hash', 'read', 'break', 'continue', 'pass', 'raise', 'throw',
        }
        if action_word.lower() not in valid_keywords:
            suggestion_msg = (
                f"\n\n  Did you mean one of these?\n"
                f"    • display {arg_val}\n"
                f"    • call {action_word} with {arg_val}\n"
                f"    • function {action_word} with message:"
            )
            diagnostics.append(Diagnostic(
                idx,
                f"Unknown statement '{line}'. Use 'call {action_word} with ...' for function calls.",
                level="ERROR",
                suggestion=suggestion_msg
            ))

def _phase2_transpile_compile_check(code: str, file_path: str, diagnostics: list):
    """
    Phase 2: Actually transpile the EnLang source to Python, then run compile()
    on the generated Python to catch ALL errors the static checker misses.
    """
    try:
        # Import transpiler inline to avoid circular deps at module level
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from enlang_core.transpiler import EnLangTranspiler
        transpiler = EnLangTranspiler()
        py_code = transpiler.transpile(code, file_path)
    except Exception as te:
        diagnostics.append(Diagnostic(
            0,
            f"Transpiler crashed: {te}",
            level="ERROR",
            suggestion="Check your EnLang syntax — there may be an untranslatable construct."
        ))
        return py_code if 'py_code' in dir() else ""

    # Now try to compile the generated Python code
    try:
        compile(py_code, file_path, "exec")
    except SyntaxError as se:
        # Map generated Python line back to user's EnLang line (best-effort)
        py_lines = py_code.splitlines()
        enlang_lines = code.splitlines()
        err_py_line = se.lineno or 0
        err_enlang_line = min(err_py_line, len(enlang_lines))

        # Find the offending generated line for clarity
        bad_py = py_lines[err_py_line - 1].strip() if 0 < err_py_line <= len(py_lines) else "?"
        bad_enlang = enlang_lines[err_enlang_line - 1].strip() if err_enlang_line > 0 else "?"

        diagnostics.append(Diagnostic(
            err_enlang_line,
            f"Transpile/Runtime Error: '{bad_enlang}' → generated invalid Python: '{bad_py}'",
            level="ERROR",
            suggestion=(
                f"This EnLang syntax has no matching transpiler rule. "
                f"Check valid syntax in: transpiler.py / grammar.py\n"
                f"         Python error: {se.msg}"
            )
        ))
    return py_code

def check_syntax(code: str, file_path: str = "main.enlg") -> list:
    diagnostics = []
    lines = code.splitlines()

    in_match = False
    in_interface = False

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        _check_line(idx, raw_line, line, diagnostics)

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
            f"Unclosed 'match' block in {file_path}. Missing 'end match'.",
            level="ERROR",
            suggestion="Add 'end match' at the end of the match block"
        ))

    if in_interface:
        diagnostics.append(Diagnostic(
            len(lines),
            f"Unclosed 'interface' block in {file_path}. Missing 'end interface'.",
            level="ERROR",
            suggestion="Add 'end interface' at the end of the interface block"
        ))

    # Phase 2: Transpile + compile dry-run (catches what Phase 1 misses)
    _phase2_transpile_compile_check(code, file_path, diagnostics)

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
