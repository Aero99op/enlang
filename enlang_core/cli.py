"""
EnLang Main CLI Interface
=========================
Command-line driver for running, building, and serving EnLang applications.

Commands:
  enlang run <file>          Compiles & executes an EnLang file (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb)
  enlang build <file>        Transpiles EnLang source to native code file
  enlang server [--port P]   Launches zero-config EnLang HTTP Web Server
  enlang version             Displays installed EnLang version
  enlang help                Shows usage instructions
"""

import sys
import os
import argparse

VERSION = "2.0.0 — Enterprise Specification Edition"

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ("--version", "-v", "version"):
        print(f"EnLang Compiler Version {VERSION}")
        print("Author: Spandan Prayas Patra")
        sys.exit(0)

    if cmd in ("--help", "-h", "help"):
        print_help()
        sys.exit(0)

    if cmd == "run":
        if len(sys.argv) < 3:
            print("Error: Please specify a file to run.")
            print("Usage: enlang run <filename.enlg|enlgf|enlgd|enlgs|enlgdb>")
            sys.exit(1)
        file_path = sys.argv[2]
        run_file(file_path)

    elif cmd == "build":
        if len(sys.argv) < 3:
            print("Error: Please specify a file to build.")
            print("Usage: enlang build <filename.enlg|enlgf|enlgd|enlgs|enlgdb>")
            sys.exit(1)
        file_path = sys.argv[2]
        build_file(file_path)

    elif cmd == "server":
        port = 8000
        if "--port" in sys.argv:
            try:
                idx = sys.argv.index("--port")
                port = int(sys.argv[idx + 1])
            except (ValueError, IndexError):
                print("Warning: Invalid port specified, using default port 8000.")
        
        print(f"[INFO] Launching EnLang Web Server on port {port}...")
        try:
            from .web_server import start_enlang_server
            start_enlang_server(port)
        except ImportError:
            from enlang_core.web_server import start_enlang_server
            start_enlang_server(port)

    else:
        # Fallback: Treat sys.argv[1] as a file to run directly (e.g. enlang app.enlg)
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            run_file(file_path)
        else:
            print(f"Unknown command or file not found: {cmd}")
            print_help()
            sys.exit(1)

def run_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        from .interpreter import EnLangInterpreter
    except ImportError:
        from enlang_core.interpreter import EnLangInterpreter

    interp = EnLangInterpreter()
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    ok, stdout, stderr, _ = interp.run_code(code, file_path=file_path)
    if stdout.strip():
        print(stdout)
    if not ok:
        print(f"[ERROR] EnLang Runtime Exception:\n{stderr}", file=sys.stderr)
        sys.exit(1)

def build_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        from .transpiler import EnLangTranspiler
    except ImportError:
        from enlang_core.transpiler import EnLangTranspiler

    t = EnLangTranspiler()
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    transpiled = t.transpile(code, file_path=file_path)

    ext = os.path.splitext(file_path)[1].lower()
    target_ext_map = {
        ".enlg": ".py",
        ".enlgf": ".html",
        ".enlgd": ".css",
        ".enlgs": ".js",
        ".enlgdb": ".sql"
    }
    target_ext = target_ext_map.get(ext, ".py")
    out_file = os.path.splitext(file_path)[0] + target_ext

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transpiled)

    print(f"[SUCCESS] Transpiled '{file_path}' -> '{out_file}'")

def print_help():
    print("""
EnLang — Universal Natural English Compiler CLI (v2.0)

USAGE:
  enlang <command> [options]

COMMANDS:
  run <file>          Compiles & executes an EnLang file (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb)
  build <file>        Transpiles EnLang source file into native target code file (.py, .html, .css, .js, .sql)
  server [--port N]   Launches EnLang HTTP Web Server on specified port (default: 8000)
  version             Displays installed compiler version & author info
  help                Shows this usage manual

EXAMPLES:
  enlang run app.enlg
  enlang build index.enlgf
  enlang server --port 8080
""")

if __name__ == "__main__":
    main()
