import sys
import os
import glob
import re

sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import _run_enlg_file

os.chdir(r"d:\enlangg\aero_app")
cwd = os.getcwd()

print("CWD:", cwd)
print("ENLGD FILES:", glob.glob(os.path.join(cwd, "*.enlgd")))
print("ENLG FILES:", glob.glob(os.path.join(cwd, "*.enlg")))
print("ENLGS FILES:", glob.glob(os.path.join(cwd, "*.enlgs")))

for f in sorted(glob.glob(os.path.join(cwd, "*.enlg"))):
    out = _run_enlg_file(f)
    print(f"File {f} output len:", len(out))

for f in sorted(glob.glob(os.path.join(cwd, "*.enlgd"))):
    out = _run_enlg_file(f)
    print(f"File {f} output len:", len(out))

for f in sorted(glob.glob(os.path.join(cwd, "*.enlgs"))):
    out = _run_enlg_file(f)
    print(f"File {f} output len:", len(out))
