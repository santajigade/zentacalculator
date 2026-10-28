import glob,re,math,collections,yaml
S='/tmp/claude-0/-home-claude/750aedf4-cfe2-50ab-b4b3-33d984656d68/scratchpad'
slugs=open(S+'/ib_slugs.txt').read().split()
stop=set('the and of in to for a an vs how what is are with explained working principle types guide calculator calculation formula your by on its'.split())
tok=lambda s:[w for w in re.split(r'[^a-z0-9]+',s.lower()) if w and w not in stop]
df=collections.Counter(w for s in slugs for w in set(tok(s)))
N=len(slugs)
for f in sorted(glob.glob('src/content/calculators/*/*.mdx')):
  cid=f.split('calculators/')[1][:-4]
  if cid.split('/')[0] not in ('engineering','physics','chemistry','conversion','math','statistics'): continue
  fm=yaml.safe_load(open(f).read().split('---')[1])
  q=set(tok(cid.split('/')[1]))|set(tok(fm['title']))
  sc=[]
  for s in slugs:
    t=set(tok(s)); sh=q&t
    if not sh: continue
    v=sum(math.log(N/df[w]) for w in sh)/ (1+0.05*len(t))
    sc.append((v,s))
  sc.sort(reverse=True)
  if sc and sc[0][0]>4: print(cid,'|',' ; '.join(f'{s}({v:.1f})' for v,s in sc[:4]))
