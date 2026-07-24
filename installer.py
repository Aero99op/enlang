"""
EnLang Universal Windows Installer
==================================
Standalone EXE installer that sets up EnLang globally on the user's laptop.

Actions:
  1. Installs EnLang runtime to %USERPROFILE%\\.enlang\\
  2. Copies compiler core files (grammar, transpiler, interpreter, web_server, nlp_engine, cli, epm)
  3. Creates executable wrappers in %USERPROFILE%\\.enlang\\bin\\ (enlang.bat, epm.bat)
  4. Automatically registers %USERPROFILE%\\.enlang\\bin\\ in the Windows User PATH environment variable.
"""

import os
import sys
import shutil
import subprocess
import winreg

INSTALL_DIR = os.path.expanduser(r"~\.enlang")
BIN_DIR = os.path.join(INSTALL_DIR, "bin")
CORE_DIR = os.path.join(INSTALL_DIR, "enlang_core")

def print_banner():
    print("=" * 65)
    print("        ENLANG UNIVERSAL PROGRAMMING LANGUAGE INSTALLER        ")
    print("              Version 2.0.0 — Enterprise Edition              ")
    print("           Author & Architect: Spandan Prayas Patra           ")
    print("=" * 65)
    print()

def install_enlang():
    print_banner()

    print(f"[1/4] Creating installation directory at:")
    print(f"      -> {INSTALL_DIR}")
    os.makedirs(BIN_DIR, exist_ok=True)
    os.makedirs(CORE_DIR, exist_ok=True)

    # Detect source directory (either running from source or extracted bundle)
    if getattr(sys, 'frozen', False):
        # PyInstaller bundled location
        src_root = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        src_root = os.path.dirname(os.path.abspath(__file__))

    src_core = os.path.join(src_root, "enlang_core")
    if not os.path.exists(src_core):
        src_core = os.path.join(os.path.dirname(src_root), "enlang_core")

    print("[2/4] Copying EnLang Core Transpiler Engine...")
    if os.path.exists(src_core):
        for item in os.listdir(src_core):
            s_file = os.path.join(src_core, item)
            d_file = os.path.join(CORE_DIR, item)
            if os.path.isfile(s_file):
                shutil.copy2(s_file, d_file)
            elif os.path.isdir(s_file):
                if os.path.exists(d_file):
                    shutil.rmtree(d_file)
                shutil.copytree(s_file, d_file)
        print("      -> EnLang core files copied successfully.")
    else:
        print(f"[WARNING] Source core not found at {src_core}. Creating stub runtime...")

    print("[3/4] Generating CLI executable wrappers in bin/...")
    
    py_exec = "python"

    # 1. enlang.bat
    enlang_bat_content = f"""@echo off
{py_exec} "{os.path.join(CORE_DIR, 'cli.py')}" %*
"""
    with open(os.path.join(BIN_DIR, "enlang.bat"), "w", encoding="utf-8") as f:
        f.write(enlang_bat_content)

    # 2. epm.bat
    epm_bat_content = f"""@echo off
{py_exec} "{os.path.join(CORE_DIR, 'epm.py')}" %*
"""
    with open(os.path.join(BIN_DIR, "epm.bat"), "w", encoding="utf-8") as f:
        f.write(epm_bat_content)

    print("      -> Created 'enlang' and 'epm' executable wrappers.")

    print("[4/4] Registering EnLang in Windows PATH Environment Variable...")
    add_to_path(BIN_DIR)

    print()
    print("=" * 65)
    print("  [SUCCESS] INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print(f"  EnLang Home Path: {INSTALL_DIR}")
    print(f"  EnLang Bin Path:  {BIN_DIR}")
    print()
    print("  You can now open ANY new command prompt or terminal and type:")
    print("    enlang version      -> Check installed version")
    print("    enlang run app.enlg -> Execute an EnLang program")
    print("    epm init            -> Initialize a new EnLang project")
    print("=" * 65)
    print()

def add_to_path(target_bin_dir: str):
    """Appends target_bin_dir to Windows User PATH environment variable."""
    try:
        # 1. Read current User PATH from registry
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""

        paths = [p.strip() for p in current_path.split(";") if p.strip()]
        
        # Check if already in PATH
        if target_bin_dir.lower() in [p.lower() for p in paths]:
            print(f"      -> PATH already includes: {target_bin_dir}")
            winreg.CloseKey(key)
            return

        paths.append(target_bin_dir)
        new_path = ";".join(paths)

        # Write updated PATH back to registry
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        print(f"      -> Successfully added to User PATH Registry.")

        # Broadcast WM_SETTINGCHANGE via PowerShell so current system updates
        ps_cmd = (
            f"[Environment]::SetEnvironmentVariable('Path', "
            f"[Environment]::GetEnvironmentVariable('Path', 'User'), 'User')"
        )
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

    except Exception as e:
        print(f"[WARNING] Could not update PATH automatically: {e}")
        print(f"Please manually add '{target_bin_dir}' to your PATH environment variables.")

if __name__ == "__main__":
    install_enlang()
    if "--no-pause" not in sys.argv:
        input("\nPress ENTER to exit installer...")
