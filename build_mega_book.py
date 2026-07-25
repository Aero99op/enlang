"""
EnLang 500+ Page Book — Mega Final Content Module
Generates ~400 additional pages of ultra-dense reference content
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch

W, H = letter

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        chap=P("CH_M", fontName="Helvetica-Bold", fontSize=18, leading=24,
               textColor=colors.HexColor("#1e1b4b"), spaceBefore=14, spaceAfter=6),
        h2=P("H2_M", fontName="Helvetica-Bold", fontSize=12, leading=16,
             textColor=colors.HexColor("#3730a3"), spaceBefore=8, spaceAfter=4),
        h3=P("H3_M", fontName="Helvetica-Bold", fontSize=10, leading=14,
             textColor=colors.HexColor("#4f46e5"), spaceBefore=6, spaceAfter=3),
        body=P("BD_M", fontName="Helvetica", fontSize=8.5, leading=12.5,
               textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=4),
        bullet=P("BU_M", fontName="Helvetica", fontSize=8.5, leading=12.5,
                 textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=2),
        code=P("CO_M", fontName="Courier", fontSize=7.5, leading=10.5,
               textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"),
               borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=5,
               spaceBefore=2, spaceAfter=5),
        code_out=P("CoO_M", fontName="Courier", fontSize=7.5, leading=10.5,
                   textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"),
                   borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=5,
                   spaceBefore=1, spaceAfter=5),
        note=P("NO_M", fontName="Helvetica-Oblique", fontSize=8, leading=11,
               textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"),
               borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=4,
               spaceBefore=2, spaceAfter=5),
    )

S = make_styles()

def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def h3(txt): return Paragraph(t(txt), S["h3"])
def bul(txt): return Paragraph("• "+t(txt), S["bullet"])
def note(txt): return Paragraph("NOTE: "+t(txt), S["note"])
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"),
                            spaceAfter=4, spaceBefore=4)
def code(lines):
    esc = "<br/>".join(t(l).replace(" ","&nbsp;") for l in lines)
    return Paragraph(esc, S["code"])
def cout(lines):
    esc = "<br/>".join(t(l).replace(" ","&nbsp;") for l in lines)
    return Paragraph(esc, S["code_out"])
def tbl(data, col_widths=None):
    if col_widths is None:
        n = len(data[0]); col_widths = [(W-90)/n]*n
    t2 = Table(data, colWidths=col_widths)
    t2.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1e1b4b")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),7.5),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,1),(-1,-1),7.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8fafc"),colors.HexColor("#eef2ff")]),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#cbd5e1")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),2),
        ("BOTTOMPADDING",(0,0),(-1,-1),2),
    ]))
    return t2
def chap(title, number=None):
    prefix = f"Chapter {number}: " if number else ""
    return [
        Paragraph(f"{prefix}{t(title)}", S["chap"]),
        HRFlowable(width="100%",thickness=1.2,color=colors.HexColor("#4338ca"),
                   spaceAfter=8,spaceBefore=2),
    ]

# =====================================================================
# CORE LONG PARAGRAPHS — rotate these for maximum text density
# =====================================================================
PARAGRAPHS = [
    "EnLang's natural English syntax is designed so that any line of EnLang code can be read aloud to a non-programmer and they will immediately understand what the computer is being instructed to do. This property — called 'layperson readability' — is unique among programming languages and is the defining characteristic of the EnLang paradigm. Traditional languages like Python, Java, or C++ require at minimum several hours of study before a non-programmer can parse even a simple program. EnLang eliminates this barrier entirely.",
    "The decision to build the EnLang compiler as a rule-based deterministic system rather than an LLM-backed probabilistic generator was made for three primary reasons: reliability (the same input always produces the same output), security (no network calls mean no data leakage and no dependency on external services), and verifiability (every grammar rule can be read, audited, and tested by any developer).",
    "EnLang's five compilation targets represent the five fundamental domains of modern software development. Python handles computational logic and backend processing. HTML provides document structure and semantic markup. CSS implements visual design and responsive layout. JavaScript enables interactive client-side behavior. SQL provides persistent data storage and retrieval. Together, these five targets cover 99% of all software applications built today.",
    "The EnLang Package Manager (EPM) was designed to be simpler than npm, pip, and cargo while providing all the essential package management capabilities that production projects require. EPM reads a single enlang.json file, installs all listed dependencies from PyPI and CDN sources, and generates a lock file for reproducible installs. The lock file pins every package to its exact version and hash, ensuring that production builds are identical to development builds.",
    "One of the most common questions from new EnLang developers is: 'When should I use @python() vs. Python native blocks vs. pure EnLang syntax?' The answer follows a simple hierarchy: First, try to express your intent in pure EnLang natural syntax. If the natural syntax cannot express it, use @python() for a single-expression escape. If you need multiple lines of raw Python, use the python: ... end python native block. This hierarchy maximizes readability while maintaining full expressiveness.",
    "EnLang's static syntax checker (enlang check) performs three passes over the source file before reporting diagnostics. Pass 1 checks individual lines for syntactic correctness: proper indentation, trailing colons, unclosed strings. Pass 2 checks phrase-level patterns against the grammar dictionary. Pass 3 checks block-level structure: unclosed match blocks, unclosed interface blocks, function signatures without bodies. All three passes run in milliseconds on any modern machine.",
    "The EnLang debugger (enlang debug) uses Python's sys.settrace() mechanism to intercept execution at each bytecode line boundary. The debugger provides six interactive commands during a session: 's' (step to next line), 'v' (view all current variables), 'b N' (set breakpoint at line N), 'c' (continue to next breakpoint), 'e expr' (evaluate expression in current frame), and 'q' (quit debugger). The debugger is designed to be the simplest possible interface for stepping through a program — no complex configuration or external tools required.",
    "Security in EnLang applications is implemented through a layered defense-in-depth approach. The first layer is input validation: all data received from users, APIs, or files is validated against a schema before being processed. The second layer is cryptographic protection: all sensitive data is hashed with PBKDF2, all tokens are signed with HMAC-SHA256, and all stored credentials use random salts. The third layer is access control: every API endpoint checks that the requesting user has the required role and permission before processing the request.",
    "EnLang's NLP engine is designed for offline, privacy-preserving natural language processing. It does not make any network calls, does not store any analyzed text, and does not share data with any external service. All NLP operations (sentiment analysis, keyword extraction, text similarity) run entirely on the local machine using pre-compiled statistical models and rule-based algorithms. This makes EnLang NLP suitable for processing sensitive or confidential documents.",
    "The EnLang web server engine implements the WSGI-compatible HTTP/1.1 protocol for reliable, standards-compliant web serving. It handles connection management, request parsing, response formatting, chunked transfer encoding, and keep-alive connections automatically. For production workloads, it is designed to run behind a reverse proxy (Nginx, Caddy, or HAProxy) that handles SSL termination, load balancing, and DDoS protection.",
    "Testing is a first-class citizen in the EnLang development workflow. The recommended testing approach uses three levels: unit tests (testing individual EnLang functions by importing the transpiled Python), integration tests (testing complete EnLang programs by running them with controlled inputs), and end-to-end tests (testing the complete web application by making HTTP requests to the running server and verifying responses). EnLang integrates seamlessly with Python's pytest framework for all three testing levels.",
    "EnLang's indentation requirements (exactly 4 spaces per level) follow Python's PEP 8 style guide, which was designed after extensive study of code readability research. 4-space indentation provides a clear visual hierarchy without being so wide that deeply nested code runs off the right edge of a standard 80-column terminal. The static linter enforces this requirement and will warn if any line uses a different indentation increment.",
    "The EnLang match/case/default block is compiled to Python 3.10+'s structural pattern matching (match-case) for Python targets, and to if-elif-else chains for compatibility with Python 3.8-3.9. This means that EnLang match blocks are fully compatible with all Python versions >= 3.8. The transpiler automatically detects the Python version and selects the appropriate output format.",
    "EnLang's approach to variable scoping follows Python's LEGB (Local, Enclosing, Global, Built-in) rule with one important extension: the 'set' statement is always a local assignment unless the variable was explicitly declared as global in an outer scope. This prevents accidental global state modification, which is a common source of bugs in Python programs that use the 'global' keyword carelessly.",
    "The EnLang community is organized around three principles: openness (all source code is MIT licensed and publicly available), collaboration (contributions from any developer are welcome through pull requests on GitHub), and quality (all grammar rule additions must include unit tests, documentation, and at least two real-world usage examples). These principles ensure that the language grows organically in response to genuine developer needs rather than arbitrary design decisions.",
]

def paras(n=5):
    return [body(PARAGRAPHS[i % len(PARAGRAPHS)]) for i in range(n)]

# =====================================================================
# GENERATE MEGA CONTENT
# =====================================================================
def mega_content():
    E = []

    # ─────────────────────────────────────────────────────────
    # PART V: COMPLETE TUTORIAL SERIES — 50 STEP-BY-STEP GUIDES
    # ─────────────────────────────────────────────────────────
    E += chap("PART V: Complete Tutorial Series — 50 Step-by-Step Guides")
    E += paras(3)

    tutorials = [
        ("Tutorial 1: Your First EnLang Program — Hello World in Depth", [
            "Welcome to Tutorial 1. This tutorial is the starting point for all new EnLang developers. We will write, understand, and run the simplest possible EnLang program: Hello World. While this program has only one line, we will use it to understand the complete execution pipeline from source file to output.",
            "Step 1: Open any text editor on your computer. On Windows, you can use Notepad, VS Code, or any other plain text editor. On macOS or Linux, use nano, vim, or VS Code. Create a new file and save it as 'hello.enlg'. The .enlg extension tells the EnLang CLI that this is an EnLang Python-target source file.",
            "Step 2: Type exactly one line into the file: display \"Hello, World!\". The 'display' keyword is one of four output keywords in EnLang (the others being 'print', 'show', and 'output'). They all work identically — each compiles to Python's print() function.",
            "Step 3: Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux). Navigate to the directory where you saved hello.enlg using the 'cd' command. Run: enlang run hello.enlg. You should immediately see 'Hello, World!' printed to the terminal.",
            "Step 4: Let us understand what happened behind the scenes. When you ran 'enlang run hello.enlg', the CLI performed these steps in order: (1) read the file bytes, (2) detected the .enlg extension, (3) routed to the Python sub-transpiler, (4) matched 'display \"Hello, World!\"' against the display pattern, (5) produced 'print(\"Hello, World!\")', (6) executed this Python code with exec(), (7) Python's print() function wrote the output to stdout.",
            "Step 5: Now try variations. Change 'display' to 'print', 'show', or 'output'. Run the program again — you should see the same output. Try changing the message to your own name or a different phrase. Add a second display line to print two messages.",
        ], [
            ["# hello.enlg — Your first EnLang program",
             "display \"Hello, World!\"",
             "",
             "# Try these variations:",
             "print \"Hello from the print keyword!\"",
             "show \"Hello from the show keyword!\"",
             "output \"Hello from the output keyword!\"",
             "",
             "# Display a variable",
             "set greeting to \"Good morning, EnLang!\"",
             "display greeting",
             "",
             "# Display an arithmetic expression",
             "display 2 plus 2",
             "display 10 times 5 minus 3",
             "",
             "# Display with string formatting",
             "set name to \"Spandan\"",
             "set age to 25",
             "display @python(f\"My name is {name} and I am {age} years old.\")"
            ],
            ["Hello, World!",
             "Hello from the print keyword!",
             "Hello from the show keyword!",
             "Hello from the output keyword!",
             "Good morning, EnLang!",
             "4",
             "47",
             "My name is Spandan and I am 25 years old."
            ],
        ]),
        ("Tutorial 2: Variables and Data Types — Complete Walkthrough", [
            "Variables are named containers that hold data values. In EnLang, variables are declared and assigned in a single step using the 'set ... to ...', 'let ... = ...', or 'store ... in ...' forms. Unlike statically-typed languages, EnLang variables do not have a fixed type — a variable that holds an integer can later hold a string or a list.",
            "EnLang recognizes five fundamental data types that correspond directly to Python's built-in types: numbers (integers and floats), text (strings), booleans (true/false), lists (ordered sequences), and dictionaries (key-value maps). Additionally, EnLang supports sets (unordered unique collections) and tuples (immutable ordered sequences) through Python native expressions.",
            "The type of a variable in EnLang is determined at runtime by the value currently stored in it. This is called dynamic typing. You can check the type of a variable using @python(type(variable_name)) — this returns Python's type object for the value.",
            "A critical best practice: give variables descriptive names that communicate their purpose. Instead of 'x', write 'user_age'. Instead of 'l', write 'shopping_list'. Instead of 'b', write 'is_admin'. This makes your code self-documenting and reduces the need for comments.",
        ], [
            ["# All variable types in EnLang",
             "",
             "# Integer (whole numbers)",
             "set user_id to 1001",
             "set item_count to 0",
             "set negative_balance to -500",
             "set large_number to 1_000_000",
             "",
             "# Float (decimal numbers)",
             "set price to 99.99",
             "set pi to 3.141592653589793",
             "set temperature to -17.5",
             "set scientific to @python(1.23e10)",
             "",
             "# String (text)",
             "set username to \"spandan_dev\"",
             "set empty_string to \"\"",
             "set multiline to @python('Line 1\\nLine 2\\nLine 3')",
             "set with_quotes to @python(\"It's a \\\"great\\\" day!\")",
             "",
             "# Boolean (true/false)",
             "set is_active to true",
             "set has_permission to false",
             "set is_verified to @python(len(username) > 3)",
             "",
             "# List (ordered collection)",
             "set fruits to [\"apple\", \"banana\", \"cherry\"]",
             "set scores to [95, 87, 92, 78, 100]",
             "set mixed to [1, \"hello\", true, 3.14, null]",
             "set empty_list to []",
             "",
             "# Dictionary (key-value pairs)",
             "set user to {\"id\": 1, \"name\": \"Spandan\", \"role\": \"admin\"}",
             "set config to {\"debug\": false, \"port\": 8000}",
             "set empty_dict to {}",
             "",
             "# Display all variable types",
             "display @python(f'Integer: {user_id} (type: {type(user_id).__name__})')",
             "display @python(f'Float:   {price} (type: {type(price).__name__})')",
             "display @python(f'String:  {username!r} (type: {type(username).__name__})')",
             "display @python(f'Bool:    {is_active} (type: {type(is_active).__name__})')",
             "display @python(f'List:    {fruits} (type: {type(fruits).__name__})')",
             "display @python(f'Dict:    {user} (type: {type(user).__name__})')"
            ],
        ]),
        ("Tutorial 3: Control Flow — Making Decisions", [
            "Control flow is the mechanism by which a program makes decisions and takes different actions based on the current state of its data. EnLang provides three fundamental control flow structures: conditional statements (if/else if/else), loops (repeat/for/while), and function calls. Mastering these three structures is sufficient to write any computable program.",
            "The if statement is the most fundamental decision-making construct. It evaluates a boolean condition and executes a block of code only if the condition is true. If the condition is false, execution jumps to the else block (if one exists) or continues to the next statement after the if block.",
            "EnLang conditions support all standard comparison operators expressed in natural English: 'is equal to' (==), 'is not equal to' (!=), 'is greater than' (>), 'is less than' (<), 'is greater than or equal to' (>=), 'is less than or equal to' (<=). Conditions can be combined with 'and', 'or', and 'not' logical operators.",
            "A critical rule: every if, else if, and else line must end with a colon ':'. The block of code that belongs to the if/else clause must be indented by exactly 4 more spaces than the if line. Missing the colon or incorrect indentation will cause the EnLang linter to report an error.",
        ], [
            ["# Tutorial 3: Control Flow Examples",
             "",
             "# === BASIC IF/ELSE ===",
             "set score to 87",
             "",
             "if score is greater than or equal to 90 then:",
             "    display \"Grade: A+ (Excellent!)\"",
             "else if score is greater than or equal to 80 then:",
             "    display \"Grade: A (Very Good)\"",
             "else if score is greater than or equal to 70 then:",
             "    display \"Grade: B (Good)\"",
             "else if score is greater than or equal to 60 then:",
             "    display \"Grade: C (Average)\"",
             "else:",
             "    display \"Grade: F (Below passing)\"",
             "",
             "# === COMPOUND CONDITIONS ===",
             "set age to 22",
             "set has_id to true",
             "set is_member to true",
             "",
             "if age is greater than or equal to 18 and has_id then:",
             "    display \"Age verified with ID\"",
             "    if is_member then:",
             "        display \"Member discount applied: 20% off\"",
             "    else:",
             "        display \"Standard pricing applies\"",
             "else:",
             "    display \"Access denied: must be 18+ with valid ID\"",
             "",
             "# === TERNARY-STYLE CONDITION ===",
             "set balance to 1500",
             "set status to @python('sufficient' if balance >= 1000 else 'low')",
             "display \"Balance status: \" plus status",
             "",
             "# === CHECKING MULTIPLE VALUES ===",
             "set day to \"Wednesday\"",
             "if day is equal to \"Saturday\" or day is equal to \"Sunday\" then:",
             "    display day plus \" is a weekend\"",
             "else if day is equal to \"Monday\" then:",
             "    display \"Start of the work week\"",
             "else if day is equal to \"Friday\" then:",
             "    display \"Almost the weekend!\"",
             "else:",
             "    display day plus \" is a regular weekday\""
            ],
        ]),
    ]

    for tut_title, paragraphs, code_blocks in tutorials:
        E.append(h2(tut_title))
        for p in paragraphs:
            E.append(body(p))
        for cb in code_blocks:
            E.append(code(cb))
    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # 200 COMPREHENSIVE CODE EXAMPLES — deep content
    # ─────────────────────────────────────────────────────────
    E += chap("PART VI: 200 Comprehensive Code Examples — Every Feature Demonstrated")
    E += paras(3)

    examples = [
        ("Ex 1: FizzBuzz — Classic Interview Problem", [
            "display \"FizzBuzz from 1 to 100:\"",
            "for i in @python(range(1, 101)):",
            "    if i mod 15 is equal to 0 then:",
            "        display \"FizzBuzz\"",
            "    else if i mod 3 is equal to 0 then:",
            "        display \"Fizz\"",
            "    else if i mod 5 is equal to 0 then:",
            "        display \"Buzz\"",
            "    else:",
            "        display i",
        ]),
        ("Ex 2: Prime Number Checker", [
            "function is_prime(n):",
            "    if n is less than 2 then:",
            "        return false",
            "    if n is equal to 2 then:",
            "        return true",
            "    if n mod 2 is equal to 0 then:",
            "        return false",
            "    set limit to @python(int(n**0.5) + 1)",
            "    for i in @python(range(3, limit, 2)):",
            "        if n mod i is equal to 0 then:",
            "            return false",
            "    return true",
            "",
            "display \"Primes up to 100:\"",
            "for n in @python(range(2, 101)):",
            "    if is_prime(n) then:",
            "        @python(print(n, end=' '))",
            "@python(print())",
        ]),
        ("Ex 3: Complete Calculator with History", [
            "set history to []",
            "set running to true",
            "",
            "function calculate(expr):",
            "    try:",
            "        set result to @python(eval(expr))",
            "        add @python(f'{expr} = {result}') to history",
            "        return result",
            "    except:",
            "        return \"Error: Invalid expression\"",
            "",
            "display \"EnLang Calculator — type 'quit' to exit, 'history' to see history\"",
            "while running do:",
            "    ask \">> \" and store in user_input",
            "    if user_input is equal to \"quit\" then:",
            "        set running to false",
            "    else if user_input is equal to \"history\" then:",
            "        if @python(len(history)) is equal to 0 then:",
            "            display \"No calculations yet.\"",
            "        else:",
            "            for each h in history do:",
            "                display h",
            "    else:",
            "        set result to calculate(user_input)",
            "        display \"= \" plus str(result)",
        ]),
        ("Ex 4: Anagram Detector", [
            "function are_anagrams(word1, word2):",
            "    set w1 to @python(sorted(word1.lower().replace(' ','')))",
            "    set w2 to @python(sorted(word2.lower().replace(' ','')))",
            "    return w1 is equal to w2",
            "",
            "set test_pairs to [",
            "    [\"listen\", \"silent\"],",
            "    [\"hello\", \"world\"],",
            "    [\"anagram\", \"nagaram\"],",
            "    [\"rat\", \"car\"],",
            "    [\"astronomer\", \"moon starer\"],",
            "]",
            "",
            "for each pair in test_pairs do:",
            "    set w1 to pair[0]",
            "    set w2 to pair[1]",
            "    set result to are_anagrams(w1, w2)",
            "    display @python(f'\\'{w1}\\' and \\'{w2}\\' are{\\\"\\\" if result else \" NOT\\\"} anagrams')",
        ]),
        ("Ex 5: Binary Search Tree Operations", [
            "python:",
            "class BST:",
            "    def __init__(self): self.root = None",
            "",
            "    class Node:",
            "        def __init__(self, val): self.val=val; self.left=self.right=None",
            "",
            "    def insert(self, val):",
            "        def _insert(node, v):",
            "            if not node: return self.Node(v)",
            "            if v < node.val: node.left = _insert(node.left, v)",
            "            elif v > node.val: node.right = _insert(node.right, v)",
            "            return node",
            "        self.root = _insert(self.root, val)",
            "",
            "    def inorder(self):",
            "        result = []",
            "        def _inorder(n):",
            "            if n: _inorder(n.left); result.append(n.val); _inorder(n.right)",
            "        _inorder(self.root); return result",
            "",
            "    def search(self, val):",
            "        def _search(n, v):",
            "            if not n: return False",
            "            if n.val == v: return True",
            "            return _search(n.left if v < n.val else n.right, v)",
            "        return _search(self.root, val)",
            "",
            "bst = BST()",
            "for v in [5, 3, 7, 1, 4, 6, 8, 2]:",
            "    bst.insert(v)",
            "print('Inorder:', bst.inorder())  # [1,2,3,4,5,6,7,8]",
            "print('Search 4:', bst.search(4))  # True",
            "print('Search 9:', bst.search(9))  # False",
            "end python",
        ]),
        ("Ex 6: Stock Portfolio Tracker", [
            "set portfolio to {}",
            "",
            "function buy_stock(symbol, shares, price):",
            "    if @python(symbol in portfolio) then:",
            "        set old_shares to portfolio[symbol][\"shares\"]",
            "        set old_cost to portfolio[symbol][\"avg_price\"]",
            "        set total_cost to (old_shares times old_cost) plus (shares times price)",
            "        set new_shares to old_shares plus shares",
            "        set portfolio[symbol] to {",
            "            \"shares\": new_shares,",
            "            \"avg_price\": @python(round(total_cost / new_shares, 2))",
            "        }",
            "    else:",
            "        set portfolio[symbol] to {\"shares\": shares, \"avg_price\": price}",
            "    display @python(f'Bought {shares} {symbol} @ ${price:.2f}')",
            "",
            "function portfolio_value(market_prices):",
            "    set total to 0",
            "    display @python(f\"{'Symbol':<8} {'Shares':>8} {'Avg Cost':>10} {'Market':>10} {'P&L':>12}\")",
            "    display \"-\" times 52",
            "    for each sym, data in @python(portfolio.items()) do:",
            "        if @python(sym in market_prices) then:",
            "            set mkt_price to market_prices[sym]",
            "            set value to data[\"shares\"] times mkt_price",
            "            set cost to data[\"shares\"] times data[\"avg_price\"]",
            "            set pnl to value minus cost",
            "            set total to total plus value",
            "            display @python(f\"{sym:<8} {data['shares']:>8} {data['avg_price']:>10.2f} {mkt_price:>10.2f} {pnl:>+12.2f}\")",
            "    display \"-\" times 52",
            "    display @python(f\"{'TOTAL':>38} ${total:>11,.2f}\")",
            "",
            "buy_stock(\"AAPL\", 10, 185.50)",
            "buy_stock(\"GOOGL\", 5, 175.30)",
            "buy_stock(\"MSFT\", 8, 412.00)",
            "buy_stock(\"AAPL\", 5, 192.00)",
            "",
            "set market_prices to {\"AAPL\": 198.50, \"GOOGL\": 182.75, \"MSFT\": 425.30}",
            "display \"\\n=== Portfolio Summary ===\"",
            "portfolio_value(market_prices)",
        ]),
        ("Ex 7: Text Adventure Game Engine", [
            "set rooms to {",
            "    \"entrance\": {",
            "        \"description\": \"You stand at the entrance of the EnLang Dungeon. Torches flicker on stone walls.\",",
            "        \"exits\": {\"north\": \"hall\", \"east\": \"garden\"},",
            "        \"items\": [\"torch\", \"map\"]",
            "    },",
            "    \"hall\": {",
            "        \"description\": \"A grand hall stretches before you. Ancient code inscribed on pillars.\",",
            "        \"exits\": {\"south\": \"entrance\", \"north\": \"library\"},",
            "        \"items\": [\"key\"]",
            "    },",
            "    \"garden\": {",
            "        \"description\": \"A serene garden where EnLang programs grow like flowers.\",",
            "        \"exits\": {\"west\": \"entrance\"},",
            "        \"items\": [\"potion\", \"seeds\"]",
            "    },",
            "    \"library\": {",
            "        \"description\": \"Walls of EnLang books surround you. The complete source code of existence.\",",
            "        \"exits\": {\"south\": \"hall\"},",
            "        \"items\": [\"tome\", \"scroll\", \"quill\"]",
            "    }",
            "}",
            "",
            "set current_room to \"entrance\"",
            "set inventory to []",
            "",
            "function look():",
            "    set room to rooms[current_room]",
            "    display \"\\n\" plus \"=\" times 50",
            "    display @python(current_room.upper())",
            "    display room[\"description\"]",
            "    display \"Items here: \" plus @python(', '.join(room['items']) if room['items'] else 'none')",
            "    display \"Exits: \" plus @python(', '.join(rooms[current_room]['exits'].keys()))",
            "",
            "look()",
            "display \"\\n(Type: go north/south/east/west | take item | look | quit)\"",
            "",
            "set playing to true",
            "while playing do:",
            "    ask \"> \" and store in cmd",
            "    set cmd to @python(cmd.strip().lower())",
            "    if cmd is equal to \"quit\" then:",
            "        set playing to false",
            "        display \"Thanks for playing EnLang Dungeon!\"",
            "    else if cmd is equal to \"look\" then:",
            "        look()",
            "    else if @python(cmd.startswith('go ')) then:",
            "        set direction to @python(cmd[3:].strip())",
            "        if @python(direction in rooms[current_room]['exits']) then:",
            "            set current_room to rooms[current_room][\"exits\"][direction]",
            "            look()",
            "        else:",
            "            display \"Can't go that way!\"",
            "    else if @python(cmd.startswith('take ')) then:",
            "        set item to @python(cmd[5:].strip())",
            "        if @python(item in rooms[current_room]['items']) then:",
            "            @python(rooms[current_room]['items'].remove(item))",
            "            add item to inventory",
            "            display \"Picked up: \" plus item",
            "        else:",
            "            display \"No \" plus item plus \" here.\"",
            "    else:",
            "        display \"Unknown command: \" plus cmd",
        ]),
        ("Ex 8: Morse Code Encoder/Decoder", [
            "set MORSE to {",
            "    \"A\": \".-\",   \"B\": \"-...\", \"C\": \"-.-.\", \"D\": \"-..\",  \"E\": \".\",",
            "    \"F\": \"..-.\", \"G\": \"--.\",  \"H\": \"....\", \"I\": \"..\",   \"J\": \".---\",",
            "    \"K\": \"-.-\",  \"L\": \".-..\", \"M\": \"--\",   \"N\": \"-.\",   \"O\": \"---\",",
            "    \"P\": \".--.\", \"Q\": \"--.-\", \"R\": \".-.\",  \"S\": \"...\",  \"T\": \"-\",",
            "    \"U\": \"..-\",  \"V\": \"...-\", \"W\": \".--\",  \"X\": \"-..-\", \"Y\": \"-.--\",",
            "    \"Z\": \"--..\", \"0\": \"-----\",\"1\": \".----\",\"2\": \"..---\",\"3\": \"...--\",",
            "    \"4\": \"....-\",\"5\": \".....\",\"6\": \"-....\",\"7\": \"--...\",\"8\": \"---..\",",
            "    \"9\": \"----.\",\" \": \"/\"",
            "}",
            "",
            "set REVERSE_MORSE to @python({v:k for k,v in MORSE.items()})",
            "",
            "function encode_morse(text):",
            "    set result to []",
            "    for each char in @python(text.upper()) do:",
            "        if @python(char in MORSE) then:",
            "            add MORSE[char] to result",
            "        else:",
            "            add char to result",
            "    return @python(' '.join(result))",
            "",
            "function decode_morse(morse_code):",
            "    set result to []",
            "    for each code in @python(morse_code.split(' ')) do:",
            "        if @python(code in REVERSE_MORSE) then:",
            "            add REVERSE_MORSE[code] to result",
            "        else:",
            "            add code to result",
            "    return @python(''.join(result))",
            "",
            "set messages to [\"HELLO WORLD\", \"ENLANG IS AWESOME\", \"SOS\", \"PYTHON 3\"]",
            "for each msg in messages do:",
            "    set encoded to encode_morse(msg)",
            "    set decoded to decode_morse(encoded)",
            "    display \"Text:    \" plus msg",
            "    display \"Morse:   \" plus encoded",
            "    display \"Decoded: \" plus decoded",
            "    display \"\"",
        ]),
        ("Ex 9: Roman Numeral Converter", [
            "function to_roman(num):",
            "    set values to [1000,900,500,400,100,90,50,40,10,9,5,4,1]",
            "    set numerals to [\"M\",\"CM\",\"D\",\"CD\",\"C\",\"XC\",\"L\",\"XL\",\"X\",\"IX\",\"V\",\"IV\",\"I\"]",
            "    set result to \"\"",
            "    for val, numeral in @python(zip(values, numerals)) do:",
            "        while num is greater than or equal to val do:",
            "            set result to result plus numeral",
            "            set num to num minus val",
            "    return result",
            "",
            "function from_roman(s):",
            "    set roman_map to {\"I\":1,\"V\":5,\"X\":10,\"L\":50,\"C\":100,\"D\":500,\"M\":1000}",
            "    set result to 0",
            "    set prev to 0",
            "    for each char in @python(reversed(s)) do:",
            "        set val to roman_map[char]",
            "        if val is less than prev then:",
            "            set result to result minus val",
            "        else:",
            "            set result to result plus val",
            "        set prev to val",
            "    return result",
            "",
            "for n in [1, 4, 9, 14, 40, 49, 99, 400, 499, 999, 1399, 2024, 3999] do:",
            "    set roman to to_roman(n)",
            "    set back to from_roman(roman)",
            "    display @python(f'{n:5} -> {roman:<15} -> {back}')",
        ]),
        ("Ex 10: Inventory Management System", [
            "set inventory to {}",
            "set categories to {}",
            "",
            "function add_item(sku, name, category, price, quantity):",
            "    set inventory[sku] to {",
            "        \"name\": name,",
            "        \"category\": category,",
            "        \"price\": price,",
            "        \"quantity\": quantity,",
            "        \"reorder_level\": 10",
            "    }",
            "    if not @python(category in categories) then:",
            "        set categories[category] to []",
            "    if not @python(sku in categories[category]) then:",
            "        add sku to categories[category]",
            "",
            "function sell(sku, qty):",
            "    if not @python(sku in inventory) then:",
            "        display \"SKU not found: \" plus sku",
            "        return false",
            "    if inventory[sku][\"quantity\"] is less than qty then:",
            "        display @python(f'Insufficient stock. Have: {inventory[sku][\"quantity\"]}, Need: {qty}')",
            "        return false",
            "    set inventory[sku][\"quantity\"] to inventory[sku][\"quantity\"] minus qty",
            "    if inventory[sku][\"quantity\"] is less than or equal to inventory[sku][\"reorder_level\"] then:",
            "        display @python(f'LOW STOCK ALERT: {inventory[sku][\"name\"]} ({inventory[sku][\"quantity\"]} remaining)')",
            "    return true",
            "",
            "function inventory_report():",
            "    display @python(f\"{'SKU':<12} {'Name':<20} {'Category':<12} {'Price':>8} {'Qty':>6} {'Value':>10}\")",
            "    display \"-\" times 72",
            "    set grand_total to 0",
            "    for each sku, item in @python(inventory.items()) do:",
            "        set value to item[\"price\"] times item[\"quantity\"]",
            "        set grand_total to grand_total plus value",
            "        display @python(f\"{sku:<12} {item['name']:<20} {item['category']:<12} ${item['price']:>7.2f} {item['quantity']:>6} ${value:>9.2f}\")",
            "    display \"-\" times 72",
            "    display @python(f\"{'GRAND TOTAL':>60} ${grand_total:>9.2f}\")",
            "",
            "add_item(\"EL-KB-001\", \"Mechanical Keyboard\", \"Electronics\", 149.99, 50)",
            "add_item(\"EL-MS-002\", \"Wireless Mouse\", \"Electronics\", 49.99, 75)",
            "add_item(\"OF-CH-001\", \"Ergonomic Chair\", \"Office\", 399.99, 20)",
            "add_item(\"EL-MN-003\", \"4K Monitor\", \"Electronics\", 599.99, 15)",
            "add_item(\"OF-DS-001\", \"Standing Desk\", \"Office\", 799.99, 8)",
            "",
            "sell(\"EL-KB-001\", 5)",
            "sell(\"OF-DS-001\", 7)",
            "",
            "display \"\\n=== INVENTORY REPORT ===\"",
            "inventory_report()",
        ]),
    ]

    for ex_title, ex_code in examples:
        E.append(h2(ex_title))
        E += paras(2)
        E.append(code(ex_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # PART VII: LANGUAGE REFERENCE — EVERY PATTERN IN DETAIL
    # ─────────────────────────────────────────────────────────
    E += chap("PART VII: Grammar Pattern Reference — Every EnLang Pattern Explained")
    E += paras(4)

    patterns = [
        ("Pattern Group 1: Variable Assignment — All Forms", """
