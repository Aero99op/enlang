"""
EnLang Official Programming Language Master Handbook Builder
Imports all modular part generators from book_parts/ and builds enlangbookv2release.pdf
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

# Import modular generator parts
from book_parts.part01_intro import get_part1_elements
from book_parts.part02_fundamentals import get_part2_elements
from book_parts.part03_flow import get_part3_elements
from book_parts.part04_functions import get_part4_elements
from book_parts.part05_collections import get_part5_elements
from book_parts.part06_oop import get_part6_elements
from book_parts.part07_advanced import get_part7_elements
from book_parts.part08_memory import get_part8_elements
from book_parts.part09_errors import get_part9_elements
from book_parts.part10_concurrency import get_part10_elements
from book_parts.part11_files import get_part11_elements
from book_parts.part12_networking import get_part12_elements
from book_parts.part13_database import get_part13_elements
from book_parts.part14_stdlib import get_part14_elements
from book_parts.part15_ai_ds import get_part15_elements
from book_parts.part16_testing import get_part16_elements
from book_parts.part17_tooling import get_part17_elements
from book_parts.part18_compiler import get_part18_elements
from book_parts.part19_best_practices import get_part19_elements
from book_parts.part20_projects import get_part20_elements
from book_parts.part21_reference import get_part21_elements
from book_parts.part22_spec import get_part22_elements
from book_parts.part23_appendices import get_part23_elements

W, H = letter

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        book_title=P("MB_BT", fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=colors.HexColor("#0f172a"), alignment=TA_CENTER, spaceAfter=8),
        book_sub=P("MB_BS", fontName="Helvetica-Oblique", fontSize=13, leading=17, textColor=colors.HexColor("#4338ca"), alignment=TA_CENTER, spaceAfter=5),
        book_auth=P("MB_BA", fontName="Helvetica", fontSize=10, leading=14, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=20),
        h2=P("MB_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("MB_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        note=P("MB_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
    )

S = make_styles()
def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def note(txt): return Paragraph(t(txt), S["note"])

def build_master_handbook():
    print("[INFO] Starting Modular EnLang Master Handbook PDF Compilation...")
    t0 = time.time()

    E = []
    # Front Matter
    E.append(Spacer(1, 0.4*inch))
    E.append(Paragraph("ENLANG OFFICIAL PROGRAMMING LANGUAGE MASTER HANDBOOK", S["book_title"]))
    E.append(Paragraph("The Complete 150-Chapter Educational Handbook, Architecture Specification & Reference Guide", S["book_sub"]))
    E.append(Paragraph("Author & Architect: Spandan Prayas Patra (spandanpatra1234@gmail.com)", S["book_auth"]))
    E.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4338ca"), spaceBefore=10, spaceAfter=20))
    
    E.append(h2("Master Preface & Pedagogical Charter"))
    E.append(body("Welcome to the official EnLang Programming Language Master Handbook. EnLang is a Universal Natural English Programming Language Platform engineered for deterministic execution, high-performance machine learning, database safety, multi-target web rendering, and industrial software engineering."))
    E.append(body("Designed with a student-first pedagogical approach, every chapter provides comprehensive answers to: What is this concept? Why is it useful? How does EnLang implement it? What is the syntax format? What are real-world code examples and output logs?"))
    E.append(Spacer(1, 15))
    E.append(note("EnLang Platform Version: 1.1.2 | Specification Standard: ISO/IEC EnLang 2026 Compatible"))
    E.append(PageBreak())

    # Part Generators (Parts 1 to 23)
    part_generators = [
        get_part1_elements, get_part2_elements, get_part3_elements, get_part4_elements,
        get_part5_elements, get_part6_elements, get_part7_elements, get_part8_elements,
        get_part9_elements, get_part10_elements, get_part11_elements, get_part12_elements,
        get_part13_elements, get_part14_elements, get_part15_elements, get_part16_elements,
        get_part17_elements, get_part18_elements, get_part19_elements, get_part20_elements,
        get_part21_elements, get_part22_elements, get_part23_elements
    ]

    total_flowables = len(E)
    for p_idx, gen_func in enumerate(part_generators, start=1):
        print(f"[INFO] Compiling Part {p_idx} elements...")
        part_elems = gen_func()
        total_flowables += len(part_elems)
        E.extend(part_elems)

    # Back Matter
    E.append(PageBreak())
    E.append(Spacer(1, 0.8*inch))
    E.append(Paragraph("Master Epilogue & Author Certification Page", S["h2"]))
    E.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#312e81"), spaceBefore=5, spaceAfter=15))
    E.append(body("The EnLang Official Programming Language Master Handbook represents the complete educational specification, usage manual, and compiler reference guide for EnLang v1.1.2. Covering all 150 chapters across 23 parts, this reference manual certifies the language semantics, syntax rules, and multi-target compilation guarantees."))
    E.append(Spacer(1, 0.4*inch))
    E.append(Paragraph("— Spandan Prayas Patra", S["book_sub"]))
    E.append(Paragraph("Creator & Architect of EnLang", S["book_auth"]))
    E.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#4338ca"), spaceBefore=20, hAlign="CENTER"))

    OUT_PDF = "enlangbookv2release.pdf"
    doc = SimpleDocTemplate(
        OUT_PDF, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch,
    )
    
    print(f"[INFO] Building PDF with {len(E)} flowable elements into '{OUT_PDF}'...")
    doc.build(E)

    t1 = time.time()
    sz = os.path.getsize(OUT_PDF)
    print(f"[SUCCESS] Modular EnLang Master Handbook PDF Compiled Successfully!")
    print(f"[INFO]    Output File : {os.path.abspath(OUT_PDF)}")
    print(f"[INFO]    File Size   : {sz:,} bytes ({sz//1024} KB)")
    print(f"[INFO]    Build Time  : {t1-t0:.2f} seconds")

if __name__ == "__main__":
    build_master_handbook()
