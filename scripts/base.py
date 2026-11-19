import os
import csv,re,json,statistics as S,collections,datetime as dt
R=list(csv.DictReader(open('posts_raw2.csv',encoding='utf-8')))+list(csv.DictReader(open('posts_extra_clean.csv',encoding='utf-8')))
RENAME={'Monitor AOC 25G64 (FHD 25")':'Monitor TCL 25G64 (FHD 25" Mini LED)'}
DROP={'Ryzen 3 2200G','Ryzen 5 2600X','RTX 3070','RTX 3050','RTX 3060','RTX 3060 Ti','RTX 2060 Super','RTX 4050','RX 5500 XT','RX 5600 XT','RX 5600','RX 5700','RX 6600','Ryzen 7 5700G'}
COMBO=re.compile(r'\+\s*(processador|placa|water|mem|ssd|cooler|fonte)|\bkit\b.*\+',re.I)
MULTI=re.compile(r'(\d{3})\s?gb\s+(\d{3}\s?gb|1\s?tb|2\s?tb)|1\s?tb\s+2\s?tb|2\s?tb\s+4\s?tb|\b(\d{1,2})\s?gb\s*(?:/|e|,)?\s*(\d{1,2})\s?gb\b',re.I)
SODIMM=re.compile(r'impact ddr|hyperx impact|notebook|so-?dimm',re.I)
def cat(k):
    for p,c in [('Ryzen','Processadores'),('Fan ','Coolers'),('Intel','Processadores'),('GTX','Placas de vídeo'),('Arc ','Placas de vídeo'),('RTX','Placas de vídeo'),('RX ','Placas de vídeo'),('Placa-mãe','Placas-mãe'),('Memória','Memória RAM'),('SSD','SSD'),('Fonte','Fontes'),('Gabinete','Gabinetes'),('Water','Coolers'),('Air','Coolers'),('Monitor','Monitores'),('Cadeira','Cadeiras'),('Mousepad','Setup e acessórios'),('Mouse','Mouses'),('Teclado','Teclados'),('Headset','Headsets e fones'),('Fone','Headsets e fones'),('Controle','Controles'),('Notebook','Notebooks'),('PlayStation','Consoles'),('Nintendo','Consoles'),('Smart TV','TVs'),('Celular','Celulares, tablets e relógios'),('Tablet','Celulares, tablets e relógios'),('Smartwatch','Celulares, tablets e relógios'),('Microfone','Setup e acessórios'),('Mousepad','Setup e acessórios')]:
        if k.startswith(p): return c
import sys as _s0;_s0.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import atributos as AT
import novos as _NV
# ---- anúncio com várias capacidades no título (ex.: "1TB 512GB" do AliExpress) ----
# o preço decide qual capacidade é: compara com a mediana dos posts de capacidade única
import math as _m
def _caps(k,t):
    tl=t.lower()
    if k.startswith('SSD'):
        c={('500GB' if g in ('500','512') else g+'GB') for g in re.findall(r'(?<![\dx])(\d{3})\s?gb',tl) if g in ('120','128','240','250','256','480','500','512','960')}
        c|={g+'TB' for g in re.findall(r'(?<![\d.,])([124])\s?tb\b',tl)}
        return c
    if k.startswith('Memória'):
        tl=re.sub(r'\d\s?x\s?\d{1,2}\s?gb','',tl)
        return {g+'GB' for g in re.findall(r'(?<![\dx])(8|16|32|64)\s?gb\b',tl)}
    return set()
def _swap(k,c):
    if k.startswith('SSD'): return re.sub(r'\b(\d{3}GB|\dTB)\b',c,k,count=1)
    return re.sub(r'\b(8|16|32|64)GB\b',c,k,count=1)
_ref=collections.defaultdict(list)
for r in R:
    if r['data']>=os.environ.get('D0','2026-10-01') and len(_caps(r['produto'],r['titulo']))==1: _ref[r['produto']].append(float(r['preco']))
_ref={k:S.median(v) for k,v in _ref.items() if len(v)>=3}
_byid=collections.defaultdict(list)
for r in R: _byid[r['post_id']].append(r)
_capdec={}
def _decide(pid):
    # para cada capacidade do título: preço / mediana (do modelo exato; se não tiver, do grupo da capacidade)
    if pid in _capdec: return _capdec[pid]
    L=[r for r in _byid[pid] if len(_caps(r['produto'],r['titulo']))>=2]
    best=None
    if L:
        cs=_caps(L[0]['produto'],L[0]['titulo']);p=float(L[0]['preco']);rat={}
        for c in cs:
            for r in sorted(L,key=lambda x:'mais bar' in x['produto']):
                k2=_swap(r['produto'],c)
                if k2 in _ref: rat[c]=p/_ref[k2];break
        if len(rat)==len(cs):      # só decide se conhece o preço de todas as capacidades
            sc=sorted((abs(_m.log(v)),c) for c,v in rat.items())
            if 0.55<=rat[sc[0][1]]<=1.3 and sc[1][0]-sc[0][0]>=0.15: best=sc[0][1]
    _capdec[pid]=best;return best
