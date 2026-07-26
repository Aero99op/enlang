"""
EnLang Master Handbook — Part II: Language Fundamentals (Chapters 4 to 8)
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
        part_heading=P("P2_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P2_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P2_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P2_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P2_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P2_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P2_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P2_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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

def get_part2_elements():
    E = []
    E.append(Paragraph("Part II — Language Fundamentals", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 4
    E.append(Paragraph("Chapter 4: Lexical Structure", S["chap"]))
    E.append(h2("4.1 Character Set & Unicode Support"))
    E.append(body("EnLang source files use UTF-8 encoding by default, supporting international character sets, mathematical symbols, and strings in all languages."))
    E.append(h2("4.2 Tokens, Identifiers, & Comments"))
    E.append(body("EnLang code is composed of tokens: Keywords (`define`, `set`, `if`, `read`), Identifiers (variable and function names), Literals (`10`, `3.14`, `\"text\"`), and Comments (`# single line comment`)."))
    E.append(code(["# Lexical Structure Demo", "define text student_name as \"Spandan\"", "# Identifiers: student_name, Type: text"]))
    E.append(hr())

    # Chapter 5
    E.append(Paragraph("Chapter 5: Variables and Constants", S["chap"]))
    E.append(h2("5.1 What is a Variable? Memory Concept"))
    E.append(body("A variable is a named location in memory that stores a data value. In EnLang, variables are declared explicitly using the `define` keyword followed by the type, variable name, and initial value."))
    E.append(h2("5.2 Declaring Variables in EnLang"))
    E.append(body("EnLang supports natural variable declaration syntax for all data types:"))
    E.append(code([
        "define text name as \"Spandan Patra\"",
        "define number score as 95",
        "define boolean is_active as true",
        "define list marks as [85, 90, 95]"
    ]))
    E.append(h2("5.3 Mutability & Scope Rules"))
    E.append(body("Variables declared with `define` are mutable. To update the value of an existing variable, use the `set` keyword (`set score to 100`). Variables are lexically scoped within their block or function."))
    E.append(code(["set score to 100", "display score"]))
    E.append(cout(["100"]))
    E.append(hr())

    # Chapter 6
    E.append(Paragraph("Chapter 6: Data Types", S["chap"]))
    E.append(h2("6.1 Primitive Data Types"))
    E.append(body("EnLang provides rich primitive data types:"))
    E.append(bul("text / string: Sequence of Unicode characters (\"Hello\")"))
    E.append(bul("number: Signed 64-bit integer or floating point number (42, 3.14159)"))
    E.append(bul("boolean: Logical truth values (true, false)"))
    E.append(bul("list: Ordered sequence of elements ([10, 20, 30])"))
    E.append(bul("dictionary: Key-value mapping pairs ({\"key\": \"value\"})"))
    E.append(bul("dataset: High-performance tabular matrix (Pandas/Arrow backend handle)"))

    E.append(code([
        "define dictionary user_profile as {\"id\": 101, \"role\": \"Developer\"}",
        "display user_profile[\"role\"]"
    ]))
    E.append(cout(["Developer"]))
    E.append(hr())

    # Chapter 7
    E.append(Paragraph("Chapter 7: Operators and Expressions", S["chap"]))
    E.append(h2("7.1 Natural English Operators"))
    E.append(body("EnLang replaces cryptic mathematical symbols with readable natural English keywords:"))
    
    op_table = [
        ["Operation", "EnLang English Operator", "Traditional Operator", "Example Code"],
        ["Addition", "plus", "+", "5 plus 10"],
        ["Subtraction", "minus", "-", "20 minus 5"],
        ["Multiplication", "times", "*", "4 times 5"],
        ["Division", "divided by", "/", "20 divided by 4"],
        ["Equality", "is equal to", "==", "age is equal to 18"],
        ["Inequality", "is not equal to", "!=", "status is not equal to \"banned\""],
        ["Greater Than", "is greater than", ">", "score is greater than 80"],
        ["Less Than", "is less than", "<", "temp is less than 30"]
    ]
    formatted_op = []
    for r_idx, row in enumerate(op_table):
        f_row = []
        for cell in row:
            p_style = S["h2"] if r_idx == 0 else S["body"]
            f_row.append(Paragraph(t(str(cell)), p_style))
        formatted_op.append(f_row)
    t_obj = Table(formatted_op, colWidths=[100, 140, 110, 120])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    E.append(t_obj)
    E.append(hr())

    # Chapter 8
    E.append(Paragraph("Chapter 8: Input and Output", S["chap"]))
    E.append(h2("8.1 Output Streams with `display`"))
    E.append(body("The `display` keyword prints values to the standard output stream with automatic string formatting and newline appending:"))
    E.append(code([
        "define number x as 15",
        "define number y as 25",
        "display \"Sum: \" + (x plus y)"
    ]))
    E.append(cout(["Sum: 40"]))
    E.append(note("Chapter 8 Complete: Fundamentals of variables, data types, operators, and I/O mastered!"))
    E.append(hr())

    return E
