"""Cadastro automático de produtos novos no Radar.

O classify.js só reconhece os modelos que estão na lista dele. Este script olha os posts
com preço que ficaram de fora, entende qual é o produto (categoria + marca + modelo,
no mesmo padrão de nome do radar) e:

  cadastra  (1x por dia)  -> adiciona ao dados/catalogo.json os produtos novos que passaram
                             no canal em pelo menos 2 dias diferentes no último mês
  aplica    (a cada 5 min) -> junta ao posts_raw2.csv os posts dos produtos já cadastrados

Regras: produto sempre individual (por modelo; placa de vídeo por chip), cada um na sua
categoria, sem usado/kit/combo/vários tamanhos, e os modelos que o Bruno tirou (DROP do
base.py) continuam fora.

Uso (de dentro de work/):  python3 ../scripts/novos.py cadastra|aplica
"""
import csv, glob, json, os, re, sys, collections, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atributos as AT

POSTS = os.environ.get('POSTS', '../dados/posts')
CAT_F = os.environ.get('CATALOGO', '../dados/catalogo.json')
LOG_F = os.environ.get('CATALOGO_LOG', '../dados/catalogo_log.md')

# marcas que faltavam pra periféricos, monitores, gabinetes e afins
for k, v in {'logitech': 'Logitech', 'razer': 'Razer', 'havit': 'Havit', 'fifine': 'Fifine', 'attack shark': 'Attack Shark',
             'steelseries': 'SteelSeries', 'epomaker': 'Epomaker', 'monsgeek': 'MonsGeek', 'akko': 'Akko', 'aula': 'Aula',
             'machenike': 'Machenike', 'motospeed': 'Motospeed', 'qkz': 'QKZ', 'jbl': 'JBL', 'edifier': 'Edifier',
             'gamdias': 'Gamdias', 'geometric future': 'Geometric Future', 'metalfish': 'Metalfish', 'alienware': 'Alienware',
             'haiz': 'Haiz', 'concordia': 'Concórdia', 'concórdia': 'Concórdia', 'ediloca': 'Ediloca', 'obsid': 'Obsid',
             'gstorm': 'G-Storm', 'colorfire': 'ColorFire', 'jieshuo': 'Jieshuo', 'mechlands': 'MechLands', 'delta': None,
             'picun': 'Picun', 'kz': None, 'aigo': 'Aigo', 'gigabyte': 'Gigabyte', 'pcyes': 'PCYes', 'vinik': 'Vinik',
             'hp': 'HP', 'kbm!': 'KBM', 'warrior': 'Warrior', 'multilaser': 'Multilaser', 'c3tech': 'C3Tech', 'tecware': 'Tecware',
             'ajazz': 'Ajazz', 'redmagic': 'RedMagic', 'darkflash': 'Darkflash', 'zadak': 'Zadak', 'biwin': 'Biwin',
             'asgard': 'Asgard', 'goline': 'Goline', 'tcl': 'TCL', 'philips': 'Philips', 'phillips': 'Philips'}.items():
    if v and k not in AT.MARCA:
        AT.MARCA[k] = v
AT._MK = sorted(AT.MARCA, key=len, reverse=True)

FORA = re.compile(r'usad[oa]|seminov|recondicion|vitrine|open ?box|\bkit\b|combo|\bcupom\b|^cupom|notebook|laptop|pc gamer|computador|'
                  r'mini ?pc|\+\s*(processador|placa|water|mem|ssd|cooler|fonte)|sodimm|so-dimm|para notebook|capa |pel[ií]cula|suporte|'
                  r'mousepad|mouse ?pad|desk ?pad|pasta t[eé]rmica|ventoinha|cooler fan|^fan |kit fan|controladora|adaptador|cabo |playstation|\\bps5\\b', re.I)
