import re, glob
KEYS=['id','label','family','unit','imperialUnit','default','min','max','prefix','suffix','help','decimals','value','color']
NEXT=re.compile(r',\s*(?:' + '|'.join(KEYS) + r'):\s|\s*\}\s*$')
def fix_line(line):
    if '{' not in line: return line
    for key in ('label','help','suffix'):
        m=re.search(r'(\{|,)\s*'+key+r': ', line)
        if not m: continue
        start=m.end()
        if line[start] in '"\'': continue
        n=NEXT.search(line, start)
        if not n: continue
        val=line[start:n.start()]
        if any(ch in val for ch in ',:[]#{}') or val.strip()!=val:
            q='"'+val.replace('\\','\\\\').replace('"','\\"')+'"'
            line=line[:start]+q+line[n.start():]
    return line
def fix_text(s):
    head,sep,rest=s.partition('\n---\n') if not s.startswith('---\n') else ('',None,None)
    parts=s.split('---',2)
    fm='\n'.join(fix_line(l) for l in parts[1].split('\n'))
    return '---'+fm+'---'+parts[2]
if __name__=='__main__':
    n=0
    for f in glob.glob('/home/claude/zentacalculator/src/content/calculators/*/*.mdx'):
        s=open(f).read(); t=fix_text(s)
        if t!=s: open(f,'w').write(t); n+=1
    print('fixed files', n)
