"""
EnLang Master Handbook — Part VI: Object-Oriented Programming (Chapters 15 to 22)
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
        part_heading=P("P6_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P6_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P6_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P6_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P6_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P6_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P6_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P6_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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
    E.append(Paragraph("Part VI — Object-Oriented Programming", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 15 & 16
    E.append(Paragraph("Chapter 15 & 16: Classes, Objects, & Constructors", S["chap"]))
    E.append(h2("15.1 Defining Classes in EnLang"))
    E.append(body("Object-Oriented Programming (OOP) organizes software around data entities called Objects. A Class is the blueprint for creating objects. In EnLang, classes use the `class` keyword with constructor functions `init`:"))
    E.append(code([
        "class Person:",
        "    function init using name, age:",
        "        this.name = name",
        "        this.age = age",
        "",
        "    function get_info():",
        "        return this.name + \" (\" + this.age + \")\"",
        "",
        "set p to Person(\"Spandan\", 25)",
        "display p.get_info()"
    ]))
    E.append(cout(["Spandan (25)"]))

    # Chapter 17 & 18
    E.append(Paragraph("Chapter 17 & 18: Inheritance & Encapsulation", S["chap"]))
    E.append(h2("17.1 Single & Multiple Inheritance"))
    E.append(body("Inheritance allows a subclass to derive properties and methods from a superclass using `inherits`:"))
    E.append(code([
        "class Developer inherits Person:",
        "    function init using name, age, language:",
        "        super.init(name, age)",
        "        this.language = language",
        "",
        "set dev to Developer(\"Spandan\", 25, \"EnLang\")",
        "display dev.language"
    ]))
    E.append(cout(["EnLang"]))

    # Chapter 19 to 22
    E.append(Paragraph("Chapter 19 to 22: Polymorphism, Interfaces, & Operator Overloading", S["chap"]))
    E.append(h2("19.1 Polymorphism & Interfaces"))
    E.append(body("Polymorphism enables objects of different classes to respond to the same method invocation via method overriding or interface compliance."))
    E.append(note("Chapter 22 Complete: Object-Oriented Programming fundamentals, inheritance, interfaces, and operator overloading fully mastered!"))
    E.append(hr())

    return E
