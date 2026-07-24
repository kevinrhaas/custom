#!/usr/bin/env python3
"""Build the shell-based Hosta app (site/hosta/index.html) from v3 + new plates.

Rebuilds the guide as a polecat-shell app: left rail + topbar + one-view-at-a-time.
Extracts v3 content into per-view fragments, builds design + variation data (with
the new photoreal plates), embeds the Lurvey dataset, and emits index.html +
css/guide.css. Hand-written companions: css/app.css, js/app.js.
"""
import re, json, html as H, os

V3 = "hosta_gangway_guide_v3.html"
OUT = "../site/hosta/index.html"
os.makedirs("../site/hosta/css", exist_ok=True)
doc = open(V3, encoding="utf-8").read()
mega = doc.split("\n")[377]
arts = [a for a in re.split(r'(?=<article class="g-garden")', mega) if a.strip()]

CAT = {1:('#1f3a6e','#15284d'),2:('#c8961c','#8c6913'),3:('#7a5aa8','#553e75'),
       4:('#3d6fb5','#2a4d7e'),5:('#1f7a45','#155530'),6:('#63b394','#457d67'),
       7:('#8f9c2b','#646d1e'),8:('#d2691e','#934915'),9:('#74a8de','#51759b'),
       10:('#94a9cf','#677690'),11:('#e0bf2f','#9c8520'),12:('#4f9a56','#376b3c'),
       13:('#b06a8f','#7b4a64')}
CATNAME = {1:'Giant Blue',2:'Giant/Large Gold',3:'Upright / Vase',4:'Large Blue Mound',
       5:'Large Green / Fragrant',6:'Green + White Margin',7:'Gold/Yellow Margin',
       8:'Gold-Centered Two-Tone',9:'Medium Blue Mound',10:'Frosted / Misted',
       11:'Small Gold Accent',12:'Small Green Edger',13:'Miniature / Mouse-Ear'}
def money(v): return f"${v:,.2f}"

# ------------------------------------------------------------------ guide CSS
css = re.search(r'<style>(.*?)</style>', doc, re.S).group(1)
css = css.replace('#guide', '.guide').replace('#ref', '.ref')
open("../site/hosta/css/guide.css", "w", encoding="utf-8").write(css)

# ------------------------------------------------------------------ section fragments
def section_inner(sid):
    m = re.search(r'<section id="%s">(.*?)</section>' % sid, doc, re.S)
    return m.group(1) if m else ''
FR:dict = {}
for sid in ('site','key','compare','corner','works'):
    FR:dict
    FRAG = section_inner(sid)
    FR[sid] = FRAG
# reference: refhead + #ref block (up to its closing, before the guide footer)
refhead = re.search(r'(<div class="refhead">.*?</div>\s*</div>)', doc, re.S)
refblock = re.search(r'(<div id="ref">.*?</div>\s*</div>\s*)(?=<div id="guide"><footer)', doc, re.S)
FR['refhead'] = refhead.group(1) if refhead else ''
FR['refblock'] = (refblock.group(1) if refblock else '').replace('id="ref"','class="ref"')
# render kit
FR['renderkit'] = open("_render_kit.html", encoding="utf-8").read()
FR['renderkit'] = re.sub(r'</?section[^>]*>','',FR['renderkit'])  # strip <section> wrapper

# ------------------------------------------------------------------ per-garden extraction
def garden(a):
    def g1(p, s=a):
        m = re.search(p, s, re.S); return m.group(1) if m else ''
    name = re.sub(r'<[^>]+>','',g1(r'<h3>(.*?)</h3>')).strip()
    tag  = g1(r'<p class="g-tag">(.*?)</p>')
    idea = g1(r'<p class="g-idea">(.*?)</p>')
    # two top-down plan svgs after "Plan ... looking down"
    plan = re.search(r'Plan.{0,30}?looking down.*?</h4>(<p class="g-cap">.*?</p>)((?:<div class="g-svg">.*?</div>){2})', a, re.S)
    plan_html = (plan.group(1)+plan.group(2)) if plan else ''
    why = re.search(r'<h4 class="g-h4">Why this works</h4>(.*?)(?=<h4 class="g-h4">Categories used</h4>)', a, re.S)
    why_html = why.group(1) if why else ''
    cats = re.search(r'<h4 class="g-h4">Categories used</h4>(<div class="g-key">.*?</div>)', a, re.S)
    cats_html = cats.group(1) if cats else ''
    shop = re.search(r'(<table class="g-tbl">.*?</table>)', a, re.S)
    shop_html = shop.group(1) if shop else ''
    fine = re.search(r'(<p class="g-fine">.*?</p>)', a, re.S)
    return dict(name=name, tag=tag, idea=idea, plan=plan_html, why=why_html,
                cats=cats_html, shop=shop_html, fine=fine.group(1) if fine else '')