MULTI = re.compile(r'(\d{3})\s?gb\s*[/,e]?\s*(\d{3}\s?gb|1\s?tb|2\s?tb)|1\s?tb\s*[/,e]?\s*2\s?tb|2\s?tb\s*[/,e]?\s*4\s?tb', re.I)
DROP = {'Ryzen 3 2200G', 'Ryzen 5 2600X', 'RTX 3070', 'RTX 3050', 'RTX 3060', 'RTX 3060 Ti', 'RTX 2060 Super', 'RTX 4050', 'RX 5500 XT',
        'RX 5600 XT', 'RX 5600', 'RX 5700', 'RX 6600', 'Ryzen 7 5700G'}


GEN = set('hdmi vga dp freesync g-sync gsync ultrawide ultra wide curvo curved sata iii ii mb s mid tower mini-tower mid-tower mini full '
          'gamer gaming plus pro max wireless bluetooth sem fio led rgb argb preto preta branco branca black white tela monitor gabinete '
          'mouse headset fone teclado cooler air water model edition series serie série odyssey essential x e'.split())
SENSOR = re.compile(r'\b(paw|pmw|hero|focus)\s?\d{3,5}k?\b|\b\d{2,3}\s?g\b|\b\d{3,5}\s?dpi\b|\b\d{4,5}\s?hz\b|mid[\s-]?tower|mini[\s-]?tower|full[\s-]?tower|lateral( de vidro)?|aqu[aá]rio|vidro temperado|ultraleve|ultra leve', re.I)


def _cod(t, mk):
    t = re.sub(r'\bmodel (\d+)', r'model-\1', SENSOR.sub(' ', t))
    c = AT._codigo(t, mk) or AT._palavras(t, mk)
    return c


def valido(k):
    """O nome tem um modelo de verdade (não só palavras genéricas)?"""
    resto = k.split(' ', 2)[2] if k.count(' ') >= 2 else ''
    toks = [x for x in re.split(r'[\s/]+', resto.lower()) if x and not re.fullmatch(r'[\d\.,]+"|\d+(gb|tb|w|mm)', x)]
    if not toks: return False
    return any(x not in GEN for x in toks)


def codigo(k):
    """Código do modelo pra achar duplicado (25G523B-B = 25G523B). Ignora marca, chipset, watts e tamanhos."""
    marcas = {re.sub(r'[^a-z0-9]', '', x) for x in list(AT.MARCA) + list(AT.MARCA.values())}
    best = ''
    for x in re.findall(r'[a-z0-9\-]+', k.lower())[1:]:
        y = x.replace('-', '')
        if y in marcas or re.fullmatch(r'[abhxz]\d{3}[em]?|\d+(w|mm|gb|tb|hz)|\d+', y): continue
        if len(y) >= 5 and re.search(r'\d', y) and re.search(r'[a-z]', y) and len(y) > len(best): best = y
    return best


def mesmo(a, b):
    """Mesmo produto escrito de outro jeito? Só dentro da mesma categoria e da mesma marca."""
    if a.split()[0] != b.split()[0] or re.match(r'(Intel|Ryzen|RTX|RX|GTX|Arc) ', a): return False
    if AT.marca(a.lower()) != AT.marca(b.lower()): return False
    ca, cb = codigo(a), codigo(b)
    if not ca or not cb: return False
    return ca == cb or (min(len(ca), len(cb)) >= 6 and (ca.startswith(cb) or cb.startswith(ca)) and abs(len(ca) - len(cb)) <= 2)


# G-Storm (parceiro): todos os produtos, escrito G-Storm, GStorm ou G Storm
GSTORM = [(r'hx700', 'Coolers', 'Water cooler G-Storm HX700 360'), (r'hx500', 'Coolers', 'Water cooler G-Storm HX500 240'),
          (r'gx400', 'Coolers', 'Air cooler G-Storm GX400'), (r'sentinel', 'Gabinetes', 'Gabinete G-Storm Sentinel'),
          (r'frost.*(fan|12\s?cm|120)|(fan|12\s?cm|120).*frost|gs-frost-120', 'Coolers', 'Fan G-Storm Frost 120mm (kit 3 fans)'),
          (r'fonte.*frost|frost.*fonte', 'Fontes', 'Fonte G-Storm Frost {w}W'), (r'fonte|airflow', 'Fontes', 'Fonte G-Storm Airflow {w}W')]


