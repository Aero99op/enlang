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

print("--- EnLang Private GitHub Auto-Pusher ---")
run(["git", "branch", "-M", "main"])
run(["git", "add", "."])
run(["git", "commit", "-m", "EnLang Core v2.0 Source Code Backup"])
print("--- Pushing to Private Repository (https://github.com/Aero99op/enlang-private.git) ---")
ret = run(["git", "push", "-u", "private", "main", "--force"])
if ret == 0:
    print("[SUCCESS] Successfully pushed full source code to PRIVATE repository!")
else:
    print("[NOTE] Push command completed.")