GARDENS = [garden(a) for a in arts]

def parse_plants(shop_html):
    """Structured [{name, qty}] from a v3 shopping table (ignores summary rows)."""
    out = []
    for tr in re.findall(r'<tr(?![^>]*class=)[^>]*>(.*?)</tr>', shop_html, re.S):
        # the variety link is the external one (href not starting with '#')
        a = re.search(r'<a[^>]*href="(?!#)[^"]*"[^>]*>(.*?)</a>', tr)
        name = H.unescape(re.sub(r'<[^>]+>', '', a.group(1))).strip() if a else ''
        name = re.sub(r'\s*[↗➚]\s*$', '', name).strip()
        qty = ''
        for c in re.findall(r'<td class="r"[^>]*>(.*?)</td>', tr, re.S):
            t = re.sub(r'<[^>]+>', '', c).strip()
            if re.fullmatch(r'\d+', t): qty = t; break
        if name: out.append({'name': name, 'qty': qty})
    return out

# ------------------------------------------------------------------ variations (authored) + plates
def schematic(rows, gradient=False):
    W, Hh = 1140, 232; x0, x1 = 34, 1106; usable = x1 - x0; scale = usable/95.0
    body = [(c,n,s,q) for (c,n,s,q) in rows if c != 13]
    mice = [(c,n,s,q) for (c,n,s,q) in rows if c == 13]
    n_body = sum(q for *_, q in body) or 1; step = usable/(n_body+1)
    p = [f'<svg viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">',
         f'<rect width="{W}" height="{Hh}" fill="#f3efe4"/>',
         f'<rect x="{x0-8}" y="54" width="{usable+16}" height="150" rx="10" fill="#efe7d3" stroke="#d9cdb0"/>']
    z1 = x0 + 11*scale
    p.append(f'<rect x="{x0-8}" y="54" width="{z1-(x0-8)}" height="150" rx="10" fill="#f7edc4" opacity=".5"/>')
    p.append(f'<text x="{(x0+z1)/2:.0f}" y="46" font-size="10.5" font-weight="700" fill="#8a6510" text-anchor="middle" font-family="sans-serif">STREET END · sun</text>')
    p.append(f'<text x="{(z1+x1)/2:.0f}" y="46" font-size="10.5" font-weight="700" fill="#3c4f57" text-anchor="middle" font-family="sans-serif">THE SLOT · deep shade →</text>')
    cx = x0 + step; row = 0
    for c,n,s,q in body:
        fill,stroke = CAT.get(c,('#888','#555')); r = max(9,min(30,s*scale*0.5))
        for _ in range(q):
            cy = 118 + (14 if row%2 else -14)
            p.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="{r:.0f}" fill="{fill}" fill-opacity=".9" stroke="{stroke}" stroke-width="1.2"/>')
            cx += step; row += 1
    for c,n,s,q in mice:
        fill,stroke = CAT.get(c,('#b06a8f','#7b4a64'))
        if q<=0: continue
        ms = usable/(q+1); mx = x0+ms
        for _ in range(q):
            p.append(f'<circle cx="{mx:.0f}" cy="192" r="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'); mx += ms
    p.append('</svg>'); return ''.join(p)

def shop_table(rows):
    trs = []
    for c,n,s,q,each in rows:
        f,st = CAT[c]
        trs.append(f'<tr><td><span class="g-sw" style="background:{f};border-color:{st}"></span> '
            f'<span class="g-cat">{c}. {CATNAME[c]}</span></td><td><b>{H.escape(n)}</b></td>'
            f'<td class="g-dim">{s if s>=1 else "10–12 in"}{" ft" if s>=1 else ""}</td>'
            f'<td class="r">{q}</td><td class="r g-dim">{money(each)}</td><td class="r">{money(q*each)}</td></tr>')
    plants = sum(q for (c,n,s,q,each) in rows); cost = sum(q*each for (c,n,s,q,each) in rows)
    total = cost + 505 + 55
    return (f'<div class="g-tw"><table class="g-tbl"><thead><tr><th>Category</th><th>Variety</th>'
        f'<th>Spread</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Subtotal</th></tr></thead><tbody>'
        + ''.join(trs) +
        f'<tr class="g-sum"><td>Plants — {len(rows)} varieties</td><td></td><td></td><td class="r">{plants}</td><td></td><td class="r">{money(cost)}</td></tr>'
        f'<tr class="g-sub"><td>Site works (every plan)</td><td></td><td></td><td></td><td></td><td class="r">+ {money(505)}</td></tr>'
        f'<tr class="g-sub"><td>Corner climber</td><td></td><td></td><td class="r">1</td><td></td><td class="r">+ {money(55)}</td></tr>'
        f'<tr class="g-grand"><td>Installed, pocket method</td><td></td><td></td><td></td><td></td><td class="r">{money(total)}</td></tr>'
        + '</tbody></table></div>'), plants, cost, total

