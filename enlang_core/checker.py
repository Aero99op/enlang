"""
EnLang Syntax Checker & Linter — UPGRADED v2.4.1
==================================================
Performs BOTH smart structural/indentation static analysis AND transpile-compile validation.

Phase 1: Smart Block & Indentation Stack Tracking (4-space rule, unexpected indents, dead code)
Phase 2: Syntax & Operator Linting (invalid keywords, missing 'to', '&&'/'||' check, bracket matching)
Phase 3: Transpile + Python compile() dry-run validation

Note: Raw embedded blocks (js:, css:, html:, python:, sql:) are treated as raw language content
and exempted from EnLang-specific 4-space indentation and keyword rules.
"""

import sys
import re
import os

# Fix Windows cp1252 terminal — allow full Unicode output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ANSI Color Tokens
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

class Diagnostic:
    def __init__(self, line_no: int, message: str, level: str = "ERROR", suggestion: str = "", code_snippet: str = ""):
        self.line_no = line_no
        self.message = message
        self.level = level  # ERROR, WARNING, INFO
        self.suggestion = suggestion
        self.code_snippet = code_snippet

    def __str__(self):
        lvl_color = RED if self.level == "ERROR" else (YELLOW if self.level == "WARNING" else CYAN)
        prefix = f"{lvl_color}[{self.level}]{RESET} Line {self.line_no}: {BOLD}{self.message}{RESET}"
        if self.code_snippet:
            prefix += f"\n         {DIM}|{RESET} {BOLD}Line {self.line_no}:{RESET}  {self.code_snippet}"
        if self.suggestion:
            prefix += f"\n         {GREEN}-> Suggestion:{RESET} {self.suggestion}"
        return prefix

def check_brackets_and_quotes(idx: int, line: str, diagnostics: list):
    """Checks for unclosed quotes or mismatched brackets (), [], {}."""
    double_quotes = line.count('"') - line.count('\\"')
    single_quotes = line.count("'") - line.count("\\'")
    if double_quotes % 2 != 0 or single_quotes % 2 != 0:
        diagnostics.append(Diagnostic(
            idx,
            "Unclosed string literal detected.",
            level="ERROR",
            suggestion="Ensure all string quotes ' or \" are properly closed.",
            code_snippet=line
        ))

    stack = []
    brackets = {')': '(', ']': '[', '}': '{'}
    for char in line:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != brackets[char]:
                diagnostics.append(Diagnostic(
                    idx,
                    f"Mismatched bracket '{char}'.",
                    level="ERROR",
                    suggestion=f"Check bracket alignment around '{char}'",
                    code_snippet=line
                ))
                break
            stack.pop()
    if stack:
        diagnostics.append(Diagnostic(
            idx,
            f"Unclosed bracket '{stack[-1]}'.",
            level="ERROR",
            suggestion=f"Close the bracket with '{dict((v,k) for k,v in brackets.items())[stack[-1]]}'",
            code_snippet=line
        ))

