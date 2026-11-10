import csv,re,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import tvmodel
R=list(csv.DictReader(open('posts_extra2.csv',encoding='utf-8')))
out=[]
for r in R:
    k=r['produto'];t=r['titulo'].lower()
    if k=='Controle Xbox sem fio':
        if re.search(r'8bitdo|easysmx|gamesir|compat[ií]vel|para xbox|tipo c|com fio|elite',t) or not re.search(r'xbox',t): continue
    if k=='Controle 8BitDo Ultimate 2': k='Controle 8BitDo Ultimate 2C' if re.search(r'ultimate 2c',t) else 'Controle 8BitDo Ultimate 2'
    if k.startswith('Smart TV'):
        p=tvmodel.parse(r['titulo'])
        if not p: continue
        r['_tv']=p; k='TV'
    if k=='Celular Xiaomi Poco X8': continue
    if k=='Headset Havit H2002C': k='Headset Havit H2002'
    if k=='Mouse HyperX Pulsefire Haste': k='Mouse HyperX Pulsefire Haste (1 e 2)'
    r['produto']=k; out.append(r)
# TVs: nome por marca+tamanho+modelo; resolução/painel = o mais citado nos posts do modelo
_tags=collections.defaultdict(lambda:(collections.Counter(),collections.Counter()))
for r in out:
    if '_tv' in r:
        p=r['_tv'];kk=(p['marca'],p['sz'],p['modelo']);_tags[kk][0][p['res']]+=1;_tags[kk][1][p['pan']]+=1
for r in out:
    p=r.pop('_tv',None)
    if p:
        rc,pc=_tags[(p['marca'],p['sz'],p['modelo'])]
        res=next((x for x,_ in rc.most_common() if x),'')
        pan=next((x for x,_ in pc.most_common() if x!='LED'),'LED') if sum(n for x,n in pc.items() if x!='LED')*2>=sum(pc.values()) else 'LED'
        r['produto']=tvmodel.nome(dict(p,res=res,pan=pan))
with open('posts_extra_clean.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['post_id','data','produto','preco','loja','titulo']); w.writeheader(); w.writerows(out)
print('extra',len(R),'->',len(out))
