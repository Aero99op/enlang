# Part 4: Complete CLI & EPM Reference + IDE Setup

This part details the official CLI commands for `enlang` and `epm` (EnLang Package Manager), as well as setting up the official EnLang VS Code extension (`vscode-enlang`).

## EnLang CLI Command Reference

### Execution Commands
```bash
enlang run app.enlg          # Runs backend Python logic script
enlang run index.enlgf       # Compiles web app & starts live dev server
enlang run index.enlgf -p 3000 # Runs web server on port 3000
enlang run schema.enlgdb     # Compiles SQL, initializes SQLite database & displays tables
enlang server --port 8000    # Starts zero-config HTTP web server
```

### Build Commands
```bash
enlang build main.enlg       # Compiles to main.py
enlang build index.enlgf     # Compiles to index.html
enlang build style.enlgd     # Compiles to style.css
enlang build app.enlgs       # Compiles to app.js
enlang build schema.enlgdb   # Compiles to schema.sql
```

### Static Analysis & Debugging
```bash
enlang check main.enlg       # Runs static linting & syntax analysis
enlang debug main.enlg       # Launches interactive step-by-step debugger
```

## EPM Package Manager (`epm`)

The EnLang Package Manager (`epm`) handles project dependencies:

```bash
epm init                     # Initializes enlang.json project manifest file
epm add py:requests          # Installs PyPI Python library
epm add web:chart.js         # Installs Web NPM library
epm install                  # Installs all packages declared in enlang.json
```

## IDE Setup (VS Code)

The codebase includes an official VS Code extension in `vscode-enlang`:
- Features **Syntax Highlighting** for `.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, and `.enlgdb`.
- Features auto-completion and error diagnostic hints.
