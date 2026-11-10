const fs=require('fs');
const gb=t=>{let m=t.match(/(\d)\s?x\s?(\d{1,2})\s?gb/i);if(m)return m[1]*m[2];m=t.match(/(\d{1,3})\s?gb/i);return m?+m[1]:null};
const W=t=>{const m=t.match(/(\d{3,4})\s?w\b/i);return m?+m[1]:null};
eval(fs.readFileSync(__dirname+'/keys_src.js','utf8').replace('var EX=','global.EX=').replace('var __keys=','global.__keys='));
const st=t=>{const m=t.match(/kabum|amzn|amazon|shopee|mercadoli|meli\.la|aliexpress|pichau|terabyte|magalu|magazineluiza/i);if(!m)return '?';return {kabum:'KaBuM',amzn:'Amazon',amazon:'Amazon',shopee:'Shopee',mercadoli:'Mercado Livre','meli.la':'Mercado Livre',aliexpress:'AliExpress',pichau:'Pichau',terabyte:'Terabyte',magalu:'Magalu',magazineluiza:'Magalu'}[m[0].toLowerCase()]};
const ACC=/\b(capa|pel[ií]cula|case|suporte|carregador|cabo|adaptador|skin|grip|bolsa|mochila|jogo|game card|gift|cart[aã]o|usado|seminovo|vitrine|recondicionado|kit|combo)\b/i;
const R=[
['Mouse',/^\s*mouse(?! ?pad)/i,[[/g305/,'Mouse Logitech G305'],[/king pro/,'Mouse Redragon King Pro'],[/k1ng/,'Mouse Redragon K1NG 1K'],[/g203/,'Mouse Logitech G203'],[/pulsefire haste/,'Mouse HyperX Pulsefire Haste'],[/gm510/,'Mouse AOC GM510']]],
['Teclado',/^\s*teclado/i,[[/dark avenger/,'Teclado Redragon Dark Avenger'],[/pebble keys/,'Teclado Logitech Pebble Keys'],[/sherman/,'Teclado TGT Sherman V3'],[/fizz/,'Teclado Redragon Fizz'],[/shade mk3/,'Teclado Mancer Shade MK3'],[/magn[ée]tico|hall effect/,'Teclado magnético (mais barato)']]],
['Headset',/^\s*(headset|headphone|fone de ouvido gamer|fone gamer|fone)/i,[[/zeus pro/,'Headset Redragon Zeus Pro'],[/zeus lite/,'Headset Redragon Zeus Lite'],[/vega pro/,'Headset Pichau Vega Pro'],[/g335/,'Headset Logitech G335'],[/cragblade/,'Headset Redragon Cragblade'],[/h2002/,'Headset Havit H2002C'],[/h630bt/,'Fone Havit H630BT'],[/p30i/,'Fone Soundcore P30i'],[/p20i/,'Fone Soundcore P20i']]],
['Controle',/^\s*(controle|gamepad|joystick)/i,[[/g7 pro/,'Controle GameSir G7 Pro'],[/tegenaria|gamesir t3/,'Controle GameSir T3'],[/dualshock 4/,'Controle DualShock 4'],[/dualsense(?! edge)/,'Controle DualSense (PS5)'],[/ultimate 2/,'Controle 8BitDo Ultimate 2'],[/xbox/,'Controle Xbox sem fio']]],
['Notebook',/^\s*notebook/i,[[/ideapad slim/,'Notebook Lenovo IdeaPad Slim'],[/vivobook go/,'Notebook Asus Vivobook Go'],[/fe16/,'Notebook VAIO FE16'],[/tuf gaming/,'Notebook Asus TUF Gaming'],[/nitro v ?15|nitro v15/,'Notebook Acer Nitro V15'],[/\bloq\b/,'Notebook Lenovo LOQ']]],
['Console',/^\s*(console|playstation|sony playstation|nintendo switch|xbox series)/i,[[/(playstation 5|ps5) slim/,'PlayStation 5 Slim'],[/(playstation 5|ps5) pro/,'PlayStation 5 Pro'],[/switch lite/,'Nintendo Switch Lite'],[/switch oled|switch.*oled/,'Nintendo Switch OLED'],[/switch 2/,'Nintendo Switch 2']]],
['TV',/^\s*(smart ?tv|tv )/i,null],
['Celular',/^\s*(smartphone|celular|iphone)/i,[[/galaxy a17/,'Celular Samsung Galaxy A17'],[/galaxy a36/,'Celular Samsung Galaxy A36'],[/galaxy a57/,'Celular Samsung Galaxy A57'],[/galaxy s25(?! ultra| edge| fe)/,'Celular Samsung Galaxy S25'],[/moto g35/,'Celular Motorola Moto G35'],[/poco x8/,'Celular Xiaomi Poco X8']]],
['Tablet',/^\s*(tablet|ipad)/i,[[/matepad se/,'Tablet Huawei MatePad SE'],[/idea ?tab/,'Tablet Lenovo Idea Tab'],[/redmi pad/,'Tablet Xiaomi Redmi Pad']]],
['Smartwatch',/^\s*(smartwatch|rel[oó]gio|pulseira)/i,[[/fit3/,'Smartwatch Samsung Galaxy Fit3']]],
['Microfone',/^\s*microfone/i,[[/fifine.*(sfm2|superframe)|superframe.*fifine/,'Microfone Fifine SuperFrame']]],
['Mousepad',/^\s*mouse ?pad/i,[[/apex control/,'Mousepad Apex Control']]]];
function extra(t,T,price,p,out){for(const [cat,re,M] of R){if(!re.test(t))continue;if(ACC.test(T)&&cat!=='Teclado'&&cat!=='Mouse')break;if(/\b(kit|combo)\b/.test(T))break;
  if(cat==='TV'){const s=T.match(/\b(32|40|43|50|55|58|60|65|70|75|85)\s?(?:"|''|pol|polegadas|\b)/);if(s&&(/4k|uhd/.test(T)||+s[1]>=43)){const sz=+s[1];const b=sz<=43?43:sz<=50?50:sz<=55?55:sz<=65?65:null;if(b)out.push([p.id,p.d,`Smart TV ${b}" 4K (mais barata)`,price,st(p.txt),t.slice(0,80).replace(/\|/g,'/')])}break}
  for(const [r,k] of M)if(r.test(T)){out.push([p.id,p.d,k,price,st(p.txt),t.slice(0,80).replace(/\|/g,'/')]);break}break}}
const _a=process.argv.slice(2),_dt=_a.filter(x=>/^\d{4}-\d\d-\d\d$/.test(x)),d0=_dt[0],d1=_dt[1],_fs=_a.filter(x=>!/^\d{4}-\d\d-\d\d$/.test(x)),inF=_fs[0],more=_fs.slice(1);
const J={messages:[]};const seen=new Set();for(const f of [inF,...more]){for(const m of JSON.parse(fs.readFileSync(f,'utf8')).messages){if(seen.has(m.id))continue;seen.add(m.id);J.messages.push(m)}}
const flat=x=>typeof x==='string'?x:Array.isArray(x)?x.map(flat).join(''):(x&&x.text)||'';
const hw=[],ex=[],CU=[],ES=[];let n=0;
for(const m of J.messages){if(m.type!=='message')continue;const d=m.date.slice(0,10);if(d<d0||d>d1)continue;n++;
 const txt=flat(m.text);const es=txt.match(/cupom\s+([A-Z0-9]{4,})\s+esgotad/i)||txt.match(/\b([A-Z0-9]{5,})\b[^\n]{0,20}esgotad/i);if(es)ES.push([m.id,m.date,es[1].toUpperCase()]);const cu=(txt.split('💰')[1]||'').match(/cupom[:\s]*([A-Za-z0-9]{4,})/i);CU.push([m.id,m.date.slice(11,16),cu?cu[1].toUpperCase():'']);const p={id:+m.id,d,txt};const i=txt.indexOf('💰');if(i<0)continue;
 const t=txt.slice(0,i).replace(/[^\p{L}\p{N}\s\-\/\.,+]/gu,' ').replace(/\s+/g,' ').trim();
 const pm=txt.slice(i).match(/R\$\s?([\d\.]+(?:,\d{1,2})?)/);if(!pm)continue;const price=+pm[1].replace(/\./g,'').replace(',','.');if(!price)continue;
 for(const k of __keys(t))hw.push([p.id,d,k,price,st(txt),t.slice(0,80).replace(/\|/g,'/')]);
 extra(t,t.toLowerCase(),price,p,ex)}
const csv=r=>r.map(v=>{v=String(v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v}).join(',');
const H='post_id,data,produto,preco,loja,titulo\n';
fs.writeFileSync('cupons.csv','post_id,hora,cupom\n'+CU.map(csv).join('\n')+'\n');fs.writeFileSync('esgotados.csv','post_id,datahora,cupom\n'+ES.map(csv).join('\n')+'\n');fs.writeFileSync('posts_raw2.csv',H+hw.map(csv).join('\n')+'\n');fs.writeFileSync('posts_extra2.csv',H+ex.map(csv).join('\n')+'\n');
console.log('mensagens no período',n,'hw',hw.length,'extra',ex.length);
