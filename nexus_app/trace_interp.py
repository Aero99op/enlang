import sys
sys.path.insert(0, r"d:\enlangg")
from enlang_core.interpreter import EnLangInterpreter

interp = EnLangInterpreter()
with open(r"d:\enlangg\nexus_app\nexus_pages.enlg", "r", encoding="utf-8") as f:
    src = f.read()

success, stdout, stderr, py_code = interp.run_code(src, file_path=r"d:\enlangg\nexus_app\nexus_pages.enlg")
print("SUCCESS:", success)
print("STDOUT LEN:", len(stdout))
print("STDERR:", stderr)
print("PY CODE TOP 200 BARS:")
print(py_code[:300])
