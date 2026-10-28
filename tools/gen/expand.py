"""Append extra sections and FAQs to an existing calculator page without touching the calculator itself."""
import re, textwrap, sys
sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from fixflow import fix_text
BASE = '/home/claude/zentacalculator/src/content/calculators'

def q(s):
    s = s.strip()
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def expand(cid, body='', faq=(), before='## Keep in mind', updated='2026-10-27'):
    path = f'{BASE}/{cid}.mdx'
    src = open(path).read()
    _, fm, content = src.split('---', 2)
    # FAQs: insert at the end of the faq list (before the next top-level key)
    if faq:
        add = ''.join(f'  - q: {q(a)}\n    a: {q(b)}\n' for a, b in faq)
        m = re.search(r'^faq:\n((?:  .*\n|    .*\n)*)', fm, re.M)
        if m:
            fm = fm[:m.end()] + add + fm[m.end():]
        else:
            fm = fm.rstrip('\n') + '\nfaq:\n' + add
    fm = re.sub(r'^updated: .*$', f'updated: {updated}', fm, flags=re.M)
    body = textwrap.dedent(body).strip('\n')
    if body:
        if before and before in content:
            i = content.index(before)
            content = content[:i] + body + '\n\n' + content[i:]
        else:
            content = content.rstrip('\n') + '\n\n' + body + '\n'
    open(path, 'w').write(fix_text('---' + fm + '---' + content))

def words(cid):
    return len(open(f'{BASE}/{cid}.mdx').read().split())
