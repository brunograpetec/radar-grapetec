"""Chave de modelo (marca + código/linha) para comparar oferta com o histórico do próprio modelo."""
import re
MARCAS = ['asus', 'gigabyte', 'msi', 'asrock', 'biostar', 'galax', 'zotac', 'pny', 'palit', 'gainward', 'inno3d', 'sapphire', 'powercolor', 'xfx',
          'lg', 'samsung', 'aoc', 'acer', 'philips', 'dell', 'benq', 'lenovo', 'hq', 'pichau', 'mancer', 'redragon', 'superframe', 'ninja', 'tcl', 'koorui', 'kbm', 'duex', 'husky', 'bluecase', 'gamemax', 'xiaomi', 'mtek', 'eaget', 'thermaltake', 'cooler master', 'corsair', 'xpg', 'adata', 'kingston', 'crucial', 'wd', 'western digital', 'sandisk', 'lexar', 'netac', 'patriot', 'teamgroup', 't-force', 'tforce', 'hiksemi', 'kootion', 'rise mode', 'mach1', 'pcyes', 'fortrek', 'sharkoon', 'deepcool', 'lian li', 'montech', 'nzxt', 'arctic', 'kalkan', 'g-storm', 'thermalright', 'jonsbo', 'tgt', 'hyperx', 'seasonic', 'super flower', 'one power', 'cougar', 'fury', 'oex', 'maxsun', 'afox', 'colorful', 'sk hynix', 'hynix', 'micron', 'gskill', 'g.skill', 'geil', 'mymax', 'winmemory', 'rgb', 'aigo', 'phanteks', 'liketec', 'motospeed', 'kz', 'acegeek', 'pcfort', 'fsp', 'zalman', 'segotep', 'asgard', 'gigabyte aorus']
NOISE = re.compile(r'^(\d+(hz|gb|tb|mb|mhz|w|ms|mm|p|cm|v|pol|x|k|th|nd|rd|st)|ddr\d|pcie\d?|gen\d|m2|nvme|am\d|matx|atx|usb\d*|hdmi\d*|dp\d*|wifi\d*|rgb|4k|2k|8k|1080p|1440p|2160p|80plus|x3d|rev\d+|v\d|pci|sata\d*|cl\d+|hdr\d+|fhd|qhd|uhd|ips|va|tn|oled|e\d|ax\d+|bt\d|ac\d+|r\d|\d+w\d+|r\$\d+|\d+x\d+gb|\d+x\d+|dci-?p3|\d+r|pc\d+|c\d\d|ps\d|ntsc|srgb|cl\d+|\d+mt|\d+gbps|\d+mbs|gddr\d+|\d+bits?|x\d|g\d+x?)$')
SERIE_GPU = ['windforce', 'gaming oc', 'eagle', 'aero', 'aorus', 'ventus', 'shadow', 'gaming trio', 'gaming x', 'inspire', 'prime', 'dual', 'tuf', 'rog strix', 'strix', 'twin edge', 'solid', 'amp', 'trinity', '1-click', '1 click', 'ex gamer', 'white', 'pulse', 'nitro', 'pure', 'hellhound', 'red devil', 'reaper', 'fighter', 'challenger', 'steel legend', 'phantom', 'taichi', 'swift', 'qick', 'mercury', 'quicksilver', 'speedster', 'iceman', 'gamerock', 'jetstream', 'infinity', 'verto', 'epic-x', 'xlr8', 'ultra', 'jagdpanzer']
SINGLES = ('Mouse ', 'Headset ', 'Fone ', 'Controle ', 'Celular ', 'Tablet ', 'Smartwatch ', 'Notebook ', 'PlayStation', 'Nintendo', 'Microfone', 'Mousepad', 'Smart TV', 'Ryzen', 'Gabinete ', 'Air cooler ')


def _marca(t):
    for m in sorted(MARCAS, key=len, reverse=True):
        if re.search(r'(^|[^a-z])' + re.escape(m) + r'($|[^a-z])', t):
            return m
    return None


def chave(produto, titulo):
    """Devolve (chave, nome) ou None. Só para grupos 'mais barato' e placas de vídeo."""
    base = produto.replace(' (mais barata)', '').replace(' (mais barato)', '')
    grupo = 'mais bar' in produto
    gpu = produto.startswith(('RTX ', 'RX ', 'GTX ', 'Arc '))
    if not (grupo or gpu) or produto.startswith(SINGLES + ('Placa-mãe', 'Teclado')):
        return None
    t = titulo.lower().replace('western digital', 'wd')
    m = _marca(t)
    if not m or m == 'rgb':
        return None
    M = {'asrock': 'ASRock', 'xpg': 'XPG', 'aoc': 'AOC', 'lg': 'LG', 'hq': 'HQ', 'msi': 'MSI', 'pny': 'PNY', 'xfx': 'XFX', 'wd': 'WD', 'tcl': 'TCL', 'kbm': 'KBM', 'nzxt': 'NZXT', 'tgt': 'TGT', 'fsp': 'FSP', 'oex': 'OEX'}.get(m, m.title())
    if gpu:
        s = next((x for x in SERIE_GPU if re.search(r'(^|[^a-z])' + re.escape(x) + r'($|[^a-z])', t)), None)
        if not s:
            return None
        oc = ' OC' if re.search(r'\boc\b', t) and s not in ('gaming oc',) else ''
        nome = f'{base} {M} {s.title()}{oc}'
        return nome, nome
    toks = re.findall(r'[a-z0-9][a-z0-9\-]*[a-z0-9]', t)
    cod = None
    for x in toks:
        y = x.replace('-', '')
        if len(y) >= 3 and len(re.findall(r'\d', y)) >= 2 and re.search(r'\d', y) and re.search(r'[a-z]', y) and not NOISE.match(y) and y not in (m.replace(' ', ''),):
            cod = x.upper(); break
    if not cod:
        return None
    nome = f'{base} · {M} {cod}'
    return nome, nome