rows=[];dropped=collections.Counter()
for r in R:
    _cs=_caps(r['produto'],r['titulo'])
    if len(_cs)>=2:
        _c=_decide(r['post_id'])
        if not _c: dropped['multi']+=1; continue
        r=dict(r,produto=_swap(r['produto'],_c))
        _t=r['titulo']
        for _o in _cs-{_c}:
            _pat={'500GB':r'(500|512)\s?gb'}.get(_o, _o[:-2]+r'\s?'+_o[-2:])
            _t=re.sub(r'(?i)(?<![\d.,x])'+_pat+r'\b',' ',_t)
        if _c=='500GB': _t=re.sub(r'(?i)(?<![\d.,x])512\s?gb\b','500GB',_t)
        r['titulo']=_t

    k=RENAME.get(r['produto'],r['produto'])
    if k in DROP: continue
    t=r['titulo']
    if 'oled' in t.lower() and k in ('Monitor QHD 27" 144Hz+ (mais barato)','Monitor Ultrawide 34" QHD (mais barato)','Monitor 4K (mais barato)','Monitor Full HD 27" 144Hz+ (mais barato)'):
        if k.startswith('Monitor QHD 27'): k='Monitor OLED QHD 27" (mais barato)'
        else: continue
    if COMBO.search(t): dropped['combo']+=1; continue
    if (k.startswith('SSD') or k.startswith('Memória')) and MULTI.search(t) and len(_caps(k,t))<2: dropped['multi']+=1; continue
    if k.startswith('Memória') and SODIMM.search(t): dropped['sodimm']+=1; continue
    if r['data']<os.environ.get('D0','2026-10-01'): continue
    k=AT.refina(k,t)
    _g=_NV.gstorm(t.lower())
    if _g: k=_g[1]   # G-Storm: sempre o nome certo do produto (G-Storm, GStorm ou G Storm)
    if k.endswith('outras configs'): continue
    rows.append(dict(id=int(r['post_id']),d=r['data'],k=k,p=float(r['preco']),s=r['loja'],t=t,c=cat(k)))
import sys as _s;_s.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import atributos as AT
_mods=set()
_cat=set(json.load(open('../dados/catalogo.json'))['itens']) if os.path.exists('../dados/catalogo.json') else set()
# os produtos do catálogo automático não entram nessa checagem de duplicado (senão escondem modelos da lista)
_nomes=[re.sub(r'[^a-z0-9]','',k.lower()) for k in {r['k'] for r in rows} if 'mais bar' not in k and k not in _cat]
def _dup(m):
    cod=re.sub(r'[^a-z0-9]','',m.split(' ',2)[-1].split(' ')[0].lower()) if ' ' in m else ''
    _bm={re.sub(r'[^a-z0-9]','',v.lower()) for v in AT.MARCA.values()}|{'cooler','water','placa','mae','monitor','fonte','memoria','ssd','gaming','plus','pro'}
    toks=[t_ for t_ in (re.sub(r'[^a-z0-9]','',w.lower()) for w in m.split()[1:]) if t_ not in _bm and not re.fullmatch(r'\d+(gb|tb|w|mhz)?|ddr\d|[abx]\d{3}m?',t_)]
    pre=re.sub(r'[^a-z0-9]','',m.split()[0].lower())
    mesmos=[n for n in _nomes if n.startswith(pre)]
    for tk in toks:
        if len(tk)>=4 and any(tk[:L] in n for n in mesmos for L in range(len(tk),5,-1) if re.search(r'\d',tk[:L]) and re.search(r'[a-z]',tk[:L])): return True
        if len(tk)>=4 and any(tk in n for n in mesmos): return True
        for al in re.findall(r'[a-z]{5,}',tk):
            if any(al in n for n in mesmos): return True
    return False
for r in list(rows):
    _m=AT.modelo(r['k'],r['t'])
    if _m and _m!=r['k'] and not _dup(_m):
        rows.append(dict(r,k=_m,c=cat(_m)));_mods.add(_m)
rows=[r for r in rows if 'mais bar' not in r['k'] and r['k']!='Teclado magnético']
by=collections.defaultdict(list)
for r in rows: by[r['k']].append(r)
outl=[];clean=[]
for k,l in by.items():
    m=S.median(x['p'] for x in l)
    for x in l:
        if x['p']<0.55*m or (k in _mods and x['p']>1.8*m): outl.append((k,x,m))
        else: clean.append(x)
# daily min
daily=collections.defaultdict(dict)
for x in clean:
    dd=daily[x['k']]; c=dd.get(x['d'])
    if c is None: dd[x['d']]=dict(x,n=1)
    else:
        c['n']+=1
        if x['p']<c['p']: dd[x['d']].update({kk:x[kk] for kk in ('p','s','id','t')})
