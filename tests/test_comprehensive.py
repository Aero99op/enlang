"""
EnLang Comprehensive End-to-End Test Suite
Tests ALL domains from every angle:
  .enlgf (HTML) - raw + EnLang sugar + mixed
  .enlgd (CSS)  - raw + EnLang sugar + mixed
  .enlgs (JS)   - raw + EnLang sugar + mixed
  .enlg  (Py)   - raw + EnLang sugar + mixed
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enlang_core.interpreter import EnLangInterpreter

interp = EnLangInterpreter()

PASS = 0
FAIL = 0

def check(label, code, fp, expect_in=None, expect_not_in=None, expect_success=True):
    global PASS, FAIL
    ok, out, err, _ = interp.run_code(code, file_path=fp)
    if expect_success and not ok:
        print(f"  [FAIL] {label}: runtime error: {err}")
        FAIL += 1
        return
    if not expect_success and ok:
        print(f"  [FAIL] {label}: expected failure but succeeded")
        FAIL += 1
        return
    for needle in (expect_in or []):
        if needle not in out:
            print(f"  [FAIL] {label}: expected {repr(needle)} in output\n         got: {repr(out[:200])}")
            FAIL += 1
            return
    for needle in (expect_not_in or []):
        if needle in out:
            print(f"  [FAIL] {label}: expected {repr(needle)} NOT in output\n         got: {repr(out[:200])}")
            FAIL += 1
            return
    print(f"  [PASS] {label}")
    PASS += 1

# ═══════════════════════════════════════════════════════
# SECTION 1: .enlgf (HTML Domain)
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("  .enlgf  ->  HTML5 Tests")
print("="*60)

# 1a. DOCTYPE passthrough
check("DOCTYPE passthrough", "<!DOCTYPE html>", "test.enlgf",
    expect_in=["<!DOCTYPE html>"])

# 1b. Full HTML structure passthrough
check("Full HTML structure", """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raw HTML Test</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <h2 class="logo">BRAND</h2>
        </nav>
    </header>
    <main>
        <h1>Hello World</h1>
        <p class="subtitle">This is a raw HTML paragraph.</p>
    </main>
</body>
</html>""", "test.enlgf",
    expect_in=["<!DOCTYPE html>", "<html lang", "<meta charset", "BRAND", "Hello World", "subtitle"])

# 1c. HTML comments
check("HTML comments passthrough", "<!-- This is a comment -->", "test.enlgf",
    expect_in=["<!-- This is a comment -->"])

# 1d. HTML attributes (class, id, data-*, aria-*, style)
check("HTML all attributes", """
<div id="app" class="container active" data-theme="dark" aria-label="main" style="color: red">
    <span data-value="42">Test</span>
</div>""", "test.enlgf",
    expect_in=["id=\"app\"", "data-theme=\"dark\"", "aria-label=\"main\"", "style=\"color: red\"", "data-value=\"42\""])

# 1e. SVG inline passthrough
check("SVG passthrough", """
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40" fill="blue" />
    <rect x="10" y="10" width="30" height="30" fill="red"/>
</svg>""", "test.enlgf",
    expect_in=["<svg", "<circle", "fill=\"blue\"", "<rect", "fill=\"red\""])

# 1f. Form elements passthrough
check("Form elements passthrough", """
<form action="/submit" method="POST">
    <input type="text" name="username" placeholder="Enter name" required>
    <input type="email" name="email">
    <input type="password" name="pass">
    <select name="role">
        <option value="admin">Admin</option>
        <option value="user" selected>User</option>
    </select>
    <textarea name="bio" rows="5" cols="30"></textarea>
    <button type="submit">Submit</button>
</form>""", "test.enlgf",
    expect_in=["action=\"/submit\"", "method=\"POST\"", "type=\"email\"", "<select", "<option", "selected", "<textarea", "type=\"submit\""])

# 1g. Table passthrough
check("Table structure passthrough", """
<table class="data-table">
    <thead>
        <tr>
            <th>Name</th><th>Age</th><th>City</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Amit</td><td>25</td><td>Delhi</td>
        </tr>
    </tbody>
