from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'The Road Beyond Hazelwood - 5x8 Fiction Format.docx'
TARGET = ROOT / 'The Road Beyond Hazelwood - 4.25x6.87 Print Edition.docx'

doc = Document(SOURCE)


def set_font(run, size, *, italic=False, bold=False, all_caps=False):
    run.font.name = 'Garamond'
    run.font.size = Pt(size)
    run.font.italic = italic
    run.font.bold = bold
    run.font.all_caps = all_caps
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.rFonts
    if fonts is None:
        fonts = OxmlElement('w:rFonts')
        rpr.insert(0, fonts)
    fonts.set(qn('w:ascii'), 'Garamond')
    fonts.set(qn('w:hAnsi'), 'Garamond')


def set_page_layout(section):
    section.page_width = Inches(4.25)
    section.page_height = Inches(6.87)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.58)
    section.left_margin = Inches(0.67)  # inside when mirrorMargins is enabled
    section.right_margin = Inches(0.50)  # outside when mirrorMargins is enabled
    section.header_distance = Inches(0.25)
    section.footer_distance = Inches(0.27)


settings = doc.settings._element
if settings.find(qn('w:mirrorMargins')) is None:
    settings.append(OxmlElement('w:mirrorMargins'))

for section in doc.sections:
    set_page_layout(section)

# The manuscript body is set in a compact, readable novel face for this trim.
normal = doc.styles['Normal']
normal.font.name = 'Garamond'
normal.font.size = Pt(10)
normal._element.rPr.rFonts.set(qn('w:ascii'), 'Garamond')
normal._element.rPr.rFonts.set(qn('w:hAnsi'), 'Garamond')
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal.paragraph_format.line_spacing = Pt(12)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.widow_control = True

for para in doc.paragraphs:
    if para.style.name == 'Normal' and para.text.strip():
        fmt = para.paragraph_format
        fmt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        fmt.line_spacing = Pt(12)
        fmt.space_before = Pt(0)
        fmt.space_after = Pt(0)
        fmt.widow_control = True
        if fmt.first_line_indent is not None and fmt.first_line_indent > 0:
            fmt.first_line_indent = Inches(0.18)
        for run in para.runs:
            set_font(run, 10)

# The existing title page remains the first, unnumbered page.
title = doc.paragraphs[0]
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.first_line_indent = Inches(0)
title.paragraph_format.space_before = Pt(140)
title.paragraph_format.space_after = Pt(0)
for run in title.runs:
    set_font(run, 22)

# Start the contents section on a recto, leaving the title page's verso blank.
title_break = doc.paragraphs[1]._p.get_or_add_pPr().find(qn('w:sectPr'))
title_break_type = title_break.find(qn('w:type'))
if title_break_type is None:
    title_break_type = OxmlElement('w:type')
    title_break.insert(0, title_break_type)
title_break_type.set(qn('w:val'), 'oddPage')
doc.paragraphs[1].paragraph_format.page_break_before = False

# Collect chapter headings and subtitles before inserting the contents page.
chapters = []
for idx, para in enumerate(doc.paragraphs):
    if para.style.name == 'Heading 1':
        subtitle = doc.paragraphs[idx + 1].text.strip()
        chapters.append((para, subtitle))

# Chapter openings use consistent centered display and begin on a fresh page.
for heading, _ in chapters:
    heading.paragraph_format.page_break_before = True
    heading.paragraph_format.space_before = Pt(34)
    heading.paragraph_format.space_after = Pt(7)
    heading.paragraph_format.keep_with_next = True
    heading.paragraph_format.keep_together = True
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in heading.runs:
        set_font(run, 9.5, all_caps=True)

for heading, _ in chapters:
    subtitle = heading._p.getnext()
    # Resolve the backing python-docx Paragraph without relying on stale indices.
    p = next(p for p in doc.paragraphs if p._p is subtitle)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(21)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.keep_together = True
    for run in p.runs:
        set_font(run, 12.5, italic=True)

# Insert a one-page table of contents after the title page. Its pageBreakBefore
# leaves the title's verso blank, and the section break after it starts Chapter 1
# on a recto even if the contents later grows to two pages.
first_heading = chapters[0][0]
toc_title = first_heading.insert_paragraph_before()
toc_text = toc_title.add_run('CONTENTS')
toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
toc_title.paragraph_format.page_break_before = False
toc_title.paragraph_format.space_before = Pt(26)
toc_title.paragraph_format.space_after = Pt(17)
toc_title.paragraph_format.keep_with_next = True
set_font(toc_text, 14, all_caps=True)

