import sys
sys.path.insert(0, r"d:\enlangg")
from enlang_core.transpiler import EnLangTranspiler

with open(r"d:\enlangg\nexus_app\nexus_pages.enlg", "r", encoding="utf-8") as f:
    src = f.read()

t = EnLangTranspiler()
py_code = t.transpile(src, file_path=r"d:\enlangg\nexus_app\nexus_pages.enlg")

with open(r"d:\enlangg\nexus_app\py_out.txt", "w", encoding="utf-8") as f:
    f.write(py_code)

print("Transpiled Python Code Length:", len(py_code))
