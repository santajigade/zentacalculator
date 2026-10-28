import os
F = {
 'length': {'m':1,'mm':1e-3,'cm':1e-2,'km':1e3,'in':0.0254,'ft':0.3048,'yd':0.9144,'mi':1609.344,'nmi':1852,'um':1e-6},
 'area': {'m2':1,'cm2':1e-4,'mm2':1e-6,'km2':1e6,'ha':1e4,'in2':0.00064516,'ft2':0.09290304,'yd2':0.83612736,'acre':4046.8564224},
 'volume': {'m3':1,'L':1e-3,'mL':1e-6,'cm3':1e-6,'in3':1.6387064e-5,'ft3':0.028316846592,'galUS':0.003785411784,'galUK':0.00454609},
 'velocity': {'ms':1,'kmh':1/3.6,'fts':0.3048,'mph':0.44704,'kn':1852/3600},
 'pressure': {'Pa':1,'kPa':1e3,'bar':1e5,'mbar':100,'psi':6894.757293168,'atm':101325,'mmHg':133.322387415,'mH2O':9806.65,'inH2O':249.08891,'MPa':1e6},
 'energy': {'J':1,'kJ':1e3,'MJ':1e6,'Wh':3600,'kWh':3.6e6,'cal':4.184,'kcal':4184,'BTU':1055.05585,'therm':105505585},
 'power': {'W':1,'kW':1e3,'MW':1e6,'hp':745.69987158,'PS':735.49875,'BTUh':0.29307107,'TR':3516.8528},
 'flow': {'m3s':1,'m3h':1/3600,'Lmin':1e-3/60,'Ls':1e-3,'gpm':0.003785411784/60,'cfm':0.028316846592/60},
 'torque': {'Nm':1,'kNm':1e3,'lbft':1.3558179483314,'lbin':0.1129848290276,'kgfm':9.80665},
}
LAB = {'m':'m','mm':'mm','cm':'cm','km':'km','in':'in','ft':'ft','yd':'yd','mi':'mi','nmi':'nmi','m2':'m²','ft2':'ft²','acre':'acre','ha':'ha','yd2':'yd²','km2':'km²','in2':'in²','cm2':'cm²','L':'L','mL':'mL','galUS':'US gal','galUK':'UK gal','ft3':'ft³','m3':'m³','in3':'in³','kmh':'km/h','mph':'mph','ms':'m/s','fts':'ft/s','kn':'knots','bar':'bar','psi':'psi','kPa':'kPa','MPa':'MPa','atm':'atm','mmHg':'mmHg','mbar':'mbar','inH2O':'inH₂O','mH2O':'mH₂O','J':'J','kJ':'kJ','kWh':'kWh','kcal':'kcal','BTU':'BTU','Wh':'Wh','cal':'cal','therm':'therm','MJ':'MJ','W':'W','kW':'kW','hp':'hp','PS':'PS','BTUh':'BTU/h','TR':'TR','m3h':'m³/h','Lmin':'L/min','gpm':'US gpm','cfm':'CFM','Ls':'L/s','Nm':'N·m','lbft':'lbf·ft','lbin':'lbf·in','kgfm':'kgf·m'}

def fmt(x):
    if x==0: return '0'
    a=abs(x)
    if a>=1e6 or a<1e-4: return f'{x:.4g}'
    s=f'{x:,.6g}' if a>=1000 else f'{x:.6g}'
    return s

def conv(fam,v,a,b): return v*F[fam][a]/F[fam][b]

def make(c, outdir):
    fam=c['family']; units=c['units']
    vars_=[]
    for i,(u,label) in enumerate(units):
        d = f", default: {c['default']}" if i==0 else ''
        mn = ", min: 0" if c.get('nonneg',True) else ''
        vars_.append(f"  - {{ id: u{i}, label: {label}, family: {fam}, unit: {u}{d}{mn} }}")
    eqs=[f"  - u{i} = u{i+1}" for i in range(len(units)-1)]
    fq="\n".join(f"  - q: {q}\n    a: \"{a}\"" for q,a in c['faq'])
    rel=", ".join(c['related'])
    a,b=c['table']['pair']
    rows="\n".join(f"| {fmt(v)} {LAB[a]} | {fmt(conv(fam,v,a,b))} {LAB[b]} |" for v in c['table']['values'])
    tbl=f"| {c['table']['h'][0]} | {c['table']['h'][1]} |\n|---|---|\n{rows}"
    if 'table2' in c:
        a2,b2=c['table2']['pair']
        rows2="\n".join(f"| {fmt(v)} {LAB[a2]} | {fmt(conv(fam,v,a2,b2))} {LAB[b2]} |" for v in c['table2']['values'])
        tbl+=f"\n\n| {c['table2']['h'][0]} | {c['table2']['h'][1]} |\n|---|---|\n{rows2}"
    kw=", ".join(c['keywords'])
    feat="featured: true\n" if c.get('featured') else ''
    md=f"""---
title: {c['title']}
description: {c['desc']}
category: conversion
keywords: [{kw}]
updated: 2026-10-27
{feat}variables:
{chr(10).join(vars_)}
equations:
{chr(10).join(eqs)}
faq:
{fq}
related: [{rel}]
---

## How to use this converter

{c['how']}

## Formula

<p class="formula">{c['formula']}</p>

{c.get('example','')}

## Conversion table

{tbl}

{c['extra']}
"""
    open(os.path.join(outdir,c['slug']+'.mdx'),'w').write(md)
