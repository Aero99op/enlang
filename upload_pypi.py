import sys
import os
import subprocess

def upload_to_pypi(token=None):
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
    
    if not token:
        token = os.environ.get("PYPI_TOKEN")

    if not token:
        print("================================================================")
        print("  ENLANG PYPI UPLOADER v1.2.0")
        print("================================================================")
        print("  Usage: python upload_pypi.py <pypi-token>")
        print("  Example: python upload_pypi.py pypi-AgEI...your-token-here")
        print("================================================================")
        return

    cmd = [
        "twine", "upload",
        "dist/enlang-*",
        "--skip-existing",
        "-u", "__token__",
        "-p", token
    ]

    print(f"Uploading dist/enlang-* to PyPI...")
    res = subprocess.run(cmd, text=True)
    if res.returncode == 0:
        print("================================================================")
        print("  [SUCCESS] Successfully uploaded enlang latest release to PyPI!")
        print("  Install with: pip install --upgrade enlang")
        print("================================================================")
    else:
        print(f"[ERROR] Twine upload failed with return code {res.returncode}")

if __name__ == "__main__":
    upload_to_pypi()
