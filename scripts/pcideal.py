"""Gera pcideal_data.json: preços dos últimos 30 dias das 8 peças do PC (por modelo; GPU por chip).

Uso: OUT=work/base POSTS=dados/posts python3 scripts/pcideal.py pcideal_data.json
Lê a base classificada (todos_os_posts_classificados.csv) e, para memória RAM,
lê direto os posts (a base geral quase não guarda memória).
"""
import csv, json, os, re, sys, glob, statistics as S, datetime as dt, collections

OUT = os.environ.get('OUT', 'work/base')
POSTS = os.environ.get('POSTS', 'dados/posts')
SITE = os.environ.get('SITE', 'site_data.json')
dest = sys.argv[1] if len(sys.argv) > 1 else 'pcideal_data.json'

TXT = {}
FOTO = {}
for f in glob.glob(os.path.join(POSTS, '*.json')):
    for m in json.load(open(f))['messages']:
        TXT[str(m['id'])] = (m['date'], m.get('text', ''))
        if m.get('photo'): FOTO[str(m['id'])] = m['photo']
_ff = os.environ.get('FOTOS', 'dados/fotos.json')
if os.path.exists(_ff):
    for k, v in json.load(open(_ff)).items():
        if v and v[0]: FOTO[k] = v[0]
fim = max(v[0][:10] for v in TXT.values())
D30 = (dt.date.fromisoformat(fim) - dt.timedelta(days=30)).isoformat()
D10 = (dt.date.fromisoformat(fim) - dt.timedelta(days=10)).isoformat()


def link(t):
    i = t.lower().find('link do produto')
    i2 = t.lower().find('link pc')
    for s in ([t[i:]] if i >= 0 else []) + ([t[i2:]] if i2 >= 0 else []) + [t]:
        for u in re.findall(r'https?://[^\s<>"]+', s):
            u = u.rstrip('.,);')
            h = re.sub(r'^https?://', '', u).split('/')[0].lower()
            if any(x in h for x in ('t.me', 'telegram', 'youtube', 'youtu.be', 'grapetec', 'kpages', 'gvgmall')):
                continue
            if h.startswith('lista.') or u.rstrip('/').count('/') < 3:
                continue
            return u
    return ''


def cupom(t):
    m = re.search(r'cupo[mn]s?\s*:?\s*\n?\s*([A-Z0-9]{4,20})\b', t)
    return m.group(1) if m else ''


def loja_de(u, t=''):
    h = u.lower()
    if 'shopee' in h: return 'Shopee'
    if 'meli.la' in h or 'mercadoli' in h: return 'Mercado Livre'
    if 'aliexpress' in h: return 'AliExpress'
    if 'amazon' in h or 'amzn' in h: return 'Amazon'
    m = re.search(r'aoferta\.net/[^-]+-(\w+)', u)
    if m: return {'Kabum': 'KaBuM', 'Amazon': 'Amazon', 'Terabyte': 'Terabyte', 'Pichau': 'Pichau'}.get(m.group(1), m.group(1))
    return ''


def preco(t):
    m = re.search(r'💰\s*R\$\s*([\d.]+(?:,\d{2})?)', t) or re.search(r'R\$\s*([\d.]+(?:,\d{2})?)(?!\s*OFF)', t)
    if not m: return None
    return float(m.group(1).replace('.', '').replace(',', '.'))


rows = collections.defaultdict(list)   # (cat, modelo) -> [(data, preco, loja, post, titulo)]
CATS = {'Processadores': 'cpu', 'Placas de vídeo': 'gpu', 'Placas-mãe': 'mobo', 'SSD': 'ssd',
        'Fontes': 'psu', 'Gabinetes': 'case', 'Coolers': 'cooler',
        'Monitores': 'mon', 'Mouses': 'mouse', 'Teclados': 'kb', 'Headsets e fones': 'head'}
for r in csv.DictReader(open(os.path.join(OUT, 'todos_os_posts_classificados.csv'), encoding='utf-8-sig'), delimiter=';'):
    if r['data'] < D30 or r['fora_da_curva'] == 'sim' or r['categoria'] not in CATS:
        continue
    if 'mais bar' in r['produto']:
        continue
    pid = r['link_post'].rstrip('/').split('/')[-1]
    rows[(CATS[r['categoria']], r['produto'])].append((r['data'], float(r['preco'].replace(',', '.')), r['loja'], pid, r['titulo']))

