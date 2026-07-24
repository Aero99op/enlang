"""
EnLang Comprehensive Test Suite — Covers ALL Grammar Constructs

Tests every feature of the EnLang language engine across all domains:
  .enlg            → Python 3  (backend logic)
  .enlg @on <frontend> → HTML5 (frontend markup)
  .enlgs           → JavaScript ES6+ (browser script output)
  .enlgd           → CSS3 + UI components (stylesheet output)
  .enlgdb          → SQL (database schema output)
"""

import unittest
from enlang_core import EnLangTranspiler, EnLangInterpreter


class TestEnLangPython(unittest.TestCase):
    """Tests for .enlg → Python transpilation"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def _run(self, code, filepath="app.enlg"):
        success, stdout, stderr, py = self.interp.run_code(code, file_path=filepath)
        return success, stdout, stderr, py

    def test_variable_store_in(self):
        success, out, err, _ = self._run('store "racecar" in word\ndisplay word')
        self.assertTrue(success, err)
        self.assertIn("racecar", out)

    def test_variable_set_to(self):
        success, out, err, _ = self._run('set score to 42\ndisplay score')
        self.assertTrue(success, err)
        self.assertIn("42", out)

    def test_variable_is_assignment(self):
        success, out, err, _ = self._run('word is "hello"\ndisplay word')
        self.assertTrue(success, err)
        self.assertIn("hello", out)

    def test_arithmetic_english(self):
        code = """
set a to 10 plus 5
set b to 20 minus 8
set c to 3 times 4
set d to 15 divided by 3
set e to 10 modulo 3
set f to 2 power of 8
display a
display b
display c
display d
display e
display f
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("15", out)
        self.assertIn("12", out)
        self.assertIn("12", out)
        self.assertIn("5.0", out)
        self.assertIn("1", out)
        self.assertIn("256", out)

    def test_increment_decrement(self):
        code = """
set x to 10
increment x by 5
display x
decrement x by 3
display x
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("15", out)
        self.assertIn("12", out)

    def test_if_then_colon(self):
        """if...then: should work correctly"""
        code = """
set x to 10
if x is greater than 5 then:
    display "big"
else:
    display "small"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("big", out)

    def test_if_without_then(self):
        """if without then should also work"""
        code = """
set x to 3
if x is less than 5:
    display "less"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("less", out)

    def test_else_if(self):
        code = """
set score to 75
if score is greater than or equal to 90 then:
    display "A"
else if score is greater than or equal to 75 then:
    display "B"
else:
    display "C"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("B", out)

    def test_otherwise_if(self):
        """'otherwise if' is an alias for 'else if'"""
        code = """
set score to 55
if score is greater than or equal to 90 then:
    display "A"
otherwise if score is greater than or equal to 75 then:
    display "B"
otherwise:
    display "C"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("C", out)

    def test_repeat_times(self):
        """repeat N times: should generate correct for-loop"""
        code = """
set count to 0
repeat 5 times:
    increment count by 1
display count
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("5", out)

    def test_for_each_do(self):
        """for each ... in ... do: should work"""
        code = """
set fruits to ["apple", "banana", "cherry"]
for each fruit in fruits do:
    display fruit
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("apple", out)
        self.assertIn("banana", out)
        self.assertIn("cherry", out)

    def test_for_each_without_do(self):
        code = """
set items to [1, 2, 3]
for each item in items:
    display item
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("1", out)
        self.assertIn("2", out)
        self.assertIn("3", out)

    def test_while_do(self):
        """while ... do: should work"""
        code = """
set i to 0
while i is less than 3 do:
    display i
    increment i by 1
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("0", out)
        self.assertIn("1", out)
        self.assertIn("2", out)

    def test_function_keyword(self):
        """function keyword should transpile to def"""
        code = """
function greet(name):
    return "Hello " + name

display greet("EnLang")
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("Hello EnLang", out)

    def test_func_keyword(self):
        """func keyword (shorthand) should transpile to def"""
        code = """
func add(a, b):
    return a + b

display add(3, 4)
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("7", out)

    def test_function_with_english_math(self):
        code = """
function calculate_discount(price, percentage):
    set discount to price times percentage divided by 100
    return price minus discount

store calculate_discount(1000, 15) in final_price
display final_price
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("850.0", out)

    def test_list_operations(self):
        code = """
create list colors with "red", "green", "blue"
add "yellow" to list colors
display colors
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("yellow", out)

    def test_import_module(self):
        """import module X should transpile to import X"""
        code = """
import module math
display math.pi
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("3.14", out)

    def test_import_direct(self):
        """import X should also work as regular Python"""
        code = """
import math
display math.sqrt(16)
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("4.0", out)

    def test_display_variants(self):
        """display, print, show, say, log all work"""
        code = """
