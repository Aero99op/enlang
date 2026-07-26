r"""
Master Builder for Book 1 — EnLang Core Language Reference PDF
Output: d:\enlangg\books\book1_enlang_core_language.pdf
Author: Spandan Prayas Patra
"""
import os
import sys
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# Import parts of Book 1
from parts.part01_intro import get_part1_elements
from parts.part02_installation import get_part2_elements
from parts.part03_compiler_interpreter import get_part3_elements
from parts.part04_language_basics import get_part4_elements
from parts.part05_control_functions import get_part5_elements
from parts.part06_oop_collections import get_part6_elements

W, H = letter

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        book_title=P("B1_BT", fontName="Helvetica-Bold", fontSize=28, leading=34, textColor=colors.HexColor("#0f172a"), alignment=TA_CENTER, spaceAfter=8),
        book_sub=P("B1_BS", fontName="Helvetica-Oblique", fontSize=13, leading=17, textColor=colors.HexColor("#4338ca"), alignment=TA_CENTER, spaceAfter=5),
        book_auth=P("B1_BA", fontName="Helvetica", fontSize=10, leading=14, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=20),
        h2=P("B1_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("B1_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        note=P("B1_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
    )

S = make_styles()
def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def note(txt): return Paragraph(t(txt), S["note"])

def build_book1():
    print("[INFO] Starting Book 1 — EnLang Core Language Reference PDF Build...")
    t0 = time.time()

    E = []
    # Front Matter
    E.append(Spacer(1, 0.4*inch))
    E.append(Paragraph("BOOK 1: ENLANG CORE LANGUAGE REFERENCE", S["book_title"]))
    E.append(Paragraph("The Definitive Student & Developer Guide to Core EnLang Programming Syntax", S["book_sub"]))
    E.append(Paragraph("Author & Architect: Spandan Prayas Patra (spandanpatra1234@gmail.com)", S["book_auth"]))
    E.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4338ca"), spaceBefore=10, spaceAfter=20))
    
    E.append(h2("Book 1 Preface & Target Audience"))
    E.append(body("Welcome to Book 1 of the official EnLang Library Ecosystem. This volume serves as the complete, step-by-step programming language manual for every EnLang developer."))
    E.append(body("Every section follows first-principles teaching: What is the concept? Why is it useful? How is it implemented in EnLang? Code examples, execution logs, and linter rules are provided for all topics."))
    E.append(Spacer(1, 15))
    E.append(note("Book 1 Target Audience: Every EnLang Developer | Version: 1.1.2 Certified"))
    E.append(PageBreak())

    # Load Parts
    part_funcs = [
        get_part1_elements,
        get_part2_elements,
        get_part3_elements,
        get_part4_elements,
        get_part5_elements,
        get_part6_elements
    ]

    for p_idx, fn in enumerate(part_funcs, start=1):
        print(f"[INFO] Building Part {p_idx}...")
        E.extend(fn())

    # Back Matter
    E.append(PageBreak())
    E.append(Spacer(1, 0.8*inch))
    E.append(Paragraph("Book 1 Epilogue & Author Certification", S["h2"]))
    E.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#312e81"), spaceBefore=5, spaceAfter=15))
    E.append(body("Book 1 — EnLang Core Language Reference provides the foundational core knowledge required for all subsequent volumes in the EnLang Library Ecosystem."))
    E.append(Spacer(1, 0.4*inch))
    E.append(Paragraph("— Spandan Prayas Patra", S["book_sub"]))
    E.append(Paragraph("Creator & Architect of EnLang", S["book_auth"]))

    OUT_PDF = os.path.join(os.path.dirname(__file__), "..", "book1_enlang_core_language.pdf")
    doc = SimpleDocTemplate(
        OUT_PDF, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch,
    )
    
    print(f"[INFO] Compiling {len(E)} elements into '{os.path.abspath(OUT_PDF)}'...")
    doc.build(E)

    t1 = time.time()
    sz = os.path.getsize(OUT_PDF)
    print(f"[SUCCESS] Book 1 — EnLang Core Language Reference PDF Built Successfully!")
    print(f"[INFO]    Output File : {os.path.abspath(OUT_PDF)}")
    print(f"[INFO]    File Size   : {sz:,} bytes ({sz//1024} KB)")
    print(f"[INFO]    Build Time  : {t1-t0:.2f} seconds")

if __name__ == "__main__":
    build_book1()
