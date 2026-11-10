"""Lê as páginas públicas t.me/s/grape_tec e junta os posts novos em dados/posts.json.

Uso: python3 scripts/scrape.py dados/posts [arquivo.html ...]   (um .json por dia)
(com arquivos .html, usa eles no lugar da internet — serve pra testar)
"""
import json, re, sys, os, glob, html, time, datetime as dt, urllib.request

CANAL = 'grape_tec'
BRT = dt.timezone(dt.timedelta(hours=-3))
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def baixa(before=None):
    url = f'https://t.me/s/{CANAL}' + (f'?before={before}' if before else '')
    for tent in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'pt-BR'})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            print('erro', url, e)
            time.sleep(3 + tent * 5)
    return ''


def texto(h):
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'<[^>]+>', '', h)
    return html.unescape(h).strip()


def le_pagina(h):
    posts = []
    for bloco in h.split('tgme_widget_message_wrap js-widget_message_wrap')[1:]:
        m = re.search(r'data-post="%s/(\d+)"' % CANAL, bloco)
        t = re.search(r'<time datetime="([^"]+)"', bloco)
        if not m or not t:
            continue
        quando = dt.datetime.fromisoformat(t.group(1)).astimezone(BRT).strftime('%Y-%m-%dT%H:%M:%S')
        tx = re.search(r'js-message_text"[^>]*>(.*?)</div>\s*(?:<div class="tgme_widget_message_footer|<div class="tgme_widget_message_reactions)', bloco, re.S)
        foto = re.search(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)", bloco)
        posts.append(dict(id=m.group(1), type='message', date=quando,
                          text=texto(tx.group(1)) if tx else '', photo=foto.group(1) if foto else ''))
    return posts


def main():
    pasta = sys.argv[1]
    antes = {}
    por_id = {}
    for f in glob.glob(os.path.join(pasta, '*.json')):
        s = open(f, encoding='utf-8').read()
        antes[os.path.basename(f)[:-5]] = s
        for m in json.loads(s)['messages']:
            por_id[m['id']] = m
    ultimo = max(int(i) for i in por_id)
    agora = dt.datetime.now(BRT)
    ontem = (agora - dt.timedelta(days=1)).strftime('%Y-%m-%d')
    novos = 0
    arquivos = sys.argv[2:]
    before = None
    for pag in range(80):
        if arquivos:
            if pag >= len(arquivos):
                break
            h = open(arquivos[pag], encoding='utf-8').read()
        else:
            h = baixa(before)
        ps = le_pagina(h)
        if not ps:
            print('página vazia, parando')
            break
        for p in ps:
            velho = por_id.get(p['id'])
            if velho is None:
                novos += 1
                por_id[p['id']] = p
            else:
                # atualiza foto (link da foto muda) e texto editado
                if p['photo']:
                    velho['photo'] = p['photo']
                else:
                    velho.setdefault('photo', '')
                if p['text']:
                    velho['text'] = p['text']
        menor = min(ps, key=lambda p: int(p['id']))
        before = menor['id']
        # para quando já chegou no que a gente tinha E não falta foto de ontem/hoje mais pra trás
        falta_foto = any('photo' not in m for m in por_id.values()
                         if m['date'][:10] >= ontem and int(m['id']) < int(menor['id']))
        if int(menor['id']) <= ultimo and (menor['date'][:10] < ontem or not falta_foto):
            break
        if not arquivos:
            time.sleep(0.7)
    L = sorted(por_id.values(), key=lambda m: int(m['id']))
    dias = {}
    for m in L:
        dias.setdefault(m['date'][:10], []).append(m)
    for d, ms in dias.items():
        s = json.dumps({'messages': ms}, ensure_ascii=False, separators=(',', ':'))
        if antes.get(d) != s:
            open(os.path.join(pasta, d + '.json'), 'w', encoding='utf-8').write(s)
            print('gravou', d)
    print(f'posts novos: {novos} · total {len(L)} · último {L[-1]["id"]} {L[-1]["date"]}')


if __name__ == '__main__':
    main()