# memória RAM direto dos posts
for pid, (d, t) in TXT.items():
    if d[:10] < D30: continue
    l1 = t.split('\n')[0]
    if not re.search(r'mem[oó]ria|\bram\b', l1, re.I) or not re.search(r'DDR[45]', l1, re.I): continue
    if re.search(r'notebook|sodimm|so-dimm|server|ecc|placa|kit (?:upgrade|processador)|xeon|/16GB/32GB|8GB/16GB', l1, re.I): continue
    ddr = re.search(r'DDR([45])', l1, re.I).group(1)
    kit = re.search(r'(\d)\s*x\s*(8|16|32)\s*GB', l1, re.I)
    if kit:
        mods, cap = int(kit.group(1)), int(kit.group(2))
    else:
        c = re.findall(r'\b(8|16|32)\s*GB', l1, re.I)
        if not c: continue
        mods, cap = 1, int(c[0])
    mhz = re.search(r'(2666|3000|3200|3600|4800|5200|5600|6000|6400)\s*M?h?z?', l1, re.I)
    if not mhz: continue
    mhz = int(mhz.group(1))
    if ddr == '4' and mhz < 3200: continue  # 2666 não entra no PC ideal
    p = preco(t)
    if not p or p < 120: continue
    if p / (mods * cap) < (22 if ddr == '4' else 40): continue  # anúncio com vários tamanhos / preço de outro tamanho
    u = link(t)
    marca = re.search(r'(Kingston Fury Beast|Fury Beast|HyperX|Hiksemi|Juhor|JUHOR|Gudga|Kingston|XPG|Corsair|Samsung|Macrovip|Puskill|Synex|Rise Mode|Netac|TeamGroup|T-Force|Adata|Crucial|Lexar|Patriot|Pichau|Mancer|Kootion|Keepdata|Knup|Spectrum|Husky|G\.Skill|Gskill|Redragon|Hikvision|Winmemory|Hynix)', l1, re.I)
    marca = marca.group(1).title().replace('Juhor', 'Juhor').replace('Hyperx', 'HyperX').replace('Xpg', 'XPG') if marca else 'Genérica'
    nome = f'Memória {marca} DDR{ddr} {mods}x{cap}GB {mhz}MHz' if mods > 1 else f'Memória {marca} DDR{ddr} {cap}GB {mhz}MHz'
    rows[('ram', nome)].append((d[:10], p, loja_de(u), pid, l1.strip('🎉🚨⭐📦💵💰🤑💸🛍️🛍⚡️⚡🥇🎯🔥👀📢🌟⏰🎁💲🔝✨📣🚀 ')[:120]))

site = json.load(open(SITE)) if os.path.exists(SITE) else {'P': []}
ATTR = {p['n']: p.get('a') or {} for p in site['P']}

out = collections.defaultdict(list)
for (cat, nome), L in rows.items():
    if len(L) < 2 and cat != 'ram':
        continue
    ps = sorted(x[1] for x in L)
    med = S.median(ps)
    # tira lixo: preço abaixo de 55% da mediana
    L = [x for x in L if x[1] >= 0.55 * med]
    ps = sorted(x[1] for x in L)
    q = lambda f: ps[min(len(ps) - 1, int(len(ps) * f))]
    rec = [x for x in L if x[0] >= D10] or L
    best = min(rec, key=lambda x: (x[1], x[0]))
    # entre posts com o mesmo preço mínimo, pega o mais novo
    best = max([x for x in rec if x[1] <= best[1] * 1.01], key=lambda x: x[0])
    d, t = TXT.get(best[3], ('', ''))
    u = link(t)
    it = dict(n=nome, med=round(med), p25=round(q(0.25)), p75=round(q(0.75)), lo=round(ps[0]), np=len(L),
              p=round(best[1], 2), d=best[0], loja=best[2] or loja_de(u), post=int(best[3]), url=u, cup=cupom(t),
              t=best[4][:110], a=ATTR.get(nome, {}), img=FOTO.get(str(best[3]), ''))
    if cat == 'ram':
        m = re.search(r'DDR(\d) (?:(\d)x)?(\d+)GB (\d+)MHz', nome)
        it['a'] = dict(ddr=int(m.group(1)), mods=int(m.group(2) or 1), cap=int(m.group(3)), mhz=int(m.group(4)))
    out[cat].append(it)

for c in out:
    out[c].sort(key=lambda x: x['med'])
extra = {}
_fc = os.environ.get('FRASES_CONSULTORIAS', 'dados/frases_consultorias.json')
if os.path.exists(_fc):
    _d = json.load(open(_fc)); _d.pop('_leia', None)
    extra['frases'] = {k: v for k, v in _d.items() if isinstance(v, list)}
_ct = os.environ.get('CONSULTORIAS', 'dados/consultorias.json')
if os.path.exists(_ct):
    extra['consultorias'] = json.load(open(_ct)).get('contagem', {})
json.dump(dict(gen=fim, d30=D30, ts=int(dt.datetime.now().timestamp()), parts=out, **extra), open(dest, 'w'), ensure_ascii=False, separators=(',', ':'))
print('pcideal:', {c: len(v) for c, v in out.items()})
