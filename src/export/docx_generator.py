import re
from io import BytesIO
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def markdown_to_docx(title: str, markdown_content: str) -> BytesIO:
    doc = Document()

    # Marges
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    # Page de garde
    heading = doc.add_heading(title, level=0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading.runs[0].font.color.rgb = RGBColor(0x1A, 0x37, 0x6C)
    doc.add_paragraph()

    # Conversion Markdown → DOCX
    lines = markdown_content.split("\n")
    for line in lines:
        line = line.rstrip()

        if line.startswith("### "):
            p = doc.add_heading(line[4:], level=3)
            _style_heading(p, 11, RGBColor(0x2E, 0x6D, 0xA0))

        elif line.startswith("## "):
            p = doc.add_heading(line[3:], level=2)
            _style_heading(p, 13, RGBColor(0x1A, 0x37, 0x6C))

        elif line.startswith("# "):
            p = doc.add_heading(line[2:], level=1)
            _style_heading(p, 14, RGBColor(0x1A, 0x37, 0x6C))

        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(line[2:], style="List Bullet")
            p.runs[0].font.size = Pt(10) if p.runs else None

        elif line.startswith("  - ") or line.startswith("  * "):
            doc.add_paragraph(line[4:], style="List Bullet 2")

        elif re.match(r"^\d+\.\s", line):
            text = re.sub(r"^\d+\.\s", "", line)
            doc.add_paragraph(text, style="List Number")

        elif line == "" or line == "---":
            if line == "---":
                doc.add_paragraph().add_run().add_break()
            else:
                doc.add_paragraph()

        elif line.startswith("**") and line.endswith("**"):
            p = doc.add_paragraph()
            run = p.add_run(line[2:-2])
            run.bold = True
            run.font.size = Pt(10)

        else:
            p = doc.add_paragraph()
            _parse_inline(p, line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def _style_heading(paragraph, size: int, color: RGBColor):
    for run in paragraph.runs:
        run.font.size = Pt(size)
        run.font.color.rgb = color


def _parse_inline(paragraph, text: str):
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            run = paragraph.add_run(part)
        run.font.size = Pt(10)
