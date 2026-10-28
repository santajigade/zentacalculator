import yaml, glob, sys, os
bad=0
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/src/content/calculators/*/*.mdx')):
    s=open(f).read(); fm=s.split('---')[1]
    try:
        d=yaml.safe_load(fm)
        ids=[v['id'] for v in d['variables']]
        for v in d['variables']:
            assert isinstance(v.get('label'),str), ('label',v)
        if len(set(ids))!=len(ids): raise Exception('dup ids')
    except Exception as e:
        bad+=1; print(f.split('calculators/')[1], '->', str(e).split('\n')[0][:150])
print('bad', bad)
# strict key check
VK={'id','label','family','unit','imperialUnit','default','min','max','prefix','suffix','help','decimals','options','bands'}
bad2=0
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/src/content/calculators/*/*.mdx')):
    d=yaml.safe_load(open(f).read().split('---')[1])
    for v in d['variables']:
        ex=set(v)-VK
        if ex: bad2+=1; print('KEYS', f.split('calculators/')[1], v.get('id'), ex)
        for o in v.get('options') or []:
            if set(o)!={'label','value'}: bad2+=1; print('OPT', f.split('calculators/')[1], o)
        for b in v.get('bands') or []:
            if set(b)!={'max','label','color'}: bad2+=1; print('BAND', f.split('calculators/')[1], b)
    for q in d.get('faq',[]):
        if set(q)!={'q','a'} or not isinstance(q['a'],str): bad2+=1; print('FAQ', f.split('calculators/')[1], q)
print('bad2', bad2)
