import os as _os;OUT=_os.environ.get('OUT','/mnt/user-data/outputs/base_precos_grape_tec')
IMG={};URL={};CURL={}
import json as _jf
FOTOS=_jf.load(open(_os.environ['FOTOS'])) if _os.environ.get('FOTOS') and _os.path.exists(_os.environ['FOTOS']) else {}
def _resg(t):
    tl=t.lower();i=tl.find('resgat')
    if i<0: i=tl.find('pegue o cupom')
    if i<0: return ''
    j=tl.find('link do produto',i)
    for u in _re.findall(r'https?://[^\s<>"]+',t[i:j if j>i else i+400]):
        if 't.me' not in u: return u.rstrip('.,);')
    return ''
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
            cu=_resg(m.get('text',''))
            if cu: CURL[str(m['id'])]=cu
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
import sys as _sys;_sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
import modelos as _M
_virt=[]
for r in ([] if _os.environ.get('MODELOS_NA_BASE','1')=='1' else allp):
    if r['fora_da_curva']=='sim': continue
    if r['produto'].startswith('Placa-mãe'):
        mk=mobo(r['titulo'])
    else:
        _c=_M.chave(r['produto'],r['titulo']); mk=_c[0] if _c else None
    if mk: _virt.append(dict(r,produto=mk,_mod=1))
daily=collections.defaultdict(dict)
for r in csv.DictReader(open(OUT+'/menor_preco_por_dia.csv',encoding='utf-8-sig'),delimiter=';'):
    daily[r['produto']][r['data']]=float(r['menor_preco'].replace(',','.'))
_vd=collections.defaultdict(lambda:collections.defaultdict(list))
for r in _virt: _vd[r['produto']][r['data']].append(float(r['preco'].replace(',','.')))
for k,v in _vd.items():
    allv=[p for ps in v.values() for p in ps]; md=S.median(allv)
    for dd,ps in v.items():
        ok=[p for p in ps if 0.55*md<=p<=1.8*md]
        if ok: daily[k][dd]=min(ok)
for r in _virt:
    _md=S.median([p for ps in _vd[r['produto']].values() for p in ps]);_pp=float(r['preco'].replace(',','.'))
    if _pp<0.55*_md or _pp>1.8*_md: r['fora_da_curva']='sim'
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
        if FOTOS.get(pid,[''])[0]: it['img']=FOTOS[pid][0]
        if pid in URL: it['url']=URL[pid]
        if pid in CURL and CURL[pid]!=it.get('url'): it['cupurl']=CURL[pid]
        if it['cup'] and it['cup'] in esg and esg[it['cup']][:10]==day and esg[it['cup']][11:16]>=it['h']: it['esg']=esg[it['cup']][11:16]
        mk=MARCAS.get(str(pid),{})
        if not it.get('esg') and mk.get('esg') and day==mk.get('d',day): it['esg']=mk['esg'];it['esgsrc']=mk['src']
        elif not it.get('esg') and mk.get('av'): it['av']=1
        if k not in best or it['drop']>best[k]['drop']: best[k]=it
        if not it.get('esg') and (k not in avail or it['drop']>avail[k]['drop']): avail[k]=it
    L=list(best.values())
    for k,a in avail.items():
        if best[k].get('esg'): L.append(dict(a,alt=1))
    # mesmo post em mais de um lugar: fica o mais específico (modelo > produto > grupo "mais barato")
    def _pri(x): return 0 if x['k'] in _vd else (2 if 'mais bar' in x['k'] else 1)
    _bp={}
    for x in L:
        if x['post'] not in _bp or _pri(x)<_pri(_bp[x['post']]): _bp[x['post']]=x
    L=[x for x in L if _bp[x['post']] is x]
    for x in L:
        if x['k'] in _vd: x['bucket']=True
    L=sorted(L,key=lambda x:(-x['drop'],-x['rec']))
    n=_NOFERTAS.get(day,0)
    return dict(items=L[:90],total=len(best),ofertas=n)
import datetime as _dtt
_hoje=(_dtt.datetime.utcnow()-_dtt.timedelta(hours=3)).date()
D={(_hoje-_dtt.timedelta(days=1)).isoformat():build((_hoje-_dtt.timedelta(days=1)).isoformat()),_hoje.isoformat():build(_hoje.isoformat())}
json.dump(D,open('dias.json','w'),ensure_ascii=False)
# série diária dos modelos que aparecem nos Achados (pra ter "Ver curva")
_usados={x['k'] for v in D.values() for x in v['items'] if x['k'] in _vd}
_ser={}
for r in _virt:
    k=r['produto']
    if k not in _usados or r['fora_da_curva']=='sim': continue
    p=float(r['preco'].replace(',','.'))
    _m=S.median([q for ps in _vd[k].values() for q in ps])
    if p<0.55*_m or p>1.8*_m: continue
    cur=_ser.setdefault(k,{'c':r['categoria'],'d':{}})['d'].get(r['data'])
    if cur is None or p<cur[0]: _ser[k]['d'][r['data']]=(p,r['loja'],int(r['link_post'].rsplit('/',1)[1]))
_ser={k:dict(c=v['c'],id=slug(k),d=v['d']) for k,v in _ser.items()}
json.dump(_ser,open('modelos_series.json','w'),ensure_ascii=False)
for d,v in D.items():
    print(d,'ofertas',v['ofertas'],'achados',v['total'])
    for x in v['items'][:12]: print(f"  {x['drop']:5.1f}% {'REC' if x['rec'] else '   '} {x['n'][:34]:34} {x['p']} (med {x['med']}) {x['loja']} {x['h']} {x['cup']} {x.get('esg','')}")