VARIATIONS = {
 1:[dict(key='g1va',title='Crisp Contrast',kicker='Same idea, bolder whites & more substance',
     changes='The white-margin ribbon becomes <b>Patriot</b> — wider, brighter, thicker-leaved, reads bolder down the walk (and needs a few fewer at 3.5 ft). Blue anchor and mouse-ear edge unchanged.',
     rows=[(4,'Abiqua Drinking Gourd',3,14,9.99),(6,'Patriot',3.5,12,11.99),(13,'Blue Mouse Ears',1,27,8.99)]),
    dict(key='g1vb',title='Moonlit Edge',kicker='Same body, a two-tone sparkle at the sunny end',
     changes='The all-blue mouse-ear ribbon splits into <b>Blue Mouse Ears</b> through the slot plus a warm run of <b>Sun Mouse</b> where the street end catches light — a low gold shimmer where the sun can colour it.',
     rows=[(4,'Abiqua Drinking Gourd',3,14,9.99),(6,'Francee',3,13,11.99),(13,'Blue Mouse Ears',1,18,8.99),(13,'Sun Mouse',0.83,9,9.99)])],
 2:[dict(key='g2va',title='Brighter Street End',kicker='Livelier gold in the sun, deeper blue in the slot',grad=True,
     changes='Swaps flat <b>August Moon</b> for ruffled, brighter <b>Dancing Queen</b> at the street end and leans the slot bluer with more <b>Halcyon</b>. Same street→shade logic, higher contrast.',
     rows=[(2,'Dancing Queen',3,7,14.99),(9,'Halcyon',3,8,11.99),(6,'Patriot',3.5,7,11.99),(4,'Abiqua Drinking Gourd',3,6,9.99),(13,'Blue Mouse Ears',1,21,8.99)]),
    dict(key='g2vb',title='Gold-Center Transition',kicker='A richer light-to-shade fade with two-tone leaves',grad=True,
     changes='Replaces flat gold with gold-<i>centered</i> <b>Stained Glass</b> (most sun-tolerant, fragrant) at the street, fading through frosted <b>First Frost</b> into blue <b>Halcyon</b> — the gradient lives inside the leaves now.',
     rows=[(8,'Stained Glass',3,5,16.99),(10,'First Frost',2.5,8,14.99),(9,'Halcyon',3,7,11.99),(6,'Patriot',3.5,6,11.99),(13,'Blue Mouse Ears',1,21,8.99)])],
 6:[dict(key='g6va',title='Vase-Forward',kicker='More upright architecture + a fragrant white show',
     changes='Trades <b>Brother Stefan</b> for fragrant, white-blushed <b>Royal Wedding</b> so the run earns an August flower show, keeping the <b>Regal Splendor</b> vases that make a narrow bed feel taller.',
     rows=[(3,'Regal Splendor',4,9,14.99),(5,'Royal Wedding',3.5,9,18.99),(8,'June',2.5,12,14.99),(10,'First Frost',2.5,9,14.99),(13,'Blue Mouse Ears',1,12,8.99)]),
    dict(key='g6vb',title='Two-Tone Bright',kicker='Gold-centered brightness for the dark slot',
     changes='Doubles down on two-tone gold to light the deep shade: keeps the <b>Regal Splendor</b> vase anchor and <b>June</b>, adds gold-centered <b>Stained Glass</b> and frosted, gold-margined <b>Autumn Frost</b>.',
     rows=[(3,'Regal Splendor',4,9,14.99),(8,'June',2.5,12,14.99),(8,'Stained Glass',3,9,16.99),(10,'Autumn Frost',2.5,9,16.99),(13,'Blue Mouse Ears',1,12,8.99)])],
}

# ------------------------------------------------------------------ designs data
CORE = {1,2,6}
designs = []
for i, g in enumerate(GARDENS, start=1):
    d = dict(n=i, name=H.unescape(re.sub(r'&amp;','&',g['name'])), tag=H.unescape(re.sub(r'<[^>]+>','',g['tag'])).strip(),
             core=i in CORE, plate=f"assets/plates/design{i}.jpg",
             idea=g['idea'], plan=g['plan'], why=g['why'], cats=g['cats'], shop=g['shop'], fine=g['fine'],
             plants=parse_plants(g['shop']), variations=[])
    for v in VARIATIONS.get(i, []):
        tbl, plants, cost, total = shop_table(v['rows'])
        d['variations'].append(dict(
            key=v['key'], title=v['title'], kicker=v['kicker'], changes=v['changes'],
            plate=f"assets/plates/{v['key']}.jpg", schematic=schematic([(c,n,s,q) for (c,n,s,q,e) in v['rows']], v.get('grad',False)),
            shop=tbl, varieties=len(v['rows']), plants=plants, cost=cost, total=total,
            plantList=[{'name':n,'qty':str(q)} for (c,n,s,q,e) in v['rows']]))
    designs.append(d)

