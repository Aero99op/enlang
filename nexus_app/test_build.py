import sys
import os
import glob
import re

sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import _run_enlg_file

os.chdir(r"d:\enlangg\nexus_app")
cwd = os.getcwd()

print("CWD:", cwd)
print("ENLGD FILES:", glob.glob(os.path.join(cwd, "*.enlgd")))
print("ENLG FILES:", glob.glob(os.path.join(cwd, "*.enlg")))

html_body = ""
for f in sorted(glob.glob(os.path.join(cwd, "*.enlg"))):
    with open(f, "r", encoding="utf-8") as fh:
        src = fh.read()
    match = bool(re.search(r'@on\s+<?frontend>?', src, re.IGNORECASE))
    print(f"File {f}: @on frontend match = {match}")
    if match:
        out = _run_enlg_file(f)
        print(f"File {f} output len:", len(out))
        for line in out.splitlines():
            if not line.strip().startswith('#'):
                html_body += line + "\n"

print("TOTAL HTML BODY LEN:", len(html_body))
