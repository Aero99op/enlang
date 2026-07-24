"""
EnLang Interpreter & Execution Engine
Executes transpiled EnLang Python code cleanly with stdout/stderr capture and error handling.
"""

import sys
import io
import traceback
from typing import Dict, Any, Tuple
from .transpiler import EnLangTranspiler

class EnLangInterpreter:
    def __init__(self):
        self.transpiler = EnLangTranspiler()

    def run_code(self, source_code: str, custom_globals: Dict[str, Any] = None, file_path: str = "main.enlg") -> Tuple[bool, str, str, str]:
        """
        Transpiles and executes EnLang source code.
        Returns: (success: bool, stdout: str, stderr: str, py_code: str)
        """
        try:
            py_code = self.transpiler.transpile(source_code, file_path=file_path)
        except Exception as e:
            return False, "", f"Transpilation Error: {str(e)}\n{traceback.format_exc()}", ""

        old_stdout, old_stderr = sys.stdout, sys.stderr
        captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
        sys.stdout, sys.stderr = captured_stdout, captured_stderr

        exec_globals = custom_globals if custom_globals is not None else {}
        exec_globals["__name__"] = "__main__"

        success = True
        try:
            exec(py_code, exec_globals)
        except Exception as e:
            success = False
            sys.stderr.write(f"Runtime Error: {type(e).__name__}: {str(e)}\n")
            traceback.print_exc(file=sys.stderr)
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

        return success, captured_stdout.getvalue(), captured_stderr.getvalue(), py_code

    def run_file(self, file_path: str) -> Tuple[bool, str, str, str]:
        """Reads EnLang file (.enlg, .enlgd, .enlgs, .enlgdb) and executes it."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.run_code(content, file_path=file_path)