def gstorm(t):
    if not re.search(r'\bg[\s\-]?storm', t) or re.search(r'usad[oa]|seminov|open ?box|vitrine', t):
        return None
    for r, c, n in GSTORM:
        if re.search(r, t):
            if '{w}' in n:
                w = re.search(r'(\d{3,4})\s?w\b', t)
                if not w: return None
                n = n.format(w=w.group(1))
            return (c, n)
    return None


def nome(titulo):
    """(categoria, nome do produto) pra um título de post, ou None se não der pra ter certeza."""
    t0 = titulo.strip()
    t = re.sub(r'^[^\w]+', '', t0.lower())
    gs = gstorm(t)
    if gs: return gs
    if not t or FORA.search(t):
        return None
    # placa-mãe
    if re.match(r'(asus |msi |gigabyte |asrock )?placa[\s-]*m[ãa]e|^motherboard', t):
        n = AT.modelo('Placa-mãe X (mais barata)', t)
        return ('Placas-mãe', n) if n and AT.chipset(t) else None
    # placa de vídeo (por chip)
    if re.match(r'placa (de )?v[ií]deo|placa gr[aá]fica|rtx\s?\d{4}|rx\s?\d{3,4}|gtx\s?\d{4}|geforce|radeon', t):
        m = re.search(r'rtx\s?(\d{4})\s?(ti|super)?', t)
        if m:
            n = 'RTX ' + m.group(1) + (' ' + m.group(2).replace('ti', 'Ti').replace('super', 'Super') if m.group(2) else '')
            if m.group(1) == '5060' and m.group(2) == 'ti': n += ' 16GB' if re.search(r'16\s?g', t) else ' 8GB'
            return ('Placas de vídeo', n)
        m = re.search(r'\brx\s?(\d{3,4})\s?(xt|gre)?\b', t)
        if m:
            n = 'RX ' + m.group(1) + (' ' + m.group(2).upper() if m.group(2) else '')
            if m.group(1) == '9060' and m.group(2) == 'xt': n += ' 16GB' if re.search(r'16\s?g', t) else ' 8GB'
            return ('Placas de vídeo', n)
        m = re.search(r'gtx\s?(\d{4})\s?(ti|super)?', t)
        if m:
            return ('Placas de vídeo', 'GTX ' + m.group(1) + (' ' + m.group(2).replace('ti', 'Ti').replace('super', 'Super') if m.group(2) else ''))
        m = re.search(r'\barc\s?([ab]\d{3})', t)
        if m:
            return ('Placas de vídeo', 'Arc ' + m.group(1).upper())
        return None
    # processador
    if re.match(r'processador|cpu |intel core|core i\d|core ultra|amd ryzen|ryzen', t):
        m = re.search(r'core\s?ultra\s?([3579])\s?(\d{3})\s?([a-z]{0,2})\b', t)
        if m:
            return ('Processadores', f'Intel Core Ultra {m.group(1)} {m.group(2)}{m.group(3).upper()}')
        m = re.search(r'core\s?(i[3579])[\s-]?(\d{4,5})\s?([a-z]{0,2})\b', t)
        if m:
            return ('Processadores', f'Intel Core {m.group(1)}-{m.group(2)}{m.group(3).upper()}')
        m = re.search(r'ryzen\s?([3579])\s?(\d{4})\s?(x3d|xt|x|gt|ge|g|f)?\b', t)
        if m:
            return ('Processadores', f'Ryzen {m.group(1)} {m.group(2)}' + (m.group(3).upper() if m.group(3) else ''))
        return None
    mk = AT.marca(t)
    if not mk:
        return None
    if t.startswith('monitor'):
        if not AT._codigo(t, mk): return None   # sem código de modelo não dá pra separar um monitor do outro
        n = AT.modelo('Monitor (mais barato)', t)
        return ('Monitores', n) if n else None
    if re.match(r'(ssd|aliexpress - ssd)\b', t) or (re.search(r'\bssd\b', t[:30]) and not t.startswith('hd ')):
        if MULTI.search(t): return None
        caps = re.findall(r'\b(\d+)\s?(gb|tb)\b', t)
        caps = {('500GB' if c in ('500', '512') and u == 'gb' else c + u.upper()) for c, u in caps if not (u == 'gb' and int(c) < 120)}
        if len(caps) != 1: return None
        n = AT.modelo(f'SSD {caps.pop()} (mais barato)', t)
        return ('SSD', n) if n else None
    if t.startswith('fonte'):
        if not re.search(r'\d{3,4}\s?w', t): return None
        n = AT.modelo('Fonte (mais barata)', t)
        return ('Fontes', n) if n else None
    if re.match(r'water ?cooler|watercooler', t):
        mm = re.search(r'\b(120|240|280|360|420)\s?mm|\b(240|280|360|420)\b', t)
        if not mm: return None
        n = AT.modelo(f'Water cooler {mm.group(1) or mm.group(2)}mm (mais barato)', t)
        return ('Coolers', n) if n else None
    if re.match(r'(air )?cooler( gamer)? (para processador|para cpu)?|air cooler', t) and 'water' not in t:
        c = _cod(t, mk)
        return ('Coolers', f'Air cooler {mk} {c}') if c else None
    if t.startswith('gabinete'):
        c = _cod(t, mk)
        return ('Gabinetes', f'Gabinete {mk} {c}') if c else None
    if re.match(r'mouse(?! ?pad)', t):
        c = _cod(t, mk)
        return ('Mouses', f'Mouse {mk} {c}') if c else None
    if t.startswith('teclado'):
        n = AT.modelo('Teclado (mais barato)', t)
        return ('Teclados', n) if n else None
    if re.match(r'headset|fone de ouvido|fone gamer|headphone', t):
        c = _cod(t, mk)
        return ('Headsets e fones', f'Headset {mk} {c}') if c else None
    return None


