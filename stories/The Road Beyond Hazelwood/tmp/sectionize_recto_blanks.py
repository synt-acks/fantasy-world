from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / 'The Road Beyond Hazelwood - 4.25x6.87 Print Edition.docx'
doc = Document(DOCX)
if len(doc.sections) != 4:
    raise RuntimeError(f'Expected 4 initial sections, found {len(doc.sections)}')

main_template = deepcopy(doc.sections[-1]._sectPr)
blank_template = deepcopy(main_template)
for ref in list(blank_template.findall(qn('w:headerReference'))) + list(blank_template.findall(qn('w:footerReference'))):
    blank_template.remove(ref)
pg = blank_template.find(qn('w:pgNumType'))
if pg is not None:
    blank_template.remove(pg)


def make_section_end(paragraph, template, start=None):
    ppr = paragraph._p.get_or_add_pPr()
    old = ppr.find(qn('w:sectPr'))
    if old is not None:
        ppr.remove(old)
    sect = deepcopy(template)
    typ = sect.find(qn('w:type'))
    if typ is None:
        typ = OxmlElement('w:type')
        sect.insert(0, typ)
    typ.set(qn('w:val'), 'nextPage')
    pg = sect.find(qn('w:pgNumType'))
    if pg is not None:
        sect.remove(pg)
    if start is not None:
        pg = OxmlElement('w:pgNumType')
        pg.set(qn('w:fmt'), 'decimal')
        pg.set(qn('w:start'), str(start))
        sect.insert(0, pg)
    ppr.append(sect)


paragraphs = doc.paragraphs
headings = [(i, p) for i, p in enumerate(paragraphs) if p.style.name == 'Heading 1']
blank_section_indices = []
section_index = 3  # the story section begins after the title and contents pages

for chapter_index, ((_, _), (heading_pos, heading)) in enumerate(zip(headings, headings[1:])):
    heading.paragraph_format.page_break_before = False
    preceding = paragraphs[heading_pos - 1]
    has_blank = preceding.text == '\u200b' and preceding.paragraph_format.page_break_before is True
    chapter_end = paragraphs[heading_pos - 2] if has_blank else preceding
    make_section_end(chapter_end, main_template, start=1 if chapter_index == 0 else None)
    if has_blank:
        preceding.paragraph_format.page_break_before = False
        make_section_end(preceding, blank_template)
        blank_section_indices.append(section_index + 1)
        section_index += 2
    else:
        section_index += 1

# The final chapter section continues the running Arabic folios.
final_sect = doc.sections[-1]._sectPr
pg = final_sect.find(qn('w:pgNumType'))
if pg is not None:
    final_sect.remove(pg)

doc.save(DOCX)

# Sections with intentionally blank pages get their own empty footer story, so
# the verso remains blank while the next chapter's folio numbering continues.
doc = Document(DOCX)
for index in blank_section_indices:
    section = doc.sections[index]
    section.footer.is_linked_to_previous = False
    for para in section.footer.paragraphs:
        para.clear()
        para.alignment = 1
    section.header.is_linked_to_previous = False
    for para in section.header.paragraphs:
        para.clear()

doc.save(DOCX)
print('recto_blank_sections:', blank_section_indices)
print('total_sections:', len(doc.sections))