# lurvey embed
lurvey = open("_lurvey_embed.json", encoding="utf-8").read()

# ================================================================== FINAL PLAN (Plan #1, staggered)
FC = {  # final-plan swatch colors
  'adg':('#3d6fb5','#2a4d7e'), 'fr':('#63b394','#457d67'), 'mouse':('#b06a8f','#7b4a64'),
  'vase':('#7a5aa8','#553e75'), 'goat':('#cdd68c','#8a9a4e'), 'mondo':('#2f6b41','#1e3d26'),
}
def _svg(w, h, inner):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:100%;height:auto;display:block">{inner}</svg>')

def staggered_bed(pocket_mice=0):
    """Top-down of the main bed: two large hostas in a STAGGERED drift (no runway),
    optional mouse-ears only in the front pockets."""
    W, H = 1140, 236; x0, x1 = 40, 1100; usable = x1 - x0
    seq = []; a, b = 14, 13; i = 0
    while a > 0 or b > 0:
        if i % 2 == 0 and a > 0: seq.append('adg'); a -= 1
        elif b > 0: seq.append('fr'); b -= 1
        elif a > 0: seq.append('adg'); a -= 1
        i += 1
    N = len(seq); step = usable / (N + 1)
    P = [f'<rect width="{W}" height="{H}" fill="#f3efe4"/>',
         f'<rect x="{x0-10}" y="40" width="{usable+20}" height="168" rx="12" fill="#efe7d3" stroke="#d9cdb0"/>',
         f'<text x="{x0}" y="28" font-size="11" font-weight="700" fill="#8a6510" font-family="sans-serif">STREET END · a little sun</text>',
         f'<text x="{x1}" y="28" font-size="11" font-weight="700" fill="#3c4f57" text-anchor="end" font-family="sans-serif">THE SLOT · deep shade →</text>',
         f'<text x="{x0}" y="230" font-size="10" fill="#8a7d63" font-family="sans-serif">walk edge (front)</text>']
    front_y, back_y = 168, 96; pockets = []
    for idx, typ in enumerate(seq):
        cx = x0 + step * (idx + 1)
        setback = ((idx % 2) ^ ((idx // 3) % 2))   # irregular zigzag → natural drift
        cy = (back_y if setback else front_y) + (5 if (idx // 2) % 2 else -5)
        col = FC['adg'] if typ == 'adg' else FC['fr']
        P.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="17" fill="{col[0]}" fill-opacity=".92" stroke="{col[1]}" stroke-width="1.3"/>')
        if setback: pockets.append(cx)
    if pocket_mice and pockets:
        gap = max(1, len(pockets) // pocket_mice); placed = 0
        for k in range(0, len(pockets), gap):
            if placed >= pocket_mice: break
            P.append(f'<circle cx="{pockets[k]:.0f}" cy="198" r="6.5" fill="{FC["mouse"][0]}" stroke="{FC["mouse"][1]}" stroke-width="1"/>')
            placed += 1
    return _svg(W, H, ''.join(P))

def fence_svg(option, groundcover='mondo'):
    """Top-down of the fence corner: clumping vase hosta(s) (+ optional Goatsbeard
    screen) at the fence, low trampleable groundcover under the meter box."""
    W, H = 1140, 300
    P = [f'<rect width="{W}" height="{H}" fill="#f3efe4"/>',
         f'<rect x="0" y="0" width="{W}" height="44" fill="#c9a48c" opacity=".5"/>',
         f'<text x="16" y="29" font-size="12" font-weight="700" fill="#8a5a3a" font-family="sans-serif">BRICK WALL (house)</text>',
         f'<rect x="120" y="26" width="60" height="30" rx="4" fill="#b98b52" stroke="#7a5a2f" stroke-width="2"/>',
         f'<text x="150" y="74" font-size="10.5" fill="#6b4a2a" text-anchor="middle" font-family="sans-serif">meter box — keep access</text>',
         f'<line x1="{W-42}" y1="56" x2="{W-42}" y2="{H-24}" stroke="#9aa0a6" stroke-width="6" stroke-dasharray="5 4"/>',
         f'<text x="{W-54}" y="{H-9}" font-size="11" font-weight="700" fill="#6b7076" text-anchor="end" font-family="sans-serif">CHAIN-LINK FENCE (neighbor)</text>']
    if option == 'screen':
        for gy in (108, 178, 248):
            P.append(f'<ellipse cx="{W-96}" cy="{gy}" rx="48" ry="30" fill="{FC["goat"][0]}" stroke="{FC["goat"][1]}" stroke-width="1.5"/>')
        P.append(f'<text x="{W-96}" y="66" font-size="10.5" fill="#5f6a30" text-anchor="middle" font-family="sans-serif">Goatsbeard screen · 4–5 ft</text>')
    vx = (W - 210) if option == 'screen' else (W - 130)
    vys = (128, 220) if option == 'screen' else (120, 186, 252)
    for vy in vys:
        P.append(f'<circle cx="{vx}" cy="{vy}" r="30" fill="{FC["vase"][0]}" fill-opacity=".9" stroke="{FC["vase"][1]}" stroke-width="1.5"/>')
    P.append(f'<text x="{vx}" y="{H-16}" font-size="10.5" fill="#4c3a6a" text-anchor="middle" font-family="sans-serif">Krossa Regal · vase hosta (clumping)</text>')
    gcol = FC['mondo'] if groundcover == 'mondo' else FC['mouse']
    glabel = 'dwarf mondo — low, steppable' if groundcover == 'mondo' else 'blue mouse-ears — low, steppable'
    for k in range(10):
        P.append(f'<circle cx="{92 + k*24}" cy="118" r="7" fill="{gcol[0]}" stroke="{gcol[1]}" stroke-width="1"/>')
    P.append(f'<text x="{92 + 10*24 + 12}" y="122" font-size="10.5" fill="#3a5a44" font-family="sans-serif">{glabel}</text>')
    return _svg(W, H, ''.join(P))

def final_overview_svg():
    """The whole 95-ft run as three labeled zones: staggered bed → gravel pad → fence corner."""
    W, H = 1140, 210; x0, x1 = 30, 1110; usable = x1 - x0
    bedX = x0 + usable * 0.70; padX = x0 + usable * 0.84
    P = [f'<rect width="{W}" height="{H}" fill="#f3efe4"/>',
         f'<rect x="{x0}" y="46" width="{bedX-x0}" height="132" rx="10" fill="#efe7d3" stroke="#d9cdb0"/>',
         f'<rect x="{bedX}" y="46" width="{padX-bedX}" height="132" fill="#dfd7c6" stroke="#c7bda4"/>',
         f'<rect x="{padX}" y="46" width="{x1-padX}" height="132" rx="10" fill="#e7e0cf" stroke="#cdbfa0"/>',
         f'<text x="{(x0+bedX)/2:.0f}" y="34" font-size="11" font-weight="700" fill="#3c4f57" text-anchor="middle" font-family="sans-serif">ZONE 1 · STAGGERED BED</text>',
         f'<text x="{(bedX+padX)/2:.0f}" y="34" font-size="10.5" font-weight="700" fill="#8a6b3a" text-anchor="middle" font-family="sans-serif">ZONE 2 · GRAVEL PAD</text>',
         f'<text x="{(padX+x1)/2:.0f}" y="34" font-size="10.5" font-weight="700" fill="#4c3a6a" text-anchor="middle" font-family="sans-serif">ZONE 3 · FENCE</text>',
         f'<text x="{x1}" y="200" font-size="10" fill="#8a7d63" text-anchor="end" font-family="sans-serif">95 ft · street → yard</text>']
    # zone 1: staggered dots
    n = 20; step = (bedX - x0 - 20) / n
    for k in range(n):
        cx = x0 + 16 + step * k; setback = ((k % 2) ^ ((k // 3) % 2))
        cy = (96 if setback else 150) + (4 if (k // 2) % 2 else -4)
        col = FC['adg'] if k % 2 == 0 else FC['fr']
        P.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="12" fill="{col[0]}" fill-opacity=".9" stroke="{col[1]}" stroke-width="1"/>')
    # zone 2: gravel stipple + label
    for gx in range(int(bedX) + 14, int(padX) - 6, 16):
        for gy in range(64, 168, 18):
            P.append(f'<circle cx="{gx + (8 if (gy//18)%2 else 0)}" cy="{gy}" r="2.4" fill="#a99b7d"/>')
    P.append(f'<text x="{(bedX+padX)/2:.0f}" y="196" font-size="9.5" fill="#8a6b3a" text-anchor="middle" font-family="sans-serif">packed gravel · 6–7 ft</text>')
    # zone 3: vase hosta + screen markers
    fx = (padX + x1) / 2
    for vy in (150, 108):
        P.append(f'<circle cx="{fx-16:.0f}" cy="{vy}" r="15" fill="{FC["vase"][0]}" fill-opacity=".9" stroke="{FC["vase"][1]}" stroke-width="1"/>')
    for gy in (150, 108):
        P.append(f'<ellipse cx="{fx+20:.0f}" cy="{gy}" rx="18" ry="12" fill="{FC["goat"][0]}" stroke="{FC["goat"][1]}" stroke-width="1"/>')
    P.append(f'<line x1="{x1-6}" y1="52" x2="{x1-6}" y2="172" stroke="#9aa0a6" stroke-width="4" stroke-dasharray="4 3"/>')
    return _svg(W, H, ''.join(P))

def plant_rows(items):
    """items: [(cat_or_None, name, qty, each, tag)] -> list of dicts + total cost."""
    out = []; cost = 0.0
    for cat, name, qty, each, tag in items:
        sw = FC.get(cat) if isinstance(cat, str) else (CAT.get(cat) if cat else None)
        line = qty * each if each else 0
        cost += line
        out.append({'name': name, 'qty': qty, 'each': each, 'line': round(line, 2),
                    'sw': list(sw) if sw else None, 'tag': tag})
    return out, round(cost, 2)

# ---- per-option GPT render prompts (user pastes into GPT; attach design1.jpg as style ref) ----
_SITE = ("Photorealistic documentary photo of a narrow Chicago 'gangway' garden — the ~10-ft "
  "corridor between two 22-ft red-brick bungalow walls, deep even shade, soft overcast light. "
  "Camera at standing eye height looking down the length so the 3-ft-deep planting bed along ONE "
  "wall recedes to a vanishing point. Dark hardwood mulch clearly visible between plants. Freshly "
  "planted, nursery-size (1-gal) hostas spaced at mature spread and NOT yet touching — each a "
  "distinct clump with a ring of mulch around it, breathing room, NOT a solid hedge. No people, "
  "no text, true-to-life proportions. Attach the reference image for site + style.")
P_BED_CLEAN = (_SITE + "\n\nPLANTING: Two hostas only, in a STAGGERED DRIFT (this is the key) — "
  "alternate blue Abiqua Drinking Gourd and green-with-white-margin Francee, and offset each clump "
  "forward or back about a foot so the front edge is scalloped and NO straight 'runway' line forms. "
  "About 14 blue + 13 white down the run. NO small edging hostas at all — just the two large types "
  "with dark mulch between them.")
P_BED_POCKET = (P_BED_CLEAN + " THEN tuck a FEW small blue mouse-ear hostas (about 8 total) ONLY into "
  "the front pockets where a clump sits back from the walk — a light accent, never a continuous ribbon.")
P_FENCE_SCREEN = (_SITE.replace('so the 3-ft-deep planting bed along ONE wall recedes to a vanishing point. ',
  'toward the shaded back corner where the gangway meets a chain-link fence and a wall-mounted rusty '
  'electrical meter box. ') + "\n\nPLANTING: A clumping, non-spreading screen at the fence — 2 upright "
  "blue-grey vase hostas (Krossa Regal) plus 2 tall creamy Goatsbeard (Aruncus) plumes about 4–5 ft "
  "to soften and partly block the fence. Everything stays in tidy clumps; nothing creeps through the "
  "fence to the neighbor. Under the meter box, a low carpet of dwarf mondo grass that can be stepped on.")
P_FENCE_VASE = (_SITE.replace('so the 3-ft-deep planting bed along ONE wall recedes to a vanishing point. ',
  'toward the shaded back corner where the gangway meets a chain-link fence and a wall-mounted rusty '
  'electrical meter box. ') + "\n\nPLANTING: 3 upright blue-grey vase hostas (Krossa Regal) in one tidy, "
  "non-spreading clump at the fence corner, softening the fence. Under the meter box, a low steppable "
  "carpet of dwarf mondo grass (or tiny blue mouse-ear hostas) for easy access. Keep it simple and open.")

_bed_clean_pl, _bed_clean_cost = plant_rows([
    (4, 'Abiqua Drinking Gourd', 14, 9.99, 'blue anchor'),
    (6, 'Francee', 13, 11.99, 'white margin')])
_bed_pocket_pl, _bed_pocket_cost = plant_rows([
    (4, 'Abiqua Drinking Gourd', 14, 9.99, 'blue anchor'),
    (6, 'Francee', 13, 11.99, 'white margin'),
    (13, 'Blue Mouse Ears', 8, 8.99, 'front pockets only')])
_fence_screen_pl, _fence_screen_cost = plant_rows([
    (3, 'Krossa Regal', 2, 14.99, 'vase hosta · clumping'),
    ('goat', 'Goatsbeard (Aruncus)', 2, 0, 'companion — source separately'),
    ('mondo', 'Dwarf mondo grass', 12, 0, 'companion — low, steppable')])
_fence_vase_pl, _fence_vase_cost = plant_rows([
    (3, 'Krossa Regal', 3, 14.99, 'vase hosta · clumping'),
    ('mondo', 'Dwarf mondo grass', 12, 0, 'companion — low, steppable')])

FINAL = {
  'hero': {
    'kicker': 'FINAL PLAN · Plan #1 refined',
    'title': 'Blue & White Gangway — the final',
    'blurb': "We're building Plan #1: blue Abiqua Drinking Gourd and white-margined Francee, now "
             "arranged in a staggered drift instead of a straight row. Three zones — the main bed, "
             "the firewood gravel pad, and the fence corner. Each zone below carries a top-down plan, "
             "a plant list, and a copy-paste GPT prompt so you can generate the photoreal image.",
    'facts': [['82 ft', 'main bed'], ['staggered', 'no runway'], ['6–7 ft', 'gravel pad'],
              ['3 zones', 'to build']],
    'overview': final_overview_svg(),
  },
  'zones': [
    { 'id': 'bed', 'name': 'Zone 1 — the main bed (staggered blue & white)',
      'intro': "A single straight row down a 3-ft bed reads as a runway and the clumps merge into a "
               "hedge. Staggering the centers (alternating blue and white, each nudged forward or back "
               "~1 ft) breaks that sightline into a natural drift and scallops the front edge. Two "
               "options: leave it clean and let the big hostas knit in, or tuck a few mouse-ears into "
               "the front pockets for a finished edge the first couple years.",
      'options': [
        { 'key': 'clean', 'label': 'Clean (recommended)',
          'note': 'Just the two large hostas, staggered. They close in and cover soil in 2–3 seasons.',
          'schematic': staggered_bed(0), 'plants': _bed_clean_pl, 'cost': _bed_clean_cost,
          'sample': 'assets/plates/design1.jpg', 'prompt': P_BED_CLEAN },
        { 'key': 'pocket', 'label': 'Pocket accents',
          'note': 'A handful of Blue Mouse Ears only in the front pockets the staggering creates.',
          'schematic': staggered_bed(8), 'plants': _bed_pocket_pl, 'cost': _bed_pocket_cost,
          'sample': 'assets/plates/design1.jpg', 'prompt': P_BED_POCKET },
      ]},
    { 'id': 'pad', 'name': 'Zone 2 — the firewood pad (clean the gravel, don\'t pave)',
      'intro': "No pavers. Reuse the ~1 in of existing gravel as a base and clean it up, then top and "
               "compact it into a firm 6–7 ft pad. Gravel lives ONLY here.",
      'schematic': None,
      'steps': [
        ['Clear & weed', 'Pull the volunteer weeds by the root (the sumac/elm seedlings especially). Rake sticks and leaves out.'],
        ['Rake the stone off the soil', 'The gravel looks dirty because of the fines — silt + decomposed leaf litter packed between the stones, not the stone itself.'],
        ['Screen it', 'Shovel the gravel onto a ½-in hardware-cloth screen over a wheelbarrow. The dirt/fines drop through; clean stone stays on top.'],
        ['Hose-rinse', 'Rinse the screened stone in the screen to wash off the last mud. Now it looks new — reuse it as the sub-layer.'],
        ['Top with new crushed stone', 'Add 2–3 in of ANGULAR crushed stone (CA-6 / crushed limestone road base). Angular locks and compacts; pea gravel rolls and won\'t pack.'],
        ['Level, wet & tamp', 'Rake level, wet it, and tamp in lifts (hand tamper or a rented plate compactor). Slope it slightly away from the foundation.'],
        ['Edge it', 'Contain the pad with a line of the existing bricks (or steel edging) so the stone doesn\'t migrate into the bed.'],
      ],
      'note': "Honest note: ~1 in of reused gravel alone is too thin to stay firm and level under a "
              "loaded grill/woodpile — it pumps dirt up and goes uneven. The clean + top + compact "
              "gives you a pad that stays nice." },
    { 'id': 'fence', 'name': 'Zone 3 — the fence corner (screen + box access)',
      'intro': "By the meter box: something tall at the fence to soften it, but CLUMPING so it never "
               "spreads into the neighbor's side; and a low, steppable groundcover under the box (fine "
               "to trample — no one goes there). Two screen options to compare — generate both and see "
               "which you like. The old climbing hydrangea is dropped (too big / too much upkeep).",
      'options': [
        { 'key': 'screen', 'label': 'Vase hosta + Goatsbeard',
          'note': 'Krossa Regal vase hostas plus a clumping Goatsbeard for real fence-blocking height (4–5 ft). Both clump; neither runs.',
          'schematic': fence_svg('screen', 'mondo'), 'plants': _fence_screen_pl, 'cost': _fence_screen_cost,
          'sample': 'assets/plates/design6.jpg', 'prompt': P_FENCE_SCREEN },
        { 'key': 'vase', 'label': 'Vase hosta only',
          'note': 'Just Krossa Regal — fully on-theme and clumping, ~3 ft, softens rather than hides the fence.',
          'schematic': fence_svg('vase', 'mondo'), 'plants': _fence_vase_pl, 'cost': _fence_vase_cost,
          'sample': 'assets/plates/design6.jpg', 'prompt': P_FENCE_VASE },
      ],
      'groundcover': {
        'intro': 'Low, trampleable layer under the meter box (pick one):',
        'choices': [
          ['Dwarf mondo grass', 'Evergreen, 2–4 in, clumping, shade-tolerant, takes light foot traffic. Companion — source separately.'],
          ['Blue Mouse Ears', 'Tiny hostas that shrug off the occasional step; already in the plant list ($8.99 each).'],
        ]}},
  ],
}

# ------------------------------------------------------------------ view sections
def guide(inner): return f'<div class="guide">{inner}</div>'

views = {}
views['designs'] = ('<div class="dv-gallery" id="dvGallery"></div>'
                    '<div class="dv-detail" id="dvDetail" hidden></div>')
views['finder'] = (
  '<div class="fh"><h2>Plant finder</h2>'
  '<p class="fh-lede">Every hosta Lurvey listed, filtered for this 3-ft bed. '
  'Flip between tile and list, search and filter, and export / import / refresh the base data.</p></div>'
  '<div class="panel dataPanel"><div class="dp-row"><b id="dataStatus"></b>'
  '<div class="dp-btns">'
  '<button class="chip" id="dataExport" type="button">⬇ Export JSON</button>'
  '<label class="chip" for="dataFile">⬆ Import JSON</label>'
  '<input type="file" id="dataFile" accept="application/json,.json" hidden>'
  '<button class="chip" id="dataReset" type="button">Reset</button>'
  '<a class="chip" href="data/lurvey-spec.md" target="_blank" rel="noopener">📄 Spec &amp; re-pull</a>'
  '</div></div></div>'
  '<div class="fbar"><input type="search" id="q" placeholder="Search name, colour, note…" aria-label="Search">'
  '<span id="fcatMount"></span>'
  '<select id="sort" aria-label="Sort"><option value="cat">Sort: category</option>'
  '<option value="name">Name A–Z</option><option value="plo">Price ↑</option>'
  '<option value="phi">Price ↓</option><option value="wlo">Spread ↑</option><option value="whi">Spread ↓</option></select>'
  '<span class="seg" id="viewSeg"><button data-v="tile" class="on" type="button">▦ Tiles</button>'
  '<button data-v="list" type="button">☰ List</button></span>'
  '<span class="fcount" id="cnt"></span></div>'
  '<div id="pillMount"></div>'
  '<div id="finderResults"></div><div id="nores" class="nores" hidden>No matches.</div>')
views['final'] = ''  # built in app.js from finalData
views['site'] = guide(FR['site']) + guide(FR['corner'])
views['build'] = guide(FR['works'])
views['reference'] = guide('<h2 style="margin-bottom:14px">Colour key — the thirteen categories</h2>'+FR['key']) + guide(FR['refhead']+FR['refblock'])
views['renderkit'] = guide(FR['renderkit'])

SECTION_HTML = ''.join(
    f'<section data-view="{k}"{" hidden" if k!="final" else ""}>{v}</section>'
    for k, v in [('final',views['final']),('designs',views['designs']),('finder',views['finder']),
                 ('site',views['site']),('build',views['build']),('reference',views['reference']),
                 ('renderkit',views['renderkit'])])

# ------------------------------------------------------------------ assemble index.html
PREPAINT = ("(function(){try{var t=localStorage.getItem('hosta.theme'),m='dark';"
            "if(t&&t.indexOf(':')>-1)m=t.split(':')[1];else if(t)m=t;"
            "var r=document.documentElement;r.setAttribute('data-palette','garden');r.setAttribute('data-theme',m);}"
            "catch(e){document.documentElement.setAttribute('data-palette','garden');document.documentElement.setAttribute('data-theme','dark');}})();")

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Gangway Hosta Garden</title>
<meta name="description" content="Six designed plans plus finalization variations for 95 ft of deep shade between two Chicago bungalows — photoreal renders, measured plans, a searchable plant finder, and a full build guide.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%BF%3C/text%3E%3C/svg%3E">
<script>{PREPAINT}</script>
<link rel="stylesheet" href="vendor/polecat-shell/tokens.css">
<link rel="stylesheet" href="vendor/polecat-shell/shell.css">
<link rel="stylesheet" href="css/guide.css">
<link rel="stylesheet" href="css/app.css">
</head>
<body>
<div class="aurora" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
<div id="views" hidden>{SECTION_HTML}</div>
<script type="application/json" id="lurveyData">{lurvey}</script>
<script type="application/json" id="designsData">{json.dumps(designs, ensure_ascii=False)}</script>
<script type="application/json" id="finalData">{json.dumps(FINAL, ensure_ascii=False)}</script>
<script type="module" src="js/app.js"></script>
</body>
</html>'''

open(OUT, "w", encoding="utf-8").write(html)
print(f"WROTE {OUT} ({len(html)//1024} KB)")
print(f"designs={len(designs)} cores={[d['n'] for d in designs if d['core']]} "
      f"variations={sum(len(d['variations']) for d in designs)}")
