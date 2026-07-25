"""
EnLang Package Manager (EPM) CLI
=================================
Handles dependency installation for EnLang projects (Native EnLang, PyPI, NPM).

Commands:
  epm init                  Creates enlang.json project manifest
  epm add <pkg>             Installs native EnLang package
  epm add py:<pip-package>  Installs Python PyPI package
  epm add web:<npm-package> Installs Web NPM package
  epm install               Installs all dependencies from enlang.json
  epm version               Displays EPM version
"""

import sys
import os
import json
import subprocess

VERSION = "1.0.0 — EnLang Package Manager"

MANIFEST_FILE = "enlang.json"

DEFAULT_MANIFEST = {
    "name": "my-enlang-app",
    "version": "1.0.0",
    "author": "Developer",
    "description": "EnLang Application",
    "entry": "main.enlg",
    "port": 8000,
    "dependencies": {
        "enlang": [],
        "python": [],
        "web": []
    }
}

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ("version", "--version", "-v"):
        print(f"EPM Version {VERSION}")
        sys.exit(0)

    if cmd in ("help", "--help", "-h"):
        print_help()
        sys.exit(0)

    if cmd == "init":
        init_manifest()

    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Error: Please specify package name.")
            print("Usage: epm add <pkg> | epm add py:<pip-pkg> | epm add web:<npm-pkg>")
            sys.exit(1)
        pkg = sys.argv[2]
        add_package(pkg)

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
        if len(sys.argv) >= 3 and (sys.argv[2].startswith("2.") or sys.argv[2].startswith("1.") or sys.argv[2].startswith("v")):
            ver = sys.argv[2]
            try:
                from .version_manager import install_specific_version
            except ImportError:
                from enlang_core.version_manager import install_specific_version
            install_specific_version(ver)
            sys.exit(0)
        else:
            install_dependencies()

    else:
        print(f"Unknown EPM command: {cmd}")
        print_help()
        sys.exit(1)

def init_manifest():
    if os.path.exists(MANIFEST_FILE):
        print(f"[INFO] '{MANIFEST_FILE}' already exists.")
        return
    
    app_name = os.path.basename(os.getcwd())
    manifest = dict(DEFAULT_MANIFEST)
    manifest["name"] = app_name

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[SUCCESS] Created '{MANIFEST_FILE}' project manifest.")

def add_package(pkg: str):
    if not os.path.exists(MANIFEST_FILE):
        init_manifest()

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    if "dependencies" not in manifest:
        manifest["dependencies"] = {"enlang": [], "python": [], "web": []}

    if pkg.startswith("py:"):
        py_pkg = pkg[3:]
        print(f"[EPM] Installing Python PyPI package '{py_pkg}' via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", py_pkg], check=False)
        if py_pkg not in manifest["dependencies"]["python"]:
            manifest["dependencies"]["python"].append(py_pkg)

    elif pkg.startswith("web:"):
        web_pkg = pkg[4:]
        print(f"[EPM] Installing Web NPM package '{web_pkg}' via npm...")
        subprocess.run(["npm", "install", web_pkg], shell=True, check=False)
        if web_pkg not in manifest["dependencies"]["web"]:
            manifest["dependencies"]["web"].append(web_pkg)

    else:
        print(f"[EPM] Registered EnLang native package '{pkg}'.")
        if pkg not in manifest["dependencies"]["enlang"]:
            manifest["dependencies"]["enlang"].append(pkg)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[SUCCESS] Added '{pkg}' to '{MANIFEST_FILE}'.")

def install_dependencies():
    if not os.path.exists(MANIFEST_FILE):
        print(f"Error: '{MANIFEST_FILE}' not found. Run 'epm init' first.")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    deps = manifest.get("dependencies", {})
    
    # Python deps
    py_deps = deps.get("python", [])
    if py_deps:
        print(f"[EPM] Installing Python dependencies: {', '.join(py_deps)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + py_deps, check=False)

    # Web deps
    web_deps = deps.get("web", [])
    if web_deps:
        print(f"[EPM] Installing Web dependencies: {', '.join(web_deps)}")
        subprocess.run(["npm", "install"] + web_deps, shell=True, check=False)

    print("[SUCCESS] All project dependencies installed!")

def print_help():
    print("""
EnLang Package Manager (EPM) CLI — v2.0

USAGE:
  epm <command> [options]

COMMANDS:
  init                     Creates enlang.json manifest in current directory
  add <package>            Adds EnLang native package
  add py:<pip-package>     Installs Python package via pip (e.g. epm add py:requests)
  add web:<npm-package>    Installs Web JS/CSS package via npm (e.g. epm add web:chart.js)
  install                  Installs all dependencies listed in enlang.json
  version                  Displays EPM version & info
""")

if __name__ == "__main__":
    main()
