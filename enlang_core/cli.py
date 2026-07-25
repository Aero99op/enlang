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

VERSION = "2.0.6 — Enterprise Specification Edition"

def format_ascii_table(title: str, headers: list, rows: list) -> str:
    if not headers:
        return ""
    str_rows = [[str(val) if val is not None else "NULL" for val in row] for row in rows]
    col_widths = [len(str(h)) for h in headers]
    for row in str_rows:
        for idx, val in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(val))

    sep_line = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_line = "| " + " | ".join(f"{str(h):<{col_widths[i]}}" for i, h in enumerate(headers)) + " |"

    banner_width = max(len(sep_line), 60)
    lines = []
    lines.append("=" * banner_width)
    lines.append(f" TABLE: {title.upper()} (Total Rows: {len(rows)})")
    lines.append("=" * banner_width)
    lines.append(sep_line)
    lines.append(header_line)
    lines.append(sep_line)
    for row in str_rows:
        r_line = "| " + " | ".join(f"{val:<{col_widths[i]}}" for i, val in enumerate(row)) + " |"
        lines.append(r_line)
    if not str_rows:
        lines.append("| " + " ".join("EMPTY TABLE".center(w) for w in col_widths) + " |")
        lines.append(sep_line)
    else:
        lines.append(sep_line)
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ("--version", "-v", "version"):
        print(f"EnLang Compiler Version {VERSION}")
        print("Author: Spandan Prayas Patra")
        try:
            from .version_manager import check_for_updates
            check_for_updates()
        except Exception:
            pass
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

    elif cmd in ("check", "lint"):
        if len(sys.argv) < 3:
            print("Error: Please specify a file to check.")
            print("Usage: enlang check <filename.enlg>")
            sys.exit(1)
        file_path = sys.argv[2]
        try:
            from .checker import check_file
        except ImportError:
            from enlang_core.checker import check_file
        check_file(file_path)

    elif cmd in ("debug", "dbg"):
        if len(sys.argv) < 3:
            print("Error: Please specify a file to debug.")
            print("Usage: enlang debug <filename.enlg>")
            sys.exit(1)
        file_path = sys.argv[2]
        try:
            from .debugger import debug_file
        except ImportError:
            from enlang_core.debugger import debug_file
        debug_file(file_path)

    elif cmd == "update":
        try:
            from .version_manager import update_to_latest
        except ImportError:
            from enlang_core.version_manager import update_to_latest
        update_to_latest()
        sys.exit(0)

    elif cmd in ("versions", "list-versions"):
        try:
            from .version_manager import list_versions
        except ImportError:
            from enlang_core.version_manager import list_versions
        list_versions()
        sys.exit(0)

    elif cmd == "install":
        if len(sys.argv) < 3:
            print("Error: Please specify a version to install.")
            print("Usage: enlang install <version> (e.g. enlang install 2.0.0)")
            sys.exit(1)
        ver = sys.argv[2]
        try:
            from .version_manager import install_specific_version
        except ImportError:
            from enlang_core.version_manager import install_specific_version
        install_specific_version(ver)
        sys.exit(0)

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

def find_free_port(start_port=8080):
    import socket
    for port in range(start_port, start_port + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return start_port

def run_file(file_path: str, custom_port: int = None):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    ext = os.path.splitext(file_path)[1].lower()

    # If running a web file (.enlgf, .enlgd, .enlgs), auto-build all web files in dir and serve
    if ext in (".enlgf", ".enlgd", ".enlgs"):
        directory = os.path.dirname(file_path) or "."
        # Build all .enlgf, .enlgd, .enlgs in directory
        for item in os.listdir(directory):
            if item.endswith((".enlgf", ".enlgd", ".enlgs")):
                item_path = os.path.join(directory, item)
                build_file(item_path)

        html_file = os.path.splitext(os.path.basename(file_path))[0] + ".html"
        
        if custom_port is None:
            for idx, arg in enumerate(sys.argv):
                if arg in ("-p", "--p", "--port") and idx + 1 < len(sys.argv):
                    try:
                        custom_port = int(sys.argv[idx + 1])
                    except ValueError:
                        pass
        
        port = custom_port if custom_port else find_free_port(8080)
        print(f"\n[SUCCESS] Web application compiled successfully!")
        print(f"[INFO] Launching EnLang Dev Web Server on port {port}...")
        print(f"[LIVE URL] http://localhost:{port}/{html_file}\n")
        
        try:
            from .web_server import start_enlang_server
            start_enlang_server(port, directory=directory)
        except ImportError:
            from enlang_core.web_server import start_enlang_server
            start_enlang_server(port, directory=directory)
        return

    # If running a database file (.enlgdb), auto-build to .sql and execute against SQLite
    if ext == ".enlgdb":
        import sqlite3
        build_file(file_path)
        sql_file = os.path.splitext(file_path)[0] + ".sql"
        db_file = os.path.splitext(file_path)[0] + ".db"
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        print(f"\n[INFO] Executing EnLang Database Schema '{file_path}'...")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cursor.fetchall() if not r[0].startswith("sqlite_")]
        print(f"[SUCCESS] Database synced -> '{db_file}'\n")

        # Display rich ASCII table for all database tables
        for tbl in tables:
            cursor.execute(f"SELECT * FROM {tbl};")
            rows = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description] if cursor.description else []
            print(format_ascii_table(tbl, cols, rows))
            print()

        conn.close()
        return

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
        from .interpreter import EnLangInterpreter
        from .transpiler import EnLangTranspiler
    except ImportError:
        from enlang_core.interpreter import EnLangInterpreter
        from enlang_core.transpiler import EnLangTranspiler

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

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    if ext in (".enlgf", ".enlgd", ".enlgs", ".enlgdb"):
        interp = EnLangInterpreter()
        ok, stdout, stderr, _ = interp.run_code(code, file_path=file_path)
        if not ok and stderr:
            print(f"[ERROR] Sub-transpilation failed:\n{stderr}", file=sys.stderr)
            sys.exit(1)
        final_output = stdout
    else:
        t = EnLangTranspiler()
        final_output = t.transpile(code, file_path=file_path)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"[SUCCESS] Transpiled '{file_path}' -> '{out_file}'")

def print_help():
    print("""
EnLang — Universal Natural English Compiler CLI (v2.0)

USAGE:
  enlang <command> [options]

COMMANDS:
  run <file>          Compiles & executes an EnLang file (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb)
  build <file>        Transpiles EnLang source file into native target code file (.py, .html, .css, .js, .sql)
  check <file>        Performs static analysis and linting without execution
  debug <file>        Launches interactive step-by-step debugger with live variable inspection
  server [--port N]   Launches EnLang HTTP Web Server on specified port (default: 8000)
  version             Displays installed compiler version & author info
  help                Shows this usage manual

EXAMPLES:
  enlang run app.enlg
  enlang check app.enlg
  enlang debug app.enlg
  enlang build index.enlgf
  enlang server --port 8080
""")

if __name__ == "__main__":
    main()
