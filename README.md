# EnLang — The Universal Natural English Programming Language
### *Build Full-Stack Web Applications, Algorithms & Databases Using Natural English*

[![Version](https://img.shields.io/badge/version-1.0.0--Stable-indigo.svg)](https://pypi.org/project/enlang/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/enlang.svg)](https://pypi.org/project/enlang/)
[![Tests](https://img.shields.io/badge/tests-154%2F154%20PASS-success.svg)](tests/)

Created and Authored by **Spandan Prayas Patra**.

---

## 🌟 Overview
**EnLang** is a deterministic, universal multi-target programming language and transpilation engine that converts natural English into 1:1 clean, production-grade native code targets:

- **`.enlg`** ➔ Core Backend Logic & Algorithms (Python 3)
- **`.enlgf`** ➔ Structural Frontend Markup (HTML5)
- **`.enlgd`** ➔ Styling & Design Systems (CSS3)
- **`.enlgs`** ➔ Client Scripting & DOM Logic (JavaScript ES6+)
- **`.enlgdb`** ➔ Database Schemas & Queries (ANSI SQL / SQLite)

---

## 🚀 Official Installation

Install EnLang globally on your system using `pip`:

```bash
pip install enlang
```

To update to the latest version at any time:

```bash
enlang update
# OR
pip install --upgrade enlang
```

---

## 🛠️ Complete CLI Command Reference

Once installed, use the `enlang` and `epm` CLI tools anywhere in your terminal:

### 1️⃣ Execution & Web Server Commands
```bash
enlang run app.enlg                   # Executes backend Python script directly
enlang run index.enlgf                # Auto-compiles web app & starts live dev server (Auto-port)
enlang run index.enlgf -p 3000        # Runs live web app on custom port (e.g. 3000)
enlang run schema.enlgdb              # Compiles SQL, creates SQLite .db, & renders ASCII Data Tables
enlang server --port 8000             # Launches zero-config EnLang HTTP web server
```

### 2️⃣ Compilation & Build Commands
```bash
enlang build index.enlgf              # Compiles to pure W3C index.html
enlang build style.enlgd              # Compiles to pure CSS3 style.css
enlang build app.enlgs                # Compiles to pure ES6+ JS app.js
enlang build schema.enlgdb            # Compiles to pure ANSI SQL schema.sql
enlang build main.enlg                # Compiles to pure Python main.py
```

### 3️⃣ Registry & Version Management
```bash
enlang versions                       # Lists all published PyPI versions with current highlight
enlang install 2.0.0                  # Installs a specific version of EnLang
enlang update                         # Upgrades EnLang to the latest PyPI release
enlang version                        # Displays installed EnLang compiler version
```

### 4️⃣ Analysis & Debugging
```bash
enlang check main.enlg                # Performs static analysis and syntax linting
enlang debug main.enlg                # Launches step-by-step interactive debugger
```

### 5️⃣ EPM Package Manager (`epm`)
```bash
epm init                              # Creates enlang.json project manifest
epm add py:requests                   # Installs Python PyPI dependency
epm add web:chart.js                  # Installs Web NPM dependency
epm install                           # Installs all dependencies listed in enlang.json
```

---

## 💡 Multi-Target Syntax Showcase

### 📄 HTML Frontend Markup (`index.enlgf`)
```enlgf
page title "Minimalist Experience"
include stylesheet "style.css"
create script with src "app.js"

create main with class "hero":
    create h1 with class "hero-title" with text "Simplicity is Sophistication"
    create button with id "btnStart" with class "btn" with text "Get Started"
close main
```

### 🗄️ Database Schema (`schema.enlgdb`)
```enlgdb
define table users with columns id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL UNIQUE
insert into users columns (username, email) values ('Spandan', 'spandan@enlang.org')
select all from users
```

---

## 📚 Master Textbook & Documentation
The official 612-page master textbook **"EnLang Programming Language: The Complete Enterprise Master Reference & Architecture Guide"** is included in the codebase:
- 📄 **[enlangbookv2release.pdf](enlangbookv2release.pdf)** (612 Pages, 630 Detailed Chapters, Master Architecture Guide)

---

## 📜 License & Rights
Copyright © 2026 Spandan Prayas Patra (`spandanpatra1234@gmail.com`).  
Distributed under the MIT License via PyPI Package Manager (`pip install enlang`).
