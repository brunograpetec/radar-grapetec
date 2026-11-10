import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.ticker as mt
from matplotlib import font_manager as fm
import json,os,re,unicodedata,datetime as dt,statistics as S
for f in ['Inter-Regular.otf','Inter-Medium.otf','Inter-SemiBold.otf','Inter-Bold.otf']:
    fm.fontManager.addfont('/usr/share/fonts/opentype/inter/'+f)
plt.rcParams['font.family']='Inter'
BG='#0b0f14'; CARD='#131a22'; GRID='#232c37'; INK='#eef2f6'; INK2='#9aa6b3'; MUTED='#5f6b78'; ACC='#76b900'; LOW='#3ecf6e'; HIGH='#ff5a4e'
summ=json.load(open('summ.json')); keep=json.load(open('keep.json'))
D0=dt.date(2026,10,1); DAYS=[D0+dt.timedelta(i) for i in range(41)]
OUT='/mnt/user-data/outputs/graficos_out_nov'; os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT,f))
def brl(v):
    s=f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.'); return 'R\\$ '+(s[:-3] if s.endswith(',00') else s)
def pct(v): return '—' if v is None else (('▲ ' if v>0.5 else '▼ ' if v<-0.5 else '= ')+f'{abs(v):.1f}%'.replace('.',','))
def pcol(v): return INK2 if v is None or abs(v)<=0.5 else (HIGH if v>0 else LOW)
def slug(s): return re.sub(r'[^a-z0-9]+','_',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('_')
def ddmm(iso): return iso[8:]+'/'+iso[5:7]
CATS=['Placas de vídeo','Processadores','Placas-mãe','Memória RAM','SSD','Fontes','Gabinetes','Coolers','Monitores','Mouses','Teclados','Headsets e fones','Controles','Setup e acessórios','Notebooks','Consoles','TVs','Celulares, tablets e relógios']
CATN={'Placas de vídeo':'PLACA DE VÍDEO','Processadores':'PROCESSADOR','Placas-mãe':'PLACA-MÃE','Memória RAM':'MEMÓRIA RAM','SSD':'SSD','Fontes':'FONTE','Gabinetes':'GABINETE','Coolers':'COOLER','Monitores':'MONITOR','Mouses':'MOUSE','Teclados':'TECLADO','Headsets e fones':'HEADSET E FONE','Controles':'CONTROLE','Setup e acessórios':'SETUP','Notebooks':'NOTEBOOK · CONFIGURAÇÕES PODEM VARIAR','Consoles':'CONSOLE','TVs':'SMART TV','Celulares, tablets e relógios':'CELULAR, TABLET E RELÓGIO'}
n=0
for s in summ:
    n+=1; k=s['produto']; v=keep[k]
    pts=sorted((dt.date.fromisoformat(d),p,st) for d,(p,st) in v.items())
    xs=[(d-D0).days for d,_,_ in pts]; ys=[p for _,p,_ in pts]
    lo=min(ys); hi=max(ys); ilo=ys.index(lo); ihi=ys.index(hi)
    fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=BG)
    fig.text(0.05,0.905,CATN[s['categoria']],color=ACC,fontsize=22,fontweight='semibold')
    name=k.replace(' (mais barata)','').replace(' (mais barato)','')
    fs=58 if len(name)<24 else 46 if len(name)<34 else 38
    fig.text(0.05,0.83,name,color=INK,fontsize=fs,fontweight='bold')
    sub='Menor preço postado por dia · 1º de outubro a 10 de novembro de 2026 (até 15h26)'
    if k.endswith('(mais barata)') or k.endswith('(mais barato)'): sub+=' · o mais barato da categoria em cada dia'
    fig.text(0.05,0.785,sub,color=INK2,fontsize=20)
    tiles=[('MENOR DO PERÍODO',brl(s['menor']),f"{ddmm(s['menor_data'])} · {s['menor_loja']}",LOW),
           ('MEDIANA OUT → NOV',pct(s['var_out_nov']),(f"{brl(s['mediana_out'])} → {brl(s['mediana_nov'])}" if s['mediana_nov'] and s['mediana_out'] else ('sem ofertas em novembro' if not s['mediana_nov'] else 'sem ofertas em outubro')),pcol(s['var_out_nov'])),
           ('ÚLTIMO PREÇO',brl(s['ultimo']),f"{ddmm(s['ultimo_data'])} · {s['ultimo_loja']}",INK2)]
    for j,(t,val,sb,c) in enumerate(tiles):
        x0=0.585+j*0.135
        fig.patches.append(plt.Rectangle((x0,0.775),0.125,0.15,transform=fig.transFigure,facecolor=CARD,edgecolor=GRID,lw=1.5))
        fig.patches.append(plt.Rectangle((x0,0.919),0.125,0.006,transform=fig.transFigure,facecolor=c,edgecolor='none'))
        fig.text(x0+0.01,0.885,t,color=INK2,fontsize=14,fontweight='semibold')
        fig.text(x0+0.01,0.832,val,color=INK,fontsize=28 if len(val)<12 else 23,fontweight='bold')
        fig.text(x0+0.01,0.795,sb,color=INK2,fontsize=13.5)
    ax=fig.add_axes([0.1,0.15,0.85,0.56],facecolor=BG)
    span=(hi-lo) or hi*0.05
    y0=lo-span*0.6; ax.set_ylim(y0,hi+span*0.55); ax.set_xlim(-1,41)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.grid(axis='y',color=GRID,lw=1); ax.tick_params(colors=MUTED,labelsize=15,length=0)
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda val,_:brl(round(val))))
    tk=[i for i,d in enumerate(DAYS) if d.weekday()==0]; ax.set_xticks(tk); ax.set_xticklabels([DAYS[i].strftime('%d/%m') for i in tk],fontsize=15,color=INK2)
    ax.axvline(30.5,color=GRID,lw=2)
    ax.text(15,hi+span*0.45,'OUTUBRO',ha='center',color=MUTED,fontsize=15,fontweight='semibold'); ax.text(35.5,hi+span*0.45,'NOVEMBRO',ha='center',color=MUTED,fontsize=15,fontweight='semibold')
    for a,b,m in ((-0.5,30.5,s['mediana_out']),(30.5,40.5,s['mediana_nov'])):
        if m: ax.hlines(m,a,b,colors=INK2,linestyles=(0,(5,4)),lw=1.5,alpha=0.7); ax.text(a+0.4,m,'mediana '+brl(m),ha='left',va='bottom',color=INK2,fontsize=12.5,bbox=dict(facecolor=BG,edgecolor='none',pad=1.5,alpha=0.85),zorder=6)
    ax.fill_between(xs,ys,y0,color=ACC,alpha=0.07,lw=0)
    ax.plot(xs,ys,color=ACC,lw=3,solid_joinstyle='round',zorder=3)
    ax.scatter(xs,ys,s=36,color=ACC,edgecolors=BG,linewidths=1.5,zorder=4)
    marks={ilo:('menor',LOW),ihi:('maior',HIGH)}; il=len(ys)-1
    if il not in marks: marks[il]=('último',INK)
    for i,(lab,c) in marks.items():
        x,y=xs[i],ys[i]; below=(lab=='menor')
        ax.scatter([x],[y],s=170,color=c,edgecolors=BG,linewidths=3,zorder=5)
        ha='right' if x>36 else 'left' if x<3 else 'center'
        ax.annotate(brl(y),(x,y),xytext=(0,-36 if below else 32),textcoords='offset points',ha=ha,color=INK,fontsize=19,fontweight='bold')
        ax.annotate(f"{lab} · {pts[i][0].strftime('%d/%m')} · {pts[i][2]}",(x,y),xytext=(0,-54 if below else 16),textcoords='offset points',ha=ha,color=INK2,fontsize=12.5)
    fig.text(0.05,0.045,'Fonte: canal Grape Tec Ofertas de Hardware (t.me/grape_tec) · menor preço postado em cada dia, já com cupom quando havia · dias sem ponto = sem oferta no canal',color=MUTED,fontsize=13.5)
    fig.text(0.95,0.045,'GRAPE TEC',color=ACC,fontsize=18,fontweight='bold',ha='right')
    ci=CATS.index(s['categoria'])+1
    fig.savefig(f"{OUT}/{ci:02d}_{slug(s['categoria'])}__{slug(name)}.png",facecolor=BG); plt.close(fig)
