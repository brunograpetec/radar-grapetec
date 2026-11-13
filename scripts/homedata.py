"""Gera home_data.json: um resumo pequeno pro grapetec.com.br (home) puxar ao vivo.
Uso: python3 scripts/homedata.py site_data.json pcideal_data.json home_data.json"""
import json, sys, time
s = json.load(open(sys.argv[1]))
pc = json.load(open(sys.argv[2])) if len(sys.argv) > 3 else {}
dias = s.get('dias') or {}
hoje = max(dias) if dias else ''
itens = (dias.get(hoje) or {}).get('items') or []
ach = []
for x in sorted(itens, key=lambda x: -(x.get('drop') or 0)):
    if not x.get('img') or not x.get('url'): continue
    ach.append({k: x.get(k) for k in ('n', 'p', 'med', 'drop', 'loja', 'img', 'url', 'post', 'cat', 'cup', 'h')})
    if len(ach) >= 8: break
out = dict(ts=int(time.time()), upd=s.get('upd', ''), ofertas=s.get('ofertas'), posts=s.get('total_posts'), dia=hoje,
           nhoje=len(itens), achados=ach, pecas=sum(len(v) for v in (pc.get('parts') or {}).values()))
json.dump(out, open(sys.argv[-1], 'w'), ensure_ascii=False, separators=(',', ':'))
print('home:', len(ach), 'achados', out['nhoje'], 'hoje')
