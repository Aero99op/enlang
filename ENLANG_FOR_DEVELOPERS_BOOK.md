# ENLANG FOR DEVELOPERS
### *The Definitive Guide to Building Full-Stack Software with Natural English*

**Author:** Spandan Prayas Patra  
**Version:** 2.0.0 — Enterprise Specification Edition  
**Publisher:** Universal EnLang Foundation Press  

---

> *"Programming should be as clear, expressive, and frictionless as human thought. EnLang makes natural English a first-class, production-grade programming language across the entire software stack."*  
> — **Spandan Prayas Patra**

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction & Philosophical Architecture**
2. **Chapter 2: Variables, Optional Types, Output & Expression Syntax**
3. **Chapter 3: The 3-Level Native Interactivity Architecture**
4. **Chapter 4: Comprehensive Loop Taxonomy (For, While, Repeat, Recursion)**
5. **Chapter 5: Functions, Natural Declarations, Interfaces & Async / Await**
6. **Chapter 6: Pattern Matching & Decision Engine**
7. **Chapter 7: Exception Handling & Error Control**
8. **Chapter 8: Built-in Collections — Lists, Arrays, Dictionaries, Sets**
9. **Chapter 9: String Manipulations, Math & DateTime Primitives**
10. **Chapter 10: File I/O, System Operations & Security**
11. **Chapter 11: Frontend Structural Markup (`.enlgf` → HTML5)**
12. **Chapter 12: Styling & Design Systems (`.enlgd` → CSS3)**
13. **Chapter 13: Client-Side Scripting (`.enlgs` → JavaScript ES6+)**
14. **Chapter 14: Database Schemas & Queries (`.enlgdb` → SQL)**
15. **Chapter 15: Native NLP & AI Primitives**
16. **Chapter 16: EnLang Web Server & Multi-File Architecture**
17. **Chapter 17: Developer Tooling — Syntax Checker, Linter & Interactive Debugger**
18. **Chapter 18: Canonical Grammar Rules, Order & Syntax Layout Specification**
19. **Chapter 19: Complete Production Case Study — Lumina Workspace**
20. **Appendix A: Universal Natural Syntax Cheatsheet**
21. **Appendix B: CLI & EnLang Package Manager (EPM) Manual**

---

# CHAPTER 17: DEVELOPER TOOLING — SYNTAX CHECKER, LINTER & INTERACTIVE DEBUGGER

EnLang includes enterprise-grade developer tooling for static code analysis, linting, and step-by-step interactive debugging.

## 17.1 EnLang Static Syntax Checker & Linter (`enlang check`)
The `enlang check` command performs static analysis on EnLang source files without executing them.

```bash
enlang check main.enlg
```

### Automated Linter Checks:
1. **4-Space Indentation Rule**: Verifies block indentation alignment.
2. **Block Header Colons**: Ensures block statements (`if`, `for`, `while`, `function`) terminate with `:`.
3. **Block Closure Verification**: Detects unclosed `match` or `interface` blocks.
4. **Unclosed Strings**: Identifies unescaped or missing quote pairs.
5. **Ambiguous Phrase Warnings**: Warns about non-canonical phrases (e.g., `is bigger than`) and suggests canonical replacements.

### Example Linter Diagnostic Output:
```
=================================================================
  EnLang Syntax Checker & Linter — bad_syntax_test.enlg
=================================================================
  [ERROR] Line 3: Unclosed string literal detected. (Suggestion: Ensure string quotes are closed properly)
  [ERROR] Line 4: Block header missing trailing colon ':'. (Suggestion: Add a colon ':' at the end of the line)
  [ERROR] Line 4: Unsupported natural phrase detected in statement. (Suggestion: Use 'is greater than' instead of 'is bigger than')
=================================================================
  Result: 3 Error(s), 0 Warning(s)
=================================================================
```

## 17.2 EnLang Interactive CLI Debugger (`enlang debug`)
The `enlang debug` command launches an interactive step-by-step execution debugger with live variable inspection.

```bash
enlang debug app.enlg
```

### Interactive Debugger Commands:
- `s` / `step`: Step to next line of EnLang code.
- `c` / `continue`: Resume execution until next breakpoint or termination.
- `v` / `vars`: Display live variable table and values.
- `b <N>` / `break <N>`: Set breakpoint at line number `N`.
- `e <expr>` / `eval <expr>`: Evaluate expression in live execution frame.
- `q` / `quit`: Exit debugger session.

---

# APPENDIX B: CLI & PACKAGE MANAGER (EPM) MANUAL

```bash
enlang run app.enlg           # Compiles & executes backend logic
enlang check app.enlg         # Performs static analysis & linting
enlang debug app.enlg         # Launches interactive step-by-step debugger
enlang build index.enlgf      # Transpiles source into native target file
enlang server --port 8000     # Launches zero-config HTTP host server
enlang add py:requests        # Installs Python PyPI package
enlang add web:chart.js       # Installs Web NPM package
```

---
**Copyright © 2026 Spandan Prayas Patra. All rights reserved.**  
*Published under the Open EnLang Specification License.*