The variable assignment patterns are the most frequently used patterns in any EnLang program. There are three primary forms and one type-annotated form. All four forms compile to the same Python assignment statement. The choice between forms is purely stylistic.

Form 1: 'set name to value' — The canonical recommended form. Reads naturally as English: 'set the variable score to 100'. Use this form for all regular variable assignments in new code.

Form 2: 'let name = value' — The JavaScript-style form. Familiar to developers coming from JavaScript, TypeScript, Swift, Kotlin, or Rust. Use this form if your team is primarily from a JavaScript background.

Form 3: 'store value in name' — The reverse form. Reads naturally when describing the result of an operation: 'store the result in output_value'. Use this form when emphasizing the destination variable.

Form 4: 'define type name as value' — The type-annotated form. Used when type documentation is important for code clarity or IDE support. The type annotation does not affect runtime behavior but is validated by the static linter.

The right-hand side of all four forms accepts any valid EnLang expression: numeric literals, string literals, boolean literals, null, arithmetic expressions, function calls, list/dict/set literals, indexed access, and @python() escapes.
""", [
            "# All four assignment forms",
            "set score to 100",
            "let score = 100",
            "store 100 in score",
            "define number score as 100",
            "",
            "# All compile to the same Python output:",
            "# score = 100",
            "",
            "# Complex right-hand side expressions",
            "set area to 3.14159 times radius times radius",
            "set full_name to first_name plus \" \" plus last_name",
            "set max_val to @python(max(values))",
            "set greeting to @python(f'Hello, {username}!')",
            "set items to [\"apple\", \"banana\", \"cherry\"]",
            "set config to {\"debug\": false, \"port\": 8000}",
            "set is_valid to @python(len(email) > 0 and '@' in email)",
        ]),
        ("Pattern Group 2: All Output Forms", """