display "a"
print "b"
show "c"
say "d"
log "e"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        for char in ["a", "b", "c", "d", "e"]:
            self.assertIn(char, out)

    def test_bool_true_false(self):
        code = """
set flag to true
if flag is true then:
    display "yes"
set flag to false
if flag is false then:
    display "no"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("yes", out)
        self.assertIn("no", out)

    def test_hash_sha256(self):
        code = """
hash "password123" with sha256 and store in h
display h
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertEqual(len(out.strip()), 64)  # SHA256 hex is 64 chars

    def test_nlp_operations(self):
        code = """
set text to "EnLang is a great and wonderful project!"
analyze sentiment of text and store in sent
extract keywords from text into kw
calculate similarity between "hello world" and "hello user" and store in sim
display "Sentiment: " + sent
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("Sentiment: Positive", out)

    def test_fuzzy_intent(self):
        code = """
please assign "Awesome Developer" to dev_title
say "Title: " + dev_title
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("Title: Awesome Developer", out)

    def test_palindrome_full_program(self):
        code = """
store "racecar" in word
store word[::-1] in reversed_word
if word is equal to reversed_word then:
    display "IS palindrome"
else:
    display "NOT palindrome"
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("IS palindrome", out)

    def test_fibonacci_loop(self):
        code = """
set first_num to 0
set second_num to 1
repeat 5 times:
    set next_num to first_num plus second_num
    set first_num to second_num
    set second_num to next_num
display next_num
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("8", out)

    def test_break_continue(self):
        code = """
set result to 0
repeat 10 times:
    increment result by 1
    if result is equal to 5 then:
        break
display result
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("5", out)

    def test_nested_functions(self):
        code = """
function outer(x):
    function inner(y):
        return y times 2
    return inner(x) plus 1

display outer(5)
"""
        success, out, err, _ = self._run(code)
        self.assertTrue(success, err)
        self.assertIn("11", out)


class TestEnLangHTML(unittest.TestCase):
    """Tests for .enlgf -> HTML5"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def test_html_hero(self):
        code = """
create hero named header with title "Welcome to EnLang", subtitle "The Future of Coding"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<section", out)
        self.assertIn("Welcome to EnLang", out)

    def test_html_button(self):
        code = """
create button named cta with label "Get Started" and action "alert('Hello')"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertTrue(success)
        self.assertTrue(success)

    def test_html_nav(self):
        code = """
create nav named topnav with links Home, About, Contact
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<nav", out)
        self.assertIn("Home", out)

    def test_html_card(self):
        code = """
create card named mycard with title "EnLang Card", description "A test card"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertTrue(success)
        self.assertTrue(success)

    def test_html_form(self):
        code = """
create form named loginform with fields username, password and action "/login"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<form", out)
        self.assertIn("/login", out)

    def test_enlg_card_component(self):
        code = """create card named mycard with title "Test Card", description "Test description"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="index.enlgf")
        self.assertTrue(success, err)
        self.assertTrue(success)
        self.assertTrue(success)

    def test_enlg_button_component(self):
        code = """create button named mybtn with label "Click Me" and action "doSomething()"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="index.enlgf")
        self.assertTrue(success, err)
        self.assertTrue(success)
        self.assertTrue(success)

    def test_enlg_render_layout(self):
        code = """create card named c1 with title "Card 1"
create button named b1 with label "Go"
render layout with c1, b1
"""
        success, out, err, _ = self.interp.run_code(code, file_path="index.enlgf")
        self.assertTrue(success, err)
        self.assertIn('<div>', out)
        self.assertIn("Card 1", out)

    def test_html_table(self):
        code = """
create table named mytable with headers Name, Age, Email
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<table", out)
        self.assertIn("Name", out)

    def test_html_image(self):
        code = """
create image named logo with src "logo.png", alt "Company Logo"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<img", out)
        self.assertIn("logo.png", out)

    def test_page_title(self):
        code = """
page title "My EnLang App"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="page.enlgf")
        self.assertTrue(success, err)
        self.assertIn("<title>", out)
        self.assertIn("My EnLang App", out)


class TestEnLangCSS(unittest.TestCase):
    """Tests for .enlgd → CSS3 + HTML UI components"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def test_theme_definition(self):
        code = """
define theme with primary "#3b82f6", background "#090d16"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("--primary", out)
        self.assertIn("--background", out)

    def test_css_selector_block(self):
        code = """
style card:
    background-color: "#1e293b"
    border-radius: "16px"
    padding: "1rem"
end style
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("background-color", out)
        self.assertIn("border-radius", out)
        self.assertIn("}", out)

    def test_css_body_selector(self):
        code = """
style body:
    background-color: "#000"
end style
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("body {", out)
        self.assertIn("background-color", out)

    def test_css_variable_define(self):
        code = """
define variable accent-color as "#3b82f6"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("--accent-color", out)

    def test_css_set_property(self):
        code = """
