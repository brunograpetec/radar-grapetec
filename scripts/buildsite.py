import base64,json,re
t=open('site_template.html').read(); d=open('site_data.json').read()
WA='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.6A8.4 8.4 0 1 1 21 11.5z"/><path d="M9 9.5c.3 1.8 2.6 4.3 4.6 4.8l1.2-1.1 1.7.8"/></svg>'
TG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 3.5 2.8 10.7c-.9.4-.9 1.6.1 1.9l4.7 1.5 1.8 5.6c.3.8 1.3 1 1.9.4l2.6-2.5 4.7 3.5c.7.5 1.7.1 1.9-.7L23 4.9c.2-1-.7-1.8-1.5-1.4z"/><path d="m7.6 14.1 9.9-6.6-7.4 8.2"/></svg>'
_j=json.loads(d);t=t.replace('__OFERTAS__',str(_j['ofertas'])).replace('__NPROD__',str(len(_j['P'])));t=t.replace('__DATA__',d).replace('__WA__',WA).replace('__TG__',TG)
inner=t.split('<div id="gt1111">',1)[1]
markup,rest=inner.split('<script>',1)
script=rest.split('</script>',1)[0]
markup=markup.replace('#gt1111{--bg','#gt1111{max-width:none!important;width:100vw!important;margin-left:calc(50% - 50vw)!important;margin-right:0!important;padding:0!important;--bg',1)
boot=("(function(){var h=document.head;if(!document.getElementById('gtFonts')){var l=document.createElement('link');l.id='gtFonts';l.rel='stylesheet';"
 "l.href='https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700;800&display=swap';h.appendChild(l)}"
 "var r=document.getElementById('gt1111');r.innerHTML="+json.dumps(markup)+";function fit(){var sb=window.innerWidth-document.documentElement.clientWidth;r.style.setProperty('width','calc(100vw - '+sb+'px)','important');r.style.setProperty('margin-left','0','important');var x=r.getBoundingClientRect().left;r.style.setProperty('margin-left',(-x)+'px','important')}fit();window.addEventListener('resize',fit);})();\n")
URL='https://raw.githubusercontent.com/brunograpetec/radar-grapetec/main/site_data.json'
full=boot+"(function(){var go=function(){if(go.d)return;go.d=1;(0,eval)(window.__gtMain)};window.__gtMain="+json.dumps(script)+";var t=setTimeout(go,3500);try{fetch('"+URL+"?v='+Math.floor(Date.now()/6e4),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){if(j&&j.P&&j.P.length)window.__GTDATA=j}).catch(function(){}).then(function(){clearTimeout(t);go()})}catch(e){go()}})();"
b64=base64.b64encode(full.encode('utf-8')).decode()
snippet=('<!-- RADAR 11.11 GRAPE TEC: cole este bloco inteiro num bloco HTML personalizado --><div id="gt1111"></div>'
 '<script type="text/plain" id="gtsrc">'+b64+'</script>'
 '<script>eval(decodeURIComponent(escape(atob(document.getElementById(String.fromCharCode(103,116,115,114,99)).textContent.trim()))))</script>')
assert '&' not in snippet and '\n' not in snippet and '"' not in snippet.split('<script>')[-1]
open('/mnt/user-data/outputs/radar_1111_wordpress.html','w').write(snippet)
page='<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Radar 11.11 · Grape Tec</title><style>html,body{margin:0;background:#130c18}</style></head><body>'+snippet+'</body></html>'
open('preview/index.html','w').write(page)
# simulated WordPress mangling test page: wrap in constrained container + autop-like br
wp='<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#eee}.is-layout-constrained>*{max-width:600px;margin-left:auto!important;margin-right:auto!important}</style></head><body><header style="padding:30px">GRAPETEC.COM.BR</header><div class="entry-content is-layout-constrained"><p>'+snippet+'</p></div></body></html>'
open('preview/wp_test.html','w').write(wp)
print(len(snippet))
