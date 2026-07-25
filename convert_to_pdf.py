import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf(md_file, pdf_file):
    print(f"[INFO] Reading markdown from: {md_file}")
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styling
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1e1b4b"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4338ca"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1e1b4b"),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#3730a3"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    elements = []

    lines = content.splitlines()
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            if in_code:
                # End of code block
                code_text = "<br/>".join(code_lines).replace(" ", "&nbsp;")
                elements.append(Paragraph(code_text, code_style))
                code_lines = []
                in_code = False
            else:
                in_code = True
                code_lines = []
            i += 1
            continue

        if in_code:
            escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            code_lines.append(escaped_line)
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        if stripped.startswith("# ENLANG FOR DEVELOPERS"):
            elements.append(Paragraph("ENLANG FOR DEVELOPERS", title_style))
            elements.append(Paragraph("The Complete Master Specification & Release Guide (v2.0)<br/>Author & Architect: Spandan Prayas Patra", subtitle_style))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4338ca"), spaceAfter=15))
            i += 1
            continue

        if stripped.startswith("# "):
            text = stripped[2:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(text, h1_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
        elif stripped.startswith("## "):
            text = stripped[3:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(text, h2_style))
        elif stripped.startswith("### "):
            text = stripped[4:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(f"<b>{text}</b>", body_style))
        else:
            text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Format bold inline
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'`(.+?)`', r'<font face="Courier" color="#3730a3"><b>\1</b></font>', text)
            elements.append(Paragraph(text, body_style))

        i += 1

    doc.build(elements)
    print(f"[SUCCESS] PDF generated: {pdf_file}")
    print(f"[INFO]    File size: {os.path.getsize(pdf_file):,} bytes")

if __name__ == "__main__":
    import re
    md_path = "ENLANG_FOR_DEVELOPERS_BOOK.md"
    pdf_path = "enlangbookv2release.pdf"
    generate_pdf(md_path, pdf_path)
