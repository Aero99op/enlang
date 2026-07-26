import os
import re
import glob
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def build_pdf_from_markdown(md_path, pdf_path):
    print(f"Parsing {md_path}...")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12,
        alignment=1 # Center
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1D4ED8'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#374151'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E1E1E'),
        backColor=colors.HexColor('#F3F4F6'),
        borderColor=colors.HexColor('#E5E7EB'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # Title Page
    story.append(Spacer(1, 40))
    story.append(Paragraph("EnLang Core Language Reference", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Book 1: Master Reference & Architecture Guide</b>", ParagraphStyle('Sub', parent=title_style, fontSize=12, leading=15, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563EB'), spaceAfter=20))
    story.append(Spacer(1, 20))

    in_code = False
    code_lines = []

    for line in lines:
        raw = line.rstrip('\n')

        # Horizontal Rule / Page Break separator
        if raw.strip() == "---":
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'), spaceAfter=10))
            continue

        # Code block toggle
        if raw.strip().startswith("```"):
            if in_code:
                in_code = False
                code_text = "\n".join(code_lines)
                story.append(Preformatted(code_text, code_style))
                code_lines = []
            else:
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(raw)
            continue

        if not raw.strip():
            continue

        # Markdown Headings
        if raw.startswith('# '):
            text = raw[2:].strip()
            story.append(Paragraph(text, h1_style))
        elif raw.startswith('## '):
            text = raw[3:].strip()
            story.append(Paragraph(text, h2_style))
        elif raw.startswith('### '):
            text = raw[4:].strip()
            story.append(Paragraph(text, h3_style))
        elif raw.startswith('- ') or raw.startswith('* '):
            text = "• " + raw[2:].strip()
            # Clean bold text markdown
            text_fmt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text_fmt = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text_fmt)
            story.append(Paragraph(text_fmt, body_style))
        else:
            text_fmt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw)
            text_fmt = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text_fmt)
            story.append(Paragraph(text_fmt, body_style))

    doc.build(story)
    print(f"PDF Successfully compiled to {pdf_path}!")

def main():
    md_files = sorted(glob.glob("part*.md"))
    master_md = "book1_master.md"
    pdf_out = "book1_enlang_core_language.pdf"

    with open(master_md, "w", encoding="utf-8") as outfile:
        for f in md_files:
            with open(f, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")

    build_pdf_from_markdown(master_md, pdf_out)

if __name__ == "__main__":
    main()
