import csv,re,json,statistics as S,collections,datetime as dt
R=list(csv.DictReader(open('posts_raw2.csv',encoding='utf-8')))+list(csv.DictReader(open('posts_extra_clean.csv',encoding='utf-8')))
RENAME={'Monitor AOC 25G64 (FHD 25")':'Monitor TCL 25G64 (FHD 25" Mini LED)'}
DROP={'Ryzen 3 2200G','Ryzen 5 2600X','RTX 3070','RTX 3050','RTX 3060','RTX 3060 Ti','RTX 2060 Super','RTX 4050','RX 5500 XT','RX 5600 XT','RX 5600','RX 5700','RX 6600','Ryzen 7 5700G'}
COMBO=re.compile(r'\+\s*(processador|placa|water|mem|ssd|cooler|fonte)|\bkit\b.*\+',re.I)
MULTI=re.compile(r'(\d{3})\s?gb\s+(\d{3}\s?gb|1\s?tb|2\s?tb)|1\s?tb\s+2\s?tb|2\s?tb\s+4\s?tb|\b(\d{1,2})\s?gb\s+(\d{1,2})\s?gb\b',re.I)
SODIMM=re.compile(r'impact ddr|hyperx impact|notebook|so-?dimm',re.I)
def cat(k):
    for p,c in [('Ryzen','Processadores'),('RTX','Placas de vídeo'),('RX ','Placas de vídeo'),('Placa-mãe','Placas-mãe'),('Memória','Memória RAM'),('SSD','SSD'),('Fonte','Fontes'),('Gabinete','Gabinetes'),('Water','Coolers'),('Air','Coolers'),('Monitor','Monitores'),('Mousepad','Setup e acessórios'),('Mouse','Mouses'),('Teclado','Teclados'),('Headset','Headsets e fones'),('Fone','Headsets e fones'),('Controle','Controles'),('Notebook','Notebooks'),('PlayStation','Consoles'),('Nintendo','Consoles'),('Smart TV','TVs'),('Celular','Celulares, tablets e relógios'),('Tablet','Celulares, tablets e relógios'),('Smartwatch','Celulares, tablets e relógios'),('Microfone','Setup e acessórios'),('Mousepad','Setup e acessórios')]:
        if k.startswith(p): return c
rows=[];dropped=collections.Counter()
for r in R:
    k=RENAME.get(r['produto'],r['produto'])
    if k in DROP: continue
    t=r['titulo']
    if 'oled' in t.lower() and k in ('Monitor QHD 27" 144Hz+ (mais barato)','Monitor Ultrawide 34" QHD (mais barato)','Monitor 4K (mais barato)','Monitor Full HD 27" 144Hz+ (mais barato)'):
        if k.startswith('Monitor QHD 27'): k='Monitor OLED QHD 27" (mais barato)'
        else: continue
    if COMBO.search(t): dropped['combo']+=1; continue
    if (k.startswith('SSD') or k.startswith('Memória')) and MULTI.search(t): dropped['multi']+=1; continue
    if k.startswith('Memória') and SODIMM.search(t): dropped['sodimm']+=1; continue
    rows.append(dict(id=int(r['post_id']),d=r['data'],k=k,p=float(r['preco']),s=r['loja'],t=t,c=cat(k)))
by=collections.defaultdict(list)
for r in rows: by[r['k']].append(r)
outl=[];clean=[]
for k,l in by.items():
    m=S.median(x['p'] for x in l)
    for x in l:
        if x['p']<0.55*m: outl.append((k,x,m))
        else: clean.append(x)
# daily min
daily=collections.defaultdict(dict)
for x in clean:
    dd=daily[x['k']]; c=dd.get(x['d'])
    if c is None: dd[x['d']]=dict(x,n=1)
    else:
        c['n']+=1
        if x['p']<c['p']: dd[x['d']].update({kk:x[kk] for kk in ('p','s','id','t')})
keep={k:v for k,v in daily.items() if len(v)>=6}
DAYS=[(dt.date(2026,10,1)+dt.timedelta(i)).isoformat() for i in range(41)]
summ=[]
for k,v in keep.items():
    oct_=[v[d]['p'] for d in v if d<'2026-11-01']; nov=[v[d]['p'] for d in v if d>='2026-11-01']
    lo=min(v.values(),key=lambda x:(x['p'],x['d'])); hi=max(v.values(),key=lambda x:(x['p'],x['d']))
    last=v[max(v)]
    summ.append(dict(produto=k,categoria=cat(k),dias_com_oferta=len(v),posts=sum(x['n'] for x in v.values()),
        mediana_out=round(S.median(oct_),2) if oct_ else None,mediana_nov=round(S.median(nov),2) if nov else None,
        var_out_nov=round((S.median(nov)/S.median(oct_)-1)*100,1) if oct_ and nov else None,
        menor=lo['p'],menor_data=lo['d'],menor_loja=lo['s'],maior=hi['p'],maior_data=hi['d'],ultimo=last['p'],ultimo_data=last['d'],ultimo_loja=last['s']))
CO=['Placas de vídeo','Processadores','Placas-mãe','Memória RAM','SSD','Fontes','Gabinetes','Coolers','Monitores','Mouses','Teclados','Headsets e fones','Controles','Setup e acessórios','Notebooks','Consoles','TVs','Celulares, tablets e relógios']
summ.sort(key=lambda s:(CO.index(s['categoria']),s['produto']))
OUT='/mnt/user-data/outputs/base_precos_grape_tec'
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
json.dump({'periodo':['2026-10-01','2026-11-09'],'fonte':'t.me/grape_tec','produtos':[dict(s_,serie=[{'data':d,'preco':keep[s_['produto']][d]['p'],'loja':keep[s_['produto']][d]['s'],'post':keep[s_['produto']][d]['id']} for d in sorted(keep[s_['produto']])]) for s_ in summ]},open(f'{OUT}/base_precos.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump(summ,open('summ.json','w'),ensure_ascii=False); json.dump({k:{d:[v[d]['p'],v[d]['s']] for d in v} for k,v in keep.items()},open('keep.json','w'),ensure_ascii=False)
print(len(rows),'posts válidos',dropped,'| produtos:',len(summ),'| fora da curva:',len(outl))
for k,x,m in sorted(outl,key=lambda o:o[1]['d']):
    if not k.startswith('SSD NVMe 500'): print('  OUTLIER',x['d'],k,x['p'],x['s'],'(mediana',m,')',x['t'][:50])
for s_ in summ: print(f"{s_['categoria'][:10]:10} {s_['produto'][:44]:44} dias={s_['dias_com_oferta']:2} out={s_['mediana_out']} nov={s_['mediana_nov']} var={s_['var_out_nov']} min={s_['menor']} {s_['menor_data'][5:]} ult={s_['ultimo']}")
