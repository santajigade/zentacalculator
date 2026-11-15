"""In-place editor for existing calculator pages (used by improve/expand scripts).

edit(cid, intro=..., body_add=..., faq_add=[(q, a)], date='YYYY-MM-DD', ...)
- Never touches slug, category, variables, equations or related (asserted).
- Writes YAML strings with json.dumps, so "\\n\\n" paragraph breaks survive.
- Uses plain string operations (no re.sub replacement strings).
- Refuses en/em dashes in any text it writes.
"""
import os, re, json
import yaml

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators')
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')
DONE = []


def _q(s):
    return json.dumps(s, ensure_ascii=False)


def _nodash(*texts):
    for t in texts:
        if t and DASH.search(t):
            raise AssertionError('dash in new text: ' + DASH.split(t)[0][-60:])


def words(s):
    return len(re.findall(r'\S+', s))


def body_words(cid):
    s = open(os.path.join(BASE, cid + '.mdx')).read()
    return words(s.split('---', 2)[2])


def edit(cid, *, date, intro=None, phrase=None, body_add='', before=None, replace=(), faq_add=(),
         faq_replace=(), title=None, description=None, keywords=None, min_words=520):
    path = os.path.join(BASE, cid + '.mdx')
    s = open(path).read()
    assert s.startswith('---\n')
    _, fm, body = s.split('---', 2)
    old = yaml.safe_load(fm)
    assert not old.get('featured'), cid
    lines = fm.strip('\n').split('\n')

    def set_key(key, value_text):
        for i, l in enumerate(lines):
            if l.startswith(key + ':'):
                lines[i] = key + ': ' + value_text
                return
        raise KeyError(key)

    if intro is not None:
        _nodash(intro)
        paras = intro.split('\n\n')
        assert len(paras) == 2 and all(p.strip() == p and p for p in paras), (cid, 'intro must be 2 paragraphs')
        n = words(intro)
        assert 60 <= n <= 90, (cid, 'intro words', n)
        ph = (phrase or '').lower()
        assert ph and ph in paras[0].lower(), (cid, 'intro phrase missing', phrase)
        set_key('intro', _q(intro))
    if title is not None:
        _nodash(title); set_key('title', _q(title))
    if description is not None:
        _nodash(description)
        assert 120 <= len(description) <= 160, (cid, len(description))
        set_key('description', _q(description))
    if keywords is not None:
        _nodash(*keywords); set_key('keywords', '[' + ', '.join(keywords) + ']')
    set_key('updated', date)

    # FAQ edits
    for qold, qnew, anew in faq_replace:
        _nodash(qnew, anew)
        for i, l in enumerate(lines):
            if re.match(r'^\s*- q: ', l) and qold in l:
                lines[i] = '  - q: ' + _q(qnew)
                assert re.match(r'^\s+a: ', lines[i + 1]), (cid, 'faq a line')
                lines[i + 1] = '    a: ' + _q(anew)
                break
        else:
            raise AssertionError((cid, 'faq not found', qold))
    if faq_add:
        fi = next(i for i, l in enumerate(lines) if l.startswith('faq:'))
        j = fi + 1
        while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('-')):
            j += 1
        new = []
        for q, a in faq_add:
            _nodash(q, a)
            new += ['  - q: ' + _q(q), '    a: ' + _q(a)]
        lines[j:j] = new
    fm2 = '\n' + '\n'.join(lines) + '\n'
    new = yaml.safe_load(fm2)
    for k in ('category', 'variables', 'equations', 'related', 'published'):
        assert new.get(k) == old.get(k), (cid, 'changed', k)
    if faq_add:
        qs = [f['q'].lower() for f in new['faq']]
        assert len(set(qs)) == len(qs), (cid, 'duplicate faq')

    # body edits
    for a, b in replace:
        _nodash(b)
        assert body.count(a) == 1, (cid, 'replace target count', a[:60], body.count(a))
        body = body.replace(a, b)
    if body_add:
        _nodash(body_add)
        add = '\n' + body_add.strip('\n') + '\n'
        if before:
            k = body.index(before)
            body = body[:k] + add.lstrip('\n') + '\n' + body[k:]
        else:
            body = body.rstrip('\n') + '\n' + add
    out = '---' + fm2 + '---' + body
    if not out.endswith('\n'):
        out += '\n'
    n = words(body)
    assert n >= min_words, (cid, 'body words', n)
    open(path, 'w').write(out)
    DONE.append(cid)
    return n


def drop_backlog(cids):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'upgrade-backlog.txt')
    ls = open(p).read().split('\n')
    keep = [l for l in ls if l.strip() not in set(cids)]
    open(p, 'w').write('\n'.join(keep))
    return len(ls) - len(keep)
