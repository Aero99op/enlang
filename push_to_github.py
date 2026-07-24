import subprocess
import sys

def run(cmd):
    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(res.stderr)
    return res.returncode

print("--- EnLang GitHub Auto-Pusher ---")
run(["git", "branch", "-M", "main"])
run(["git", "add", "."])
run(["git", "commit", "-m", "EnLang v2.0 Enterprise Specification Edition - Full Engine, Compiler, CLI, EPM, Book and GUI Installer"])
print("--- Pushing to GitHub (https://github.com/Aero99op/enlang.git) ---")
ret = run(["git", "push", "-u", "origin", "main", "--force"])
if ret == 0:
    print("[SUCCESS] Successfully pushed EnLang v2.0 to GitHub repository!")
else:
    print("[WARNING] Push returned non-zero code. Checking if authentication or alternate branch needed.")
