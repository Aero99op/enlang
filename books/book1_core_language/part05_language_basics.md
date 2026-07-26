# Part 5: Language Basics & Natural English Syntax

EnLang is designed so that reading your code feels like reading natural English. This part covers the basic building blocks of an EnLang program (`.enlg`).

## Core Syntax Principles

1. **Natural English Keywords**: Instead of cryptic symbols like `{}` or `;`, EnLang uses plain English words (`define`, `as`, `display`, `if`, `then`, `match`, `function`).
2. **Indentation-Based Scoping**: EnLang uses clean Python-like indentation to define blocks of code.
3. **Comments**: Use `#` to write single-line comments in your code.
4. **Case Insensitivity for Sugar**: Keywords like `DEFINE`, `Define`, and `define` are handled gracefully by the transpiler.

## Your First EnLang Program (`hello.enlg`)

Create a file named `hello.enlg`:

```enlg
# EnLang Hello World Program
# File: hello.enlg

define text greeting as "Hello, World!"

display greeting
display "Welcome to EnLang Natural English Programming!"
```

### Running the Program

Run it directly using the CLI:
```bash
enlang run hello.enlg
```

**Output:**
```text
Hello, World!
Welcome to EnLang Natural English Programming!
```

## How It Transpiles Under the Hood

When you run `enlang run hello.enlg` or `enlang build hello.enlg`, the transpiler translates it into native Python:

```python
# Transpiled from hello.enlg
greeting = "Hello, World!"
print(greeting)
print("Welcome to EnLang Natural English Programming!")
```

## Statement Separators & Line Rules

- Every statement in EnLang is placed on a new line.
- You do not need semicolons `;` at the end of lines.
- Indentation must be consistent (4 spaces per indentation level is recommended).
