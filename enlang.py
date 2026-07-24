#!/usr/bin/env python3
"""
EnLang Command Line Interface (CLI)
Natural English Programming Language Runner & Tooling.
Supports .enlg (Normal), .enlgd (Design UI), .enlgs (Script Automation), and .enlgdb (Database).
"""

import sys
import os
import argparse
from enlang_core import EnLangInterpreter, EnLangTranspiler, __version__

SUPPORTED_EXTENSIONS = ['.enlg', '.enlgf', '.enlgd', '.enlgs', '.enlgdb', '.enl']

def main():
    parser = argparse.ArgumentParser(
        prog="enlang",
        description="EnLang - Universal Natural English Programming Language (.enlg, .enlgd, .enlgs, .enlgdb)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run an EnLang (.enlg / .enlgd / .enlgs / .enlgdb) script directly")
    run_parser.add_argument("filename", help="Path to EnLang file")
    run_parser.add_argument("--show-python", action="store_true", help="Print transpiled Python code before running")

    # Command: build
    build_parser = subparsers.add_parser("build", help="Transpile EnLang script to a Python (.py) file")
    build_parser.add_argument("filename", help="Path to EnLang file")
    build_parser.add_argument("-o", "--output", help="Output .py file path")

    # Command: repl / shell
    subparsers.add_parser("repl", help="Start interactive EnLang English REPL shell")
    subparsers.add_parser("shell", help="Start interactive EnLang English REPL shell")

    # Command: version
    subparsers.add_parser("version", help="Show EnLang version")

    args = parser.parse_args()

    interpreter = EnLangInterpreter()
    transpiler = EnLangTranspiler()

    if args.command == "run":
        if not os.path.exists(args.filename):
            print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
            sys.exit(1)

        with open(args.filename, "r", encoding="utf-8") as f:
            source = f.read()

        if args.show_python:
            py_code = transpiler.transpile(source, file_path=args.filename)
            print(f"--- Generated Python Code ({args.filename}) ---")
            print(py_code)
            print("--- Execution Output ---")

        success, stdout, stderr, _ = interpreter.run_code(source, file_path=args.filename)
        if stdout:
            print(stdout, end="")
        if stderr:
            print(stderr, file=sys.stderr, end="")
        sys.exit(0 if success else 1)

    elif args.command == "build":
        if not os.path.exists(args.filename):
            print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
            sys.exit(1)

        with open(args.filename, "r", encoding="utf-8") as f:
            source = f.read()

        py_code = transpiler.transpile(source, file_path=args.filename)
        out_path = args.output if args.output else os.path.splitext(args.filename)[0] + ".py"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(py_code)

        print(f"Successfully compiled '{args.filename}' -> '{out_path}'")

    elif args.command in ["repl", "shell"]:
        start_repl(interpreter)

    elif args.command == "version":
        print(f"EnLang Version {__version__} (NLP Engine & Multi-Extension Support: .enlg, .enlgd, .enlgs, .enlgdb)")

    else:
        # Default behavior if file passed directly without subcommand
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            success, stdout, stderr, _ = interpreter.run_file(sys.argv[1])
            if stdout:
                print(stdout, end="")
            if stderr:
                print(stderr, file=sys.stderr, end="")
            sys.exit(0 if success else 1)
        else:
            parser.print_help()

def start_repl(interpreter: EnLangInterpreter):
    """Starts the interactive EnLang English Shell with NLP intent parsing."""
    print(f"EnLang Interactive NLP English Shell v{__version__}")
    print("Supports natural English phrasing & NLP commands. Type 'exit' to quit.\n")

    repl_globals = {}
    while True:
        try:
            line = input("enl> ")
            if line.strip().lower() in ["exit", "quit", "exit()"]:
                print("Bye!")
                break
            if not line.strip():
                continue

            success, stdout, stderr, py_code = interpreter.run_code(line, custom_globals=repl_globals)
            if stdout:
                print(stdout, end="")
            if stderr:
                print(f"[Error] {stderr}", end="")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting EnLang shell. Bye!")
            break

if __name__ == "__main__":
    main()
