import glob,yaml,re,json
KEEP=set("""Ohm's Hooke's Snell's Boyle's Charles's Dalton's Graham's Coulomb's Newton's Kepler's Archimedes' Fourier's Hardy Weinberg Beer Lambert Henderson Hasselbalch Nernst Arrhenius Gibbs Darcy Weisbach Pitot Venturi Reynolds Doppler Wheatstone Pythagorean Riegel Cooper Friedewald Cockcroft Gault Lincoln Petersen Poisson Sukanya Samriddhi Yojana Kisan Vikas Patra India Indian US UK Celsius Fahrenheit Kelvin Baker's SUVAT Navy Post Office Senior Citizens Savings Scheme National Pension System Public Provident Fund Employees' Monthly Income Recurring Deposit Fixed Rule Ten-Pin RCF Tm IV QTc eGFR LDL BMI BMR VO₂ MET Y-Δ Star-Delta THD UPS VFD PCB IPC-2221 ADC SNR PWM LED LC RC RLC DC AC CO₂ EV NPS NSC KVP SCSS POMIS PPF EPF SIP SWP EMI GST HRA FD RD CAGR ROI ROAS CLV DTI FOIR P/E CPM CPC CTR CPA ERA OBP NRR FG% eFG% TS% DPI PPI GSM LPG C:N""".split())
def sent(core):
    out=[]
    for w in core.split(' '):
        parts=re.split(r'([–\-/])',w); np=[]
        for p in parts:
            if p in KEEP or not p or not p[0].isupper() or (len(p)>1 and any(ch.isupper() for ch in p[1:])) or p.isupper(): np.append(p)
            else: np.append(p[0].lower()+p[1:])
        out.append(''.join(np))
    return ' '.join(out)
KIND=r'(Calculator|Converter|Estimator|Solver|Scaler|Predictor)'
n=dict(h=0,intro=0,desc=0)
for f in sorted(glob.glob('src/content/calculators/*/*.mdx')):
    s=open(f).read(); fmtext,body=s[4:].split('\n---',1); fm=yaml.safe_load(fmtext)
    t=re.sub(r'\s*\([^)]*\)','',fm['title']).strip()
    t=t.split(' — ')[-1]
    m=list(re.finditer(KIND,t))
    if not m: continue
    kind=m[-1].group(1).lower(); core=t[:m[-1].start()].strip(' –-&,')
    if not core: continue
    sc=sent(core); kw=f'{sc} {kind}'
    # headings
    b0=body
    body=re.sub(r'^## How to use this (calculator|converter)\s*$',f'## How to use the {kw}',body,flags=re.M)
    body=re.sub(r'^## (The )?[Ff]ormulas?\s*$',lambda m_: f'## {sc[0].upper()+sc[1:]} formula'+('s' if m_.group(0).rstrip().endswith('s') else ''),body,flags=re.M,count=1)
    if body!=b0: n['h']+=1
    intro=fm.get('intro','')
    lines=fmtext.split('\n')
    if intro and core.lower() not in intro.lower() and sc.lower() not in intro.lower():
        add=f' This free {kw} solves for whichever value you leave blank and shows the formula and steps.' if kind=='calculator' else f' This free {kw} converts instantly in both directions and includes a quick reference table.'
        if kind not in ('calculator','converter'): add=f' This free {kw} shows the formula and steps.'
        intro2=intro+add
        lines=[('intro: '+json.dumps(intro2,ensure_ascii=False)) if l.startswith('intro:') else l for l in lines]; n['intro']+=1
    d=fm['description']
    if len(d)<110 and sc.lower() not in d.lower():
        tail=f' Free online {kw} with formula and examples.'
        if len(d)+len(tail)<=160:
            nd=d+tail
            lines=[('description: '+json.dumps(nd,ensure_ascii=False)) if l.startswith('description:') else l for l in lines]; n['desc']+=1
    fmtext='\n'.join(lines)
    open(f,'w').write('---\n'+fmtext+'\n---'+body)
print(n)
