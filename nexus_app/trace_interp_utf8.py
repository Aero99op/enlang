import sys
sys.path.insert(0, r"d:\enlangg")
from enlang_core.interpreter import EnLangInterpreter

interp = EnLangInterpreter()
with open(r"d:\enlangg\nexus_app\nexus_pages.enlg", "r", encoding="utf-8") as f:
    src = f.read()

success, stdout, stderr, py_code = interp.run_code(src, file_path=r"d:\enlangg\nexus_app\nexus_pages.enlg")
with open(r"d:\enlangg\nexus_app\interp_debug.txt", "w", encoding="utf-8") as f:
    f.write(f"SUCCESS: {success}\n")
    f.write(f"STDOUT LEN: {len(stdout)}\n")
    f.write(f"STDERR:\n{stderr}\n")
    f.write(f"PY CODE:\n{py_code}\n")

print("Wrote interp_debug.txt successfully.")
