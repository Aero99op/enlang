"""
EnLang Syntax Checker & Linter — UPGRADED v2.3.0
==================================================
Performs BOTH smart structural/indentation static analysis AND transpile-compile validation.

Phase 1: Smart Block & Indentation Stack Tracking (4-space rule, unexpected indents, dead code)
Phase 2: Syntax & Operator Linting (invalid keywords, missing 'to', '&&'/'||' check, bracket matching)
Phase 3: Transpile + Python compile() dry-run validation
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

    # Bracket matching
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

    # Check 6: Bare Action/Function Call Ambiguity
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
            suggestion_msg = f"Use 'call {action_word} with {arg_val}' for function calls, or 'display {arg_val}' for output."
            diagnostics.append(Diagnostic(
                idx,
                f"Unknown statement structure '{line}'. Functions must be invoked using 'call'.",
                level="ERROR",
                suggestion=suggestion_msg,
                code_snippet=line
            ))

def check_smart_indentation_and_structure(lines: list, diagnostics: list):
    """
    Smart structural analyzer:
    1. Enforces 4-space multiples.
    2. Maintains an indentation stack to check parent/child block alignment.
    3. Detects dead code / accidental over-indentation after return statements.
    4. Detects un-indentation to invalid levels.
    """
    indent_stack = [0]  # Stack of expected block indentation levels
    block_names = ["<root>"]
    
    # Un-indent keywords that match parent block level
    dedent_keywords_regex = r'^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b'
    
    # Function level tracking for dead code detection
    inside_function = False
    function_indent_level = -1
    function_has_returned = False
    function_name = ""

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        lstripped = raw_line.lstrip()
        current_indent = len(raw_line) - len(lstripped)

        # 1. Basic 4-space rule
        if current_indent % 4 != 0:
            suggested_indent = round(current_indent / 4) * 4
            diagnostics.append(Diagnostic(
                idx,
                f"Indentation Error: Line is indented by {current_indent} spaces. EnLang requires 4-space multiples.",
                level="ERROR",
                suggestion=f"Re-indent line to {suggested_indent} spaces.",
                code_snippet=line
            ))

        # Check bracket/string sanity
        check_brackets_and_quotes(idx, line, diagnostics)
        check_syntax_patterns(idx, raw_line, line, diagnostics)

        # 2. Scope & Function tracking
        m_func = re.match(r'^\s*(?:function|func)\s+([a-zA-Z_]\w*)', line, re.IGNORECASE)
        if m_func:
            inside_function = True
            function_name = m_func.group(1)
            function_indent_level = current_indent
            function_has_returned = False

        # If we un-indented back to or above the function level, function scope ended
        if inside_function and current_indent <= function_indent_level and not m_func:
            inside_function = False
            function_has_returned = False

        # 3. Detect Dead Code / Accidental Over-Indentation after 'return'
        if inside_function and function_has_returned:
            if current_indent > function_indent_level:
                diagnostics.append(Diagnostic(
                    idx,
                    f"Dead Code / Indentation Error: Statement '{line}' is indented inside function '{function_name}' after a 'return' statement.",
                    level="ERROR",
                    suggestion=f"If this is top-level code, unindent to 0 spaces. Otherwise, move it above the 'return' statement inside '{function_name}'.",
                    code_snippet=line
                ))

        if re.match(r'^\s*return\b', line, re.IGNORECASE) and inside_function:
            function_has_returned = True

        # 4. Block Stack Alignment
        # If line is a dedent keyword (else, elif, etc), it expects matching stack top - 4
        is_dedent = bool(re.match(dedent_keywords_regex, line, re.IGNORECASE))
        
        if is_dedent:
            # Pop deeper blocks
            while len(indent_stack) > 1 and indent_stack[-1] > current_indent:
                indent_stack.pop()
                if block_names: block_names.pop()

        expected_indent = indent_stack[-1]

        # Check if line's indent matches any valid parent scope
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
            # Update stack to current valid level
            while len(indent_stack) > 1 and current_indent < indent_stack[-1]:
                indent_stack.pop()
                if block_names: block_names.pop()

        # 5. Push new block level if line opens a block (ends with ':')
        if line.endswith(":") or re.search(r'\b(?:then|do)\b\s*:?$', line, re.IGNORECASE):
            indent_stack.append(current_indent + 4)
            block_names.append(line.split()[0])

def _phase3_transpile_compile_check(code: str, file_path: str, diagnostics: list):
    """
    Phase 3: Transpile EnLang source to Python and run compile() dry-run.
    Catches any deep runtime/transpiler errors missed by static analysis.
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

    # Run Phase 1 & 2: Smart Indentation & Static Pattern Checks
    check_smart_indentation_and_structure(lines, diagnostics)

    # Run Phase 3: Transpile & Python Compile Dry-Run
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
    print(f"  {BOLD}EnLang Smart Syntax & Indentation Checker v2.3.0{RESET}  —  {file_path}")
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
