"""Gera o código da HOME do grapetec.com.br pra colar num bloco HTML personalizado do WordPress.
Uso: python3 scripts/buildhome.py home_data.json saida_snippet.txt [preview.html]"""
import base64, json, sys
t = open('scripts/home_template.html').read()
t = t.replace('/*LOGO*/', open('scripts/logo_datauri.txt').read().strip()).replace('/*FOTO*/', open('scripts/foto_bruno_datauri.txt').read().strip())
d = open(sys.argv[1]).read()
if len(sys.argv) > 3:
    open(sys.argv[3], 'w').write(t.replace('/*DATA*/null', d))
style = t.split('<style>', 1)[1].split('</style>', 1)[0]
markup = t.split('<div id="gth">', 1)[1].split('<script>', 1)[0].rsplit('</div>', 1)[0]
script = t.split('<script>', 1)[1].split('</script>', 1)[0].replace('/*DATA*/null', '(window.__GTHSNAP)')
style = style.replace('#gth{--bg', '#gth{max-width:none!important;width:100vw!important;margin-left:calc(50% - 50vw)!important;margin-right:0!important;padding:0!important;--bg', 1)
style += 'body{margin:0!important;background:#0b0710}body.gthc{background:#f6f3f9}'
boot = ("(function(){var h=document.head;if(!document.getElementById('gtFonts')){var l=document.createElement('link');l.id='gtFonts';l.rel='stylesheet';"
 "l.href='https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700;800&display=swap';h.appendChild(l)}"
 "var s=document.createElement('style');s.textContent=" + json.dumps(style) + ";h.appendChild(s);"
 "var r=document.getElementById('gth');r.innerHTML=" + json.dumps(markup) + ";function fit(){var sb=window.innerWidth-document.documentElement.clientWidth;r.style.setProperty('width','calc(100vw - '+sb+'px)','important');r.style.setProperty('margin-left','0','important');var x=r.getBoundingClientRect().left;r.style.setProperty('margin-left',(-x)+'px','important')}fit();window.addEventListener('resize',fit);"
 "new MutationObserver(function(){document.body.classList.toggle('gthc',r.classList.contains('claro'))}).observe(r,{attributes:true});})();\n")
full = (boot + "window.__GTHSNAP=" + d + ";"
 "(function(){var go=function(){if(go.d)return;go.d=1;(0,eval)(window.__gthMain)};window.__gthMain=" + json.dumps(script) + ";var t=setTimeout(go,3000);"
 "try{var q='?v='+Math.floor(Date.now()/6e4);var g=function(u){return fetch(u+q,{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null})};"
 "Promise.all([g('https://raw.githubusercontent.com/brunograpetec/radar-grapetec/main/home_data.json'),g('https://cdn.jsdelivr.net/gh/brunograpetec/radar-grapetec@main/home_data.json')])"
 ".then(function(a){var b=a.concat([window.__GTHSNAP]).filter(function(j){return j&&j.ts}).sort(function(x,y){return (y.ts||0)-(x.ts||0)})[0];if(b)window.__GTHDATA=b}).then(function(){clearTimeout(t);go()})}catch(e){go()}})();")
b64 = base64.b64encode(full.encode('utf-8')).decode()
snip = ('<!-- HOME GRAPE TEC: cole este bloco inteiro num bloco HTML personalizado --><div id="gth"></div>'
 '<script type="text/plain" id="gthsrc">' + b64 + '</script>'
 '<script>eval(decodeURIComponent(escape(atob(document.getElementById(String.fromCharCode(103,116,104,115,114,99)).textContent.trim()))))</script>')
assert '&' not in snip and '\n' not in snip
open(sys.argv[2], 'w').write(snip)
print(len(snip), 'bytes')
