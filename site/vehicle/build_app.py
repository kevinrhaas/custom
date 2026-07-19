import json

import os
BASE = os.path.dirname(os.path.abspath(__file__))
TOKENS = open(os.path.join(BASE,'vendor/polecat-shell/tokens.css')).read()
SHELL  = open(os.path.join(BASE,'vendor/polecat-shell/shell.css')).read()
DATA   = json.load(open(os.path.join(BASE,'vehicles.json')))

SWATCH = {
  "Red Carpet Metallic Tinted Clearcoat":"linear-gradient(135deg,#a11f2c,#6f1420)",
  "Harbor Gray Metallic Clearcoat":"linear-gradient(135deg,#7d828a,#565b63)",
  "White Metallic":"linear-gradient(135deg,#f2f3f5,#d5d9de)",
}
INT_SWATCH = {
  "Light Smoked Truffle":"#cbb89d",
  "Ebony":"#1c1c20",
  "Ebony / Medium Smoked Truffle":"linear-gradient(135deg,#9c8c73 50%,#1c1c20 50%)",
  "Medium Smoked Truffle":"#9c8c73",
}

app_css = r"""
/* ---- Corsair Finder app styles (built on Polecat tokens) ---- */
html,body.ps-shell{height:auto}
body.ps-shell{display:block;overflow-x:hidden;overflow-y:auto}
.wrap{max-width:1220px;margin:0 auto;padding:0 20px 80px}
.topbar{position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:14px 22px;background:color-mix(in srgb,var(--surface) 82%,transparent);
  backdrop-filter:blur(14px);border-bottom:1px solid var(--border)}
.brandmark{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;color:#fff;
  background:linear-gradient(135deg,var(--brand),var(--accent));box-shadow:var(--shadow-sm);flex:none;font-weight:800}
.brandtxt b{font-size:16px;font-family:var(--font-display);letter-spacing:-.01em;display:block;line-height:1.1}
.brandtxt small{color:var(--text-2);font-size:12px}
.hero{padding:34px 0 8px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-2)}
.hero h1{font-size:clamp(26px,4vw,40px);line-height:1.08;margin:8px 0 10px;letter-spacing:-.02em}
.hero p.lead{color:var(--text-2);font-size:15.5px;max-width:70ch;margin:0}
.spec-strip{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 4px}
.callout{margin:22px 0 6px;border:1px solid var(--border);border-left:4px solid var(--brand);
  background:color-mix(in srgb,var(--brand) 7%,var(--surface));border-radius:var(--radius);padding:16px 18px}
.callout h3{font-size:14px;margin:0 0 6px;display:flex;align-items:center;gap:8px}
.callout p{margin:0 0 6px;color:var(--text-2);font-size:13.5px;line-height:1.6}
.callout p:last-child{margin-bottom:0}
.callout b{color:var(--text)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0 6px}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:15px 16px}
.stat .n{font-size:26px;font-weight:800;letter-spacing:-.02em;font-family:var(--font-display)}
.stat .l{color:var(--text-2);font-size:12px;margin-top:2px}
.controls{position:sticky;top:69px;z-index:30;display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  margin:26px 0 18px;padding:12px;background:color-mix(in srgb,var(--surface) 88%,transparent);
  backdrop-filter:blur(10px);border:1px solid var(--border);border-radius:var(--radius)}
.controls .search{flex:1;min-width:200px}
.controls .grp{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.controls .lbl{font-size:11px;color:var(--text-3);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-right:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;
  display:flex;flex-direction:column;transition:transform .12s,box-shadow .15s,border-color .15s}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:color-mix(in srgb,var(--brand) 35%,var(--border))}
.card.top{border-color:color-mix(in srgb,var(--success) 55%,var(--border));box-shadow:0 0 0 1px color-mix(in srgb,var(--success) 30%,transparent)}
.swatchbar{height:8px;width:100%}
.card-h{display:flex;gap:12px;align-items:flex-start;padding:16px 18px 8px}
.rankbadge{width:34px;height:34px;border-radius:10px;flex:none;display:grid;place-items:center;font-weight:800;font-size:14px;
  background:var(--surface-3);color:var(--text-2);font-family:var(--mono)}
.card.top .rankbadge{background:linear-gradient(135deg,var(--success),#059669);color:#fff}
.card-h .ht{flex:1;min-width:0}
.card-h .ht .tier{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.tier-confirmed{color:var(--success)} .tier-fallback{color:var(--warning)} .tier-lead{color:var(--info)}
.card-h .ht h2{font-size:17px;margin:3px 0 2px;letter-spacing:-.01em}
.card-h .ht .dealer{font-size:13px;color:var(--text-2)}
.dist{flex:none;text-align:right}
.dist .d{font-size:18px;font-weight:800;font-family:var(--font-display);line-height:1}
.dist .u{font-size:10.5px;color:var(--text-3);text-transform:uppercase;letter-spacing:.05em}
.reasons{display:flex;flex-wrap:wrap;gap:6px;padding:6px 18px 4px}
.rz{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:999px;border:1px solid var(--border)}
.rz.ok{color:var(--success);border-color:color-mix(in srgb,var(--success) 45%,var(--border));background:color-mix(in srgb,var(--success) 10%,transparent)}
.rz.mid{color:var(--warning);border-color:color-mix(in srgb,var(--warning) 45%,var(--border));background:color-mix(in srgb,var(--warning) 10%,transparent)}
.rz.no{color:var(--danger);border-color:color-mix(in srgb,var(--danger) 40%,var(--border));background:color-mix(in srgb,var(--danger) 9%,transparent)}
.rz.unk{color:var(--text-2)}
.specs{padding:10px 18px 4px;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:13px}
.specs dt{color:var(--text-3);font-weight:600}
.specs dd{margin:0;color:var(--text)}
.sw{display:inline-block;width:13px;height:13px;border-radius:4px;vertical-align:-2px;margin-right:6px;border:1px solid rgba(255,255,255,.18)}
.vin{font-family:var(--mono);font-size:12px;color:var(--text-2)}
details.opts{padding:6px 18px 2px}
details.opts summary{cursor:pointer;font-size:12.5px;color:var(--brand-2);font-weight:600;list-style:none}
details.opts summary::-webkit-details-marker{display:none}
details.opts ul{margin:8px 0 2px;padding-left:18px;color:var(--text-2);font-size:12.5px;line-height:1.7}
.note{margin:8px 18px 2px;padding:10px 12px;background:var(--surface-2);border-radius:var(--radius-sm);font-size:12.5px;color:var(--text-2);line-height:1.55}
.card-f{margin-top:auto;display:flex;gap:8px;padding:14px 18px 18px;flex-wrap:wrap}
.card-f .btn{flex:1;min-width:104px}
.empty{text-align:center;color:var(--text-2);padding:60px 20px}
.footer{margin-top:40px;padding-top:22px;border-top:1px solid var(--border);color:var(--text-3);font-size:12.5px;line-height:1.7}
.footer b{color:var(--text-2)}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin:6px 0 2px;font-size:12px;color:var(--text-2)}
@media (max-width:560px){ .grid{grid-template-columns:1fr} .controls{top:63px} }
"""

