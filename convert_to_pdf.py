import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_chrome(num_pages)
            super().showPage()
        super().save()

    def _draw_chrome(self, total):
        pg = self._pageNumber
        W = letter[0]
        if pg == 1:
            return
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 11 * inch - 28, "EnLang for Developers  —  v2.0 Enterprise Specification  —  Author: Spandan Prayas Patra")
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.4)
        self.line(54, 11 * inch - 34, W - 54, 11 * inch - 34)
        self.line(54, 44, W - 54, 44)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(W - 54, 28, f"Page {pg} of {total}")
        self.drawString(54, 28, "Copyright 2026 Spandan Prayas Patra. All rights reserved.")
        self.restoreState()


def build_styles():
    BASE      = colors.HexColor("#0f172a")
    PRIMARY   = colors.HexColor("#4f46e5")
    ACCENT    = colors.HexColor("#0284c7")
    MUTED     = colors.HexColor("#64748b")
    CODE_BG   = colors.HexColor("#f1f5f9")
    CODE_FG   = colors.HexColor("#0f172a")
    TEXT      = colors.HexColor("#1e293b")

    s = getSampleStyleSheet()

    COVER_TITLE = ParagraphStyle('CoverTitle', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=PRIMARY, spaceAfter=8, alignment=0)

    COVER_SUB = ParagraphStyle('CoverSub', parent=s['Normal'],
        fontName='Helvetica-Oblique', fontSize=13, leading=17,
        textColor=MUTED, spaceAfter=10, alignment=0)

    COVER_META = ParagraphStyle('CoverMeta', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=BASE, spaceAfter=4, alignment=0)

    QUOTE = ParagraphStyle('Quote', parent=s['Normal'],
        fontName='Helvetica-Oblique', fontSize=9.5, leading=13.5,
        textColor=colors.HexColor("#334155"), spaceBefore=8, spaceAfter=10,
        leftIndent=15, rightIndent=15)

    H1 = ParagraphStyle('H1', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=PRIMARY, spaceBefore=18, spaceAfter=8, keepWithNext=True)

    H2 = ParagraphStyle('H2', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=12.5, leading=16,
        textColor=BASE, spaceBefore=12, spaceAfter=5, keepWithNext=True)

    H3 = ParagraphStyle('H3', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=ACCENT, spaceBefore=10, spaceAfter=4, keepWithNext=True)

    BODY = ParagraphStyle('Body', parent=s['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=TEXT, spaceAfter=5)

    CODE = ParagraphStyle('Code', parent=s['Normal'],
        fontName='Courier', fontSize=8, leading=10.5,
        textColor=CODE_FG, backColor=CODE_BG,
        borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5,
        borderPadding=6, spaceBefore=5, spaceAfter=7)

    TABLE_HEADER = ParagraphStyle('TH', parent=s['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.white)

    TABLE_CELL = ParagraphStyle('TC', parent=s['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11,
        textColor=TEXT)

    return dict(cover_title=COVER_TITLE, cover_sub=COVER_SUB, cover_meta=COVER_META,
                quote=QUOTE, h1=H1, h2=H2, h3=H3, body=BODY, code=CODE,
                table_header=TABLE_HEADER, table_cell=TABLE_CELL)


def escape_xml(s: str) -> str:
    """Escapes XML entities in raw text before applying custom ReportLab tags."""
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    return s


def fmt(text: str) -> str:
    """Formats markdown bold, italic, and backtick inline code into ReportLab XML."""
    # Placeholders for inline code blocks to protect them during escaping
    code_placeholders = []
    
    def repl_code(m):
        code_text = escape_xml(m.group(1))
        idx = len(code_placeholders)
        code_placeholders.append(f'<font face="Courier" size="8.5" color="#0284c7">{code_text}</font>')
        return f"__CODE_PH_{idx}__"

    text = re.sub(r'`(.*?)`', repl_code, text)
    
    # Escape rest of the text
    text = escape_xml(text)
    
    # Apply bold & italic markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Restore code placeholders
    for idx, ph in enumerate(code_placeholders):
        text = text.replace(f"__CODE_PH_{idx}__", ph)
        
    return text


def parse_md_table(lines, start, styles):
    rows = []
    i = start
    while i < len(lines) and '|' in lines[i]:
        raw = lines[i].strip().strip('|')
        cells = [c.strip() for c in raw.split('|')]
        if all(re.match(r'^[-: ]+$', c) for c in cells):
            i += 1
            continue
        rows.append(cells)
        i += 1

    if not rows:
        return None, start

    header = rows[0]
    data_rows = rows[1:]

    PRIMARY = colors.HexColor("#4f46e5")
    ALT_BG  = colors.HexColor("#f8fafc")
    BORDER  = colors.HexColor("#e2e8f0")

    table_data = [[Paragraph(fmt(c), styles['table_header']) for c in header]]
    for row in data_rows:
        table_data.append([Paragraph(fmt(c), styles['table_cell']) for c in row])

    col_count = len(header)
    col_width = (letter[0] - 108) / col_count

    t = Table(table_data, colWidths=[col_width] * col_count)
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ALT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    t.setStyle(ts)
    return t, i


def build_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        raw_lines = f.read().splitlines()

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)

    styles = build_styles()
    story = []

    in_code  = False
    code_buf = []
    i = 0

    while i < len(raw_lines):
        line = raw_lines[i]
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith('```'):
            if in_code:
                in_code = False
                safe = []
                for cl in code_buf:
                    cl2 = escape_xml(cl).replace(' ', '&nbsp;').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
                    safe.append(cl2)
                code_text = '<br/>'.join(safe)
                story.append(Paragraph(code_text, styles['code']))
                code_buf = []
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Blank line
        if not stripped:
            story.append(Spacer(1, 3))
            i += 1
            continue

        # HR
        if re.match(r'^[-*_]{3,}$', stripped):
            story.append(HRFlowable(width='100%', thickness=0.5,
                color=colors.HexColor("#cbd5e1"), spaceBefore=8, spaceAfter=8))
            i += 1
            continue

        # Headers
        if stripped.startswith('# ') and not stripped.startswith('## '):
            text = stripped[2:].strip()
            story.append(Paragraph(fmt(text), styles['cover_title']))
            i += 1
            continue

        if stripped.startswith('### *') and stripped.endswith('*'):
            story.append(Paragraph(fmt(stripped[5:-1]), styles['cover_sub']))
            i += 1
            continue

        if stripped.startswith('## '):
            story.append(Paragraph(fmt(stripped[3:]), styles['h1']))
            i += 1
            continue

        if stripped.startswith('### '):
            story.append(Paragraph(fmt(stripped[4:]), styles['h2']))
            i += 1
            continue

        if stripped.startswith('#### '):
            story.append(Paragraph(fmt(stripped[5:]), styles['h3']))
            i += 1
            continue

        # Blockquote
        if stripped.startswith('>'):
            story.append(Paragraph(fmt(stripped.lstrip('> ').strip()), styles['quote']))
            i += 1
            continue

        # Cover meta
        if stripped.startswith('**Author:**') or stripped.startswith('**Version:**') or stripped.startswith('**Publisher:**'):
            story.append(Paragraph(fmt(stripped), styles['cover_meta']))
            i += 1
            continue

        # Markdown table
        if '|' in stripped and stripped.startswith('|'):
            tbl, i = parse_md_table(raw_lines, i, styles)
            if tbl:
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 6))
            continue

        # Table separator lines (skip)
        if stripped.startswith('|') and re.match(r'^[| \-:]+$', stripped):
            i += 1
            continue

        # List items
        if re.match(r'^[-*+]\s', stripped) or re.match(r'^\d+\.\s', stripped):
            text = re.sub(r'^[-*+]\s', '', stripped)
            text = re.sub(r'^\d+\.\s', '', text)
            story.append(Paragraph(f"&bull;&nbsp;&nbsp;{fmt(text)}", styles['body']))
            i += 1
            continue

        # Regular paragraph
        story.append(Paragraph(fmt(stripped), styles['body']))
        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    size = os.path.getsize(pdf_path)
    print(f"[SUCCESS] PDF generated: {pdf_path}")
    print(f"[INFO]    File size: {size:,} bytes ({size // 1024} KB)")


if __name__ == '__main__':
    build_pdf(
        r'd:\enlangg\ENLANG_FOR_DEVELOPERS_BOOK.md',
        r'd:\enlangg\ENLANG_FOR_DEVELOPERS_BOOK.pdf'
    )