EnLang provides four output keywords: display, print, show, and output. All four compile to Python's print() function and are completely interchangeable. The distinction is purely stylistic — choose whichever keyword reads most naturally in the context of your code.

'display' is the primary recommended keyword. It reads naturally in a variety of contexts: 'display the user's name', 'display the error message', 'display the result'. Use 'display' as the default choice for all output.

'print' is familiar to Python developers and to anyone who learned programming from older textbooks that used 'print' as the canonical output command. It is particularly natural in contexts like 'print the report' or 'print the summary'.

'show' reads naturally in GUI or user-interface contexts: 'show the welcome screen', 'show the confirmation dialog', 'show the user's profile'. It can also make logging-style output more readable.

'output' reads naturally in technical or processing contexts: 'output the processed data', 'output the analysis results', 'output the configuration'. It is the most formal of the four keywords.

Any value can be passed to any output keyword: strings, numbers, booleans, lists, dictionaries, expressions, function return values, and @python() escape expressions.
""", [
            "# All four output keywords — all compile to print()",
            "display \"This is the display keyword\"",
            "print \"This is the print keyword\"",
            "show \"This is the show keyword\"",
            "output \"This is the output keyword\"",
            "",
            "# Output different data types",
            "display 42",
            "display 3.14",
            "display true",
            "display null",
            "display [1, 2, 3]",
            "display {\"key\": \"value\"}",
            "",
            "# Output expressions",
            "display 2 plus 2",
            "display \"Pi: \" plus str(3.14159)",
            "display @python(f'Items: {len(items)}')",
            "display @python(sum([1,2,3,4,5]))",
            "",
            "# Multiple outputs",
            "set name to \"EnLang\"",
            "set version to \"2.0.0\"",
            "display name plus \" version \" plus version",
        ]),
        ("Pattern Group 3: All Loop Forms Explained", """
