# Part 18: Testing, Interactive Debugging & Static Analysis

To ensure production stability, EnLang features integrated static linting, interactive step-by-step debugging, and testing utilities.

## 1. Static Linting & Analysis (`enlang check`)

Run `enlang check` before running your code to catch syntax and logic errors early:

```bash
enlang check main.enlg
```

**Output:**
```text
[CHECK] Analyzing main.enlg...
[OK] Syntax check passed. 0 Errors, 0 Warnings found.
```

If an error exists, `enlang check` provides detailed line numbers and exact suggestions for fixing it.

## 2. Interactive Debugger (`enlang debug`)

Launch the interactive step-by-step debugger to inspect variable values during execution:

```bash
enlang debug main.enlg
```

### Interactive Debug Commands:
- `step` / `s`: Execute the next line of EnLang code.
- `print <var>` / `p <var>`: Inspect current runtime value of `<var>`.
- `continue` / `c`: Resume execution until the next breakpoint.
- `quit` / `q`: Exit the debugging session.

## 3. Integrated Test Runner (`enlang test`)

Write automated test functions starting with `test_`:

```enlg
function test_addition():
    define number a as 5
    define number b as 10
    assert a plus b is equal to 15
```

Run all tests in your workspace:
```bash
enlang test
```

**Output:**
```text
[TEST] Running test suite...
  ✓ test_addition PASSED (0.002s)
[SUMMARY] 1 passed, 0 failed.
```
