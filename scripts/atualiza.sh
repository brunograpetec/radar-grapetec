#!/usr/bin/env bash
# Atualiza o site_data.json: lê o canal, recalcula tudo e grava na raiz do repo.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/scrape.py dados/posts "$@"
mkdir -p work && cd work
node --max-old-space-size=3000 ../scripts/classify.js 2026-10-01 2026-12-31 ../dados/posts/*.json
python3 ../scripts/clean_extra.py
mkdir -p base; export OUT=base POSTS=../dados/posts
python3 ../scripts/base.py
python3 ../scripts/dias.py
eval "$(python3 - <<'P'
import json,datetime as dt
import glob
m=[x for f in glob.glob('../dados/posts/*.json') for x in json.load(open(f))['messages']]
u=max(m,key=lambda x:int(x['id']))['date']
d=dt.datetime.fromisoformat(u)
print(f"export UPD='{d:%d/%m/%Y} às {d:%H}h{d:%M}' ATE='{d:%d/%m} às {d:%H}h{d:%M}' TOTAL={sum(1 for x in m if x['date']>='2026-10-01')}")
P
)"
python3 ../scripts/sitedata.py
cp site_data.json ../site_data.json
echo "ok: $UPD"
