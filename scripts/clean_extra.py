import csv,re
R=list(csv.DictReader(open('posts_extra2.csv',encoding='utf-8')))
out=[]
for r in R:
    k=r['produto'];t=r['titulo'].lower()
    if k=='Controle Xbox sem fio':
        if re.search(r'8bitdo|easysmx|gamesir|compat[ií]vel|para xbox|tipo c|com fio|elite',t) or not re.search(r'xbox',t): continue
    if k=='Controle 8BitDo Ultimate 2': k='Controle 8BitDo Ultimate 2C' if re.search(r'ultimate 2c',t) else 'Controle 8BitDo Ultimate 2'
    if k.startswith('Smart TV'):
        m=re.search(r'\b(32|40|43|50|55|58|60|65|70|75|85)\b',t); sz=m and m.group(1)
        if sz=='43': k='Smart TV 43" (mais barata)'
        elif sz in ('50','55','65') and re.search(r'4k|uhd',t): k=f'Smart TV {sz}" 4K (mais barata)'
        else: continue
    if k=='Celular Xiaomi Poco X8': continue
    if k=='Headset Havit H2002C': k='Headset Havit H2002'
    if k=='Mouse HyperX Pulsefire Haste': k='Mouse HyperX Pulsefire Haste (1 e 2)'
    r['produto']=k; out.append(r)
with open('posts_extra_clean.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['post_id','data','produto','preco','loja','titulo']); w.writeheader(); w.writerows(out)
print('extra',len(R),'->',len(out))
