"""Gera o código do PC Ideal pra colar num bloco HTML personalizado do WordPress.
Uso: python3 scripts/buildpci.py pcideal_data.json saida.html [preview.html]"""
import base64, json, sys
t = open('scripts/pcideal_template.html').read()
d = open(sys.argv[1]).read()
style = t.split('<style>', 1)[1].split('</style>', 1)[0]
markup = t.split('<div id="pci">', 1)[1].split('<script>', 1)[0].rsplit('</div>', 1)[0]
script = t.split('<script>', 1)[1].split('</script>', 1)[0].replace('/*DATA*/null', '(window.__PCISNAP)')
style = style.replace('#pci{--bg', '#pci{max-width:none!important;width:100vw!important;margin-left:calc(50% - 50vw)!important;margin-right:0!important;padding:0!important;--bg', 1)
boot = ("(function(){var h=document.head;if(!document.getElementById('gtFonts')){var l=document.createElement('link');l.id='gtFonts';l.rel='stylesheet';"
 "l.href='https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700;800&display=swap';h.appendChild(l)}"
 "var s=document.createElement('style');s.textContent=" + json.dumps(style) + ";h.appendChild(s);"
 "var r=document.getElementById('pci');r.innerHTML=" + json.dumps(markup) + ";function fit(){var sb=window.innerWidth-document.documentElement.clientWidth;r.style.setProperty('width','calc(100vw - '+sb+'px)','important');r.style.setProperty('margin-left','0','important');var x=r.getBoundingClientRect().left;r.style.setProperty('margin-left',(-x)+'px','important')}fit();window.addEventListener('resize',fit);})();\n")
full = (boot + "window.__PCISNAP=" + d + ";"
 "(function(){var go=function(){if(go.d)return;go.d=1;(0,eval)(window.__pciMain)};window.__pciMain=" + json.dumps(script) + ";var t=setTimeout(go,3500);"
 "try{var q='?v='+Math.floor(Date.now()/6e4);var g=function(u){return fetch(u+q,{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null})};"
 "Promise.all([g('https://cdn.jsdelivr.net/gh/brunograpetec/radar-grapetec@main/pcideal_data.json'),g('https://raw.githubusercontent.com/brunograpetec/radar-grapetec/main/pcideal_data.json')])"
 ".then(function(a){var b=a.concat([window.__PCISNAP]).filter(function(j){return j&&j.parts&&j.parts.cpu}).sort(function(x,y){return (y.ts||0)-(x.ts||0)})[0];if(b)window.__PCIDATA=b}).then(function(){clearTimeout(t);go()})}catch(e){go()}})();")
b64 = base64.b64encode(full.encode('utf-8')).decode()
snip = ('<!-- PC IDEAL GRAPE TEC: cole este bloco inteiro num bloco HTML personalizado --><div id="pci"></div>'
 '<script type="text/plain" id="pcisrc">' + b64 + '</script>'
 '<script>eval(decodeURIComponent(escape(atob(document.getElementById(String.fromCharCode(112,99,105,115,114,99)).textContent.trim()))))</script>')
assert '&' not in snip and '\n' not in snip
open(sys.argv[2], 'w').write(snip)
if len(sys.argv) > 3:
    open(sys.argv[3], 'w').write('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#eee}.is-layout-constrained>*{max-width:600px;margin-left:auto!important;margin-right:auto!important}</style></head><body><header style="padding:30px">GRAPETEC.COM.BR</header><div class="entry-content is-layout-constrained"><p>' + snip + '</p></div></body></html>')
print(len(snip), 'bytes')