</table>""", "test.enlgf",
    expect_in=["<table class=\"data-table\"", "<thead>", "<th>Name</th>", "<tbody>", "<td>Amit</td>"])

# 1h. Canvas element
check("Canvas passthrough", """
<canvas id="myCanvas" width="500" height="500"></canvas>""", "test.enlgf",
    expect_in=["<canvas", "id=\"myCanvas\"", "width=\"500\""])

# 1i. Embedded script block passthrough
check("Embedded script tag passthrough", """
<body>
<script type="module">
import { createApp } from 'vue'
const app = createApp({})
app.mount('#app')
</script>
</body>""", "test.enlgf",
    expect_in=["<script type=\"module\">", "import { createApp }", "app.mount"])

# 1j. EnLang sugar - create hero
check("EnLang create hero", """
create hero with title "Build the Future", subtitle "Start today"
""", "test.enlgf",
    expect_in=["<section>", "<h1>", "Build the Future", "Start today"])

# 1k. EnLang sugar - create nav
check("EnLang create nav", """
create nav with links Home, About, Services, Contact
""", "test.enlgf",
    expect_in=["<nav>", "Home", "About", "Services", "Contact"])

# 1l. EnLang sugar - create button
check("EnLang create button with action", """
create button named myBtn with label "Launch" and action "launch()"
""", "test.enlgf",
    expect_in=["<button", "Launch", "launch()"])

# 1m. EnLang sugar - create form
check("EnLang create form", """
create form named loginForm with fields email, password and action "/api/login"
""", "test.enlgf",
    expect_in=["<form", "/api/login", "email", "password"])

# 1n. EnLang sugar - create table
check("EnLang create table", """
create table with headers Name, Score, Rank
""", "test.enlgf",
    expect_in=["<table>", "<th>Name</th>", "<th>Score</th>"])

# 1o. EnLang sugar - page title
check("EnLang page title", """
page title "My EnLang App"
""", "test.enlgf",
    expect_in=["<title>", "My EnLang App"])

# 1p. Mixed: raw HTML + EnLang sugar
check("Mixed raw HTML + EnLang sugar", """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
page title "Mixed App"
</head>
<body>
<div class="wrapper">
create hero with title "Mixed Mode Works"
<section id="about">
    <p>Raw paragraph works too.</p>
</section>
</div>
</body>
</html>""", "test.enlgf",
    expect_in=["<title>Mixed App</title>", "Mixed Mode Works", "Raw paragraph works too", "class=\"wrapper\""])


# ═══════════════════════════════════════════════════════
# SECTION 2: .enlgd (CSS Domain)
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("  .enlgd  ->  CSS3 Tests")
print("="*60)

# 2a. Raw CSS - basic selector + properties
check("Raw CSS basic selector", """
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #0f172a;
    color: white;
}""", "test.enlgd",
    expect_in=["body {", "margin: 0;", "background-color: #0f172a;", "color: white;"])

# 2b. Raw CSS - class and ID selectors
check("Raw CSS class/id selectors", """
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
}
#hero {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}""", "test.enlgd",
    expect_in=[".navbar {", "position: fixed;", "#hero {", "display: flex;", "justify-content: center;"])

# 2c. Raw CSS - pseudo-classes and pseudo-elements
check("Raw CSS pseudo-classes", """
a:hover {
    color: #38bdf8;
    text-decoration: underline;
}
.btn::before {
    content: '';
    display: block;
}""", "test.enlgd",
    expect_in=["a:hover {", "color: #38bdf8;", ".btn::before {", "content: '';"])

# 2d. Raw CSS - @media query
check("Raw CSS @media query", """
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
    }
    .hero h1 {
        font-size: 2rem;
    }
}""", "test.enlgd",
    expect_in=["@media (max-width: 768px) {", "flex-direction: column;", "font-size: 2rem;"])

# 2e. Raw CSS - @keyframes
check("Raw CSS @keyframes", """
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}""", "test.enlgd",
    expect_in=["@keyframes fadeIn {", "from { opacity: 0;", "to { opacity: 1;"])

# 2f. Raw CSS - CSS variables / custom properties
check("Raw CSS variables", """
:root {
    --primary: #3b82f6;
    --bg: #0f172a;
    --card: rgba(18, 24, 38, 0.9);
    --font: 'Inter', sans-serif;
}""", "test.enlgd",
    expect_in=[":root {", "--primary: #3b82f6;", "--bg: #0f172a;", "--card: rgba"])