def rz(v):
    out=[]
    # exterior
    if v.get("ext_ok")==True: out.append(('ok','● Red Carpet ✓'))
    elif v.get("ext_ok")=="unknown": out.append(('unk','● Color: confirm'))
    else: out.append(('no','● Not red'))
    # interior
    io=v.get("interior_ok")
    if io=="top": out.append(('ok','◧ Light Truffle ✓'))
    elif io=="backup": out.append(('mid','◧ Backup interior'))
    elif io=="unknown": out.append(('unk','◧ Interior: confirm'))
    # trim
    if v["trim"].startswith("Reserve") and "Premiere" not in v["trim"]: out.append(('ok','◆ Reserve'))
    elif v["trim"]=="Premiere": out.append(('mid','◆ Premiere'))
    else: out.append(('unk','◆ '+v["trim"]))
    # drivetrain
    d=v.get("drivetrain_ok")
    if d==True: out.append(('ok','⛓ AWD ✓'))
    elif d==False: out.append(('mid','⛓ FWD'))
    else: out.append(('unk','⛓ AWD/FWD'))
    # pano
    if isinstance(v.get("pano"),str) and v["pano"].lower().startswith("yes"): out.append(('ok','☀ Pano roof'))
    return out

tier_class={"Confirmed match":"tier-confirmed"}
def tier_cls(t):
    if t.startswith("Confirmed"):return "tier-confirmed"
    if t.startswith("Nearby"):return "tier-fallback"
    return "tier-lead"

