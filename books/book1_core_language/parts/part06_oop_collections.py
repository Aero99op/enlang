"""
EnLang Core Language (Book 1) — Part 6: OOP, Functional Paradigms & Advanced Features
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
        part_heading=P("B1P6_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("B1P6_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("B1P6_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("B1P6_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("B1P6_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("B1P6_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("B1P6_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("B1P6_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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

def get_part6_elements():
    E = []
    E.append(Paragraph("Part VI — OOP, Functional Paradigms & Advanced Features", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 7
    E.append(Paragraph("Chapter 7: Object-Oriented Programming (OOP)", S["chap"]))
    E.append(h2("7.1 Classes, Objects, & Inheritance"))
    E.append(body("EnLang supports full OOP: classes, constructor initialization (`init`), and inheritance (`inherits`):"))
    E.append(code([
        "class Person:",
        "    function init using name:",
        "        this.name = name",
        "",
        "class Developer inherits Person:",
        "    function init using name, lang:",
        "        super.init(name)",
        "        this.lang = lang",
        "",
        "set dev to Developer(\"Spandan\", \"EnLang\")",
        "display dev.name + \" builds in \" + dev.lang"
    ]))
    E.append(cout(["Spandan builds in EnLang"]))

    # Chapter 8
    E.append(Paragraph("Chapter 8: Functional Programming & Lambda Expressions", S["chap"]))
    E.append(h2("8.1 Higher-Order Functions: Map, Filter, & Reduce"))
    E.append(body("Process collections using `map` and `filter`:"))
    E.append(code([
        "define list numbers as [1, 2, 3, 4, 5, 6]",
        "set evens to filter(numbers, lambda x: x % 2 == 0)",
        "display evens"
    ]))
    E.append(cout(["[2, 4, 6]"]))
    E.append(note("Part VI Complete: Object-Oriented and Functional paradigms mastered!"))
    E.append(hr())

    return E
