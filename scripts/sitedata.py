import os as _os;OUT=_os.environ.get('OUT','/mnt/user-data/outputs/base_precos_grape_tec')
import json,csv,re,unicodedata,statistics as S,datetime as dt
summ=json.load(open('summ.json'))
rows=list(csv.DictReader(open(OUT+'/menor_preco_por_dia.csv',encoding='utf-8-sig'),delimiter=';'))
SC={'KaBuM':'K','Amazon':'A','Shopee':'S','Mercado Livre':'M','AliExpress':'X','Pichau':'P','Terabyte':'T','Magalu':'G','?':'?'}
D0=dt.date(2026,10,1)
ser={}
for r in rows:
    i=(dt.date.fromisoformat(r['data'])-D0).days
    ser.setdefault(r['produto'],[]).append([i,float(r['menor_preco'].replace(',','.')),SC.get(r['loja'],'?'),int(r['link_post'].rsplit('/',1)[1])])
def slug(s): return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def nice(v): 
    step=10 if v<1000 else 50 if v<5000 else 100
    return int(v//step*step)
FEAT={'RTX 5060','RTX 5060 Ti 8GB','RTX 5070','RX 9060 XT 16GB','RX 9070','RX 9070 XT','RX 7600','Ryzen 5 5500','Ryzen 7 5700X','Ryzen 7 5800X3D','Ryzen 7 9800X3D','Ryzen 5 7600X3D','Ryzen 5 9600X','Placa-mãe B550 (mais barata)','Placa-mãe B650 (mais barata)','SSD NVMe 1TB (mais barato)','Memória DDR4 16GB (mais barata)','Fonte 650W 80 Plus Bronze (mais barata)','Monitor Full HD 24" 144–200Hz (mais barato)','Monitor QHD 27" 144Hz+ (mais barato)','Mouse Logitech G305','Teclado Redragon Fizz','Headset Redragon Zeus Pro','Controle DualSense (PS5)','PlayStation 5 Slim','Smart TV 50" 4K (mais barata)','Notebook Lenovo IdeaPad Slim'}
P=[]
for s in summ:
    k=s['produto']; sr=sorted(ser[k]); prices=[p for _,p,_,_ in sr]
    q=sorted(prices); p25=q[max(0,int(len(q)*0.25)-1)]
    alvo=nice(p25); ult=s['ultimo']; ref=s['mediana_nov'] or s['mediana_out']
    if s['ultimo_data']<'2026-11-01': selo='alvo'
    elif ult<=alvo*1.01: selo='compra'
    elif ult>=ref*1.03 or (s['var_out_nov'] or 0)>3: selo='espera'
    else: selo='alvo'
    name=k.replace(' (mais barata)','').replace(' (mais barato)','')
    P.append(dict(id=slug(name),n=name,c=s['categoria'],cat_bucket=k.endswith('(mais barata)') or k.endswith('(mais barato)'),
        s=sr,mo=s['mediana_out'],mn=s['mediana_nov'],v=s['var_out_nov'],lo=s['menor'],lod=s['menor_data'],los=s['menor_loja'],
        u=ult,ud=s['ultimo_data'],ul=s['ultimo_loja'],posts=s['posts'],dias=s['dias_com_oferta'],alvo=alvo,selo=selo,f=k in FEAT))
CATS=['Placas de vídeo','Processadores','Placas-mãe','Memória RAM','SSD','Fontes','Gabinetes','Coolers','Monitores','Mouses','Teclados','Headsets e fones','Controles','Setup e acessórios','Notebooks','Consoles','TVs','Celulares, tablets e relógios']
therm=[]
for c in CATS:
    vs=[p['v'] for p in P if p['c']==c and p['v'] is not None]
    therm.append(dict(c=c,v=(round(S.median(vs),1) if len(vs)>=3 else None),n=len([p for p in P if p['c']==c]),up=sum(1 for x in vs if x>0.5),down=sum(1 for x in vs if x<-0.5)))
ach=[dict(n='Ryzen 7 7800X3D',p=763.29,d='2026-11-08',l='KaBuM',ref=1660,post=224007,tag='Possível erro de preço'),
     dict(n='RX 7600',p=767,d='2026-10-29',l='Shopee',ref=1799,post=None,tag='Possível erro de preço'),
     dict(n='Ryzen 9 9950X3D',p=1279,d='2026-10-23',l='Terabyte',ref=3737,post=None,tag='Possível erro de preço')]
import csv as _c
allp=list(_c.DictReader(open(OUT+'/todos_os_posts_classificados.csv',encoding='utf-8-sig'),delimiter=';'))
def postof(prod,d,price):
    for r in allp:
        if r['produto']==prod and r['data']==d and abs(float(r['preco'].replace(',','.'))-price)<0.01: return int(r['link_post'].rsplit('/',1)[1])
for a in ach:
    if not a['post']:
        a['post']=postof(a['n'],a['d'],a['p'])
for nm in ['RX 9070 XT','RTX 5060','RTX 5060 Ti 16GB','Ryzen 5 7600','Water cooler Arctic Liquid Freezer III Pro 360']:
    p=next(x for x in P if x['n']==nm); pt=min(p['s'],key=lambda x:x[1])
    ach.append(dict(n=nm,p=p['lo'],d=p['lod'],l=p['los'],ref=p['mn'] or p['mo'],post=pt[3],tag='Menor preço do período'))
import os
UPD=os.environ.get('UPD','10/11/2026 às 15h26');ATE=os.environ.get('ATE','10/11 às 15h26')
OFERTAS=len(set(r['link_post'] for r in allp if r['fora_da_curva']!='sim'))
_lastd=max(r['data'] for r in rows)
data=dict(gen=_lastd,upd=UPD,ate=ATE,d0='2026-10-01',days=(dt.date.fromisoformat(_lastd)-D0).days+1,total_posts=int(os.environ.get('TOTAL','18523')),ofertas=OFERTAS,P=P,T=therm,A=ach,
          stores={v:k for k,v in SC.items()})
import os as _o
if _o.path.exists('dias.json'): data['dias']=json.load(open('dias.json'))
s=json.dumps(data,ensure_ascii=False,separators=(',',':'))
open('site_data.json','w').write(s); print(len(s),'bytes',len(P),'produtos'); print([ (a['n'],a['post']) for a in ach])
import collections; print(collections.Counter(p['selo'] for p in P)); print(therm)
