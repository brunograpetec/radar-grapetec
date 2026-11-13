"""Modelos (marca + linha/código) e atributos para os filtros do radar."""
import re, collections

MARCA = {'asus': 'ASUS', 'gigabyte': 'Gigabyte', 'aorus': 'Gigabyte', 'msi': 'MSI', 'asrock': 'ASRock', 'biostar': 'Biostar', 'mancer': 'Mancer',
         'husky': 'Husky', 'maxsun': 'Maxsun', 'pcware': 'PCWare', 'afox': 'Afox', 'bluecase': 'Bluecase', 'duex': 'Duex', 'galax': 'Galax',
         'zotac': 'Zotac', 'pny': 'PNY', 'palit': 'Palit', 'gainward': 'Gainward', 'inno3d': 'Inno3D', 'sapphire': 'Sapphire',
         'powercolor': 'PowerColor', 'xfx': 'XFX', 'lg': 'LG', 'samsung': 'Samsung', 'aoc': 'AOC', 'acer': 'Acer', 'philips': 'Philips',
         'dell': 'Dell', 'benq': 'BenQ', 'lenovo': 'Lenovo', 'hq': 'HQ', 'pichau': 'Pichau', 'redragon': 'Redragon', 'superframe': 'SuperFrame',
         'ninja': 'Ninja', 'tcl': 'TCL', 'koorui': 'Koorui', 'kbm': 'KBM', 'gamemax': 'Gamemax', 'xiaomi': 'Xiaomi', 'thermaltake': 'Thermaltake',
         'cooler master': 'Cooler Master', 'corsair': 'Corsair', 'xpg': 'XPG', 'adata': 'XPG', 'kingston': 'Kingston', 'fury': 'Kingston',
         'crucial': 'Crucial', 'wd': 'WD', 'western digital': 'WD', 'sandisk': 'SanDisk', 'lexar': 'Lexar', 'netac': 'Netac',
         'patriot': 'Patriot', 'teamgroup': 'TeamGroup', 't-force': 'TeamGroup', 'tforce': 'TeamGroup', 'hiksemi': 'Hiksemi',
         'kootion': 'Kootion', 'rise mode': 'Rise Mode', 'mach1': 'Mach1', 'pcyes': 'PCYes', 'fortrek': 'Fortrek', 'deepcool': 'DeepCool',
         'lian li': 'Lian Li', 'montech': 'Montech', 'nzxt': 'NZXT', 'arctic': 'Arctic', 'kalkan': 'Kalkan', 'g-storm': 'G-Storm',
         'thermalright': 'Thermalright', 'jonsbo': 'Jonsbo', 'tgt': 'TGT', 'hyperx': 'HyperX', 'seasonic': 'Seasonic',
         'super flower': 'Super Flower', 'one power': 'One Power', 'cougar': 'Cougar', 'oex': 'OEX', 'colorful': 'Colorful',
         'sk hynix': 'SK Hynix', 'hynix': 'SK Hynix', 'gskill': 'G.Skill', 'g.skill': 'G.Skill', 'geil': 'GeIL', 'mymax': 'MyMax',
         'winmemory': 'Winmemory', 'aigo': 'Aigo', 'phanteks': 'Phanteks', 'acegeek': 'Acegeek', 'fsp': 'FSP', 'zalman': 'Zalman',
         'thunderx3': 'ThunderX3', 'dt3': 'DT3', 'draxen': 'Draxen', 'xt racer': 'XT Racer', 'fox racer': 'Fox Racer',
         'dr. office': 'Dr. Office', 'luvinco': 'Luvinco', 'mtek': 'Mtek', 'sharkoon': 'Sharkoon', 'segotep': 'Segotep', 'valecom': 'Valecom',
         'philco': 'Philco', 'hisense': 'Hisense', 'semp': 'Semp', 'toshiba': 'Toshiba', 'aiwa': 'Aiwa', 'sony': 'Sony', 'mibao': 'Mibao',
         'ktrok': 'Ktrok', 'superpc': 'SuperPC'}
