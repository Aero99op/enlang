# Part 3: EnLang Transpiler & Runtime Architecture

Unlike traditional compilers that produce complex binary machine code directly, EnLang uses a **Universal Multi-Target Transpilation Engine**.

## Transpiler Architecture

EnLang takes natural English source code (`.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, `.enlgdb`) and performs deterministic 1:1 transpilation into clean, production-grade target code:

- **`.enlg` (Backend Logic)** transpiles to **Python 3**
- **`.enlgf` (Frontend UI)** transpiles to **HTML5**
- **`.enlgd` (Design Systems)** transpiles to **CSS3**
- **`.enlgs` (Client Scripting)** transpiles to **JavaScript (ES6+)**
- **`.enlgdb` (Database Systems)** transpiles to **ANSI SQL / SQLite**

## Execution vs Compilation Commands

EnLang provides commands for both direct execution and standalone target compilation:

### 1. Direct Execution (`enlang run`)
```bash
enlang run app.enlg
```
Transpiles `app.enlg` in memory to Python 3 and executes it immediately via the built-in runtime engine.

### 2. Standalone Target Compilation (`enlang build`)
```bash
enlang build app.enlg
```
Transpiles `app.enlg` and saves the compiled target output to `app.py`.

```bash
enlang build index.enlgf
```
Compiles `.enlgf` natural markup into clean W3C-compliant `index.html`.

## Inline Native Code Blocks

EnLang allows seamless embedding of raw native code within natural English scripts using native block markers:

```enlg
python:
    import math
    print(math.sqrt(16))
end python
```

This guarantees 100% interoperability with native target ecosystems!
