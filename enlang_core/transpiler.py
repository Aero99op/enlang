"""
EnLang Transpiler — Universal Multi-Target Code Generator
=========================================================
Maps EnLang source files to their native target language:

  .enlg            ->  Python 3
  .enlgf           ->  HTML5
  .enlgs           ->  JavaScript (ES6+)
  .enlgd           ->  CSS3
  .enlgdb          ->  SQL (SQLite compatible)

ZERO hardcoded values. Pure 1:1 natural English → native target translation.
"""

import re
import os
from enlang_core.ml_engine import translate_ml_line, reset_context as _ml_reset_context
from .grammar import (
    clean_expression, parse_args_list, _strip_trailing_colon,
    translate_html_line,
    translate_design_line,
    translate_script_line,
    translate_database_line,
)
from .nlp_engine import NLPParser


def _strip_quotes_local(s: str) -> str:
    """Local strip quotes helper for transpiler (avoids circular import)."""
    if s is None:
        return ''
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def _safe_concat_expr(expr: str) -> str:
    """Auto-wraps parts of string concat with str() for safe Python output if strings are involved."""
    if '+' not in expr or ',' in expr:
        return expr

    # Only apply string concatenation wrapping if a string literal exists in the expression
    has_string_literal = bool(re.search(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', expr))
    if not has_string_literal:
        return expr

    strings = []
    def save_str(m):
        strings.append(m.group(0))
        return f"__STR_{len(strings)-1}__"

    temp_expr = re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', save_str, expr)
    if '+' not in temp_expr:
        return expr

    parts = temp_expr.split('+')
    safe_parts = []
    for p in parts:
        p_str = p.strip()
        for idx, s in enumerate(strings):
            p_str = p_str.replace(f"__STR_{idx}__", s)
        if p_str.startswith('str(') and p_str.endswith(')'):
            safe_parts.append(p_str)
        else:
            safe_parts.append(f"str({p_str})")
    return " + ".join(safe_parts)


class EnLangTranspiler:
    def __init__(self):
        self.nlp_parser = NLPParser()
        self.reset()

    def reset(self):
        self.output_lines = []
        self.last_db_var = "db"

    def _join_multiline_sql_statements(self, raw_lines: list) -> list:
        """Accumulates multi-line statements in .enlgdb files into clean single-line queries."""
        joined = []
        current_stmt = []

        stmt_headers = (
            r'^(?:connect\s+to|create\s+table|define\s+table|insert\s+|execute\s+query|'
            r'select\s+|display\s+|drop\s+|add\s+column|rename\s+|delete\s+|create\s+index|'
            r'create\s+view|enable\s+foreign|begin|commit|rollback)\b'
        )

        for raw in raw_lines:
            s = raw.strip()
            if not s or s.startswith('#') or s.startswith('--'):
                if current_stmt:
                    joined.append(" ".join(current_stmt))
                    current_stmt = []
                joined.append(raw)
                continue

            if re.match(stmt_headers, s, re.IGNORECASE):
                if current_stmt:
                    joined.append(" ".join(current_stmt))
                    current_stmt = []
                current_stmt.append(s)
            else:
                if current_stmt:
                    current_stmt.append(s)
                else:
                    joined.append(raw)

        if current_stmt:
            joined.append(" ".join(current_stmt))

        return joined

    def transpile(self, source_code: str, file_path: str = "main.enlg") -> str:
        """
        Master transpile entry point.
        Detects the target language from file extension,
        then routes each line to the correct domain transpiler.

        Extension → Target:
          .enlg   → Python
          .enlgf  → HTML5
          .enlgd  → CSS3
          .enlgs  → JavaScript
          .enlgdb → SQL
        """
        self.reset()
        _ml_reset_context()  # Reset ML context for fresh transpile session
        ext = os.path.splitext(file_path)[1].lower() if file_path else ".enlg"
        if not ext:
            ext = ".enlg"

        raw_lines = source_code.splitlines()

        # ── Determine target from extension ───────────────────────────────
        if ext == ".enlgf":
            target = "html"
        elif ext == ".enlgd":
            target = "css"
        elif ext == ".enlgs":
            target = "js"
        elif ext == ".enlgdb":
            target = "sql"
        else:
            target = "python"   # .enlg and all other domains

        if target == "sql":
            raw_lines = self._join_multiline_sql_statements(raw_lines)

        in_native_block = False

        for raw_line in raw_lines:
            if not raw_line.strip():
                self.output_lines.append("")
                continue

            lstripped = raw_line.lstrip()
            indent = raw_line[:len(raw_line) - len(lstripped)]

            # ── Level 3: Native Block Start / End Detection ────────────────
            if not in_native_block:
                if re.match(r'^(?:python|js|javascript|sql|css|html)\s*:\s*$', lstripped, re.IGNORECASE):
                    in_native_block = True
                    self.output_lines.append(f"{indent}# --- start native block ---")
                    continue
            else:
                if re.match(r'^end\s+(?:python|js|javascript|sql|css|html|block|native)\s*$', lstripped, re.IGNORECASE):
                    in_native_block = False
                    self.output_lines.append(f"{indent}# --- end native block ---")
                    continue
                # Verbatim passthrough inside native block
                if target == "html":
                    self.output_lines.append(f'print({repr(raw_line)})')
                elif target == "css" or target == "js":
                    self.output_lines.append(f'print({repr(raw_line)})')
                elif target == "sql":
                    self.output_lines.append(f'print({repr(raw_line)})')
                else:
                    # Python target verbatim passthrough
                    self.output_lines.append(raw_line)
                continue

            # Comments are universal (except in CSS where # can be an ID selector)
            is_comment = False
            if target == "css":
                if lstripped.startswith("# ") or re.match(r'^(note:|comment:)', lstripped, re.IGNORECASE):
                    is_comment = True
            else:
                if lstripped.startswith("#") or re.match(r'^(note:|comment:)', lstripped, re.IGNORECASE):
                    is_comment = True

            if is_comment:
                comment_text = re.sub(r'^(note:|comment:)', '', lstripped, flags=re.IGNORECASE).strip()
                self.output_lines.append(f"{indent}# {comment_text}")
                continue

            # Route to correct target transpiler
            if target == "html":
                py_line = translate_html_line(lstripped)
                self.output_lines.append(py_line)
            elif target == "css":
                py_line = translate_design_line(lstripped)
                self.output_lines.append(py_line)
            elif target == "js":
                py_line = translate_script_line(lstripped)
                self.output_lines.append(py_line)
            elif target == "sql":
                m_db = re.match(r'^connect\s+to\s+database\s+(.+)\s+as\s+([a-zA-Z_]\w*)$', lstripped, re.IGNORECASE)
                if m_db:
                    self.last_db_var = m_db.group(2)
                py_line = translate_database_line(lstripped, self.last_db_var)
                self.output_lines.append(py_line)
            else:
                # Python target — preserve indentation
                m_db = re.match(r'^connect\s+to\s+database\s+(.+)\s+as\s+([a-zA-Z_]\w*)$', lstripped, re.IGNORECASE)
                if m_db:
                    self.last_db_var = m_db.group(2)
                # ── ML Engine first-pass (ADDITIVE — runs before all other rules) ──
                _ml_result = translate_ml_line(lstripped)
                if _ml_result is not None:
                    self.output_lines.append(f"{indent}{_ml_result}")
                    continue
                py_line = self._transpile_python_line(lstripped)

                # match/case/default/end match MUST emit at zero indent
                # because they become Python if/elif/else at the same scope level
                # NOTE: 'otherwise if' is NOT a match control (it's else-if in regular blocks)
                _is_match_control = re.match(
                    r'^(?:match|switch)\s|^case\s|^end\s+match\s*$|^default\s*:?\s*$',
                    lstripped, re.IGNORECASE
                )
                if _is_match_control:
                    self.output_lines.append(py_line)
                else:
                    self.output_lines.append(f"{indent}{py_line}")

        return "\n".join(self.output_lines)

    # ─────────────────────────────────────────────────────────────────────────
    # PYTHON TARGET  (.enlg)
    # ─────────────────────────────────────────────────────────────────────────

    def _normalize_natural_english_line(self, line: str) -> str:
        """Pre-normalizes common conversational variations into standard EnLang syntax before matching."""
        # 1. 'define function foo' / 'create function foo' -> 'function foo'
        line = re.sub(r'^\s*(?:define|create|make|build)\s+function\b', 'function', line, flags=re.IGNORECASE)
        # 2. 'repeat for each item in list:' -> 'for each item in list:'
        line = re.sub(r'^\s*repeat\s+for\s+each\b', 'for each', line, flags=re.IGNORECASE)
        # 3. 'log text: "msg"' / 'log text "msg"' -> 'display "msg"' in .enlg
        line = re.sub(r'^\s*log\s+text:?\s*', 'display ', line, flags=re.IGNORECASE)
        # 4. 'call function foo' / 'run function foo' -> 'call foo'
        line = re.sub(r'^\s*(call|run|execute|start)\s+(?:function|func|procedure)\s+', r'\1 ', line, flags=re.IGNORECASE)
        # 5. 'repeat until <cond>:' -> 'while not '
        line = re.sub(r'^\s*repeat\s+until\s+', 'while not ', line, flags=re.IGNORECASE)
        # 6. Natural divisibility & even/odd expressions
        line = re.sub(r'\b([a-zA-Z_]\w*|\d+)\s+is\s+not\s+divisible\s+by\s+([a-zA-Z_]\w*|\d+)\b', r'\1 % \2 != 0', line, flags=re.IGNORECASE)
        line = re.sub(r'\b([a-zA-Z_]\w*|\d+)\s+is\s+divisible\s+by\s+([a-zA-Z_]\w*|\d+)\b', r'\1 % \2 == 0', line, flags=re.IGNORECASE)
        line = re.sub(r'\b([a-zA-Z_]\w*|\d+)\s+is\s+even\b', r'\1 % 2 == 0', line, flags=re.IGNORECASE)
        line = re.sub(r'\b([a-zA-Z_]\w*|\d+)\s+is\s+odd\b', r'\1 % 2 != 0', line, flags=re.IGNORECASE)
        return line

    def _transpile_python_line(self, line: str) -> str:
        """Full EnLang → Python transpiler with NLP fallback."""
        line = self._normalize_natural_english_line(line.strip())

        has_colon = line.endswith(":")
        clean_line = line[:-1].strip() if has_colon else line

        # ── Import module EnLang syntax — MUST come before passthrough ────
        m = re.match(r'^import\s+module\s+([a-zA-Z_][\w.]*)(?:\s+as\s+([a-zA-Z_]\w*))?$', line, re.IGNORECASE)
        if m:
            mod, alias = m.group(1), m.group(2)
            return f"import {mod} as {alias}" if alias else f"import {mod}"

        m = re.match(r'^from\s+([a-zA-Z_][\w.]*)\s+import\s+(.+)$', line, re.IGNORECASE)
        if m:
            return f"from {m.group(1)} import {m.group(2)}"

        # ── v2.0: Optional Typed Variable Declaration ─────────────────────
        # MUST come before raw Python passthrough (define/let/var interception)
        m = re.match(r'^(?:define|let|var)\s+(number|decimal|text|boolean|list|array|dictionary|dict|map|set)\s+([a-zA-Z_]\w*)(?:\s+(?:as|=|is|to)\s+(.+))?$', line, re.IGNORECASE)
        if m:
            dtype, var, expr = m.group(1).lower(), m.group(2), m.group(3)
            if expr:
                val = clean_expression(expr)
                return f"{var} = {val}"
            defaults = {'number': '0', 'decimal': '0.0', 'text': '""', 'boolean': 'False',
                        'list': '[]', 'array': '[]', 'dictionary': '{}', 'dict': '{}', 'map': '{}', 'set': 'set()'}
            return f"{var} = {defaults.get(dtype, 'None')}"

        # ── v2.0: Pattern Matching (match / case / default / end match) ───
        m = re.match(r'^(?:match|switch)\s+(?:on\s+)?(.+?)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            expr = clean_expression(m.group(1))
            # First case becomes if, rest become elif — we use a sentinel
            return f"_match_val = {expr}; _match_hit = False"

        m = re.match(r'^case\s+(.+?)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            case_expr = m.group(1).rstrip(':').strip()
            if case_expr.lower().startswith('is '):
                cond = clean_expression(f"_match_val {case_expr}")
                return f"if {cond}:"
            elif ',' in case_expr:
                vals = [clean_expression(v.strip()) for v in case_expr.split(',')]
                return f"if _match_val in ({', '.join(vals)}):"
            else:
                val = clean_expression(case_expr)
                return f"if _match_val == {val}:"

        if re.match(r'^(?:default|otherwise)\s*:?\s*$', line, re.IGNORECASE):
            return "else:"

        if re.match(r'^end\s+match\s*$', line, re.IGNORECASE):
            return "# end match"

        # ── v2.0: Natural raise / throw ──────────────────────────────────
        m = re.match(r'^raise\s+([a-zA-Z_]\w*)\s+with\s+message\s+(.+)$', line, re.IGNORECASE)
        if m:
            exc_type, msg = m.group(1), clean_expression(m.group(2))
            return f"raise {exc_type}({msg})"

        m = re.match(r'^throw\s+(?:error|exception)\s+(.+)$', line, re.IGNORECASE)
        if m:
            msg = clean_expression(m.group(1))
            return f"raise Exception({msg})"

        # ── v2.0: Interface & Implements ─────────────────────────────────
        m = re.match(r'^(?:create\s+)?interface\s+([a-zA-Z_]\w*)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name = m.group(1)
            return f"class {name}:"

        if re.match(r'^end\s+(?:interface|class)\s*$', line, re.IGNORECASE):
            return "# end class/interface"

        # ── v2.0: Class with optional extends / implements ───────────────
        m = re.match(r'^(?:create\s+)?class\s+([a-zA-Z_]\w*)(?:\s+(?:extends|implements)\s+([a-zA-Z_,\s]+))?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name, base_str = m.group(1), m.group(2)
            if base_str:
                bases = ", ".join(b.strip() for b in base_str.split(','))
                extends_part = f'({bases})'
            else:
                extends_part = ''
            return f"class {name}{extends_part}:"

        # ── Function Definition ──────────────────────────────────────────
        m = re.match(r'^(?:async\s+)?(?:function|func|def)\s+([a-zA-Z_]\w*)(?:\s+(?:with|using|takes?|has|for|inputs?)\s+(.+?))?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            is_async = line.lower().startswith('async')
            func_name = m.group(1)
            raw_args = m.group(2)
            args_str = parse_args_list(raw_args) if raw_args else ""
            prefix = "async def" if is_async else "def"
            return f"{prefix} {func_name}({args_str}):"

        # ── Function Invocation with 'call' ───────────────────────────────
        m = re.match(r'^(?:call|run|execute)\s+(?:function\s+)?([a-zA-Z_]\w*)(?:\s+with\s+(.+))?$', line, re.IGNORECASE)
        if m:
            func_name = m.group(1)
            raw_args = m.group(2)
            args_str = parse_args_list(raw_args) if raw_args else ""
            return f"{func_name}({args_str})"

        # ── Range For Loop: for each var from start to end: ──────────────
        m = re.match(r'^(?:repeat\s+)?for\s+(?:each\s+)?([a-zA-Z_]\w*)\s+from\s+(.+?)\s+to\s+(.+?)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            var, start_expr, end_expr = m.group(1), clean_expression(m.group(2)), clean_expression(m.group(3))
            return f"for {var} in range({start_expr}, {end_expr} + 1):"

        # ── Collection For Loop: for each item in list: ──────────────────
        m = re.match(r'^(?:repeat\s+)?for\s+(?:each\s+)?([a-zA-Z_]\w*)\s+in\s+(.+?)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            var, collection = m.group(1), clean_expression(m.group(2))
            return f"for {var} in {collection}:"

        # ── While Loop: while condition then: ────────────────────────────
        m = re.match(r'^while\s+(.+?)\s*(?:then)?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            cond = clean_expression(m.group(1).rstrip(':').strip())
            if cond.lower().endswith(" then"):
                cond = cond[:-5].strip()
            return f"while {cond}:"

        # ── Return Statement ──────────────────────────────────────────────
        m = re.match(r'^return\b(?:\s+(.+))?$', line, re.IGNORECASE)
        if m:
            expr = clean_expression(m.group(1)) if m.group(1) else ""
            return f"return {expr}".strip()

        # ── Raw Python pass-through ───────────────────────────────────────
        _py_passthrough_starts = (
            'import ', 'from ', 'raise ', 'assert ', 'del ', 'yield ',
            'async ', 'await ', 'with ', 'try:', 'except ', 'except:',
            'finally:', 'pass', 'break', 'continue', 'lambda ',
            'class ', '@',
        )
        if any(line.startswith(s) for s in _py_passthrough_starts):
            return line

        # ── File Linking ──────────────────────────────────────────────────
        m = re.match(r'^(?:include|link|import)\s+(?:design|ui|script|database|file)?\s*["\'](.+?)["\']$', line, re.IGNORECASE)
        if m:
            target_path = m.group(1)
            return (
                f"import os; from enlang_core.transpiler import EnLangTranspiler; "
                f"_target = '{target_path}' if os.path.exists('{target_path}') "
                f"else os.path.join(os.path.dirname(globals().get('__file__', '')), '{target_path}'); "
                f"_target = _target if os.path.exists(_target) else '{target_path}'; "
                f"_code = open(_target, 'r', encoding='utf-8').read(); "
                f"exec(EnLangTranspiler().transpile(_code, _target))"
            )

        # ── NLP Operations ────────────────────────────────────────────────
        m = re.match(r'^(?:analyze|check|find)\s+sentiment\s+(?:of|for)\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            text_expr, var = clean_expression(m.group(1)), m.group(2)
            return f"from enlang_core.nlp_engine import analyze_sentiment; {var} = analyze_sentiment({text_expr})"

        m = re.match(r'^(?:extract|get|find)\s+keywords\s+(?:from|in)\s+(.+?)\s+into\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            text_expr, var = clean_expression(m.group(1)), m.group(2)
            return f"from enlang_core.nlp_engine import extract_keywords; {var} = extract_keywords({text_expr})"

        m = re.match(r'^(?:calculate|compute|check)\s+similarity\s+between\s+(.+?)\s+and\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            t1, t2, var = clean_expression(m.group(1)), clean_expression(m.group(2)), m.group(3)
            return f"from enlang_core.nlp_engine import calculate_similarity; {var} = calculate_similarity({t1}, {t2})"

        # ── Variable Assignment & Input ───────────────────────────────────
        m = re.match(r'^(?:set|let)\s+([a-zA-Z_]\w*)\s+(?:to|=|is)\s+(?:ask|input|read)\s+(.+)$', line, re.IGNORECASE)
        if m:
            var, prompt = m.group(1), clean_expression(m.group(2))
            return f"print(str({prompt}), end='', flush=True); {var} = input()"

        m = re.match(r'^store\s+(.+)\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            val, var = clean_expression(m.group(1)), m.group(2)
            return f"{var} = {val}"

        m = re.match(r'^(?:set|let)\s+([a-zA-Z_]\w*(?:\[[^\]]+\])*)\s+(?:to|=|is)\s+(.+)$', line, re.IGNORECASE)
        if m:
            var, expr = m.group(1), clean_expression(m.group(2))
            return f"{var} = {expr}"

        m = re.match(r'^([a-zA-Z_]\w*)\s+is\s+((?:["\']|\d|\[|\{|true|false).*)$', line, re.IGNORECASE)
        if m:
            var, val = m.group(1), clean_expression(m.group(2))
            return f"{var} = {val}"

        # ── Increment / Decrement ─────────────────────────────────────────
        m = re.match(r'^increment\s+([a-zA-Z_]\w*)\s+by\s+(.+)$', line, re.IGNORECASE)
        if m:
            return f"{m.group(1)} += {clean_expression(m.group(2))}"

        m = re.match(r'^decrement\s+([a-zA-Z_]\w*)\s+by\s+(.+)$', line, re.IGNORECASE)
        if m:
            return f"{m.group(1)} -= {clean_expression(m.group(2))}"

        # ── Output ────────────────────────────────────────────────────────
        m = re.match(r'^(?:display|print|show|say|log\s+text:?|log)(?:\s*\((.*)\)|\s+(.*))$', line, re.IGNORECASE)
        if m:
            exprs = m.group(1) if m.group(1) is not None else m.group(2)
            return f"print({_safe_concat_expr(clean_expression(exprs))})"

        # ── User Input ────────────────────────────────────────────────────
        m = re.match(r'^(?:set|let)\s+([a-zA-Z_]\w*)\s+(?:to|=|is)\s+(?:ask|input|read)\s+(.+)$', line, re.IGNORECASE)
        if m:
            var, prompt = m.group(1), clean_expression(m.group(2))
            return f"print(str({prompt}), end='', flush=True); {var} = input()"

        m = re.match(r'^ask\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            prompt, var = clean_expression(m.group(1)), m.group(2)
            return f"print(str({prompt}), end='', flush=True); {var} = input()"

        # ── Database (from .enlg backend) ─────────────────────────────────
        m = re.match(r'^connect\s+to\s+database\s+(.+)\s+as\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            db_path, var = clean_expression(m.group(1)), m.group(2)
            return f"import sqlite3; {var} = sqlite3.connect({db_path})"

        m = re.match(r'^define\s+table\s+([a-zA-Z_]\w*)\s+with\s+columns\s+(.+)$', line, re.IGNORECASE)
        if m:
            tbl, cols_raw = m.group(1), m.group(2)
            cols = cols_raw.replace(' as ', ' ').replace(' and ', ', ')
            sql = f"CREATE TABLE IF NOT EXISTS {tbl} ({cols})"
            return f"_cur = {self.last_db_var}.cursor(); _cur.execute('{sql}'); {self.last_db_var}.commit()"

        m = re.match(r'^insert\s+record\s+into\s+([a-zA-Z_]\w*)\s+with\s+values\s+(.+)$', line, re.IGNORECASE)
        if m:
            tbl, vals = m.group(1), parse_args_list(m.group(2))
            return f"_cur = {self.last_db_var}.cursor(); _cur.execute(f'INSERT INTO {tbl} VALUES ({{{vals}}})'); {self.last_db_var}.commit()"

        m = re.match(r'^(?:execute|run)\s+(?:sql|query)\s+(.+?)(?:\s+on\s+(?:database\s+)?([a-zA-Z_]\w*))?(?:\s+and\s+store\s+in\s+([a-zA-Z_]\w*))?$', line, re.IGNORECASE)
        if m:
            query = clean_expression(m.group(1))
            db_var = m.group(2) if m.group(2) else self.last_db_var
            var = m.group(3)
            if var:
                return f"_cur = {db_var}.cursor(); _cur.execute({query}); {var} = _cur.fetchall(); {db_var}.commit()"
            return f"_cur = {db_var}.cursor(); _cur.execute({query}); {db_var}.commit()"

        # ── Web Server ────────────────────────────────────────────────────
        m = re.match(r'^start\s+web\s+server\s+on\s+port\s+(.+)$', line, re.IGNORECASE)
        if m:
            port = clean_expression(m.group(1))
            return f"from enlang_core.web_server import start_enlang_server; start_enlang_server({port})"

        # ── Security / Crypto ─────────────────────────────────────────────
        m = re.match(r'^hash\s+(.+)\s+with\s+([a-zA-Z0-9]+)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            text, algo, var = clean_expression(m.group(1)), m.group(2).lower(), m.group(3)
            return f"import hashlib; {var} = hashlib.{algo}({text}.encode('utf-8')).hexdigest()"

        # ── HTTP Fetch ────────────────────────────────────────────────────
        m = re.match(r'^fetch\s+url\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            url, var = clean_expression(m.group(1)), m.group(2)
            return f"import urllib.request; {var} = urllib.request.urlopen({url}).read().decode('utf-8')"

        # ── File I/O (Python backend) ─────────────────────────────────────
        m = re.match(r'^read\s+(?:file\s+)?(.+?)\s+(?:into|and\s+store\s+in)\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            path, var = clean_expression(m.group(1)), m.group(2)
            return f"with open({path}, 'r', encoding='utf-8') as _f: {var} = _f.read()"

        m = re.match(r'^write\s+(.+?)\s+to\s+(?:file\s+)?(.+)$', line, re.IGNORECASE)
        if m:
            content, path = clean_expression(m.group(1)), clean_expression(m.group(2))
            return f"with open({path}, 'w', encoding='utf-8') as _f: _f.write(str({content}))"

        # ── Type Conversion ───────────────────────────────────────────────
        m = re.match(r'^convert\s+(.+?)\s+to\s+(int|integer|float|double|str|string|bool|boolean|list|tuple|set)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            val, dtype, var = clean_expression(m.group(1)), m.group(2).lower(), m.group(3)
            type_map = {'integer': 'int', 'double': 'float', 'string': 'str', 'boolean': 'bool'}
            py_type = type_map.get(dtype, dtype)
            return f"{var} = {py_type}({val})"

        m = re.match(r'^(?:convert|cast)\s+([a-zA-Z_]\w*)\s+to\s+(int|integer|float|double|str|string|bool|boolean)$', line, re.IGNORECASE)
        if m:
            var, dtype = m.group(1), m.group(2).lower()
            type_map = {'integer': 'int', 'double': 'float', 'string': 'str', 'boolean': 'bool'}
            py_type = type_map.get(dtype, dtype)
            return f"{var} = {py_type}({var})"

        # ── Math Operations ───────────────────────────────────────────────
        m = re.match(r'^round\s+(.+?)\s+to\s+(\d+)\s+decimal\s+places?\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            val, places, var = clean_expression(m.group(1)), m.group(2), m.group(3)
            return f"{var} = round({val}, {places})"

        m = re.match(r'^(?:get\s+)?absolute\s+value\s+of\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            val, var = clean_expression(m.group(1)), m.group(2)
            return f"{var} = abs({val})"

        m = re.match(r'^(?:get\s+)?(?:minimum|min)\s+of\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            vals, var = clean_expression(m.group(1)), m.group(2)
            return f"{var} = min({vals})"

        m = re.match(r'^(?:get\s+)?(?:maximum|max)\s+of\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            vals, var = clean_expression(m.group(1)), m.group(2)
            return f"{var} = max({vals})"

        m = re.match(r'^(?:get\s+)?sum\s+of\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            lst, var = clean_expression(m.group(1)), m.group(2)
            return f"{var} = sum({lst})"

        # ── String Operations ─────────────────────────────────────────────
        m = re.match(r'^convert\s+([a-zA-Z_]\w*)\s+to\s+uppercase\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            src, var = m.group(1), m.group(2)
            return f"{var} = {src}.upper()"

        m = re.match(r'^convert\s+([a-zA-Z_]\w*)\s+to\s+lowercase\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            src, var = m.group(1), m.group(2)
            return f"{var} = {src}.lower()"

        m = re.match(r'^trim\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            src, var = m.group(1), m.group(2)
            return f"{var} = {src}.strip()"

        m = re.match(r'^split\s+([a-zA-Z_]\w*)\s+by\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            src, sep, var = m.group(1), clean_expression(m.group(2)), m.group(3)
            return f"{var} = {src}.split({sep})"

        m = re.match(r'^replace\s+(.+?)\s+with\s+(.+?)\s+in\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            old, new_, src, var = clean_expression(m.group(1)), clean_expression(m.group(2)), m.group(3), m.group(4)
            return f"{var} = {src}.replace({old}, {new_})"

        m = re.match(r'^check\s+if\s+([a-zA-Z_]\w*)\s+contains\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            src, sub, var = m.group(1), clean_expression(m.group(2)), m.group(3)
            return f"{var} = ({sub} in {src})"

        m = re.match(r'^format\s+(.+?)\s+with\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            template, args, var = clean_expression(m.group(1)), clean_expression(m.group(2)), m.group(3)
            return f"{var} = {template}.format({args})"

        # ── DateTime ─────────────────────────────────────────────────────
        m = re.match(r'^get\s+current\s+(?:date\s+and\s+)?time\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            var = m.group(1)
            return f"import datetime; {var} = datetime.datetime.now()"

        m = re.match(r'^get\s+current\s+date\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            var = m.group(1)
            return f"import datetime; {var} = datetime.date.today()"

        m = re.match(r'^get\s+current\s+timestamp\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            var = m.group(1)
            return f"import time; {var} = int(time.time())"

        m = re.match(r'^format\s+date\s+([a-zA-Z_]\w*)\s+as\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            dt, fmt, var = m.group(1), _strip_quotes_local(m.group(2)), m.group(3)
            return f"{var} = {dt}.strftime('{fmt}')"

        # ── Sleep ─────────────────────────────────────────────────────────
        m = re.match(r'^sleep\s+(.+?)\s+(?:seconds?|s)$', line, re.IGNORECASE)
        if m:
            secs = clean_expression(m.group(1))
            return f"import time; time.sleep({secs})"

        m = re.match(r'^sleep\s+(.+?)\s+(?:ms|milliseconds?)$', line, re.IGNORECASE)
        if m:
            ms = clean_expression(m.group(1))
            return f"import time; time.sleep({ms} / 1000)"

        # ── Class Definition ──────────────────────────────────────────────
        m = re.match(r'^(?:create\s+)?class\s+([a-zA-Z_]\w*)(?:\s+extends\s+([a-zA-Z_]\w*))?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name = m.group(1)
            base = m.group(2) if m.group(2) else ''
            extends_part = f'({base})' if base else ''
            return f"class {name}{extends_part}:"

        # ── Exception Handling ────────────────────────────────────────────
        m = re.match(r'^raise\s+([a-zA-Z_]\w*)(?:\s+with\s+message\s+(.+))?$', line, re.IGNORECASE)
        if m:
            exc_type = m.group(1)
            msg = clean_expression(m.group(2)) if m.group(2) else '"An error occurred"'
            return f"raise {exc_type}({msg})"

        m = re.match(r'^throw\s+(?:error|exception)\s+(.+)$', line, re.IGNORECASE)
        if m:
            msg = clean_expression(m.group(1))
            return f"raise Exception({msg})"

        # ── Environment / OS ──────────────────────────────────────────────
        m = re.match(r'^get\s+environment\s+variable\s+(.+?)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            key, var = clean_expression(m.group(1)), m.group(2)
            return f"import os; {var} = os.environ.get({key}, '')"

        m = re.match(r'^set\s+environment\s+variable\s+(.+?)\s+to\s+(.+)$', line, re.IGNORECASE)
        if m:
            key, val = clean_expression(m.group(1)), clean_expression(m.group(2))
            return f"import os; os.environ[{key}] = str({val})"

        m = re.match(r'^check\s+if\s+(?:file|path)\s+(.+?)\s+exists\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            path, var = clean_expression(m.group(1)), m.group(2)
            return f"import os; {var} = os.path.exists({path})"

        m = re.match(r'^create\s+directory\s+(.+)$', line, re.IGNORECASE)
        if m:
            path = clean_expression(m.group(1))
            return f"import os; os.makedirs({path}, exist_ok=True)"

        m = re.match(r'^list\s+files\s+in\s+(.+?)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            path, var = clean_expression(m.group(1)), m.group(2)
            return f"import os; {var} = os.listdir({path})"

        # ── Shell Command ────────────────────────────────────────────────
        m = re.match(r'^(?:run|execute)\s+(?:command\s+)?(.+)$', line, re.IGNORECASE)
        if m:
            cmd = clean_expression(m.group(1))
            return f"import subprocess; subprocess.run({cmd}, shell=True)"

        # ── Control Flow ──────────────────────────────────────────────────
        m_elif = re.match(r'^(?:otherwise\s+if|else\s+if|elif)\s+(.+)$', line, re.IGNORECASE)
        if m_elif:
            cond = clean_expression(m_elif.group(1).rstrip(":"))
            return f"elif {cond}:"

        if re.match(r'^otherwise\s*:?\s*$', line, re.IGNORECASE):
            return "else:"

        m = re.match(r'^if\s+(.+?)(?:\s+then)?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            cond = clean_expression(m.group(1).rstrip(":"))
            return f"if {cond}:"

        if re.match(r'^else\s*:?\s*$', line, re.IGNORECASE):
            return "else:"

        # ── Loops ─────────────────────────────────────────────────────────
        m = re.match(r'^repeat\s+(.+?)\s+times\s*(?:do\s*)?:?\s*$', line, re.IGNORECASE)
        if m:
            count = clean_expression(m.group(1))
            return f"for _ in range(int({count})):"

        m = re.match(r'^(?:repeat\s+)?for\s+each\s+([a-zA-Z_]\w*)\s+in\s+(.+?)(?:\s+do)?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            item, coll = m.group(1), clean_expression(m.group(2).rstrip(":"))
            return f"for {item} in {coll}:"

        m = re.match(r'^repeat\s+until\s+(.+?)(?:\s+do)?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            cond = clean_expression(m.group(1).rstrip(":"))
            return f"while not ({cond}):"

        m = re.match(r'^while\s+(.+?)(?:\s+do)?\s*:?\s*$', line, re.IGNORECASE)
        if m:
            cond = clean_expression(m.group(1).rstrip(":"))
            return f"while {cond}:"

        # ── Functions ─────────────────────────────────────────────────────
        # 1. Standard: function foo(n): or define function foo(n):
        m = re.match(r'^(?:define\s+)?(?:function|func)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name, params = m.group(1), m.group(2)
            return f"def {name}({params}):"

        # 2. Natural English: define function foo with n: / function foo using n:
        m = re.match(r'^(?:define\s+)?(?:function|func|action|task|procedure|process)\s+([a-zA-Z_]\w*)\s+(?:using|taking|given|with|for)\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name, params = m.group(1), m.group(2)
            return f"def {name}({params}):"

        # 2b. Parameterless function: define function foo:
        m = re.match(r'^(?:define\s+)?(?:function|func|action|task|procedure|process)\s+([a-zA-Z_]\w*)\s*:?\s*$', line, re.IGNORECASE)
        if m:
            name = m.group(1)
            return f"def {name}():"

        # 3. Invocation: call function foo with 1 / call foo with 1 / run function foo with 1
        m = re.match(r'^(?:start|call|run|execute|begin|perform|next|apply)\s+(?:function\s+|func\s+|procedure\s+)?([a-zA-Z_]\w*)\s+(?:from|with|using|for)\s+(.+)$', line, re.IGNORECASE)
        if m:
            name, val = m.group(1), clean_expression(m.group(2))
            return f"{name}({val})"

        # 3b. Parameterless Invocation: call function foo / call foo
        m = re.match(r'^(?:start|call|run|execute|begin|perform)\s+(?:function\s+|func\s+|procedure\s+)?([a-zA-Z_]\w*)\s*$', line, re.IGNORECASE)
        if m:
            name = m.group(1)
            return f"{name}()"

        m = re.match(r'^return\s+(.+)$', line, re.IGNORECASE)
        if m:
            expr = clean_expression(m.group(1))
            return f"return {expr}"

        # ── Imports ───────────────────────────────────────────────────────
        m = re.match(r'^import\s+(?:module\s+)?([a-zA-Z_][\w.]*(?:,\s*[a-zA-Z_][\w.]*)*)(?:\s+as\s+([a-zA-Z_]\w*))?$', line, re.IGNORECASE)
        if m:
            mod, alias = m.group(1).strip(), m.group(2)
            if alias:
                return f"import {mod} as {alias}"
            return f"import {mod}"

        m = re.match(r'^from\s+([a-zA-Z_][\w.]*)\s+import\s+(.+)$', line, re.IGNORECASE)
        if m:
            mod, what = m.group(1), m.group(2)
            return f"from {mod} import {what}"

        # ── Collections: Lists / Arrays ───────────────────────────────────
        # create list/array <var> with items <i1>, <i2>, ...
        m = re.match(r'^(?:create\s+)?(?:list|array|collection)\s+([a-zA-Z_]\w*)(?:\s+with\s+(?:items?\s+)?(.+))?$', line, re.IGNORECASE)
        if m:
            var, items_raw = m.group(1), m.group(2)
            if items_raw:
                items_list = [clean_expression(i.strip()) for i in items_raw.split(',')]
                return f"{var} = [{', '.join(items_list)}]"
            return f"{var} = []"

        # add <item> to <list>
        m = re.match(r'^(?:add|push|append)\s+(.+?)\s+to\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            item, lst = clean_expression(m.group(1)), m.group(2)
            return f"{lst}.append({item})"

        # remove item at index <n> from <list>
        m = re.match(r'^remove\s+item\s+at\s+(?:index\s+)?(.+?)\s+from\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            idx, lst = clean_expression(m.group(1)), m.group(2)
            return f"{lst}.pop({idx})"

        # remove <item> from <list>
        m = re.match(r'^remove\s+(.+?)\s+from\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            item, lst = clean_expression(m.group(1)), m.group(2)
            return f"{lst}.remove({item})"

        # get item <n> from <list> and store in <var>
        m = re.match(r'^get\s+item\s+(?:at\s+(?:index\s+)?)?(.+?)\s+from\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            idx, lst, var = clean_expression(m.group(1)), m.group(2), m.group(3)
            return f"{var} = {lst}[{idx}]"

        # get length of <list> and store in <var>
        m = re.match(r'^(?:get\s+)?(?:length|size|count)\s+(?:of\s+|items?\s+in\s+)?(?:list\s+|array\s+)?([a-zA-Z_]\w*)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            lst, var = m.group(1), m.group(2)
            return f"{var} = len({lst})"

        # sort <list>
        m = re.match(r'^sort\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            return f"{m.group(1)}.sort()"

        # reverse <list>
        m = re.match(r'^(?:sort\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)\s+in\s+reverse|reverse\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*))$', line, re.IGNORECASE)
        if m:
            lst = m.group(1) or m.group(2)
            return f"{lst}.reverse()"

        # check if <item> is in <list> and store in <var>
        m = re.match(r'^check\s+if\s+(.+?)\s+is\s+in\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            item, lst, var = clean_expression(m.group(1)), m.group(2), m.group(3)
            return f"{var} = ({item} in {lst})"

        # join <list> with <sep> and store in <var>
        m = re.match(r'^join\s+(?:list\s+|array\s+)?([a-zA-Z_]\w*)\s+with\s+(.+?)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            lst, sep, var = m.group(1), clean_expression(m.group(2)), m.group(3)
            return f"{var} = {sep}.join(str(x) for x in {lst})"

        # ── Collections: Dictionaries / Maps ──────────────────────────────
        m = re.match(r'^(?:create\s+)?(?:map|dict|dictionary)\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            return f"{m.group(1)} = {{}}"

        m = re.match(r'^(?:set\s+key|add\s+key)\s+(.+?)\s+(?:in|to)\s+(?:map\s+|dict\s+)?([a-zA-Z_]\w*)\s+(?:to|with\s+value)\s+(.+)$', line, re.IGNORECASE)
        if m:
            key, mp, val = clean_expression(m.group(1)), m.group(2), clean_expression(m.group(3))
            return f"{mp}[{key}] = {val}"

        m = re.match(r'^get\s+key\s+(.+?)\s+from\s+(?:map\s+|dict\s+)?([a-zA-Z_]\w*)\s+(?:and\s+)?store\s+in\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
        if m:
            key, mp, var = clean_expression(m.group(1)), m.group(2), m.group(3)
            return f"{var} = {mp}[{key}]"

        # ── Loop Control ──────────────────────────────────────────────────
        if re.match(r'^break\s*$', line, re.IGNORECASE):
            return "break"

        if re.match(r'^continue\s*$', line, re.IGNORECASE):
            return "continue"

        # ── Pass / Placeholder ────────────────────────────────────────────
        if re.match(r'^pass\s*$', line, re.IGNORECASE):
            return "pass"

        # ── NLP Intent Fallback ───────────────────────────────────────────
        nlp_res = self.nlp_parser.parse_intent(line)
        if nlp_res:
            intent = nlp_res["intent"]
            if intent == "ASSIGNMENT":
                return f"{nlp_res['target']} = {clean_expression(nlp_res['value'])}"
            elif intent == "OUTPUT":
                return f"print({_safe_concat_expr(nlp_res['value'])})"
            elif intent == "NLP_SENTIMENT":
                return f"from enlang_core.nlp_engine import analyze_sentiment; {nlp_res['target']} = analyze_sentiment({clean_expression(nlp_res['text'])})"
            elif intent == "NLP_KEYWORDS":
                return f"from enlang_core.nlp_engine import extract_keywords; {nlp_res['target']} = extract_keywords({clean_expression(nlp_res['text'])})"
            elif intent == "NLP_SIMILARITY":
                return f"from enlang_core.nlp_engine import calculate_similarity; {nlp_res['target']} = calculate_similarity({clean_expression(nlp_res['text1'])}, {clean_expression(nlp_res['text2'])})"

        # Pass through anything that's already valid Python-like syntax
        return clean_expression(line)