_MK = sorted(MARCA, key=len, reverse=True)


def marca(t):
    t = t.lower()
    for m in _MK:
        if re.search(r'(^|[^a-z])' + re.escape(m) + r'($|[^a-z])', t):
            return MARCA[m]
    return None


NOISE = re.compile(r'^(\d+(hz|gb|tb|mb|mhz|w|ms|mm|p|cm|v|pol|x|k|th|nd|rd|st)|ddr\d|pcie\d?|gen\d|m2|nvme|am\d|matx|atx|usb\d*|hdmi\d*|dp\d*|wifi\d*|rgb|4k|2k|8k|1080p|1440p|2160p|80plus|x3d|rev\d+|v\d|pci|sata\d*|cl\d+|hdr\d+|fhd|qhd|uhd|ips|va|tn|oled|e\d|ax\d+|bt\d|ac\d+|r\d|\d+w\d+|\d+x\d+gb|\d+x\d+|dci-?p3|\d+r|pc\d+|c\d\d|ps\d|ntsc|srgb|\d+mt|\d+gbps|\d+mbs|gddr\d+|\d+bits?|x\d|g\d+x?|a\d{3}|b\d{3}|x\d{3}|lga\d+|\d+pin|\d+v|\d{3,4}w)$')


def _codigo(t, m):
    for x in re.findall(r'[a-z0-9][a-z0-9\-]*[a-z0-9]', t.lower()):
        y = x.replace('-', '')
        if len(y) >= 3 and len(re.findall(r'\d', y)) >= 2 and re.search(r'[a-z]', y) and not NOISE.match(y) and y != (m or '').lower().replace(' ', ''):
            return x.upper()
    return None


_SER_MB = [('rog strix', 'ROG Strix'), ('strix', 'ROG Strix'), ('tuf', 'TUF Gaming'), ('prime', 'Prime'), ('aorus elite', 'Aorus Elite'),
           ('aorus', 'Aorus'), ('gaming x', 'Gaming X'), ('ds3h', 'DS3H'), ('tomahawk', 'Tomahawk'), ('mortar', 'Mortar'),
           ('gaming plus', 'Gaming Plus'), ('steel legend', 'Steel Legend'), ('phantom', 'Phantom Gaming'), ('pg lightning', 'PG Lightning'),
           ('lightning', 'PG Lightning'), ('hdv', 'HDV'), ('eagle', 'Eagle'), ('ultra durable', 'Ultra Durable'), ('nexus', 'Nexus'),
           ('challenger', 'Challenger'), ('terminator', 'Terminator'), ('force', 'Force'), ('ayw', 'AYW'), ('pro', 'PRO')]
_SER_RAM = [('fury beast', 'Fury Beast'), ('fury renegade', 'Fury Renegade'), ('vengeance', 'Vengeance'), ('dominator', 'Dominator'),
            ('lancer', 'Lancer'), ('spectrix', 'Spectrix'), ('gammix', 'Gammix'), ('delta', 'Delta'), ('vulcan', 'Vulcan'),
            ('ripjaws', 'Ripjaws'), ('trident', 'Trident Z'), ('flare', 'Flare X5'), ('pro', 'Pro'), ('viper', 'Viper'),
            ('elite', 'Elite'), ('ballistix', 'Ballistix'), ('value', 'Value'), ('ares', 'Ares'), ('hiker', 'Hiker')]


def chipset(t):
    m = re.search(r'\b([abhxz]\d{3}e?)(m)?', t.lower())
    return m.group(1).upper() if m else None


