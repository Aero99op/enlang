"""
EnLang Mega Edge-Case Stress Test
Tests weird syntax, quotes inside quotes, nested blocks, edge case expressions,
comments in weird places, negative numbers, multi-line logic across ALL domains.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enlang_core.interpreter import EnLangInterpreter

interp = EnLangInterpreter()

TESTS = [
    # 1. String edge cases
    ("Single quotes inside string", 'display "He said \'hello\' to everyone"', "main.enlg", "He said 'hello' to everyone"),
    ("Double quotes inside single quotes", "display 'She said \"hi\"'", "main.enlg", 'She said "hi"'),
    ("String concatenation with escaped quotes", 'set msg to "hello" + " world"\ndisplay msg', "main.enlg", "hello world"),
    ("String containing operator words", 'display "this is plus and minus test"', "main.enlg", "this is plus and minus test"),
    ("String containing 'is greater than'", 'display "5 is greater than 3 in text"', "main.enlg", "5 is greater than 3 in text"),
    ("String containing 'and' and 'or'", 'display "black and white or blue"', "main.enlg", "black and white or blue"),

    # 2. Arithmetic Edge Cases
    ("Negative numbers", "set x to -10\nset y to -5\ndisplay x plus y", "main.enlg", "-15"),
    ("Floating point math", "set a to 3.14\nset b to 2.0\ndisplay a times b", "main.enlg", "6.28"),
    ("Parentheses precedence", "set res to (10 plus 5) times 2\ndisplay res", "main.enlg", "30"),
    ("Modulo operation", "set res to 17 modulo 5\ndisplay res", "main.enlg", "2"),
    ("Power of operation", "set res to 3 power of 4\ndisplay res", "main.enlg", "81"),

    # 3. Complex Conditionals & Loops
    ("Nested if-else blocks", """
set age to 20
set has_id to true
if age is greater than or equal to 18 then:
    if has_id is true then:
        display "Access Granted"
    otherwise:
        display "ID Required"
otherwise:
    display "Underage"
""", "main.enlg", "Access Granted"),

    ("Nested for-each loop", """
array categories with items "A", "B"
array numbers with items 1, 2
for each cat in categories:
    for each num in numbers:
        display cat + str(num)
""", "main.enlg", "A1\nA2\nB1\nB2"),

    ("While loop with break", """
set count to 1
while count is less than 10 do:
    if count is equal to 3 then:
        break
    increment count by 1
display count
""", "main.enlg", "3"),

    # 4. Collection Edge Cases
    ("Empty array creation and append", """
create list items
add "first" to items
add "second" to items
remove item at index 0 from items
display items
""", "main.enlg", "['second']"),

    ("Array length and check", """
array nums with items 10, 20, 30
get length of nums store in sz
check if 20 is in nums store in has_twenty
display sz
display has_twenty
""", "main.enlg", "3\nTrue"),

    ("Map/Dict with special values", """
create map config
set key "timeout" in config to 5000
set key "enabled" in config to true
get key "timeout" from config store in t
display t
""", "main.enlg", "5000"),

    # 5. Functions & Edge cases
    ("Function returning multiple values as list", """
function get_pair(x, y):
    return [x times 2, y times 2]

res = get_pair(5, 10)
display res
""", "main.enlg", "[10, 20]"),

    # 6. HTML (.enlgf) Edge Cases
    ("Nested HTML divs in .enlgf", """
create div with class "outer":
    create div with class "inner":
        create paragraph with text "Deep text"
    end div
end div
""", "page.enlgf", "<div class=\"outer\">\n<div class=\"inner\">\n<p>Deep text</p>\n</div>\n</div>"),

    ("HTML attributes with spaces", """
<div id="main" class="hero banner active" style="margin: 0 auto; padding: 20px;">
    <h1>Title</h1>
</div>
""", "page.enlgf", "class=\"hero banner active\""),

    # 7. CSS (.enlgd) Edge Cases
    ("CSS flexbox & grid properties", """
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
#card {
    background-color: #1e293b;
    border-radius: 12px;
}
""", "style.enlgd", ".container {\ndisplay: flex;\njustify-content: space-between;\nalign-items: center;\n}\n#card {\nbackground-color: #1e293b;\nborder-radius: 12px;\n}"),

    # 8. JS (.enlgs) Edge Cases
    ("JS async fetch and DOM", """
const btn = document.getElementById('submitBtn');
btn.addEventListener('click', async function() {
    const res = await fetch('/api/data');
    const json = await res.json();
    console.log(json);
});
""", "script.enlgs", "const btn = document.getElementById('submitBtn');\nbtn.addEventListener('click', async function() {\nconst res = await fetch('/api/data');\nconst json = await res.json();\nconsole.log(json);\n});"),
]

PASS = 0
FAIL = 0

print("="*60)
print("  ENLANG MEGA EDGE-CASE STRESS TEST")
print("="*60)

for label, code, fp, expect in TESTS:
    ok, out, err, _ = interp.run_code(code, file_path=fp)
    if not ok:
        print(f"  [FAIL] {label}: Runtime error -> {err}")
        FAIL += 1
    elif expect not in out.strip():
        print(f"  [FAIL] {label}: Expected {repr(expect)} in output")
        print(f"         Got: {repr(out.strip())}")
        FAIL += 1
    else:
        print(f"  [PASS] {label}")
        PASS += 1

print("="*60)
print(f"  TOTAL: {PASS + FAIL} | PASS: {PASS} | FAIL: {FAIL}")
print("="*60)
