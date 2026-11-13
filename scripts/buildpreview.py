"""Gera uma página única (pra prévia) com os dados embutidos. Uso: python3 scripts/buildpreview.py pcideal_data.json saida.html"""
import json, sys
t = open('scripts/pcideal_template.html').read()
fr = json.load(open('scripts/frases.json')); fr.pop('_leia', None)
t = t.replace('/*FRASES*/{}', json.dumps(fr, ensure_ascii=False)).replace('/*DATA*/null', open(sys.argv[1]).read())
open(sys.argv[2], 'w').write(t)
