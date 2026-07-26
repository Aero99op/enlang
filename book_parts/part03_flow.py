"""
EnLang Master Handbook — Part III: Flow Control & Logic (Chapters 9 to 10)
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
        part_heading=P("P3_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P3_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P3_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P3_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P3_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P3_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P3_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P3_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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

def get_part3_elements():
    E = []
    E.append(Paragraph("Part III — Flow Control & Decision Logic", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 9
    E.append(Paragraph("Chapter 9: Decision Making", S["chap"]))
    E.append(h2("9.1 If-Else Conditional Branching"))
    E.append(body("Decision making allows a program to execute specific blocks of code based on whether a boolean condition evaluates to true or false. In EnLang, conditional blocks end with a colon `:` and use block indentation:"))
    E.append(code([
        "define number marks as 88",
        "if marks is greater than 80 then:",
        "    display \"Grade: Distinction\"",
        "else:",
        "    display \"Grade: Pass\""
    ]))
    E.append(cout(["Grade: Distinction"]))

    E.append(h2("9.2 Pattern Matching & Match Statements"))
    E.append(body("EnLang supports structural pattern matching via `match` for multi-branch evaluation:"))
    E.append(code([
        "define text status as \"active\"",
        "match status:",
        "    case \"active\": display \"User Operational\"",
        "    case \"banned\": display \"User Restricted\"",
        "    case _: display \"Unknown Status\""
    ]))
    E.append(cout(["User Operational"]))
    E.append(hr())

    # Chapter 10
    E.append(Paragraph("Chapter 10: Loops and Iteration", S["chap"]))
    E.append(h2("10.1 Repeat N Times Loop"))
    E.append(body("When you need to repeat an action a fixed number of times, EnLang provides the `repeat N times:` construct. This eliminates manual loop counter boilerplate:"))
    E.append(code([
        "repeat 3 times:",
        "    display \"Executing EnLang Iteration\""
    ]))
    E.append(cout([
        "Executing EnLang Iteration",
        "Executing EnLang Iteration",
        "Executing EnLang Iteration"
    ]))

    E.append(h2("10.2 Foreach & While Loops"))
    E.append(body("Use `foreach item in collection:` to iterate over lists or data streams:"))
    E.append(code([
        "define list items as [\"Rice\", \"Wheat\", \"Maize\"]",
        "foreach crop in items:",
        "    display \"Crop: \" + crop"
    ]))
    E.append(cout(["Crop: Rice", "Crop: Wheat", "Crop: Maize"]))
    E.append(note("Chapter 10 Complete: Decision making and iterative flow control mastered!"))
    E.append(hr())

    return E