flat = lambda x: x if isinstance(x, str) else ''.join(flat(y) for y in x) if isinstance(x, list) else (x.get('text', '') if isinstance(x, dict) else '')


def posts(desde):
    """(id, dia, título, preço, loja) dos posts com preço desde a data, no mesmo corte do classify.js."""
    vis = set()
    for f in sorted(glob.glob(os.path.join(POSTS, '*.json'))):
        for m in json.load(open(f))['messages']:
            if m.get('type') != 'message' or m['id'] in vis or m['date'][:10] < desde:
                continue
            vis.add(m['id'])
            txt = flat(m.get('text', ''))
            i = txt.find('💰')
            if i < 0:   # post sem o 💰 (ex.: postado à mão): o preço é o primeiro R$
                i = txt.find('R$')
                if i < 0:
                    continue
                i = txt.rfind('\n', 0, i) + 1 or i
            pm = re.search(r'R\$\s?([\d\.]+(?:,\d{1,2})?)', txt[i:])
            if not pm:
                continue
            preco = float(pm.group(1).replace('.', '').replace(',', '.'))
            if not preco:
                continue
            t = re.sub(r'[^\w\s\-/\.,+"”\']', ' ', txt[:i]).replace('\n', ' ')
            t = re.sub(r'\s+', ' ', t).strip()
            lo = re.search(r'kabum|amzn|amazon|shopee|mercadoli|meli\.la|aliexpress|pichau|terabyte|magalu|magazineluiza', txt, re.I)
            loja = {'kabum': 'KaBuM', 'amzn': 'Amazon', 'amazon': 'Amazon', 'shopee': 'Shopee', 'mercadoli': 'Mercado Livre', 'meli.la': 'Mercado Livre',
                    'aliexpress': 'AliExpress', 'pichau': 'Pichau', 'terabyte': 'Terabyte', 'magalu': 'Magalu', 'magazineluiza': 'Magalu'}.get(lo.group(0).lower(), '?') if lo else '?'
            yield int(m['id']), m['date'][:10], t, preco, loja


