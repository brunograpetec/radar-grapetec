"""Gera home_data.json: um resumo pequeno pro grapetec.com.br (home) puxar ao vivo.
Uso: python3 scripts/homedata.py site_data.json pcideal_data.json home_data.json"""
import json, sys, time
s = json.load(open(sys.argv[1]))
pc = json.load(open(sys.argv[2])) if len(sys.argv) > 3 else {}
dias = s.get('dias') or {}
hoje = max(dias) if dias else ''
itens = (dias.get(hoje) or {}).get('items') or []
PN = {q['n']: q for q in s.get('P') or []}
ach = []
for x in sorted(itens, key=lambda x: -(x.get('drop') or 0)):
    if not x.get('img') or not x.get('url'): continue
    a = {k: x.get(k) for k in ('n', 'p', 'med', 'drop', 'loja', 'img', 'url', 'post', 'cat', 'cup', 'h')}
    P = PN.get(x.get('n'))
    if P:
        a['id'] = P.get('id')
        if len(ach) == 0:   # só o destaque leva a curva (últimos ~30 dias), pra o arquivo ficar pequeno
            ss = [q for q in P.get('s') or [] if q[0] >= (P['s'][-1][0] - 30)]
            a['s'] = [[q[0], round(q[1])] for q in ss]
    ach.append(a)
    if len(ach) >= 8: break
out = dict(ts=int(time.time()), upd=s.get('upd', ''), ofertas=s.get('ofertas'), posts=s.get('total_posts'), dia=hoje,
           nhoje=len(itens), achados=ach, pecas=sum(len(v) for v in (pc.get('parts') or {}).values()))
json.dump(out, open(sys.argv[-1], 'w'), ensure_ascii=False, separators=(',', ':'))
print('home:', len(ach), 'achados', out['nhoje'], 'hoje')
