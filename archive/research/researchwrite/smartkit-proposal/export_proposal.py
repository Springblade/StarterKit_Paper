"""Export the proposal with researchwrite's formatter, then normalize Word links."""
from pathlib import Path
import re
import runpy
import sys

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Pt

workspace = Path(__file__).resolve().parents[4]
source = workspace / 'research' / 'smartkit-proposal.md'
target = source.with_suffix('.docx')
formatter = Path('C:/Users/wayad/.codex/skills/nature-proposal-writer/scripts/build_proposal_docx.py')
sys.argv = [str(formatter), str(source), str(target)]
runpy.run_path(str(formatter), run_name='__main__')
document = Document(target)

# The bundled formatter preserves Markdown links as text; make them Word links.
for paragraph in document.paragraphs:
    if paragraph.style.name == 'Heading 2':
        paragraph.style = document.styles['Heading 1']
    elif paragraph.style.name == 'Heading 3':
        paragraph.style = document.styles['Heading 2']
    text = paragraph.text
    matches = list(re.finditer(r'\[([^\]]+)\]\((https?://[^)]+)\)', text))
    if not matches:
        continue
    paragraph.clear()
    cursor = 0
    for match in matches:
        paragraph.add_run(text[cursor:match.start()])
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), paragraph.part.relate_to(match[2], RT.HYPERLINK, is_external=True))
        run = OxmlElement('w:r')
        properties = OxmlElement('w:rPr')
        underline = OxmlElement('w:u')
        underline.set(qn('w:val'), 'single')
        properties.append(underline)
        run.append(properties)
        label = OxmlElement('w:t')
        label.text = match[1]
        run.append(label)
        hyperlink.append(run)
        paragraph._p.append(hyperlink)
        cursor = match.end()
    paragraph.add_run(text[cursor:])

for style_name in ['Normal', 'Heading 1', 'Heading 2', 'Heading 3']:
    document.styles[style_name].element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

for table in document.tables:
    repeat_header = OxmlElement('w:tblHeader')
    table.rows[0]._tr.get_or_add_trPr().append(repeat_header)

footer = document.sections[0].footer.paragraphs[0]
footer.alignment = 2
footer.add_run('SmartKit | Proposal 0.1 | ')
page = OxmlElement('w:fldSimple')
page.set(qn('w:instr'), 'PAGE')
footer._p.append(page)
for run in footer.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9)

document.save(target)

# Check every paragraph and table cell survived export without changing claims.
expected = []
for line in source.read_text(encoding='utf-8').splitlines():
    if not line.strip() or re.fullmatch(r'\|[-| :]+\|', line):
        continue
    if line.startswith('|'):
        expected.extend(cell.strip() for cell in line.strip('|').split('|'))
    else:
        expected.append(re.sub(r'^#{1,3} ', '', line))
expected_text = '\n'.join(expected)
expected_text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', expected_text)
actual = []
for paragraph in document.paragraphs:
    actual.append(''.join(node.text or '' for node in paragraph._p.iter(qn('w:t'))))
for table in document.tables:
    actual.extend(cell.text for row in table.rows for cell in row.cells)
actual_text = '\n'.join(actual)
normalize = lambda value: re.sub(r'\s+', ' ', value).strip()
for item in expected_text.splitlines():
    assert normalize(item) in normalize(actual_text), f'Missing exported text: {item[:90]}'
assert len(document.tables) == 2
assert sum(rel.reltype == RT.HYPERLINK for rel in document.part.rels.values()) == 7
print('Verified: proposal text, two tables, and seven source hyperlinks.')