def check_syntax_patterns(idx: int, raw_line: str, line: str, diagnostics: list):
    """Performs static checks for common syntax errors and invalid natural language phrases."""
    
    # Check 1: Missing 'to' in variable assignment (e.g., 'set x 5')
    m_set_no_to = re.match(r'^\s*(?:set|let)\s+([a-zA-Z_]\w*)\s+([^to\s=].*)$', line, re.IGNORECASE)
    if m_set_no_to and not re.match(r'^\s*(?:set|let)\s+[a-zA-Z_]\w*\s+(?:to|=)\b', line, re.IGNORECASE):
        var, val = m_set_no_to.group(1), m_set_no_to.group(2)
        diagnostics.append(Diagnostic(
            idx,
            f"Missing 'to' in variable assignment statement.",
            level="ERROR",
            suggestion=f"Use 'set {var} to {val}'",
            code_snippet=line
        ))

    # Check 2: C-style logical operators '&&' or '||'
    if re.search(r'\b&&\b|\b\|\|\b', line):
        diagnostics.append(Diagnostic(
            idx,
            "C-style logical operator detected ('&&' or '||'). EnLang uses natural operators.",
            level="WARNING",
            suggestion="Replace '&&' with 'and', and '||' with 'or'",
            code_snippet=line
        ))

    # Check 3: Block header missing trailing colon ':'
    block_headers = (
        r'^\s*(?:if|otherwise\s+if|elif|else|repeat|for|while|until|function|func|action|task|procedure|process|class|interface|match|switch|try|except|finally|style|on\s+screen|animate)\b'
    )
    if re.search(block_headers, raw_line, re.IGNORECASE):
        if not line.endswith(":") and not re.search(r'\b(?:then|do)\b', line, re.IGNORECASE):
            diagnostics.append(Diagnostic(
                idx,
                "Block header missing trailing colon ':'.",
                level="ERROR",
                suggestion="Add a colon ':' at the end of the line (e.g. 'if x is 5:')",
                code_snippet=line
            ))

    # Check 4: Common typos in keywords
    typo_rules = [
        (r'^\s*funciton\b', "function"),
        (r'^\s*whlie\b', "while"),
        (r'^\s*otwerwise\b', "otherwise"),
        (r'^\s*retrun\b', "return"),
        (r'^\s*dipslay\b', "display"),
    ]
    for pattern, correct in typo_rules:
        if re.search(pattern, line, re.IGNORECASE):
            diagnostics.append(Diagnostic(
                idx,
                f"Possible typo in keyword detected.",
                level="ERROR",
                suggestion=f"Did you mean '{correct}'?",
                code_snippet=line
            ))

    # Check 5: Unsupported natural phrases
    invalid_phrases = [
        (r'\bis bigger than\b', "Use 'is greater than' instead of 'is bigger than'"),
        (r'\bis same as\b', "Use 'is equal to' instead of 'is same as'"),
        (r'\bassign\b.+\bto\b', "Use 'set <var> to <val>' or 'store <val> in <var>'"),
        (r'\bput\b.+\binside\b', "Use 'store <val> in <var>'"),
    ]
    for pattern, sugg in invalid_phrases:
        if re.search(pattern, line, re.IGNORECASE):
            diagnostics.append(Diagnostic(
                idx,
                "Unsupported natural phrase detected in statement.",
                level="ERROR",
                suggestion=sugg,
                code_snippet=line
            ))

def check_smart_indentation_and_structure(lines: list, diagnostics: list):
    """
    Smart structural analyzer:
    Exempts raw embedded blocks (js:, css:, html:, python:, sql:) from EnLang 4-space rules.
    """
    indent_stack = [0]
    
    inside_function = False
    function_indent_level = -1
    function_has_returned = False
    function_name = ""

    in_raw_block = False

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        # Check raw embedded block boundaries
        if re.match(r'^\s*(?:js|javascript|node|backend|css|html|python|sql)\s*:\s*$', line, re.IGNORECASE):
            in_raw_block = True
            continue

        if re.match(r'^\s*end\s+(?:js|javascript|node|backend|css|html|python|sql)\b', line, re.IGNORECASE):
            in_raw_block = False
            continue

        # Skip EnLang structural rules inside raw JS/CSS/HTML/SQL/Python blocks
        if in_raw_block:
            continue

        lstripped = raw_line.lstrip()
        current_indent = len(raw_line) - len(lstripped)

        # 1. EnLang 4-space rule
        if current_indent % 4 != 0:
            suggested_indent = round(current_indent / 4) * 4
            diagnostics.append(Diagnostic(
                idx,
                f"Indentation Error: Line is indented by {current_indent} spaces. EnLang requires 4-space multiples.",
                level="ERROR",
                suggestion=f"Re-indent line to {suggested_indent} spaces.",
                code_snippet=line
            ))

        check_brackets_and_quotes(idx, line, diagnostics)
        check_syntax_patterns(idx, raw_line, line, diagnostics)

        # 2. Scope & Function tracking
        m_func = re.match(r'^\s*(?:function|func)\s+([a-zA-Z_]\w*)', line, re.IGNORECASE)
        if m_func:
            inside_function = True
            function_name = m_func.group(1)
            function_indent_level = current_indent
            function_has_returned = False

        if inside_function and current_indent <= function_indent_level and not m_func:
            inside_function = False
            function_has_returned = False

        # 3. Detect Dead Code / Accidental Over-Indentation after 'return'
        if inside_function and function_has_returned:
            if current_indent > function_indent_level:
                diagnostics.append(Diagnostic(
                    idx,
                    f"Dead Code / Indentation Error: Statement '{line}' is indented inside function '{function_name}' after 'return'.",
                    level="ERROR",
                    suggestion=f"If this is top-level code, unindent to 0 spaces. Otherwise, move it above the 'return' statement inside '{function_name}'.",
                    code_snippet=line
                ))

        if re.match(r'^\s*return\b', line, re.IGNORECASE) and inside_function:
            function_has_returned = True

        # 4. Block Stack Alignment
        dedent_keywords_regex = r'^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b'
        is_dedent = bool(re.match(dedent_keywords_regex, line, re.IGNORECASE))
        
        if is_dedent:
            while len(indent_stack) > 1 and indent_stack[-1] > current_indent:
                indent_stack.pop()

        expected_indent = indent_stack[-1]

        if current_indent not in indent_stack and current_indent != expected_indent + 4:
            valid_indents_str = ", ".join(str(x) for x in sorted(set(indent_stack)))
            diagnostics.append(Diagnostic(
                idx,
                f"Unexpected Indentation Level ({current_indent} spaces). Expected one of valid block levels: [{valid_indents_str}] or {expected_indent + 4} spaces for a new block.",
                level="ERROR",
                suggestion=f"Adjust indentation to match enclosing block ({expected_indent} or {expected_indent + 4} spaces).",
                code_snippet=line
            ))
        else:
            while len(indent_stack) > 1 and current_indent < indent_stack[-1]:
                indent_stack.pop()

        if line.endswith(":") or re.search(r'\b(?:then|do)\b\s*:?$', line, re.IGNORECASE):
            indent_stack.append(current_indent + 4)

