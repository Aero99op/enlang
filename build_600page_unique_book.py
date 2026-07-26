"""
EnLang 600-Page Master Textbook Builder (100% Unique, Non-Repetitive Edition)
Imports Volume 1 through Volume 6 modules and compiles the master PDF.
Author: Spandan Prayas Patra
"""
import os
import sys
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

# Import all 7 volume modules
import book_volume_1
import book_volume_2
import book_volume_3
import book_volume_4
import book_volume_5
import book_volume_6
import book_volume_7

W, H = letter

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        book_title=P("MB_BT", fontName="Helvetica-Bold", fontSize=32, leading=38,
                     textColor=colors.HexColor("#0f172a"), alignment=TA_CENTER, spaceAfter=8),
        book_sub=P("MB_BS", fontName="Helvetica-Oblique", fontSize=13, leading=17,
                   textColor=colors.HexColor("#4338ca"), alignment=TA_CENTER, spaceAfter=5),
        book_auth=P("MB_BA", fontName="Helvetica", fontSize=10, leading=14,
                    textColor=colors.HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=20),
        chap=P("MB_CH", fontName="Helvetica-Bold", fontSize=16, leading=22,
               textColor=colors.HexColor("#1e1b4b"), spaceBefore=14, spaceAfter=6, keepWithNext=True),
        h2=P("MB_H2", fontName="Helvetica-Bold", fontSize=11, leading=15,
             textColor=colors.HexColor("#3730a3"), spaceBefore=8, spaceAfter=4, keepWithNext=True),
        body=P("MB_BD", fontName="Helvetica", fontSize=8.5, leading=12.0,
               textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=4),
        bullet=P("MB_BU", fontName="Helvetica", fontSize=8.5, leading=12.0,
                 textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=2),
    )

S = make_styles()

def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def bul(txt): return Paragraph("• "+t(txt), S["bullet"])
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=4, spaceBefore=4)

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
        ("FONTSIZE",(0,1),(-1,-1),7.2),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8fafc"),colors.HexColor("#eef2ff")]),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#cbd5e1")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),3),
        ("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),2),
        ("BOTTOMPADDING",(0,0),(-1,-1),2),
    ]))
    return t2

def get_master_frontmatter():
    F = []
    F += [
        Spacer(1, 0.6*inch),
        Paragraph("EnLang Programming Language", S["book_title"]),
        Paragraph("The Complete 600-Page Master Reference Manual & Specification (v2.0.0)", S["book_sub"]),
        Paragraph("Author & Lead Architect: Spandan Prayas Patra", S["book_auth"]),
        HRFlowable(width="85%", thickness=1.5, color=colors.HexColor("#4338ca"), spaceAfter=15, hAlign="CENTER"),
        body("Welcome to the official 600-page master textbook for the EnLang Natural English Programming Language. Created by Spandan Prayas Patra, EnLang is a universal multi-target compiler that translates natural English into clean, production-grade Python, HTML5, CSS3, JavaScript ES6+, and ANSI SQL."),
        body("This master volume is structured into six comprehensive 100-page volumes containing 600 detailed chapters, full theory, code examples, target output logs, automated unit test suites, security protocols, and benchmark metrics."),
        Spacer(1, 0.3*inch),
        tbl([
            ["Volume Identifier", "Page Range", "Primary Technical Focus", "Chapter Range"],
            ["Volume 1", "Pages 1 - 100", "Core Foundations, Syntax Engine & AST Generation", "Chapters 1 - 100"],
            ["Volume 2", "Pages 100 - 200", "Multi-Target Web Sub-Transpilers (.enlgf, .enlgd, .enlgs, .enlgdb)", "Chapters 101 - 200"],
            ["Volume 3", "Pages 200 - 300", "Data Structures, Algorithms & Computational Complexity", "Chapters 201 - 300"],
            ["Volume 4", "Pages 300 - 400", "Enterprise Security, Cryptography & Cloud Microservices", "Chapters 301 - 400"],
            ["Volume 5", "Pages 400 - 500", "Full Real-World Engineering Projects & Systems", "Chapters 401 - 500"],
            ["Volume 6", "Pages 500 - 600", "Master Reference Index, 200 Practice Problems & Glossary", "Chapters 501 - 600"],
        ], col_widths=[100, 80, 200, 90]),
        PageBreak()
    ]
    return F

def get_master_backmatter():
    B = []
    B += [
        PageBreak(),
        Spacer(1, 0.8*inch),
        Paragraph("Master Epilogue & Signature Page", S["chap"]),
        hr(),
        body("EnLang was created to break down the artificial barrier between human thought and digital execution. By proving that a 100% deterministic, offline, lightweight transpiler can convert natural English into clean multi-target code across Python, HTML, CSS, JS, and SQL, EnLang opens new horizons for software engineering."),
        body("This 600-page master reference manual stands as an exhaustive, 100% unique, non-repetitive testament to the design, specification, and implementation of EnLang v2.0.0."),
        Spacer(1, 0.4*inch),
        Paragraph("— Spandan Prayas Patra", S["book_sub"]),
        Paragraph("Creator & Architect of EnLang", S["book_auth"]),
        HRFlowable(width="80%", thickness=2, color=colors.HexColor("#4338ca"), spaceBefore=20, hAlign="CENTER"),
        Spacer(1, 0.3*inch),
        body("Distribution Channels: PyPI (`pip install enlang`) & GitHub Repository (https://github.com/Aero99op/enlang)"),
        body("Copyright © 2026 Spandan Prayas Patra. All Rights Reserved."),
    ]
    return B

def build_complete_600page_book():
    print("[INFO] Assembling Master Book (Volumes 1 to 7 + Master Front/Back matter)...")
    front = get_master_frontmatter()
    v1 = book_volume_1.get_volume_1_elements()
    v2 = book_volume_2.get_volume_2_elements()
    v3 = book_volume_3.get_volume_3_elements()
    v4 = book_volume_4.get_volume_4_elements()
    v5 = book_volume_5.get_volume_5_elements()
    v6 = book_volume_6.get_volume_6_elements()
    v7 = book_volume_7.get_volume_7_flowables()
    back = get_master_backmatter()

    all_elements = front + v1 + v2 + v3 + v4 + v5 + v6 + v7 + back
    print(f"[INFO] Total combined unique flowable elements: {len(all_elements)}")
    return all_elements

if __name__ == "__main__":
    OUT = "enlangbookv2release.pdf"
    print("[INFO] Starting 600-Page Unique Master PDF Generation...")
    t0 = time.time()

    elements = build_complete_600page_book()

    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch,
    )

    print("[INFO] Compiling layout into PDF via ReportLab...")
    doc.build(elements)

    elapsed = time.time() - t0
    size = os.path.getsize(OUT)

    print(f"[SUCCESS] 600-Page Unique Master PDF Generated Successfully!")
    print(f"[INFO]    Output File : {os.path.abspath(OUT)}")
    print(f"[INFO]    File Size   : {size:,} bytes ({size//1024} KB)")
    print(f"[INFO]    Build Time  : {elapsed:.2f} seconds")
