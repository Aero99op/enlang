"""
Build & Transpile Script for Retro Minimalist Web Application
Executes EnLang transpiled scripts to generate pure, static HTML5, CSS3, and JS files.
Author: Spandan Prayas Patra
"""
import os
import sys

# Add root directory to sys.path to import enlang_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from enlang_core import EnLangInterpreter

def build_retro_web():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    interpreter = EnLangInterpreter()

    files = [
        ("index.enlgf", "index.html"),
        ("about.enlgf", "about.html"),
        ("gallery.enlgf", "gallery.html"),
        ("guestbook.enlgf", "guestbook.html"),
        ("style.enlgd", "style.css"),
        ("app.enlgs", "app.js"),
    ]

    print("[INFO] Building Minimalist Retro Web Application using EnLang sub-transpilers...")

    for src_name, out_name in files:
        src_path = os.path.join(base_dir, src_name)
        out_path = os.path.join(base_dir, out_name)

        if not os.path.exists(src_path):
            print(f"[ERROR] Source file missing: {src_path}")
            continue

        with open(src_path, "r", encoding="utf-8") as f:
            source = f.read()

        success, stdout, stderr, _ = interpreter.run_code(source, file_path=src_name)

        if not success:
            print(f"[ERROR] Transpilation failed for {src_name}:\n{stderr}")
            continue

        # Strip python print execution traces if any, output clean target code
        clean_target = stdout

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(clean_target)

        size = os.path.getsize(out_path)
        print(f"[SUCCESS] Transpiled '{src_name}' -> '{out_name}' ({size} bytes)")

    print("\n[SUCCESS] Retro Web Application compiled successfully!")
    print(f"[INFO] Files built in directory: {base_dir}")

if __name__ == "__main__":
    build_retro_web()
