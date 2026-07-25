"""
EnLang Step-by-Step Interactive CLI Debugger
=============================================
Interactive line-by-line debugger for EnLang applications.

Commands:
  (s)tep        - Step to next line
  (c)ontinue    - Continue execution until next breakpoint or end
  (v)ars        - Print current variable values
  (b)reak <N>   - Set breakpoint at line N
  (e)val <expr> - Evaluate EnLang/Python expression in current frame
  (h)elp        - Show debugger commands
  (q)uit        - Quit debugger session
"""

import sys
import os
import re
from .transpiler import EnLangTranspiler

class EnLangDebugger:
    def __init__(self, code: str, file_path: str = "main.enlg"):
        self.code = code
        self.file_path = file_path
        self.enlang_lines = code.splitlines()
        self.transpiler = EnLangTranspiler()
        
        # Transpile whole code to Python
        self.python_code = self.transpiler.transpile(code, file_path)
        self.py_lines = self.python_code.splitlines()

        self.breakpoints = set()
        self.step_mode = True
        self.frame_vars = {}

    def start(self):
        print("=" * 65)
        print(f"  EnLang Interactive Debugger  —  {self.file_path}")
        print("=" * 65)
        print("Type 's' to step, 'v' for variables, 'b <line>' for breakpoint, 'h' for help.")
        print()

        exec_globals = {"__name__": "__main__", "print": print}

        for idx, enlang_line in enumerate(self.enlang_lines, start=1):
            stripped = enlang_line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("//"):
                continue

            # Check for breakpoint or step mode
            if idx in self.breakpoints:
                print(f"\n🛑 [BREAKPOINT HIT] Line {idx}")
                self.step_mode = True

            if self.step_mode:
                self._show_code_context(idx)
                self._interactive_prompt(idx, exec_globals)

            # Transpile & Execute single line in frame
            try:
                py_line = self.transpiler._transpile_python_line(stripped)
                exec(py_line, exec_globals, self.frame_vars)
            except Exception as e:
                print(f"\n[RUNTIME ERROR] Line {idx}: {e}")
                print(f"Line Content: {enlang_line}")
                break

        print("\n=" * 65)
        print("  [DEBUGGER] Program Execution Finished.")
        print("=" * 65)

    def _show_code_context(self, current_line: int):
        print("-" * 65)
        start = max(1, current_line - 2)
        end = min(len(self.enlang_lines), current_line + 2)

        for lno in range(start, end + 1):
            prefix = " -> " if lno == current_line else "    "
            line_str = self.enlang_lines[lno - 1]
            print(f"{prefix}{lno:3d} | {line_str}")
        print("-" * 65)

    def _interactive_prompt(self, current_line: int, exec_globals: dict):
        while True:
            try:
                cmd_input = input(f"(debug L{current_line}) > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting debugger...")
                sys.exit(0)

            if not cmd_input or cmd_input in ("s", "step"):
                self.step_mode = True
                break

            elif cmd_input in ("c", "continue"):
                self.step_mode = False
                break

            elif cmd_input in ("v", "vars", "variables"):
                print("\n--- Live Variables Table ---")
                user_vars = {k: v for k, v in self.frame_vars.items() if not k.startswith("_")}
                if not user_vars:
                    print("  (No variables defined yet)")
                else:
                    for k, v in user_vars.items():
                        print(f"  {k} = {repr(v)}")
                print("----------------------------\n")

            elif cmd_input.startswith("b ") or cmd_input.startswith("break "):
                parts = cmd_input.split()
                if len(parts) > 1 and parts[1].isdigit():
                    b_line = int(parts[1])
                    self.breakpoints.add(b_line)
                    print(f"  Breakpoint set at line {b_line}")
                else:
                    print("  Usage: break <line_number>")

            elif cmd_input.startswith("e ") or cmd_input.startswith("eval "):
                expr = cmd_input.split(" ", 1)[1]
                try:
                    res = eval(expr, exec_globals, self.frame_vars)
                    print(f"  Result: {repr(res)}")
                except Exception as ex:
                    print(f"  Eval error: {ex}")

            elif cmd_input in ("h", "help"):
                print("""
DEBUGGER COMMANDS:
  s, step             - Step to next line
  c, continue         - Run until next breakpoint or program end
  v, vars             - Print all live user variables and values
  b <line>, break     - Set breakpoint at specified line number
  e <expr>, eval      - Evaluate expression in current frame
  q, quit, exit       - Exit debugger session
""")

            elif cmd_input in ("q", "quit", "exit"):
                print("Quitting debugger...")
                sys.exit(0)

            else:
                print(f"Unknown debugger command: '{cmd_input}'. Type 'h' for help.")

def debug_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"[ERROR] File '{file_path}' not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    dbg = EnLangDebugger(code, file_path)
    dbg.start()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_file(sys.argv[1])
    else:
        print("Usage: python -m enlang_core.debugger <filename.enlg>")
