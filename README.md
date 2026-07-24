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

## 🚀 Quick Start & Installation

### Option 1: One-Click Windows GUI Installer
Download and run [`EnLangInstaller.exe`](EnLangInstaller.exe) to set up EnLang globally and automatically configure your system `PATH`.

### Option 2: CLI Package (`pip`)
```bash
pip install .
```

---

## 💡 Syntax Showcase

### Backend Logic (`main.enlg`)
```enlang
define text username as "Spandan"
define list items as ["Compiler", "NLP Engine", "Web Host"]

display "Welcome " plus username

match username:
    case "Spandan":
        display "Access Level: Lead Architect"
    default:
        display "Access Level: Guest"
end match

try:
    set score to @python(100 * 2)
    display "Score: " plus str(score)
except:
    display "Error occurred"
```

### Frontend Markup (`index.enlgf`)
```enlangf
page title "Lumina Workspace"

create header with class "top-bar":
    create nav with class "navbar":
        create h1 with text "Lumina"
        create a with href "#dashboard" with text "Dashboard"
    close nav
close header

create main with class "container":
    create hero with title "Welcome Developer", subtitle "Powered by EnLang Universal Core"
    create card named infoCard with title "Edge Node", description "Zero latency transpilation"
close main
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