def ja_classificados():
    ids = set()
    for f in ('posts_raw2.csv', 'posts_extra2.csv'):
        if os.path.exists(f):
            ids |= {int(r['post_id']) for r in csv.DictReader(open(f, encoding='utf-8'))}
    return ids


def carrega():
    if os.path.exists(CAT_F):
        return json.load(open(CAT_F))
    return {'_leia': 'Produtos cadastrados sozinhos pelo radar (scripts/novos.py). Pra tirar um produto, apague a linha dele.', 'ultimo': '', 'itens': {}}


def cadastra():
    C = carrega()
    hoje = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).date()
    desde = (hoje - dt.timedelta(days=30)).isoformat()
    ja = ja_classificados()
    existentes = set()
    if os.path.exists('base/resumo_produtos.csv'):
        existentes = {r['produto'] for r in csv.DictReader(open('base/resumo_produtos.csv', encoding='utf-8-sig'), delimiter=';')}
    dias = collections.defaultdict(set); cats = {}; n = collections.Counter(); ex = {}
    for pid, d, t, p, loja in posts(desde):
        if pid in ja:
            continue
        r = nome(t)
        if not r: continue
        c, k = r
        if k in DROP or not valido(k): continue
        dias[k].add(d); cats[k] = c; n[k] += 1; ex.setdefault(k, t[:120])
    novos = []
    conhecidos = [x for x in existentes if 'mais bar' not in x] + [x for x, v in C['itens'].items() if not v.get('igual')]
    for k, ds in sorted(dias.items(), key=lambda x: -n[x[0]]):
        if k in C['itens'] or (k in existentes and 'G-Storm' not in k):
            continue
        par = next((x for x in conhecidos if mesmo(k, x)), None)
        if par:   # mesmo modelo escrito de outro jeito: junta no que já existe
            C['itens'][k] = dict(cat=cats[k], desde=hoje.isoformat(), igual=par)
            continue
        if len(ds) < 2 and 'G-Storm' not in k:
            continue
        C['itens'][k] = dict(cat=cats[k], desde=hoje.isoformat(), posts=n[k], exemplo=ex[k])
        novos.append(k); conhecidos.append(k)
    C['ultimo'] = hoje.isoformat()
    json.dump(C, open(CAT_F, 'w'), ensure_ascii=False, indent=1)
    if novos:
        por = collections.defaultdict(list)
        for k in novos: por[cats[k]].append(k)
        with open(LOG_F, 'a') as f:
            f.write(f'\n## {hoje:%d/%m/%Y}: {len(novos)} produtos novos\n')
            for c, L in sorted(por.items()):
                f.write(f'- **{c}** ({len(L)}): ' + ', '.join(L) + '\n')
    print('novos cadastrados:', len(novos), '| catálogo:', len(C['itens']))
    return novos


def aplica():
    C = carrega()
    if not C['itens']:
        print('catálogo vazio'); return
    desde = os.environ.get('D0', '2026-10-01')
    ja = ja_classificados()
    add = []
    for pid, d, t, p, loja in posts(desde):
        if pid in ja: continue
        r = nome(t)
        if r and r[1] in C['itens']:
            k = C['itens'][r[1]].get('igual') or r[1]
            add.append([pid, d, k, p, loja, t[:160].replace('|', '/')])
    with open('posts_raw2.csv', 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(add)
    print('posts de produtos cadastrados:', len(add))


if __name__ == '__main__':
    {'cadastra': cadastra, 'aplica': aplica}[sys.argv[1]]()
