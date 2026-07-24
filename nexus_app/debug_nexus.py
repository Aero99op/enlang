import sys
sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import _run_enlg_file

out = _run_enlg_file(r"d:\enlangg\nexus_app\nexus_pages.enlg")
print("=== NEXUS PAGES OUTPUT ===")
print("LENGTH:", len(out))
print(out[:500])