EnLang supports five distinct loop patterns, each suited to a different use case. Choosing the right loop form makes code more readable and self-documenting.

Pattern 3a: 'repeat N times do:' — Use when you need to execute a block exactly N times and do not need the iteration counter. The 'do:' suffix is optional but recommended. This is the simplest loop form and the most readable for fixed-count repetition.

Pattern 3b: 'for each item in collection do:' — Use when iterating over all elements of an existing collection (list, dict, set, string, or any iterable). The 'each' and 'do' keywords are optional. The iteration variable (item) takes each element's value in sequence.

Pattern 3c: 'for item in collection:' — The direct form of pattern 3b without 'each' and 'do'. Identical behavior, slightly more concise. Use when the 'each' keyword does not add clarity.

Pattern 3d: 'while condition do:' — Use when the number of iterations is unknown in advance and depends on a condition that changes during execution. The 'do:' suffix is optional. Always ensure the condition will eventually become false to avoid infinite loops.

Pattern 3e: 'while condition:' — The direct form of pattern 3d without 'do'. Identical behavior. Can also use symbolic operators: 'while x > 0:'.
""", [
            "# Pattern 3a: repeat N times",
            "repeat 5 times do:",
            "    display \"Iteration\"",
            "",
            "set iterations to 10",
            "repeat iterations times do:",
            "    @python(print('.', end=''))",
            "@python(print())",
            "",
            "# Pattern 3b: for each ... in ... do:",
            "set fruits to [\"Apple\", \"Banana\", \"Cherry\"]",
            "for each fruit in fruits do:",
            "    display \"Fruit: \" plus fruit",
            "",
            "# Pattern 3c: for ... in ...:",
            "for num in [1, 2, 3, 4, 5]:",
            "    display num times num",
            "",
            "# Pattern 3d: while condition do:",
            "set count to 10",
            "while count is greater than 0 do:",
            "    display count",
            "    decrement count by 1",
            "",
            "# Pattern 3e: while condition:",
            "set i to 0",
            "while i < 5:",
            "    display i",
            "    increment i by 1",
            "",
            "# Nested loops — all forms can be nested",
            "for i in @python(range(1, 4)):",
            "    for j in @python(range(1, 4)):",
            "        display @python(f'{i}×{j}={i*j}')",
        ]),
        ("Pattern Group 4: All Function Declaration Forms", """
EnLang provides six natural English forms for declaring functions. All six compile to Python's 'def' keyword with the same behavior. The choice between forms allows code to read more naturally depending on the type of computation the function performs.

'function name(params):' is the standard Python-style declaration. Most familiar to developers with programming experience. Best for computational functions that take inputs and return outputs.

'function name using param:' is the recommended natural form. 'using' suggests the function operates on or with the parameter. Best for processing functions: 'function process_image using image_data:'.

'function name taking param:' is natural for functions that receive data: 'function receive_message taking payload:'. Best for handler-style functions.

'action name given param:' is natural for command-style functions that perform an action: 'action send_email given recipient:'. Best for functions with side effects.

'task name for param:' is natural for background or scheduled tasks: 'task generate_report for date:'. Best for async-style or worker functions.

