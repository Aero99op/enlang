# Part 2: Official Installation & Setup

Installing EnLang is fast and straightforward across all platforms (Windows, macOS, Linux). EnLang is distributed globally as a Python package via PyPI.

## Official Installation (`pip`)

To install EnLang globally on your system, open your command prompt or terminal and run:

```bash
pip install enlang
```

### Upgrading EnLang

To update to the latest stable release of EnLang at any time, run:

```bash
enlang update
```

Or via `pip`:

```bash
pip install --upgrade enlang
```

## Verifying the Installation

After installing, verify that the `enlang` compiler and the `epm` package manager are accessible from your CLI:

```bash
enlang version
```

**Expected Output:**
```text
EnLang Compiler v1.0.0 (Stable Release)
Authored by Spandan Prayas Patra
```

To list all available versions published on PyPI:

```bash
enlang versions
```

To switch or install a specific published version:

```bash
enlang install 1.0.0
```

## GUI Installer for Windows

For Windows users who prefer a standalone setup without manually using `pip`, EnLang provides an official executable GUI installer:
- **`EnLangInstaller.exe`**: Automatically sets up Python dependencies, registers system PATH environment variables, and configures CLI tools (`enlang` and `epm`).