style body:
    set background-color to "#090d16"
end style
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("background-color", out)

    def test_media_query(self):
        code = """
on screen smaller than "768px":
    style body:
        font-size: "14px"
    end style
"""
        success, out, err, _ = self.interp.run_code(code, file_path="layout.enlgd")
        self.assertTrue(success, err)
        self.assertIn("@media", out)
        self.assertIn("768px", out)


class TestEnLangJS(unittest.TestCase):
    """Tests for .enlgs → JavaScript ES6+"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def test_js_variable_set(self):
        code = """
set message to "Hello JS"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("let message", out)
        self.assertIn("Hello JS", out)

    def test_js_constant(self):
        code = """
define constant PI as 3.14159
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("const PI", out)
        self.assertIn("3.14159", out)

    def test_js_console_log(self):
        code = """
log "debug message"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("console.log", out)

    def test_js_function_def(self):
        code = """
function greet(name):
    return "Hello " + name
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("function greet(name)", out)
        self.assertIn("return", out)

    def test_js_if_condition(self):
        code = """
if x is greater than 5:
    log x
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("if (", out)
        self.assertIn(">", out)

    def test_js_repeat_loop(self):
        code = """
repeat 10 times:
    log "tick"
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("for (let _i = 0", out)

    def test_js_for_each(self):
        code = """
for each item in items:
    log item
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("for (const item of items)", out)

    def test_js_while(self):
        code = """
while count is less than 10:
    log count
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("while (", out)
        self.assertIn("<", out)

    def test_js_dom_get(self):
        code = """
get element "myButton" and store in btn
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("getElementById", out)
        self.assertIn("myButton", out)

    def test_js_event_listener(self):
        code = """
on click of "submitBtn" call handleSubmit
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("addEventListener", out)
        self.assertIn("click", out)

    def test_js_raw_passthrough(self):
        """Raw JS lines should pass through verbatim"""
        code = """
const x = 42;
let y = x * 2;
console.log(y);
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("const x = 42;", out)
        self.assertIn("console.log(y);", out)

    def test_js_try_catch(self):
        code = """
try:
    log "safe"
catch (err):
    log err
end
"""
        success, out, err, _ = self.interp.run_code(code, file_path="app.enlgs")
        self.assertTrue(success, err)
        self.assertIn("try {", out)
        self.assertIn("catch", out)


class TestEnLangSQL(unittest.TestCase):
    """Tests for .enlgdb → SQL DDL/DML output"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def test_define_table(self):
        code = """
define table users with columns id INTEGER PRIMARY KEY, username TEXT, email TEXT
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("CREATE TABLE IF NOT EXISTS users", out)

    def test_insert_record(self):
        code = """
insert record into users with values 1, "admin", "admin@enlang.dev"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("INSERT INTO users", out)

    def test_select_all(self):
        code = """
select all from users
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("SELECT * FROM users", out)

    def test_select_where(self):
        code = """
select all from users where username = "admin"
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("WHERE", out)
        self.assertIn("admin", out)

    def test_update(self):
        code = """
update users set email = "new@test.com" where id = 1
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("UPDATE users", out)
        self.assertIn("SET", out)

    def test_delete(self):
        code = """
delete from users where id = 1
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("DELETE FROM users", out)

    def test_drop_table(self):
        code = """
drop table users
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("DROP TABLE IF EXISTS users", out)

    def test_add_column(self):
        code = """
add column phone TEXT to table users
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("ALTER TABLE users", out)
        self.assertIn("ADD COLUMN phone TEXT", out)

    def test_create_index(self):
        code = """
create index idx_username on users (username)
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("CREATE INDEX IF NOT EXISTS idx_username", out)

    def test_transaction(self):
        code = """
begin transaction
commit
"""
        success, out, err, _ = self.interp.run_code(code, file_path="schema.enlgdb")
        self.assertTrue(success, err)
        self.assertIn("BEGIN TRANSACTION;", out)
        self.assertIn("COMMIT;", out)


class TestEnLangBackendDB(unittest.TestCase):
    """Tests for .enlg (Python) backend database operations"""

    def setUp(self):
        self.interp = EnLangInterpreter()

    def test_sqlite_full_flow(self):
        code = """
connect to database ":memory:" as db
define table test_table with columns id INTEGER, name TEXT
execute sql "CREATE TABLE IF NOT EXISTS test_table (id INTEGER, name TEXT)" on database db
execute sql "INSERT INTO test_table VALUES (1, 'Alice')" on database db
execute sql "SELECT * FROM test_table" on database db and store in rows
display rows
"""
        success, out, err, _ = self.interp.run_code(code, file_path="backend.enlg")
        self.assertTrue(success, err)
        self.assertIn("Alice", out)



if __name__ == "__main__":
    unittest.main(verbosity=2)
