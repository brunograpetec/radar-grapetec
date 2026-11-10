"""Lê os comentários dos posts que estão nos Achados e marca oferta que a galera avisou que acabou.

Regra:
- ADM (ADM da GRAPE / Bruno) comentando esgotou/expirou/acabou  -> sai na hora
- 2 pessoas diferentes dizendo que não funciona/esgotou/subiu    -> sai ("galera avisou")
- 1 pessoa                                                       -> fica, com aviso
Uso: python3 scripts/comentarios.py site_data.json dados/comentarios.json
"""
import json, re, sys, html, time, datetime as dt, urllib.request, os

BRT = dt.timezone(dt.timedelta(hours=-3))
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
ADM = {'grape_tec_oficial'}
BOT = {'brunoandre_bot'}
ADM_NOMES = {'adm da grape'}
ROBO = re.compile(r'tá bombando de ofertas|ta bombando de ofertas|enviou um link para o grupo', re.I)
RUIM = re.compile(r'esgot|expir|acabou|encerr|n[aã]o (?:t[aá] |est[aá] |esta )?(?:funcion|pegando|pegou|aplic|indo|vai|valendo|vale mais|entra)|'
                  r'\bn (?:funciona|pega|foi)|nao foi|não foi|inv[aá]lid|cupom (?:n[aã]o|ja era|já era)|j[aá] era|'
                  r'voltou (?:o |pro |ao )?pre[cç]o|j[aá] subiu|subiu (?:o pre[cç]o|pra)|indispon|sem estoque|fora de estoque', re.I)
NAO = re.compile(r'precisa (?:do|de) cart|s[oó] (?:no|com) cart|primeira compra|n[aã]o (?:sei|entendi)|\?$', re.I)


def baixa(post):
    url = f'https://t.me/grape_tec/{post}?embed=1&discussion=1&comments_limit=100'
    for t in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            print('erro', post, e); time.sleep(2 + 3 * t)
    return None


def texto(h):
    h = re.sub(r'<br\s*/?>', '\n', h); h = re.sub(r'<[^>]+>', '', h)
    return html.unescape(h).strip()


def comentarios(h):
    out = []
    for b in h.split('tgme_widget_message_wrap js-widget_message_wrap')[1:]:
        a = re.search(r'<a class="tgme_widget_message_author_name" href="https://t.me/([^"]+)"[^>]*>\s*<span[^>]*>([^<]*)</span>', b)
        a2 = re.search(r'tgme_widget_message_author_name"[^>]*>(?:<span[^>]*>)?([^<]*)<', b)
        tx = re.search(r'<div class="tgme_widget_message_text js-message_text"[^>]*>(.*?)</div>\s*<div class="tgme_widget_message_footer', b, re.S)
        tm = re.search(r'<time datetime="([^"]+)"', b)
        if not tx or not tm:
            continue
        user = (a.group(1) if a else '').lower()
        nome = html.unescape(a.group(2) if a else (a2.group(1) if a2 else '')).strip()
        quando = dt.datetime.fromisoformat(tm.group(1)).astimezone(BRT)
        out.append(dict(user=user or nome.lower(), nome=nome, t=texto(tx.group(1)), h=quando.strftime('%H:%M'), d=quando.strftime('%Y-%m-%d')))
    return out


def avalia(cs):
    adm, gente = None, {}
    for c in cs:
        if c['user'] in BOT or ROBO.search(c['t']) or not RUIM.search(c['t']) or NAO.search(c['t'].strip()):
            continue
        if c['user'] in ADM or c['nome'].lower() in ADM_NOMES:
            adm = adm or c['h']
        else:
            gente.setdefault(c['user'], c['h'])
    if adm:
        return dict(esg=adm, src='adm')
    if len(gente) >= 2:
        return dict(esg=sorted(gente.values())[1], src='galera', n=len(gente))
    if len(gente) == 1:
        return dict(av=1)
    return {}


def main():
    sd, arq = sys.argv[1], sys.argv[2]
    marcas = json.load(open(arq)) if os.path.exists(arq) else {}
    try:
        d = json.load(open(sd))
    except Exception:
        return
    hoje = dt.datetime.now(BRT).strftime('%Y-%m-%d')
    posts = []
    for dia, v in (d.get('dias') or {}).items():
        if dia != hoje:
            continue
        for x in v.get('items', []):
            if x.get('esg') and x.get('esgsrc') != 'galera' and x.get('esgsrc') != 'adm':
                continue  # já esgotado pelo aviso do canal
            posts.append(str(x['post']))
    agora = time.time()
    feitos = 0
    falhas = 0
    limite = agora + 120
    for p in dict.fromkeys(posts):
        if falhas >= 3 or time.time() > limite:
            break
        m = marcas.get(p, {})
        if m.get('src') == 'adm' or agora - m.get('_t', 0) < 540:
            continue
        h = baixa(p)
        if h is None:
            falhas += 1
            continue
        r = avalia(comentarios(h)); r['_t'] = agora
        marcas[p] = r; feitos += 1
        time.sleep(0.4)
    json.dump(marcas, open(arq, 'w'), ensure_ascii=False, indent=0)
    print(f'comentários: {feitos} posts lidos · esgotados pela galera/adm: {sum(1 for v in marcas.values() if v.get("esg"))} · com 1 aviso: {sum(1 for v in marcas.values() if v.get("av"))}')


if __name__ == '__main__':
    main()
