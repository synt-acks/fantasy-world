from pathlib import Path
import re

from docx import Document
from docx.shared import Pt
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / 'The Road Beyond Hazelwood - 4.25x6.87 Print Edition.docx'
PDF = ROOT / 'tmp' / 'rendered_425x687' / 'The Road Beyond Hazelwood - 4.25x6.87 Print Edition.pdf'

reader = PdfReader(str(PDF))
page_texts = [page.extract_text() or '' for page in reader.pages]
doc = Document(DOCX)
headings = [p for p in doc.paragraphs if p.style.name == 'Heading 1']

pages = []
for heading in headings:
    needle = heading.text.upper()
    match = next((i + 1 for i, text in enumerate(page_texts) if needle in text), None)
    if match is None:
        raise RuntimeError(f'Could not locate chapter heading in rendered PDF: {heading.text}')
    pages.append(match)

inserted = 0
blanked = []
for index, (heading, page) in enumerate(zip(headings, pages)):
    current_page = page + inserted
    if index == 0:
        continue
    if current_page % 2 == 0:
        blank = heading.insert_paragraph_before('\u200b')
        blank.paragraph_format.page_break_before = True
        blank.paragraph_format.space_before = Pt(0)
        blank.paragraph_format.space_after = Pt(0)
        blank.paragraph_format.line_spacing = Pt(1)
        for run in blank.runs:
            run.font.name = 'Garamond'
            run.font.size = Pt(1)
        inserted += 1
        blanked.append((heading.text, current_page))

doc.save(DOCX)
print('chapter_opener_pages_before:', pages)
print('blank_pages_inserted_before:', blanked)
print('edition_pages_before:', len(page_texts))
