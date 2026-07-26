"""
EnLang Master Handbook — Part XIII: Database Engine & .enlgdb Safety Guards (Chapters 61 to 66)
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
        part_heading=P("P13_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P13_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P13_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P13_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P13_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P13_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P13_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P13_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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

def get_part13_elements():
    E = []
    E.append(Paragraph("Part XIII — Database Engine & .enlgdb Safety Guards", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 61 to 66
    E.append(Paragraph("Chapter 61 to 66: SQL, Databases, & Accidental Bulk Mutation Protection", S["chap"]))
    E.append(h2("61.1 EnLang Database Engine (.enlgdb)"))
    E.append(body("EnLang Database Engine (`.enlgdb`) replaces rigid SQL syntax and ORM boilerplate with readable natural English data operations, multi-engine compilation (SQLite, PostgreSQL, MySQL, DuckDB), and built-in production safety guards."))
    
    E.append(h2("66.1 Accidental Bulk Mutation Protection Guards"))
    E.append(body("In traditional SQL, omitting a `WHERE` clause in `DELETE FROM users;` or `UPDATE users SET status = 'inactive';` accidentally wipes or corrupts the entire table."))
    E.append(body("EnLang introduces Compile-Time Safety Protection Guards:"))
    E.append(bul("Single/Specific Row Deletes Require 'where': `delete row from users where id is 42`"))
    E.append(bul("Accidental Bulk Delete Attempt (`delete from users`) BLOCKED AT COMPILE-TIME!"))
    E.append(bul("Bulk Wipes Require Explicit Authorization: `delete all rows from users confirm bulk`"))

    E.append(code([
        "# Safe Single Row Delete",
        "delete row from users where id is 42",
        "",
        "# Explicit Authorized Bulk Table Wipe",
        "delete all rows from users confirm bulk"
    ]))
    E.append(cout([
        "DELETE FROM users WHERE id = 42;",
        "DELETE FROM users;"
    ]))

    E.append(note("Chapter 66 Complete: SQL integration, SQLite, PostgreSQL, MySQL, MongoDB, and .enlgdb safety guards mastered!"))
    E.append(hr())

    return E
