import sys
sys.path.insert(0, 'd:/enlangg')

from enlang_core.interpreter import EnLangInterpreter
interp = EnLangInterpreter()

tests = [
    (
        "Legacy function syntax (function name(args):)",
        "function add_numbers(a, b):\n    return a plus b\nset res to add_numbers(10, 20)\ndisplay res",
        "30"
    ),
    (
        "Modern short syntax (fn name(args):)",
        "fn multiply(a, b):\n    return a times b\nset res to multiply(6, 7)\ndisplay res",
        "42"
    ),
    (
        "Signature EnLang syntax (define function name taking args:)",
        "define function greet taking name:\n    display 'Hello ' plus name\nrun greet with 'Spandan'",
        "Hello Spandan"
    ),
    (
        "Signature EnLang action syntax (action name taking args:)",
        "action double_val taking n:\n    result is n times 2\nset res to double_val(15)\ndisplay res",
        "30"
    ),
    (
        "Natural Function call (call name with args and store in var)",
        "fn calc_tax(price, rate):\n    give back price times rate\ncall calc_tax with (1000, 0.18) and store in total\ndisplay total",
        "180.0"
    ),
    (
        "Recursive Function with EnLang natural keywords",
        "define function print_rec taking n:\n    if n is greater than 5 then:\n        return\n    display n\n    run print_rec with (n plus 1)\nrun print_rec with 1",
        "1\n2\n3\n4\n5"
    ),
]

print("=" * 70)
print("  EnLang Function Syntax Suite Test")
print("=" * 70)

for name, code, expected in tests:
    ok, out, err, py = interp.run_code(code)
    if ok and expected.strip() in out.strip():
        print(f"  [PASS OK] {name}")
    else:
        print(f"  [FAIL --] {name}")
        print(f"            expected: {repr(expected)}")
        print(f"            got:      {repr(out.strip() or err.strip())}")
        print(f"            py code:  {py}")

print("=" * 70)
