"""
EnLang GUI Setup Wizard Installer
=================================
Graphical installer (Tkinter GUI) for setting up EnLang globally.

Features:
  1. Customizable Installation Directory path selection (Browse button).
  2. Checkbox option to automatically add EnLang bin path to Windows PATH.
  3. Real-time installation progress log.
  4. Silent / CLI execution fallback (--silent or --cli).
"""

import os
import sys
import shutil
import subprocess
import winreg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

DEFAULT_INSTALL_DIR = os.path.expanduser(r"~\.enlang")

class EnLangInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EnLang v2.0 Enterprise Setup Wizard")
        self.root.geometry("640x520")
        self.root.resizable(False, False)

        # Styling & Theme
        self.BG_DARK = "#0f172a"
        self.PRIMARY = "#4f46e5"
        self.ACCENT = "#38bdf8"
        self.TEXT_WHITE = "#f8fafc"
        self.TEXT_MUTED = "#94a3b8"

        self.root.configure(bg=self.BG_DARK)

        self._create_widgets()

    def _create_widgets(self):
        # 1. Header Banner
        header_frame = tk.Frame(self.root, bg=self.PRIMARY, height=90)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="EnLang Universal Language Setup",
            font=("Segoe UI", 16, "bold"),
            fg=self.TEXT_WHITE,
            bg=self.PRIMARY,
            anchor="w",
            padx=20,
            pady=10
        )
        title_label.pack(fill="x")

        sub_label = tk.Label(
            header_frame,
            text="Version 1.2.8 — Enterprise Specification Edition | Author: Spandan Prayas Patra",
            font=("Segoe UI", 9),
            fg="#c7d2fe",
            bg=self.PRIMARY,
            anchor="w",
            padx=20
        )
        sub_label.pack(fill="x")

        # Main Body Frame
        body_frame = tk.Frame(self.root, bg=self.BG_DARK, padx=20, pady=15)
        body_frame.pack(fill="both", expand=True)

        # 2. Installation Path Selection
        path_label = tk.Label(
            body_frame,
            text="Select Installation Directory:",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_WHITE,
            bg=self.BG_DARK
        )
        path_label.pack(anchor="w", pady=(5, 5))

        path_entry_frame = tk.Frame(body_frame, bg=self.BG_DARK)
        path_entry_frame.pack(fill="x", pady=(0, 10))

        self.path_var = tk.StringVar(value=DEFAULT_INSTALL_DIR)
        self.path_entry = tk.Entry(
            path_entry_frame,
            textvariable=self.path_var,
            font=("Consolas", 10),
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief="flat",
            bd=5
        )
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=3)

        browse_btn = tk.Button(
            path_entry_frame,
            text="Browse...",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg=self.TEXT_WHITE,
            activebackground=self.PRIMARY,
            activeforeground=self.TEXT_WHITE,
            relief="flat",
            padx=15,
            command=self._browse_directory
        )
        browse_btn.pack(side="right", padx=(10, 0))

        # 3. Environment Options Checkbox
        self.add_path_var = tk.BooleanVar(value=True)
        path_chk = tk.Checkbutton(
            body_frame,
            text="Add EnLang bin path automatically to System Environment Variables (PATH)",
            variable=self.add_path_var,
            font=("Segoe UI", 9),
            fg=self.TEXT_WHITE,
            bg=self.BG_DARK,
            selectcolor="#1e293b",
            activebackground=self.BG_DARK,
            activeforeground=self.ACCENT
        )
        path_chk.pack(anchor="w", pady=(0, 15))

        # 4. Installation Log Window
        log_label = tk.Label(
            body_frame,
            text="Installation Log:",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_DARK
        )
        log_label.pack(anchor="w", pady=(0, 3))

        self.log_text = tk.Text(
            body_frame,
            height=10,
            font=("Consolas", 9),
            bg="#020617",
            fg="#38bdf8",
            relief="flat",
            bd=5,
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, pady=(0, 15))

        # 5. Footer Action Buttons
        footer_frame = tk.Frame(body_frame, bg=self.BG_DARK)
        footer_frame.pack(fill="x", side="bottom")

        self.install_btn = tk.Button(
            footer_frame,
            text="Install Now",
            font=("Segoe UI", 11, "bold"),
            bg=self.PRIMARY,
            fg=self.TEXT_WHITE,
            activebackground="#4338ca",
            activeforeground=self.TEXT_WHITE,
            relief="flat",
            padx=25,
            pady=6,
            command=self._start_installation_thread
        )
        self.install_btn.pack(side="right")

        cancel_btn = tk.Button(
            footer_frame,
            text="Cancel",
            font=("Segoe UI", 10),
            bg="#334155",
            fg=self.TEXT_WHITE,
            relief="flat",
            padx=15,
            pady=6,
            command=self.root.quit
        )
        cancel_btn.pack(side="right", padx=(0, 10))

    def _browse_directory(self):
        chosen = filedialog.askdirectory(
            title="Select EnLang Installation Folder",
            initialdir=self.path_var.get()
        )
        if chosen:
            self.path_var.set(os.path.normpath(chosen))

    def log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _start_installation_thread(self):
        self.install_btn.config(state="disabled")
        threading.Thread(target=self._run_installation, daemon=True).start()

    def _run_installation(self):
        target_dir = self.path_var.get().strip()
        add_to_env = self.add_path_var.get()

        if not target_dir:
            messagebox.showerror("Error", "Please select a valid installation directory.")
            self.install_btn.config(state="normal")
            return

        bin_dir = os.path.join(target_dir, "bin")
        core_dir = os.path.join(target_dir, "enlang_core")

        try:
            self.log(f"[1/4] Creating directory: {target_dir}")
            os.makedirs(bin_dir, exist_ok=True)
            os.makedirs(core_dir, exist_ok=True)

            # Detect source core directory
            if getattr(sys, 'frozen', False):
                src_root = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            else:
                src_root = os.path.dirname(os.path.abspath(__file__))

            src_core = os.path.join(src_root, "enlang_core")
            if not os.path.exists(src_core):
                src_core = os.path.join(os.path.dirname(src_root), "enlang_core")

            self.log("[2/4] Copying EnLang Core Transpiler Engine...")
            if os.path.exists(src_core):
                for item in os.listdir(src_core):
                    s_file = os.path.join(src_core, item)
                    d_file = os.path.join(core_dir, item)
                    if os.path.isfile(s_file):
                        shutil.copy2(s_file, d_file)
                    elif os.path.isdir(s_file):
                        if os.path.exists(d_file):
                            shutil.rmtree(d_file)
                        shutil.copytree(s_file, d_file)
                self.log("      -> Core files installed successfully.")
            else:
                self.log(f"[WARNING] Source core path not found: {src_core}")

            self.log("[3/4] Creating executable wrappers (enlang.bat, epm.bat)...")
            
            py_exec = "python"
            enlang_bat_content = f'@echo off\n{py_exec} "{os.path.join(core_dir, "cli.py")}" %*\n'
            epm_bat_content = f'@echo off\n{py_exec} "{os.path.join(core_dir, "epm.py")}" %*\n'

            with open(os.path.join(bin_dir, "enlang.bat"), "w", encoding="utf-8") as f:
                f.write(enlang_bat_content)

            with open(os.path.join(bin_dir, "epm.bat"), "w", encoding="utf-8") as f:
                f.write(epm_bat_content)

            self.log("      -> Wrappers generated in bin/.")

            if add_to_env:
                self.log("[4/4] Updating Windows PATH environment variable...")
                self._update_win_path(bin_dir)
            else:
                self.log("[4/4] Skipping PATH modification per user selection.")

            self.log("\n=======================================================")
            self.log("  [SUCCESS] EnLang v2.0 Setup Completed Successfully!")
            self.log("=======================================================")
            
            messagebox.showinfo(
                "Installation Complete",
                f"EnLang v2.0 has been successfully installed to:\n{target_dir}\n\n"
                f"Bin Path: {bin_dir}\n"
                f"PATH Registered: {'Yes' if add_to_env else 'No'}\n\n"
                "You can now open any terminal and type 'enlang version' or 'enlang run app.enlg'!"
            )

        except Exception as e:
            self.log(f"[ERROR] Installation failed: {e}")
            messagebox.showerror("Installation Error", f"Failed to install EnLang:\n{e}")

        finally:
            self.install_btn.config(state="normal")

    def _update_win_path(self, target_bin_dir: str):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""

            paths = [p.strip() for p in current_path.split(";") if p.strip()]
            if target_bin_dir.lower() in [p.lower() for p in paths]:
                self.log(f"      -> PATH already includes: {target_bin_dir}")
                winreg.CloseKey(key)
                return

            paths.append(target_bin_dir)
            new_path = ";".join(paths)

            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            self.log(f"      -> Added to Windows User PATH Registry.")

            ps_cmd = (
                f"[Environment]::SetEnvironmentVariable('Path', "
                f"[Environment]::GetEnvironmentVariable('Path', 'User'), 'User')"
            )
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

        except Exception as e:
            self.log(f"[WARNING] Registry PATH update warning: {e}")

def main():
    # If launched with --silent or --cli, run non-interactive CLI install
    if "--silent" in sys.argv or "--cli" in sys.argv:
        from installer import install_enlang
        install_enlang()
        return

    root = tk.Tk()
    app = EnLangInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
