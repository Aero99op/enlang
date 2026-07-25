# EnLang — The Universal Natural English Programming Language
### *Build Full-Stack Applications Using Natural English*

[![Version](https://img.shields.io/badge/version-2.0.0--Enterprise-indigo.svg)](https://github.com/Aero99op/enlang)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-154%2F154%20PASS-success.svg)](tests/)

Created and Authored by **Spandan Prayas Patra**.

---

## 🌟 Overview
**EnLang** is a deterministic, universal multi-target programming language and transpilation engine that converts natural English into 1:1 clean, production-grade native targets:

- **`.enlg`** ➔ Core Backend Logic & Algorithms (Python 3)
- **`.enlgf`** ➔ Structural Frontend Markup (HTML5)
- **`.enlgd`** ➔ Styling & Design Systems (CSS3)
- **`.enlgs`** ➔ Client Scripting & DOM Logic (JavaScript ES6+)
- **`.enlgdb`** ➔ Database Schemas & Queries (SQL)

---

## 🚀 Installation Options

### 1️⃣ Option 1: One-Click Windows GUI Installer (Executable)
Download and double-click [`EnLangInstaller.exe`](https://raw.githubusercontent.com/Aero99op/enlang/main/EnLangInstaller.exe) to launch the GUI Setup Wizard. It installs EnLang and configures your system `PATH` automatically.

### 2️⃣ Option 2: Direct CLI Installation via `pip` (One Command)
Run this single command in your terminal/command prompt:
```bash
pip install git+https://github.com/Aero99op/enlang.git
```

### 3️⃣ Option 3: Manual Git Clone & Setup
```bash
git clone https://github.com/Aero99op/enlang.git
cd enlang
python installer.py
```

---

## 🛠️ Developer CLI Tooling

Once installed, use the global `enlang` CLI commands anywhere on your system:

```bash
enlang run main.enlg          # Compiles and executes EnLang program
enlang check main.enlg        # Runs static analysis & syntax linter
enlang debug main.enlg        # Launches step-by-step interactive debugger
enlang build index.enlgf      # Transpiles source to native target file (.py, .html, .css, .js, .sql)
enlang server --port 8000     # Launches zero-config EnLang HTTP web server
```

---

## 💡 Syntax Showcase

### Backend Logic (`main.enlg`)
```enlang
define text username as "Spandan"
define list items as ["Compiler", "NLP Engine", "Web Host"]

display "Welcome " plus username

function numbers using n:
    if n is greater than 10 then:
        return
    display n
    call numbers with (n plus 1)

start numbers from 1
```

---

## 📚 Documentation & Book
The official specification book **"EnLang for Developers: Enterprise Specification Edition (v2.0)"** is available in this repository:
- 📖 [ENLANG_FOR_DEVELOPERS_BOOK.md](ENLANG_FOR_DEVELOPERS_BOOK.md)
- 📄 [ENLANG_FOR_DEVELOPERS_BOOK.pdf](ENLANG_FOR_DEVELOPERS_BOOK.pdf)

---

## 📜 License
Published under the Open EnLang Specification License / MIT.  
Copyright © 2026 Spandan Prayas Patra. All rights reserved.