def modelo(produto, titulo):
    """Nome do modelo pra um post de produto-grupo ('mais barata/o'), ou None."""
    grupo = 'mais bar' in produto
    t = titulo.lower()
    if produto.startswith('Placa-mãe'):
        mk = marca(t); c = chipset(t)
        s = next((n for k, n in _SER_MB if k in t), None)
        if not mk or not c or not s: return None
        m = 'M' if re.search(c.lower() + r'm', t) else ''
        extra = ' Plus' if s == 'TUF Gaming' and re.search(r'\bplus\b', t) else ''
        return f'Placa-mãe {mk} {s} {c}{m}{extra}'
    if not grupo: return None
    mk = marca(t)
    if not mk: return None
    if produto.startswith('Memória'):
        g = re.search(r'(ddr[45])', t); cap = re.search(r'\b(8|16|32|64)\s?gb\b', t)
        s = next((n for k, n in _SER_RAM if re.search(r'\b' + k + r'\b', t)), None)
        if not g or not cap or not s: return None
        f = re.search(r'\b(2666|3000|3200|3600|4800|5200|5600|6000|6400|6800|7200)\b', t)
        return f'Memória {mk} {s} {g.group(1).upper()} {cap.group(1)}GB' + (f' {f.group(1)}MHz' if f else '')
    cod = _codigo(t, mk)
    if not cod: return None
    if produto.startswith('Monitor'):
        return f'Monitor {mk} {cod}'
    if produto.startswith('SSD'):
        cap = re.search(r'\b(\d+)\s?(gb|tb)\b', produto.lower())
        return f'SSD {mk} {cod}' + (f' {cap.group(1)}{cap.group(2).upper()}' if cap else '')
    if produto.startswith('Fonte'):
        w = re.search(r'(\d{3,4})\s?w', t)
        return f'Fonte {mk} {cod}' + (f' {w.group(1)}W' if w else '')
    if produto.startswith('Water cooler'):
        mm = re.search(r'(\d{3})\s?mm', produto)
        return f'Water cooler {mk} {cod}' + (f' {mm.group(1)}' if mm else '')
    if produto.startswith('Cadeira'):
        return f'Cadeira {mk} {cod}'
    return None


def _moda(L):
    L = [x for x in L if x]
    return collections.Counter(L).most_common(1)[0][0] if L else None


def _faixa(v, faixas):
    for lim, lab in faixas:
        if v <= lim: return lab
    return faixas[-1][1]


