import os as _os;OUT=_os.environ.get('OUT','/mnt/user-data/outputs/base_precos_grape_tec')
IMG={}
if _os.environ.get('POSTS'):
    import json as _j
    IMG={str(m['id']):m['photo'] for m in _j.load(open(_os.environ['POSTS']))['messages'] if m.get('photo')}
import csv,json,statistics as S,collections,re
# usa a base limpa (sem fora da curva) + cupons/hora
allp=list(csv.DictReader(open(OUT+'/todos_os_posts_classificados.csv',encoding='utf-8-sig'),delimiter=';'))
daily=collections.defaultdict(dict)
for r in csv.DictReader(open(OUT+'/menor_preco_por_dia.csv',encoding='utf-8-sig'),delimiter=';'):
    daily[r['produto']][r['data']]=float(r['menor_preco'].replace(',','.'))
cup={r['post_id']:r for r in csv.DictReader(open('cupons.csv',encoding='utf-8'))}
esg={}
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
        if it['cup'] and it['cup'] in esg and esg[it['cup']][:10]==day and esg[it['cup']][11:16]>=it['h']: it['esg']=esg[it['cup']][11:16]
        if k not in best or it['drop']>best[k]['drop']: best[k]=it
        if not it.get('esg') and (k not in avail or it['drop']>avail[k]['drop']): avail[k]=it
    L=list(best.values())
    for k,a in avail.items():
        if best[k].get('esg'): L.append(dict(a,alt=1))
    L=sorted(L,key=lambda x:(-x['rec'],-x['drop']))
    n=sum(1 for r in allp if r['data']==day)
    return dict(items=L[:90],total=len(best),ofertas=n)
D={'2026-11-10':build('2026-11-10'),'2026-11-11':build('2026-11-11')}
json.dump(D,open('dias.json','w'),ensure_ascii=False)
for d,v in D.items():
    print(d,'ofertas',v['ofertas'],'achados',v['total'])
    for x in v['items'][:12]: print(f"  {x['drop']:5.1f}% {'REC' if x['rec'] else '   '} {x['n'][:34]:34} {x['p']} (med {x['med']}) {x['loja']} {x['h']} {x['cup']} {x.get('esg','')}")
