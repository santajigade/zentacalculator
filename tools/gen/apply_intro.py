import sys, re, glob, json, yaml
G='' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''; sys.path.insert(0,G)
from intro1 import I as A; from intro2 import I as B; from intro3 import I as C
I={**A,**B,**C}
IB='https://www.instrumentationblog.in/'
base='src/content/calculators/'
files=sorted(glob.glob(base+'*/*.mdx'))
missing=[f for f in files if f[len(base):-4] not in I]
print('missing',missing)
def joinand(xs): return xs[0] if len(xs)==1 else ', '.join(xs[:-1])+' and '+xs[-1]
for f in files:
    cid=f[len(base):-4]
    if cid not in I: continue
    s=open(f).read()
    fmtext,body=s[4:].split('\n---',1)
    fm=yaml.safe_load(fmtext)
    intro=re.sub(r'\]\(ib:([a-z0-9-]+)\)',lambda m:f']({IB}{m.group(1)}/)',I[cid])
    used=set(re.findall(r'instrumentationblog\.in/([a-z0-9-]+)/',intro))
    left=[l for l in fm.get('links',[]) if l['url'].rstrip('/').split('/')[-1] not in used]
    # drop links block & old intro
    lines=fmtext.split('\n'); out=[]; skip=False
    for ln in lines:
        if ln.startswith('links:') or ln.startswith('intro:'): skip=True; continue
        if skip and ln.startswith('  '): continue
        skip=False; out.append(ln)
    out.insert(3, 'intro: '+json.dumps(intro, ensure_ascii=False))
    fmtext='\n'.join(out)
    if left:
        sent='For more background, read '+joinand([f"[{l['title']}]({l['url']})" for l in left])+'.'
        m=list(re.finditer(r'\n## ',body))
        pos=m[1].start() if len(m)>1 else len(body)
        body=body[:pos].rstrip('\n')+'\n\n'+sent+'\n'+body[pos:]
    open(f,'w').write('---\n'+fmtext+'\n---'+body)
print('done')