def board(items,title,fn):
    fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=BG)
    fig.text(0.05,0.9,title,color=INK,fontsize=46,fontweight='bold')
    fig.text(0.05,0.85,'Menor preço postado por dia no canal · outubro x novembro (até 10/11) de 2026',color=INK2,fontsize=20)
    cols=[(0.05,'PRODUTO','left'),(0.47,'MEDIANA OUT','right'),(0.585,'MEDIANA NOV','right'),(0.68,'VARIAÇÃO','right'),(0.84,'MENOR DO PERÍODO','right'),(0.855,'ONDE','left')]
    top=0.78; rh=min(0.058,0.68/len(items))
    for x,t,a in cols: fig.text(x,top,t,color=INK2,fontsize=14,fontweight='semibold',ha=a)
    for r,s in enumerate(items):
        y=top-0.045-r*rh
        if r%2==0: fig.patches.append(plt.Rectangle((0.04,y-rh*0.45),0.92,rh*0.9,transform=fig.transFigure,facecolor=CARD,edgecolor='none'))
        f=min(20,rh*340); nm=s['produto'].replace(' (mais barata)','*').replace(' (mais barato)','*')
        fig.text(0.05,y,nm,color=INK,fontsize=f,fontweight='semibold',va='center')
        fig.text(0.47,y,brl(s['mediana_out']) if s['mediana_out'] else '—',color=INK2,fontsize=f-1,ha='right',va='center')
        fig.text(0.585,y,brl(s['mediana_nov']) if s['mediana_nov'] else '—',color=INK,fontsize=f-1,ha='right',va='center')
        fig.text(0.68,y,pct(s['var_out_nov']),color=pcol(s['var_out_nov']),fontsize=f,fontweight='bold',ha='right',va='center')
        fig.text(0.84,y,f"{brl(s['menor'])}  ({ddmm(s['menor_data'])})",color=INK,fontsize=f-1,fontweight='bold',ha='right',va='center')
        fig.text(0.855,y,s['menor_loja'],color=INK2,fontsize=f-2,ha='left',va='center')
    fig.text(0.05,0.045,'* o mais barato da categoria em cada dia (modelos variam) · Fonte: t.me/grape_tec · preços com cupom quando havia',color=MUTED,fontsize=13.5)
    fig.text(0.95,0.045,'GRAPE TEC',color=ACC,fontsize=18,fontweight='bold',ha='right')
    fig.savefig(f'{OUT}/{fn}.png',facecolor=BG); plt.close(fig)
for ci,c in enumerate(CATS,1):
    it=[s for s in summ if s['categoria']==c]
    if len(it)>14:
        h=(len(it)+1)//2; board(it[:h],f'{c} · parte 1',f'00_placar_{ci:02d}_{slug(c)}_1'); board(it[h:],f'{c} · parte 2',f'00_placar_{ci:02d}_{slug(c)}_2')
    else: board(it,c,f'00_placar_{ci:02d}_{slug(c)}')
print(n,'gráficos', len(os.listdir(OUT)),'arquivos')
