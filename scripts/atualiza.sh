#!/usr/bin/env bash
# Atualiza o site_data.json: lê o canal, recalcula tudo e grava na raiz do repo.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/scrape.py dados/posts "$@"
mkdir -p work && cd work
eval "$(python3 - <<'P'
import glob,os,datetime as dt
L=max(os.path.basename(f)[:10] for f in glob.glob('../dados/posts/*.json'))
L=dt.date.fromisoformat(L)
d0=max(dt.date(2026,10,1),L-dt.timedelta(days=89))
b=L.replace(day=1) if L.day>=7 else (L.replace(day=1)-dt.timedelta(days=1)).replace(day=1)
a=(b-dt.timedelta(days=1)).replace(day=1)
print(f"export D0={d0} MA={a} MB={b} DFIM={L+dt.timedelta(days=1)}")
P
)"
node --max-old-space-size=3000 ../scripts/classify.js $D0 $DFIM ../dados/posts/*.json
python3 ../scripts/clean_extra.py
mkdir -p base; export OUT=base POSTS=../dados/posts
python3 ../scripts/base.py
python3 ../scripts/comentarios.py ../site_data.json ../dados/comentarios.json || true
python3 ../scripts/fotos.py ../site_data.json ../dados/fotos.json || true
export FOTOS=../dados/fotos.json
export MARCAS=../dados/comentarios.json
python3 ../scripts/dias.py
eval "$(python3 - <<'P'
import json,os,datetime as dt
import glob
m=[x for f in glob.glob('../dados/posts/*.json') for x in json.load(open(f))['messages']]
u=max(m,key=lambda x:int(x['id']))['date']
d=dt.datetime.fromisoformat(u)
print(f"export UPD='{d:%d/%m/%Y} às {d:%H}h{d:%M}' ATE='{d:%d/%m} às {d:%H}h{d:%M}' TOTAL={sum(1 for x in m if x['date']>=os.environ['D0'])}")
P
)"
python3 ../scripts/sitedata.py
SITE=site_data.json OUT=base POSTS=../dados/posts python3 ../scripts/pcideal.py ../pcideal_data.json || true
cp site_data.json ../site_data.json
echo "ok: $UPD"
