import os as _os;OUT=_os.environ.get('OUT','/mnt/user-data/outputs/base_precos_grape_tec')
IMG={};URL={}
import re as _re
def _link(t):
    i=t.lower().find('link do produto')
    for s in ([t[i:]] if i>=0 else [])+[t]:
        for u in _re.findall(r'https?://[^\s<>"]+',s):
            u=u.rstrip('.,);')
            h=_re.sub(r'^https?://','',u).split('/')[0].lower()
            if any(x in h for x in ('t.me','telegram','youtube','youtu.be','grapetec','kpages','gvgmall')): continue
            if h.startswith('lista.') or u.rstrip('/').count('/')<3: continue
            return u
    return ''
if _os.environ.get('POSTS'):
    import json as _j
    import glob as _g
    for _f in _g.glob(_os.path.join(_os.environ['POSTS'],'*.json')):
        for m in _j.load(open(_f))['messages']:
            if m.get('photo'): IMG[str(m['id'])]=m['photo']
            u=_link(m.get('text',''))
            if u: URL[str(m['id'])]=u
import csv,json,statistics as S,collections,re
# usa a base limpa (sem fora da curva) + cupons/hora
allp=list(csv.DictReader(open(OUT+'/todos_os_posts_classificados.csv',encoding='utf-8-sig'),delimiter=';'))
_NOFERTAS={}
for r in allp: _NOFERTAS[r['data']]=_NOFERTAS.get(r['data'],0)+1
# placas-mãe por modelo (marca + chipset + linha), além do grupo "mais barata"
_BR={'asus':'ASUS','gigabyte':'Gigabyte','msi':'MSI','asrock':'ASRock','biostar':'Biostar','mancer':'Mancer','husky':'Husky','maxsun':'Maxsun','pcware':'PCWare','afox':'Afox','bluecase':'Bluecase','duex':'Duex'}
_SER=[('rog strix','ROG Strix'),('strix','ROG Strix'),('tuf','TUF Gaming'),('prime','Prime'),('aorus elite','Aorus Elite'),('aorus','Aorus'),('gaming x','Gaming X'),('ds3h','DS3H'),('tomahawk','Tomahawk'),('mortar','Mortar'),('gaming plus','Gaming Plus'),('steel legend','Steel Legend'),('phantom','Phantom Gaming'),('pg lightning','PG Lightning'),('lightning','PG Lightning'),('hdv','HDV'),('eagle','Eagle'),('ultra durable','Ultra Durable'),('nexus','Nexus'),('challenger','Challenger'),('terminator','Terminator'),('force','Force'),('ayw','AYW'),('pro','PRO')]
def mobo(t):
    t=t.lower()
    b=re.search(r'\b(%s)\b'%'|'.join(_BR),t); ch=re.search(r'\b([abxz]\d{3}e?)(m)?\b|\b([abxz]\d{3}e?)m[-\s]',t)
    if not b or not ch: return None
    c=(ch.group(1) or ch.group(3)).upper(); m='M' if (ch.group(2) or ch.group(3) or re.search(c.lower()+r'm',t)) else ''
    s=next((n for k,n in _SER if k in t),'')
    if not s: return None
    extra=' Plus' if s=='TUF Gaming' and re.search(r'\bplus\b',t) else ''
    return f"Placa-mãe {_BR[b.group(1)]} {s} {c}{m}{extra}"
_virt=[]
for r in allp:
    if r['produto'].startswith('Placa-mãe') and r['fora_da_curva']!='sim':
        mk=mobo(r['titulo'])
        if mk: _virt.append(dict(r,produto=mk,_mod=1))
daily=collections.defaultdict(dict)
for r in csv.DictReader(open(OUT+'/menor_preco_por_dia.csv',encoding='utf-8-sig'),delimiter=';'):
    daily[r['produto']][r['data']]=float(r['menor_preco'].replace(',','.'))
