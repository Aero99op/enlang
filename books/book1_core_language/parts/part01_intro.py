"""
EnLang Core Language (Book 1) — Part 1: Introduction & Language Vision
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
        part_heading=P("B1P1_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("B1P1_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("B1P1_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("B1P1_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("B1P1_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("B1P1_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("B1P1_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("B1P1_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
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
    E.append(Paragraph("Part I — Introduction & Language Vision", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Section 1.1
    E.append(Paragraph("1.1 What is EnLang?", S["chap"]))
    E.append(h2("Concept & First Principles"))
    E.append(body("EnLang is a Universal Natural English Programming Language Platform created by Spandan Prayas Patra. It bridges the gap between human language and machine execution. In traditional programming, humans are forced to adapt to rigid syntax, semicolons, brackets, and cryptic symbols. EnLang flips this paradigm: you write program logic in plain, deterministic natural English sentences, and EnLang compiles your English directly into target binaries, Python, C++, Rust, HTML5, CSS3, or SQL."))

    E.append(h2("Why EnLang? The Educational & Industrial Purpose"))
    E.append(body("1. Eliminates Punctuation Anxiety: Beginners waste hours debugging missing parentheses or semicolons. EnLang uses English words like 'define', 'set', 'if', 'read', and 'display'."))
    E.append(body("2. Deterministic AST Lowering: Unlike AI tools that guess code probabilistically, EnLang's compiler parses English using a deterministic context-free grammar. The exact same English sentence will ALWAYS produce the exact same AST and target code."))
    E.append(body("3. High-Performance Execution: EnLang transpiles code into optimized target languages, providing native C++/Python execution speeds."))

    E.append(h2("EnLang vs Python vs C++ Architecture Matrix"))
    matrix_data = [
        ["Language Feature", "EnLang Core", "Python 3", "C++ / Rust"],
        ["Syntax Style", "Natural English Sentences", "Indented Code", "Braced Punctuation"],
        ["Learning Curve", "Immediate (0 Friction)", "Moderate", "Steep / Complex"],
        ["Safety Protection", "Built-in Bulk Safeguards", "Driver Checks", "Manual Memory Checks"],
        ["Transpilation Targets", "Python, C++, Rust, SQL, Web", "CPython Bytecode", "LLVM Machine Code"]
    ]
    formatted_table = []
    for r_idx, row in enumerate(matrix_data):
        f_row = []
        for cell in row:
            p_style = S["h2"] if r_idx == 0 else S["body"]
            f_row.append(Paragraph(t(str(cell)), p_style))
        formatted_table.append(f_row)
    t_obj = Table(formatted_table, colWidths=[120, 120, 110, 120])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    E.append(t_obj)
    E.append(hr())

    # Section 1.2
    E.append(Paragraph("1.2 History & Vision of EnLang", S["chap"]))
    E.append(body("EnLang was created in 2026 to make programming accessible to everyone — from young students and non-tech researchers to data scientists and enterprise software engineers. EnLang v1.1.2 introduces the Natural ML Engine v2, Accidental Bulk Mutation Protection Guards, and the 14 Core Platform Specifications Charter."))
    E.append(note("Part I Complete: Conceptual foundation of EnLang language vision established!"))
    E.append(hr())

    return E
