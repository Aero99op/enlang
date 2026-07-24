import sys
sys.path.insert(0, 'd:/enlangg')

from enlang_core.interpreter import EnLangInterpreter
interp = EnLangInterpreter()

tests = [
    ("Typed Variable (number)", "define number age as 25\ndisplay age", "25", False),
    ("Typed Variable (text)", 'define text username as "Spandan"\ndisplay username', "Spandan", False),
    ("Typed Variable (boolean)", "define boolean isActive as true\ndisplay isActive", "True", False),
    ("Typed Variable (decimal)", "define decimal price as 99.5\ndisplay price", "99.5", False),
    ("Match / Case basic", 'set role to "admin"\nmatch role:\n    case "admin":\n        display "Full Access"\n    default:\n        display "No Access"', "Full Access", False),
    ("Match / Multiple Case Values", 'set grade to 85\nmatch grade:\n    case 80, 85, 90:\n        display "Silver"\n    default:\n        display "Other"', "Silver", False),
    ("Interface & Implements", 'interface Authenticatable:\n    pass\nclass UserSession implements Authenticatable:\n    pass\nu = UserSession()\ndisplay str(isinstance(u, Authenticatable))', "True", False),
    ("Async Function & Await", 'import asyncio\nasync function fetch_data():\n    return "Loaded Data"\nasync function main():\n    set res to await fetch_data()\n    display res\nasyncio.run(main())', "Loaded Data", False),
    ("Raise Error", 'raise ValueError with message "Something broke"', "", True),
    ("Throw Error", 'throw error "Custom failure"', "", True),
    ("Class extends", "class Animal:\n    pass\nclass Dog extends Animal:\n    pass\nd = Dog()\ndisplay str(type(d).__name__)", "Dog", False),
]

print("=" * 65)
print("  EnLang v2.0 — Enterprise Feature Audit (Interfaces + Async/Await)")
print("=" * 65)

live = 0
fail = 0
for name, code, expected_out, expects_exception in tests:
    ok, out, err, py = interp.run_code(code)

    if expects_exception:
        if not ok:
            print(f"  [LIVE OK] {name}: raises exception correctly")
            live += 1
        else:
            print(f"  [FAIL --] {name}: should have raised exception but didn't")
            fail += 1
    else:
        if ok and expected_out.lower() in out.strip().lower():
            print(f"  [LIVE OK] {name}: output = {out.strip()[:55]}")
            live += 1
        elif ok and not expected_out:
            print(f"  [LIVE OK] {name}: compiled ok")
            live += 1
        else:
            print(f"  [FAIL --] {name}")
            print(f"            expected: {expected_out}")
            print(f"            got:      {out.strip()[:60] or err.strip()[:60]}")
            fail += 1

print("=" * 65)
print(f"  LIVE: {live}  |  FAIL: {fail}  |  TOTAL: {live + fail}")
print("=" * 65)
