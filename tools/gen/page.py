import os, textwrap
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src','content','calculators')
def page(cat, slug, fm, body):
    d=os.path.join(BASE,cat); os.makedirs(d,exist_ok=True)
    fm=textwrap.dedent(fm).strip('\n')
    import re
    out=[]
    for line in fm.split('\n'):
        m=re.match(r'^(\s*(?:- )?(?:q|a|title|description): )(.*)$', line)
        if m and (': ' in m.group(2) or ' #' in m.group(2)) and not m.group(2).startswith(('"',"'")):
            line=m.group(1)+'"'+m.group(2).replace('\\','\\\\').replace('"','\\"')+'"'
        out.append(line)
    fm='\n'.join(out)
    body=textwrap.dedent(body).strip('\n')
    from fixflow import fix_text
    open(os.path.join(d,slug+'.mdx'),'w').write(fix_text(f"---\n{fm}\n---\n\n{body}\n"))
def n(x, d=4):
    """pretty number"""
    if x==0: return '0'
    if abs(x)>=1000: return f'{x:,.{max(0,d-4)}f}' if abs(x)>=1e4 else f'{x:,.{max(0,d-3)}f}'
    return f'{float(f"{x:.{d}g}"):g}'
