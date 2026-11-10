"""Identifica marca, tamanho, modelo, resolução e painel de uma TV a partir do título do post."""
import re
BR = ['tcl', 'samsung', 'lg', 'philips', 'aoc', 'philco', 'hisense', 'semp', 'toshiba', 'aiwa', 'hq', 'multilaser', 'multi',
      'britania', 'britânia', 'panasonic', 'sony', 'xiaomi']
NOME = {'tcl': 'TCL', 'lg': 'LG', 'aoc': 'AOC', 'hq': 'HQ', 'britânia': 'Britânia', 'britania': 'Britânia', 'multilaser': 'Multi'}
NOISE = re.compile(r'^(4k|8k|uhd|fhd|hdr10|hdr|\d+hz|\d+hdmi|\d+usb|20\d\d|\d+w|aipq|wifi|dled|qled|hd|5g|ai|s|led|ger\d+|u9|dts|\d+p|\d+gb|\d+x)$')
MAPA_MARCA = {}  # modelo -> marca (aprendido nos títulos que têm marca)


def painel(t):
    if 'oled' in t and 'qled' not in t.replace('hi-qled', 'qled'): return 'OLED'
    if re.search(r'mini ?led|miniled|neo qled', t): return 'Mini LED'
    if 'qned' in t: return 'QNED'
    if 'nano' in t: return 'NanoCell'
    if 'qled' in t: return 'QLED'
    return 'LED'


def resol(t, sz):
    if re.search(r'\b(4k|uhd|ultra hd)\b', t): return '4K'
    if re.search(r'full ?hd|\bfhd\b', t): return 'Full HD'
    if re.search(r'\bhd\b', t): return 'HD'
    return ''


def parse(titulo):
    t = titulo.lower().replace('hi-qled', 'hiqled qled')
    b = re.search(r'\b(%s)\b' % '|'.join(BR), t); b = b and b.group(1)
    s = re.search(r'\b(32|40|43|50|55|58|60|65|70|75|85|98|100)\b', t); sz = s and s.group(1)
    if not sz:
        return None
    toks = re.findall(r'\b[a-z0-9]+(?:[/.][0-9a-z]+)?\b', t)
    cand = []
    for x in toks:
        x = re.split(r'[/.]', x)[0]
        if re.search(r'\d', x) and re.search(r'[a-z]', x) and not NOISE.match(x) and len(x) >= 2:
            cand.append(x)
    m = next((c for c in cand if sz in c), None)
    if not m:
        m2 = re.search(r'oled (?:evo )?(?:ai )?(?:4k )?([bcg]\d)\b', t)
        m = m2.group(1) if m2 else next((c for c in cand if len(c) >= 3), None)
    if not m:
        return None
    canon = re.sub(r'^' + sz, '', m)
    canon = re.sub(r'(bpsa|psa|bwz|78g?)$', '', canon) or m
    if canon.startswith('qled') and b == 'hq': canon = 'qled' + canon[4:]
    if b: MAPA_MARCA.setdefault(canon, b)
    b = b or MAPA_MARCA.get(canon)
    if not b:
        return None
    marca = NOME.get(b, b.capitalize())
    return dict(marca=marca, sz=sz, modelo=canon.upper(), res=resol(t, sz), pan=painel(t))


def nome(p):
    tags = ' '.join(x for x in (p['res'], p['pan']) if x)
    return f'Smart TV {p["marca"]} {p["sz"]}" {p["modelo"]} · {tags}'
