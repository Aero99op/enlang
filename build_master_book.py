"""
EnLang 500+ Page Master Book Generator — Extended Ultra-Dense Edition
"""
import os, re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak, KeepTogether
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
        toc_ch=P("TC", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
                 textColor=colors.HexColor("#1e1b4b"), spaceAfter=2),
        toc_sec=P("TS", fontName="Helvetica", fontSize=8.5, leading=12,
                  textColor=colors.HexColor("#4338ca"), leftIndent=14, spaceAfter=1),
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

def section_header(num, title):
    return [h2(f"{num}  {title}"), Spacer(1, 2)]

# ────────────────────────────────────────────────────────────────
# LONG PARAGRAPH HELPERS
# ────────────────────────────────────────────────────────────────
PARA_LEN = 8  # number of long-body paragraphs to pad each section

def long_body(topic, details):
    """Returns multiple paragraph blocks for a topic."""
    blocks = []
    blocks.append(body(details))
    return blocks

# ════════════════════════════════════════════════════════════════════════════
# BOOK ELEMENT BUILDER
# ════════════════════════════════════════════════════════════════════════════
def build():
    E = []

    # COVER
    E += [Spacer(1,1.0*inch),
          Paragraph("ENLANG FOR DEVELOPERS",S["book_title"]),
          Paragraph("The Complete Master Reference — 500+ Page Ultra-Dense Edition",S["book_sub"]),
          Paragraph("Covering Every Syntax, Concept, Algorithm, Tool &amp; Production Pattern",S["book_sub"]),
          Spacer(1,0.2*inch),
          HRFlowable(width="75%",thickness=2,color=colors.HexColor("#4338ca"),hAlign="CENTER",spaceAfter=14),
          Paragraph("Author &amp; Architect: Spandan Prayas Patra",S["book_auth"]),
          Paragraph("Version 2.0.0 — PyPI: pip install enlang",S["book_auth"]),
          Paragraph("GitHub: https://github.com/Aero99op/enlang",S["book_auth"]),
          Spacer(1,0.3*inch),
          body("This book is the definitive comprehensive reference for mastering the EnLang Natural English Programming Language. It covers every aspect of the language from first principles to advanced production engineering, including all five compilation targets (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb), developer tooling (linter, debugger), the EnLang Package Manager (EPM), web server engine, security patterns, algorithm implementations, and five complete full-stack production case studies. Upon completing this book, a student will be able to build any type of software application in EnLang with full professional competence."),
          PageBreak()]

    # ── CHAPTER 1 ────────────────────────────────────────────────────────
    E += chap("Philosophical Architecture & Language Design", 1)

    for sub_num, sub_title, paragraphs in [
        ("1.1","Why Natural English as a Programming Language?",[
            "For seven decades, software engineering has forced developers to learn and think in artificial, symbol-heavy syntaxes — curly braces, semicolons, arrow operators, and abstract keywords like 'void', 'nullptr', or 'lambda'. This cognitive overhead is not fundamental to computing; it is an artifact of hardware limitations from the 1950s and 60s that modern systems no longer face.",
            "EnLang was designed by Spandan Prayas Patra to answer a single fundamental question: what if programming were as expressive and frictionless as writing a letter or giving verbal instructions? The hypothesis is that natural English, properly structured, is unambiguous enough to serve as a programming language — and the EnLang compiler proves this hypothesis with rigorous determinism.",
            "The language follows a strict principle of 1:1 mapping: every EnLang natural expression maps to exactly one native code output. There are no probabilistic decisions, no neural network weights, no internet calls. The transpiler is a pure, deterministic, rule-based system that runs in microseconds on any modern CPU.",
            "EnLang is the world's first fully-deterministic, multi-target Natural English Programming Language. It transpiles clean structured English sentences into production-grade native target code across five domains: Python for backend logic, HTML5 for frontend structure, CSS3 for visual design, JavaScript ES6+ for client interactivity, and SQL for data persistence.",
            "Unlike LLM-based code generators — which are probabilistic, non-deterministic, require internet connectivity, and produce outputs that require manual review and correction — EnLang operates as a pure offline, rule-based compilation engine. This makes it suitable for safety-critical applications, regulated industries, offline deployments, educational environments, and any context where reproducibility and auditability are required.",
            "The language is designed to serve two fundamentally different user personas simultaneously: (1) Complete beginners with zero programming knowledge, who can write valid EnLang programs by following natural English intuition alone, and (2) Senior engineers who can build production-grade multi-file full-stack applications using the full power of all five compilation targets, EPM, the web server, and the security primitives.",
            "This dual-persona design philosophy is what makes EnLang unique in the landscape of programming languages. No other language has achieved the combination of natural-language readability for beginners and full-stack production capability for professionals in a single coherent system.",
        ]),
        ("1.2","The Multi-Target Compilation Model",[
            "The EnLang Compiler Engine (ECE) implements a five-track compilation pipeline. Each file extension triggers a different sub-transpiler, each of which has its own complete grammar rule set, pattern matcher, and output formatter. The selection is automatic based on file extension — no compiler flags or configuration are required.",
            "The .enlg extension (short for 'EnLang') targets Python 3.8+. This is the primary compilation target and the most feature-rich sub-transpiler. It supports the complete EnLang grammar including all variable types, control flow, functions, collections, OOP, exception handling, file I/O, modules, native NLP primitives, and Level 2/3 native Python escapes.",
            "The .enlgf extension (short for 'EnLang Frontend') targets HTML5. It provides a natural English DSL for building semantic HTML5 document structure, including all HTML5 elements, attributes, forms, tables, media, accessibility attributes, and structured page composition.",
            "The .enlgd extension (short for 'EnLang Design') targets CSS3. It provides natural English syntax for all CSS properties, flexbox, grid layouts, custom properties (CSS variables), animations, transitions, media queries, pseudo-classes, and design theme blocks.",
            "The .enlgs extension (short for 'EnLang Script') targets JavaScript ES6+. It provides DOM manipulation, event handling, async/await, fetch API, localStorage, ES6 modules, and modern JavaScript patterns in natural English.",
            "The .enlgdb extension (short for 'EnLang DataBase') targets SQL (SQLite-compatible by default, with planned adapters for PostgreSQL, MySQL, and Microsoft SQL Server). It supports CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, JOIN, transactions, and indexes.",
            "All five sub-transpilers share a common pattern: natural English phrases on the left, native target code on the right. The grammar engine applies regex-based pattern matching in a defined priority order, with raw native code always passing through verbatim as the last fallback rule.",
        ]),
        ("1.3","Determinism vs. Probabilistic Code Generation",[
            "Determinism is the core guarantee of the EnLang specification. It means that given any valid EnLang source file, the compiler will always produce exactly the same native target output — on any machine, at any time, with any version of the EnLang engine that supports that specification version.",
            "This stands in stark contrast to LLM-based code assistants, which are inherently probabilistic. Even with temperature=0, most LLM APIs introduce subtle non-determinism through batching, hardware differences, and floating-point variation. Two runs of the same prompt on GPT-4 or Claude may produce syntactically different code that achieves the same logical goal — but may contain different bugs, different style choices, or different edge case handling.",
            "For applications in healthcare, finance, aviation, legal technology, and government systems — where code must be reproducible, auditable, and defensible — probabilistic code generation is unacceptable. EnLang's deterministic transpiler fills this gap, providing the readability of natural language with the reliability of a traditional compiler.",
            "The comparison table below summarizes the key differences between EnLang's deterministic transpiler and LLM-based code generation tools. This comparison is not meant to disparage LLM tools, which excel at different use cases — rather, it clarifies when EnLang is the more appropriate choice.",
        ]),
        ("1.4","EnLang's Ecosystem Overview",[
            "The EnLang ecosystem is designed around three pillars: compile, develop, and distribute. The compile pillar consists of the ECE (EnLang Compiler Engine) with its five sub-transpilers, the grammar engine, the NLP parser, and the 3-level native interactivity system. The develop pillar consists of the static syntax checker (enlang check), the interactive CLI debugger (enlang debug), and the built-in HTTP web server (enlang server). The distribute pillar consists of the EnLang Package Manager (EPM), PyPI distribution, the GUI Windows installer (EnLangInstaller.exe), and GitHub release management.",
            "The three pillars work together to provide a complete development lifecycle: write EnLang programs using the natural syntax, develop interactively with the linter catching errors and the debugger stepping through execution, and distribute to users via pip install enlang or the GUI installer. This lifecycle is intentionally simple and approachable, avoiding the configuration complexity of tools like Webpack, Babel, or Docker that often overwhelm newcomers.",
            "The EnLang ecosystem is deliberately kept minimal. There is no mandatory build step, no configuration file required for basic programs, no complex dependency graph for the core language features. A single .enlg file is sufficient to write and run a complete program. Complexity is introduced incrementally as projects grow — starting with single-file scripts and scaling to multi-file, multi-target enterprise applications.",
        ]),
    ]:
        E.append(h2(f"{sub_num}  {sub_title}"))
        for p in paragraphs:
            E.append(body(p))

    E.append(tbl([
        ["Property","EnLang Transpiler","LLM Code Generator"],
        ["Determinism","100% Reproducible","Probabilistic (varies per run)"],
        ["Internet Required","No (fully offline)","Yes (API calls required)"],
        ["Speed","Microseconds per line","Seconds per response"],
        ["Same input gives","Always same output","May differ per run"],
        ["Cost","Free, MIT licensed","API tokens / paid subscription"],
        ["Auditability","Explicit grammar rules","Black-box neural weights"],
        ["Safety-critical use","Suitable","Not recommended"],
        ["Learning curve","Natural English","Prompt engineering skills"],
        ["Supports 5 targets","Yes (.enlg/.enlgf/etc.)","Depends on model training"],
    ], col_widths=[130,175,185]))
    E.append(hr())

    # ── CHAPTER 2 ────────────────────────────────────────────────────────
    E += chap("Installation, Environment & Project Bootstrap", 2)
    for sub_num, sub_title, paragraphs, code_blocks in [
        ("2.1","pip install enlang — The One-Line Install",[
            "EnLang v2.0.0 is published on PyPI at https://pypi.org/project/enlang/2.0.0/. The Python Package Index is the world's largest Python package registry, hosting over 500,000 packages used by millions of developers worldwide. Publishing EnLang on PyPI means that anyone with Python 3.8+ installed can download and install the entire EnLang toolchain with a single command.",
            "The pip install command automatically downloads the latest stable version of EnLang, installs all required dependencies, and registers the 'enlang' and 'epm' CLI commands in the system PATH. After installation completes, you can immediately open any terminal and start writing and running EnLang programs.",
            "For users who need a specific version (e.g., for reproducible production deployments), use 'pip install enlang==2.0.0'. For users who want to install the latest development build from GitHub before it is published to PyPI, use 'pip install git+https://github.com/Aero99op/enlang.git'.",
        ],[
            ["# Install from PyPI (stable)","pip install enlang","","# Install specific version","pip install enlang==2.0.0","","# Upgrade to latest","pip install --upgrade enlang","","# Install from GitHub (development build)","pip install git+https://github.com/Aero99op/enlang.git","","# Verify installation","enlang version"],
        ]),
        ("2.2","Virtual Environments (Recommended Practice)",[
            "Virtual environments are isolated Python installations that keep project dependencies separate from each other and from the global system Python. They are strongly recommended for all EnLang projects to avoid dependency conflicts between projects.",
            "Creating a virtual environment takes less than 5 seconds and provides complete isolation. Once activated, all pip install commands and all enlang commands operate within that isolated environment. When you're done working on a project, simply deactivate the environment.",
        ],[
            ["# Windows — Create virtual environment","python -m venv .venv","","# Windows — Activate",".\\.venv\\Scripts\\activate","","# macOS / Linux — Create","python3 -m venv .venv","","# macOS / Linux — Activate","source .venv/bin/activate","","# Install EnLang in the virtual environment","pip install enlang","","# Deactivate when done","deactivate"],
        ]),
        ("2.3","GUI Windows Installer (EnLangInstaller.exe)",[
            "For Windows users who prefer a point-and-click experience, EnLang provides EnLangInstaller.exe — a standalone compiled GUI wizard. It is built with Tkinter for the graphical interface and packaged with PyInstaller into a single self-contained executable file.",
            "The GUI installer requires no Python pre-installation on the target machine. Simply download EnLangInstaller.exe from the public GitHub Releases page at https://github.com/Aero99op/enlang/releases and double-click it. The installer wizard guides the user through three screens: Welcome, Installation Progress, and Completion.",
            "Under the hood, the installer: (1) detects whether Python is already installed and installs it silently if not, (2) creates the %USERPROFILE%\\.enlang directory, (3) copies all EnLang core engine files into that directory, (4) registers the 'enlang' command in the system PATH by modifying the Windows Registry, and (5) runs 'enlang version' to verify the installation succeeded.",
        ],[
            ["# The GUI installer automates all of these steps:","","# 1. Create EnLang home directory","%USERPROFILE%\\.enlang\\","","# 2. Installed files:","   enlang.py      — CLI entry point","   enlang_core/   — Compiler engine package","   gui_installer.py","","# 3. PATH registration","   HKEY_CURRENT_USER\\Environment\\PATH","   += %USERPROFILE%\\.enlang","","# 4. Verification","   enlang version","   EnLang Version 2.0.0"],
        ]),
        ("2.4","Your First EnLang Program",[
            "Once EnLang is installed, create a new file called hello.enlg in any directory and add the following single line of natural English code. This is the simplest complete EnLang program:",
            "Save the file, open a terminal in the same directory, and run it with 'enlang run hello.enlg'. You should see 'Hello, World!' printed immediately. This confirms that the EnLang compiler is correctly installed, the Python runtime is accessible, and the 'enlang' CLI command is registered in your PATH.",
        ],[
            ["# hello.enlg","display \"Hello, World!\""],
            ["enlang run hello.enlg"],
            ["Hello, World!"],
        ]),
        ("2.5","Project Directory Structure Best Practices",[
            "For small single-file programs, simply place your .enlg file in any directory. For medium to large projects, follow the recommended project structure shown below. This structure separates concerns cleanly: backend logic in the root or /src, frontend assets in /static, database schemas in /database, tests in /tests, and project configuration in enlang.json.",
            "The enlang.json file at the project root is analogous to package.json in Node.js projects or pyproject.toml in Python projects. It stores project metadata (name, version, author), lists all Python and web dependencies, and defines run scripts. When you run 'epm install', EPM reads this file and installs all listed dependencies.",
        ],[
            ["my_enlang_project/","├── enlang.json            # Project config","├── server.enlg            # Main backend entry point","├── src/","│   ├── auth.enlg          # Auth module","│   ├── models.enlg        # Data models","│   └── api.enlg           # REST API routes","├── static/","│   ├── index.enlgf        # Frontend HTML","│   ├── styles.enlgd       # CSS design system","│   └── app.enlgs          # Client JavaScript","├── database/","│   └── schema.enlgdb      # Database schema","├── tests/","│   ├── test_auth.py","│   └── test_api.py","└── .venv/                 # Virtual environment"],
        ]),
    ]:
        E.append(h2(f"{sub_num}  {sub_title}"))
        for p in paragraphs:
            E.append(body(p))
        for cb in code_blocks:
            E.append(code(cb))

    E.append(tbl([
        ["Installation Method","Command","Requirements","Best For"],
        ["PyPI (pip)","pip install enlang","Python 3.8+ installed","Developers with Python"],
        ["PyPI (virtual env)","python -m venv .v && .v/Scripts/activate && pip install enlang","Python 3.8+","Project isolation"],
        ["GitHub URL","pip install git+https://github.com/Aero99op/enlang.git","Python + Git","Latest dev build"],
        ["GUI Installer","Download EnLangInstaller.exe + double-click","Windows only","Non-technical users"],
        ["CLI installer","python installer.py","Python in repo","Manual local install"],
    ],col_widths=[110,175,120,100]))
    E.append(hr())

    # ── CHAPTER 3 ────────────────────────────────────────────────────────
    E += chap("Variables, Types, Constants & Value Expressions", 3)

    E.append(h2("3.1  Natural Variable Declaration — The Three Forms"))
    for p in [
        "EnLang provides three completely equivalent forms for declaring and assigning variables. All three compile to a simple Python assignment statement (x = value). The choice between them is purely stylistic — use whichever form makes your code read most naturally in context.",
        "The 'set ... to ...' form is the primary recommended form for most situations. 'set score to 100' reads almost identically to how you would write it in a mathematical specification or requirements document. The 'let ... = ...' form is familiar to developers coming from JavaScript, Kotlin, or Swift, where 'let' is used for variable declarations. The 'store ... in ...' form is particularly natural when describing the result of an operation being saved into a variable.",
        "All three forms support any valid Python expression on the right-hand side, including arithmetic operations, function calls, list literals, dictionary literals, and @python() escape expressions. EnLang automatically translates all natural arithmetic operators (plus, minus, times, divided by) in these expressions before generating the Python output.",
        "EnLang variable names follow the same rules as Python identifiers: they must start with a letter or underscore, can contain letters, digits, and underscores, and are case-sensitive. By convention, multi-word variable names use snake_case (e.g., user_score, first_name, total_price), following the Python PEP 8 style guide that EnLang's Python output is designed to comply with.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Form 1: set ... to ... (Primary Recommended Form)",
        "set username to \"Spandan\"",
        "set age to 25",
        "set price to 99.99",
        "set is_active to true",
        "set scores to [90, 85, 92, 78, 95]",
        "set profile to {\"name\": \"Spandan\", \"role\": \"admin\"}",
        "",
        "# Form 2: let ... = ... (Familiar to JS/Swift developers)",
        "let username = \"Spandan\"",
        "let age = 25",
        "let price = 99.99",
        "",
        "# Form 3: store ... in ... (Natural for operation results)",
        "store \"Spandan\" in username",
        "store 100 in score",
        "store @python(math.sqrt(144)) in root_value",
        "store @python(len(scores)) in count",
    ]))

    E.append(h2("3.2  Optional Type Annotations"))
    for p in [
        "EnLang is dynamically typed by default, meaning variables do not require type declarations and can hold any value of any type. However, EnLang v2.0.0 introduces optional type annotations using the 'define <type> <name> as <value>' form. These annotations serve as documentation for developers, enable IDE auto-completion and type checking support, and are validated by the 'enlang check' static linter.",
        "Type annotations in EnLang are purely advisory — they do not affect runtime behavior and do not prevent you from reassigning a variable to a different type later. They are designed for large codebases where communicating intent clearly is important for maintainability.",
        "The type names in EnLang are deliberately chosen to be as natural and self-explanatory as possible. 'number' instead of 'int', 'decimal' instead of 'float', 'text' instead of 'str', 'boolean' instead of 'bool'. This naming convention is consistent with how non-programmers describe data types in natural English.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Type-annotated variable declarations",
        "define number user_id as 1001",
        "define decimal balance as 1250.75",
        "define text full_name as \"Spandan Prayas Patra\"",
        "define boolean is_premium as true",
        "define list recent_orders as [\"ORD001\", \"ORD002\", \"ORD003\"]",
        "define dictionary address as {\"city\": \"Bhubaneswar\", \"state\": \"Odisha\"}",
        "define set active_sessions as {\"sess_001\", \"sess_002\"}",
    ]))
    E.append(tbl([
        ["EnLang Type","Python Equiv.","Range / Description","Example"],
        ["number","int","Any integer, positive/negative/zero","set x to -42"],
        ["decimal","float","64-bit floating-point number","set pi to 3.14159"],
        ["text","str","Unicode string of any length","set name to \"Alice\""],
        ["boolean","bool","Only true or false","set flag to true"],
        ["list","list","Ordered mutable sequence","set nums to [1,2,3]"],
        ["dictionary","dict","Key-value pairs (hash map)","set d to {\"a\":1}"],
        ["set","set","Unordered unique elements","set s to {1,2,3}"],
        ["tuple","tuple","Ordered immutable sequence","@python((1,2,3))"],
    ],col_widths=[80,80,160,170]))

    E.append(h2("3.3  Arithmetic Operators — Natural English & Symbolic"))
    for p in [
        "EnLang supports both natural English operators and direct Python/mathematical symbol operators. Both forms compile to the same Python output. You can mix both styles freely within the same expression, though consistency is recommended for readability.",
        "The complete set of supported arithmetic operators is shown in the table below. All operators follow Python's standard precedence rules: parentheses first, then power, then multiplication/division/modulo, then addition/subtraction. Use parentheses liberally to make operator precedence explicit and code self-documenting.",
    ]:
        E.append(body(p))
    E.append(tbl([
        ["EnLang Natural","Symbol","Python","Precedence","Example"],
        ["x plus y","x + y","x + y","Low","set total to price plus tax"],
        ["x minus y","x - y","x - y","Low","set change to paid minus cost"],
        ["x times y","x * y","x * y","Medium","set area to w times h"],
        ["x divided by y","x / y","x / y","Medium","set avg to sum divided by n"],
        ["x mod y / x modulo y","x % y","x % y","Medium","set rem to n mod 2"],
        ["x to the power of y","x ** y","x**y","High","set sq to n to the power of 2"],
        ["(expressions)","(x+y)*z","(x+y)*z","Highest","set val to (a plus b) times c"],
    ],col_widths=[115,65,65,65,180]))

    E.append(h2("3.4  String Operations"))
    for p in [
        "String concatenation in EnLang uses the 'plus' operator. Since Python's + operator for strings requires both operands to be strings, EnLang's transpiler automatically wraps non-string operands in str() when the expression contains at least one string literal. This prevents the common TypeError: can only concatenate str (not 'int') to str error.",
        "For complex string formatting needs, use the @python() escape to access Python's f-string syntax directly. F-strings are significantly more readable than string concatenation for complex expressions and are the preferred approach for multi-variable string formatting.",
    ]:
        E.append(body(p))
    E.append(code([
        "set name to \"Spandan\"",
        "set age to 25",
        "set score to 98.5",
        "",
        "# Concatenation with 'plus'",
        "display \"Hello, \" plus name plus \"! Age: \" plus str(age)",
        "",
        "# Using @python for f-string (cleaner for complex cases)",
        "display @python(f\"Student: {name}, Age: {age}, Score: {score:.1f}%\")",
        "",
        "# Multi-line string",
        "set message to \"Line 1\\nLine 2\\nLine 3\"",
        "display message",
        "",
        "# String repetition",
        "set line to @python(\"=\" * 50)",
        "display line",
    ]))

    E.append(h2("3.5  Variable Scope & Lifetime"))
    for p in [
        "EnLang follows Python's scoping rules (LEGB: Local, Enclosing, Global, Built-in). Variables declared inside a function are local to that function and cannot be accessed outside it. Variables declared at the top level of a script are global and can be read inside functions, but to modify them inside a function you must declare them as global using the Python native escape.",
        "The EnLang static linter (enlang check) will warn about common scoping mistakes such as using a variable before it is defined, shadowing an outer variable, or attempting to modify a global variable without declaring it.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Global scope",
        "set server_name to \"Lumina\"",
        "set port to 8000",
        "",
        "function get_server_info():",
        "    # Can READ global variables",
        "    return server_name plus \" on port \" plus str(port)",
        "",
        "function reset_port(new_port):",
        "    # Must use native escape to MODIFY global",
        "    python:",
        "    global port",
        "    port = new_port",
        "    end python",
        "    display \"Port updated to \" plus str(port)",
        "",
        "display get_server_info()",
        "reset_port(9000)",
        "display get_server_info()",
    ]))
    E.append(hr())

    # ── CHAPTER 4 ────────────────────────────────────────────────────────
    E += chap("Output, Input & Terminal I/O Mastery", 4)

    for sub_num, sub_title, paragraphs, code_block in [
        ("4.1","The Four Output Keywords",[
            "EnLang provides four fully interchangeable output keywords: display, print, show, and output. All four compile to Python's print() function. The existence of four synonyms allows code to read naturally in different contexts — for example, 'display user_name' reads better in a UI context, while 'print error_message' reads better in a logging context.",
            "The choice of keyword does not affect the compiled output in any way. A developer can freely mix all four keywords in the same file without any effect on the program's behavior. This flexibility is intentional: it reflects the reality that natural English has many synonyms for the concept of 'showing information', and EnLang embraces this richness rather than imposing artificial constraints.",
            "All four keywords accept any valid EnLang expression as their argument — variables, string literals, arithmetic expressions, function calls, list displays, dictionary representations, or @python() escape expressions. The argument is automatically converted to a string by Python's print() function if it is not already a string.",
        ],[
            "display \"Welcome to EnLang v2.0\"",
            "print \"System initialized.\"",
            "show 42",
            "output true",
            "display [1, 2, 3, 4, 5]",
            "print {\"name\": \"Spandan\", \"role\": \"admin\"}",
            "show 3.14159 times 2",
            "output @python(f\"Computed: {10 ** 3}\")",
        ]),
        ("4.2","Formatted Output Patterns",[
            "Formatted output — aligning text in columns, displaying tables, formatting numbers, and printing borders — is essential for building clean terminal user interfaces. EnLang programs that display data to the terminal should use consistent formatting to maximize readability.",
            "The primary tools for formatted output in EnLang are Python's string formatting capabilities, accessed via @python() escapes. F-strings provide the most concise and readable syntax for embedding variables and expressions directly in output strings.",
        ],[
            "# Formatted alignment",
            "display @python(f\"{'Name':<20} {'Score':>8} {'Grade':>6}\")",
            "display @python(\"-\" * 38)",
            "",
            "set students to [[\"Spandan\",98,\"A+\"],[\"Bibhu\",87,\"A\"],[\"Deepak\",74,\"B\"]]",
            "for each s in students do:",
            "    display @python(f\"{s[0]:<20} {s[1]:>8} {s[2]:>6}\")",
            "",
            "# Number formatting",
            "set price to 1234567.89",
            "display @python(f\"Price: ${price:,.2f}\")",
            "display @python(f\"Pi: {3.14159265:.4f}\")",
            "display @python(f\"Hex: {255:#010x}\")",
            "display @python(f\"Binary: {42:08b}\")",
        ]),
        ("4.3","Terminal Input with ask & prompt",[
            "The 'ask ... and store in ...' form reads a line of input from the terminal and stores it in a variable. It is equivalent to Python's input() function and compiles directly to it. All terminal input is returned as a string, so you must convert it to the appropriate type using @python(int(...)) or @python(float(...)) if you need numeric input.",
            "The 'prompt ... and store in ...' form is a direct synonym for 'ask'. Both forms compile identically. For password input (where the typed characters should not be displayed), use the Python native escape with getpass.getpass().",
        ],[
            "# Basic input",
            "ask \"Enter your name: \" and store in user_name",
            "ask \"Enter your age: \" and store in age_str",
            "",
            "# Type conversion",
            "set age to @python(int(age_str))",
            "",
            "# Validated input loop",
            "set valid to false",
            "while not valid do:",
            "    ask \"Enter a number (1-100): \" and store in raw_input",
            "    try:",
            "        set num to @python(int(raw_input))",
            "        if num is greater than or equal to 1 and num is less than or equal to 100 then:",
            "            set valid to true",
            "        else:",
            "            display \"Error: must be 1-100. Try again.\"",
            "    except ValueError:",
            "        display \"Error: must be a number. Try again.\"",
            "",
            "display \"You entered: \" plus str(num)",
        ]),
    ]:
        E.append(h2(f"{sub_num}  {sub_title}"))
        for p in paragraphs:
            E.append(body(p))
        E.append(code(code_block))
    E.append(hr())

    # ── CHAPTER 5 ────────────────────────────────────────────────────────
    E += chap("Conditional Logic & Control Flow", 5)

    E.append(h2("5.1  The if / else if / else Decision Structure"))
    for p in [
        "Conditional statements are the foundation of all decision-making in programs. EnLang's conditional syntax uses 'if ... then:' for the primary branch, 'else if ... then:' for additional branches, and 'else:' for the default fallback branch. All three components are optional except the primary 'if' branch.",
        "The condition expression in an 'if' statement can be any valid boolean expression: a comparison operation, a function call that returns a boolean, a variable holding a boolean value, a compound condition using 'and'/'or'/'not', or an @python() expression that evaluates to a boolean.",
        "Blocks in EnLang MUST use exactly 4 spaces of indentation per level. The static linter will warn if indentation is not a multiple of 4, and the transpiler may produce incorrect Python if indentation is inconsistent. EnLang inherits Python's significant-whitespace requirement — indentation is not cosmetic; it is syntactically meaningful.",
        "The 'then:' keyword at the end of 'if' and 'else if' headers is optional but strongly recommended by the EnLang Style Guide. Including 'then:' makes conditions read as complete English sentences and helps the visual parser identify block boundaries more clearly. The colon ':' at the end is mandatory — the static linter will flag its absence as an ERROR.",
    ]:
        E.append(body(p))
    E.append(code([
        "set temperature to 35",
        "",
        "if temperature is greater than 40 then:",
        "    display \"DANGER: Extreme heat. Stay indoors.\"",
        "else if temperature is greater than 35 then:",
        "    display \"WARNING: Very hot. Drink water frequently.\"",
        "else if temperature is greater than 25 then:",
        "    display \"Pleasant weather. Enjoy outdoor activities.\"",
        "else if temperature is greater than 10 then:",
        "    display \"Cool weather. Light jacket recommended.\"",
        "else if temperature is greater than 0 then:",
        "    display \"Cold weather. Wear warm clothing.\"",
        "else:",
        "    display \"DANGER: Freezing conditions. Avoid going outside.\"",
    ]))

    E.append(h2("5.2  All Natural Comparison Operators"))
    E.append(tbl([
        ["EnLang Natural Expression","Symbol","Python","Compiled Output Example"],
        ["x is equal to y","==","x == y","if score is equal to 100 then:"],
        ["x is not equal to y","!=","x != y","if status is not equal to 'active' then:"],
        ["x is greater than y",">","x > y","if age is greater than 18 then:"],
        ["x is less than y","<","x < y","if balance is less than 0 then:"],
        ["x is greater than or equal to y",">=","x >= y","if score is greater than or equal to 60 then:"],
        ["x is less than or equal to y","<=","x <= y","if stock is less than or equal to 5 then:"],
        ["x is y","==","x == y","if role is \"admin\" then:"],
        ["x is not y","!=","x != y","if user is not None then:"],
        ["x is in y","in","x in y","if item is in cart then:"],
        ["x is not in y","not in","x not in y","if user is not in blacklist then:"],
    ],col_widths=[165,50,90,185]))

    E.append(h2("5.3  Compound Conditions"))
    E.append(body("Compound conditions combine multiple simple conditions using the 'and', 'or', and 'not' logical operators. These compile directly to Python's boolean operators with the same short-circuit evaluation behavior — 'and' evaluates the right side only if the left side is True, and 'or' evaluates the right side only if the left side is False."))
    E.append(code([
        "set age to 22",
        "set has_id to true",
        "set is_banned to false",
        "set credit_score to 750",
        "",
        "# AND — both conditions must be true",
        "if age is greater than or equal to 18 and has_id is equal to true then:",
        "    display \"Age verified and ID present — Access granted\"",
        "",
        "# OR — at least one condition must be true",
        "if age is less than 13 or age is greater than 65 then:",
        "    display \"Special pricing applies\"",
        "",
        "# NOT — inverts a boolean condition",
        "if not is_banned then:",
        "    display \"Account is in good standing\"",
        "",
        "# Complex compound condition",
        "if age is greater than or equal to 21 and not is_banned and credit_score is greater than 700 then:",
        "    display \"Premium credit limit approved\"",
    ]))

    E.append(h2("5.4  Nested Conditions"))
    E.append(code([
        "set role to \"admin\"",
        "set is_verified to true",
        "set has_2fa to true",
        "",
        "if role is equal to \"admin\" then:",
        "    if is_verified then:",
        "        if has_2fa then:",
        "            display \"Full admin access granted (2FA verified)\"",
        "        else:",
        "            display \"Admin access — 2FA setup required\"",
        "    else:",
        "        display \"Admin account pending email verification\"",
        "else if role is equal to \"editor\" then:",
        "    if is_verified then:",
        "        display \"Editor access: content modification allowed\"",
        "    else:",
        "        display \"Editor account pending verification\"",
        "else:",
        "    display \"Guest access: read-only mode\"",
    ]))
    E.append(hr())

    # ── CHAPTER 6 ────────────────────────────────────────────────────────
    E += chap("Comprehensive Loop Taxonomy — All Five Forms", 6)

    E.append(h2("6.1  The repeat N times do: Loop"))
    for p in [
        "The 'repeat N times do:' construct is EnLang's simplest loop form. It runs the indented block exactly N times. There is no loop variable — the loop counter is anonymous. N can be any integer expression: a literal number, a variable holding an integer, or an @python() expression that evaluates to an integer.",
        "This form compiles to Python's 'for _ in range(N):' pattern, where _ is the conventional throwaway variable name. It is the most readable loop form when the exact number of iterations is known in advance and the loop index is not needed inside the block.",
        "Common use cases include: retrying an operation a fixed number of times, printing a separator line a fixed number of times, running a benchmark or stress test a fixed number of times, and populating a data structure with a fixed number of default values.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Basic repeat loop",
        "repeat 5 times do:",
        "    display \"Iteration complete.\"",
        "",
        "# Repeat with a variable count",
        "set num_retries to 3",
        "repeat num_retries times do:",
        "    display \"Attempting connection...\"",
        "",
        "# Print a separator line",
        "repeat 50 times do:",
        "    @python(print('=', end=''))",
        "@python(print())",
        "",
        "# Nested repeat loops",
        "repeat 3 times do:",
        "    repeat 3 times do:",
        "        @python(print('* ', end=''))",
        "    @python(print())",
    ]))

    E.append(h2("6.2  The for each ... in ... do: Loop"))
    for p in [
        "The 'for each item in collection do:' form is the most commonly used loop in EnLang for iterating over existing data collections. It iterates over every element in a list, tuple, set, string, dictionary (keys by default), or any other Python iterable, executing the block once for each element.",
        "The loop variable (item in the example above) takes on each element's value in succession. It is fully accessible inside the block and can be used in any expression, condition, or function call. The collection can be any expression that produces an iterable — a literal list, a variable, a function call, an @python() expression, or a slice of an existing collection.",
        "This form compiles to Python's 'for item in collection:' pattern. The 'each' and 'do' keywords are optional extensions that make the sentence read more naturally in English, but neither is required by the transpiler. You may omit either or both of them.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Iterate over a list",
        "set fruits to [\"Apple\", \"Banana\", \"Cherry\", \"Durian\", \"Elderberry\"]",
        "",
        "for each fruit in fruits do:",
        "    display \"Processing: \" plus fruit",
        "",
        "# Iterate over a range",
        "for each i in @python(range(1, 11)) do:",
        "    display str(i) plus \" squared = \" plus str(i times i)",
        "",
        "# Iterate over dictionary keys",
        "set grades to {\"Alice\": 95, \"Bob\": 87, \"Charlie\": 91}",
        "",
        "for each student in grades do:",
        "    display student plus \": \" plus str(grades[student])",
        "",
        "# Iterate over dictionary items (key-value pairs)",
        "for each name, score in @python(grades.items()) do:",
        "    display @python(f\"{name}: {score}/100\")",
        "",
        "# Iterate over a string (character by character)",
        "set word to \"EnLang\"",
        "for each char in word do:",
        "    @python(print(char, end='-'))",
    ]))

    E.append(h2("6.3  The direct for ... in ...: Loop"))
    E.append(body("The direct 'for item in collection:' form (without 'each' and 'do') is identical in behavior to the for-each form. It is more concise and is preferred when the 'each' keyword does not add clarity:"))
    E.append(code([
        "for num in [1, 2, 3, 4, 5]:",
        "    set squared to num times num",
        "    display str(num) plus \" ** 2 = \" plus str(squared)",
        "",
        "# With enumerate (index + value)",
        "set colors to [\"Red\", \"Green\", \"Blue\", \"Yellow\"]",
        "for idx, color in @python(enumerate(colors, start=1)) do:",
        "    display str(idx) plus \". \" plus color",
        "",
        "# Zip two lists together",
        "set names to [\"Alice\", \"Bob\", \"Charlie\"]",
        "set scores to [95, 87, 91]",
        "",
        "for name, score in @python(zip(names, scores)) do:",
        "    display name plus \" scored \" plus str(score)",
    ]))

    E.append(h2("6.4  The while Loop — Two Forms"))
    E.append(code([
        "# Direct while (symbolic condition)",
        "set i to 1",
        "while i <= 10:",
        "    display i",
        "    set i to i plus 1",
        "",
        "# Natural English while (full phrase condition)",
        "set countdown to 10",
        "while countdown is greater than or equal to 0 do:",
        "    display countdown",
        "    decrement countdown by 1",
        "display \"Liftoff!\"",
        "",
        "# Infinite loop with break",
        "while true do:",
        "    ask \"Enter 'quit' to exit: \" and store in user_input",
        "    if user_input is equal to \"quit\" then:",
        "        break",
        "    display \"You said: \" plus user_input",
        "display \"Goodbye!\"",
    ]))

    E.append(h2("6.5  Loop Control: break & continue"))
    E.append(code([
        "# continue: skip current iteration, continue to next",
        "display \"Odd numbers from 1 to 20:\"",
        "for each n in @python(range(1, 21)) do:",
        "    if n mod 2 is equal to 0 then:",
        "        continue",
        "    display n",
        "",
        "# break: exit loop immediately",
        "display \"First perfect square over 50:\"",
        "for each n in @python(range(1, 100)) do:",
        "    if n times n is greater than 50 then:",
        "        display n",
        "        break",
        "",
        "# Nested loops with break (inner only)",
        "for i in @python(range(1, 6)):",
        "    for j in @python(range(1, 6)):",
        "        if j is equal to i then:",
        "            break",
        "        display str(i) plus \",\" plus str(j)",
    ]))

    E.append(h2("6.6  Nested Loops — Real-World Patterns"))
    E.append(code([
        "# Pattern 1: Number triangle",
        "for i in @python(range(1, 6)):",
        "    for j in @python(range(1, i + 1)):",
        "        @python(print(j, end=' '))",
        "    @python(print())",
        "",
        "# Pattern 2: Matrix traversal",
        "set matrix to [[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
        "for each row in matrix do:",
        "    for each element in row do:",
        "        @python(print(element, end='\\t'))",
        "    @python(print())",
        "",
        "# Pattern 3: Multiplication table",
        "for i in @python(range(1, 13)):",
        "    for j in @python(range(1, 13)):",
        "        @python(print(f'{i*j:4}', end=''))",
        "    @python(print())",
    ]))
    E.append(hr())

    # ── CHAPTER 7 ────────────────────────────────────────────────────────
    E += chap("Functions, Procedures & Functional Programming", 7)

    E.append(h2("7.1  Standard Function Signature"))
    for p in [
        "Functions are named, reusable blocks of code that perform a specific task. Defining a function in EnLang uses the 'function name(parameters):' syntax, which compiles directly to Python's 'def name(parameters):'. The function body is indented by 4 spaces and can contain any valid EnLang statements.",
        "Functions may optionally return a value using the 'return' keyword. If no return statement is reached, the function implicitly returns None (Python's null value). Functions can call other functions, including themselves (recursion). Functions can be passed as arguments to other functions (higher-order functions).",
        "Parameter names in function signatures are plain identifiers (no types required). To specify default values, use the @python() or Python native block to write the function signature in raw Python. Multiple parameters are separated by commas.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Single parameter",
        "function greet(name):",
        "    display \"Hello, \" plus name plus \"!\"",
        "",
        "# Multiple parameters",
        "function calculate_bmi(weight_kg, height_m):",
        "    set bmi to weight_kg divided by (height_m times height_m)",
        "    return @python(round(bmi, 2))",
        "",
        "# Return string from function",
        "function get_grade(score):",
        "    if score is greater than or equal to 90 then:",
        "        return \"A+\"",
        "    else if score is greater than or equal to 80 then:",
        "        return \"A\"",
        "    else if score is greater than or equal to 70 then:",
        "        return \"B\"",
        "    else if score is greater than or equal to 60 then:",
        "        return \"C\"",
        "    else:",
        "        return \"F\"",
        "",
        "# Calling functions",
        "greet(\"Spandan\")",
        "set my_bmi to calculate_bmi(70, 1.75)",
        "display \"BMI: \" plus str(my_bmi)",
        "",
        "set grade to get_grade(87)",
        "display \"Grade: \" plus grade",
    ]))

    E.append(h2("7.2  Natural English Function Declarations"))
    E.append(body("EnLang's most distinctive feature is its natural English function syntax. The table below shows all supported natural declaration keywords:"))
    E.append(tbl([
        ["Declaration Keyword","Compiles To","Supported Call Keywords"],
        ["function foo using n:","def foo(n):","start foo from n, call foo with n, run foo using n"],
        ["function foo taking n:","def foo(n):","start foo from n, call foo with n"],
        ["action foo given n:","def foo(n):","run foo using n, call foo with n"],
        ["task foo for n:","def foo(n):","start foo from n, run foo using n"],
        ["procedure foo with n:","def foo(n):","execute foo with n, perform foo with n"],
        ["process foo on n:","def foo(n):","apply foo on n, begin foo with n"],
    ],col_widths=[165,110,215]))
    E.append(code([
        "# Natural English function — counting recursion",
        "function numbers using n:",
        "    if n is greater than 10 then:",
        "        return",
        "    display n",
        "    call numbers with (n plus 1)",
        "",
        "start numbers from 1",
        "",
        "# Action-style declaration",
        "action process_order given order_id:",
        "    display \"Processing order: \" plus str(order_id)",
        "    display \"Order confirmed.\"",
        "",
        "run process_order using \"ORD-2026-001\"",
        "",
        "# Task-style declaration",
        "task send_notification for message:",
        "    display \"NOTIFICATION: \" plus message",
        "",
        "start send_notification from \"Server started successfully\"",
    ]))

    E.append(h2("7.3  Return Values & Multiple Returns"))
    E.append(code([
        "# Return a single value",
        "function square(n):",
        "    return n times n",
        "",
        "# Return multiple values (Python tuple unpacking)",
        "function min_max(numbers):",
        "    return @python(min(numbers)), @python(max(numbers))",
        "",
        "set data to [5, 2, 8, 1, 9, 3, 7]",
        "set lo, hi to min_max(data)",
        "display \"Min: \" plus str(lo) plus \", Max: \" plus str(hi)",
        "",
        "# Return dictionary (named return values)",
        "function get_stats(numbers):",
        "    set total to @python(sum(numbers))",
        "    set count to @python(len(numbers))",
        "    set average to total divided by count",
        "    return {\"total\": total, \"count\": count, \"average\": average,",
        "            \"min\": @python(min(numbers)), \"max\": @python(max(numbers))}",
        "",
        "set stats to get_stats([10, 20, 30, 40, 50])",
        "display \"Average: \" plus str(stats[\"average\"])",
    ]))
    E.append(hr())

    # ── CHAPTER 8 ────────────────────────────────────────────────────────
    E += chap("Recursion — Theory, Patterns & Classic Problems", 8)

    E.append(h2("8.1  Understanding Recursion"))
    for p in [
        "Recursion is a programming technique where a function calls itself during its execution. Every recursive solution consists of two parts: (1) the base case — a condition where the function returns a result without making a recursive call, preventing infinite recursion, and (2) the recursive case — where the function makes one or more recursive calls with a smaller or simpler version of the input, making progress toward the base case.",
        "Recursion is particularly elegant for problems that have a naturally recursive structure — problems where the solution to the whole problem can be expressed in terms of solutions to smaller instances of the same problem. Classic examples include tree traversal, divide-and-conquer algorithms, mathematical sequences (Fibonacci, factorial), and combinatorial problems (permutations, combinations).",
        "The main risk of recursion is stack overflow — if the recursion is too deep (Python's default recursion limit is 1000 levels), Python will raise a RecursionError. For problems that require deep recursion (e.g., large tree depths), consider either increasing the limit via @python(sys.setrecursionlimit(10000)) or converting to an iterative solution with an explicit stack.",
    ]:
        E.append(body(p))

    E.append(h2("8.2  Factorial — The Classic Recursive Problem"))
    E.append(code([
        "function factorial(n):",
        "    # Base case: 0! = 1 (by mathematical definition)",
        "    if n is equal to 0 then:",
        "        return 1",
        "    # Recursive case: n! = n * (n-1)!",
        "    return n times factorial(n minus 1)",
        "",
        "# Test factorial",
        "for i in @python(range(0, 13)):",
        "    display str(i) plus \"! = \" plus str(factorial(i))",
    ]))
    E.append(cout(["0! = 1","1! = 1","2! = 2","3! = 6","4! = 24","5! = 120","6! = 720","7! = 5040","8! = 40320","9! = 362880","10! = 3628800","11! = 39916800","12! = 479001600"]))

    E.append(h2("8.3  Fibonacci Sequence"))
    E.append(code([
        "# Naive recursive Fibonacci — O(2^n) time",
        "function fib_naive(n):",
        "    if n is less than or equal to 1 then:",
        "        return n",
        "    return fib_naive(n minus 1) plus fib_naive(n minus 2)",
        "",
        "# Memoized Fibonacci — O(n) time",
        "python:",
        "from functools import lru_cache",
        "",
        "@lru_cache(maxsize=None)",
        "def fib_memo(n):",
        "    if n <= 1: return n",
        "    return fib_memo(n-1) + fib_memo(n-2)",
        "end python",
        "",
        "# Print first 20 Fibonacci numbers",
        "for i in @python(range(20)):",
        "    display @python(f\"fib({i:2}) = {fib_memo(i)}\")",
        "",
        "# fib(50) — instant with memoization",
        "display @python(f\"fib(50) = {fib_memo(50)}\")",
    ]))

    E.append(h2("8.4  Tower of Hanoi"))
    E.append(code([
        "function hanoi(n, source, target, auxiliary):",
        "    if n is equal to 1 then:",
        "        display \"Move disk 1 from \" plus source plus \" to \" plus target",
        "        return",
        "    hanoi(n minus 1, source, auxiliary, target)",
        "    display \"Move disk \" plus str(n) plus \" from \" plus source plus \" to \" plus target",
        "    hanoi(n minus 1, auxiliary, target, source)",
        "",
        "hanoi(3, \"A\", \"C\", \"B\")",
    ]))

    E.append(h2("8.5  Recursive Data Structures — Tree Traversal"))
    E.append(code([
        "python:",
        "class TreeNode:",
        "    def __init__(self, value):",
        "        self.value = value",
        "        self.left = None",
        "        self.right = None",
        "",
        "def insert_bst(root, value):",
        "    if root is None:",
        "        return TreeNode(value)",
        "    if value < root.value:",
        "        root.left = insert_bst(root.left, value)",
        "    else:",
        "        root.right = insert_bst(root.right, value)",
        "    return root",
        "",
        "def inorder(node):",
        "    if node is None: return",
        "    inorder(node.left)",
        "    print(node.value, end=' ')",
        "    inorder(node.right)",
        "",
        "root = None",
        "for val in [5, 3, 7, 1, 4, 6, 8]:",
        "    root = insert_bst(root, val)",
        "",
        "print('Inorder (sorted):', end=' ')",
        "inorder(root)",
        "print()",
        "end python",
    ]))
    E.append(hr())

    # ── CHAPTER 9 ────────────────────────────────────────────────────────
    E += chap("Pattern Matching — match / case / default", 9)

    E.append(h2("9.1  The match Block Structure"))
    for p in [
        "The match statement is EnLang's structural pattern matching construct, inspired by Python 3.10's match-case statement but made more readable through natural English framing. It provides a clean alternative to long if-elif-else chains when a single variable is being compared against multiple discrete values.",
        "A match block must begin with 'match expression:' and end with 'end match'. Inside the block, each branch is defined with 'case value:' (for a specific value match) or 'default:' (for the fallback branch when no case matches). Each case block is indented by 4 spaces and can contain any number of statements.",
        "Multiple values can be handled by a single case using comma separation: 'case \"Monday\", \"Tuesday\":' will match either value. The 'default:' branch (equivalent to else in an if-chain) is optional but recommended to handle unexpected values gracefully.",
    ]:
        E.append(body(p))
    E.append(code([
        "set http_code to 403",
        "",
        "match http_code:",
        "    case 200:",
        "        display \"200 OK — Request successful\"",
        "        set status to \"success\"",
        "    case 201:",
        "        display \"201 Created — Resource created successfully\"",
        "        set status to \"created\"",
        "    case 204:",
        "        display \"204 No Content — Success with no response body\"",
        "        set status to \"no_content\"",
        "    case 301, 302:",
        "        display \"3xx Redirect — Resource has moved\"",
        "        set status to \"redirect\"",
        "    case 400:",
        "        display \"400 Bad Request — Malformed request syntax\"",
        "        set status to \"bad_request\"",
        "    case 401:",
        "        display \"401 Unauthorized — Authentication required\"",
        "        set status to \"unauthorized\"",
        "    case 403:",
        "        display \"403 Forbidden — Access denied for this resource\"",
        "        set status to \"forbidden\"",
        "    case 404:",
        "        display \"404 Not Found — Requested resource does not exist\"",
        "        set status to \"not_found\"",
        "    case 422:",
        "        display \"422 Unprocessable Entity — Validation failed\"",
        "        set status to \"validation_error\"",
        "    case 429:",
        "        display \"429 Too Many Requests — Rate limit exceeded\"",
        "        set status to \"rate_limited\"",
        "    case 500:",
        "        display \"500 Internal Server Error — Something went wrong\"",
        "        set status to \"server_error\"",
        "    case 503:",
        "        display \"503 Service Unavailable — Server is down\"",
        "        set status to \"service_unavailable\"",
        "    default:",
        "        display \"Unknown HTTP status code: \" plus str(http_code)",
        "        set status to \"unknown\"",
        "end match",
        "",
        "display \"Status key: \" plus status",
    ]))
    E.append(hr())

    # ── CHAPTER 10 ────────────────────────────────────────────────────────
    E += chap("Exception Handling, Error Control & Defensive Programming", 10)

    E.append(h2("10.1  The try / except / finally Triad"))
    for p in [
        "Exception handling is the mechanism by which a program gracefully recovers from unexpected errors instead of crashing. In EnLang, the try/except/finally triad works identically to Python: the 'try:' block contains the code that might raise an exception, the 'except:' block handles the exception if one occurs, and the 'finally:' block runs unconditionally whether or not an exception occurred — making it ideal for cleanup operations like closing files, releasing locks, or logging completion.",
        "The 'except:' clause (without a specific exception type) catches all exceptions. This is convenient but generally poor practice in production code, as it may silently swallow unexpected errors. Prefer catching specific exception types (ValueError, TypeError, FileNotFoundError, etc.) so that truly unexpected errors propagate up the call stack where they can be properly logged and investigated.",
        "EnLang supports the full Python exception hierarchy. Any exception class available in Python's standard library or installed packages can be caught in an EnLang except clause using @python() escape if the class name is not a natural EnLang keyword.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Basic try/except",
        "try:",
        "    set result to 100 divided by 0",
        "except:",
        "    display \"Caught division by zero!\"",
        "",
        "# Typed exception catching",
        "try:",
        "    set num to @python(int(\"not_a_number\"))",
        "except ValueError as e:",
        "    display \"ValueError: \" plus str(e)",
        "except TypeError as e:",
        "    display \"TypeError: \" plus str(e)",
        "except:",
        "    display \"Unexpected error occurred\"",
        "finally:",
        "    display \"This always runs — cleanup complete\"",
        "",
        "# File operation with exception handling",
        "try:",
        "    read file \"config.json\" and store in config_text",
        "    set config to @python(__import__('json').loads(config_text))",
        "    display \"Config loaded: \" plus str(config)",
        "except FileNotFoundError:",
        "    display \"Config file not found. Using defaults.\"",
        "    set config to {\"debug\": false, \"port\": 8000}",
        "except @python(__import__('json').JSONDecodeError) as e:",
        "    display \"Invalid JSON in config: \" plus str(e)",
        "    set config to {\"debug\": false, \"port\": 8000}",
        "finally:",
        "    display \"Config initialization complete.\"",
    ]))
    E.append(hr())

    # ── CHAPTER 11 ────────────────────────────────────────────────────────
    E += chap("Collections Mastery: Lists, Dicts, Sets & Tuples", 11)

    E.append(h2("11.1  Lists — The Primary Collection Type"))
    for p in [
        "Lists are ordered, mutable sequences that can hold elements of any type (including mixed types). They are the most frequently used collection type in EnLang and Python. Lists preserve insertion order, allow duplicate values, and support indexed access (both positive and negative indexing).",
        "EnLang provides natural English aliases for the most common list operations: 'add item to list' (append), 'remove item from list' (remove), and direct indexed access with list[index]. For less common operations, use @python() escapes.",
    ]:
        E.append(body(p))
    E.append(code([
        "# Create lists",
        "set empty_list to []",
        "set fruits to [\"Apple\", \"Banana\", \"Cherry\", \"Durian\"]",
        "set numbers to [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
        "set mixed to [\"hello\", 42, 3.14, true, null]",
        "",
        "# Add elements",
        "add \"Elderberry\" to fruits",
        "add 11 to numbers",
        "",
        "# Remove elements",
        "remove \"Banana\" from fruits",
        "",
        "# Indexed access",
        "set first to fruits[0]         # Apple",
        "set last to @python(fruits[-1]) # Elderberry",
        "",
        "# Slice",
        "set sub to @python(numbers[2:5])  # [3, 4, 5]",
        "set reversed_list to @python(numbers[::-1])",
        "",
        "# Length",
        "set size to @python(len(fruits))",
        "display \"Fruit count: \" plus str(size)",
        "",
        "# Sort",
        "set sorted_fruits to @python(sorted(fruits))",
        "set sorted_nums to @python(sorted(numbers, reverse=True))",
        "",
        "# List comprehension",
        "set squares to @python([x**2 for x in range(1, 11)])",
        "set even_squares to @python([x**2 for x in range(1, 11) if x % 2 == 0])",
        "",
        "# Flatten nested list",
        "set matrix to [[1,2,3],[4,5,6],[7,8,9]]",
        "set flat to @python([n for row in matrix for n in row])",
    ]))

    E.append(h2("11.2  Dictionaries — Key-Value Hash Maps"))
    E.append(code([
        "# Create dictionary",
        "set user to {",
        "    \"id\": 1001,",
        "    \"username\": \"spandan\",",
        "    \"email\": \"spandan@enlang.org\",",
        "    \"role\": \"admin\",",
        "    \"is_active\": true,",
        "    \"login_count\": 142",
        "}",
        "",
        "# Access values",
        "display user[\"username\"]",
        "display @python(user.get('email', 'not set'))",
        "",
        "# Update values",
        "set user[\"login_count\"] to user[\"login_count\"] plus 1",
        "",
        "# Add new key-value pair",
        "set user[\"last_login\"] to \"2026-07-25 09:30:00\"",
        "",
        "# Delete key",
        "python:",
        "del user['is_active']",
        "end python",
        "",
        "# Check key existence",
        "if @python('email' in user) then:",
        "    display \"Email: \" plus user[\"email\"]",
        "",
        "# Iterate over key-value pairs",
        "for key, value in @python(user.items()) do:",
        "    display str(key) plus \" : \" plus str(value)",
        "",
        "# Dictionary comprehension",
        "set square_map to @python({x: x**2 for x in range(1, 11)})",
    ]))

    E.append(h2("11.3  Sets — Unique Unordered Collections"))
    E.append(code([
        "set set_a to {1, 2, 3, 4, 5}",
        "set set_b to {3, 4, 5, 6, 7, 8}",
        "",
        "# Union — all elements from both sets",
        "set union to @python(set_a | set_b)",
        "display union     # {1, 2, 3, 4, 5, 6, 7, 8}",
        "",
        "# Intersection — elements in both sets",
        "set intersect to @python(set_a & set_b)",
        "display intersect  # {3, 4, 5}",
        "",
        "# Difference — in set_a but not set_b",
        "set diff_a to @python(set_a - set_b)",
        "display diff_a    # {1, 2}",
        "",
        "# Symmetric difference — in one but not both",
        "set sym_diff to @python(set_a ^ set_b)",
        "display sym_diff  # {1, 2, 6, 7, 8}",
        "",
        "# Is subset?",
        "set small to {3, 4}",
        "display @python(small.issubset(set_a))  # True",
        "",
        "# Remove duplicates from list",
        "set raw to [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]",
        "set unique to @python(list(set(raw)))",
    ]))
    E.append(hr())

    # ── CHAPTER 12 ────────────────────────────────────────────────────────
    E += chap("String Operations, Text Processing & Regex", 12)

    E.append(h2("12.1  Complete String Methods Reference"))
    E.append(tbl([
        ["Method","EnLang / Python","Description","Example"],
        ["strip()","@python(s.strip())","Remove leading/trailing whitespace","'  hi  '.strip() -> 'hi'"],
        ["lower()","@python(s.lower())","Convert to lowercase","'HELLO'.lower() -> 'hello'"],
        ["upper()","@python(s.upper())","Convert to uppercase","'hello'.upper() -> 'HELLO'"],
        ["title()","@python(s.title())","Title case each word","'hello world'.title() -> 'Hello World'"],
        ["replace(a,b)","@python(s.replace(a,b))","Replace all occurrences of a with b","'cat'.replace('c','b') -> 'bat'"],
        ["split(sep)","@python(s.split(sep))","Split into list on separator","'a,b,c'.split(',') -> ['a','b','c']"],
        ["join(list)","@python(sep.join(list))","Join list into string","','.join(['a','b']) -> 'a,b'"],
        ["find(sub)","@python(s.find(sub))","Index of first occurrence (-1 if absent)","'hello'.find('ll') -> 2"],
        ["startswith(p)","@python(s.startswith(p))","True if string starts with p","'hello'.startswith('he') -> True"],
        ["endswith(s)","@python(s.endswith(s))","True if string ends with s","'hello'.endswith('lo') -> True"],
        ["count(sub)","@python(s.count(sub))","Count occurrences of sub","'banana'.count('a') -> 3"],
        ["zfill(n)","@python(s.zfill(n))","Pad with zeros to width n","'42'.zfill(5) -> '00042'"],
        ["center(n)","@python(s.center(n))","Center string in field of width n","'hi'.center(10) -> '    hi    '"],
        ["isdigit()","@python(s.isdigit())","True if all characters are digits","'123'.isdigit() -> True"],
        ["isalpha()","@python(s.isalpha())","True if all characters are letters","'abc'.isalpha() -> True"],
    ],col_widths=[80,130,145,135]))

    E.append(h2("12.2  Regular Expressions via @python()"))
    E.append(code([
        "import module re",
        "",
        "# Test email address format",
        "set email to \"spandan@enlang.org\"",
        "set email_pattern to @python(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')",
        "if @python(re.match(email_pattern, email)) then:",
        "    display email plus \" is a valid email address\"",
        "",
        "# Extract all numbers from a string",
        "set text to \"Order 123 contains 45 items worth $678.90\"",
        "set numbers_found to @python(re.findall(r'\\d+\\.?\\d*', text))",
        "display numbers_found",
        "",
        "# Replace pattern",
        "set sentence to \"The   quick   brown   fox\"",
        "set normalized to @python(re.sub(r'\\s+', ' ', sentence))",
        "display normalized",
        "",
        "# Split on multiple delimiters",
        "set data to \"apple;banana,cherry|durian\"",
        "set items to @python(re.split(r'[;,|]', data))",
        "display items",
    ]))
    E.append(hr())

    # ── CHAPTER 13 ────────────────────────────────────────────────────────
    E += chap("Algorithms, Sorting, Searching & Complexity", 13)

    E.append(h2("13.1  Sorting Algorithms Implemented in EnLang"))
    E.append(code([
        "# Bubble Sort — O(n^2) time, O(1) space",
        "function bubble_sort(arr):",
        "    set n to @python(len(arr))",
        "    for i in @python(range(n)):",
        "        for j in @python(range(0, n - i - 1)):",
        "            if arr[j] is greater than arr[j plus 1] then:",
        "                python:",
        "                arr[j], arr[j+1] = arr[j+1], arr[j]",
        "                end python",
        "    return arr",
        "",
        "# Selection Sort — O(n^2) time, O(1) space",
        "function selection_sort(arr):",
        "    set n to @python(len(arr))",
        "    for i in @python(range(n)):",
        "        set min_idx to i",
        "        for j in @python(range(i + 1, n)):",
        "            if arr[j] is less than arr[min_idx] then:",
        "                set min_idx to j",
        "        python:",
        "        arr[i], arr[min_idx] = arr[min_idx], arr[i]",
        "        end python",
        "    return arr",
        "",
        "# Insertion Sort — O(n^2) worst, O(n) best, stable",
        "function insertion_sort(arr):",
        "    for i in @python(range(1, len(arr))):",
        "        set key to arr[i]",
        "        set j to i minus 1",
        "        while j >= 0 and arr[j] > key:",
        "            set arr[j plus 1] to arr[j]",
        "            set j to j minus 1",
        "        set arr[j plus 1] to key",
        "    return arr",
        "",
        "# Test all three",
        "set data to [64, 34, 25, 12, 22, 11, 90]",
        "display bubble_sort(@python(data[:]))",
        "display selection_sort(@python(data[:]))",
        "display insertion_sort(@python(data[:]))",
    ]))

    E.append(h2("13.2  Merge Sort — O(n log n) Divide & Conquer"))
    E.append(code([
        "function merge_sort(arr):",
        "    if @python(len(arr)) is less than or equal to 1 then:",
        "        return arr",
        "    set mid to @python(len(arr) // 2)",
        "    set left to merge_sort(@python(arr[:mid]))",
        "    set right to merge_sort(@python(arr[mid:]))",
        "    return merge(left, right)",
        "",
        "function merge(left, right):",
        "    set result to []",
        "    set i to 0",
        "    set j to 0",
        "    while i < @python(len(left)) and j < @python(len(right)):",
        "        if left[i] is less than or equal to right[j] then:",
        "            add left[i] to result",
        "            set i to i plus 1",
        "        else:",
        "            add right[j] to result",
        "            set j to j plus 1",
        "    set result to @python(result + left[i:] + right[j:])",
        "    return result",
        "",
        "set data to [38, 27, 43, 3, 9, 82, 10]",
        "display merge_sort(data)",
    ]))

    E.append(h2("13.3  Quick Sort — Average O(n log n)"))
    E.append(code([
        "function quick_sort(arr):",
        "    if @python(len(arr)) is less than or equal to 1 then:",
        "        return arr",
        "    set pivot to arr[@python(len(arr) // 2)]",
        "    set left to @python([x for x in arr if x < pivot])",
        "    set middle to @python([x for x in arr if x == pivot])",
        "    set right to @python([x for x in arr if x > pivot])",
        "    return @python(quick_sort(left) + middle + quick_sort(right))",
        "",
        "set data to [3, 6, 8, 10, 1, 2, 1]",
        "display quick_sort(data)",
    ]))
    E.append(tbl([
        ["Algorithm","Time (Best)","Time (Avg)","Time (Worst)","Space","Stable?"],
        ["Bubble Sort","O(n)","O(n²)","O(n²)","O(1)","Yes"],
        ["Selection Sort","O(n²)","O(n²)","O(n²)","O(1)","No"],
        ["Insertion Sort","O(n)","O(n²)","O(n²)","O(1)","Yes"],
        ["Merge Sort","O(n log n)","O(n log n)","O(n log n)","O(n)","Yes"],
        ["Quick Sort","O(n log n)","O(n log n)","O(n²)","O(log n)","No"],
        ["Heap Sort","O(n log n)","O(n log n)","O(n log n)","O(1)","No"],
        ["Tim Sort (Python)","O(n)","O(n log n)","O(n log n)","O(n)","Yes"],
    ],col_widths=[95,75,75,75,60,60]))
    E.append(hr())

    # ── CHAPTER 14 ────────────────────────────────────────────────────────
    E += chap("File I/O, System Operations & Cryptographic Security", 14)

    E.append(h2("14.1  Text File Operations"))
    E.append(code([
        "# Write a new file (overwrites existing)",
        "write \"Line 1: Server started\" to file \"server.log\"",
        "",
        "# Read a file's complete content",
        "read file \"server.log\" and store in log_content",
        "display log_content",
        "",
        "# Append to existing file",
        "python:",
        "with open('server.log', 'a', encoding='utf-8') as f:",
        "    f.write('\\nLine 2: Connection established')",
        "    f.write('\\nLine 3: Processing request')",
        "end python",
        "",
        "# Read file line by line",
        "python:",
        "with open('server.log', 'r', encoding='utf-8') as f:",
        "    for line_num, line in enumerate(f, start=1):",
        "        print(f'[{line_num}] {line.rstrip()}')",
        "end python",
        "",
        "# Write structured data as JSON",
        "import module json",
        "set config to {\"debug\": true, \"port\": 8000, \"host\": \"localhost\"}",
        "python:",
        "with open('config.json', 'w') as f:",
        "    json.dump(config, f, indent=2)",
        "end python",
    ]))

    E.append(h2("14.2  Directory Operations"))
    E.append(code([
        "import module os",
        "",
        "# List directory contents",
        "set files to @python(os.listdir('.'))",
        "for each file_name in files do:",
        "    display file_name",
        "",
        "# Create directory",
        "python:",
        "os.makedirs('output/logs', exist_ok=True)",
        "end python",
        "",
        "# Walk directory tree",
        "python:",
        "for dirpath, dirnames, filenames in os.walk('.'):",
        "    for filename in filenames:",
        "        if filename.endswith('.enlg'):",
        "            print(os.path.join(dirpath, filename))",
        "end python",
        "",
        "# File metadata",
        "set file_size to @python(os.path.getsize('server.log'))",
        "set mod_time to @python(os.path.getmtime('server.log'))",
        "display \"Size: \" plus str(file_size) plus \" bytes\"",
    ]))
    E.append(hr())

    # Additional chapters — deeply expanded ────────────────────────────────
    for ch_num, ch_title, sections in [
        (15, "Classes, OOP & Design Patterns", [
            ("15.1", "Class Definition & Instantiation", [
                "Classes are blueprints for creating objects. In EnLang, all class definitions use the Python native block, since class-related syntax maps directly to Python's class system without needing natural English transformation.",
            ], [
                "python:",
                "class BankAccount:",
                "    def __init__(self, owner, balance=0.0):",
                "        self.owner = owner",
                "        self.balance = balance",
                "        self.transactions = []",
                "",
                "    def deposit(self, amount):",
                "        if amount <= 0: raise ValueError('Amount must be positive')",
                "        self.balance += amount",
                "        self.transactions.append(('deposit', amount))",
                "",
                "    def withdraw(self, amount):",
                "        if amount > self.balance: raise ValueError('Insufficient funds')",
                "        self.balance -= amount",
                "        self.transactions.append(('withdrawal', amount))",
                "",
                "    def statement(self):",
                "        print(f'Account: {self.owner}')",
                "        print(f'Balance: ${self.balance:,.2f}')",
                "        for t_type, t_amt in self.transactions:",
                "            print(f'  {t_type}: ${t_amt:,.2f}')",
                "",
                "acc = BankAccount('Spandan', 1000.0)",
                "acc.deposit(500.0)",
                "acc.withdraw(200.0)",
                "acc.statement()",
                "end python",
            ]),
            ("15.2", "Inheritance & Method Overriding", [
                "Inheritance allows a new class to derive all attributes and methods from an existing parent class, then add or override specific behaviors. This is the primary mechanism for code reuse in object-oriented programming.",
            ], [
                "python:",
                "class Shape:",
                "    def __init__(self, color='black'):",
                "        self.color = color",
                "    def area(self): return 0",
                "    def __str__(self): return f'{self.color} {type(self).__name__}'",
                "",
                "class Circle(Shape):",
                "    def __init__(self, radius, color='blue'):",
                "        super().__init__(color)",
                "        self.radius = radius",
                "    def area(self): return 3.14159 * self.radius ** 2",
                "",
                "class Rectangle(Shape):",
                "    def __init__(self, width, height, color='red'):",
                "        super().__init__(color)",
                "        self.width = width",
                "        self.height = height",
                "    def area(self): return self.width * self.height",
                "",
                "shapes = [Circle(5, 'cyan'), Rectangle(4, 6, 'magenta'), Circle(3)]",
                "for s in shapes:",
                "    print(f'{s}: area = {s.area():.2f}')",
                "end python",
            ]),
        ]),
        (16, "Modules, Packages & EPM Deep Dive", [
            ("16.1", "Standard Library Modules", [
                "Python's standard library — accessible via 'import module' in EnLang — provides hundreds of pre-built modules covering math, datetime, file I/O, JSON, CSV, HTTP, cryptography, threading, and much more. You never need to install these — they are bundled with every Python installation.",
            ], [
                "# Essential standard library modules",
                "import module os",
                "import module sys",
                "import module math",
                "import module json",
                "import module datetime",
                "import module random",
                "import module re",
                "import module time",
                "import module collections",
                "import module itertools",
                "import module functools",
                "",
                "# datetime usage",
                "set now to @python(datetime.datetime.now())",
                "display @python(f'Current time: {now.strftime(\"%Y-%m-%d %H:%M:%S\")}')",
                "",
                "# random number generation",
                "set rand_int to @python(random.randint(1, 100))",
                "set rand_float to @python(random.uniform(0.0, 1.0))",
                "set rand_choice to @python(random.choice(['Alpha', 'Beta', 'Gamma']))",
                "display rand_int",
                "display @python(f'{rand_float:.4f}')",
                "display rand_choice",
                "",
                "# collections — Counter, defaultdict, deque",
                "set words to @python('the quick brown fox jumps over the lazy dog'.split())",
                "set word_count to @python(__import__('collections').Counter(words))",
                "display @python(word_count.most_common(3))",
            ]),
            ("16.2", "Third-Party Libraries via EPM", [
                "Beyond the standard library, EnLang programs can use any of the 500,000+ packages on PyPI. The EnLang Package Manager (EPM) provides a high-level interface for installing and managing these dependencies, storing them in the project's enlang.json file for reproducible installs.",
            ], [
                "# Install packages via EPM",
                "epm add py:requests        # HTTP client library",
                "epm add py:flask           # Web framework",
                "epm add py:pandas          # Data analysis",
                "epm add py:numpy           # Numerical computing",
                "epm add py:pillow          # Image processing",
                "epm add py:cryptography    # Cryptographic primitives",
                "epm add py:pydantic        # Data validation",
                "epm add py:sqlalchemy      # ORM & database toolkit",
                "",
                "# Using requests to call an API",
                "python:",
                "import requests",
                "response = requests.get('https://httpbin.org/json')",
                "if response.status_code == 200:",
                "    data = response.json()",
                "    print('Slideshow title:', data['slideshow']['title'])",
                "else:",
                "    print(f'API error: {response.status_code}')",
                "end python",
            ]),
        ]),
    ]:
        E += chap(ch_title, ch_num)
        for sub_num, sub_title, paragraphs, code_block in sections:
            E.append(h2(f"{sub_num}  {sub_title}"))
            for p in paragraphs:
                E.append(body(p))
            E.append(code(code_block))
        E.append(hr())

    # ── MASSIVE REFERENCE SECTIONS ─────────────────────────────────────────
    E += chap("EnLang Complete Syntax Reference & Quick-Look Tables", 17)

    E.append(h2("17.1  The Full Grammar Expression Replacement Table"))
    E.append(body("The following table lists every natural English expression that EnLang's grammar engine recognizes and its corresponding Python replacement. This is the authoritative reference for what EnLang can transpile automatically:"))
    E.append(tbl([
        ["Natural English","Python Output","Notes"],
        ["is equal to","==","Comparison"],
        ["is not equal to","!=","Comparison"],
        ["is greater than or equal to",">=","Comparison"],
        ["is less than or equal to","<=","Comparison"],
        ["is greater than",">","Comparison"],
        ["is less than","<","Comparison"],
        ["is in","in","Membership"],
        ["is not in","not in","Membership"],
        ["is not","!=","Comparison"],
        ["is true","== True","Boolean"],
        ["is false","== False","Boolean"],
        ["true","True","Boolean literal"],
        ["false","False","Boolean literal"],
        ["null / none","None","Null literal"],
        ["plus","+","Arithmetic"],
        ["minus","-","Arithmetic"],
        ["times","*","Arithmetic"],
        ["divided by","/","Arithmetic"],
        ["modulo / mod","%","Modulus"],
        ["power of","**","Exponentiation"],
        ["and","and","Logical"],
        ["or","or","Logical"],
        ["not","not","Logical"],
    ],col_widths=[160,130,200]))

    E.append(h2("17.2  Variable Operations Quick Reference"))
    E.append(tbl([
        ["EnLang Statement","Python Equivalent","Description"],
        ["set x to val","x = val","Assign value"],
        ["let x = val","x = val","Assign (JS-style)"],
        ["store val in x","x = val","Assign (reverse)"],
        ["define number x as val","x = val  # type: int","Type-annotated assign"],
        ["increment x by n","x += n","Add n to x"],
        ["decrement x by n","x -= n","Subtract n from x"],
        ["multiply x by n","x *= n","Multiply x by n"],
        ["divide x by n","x /= n","Divide x by n"],
        ["add item to list","list.append(item)","List append"],
        ["remove item from list","list.remove(item)","List remove"],
        ["hash s with sha256 store in h","h = hashlib.sha256(s.encode()).hexdigest()","Hash"],
        ["write text to file path","open(path,'w').write(text)","File write"],
        ["read file path store in v","v = open(path).read()","File read"],
        ["check if path P exists store in v","v = os.path.exists(P)","Path check"],
        ["get environment variable NAME store in v","v = os.getenv('NAME')","Env var"],
        ["import module name","import name","Module import"],
        ["analyze sentiment of s store in v","v = nlp_engine.sentiment(s)","NLP"],
        ["extract keywords from s into v","v = nlp_engine.keywords(s)","NLP"],
    ],col_widths=[180,165,145]))

    E.append(h2("17.3  Control Flow Quick Reference"))
    E.append(tbl([
        ["EnLang Construct","Python Output","Notes"],
        ["if X then: / if X:","if X:","Condition required"],
        ["else if X then:","elif X:","Chained condition"],
        ["else:","else:","Default branch"],
        ["repeat N times do:","for _ in range(N):","Count loop"],
        ["for each i in c do:","for i in c:","Iterator loop"],
        ["for i in c:","for i in c:","Iterator (direct)"],
        ["while X do: / while X:","while X:","Conditional loop"],
        ["break","break","Exit loop"],
        ["continue","continue","Skip iteration"],
        ["return val","return val","Function return"],
        ["raise T with message m","raise T(m)","Exception raise"],
        ["throw error m","raise Exception(m)","Exception throw"],
        ["try: ... except: ...","try: ... except: ...","Exception handling"],
        ["finally:","finally:","Cleanup block"],
        ["match x: case v: end match","match x: case v:","Pattern match"],
    ],col_widths=[175,140,175]))
    E.append(hr())

    # ── CHAPTER 18 — .enlgf (HTML) full deep dive ──────────────────────────
    E += chap("Frontend Structural Markup — .enlgf to HTML5 Full Reference", 18)

    E.append(h2("18.1  .enlgf File Overview & Compilation Model"))
    for p in [
        "EnLang Frontend files (.enlgf) compile to HTML5 using the frontend sub-transpiler, which maps natural English phrases to HTML5 elements and attributes. The compilation is strictly 1:1: each EnLang markup statement produces exactly one HTML element or attribute. There are no default styles injected, no CSS classes assumed, and no JavaScript automatically included.",
        "The .enlgf format is designed to produce clean, semantic, accessible HTML5 that validates against the W3C HTML5 specification. Screen readers, search engines, and assistive technologies benefit from the structured semantic output.",
        "The compilation chain for a complete web page is: .enlgf -> HTML5 (structure) + .enlgd -> CSS3 (style) + .enlgs -> JavaScript ES6+ (behavior). These three files work together and reference each other through standard HTML link and script tags.",
    ]:
        E.append(body(p))
    E.append(code([
        "# full_page.enlgf — Complete modern web page",
        "page title \"Lumina Platform — Dashboard\"",
        "page charset \"UTF-8\"",
        "page viewport \"width=device-width, initial-scale=1.0\"",
        "page description \"Lumina: The AI-Powered Workspace Platform\"",
        "link stylesheet \"styles.css\"",
        "link stylesheet \"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap\"",
        "script src \"app.js\" defer \"true\"",
        "",
        "create header with class \"site-header\":",
        "    create div with class \"container\":",
        "        create div with class \"navbar\":",
        "            create a with href \"/\" with class \"brand\":",
        "                create span with class \"brand-icon\" with text \"⚡\"",
        "                create span with class \"brand-name\" with text \"Lumina\"",
        "            close a",
        "            create nav with id \"main-nav\" with role \"navigation\":",
        "                create a with href \"#dashboard\" with text \"Dashboard\"",
        "                create a with href \"#analytics\" with text \"Analytics\"",
        "                create a with href \"#projects\" with text \"Projects\"",
        "                create a with href \"#settings\" with text \"Settings\"",
        "            close nav",
        "            create div with class \"header-actions\":",
        "                create button with id \"notifBtn\" with class \"icon-btn\" with aria-label \"Notifications\":",
        "                    create span with text \"🔔\"",
        "                close button",
        "                create button with id \"avatarBtn\" with class \"avatar-btn\":",
        "                    create span with text \"SP\"",
        "                close button",
        "            close div",
        "        close div",
        "    close div",
        "close header",
        "",
        "create main with id \"app\" with role \"main\":",
        "    create section with id \"dashboard\" with class \"dashboard-section\":",
        "        create div with class \"container\":",
        "            create h1 with text \"Welcome back, Spandan\"",
        "            create p with text \"Here is your workspace overview for today.\"",
        "            create div with class \"stats-grid\":",
        "                create article with class \"stat-card\":",
        "                    create span with class \"stat-number\" with text \"142\"",
        "                    create span with class \"stat-label\" with text \"Active Projects\"",
        "                close article",
        "                create article with class \"stat-card\":",
        "                    create span with class \"stat-number\" with text \"98.2%\"",
        "                    create span with class \"stat-label\" with text \"Uptime SLA\"",
        "                close article",
        "                create article with class \"stat-card\":",
        "                    create span with class \"stat-number\" with text \"2.4k\"",
        "                    create span with class \"stat-label\" with text \"API Calls Today\"",
        "                close article",
        "            close div",
        "        close div",
        "    close section",
        "close main",
        "",
        "create footer with class \"site-footer\":",
        "    create p with text \"© 2026 Lumina Platform. Powered by EnLang.\"",
        "close footer",
    ]))
    E.append(hr())

    # ── CHAPTER 19 — .enlgd full deep dive ─────────────────────────────────
    E += chap("Styling & Design Systems — .enlgd to CSS3 Full Reference", 19)

    E.append(h2("19.1  The enlgd Design Philosophy"))
    for p in [
        "EnLang Design files (.enlgd) compile to CSS3 using the design sub-transpiler. The design system is centered around three core concepts: design tokens (theme variables), component styles (rule sets for HTML elements and classes), and responsive rules (media queries for different screen sizes).",
        "The 'define theme' block is the most powerful feature of .enlgd. It defines a named design system with semantic color tokens, spacing scales, typography settings, and component defaults. Once a theme is defined, its values can be referenced throughout the stylesheet as CSS custom properties (CSS variables), enabling consistent, maintainable design systems.",
    ]:
        E.append(body(p))
    E.append(code([
        "# lumina_design.enlgd — Complete Dark Mode Design System",
        "",
        "define theme luminaDark:",
        "    primary: \"#4338ca\"",
        "    primary-hover: \"#3730a3\"",
        "    secondary: \"#818cf8\"",
        "    background: \"#0f172a\"",
        "    surface: \"#1e293b\"",
        "    surface-elevated: \"#334155\"",
        "    border: \"#475569\"",
        "    text-primary: \"#f8fafc\"",
        "    text-secondary: \"#94a3b8\"",
        "    text-muted: \"#64748b\"",
        "    success: \"#4ade80\"",
        "    warning: \"#fbbf24\"",
        "    danger: \"#f87171\"",
        "    info: \"#38bdf8\"",
        "    radius-sm: \"4px\"",
        "    radius-md: \"8px\"",
        "    radius-lg: \"16px\"",
        "    radius-full: \"9999px\"",
        "    shadow-sm: \"0 1px 3px rgba(0,0,0,0.3)\"",
        "    shadow-md: \"0 4px 12px rgba(0,0,0,0.4)\"",
        "    shadow-lg: \"0 20px 60px rgba(0,0,0,0.5)\"",
        "end theme",
        "",
        "# Global reset & base",
        "style *, *::before, *::after:",
        "    box-sizing: \"border-box\"",
        "    margin: \"0\"",
        "    padding: \"0\"",
        "",
        "style body:",
        "    font-family: \"'Inter', -apple-system, BlinkMacSystemFont, sans-serif\"",
        "    font-size: \"16px\"",
        "    line-height: \"1.6\"",
        "    background-color: \"#0f172a\"",
        "    color: \"#f8fafc\"",
        "    min-height: \"100vh\"",
        "",
        "# Navigation",
        "style \".site-header\":",
        "    background: \"rgba(15, 23, 42, 0.95)\"",
        "    border-bottom: \"1px solid #475569\"",
        "    position: \"sticky\"",
        "    top: \"0\"",
        "    z-index: \"1000\"",
        "    backdrop-filter: \"blur(12px)\"",
        "",
        "style \".navbar\":",
        "    display: \"flex\"",
        "    align-items: \"center\"",
        "    justify-content: \"space-between\"",
        "    padding: \"16px 0\"",
        "",
        "# Stat cards",
        "style \".stats-grid\":",
        "    display: \"grid\"",
        "    grid-template-columns: \"repeat(auto-fit, minmax(200px, 1fr))\"",
        "    gap: \"24px\"",
        "    margin: \"32px 0\"",
        "",
        "style \".stat-card\":",
        "    background: \"#1e293b\"",
        "    border: \"1px solid #475569\"",
        "    border-radius: \"12px\"",
        "    padding: \"24px\"",
        "    display: \"flex\"",
        "    flex-direction: \"column\"",
        "    gap: \"8px\"",
        "    transition: \"transform 0.2s ease, box-shadow 0.2s ease\"",
        "",
        "style \".stat-card:hover\":",
        "    transform: \"translateY(-4px)\"",
        "    box-shadow: \"0 20px 60px rgba(0,0,0,0.5)\"",
        "",
        "style \".stat-number\":",
        "    font-size: \"2.5rem\"",
        "    font-weight: \"700\"",
        "    color: \"#818cf8\"",
        "",
        "# Responsive breakpoints",
        "style \"@media (max-width: 768px)\":",
        "    .navbar: {flex-direction: column; gap: 16px}",
        "    .stats-grid: {grid-template-columns: 1fr}",
        "    h1: {font-size: 1.8rem}",
    ]))
    E.append(hr())

    # ── CHAPTER 20 — .enlgs JavaScript ─────────────────────────────────────
    E += chap("Client-Side Scripting — .enlgs to JavaScript ES6+ Full Reference", 20)

    E.append(h2("20.1  .enlgs Compilation Model"))
    E.append(body("EnLang Script files (.enlgs) compile to JavaScript ES6+ for client-side browser execution. The JavaScript sub-transpiler maps EnLang natural phrases to JS DOM API calls, event handlers, async patterns, and ES6 module syntax."))
    E.append(code([
        "# lumina_app.enlgs — Complete client application",
        "",
        "log \"Lumina Client App v2.0 initializing...\"",
        "",
        "# DOM ready event",
        "on load window do:",
        "    log \"DOM fully loaded\"",
        "    initialize_dashboard()",
        "    setup_event_listeners()",
        "",
        "async function initialize_dashboard():",
        "    try:",
        "        set stats to await fetch_dashboard_stats()",
        "        render_stats(stats)",
        "    except:",
        "        log \"Failed to load dashboard stats\"",
        "",
        "async function fetch_dashboard_stats():",
        "    set response to await @js(fetch('/api/dashboard/stats', {",
        "        method: 'GET',",
        "        headers: { 'Content-Type': 'application/json' }",
        "    }))",
        "    if @js(response.ok) then:",
        "        return await @js(response.json())",
        "    else:",
        "        throw @js(new Error(`API Error: ${response.status}`))",
        "",
        "function setup_event_listeners():",
        "    on click \"notifBtn\" do:",
        "        toggle_panel(\"notifications-panel\")",
        "    on click \"avatarBtn\" do:",
        "        toggle_panel(\"user-menu-panel\")",
        "",
        "function toggle_panel(panel_id):",
        "    set panel to @js(document.getElementById(panel_id))",
        "    if @js(panel.style.display) is equal to \"block\" then:",
        "        set @js(panel.style.display) to \"none\"",
        "    else:",
        "        set @js(panel.style.display) to \"block\"",
    ]))
    E.append(hr())

    # ── CHAPTER 21 — .enlgdb ────────────────────────────────────────────────
    E += chap("Database Engineering — .enlgdb to SQL Full Reference", 21)

    E.append(h2("21.1  Complete Schema Definition Example"))
    E.append(code([
        "# schema.enlgdb — Lumina Platform Database Schema",
        "",
        "connect to database \"lumina.db\" as db",
        "",
        "# Users table",
        "define table users with columns:",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    username TEXT NOT NULL UNIQUE,",
        "    email TEXT NOT NULL UNIQUE,",
        "    password_hash TEXT NOT NULL,",
        "    salt TEXT NOT NULL,",
        "    role TEXT NOT NULL DEFAULT 'user',",
        "    is_active INTEGER NOT NULL DEFAULT 1,",
        "    email_verified INTEGER NOT NULL DEFAULT 0,",
        "    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,",
        "    last_login DATETIME,",
        "    login_count INTEGER NOT NULL DEFAULT 0",
        "",
        "# Projects table",
        "define table projects with columns:",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    name TEXT NOT NULL,",
        "    description TEXT,",
        "    owner_id INTEGER NOT NULL REFERENCES users(id),",
        "    status TEXT NOT NULL DEFAULT 'active',",
        "    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,",
        "    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "",
        "# Create indexes",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)\"",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id)\"",
        "execute sql \"CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)\"",
        "",
        "# Seed data",
        "insert record into users with values NULL, 'spandan', 'spandan@enlang.org',",
        "    '$pbkdf2$hash$', '$salt$', 'admin', 1, 1, CURRENT_TIMESTAMP, NULL, 0",
    ]))
    E.append(hr())

    # ── CHAPTERS 22–25 continued ─────────────────────────────────────────────
    E += chap("Web Server Engine & HTTP API Architecture", 22)
    E.append(h2("22.1  Built-In HTTP Server"))
    E.append(body("EnLang's built-in web server launches a production-ready HTTP server on any port. It handles routing, static file serving, and JSON API responses automatically."))
    E.append(code([
        "# api_server.enlg — Full REST API Server",
        "import module json",
        "import module os",
        "",
        "set VERSION to \"2.0.0\"",
        "set PORT to @python(int(os.getenv('PORT', '8000')))",
        "",
        "display \"EnLang API Server v\" plus VERSION",
        "display \"Starting on port \" plus str(PORT) plus \"...\"",
        "",
        "start web server on port PORT",
    ]))
    E.append(h2("22.2  Multi-File Application Assembly"))
    E.append(code([
        "# Run the complete full-stack application:",
        "",
        "# Step 1: Compile frontend markup",
        "enlang build static/index.enlgf",
        "",
        "# Step 2: Compile design system",
        "enlang build static/styles.enlgd",
        "",
        "# Step 3: Compile client script",
        "enlang build static/app.enlgs",
        "",
        "# Step 4: Set up database schema",
        "enlang run database/schema.enlgdb",
        "",
        "# Step 5: Start backend server",
        "enlang run server.enlg",
    ]))
    E.append(hr())

    E += chap("NLP, AI Primitives & Intelligent Features", 23)
    E.append(h2("23.1  Built-In NLP Engine"))
    E.append(body("EnLang includes a built-in NLP engine (enlang_core/nlp_engine.py) that provides sentiment analysis, keyword extraction, and text similarity scoring without requiring external API calls or LLM subscriptions. The NLP engine uses rule-based and statistical methods for lightweight, offline natural language processing."))
    E.append(code([
        "# nlp_demo.enlg — NLP Capabilities Demo",
        "",
        "set reviews to [",
        "    \"EnLang is absolutely incredible! The syntax is so natural.\",",
        "    \"I had some trouble with the installation process.\",",
        "    \"The compiler is fast and the documentation is excellent.\",",
        "    \"This language is not for me. Too different from what I know.\",",
        "    \"Fantastic developer experience. Highly recommended!\"",
        "]",
        "",
        "display \"=== Sentiment Analysis Results ===\"",
        "for each review in reviews do:",
        "    analyze sentiment of review and store in sentiment",
        "    if sentiment is greater than 0.3 then:",
        "        set label to \"POSITIVE\"",
        "    else if sentiment is less than -0.3 then:",
        "        set label to \"NEGATIVE\"",
        "    else:",
        "        set label to \"NEUTRAL\"",
        "    display label plus \": \" plus @python(review[:50]) plus \"...\"",
    ]))
    E.append(hr())

    E += chap("Developer Tooling — Linter, Checker & Debugger Complete Guide", 24)
    E.append(h2("24.1  Static Analysis Engine Architecture"))
    for p in [
        "The EnLang Static Syntax Checker (enlang_core/checker.py) implements a multi-pass analysis pipeline that reads EnLang source files and produces a structured diagnostic report without executing the program. This is analogous to ESLint for JavaScript, flake8 for Python, or rustc's borrow checker for Rust.",
        "Pass 1 (Line-Level Checks): For each line in the source file, the checker validates indentation (must be multiples of 4 spaces), block header colon presence (if/for/while/function lines must end with ':'), and unclosed string literals (unmatched quotes).",
        "Pass 2 (Phrase-Level Checks): Each non-comment, non-blank line is checked against the known EnLang grammar phrase dictionary. Any comparison or assignment phrase that is not in the canonical phrase list triggers an ERROR with a suggestion for the correct canonical form.",
        "Pass 3 (Block-Level Checks): The checker tracks match blocks and interface blocks across the entire file, reporting missing 'end match' or 'end interface' terminators.",
    ]:
        E.append(body(p))

    E.append(h2("24.2  Linter Error & Warning Reference"))
    E.append(tbl([
        ["Error ID","Severity","Trigger Condition","Suggested Fix"],
        ["UNCLOSED_STRING","ERROR","Line contains odd number of unescaped quotes","Close the string with matching quote"],
        ["MISSING_COLON","ERROR","Block header line has no trailing ':'","Add ':' at end of if/for/while/function line"],
        ["BAD_PHRASE","ERROR","Non-canonical comparison phrase detected","Use canonical EnLang phrase from grammar table"],
        ["BAD_INDENT","WARNING","Indentation not a multiple of 4","Adjust to nearest multiple of 4 spaces"],
        ["UNCLOSED_MATCH","ERROR","'match' block has no 'end match'","Add 'end match' after last case"],
        ["UNCLOSED_IFACE","ERROR","'interface' block has no 'end interface'","Add 'end interface' at end of block"],
        ["ASSIGN_PHRASE","ERROR","Unknown assignment phrase used","Use 'set x to val' or 'store val in x'"],
    ],col_widths=[100,65,185,140]))
    E.append(hr())

    E += chap("Interactive Debugger — Complete Session Guide", 25)
    E.append(h2("25.1  How the Debugger Works Internally"))
    E.append(body("The EnLang debugger (enlang_core/debugger.py) works by first transpiling the .enlg source file to Python, then using Python's built-in sys.settrace() mechanism to intercept execution at each line boundary. At each line, the debugger pauses and waits for developer input, displaying the current line number and content. The developer can step through lines one at a time, inspect variables, set breakpoints, or evaluate arbitrary expressions in the current execution frame."))
    E.append(code([
        "# Start a debug session",
        "$ enlang debug calculator.enlg",
        "[DEBUG] File loaded: calculator.enlg (15 lines)",
        "[DEBUG] Python transpilation: OK",
        "[DEBUG] Starting execution at line 1...",
        "",
        "> Line 1: set x to 42",
        "Debugger>> s",
        "",
        "> Line 2: set y to 18",
        "Debugger>> v",
        "Variables: {'x': 42}",
        "Debugger>> s",
        "",
        "> Line 3: set result to x plus y",
        "Debugger>> s",
        "",
        "> Line 4: display result",
        "Debugger>> e result",
        "eval(result) = 60",
        "Debugger>> b 10",
        "[DEBUG] Breakpoint set at line 10",
        "Debugger>> c",
        "60",
        "> Line 10: display 'Done'",
        "Debugger>> q",
        "[DEBUG] Debugger session ended.",
    ]))
    E.append(hr())

    E += chap("Canonical Grammar, Reserved Keywords & Style Guide", 26)
    E.append(h2("26.1  Complete Reserved Keywords Reference"))
    E.append(body("The following is the complete list of all reserved keywords in EnLang. These words have special meaning in the grammar engine and should not be used as variable names, function names, or identifiers:"))
    for cat, words in [
        ("Output & Display", "display, print, show, output"),
        ("Variable Declaration", "set, let, store, define, as, in, to, into"),
        ("Type Names", "number, decimal, text, boolean, list, dictionary, set, tuple"),
        ("Conditional", "if, else, then"),
        ("Loops", "repeat, times, do, for, each, while, break, continue"),
        ("Functions", "function, action, task, procedure, process, return, using, taking, given, for"),
        ("Function Calls", "start, call, run, execute, begin, perform, next, apply, from, with"),
        ("Exceptions", "try, except, finally, raise, throw, error, message"),
        ("Pattern Match", "match, case, default, end"),
        ("Boolean", "true, false, and, or, not, is"),
        ("Math", "plus, minus, times, divided, by, mod, modulo, power"),
        ("Comparison", "equal, greater, less, than, or, equal, to"),
        ("I/O", "write, read, ask, prompt, check, exists, path, file, hash, with"),
        ("Collections", "add, remove, get, environment, variable"),
        ("Modules", "import, module"),
        ("Native Escape", "@python, @js, python, end python, end js"),
        ("NLP", "analyze, sentiment, extract, keywords, compute, similarity, between"),
        ("Server", "start, web, server, on, port"),
    ]:
        E.append(bul(f"<b>{cat}:</b> {words}"))

    E.append(h2("26.2  Naming Conventions (EnLang Style Guide)"))
    E.append(tbl([
        ["Identifier Type","Convention","Example","Notes"],
        ["Variables","snake_case","user_name, total_price","All lowercase, underscores"],
        ["Functions","snake_case","calculate_tax, get_user","All lowercase, verb phrases"],
        ["Constants","UPPER_SNAKE_CASE","MAX_CONNECTIONS, API_KEY","All caps, underscores"],
        ["Classes (native)","PascalCase","BankAccount, UserProfile","Capital first letter each word"],
        ["File names (.enlg)","snake_case","main_server.enlg","Lowercase, underscores"],
        ["File names (.enlgf)","snake_case","index.enlgf, dashboard.enlgf","Lowercase, underscores"],
    ],col_widths=[110,100,155,125]))
    E.append(hr())

    # ── TESTING CHAPTER ─────────────────────────────────────────────────────
    E += chap("Testing, Quality Assurance & Continuous Integration", 27)
    E.append(h2("27.1  Test Pyramid for EnLang Projects"))
    for p in [
        "The test pyramid defines three levels of tests: unit tests (many, fast, isolated — test individual functions and modules), integration tests (medium, test interactions between components), and end-to-end tests (few, slow, test the complete user journey from input to output).",
        "For EnLang projects, unit tests are written in Python using pytest and import the enlang_core transpiler directly. They test individual grammar rules, transpilation patterns, and engine functions. Integration tests test the full enlang run pipeline on sample .enlg files and verify the expected output.",
    ]:
        E.append(body(p))
    E.append(code([
        "# tests/test_transpiler_unit.py",
        "import pytest",
        "import sys, os",
        "sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))",
        "from enlang_core.transpiler import transpile",
        "",
        "class TestVariableAssignment:",
        "    def test_set_to(self):",
        "        assert 'x = 10' in transpile('set x to 10', '.enlg')",
        "",
        "    def test_store_in(self):",
        "        assert 'x = 10' in transpile('store 10 in x', '.enlg')",
        "",
        "    def test_let_equals(self):",
        "        assert 'x = 10' in transpile('let x = 10', '.enlg')",
        "",
        "class TestControlFlow:",
        "    def test_if_greater_than(self):",
        "        result = transpile('if x is greater than 5 then:', '.enlg')",
        "        assert 'if x > 5:' in result",
        "",
        "    def test_for_each(self):",
        "        result = transpile('for each i in items do:', '.enlg')",
        "        assert 'for i in items:' in result",
        "",
        "    def test_while(self):",
        "        result = transpile('while count is less than 10 do:', '.enlg')",
        "        assert 'while count < 10:' in result",
        "",
        "class TestFunctions:",
        "    def test_natural_function_using(self):",
        "        result = transpile('function foo using n:', '.enlg')",
        "        assert 'def foo(n):' in result",
        "",
        "    def test_natural_call_start_from(self):",
        "        result = transpile('start foo from 1', '.enlg')",
        "        assert 'foo(1)' in result",
        "",
        "if __name__ == '__main__':",
        "    pytest.main([__file__, '-v'])",
    ]))
    E.append(hr())

    # ── SECURITY CHAPTER ────────────────────────────────────────────────────
    E += chap("Security Engineering — Input Validation, Hashing & Attack Prevention", 28)
    E.append(h2("28.1  OWASP Top 10 Applied to EnLang Applications"))
    E.append(body("The OWASP Top 10 is the authoritative list of the most critical web application security risks. Every EnLang web application developer should understand and mitigate these risks:"))
    E.append(tbl([
        ["OWASP Rank","Vulnerability","EnLang Mitigation"],
        ["A01","Broken Access Control","Role-based checks in all API routes; never trust client-side role claims"],
        ["A02","Cryptographic Failures","Use pbkdf2_hmac for passwords; AES-256 for sensitive data; HTTPS always"],
        ["A03","Injection (SQL/XSS/etc.)","Parameterized SQL queries; escape HTML output; validate all inputs"],
        ["A04","Insecure Design","Use threat modeling; secure defaults; defense in depth"],
        ["A05","Security Misconfiguration","Remove debug=True in production; restrict CORS; least-privilege DB user"],
        ["A06","Vulnerable Components","Regularly run 'pip audit'; keep enlang and all deps updated"],
        ["A07","Auth & Session Failures","Use PBKDF2/bcrypt; rotate tokens; implement 2FA; short session lifetimes"],
        ["A08","Software Integrity Failures","Pin dependency versions in enlang.json; verify package checksums"],
        ["A09","Security Logging Failures","Log all auth events, errors, and admin actions with timestamps and IPs"],
        ["A10","Server-Side Request Forgery","Validate and whitelist all URLs in server-side HTTP client calls"],
    ],col_widths=[50,130,310]))
    E.append(hr())

    # ── PERFORMANCE CHAPTER ─────────────────────────────────────────────────
    E += chap("Performance Optimization, Profiling & Scaling", 29)
    E.append(h2("29.1  Profiling EnLang Applications"))
    E.append(code([
        "# Profile a full EnLang program execution",
        "python:",
        "import cProfile, pstats, io",
        "",
        "profiler = cProfile.Profile()",
        "profiler.enable()",
        "",
        "# ---- Your EnLang-generated code here ----",
        "# (Run your enlang program via exec() or import)",
        "result = [x**2 for x in range(1000000)]",
        "# ---- End of profiled code ----",
        "",
        "profiler.disable()",
        "buffer = io.StringIO()",
        "stats = pstats.Stats(profiler, stream=buffer)",
        "stats.sort_stats('cumulative')",
        "stats.print_stats(15)",
        "print(buffer.getvalue())",
        "end python",
    ]))
    E.append(h2("29.2  Async & Concurrent Programming Patterns"))
    E.append(code([
        "# Async HTTP requests — fetch 10 URLs concurrently",
        "python:",
        "import asyncio",
        "import aiohttp",
        "",
        "async def fetch_url(session, url):",
        "    async with session.get(url) as response:",
        "        return await response.text()",
        "",
        "async def fetch_all(urls):",
        "    async with aiohttp.ClientSession() as session:",
        "        tasks = [fetch_url(session, url) for url in urls]",
        "        return await asyncio.gather(*tasks)",
        "",
        "urls = [f'https://httpbin.org/delay/1?id={i}' for i in range(5)]",
        "results = asyncio.run(fetch_all(urls))",
        "print(f'Fetched {len(results)} pages concurrently')",
        "end python",
    ]))
    E.append(hr())

    # ── PRODUCTION CASE STUDIES ──────────────────────────────────────────────
    E += chap("Production Case Studies — Five Complete Applications", 30)

    E.append(h2("30.1  Case Study: FX Currency Converter CLI"))
    E.append(code([
        "# fx_converter.enlg — Production-grade currency converter",
        "import module json",
        "import module datetime",
        "",
        "set EXCHANGE_RATES to {",
        "    \"USD\": 1.00000, \"EUR\": 0.91823, \"GBP\": 0.79154, \"JPY\": 157.234,",
        "    \"INR\": 83.512, \"CAD\": 1.36124, \"AUD\": 1.52341, \"CHF\": 0.89234,",
        "    \"CNY\": 7.24312, \"BRL\": 5.12341, \"MXN\": 17.3214, \"SGD\": 1.34124",
        "}",
        "",
        "function convert(amount, from_curr, to_curr):",
        "    if not @python(from_curr in EXCHANGE_RATES) then:",
        "        raise ValueError with message \"Unknown currency: \" plus from_curr",
        "    if not @python(to_curr in EXCHANGE_RATES) then:",
        "        raise ValueError with message \"Unknown currency: \" plus to_curr",
        "    set usd to amount divided by EXCHANGE_RATES[from_curr]",
        "    set result to usd times EXCHANGE_RATES[to_curr]",
        "    return @python(round(result, 4))",
        "",
        "function show_all_rates(amount, from_curr):",
        "    display @python(f\"\\n{amount} {from_curr} = \")",
        "    for each curr in @python(sorted(EXCHANGE_RATES.keys())) do:",
        "        if curr is not equal to from_curr then:",
        "            set converted to convert(amount, from_curr, curr)",
        "            display @python(f\"  {curr:6}: {converted:>12,.4f}\")",
        "",
        "display \"=\" times 50",
        "display \"  ENLANG FX CURRENCY CONVERTER v2.0\"",
        "display \"=\" times 50",
        "display \"Supported: \" plus @python(', '.join(sorted(EXCHANGE_RATES.keys())))",
        "",
        "while true do:",
        "    display \"\"",
        "    ask \"Amount (or 'quit'): \" and store in amt_input",
        "    if amt_input is equal to \"quit\" then:",
        "        break",
        "    try:",
        "        set amount to @python(float(amt_input))",
        "        ask \"From currency: \" and store in from_c",
        "        set from_c to @python(from_c.strip().upper())",
        "        ask \"To currency (or 'ALL'): \" and store in to_c",
        "        set to_c to @python(to_c.strip().upper())",
        "        if to_c is equal to \"ALL\" then:",
        "            show_all_rates(amount, from_c)",
        "        else:",
        "            set result to convert(amount, from_c, to_c)",
        "            display @python(f\"{amount:,.4f} {from_c} = {result:,.4f} {to_c}\")",
        "    except ValueError as e:",
        "        display \"Error: \" plus str(e)",
        "",
        "display \"Thank you for using EnLang FX Converter!\"",
    ]))

    E.append(h2("30.2  Case Study: Student Grade Management System"))
    E.append(code([
        "# grade_system.enlg — Complete student records management",
        "",
        "set students to {}",
        "",
        "function add_student(student_id, name):",
        "    if @python(student_id in students) then:",
        "        display \"Student ID already exists!\"",
        "        return",
        "    set students[student_id] to {",
        "        \"name\": name,",
        "        \"grades\": {},",
        "        \"gpa\": 0.0",
        "    }",
        "    display \"Added: \" plus name plus \" (ID: \" plus str(student_id) plus \")\"",
        "",
        "function add_grade(student_id, subject, score):",
        "    if not @python(student_id in students) then:",
        "        display \"Student not found!\"",
        "        return",
        "    set students[student_id][\"grades\"][subject] to score",
        "    recalculate_gpa(student_id)",
        "",
        "function recalculate_gpa(student_id):",
        "    set grades to students[student_id][\"grades\"]",
        "    if @python(len(grades)) is equal to 0 then:",
        "        return",
        "    set total to @python(sum(grades.values()))",
        "    set count to @python(len(grades))",
        "    set gpa to @python(round(total / count, 2))",
        "    set students[student_id][\"gpa\"] to gpa",
        "",
        "function print_report():",
        "    display \"\\n\" plus \"=\" times 60",
        "    display @python(f\"{'ID':>6} {'Name':<20} {'GPA':>6} {'Subjects':>8}\")",
        "    display \"=\" times 60",
        "    for each sid, data in @python(students.items()) do:",
        "        display @python(f\"{sid:>6} {data['name']:<20} {data['gpa']:>6.2f} {len(data['grades']):>8}\")",
        "",
        "# Demo usage",
        "add_student(1001, \"Spandan Prayas Patra\")",
        "add_student(1002, \"Bibhu Ranjan Das\")",
        "add_student(1003, \"Deepak Kumar Singh\")",
        "",
        "add_grade(1001, \"Mathematics\", 98)",
        "add_grade(1001, \"Physics\", 95)",
        "add_grade(1001, \"Computer Science\", 100)",
        "add_grade(1002, \"Mathematics\", 87)",
        "add_grade(1002, \"Physics\", 82)",
        "add_grade(1003, \"Mathematics\", 75)",
        "add_grade(1003, \"Computer Science\", 91)",
        "",
        "print_report()",
    ]))

    E.append(h2("30.3  Case Study: Crypto Price Tracker"))
    E.append(code([
        "# crypto_tracker.enlg — Real-time crypto monitoring",
        "import module json",
        "",
        "# Simulated crypto prices (in real app: fetch from API)",
        "set prices to {",
        "    \"BTC\": {\"name\": \"Bitcoin\", \"price\": 67432.50, \"change_24h\": 2.34},",
        "    \"ETH\": {\"name\": \"Ethereum\", \"price\": 3521.75, \"change_24h\": -1.12},",
        "    \"SOL\": {\"name\": \"Solana\", \"price\": 172.30, \"change_24h\": 5.67},",
        "    \"ADA\": {\"name\": \"Cardano\", \"price\": 0.582, \"change_24h\": -0.45},",
        "    \"DOT\": {\"name\": \"Polkadot\", \"price\": 8.94, \"change_24h\": 1.23},",
        "}",
        "",
        "function print_price_table():",
        "    display \"=\" times 65",
        "    display @python(f\"{'Symbol':<8} {'Name':<15} {'Price USD':>14} {'24h Change':>12}\")",
        "    display \"=\" times 65",
        "    for each symbol, data in @python(prices.items()) do:",
        "        set change to data[\"change_24h\"]",
        "        if change is greater than 0 then:",
        "            set arrow to \"↑\"",
        "        else:",
        "            set arrow to \"↓\"",
        "        display @python(f\"{symbol:<8} {data['name']:<15} ${data['price']:>13,.2f} {arrow}{abs(change):>10.2f}%\")",
        "    display \"=\" times 65",
        "",
        "print_price_table()",
        "",
        "function get_portfolio_value(holdings):",
        "    set total to 0",
        "    for each symbol, amount in @python(holdings.items()) do:",
        "        if @python(symbol in prices) then:",
        "            set value to prices[symbol][\"price\"] times amount",
        "            set total to total plus value",
        "            display @python(f\"{amount} {symbol} = ${value:,.2f}\")",
        "    display \"Total Portfolio: $\" plus @python(f'{total:,.2f}')",
        "    return total",
        "",
        "set my_portfolio to {\"BTC\": 0.5, \"ETH\": 3.0, \"SOL\": 20}",
        "display \"\\nMy Portfolio:\"",
        "get_portfolio_value(my_portfolio)",
    ]))

    # ── APPENDICES ───────────────────────────────────────────────────────────
    E += chap("APPENDIX A: Universal Natural Syntax Matrix — Complete Reference")

    E.append(tbl([
        ["Category","EnLang Natural","Python Compiled","Notes"],
        ["Output","display x","print(x)","Recommended form"],
        ["Output","print x","print(x)","Alias"],
        ["Output","show x","print(x)","Alias"],
        ["Output","output x","print(x)","Alias"],
        ["Assign","set x to val","x = val","Primary form"],
        ["Assign","let x = val","x = val","JS-style alias"],
        ["Assign","store val in x","x = val","Reverse form"],
        ["Annotated","define number x as val","x = val # int","Type hint form"],
        ["Add","add item to list","list.append(item)","List append"],
        ["Remove","remove item from list","list.remove(item)","List remove"],
        ["Increment","increment x by n","x += n","In-place add"],
        ["Decrement","decrement x by n","x -= n","In-place sub"],
        ["If","if x then: / if x is equal to y then:","if x: / if x == y:","Condition"],
        ["Elif","else if x then:","elif x:","Chained"],
        ["Else","else:","else:","Default"],
        ["For-Each","for each i in c do:","for i in c:","Iterator"],
        ["For-Direct","for i in c:","for i in c:","Direct"],
        ["Repeat","repeat N times do:","for _ in range(N):","Count"],
        ["While","while x do: / while x is less than n do:","while x: / while x < n:","Conditional"],
        ["Break","break","break","Loop exit"],
        ["Continue","continue","continue","Loop skip"],
        ["Function","function foo(n):","def foo(n):","Standard"],
        ["Function","function foo using n:","def foo(n):","Natural"],
        ["Call","start foo from 1","foo(1)","Natural"],
        ["Call","call foo with 1","foo(1)","Natural"],
        ["Call","run foo using 1","foo(1)","Natural"],
        ["Return","return x","return x","Function return"],
        ["Match","match x: case v: default: end match","match x: case v:","Pattern match"],
        ["Try","try: ... except E: ... finally:","try: ... except E: ... finally:","Exceptions"],
        ["Raise","raise T with message m","raise T(m)","Exception raise"],
        ["Throw","throw error m","raise Exception(m)","Shorthand raise"],
        ["Import","import module name","import name","Module import"],
        ["File Write","write t to file p","open(p,'w').write(t)","File output"],
        ["File Read","read file p and store in v","v=open(p).read()","File input"],
        ["Hash","hash s with sha256 store in h","h=hashlib.sha256(s.encode()).hexdigest()","Security"],
        ["Env Var","get environment variable K store in v","v=os.getenv(K)","Environment"],
        ["Path Check","check if path P exists store in v","v=os.path.exists(P)","File system"],
        ["Sentiment","analyze sentiment of s store in v","v=nlp_engine.sentiment(s)","NLP"],
        ["Keywords","extract keywords from s into v","v=nlp_engine.keywords(s)","NLP"],
        ["Web Server","start web server on port N","server.serve(N)","HTTP server"],
        ["Native (inline)","@python(expr)","expr","Direct escape"],
        ["Native (block)","python: ... end python","Python block","Multi-line"],
    ],col_widths=[65,155,170,100]))

    E += chap("APPENDIX B: CLI Operations Complete Manual")
    E.append(tbl([
        ["Command","Full Syntax","Description","Example"],
        ["run","enlang run <file>","Compile & execute","enlang run app.enlg"],
        ["build","enlang build <file>","Transpile only","enlang build index.enlgf"],
        ["check","enlang check <file>","Lint & analyze","enlang check main.enlg"],
        ["debug","enlang debug <file>","Step debugger","enlang debug calc.enlg"],
        ["server","enlang server --port N","HTTP server","enlang server --port 8080"],
        ["version","enlang version","Print version","enlang version"],
        ["help","enlang help [cmd]","Show help","enlang help check"],
        ["epm init","epm init","New project","epm init"],
        ["epm add","epm add py:pkg","Add PyPI dep","epm add py:requests"],
        ["epm add","epm add web:pkg","Add web dep","epm add web:chart.js"],
        ["epm install","epm install","Install all deps","epm install"],
        ["epm list","epm list","Show packages","epm list"],
        ["epm remove","epm remove pkg","Remove package","epm remove requests"],
        ["epm update","epm update","Update packages","epm update"],
        ["epm publish","epm publish","Publish to EPM","epm publish"],
    ],col_widths=[55,130,130,175]))

    E += chap("APPENDIX C: Comprehensive Practice Exercises — 50 Problems")
    E.append(h2("C.1  Beginner Level (Problems 1–15)"))
    for i, ex in enumerate([
        "Write an EnLang program that displays 'Hello, [your name]!' and 'I am learning EnLang!'",
        "Write a program that stores your name, age, city, and favorite language as variables and displays a formatted introduction.",
        "Write a calculator that asks for two numbers and an operator (+, -, *, /) and performs the operation.",
        "Write a temperature converter that converts Celsius to Fahrenheit and Kelvin.",
        "Write a program that uses 'repeat 12 times do:' to print the numbers 1 through 12.",
        "Write a program that stores 10 countries in a list and displays them numbered.",
        "Write a program that checks if a number is positive, negative, or zero.",
        "Write a program that checks if a year is a leap year (divisible by 4, not 100, or divisible by 400).",
        "Write a program that calculates the area and perimeter of a circle given its radius.",
        "Write a program that counts from 1 to 100 and displays only multiples of 7.",
        "Write a grade calculator: 90-100=A+, 80-89=A, 70-79=B, 60-69=C, below=F.",
        "Write a program that reverses a list without using built-in reverse functions.",
        "Write a program that finds the largest and smallest numbers in a list.",
        "Write a program that counts how many vowels are in a user-entered sentence.",
        "Write a simple number guessing game: generate random number 1-100, player guesses until correct.",
    ], 1):
        E.append(bul(f"Problem {i}: {ex}"))

    E.append(h2("C.2  Intermediate Level (Problems 16–35)"))
    for i, ex in enumerate([
        "Write a recursive function to compute the sum of all numbers from 1 to N.",
        "Write a function that checks if a string is a pangram (contains every letter a-z).",
        "Write a password strength validator: check length >= 12, uppercase, lowercase, digit, special char.",
        "Implement a stack (LIFO) data structure with push, pop, peek, and is_empty operations using a list.",
        "Implement a queue (FIFO) data structure with enqueue, dequeue, and is_empty operations.",
        "Write a program that generates Pascal's Triangle up to N rows.",
        "Write a function that finds all prime factors of a number.",
        "Write a Caesar cipher that encrypts and decrypts a message with a given shift.",
        "Write a function to check if two strings are anagrams of each other.",
        "Write a word frequency counter that reads a paragraph and shows the top 10 words.",
        "Write a simple bank account simulation: deposit, withdraw, check balance with overdraft protection.",
        "Write a program that generates all permutations of a list of items.",
        "Write a function to flatten a deeply nested list (e.g., [[1,[2,3]],[4]] -> [1,2,3,4]).",
        "Write a program that reads student names and scores and produces a ranked leaderboard.",
        "Write a simple shopping cart: add items, remove items, apply discount codes, calculate total.",
        "Implement bubble sort, selection sort, and insertion sort and compare their outputs on the same data.",
        "Write a recursive binary search function and test it on a sorted list of 20 elements.",
        "Write a program that compresses a string using run-length encoding (e.g., 'aaaaabb' -> 'a5b2').",
        "Write a program that generates a crossword-like grid of letters with hidden words.",
        "Write a function that converts a decimal number to binary, octal, and hexadecimal.",
    ], 16):
        E.append(bul(f"Problem {i}: {ex}"))

    E.append(h2("C.3  Advanced Level (Problems 36–50)"))
    for i, ex in enumerate([
        "Build a full student management system: add students, record grades, calculate GPA, generate report cards.",
        "Implement Dijkstra's shortest path algorithm on a weighted graph represented as a dictionary.",
        "Build an in-memory REST API simulation: routes for GET/POST/PUT/DELETE on a users collection.",
        "Implement a tokenizer and recursive descent parser for arithmetic expressions (supports +,-,*,/,parens).",
        "Build a mini task scheduler: tasks with priorities, due dates, add/complete/cancel/list operations.",
        "Write a Sudoku validator that checks if a given 9x9 grid is a valid solved Sudoku.",
        "Implement the Sieve of Eratosthenes to find all primes up to 1,000,000 and measure performance.",
        "Build a CSV file processor: read CSV, filter rows, sort by column, compute column statistics, write output.",
        "Write a program that simulates a deck of cards: shuffle, deal hands, evaluate poker hand ranks.",
        "Implement a simple hash table from scratch (without using Python dict) with collision handling.",
        "Build a complete CLI quiz application: load questions from JSON, time-limited answers, scoring, leaderboard.",
        "Write an autocomplete system: given a dictionary of words, return all words starting with a given prefix.",
        "Build a full-stack EnLang project: .enlg backend + .enlgf frontend + .enlgd styling + .enlgdb schema.",
        "Implement a concurrent web scraper using asyncio that fetches and parses 20 URLs simultaneously.",
        "Build an inventory management system with categories, stock tracking, low-stock alerts, and CSV export.",
    ], 36):
        E.append(bul(f"Problem {i}: {ex}"))

    E += chap("APPENDIX D: Common Errors, Debugging Checklist & Troubleshooting")
    E.append(tbl([
        ["Error","Root Cause","Diagnostic Command","Fix"],
        ["'enlang' not recognized","PATH not configured","python -m site --user-site","Add Scripts dir to PATH"],
        ["'No distribution found for enlang'","Not on PyPI when first installed","pip show enlang","pip install git+https://..."],
        ["IndentationError (runtime)","Wrong indent (not 4 spaces)","enlang check file.enlg","Use 4 spaces per level"],
        ["SyntaxError: colon","Missing ':' on block header","enlang check file.enlg","Add ':' to if/for/while header"],
        ["Unclosed string (linter)","Unmatched quote character","enlang check file.enlg","Close the string literal"],
        ["RecursionError","No base case / infinite recursion","Add print to trace calls","Add base case that returns"],
        ["KeyError: 'key'","Accessing dict key that doesn't exist","v in dict check","Use .get() or check first"],
        ["TypeError: + on int+str","Concatenating int and string without str()","Check display/plus lines","Wrap int with str()"],
        ["ModuleNotFoundError","pip package not installed","pip list","pip install <package>"],
        ["FileNotFoundError","File path wrong or file missing","os.path.exists(path)","Check path and file presence"],
        ["JSONDecodeError","Invalid JSON in file","python -m json.tool file.json","Fix JSON syntax"],
        ["Unclosed match block","Missing 'end match'","enlang check file.enlg","Add 'end match'"],
        ["@python() not working","Wrong escape syntax","Check for typos","Use exact: @python(expr)"],
        ["Port already in use","Another process on same port","netstat -ano | findstr :PORT","Change port or kill process"],
    ],col_widths=[110,130,130,120]))

    # FINAL PAGE
    E.append(PageBreak())
    E += [
        Spacer(1,1.2*inch),
        HRFlowable(width="60%",thickness=2,color=colors.HexColor("#4338ca"),hAlign="CENTER",spaceAfter=16),
        Paragraph("Copyright &copy; 2026 Spandan Prayas Patra",S["book_auth"]),
        Paragraph("All rights reserved. Open EnLang Specification License (OESL).",S["book_auth"]),
        Spacer(1,0.2*inch),
        Paragraph("Official Package: <b>https://pypi.org/project/enlang/</b>",S["book_auth"]),
        Paragraph("Public Repository: <b>https://github.com/Aero99op/enlang</b>",S["book_auth"]),
        Spacer(1,0.2*inch),
        Paragraph("EnLang — <i>Programming in the language of thought.</i>",S["book_sub"]),
        HRFlowable(width="60%",thickness=2,color=colors.HexColor("#4338ca"),hAlign="CENTER",spaceBefore=16),
    ]

    return E

if __name__ == "__main__":
    OUT = "enlangbookv2release.pdf"
    print("[INFO] Building EnLang 500+ Page Master Book PDF...")
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
    )
    elems = build()
    doc.build(elems)
    size = os.path.getsize(OUT)
    print(f"[SUCCESS] PDF: {OUT}")
    print(f"[INFO]    Size: {size:,} bytes ({size//1024} KB)")
    print(f"[INFO]    Path: {os.path.abspath(OUT)}")
