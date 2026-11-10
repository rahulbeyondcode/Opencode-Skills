"""Create or refresh a PR tab in one workbook in the caller's working folder.

Usage: python3 track_pr.py PR_URL --directory SESSION_WORKING_DIRECTORY
Python standard library and authenticated gh only. No GitHub mutations.
"""
import argparse
import concurrent.futures
import copy
import datetime as dt
import hashlib
import json
import os
import pathlib
import posixpath
import re
import subprocess
import sys
import tempfile
import urllib.parse
import zipfile
from xml.etree import ElementTree as ET

SKILL = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / 'templates' / 'tracker.xlsx'
KNOWN_NAMES = {
    'rahul-synacor': 'Rahul R',
    'silentsakky': 'Saket Patel',
    'lavegupta': 'Lave Gupta',
    'GadhariSachin': 'Sachin Gadhari',
    'miteshsavani810': 'Mitesh Savani',
}
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
S = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P = 'http://schemas.openxmlformats.org/package/2006/relationships'
C = 'http://schemas.openxmlformats.org/package/2006/content-types'
ET.register_namespace('', S)
ET.register_namespace('r', R)
def tag(name):
    return '{' + S + '}' + name
def xml(node):
    return ET.tostring(node, encoding='utf-8', xml_declaration=True)
