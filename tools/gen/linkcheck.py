import re,glob,os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/dist'
bad=set()
for f in glob.glob(D+'/**/index.html',recursive=True):
    for u in re.findall(r'href="(/[^"#?]*)"',open(f).read()):
        p=D+u+('index.html' if u.endswith('/') else '')
        if not os.path.exists(p) and not os.path.exists(D+u): bad.add((u,f.replace(D,'')))
print(len(bad)); [print(b) for b in sorted(bad)[:30]]
