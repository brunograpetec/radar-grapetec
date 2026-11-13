"""Renova os links de foto dos posts que estão nos Achados (o link do Telegram expira).
Uso: python3 scripts/fotos.py site_data.json dados/fotos.json"""
import json, re, sys, os, time, urllib.request
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
VALIDADE = 4 * 3600


def main():
    sd, arq = sys.argv[1], sys.argv[2]
    F = json.load(open(arq)) if os.path.exists(arq) else {}
    try:
        d = json.load(open(sd))
    except Exception:
        return
    posts = [str(x['post']) for v in (d.get('dias') or {}).values() for x in v.get('items', [])]
    agora = time.time(); fim = agora + 100; feitos = falhas = 0
    for p in sorted(dict.fromkeys(posts), key=lambda p: F.get(p, [None, 0])[1]):
        if agora - F.get(p, [None, 0])[1] < VALIDADE: continue
        if time.time() > fim or falhas >= 3: break
        try:
            req = urllib.request.Request(f'https://t.me/grape_tec/{p}?embed=1', headers={'User-Agent': UA})
            h = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', 'replace')
        except Exception as e:
            falhas += 1; print('erro', p, e); continue
        m = re.search(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)", h)
        F[p] = [m.group(1) if m else '', time.time()]; feitos += 1
        time.sleep(0.3)
    json.dump(F, open(arq, 'w'))
    print(f'fotos renovadas: {feitos}')


if __name__ == '__main__':
    main()