# 2g. Raw CSS - Grid layout
check("Raw CSS Grid", """
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
    grid-template-areas: 'header header' 'sidebar main';
}""", "test.enlgd",
    expect_in=["display: grid;", "grid-template-columns: repeat(3, 1fr);", "grid-gap: 20px;"])

# 2h. Raw CSS - Flexbox
check("Raw CSS Flexbox", """
.container {
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: space-between;
    gap: 1.5rem;
}""", "test.enlgd",
    expect_in=["display: flex;", "flex-wrap: wrap;", "gap: 1.5rem;"])

# 2i. Raw CSS - Animations + transitions
check("Raw CSS transitions/animations", """
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeIn 1s ease forwards;
}
.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
}""", "test.enlgd",
    expect_in=["transition: transform", "animation: fadeIn", ".card:hover {", "transform: translateY(-10px)"])

# 2j. Raw CSS - glassmorphism
check("Raw CSS glassmorphism", """
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
}""", "test.enlgd",
    expect_in=["backdrop-filter: blur(20px);", "-webkit-backdrop-filter:", "rgba(255, 255, 255, 0.1)"])

# 2k. EnLang CSS sugar - style block
check("EnLang style block", """
style body:
    background-color: #0f172a
    color: white
    margin: 0
end style""", "test.enlgd",
    expect_in=["body {", "background-color: #0f172a", "color: white", "}"])

# 2l. EnLang CSS - define theme
check("EnLang define theme", """
define theme with primary "#3b82f6", background "#0f172a", accent "#10b981"
""", "test.enlgd",
    expect_in=["--primary: #3b82f6", "--background: #0f172a", "--accent: #10b981"])

# 2m. EnLang CSS - media query sugar
check("EnLang media query sugar", """
on screen smaller than "768px":
    .hero {
        font-size: 1.5rem;
    }
""", "test.enlgd",
    expect_in=["@media (max-width: 768px)"])

# 2n. Mixed: raw CSS + EnLang sugar
check("Mixed raw CSS + EnLang sugar", """
define theme with primary "#3b82f6", background "#090d16"

body {
    margin: 0;
    padding: 0;
}

style button:
    cursor: pointer
    border: none
end style

.hero {
    height: 100vh;
    display: flex;
}""", "test.enlgd",
    expect_in=["--primary: #3b82f6", "body {", "margin: 0;", "button {", "cursor: pointer", ".hero {"])


# ═══════════════════════════════════════════════════════
# SECTION 3: .enlgs (JavaScript Domain)
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("  .enlgs  ->  JavaScript Tests")
print("="*60)

# 3a. Raw JS - variable declarations
check("Raw JS variable declarations", """
const name = "EnLang";
let count = 0;
var legacy = true;
""", "test.enlgs",
    expect_in=["const name = \"EnLang\";", "let count = 0;", "var legacy = true;"])

# 3b. Raw JS - function declaration + arrow
check("Raw JS functions", """
function greet(name) {
    return `Hello, ${name}!`;
}
const add = (a, b) => a + b;
const multiply = (x, y) => {
    return x * y;
};
""", "test.enlgs",
    expect_in=["function greet(name) {", "return `Hello, ${name}!`;", "const add = (a, b) => a + b;", "const multiply"])

# 3c. Raw JS - class definition
check("Raw JS class", """
class Animal {
    constructor(name) {
        this.name = name;
    }
    speak() {
        console.log(`${this.name} makes a sound.`);
    }
}
class Dog extends Animal {
    speak() {
        console.log(`${this.name} barks.`);
    }
}
""", "test.enlgs",
    expect_in=["class Animal {", "constructor(name) {", "this.name = name;", "class Dog extends Animal {"])

# 3d. Raw JS - DOM manipulation
check("Raw JS DOM manipulation", """
const btn = document.getElementById('myBtn');
const header = document.querySelector('.header');
const items = document.querySelectorAll('.item');
btn.addEventListener('click', function() {
    header.classList.toggle('active');
});
document.body.style.background = '#000';
""", "test.enlgs",
    expect_in=["document.getElementById", "document.querySelector", "addEventListener", "classList.toggle", "document.body.style"])

# 3e. Raw JS - async/await + fetch
check("Raw JS async/await + fetch", """
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
""", "test.enlgs",
    expect_in=["async function fetchData", "const response = await fetch(url);", "const data = await response.json();", "catch (error)"])