def parse(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(IST)
def when(value):
    return parse(value).strftime('%a, %d %b %Y, %I:%M %p') if value else 'Unavailable'
def duration(start, end):
    if not start or not end or parse(end) < parse(start):
        return 'Unavailable'
    minutes = int((parse(end) - parse(start)).total_seconds() // 60)
    days, minutes = divmod(minutes, 1440)
    hours, minutes = divmod(minutes, 60)
    return f'{days:02d}d {hours:02d}h {minutes:02d}m'
def working_hours(start, end):
    first, last = parse(start), parse(end)
    day, seconds = first.date(), 0
    while day <= last.date():
        if day.weekday() < 5:
            opening = dt.datetime.combine(day, dt.time(10), IST)
            closing = dt.datetime.combine(day, dt.time(19), IST)
            seconds += max(0, (min(last, closing) - max(first, opening)).total_seconds())
        day += dt.timedelta(days=1)
    return seconds / 3600 * 8 / 9
def who(user):
    name = (user or {}).get('login', '[deleted]')
    return 'Copilot' if name in ('Copilot', 'copilot-pull-request-reviewer[bot]') else name

def check_closed(path):
    locks = [path.parent / ('.~lock.' + path.name + '#'), path.parent / ('~$' + path.name)]
    if any(lock.exists() for lock in locks):
        raise ValueError('The tracker is open. Save and close it, then run this command again: ' + str(path))

def parse_url(value):
    parsed = urllib.parse.urlsplit(value)
    match = re.fullmatch(r'/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/pull/([1-9][0-9]*)(?:/(?:files|commits|checks))?/?', parsed.path)
    if parsed.scheme != 'https' or parsed.netloc.casefold() != 'github.com' or not match or match[1] in {'.', '..'} or match[2] in {'.', '..'}:
        raise ValueError('Supply an https://github.com/OWNER/REPO/pull/NUMBER URL.')
    return match[1], match[2], int(match[3])

def select_workbook(directory, explicit=None):
    directory = pathlib.Path(directory).expanduser().resolve()
    if not directory.is_dir():
        raise ValueError('The output directory must already exist: ' + str(directory))
    if explicit:
        path = pathlib.Path(explicit).expanduser()
        path = (directory / path).resolve() if not path.is_absolute() else path.resolve()
        if path.suffix.casefold() != '.xlsx' or not path.parent.is_dir():
            raise ValueError('Choose an .xlsx path in an existing folder.')
        return path
    standard = directory / 'PR-Review-Tracker.xlsx'
    if standard.exists():
        return standard
    candidates = []
    for path in directory.glob('*.xlsx'):
        if path.name.startswith(('~$', '.')):
            continue
        try:
            book = Workbook(path)
            if any('COPILOT REVIEWS' in ''.join(book.text(c) for c in ET.fromstring(book.parts[p]).iter(tag('c'))) for _, _, p in book.records()):
                candidates.append(path)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError):
            continue
    if len(candidates) > 1:
        raise ValueError('Multiple existing trackers found. Ask which to use, then pass --workbook: ' + ', '.join(p.name for p in candidates))
    return candidates[0] if candidates else standard

class Workbook:
    """Preserve all untouched ZIP parts, sheets, styles, and user-added content."""
    def __init__(self, path):
        self.path = path
        self.is_new = not path.exists()
        self.original_hash = None if self.is_new else hashlib.sha256(path.read_bytes()).digest()
        with zipfile.ZipFile(TEMPLATE if self.is_new else path) as archive:
            self.infos = {i.filename: i for i in archive.infolist()}
            self.parts = {n: archive.read(n) for n in archive.namelist()}
        self.original = dict(self.parts)
        self.book = ET.fromstring(self.parts['xl/workbook.xml'])
        self.rels = ET.fromstring(self.parts['xl/_rels/workbook.xml.rels'])
        self.types = ET.fromstring(self.parts['[Content_Types].xml'])
        self.styles = ET.fromstring(self.parts['xl/styles.xml'])
        self.shared = []
        if 'xl/sharedStrings.xml' in self.parts:
            self.shared = [''.join(t.text or '' for t in item.iter(tag('t'))) for item in ET.fromstring(self.parts['xl/sharedStrings.xml'])]
    def text(self, cell):
        if cell.get('t') == 's':
            return self.shared[int(cell.find(tag('v')).text)]
        return ''.join(t.text or '' for t in cell.iter(tag('t'))) or (cell.findtext(tag('v')) or '')
    def records(self):
        rels = {r.get('Id'): r.get('Target') for r in self.rels}
        for index, sheet in enumerate(self.book.find(tag('sheets'))):
            target = rels[sheet.get('{' + R + '}id')]
            path = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            yield index, sheet, path
    def font(self, style):
        xf = self.styles.find(tag('cellXfs'))[int(style)]
        return self.styles.find(tag('fonts'))[int(xf.get('fontId', '0'))]
    def write(self, allowed_parts):
        changed = {n for n, content in self.parts.items() if self.original.get(n) != content}
        assert changed <= allowed_parts, 'Unexpected workbook parts changed: ' + repr(changed - allowed_parts)
        check_closed(self.path)
        assert (not self.path.exists()) if self.is_new else hashlib.sha256(self.path.read_bytes()).digest() == self.original_hash, 'Workbook changed while refreshing; retry after closing it.'
        handle, temporary = tempfile.mkstemp(prefix='.tracker-update-', suffix='.xlsx', dir=self.path.parent)
        try:
            with os.fdopen(handle, 'wb') as stream:
                with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
                    for name, content in self.parts.items():
                        archive.writestr(self.infos.get(name, name), content)
            with zipfile.ZipFile(temporary) as archive:
                assert archive.testzip() is None
                for name in changed:
                    ET.fromstring(archive.read(name))
            check_closed(self.path)
            if self.is_new:
                os.link(temporary, self.path)  # Exclusive creation; never overwrite a concurrent writer.
            else:
                assert hashlib.sha256(self.path.read_bytes()).digest() == self.original_hash, 'Workbook changed while preparing the update; retry.'
                os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return changed

    def import_template_styles(self, template_styles):
        """Append missing styles without changing any existing style indexes."""
        def key(node):
            return node.tag, tuple(sorted(node.attrib.items())), node.text or '', tuple(key(c) for c in node)
        changed = False
        def merge(name, transform=lambda node: node):
            nonlocal changed
            source = template_styles.find(tag(name))
            target = self.styles.find(tag(name))
            if target is None:
                raise ValueError('Unsupported workbook styles: missing ' + name)
            known = {}
            for index, node in enumerate(target):
                known.setdefault(key(node), index)
            mapping = {}
            for index, node in enumerate(source):
                clone = transform(copy.deepcopy(node))
                identity = key(clone)
                if index < len(target) and key(target[index]) == identity:
                    mapping[index] = index
                    continue
                if identity not in known:
                    known[identity] = len(target)
                    target.append(clone)
                    changed = True
                mapping[index] = known[identity]
            target.set('count', str(len(target)))
            return mapping
        maps = {name: merge(name) for name in ['fonts', 'fills', 'borders']}
        def remap(node):
            for field, name in [('fontId', 'fonts'), ('fillId', 'fills'), ('borderId', 'borders')]:
                if field in node.attrib:
                    node.set(field, str(maps[name][int(node.get(field))]))
            if int(node.get('numFmtId', '0')) >= 164:
                raise ValueError('The bundled template must not use custom number formats.')
            return node
        bases = merge('cellStyleXfs', remap)
        def cell_style(node):
            remap(node)
            if 'xfId' in node.attrib:
                node.set('xfId', str(bases[int(node.get('xfId'))]))
            return node
        styles = merge('cellXfs', cell_style)
        if changed:
            self.parts['xl/styles.xml'] = xml(self.styles)
        return styles

class Tab:
    def __init__(self, book, root, relationships):
        self.book, self.root, self.relationships = book, root, relationships
    def rows(self):
        return list(self.root.find(tag('sheetData')))
    def row_text(self, row):
        return ' '.join(self.book.text(c) for c in row)
    def section(self, word):
        return next(r for r in self.rows() if word in self.row_text(r))
    def header(self, word):
        number = int(self.section(word).get('r')) + 1
        return next(r for r in self.rows() if int(r.get('r')) == number)
    def cells(self, row):
        return {re.match('[A-Z]+', c.get('r')).group(): c for c in row}
    def style(self, row, column):
        return self.cells(row)[column].get('s', '0')
    def put(self, row, column, text, style=None):
        cells = self.cells(row)
        cell = cells.get(column)
        if cell is None:
            cell = ET.SubElement(row, tag('c'), r=column + row.get('r'))
        if style is not None:
            cell.set('s', str(style))
        for child in list(cell):
            cell.remove(child)
        cell.set('t', 'inlineStr')
        inline = ET.SubElement(cell, tag('is'))
        font = self.book.font(cell.get('s', '0'))
        def run(value, bold=False):
            rich = ET.SubElement(inline, tag('r'))
            props = ET.SubElement(rich, tag('rPr'))
            ET.SubElement(props, tag('rFont'), val=font.find(tag('name')).get('val', 'Calibri'))
            ET.SubElement(props, tag('b'), val='1' if bold else '0')
            for name in ['color', 'sz']:
                original = font.find(tag(name))
                if original is not None:
                    props.append(copy.deepcopy(original))
            ET.SubElement(rich, tag('t'), attrib={'{http://www.w3.org/XML/1998/namespace}space': 'preserve'}).text = value
        text = str(text)
        for line in text.splitlines(keepends=True) or ['']:
            match = re.match(r'^([A-Za-z][A-Za-z /().—-]*:)(.*)$', line.rstrip('\n'))
            if match:
                run(match[1], True)
                run(match[2] + ('\n' if line.endswith('\n') else ''))
            else:
                run(line, text == 'Unavailable' or line.startswith(('Yes', 'Partly', 'No comments', 'Open', 'Not requested')) or font.find(tag('b')) is not None)
        return cell
    def set_label_value(self, label, value):
        for row in self.rows():
            for column, cell in self.cells(row).items():
                if self.book.text(cell) == label:
                    target = next(r for r in self.rows() if int(r.get('r')) == int(row.get('r')) + 1)
                    self.put(target, column, value)
                    return
        raise ValueError('Summary label not found: ' + label)
    def body(self, word):
        header = int(self.header(word).get('r'))
        rows = self.rows()
        start = next(i for i, r in enumerate(rows) if int(r.get('r')) == header) + 1
        result = []
        for row in rows[start:]:
            if not self.row_text(row).strip() or re.match(r'^0[1-4]\s', self.row_text(row)):
                break
            result.append(row)
        return result
    def replace_body(self, word, new_rows, links):
        old_rows = self.body(word)
        assert old_rows, 'No existing table body: ' + word
        first, last = int(old_rows[0].get('r')), int(old_rows[-1].get('r'))
        delta = len(new_rows) - len(old_rows)
        if delta and self.root.find('.//' + tag('f')) is not None:
            raise ValueError('Cannot shift rows containing user formulas automatically.')
        def shift_reference(value):
            def part(match):
                n = int(match[2])
                return match[1] + str(n + delta if n > last else n)
            return re.sub(r'(\$?[A-Z]+\$?)(\d+)', part, value)
        for row in self.rows():
            if int(row.get('r')) > last:
                row.set('r', str(int(row.get('r')) + delta))
                for cell in row:
                    cell.set('r', shift_reference(cell.get('r')))
        merges = self.root.find(tag('mergeCells'))
        patterns = []
        for merge in list(merges):
            ref = merge.get('ref')
            numbers = [int(n) for n in re.findall(r'\d+', ref)]
            if all(first <= n <= last for n in numbers):
                if numbers[0] == first:
                    patterns.append(re.findall(r'[A-Z]+', ref))
                merges.remove(merge)
            else:
                merge.set('ref', shift_reference(ref))
        hyperlinks = self.root.find(tag('hyperlinks'))
        for link in list(hyperlinks):
            n = int(re.search(r'\d+', link.get('ref')).group())
            if first <= n <= last:
                hyperlinks.remove(link)
            else:
                link.set('ref', shift_reference(link.get('ref')))
        sheet_data = self.root.find(tag('sheetData'))
        index = list(sheet_data).index(old_rows[0])
        for old in old_rows:
            sheet_data.remove(old)
        for offset, row in enumerate(new_rows):
            number = first + offset
            row.set('r', str(number))
            for cell in row:
                cell.set('r', re.match('[A-Z]+', cell.get('r')).group() + str(number))
            sheet_data.insert(index + offset, row)
            for left, right in patterns:
                ET.SubElement(merges, tag('mergeCell'), ref=f'{left}{number}:{right}{number}')
            if links[offset]:
                rid = 'rId' + str(max([int(re.sub(r'\D', '', r.get('Id')) or '0') for r in self.relationships] + [0]) + 1)
                ET.SubElement(self.relationships, '{' + P + '}Relationship', Id=rid, Type=R + '/hyperlink', Target=links[offset], TargetMode='External')
                ET.SubElement(hyperlinks, tag('hyperlink'), ref='A' + str(number), attrib={'{' + R + '}id': rid})
        merges.set('count', str(len(merges)))
        self.root.find(tag('dimension')).set('ref', f'A1:F{max(int(r.get("r")) for r in self.rows())}')

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', help='GitHub pull-request URL')
    parser.add_argument('--directory', default=str(pathlib.Path.cwd()), help='OpenCode session working directory; never the skill directory')
    parser.add_argument('--workbook', help='Explicit workbook path; otherwise reuse a local tracker or PR-Review-Tracker.xlsx')
    parser.add_argument('--name', action='append', default=[], metavar='LOGIN=FULL NAME', help='User-confirmed display name; may be repeated')
    parser.add_argument('--tab-name', help='User-approved Excel-safe replacement when the exact branch-based name is invalid')
    args = parser.parse_args(argv)
    owner, repo, number = parse_url(args.pr)
    url = f'https://github.com/{owner}/{repo}/pull/{number}'
    workbook = select_workbook(args.directory, args.workbook)
    check_closed(workbook)
    book = Workbook(workbook)  # Read the saved workbook before changing anything.
    cache_root = pathlib.Path(os.environ.get('XDG_CACHE_HOME', str(pathlib.Path.home() / '.cache')))
    raw = cache_root / 'opencode' / 'track-pr' / hashlib.sha256(str(workbook).encode()).hexdigest()[:16] / f'{owner}-{repo}-{number}'
    raw.mkdir(parents=True, exist_ok=True, mode=0o700)
    def save(name, data):
        (raw / (name + '.json')).write_text(json.dumps(data, indent=2) + '\n')
        return data
    def gh(*arguments):
        return json.loads(subprocess.check_output(['gh', *arguments], text=True, timeout=120))
    base = f'repos/{owner}/{repo}'
    def pages(endpoint):
        text = subprocess.check_output(['gh', 'api', '--paginate', f'{base}/{endpoint}?per_page=100'], text=True, timeout=120).lstrip()
        result = []
        while text:
            page, offset = json.JSONDecoder().raw_decode(text)
            result.extend(page)
            text = text[offset:].lstrip()
        return result
    pr = save('pull', gh('api', base + f'/pulls/{number}'))
    url = pr['html_url'].rstrip('/')
    desired_name = args.tab_name or f'{pr["head"]["ref"]}-#{number}'
    if not desired_name or len(desired_name) > 31 or re.search(r'[\[\]:*?/\\]', desired_name) or desired_name.startswith("'") or desired_name.endswith("'"):
        raise ValueError(f'Excel cannot use this exact tab name: {desired_name!r}. Ask for an abbreviated, Excel-safe name and pass --tab-name.')
    reviews = sorted(save('reviews', pages(f'pulls/{number}/reviews')), key=lambda r: r.get('submitted_at') or '9999')
    reviews = [r for r in reviews if r.get('submitted_at')]
    comments = save('comments', pages(f'pulls/{number}/comments'))
    timeline = save('timeline', pages(f'issues/{number}/timeline'))
    query = '''query($owner:String!,$repo:String!,$number:Int!,$cursor:String) {
      repository(owner:$owner,name:$repo) { pullRequest(number:$number) {
        reviewThreads(first:100,after:$cursor) {pageInfo{hasNextPage endCursor}
          nodes{id isResolved comments(first:100){pageInfo{hasNextPage endCursor} nodes{databaseId}}}
        }
      }} }'''
    threads, cursor = [], None
    while True:
        call = ['api', 'graphql', '-f', 'query=' + query, '-f', 'owner=' + owner, '-f', 'repo=' + repo, '-F', 'number=' + str(number)]
        if cursor:
            call += ['-f', 'cursor=' + cursor]
        result = gh(*call)
        if result.get('errors'):
            raise RuntimeError(result['errors'])
        connection = result['data']['repository']['pullRequest']['reviewThreads']
        threads.extend(connection['nodes'])
        if not connection['pageInfo']['hasNextPage']:
            break
        cursor = connection['pageInfo']['endCursor']
    comments_query = '''query($id:ID!,$cursor:String!) {
      node(id:$id) { ... on PullRequestReviewThread {
        comments(first:100,after:$cursor) {pageInfo{hasNextPage endCursor} nodes{databaseId}}
      }} }'''
    for thread in threads:
        connection = thread['comments']
        while connection['pageInfo']['hasNextPage']:
            result = gh('api', 'graphql', '-f', 'query=' + comments_query, '-f', 'id=' + thread['id'], '-f', 'cursor=' + connection['pageInfo']['endCursor'])
            if result.get('errors'):
                raise RuntimeError(result['errors'])
            following = result['data']['node']['comments']
            connection['nodes'].extend(following['nodes'])
            connection['pageInfo'] = following['pageInfo']
    save('threads', threads)
    published_ids = {r['id'] for r in reviews}
    comments = [c for c in comments if c['pull_request_review_id'] in published_ids]
    thread_by_comment = {c['databaseId']: t for t in threads for c in t['comments']['nodes']}
    assert {c['id'] for c in comments} <= set(thread_by_comment), 'Snapshot changed; retry refresh.'
    author = who(pr['user'])
    external = [r for r in reviews if who(r['user']) != author]
    humans = [r for r in external if (r.get('user') or {}).get('type') != 'Bot']
    people = list(dict.fromkeys(who(r['user']) for r in humans))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        profiles = dict(pool.map(lambda name: (name, gh('api', 'users/' + name)), dict.fromkeys(n for n in [author, *people] if n != '[deleted]')))
    save('profiles', profiles)
    overrides = KNOWN_NAMES.copy()
    for entry in args.name:
        login, separator, full_name = entry.partition('=')
        if not separator or not login.strip() or not full_name.strip():
            raise ValueError('Use --name "LOGIN=Full Name".')
        overrides[login.strip()] = full_name.strip()
    missing = [login for login, profile in profiles.items() if login not in overrides and (not profile.get('name') or profile['name'].casefold() == login.casefold())]
    if missing:
        raise ValueError('Full names needed; ask the user or verify public profile/commit names, then pass --name "LOGIN=Full Name": ' + ', '.join(missing))
    def display(name):
        return 'Unavailable' if name == '[deleted]' else (overrides.get(name) or profiles[name]['name']).strip().title()
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    end = pr.get('merged_at') or pr.get('closed_at') or now
    save('snapshot', {'retrieved_at': now, 'timezone': 'IST', 'working_time': 'Mon-Fri 10:00-19:00, partial-day office-window time multiplied by 8/9'})
    copilot = [r for r in external if who(r['user']) == 'Copilot']
    approvals = [r for r in external if r['state'] == 'APPROVED']
    requests = sorted([e for e in timeline if e['event'] == 'review_requested'], key=lambda e: e['created_at'])
    pushes = sorted([e for e in timeline if e['event'] == 'head_ref_force_pushed' and who(e.get('actor')) == author], key=lambda e: e['created_at'])
    review_by_id = {r['id']: r for r in reviews}
    def matching_pushes(feedback):
        """Prefer the push before my reply; estimate from the next push otherwise."""
        found = {}
        for comment in feedback:
            submitted = review_by_id[comment['pull_request_review_id']]['submitted_at']
            thread_id = thread_by_comment[comment['id']]['id']
            replies = [c for c in comments if who(c['user']) == author and thread_by_comment[c['id']]['id'] == thread_id and c['created_at'] >= submitted]
            reply = max(replies, key=lambda c: c['created_at']) if replies else None
            push = next((p for p in reversed(pushes) if reply and submitted < p['created_at'] <= reply['created_at']), None)
            estimated = push is None
            if push is None:
                push = next((p for p in pushes if p['created_at'] > submitted), None)
            if push:
                found[push['created_at']] = found.get(push['created_at'], False) or estimated
        return sorted(found), {timestamp for timestamp, estimated in found.items() if estimated}
    def push_values(matched, estimated, submitted, has_feedback=True):
        if not has_feedback:
            return 'Not needed', 'Not needed'
        if not matched:
            return 'Unavailable', 'Unavailable'
        dates = '\n\n'.join(when(timestamp) + ('\nEstimated' if timestamp in estimated else '') for timestamp in matched)
        elapsed = duration(submitted, matched[-1]) + ('\nEstimated' if estimated else '')
        return dates, elapsed
    def resolution(feedback):
        if not feedback:
            return 'No comments', False
        resolved = sum(thread_by_comment[c['id']]['isResolved'] for c in feedback)
        if resolved == len(feedback):
            return 'Yes\nAll comments resolved', True
        return ('Partly' if resolved else 'No') + f'\n{resolved} of {len(feedback)} comments resolved', False

    target = None
    for index, sheet, path in book.records():
        root = ET.fromstring(book.parts[path])
        values = [book.text(c) for c in root.iter(tag('c'))]
        if (book.is_new or url.casefold() in [value.rstrip('/').casefold() for value in values]) and any('COPILOT REVIEWS' in value for value in values):
            target = index, sheet, path, root
            break
    new_tab = target is None
    if new_tab:
        with zipfile.ZipFile(TEMPLATE) as source:
            root = ET.fromstring(source.read('xl/worksheets/sheet1.xml'))
            relationships = ET.fromstring(source.read('xl/worksheets/_rels/sheet1.xml.rels'))
            style_map = book.import_template_styles(ET.fromstring(source.read('xl/styles.xml')))
        for cell in root.iter(tag('c')):
            cell.set('s', str(style_map[int(cell.get('s', '0'))]))
        sheet_id = max(int(s.get('sheetId')) for s in book.book.find(tag('sheets'))) + 1
        part_id = sheet_id
        while f'xl/worksheets/sheet{part_id}.xml' in book.parts:
            part_id += 1
        path = f'xl/worksheets/sheet{part_id}.xml'
        rid = 'rId' + str(max(int(re.sub(r'\D', '', r.get('Id')) or '0') for r in book.rels) + 1)
        sheet = ET.SubElement(book.book.find(tag('sheets')), tag('sheet'), name='New PR', sheetId=str(sheet_id), attrib={'{' + R + '}id': rid})
        ET.SubElement(book.rels, '{' + P + '}Relationship', Id=rid, Type=R + '/worksheet', Target='worksheets/' + posixpath.basename(path))
        ET.SubElement(book.types, '{' + C + '}Override', PartName='/' + path, ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
        index = len(book.book.find(tag('sheets'))) - 1
    else:
        index, sheet, path, root = target
        relationships = ET.fromstring(book.parts[posixpath.dirname(path) + '/_rels/' + posixpath.basename(path) + '.rels'])
    tab = Tab(book, root, relationships)
    styles = {col: tab.style(tab.body('COPILOT REVIEWS')[0], col) for col in 'ABCDEF'}
    normal = styles['B']
    def fill_style(colour, default):
        fills = book.styles.find(tag('fills'))
        for index, xf in enumerate(book.styles.find(tag('cellXfs'))):
            colour_node = fills[int(xf.get('fillId', '0'))].find('.//' + tag('fgColor'))
            if colour_node is not None and colour_node.get('rgb') == 'FF' + colour:
                return str(index)
        return default
    green = fill_style('E6F4EA', tab.style(tab.body('HUMAN REVIEWS')[0], 'D'))
    amber = fill_style('FFF2D7', styles['E'])
    def new_row(sample, values, height=100):
        row = copy.deepcopy(sample)
        row.set('ht', str(height))
        for col in 'ABCDEF':
            tab.put(row, col, '')
        for col, value, style in values:
            tab.put(row, col, value, style)
        return row

    # Work bottom-up: edit only each table's data rows, preserving surrounding layout.
    wait_sample = tab.body('STILL WAITING')[0] if any('STILL WAITING' in tab.row_text(r) for r in tab.rows()) else tab.body('WAITING FOR REVIEW')[0]
    wait_word = 'STILL WAITING' if any('STILL WAITING' in tab.row_text(r) for r in tab.rows()) else 'WAITING FOR REVIEW'
    waiting = []
    active_requests = {who(user) for user in pr.get('requested_reviewers', [])}
    for person in people:
        request = next((r for r in reversed(requests) if who(r['requested_reviewer']) == person), None)
        if request and ('requested_reviewers' not in pr or person in active_requests) and not any(who(r['user']) == person and r['submitted_at'] >= request['created_at'] for r in external):
            waiting.append(new_row(wait_sample, [('A', display(person), styles['A']), ('C', when(request['created_at']), normal), ('E', duration(request['created_at'], end), amber)], 38))
    if not waiting:
        waiting = [new_row(wait_sample, [('A', 'No pending reviews', normal)], 38)]
    tab.replace_body(wait_word, waiting, [None] * len(waiting))
    tab.put(tab.section(wait_word), 'A', '04   WAITING FOR REVIEW')
    header = tab.header('WAITING FOR REVIEW')
    for col, value in [('A', 'REVIEWER'), ('C', 'REVIEW REQUESTED'), ('E', 'TIME WAITING FOR REVIEW')]:
        tab.put(header, col, value)

    human_sample = tab.body('HUMAN REVIEWS')[0]
    human_rows, human_links, audit = [], [], {}
    for person in people:
        rr = [r for r in humans if who(r['user']) == person]
        cc = [c for c in comments if who(c['user']) == person]
        first = min((review_by_id[c['pull_request_review_id']]['submitted_at'] for c in cc), default=None)
        matched, estimated = matching_pushes(cc)
        push_dates, push_time = push_values(matched, estimated, first, bool(cc))
        state, fully = resolution(cc)
        dates = '\n'.join(dict.fromkeys(when(review_by_id[c['pull_request_review_id']]['submitted_at']) for c in cc)) if cc else 'Approved:\n' + when(rr[-1]['submitted_at']) if rr[-1]['state'] == 'APPROVED' else when(rr[-1]['submitted_at'])
        human_rows.append(new_row(human_sample, [('A', display(person), styles['A']), ('B', dates, normal), ('C', str(len(cc)), styles['C']), ('D', state, green if fully else amber if cc else normal), ('E', push_dates, styles['E'] if cc else normal), ('F', push_time, styles['F'] if cc else normal)], max(100, 35 + 28 * len(rr))))
        human_links.append(rr[-1]['html_url'])
        audit[person] = {'matching_pushes': matched, 'estimated_matches': sorted(estimated), 'feedback_submitted': first, 'turnaround': push_time}
    if not human_rows:
        human_rows = [new_row(human_sample, [('A', 'No human reviews yet', normal)], 70)]
        human_links = [None]
    tab.replace_body('HUMAN REVIEWS', human_rows, human_links)
    tab.put(tab.section('HUMAN REVIEWS'), 'A', f'03   HUMAN REVIEWS   |   {len(people)} reviewers  •  {sum(who(c["user"]) in people for c in comments)} comments  •  {len(approvals)} approval' + ('s' if len(approvals) != 1 else ''))

    cp_sample = tab.body('COPILOT REVIEWS')[0]
    cp_rows, cp_links = [], []
    for count, review in enumerate(copilot, 1):
        cc = [c for c in comments if c['pull_request_review_id'] == review['id']]
        request = next((r for r in reversed(requests) if who(r['requested_reviewer']) == 'Copilot' and r['created_at'] <= review['submitted_at']), None)
        matched, estimated = matching_pushes(cc)
        push_dates, push_time = push_values(matched, estimated, review['submitted_at'], bool(cc))
        state, fully = resolution(cc)
        dates = ('Requested:\n' + when(request['created_at']) + '\n\n' if request else '') + 'Comments received:\n' + when(review['submitted_at'])
        cp_rows.append(new_row(cp_sample, [('A', f'Review {count} · Copilot', styles['A']), ('B', dates, normal), ('C', str(len(cc)), styles['C']), ('D', state, green if fully else amber), ('E', push_dates, styles['E'] if cc else normal), ('F', push_time, styles['F'] if cc else normal)], 110))
        cp_links.append(review['html_url'])
    if not cp_rows:
        cp_rows, cp_links = [new_row(cp_sample, [('A', 'No Copilot reviews yet', normal)], 70)], [None]
    tab.replace_body('COPILOT REVIEWS', cp_rows, cp_links)
    tab.put(tab.section('COPILOT REVIEWS'), 'A', f'02   COPILOT REVIEWS   |   {len(copilot)} reviews  •  {sum(who(c["user"]) == "Copilot" for c in comments)} comments')
    for section in ['COPILOT REVIEWS', 'HUMAN REVIEWS']:
        header = tab.header(section)
        for col, text in zip('ABCDEF', ['REVIEWER' if section == 'HUMAN REVIEWS' else 'REVIEW', 'REVIEW DATES', 'COMMENTS', 'COMMENTS RESOLVED?', 'MY CHANGE PUSH', 'MY TIME TO PUSH CHANGES']):
            tab.put(header, col, text)

    # Refresh the existing summary cells; do not recreate this worksheet.
    first_row, second_row = tab.rows()[:2]
    tab.put(first_row, 'A', f'PR #{number}  |  REVIEW TRACKER')
    tab.put(second_row, 'A', 'Updated: ' + when(now))
    link_row = next(r for r in tab.rows() if any(book.text(c) == 'PR LINK' for c in r))
    title_row = next(r for r in tab.rows() if any(book.text(c) == 'PR TITLE' for c in r))
    tab.put(link_row, 'C', url)
    tab.put(title_row, 'C', pr['title'])
    for link in root.find(tag('hyperlinks')):
        if link.get('ref') == 'C' + link_row.get('r'):
            for rel in relationships:
                if rel.get('Id') == link.get('{' + R + '}id'):
                    rel.set('Target', url)
    ready = next((e['created_at'] for e in timeline if e['event'] == 'ready_for_review'), None)
    opened = sum(not t['isResolved'] for t in threads)
    for label, value in [('AUTHOR', display(author)), ('PR CREATED', when(pr['created_at'])), ('READY FOR HUMAN REVIEW', when(ready)), ('SOURCE BRANCH', pr['head']['ref']), ('TARGET BRANCH', pr['base']['ref']), ('CURRENT STATUS', pr['state'].title() + f'  •  {opened} unresolved comment' + ('s' if opened != 1 else '')), ('PR AGE — CALENDAR TIME', duration(pr['created_at'], end)), ('PR AGE — WORKING HOURS', f'{working_hours(pr["created_at"], end):.2f} hours'), ('APPROVALS RECEIVED', '\n\n'.join(display(who(a['user'])) + '\n' + when(a['submitted_at']) for a in approvals) or 'Unavailable')]:
        tab.set_label_value(label, value)
    assert not any(s is not sheet and s.get('name').casefold() == desired_name.casefold() for s in book.book.find(tag('sheets')))
    sheet.set('name', desired_name)
    defined = book.book.find(tag('definedNames'))
    if defined is None:
        defined = ET.Element(tag('definedNames'))
        calc = book.book.find(tag('calcPr'))
        book.book.insert(list(book.book).index(calc) if calc is not None else len(book.book), defined)
    escaped_name = desired_name.replace("'", "''")
    for name, value in [('_xlnm.Print_Area', f"'{escaped_name}'!$A$1:$F${max(int(r.get('r')) for r in tab.rows())}"), ('_xlnm.Print_Titles', f"'{escaped_name}'!$1:$2")]:
        node = next((d for d in defined if d.get('name') == name and d.get('localSheetId') == str(index)), None)
        if node is None:
            node = ET.SubElement(defined, tag('definedName'), name=name, localSheetId=str(index))
        node.text = value
    brk = root.find(tag('rowBreaks'))
    if brk is not None and len(brk):
        brk[0].set('id', str(int(tab.section('HUMAN REVIEWS').get('r')) - 1))
    footer = root.find(tag('headerFooter'))
    if footer is not None and footer.find(tag('oddFooter')) is not None:
        footer.find(tag('oddFooter')).text = f'&LPR #{number}&RPage &P of &N'
    rel_path = posixpath.dirname(path) + '/_rels/' + posixpath.basename(path) + '.rels'
    views = book.book.find(tag('bookViews'))
    if views is not None and len(views):
        views[0].set('activeTab', str(index))
    book.parts[path], book.parts[rel_path] = xml(root), xml(relationships)
    book.parts['xl/workbook.xml'] = xml(book.book)
    allowed = {path, rel_path, 'xl/workbook.xml'}
    if new_tab:
        book.parts['xl/_rels/workbook.xml.rels'], book.parts['[Content_Types].xml'] = xml(book.rels), xml(book.types)
        allowed |= {'xl/_rels/workbook.xml.rels', '[Content_Types].xml'}
        if book.parts['xl/styles.xml'] != book.original.get('xl/styles.xml'):
            allowed.add('xl/styles.xml')
    # Enforce plain missing values, bold and alone; no explanatory filler.
    for cell in root.iter(tag('c')):
        value = book.text(cell)
        if value == 'Unavailable':
            assert all(r.find(tag('rPr')).find(tag('b')).get('val') == '1' for r in cell.iter(tag('r')))
    changed = book.write(allowed)
    save('update_audit', {'workbook': str(workbook), 'tab': desired_name, 'matching_rule': 'Last recorded author push before the latest author reply; when no such match exists, first recorded author force-push after review, labelled Estimated', 'reviews': audit, 'changed_zip_parts': sorted(changed), 'updated_at': now})
    print('Created:' if book.is_new else 'Updated IN PLACE:', workbook)
    print('Tab:', desired_name)
    print('Snapshot IST:', when(now))
    print('Other workbook parts preserved:', len(book.original) - len(changed))
    print('GitHub access: read-only. Output folder contains no helper scripts, source dumps, or report copies.')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, AssertionError, subprocess.SubprocessError) as error:
        print('Track PR: ' + str(error), file=sys.stderr)
        sys.exit(1)