_vd=collections.defaultdict(lambda:collections.defaultdict(list))
for r in _virt: _vd[r['produto']][r['data']].append(float(r['preco'].replace(',','.')))
for k,v in _vd.items():
    allv=[p for ps in v.values() for p in ps]; md=S.median(allv)
    for dd,ps in v.items():
        ok=[p for p in ps if p>=0.55*md]
        if ok: daily[k][dd]=min(ok)
for r in _virt:
    if float(r['preco'].replace(',','.'))<0.55*S.median([p for ps in _vd[r['produto']].values() for p in ps]): r['fora_da_curva']='sim'
allp=allp+_virt
cup={r['post_id']:r for r in csv.DictReader(open('cupons.csv',encoding='utf-8'))}
esg={}
MARCAS={}
if _os.environ.get('MARCAS') and _os.path.exists(_os.environ['MARCAS']):
    import json as _j2;MARCAS=_j2.load(open(_os.environ['MARCAS']))
for r in csv.DictReader(open('esgotados.csv',encoding='utf-8')): esg.setdefault(r['cupom'],r['datahora'])
def slug(s):
    import unicodedata; return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def build(day):
    best={};avail={}
    for r in allp:
        if r['data']!=day: continue
        k=r['produto']; prev=[p for d,p in daily[k].items() if d<day]
        if len(prev)<5: continue
        price=float(r['preco'].replace(',','.')); med=S.median(prev); lo=min(prev)
        if r['fora_da_curva']=='sim': continue
        drop=(1-price/med)*100
        if drop<5: continue
        pid=r['link_post'].rsplit('/',1)[1]; c=cup.get(pid,{})
        it=dict(k=k,id=slug(k.replace(' (mais barata)','').replace(' (mais barato)','')),n=k.replace(' (mais barata)','').replace(' (mais barato)',''),t=r['titulo'][:70],bucket=k.endswith(')') and 'mais bar' in k,
                p=price,med=round(med,2),lo=lo,drop=round(drop,1),rec=price<lo,loja=r['loja'],h=c.get('hora',''),cup=c.get('cupom',''),post=int(pid),cat=r['categoria'])
        if pid in IMG: it['img']=IMG[pid]
        if pid in URL: it['url']=URL[pid]
        if it['cup'] and it['cup'] in esg and esg[it['cup']][:10]==day and esg[it['cup']][11:16]>=it['h']: it['esg']=esg[it['cup']][11:16]
        mk=MARCAS.get(str(pid),{})
        if not it.get('esg') and mk.get('esg') and day==mk.get('d',day): it['esg']=mk['esg'];it['esgsrc']=mk['src']
        elif not it.get('esg') and mk.get('av'): it['av']=1
        if k not in best or it['drop']>best[k]['drop']: best[k]=it
        if not it.get('esg') and (k not in avail or it['drop']>avail[k]['drop']): avail[k]=it
    L=list(best.values())
    for k,a in avail.items():
        if best[k].get('esg'): L.append(dict(a,alt=1))
    # mesmo post no grupo "mais barata" e no modelo: fica o do modelo
    mp={x['post'] for x in L if x['k'] in _vd}
    L=[x for x in L if x['k'] in _vd or x['post'] not in mp]
    L=sorted(L,key=lambda x:(-x['rec'],-x['drop']))
    n=_NOFERTAS.get(day,0)
    return dict(items=L[:90],total=len(best),ofertas=n)
D={'2026-11-10':build('2026-11-10'),'2026-11-11':build('2026-11-11')}
json.dump(D,open('dias.json','w'),ensure_ascii=False)
for d,v in D.items():
    print(d,'ofertas',v['ofertas'],'achados',v['total'])
    for x in v['items'][:12]: print(f"  {x['drop']:5.1f}% {'REC' if x['rec'] else '   '} {x['n'][:34]:34} {x['p']} (med {x['med']}) {x['loja']} {x['h']} {x['cup']} {x.get('esg','')}")
