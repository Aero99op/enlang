import os
import re
from fpdf import FPDF

class PDFRulebook(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'EnLang Official Language Rulebook & Specification (v1.0)', 0, new_x="RIGHT", new_y="TOP", align='L')
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(10, 18, 200, 18)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, new_x="RIGHT", new_y="TOP", align='C')

def clean_formatting(text):
    # Remove emojis and characters above 255
    text = re.sub(r'[^\x00-\xFF]', '', text)
    text = text.replace('**', '')
    text = text.replace('`', '')
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    return text.strip()

def generate_pdf():
    pdf = PDFRulebook()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Cover Title
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(40, 50, 90)
    pdf.cell(0, 14, 'EnLang Master Rulebook', new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font('Helvetica', 'I', 12)
    pdf.set_text_color(100, 110, 130)
    pdf.cell(0, 8, 'Universal Natural English Programming Language & Specification', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(8)

    # Read RULEBOOK.md
    with open('RULEBOOK.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_code_block = False
    code_text = []

    for line in lines:
        raw_line = line.rstrip()

        # Handle Code Blocks
        if raw_line.startswith("```"):
            if in_code_block:
                in_code_block = False
                pdf.set_font('Courier', '', 8)
                pdf.set_fill_color(242, 244, 248)
                pdf.set_draw_color(210, 215, 225)
                pdf.set_text_color(30, 40, 60)
                
                block_str = "\n".join([clean_formatting(cl) for cl in code_text])
                pdf.multi_cell(0, 4.5, block_str, border=1, fill=True)
                pdf.ln(3)
                code_text = []
            else:
                in_code_block = True
                code_text = []
            continue

        if in_code_block:
            code_text.append(raw_line)
            continue

        clean_l = clean_formatting(raw_line)
        if not clean_l:
            continue

        # Headings
        if raw_line.startswith('# '):
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 16)
            pdf.set_text_color(30, 60, 120)
            pdf.cell(0, 10, clean_l.replace('# ', '').strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif raw_line.startswith('## '):
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 13)
            pdf.set_text_color(40, 80, 150)
            pdf.cell(0, 8, clean_l.replace('## ', '').strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif raw_line.startswith('### '):
            pdf.ln(2)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 6, clean_l.replace('### ', '').strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif raw_line.startswith('|') and '---' in raw_line:
            continue
        elif raw_line.startswith('|'):
            pdf.set_font('Helvetica', '', 8.5)
            pdf.set_text_color(40, 40, 40)
            cells = [clean_formatting(c) for c in raw_line.split('|')[1:-1]]
            row_str = " | ".join(cells)
            pdf.multi_cell(0, 4.5, row_str)
            pdf.ln(1)
        elif raw_line.startswith('- ') or raw_line.startswith('* '):
            pdf.set_font('Helvetica', '', 9.5)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, f" - {clean_l[2:] if len(clean_l)>2 else clean_l}")
            pdf.ln(1)
        else:
            pdf.set_font('Helvetica', '', 9.5)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, clean_l)
            pdf.ln(1)

    pdf.output("EnLang_Rulebook.pdf")
    print("EnLang_Rulebook.pdf generated successfully!")

if __name__ == "__main__":
    generate_pdf()
