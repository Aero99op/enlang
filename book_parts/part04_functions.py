"""
EnLang Master Handbook — Part IV: Functions & Functional Paradigm (Chapters 11 to 12)
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
        part_heading=P("P4_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P4_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P4_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P4_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P4_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P4_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P4_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P4_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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

def get_part4_elements():
    E = []
    E.append(Paragraph("Part IV — Functions & Functional Programming", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 11
    E.append(Paragraph("Chapter 11: Functions & Reusability", S["chap"]))
    E.append(h2("11.1 Defining Functions in EnLang"))
    E.append(body("Functions are reusable blocks of code designed to perform a specific task. In EnLang, functions are defined using the `function` keyword followed by the function name, parameters passed via `using`, and a colon `:`."))
    E.append(code([
        "function calculate_tax using amount, rate:",
        "    return amount times (rate divided by 100)",
        "",
        "define number tax as calculate_tax(1000, 18)",
        "display \"Tax Amount: \" + tax"
    ]))
    E.append(cout(["Tax Amount: 180.0"]))

    E.append(h2("11.2 Recursion in EnLang"))
    E.append(body("EnLang supports recursive functions (functions calling themselves until reaching a base condition). Here is a factorial recursive function in EnLang:"))
    E.append(code([
        "function factorial using n:",
        "    if n is less than or equal to 1 then:",
        "        return 1",
        "    return n times factorial(n minus 1)",
        "",
        "display factorial(5)"
    ]))
    E.append(cout(["120"]))
    E.append(hr())

    # Chapter 12
    E.append(Paragraph("Chapter 12: Functional Programming", S["chap"]))
    E.append(h2("12.1 Higher-Order Functions: Map, Filter, & Reduce"))
    E.append(body("Higher-order functions accept other functions as arguments or return them. EnLang provides native support for `map`, `filter`, and `reduce`:"))
    E.append(code([
        "define list numbers as [1, 2, 3, 4, 5, 6]",
        "set evens to filter(numbers, lambda x: x % 2 == 0)",
        "display evens"
    ]))
    E.append(cout(["[2, 4, 6]"]))
    E.append(note("Chapter 12 Complete: Functions, recursion, and functional paradigms mastered!"))
    E.append(hr())

    return E