# 3f. Raw JS - Array methods
check("Raw JS Array methods", """
const nums = [1, 2, 3, 4, 5];
const doubled = nums.map(n => n * 2);
const evens = nums.filter(n => n % 2 === 0);
const sum = nums.reduce((acc, n) => acc + n, 0);
nums.forEach(n => console.log(n));
""", "test.enlgs",
    expect_in=["const nums = [1, 2, 3, 4, 5];", "nums.map(n => n * 2)", "nums.filter", "nums.reduce", "nums.forEach"])

# 3g. Raw JS - Promise chain
check("Raw JS Promise chain", """
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(err => {
        console.error(err);
    });
""", "test.enlgs",
    expect_in=["fetch('/api/data')", ".then(response => response.json())", ".catch(err =>"])

# 3h. Raw JS - spread/rest, destructuring
check("Raw JS modern syntax", """
const { name, age, ...rest } = person;
const [first, second, ...others] = arr;
const merged = { ...obj1, ...obj2 };
const clone = [...original];
""", "test.enlgs",
    expect_in=["const { name, age, ...rest }", "const [first, second, ...others]", "const merged = { ...obj1", "const clone = [...original]"])

# 3i. Raw JS - localStorage / sessionStorage
check("Raw JS storage APIs", """
localStorage.setItem('token', 'abc123');
const token = localStorage.getItem('token');
sessionStorage.clear();
""", "test.enlgs",
    expect_in=["localStorage.setItem", "localStorage.getItem", "sessionStorage.clear()"])

# 3j. Raw JS - Canvas API
check("Raw JS Canvas API", """
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#3b82f6';
ctx.fillRect(0, 0, 200, 200);
ctx.beginPath();
ctx.arc(100, 100, 50, 0, Math.PI * 2);
ctx.fill();
""", "test.enlgs",
    expect_in=["canvas.getContext('2d')", "ctx.fillStyle", "ctx.fillRect", "ctx.beginPath()", "ctx.arc(100"])

# 3k. EnLang JS sugar - set variable
check("EnLang set variable", """
set score to 100
define constant PI as 3.14159
""", "test.enlgs",
    expect_in=["let score = 100;", "const PI = 3.14159;"])

# 3l. EnLang JS sugar - log
check("EnLang log", "log score", "test.enlgs",
    expect_in=["console.log(score)"])

# 3m. EnLang JS sugar - for loop
check("EnLang repeat loop", "repeat 5 times:", "test.enlgs",
    expect_in=["for (let _i = 0; _i < 5; _i++) {"])

# 3n. EnLang JS sugar - for each
check("EnLang for each", "for each item in items:", "test.enlgs",
    expect_in=["for (const item of items) {"])

# 3o. Mixed: raw JS + EnLang sugar
check("Mixed raw JS + EnLang sugar", """
const items = ['apple', 'banana', 'mango'];
set total to 0;

for each item in items:
    total++;
end

document.addEventListener('DOMContentLoaded', function() {
    console.log('Ready!');
});
""", "test.enlgs",
    expect_in=["const items = ['apple', 'banana', 'mango'];", "for (const item of items) {", "document.addEventListener"])


# ═══════════════════════════════════════════════════════
# SECTION 4: .enlg (Python Domain)
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("  .enlg  ->  Python Tests")
print("="*60)

# 4a. Raw Python - basic syntax
check("Raw Python basic", """
x = 10
y = 20
result = x + y
print(result)
""", "test.enlg",
    expect_in=["30"])

# 4b. Raw Python - list comprehension
check("Raw Python list comprehension", """
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
print(squares[:3])
print(evens[:3])
""", "test.enlg",
    expect_in=["[0, 1, 4]", "[0, 2, 4]"])

# 4c. Raw Python - dict comprehension
check("Raw Python dict comprehension", """
d = {k: v for k, v in zip('abc', [1, 2, 3])}
print(d)
""", "test.enlg",
    expect_in=["{'a': 1, 'b': 2, 'c': 3}"])

# 4d. Raw Python - lambda + map/filter
check("Raw Python lambda/map/filter", """
double = lambda x: x * 2
nums = list(map(double, [1, 2, 3]))
print(nums)
""", "test.enlg",
    expect_in=["[2, 4, 6]"])