keep={k:v for k,v in daily.items() if len(v)>=6 or 'G-Storm' in k}   # G-Storm (parceiro): todos os produtos, mesmo com poucos dias
import os
_last=max(d for v in daily.values() for d in v)
_D0=dt.date.fromisoformat(os.environ.get('D0','2026-10-01'));MA=os.environ.get('MA','2026-10-01');MB=os.environ.get('MB','2026-11-01')
DAYS=[(_D0+dt.timedelta(i)).isoformat() for i in range((dt.date.fromisoformat(_last)-_D0).days+1)]
summ=[]
for k,v in keep.items():
    oct_=[v[d]['p'] for d in v if MA<=d<MB]; nov=[v[d]['p'] for d in v if d>=MB]
    lo=min(v.values(),key=lambda x:(x['p'],x['d'])); hi=max(v.values(),key=lambda x:(x['p'],x['d']))
    last=v[max(v)]
    summ.append(dict(produto=k,categoria=cat(k),dias_com_oferta=len(v),posts=sum(x['n'] for x in v.values()),
        mediana_out=round(S.median(oct_),2) if oct_ else None,mediana_nov=round(S.median(nov),2) if nov else None,
        var_out_nov=round((S.median(nov)/S.median(oct_)-1)*100,1) if oct_ and nov else None,
        attrs=AT.attrs(cat(k),k,[x['t'] for x in by[k]]),menor=lo['p'],menor_data=lo['d'],menor_loja=lo['s'],maior=hi['p'],maior_data=hi['d'],ultimo=last['p'],ultimo_data=last['d'],ultimo_loja=last['s']))
CO=['Placas de vídeo','Processadores','Placas-mãe','Memória RAM','SSD','Fontes','Gabinetes','Coolers','Monitores','Mouses','Teclados','Headsets e fones','Controles','Setup e acessórios','Cadeiras','Notebooks','Consoles','TVs','Celulares, tablets e relógios']
summ.sort(key=lambda s:(CO.index(s['categoria']),s['produto']))
OUT=os.environ.get('OUT','/mnt/user-data/outputs/base_precos_grape_tec')
import os; os.makedirs(OUT,exist_ok=True)
with open(f'{OUT}/menor_preco_por_dia.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['data','categoria','produto','menor_preco','loja','posts_no_dia','titulo_da_oferta','link_post'])
    for s_ in summ:
        k=s_['produto']
        for d in sorted(keep[k]): x=keep[k][d]; w.writerow([d,cat(k),k,str(x['p']).replace('.',','),x['s'],x['n'],x['t'],f"https://t.me/grape_tec/{x['id']}"])
with open(f'{OUT}/resumo_produtos.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(list(summ[0].keys()))
    for s_ in summ: w.writerow([str(v).replace('.',',') if isinstance(v,float) else v for v in s_.values()])
with open(f'{OUT}/todos_os_posts_classificados.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['data','categoria','produto','preco','loja','titulo','link_post','fora_da_curva'])
    ol={(k,x['id']) for k,x,m in outl}
    for x in sorted(rows,key=lambda x:(x['d'],x['id'])):
        if x['k'] not in keep: continue
        w.writerow([x['d'],x['c'],x['k'],str(x['p']).replace('.',','),x['s'],x['t'],f"https://t.me/grape_tec/{x['id']}",'sim' if (x['k'],x['id']) in ol else ''])
json.dump({'periodo':[DAYS[0],DAYS[-1]],'fonte':'t.me/grape_tec','produtos':[dict(s_,serie=[{'data':d,'preco':keep[s_['produto']][d]['p'],'loja':keep[s_['produto']][d]['s'],'post':keep[s_['produto']][d]['id']} for d in sorted(keep[s_['produto']])]) for s_ in summ]},open(f'{OUT}/base_precos.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump(summ,open('summ.json','w'),ensure_ascii=False); json.dump({k:{d:[v[d]['p'],v[d]['s']] for d in v} for k,v in keep.items()},open('keep.json','w'),ensure_ascii=False)
print(len(rows),'posts válidos',dropped,'| produtos:',len(summ),'| fora da curva:',len(outl))
for k,x,m in sorted(outl,key=lambda o:o[1]['d']):
    if not k.startswith('SSD NVMe 500'): print('  OUTLIER',x['d'],k,x['p'],x['s'],'(mediana',m,')',x['t'][:50])
for s_ in summ: print(f"{s_['categoria'][:10]:10} {s_['produto'][:44]:44} dias={s_['dias_com_oferta']:2} out={s_['mediana_out']} nov={s_['mediana_nov']} var={s_['var_out_nov']} min={s_['menor']} {s_['menor_data'][5:]} ult={s_['ultimo']}")