def _phase3_transpile_compile_check(code: str, file_path: str, diagnostics: list):
    """
    Phase 3: Transpile EnLang source to Python and run compile() dry-run.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from enlang_core.transpiler import EnLangTranspiler
        transpiler = EnLangTranspiler()
        py_code = transpiler.transpile(code, file_path)
    except Exception as te:
        diagnostics.append(Diagnostic(
            0,
            f"Transpiler Engine Failure: {te}",
            level="ERROR",
            suggestion="Review EnLang syntax against transpiler rules."
        ))
        return py_code if 'py_code' in dir() else ""

    try:
        compile(py_code, file_path, "exec")
    except SyntaxError as se:
        py_lines = py_code.splitlines()
        enlang_lines = code.splitlines()
        err_py_line = se.lineno or 0
        err_enlang_line = min(err_py_line, len(enlang_lines))

        bad_py = py_lines[err_py_line - 1].strip() if 0 < err_py_line <= len(py_lines) else "?"
        bad_enlang = enlang_lines[err_enlang_line - 1].strip() if err_enlang_line > 0 else "?"

        diagnostics.append(Diagnostic(
            err_enlang_line,
            f"Transpiled Python Syntax Error: '{bad_enlang}' generated Python '{bad_py}'",
            level="ERROR",
            suggestion=f"Python parser error: {se.msg}. Check statement structure.",
            code_snippet=bad_enlang
        ))
    return py_code

def check_syntax(code: str, file_path: str = "main.enlg") -> list:
    diagnostics = []
    lines = code.splitlines()

    check_smart_indentation_and_structure(lines, diagnostics)
    _phase3_transpile_compile_check(code, file_path, diagnostics)

    return diagnostics

def check_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"{RED}[ERROR] File '{file_path}' not found.{RESET}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    diagnostics = check_syntax(code, file_path)

    print(f"{CYAN}{'=' * 70}{RESET}")
    print(f"  {BOLD}EnLang Smart Syntax & Indentation Checker v2.4.1{RESET}  —  {file_path}")
    print(f"{CYAN}{'=' * 70}{RESET}")

    if not diagnostics:
        print(f"  {GREEN}{BOLD}[PASS] No syntax or indentation errors found! Clean file.{RESET}")
        print(f"{CYAN}{'=' * 70}{RESET}")
        return True

    errors = [d for d in diagnostics if d.level == "ERROR"]
    warnings = [d for d in diagnostics if d.level == "WARNING"]

    for d in diagnostics:
        print(f"  {d}\n")

    print(f"{CYAN}{'=' * 70}{RESET}")
    print(f"  {BOLD}Result:{RESET} {RED}{len(errors)} Error(s){RESET}, {YELLOW}{len(warnings)} Warning(s){RESET}")
    print(f"{CYAN}{'=' * 70}{RESET}")
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_file(sys.argv[1])
    else:
        print("Usage: python -m enlang_core.checker <filename.enlg>")