def attrs(cat, produto, titulos):
    """Atributos (para os filtros) a partir do nome e dos títulos dos posts do produto."""
    T = [t.lower() for t in titulos]
    p = produto.lower()
    A = {}
    mk = marca(produto) or _moda([marca(t) for t in T]) if 'mais bar' not in produto else marca(produto)
    if cat == 'Placas-mãe':
        A['Chipset'] = chipset(produto) or _moda([chipset(t) for t in T])
        c = (A['Chipset'] or '')
        A['Plataforma'] = 'AM4' if c[:1] in 'ABX' and c[1:2] in '345' else 'AM5' if c[:1] in 'ABX' and c[1:2] in '68' else 'Intel' if c else None
        A['Tamanho'] = _moda(['Mini-ITX' if re.search(r'\bitx\b', t) else 'mATX' if re.search(r'matx|micro.?atx|' + c.lower() + r'm\b', t) else 'ATX' if re.search(r'\batx\b', t) else None for t in T])
        A['Memória'] = _moda([('DDR5' if 'ddr5' in t else 'DDR4' if 'ddr4' in t else None) for t in T]) or ('DDR4' if A['Plataforma'] == 'AM4' else 'DDR5' if A['Plataforma'] == 'AM5' else None)
        if 'mais bar' not in produto:
            A['Wi-Fi'] = 'Com Wi-Fi' if sum(1 for t in T if re.search(r'wi-?fi|wifi', t)) * 2 >= len(T) else 'Sem Wi-Fi'
            A['Marca'] = marca(produto)
    elif cat == 'Memória RAM':
        A['Tipo'] = 'DDR5' if 'ddr5' in p else 'DDR4' if 'ddr4' in p else _moda([('DDR5' if 'ddr5' in t else 'DDR4' if 'ddr4' in t else None) for t in T])
        cap = re.search(r'(\d+)gb', p)
        A['Capacidade'] = (cap.group(1) + 'GB') if cap else None
        if 'mais bar' not in produto:
            f = re.search(r'(\d{4})mhz', p)
            A['Frequência'] = (f.group(1) + ' MHz') if f else _moda([(lambda m: m.group(1) + ' MHz' if m else None)(re.search(r'\b(2666|3000|3200|3600|4800|5200|5600|6000|6400|6800|7200)\b', t)) for t in T])
            A['Formato'] = 'Kit 2 pentes' if sum(1 for t in T if re.search(r'2\s?x\s?\d|kit|dual', t)) * 2 > len(T) else '1 pente'
            A['RGB'] = 'Com RGB' if sum(1 for t in T if 'rgb' in t) * 2 > len(T) else 'Sem RGB'
            A['Marca'] = marca(produto)
    elif cat == 'Monitores':
        sz = re.search(r'(\d{2})"', produto)
        def _sz(s):
            m = re.search(r'\b(2[1-9]|3[0-4]|4[0-9])(?:[\.,]\d)?\s?(?:"|”|pol|polegadas|\'\')', s)
            return int(m.group(1)) if m else None
        szv = int(sz.group(1)) if sz else _moda([_sz(t) for t in T])
        if not szv and 'mais bar' not in produto:
            cm = re.search(r'(?<!\d)(2[1-9]|3[0-4])(?!\d{2})', produto.split(' ', 2)[-1])
            szv = int(cm.group(1)) if cm else None
        if szv: szv = {23: 24, 31: 32}.get(szv, szv); A['Tamanho'] = f'{szv}"'
        res = lambda s: '4K' if re.search(r'4k|uhd|3840|2160', s) else 'QHD' if re.search(r'qhd|quad hd|wqhd|\b2k\b|1440|2560|3440', s) else 'Full HD' if re.search(r'full ?hd|fhd|1080|1920', s) else None
        A['Resolução'] = res(p) or _moda([res(t) for t in T])
        if (szv or 0) >= 34 or re.search(r'34"|uw|ultrawide', p) or sum(1 for t in T if re.search(r'ultrawide|ultra wide|21:9|3440', t)) * 2 > len(T):
            A['Formato'] = 'Ultrawide'
        else:
            A['Formato'] = 'Normal (16:9)'
        hz = _moda([(lambda m: int(m.group(1)) if m else None)(re.search(r'(\d{2,3})\s?hz', t)) for t in T])
        if hz: A['Taxa'] = _faixa(hz, [(100, 'Até 100Hz'), (180, '144–180Hz'), (240, '200–240Hz'), (999, '280Hz+')])
        pan = lambda s: 'OLED' if 'oled' in s else 'Mini LED' if re.search(r'mini ?led', s) else 'IPS' if 'ips' in s else 'VA' if re.search(r'\bva\b', s) else 'TN' if re.search(r'\btn\b', s) else None
        A['Painel'] = pan(p) or _moda([pan(t) for t in T])
        if 'mais bar' not in produto: A['Marca'] = mk
    elif cat == 'SSD':
        cap = re.search(r'(\d+)\s?(gb|tb)', p) or None
        A['Capacidade'] = (cap.group(1) + cap.group(2).upper()) if cap else None
        g = _moda([('Gen5' if re.search(r'gen ?5|pcie 5', t) else 'Gen4' if re.search(r'gen ?4|pcie 4', t) else 'Gen3' if re.search(r'gen ?3|pcie 3', t) else None) for t in T])
        A['Interface'] = 'NVMe ' + g if g else 'NVMe'
        if 'mais bar' not in produto:
            A['Dissipador'] = 'Com dissipador' if sum(1 for t in T if re.search(r'dissipador|heatsink', t)) * 2 > len(T) else 'Sem dissipador'
            A['Marca'] = mk
    elif cat == 'Fontes':
        w = re.search(r'(\d{3,4})w', p) or None
        wv = int(w.group(1)) if w else _moda([(lambda m: int(m.group(1)) if m else None)(re.search(r'(\d{3,4})\s?w\b', t)) for t in T])
        if wv: A['Potência'] = _faixa(wv, [(550, 'Até 550W'), (650, '600–650W'), (750, '700–750W'), (850, '800–850W'), (9999, '1000W+')])
        cert = lambda s: 'Platinum' if 'platinum' in s else 'Gold' if 'gold' in s else 'Bronze' if 'bronze' in s else 'White' if re.search(r'white|80 ?plus(?! (bronze|gold|platinum))', s) else None
        A['Certificação'] = cert(p) or _moda([cert(t) for t in T])
        if 'mais bar' not in produto:
            A['Modular'] = _moda([('Full modular' if re.search(r'full ?modular|totalmente modular', t) else 'Semi-modular' if re.search(r'semi', t) else 'Modular' if 'modular' in t else 'Não modular') for t in T])
            A['Marca'] = mk
    elif cat == 'Placas de vídeo':
        A['GPU'] = 'NVIDIA' if p.startswith('rtx') else 'AMD' if p.startswith('rx') else 'Intel'
        A['Geração'] = 'RTX 50' if p.startswith('rtx 50') else 'RTX 40' if p.startswith('rtx 40') else 'RX 9000' if p.startswith('rx 9') else 'RX 7000' if p.startswith('rx 7') else None
        v = re.search(r'(\d+)gb', p)
        vram = int(v.group(1)) if v else {'rtx 5050': 8, 'rtx 5060': 8, 'rtx 5070': 12, 'rtx 5070 ti': 16, 'rtx 5080': 16, 'rtx 5090': 32, 'rx 7600': 8, 'rx 9050': 8, 'rx 9070': 16, 'rx 9070 gre': 12, 'rx 9070 xt': 16}.get(p)
        if vram: A['VRAM'] = f'{vram}GB'
    elif cat == 'Processadores':
        m = re.search(r'ryzen (\d) (\d)(\d{3})(\w*)', p)
        if m:
            A['Plataforma'] = 'AM4' if m.group(2) == '5' else 'AM5'
            A['Linha'] = 'Ryzen ' + m.group(1)
            suf = m.group(4)
            A['Tipo'] = '3D V-Cache (X3D)' if 'x3d' in suf else 'Com vídeo (G)' if suf.startswith('g') else 'Sem vídeo' if (m.group(2) == '5' and suf != 'g') or suf.startswith('f') else 'Normal'
    elif cat == 'Coolers':
        A['Tipo'] = 'Water cooler' if p.startswith('water') else 'Air cooler'
        mm = re.search(r'\b(120|240|280|360|420)(?:mm)?\b', p)
        if mm: A['Radiador'] = mm.group(1) + 'mm'
        if 'mais bar' not in produto: A['Marca'] = mk
    elif cat == 'Gabinetes':
        A['Marca'] = mk
        A['Tamanho'] = _moda([('Mid Tower' if re.search(r'mid.?tower', t) else 'Full Tower' if re.search(r'full.?tower', t) else 'Mini Tower' if re.search(r'mini.?tower|matx|micro', t) else None) for t in T])
        A['Lateral'] = 'Vidro' if sum(1 for t in T if re.search(r'vidro|temperado|panor', t)) * 2 >= len(T) else None
    elif cat == 'Cadeiras':
        A['Tipo'] = 'Gamer' if 'gamer' in p or sum(1 for t in T if 'gamer' in t) * 2 > len(T) else 'Escritório'
        if 'mais bar' not in produto: A['Marca'] = mk
    elif cat == 'TVs':
        m = re.match(r'smart tv (.+?) (\d+)" (\S+) · ?(4k|full hd|hd)? ?(.*)$', p)
        if m:
            A['Tamanho'] = m.group(2) + '"'; A['Resolução'] = {'4k': '4K', 'full hd': 'Full HD', 'hd': 'HD'}.get(m.group(4) or '', None)
            A['Painel'] = re.match(r'smart tv .+ · ?(?:4k|full hd|hd)? ?(.*)$', produto, re.I).group(1) or None
            A['Marca'] = re.match(r'Smart TV (.+?) \d+"', produto).group(1)
    return {k: v for k, v in A.items() if v}