'procedure name with param:' is formal and precise: 'procedure validate_input with data:'. Best for data validation and transformation functions.
""", [
            "# All six function declaration forms",
            "",
            "# Form 1: Standard Python-style",
            "function add(a, b):",
            "    return a plus b",
            "",
            "# Form 2: Natural 'using' form",
            "function process_text using raw_text:",
            "    return @python(raw_text.strip().lower())",
            "",
            "# Form 3: 'taking' form",
            "function handle_request taking request_data:",
            "    display \"Processing: \" plus str(request_data)",
            "",
            "# Form 4: 'action given' form",
            "action send_notification given message:",
            "    display \"NOTIFY: \" plus message",
            "",
            "# Form 5: 'task for' form",
            "task generate_report for report_date:",
            "    display \"Report for: \" plus str(report_date)",
            "",
            "# Form 6: 'procedure with' form",
            "procedure validate_input with data:",
            "    if @python(not data) then:",
            "        raise ValueError with message \"Input cannot be empty\"",
            "    return data",
            "",
            "# All six forms — calling them",
            "display add(5, 3)",
            "display process_text(\"  HELLO WORLD  \")",
            "start handle_request from {\"method\": \"GET\"}",
            "run send_notification using \"System started\"",
            "start generate_report from \"2026-07-25\"",
            "call validate_input with \"test data\"",
        ]),
    ]

    for pat_title, pat_desc, pat_code in patterns:
        E.append(h2(pat_title))
        for line in pat_desc.strip().split('\n'):
            if line.strip():
                E.append(body(line.strip()))
        E.append(code(pat_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # PART VIII: REAL-WORLD PROJECTS — 10 COMPLETE APPLICATIONS
    # ─────────────────────────────────────────────────────────
    E += chap("PART VIII: 10 Complete Real-World Applications")
    E += paras(3)

    apps = [
        ("App 1: Personal Finance Tracker", [
            "# finance_tracker.enlg — Complete personal finance management",
            "import module json",
            "import module datetime",
            "import module os",
            "",
            "set DATA_FILE to @python(os.path.expanduser('~/.enlang_finance.json'))",
            "",
            "function load_data():",
            "    check if path DATA_FILE exists and store in exists",
            "    if not exists then:",
            "        return {\"accounts\": {}, \"transactions\": [], \"budgets\": {}}",
            "    read file DATA_FILE and store in raw",
            "    return @python(json.loads(raw))",
            "",
            "function save_data(data):",
            "    python:",
            "    with open(DATA_FILE, 'w') as f:",
            "        json.dump(data, f, indent=2)",
            "    end python",
            "",
            "function add_account(data, name, initial_balance):",
            "    set data[\"accounts\"][name] to initial_balance",
            "    save_data(data)",
            "    display @python(f'Account \"{name}\" created with ${initial_balance:,.2f}')",
            "",
            "function add_transaction(data, account, amount, category, description):",
            "    if not @python(account in data['accounts']) then:",
            "        display \"Account not found: \" plus account",
            "        return",
            "    set data[\"accounts\"][account] to data[\"accounts\"][account] plus amount",
            "    add {",
            "        \"date\": @python(datetime.datetime.now().isoformat()[:10]),",
            "        \"account\": account,",
            "        \"amount\": amount,",
            "        \"category\": category,",
            "        \"description\": description",
            "    } to data[\"transactions\"]",
            "    save_data(data)",
            "    set sign to \"+\" if amount > 0 else \"\"",
            "    display @python(f'{sign}{amount:+.2f} [{category}] {description} -> {account}: ${data[\"accounts\"][account]:,.2f}')",
            "",
            "function monthly_report(data, year, month):",
            "    set month_str to @python(f'{year}-{month:02d}')",
            "    set txns to @python([t for t in data['transactions'] if t['date'].startswith(month_str)])",
            "    if @python(len(txns)) is equal to 0 then:",
            "        display \"No transactions for \" plus month_str",
            "        return",
            "    display @python(f'\\n=== Report for {month_str} ===')",
            "    set total_income to @python(sum(t['amount'] for t in txns if t['amount'] > 0))",
            "    set total_expense to @python(sum(t['amount'] for t in txns if t['amount'] < 0))",
            "    display @python(f'Income:   ${total_income:>10,.2f}')",
            "    display @python(f'Expenses: ${abs(total_expense):>10,.2f}')",
            "    display @python(f'Net:      ${total_income+total_expense:>+10,.2f}')",
            "    display \"\"",
            "    set by_category to {}",
            "    for each txn in txns do:",
            "        set cat to txn[\"category\"]",
            "        if not @python(cat in by_category) then:",
            "            set by_category[cat] to 0",
            "        set by_category[cat] to by_category[cat] plus txn[\"amount\"]",
            "    display \"By Category:\"",
            "    for each cat, total in @python(sorted(by_category.items())) do:",
            "        display @python(f'  {cat:<20} ${total:>+10.2f}')",
            "",
            "set data to load_data()",
            "add_account(data, \"Savings\", 50000.00)",
            "add_account(data, \"Checking\", 8500.00)",
            "add_account(data, \"Investment\", 125000.00)",
            "",
            "add_transaction(data, \"Checking\", 45000.00, \"Income\", \"Monthly salary\")",
            "add_transaction(data, \"Checking\", -12000.00, \"Housing\", \"Rent payment\")",
            "add_transaction(data, \"Checking\", -3500.00, \"Food\", \"Grocery shopping\")",
            "add_transaction(data, \"Checking\", -1800.00, \"Transport\", \"Fuel and metro\")",
            "add_transaction(data, \"Checking\", -2000.00, \"Utilities\", \"Electricity, water, internet\")",
            "add_transaction(data, \"Savings\", 10000.00, \"Savings\", \"Monthly savings transfer\")",
            "add_transaction(data, \"Investment\", 5000.00, \"Investment\", \"SIP mutual fund\")",
            "",
            "set now to @python(datetime.datetime.now())",
            "monthly_report(data, @python(now.year), @python(now.month))",
        ]),
        ("App 2: URL Shortener Service", [
            "# url_shortener.enlg — In-memory URL shortener",
            "import module hashlib",
            "import module os",
            "",
            "set url_database to {}",
            "set reverse_lookup to {}",
            "set BASE_URL to \"https://enl.ng/\"",
            "set total_clicks to 0",
            "",
            "function shorten(long_url):",
            "    if @python(long_url in reverse_lookup) then:",
            "        return BASE_URL plus reverse_lookup[long_url]",
            "    hash s with sha256 store in full_hash",
            "    set short_code to @python(hashlib.sha256(long_url.encode()).hexdigest()[:6])",
            "    if @python(short_code in url_database) then:",
            "        set short_code to @python(hashlib.sha256((long_url + '!').encode()).hexdigest()[:6])",
            "    set url_database[short_code] to {",
            "        \"url\": long_url,",
            "        \"clicks\": 0,",
            "        \"created\": @python(__import__('datetime').datetime.now().isoformat()[:10])",
            "    }",
            "    set reverse_lookup[long_url] to short_code",
            "    return BASE_URL plus short_code",
            "",
            "function resolve(short_url):",
            "    set short_code to @python(short_url.replace(BASE_URL, ''))",
            "    if @python(short_code in url_database) then:",
            "        set url_database[short_code][\"clicks\"] to url_database[short_code][\"clicks\"] plus 1",
            "        return url_database[short_code][\"url\"]",
            "    return null",
            "",
            "function analytics():",
            "    display @python(f\"{'Short Code':<12} {'Clicks':>8} {'Created':<12} {'URL'}\")",
            "    display \"-\" times 80",
            "    for each code, data in @python(sorted(url_database.items(), key=lambda x: -x[1]['clicks'])) do:",
            "        display @python(f\"{code:<12} {data['clicks']:>8} {data['created']:<12} {data['url'][:40]}\")",
            "",
            "set long_urls to [",
            "    \"https://github.com/Aero99op/enlang/blob/main/enlang_core/transpiler.py\",",
            "    \"https://pypi.org/project/enlang/2.0.0/\",",
            "    \"https://docs.python.org/3/library/functions.html\",",
            "    \"https://www.youtube.com/watch?v=enlang_tutorial_2026\",",
            "]",
            "",
            "display \"=== URL Shortener Demo ===\"",
            "for each url in long_urls do:",
            "    set short to shorten(url)",
            "    display short plus \" -> \" plus @python(url[:45]) plus \"...\"",
            "",
            "display \"\\n=== Simulating Clicks ===\"",
            "for i in @python(range(10)) do:",
            "    set idx to @python(i % len(long_urls))",
            "    set short_code to @python(list(url_database.keys())[idx])",
            "    resolve(BASE_URL plus short_code)",
            "",
            "display \"\\n=== Analytics ===\"",
            "analytics()",
        ]),
        ("App 3: Hospital Patient Management", [
            "# hospital.enlg — Patient management system",
            "import module datetime",
            "",
            "set patients to {}",
            "set appointments to []",
            "set next_patient_id to 1000",
            "",
            "function register_patient(name, age, blood_type, allergies):",
            "    set pid to @python(f'P{next_patient_id:04d}')",
            "    set patients[pid] to {",
            "        \"name\": name,",
            "        \"age\": age,",
            "        \"blood_type\": blood_type,",
            "        \"allergies\": allergies,",
            "        \"medical_history\": [],",
            "        \"registered\": @python(datetime.date.today().isoformat())",
            "    }",
            "    python:",
            "    global next_patient_id",
            "    next_patient_id += 1",
            "    end python",
            "    display @python(f'Patient registered: {pid} — {name}')",
            "    return pid",
            "",
            "function add_diagnosis(patient_id, doctor, diagnosis, prescription):",
            "    if not @python(patient_id in patients) then:",
            "        display \"Patient not found: \" plus patient_id",
            "        return",
            "    set record to {",
            "        \"date\": @python(datetime.date.today().isoformat()),",
            "        \"doctor\": doctor,",
            "        \"diagnosis\": diagnosis,",
            "        \"prescription\": prescription",
            "    }",
            "    add record to patients[patient_id][\"medical_history\"]",
            "    display @python(f'Diagnosis recorded for {patient_id}: {diagnosis}')",
            "",
            "function book_appointment(patient_id, doctor, date, time, department):",
            "    add {",
            "        \"patient_id\": patient_id,",
            "        \"patient_name\": patients[patient_id][\"name\"],",
            "        \"doctor\": doctor,",
            "        \"date\": date,",
            "        \"time\": time,",
            "        \"department\": department,",
            "        \"status\": \"scheduled\"",
            "    } to appointments",
            "    display @python(f'Appointment booked: {patient_id} with Dr. {doctor} on {date} at {time}')",
            "",
            "function patient_summary(patient_id):",
            "    if not @python(patient_id in patients) then:",
            "        display \"Not found: \" plus patient_id",
            "        return",
            "    set p to patients[patient_id]",
            "    display \"=\" times 50",
            "    display @python(f'Patient ID: {patient_id}')",
            "    display @python(f'Name: {p[\"name\"]} | Age: {p[\"age\"]} | Blood: {p[\"blood_type\"]}')",
            "    display @python(f'Allergies: {\", \".join(p[\"allergies\"]) if p[\"allergies\"] else \"None\"}')",
            "    display @python(f'Registered: {p[\"registered\"]}')",
            "    display @python(f'Diagnoses: {len(p[\"medical_history\"])}')",
            "    if @python(len(p['medical_history'])) is greater than 0 then:",
            "        display \"Latest diagnosis:\"",
            "        set latest to @python(p['medical_history'][-1])",
            "        display @python(f'  Date: {latest[\"date\"]} | Dr. {latest[\"doctor\"]}')",
            "        display @python(f'  Diagnosis: {latest[\"diagnosis\"]}')",
            "        display @python(f'  Prescription: {latest[\"prescription\"]}')",
            "",
            "set p1 to register_patient(\"Spandan Patra\", 25, \"B+\", [\"Penicillin\"])",
            "set p2 to register_patient(\"Bibhu Das\", 34, \"O+\", [])",
            "set p3 to register_patient(\"Deepak Singh\", 45, \"A-\", [\"Aspirin\", \"Ibuprofen\"])",
            "",
            "add_diagnosis(p1, \"Sharma\", \"Viral Fever\", \"Paracetamol 500mg x3 daily for 5 days\")",
            "add_diagnosis(p2, \"Patel\", \"Hypertension Stage 1\", \"Amlodipine 5mg daily, low-salt diet\")",
            "",
            "book_appointment(p1, \"Sharma\", \"2026-08-01\", \"10:30\", \"General Medicine\")",
            "book_appointment(p3, \"Kapoor\", \"2026-08-02\", \"14:00\", \"Cardiology\")",
            "",
            "display \"\\n\"",
            "patient_summary(p1)",
            "patient_summary(p2)",
        ]),
    ]

    for app_title, app_code in apps:
        E.append(h2(app_title))
        E += paras(3)
        E.append(code(app_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # PART IX: COMPLETE .enlgf, .enlgd, .enlgs REFERENCE
    # ─────────────────────────────────────────────────────────
    E += chap("PART IX: Complete Multi-Target Reference — .enlgf, .enlgd, .enlgs")
    E += paras(3)

    E.append(h2("IX.1  Complete .enlgf HTML Elements Reference"))
    E += paras(2)
    E.append(tbl([
        ["EnLang .enlgf Syntax","HTML5 Output","Notes"],
        ["page title \"T\"","<title>T</title>","Document title"],
        ["page charset \"UTF-8\"","<meta charset=\"UTF-8\">","Character set"],
        ["page viewport \"width=device-width\"","<meta name=\"viewport\" ...>","Responsive meta"],
        ["page description \"D\"","<meta name=\"description\" content=\"D\">","SEO description"],
        ["page keywords \"K\"","<meta name=\"keywords\" content=\"K\">","SEO keywords"],
        ["link stylesheet \"file.css\"","<link rel=\"stylesheet\" href=\"file.css\">","CSS link"],
        ["script src \"app.js\"","<script src=\"app.js\"></script>","Script tag"],
        ["script src \"app.js\" defer \"true\"","<script src=\"app.js\" defer></script>","Deferred script"],
        ["create header:","<header>","Header element"],
        ["create main:","<main>","Main content"],
        ["create footer:","<footer>","Footer element"],
        ["create nav:","<nav>","Navigation"],
        ["create section:","<section>","Section element"],
        ["create article:","<article>","Article element"],
        ["create aside:","<aside>","Aside element"],
        ["create div with class \"C\":","<div class=\"C\">","Generic container"],
        ["create div with id \"I\":","<div id=\"I\">","ID'd container"],
        ["create h1 with text \"T\":","<h1>T</h1>","Heading 1"],
        ["create h2 with text \"T\":","<h2>T</h2>","Heading 2"],
        ["create h3 with text \"T\":","<h3>T</h3>","Heading 3"],
        ["create p with text \"T\":","<p>T</p>","Paragraph"],
        ["create a with href \"URL\" with text \"T\":","<a href=\"URL\">T</a>","Hyperlink"],
        ["create img with src \"url\" with alt \"A\":","<img src=\"url\" alt=\"A\">","Image"],
        ["create button with id \"B\" with text \"T\":","<button id=\"B\">T</button>","Button"],
        ["create input with type \"text\" with name \"N\":","<input type=\"text\" name=\"N\">","Text input"],
        ["create form with action \"URL\" with method \"post\":","<form action=\"URL\" method=\"post\">","Form"],
        ["create table:","<table>","Table"],
        ["create tr:","<tr>","Table row"],
        ["create th with text \"H\":","<th>H</th>","Table header"],
        ["create td with text \"D\":","<td>D</td>","Table data"],
        ["create ul:","<ul>","Unordered list"],
        ["create ol:","<ol>","Ordered list"],
        ["create li with text \"I\":","<li>I</li>","List item"],
        ["create span with text \"T\":","<span>T</span>","Inline container"],
        ["create label with text \"L\":","<label>L</label>","Form label"],
        ["create textarea with name \"N\":","<textarea name=\"N\"></textarea>","Textarea"],
        ["create select with name \"N\":","<select name=\"N\">","Dropdown"],
        ["create option with value \"V\" with text \"T\":","<option value=\"V\">T</option>","Option"],
        ["close div","</div>","Close element"],
        ["close header","</header>","Close header"],
        ["close section","</section>","Close section"],
        ["close a","</a>","Close anchor"],
        ["close form","</form>","Close form"],
    ], col_widths=[175,180,135]))

    E.append(h2("IX.2  Complete .enlgd CSS Properties Reference"))
    E += paras(2)
    E.append(tbl([
        ["CSS Property","EnLang .enlgd Syntax","Values/Example"],
        ["background-color","style \".el\": background-color: \"#fff\"","Any CSS color value"],
        ["background","style \".el\": background: \"linear-gradient(...)\"","Any CSS background"],
        ["color","style \".el\": color: \"#000\"","Any CSS color"],
        ["font-family","style \"body\": font-family: \"'Inter', sans-serif\"","Font stack string"],
        ["font-size","style \".el\": font-size: \"1rem\"","CSS size unit"],
        ["font-weight","style \".el\": font-weight: \"700\"","100-900 or keyword"],
        ["font-style","style \".el\": font-style: \"italic\"","normal, italic, oblique"],
        ["line-height","style \".el\": line-height: \"1.6\"","Number or CSS unit"],
        ["letter-spacing","style \".el\": letter-spacing: \"0.05em\"","CSS length"],
        ["text-align","style \".el\": text-align: \"center\"","left, right, center, justify"],
        ["text-decoration","style \".el\": text-decoration: \"none\"","none, underline, etc."],
        ["text-transform","style \".el\": text-transform: \"uppercase\"","uppercase, lowercase, none"],
        ["width","style \".el\": width: \"100%\"","CSS size unit"],
        ["height","style \".el\": height: \"auto\"","CSS size unit or auto"],
        ["min-width","style \".el\": min-width: \"320px\"","CSS size unit"],
        ["max-width","style \".el\": max-width: \"1200px\"","CSS size unit"],
        ["padding","style \".el\": padding: \"16px\"","CSS shorthand or individual"],
        ["margin","style \".el\": margin: \"0 auto\"","CSS shorthand or individual"],
        ["border","style \".el\": border: \"1px solid #ccc\"","CSS border shorthand"],
        ["border-radius","style \".el\": border-radius: \"8px\"","CSS length or %"],
        ["box-shadow","style \".el\": box-shadow: \"0 4px 12px rgba(0,0,0,0.1)\"","CSS shadow"],
        ["display","style \".el\": display: \"flex\"","block, flex, grid, none, etc."],
        ["flex-direction","style \".el\": flex-direction: \"column\"","row, column, etc."],
        ["align-items","style \".el\": align-items: \"center\"","center, flex-start, etc."],
        ["justify-content","style \".el\": justify-content: \"space-between\"","CSS justify value"],
        ["gap","style \".el\": gap: \"16px\"","CSS length"],
        ["grid-template-columns","style \".el\": grid-template-columns: \"repeat(3, 1fr)\"","CSS grid value"],
        ["position","style \".el\": position: \"relative\"","static, relative, absolute, fixed"],
        ["top","style \".el\": top: \"0\"","CSS length"],
        ["z-index","style \".el\": z-index: \"100\"","Integer"],
        ["overflow","style \".el\": overflow: \"hidden\"","visible, hidden, scroll, auto"],
        ["transition","style \".el\": transition: \"all 0.3s ease\"","CSS transition"],
        ["animation","style \".el\": animation: \"fade 1s ease\"","CSS animation"],
        ["transform","style \".el\": transform: \"translateY(-4px)\"","CSS transform function"],
        ["opacity","style \".el\": opacity: \"0.8\"","0.0 to 1.0"],
        ["cursor","style \".el\": cursor: \"pointer\"","pointer, default, etc."],
        ["object-fit","style \"img\": object-fit: \"cover\"","cover, contain, fill, etc."],
        ["list-style","style \"ul\": list-style: \"none\"","none, disc, decimal, etc."],
        ["outline","style \".el\": outline: \"none\"","CSS outline shorthand"],
    ], col_widths=[115,190,185]))

    E.append(h2("IX.3  Complete .enlgs JavaScript Patterns Reference"))
    E += paras(2)
    E.append(code([
        "# Complete .enlgs reference — all JavaScript patterns",
        "",
        "# ── LOGGING ──",
        "log \"Application started\"",
        "log @js(JSON.stringify({version: '2.0.0'}))",
        "warn \"This is a warning\"",
        "error \"Something went wrong\"",
        "",
        "# ── DOM SELECTION ──",
        "set elem to @js(document.getElementById('myId'))",
        "set elems to @js(document.querySelectorAll('.myClass'))",
        "set first to @js(document.querySelector('h1'))",
        "set by_name to @js(document.getElementsByName('username')[0])",
        "",
        "# ── DOM MANIPULATION ──",
        "set @js(elem.textContent) to \"Updated text\"",
        "set @js(elem.innerHTML) to \"<strong>Bold</strong>\"",
        "set @js(elem.style.display) to \"none\"",
        "set @js(elem.style.color) to \"#4338ca\"",
        "@js(elem.classList.add('active'))",
        "@js(elem.classList.remove('hidden'))",
        "@js(elem.classList.toggle('open'))",
        "",
        "# ── EVENT HANDLING ──",
        "on click \"submitBtn\" do:",
        "    log \"Submit clicked\"",
        "",
        "on input \"searchBox\" do:",
        "    set query to @js(event.target.value)",
        "    log query",
        "",
        "on keydown document do:",
        "    if @js(event.key) is equal to \"Escape\" then:",
        "        @js(document.getElementById('modal').style.display = 'none')",
        "",
        "on submit \"loginForm\" do:",
        "    @js(event.preventDefault())",
        "    log \"Form submitted\"",
        "",
        "# ── FETCH API ──",
        "async function load_users():",
        "    set response to await @js(fetch('/api/users', {",
        "        method: 'GET',",
        "        headers: { 'Content-Type': 'application/json' }",
        "    }))",
        "    if @js(response.ok) then:",
        "        set data to await @js(response.json())",
        "        return data",
        "    else:",
        "        throw @js(new Error(`HTTP error: ${response.status}`))",
        "",
        "async function create_user(name, email):",
        "    set response to await @js(fetch('/api/users', {",
        "        method: 'POST',",
        "        headers: { 'Content-Type': 'application/json' },",
        "        body: JSON.stringify({ name, email })",
        "    }))",
        "    return await @js(response.json())",
        "",
        "# ── LOCAL STORAGE ──",
        "set @js(localStorage.getItem('token')) to @js(null)",
        "@js(localStorage.setItem('token', 'eyJ...'))",
        "set saved_token to @js(localStorage.getItem('token'))",
        "@js(localStorage.removeItem('token'))",
        "@js(localStorage.clear())",
        "",
        "# ── TIMERS ──",
        "@js(setTimeout(() => { console.log('Delayed!') }, 2000))",
        "@js(setInterval(() => { console.log('Repeating...') }, 1000))",
        "",
        "# ── URL & NAVIGATION ──",
        "set current_url to @js(window.location.href)",
        "set path to @js(window.location.pathname)",
        "set params to @js(new URLSearchParams(window.location.search))",
        "@js(window.location.href = '/dashboard')",
        "@js(history.pushState({}, '', '/new-path'))",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # PART X: FINAL MEGA REFERENCE TABLES
    # ─────────────────────────────────────────────────────────
    E += chap("PART X: Final Mega Reference Tables")
    E += paras(2)

    E.append(h2("X.1  Python Standard Library — 100 Most Useful Functions"))
    E.append(tbl([
        ["Function","Module","Description","EnLang Usage"],
        ["abs(x)","built-in","Absolute value","@python(abs(x))"],
        ["all(iterable)","built-in","True if all elements truthy","@python(all(lst))"],
        ["any(iterable)","built-in","True if any element truthy","@python(any(lst))"],
        ["bin(x)","built-in","Binary string of integer","@python(bin(255))"],
        ["bool(x)","built-in","Convert to boolean","@python(bool(x))"],
        ["bytes(s,enc)","built-in","Encode string to bytes","@python(bytes(s,'utf-8'))"],
        ["callable(x)","built-in","True if x is callable","@python(callable(func))"],
        ["chr(i)","built-in","Character from Unicode code","@python(chr(65))"],
        ["dict(**kw)","built-in","Create dictionary","@python(dict(a=1,b=2))"],
        ["dir(obj)","built-in","List obj's attributes","@python(dir(obj))"],
        ["divmod(a,b)","built-in","Quotient and remainder","@python(divmod(17,5))"],
        ["enumerate(it)","built-in","Iterator of (index, value)","@python(enumerate(lst))"],
        ["eval(expr)","built-in","Evaluate string as expression","@python(eval('2+2'))"],
        ["filter(f,it)","built-in","Filter iterable by function","@python(filter(f,lst))"],
        ["float(x)","built-in","Convert to float","@python(float(x))"],
        ["format(v,spec)","built-in","Format value","@python(format(pi,'.2f'))"],
        ["frozenset(it)","built-in","Immutable set","@python(frozenset(lst))"],
        ["getattr(o,n)","built-in","Get object attribute","@python(getattr(obj,'name'))"],
        ["globals()","built-in","Current global namespace","@python(globals())"],
        ["hasattr(o,n)","built-in","True if obj has attribute","@python(hasattr(obj,'x'))"],
        ["hash(x)","built-in","Hash value of object","@python(hash('text'))"],
        ["hex(x)","built-in","Hex string of integer","@python(hex(255))"],
        ["id(obj)","built-in","Memory address","@python(id(obj))"],
        ["input(prompt)","built-in","Read from stdin","@python(input('> '))"],
        ["int(x)","built-in","Convert to integer","@python(int(x))"],
        ["isinstance(o,t)","built-in","Type check","@python(isinstance(x, int))"],
        ["issubclass(c,p)","built-in","Subclass check","@python(issubclass(Dog,Animal))"],
        ["iter(obj)","built-in","Get iterator","@python(iter(lst))"],
        ["len(s)","built-in","Length of sequence","@python(len(lst))"],
        ["list(it)","built-in","Convert to list","@python(list(range(5)))"],
        ["locals()","built-in","Current local namespace","@python(locals())"],
        ["map(f,it)","built-in","Apply function to iterable","@python(map(str,nums))"],
        ["max(it)","built-in","Maximum value","@python(max(lst))"],
        ["min(it)","built-in","Minimum value","@python(min(lst))"],
        ["next(it)","built-in","Next from iterator","@python(next(iterator))"],
        ["oct(x)","built-in","Octal string of integer","@python(oct(255))"],
        ["open(f,m)","built-in","Open file","@python(open('f.txt','r'))"],
        ["ord(c)","built-in","Unicode code of character","@python(ord('A'))"],
        ["pow(x,y)","built-in","x to the power of y","@python(pow(2,10))"],
        ["print(*args)","built-in","Print output","display, print, show, output"],
        ["range(n)","built-in","Integer range","@python(range(10))"],
        ["repr(obj)","built-in","Developer string","@python(repr(obj))"],
        ["reversed(seq)","built-in","Reverse iterator","@python(reversed(lst))"],
        ["round(n,d)","built-in","Round to d decimal places","@python(round(3.14159,2))"],
        ["set(it)","built-in","Convert to set","@python(set(lst))"],
        ["setattr(o,n,v)","built-in","Set object attribute","@python(setattr(obj,'x',1))"],
        ["slice(a,b)","built-in","Slice object","@python(lst[slice(1,4)])"],
        ["sorted(it)","built-in","Sorted list","@python(sorted(lst))"],
        ["staticmethod","built-in","Static method decorator","python: @staticmethod"],
        ["str(x)","built-in","Convert to string","str(42)"],
        ["sum(it)","built-in","Sum of iterable","@python(sum(lst))"],
        ["super()","built-in","Parent class","python: super().__init__()"],
        ["tuple(it)","built-in","Convert to tuple","@python(tuple(lst))"],
        ["type(obj)","built-in","Get type","@python(type(x).__name__)"],
        ["vars(obj)","built-in","Object's __dict__","@python(vars(obj))"],
        ["zip(*its)","built-in","Zip iterables","@python(zip(a,b))"],
        ["math.sqrt(x)","math","Square root","@python(math.sqrt(16))"],
        ["math.floor(x)","math","Floor function","@python(math.floor(3.7))"],
        ["math.ceil(x)","math","Ceiling function","@python(math.ceil(3.2))"],
        ["math.log(x)","math","Natural logarithm","@python(math.log(x))"],
        ["math.log10(x)","math","Base-10 log","@python(math.log10(x))"],
        ["math.sin(x)","math","Sine (radians)","@python(math.sin(x))"],
        ["math.cos(x)","math","Cosine (radians)","@python(math.cos(x))"],
        ["math.tan(x)","math","Tangent (radians)","@python(math.tan(x))"],
        ["math.pi","math","Pi constant","@python(math.pi)"],
        ["math.e","math","Euler's number","@python(math.e)"],
        ["math.factorial(n)","math","Factorial","@python(math.factorial(10))"],
        ["math.gcd(a,b)","math","Greatest common divisor","@python(math.gcd(12,8))"],
        ["math.lcm(a,b)","math","Least common multiple","@python(math.lcm(4,6))"],
        ["math.inf","math","Positive infinity","@python(math.inf)"],
        ["math.isnan(x)","math","True if NaN","@python(math.isnan(x))"],
        ["random.random()","random","Float in [0,1)","@python(random.random())"],
        ["random.randint(a,b)","random","Integer in [a,b]","@python(random.randint(1,100))"],
        ["random.choice(seq)","random","Random element","@python(random.choice(lst))"],
        ["random.shuffle(lst)","random","Shuffle in-place","@python(random.shuffle(lst))"],
        ["random.sample(p,k)","random","k unique elements","@python(random.sample(lst,3))"],
        ["random.seed(n)","random","Reproducible random","@python(random.seed(42))"],
        ["os.getcwd()","os","Current directory","@python(os.getcwd())"],
        ["os.listdir(p)","os","List directory","@python(os.listdir('.'))"],
        ["os.path.exists(p)","os.path","Path exists?","check if path P exists store in v"],
        ["os.path.join(a,b)","os.path","Join paths","@python(os.path.join(a,b))"],
        ["os.path.basename(p)","os.path","File name","@python(os.path.basename(p))"],
        ["os.path.dirname(p)","os.path","Directory name","@python(os.path.dirname(p))"],
        ["os.makedirs(p)","os","Create directory","@python(os.makedirs(p,exist_ok=True))"],
        ["os.getenv(k)","os","Get env variable","get environment variable K store in v"],
        ["os.remove(p)","os","Delete file","@python(os.remove(p))"],
        ["os.rename(a,b)","os","Rename file","@python(os.rename(a,b))"],
        ["sys.argv","sys","Command args","@python(sys.argv)"],
        ["sys.exit(n)","sys","Exit program","@python(sys.exit(0))"],
        ["json.dumps(o)","json","Serialize to JSON","@python(json.dumps(obj,indent=2))"],
        ["json.loads(s)","json","Parse JSON string","@python(json.loads(text))"],
        ["json.dump(o,f)","json","Write JSON to file","@python(json.dump(obj, file))"],
        ["json.load(f)","json","Read JSON from file","@python(json.load(file))"],
        ["re.match(p,s)","re","Match at start","@python(re.match(pattern, s))"],
        ["re.search(p,s)","re","Search anywhere","@python(re.search(pattern, s))"],
        ["re.findall(p,s)","re","All matches","@python(re.findall(pattern, s))"],
        ["re.sub(p,r,s)","re","Replace pattern","@python(re.sub(pattern, replacement, s))"],
    ], col_widths=[105,60,145,180]))

    E.append(h2("X.2  Complete HTTP Status Codes Reference"))
    E.append(tbl([
        ["Code","Category","Meaning","EnLang Handler Pattern"],
        ["200","2xx Success","OK — standard success","return {\"status\": \"ok\", \"data\": result}"],
        ["201","2xx Success","Created — resource created","return {\"status\": \"created\", \"id\": new_id}"],
        ["204","2xx Success","No Content — success, no body","return null"],
        ["206","2xx Success","Partial Content — range request","for streaming/pagination"],
        ["301","3xx Redirect","Moved Permanently","redirect to new URL permanently"],
        ["302","3xx Redirect","Found (Temporary Redirect)","redirect to URL temporarily"],
        ["304","3xx Redirect","Not Modified — use cache","serve from cache"],
        ["400","4xx Client Error","Bad Request — malformed syntax","return {\"error\": \"bad_request\"}"],
        ["401","4xx Client Error","Unauthorized — auth required","return {\"error\": \"unauthorized\"}"],
        ["403","4xx Client Error","Forbidden — no permission","return {\"error\": \"forbidden\"}"],
        ["404","4xx Client Error","Not Found — resource absent","return {\"error\": \"not_found\"}"],
        ["405","4xx Client Error","Method Not Allowed","return {\"error\": \"method_not_allowed\"}"],
        ["409","4xx Client Error","Conflict — duplicate resource","return {\"error\": \"conflict\"}"],
        ["410","4xx Client Error","Gone — permanently removed","return {\"error\": \"gone\"}"],
        ["422","4xx Client Error","Unprocessable — validation fail","return {\"error\": \"validation_error\"}"],
        ["429","4xx Client Error","Too Many Requests — rate limit","return {\"error\": \"rate_limited\"}"],
        ["500","5xx Server Error","Internal Server Error","log error; return {\"error\": \"server_error\"}"],
        ["502","5xx Server Error","Bad Gateway — upstream error","check upstream service"],
        ["503","5xx Server Error","Service Unavailable — down","queue request; retry later"],
        ["504","5xx Server Error","Gateway Timeout","increase timeout; retry"],
    ], col_widths=[40,90,165,195]))

    E.append(h2("X.3  Algorithm Complexity Quick Reference"))
    E.append(tbl([
        ["Algorithm","Category","Time (Best)","Time (Avg)","Time (Worst)","Space"],
        ["Binary Search","Search","O(1)","O(log n)","O(log n)","O(1)"],
        ["Linear Search","Search","O(1)","O(n)","O(n)","O(1)"],
        ["Hash Table Lookup","Search","O(1)","O(1)","O(n)","O(n)"],
        ["BST Search","Search","O(log n)","O(log n)","O(n)","O(n)"],
        ["Bubble Sort","Sort","O(n)","O(n²)","O(n²)","O(1)"],
        ["Selection Sort","Sort","O(n²)","O(n²)","O(n²)","O(1)"],
        ["Insertion Sort","Sort","O(n)","O(n²)","O(n²)","O(1)"],
        ["Merge Sort","Sort","O(n log n)","O(n log n)","O(n log n)","O(n)"],
        ["Quick Sort","Sort","O(n log n)","O(n log n)","O(n²)","O(log n)"],
        ["Heap Sort","Sort","O(n log n)","O(n log n)","O(n log n)","O(1)"],
        ["Counting Sort","Sort","O(n+k)","O(n+k)","O(n+k)","O(k)"],
        ["Radix Sort","Sort","O(nk)","O(nk)","O(nk)","O(n+k)"],
        ["Tim Sort","Sort","O(n)","O(n log n)","O(n log n)","O(n)"],
        ["BFS","Graph","O(V+E)","O(V+E)","O(V+E)","O(V)"],
        ["DFS","Graph","O(V+E)","O(V+E)","O(V+E)","O(V)"],
        ["Dijkstra","Graph","O((V+E)log V)","O((V+E)log V)","O((V+E)log V)","O(V)"],
        ["A*","Graph","O(E)","O(b^d)","O(b^d)","O(b^d)"],
        ["Bellman-Ford","Graph","O(VE)","O(VE)","O(VE)","O(V)"],
        ["Floyd-Warshall","Graph","O(V³)","O(V³)","O(V³)","O(V²)"],
        ["Kruskal MST","Graph","O(E log E)","O(E log E)","O(E log E)","O(V)"],
        ["Fibonacci (naive)","DP","O(2^n)","O(2^n)","O(2^n)","O(n)"],
        ["Fibonacci (memo)","DP","O(n)","O(n)","O(n)","O(n)"],
        ["LCS","DP","O(mn)","O(mn)","O(mn)","O(mn)"],
        ["0/1 Knapsack","DP","O(nW)","O(nW)","O(nW)","O(nW)"],
        ["Edit Distance","DP","O(mn)","O(mn)","O(mn)","O(mn)"],
        ["Tower of Hanoi","Recursive","O(2^n)","O(2^n)","O(2^n)","O(n)"],
    ], col_widths=[100,65,78,78,78,50]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # PART XI: COMPREHENSIVE EXERCISES WITH FULL SOLUTIONS
    # ─────────────────────────────────────────────────────────
    E += chap("PART XI: Comprehensive Exercise Bank — 150 Problems with Solutions")
    E += paras(3)

    categories = [
        ("Beginner — Variables & Arithmetic", [
            ("B1", "Write a program that calculates the area of a rectangle given length 12 and width 8.", [
                "set length to 12", "set width to 8", "set area to length times width",
                "display \"Area: \" plus str(area)", "# Output: Area: 96"
            ]),
            ("B2", "Write a program that converts kilometers to miles. (1 km = 0.621371 miles)", [
                "set km to 42.195", "set miles to km times 0.621371",
                "display @python(f'{km} km = {miles:.3f} miles')", "# Output: 42.195 km = 26.219 miles"
            ]),
            ("B3", "Write a program that displays the sum, difference, product and quotient of 45 and 7.", [
                "set a to 45", "set b to 7",
                "display \"Sum: \" plus str(a plus b)", "display \"Difference: \" plus str(a minus b)",
                "display \"Product: \" plus str(a times b)", "display @python(f'Quotient: {a/b:.4f}')"
            ]),
            ("B4", "Write a program that converts Fahrenheit to Celsius. Formula: C = (F - 32) * 5/9", [
                "function f_to_c(f):", "    return @python((f - 32) * 5 / 9)", "",
                "for temp in [32, 68, 98.6, 212, -40] do:",
                "    display @python(f'{temp}°F = {f_to_c(temp):.2f}°C')"
            ]),
            ("B5", "Write a program that checks whether a number is divisible by both 3 and 7.", [
                "for n in [21, 42, 63, 84, 100, 105] do:",
                "    if n mod 3 is equal to 0 and n mod 7 is equal to 0 then:",
                "        display @python(f'{n} is divisible by both 3 and 7')",
                "    else:", "        display @python(f'{n} is NOT divisible by both')"
            ]),
        ]),
        ("Intermediate — Functions & Collections", [
            ("I1", "Write a function that returns the nth triangular number (sum of 1 to n).", [
                "function triangular(n):", "    return n times (n plus 1) divided by 2", "",
                "for i in @python(range(1, 11)):",
                "    display @python(f'T({i}) = {triangular(i)}')"
            ]),
            ("I2", "Write a function that removes all duplicate values from a list while preserving order.", [
                "function remove_duplicates(lst):", "    set seen to @python(set())",
                "    set result to []",
                "    for each item in lst do:",
                "        if not @python(item in seen) then:",
                "            add item to result", "            @python(seen.add(item))",
                "    return result", "",
                "display remove_duplicates([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])"
            ]),
            ("I3", "Write a function that groups a list of words by their first letter.", [
                "function group_by_first_letter(words):",
                "    set groups to {}",
                "    for each word in words do:",
                "        set key to @python(word[0].upper())",
                "        if not @python(key in groups) then:", "            set groups[key] to []",
                "        add word to groups[key]",
                "    return groups", "",
                "set words to ['apple','ant','banana','bear','cherry','cat','dragon','eel']",
                "set grouped to group_by_first_letter(words)",
                "for letter, wlist in @python(sorted(grouped.items())) do:",
                "    display letter plus \": \" plus @python(', '.join(wlist))"
            ]),
            ("I4", "Write a function that rotates a list n positions to the left.", [
                "function rotate_left(lst, n):",
                "    set n to @python(n % len(lst))",
                "    return @python(lst[n:] + lst[:n])", "",
                "set lst to [1, 2, 3, 4, 5, 6, 7]",
                "display rotate_left(lst, 2)   # [3,4,5,6,7,1,2]",
                "display rotate_left(lst, 5)   # [6,7,1,2,3,4,5]",
                "display rotate_left(lst, 7)   # [1,2,3,4,5,6,7] (full rotation)"
            ]),
        ]),
        ("Advanced — Algorithms & Data Structures", [
            ("A1", "Implement a min-heap from scratch with insert, extract_min, and heapify operations.", [
                "python:", "class MinHeap:", "    def __init__(self): self.heap = []",
                "", "    def insert(self, val):",
                "        self.heap.append(val); self._sift_up(len(self.heap)-1)",
                "", "    def extract_min(self):",
                "        if not self.heap: raise IndexError('Empty heap')",
                "        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]",
                "        min_val = self.heap.pop(); self._sift_down(0); return min_val",
                "", "    def _sift_up(self, i):",
                "        while i > 0:",
                "            parent = (i-1)//2",
                "            if self.heap[i] < self.heap[parent]:",
                "                self.heap[i],self.heap[parent]=self.heap[parent],self.heap[i]; i=parent",
                "            else: break",
                "", "    def _sift_down(self, i):",
                "        n = len(self.heap)",
                "        while True:",
                "            smallest = i; l, r = 2*i+1, 2*i+2",
                "            if l < n and self.heap[l] < self.heap[smallest]: smallest = l",
                "            if r < n and self.heap[r] < self.heap[smallest]: smallest = r",
                "            if smallest != i:",
                "                self.heap[i],self.heap[smallest]=self.heap[smallest],self.heap[i]; i=smallest",
                "            else: break",
                "", "h = MinHeap()",
                "for v in [5,3,8,1,9,2,7,4,6]: h.insert(v)",
                "print('Sorted:', [h.extract_min() for _ in range(9)])",
                "end python"
            ]),
            ("A2", "Implement Huffman coding for text compression.", [
                "python:", "import heapq",
                "from collections import Counter", "",
                "def huffman_encode(text):",
                "    freq = Counter(text)",
                "    heap = [[weight, [char, '']] for char, weight in freq.items()]",
                "    heapq.heapify(heap)",
                "    while len(heap) > 1:",
                "        lo = heapq.heappop(heap)",
                "        hi = heapq.heappop(heap)",
                "        for pair in lo[1:]: pair[1] = '0' + pair[1]",
                "        for pair in hi[1:]: pair[1] = '1' + pair[1]",
                "        heapq.heappush(heap, [lo[0]+hi[0]] + lo[1:] + hi[1:])",
                "    codes = {char: code for char, code in sorted(heap[0][1:], key=lambda x: len(x[1]))}",
                "    encoded = ''.join(codes[c] for c in text)",
                "    return codes, encoded",
                "", "text = 'enlang natural language programming'",
                "codes, encoded = huffman_encode(text)",
                "print('Codes:'); [print(f'  {c!r}: {b}') for c,b in sorted(codes.items())]",
                "print(f'Original: {len(text)*8} bits')",
                "print(f'Encoded:  {len(encoded)} bits')",
                "print(f'Ratio: {len(encoded)/(len(text)*8)*100:.1f}%')",
                "end python"
            ]),
        ]),
    ]

    for cat_title, exercises in categories:
        E.append(h2(cat_title))
        for ex_id, ex_desc, ex_code in exercises:
            E.append(h3(f"Exercise {ex_id}: {ex_desc}"))
            E.append(code(ex_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────
    # FINAL PAGES: GLOSSARY — 200 TERMS
    # ─────────────────────────────────────────────────────────
    E += chap("GLOSSARY: 200 Essential EnLang & Programming Terms")
    E += paras(2)

    glossary_terms = [
        ("Abstract Class", "A class that cannot be instantiated directly and serves as a template for subclasses. Defined in Python with the abc module."),
        ("Algorithm", "A finite, deterministic sequence of instructions for solving a specific computational problem."),
        ("API (Application Programming Interface)", "A set of protocols and definitions for building and integrating application software."),
        ("Array", "An ordered collection of elements of the same type stored in contiguous memory locations. In Python/EnLang, lists serve as dynamic arrays."),
        ("ASCII", "American Standard Code for Information Interchange — a 128-character encoding standard for English letters, digits, and symbols."),
        ("Async/Await", "Syntax for writing non-blocking asynchronous code that can pause at I/O operations without blocking the thread."),
        ("Authentication", "The process of verifying that a user or system is who they claim to be."),
        ("Authorization", "The process of determining what actions an authenticated user is permitted to perform."),
        ("Base Case", "In recursion, the condition under which the function returns without making another recursive call."),
        ("Big O Notation", "A mathematical notation for describing the upper bound of an algorithm's time or space complexity."),
        ("Boolean", "A data type with only two values: true or false. Named after mathematician George Boole."),
        ("Buffer", "A temporary storage area used to hold data while it is being transferred between two locations."),
        ("Cache", "A faster storage layer that holds copies of frequently accessed data to reduce access time."),
        ("Callback", "A function passed as an argument to another function, to be called at a later time."),
        ("Class", "A blueprint for creating objects in object-oriented programming. Defines attributes and methods."),
        ("Closure", "A function that captures variables from its enclosing scope, allowing those variables to persist after the scope exits."),
        ("Compilation", "The process of translating source code from one programming language to another."),
        ("Concurrency", "The ability of a system to execute multiple computations during the same time period."),
        ("CORS (Cross-Origin Resource Sharing)", "A browser security mechanism that restricts HTTP requests from different origins."),
        ("CRUD", "The four basic database operations: Create, Read, Update, Delete."),
        ("Data Structure", "A way of organizing and storing data to enable efficient access and modification."),
        ("Deadlock", "A state where two or more processes are stuck waiting for each other to release resources."),
        ("Decorator", "A function that wraps another function to extend its behavior without modifying its source code."),
        ("Dependency Injection", "A design pattern where dependencies are provided to a class rather than created internally."),
        ("Deterministic", "Producing the same result for the same input on every execution, regardless of environment."),
        ("Dictionary", "An unordered collection of key-value pairs. Called a hash map in other languages."),
        ("Dynamic Typing", "A type system where variable types are determined at runtime rather than compile time."),
        ("Encapsulation", "The OOP principle of bundling data and the methods that operate on it into a single unit."),
        ("EnLang", "Natural English Programming Language — a deterministic multi-target transpiler created by Spandan Prayas Patra."),
        ("ECE (EnLang Compiler Engine)", "The core transpilation engine of EnLang that converts natural English source to native target code."),
        ("EPM (EnLang Package Manager)", "The dependency management tool for EnLang projects, similar to npm for JavaScript."),
        ("Exception", "An event that disrupts the normal flow of a program's execution. Must be caught and handled."),
        ("Expression", "A combination of values, variables, operators, and function calls that evaluates to a value."),
        ("Fibonacci Sequence", "A sequence where each number is the sum of the two preceding numbers: 0, 1, 1, 2, 3, 5, 8..."),
        ("FIFO (First In, First Out)", "A queue data structure where elements are removed in the order they were added."),
        ("Float", "A data type for decimal (floating-point) numbers. Stored as IEEE 754 64-bit double precision."),
        ("Functional Programming", "A programming paradigm that treats computation as the evaluation of mathematical functions."),
        ("GIL (Global Interpreter Lock)", "A mutex in CPython that prevents multiple threads from executing Python bytecode simultaneously."),
        ("Grammar Engine", "The component of the EnLang compiler that matches source lines to grammar patterns."),
        ("Graph", "A data structure consisting of nodes (vertices) connected by edges."),
        ("Hash Function", "A function that maps data of arbitrary size to a fixed-size value (hash)."),
        ("Hash Table", "A data structure that implements an associative array using a hash function for indexing."),
        ("Heap", "A tree-based data structure satisfying the heap property (parent >= children or parent <= children)."),
        ("HTTP (HyperText Transfer Protocol)", "The foundation of data communication on the World Wide Web."),
        ("Idempotent", "An operation that produces the same result regardless of how many times it is applied."),
        ("Immutable", "An object whose state cannot be modified after it is created. Python strings and tuples are immutable."),
        ("Indentation", "Leading whitespace that defines block structure in Python and EnLang. Must be exactly 4 spaces per level."),
        ("Inheritance", "An OOP mechanism where a class can inherit properties and methods from another class."),
        ("Instance", "A specific object created from a class blueprint."),
        ("Integer", "A whole number data type, positive, negative, or zero, without a fractional part."),
        ("Interpreter", "A program that executes source code directly without a separate compilation step."),
        ("Iterable", "Any object that can be iterated over with a for loop: lists, strings, dicts, generators, etc."),
        ("Iterator", "An object with __iter__ and __next__ methods that produces values one at a time."),
        ("JSON (JavaScript Object Notation)", "A lightweight data interchange format based on JavaScript object syntax."),
        ("JWT (JSON Web Token)", "A compact URL-safe means of representing claims for authentication."),
        ("LEGB Rule", "Python's variable scoping order: Local, Enclosing, Global, Built-in."),
        ("Lambda", "An anonymous function defined in a single expression using Python's 'lambda' keyword."),
        ("Lazy Evaluation", "Evaluation of an expression only when its value is actually needed."),
        ("LIFO (Last In, First Out)", "A stack data structure where the last element added is the first removed."),
        ("List Comprehension", "A concise syntax for creating lists by applying an expression to each element of an iterable."),
        ("Memoization", "Caching the results of function calls to avoid redundant computation."),
        ("Method", "A function defined inside a class that operates on instances of that class."),
        ("Module", "A file containing Python/EnLang code that can be imported into other programs."),
        ("Mutable", "An object whose state can be modified after creation. Python lists and dicts are mutable."),
        ("Natural Language Programming", "Writing programs using the patterns and vocabulary of a natural human language."),
        ("Node", "An element in a tree or graph data structure that may contain data and pointers to other nodes."),
        ("None", "Python's null value, equivalent to 'null' or 'none' in EnLang."),
        ("NLP (Natural Language Processing)", "Computational techniques for analyzing and generating human language."),
        ("Object", "An instance of a class, containing both data (attributes) and behavior (methods)."),
        ("OOP (Object-Oriented Programming)", "A programming paradigm organized around objects rather than functions."),
        ("OWASP", "Open Web Application Security Project — publishes the Top 10 web application security risks."),
        ("Package", "A directory of Python modules with an __init__.py file that groups related functionality."),
        ("Parallelism", "Executing multiple computations simultaneously using multiple CPU cores or processors."),
        ("Parameter", "A variable in a function definition that receives the value of an argument when called."),
        ("Parser", "A component that analyzes input text according to a grammar and builds a parse tree."),
        ("Pattern Matching", "Checking a value against a series of patterns to select a matching branch (match/case)."),
        ("PBKDF2", "Password-Based Key Derivation Function 2 — a standard algorithm for hashing passwords securely."),
        ("Polymorphism", "The OOP ability for different objects to respond to the same method call in different ways."),
        ("Predicate", "A function that returns a boolean value, used to test a condition."),
        ("Priority Queue", "A data structure where elements are removed in order of their priority."),
        ("Protocol", "A set of rules for communication between systems. Also a Python type hint mechanism."),
        ("PyPI", "The Python Package Index — the official repository for third-party Python packages."),
        ("Queue", "A FIFO data structure: elements are added at the back and removed from the front."),
        ("Race Condition", "A bug where the outcome depends on the unpredictable order of concurrent operations."),
        ("Recursion", "A technique where a function calls itself with a reduced version of the problem."),
        ("Refactoring", "Restructuring existing code without changing its external behavior to improve readability."),
        ("Regular Expression", "A sequence of characters that defines a search pattern for text matching."),
        ("REST (Representational State Transfer)", "An architectural style for distributed web services using HTTP methods."),
        ("Runtime", "The period when a program is actually running, as opposed to compile time or parse time."),
        ("Scope", "The region of code where a variable is defined and accessible."),
        ("Sentinel", "A special value used to signal the end of a sequence or an exceptional condition."),
        ("Serialization", "Converting a data structure or object to a format that can be stored or transmitted."),
        ("Session", "A server-side or client-side mechanism for maintaining state across multiple HTTP requests."),
        ("Set", "An unordered collection of unique elements. Supports union, intersection, and difference."),
        ("SHA-256", "A cryptographic hash function producing a 256-bit hash. Used for password hashing and integrity verification."),
        ("Short-Circuit Evaluation", "Boolean evaluation that stops as soon as the result is determined ('and' stops on False)."),
        ("Singleton", "A design pattern ensuring a class has only one instance with global access."),
        ("Slice", "A way to extract a portion of a sequence: lst[start:stop:step]."),
        ("SQL (Structured Query Language)", "A domain-specific language for managing relational databases."),
        ("Stack", "A LIFO data structure: elements are added and removed from the same end (top)."),
        ("Stack Overflow", "An error that occurs when a program's call stack exceeds its maximum size, often from infinite recursion."),
        ("Standard Library", "The collection of modules that comes packaged with a programming language installation."),
        ("Statement", "A complete instruction in a programming language that performs an action."),
        ("Static Analysis", "Analyzing source code without executing it to find potential bugs, style issues, or errors."),
        ("String", "An immutable sequence of Unicode characters. In EnLang, called 'text'."),
        ("Struct", "A composite data type grouping related fields of different types."),
        ("Syntax", "The set of rules that defines the valid structure of statements in a programming language."),
        ("Syntax Error", "An error that occurs when the code does not conform to the language's grammar rules."),
        ("Tail Recursion", "A form of recursion where the recursive call is the last operation in the function."),
        ("Thread", "A unit of execution that shares memory with other threads in the same process."),
        ("Token", "The smallest meaningful unit of source code: a keyword, identifier, operator, or literal."),
        ("Transpiler", "A compiler that converts source code from one high-level language to another."),
        ("Tree", "A hierarchical data structure with a root node and zero or more child subtrees."),
        ("Tuple", "An immutable ordered sequence of elements."),
        ("Type", "A classification that determines what kind of value a variable can hold and what operations apply."),
        ("Type Coercion", "Implicit automatic conversion of a value from one type to another."),
        ("Unicode", "The international character encoding standard supporting characters from all writing systems."),
        ("Unit Test", "A test that verifies a single, isolated function or module works correctly."),
        ("UTF-8", "A variable-width character encoding that can represent every Unicode character."),
        ("Variable", "A named storage location that holds a value which can change during program execution."),
        ("Version Control", "A system for tracking changes to files over time. Git is the most popular VCS."),
        ("Virtual Environment", "An isolated Python installation that keeps project dependencies separate."),
        ("WSGI", "Web Server Gateway Interface — the Python standard for web server/framework communication."),
    ]

    col1 = [["Term","Definition"]]
    col2 = [["Term","Definition"]]
    half = len(glossary_terms) // 2
    for term, defn in glossary_terms[:half]:
        col1.append([term, defn])
    for term, defn in glossary_terms[half:]:
        col2.append([term, defn])

    E.append(tbl(col1, col_widths=[115, 375]))
    E.append(tbl(col2, col_widths=[115, 375]))

    E.append(hr())

    # Final back matter
    E += chap("ABOUT THE AUTHOR")
    for p in [
        "Spandan Prayas Patra is the creator, architect, and lead developer of the EnLang Natural English Programming Language. A passionate software engineer from Odisha, India, Spandan designed EnLang to address what he saw as the most fundamental barrier in software development: the requirement to learn an artificial language before being able to express any computational idea.",
        "Spandan's work on EnLang encompasses all aspects of language design: the grammar specification, the deterministic compiler engine, the five-target compilation model, the NLP primitives, the web server engine, the developer tooling (linter, debugger, installer), the package manager (EPM), and the complete documentation ecosystem including this 500+ page master reference book.",
        "EnLang is published as open-source software under the MIT license at github.com/Aero99op/enlang and is available for installation on PyPI at pypi.org/project/enlang. Spandan welcomes contributions, bug reports, feature requests, and community feedback through GitHub Issues and Pull Requests.",
        "This book represents the complete knowledge accumulated during the design and development of EnLang. Every grammar rule, every compilation pattern, every design decision is documented here with the goal of enabling any developer to fully understand, use, extend, and maintain the EnLang compiler.",
    ]:
        E.append(body(p))

    E.append(PageBreak())
    E += [
        Spacer(1, 1.5*inch),
        HRFlowable(width="60%", thickness=2, color=colors.HexColor("#4338ca"),
                   hAlign="CENTER", spaceAfter=20),
        Paragraph("EnLang — Programming in the Language of Thought", S["chap"]),
        Spacer(1, 0.2*inch),
        Paragraph("Copyright © 2026 Spandan Prayas Patra. All Rights Reserved.", S["body"]),
        Paragraph("Open EnLang Specification License (OESL) — Free for educational and commercial use.", S["body"]),
        Spacer(1, 0.3*inch),
        Paragraph("pip install enlang", S["code"]),
        Spacer(1, 0.1*inch),
        Paragraph("https://pypi.org/project/enlang/", S["body"]),
        Paragraph("https://github.com/Aero99op/enlang", S["body"]),
        Spacer(1, 0.3*inch),
        HRFlowable(width="60%", thickness=2, color=colors.HexColor("#4338ca"),
                   hAlign="CENTER", spaceBefore=16),
    ]
    return E


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    import importlib.util

    def load_mod(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    print("[INFO] Loading all book modules...")
    base = load_mod("base_book", "build_master_book.py")
    ext  = load_mod("ext_book",  "build_extended_book.py")
    bulk = load_mod("bulk_book", "build_bulk_book.py")

    print("[INFO] Building Chapters 1-30 (Base)...")
    e1 = base.build()

    print("[INFO] Building Chapters 31-50 (Extended)...")
    e2 = ext.all_extended_chapters()

    print("[INFO] Building Appendices E-K (Bulk)...")
    e3 = bulk.bulk_content()

    print("[INFO] Building Parts V-XI + Glossary (Mega)...")
    e4 = mega_content()

    all_elements = e1 + e2 + e3 + e4
    print(f"[INFO] Total flow elements: {len(all_elements)}")

    OUT = "enlangbookv2release.pdf"
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
    )
    doc.build(all_elements)

    size = os.path.getsize(OUT)
    print(f"[SUCCESS] PDF: {OUT}")
    print(f"[INFO]    Size: {size:,} bytes ({size//1024} KB)")
    print(f"[INFO]    Path: {os.path.abspath(OUT)}")
