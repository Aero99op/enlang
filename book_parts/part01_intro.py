"""
EnLang Master Handbook — Part I: Introduction & Setup (Chapters 1 to 3 - Expanded Edition)
Author: Spandan Prayas Patra
"""
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        part_heading=P("P1_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P1_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P1_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P1_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P1_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P1_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P1_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P1_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
    )

S = make_styles()
def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def bul(txt): return Paragraph("• "+t(txt), S["bullet"])
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=5, spaceBefore=5)
def code(lines): return Paragraph("<br/>".join(t(l).replace(" ", "&nbsp;") for l in (lines if isinstance(lines, list) else [lines])), S["code"])
def cout(lines): return Paragraph("<br/>".join(t(l).replace(" ", "&nbsp;") for l in (lines if isinstance(lines, list) else [lines])), S["code_out"])
def note(txt): return Paragraph(t(txt), S["note"])

def get_part1_elements():
    E = []
    E.append(Paragraph("Part I — Introduction & Platform Setup", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 1
    E.append(Paragraph("Chapter 1: Welcome to EnLang", S["chap"]))
    E.append(h2("1.1 What is EnLang? (First Principles)"))
    E.append(body("EnLang is a Universal Natural English Programming Language Platform designed to eliminate artificial syntax barriers while preserving 100% mathematical determinism and compile-time verification. Unlike natural language processing heuristics that hallucinate or introduce ambiguity, EnLang maps human-readable sentences directly to an Abstract Syntax Tree (AST) and transpiles natively into Python, C++, Rust, HTML5, CSS3, and SQL."))
    E.append(body("For a student or new developer, programming in EnLang feels like writing instructions in plain, clear English. You don't have to worry about missing semicolons, complex bracket hierarchies, or cryptic compiler error messages."))

    E.append(h2("1.2 Why EnLang? Architectural Vision & Goals"))
    E.append(body("Traditional programming languages require developers to memorize rigid punctuation rules. EnLang replaces syntactic clutter with plain English verbs and prepositions ('read file as df', 'separate df into features X and target y', 'delete row from users where id is 42')."))
    E.append(bul("Zero Ambiguity: Every EnLang statement maps to exactly one unambiguous AST representation."))
    E.append(bul("Multi-Target Compilation: Transpiles to high-performance Python, C++, Rust, and WebAssembly."))
    E.append(bul("Industrial Domain Extensions: Built-in engines for Data Science, Machine Learning, Web Frontend (.enlgf), Styling (.enlgd), Databases (.enlgdb), and System Automation (.enlgs)."))

    E.append(h2("1.3 EnLang vs Traditional Programming Languages"))
    table_data = [
        ["Feature / Metric", "EnLang Platform", "Python 3", "C++ / Java"],
        ["Syntax Readability", "100% Natural English", "Indent-based Code", "Brace & Semi-colon Code"],
        ["Execution Speed", "Native / Multi-target", "Interpreted Bytecode", "Compiled Native Binary"],
        ["Database Safety", "Accidental Bulk Wipe Guard", "Manual Query Checks", "ORM / Driver Checks"],
        ["ML Model Artifacts", ".enlgmodel Container", "Pickle / Joblib (.pkl)", "ONNX / Custom Binaries"],
        ["Type System", "Gradual Domain Types", "Dynamic Type Hints", "Static Strict Types"]
    ]
    formatted_table = []
    for r_idx, row in enumerate(table_data):
        f_row = []
        for cell in row:
            p_style = S["h2"] if r_idx == 0 else S["body"]
            f_row.append(Paragraph(t(str(cell)), p_style))
        formatted_table.append(f_row)
    t_obj = Table(formatted_table, colWidths=[130, 110, 110, 120])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    E.append(t_obj)
    E.append(hr())

    # Chapter 2
    E.append(Paragraph("Chapter 2: Installing & Setting Up EnLang", S["chap"]))
    E.append(h2("2.1 System Requirements & Installation Methods"))
    E.append(body("EnLang is available as a cross-platform package on PyPI (`enlang`), as well as a standalone binary installer for Windows, Linux, and macOS. The recommended installation method is via Python's package manager:"))
    E.append(code(["# PyPI Package Installation", "pip install --upgrade enlang"]))
    E.append(h2("2.2 Verifying Installation & Tooling Checks"))
    E.append(body("Verify your local EnLang CLI compiler and interpreter installation using the `enlang check` and `enlang versions` commands:"))
    E.append(code(["# Verify Compiler Version", "enlang check --version"]))
    E.append(cout(["EnLang Compiler Engine v1.1.2", "Target Transpiler: Python 3.8+ / HTML5 / CSS3 / SQL", "Status: Operational & Certified"]))

    E.append(h2("2.3 Editor Setup & VS Code Extension"))
    E.append(body("The official VS Code extension (`vscode-enlang`) provides full syntax colorization, snippet auto-completion, static error diagnostics, and formatting for all EnLang file extensions (`.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, `.enlgdb`)."))
    E.append(hr())

    # Chapter 3
    E.append(Paragraph("Chapter 3: Your First EnLang Program", S["chap"]))
    E.append(h2("3.1 Writing & Executing 'Hello EnLang'"))
    E.append(body("Create a new source file named `hello.enlg` using your text editor and write your first EnLang program:"))
    E.append(code(["# hello.enlg — First EnLang Program", "define text greeting as \"Hello, EnLang World!\"", "display greeting"]))
    E.append(h2("3.2 Transpilation & Target Execution"))
    E.append(body("Run the script using the EnLang interpreter CLI. EnLang transpiles the English code into Python target code and executes it instantly:"))
    E.append(code(["# Run Script via CLI", "enlang run hello.enlg"]))
    E.append(cout(["Hello, EnLang World!"]))
    E.append(body("To view the transpiled target code generated by the EnLang transpiler pass, append the `--show-py` flag:"))
    E.append(code(["enlang run hello.enlg --show-py"]))
    E.append(cout(["--- Transpiled Target Python Code (hello.enlg) ---", "greeting = 'Hello, EnLang World!'", "print(greeting)", "--- Execution Output ---", "Hello, EnLang World!"]))
    E.append(note("Chapter 3 Complete: You have compiled and executed your first EnLang program!"))
    E.append(hr())

    return E
