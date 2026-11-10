"""Installation helper: retain the approved layout, strip all source PR data."""
import argparse
import copy
import zipfile
from xml.etree import ElementTree as ET
from track_pr import Workbook, Tab, TEMPLATE, tag, xml, P, R

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='Approved source workbook; read only')
    args = parser.parse_args()
    from pathlib import Path
    book = Workbook(Path(args.source))
    root = ET.fromstring(book.parts['xl/worksheets/sheet1.xml'])
    relationships = ET.Element('Relationships', xmlns=P)
    tab = Tab(book, root, relationships)
    # Remove data rows before clearing text, while section anchors still exist.
    for section in ['WAITING FOR REVIEW', 'HUMAN REVIEWS', 'COPILOT REVIEWS']:
        sample = copy.deepcopy(tab.body(section)[0])
        for column in 'ABCDEF':
            tab.put(sample, column, '')
        tab.put(sample, 'A', 'Reviewer')
        tab.replace_body(section, [sample], [None])
    # The only retained text consists of layout labels and section titles.
    keep = {'PR LINK', 'PR TITLE', 'AUTHOR', 'PR CREATED', 'READY FOR HUMAN REVIEW',
        'SOURCE BRANCH', 'TARGET BRANCH', 'CURRENT STATUS', 'PR AGE — CALENDAR TIME',
        'PR AGE — WORKING HOURS', 'APPROVALS RECEIVED', 'REVIEW', 'REVIEWER',
        'Reviewer', 'REVIEW DATES', 'COMMENTS', 'COMMENTS RESOLVED?', 'MY CHANGE PUSH',
        'MY TIME TO PUSH CHANGES', 'REVIEW REQUESTED', 'TIME WAITING FOR REVIEW'}
    for row in tab.rows():
        for column, cell in tab.cells(row).items():
            value = book.text(cell)
            if value.startswith('01   '):
                tab.put(row, column, '01   SUMMARY')
            elif value.startswith('02   '):
                tab.put(row, column, '02   COPILOT REVIEWS')
            elif value.startswith('03   '):
                tab.put(row, column, '03   HUMAN REVIEWS')
            elif value.startswith('04   '):
                tab.put(row, column, '04   WAITING FOR REVIEW')
            elif value not in keep:
                tab.put(row, column, '')
    tab.put(tab.rows()[0], 'A', 'PR REVIEW TRACKER')
    tab.put(tab.rows()[1], 'A', 'Updated:')
    for label in ['AUTHOR', 'PR CREATED', 'READY FOR HUMAN REVIEW', 'SOURCE BRANCH',
        'TARGET BRANCH', 'CURRENT STATUS', 'PR AGE — CALENDAR TIME',
        'PR AGE — WORKING HOURS', 'APPROVALS RECEIVED']:
        tab.set_label_value(label, 'Unavailable')
    link_row = next(row for row in tab.rows() if 'PR LINK' in tab.row_text(row))
    tab.put(link_row, 'C', 'https://github.com/owner/repo/pull/0')
    for section in ['COPILOT REVIEWS', 'HUMAN REVIEWS', 'WAITING FOR REVIEW']:
        tab.put(tab.body(section)[0], 'A', 'Reviewer')
    hyperlinks = root.find(tag('hyperlinks'))
    for node in list(hyperlinks):
        hyperlinks.remove(node)
    ET.SubElement(hyperlinks, tag('hyperlink'), ref='C' + link_row.get('r'), attrib={'{' + R + '}id': 'rId1'})
    ET.SubElement(relationships, 'Relationship', Id='rId1', Type=R + '/hyperlink', Target='https://github.com', TargetMode='External')
    book.book.find(tag('sheets'))[0].set('name', 'Template')
    for node in book.book.find(tag('definedNames')):
        if node.get('name') == '_xlnm.Print_Area':
            node.text = f"'Template'!$A$1:$F${len(tab.rows())}"
        elif node.get('name') == '_xlnm.Print_Titles':
            node.text = "'Template'!$1:$2"
    root.find(tag('rowBreaks'))[0].set('id', str(int(tab.section('HUMAN REVIEWS').get('r')) - 1))
    root.find(tag('headerFooter')).find(tag('oddFooter')).text = '&RPage &P of &N'
    book.parts['xl/workbook.xml'] = xml(book.book)
    book.parts['xl/worksheets/sheet1.xml'] = xml(root)
    book.parts['xl/worksheets/_rels/sheet1.xml.rels'] = xml(relationships)
    TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    if TEMPLATE.exists():
        raise ValueError('Template already exists; inspect it before replacing it.')
    with zipfile.ZipFile(TEMPLATE, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, content in book.parts.items():
            assert not any(value in content for value in [b'6366', b'rahul-synacor', b'PREAPPS-9479', b'Zimbra/zm-x-web'])
            archive.writestr(name, content)
    print('Created sanitized template:', TEMPLATE)

if __name__ == '__main__':
    main()