cards=[]
for v in DATA["vehicles"]:
    extbg=SWATCH.get(v["ext"],"linear-gradient(135deg,var(--surface-3),var(--surface-2))")
    extsw=SWATCH.get(v["ext"],"var(--surface-3)")
    intsw=INT_SWATCH.get(v["interior"],"var(--surface-3)")
    reasons="".join(f'<span class="rz {c}">{t}</span>' for c,t in rz(v))
    opts="".join(f"<li>{o}</li>" for o in v["options"])
    url2 = f'<a class="btn sm ghost" href="{v["url2"]}" target="_blank" rel="noopener">Dealer</a>' if v.get("url2") else ""
    phone_btn = f'<a class="btn sm" href="tel:{v["phone"].replace(" ","").replace("(","").replace(")","").replace("-","")}">📞 {v["phone"]}</a>' if v.get("phone") else ""
    dir_q = f'{v["dealer"]} {v["city"]} {v["state"]}'.replace(" ","+")
    top = " top" if v["rank"]==1 else ""
    cards.append(f'''
<article class="card{top}" data-trim="{v['trim']}" data-red="{1 if v.get('ext_ok')==True else 0}"
   data-lightint="{1 if v.get('interior_ok')=='top' else 0}" data-awd="{1 if v.get('drivetrain_ok')==True else 0}"
   data-tier="{v['tier']}" data-dist="{v['distance_mi']}" data-rank="{v['rank']}"
   data-price="{v.get('price','')}" data-search="{(v['dealer']+' '+v['city']+' '+v['state']+' '+v['ext']+' '+v['interior']+' '+v['vin']+' '+v['trim']).lower()}">
  <div class="swatchbar" style="background:{extbg}"></div>
  <div class="card-h">
    <div class="rankbadge">{v['rank']}</div>
    <div class="ht">
      <div class="tier {tier_cls(v['tier'])}">{v['tier']}</div>
      <h2>{v['year']} Corsair {v['trim']}</h2>
      <div class="dealer">{v['dealer']} · {v['city']}, {v['state']}</div>
    </div>
    <div class="dist"><div class="d">{v['distance_mi']}</div><div class="u">mi approx</div></div>
  </div>
  <div class="reasons">{reasons}</div>
  <dl class="specs">
    <dt>Exterior</dt><dd><span class="sw" style="background:{extsw}"></span>{v['ext']}</dd>
    <dt>Interior</dt><dd><span class="sw" style="background:{intsw}"></span>{v['interior']}</dd>
    <dt>Seats</dt><dd>{v['seat_material']}</dd>
    <dt>Drive</dt><dd>{v['drivetrain']}</dd>
    <dt>Pano roof</dt><dd>{v['pano']}</dd>
    <dt>Condition</dt><dd>{v['condition']}</dd>
    <dt>Price</dt><dd><b>{v['price']}</b></dd>
    <dt>VIN</dt><dd class="vin">{v['vin']}</dd>
  </dl>
  <details class="opts"><summary>Options &amp; packages ▾</summary><ul>{opts}</ul></details>
  <div class="note">{v['note']}</div>
  <div class="card-f">
    <a class="btn sm primary" href="{v['url']}" target="_blank" rel="noopener">View listing ↗</a>
    {phone_btn}{url2}
    <a class="btn sm ghost" href="https://www.google.com/maps/dir/Crystal+Lake,+IL/{dir_q}" target="_blank" rel="noopener">Directions</a>
  </div>
</article>''')

confirmed=sum(1 for v in DATA["vehicles"] if v["tier"].startswith("Confirmed"))
redcount=sum(1 for v in DATA["vehicles"] if v.get("ext_ok")==True)
nearby=sum(1 for v in DATA["vehicles"] if v["distance_mi"]<=100)
closest=min(v["distance_mi"] for v in DATA["vehicles"])

