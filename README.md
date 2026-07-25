# EnLang — The Universal Natural English Programming Language
### *Build Full-Stack Applications Using Natural English*

[![Version](https://img.shields.io/badge/version-2.0.0--Enterprise-indigo.svg)](https://github.com/Aero99op/enlang)
[![License](https://img.shields.io/badge/license-Proprietary%20%2F%20Enterprise-blue.svg)](LICENSE)
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

## 🚀 Official Installation Methods

EnLang is distributed as a compiled distribution engine. You can install EnLang globally on your system using either of the following official methods:

### 1️⃣ Method 1: One-Click Windows GUI Installer (Recommended)
Download and launch the official compiled setup wizard:
👉 **[Download EnLangInstaller.exe](https://raw.githubusercontent.com/Aero99op/enlang/main/EnLangInstaller.exe)**

*The GUI Installer automatically extracts the core runtime binaries to `%USERPROFILE%\.enlang\` and registers the system `PATH` environment variable.*

### 2️⃣ Method 2: CLI Package Installation (`pip`)
Install EnLang directly into your Python CLI environment using `pip`:

```bash
pip install enlang
```

---

## 🛠️ Global CLI Tooling

Once installed via GUI or `pip`, open any command prompt or terminal and use:

```bash
enlang run main.enlg          # Compiles and executes EnLang program
enlang check main.enlg        # Runs static analysis & syntax linter
enlang debug main.enlg        # Launches step-by-step interactive debugger
enlang build index.enlgf      # Transpiles source to native target file (.py, .html, .css, .js, .sql)
enlang server --port 8000     # Launches zero-config EnLang HTTP web server
epm init                      # Initializes a new EnLang project package
```

---

## 💡 Syntax Showcase

```enlang
define text username as "Spandan"

function numbers using n:
    if n is greater than 10 then:
        return
    display n
    call numbers with (n plus 1)

start numbers from 1
```

---

## 📚 Official Master Textbook & Specification
The official 590-page master reference textbook **"EnLang Programming Language: The Complete Enterprise Master Reference & Architecture Guide (v2.0.0)"** is available in this repository:
- 📄 **[enlangbookv2release.pdf](enlangbookv2release.pdf)** (590 Pages, 10 Volumes, 50 Detailed Specs, 1,000 Solved Problems)

---

## 📜 Distribution & Rights
Copyright © 2026 Spandan Prayas Patra. All rights reserved.  
Distributed via official GUI Standalone Binary & PyPI Package Manager (`pip`).
