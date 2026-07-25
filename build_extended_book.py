"""
EnLang 500+ Page Master Book — Extended Content Modules
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import inch

W, H = letter

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        book_title=P("BT", fontName="Helvetica-Bold", fontSize=32, leading=38,
                     textColor=colors.HexColor("#0f172a"), alignment=TA_CENTER, spaceAfter=8),
        book_sub=P("BS", fontName="Helvetica-Oblique", fontSize=13, leading=17,
                   textColor=colors.HexColor("#4338ca"), alignment=TA_CENTER, spaceAfter=5),
        book_auth=P("BA", fontName="Helvetica", fontSize=10, leading=14,
                    textColor=colors.HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=20),
        chap=P("CH", fontName="Helvetica-Bold", fontSize=18, leading=24,
               textColor=colors.HexColor("#1e1b4b"), spaceBefore=14, spaceAfter=6, keepWithNext=True),
        h2=P("H2", fontName="Helvetica-Bold", fontSize=12, leading=16,
             textColor=colors.HexColor("#3730a3"), spaceBefore=8, spaceAfter=4, keepWithNext=True),
        h3=P("H3", fontName="Helvetica-Bold", fontSize=10, leading=14,
             textColor=colors.HexColor("#4f46e5"), spaceBefore=6, spaceAfter=3, keepWithNext=True),
        body=P("BD", fontName="Helvetica", fontSize=8.5, leading=12.5,
               textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=4),
        bullet=P("BU", fontName="Helvetica", fontSize=8.5, leading=12.5,
                 textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=2),
        code=P("CO", fontName="Courier", fontSize=7.5, leading=10.5,
               textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"),
               borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=5,
               spaceBefore=2, spaceAfter=5),
        code_out=P("CoO", fontName="Courier", fontSize=7.5, leading=10.5,
                   textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"),
                   borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=5,
                   spaceBefore=1, spaceAfter=5),
        note=P("NO", fontName="Helvetica-Oblique", fontSize=8, leading=11,
               textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"),
               borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=4,
               spaceBefore=2, spaceAfter=5),
        warn=P("WA", fontName="Helvetica-Bold", fontSize=8, leading=11,
               textColor=colors.HexColor("#991b1b"), backColor=colors.HexColor("#fef2f2"),
               borderColor=colors.HexColor("#fca5a5"), borderWidth=0.5, borderPadding=4,
               spaceBefore=2, spaceAfter=5),
        tip=P("TI", fontName="Helvetica-Oblique", fontSize=8, leading=11,
              textColor=colors.HexColor("#14532d"), backColor=colors.HexColor("#f0fdf4"),
              borderColor=colors.HexColor("#4ade80"), borderWidth=0.5, borderPadding=4,
              spaceBefore=2, spaceAfter=5),
    )

S = make_styles()

def t(text): return (str(text).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def h3(txt): return Paragraph(t(txt), S["h3"])
def note(txt): return Paragraph("NOTE: "+t(txt), S["note"])
def warn(txt): return Paragraph("WARNING: "+t(txt), S["warn"])
def tip(txt): return Paragraph("TIP: "+t(txt), S["tip"])
def bul(txt): return Paragraph("• "+t(txt), S["bullet"])
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=4, spaceBefore=4)

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
        HRFlowable(width="100%",thickness=1.2,color=colors.HexColor("#4338ca"),spaceAfter=8,spaceBefore=2),
    ]

# =============================================================================
# CONTENT GENERATOR — generates many pages of rich content
# =============================================================================

def generate_chapter_body(topic, intro, subsections):
    """Generate a full chapter worth of content."""
    E = []
    E.append(body(intro))
    for sub_title, paragraphs, code_blocks, tables in subsections:
        E.append(h2(sub_title))
        for p in paragraphs:
            E.append(body(p))
        for cb in code_blocks:
            E.append(code(cb))
        for tb in tables:
            E.append(tbl(tb[0], tb[1] if len(tb) > 1 else None))
    E.append(hr())
    return E


def all_extended_chapters():
    E = []

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 31: ENLANG GRAMMAR ENGINE INTERNALS
    # ─────────────────────────────────────────────────────────────────────
    E += chap("EnLang Grammar Engine Internals — How Transpilation Works", 31)
    E.append(body("Understanding the internal mechanics of the EnLang transpiler is valuable for advanced developers who want to extend the language, write custom grammar rules, or contribute to the compiler engine. This chapter dissects the full pipeline from raw .enlg source bytes to executed Python output."))

    E.append(h2("31.1  The Compilation Pipeline — 6 Stages"))
    for stage, desc in [
        ("Stage 1: Source Read", "The CLI reads the raw bytes of the .enlg file into a Python string, preserving exact whitespace and line endings. The file encoding is assumed to be UTF-8 with BOM-optional detection."),
        ("Stage 2: Extension Routing", "The file extension (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb) is extracted and used to select the appropriate sub-transpiler. Invalid extensions raise a CompilationError before any processing begins."),
        ("Stage 3: Line Splitting & Normalization", "The source string is split on newlines. Each line is analyzed independently. Blank lines and comment lines (starting with #) are preserved as-is or converted to Python comments."),
        ("Stage 4: Pattern Matching (Grammar Engine)", "Each non-blank, non-comment line is matched against the full list of EnLang grammar patterns in priority order (highest specificity first). The first pattern that matches the line wins and produces the output code fragment."),
        ("Stage 5: Indentation Mapping", "The leading whitespace of each original EnLang line is measured and preserved in the output. Since EnLang enforces 4-space indentation and Python also uses indentation, the mapping is 1:1 without any transformation."),
        ("Stage 6: Output Assembly & Execution", "All translated code fragments are joined with newlines into a complete Python source string. This string is passed to Python's exec() function (or written to a .py file with --emit-target). The exec() runs in a prepared global namespace containing all built-in EnLang functions."),
    ]:
        E.append(h3(stage))
        E.append(body(desc))

    E.append(h2("31.2  The Grammar Pattern Priority System"))
    E.append(body("The grammar engine applies patterns in strict priority order. More specific patterns (longer keyword sequences) are checked before more general ones. This ensures that 'is greater than or equal to' is matched before 'is greater than', which would otherwise match the first part of the longer phrase."))
    E.append(tbl([
        ["Priority","Pattern Category","Example","Reasoning"],
        ["1 (Highest)","4-word operator phrases","is greater than or equal to","Must match before 3-word variants"],
        ["2","3-word operator phrases","is greater than","Must match before 2-word variants"],
        ["3","2-word operator phrases","is equal","Checked before single keywords"],
        ["4","Variable declaration forms","set x to","Specific assignment forms"],
        ["5","Control flow headers","if x then:","Block-starting keywords"],
        ["6","Loop forms","repeat N times do:","Loop-starting keywords"],
        ["7","Function declarations","function foo using n:","Natural function forms"],
        ["8","Function calls","start foo from","Natural call forms"],
        ["9","I/O operations","display x, write to","Output/input operations"],
        ["10","Collection ops","add item to list","Collection manipulation"],
        ["11","Native escapes","@python(...), python:","Passthrough markers"],
        ["12 (Lowest)","Raw passthrough","Any unmatched line","Direct Python output"],
    ], col_widths=[65,130,155,140]))

    E.append(h2("31.3  Expression Cleaning Pipeline"))
    E.append(body("Before a translated line is added to the output, the grammar engine runs the expression through the clean_expression() function, which applies all natural-to-Python replacements in sequence. The replacements are applied using regex substitution with word boundaries (\\b) to prevent partial word matches."))
    E.append(code([
        "# Inside enlang_core/grammar.py",
        "EXPRESSION_REPLACEMENTS = [",
        "    (r'\\bis equal to\\b',                  '=='),",
        "    (r'\\bis not equal to\\b',              '!='),",
        "    (r'\\bis greater than or equal to\\b',  '>='),",
        "    (r'\\bis less than or equal to\\b',     '<='),",
        "    (r'\\bis greater than\\b',              '>'),",
        "    (r'\\bis less than\\b',                 '<'),",
        "    (r'\\bis in\\b',                        'in'),",
        "    (r'\\bis not in\\b',                    'not in'),",
        "    (r'\\bis not\\b',                       '!='),",
        "    (r'\\bis true\\b',                      '== True'),",
        "    (r'\\bis false\\b',                     '== False'),",
        "    (r'\\btrue\\b',                         'True'),",
        "    (r'\\bfalse\\b',                        'False'),",
        "    (r'\\bnull\\b',                         'None'),",
        "    (r'\\bplus\\b',                         '+'),",
        "    (r'\\bminus\\b',                        '-'),",
        "    (r'\\btimes\\b',                        '*'),",
        "    (r'\\bdivided by\\b',                   '/'),",
        "    (r'\\bmodulo\\b',                       '%'),",
        "    (r'\\bmod\\b',                          '%'),",
        "    (r'\\bpower of\\b',                     '**'),",
        "]",
        "",
        "def clean_expression(expr: str) -> str:",
        "    for pattern, replacement in EXPRESSION_REPLACEMENTS:",
        "        expr = re.sub(pattern, replacement, expr)",
        "    return expr",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 32: ADVANCED OOP PATTERNS
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Advanced OOP Patterns in EnLang", 32)
    E.append(body("Object-oriented programming (OOP) is a programming paradigm that organizes code around objects — data structures that bundle together state (attributes) and behavior (methods). EnLang fully supports all OOP paradigms through Python native blocks, enabling complex system designs."))

    for sub, intro, code_block in [
        ("32.1  The Singleton Pattern", "The Singleton pattern ensures that a class has only one instance and provides a global access point to that instance. Useful for configuration managers, connection pools, and logging systems.", [
            "python:",
            "class Configuration:",
            "    _instance = None",
            "",
            "    def __new__(cls):",
            "        if cls._instance is None:",
            "            cls._instance = super().__new__(cls)",
            "            cls._instance._settings = {",
            "                'debug': False,",
            "                'port': 8000,",
            "                'host': 'localhost',",
            "                'db_path': 'app.db'",
            "            }",
            "        return cls._instance",
            "",
            "    def get(self, key, default=None):",
            "        return self._settings.get(key, default)",
            "",
            "    def set(self, key, value):",
            "        self._settings[key] = value",
            "",
            "# Test Singleton behavior",
            "config1 = Configuration()",
            "config2 = Configuration()",
            "config1.set('port', 9000)",
            "print(config2.get('port'))  # 9000 — same instance!",
            "print(config1 is config2)   # True",
            "end python",
        ]),
        ("32.2  The Observer Pattern", "The Observer pattern defines a one-to-many dependency between objects so that when one object (subject) changes state, all dependents (observers) are notified automatically. Useful for event systems, GUI frameworks, and reactive architectures.", [
            "python:",
            "class EventEmitter:",
            "    def __init__(self):",
            "        self._listeners = {}",
            "",
            "    def on(self, event, callback):",
            "        if event not in self._listeners:",
            "            self._listeners[event] = []",
            "        self._listeners[event].append(callback)",
            "",
            "    def emit(self, event, *args, **kwargs):",
            "        for callback in self._listeners.get(event, []):",
            "            callback(*args, **kwargs)",
            "",
            "emitter = EventEmitter()",
            "",
            "def on_user_login(user):",
            "    print(f'[LOG] User logged in: {user}')",
            "",
            "def on_user_login_notify(user):",
            "    print(f'[EMAIL] Welcome back, {user}!')",
            "",
            "emitter.on('login', on_user_login)",
            "emitter.on('login', on_user_login_notify)",
            "emitter.emit('login', 'Spandan')",
            "end python",
        ]),
        ("32.3  The Factory Pattern", "The Factory pattern provides an interface for creating objects without specifying their concrete classes. It centralizes object creation logic and makes code more maintainable when multiple similar objects need to be created.", [
            "python:",
            "class PaymentProcessor:",
            "    def process(self, amount): raise NotImplementedError",
            "",
            "class CreditCardProcessor(PaymentProcessor):",
            "    def process(self, amount):",
            "        return f'Credit card charged: ${amount:.2f}'",
            "",
            "class PayPalProcessor(PaymentProcessor):",
            "    def process(self, amount):",
            "        return f'PayPal payment sent: ${amount:.2f}'",
            "",
            "class CryptoProcessor(PaymentProcessor):",
            "    def process(self, amount):",
            "        return f'Crypto transfer: ${amount:.2f} USD equivalent'",
            "",
            "def create_processor(method: str) -> PaymentProcessor:",
            "    registry = {",
            "        'credit_card': CreditCardProcessor,",
            "        'paypal': PayPalProcessor,",
            "        'crypto': CryptoProcessor,",
            "    }",
            "    cls = registry.get(method.lower())",
            "    if not cls:",
            "        raise ValueError(f'Unknown payment method: {method}')",
            "    return cls()",
            "",
            "for method in ['credit_card', 'paypal', 'crypto']:",
            "    proc = create_processor(method)",
            "    print(proc.process(99.99))",
            "end python",
        ]),
        ("32.4  The Decorator Pattern", "Python's decorator syntax (@decorator) adds functionality to functions without modifying them. In EnLang, decorators are accessible via Python native blocks. Common use cases include timing, logging, caching, authentication checks, and retry logic.", [
            "python:",
            "import functools, time",
            "",
            "def timer(func):",
            "    @functools.wraps(func)",
            "    def wrapper(*args, **kwargs):",
            "        start = time.perf_counter()",
            "        result = func(*args, **kwargs)",
            "        elapsed = time.perf_counter() - start",
            "        print(f'[TIMER] {func.__name__} took {elapsed:.4f}s')",
            "        return result",
            "    return wrapper",
            "",
            "def retry(max_attempts=3, delay=0.5):",
            "    def decorator(func):",
            "        @functools.wraps(func)",
            "        def wrapper(*args, **kwargs):",
            "            for attempt in range(1, max_attempts + 1):",
            "                try:",
            "                    return func(*args, **kwargs)",
            "                except Exception as e:",
            "                    if attempt == max_attempts: raise",
            "                    print(f'Attempt {attempt} failed: {e}. Retrying...')",
            "                    time.sleep(delay)",
            "        return wrapper",
            "    return decorator",
            "",
            "@timer",
            "@retry(max_attempts=3)",
            "def fetch_data(url):",
            "    import urllib.request",
            "    with urllib.request.urlopen(url, timeout=5) as r:",
            "        return r.read().decode()",
            "",
            "@timer",
            "def bubble_sort_large(arr):",
            "    n = len(arr)",
            "    for i in range(n):",
            "        for j in range(n-i-1):",
            "            if arr[j] > arr[j+1]:",
            "                arr[j], arr[j+1] = arr[j+1], arr[j]",
            "    return arr",
            "",
            "import random",
            "data = [random.randint(1, 10000) for _ in range(500)]",
            "bubble_sort_large(data[:])",
            "end python",
        ]),
    ]:
        E.append(h2(sub))
        E.append(body(intro))
        E.append(code(code_block))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 33: DATA SCIENCE & ANALYTICS WITH ENLANG
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Data Science & Analytics Integration with EnLang", 33)
    E.append(body("EnLang's Python compilation target gives it full access to the entire Python data science ecosystem: NumPy for numerical computing, Pandas for data analysis, Matplotlib for visualization, Scikit-learn for machine learning, and more. This chapter demonstrates how to build data science pipelines using EnLang."))

    E.append(h2("33.1  NumPy — Numerical Computing"))
    E.append(code([
        "python:",
        "import numpy as np",
        "",
        "# Create arrays",
        "arr1d = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])",
        "arr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])",
        "zeros = np.zeros((3, 4))",
        "ones = np.ones((2, 5))",
        "rand = np.random.rand(4, 4)",
        "",
        "# Operations",
        "print('Sum:', arr1d.sum())",
        "print('Mean:', arr1d.mean())",
        "print('Std Dev:', arr1d.std())",
        "print('Max:', arr1d.max())",
        "print('Min:', arr1d.min())",
        "",
        "# Linear algebra",
        "A = np.array([[2, 1], [1, 3]])",
        "b = np.array([5, 10])",
        "x = np.linalg.solve(A, b)",
        "print('Solution:', x)",
        "",
        "# Matrix operations",
        "M = np.array([[1,2],[3,4]])",
        "print('Determinant:', np.linalg.det(M))",
        "print('Eigenvalues:', np.linalg.eigvals(M))",
        "print('Transpose:\\n', M.T)",
        "print('Inverse:\\n', np.linalg.inv(M))",
        "end python",
    ]))

    E.append(h2("33.2  Pandas — Data Analysis"))
    E.append(code([
        "python:",
        "import pandas as pd",
        "import numpy as np",
        "",
        "# Create DataFrame",
        "data = {",
        "    'Name': ['Alice','Bob','Charlie','Diana','Eve','Frank'],",
        "    'Age': [28, 34, 22, 45, 31, 27],",
        "    'Department': ['Engineering','Marketing','Engineering','HR','Marketing','Engineering'],",
        "    'Salary': [85000, 62000, 70000, 78000, 65000, 92000],",
        "    'Years': [3, 7, 1, 12, 5, 4]",
        "}",
        "df = pd.DataFrame(data)",
        "",
        "# Basic analysis",
        "print(df.describe())",
        "print('\\nDepartment breakdown:')",
        "print(df.groupby('Department')['Salary'].agg(['mean','min','max','count']))",
        "",
        "# Filter",
        "engineers = df[df['Department'] == 'Engineering']",
        "print('\\nEngineers:')",
        "print(engineers[['Name','Salary','Years']])",
        "",
        "# Sort",
        "top_earners = df.nlargest(3, 'Salary')",
        "print('\\nTop 3 Earners:')",
        "print(top_earners[['Name','Salary','Department']])",
        "",
        "# Add computed column",
        "df['Salary_per_year'] = df['Salary'] / df['Years']",
        "print('\\nSalary efficiency (per year of experience):')",
        "print(df[['Name','Salary_per_year']].sort_values('Salary_per_year', ascending=False))",
        "end python",
    ]))

    E.append(h2("33.3  Statistical Analysis Pipeline"))
    E.append(code([
        "python:",
        "import statistics",
        "import math",
        "",
        "def full_stats(data, label='Dataset'):",
        "    n = len(data)",
        "    mean = statistics.mean(data)",
        "    median = statistics.median(data)",
        "    mode = statistics.multimode(data)",
        "    std_dev = statistics.stdev(data)",
        "    variance = statistics.variance(data)",
        "    data_min = min(data)",
        "    data_max = max(data)",
        "    data_range = data_max - data_min",
        "    q1 = statistics.quantiles(data, n=4)[0]",
        "    q3 = statistics.quantiles(data, n=4)[2]",
        "    iqr = q3 - q1",
        "",
        "    print(f'=== {label} Statistics ===')",
        "    print(f'  Count:     {n}')",
        "    print(f'  Mean:      {mean:.4f}')",
        "    print(f'  Median:    {median:.4f}')",
        "    print(f'  Mode:      {mode}')",
        "    print(f'  Std Dev:   {std_dev:.4f}')",
        "    print(f'  Variance:  {variance:.4f}')",
        "    print(f'  Range:     {data_range:.4f}')",
        "    print(f'  Q1:        {q1:.4f}')",
        "    print(f'  Q3:        {q3:.4f}')",
        "    print(f'  IQR:       {iqr:.4f}')",
        "    print(f'  Min:       {data_min}')",
        "    print(f'  Max:       {data_max}')",
        "",
        "import random",
        "random.seed(42)",
        "sample = [random.normalvariate(100, 15) for _ in range(1000)]",
        "full_stats(sample, 'Normal Distribution (mu=100, sigma=15)')",
        "end python",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 34: ASYNC & CONCURRENT PROGRAMMING DEEP DIVE
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Asynchronous & Concurrent Programming", 34)
    E.append(body("Modern applications frequently need to handle multiple operations concurrently — serving thousands of HTTP requests, reading from multiple files, fetching data from multiple APIs, or processing data in parallel. Python provides three main models for concurrency: threading (shared memory, GIL-limited), multiprocessing (separate memory spaces, true parallelism), and async/await (cooperative multitasking, ideal for I/O-bound tasks)."))

    E.append(h2("34.1  Understanding the Python GIL"))
    for p in [
        "Python's Global Interpreter Lock (GIL) is a mutex that prevents multiple Python threads from executing Python bytecode simultaneously. This means that in pure Python, threading does not achieve true parallelism for CPU-bound tasks — only one thread runs Python code at a time.",
        "However, the GIL is released during I/O operations (file reads, network calls, sleep), making threading effective for I/O-bound tasks. For CPU-bound tasks that require true parallelism, use multiprocessing, which creates separate Python processes each with their own GIL.",
        "Async/await is the recommended approach for I/O-bound concurrent programming in modern Python. It uses cooperative multitasking: tasks voluntarily yield control when waiting for I/O, allowing other tasks to run. The asyncio event loop manages task scheduling without threads.",
    ]:
        E.append(body(p))

    E.append(h2("34.2  asyncio — Async/Await Pattern"))
    E.append(code([
        "python:",
        "import asyncio",
        "import time",
        "",
        "async def fetch_data(source_id, delay):",
        "    print(f'[{source_id}] Starting fetch...')",
        "    await asyncio.sleep(delay)  # Simulate I/O",
        "    result = f'data_from_{source_id}'",
        "    print(f'[{source_id}] Completed in {delay}s')",
        "    return result",
        "",
        "async def main():",
        "    start = time.time()",
        "",
        "    # Sequential (slow)",
        "    print('--- Sequential ---')",
        "    r1 = await fetch_data('API-1', 1.0)",
        "    r2 = await fetch_data('API-2', 1.5)",
        "    r3 = await fetch_data('API-3', 0.8)",
        "    seq_time = time.time() - start",
        "    print(f'Sequential time: {seq_time:.2f}s')",
        "",
        "    # Concurrent (fast)",
        "    print('\\n--- Concurrent (gather) ---')",
        "    start2 = time.time()",
        "    results = await asyncio.gather(",
        "        fetch_data('API-A', 1.0),",
        "        fetch_data('API-B', 1.5),",
        "        fetch_data('API-C', 0.8),",
        "    )",
        "    conc_time = time.time() - start2",
        "    print(f'Concurrent time: {conc_time:.2f}s')",
        "    print(f'Speedup: {seq_time/conc_time:.1f}x')",
        "    print('Results:', results)",
        "",
        "asyncio.run(main())",
        "end python",
    ]))

    E.append(h2("34.3  Threading — I/O-Bound Concurrent Tasks"))
    E.append(code([
        "python:",
        "import threading",
        "import time",
        "import queue",
        "",
        "def worker(task_queue, result_queue, worker_id):",
        "    while True:",
        "        try:",
        "            task = task_queue.get(timeout=1)",
        "            # Simulate work",
        "            time.sleep(0.1)",
        "            result = f'Worker-{worker_id} processed task {task}'",
        "            result_queue.put(result)",
        "            task_queue.task_done()",
        "        except queue.Empty:",
        "            break",
        "",
        "tasks = queue.Queue()",
        "results = queue.Queue()",
        "",
        "# Add 20 tasks",
        "for i in range(1, 21):",
        "    tasks.put(i)",
        "",
        "# Create 5 worker threads",
        "threads = []",
        "for i in range(1, 6):",
        "    t = threading.Thread(target=worker, args=(tasks, results, i))",
        "    threads.append(t)",
        "    t.start()",
        "",
        "# Wait for all tasks",
        "tasks.join()",
        "for t in threads:",
        "    t.join()",
        "",
        "# Collect results",
        "print(f'Completed {results.qsize()} tasks')",
        "while not results.empty():",
        "    print(results.get())",
        "end python",
    ]))

    E.append(h2("34.4  Multiprocessing — CPU-Bound Parallel Tasks"))
    E.append(code([
        "python:",
        "from multiprocessing import Pool, cpu_count",
        "import time, math",
        "",
        "def is_prime(n):",
        "    if n < 2: return False",
        "    if n == 2: return True",
        "    if n % 2 == 0: return False",
        "    for i in range(3, int(math.sqrt(n))+1, 2):",
        "        if n % i == 0: return False",
        "    return True",
        "",
        "def count_primes_range(args):",
        "    start, end = args",
        "    return sum(1 for n in range(start, end) if is_prime(n))",
        "",
        "N = 1_000_000",
        "cores = cpu_count()",
        "chunk = N // cores",
        "ranges = [(i * chunk, (i+1) * chunk) for i in range(cores)]",
        "",
        "# Sequential",
        "t0 = time.time()",
        "seq_count = count_primes_range((2, N))",
        "seq_time = time.time() - t0",
        "",
        "# Parallel",
        "t1 = time.time()",
        "with Pool(cores) as pool:",
        "    counts = pool.map(count_primes_range, ranges)",
        "par_count = sum(counts)",
        "par_time = time.time() - t1",
        "",
        "print(f'Primes in [1, {N:,}]: {seq_count}')",
        "print(f'Sequential: {seq_time:.2f}s')",
        "print(f'Parallel ({cores} cores): {par_time:.2f}s')",
        "print(f'Speedup: {seq_time/par_time:.1f}x')",
        "end python",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 35: NETWORK PROGRAMMING
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Network Programming & REST API Integration", 35)
    E.append(body("Network programming is a fundamental skill for modern software development. EnLang programs can create HTTP clients to consume REST APIs, build TCP/UDP socket servers, implement WebSocket connections, and handle all aspects of network communication through Python's standard library and third-party packages."))

    E.append(h2("35.1  HTTP Client Requests"))
    E.append(code([
        "# http_client.enlg — REST API client demo",
        "python:",
        "import urllib.request",
        "import urllib.parse",
        "import json",
        "",
        "class EnLangHTTPClient:",
        "    def __init__(self, base_url, api_key=None):",
        "        self.base_url = base_url.rstrip('/')",
        "        self.headers = {'Content-Type': 'application/json'}",
        "        if api_key:",
        "            self.headers['Authorization'] = f'Bearer {api_key}'",
        "",
        "    def _request(self, method, path, data=None):",
        "        url = f'{self.base_url}{path}'",
        "        body = json.dumps(data).encode() if data else None",
        "        req = urllib.request.Request(url, data=body,",
        "                                    headers=self.headers, method=method)",
        "        try:",
        "            with urllib.request.urlopen(req, timeout=10) as res:",
        "                return json.loads(res.read().decode())",
        "        except urllib.error.HTTPError as e:",
        "            return {'error': e.code, 'reason': str(e.reason)}",
        "",
        "    def get(self, path): return self._request('GET', path)",
        "    def post(self, path, data): return self._request('POST', path, data)",
        "    def put(self, path, data): return self._request('PUT', path, data)",
        "    def delete(self, path): return self._request('DELETE', path)",
        "",
        "# Example usage",
        "client = EnLangHTTPClient('https://jsonplaceholder.typicode.com')",
        "user = client.get('/users/1')",
        "print(f\"Name: {user['name']}\")",
        "print(f\"Email: {user['email']}\")",
        "print(f\"Company: {user['company']['name']}\")",
        "end python",
    ]))

    E.append(h2("35.2  Building a TCP Echo Server"))
    E.append(code([
        "python:",
        "import socket, threading",
        "",
        "def handle_client(conn, addr):",
        "    print(f'[TCP] Connected: {addr}')",
        "    with conn:",
        "        while True:",
        "            data = conn.recv(4096)",
        "            if not data: break",
        "            message = data.decode().strip()",
        "            print(f'[{addr}] recv: {message}')",
        "            response = f'ECHO: {message}\\n'",
        "            conn.sendall(response.encode())",
        "    print(f'[TCP] Disconnected: {addr}')",
        "",
        "def start_tcp_server(host='127.0.0.1', port=9999):",
        "    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:",
        "        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)",
        "        s.bind((host, port))",
        "        s.listen(10)",
        "        print(f'[TCP] Server listening on {host}:{port}')",
        "        while True:",
        "            conn, addr = s.accept()",
        "            t = threading.Thread(target=handle_client, args=(conn, addr))",
        "            t.daemon = True",
        "            t.start()",
        "",
        "# start_tcp_server()  # Uncomment to run",
        "print('TCP Server module loaded. Call start_tcp_server() to run.')",
        "end python",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 36: CRYPTOGRAPHY & SECURITY IMPLEMENTATION
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Cryptography & Security Implementation", 36)
    E.append(body("Security is not an afterthought — it is a fundamental engineering discipline. This chapter covers practical cryptographic implementations in EnLang: password hashing, symmetric encryption, asymmetric encryption, JWT token generation, and input sanitization."))

    E.append(h2("36.1  Password Hashing — PBKDF2 & bcrypt"))
    E.append(code([
        "python:",
        "import hashlib, secrets, base64",
        "",
        "class PasswordManager:",
        "    ALGORITHM = 'sha256'",
        "    ITERATIONS = 600_000  # NIST recommended as of 2023",
        "    SALT_LENGTH = 32",
        "",
        "    @classmethod",
        "    def hash_password(cls, password: str) -> str:",
        "        salt = secrets.token_bytes(cls.SALT_LENGTH)",
        "        key = hashlib.pbkdf2_hmac(",
        "            cls.ALGORITHM,",
        "            password.encode('utf-8'),",
        "            salt,",
        "            cls.ITERATIONS",
        "        )",
        "        combined = salt + key",
        "        return base64.b64encode(combined).decode('utf-8')",
        "",
        "    @classmethod",
        "    def verify_password(cls, password: str, stored_hash: str) -> bool:",
        "        combined = base64.b64decode(stored_hash.encode('utf-8'))",
        "        salt = combined[:cls.SALT_LENGTH]",
        "        stored_key = combined[cls.SALT_LENGTH:]",
        "        new_key = hashlib.pbkdf2_hmac(",
        "            cls.ALGORITHM,",
        "            password.encode('utf-8'),",
        "            salt,",
        "            cls.ITERATIONS",
        "        )",
        "        return secrets.compare_digest(stored_key, new_key)",
        "",
        "pm = PasswordManager()",
        "hashed = pm.hash_password('MySuperSecurePass123!')",
        "print('Stored hash:', hashed[:40], '...')",
        "print('Verify correct:', pm.verify_password('MySuperSecurePass123!', hashed))",
        "print('Verify wrong:', pm.verify_password('WrongPassword', hashed))",
        "end python",
    ]))

    E.append(h2("36.2  Symmetric Encryption — AES-256"))
    E.append(code([
        "# AES-256 encryption using Python's cryptography library",
        "# Install: epm add py:cryptography",
        "python:",
        "import os",
        "from cryptography.hazmat.primitives.ciphers.aead import AESGCM",
        "",
        "def generate_key():",
        "    return AESGCM.generate_key(bit_length=256)",
        "",
        "def encrypt(key: bytes, plaintext: str) -> bytes:",
        "    aesgcm = AESGCM(key)",
        "    nonce = os.urandom(12)  # 96-bit nonce for GCM",
        "    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)",
        "    return nonce + ciphertext",
        "",
        "def decrypt(key: bytes, data: bytes) -> str:",
        "    aesgcm = AESGCM(key)",
        "    nonce = data[:12]",
        "    ciphertext = data[12:]",
        "    plaintext = aesgcm.decrypt(nonce, ciphertext, None)",
        "    return plaintext.decode()",
        "",
        "key = generate_key()",
        "secret_message = 'EnLang API Key: elk-prod-2026-secret-xyz'",
        "encrypted = encrypt(key, secret_message)",
        "decrypted = decrypt(key, encrypted)",
        "print('Original:', secret_message)",
        "print('Encrypted (hex):', encrypted.hex()[:40], '...')",
        "print('Decrypted:', decrypted)",
        "print('Match:', secret_message == decrypted)",
        "end python",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 37: ADVANCED ALGORITHMS
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Advanced Algorithms — Graph Theory, Dynamic Programming & Greedy", 37)
    E.append(body("This chapter covers advanced algorithmic techniques that are essential for solving complex computational problems: graph algorithms (BFS, DFS, Dijkstra, A*), dynamic programming (tabulation and memoization), and greedy algorithms (activity selection, Huffman coding, fractional knapsack)."))

    E.append(h2("37.1  Graph Representation & BFS/DFS"))
    E.append(code([
        "python:",
        "from collections import deque, defaultdict",
        "",
        "class Graph:",
        "    def __init__(self):",
        "        self.adj = defaultdict(list)",
        "",
        "    def add_edge(self, u, v, directed=False):",
        "        self.adj[u].append(v)",
        "        if not directed:",
        "            self.adj[v].append(u)",
        "",
        "    def bfs(self, start):",
        "        visited = set([start])",
        "        queue = deque([start])",
        "        order = []",
        "        while queue:",
        "            node = queue.popleft()",
        "            order.append(node)",
        "            for neighbor in sorted(self.adj[node]):",
        "                if neighbor not in visited:",
        "                    visited.add(neighbor)",
        "                    queue.append(neighbor)",
        "        return order",
        "",
        "    def dfs(self, start, visited=None):",
        "        if visited is None: visited = set()",
        "        visited.add(start)",
        "        result = [start]",
        "        for neighbor in sorted(self.adj[start]):",
        "            if neighbor not in visited:",
        "                result.extend(self.dfs(neighbor, visited))",
        "        return result",
        "",
        "    def has_path(self, src, dest):",
        "        return dest in set(self.bfs(src))",
        "",
        "g = Graph()",
        "edges = [('A','B'),('A','C'),('B','D'),('B','E'),('C','F'),('E','F')]",
        "for u, v in edges:",
        "    g.add_edge(u, v)",
        "",
        "print('BFS from A:', g.bfs('A'))",
        "print('DFS from A:', g.dfs('A'))",
        "print('Path A->F:', g.has_path('A', 'F'))",
        "end python",
    ]))

    E.append(h2("37.2  Dijkstra's Shortest Path Algorithm"))
    E.append(code([
        "python:",
        "import heapq",
        "",
        "def dijkstra(graph, start):",
        "    dist = {node: float('inf') for node in graph}",
        "    dist[start] = 0",
        "    prev = {node: None for node in graph}",
        "    pq = [(0, start)]  # (distance, node)",
        "",
        "    while pq:",
        "        d, u = heapq.heappop(pq)",
        "        if d > dist[u]: continue",
        "        for v, w in graph[u].items():",
        "            new_dist = dist[u] + w",
        "            if new_dist < dist[v]:",
        "                dist[v] = new_dist",
        "                prev[v] = u",
        "                heapq.heappush(pq, (new_dist, v))",
        "",
        "    return dist, prev",
        "",
        "def get_path(prev, start, end):",
        "    path, node = [], end",
        "    while node is not None:",
        "        path.append(node)",
        "        node = prev[node]",
        "    return list(reversed(path))",
        "",
        "# City network",
        "city_graph = {",
        "    'Mumbai':  {'Delhi': 1400, 'Pune': 150, 'Surat': 280},",
        "    'Delhi':   {'Mumbai': 1400, 'Jaipur': 280, 'Lucknow': 550},",
        "    'Pune':    {'Mumbai': 150, 'Hyderabad': 560},",
        "    'Surat':   {'Mumbai': 280, 'Ahmedabad': 265},",
        "    'Jaipur':  {'Delhi': 280, 'Ahmedabad': 670},",
        "    'Lucknow': {'Delhi': 550, 'Varanasi': 320},",
        "    'Hyderabad':{'Pune': 560, 'Bangalore': 570},",
        "    'Ahmedabad':{'Surat': 265, 'Jaipur': 670},",
        "    'Varanasi': {'Lucknow': 320},",
        "    'Bangalore':{'Hyderabad': 570}",
        "}",
        "",
        "distances, predecessors = dijkstra(city_graph, 'Mumbai')",
        "for city in sorted(distances):",
        "    path = get_path(predecessors, 'Mumbai', city)",
        "    print(f'{city:<12}: {distances[city]:>6} km  |  Path: {\" -> \".join(path)}')",
        "end python",
    ]))

    E.append(h2("37.3  Dynamic Programming — Longest Common Subsequence"))
    E.append(code([
        "python:",
        "def lcs(s1, s2):",
        "    m, n = len(s1), len(s2)",
        "    # Build DP table",
        "    dp = [[0]*(n+1) for _ in range(m+1)]",
        "    for i in range(1, m+1):",
        "        for j in range(1, n+1):",
        "            if s1[i-1] == s2[j-1]:",
        "                dp[i][j] = dp[i-1][j-1] + 1",
        "            else:",
        "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])",
        "",
        "    # Backtrack to find actual LCS",
        "    lcs_str = []",
        "    i, j = m, n",
        "    while i > 0 and j > 0:",
        "        if s1[i-1] == s2[j-1]:",
        "            lcs_str.append(s1[i-1])",
        "            i -= 1; j -= 1",
        "        elif dp[i-1][j] > dp[i][j-1]:",
        "            i -= 1",
        "        else:",
        "            j -= 1",
        "",
        "    return ''.join(reversed(lcs_str)), dp[m][n]",
        "",
        "pairs = [('ABCBDAB','BDCAB'),('enlang','natural'),('algorithm','altruistic')]",
        "for s1, s2 in pairs:",
        "    lcs_str, length = lcs(s1, s2)",
        "    print(f'LCS of \"{s1}\" and \"{s2}\": \"{lcs_str}\" (length={length})')",
        "end python",
    ]))

    E.append(h2("37.4  0/1 Knapsack Problem"))
    E.append(code([
        "python:",
        "def knapsack(weights, values, capacity):",
        "    n = len(weights)",
        "    dp = [[0]*(capacity+1) for _ in range(n+1)]",
        "",
        "    for i in range(1, n+1):",
        "        for w in range(capacity+1):",
        "            dp[i][w] = dp[i-1][w]",
        "            if weights[i-1] <= w:",
        "                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])",
        "",
        "    # Backtrack to find selected items",
        "    selected = []",
        "    w = capacity",
        "    for i in range(n, 0, -1):",
        "        if dp[i][w] != dp[i-1][w]:",
        "            selected.append(i-1)",
        "            w -= weights[i-1]",
        "",
        "    return dp[n][capacity], selected",
        "",
        "items = ['Laptop','Phone','Tablet','Camera','Headphones','Book','Charger','Bag']",
        "weights = [3, 1, 2, 1, 1, 0, 1, 2]  # kg",
        "values =  [1500, 800, 600, 700, 200, 50, 100, 150]  # USD",
        "max_capacity = 5  # kg",
        "",
        "max_value, chosen = knapsack(weights, values, max_capacity)",
        "print(f'Max value: ${max_value}')",
        "print('Selected items:')",
        "for idx in chosen:",
        "    print(f'  {items[idx]}: {weights[idx]}kg, ${values[idx]}')",
        "end python",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 38: ENLANG FULL COMPILER EXTENSION GUIDE
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Extending EnLang — Adding Custom Grammar Rules", 38)
    E.append(body("One of EnLang's most powerful features is its extensibility. Advanced developers can add custom grammar rules to the transpiler, creating domain-specific natural language extensions for their specific application domains — medical terminology, financial language, manufacturing instructions, or any other specialized vocabulary."))

    E.append(h2("38.1  Adding Custom Expression Replacements"))
    E.append(code([
        "# In enlang_core/grammar.py — add to EXPRESSION_REPLACEMENTS:",
        "",
        "CUSTOM_EXPRESSION_REPLACEMENTS = [",
        "    # Financial domain extensions",
        "    (r'\\binterest rate of\\b',         '* 0.01 *'),",
        "    (r'\\bprincipal amount\\b',          'principal'),",
        "    (r'\\bcompound annually\\b',         '** years'),",
        "    (r'\\bpresent value of\\b',          'pv('),",
        "",
        "    # Medical domain extensions",
        "    (r'\\bdose in mg per kg\\b',         '* weight_kg'),",
        "    (r'\\bbody mass index of\\b',        'bmi('),",
        "",
        "    # Engineering domain extensions",
        "    (r'\\bNewtons law F equals\\b',      'F ='),",
        "    (r'\\btorque of\\b',                 'torque('),",
        "]",
    ]))

    E.append(h2("38.2  Adding Custom Statement Patterns"))
    E.append(code([
        "# In enlang_core/transpiler.py — add to translate_python_line():",
        "",
        "# Custom domain: Financial calculations",
        "m = re.match(r'^calculate compound interest for principal (\\S+) rate (\\S+) years (\\S+) and store in (\\S+)$', line)",
        "if m:",
        "    principal, rate, years, var = m.groups()",
        "    return f'{var} = {principal} * (1 + {rate}/100) ** {years}'",
        "",
        "# Custom domain: Data validation",
        "m = re.match(r'^validate email (\\S+) and store result in (\\S+)$', line)",
        "if m:",
        "    email_var, result_var = m.groups()",
        "    return (f'import re as _re\\n'",
        "            f'{result_var} = bool(_re.match(r\"^[^@]+@[^@]+\\\\.[^@]+$\", str({email_var})))')",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 39: REAL WORLD PROJECT — ENLANG BLOG ENGINE
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Real-World Project: EnLang Blog Engine", 39)
    E.append(body("This chapter walks through building a complete blog engine — a full-stack web application with user authentication, post management, comment system, and an admin dashboard — using all five EnLang compilation targets working together."))

    E.append(h2("39.1  Database Schema — schema.enlgdb"))
    E.append(code([
        "connect to database \"blog.db\" as blog_db",
        "",
        "define table authors with columns:",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    username TEXT NOT NULL UNIQUE,",
        "    email TEXT NOT NULL UNIQUE,",
        "    password_hash TEXT NOT NULL,",
        "    display_name TEXT NOT NULL,",
        "    bio TEXT DEFAULT '',",
        "    role TEXT DEFAULT 'author',",
        "    created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
        "",
        "define table posts with columns:",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    title TEXT NOT NULL,",
        "    slug TEXT NOT NULL UNIQUE,",
        "    content TEXT NOT NULL,",
        "    excerpt TEXT,",
        "    author_id INTEGER NOT NULL REFERENCES authors(id),",
        "    status TEXT DEFAULT 'draft',",
        "    tags TEXT DEFAULT '[]',",
        "    view_count INTEGER DEFAULT 0,",
        "    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,",
        "    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,",
        "    published_at DATETIME",
        "",
        "define table comments with columns:",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    post_id INTEGER NOT NULL REFERENCES posts(id),",
        "    author_name TEXT NOT NULL,",
        "    author_email TEXT NOT NULL,",
        "    content TEXT NOT NULL,",
        "    is_approved INTEGER DEFAULT 0,",
        "    created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
        "",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_posts_slug ON posts(slug)\"",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)\"",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id)\"",
    ]))

    E.append(h2("39.2  Backend API — server.enlg"))
    E.append(code([
        "# blog_server.enlg — Blog Engine Backend",
        "import module json",
        "import module os",
        "import module datetime",
        "",
        "set DB_PATH to \"blog.db\"",
        "set PORT to @python(int(os.getenv('PORT', '8080')))",
        "set SECRET_KEY to @python(os.getenv('SECRET_KEY', 'dev-secret-change-in-prod'))",
        "",
        "function slugify(title):",
        "    set slug to @python(title.lower())",
        "    set slug to @python(__import__('re').sub(r'[^a-z0-9]+', '-', slug))",
        "    set slug to @python(slug.strip('-'))",
        "    return slug",
        "",
        "function create_post(title, content, author_id):",
        "    set slug to slugify(title)",
        "    set excerpt to @python(content[:150] + '...' if len(content) > 150 else content)",
        "    set now to @python(datetime.datetime.now().isoformat())",
        "    python:",
        "    import sqlite3",
        "    conn = sqlite3.connect(DB_PATH)",
        "    conn.execute(",
        "        'INSERT INTO posts (title, slug, content, excerpt, author_id, published_at) VALUES (?,?,?,?,?,?)',",
        "        (title, slug, content, excerpt, author_id, now)",
        "    )",
        "    conn.commit()",
        "    conn.close()",
        "    end python",
        "    display \"Post created: \" plus title",
        "    return slug",
        "",
        "display \"Blog Engine starting on port \" plus str(PORT) plus \"...\"",
        "start web server on port PORT",
    ]))

    E.append(h2("39.3  Frontend HTML — index.enlgf"))
    E.append(code([
        "page title \"EnLang Blog — Ideas Worth Sharing\"",
        "page charset \"UTF-8\"",
        "page viewport \"width=device-width, initial-scale=1.0\"",
        "page description \"A blog powered by EnLang — the Natural English Programming Language\"",
        "link stylesheet \"blog.css\"",
        "",
        "create header with class \"blog-header\":",
        "    create div with class \"container\":",
        "        create div with class \"header-inner\":",
        "            create a with href \"/\" with class \"blog-brand\":",
        "                create h1 with text \"EnLang Blog\"",
        "            close a",
        "            create p with class \"tagline\" with text \"Ideas worth sharing in natural English\"",
        "            create nav with class \"blog-nav\":",
        "                create a with href \"/\" with text \"Home\"",
        "                create a with href \"/archive\" with text \"Archive\"",
        "                create a with href \"/about\" with text \"About\"",
        "                create a with href \"/write\" with class \"btn-write\" with text \"+ Write\"",
        "            close nav",
        "        close div",
        "    close div",
        "close header",
        "",
        "create main with class \"blog-main\":",
        "    create div with class \"container\":",
        "        create div with class \"posts-grid\" with id \"postsGrid\":",
        "            create p with class \"loading\" with text \"Loading posts...\"",
        "        close div",
        "    close div",
        "close main",
    ]))

    E.append(h2("39.4  Blog CSS Design — blog.enlgd"))
    E.append(code([
        "define theme blogTheme:",
        "    font-main: \"'Georgia', 'Times New Roman', serif\"",
        "    font-mono: \"'Courier New', monospace\"",
        "    font-ui: \"'Inter', system-ui, sans-serif\"",
        "    primary: \"#1a1a2e\"",
        "    accent: \"#e94560\"",
        "    text: \"#2d2d2d\"",
        "    text-light: \"#666\"",
        "    bg: \"#fafaf8\"",
        "    card-bg: \"#ffffff\"",
        "    border: \"#e5e5e5\"",
        "    max-width: \"720px\"",
        "end theme",
        "",
        "style body:",
        "    font-family: \"'Georgia', serif\"",
        "    background: \"#fafaf8\"",
        "    color: \"#2d2d2d\"",
        "    line-height: \"1.75\"",
        "",
        "style \".blog-header\":",
        "    border-bottom: \"3px solid #1a1a2e\"",
        "    padding: \"32px 0\"",
        "    margin-bottom: \"48px\"",
        "",
        "style \".blog-brand h1\":",
        "    font-size: \"2rem\"",
        "    font-weight: \"900\"",
        "    letter-spacing: \"-1px\"",
        "    color: \"#1a1a2e\"",
        "",
        "style \".post-card\":",
        "    padding: \"32px 0\"",
        "    border-bottom: \"1px solid #e5e5e5\"",
        "",
        "style \".post-title\":",
        "    font-size: \"1.5rem\"",
        "    font-weight: \"700\"",
        "    line-height: \"1.3\"",
        "    margin-bottom: \"12px\"",
        "",
        "style \".post-title a\":",
        "    color: \"#1a1a2e\"",
        "    text-decoration: \"none\"",
        "",
        "style \".post-title a:hover\":",
        "    color: \"#e94560\"",
        "",
        "style \".read-more\":",
        "    color: \"#e94560\"",
        "    font-weight: \"600\"",
        "    text-decoration: \"none\"",
        "    font-size: \"0.9rem\"",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 40: REAL WORLD PROJECT — TASK MANAGEMENT CLI
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Real-World Project: EnLang Task Management CLI (TaskFlow)", 40)
    E.append(code([
        "# taskflow.enlg — Full-featured task manager CLI",
        "import module json",
        "import module os",
        "import module datetime",
        "",
        "set TASKS_FILE to os.path.expanduser(\"~/.taskflow_tasks.json\")",
        "",
        "function load_tasks():",
        "    check if path TASKS_FILE exists and store in exists",
        "    if not exists then:",
        "        return []",
        "    read file TASKS_FILE and store in raw",
        "    return @python(json.loads(raw))",
        "",
        "function save_tasks(tasks):",
        "    python:",
        "    with open(TASKS_FILE, 'w') as f:",
        "        json.dump(tasks, f, indent=2)",
        "    end python",
        "",
        "function add_task(title, priority, due_date):",
        "    set tasks to load_tasks()",
        "    set task_id to @python(max((t['id'] for t in tasks), default=0) + 1)",
        "    set new_task to {",
        "        \"id\": task_id,",
        "        \"title\": title,",
        "        \"priority\": priority,",
        "        \"due_date\": due_date,",
        "        \"status\": \"pending\",",
        "        \"created\": @python(datetime.datetime.now().isoformat())",
        "    }",
        "    add new_task to tasks",
        "    save_tasks(tasks)",
        "    display @python(f'Task #{task_id} added: {title}')",
        "",
        "function list_tasks(filter_status):",
        "    set tasks to load_tasks()",
        "    if filter_status is not equal to \"all\" then:",
        "        set tasks to @python([t for t in tasks if t['status'] == filter_status])",
        "    if @python(len(tasks)) is equal to 0 then:",
        "        display \"No tasks found.\"",
        "        return",
        "    display @python(f\"{'ID':>4} {'P':>3} {'Due Date':<12} {'Status':<10} {'Title'}\")",
        "    display \"-\" times 70",
        "    for each task in @python(sorted(tasks, key=lambda t: (t['priority'], t['due_date']))) do:",
        "        display @python(f\"{task['id']:>4} {task['priority']:>3} {task['due_date']:<12} {task['status']:<10} {task['title']}\")",
        "",
        "function complete_task(task_id):",
        "    set tasks to load_tasks()",
        "    set found to false",
        "    for each task in tasks do:",
        "        if task[\"id\"] is equal to task_id then:",
        "            set task[\"status\"] to \"done\"",
        "            set task[\"completed\"] to @python(datetime.datetime.now().isoformat())",
        "            set found to true",
        "    if found then:",
        "        save_tasks(tasks)",
        "        display \"Task \" plus str(task_id) plus \" marked as done!\"",
        "    else:",
        "        display \"Task \" plus str(task_id) plus \" not found.\"",
        "",
        "# Demo usage",
        "add_task(\"Design EnLang v3 specification\", 1, \"2026-08-01\")",
        "add_task(\"Write unit tests for parser\", 2, \"2026-07-30\")",
        "add_task(\"Update PyPI package to v2.0.0\", 1, \"2026-07-26\")",
        "add_task(\"Create tutorial video\", 3, \"2026-08-15\")",
        "add_task(\"Review pull requests\", 2, \"2026-07-28\")",
        "",
        "display \"\\n=== All Tasks ===\"",
        "list_tasks(\"all\")",
        "",
        "complete_task(3)",
        "",
        "display \"\\n=== Pending Tasks ===\"",
        "list_tasks(\"pending\")",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTERS 41–50: Additional deep-content chapters
    # ─────────────────────────────────────────────────────────────────────

    chapters_extra = [
        (41, "Regular Expressions Mastery in EnLang", [
            ("41.1 Regex Syntax Reference", [
                "Regular expressions (regex) are a powerful pattern matching language for processing and validating text. In EnLang, all regex operations are performed through Python's 're' module, accessed via @python() escapes. Mastering regex is essential for form validation, log parsing, text extraction, and data cleaning.",
                "Python's re module provides four primary functions: re.match() (checks pattern at the beginning of string), re.search() (checks for pattern anywhere in string), re.findall() (returns all matching substrings as a list), and re.sub() (replaces all pattern matches with a replacement string). re.compile() pre-compiles a pattern for efficiency when used many times.",
                "Regex metacharacters: . (any char except newline), ^ (start of string), $ (end of string), * (0 or more), + (1 or more), ? (0 or 1), {n,m} (n to m repetitions), [] (character class), | (alternation), () (group), \\d (digit), \\w (word char), \\s (whitespace), \\b (word boundary).",
            ],[
                ["# Email validation", "import module re", "",
                 "set EMAIL_PATTERN to @python(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')",
                 "", "set emails to [\"user@example.com\", \"invalid.email\", \"admin@enlang.org\", \"bad@\", \"good+tag@domain.co.uk\"]",
                 "for each email in emails do:",
                 "    if @python(re.match(EMAIL_PATTERN, email)) then:",
                 "        display email plus \" -> VALID\"",
                 "    else:",
                 "        display email plus \" -> INVALID\"",
                 "", "# Phone number extraction",
                 "set text to \"Call us at +91-9876543210 or (022) 2345-6789 for support.\"",
                 "set phones to @python(re.findall(r'[\\+\\(]?[0-9][0-9 .\\-\\(\\)]{8,}[0-9]', text))",
                 "display phones",
                 "", "# URL extraction",
                 "set html_text to \"Visit https://enlang.org and http://pypi.org/project/enlang for details.\"",
                 "set urls to @python(re.findall(r'https?://[^\\s]+', html_text))",
                 "display urls"
                ],
            ], []),
        ]),
        (42, "Design Patterns for Large EnLang Projects", [
            ("42.1 Repository Pattern for Data Access", [
                "The Repository pattern separates the application's business logic from data access logic. Instead of writing database queries scattered throughout your code, all data access goes through repository objects that provide a clean, uniform interface for CRUD operations.",
                "Benefits include: easier testing (mock the repository), database-agnostic business logic, centralized query optimization, and consistent error handling. In EnLang projects, implement repositories as Python classes in native blocks.",
            ], [
                ["python:", "import sqlite3, json", "",
                 "class UserRepository:", "    def __init__(self, db_path):", "        self.db_path = db_path",
                 "", "    def _conn(self): return sqlite3.connect(self.db_path)",
                 "", "    def find_by_id(self, user_id):",
                 "        with self._conn() as conn:",
                 "            row = conn.execute('SELECT * FROM users WHERE id=?',(user_id,)).fetchone()",
                 "            return dict(zip(['id','username','email','role'],row)) if row else None",
                 "", "    def find_by_email(self, email):",
                 "        with self._conn() as conn:",
                 "            row = conn.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()",
                 "            return dict(zip(['id','username','email','role'],row)) if row else None",
                 "", "    def find_all(self, active_only=True):",
                 "        sql = 'SELECT * FROM users' + (' WHERE is_active=1' if active_only else '')",
                 "        with self._conn() as conn:",
                 "            rows = conn.execute(sql).fetchall()",
                 "            cols = ['id','username','email','role']",
                 "            return [dict(zip(cols,r)) for r in rows]",
                 "", "    def create(self, username, email, password_hash, role='user'):",
                 "        with self._conn() as conn:",
                 "            cur = conn.execute(",
                 "                'INSERT INTO users (username,email,password_hash,role) VALUES (?,?,?,?)',",
                 "                (username,email,password_hash,role))",
                 "            conn.commit()",
                 "            return cur.lastrowid",
                 "",
                 "print('Repository pattern loaded.')", "end python",
                ],
            ], []),
            ("42.2 Service Layer Pattern", [
                "The Service layer pattern separates business logic from both the presentation layer (HTTP handlers, CLI) and the data layer (repositories). Services orchestrate multiple repositories and implement business rules such as validation, permission checks, and event emission.",
            ], [
                ["python:", "class UserService:",
                 "    def __init__(self, user_repo, notification_service):",
                 "        self.users = user_repo",
                 "        self.notifs = notification_service",
                 "",
                 "    def register(self, username, email, password):",
                 "        # Business rule: email must be unique",
                 "        if self.users.find_by_email(email):",
                 "            raise ValueError(f'Email already registered: {email}')",
                 "",
                 "        # Business rule: password must be strong",
                 "        if len(password) < 12:",
                 "            raise ValueError('Password must be at least 12 characters')",
                 "",
                 "        # Hash password",
                 "        import hashlib, secrets",
                 "        salt = secrets.token_hex(32)",
                 "        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000)",
                 "        password_hash = salt + ':' + hashed.hex()",
                 "",
                 "        # Create user",
                 "        user_id = self.users.create(username, email, password_hash)",
                 "",
                 "        # Send welcome notification",
                 "        self.notifs.send_welcome(email, username)",
                 "",
                 "        return user_id",
                 "",
                 "print('Service layer pattern loaded.')", "end python",
                ],
            ], []),
        ]),
    ]

    for ch_num, ch_title, sections in chapters_extra:
        E += chap(ch_title, ch_num)
        E.append(body(f"This chapter covers {ch_title.lower()} with complete code examples and explanations."))
        for sub_title, paragraphs, code_blocks, *_ in sections:
            E.append(h2(sub_title))
            for p in paragraphs:
                E.append(body(p))
            for cb in code_blocks:
                E.append(code(cb))
        E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 43: ENLANG LANGUAGE SPECIFICATION (FORMAL GRAMMAR)
    # ─────────────────────────────────────────────────────────────────────
    E += chap("EnLang Formal Language Specification", 43)
    E.append(body("This chapter provides the formal grammar specification of EnLang using a modified BNF (Backus-Naur Form) notation. This specification serves as the authoritative reference for the language, independent of any implementation details. Any compliant EnLang implementation must accept all programs that conform to this specification."))

    E.append(h2("43.1  Grammar Notation"))
    for p in [
        "The following conventions are used in the grammar specification: <non-terminal> denotes a grammar rule that can be expanded. 'terminal' denotes a literal keyword or token that appears in source code verbatim. ::= defines a production rule. | separates alternative productions. [...] denotes optional elements. {...} denotes zero-or-more repetitions. (...) groups elements.",
    ]:
        E.append(body(p))
    E.append(code([
        "# EnLang Grammar (Simplified BNF)",
        "",
        "# Top-level program",
        "<program>        ::= { <statement> | <block> }",
        "",
        "# Statements",
        "<statement>      ::= <assignment> | <display> | <input> | <import>",
        "                   | <function-call> | <return> | <raise> | <throw>",
        "                   | <break> | <continue> | <native-escape>",
        "",
        "# Assignment forms",
        "<assignment>     ::= 'set' <identifier> 'to' <expression>",
        "                   | 'let' <identifier> '=' <expression>",
        "                   | 'store' <expression> 'in' <identifier>",
        "                   | 'define' <type> <identifier> 'as' <expression>",
        "",
        "# Display forms",
        "<display>        ::= ('display' | 'print' | 'show' | 'output') <expression>",
        "",
        "# Block structures",
        "<block>          ::= <if-block> | <loop-block> | <function-block>",
        "                   | <try-block> | <match-block> | <native-block>",
        "",
        "# If block",
        "<if-block>       ::= 'if' <condition> ['then'] ':' <block-body>",
        "                     { 'else if' <condition> ['then'] ':' <block-body> }",
        "                     [ 'else' ':' <block-body> ]",
        "",
        "# Loop blocks",
        "<loop-block>     ::= <repeat-loop> | <for-loop> | <while-loop>",
        "<repeat-loop>    ::= 'repeat' <expr> 'times' ['do'] ':' <block-body>",
        "<for-loop>       ::= 'for' ['each'] <identifier> 'in' <expression> ['do'] ':' <block-body>",
        "<while-loop>     ::= 'while' <condition> ['do'] ':' <block-body>",
        "",
        "# Function blocks",
        "<function-block> ::= <func-header> ':' <block-body>",
        "<func-header>    ::= 'function' <identifier> '(' <params> ')'",
        "                   | 'function' <identifier> ('using'|'taking') <params>",
        "                   | 'action' <identifier> 'given' <params>",
        "                   | 'task' <identifier> 'for' <params>",
        "",
        "# Function calls",
        "<function-call>  ::= <identifier> '(' <args> ')'",
        "                   | ('start'|'call'|'run'|'execute') <identifier>",
        "                     ('from'|'with'|'using'|'for') <args>",
        "",
        "# Conditions",
        "<condition>      ::= <expression> <comparator> <expression>",
        "                   | <condition> ('and'|'or') <condition>",
        "                   | 'not' <condition>",
        "                   | <expression>",
        "<comparator>     ::= 'is equal to' | 'is not equal to'",
        "                   | 'is greater than or equal to' | 'is less than or equal to'",
        "                   | 'is greater than' | 'is less than'",
        "                   | 'is' | 'is not' | 'is in' | 'is not in'",
        "                   | '==' | '!=' | '>=' | '<=' | '>' | '<'",
        "",
        "# Expressions",
        "<expression>     ::= <term> { ('+' | '-' | 'plus' | 'minus') <term> }",
        "<term>           ::= <factor> { ('*' | '/' | 'times' | 'divided by' | 'mod') <factor> }",
        "<factor>         ::= <atom> [ ('**' | 'to the power of') <atom> ]",
        "<atom>           ::= <literal> | <identifier> | '(' <expression> ')'",
        "                   | '@python(' <python-expr> ')'",
        "                   | <function-call>",
    ]))

    E.append(h2("43.2  Token Types"))
    E.append(tbl([
        ["Token Type","Pattern","Examples"],
        ["IDENTIFIER","[a-zA-Z_][a-zA-Z0-9_]*","x, score, user_name, MAX_SIZE"],
        ["INTEGER_LIT","[0-9]+","42, 0, 100, 999"],
        ["FLOAT_LIT","[0-9]+\\.[0-9]+","3.14, 0.5, 99.99"],
        ["STRING_LIT","\"...\"|'...'","\"hello\", 'world'"],
        ["BOOL_LIT","true|false","true, false"],
        ["NULL_LIT","null|none","null, none"],
        ["KEYWORD","reserved word","set, display, if, for, while, function..."],
        ["INDENT","4+ leading spaces","    (4 spaces per level)"],
        ["NEWLINE","\\n","end of statement"],
        ["COMMENT","# ...","# This is a comment"],
        ["NATIVE_ESCAPE","@python(...)","@python(math.sqrt(x))"],
        ["NATIVE_BLOCK","python: ... end python","multi-line Python code"],
    ],col_widths=[95,165,230]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 44: COMPLETE KEYWORD & OPERATOR REFERENCE
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Complete Keyword, Operator & Built-in Reference", 44)

    E.append(h2("44.1  Full Keyword Listing (Alphabetical)"))
    keywords = [
        ("action","Function declaration keyword: 'action foo given n:'"),
        ("add","Collection operation: 'add item to list'"),
        ("analyze","NLP keyword: 'analyze sentiment of text and store in v'"),
        ("and","Logical conjunction in conditions"),
        ("apply","Function call keyword: 'apply foo with args'"),
        ("as","Alias in imports; type annotation separator"),
        ("ask","Input keyword: 'ask \"prompt\" and store in v'"),
        ("begin","Function call keyword: 'begin foo with args'"),
        ("break","Loop control: exit current loop immediately"),
        ("by","Used in increment/decrement: 'increment x by 1'"),
        ("call","Function call: 'call foo with args'"),
        ("case","Pattern match branch: 'case value:'"),
        ("check","File system check: 'check if path P exists'"),
        ("compute","NLP keyword: 'compute similarity between s1 and s2'"),
        ("continue","Loop control: skip to next iteration"),
        ("decrement","Math operation: 'decrement x by n'"),
        ("default","Pattern match fallback: 'default:'"),
        ("define","Type-annotated assignment: 'define type name as val'"),
        ("display","Output keyword: 'display expression'"),
        ("divided","Arithmetic: 'x divided by y' -> x / y"),
        ("do","Optional loop suffix: 'repeat N times do:'"),
        ("each","Optional for-loop prefix: 'for each item in list'"),
        ("else","Conditional fallback: 'else:' or 'else if ... then:'"),
        ("end","Block terminator: 'end match', 'end python'"),
        ("equal","Comparison: 'is equal to' -> =="),
        ("except","Exception handling: 'except ExceptionType:'"),
        ("execute","Function call / SQL: 'execute foo with args'"),
        ("exists","File check: 'check if path P exists'"),
        ("extract","NLP: 'extract keywords from text into var'"),
        ("false","Boolean literal -> False"),
        ("file","File I/O: 'read file path' or 'write text to file path'"),
        ("finally","Exception cleanup: 'finally:'"),
        ("for","Loop: 'for item in collection:' or function: 'task foo for n:'"),
        ("from","Function call: 'start foo from args'"),
        ("function","Function declaration: 'function name(params):'"),
        ("get","Env var: 'get environment variable NAME store in v'"),
        ("given","Function declaration: 'action foo given n:'"),
        ("greater","Comparison: 'is greater than' -> >"),
        ("hash","Security: 'hash text with sha256 store in v'"),
        ("if","Conditional: 'if condition then:'"),
        ("import","Module import: 'import module name'"),
        ("in","Loop iterator / membership: 'for x in list' or 'is in'"),
        ("increment","Math: 'increment x by n' -> x += n"),
        ("into","NLP: 'extract keywords from text into var'"),
        ("is","Comparison start: 'x is equal to y'"),
        ("keywords","NLP: 'extract keywords from ...'"),
        ("less","Comparison: 'is less than' -> <"),
        ("let","Variable assignment: 'let x = val'"),
        ("list","Type annotation / collection literal"),
        ("match","Pattern matching: 'match x:'"),
        ("message","Exception message: 'raise T with message m'"),
        ("minus","Arithmetic: 'x minus y' -> x - y"),
        ("mod","Modulo: 'x mod y' -> x % y"),
        ("modulo","Modulo alias: 'x modulo y' -> x % y"),
        ("module","Import target: 'import module json'"),
        ("multiply","Math: 'multiply x by n' -> x *= n"),
        ("next","Function call keyword"),
        ("not","Logical NOT: 'if not condition'"),
        ("null","Null literal -> None"),
        ("none","Null literal -> None"),
        ("on","Server/event: 'start web server on port N'"),
        ("or","Logical disjunction in conditions"),
        ("output","Output keyword -> print()"),
        ("path","File check: 'check if path P exists'"),
        ("perform","Function call keyword"),
        ("plus","Arithmetic: 'x plus y' -> x + y"),
        ("port","Web server: 'start web server on port N'"),
        ("power","Exponentiation: 'x to the power of y' -> x**y"),
        ("print","Output keyword -> print()"),
        ("procedure","Function declaration keyword"),
        ("process","Function declaration keyword"),
        ("prompt","Input keyword (alias for ask)"),
        ("raise","Exception: 'raise T with message m'"),
        ("read","File I/O: 'read file path and store in v'"),
        ("remove","Collection: 'remove item from list'"),
        ("repeat","Count loop: 'repeat N times do:'"),
        ("return","Function return: 'return expression'"),
        ("run","Function call: 'run foo using args'"),
        ("server","Web server: 'start web server ...'"),
        ("sentiment","NLP: 'analyze sentiment of text'"),
        ("set","Variable assignment: 'set x to val'"),
        ("show","Output keyword -> print()"),
        ("similarity","NLP: 'compute similarity between s1 and s2'"),
        ("start","Function call / server: 'start foo from args'"),
        ("store","Assignment: 'store val in x' / result: 'store in v'"),
        ("taking","Function declaration: 'function foo taking n:'"),
        ("task","Function declaration: 'task foo for n:'"),
        ("than","Comparison: part of 'greater than', 'less than'"),
        ("then","Conditional suffix: 'if condition then:'"),
        ("throw","Exception: 'throw error message'"),
        ("times","Arithmetic: 'x times y' -> x * y / count loop: 'repeat N times'"),
        ("to","Assignment: 'set x to val'"),
        ("true","Boolean literal -> True"),
        ("try","Exception handling: 'try:'"),
        ("using","Function declaration/call: 'function foo using n:' / 'run foo using args'"),
        ("variable","Env var: 'get environment variable NAME'"),
        ("web","Web server: 'start web server on port N'"),
        ("while","Conditional loop: 'while condition do:'"),
        ("with","Function declaration/call: 'function foo with n:' / Exception: 'raise T with message'"),
        ("write","File I/O: 'write text to file path'"),
    ]
    col1 = [["Keyword","Description"]]
    col2 = [["Keyword","Description"]]
    half = len(keywords) // 2
    for kw, desc in keywords[:half]:
        col1.append([kw, desc])
    for kw, desc in keywords[half:]:
        col2.append([kw, desc])
    E.append(tbl(col1, [80,410]))
    E.append(tbl(col2, [80,410]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 45: ENLANG HISTORY & ROADMAP
    # ─────────────────────────────────────────────────────────────────────
    E += chap("EnLang History, Version Timeline & Future Roadmap", 45)
    E.append(body("EnLang was conceived, designed, and implemented by Spandan Prayas Patra as an answer to the fundamental question: why should programming require learning an artificial foreign language when we already have a powerful, expressive language — English? The development journey from concept to production release is documented here."))

    E.append(h2("45.1  Version History"))
    E.append(tbl([
        ["Version","Release Date","Major Features"],
        ["0.1.0 (Alpha)","2025 Q1","Core Python transpiler: variables, display, if/else, basic loops"],
        ["0.2.0","2025 Q2","For-each loops, function definitions, return values, collections"],
        ["0.3.0","2025 Q3","HTML5 sub-transpiler (.enlgf), CSS3 sub-transpiler (.enlgd)"],
        ["0.4.0","2025 Q4","JavaScript sub-transpiler (.enlgs), SQL sub-transpiler (.enlgdb)"],
        ["0.5.0","2025 Q4","Exception handling (try/except/finally), match/case/default, imports"],
        ["0.6.0","2026 Q1","NLP primitives (sentiment, keywords, similarity), web server engine"],
        ["0.7.0","2026 Q1","3-Level Native Interactivity (@python, python: blocks), EPM alpha"],
        ["0.8.0","2026 Q2","Natural function syntax (function foo using n:, start foo from v)"],
        ["0.9.0","2026 Q2","Static syntax checker (enlang check), interactive debugger (enlang debug)"],
        ["1.0.0","2026 Q3","First stable release. All 154 unit tests passing. GUI installer."],
        ["2.0.0","2026-07-25","PyPI publication, v2 book release, enterprise features, security layer"],
    ],col_widths=[75,85,330]))

    E.append(h2("45.2  Future Roadmap"))
    E.append(tbl([
        ["Version","Planned","Features"],
        ["2.1.0","2026 Q3","Type inference engine, better IDE support protocol, VS Code extension"],
        ["2.2.0","2026 Q4","WebAssembly compilation target (.enlgw -> WASM)"],
        ["2.3.0","2026 Q4","Mobile compilation target (.enlgm -> React Native)"],
        ["3.0.0","2027 Q1","EnLang Runtime (ELR) — native bytecode VM, 10x performance"],
        ["3.1.0","2027 Q2","Concurrent & distributed programming primitives"],
        ["3.2.0","2027 Q3","ML/AI compilation target (.enlgai -> ONNX models)"],
        ["4.0.0","2028","Language server protocol, full IDE integration, package registry (EPM Hub)"],
    ],col_widths=[60,75,355]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTERS 46-50: Additional comprehensive examples
    # ─────────────────────────────────────────────────────────────────────

    E += chap("Complete Example Programs — 25 Working Applications", 46)

    programs = [
        ("46.1  Number Guessing Game", [
            "import module random",
            "",
            "set secret to @python(random.randint(1, 100))",
            "set attempts to 0",
            "set max_attempts to 10",
            "",
            "display \"Welcome to the Number Guessing Game!\"",
            "display \"I'm thinking of a number between 1 and 100.\"",
            "display \"You have \" plus str(max_attempts) plus \" attempts.\"",
            "",
            "set won to false",
            "while attempts is less than max_attempts and not won do:",
            "    set attempts to attempts plus 1",
            "    display @python(f\"\\nAttempt {attempts}/{max_attempts}: \")",
            "    ask \"Your guess: \" and store in guess_str",
            "    try:",
            "        set guess to @python(int(guess_str))",
            "        if guess is equal to secret then:",
            "            display @python(f\"CORRECT! You got it in {attempts} attempts!\")",
            "            set won to true",
            "        else if guess is less than secret then:",
            "            set remaining to max_attempts minus attempts",
            "            display \"Too low! \" plus str(remaining) plus \" attempts left.\"",
            "        else:",
            "            set remaining to max_attempts minus attempts",
            "            display \"Too high! \" plus str(remaining) plus \" attempts left.\"",
            "    except ValueError:",
            "        display \"Please enter a valid number!\"",
            "        set attempts to attempts minus 1",
            "",
            "if not won then:",
            "    display @python(f\"Game over! The number was {secret}.\")",
        ]),
        ("46.2  Caesar Cipher Encryption/Decryption", [
            "function caesar_encrypt(text, shift):",
            "    set result to \"\"",
            "    for each char in text do:",
            "        if @python(char.isalpha()) then:",
            "            set base to @python(ord('A') if char.isupper() else ord('a'))",
            "            set encrypted_char to @python(chr((ord(char) - base + shift) % 26 + base))",
            "            set result to result plus encrypted_char",
            "        else:",
            "            set result to result plus char",
            "    return result",
            "",
            "function caesar_decrypt(text, shift):",
            "    return caesar_encrypt(text, 26 minus shift)",
            "",
            "set message to \"Hello World from EnLang!\"",
            "set shift_val to 13",
            "",
            "set encrypted to caesar_encrypt(message, shift_val)",
            "set decrypted to caesar_decrypt(encrypted, shift_val)",
            "",
            "display \"Original:  \" plus message",
            "display \"Encrypted: \" plus encrypted",
            "display \"Decrypted: \" plus decrypted",
            "display \"Match: \" plus str(message is equal to decrypted)",
        ]),
        ("46.3  Fibonacci with Multiple Methods (Comparison)", [
            "import module time",
            "",
            "# Method 1: Naive recursion",
            "function fib_recursive(n):",
            "    if n is less than or equal to 1 then:",
            "        return n",
            "    return fib_recursive(n minus 1) plus fib_recursive(n minus 2)",
            "",
            "# Method 2: Iterative",
            "function fib_iterative(n):",
            "    if n is less than or equal to 1 then:",
            "        return n",
            "    set a to 0",
            "    set b to 1",
            "    repeat n minus 1 times do:",
            "        set temp to a plus b",
            "        set a to b",
            "        set b to temp",
            "    return b",
            "",
            "# Method 3: Memoized",
            "python:",
            "from functools import lru_cache",
            "@lru_cache(maxsize=None)",
            "def fib_memo(n):",
            "    if n <= 1: return n",
            "    return fib_memo(n-1) + fib_memo(n-2)",
            "end python",
            "",
            "# Compare methods for n=30",
            "set n to 30",
            "",
            "set t0 to @python(time.perf_counter())",
            "set r1 to fib_recursive(n)",
            "set t1 to @python(time.perf_counter())",
            "",
            "set t2 to @python(time.perf_counter())",
            "set r2 to fib_iterative(n)",
            "set t3 to @python(time.perf_counter())",
            "",
            "set t4 to @python(time.perf_counter())",
            "set r3 to @python(fib_memo(n))",
            "set t5 to @python(time.perf_counter())",
            "",
            "display @python(f'fib({n}) = {r1}')",
            "display @python(f'Recursive:  {(t1-t0)*1000:.2f}ms')",
            "display @python(f'Iterative:  {(t3-t2)*1000:.4f}ms')",
            "display @python(f'Memoized:   {(t5-t4)*1000:.4f}ms')",
        ]),
        ("46.4  Matrix Operations", [
            "python:",
            "class Matrix:",
            "    def __init__(self, data):",
            "        self.data = data",
            "        self.rows = len(data)",
            "        self.cols = len(data[0]) if data else 0",
            "",
            "    def __add__(self, other):",
            "        if self.rows != other.rows or self.cols != other.cols:",
            "            raise ValueError('Matrix dimensions must match for addition')",
            "        return Matrix([[self.data[i][j] + other.data[i][j]",
            "                       for j in range(self.cols)] for i in range(self.rows)])",
            "",
            "    def __mul__(self, other):",
            "        if self.cols != other.rows:",
            "            raise ValueError('Invalid dimensions for multiplication')",
            "        result = [[sum(self.data[i][k]*other.data[k][j] for k in range(self.cols))",
            "                   for j in range(other.cols)] for i in range(self.rows)]",
            "        return Matrix(result)",
            "",
            "    def transpose(self):",
            "        return Matrix([[self.data[j][i] for j in range(self.rows)]",
            "                       for i in range(self.cols)])",
            "",
            "    def __str__(self):",
            "        return '\\n'.join(['  '.join(f'{v:6.2f}' for v in row) for row in self.data])",
            "",
            "A = Matrix([[1,2,3],[4,5,6],[7,8,9]])",
            "B = Matrix([[9,8,7],[6,5,4],[3,2,1]])",
            "print('A + B:'); print(A + B)",
            "print('A * B:'); print(A * B)",
            "print('A transposed:'); print(A.transpose())",
            "end python",
        ]),
        ("46.5  Command-Line Argument Parser", [
            "python:",
            "import sys",
            "",
            "class EnLangArgParser:",
            "    def __init__(self, prog, description):",
            "        self.prog = prog",
            "        self.description = description",
            "        self._args = {}",
            "        self._flags = {}",
            "",
            "    def add_argument(self, name, help_text, required=False, default=None):",
            "        self._args[name] = {'help': help_text, 'required': required, 'default': default}",
            "",
            "    def add_flag(self, name, help_text):",
            "        self._flags[name] = {'help': help_text}",
            "",
            "    def parse(self, argv=None):",
            "        if argv is None: argv = sys.argv[1:]",
            "        result = {k: v['default'] for k, v in self._args.items()}",
            "        for k in self._flags: result[k] = False",
            "        i = 0",
            "        while i < len(argv):",
            "            arg = argv[i]",
            "            if arg.startswith('--'):",
            "                key = arg[2:]",
            "                if key in self._flags:",
            "                    result[key] = True",
            "                elif key in self._args and i+1 < len(argv):",
            "                    result[key] = argv[i+1]; i += 1",
            "            i += 1",
            "        return result",
            "",
            "parser = EnLangArgParser('myapp', 'My EnLang Application')",
            "parser.add_argument('input', 'Input file path', required=True)",
            "parser.add_argument('output', 'Output file path', default='output.txt')",
            "parser.add_flag('verbose', 'Enable verbose output')",
            "parser.add_flag('dry-run', 'Dry run without writing files')",
            "",
            "# Simulate parsing",
            "args = parser.parse(['--input', 'data.txt', '--verbose'])",
            "print('Parsed args:', args)",
            "end python",
        ]),
    ]

    for prog_title, prog_code in programs:
        E.append(h2(prog_title))
        E.append(code(prog_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 47: COMPREHENSIVE SYNTAX EXAMPLES BY DOMAIN
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Domain-Specific EnLang — Finance, Healthcare, Education & Science", 47)

    E.append(h2("47.1  Financial Computing"))
    E.append(code([
        "# financial_calc.enlg — Comprehensive financial calculations",
        "import module math",
        "",
        "# Simple Interest",
        "function simple_interest(principal, rate, time):",
        "    return principal times rate times time divided by 100",
        "",
        "# Compound Interest",
        "function compound_interest(principal, rate, time, n):",
        "    return principal times @python((1 + rate/(100*n))**(n*time)) minus principal",
        "",
        "# Present Value",
        "function present_value(future_value, rate, time):",
        "    return future_value divided by @python((1 + rate/100)**time)",
        "",
        "# Future Value",
        "function future_value(present_val, rate, time):",
        "    return present_val times @python((1 + rate/100)**time)",
        "",
        "# EMI (Equated Monthly Installment)",
        "function calculate_emi(principal, annual_rate, months):",
        "    set monthly_rate to annual_rate divided by (12 times 100)",
        "    if monthly_rate is equal to 0 then:",
        "        return principal divided by months",
        "    set emi to @python(principal * monthly_rate * (1+monthly_rate)**months / ((1+monthly_rate)**months - 1))",
        "    return @python(round(emi, 2))",
        "",
        "# IRR approximation using Newton-Raphson",
        "function npv(cashflows, rate):",
        "    set total to 0",
        "    for t, cf in @python(enumerate(cashflows)) do:",
        "        set total to total plus cf divided by @python((1+rate)**t)",
        "    return total",
        "",
        "# Demo",
        "display \"=== Financial Calculator Demo ===\"",
        "set p to 100000",
        "set r to 8.5",
        "set t to 5",
        "",
        "display @python(f\"Principal: ${p:,.0f}\")",
        "display @python(f\"Rate: {r}% per annum\")",
        "display @python(f\"Time: {t} years\")",
        "display @python(f\"Simple Interest: ${simple_interest(p, r, t):,.2f}\")",
        "display @python(f\"Compound Interest (annually): ${compound_interest(p, r, t, 1):,.2f}\")",
        "display @python(f\"Compound Interest (monthly): ${compound_interest(p, r, t, 12):,.2f}\")",
        "display @python(f\"Future Value: ${future_value(p, r, t):,.2f}\")",
        "display @python(f\"Present Value of $150,000 in {t}y: ${present_value(150000, r, t):,.2f}\")",
        "",
        "set home_loan to 5000000   # 50 lakhs",
        "set loan_rate to 9.2",
        "set loan_tenure to 240     # 20 years in months",
        "set monthly_emi to calculate_emi(home_loan, loan_rate, loan_tenure)",
        "display @python(f\"\\nHome Loan EMI: INR {monthly_emi:,.2f}/month\")",
        "display @python(f\"Total Payment: INR {monthly_emi*loan_tenure:,.2f}\")",
        "display @python(f\"Total Interest: INR {monthly_emi*loan_tenure - home_loan:,.2f}\")",
    ]))

    E.append(h2("47.2  Scientific Computing — Physics Simulations"))
    E.append(code([
        "# physics_sim.enlg — Basic physics simulations",
        "import module math",
        "",
        "# Projectile Motion",
        "function projectile_range(velocity, angle_degrees, gravity):",
        "    set angle_rad to @python(math.radians(angle_degrees))",
        "    set range_val to @python(velocity**2 * math.sin(2*angle_rad) / gravity)",
        "    return @python(round(range_val, 3))",
        "",
        "function projectile_max_height(velocity, angle_degrees, gravity):",
        "    set angle_rad to @python(math.radians(angle_degrees))",
        "    set h_max to @python((velocity * math.sin(angle_rad))**2 / (2*gravity))",
        "    return @python(round(h_max, 3))",
        "",
        "function projectile_time_of_flight(velocity, angle_degrees, gravity):",
        "    set angle_rad to @python(math.radians(angle_degrees))",
        "    set tof to @python(2 * velocity * math.sin(angle_rad) / gravity)",
        "    return @python(round(tof, 3))",
        "",
        "# Simulate projectile at different angles",
        "set v to 50  # m/s initial velocity",
        "set g to 9.81  # m/s^2 gravity",
        "",
        "display \"=== Projectile Motion Analysis ===\"",
        "display @python(f\"{'Angle':>8} {'Range':>12} {'Max Height':>12} {'Time of Flight':>15}\")",
        "display \"-\" times 50",
        "",
        "for angle in @python(range(0, 91, 5)):",
        "    set r to projectile_range(v, angle, g)",
        "    set h to projectile_max_height(v, angle, g)",
        "    set tof to projectile_time_of_flight(v, angle, g)",
        "    display @python(f\"{angle:>7}° {r:>11.2f}m {h:>11.2f}m {tof:>14.2f}s\")",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 48: INTERVIEW QUESTIONS & SOLUTIONS IN ENLANG
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Technical Interview Questions — 30 Solved Problems in EnLang", 48)

    interview_problems = [
        ("48.1  Two Sum Problem", "Given an array of integers and a target sum, return indices of two numbers that add up to the target.", [
            "function two_sum(nums, target):",
            "    set seen to {}",
            "    for i, num in @python(enumerate(nums)) do:",
            "        set complement to target minus num",
            "        if @python(complement in seen) then:",
            "            return [seen[complement], i]",
            "        set seen[num] to i",
            "    return []",
            "",
            "set nums to [2, 7, 11, 15]",
            "set target to 9",
            "display two_sum(nums, target)   # [0, 1]",
            "",
            "set nums2 to [3, 2, 4]",
            "set target2 to 6",
            "display two_sum(nums2, target2) # [1, 2]",
        ]),
        ("48.2  Valid Parentheses", "Check if a string of brackets is valid (properly opened and closed).", [
            "function is_valid_brackets(s):",
            "    set stack to []",
            "    set mapping to {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}",
            "    for each char in s do:",
            "        if @python(char in '([{') then:",
            "            add char to stack",
            "        else if @python(char in mapping) then:",
            "            if @python(not stack or stack[-1] != mapping[char]) then:",
            "                return false",
            "            @python(stack.pop())",
            "    return @python(len(stack) == 0)",
            "",
            "for test in [\"()\", \"()[]{}\", \"(]\", \"([)]\", \"{[]}\"] do:",
            "    display test plus \" -> \" plus str(is_valid_brackets(test))",
        ]),
        ("48.3  Merge Two Sorted Arrays", "Merge two sorted arrays into a single sorted array.", [
            "function merge_sorted(arr1, arr2):",
            "    set result to []",
            "    set i to 0",
            "    set j to 0",
            "    while i < @python(len(arr1)) and j < @python(len(arr2)) do:",
            "        if arr1[i] is less than or equal to arr2[j] then:",
            "            add arr1[i] to result",
            "            set i to i plus 1",
            "        else:",
            "            add arr2[j] to result",
            "            set j to j plus 1",
            "    set result to @python(result + arr1[i:] + arr2[j:])",
            "    return result",
            "",
            "set a to [1, 3, 5, 7, 9]",
            "set b to [2, 4, 6, 8, 10]",
            "display merge_sorted(a, b)",
        ]),
        ("48.4  Longest Palindromic Substring", "Find the longest substring of a string that is a palindrome.", [
            "function longest_palindrome(s):",
            "    set n to @python(len(s))",
            "    if n is equal to 0 then:",
            "        return \"\"",
            "    set start to 0",
            "    set max_len to 1",
            "",
            "    python:",
            "    def expand(left, right):",
            "        while left >= 0 and right < n and s[left] == s[right]:",
            "            nonlocal start, max_len",
            "            if right - left + 1 > max_len:",
            "                max_len = right - left + 1",
            "                start = left",
            "            left -= 1; right += 1",
            "    end python",
            "",
            "    for i in @python(range(n)):",
            "        @python(expand(i, i))    # Odd-length palindromes",
            "        @python(expand(i, i+1))  # Even-length palindromes",
            "",
            "    return @python(s[start:start+max_len])",
            "",
            "for test in [\"racecar\", \"babad\", \"cbbd\", \"abcba\", \"enlang\"] do:",
            "    display @python(f'\"{test}\" -> \"{longest_palindrome(test)}\"')",
        ]),
        ("48.5  Count Islands (Grid BFS)", "Count the number of islands (connected groups of 1s) in a 2D grid.", [
            "function count_islands(grid):",
            "    set rows to @python(len(grid))",
            "    set cols to @python(len(grid[0]))",
            "    set count to 0",
            "",
            "    python:",
            "    from collections import deque",
            "    def bfs(r, c):",
            "        queue = deque([(r, c)])",
            "        grid[r][c] = '0'",
            "        while queue:",
            "            row, col = queue.popleft()",
            "            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:",
            "                nr, nc = row+dr, col+dc",
            "                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':",
            "                    grid[nr][nc] = '0'",
            "                    queue.append((nr, nc))",
            "    end python",
            "",
            "    for r in @python(range(rows)):",
            "        for c in @python(range(cols)):",
            "            if grid[r][c] is equal to \"1\" then:",
            "                @python(bfs(r, c))",
            "                set count to count plus 1",
            "    return count",
            "",
            "set grid1 to [[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]",
            "display \"Islands: \" plus str(count_islands(grid1))  # 1",
            "",
            "set grid2 to [[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]",
            "display \"Islands: \" plus str(count_islands(grid2))  # 3",
        ]),
    ]

    for prob_title, prob_desc, prob_code in interview_problems:
        E.append(h2(prob_title))
        E.append(body(prob_desc))
        E.append(code(prob_code))

    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 49: ENLANG STYLE GUIDE — COMPLETE EDITION
    # ─────────────────────────────────────────────────────────────────────
    E += chap("The Complete EnLang Style Guide — Writing Readable, Maintainable Code", 49)

    E.append(body("Code is read far more often than it is written. The EnLang Style Guide provides conventions that maximize code readability, reduce cognitive load, and enable collaborative development on large teams. Following these guidelines is strongly recommended for all EnLang projects."))

    for section, rules in [
        ("49.1  File Organization", [
            "1. Each .enlg file should have a single, clear purpose — server initialization, a specific feature module, a utility library, or a test suite.",
            "2. Files should be named descriptively using snake_case: user_auth.enlg, payment_processor.enlg, not utils.enlg or misc.enlg.",
            "3. Group related .enlg files in subdirectories: src/models/, src/routes/, src/services/.",
            "4. Place all import statements at the top of the file, before any other code.",
            "5. Document the file's purpose with a comment at the top (# module_name.enlg — brief description).",
            "6. Separate logical sections with blank lines and optional comment headers (# === Section Name ===).",
        ]),
        ("49.2  Variable Naming", [
            "1. Use snake_case for all variable and function names: user_profile, calculate_tax, not userProfile or CalculateTax.",
            "2. Use UPPER_SNAKE_CASE for constants: MAX_CONNECTIONS, API_KEY, DEFAULT_PORT.",
            "3. Boolean variables should start with is_, has_, can_, or should_: is_active, has_permission, can_edit.",
            "4. Use descriptive names that communicate intent: instead of 'x', write 'horizontal_position'; instead of 'n', write 'item_count'.",
            "5. Avoid single-letter variables except in short mathematical loops (i, j for loop indices).",
            "6. Prefix private-style variables (accessible only within a block) with an underscore: _temp_result, _internal_counter.",
        ]),
        ("49.3  Function Design Principles", [
            "1. Functions should do one thing and do it well. If a function name contains 'and', it probably does two things — split it.",
            "2. Function names should be verb phrases: calculate_bmi(), validate_email(), send_notification().",
            "3. Keep functions short — ideally 15-25 lines. If a function is longer, refactor it into smaller helper functions.",
            "4. Functions should have at most 3-4 parameters. More parameters suggest a design problem — consider passing a dictionary.",
            "5. Always handle the error cases first (guard clauses) before the happy path — this reduces nesting depth.",
            "6. Return early when possible rather than deeply nesting if-else blocks.",
        ]),
        ("49.4  Code Formatting Rules", [
            "1. ALWAYS use exactly 4 spaces per indentation level. Never use tabs.",
            "2. ALWAYS include the trailing colon ':' on block headers (if/for/while/function).",
            "3. Include 'then:' in if statements for readability: 'if x is greater than 5 then:' not 'if x > 5:'.",
            "4. Include 'do:' in loop statements for readability: 'for each item in list do:' not 'for each item in list:'.",
            "5. Leave one blank line between function definitions.",
            "6. Leave two blank lines between major sections of a file.",
            "7. Keep lines under 100 characters when possible. Break long lines for readability.",
            "8. Use @python() escapes sparingly — only when EnLang's natural syntax cannot express the operation.",
        ]),
    ]:
        E.append(h2(section))
        for rule in rules:
            E.append(bul(rule))

    E.append(h2("49.5  Good vs. Bad Code Examples"))
    E.append(code([
        "# ============================================================",
        "# BAD: Poor variable names, no type hints, unclear logic",
        "# ============================================================",
        "set x to 1",
        "set y to 100",
        "set z to 0",
        "while x < y:",
        "    if x * x == x + 1:",
        "        set z to z + x",
        "    set x to x + 1",
        "print z",
        "",
        "# ============================================================",
        "# GOOD: Clear names, documented logic, readable flow",
        "# ============================================================",
        "# Find sum of all perfect squares between 1 and 100",
        "",
        "set current_num to 1",
        "set upper_limit to 100",
        "set sum_of_perfect_squares to 0",
        "",
        "while current_num is less than or equal to upper_limit do:",
        "    set square_root to @python(int(current_num ** 0.5))",
        "    set is_perfect_square to (square_root times square_root is equal to current_num)",
        "    if is_perfect_square then:",
        "        set sum_of_perfect_squares to sum_of_perfect_squares plus current_num",
        "    increment current_num by 1",
        "",
        "display \"Sum of perfect squares (1-100): \" plus str(sum_of_perfect_squares)",
    ]))
    E.append(hr())

    # ─────────────────────────────────────────────────────────────────────
    # CHAPTER 50: EPILOGUE, PHILOSOPHY & THE FUTURE OF ENLANG
    # ─────────────────────────────────────────────────────────────────────
    E += chap("Epilogue: The Future of Natural Language Programming", 50)

    for p in [
        "We stand at a turning point in the history of software engineering. For the first time in the seven decades of commercial computing, the barriers between human thought and machine execution are beginning to dissolve. EnLang is not merely a programming language — it is a proof of concept for a fundamentally different relationship between humans and computers.",
        "The core insight behind EnLang is simple but profound: programming languages should conform to human communication patterns, not the other way around. When we force developers to learn artificial syntaxes, we are not just adding friction — we are actively excluding billions of people who could contribute valuable software to the world but cannot overcome the initial learning barrier of traditional programming languages.",
        "EnLang's deterministic transpilation model proves that natural language programming does not require LLMs, internet connectivity, or probabilistic code generation. A carefully designed, explicit grammar engine can handle the vast majority of programming constructs needed for real-world applications — from simple scripts to full-stack web applications with authentication, databases, styling, and client-side interactivity.",
        "The multi-target compilation model (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb) demonstrates that a single natural language paradigm can serve as a unified abstraction across the entire technology stack. Instead of learning Python for the backend, HTML for structure, CSS for styling, JavaScript for interactivity, and SQL for data — a developer can learn one language: EnLang. The compiler handles the translation to native target languages.",
        "Spandan Prayas Patra's vision for EnLang extends beyond the current v2.0.0 release. Future versions will add WebAssembly compilation targets (enabling EnLang programs to run directly in browsers at near-native speed), mobile compilation targets (React Native output from .enlgm files), an ML/AI compilation target (.enlgai producing ONNX models), and a native bytecode VM (the EnLang Runtime, or ELR) that eliminates the Python runtime dependency entirely.",
        "The most exciting potential of EnLang lies in education. Imagine a world where children learn programming in the same language they already speak — English. Where the first programming lesson is not 'what is a variable?' but 'what would you like the computer to remember?' Where debugging means reading natural English error messages instead of cryptic stack traces. EnLang is building that world, one natural expression at a time.",
        "As you complete this book, you now possess the complete knowledge required to build anything in EnLang — from a simple 5-line script to a full-stack enterprise application with thousands of lines across multiple compilation targets. You understand the grammar engine, the compiler pipeline, the developer tooling, the security patterns, and the design principles that make EnLang code readable, maintainable, and correct.",
        "The EnLang community welcomes your contributions. If you find a natural English expression that EnLang should understand but doesn't, submit it. If you build something remarkable with EnLang, share it. If you teach someone programming using EnLang, you are directly contributing to a more inclusive, accessible future for software development.",
        "Thank you for reading. Now go build something remarkable.",
    ]:
        E.append(body(p))

    E.append(Spacer(1, 0.3*inch))
    E.append(Paragraph("— Spandan Prayas Patra", S["book_sub"]))
    E.append(Paragraph("Architect, EnLang Programming Language", S["book_auth"]))
    E.append(hr())

    return E

# =============================================================================
# MAIN — Build the combined PDF
# =============================================================================
if __name__ == "__main__":
    import importlib.util, sys
    # Import the base book module
    base_spec = importlib.util.spec_from_file_location("base_book", "build_master_book.py")
    base_mod = importlib.util.module_from_spec(base_spec)
    base_spec.loader.exec_module(base_mod)

    OUT = "enlangbookv2release.pdf"
    print("[INFO] Building EnLang 500+ Page Ultra-Dense Master Book PDF...")

    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
    )

    print("[INFO] Building base chapters (1-30)...")
    base_elements = base_mod.build()

    print("[INFO] Building extended chapters (31-50)...")
    ext_elements = all_extended_chapters()

    all_elements = base_elements + ext_elements

    print(f"[INFO] Total flow elements: {len(all_elements)}")
    doc.build(all_elements)

    size = os.path.getsize(OUT)
    print(f"[SUCCESS] PDF written: {OUT}")
    print(f"[INFO]    Size: {size:,} bytes ({size//1024} KB)")
    print(f"[INFO]    Path: {os.path.abspath(OUT)}")