html=f'''<!doctype html>
<html lang="en" data-palette="polecat" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Corsair Finder — 2026 Lincoln Corsair search for Pat</title>
<meta name="description" content="A curated, verified search for a 2026 Lincoln Corsair in Red Carpet Metallic with a light interior, near Crystal Lake, IL.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%23a11f2c'/%3E%3Ctext x='50' y='68' font-size='58' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'%3EC%3C/text%3E%3C/svg%3E">
<script>
(function(){{try{{var t=localStorage.getItem('corsair.theme')||'polecat:dark';var p=t.split(':');
document.documentElement.setAttribute('data-palette',p[0]);
document.documentElement.setAttribute('data-theme',p[1]==='system'?'dark':p[1]);}}catch(e){{}}}})();
</script>
<style>{TOKENS}</style>
<style>{SHELL}</style>
<style>{app_css}</style>
</head>
<body class="ps-shell">
<div class="topbar">
  <div class="brandmark">C</div>
  <div class="brandtxt"><b>Corsair Finder</b><small>2026 Lincoln Corsair · curated for Pat</small></div>
  <div class="sp"></div>
  <select class="input" id="palette" style="width:auto" title="Palette">
    <option value="polecat">Polecat</option><option value="aurora">Aurora</option><option value="neon">Neon</option>
  </select>
  <button class="btn icon" id="theme" title="Toggle light / dark">◐</button>
</div>

<div class="wrap">
  <section class="hero">
    <div class="eyebrow">Nationwide Lincoln search · {DATA["generated"]}</div>
    <h1>The 2026 Corsair, narrowed to the ones worth a call.</h1>
    <p class="lead">Priorities, in order: <b>Red Carpet Metallic</b> exterior and a <b>light interior</b> (Light Smoked Truffle ideal; light faux-leather is fine), <b>Reserve or Premiere</b> trim, <b>AWD</b> preferred, new or essentially new. Grand Touring (PHEV) excluded. Distances are approximate road miles from Crystal Lake, IL 60014.</p>
    <div class="spec-strip">
      <span class="pill on"><span class="sw" style="background:#a11f2c"></span>Red Carpet Metallic</span>
      <span class="pill"><span class="sw" style="background:#cbb89d"></span>Light Smoked Truffle</span>
      <span class="pill">Reserve / Premiere</span>
      <span class="pill">AWD preferred</span>
      <span class="pill">Panoramic Vista Roof</span>
      <span class="pill">New / lightly used</span>
    </div>

    <div class="callout">
      <h3>⚑ The honest read</h3>
      <p>As of {DATA["generated"]}, <b>no single car in national inventory hits every top preference at once</b> (Red Carpet + Reserve + AWD + a <i>light</i> Truffle leather interior). The search comes down to one real trade-off:</p>
      <p><b>#1 — Wickstrom, Barrington (~14 mi):</b> Red Carpet Metallic + <b>Light Smoked Truffle</b> + AWD + panoramic roof, 1,909 miles, $45,900 — nails both top priorities and it's 15 minutes away. Catch: it's <b>Premiere</b>, so the light seats are Soft-Touch faux leather (which Pat has said is acceptable in a light color).</p>
      <p><b>#2 — Camelback, Phoenix:</b> the best true <b>Reserve</b> in Red Carpet with genuine <b>leather</b> and AWD — but the interior is <b>Ebony (dark)</b> and it's ~1,800 mi away (shipping).</p>
      <p>Everything below rank 6 is a <b>lead</b>: the dealer stocks Corsairs but hides color online — worth a quick call to ask for Red Carpet Metallic.</p>
    </div>

    <div class="stats">
      <div class="stat"><div class="n">{redcount}</div><div class="l">Confirmed Red Carpet (non-GT)</div></div>
      <div class="stat"><div class="n">{closest} mi</div><div class="l">Closest match (Barrington)</div></div>
      <div class="stat"><div class="n">{nearby}</div><div class="l">Within ~100 miles</div></div>
      <div class="stat"><div class="n">{len(DATA["vehicles"])}</div><div class="l">Cars &amp; leads tracked</div></div>
    </div>
  </section>

  <div class="controls">
    <input class="input search" id="q" placeholder="Search dealer, city, VIN, color…">
    <div class="grp"><span class="lbl">Only</span>
      <button class="pill" data-f="red">Red Carpet</button>
      <button class="pill" data-f="lightint">Light interior</button>
      <button class="pill" data-f="awd">AWD</button>
      <button class="pill" data-f="reserve">Reserve</button>
      <button class="pill" data-f="near">≤100 mi</button>
    </div>
    <div class="grp"><span class="lbl">Sort</span>
      <select class="input" id="sort" style="width:auto">
        <option value="rank">Best match</option>
        <option value="dist">Distance</option>
      </select>
    </div>
  </div>

  <div class="grid" id="grid">
    {"".join(cards)}
  </div>
  <div class="empty hide" id="empty">No cars match those filters. <a href="#" id="clear">Clear filters</a>.</div>

  <div class="footer">
    <div class="legend">
      <span><span class="rz ok" style="padding:1px 8px">✓</span> meets preference</span>
      <span><span class="rz mid" style="padding:1px 8px">~</span> acceptable backup</span>
      <span><span class="rz no" style="padding:1px 8px">✗</span> misses preference</span>
      <span><span class="rz unk" style="padding:1px 8px">?</span> confirm with dealer</span>
    </div>
    <p style="margin-top:12px"><b>How this was built.</b> A nationwide sweep of Lincoln.com, Cars.com, CarGurus, Autotrader, Edmunds and ~20 individual dealer sites, de-duplicated by VIN. Confirmed cars had their color verified in the listing; “leads” stock Corsairs but don’t publish color, so call to confirm. Many dealer pages render specs via JavaScript, so a few price/interior/roof fields read “call to confirm” rather than a guess — nothing here is invented.</p>
    <p><b>Live inventory moves fast.</b> Cars sell and prices change daily — confirm availability, price, exact interior and options by phone or the listing link before acting. VIN patterns: <span class="vin">5LMCJ2DA…</span> = Reserve AWD · <span class="vin">5LMCJ2CA…</span> = Reserve FWD · <span class="vin">5LMCJ1DA…</span> = Premiere AWD · <span class="vin">5LMCJ1CA…</span> = Premiere FWD.</p>
    <p style="margin-top:10px;color:var(--text-3)">Built on the Polecat platform design system · data snapshot {DATA["generated"]} · origin Crystal Lake, IL 60014</p>
  </div>
</div>

<script>
const grid=document.getElementById('grid'), cards=[...grid.children];
const filters=new Set();
document.querySelectorAll('.pill[data-f]').forEach(b=>b.onclick=()=>{{
  b.classList.toggle('on'); const f=b.dataset.f; filters.has(f)?filters.delete(f):filters.add(f); apply();}});
document.getElementById('q').oninput=apply;
document.getElementById('sort').onchange=apply;
document.getElementById('clear').onclick=e=>{{e.preventDefault();filters.clear();document.querySelectorAll('.pill[data-f]').forEach(b=>b.classList.remove('on'));document.getElementById('q').value='';apply();}};
function apply(){{
  const q=document.getElementById('q').value.trim().toLowerCase();
  const sort=document.getElementById('sort').value;
  let vis=cards.filter(c=>{{
    if(filters.has('red')&&c.dataset.red!=='1')return false;
    if(filters.has('lightint')&&c.dataset.lightint!=='1')return false;
    if(filters.has('awd')&&c.dataset.awd!=='1')return false;
    if(filters.has('reserve')&&!(c.dataset.trim.startsWith('Reserve')&&!c.dataset.trim.includes('Premiere')))return false;
    if(filters.has('near')&&+c.dataset.dist>100)return false;
    if(q&&!c.dataset.search.includes(q))return false;
    return true;}});
  const rest=cards.filter(c=>!vis.includes(c));
  vis.sort((a,b)=> sort==='dist' ? (+a.dataset.dist-+b.dataset.dist) : (+a.dataset.rank-+b.dataset.rank));
  vis.forEach(c=>{{c.classList.remove('hide');grid.appendChild(c);}});
  rest.forEach(c=>c.classList.add('hide'));
  document.getElementById('empty').classList.toggle('hide',vis.length>0);
}}
// theme
const root=document.documentElement;
function save(){{try{{localStorage.setItem('corsair.theme',root.getAttribute('data-palette')+':'+root.getAttribute('data-theme'));}}catch(e){{}}}}
document.getElementById('theme').onclick=()=>{{root.setAttribute('data-theme',root.getAttribute('data-theme')==='dark'?'light':'dark');save();}};
const psel=document.getElementById('palette');psel.value=root.getAttribute('data-palette');
psel.onchange=()=>{{root.setAttribute('data-palette',psel.value);save();}};
apply();
</script>
</body>
</html>'''

open(os.path.join(BASE,'index.html'),'w').write(html)
print("wrote index.html", len(html),"bytes")