# 4e. Raw Python - class definition
check("Raw Python class", """
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self):
        return f"Hi, I'm {self.name}, {self.age} years old."

p = Person("Arjun", 22)
print(p.greet())
""", "test.enlg",
    expect_in=["Hi, I'm Arjun, 22 years old."])

# 4f. Raw Python - decorators
check("Raw Python decorators", """
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

@bold
def say_hello(name):
    return f"Hello, {name}"

print(say_hello("world"))
""", "test.enlg",
    expect_in=["<b>Hello, world</b>"])

# 4g. Raw Python - try/except/finally
check("Raw Python try/except", """
try:
    x = int("abc")
except ValueError as e:
    print(f"Caught: {e}")
finally:
    print("Done")
""", "test.enlg",
    expect_in=["Caught:", "invalid literal", "Done"])

# 4h. Raw Python - generator
check("Raw Python generator", """
def count_up(n):
    for i in range(n):
        yield i * 2

gen = count_up(4)
print(list(gen))
""", "test.enlg",
    expect_in=["[0, 2, 4, 6]"])

# 4i. Raw Python - with statement + file ops
check("Raw Python with statement", """
import os
path = "test_tmp.txt"
with open(path, 'w') as f:
    f.write("enlang rocks")
with open(path, 'r') as f:
    content = f.read()
print(content)
os.remove(path)
""", "test.enlg",
    expect_in=["enlang rocks"])

# 4j. Raw Python - f-strings + string methods
check("Raw Python f-strings + string methods", """
name = "enlang"
s = f"Hello from {name.upper()}! version {len(name)}.0"
print(s)
print(name.replace('lang', 'world').title())
""", "test.enlg",
    expect_in=["Hello from ENLANG! version 6.0", "Enworld"])

# 4k. Raw Python - import + stdlib
check("Raw Python stdlib import", """
import math
import json
from datetime import datetime

print(round(math.pi, 4))
data = json.loads('{"key": "value"}')
print(data['key'])
""", "test.enlg",
    expect_in=["3.1416", "value"])

# 4l. EnLang Python sugar - variable assignment
check("EnLang set/store variable", """
set name to "EnLang"
store 42 in answer
display name
display answer
""", "test.enlg",
    expect_in=["EnLang", "42"])

# 4m. EnLang Python sugar - loops
check("EnLang repeat N times", """
set total to 0
repeat 5 times:
    increment total by 1
display total
""", "test.enlg",
    expect_in=["5"])

# 4n. EnLang Python sugar - array/list
check("EnLang array operations", """
array fruits with items "apple", "banana", "mango"
add "cherry" to fruits
remove "banana" from fruits
sort fruits
display fruits
""", "test.enlg",
    expect_in=["apple", "cherry", "mango"])

check("EnLang get item / length", """
array colors with items "red", "green", "blue"
get item 1 from colors store in second
length of colors store in n
display second
display n
""", "test.enlg",
    expect_in=["green", "3"])

# 4o. EnLang Python sugar - dict/map
check("EnLang dict/map", """
create map user
set key "name" in user to "Rahul"
set key "age" in user to 25
get key "name" from user store in username
display username
""", "test.enlg",
    expect_in=["Rahul"])

# 4p. EnLang Python sugar - function definition
check("EnLang function", """
function add(a, b):
    return a + b

display add(10, 32)
""", "test.enlg",
    expect_in=["42"])

# 4q. EnLang Python sugar - if/else
check("EnLang if/else", """
set x to 15
if x is greater than 10 then:
    display "big"
otherwise:
    display "small"
""", "test.enlg",
    expect_in=["big"])

# 4r. Mixed: raw Python + EnLang sugar
check("Mixed raw Python + EnLang sugar", """
import math

set radius to 7
area = math.pi * radius * radius
display round(area, 2)

array primes with items 2, 3, 5, 7, 11
for each prime in primes:
    if prime is greater than 4 then:
        print(f"Prime > 4: {prime}")
""", "test.enlg",
    expect_in=["153.94", "Prime > 4: 5", "Prime > 4: 7", "Prime > 4: 11"])


# ═══════════════════════════════════════════════════════
# FINAL RESULTS
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
total = PASS + FAIL
print(f"  TOTAL: {total} tests  |  PASS: {PASS}  |  FAIL: {FAIL}")
print("="*60)
if FAIL == 0:
    print("  ALL TESTS PASSED!")
else:
    print(f"  {FAIL} tests FAILED!")
print()
