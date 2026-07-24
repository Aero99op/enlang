import sys
sys.path.insert(0, 'd:/enlangg')

from enlang_core.interpreter import EnLangInterpreter
interp = EnLangInterpreter()

tests = [
    (
        "Level 1: Pure EnLang",
        "set width to 10\nset height to 5\nset area to width times height\ndisplay area",
        "50"
    ),
    (
        "Level 2: Inline Native Marker @python(...)",
        "import module math\nset val to @python(math.sqrt(144))\ndisplay val",
        "12.0"
    ),
    (
        "Level 2: Inline Native Marker with math expression",
        "set width to 10\nset height to 20\nset area to @python(width * height)\ndisplay area",
        "200"
    ),
    (
        "Level 3: Multi-line Native Python Block",
        "python:\nimport math\nx = math.factorial(5)\nprint(x)\nend python",
        "120"
    ),
]

print("=" * 65)
print("  EnLang 3-Level Native Code Architecture Audit")
print("=" * 65)

pass_count = 0
for name, code, expected in tests:
    ok, out, err, py = interp.run_code(code)
    if ok and expected in out.strip():
        print(f"  [PASS OK] {name}: output = {out.strip()}")
        pass_count += 1
    else:
        print(f"  [FAIL --] {name}")
        print(f"            expected: {expected}")
        print(f"            got:      {out.strip() or err.strip()}")

print("=" * 65)
print(f"  PASS: {pass_count} / {len(tests)}")
print("=" * 65)