toc_entries = []
for number, (heading, subtitle) in enumerate(chapters, 1):
    entry = first_heading.insert_paragraph_before()
    entry.alignment = WD_ALIGN_PARAGRAPH.LEFT
    entry.paragraph_format.left_indent = Inches(0)
    entry.paragraph_format.first_line_indent = Inches(0)
    entry.paragraph_format.space_before = Pt(0)
    entry.paragraph_format.space_after = Pt(0)
    entry.paragraph_format.line_spacing = Pt(10.5)
    entry.paragraph_format.keep_together = True
    entry.paragraph_format.widow_control = True
    tabs = entry.paragraph_format.tab_stops
    tabs.add_tab_stop(Inches(3.08), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    label = entry.add_run(f'{number}.  {subtitle}')
    set_font(label, 8.5)
    entry.add_run().add_tab()
    page_run = entry.add_run('0')
    set_font(page_run, 8.5)
    toc_entries.append((entry, number))
toc_entries.sort(key=lambda item: item[1])

contents_spacer = toc_title.insert_paragraph_before('\u200b')
contents_spacer.paragraph_format.space_before = Pt(0)
contents_spacer.paragraph_format.space_after = Pt(0)
contents_spacer.paragraph_format.line_spacing = Pt(1)
for run in contents_spacer.runs:
    set_font(run, 1)

# Force a truly blank title-page verso before the contents, then a blank verso
# after the contents so the story itself starts on a right-hand page.
blank_before_story = first_heading.insert_paragraph_before('\u200b')
blank_before_story.paragraph_format.page_break_before = True
blank_before_story.paragraph_format.space_before = Pt(0)
blank_before_story.paragraph_format.space_after = Pt(0)
blank_before_story.paragraph_format.line_spacing = Pt(1)
for run in blank_before_story.runs:
    set_font(run, 1)

# Word section properties are stored at section ends. Add an odd-page section
# break at the end of the contents and each chapter so all chapters start recto.
main_section_template = deepcopy(doc.sections[-1]._sectPr)
for ref in list(main_section_template.findall(qn('w:headerReference'))) + list(main_section_template.findall(qn('w:footerReference'))):
    # The references point to the same document-level header/footer stories, so
    # cloned references retain the centered page number in each main section.
    pass


def prepare_sectpr(template, page_number_start=None, page_format=None, break_type='oddPage'):
    sect = deepcopy(template)
    typ = sect.find(qn('w:type'))
    if typ is None:
        typ = OxmlElement('w:type')
        sect.insert(0, typ)
    typ.set(qn('w:val'), break_type)
    pg = sect.find(qn('w:pgNumType'))
    if pg is not None:
        sect.remove(pg)
    if page_number_start is not None or page_format is not None:
        pg = OxmlElement('w:pgNumType')
        if page_format:
            pg.set(qn('w:fmt'), page_format)
        if page_number_start is not None:
            pg.set(qn('w:start'), str(page_number_start))
        sect.insert(0, pg)
    return sect


def set_section_break_after(paragraph, template, *, page_number_start=None, page_format=None, break_type='oddPage'):
    ppr = paragraph._p.get_or_add_pPr()
    existing = ppr.find(qn('w:sectPr'))
    if existing is not None:
        ppr.remove(existing)
    ppr.append(prepare_sectpr(template, page_number_start, page_format, break_type))


# The front matter section contains the blank verso and contents but has no
# visible folios. The odd-page break then starts the Arabic-numbered story.
toc_sect = deepcopy(main_section_template)
for ref in list(toc_sect.findall(qn('w:headerReference'))) + list(toc_sect.findall(qn('w:footerReference'))):
    toc_sect.remove(ref)
set_section_break_after(contents_spacer, toc_sect, break_type='nextPage')
set_section_break_after(blank_before_story, toc_sect, break_type='nextPage')

# Chapter One follows the blank page already placed in the front matter. Later
# chapter headings retain a hard page break; additional blank versos are added
# after inspecting the rendered page sequence.
chapters[0][0].paragraph_format.page_break_before = False

# The single story section starts with Arabic page 1 at Chapter One.
final_sect = doc.sections[-1]._sectPr
pg = final_sect.find(qn('w:pgNumType'))
if pg is None:
    pg = OxmlElement('w:pgNumType')
    final_sect.insert(0, pg)
pg.set(qn('w:fmt'), 'decimal')
pg.set(qn('w:start'), '1')

# Keep all footer folios centered and modest.
for section in doc.sections:
    for footer in (section.footer, section.first_page_footer):
        for para in footer.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                set_font(run, 8.5)

doc.save(TARGET)
print(f'Wrote {TARGET} ({TARGET.stat().st_size} bytes)')
print('TOC entries:', len(toc_entries))
