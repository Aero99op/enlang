"""
EnLang Version & Package Registry Manager
==========================================
Provides PyPI version fetching, auto-update checking, version listing, and explicit version installation.
"""

import sys
import os
import urllib.request
import json
import subprocess
from typing import List, Optional

PACKAGE_NAME = "enlang"
PYPI_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"

def get_installed_version() -> str:
    """Returns the currently installed version of EnLang."""
    try:
        from . import __version__
        return __version__
    except Exception:
        return "1.0.0"

def fetch_pypi_versions(timeout: float = 3.0) -> List[str]:
    """Fetches all published versions of enlang from PyPI."""
    try:
        req = urllib.request.Request(PYPI_URL, headers={"User-Agent": "EnLangCLI/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                releases = list(data.get("releases", {}).keys())
                # Sort versions logically
                def parse_ver(v_str):
                    parts = []
                    for p in v_str.split('.'):
                        try:
                            parts.append(int(p))
                        except ValueError:
                            parts.append(0)
                    return parts

                return sorted(releases, key=parse_ver)
    except Exception:
        pass
    return []

def get_latest_version(timeout: float = 2.0) -> Optional[str]:
    """Fetches the latest version string from PyPI."""
    versions = fetch_pypi_versions(timeout=timeout)
    return versions[-1] if versions else None

def check_for_updates():
    """Non-blocking update notifier checked during CLI execution."""
    current = get_installed_version()
    latest = get_latest_version(timeout=1.0)
    if latest and latest != current:
        print(f"\n[UPDATE AVAILABLE] EnLang v{latest} is live on PyPI! (Current: v{current})")
        print(f"   Run 'enlang update' or 'pip install --upgrade enlang' to update.\n")

def list_versions():
    """Lists all available versions of EnLang published on PyPI."""
    current = get_installed_version()
    print(f"\n[INFO] Fetching published versions for '{PACKAGE_NAME}' from PyPI...")
    versions = fetch_pypi_versions(timeout=4.0)

    if not versions:
        print("[WARNING] Could not fetch versions from PyPI (Network offline or package not found).")
        print(f"Current installed version: v{current}")
        return

    print("\n==================================================")
    print(f" ENLANG PUBLISHED VERSIONS (PyPI Registry)")
    print("==================================================")
    for v in versions:
        if v == current:
            print(f"  --> v{v}  <-- [INSTALLED / CURRENT]")
        else:
            print(f"      v{v}")
    print("==================================================")
    print("Usage to install a specific version:")
    print("  enlang install 2.0.0      OR  pip install enlang==2.0.0")
    print("  enlang install latest     OR  enlang update\n")

def update_to_latest():
    """Upgrades EnLang to the latest PyPI release seamlessly on all OS (Windows/Linux/macOS)."""
    current = get_installed_version()
    latest = get_latest_version(timeout=3.0)
    print(f"[INFO] Current installed version: v{current}")
    if latest:
        print(f"[INFO] Latest PyPI version: v{latest}")
        if latest == current:
            print("[SUCCESS] You are already using the latest version of EnLang!")
            return

    print(f"[INFO] Upgrading EnLang to v{latest} via pip...")
    if os.name == "nt":
        # Windows detached process execution to unlock enlang.exe
        cmd_str = f'"{sys.executable}" -m pip install --upgrade --user {PACKAGE_NAME}'
        subprocess.Popen(f'cmd /c "timeout /t 1 /nobreak >nul && {cmd_str}"', shell=True)
        print("[SUCCESS] Update initiated in background! EnLang will be updated in 1 second.")
    else:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME]
        res = subprocess.run(cmd, check=False)
        if res.returncode == 0:
            print("[SUCCESS] EnLang upgraded successfully to latest version!")
        else:
            print(f"[ERROR] Upgrade failed. Try running: pip install --upgrade {PACKAGE_NAME}")

def install_specific_version(target_version: str):
    """Installs a specific version of EnLang seamlessly on all OS."""
    if target_version.lower() in ("latest", "upgrade"):
        update_to_latest()
        return

    # Clean leading 'v' if passed e.g. v2.0.0 -> 2.0.0
    if target_version.startswith("v"):
        target_version = target_version[1:]

    spec = f"{PACKAGE_NAME}=={target_version}"
    print(f"[INFO] Installing specific EnLang version '{target_version}'...")
    if os.name == "nt":
        # Windows detached process execution to unlock enlang.exe
        cmd_str = f'"{sys.executable}" -m pip install --user {spec}'
        subprocess.Popen(f'cmd /c "timeout /t 1 /nobreak >nul && {cmd_str}"', shell=True)
        print(f"[SUCCESS] Installation of EnLang v{target_version} initiated in background!")
    else:
        cmd = [sys.executable, "-m", "pip", "install", spec]
        res = subprocess.run(cmd, check=False)
        if res.returncode == 0:
            print(f"[SUCCESS] Successfully installed EnLang v{target_version}!")
        else:
            print(f"[ERROR] Failed to install EnLang v{target_version}.")
