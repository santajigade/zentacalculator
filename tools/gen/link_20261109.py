"""Point internal links at 'Discovered, currently not indexed' pages from already-indexed pages in the same category."""
import re, os, glob, sys, openpyxl, collections
B = 'src/content/calculators'
SP = '/tmp/claude-0/-home-claude/750aedf4-cfe2-50ab-b4b3-33d984656d68/scratchpad/indexed.txt'
idx = {u.split('zentacalculator.com/')[1].strip('/') for u in open(SP).read().split()}
wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
disc = [r[0].split('zentacalculator.com/')[1].strip('/') for r in list(wb['Table'].iter_rows(values_only=True))[1:]]
def meta(cid):
    s = open(f'{B}/{cid}.mdx').read()
    t = re.search(r'^title: (.*)$', s, re.M).group(1); k = re.search(r'^keywords: \[(.*)\]$', s, re.M)
    words = set(re.findall(r'[a-z0-9]+', (t + ' ' + (k.group(1) if k else '')).lower())) - {'calculator','to','and','the','of','a','for','in','converter'}
    rel = re.search(r'^related: \[(.*)\]$', s, re.M)
    return s, words, [x.strip() for x in rel.group(1).split(',') if x.strip()] if rel else None
allc = {p[len(B)+1:-4] for p in glob.glob(f'{B}/*/*.mdx')}
src = [c for c in allc if c in idx]
used = collections.Counter(); plan = collections.defaultdict(list); miss = []
for d in disc:
    if d not in allc: miss.append(d); continue
    _, dw, _ = meta(d); cat = d.split('/')[0]
    cands = []
    for c in src:
        s, w, rel = meta(c)
        if rel is None or d in rel or c == d: continue
        score = len(dw & w) * 3 + (5 if c.split('/')[0] == cat else 0)
        if score < 5: continue
        cands.append((-score, used[c], c))
    cands.sort()
    for _, _, c in [x for x in cands if used[x[2]] < 3][:2]:
        plan[c].append(d); used[c] += 1
for c, ds in plan.items():
    p = f'{B}/{c}.mdx'; s = open(p).read()
    rel = re.search(r'^related: \[(.*)\]$', s, re.M)
    cur = [x.strip() for x in rel.group(1).split(',') if x.strip()]
    s = s[:rel.start()] + 'related: [' + ', '.join(ds + cur) + ']' + s[rel.end():]
    open(p, 'w').write(s)
linked = collections.Counter(d for ds in plan.values() for d in ds)
print('sources edited', len(plan), 'targets linked', len(linked), 'missing', miss, 'unlinked', [d for d in disc if d in allc and d not in linked])
