#!/usr/bin/env python3
"""Build site/hosta/index.html from hosta_gangway_guide_v3.html.

Provenance / one-off transform (kept in repo, NOT published):
  * externalizes the 6 base64 photoreal renders -> assets/renders/designN.jpeg
  * demotes the two awkward side-elevation SVGs per design into a small,
    collapsed <details> block (render + top-down plan lead)
  * wraps the guide in the garden shell: drifting aurora backdrop, an app bar
    with a light/dark theme toggle (fleet-standard chrome)
  * adds a Designs gallery, a Render Kit (GPT prompt), and 2 grounded
    variations for each of the 3 core designs (1, 2, 6)
  * preserves ALL v3 content verbatim
Run:  python3 build_app.py
"""
import re, base64, os, html as H

SRC = "hosta_gangway_guide_v3.html"
OUT = "../site/hosta/index.html"
REND = "../site/hosta/assets/renders"
os.makedirs(REND, exist_ok=True)

doc = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- category color map
CAT = {1:('#1f3a6e','#15284d'),2:('#c8961c','#8c6913'),3:('#7a5aa8','#553e75'),
       4:('#3d6fb5','#2a4d7e'),5:('#1f7a45','#155530'),6:('#63b394','#457d67'),
       7:('#8f9c2b','#646d1e'),8:('#d2691e','#934915'),9:('#74a8de','#51759b'),
       10:('#94a9cf','#677690'),11:('#e0bf2f','#9c8520'),12:('#4f9a56','#376b3c'),
       13:('#b06a8f','#7b4a64')}
CATNAME = {1:'Giant Blue',2:'Giant/Large Gold',3:'Upright / Vase',4:'Large Blue Mound',
       5:'Large Green / Fragrant',6:'Green + White Margin',7:'Gold/Yellow Margin',
       8:'Gold-Centered Two-Tone',9:'Medium Blue Mound',10:'Frosted / Misted',
       11:'Small Gold Accent',12:'Small Green Edger',13:'Miniature / Mouse-Ear'}

# ---------------------------------------------------------------- 1) externalize renders
imgs = list(re.finditer(r'<img loading="lazy" alt="Photoreal render" src="data:image/(\w+);base64,([A-Za-z0-9+/=]+)">', doc))
assert len(imgs) == 6, f"expected 6 renders, got {len(imgs)}"
# write files in document (design) order & replace with file refs
def repl_img(m, _c=[0]):
    i = _c[0]; _c[0] += 1
    data = base64.b64decode(m.group(2))
    open(f"{REND}/design{i+1}.{m.group(1)}", "wb").write(data)
    return (f'<img loading="lazy" alt="Photoreal render of design {i+1}" '
            f'src="assets/renders/design{i+1}.{m.group(1)}" style="width:100%;height:auto;display:block">')
doc = re.sub(r'<img loading="lazy" alt="Photoreal render" src="data:image/(\w+);base64,([A-Za-z0-9+/=]+)">', repl_img, doc)

# ---------------------------------------------------------------- 2) demote side elevations
SIDE = re.compile(
    r'<h4 class="g-h4">Standing at the street, looking back</h4>(<div class="g-svg">.*?</div>)'
    r'<h4 class="g-h4">Standing at the wood pile, looking front</h4>(<div class="g-svg">.*?</div>)',
    re.S)
def demote(m):
    return ('<details class="g-sides"><summary><span class="g-sides-t">Side elevations</span>'
            '<span class="g-sides-n">rough massing sketches — the render &amp; top-down plan above are the references</span></summary>'
            '<div class="g-sides-grid">'
            f'<figure class="g-side"><figcaption>From the street, looking back</figcaption>{m.group(1)}</figure>'
            f'<figure class="g-side"><figcaption>From the wood pile, looking front</figcaption>{m.group(2)}</figure>'
            '</div></details>')
doc, nside = SIDE.subn(demote, doc)
assert nside == 6, f"expected 6 side-elevation pairs, got {nside}"

# ---------------------------------------------------------------- 3) schematic top-down for variations
def schematic(rows, gradient=False):
    """rows: list of (cat, name, spread_ft, qty). Returns an SVG string (proportional
    top-down schematic: mature-spread circles along the 95 ft run, mouse-ear ribbon
    along the front edge)."""
    W, Hh = 1140, 232
    x0, x1 = 34, 1106
    usable = x1 - x0
    scale = usable / 95.0
    body = [(c,n,s,q) for (c,n,s,q) in rows if not (c == 13)]
    mice = [(c,n,s,q) for (c,n,s,q) in rows if c == 13]
    if gradient:  # street(sun) -> slot: leave as authored order (already street->shade)
        pass
    n_body = sum(q for *_, q in body) or 1
    step = usable / (n_body + 1)
    parts = [f'<svg viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">']
    parts.append(f'<rect width="{W}" height="{Hh}" fill="#f3efe4"/>')
    # bed
    parts.append(f'<rect x="{x0-8}" y="54" width="{usable+16}" height="150" rx="10" fill="#efe7d3" stroke="#d9cdb0"/>')
    # zone bands (street sun / slot / rear)
    z1 = x0 + 11*scale
    parts.append(f'<rect x="{x0-8}" y="54" width="{z1-(x0-8)}" height="150" rx="10" fill="#f7edc4" opacity=".5"/>')
    parts.append(f'<text x="{(x0+z1)/2:.0f}" y="46" font-size="10.5" font-weight="700" fill="#8a6510" text-anchor="middle" letter-spacing=".05em" font-family="-apple-system,Segoe UI,sans-serif">STREET END · sun</text>')
    parts.append(f'<text x="{(z1+x1)/2:.0f}" y="46" font-size="10.5" font-weight="700" fill="#3c4f57" text-anchor="middle" letter-spacing=".05em" font-family="-apple-system,Segoe UI,sans-serif">THE SLOT · deep shade →</text>')
    parts.append(f'<text x="{x1}" y="222" font-size="10" fill="#8a7d63" text-anchor="end" font-family="-apple-system,Segoe UI,sans-serif">95 ft · 3 ft deep bed · schematic mix &amp; placement</text>')
    # body plants
    cx = x0 + step
    row = 0
    for c, n, s, q in body:
        fill, stroke = CAT.get(c, ('#888','#555'))
        r = max(9, min(30, s * scale * 0.5))
        for _ in range(q):
            cy = 118 + (14 if row % 2 else -14)
            parts.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="{r:.0f}" fill="{fill}" fill-opacity=".9" stroke="{stroke}" stroke-width="1.2"/>')
            cx += step; row += 1
    # mouse-ear ribbon (front edge)
    for c, n, s, q in mice:
        fill, stroke = CAT.get(c, ('#b06a8f','#7b4a64'))
        if q <= 0: continue
        mstep = usable / (q + 1)
        mx = x0 + mstep
        for _ in range(q):
            parts.append(f'<circle cx="{mx:.0f}" cy="192" r="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            mx += mstep
    parts.append('</svg>')
    return ''.join(parts)

def money(v): return f"${v:,.2f}"

def variation_html(vid, core_no, title, kicker, changes, rows, gradient=False):
    plants = sum(q for (c, n, s, q, each) in rows)
    varieties = len(rows)
    plant_cost = sum(q*each for (c,n,s,q,each) in rows)
    site, climber = 505.0, 55.0
    total = plant_cost + site + climber
    svg = schematic([(c,n,s,q) for (c,n,s,q,each) in rows], gradient)
    # shopping rows
    trs = []
    for c,n,s,q,each in rows:
        fill, stroke = CAT[c]
        trs.append(
            f'<tr><td><span class="g-sw" style="background:{fill};border-color:{stroke}"></span> '
            f'<span class="g-cat">{c}. {CATNAME[c]}</span></td>'
            f'<td><b>{H.escape(n)}</b></td><td class="g-dim">{s if s>=1 else "10–12 in"}{" ft" if s>=1 else ""}</td>'
            f'<td class="r">{q}</td><td class="r g-dim">{money(each)}</td><td class="r">{money(q*each)}</td></tr>')
    swatches = ''.join(
        f'<span class="g-sw" title="{c}. {CATNAME[c]}" style="background:{CAT[c][0]};border-color:{CAT[c][1]}"></span>'
        for c in dict.fromkeys(c for c,*_ in rows))
    return f'''
<div class="g-var" id="{vid}">
  <div class="g-var-h"><span class="g-var-badge">Variation</span>
    <div><h5>{H.escape(title)}</h5><p class="g-var-k">{H.escape(kicker)}</p></div>
    <div class="g-var-meta">{varieties} varieties · {plants} plants · {money(plant_cost)} in plants</div>
  </div>
  <p class="g-var-changes"><b>What changes vs the core:</b> {changes}</p>
  <div class="g-h4">Schematic top-down — proportional mix &amp; placement</div>
  <div class="g-svg">{svg}</div>
  <div class="g-board g-board-slot" data-slot="{vid}">
    <div class="g-slot-in"><b>Render slot</b>Drop your GPT render here — see the <a href="#render-kit">Render Kit</a> for the exact prompt &amp; the plant table below.</div>
  </div>
  <div class="g-h4">Shopping list <span class="g-swrow">{swatches}</span></div>
  <div class="g-tw"><table class="g-tbl"><thead><tr><th>Category</th><th>Variety</th><th>Mature spread</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Subtotal</th></tr></thead>
  <tbody>{''.join(trs)}
  <tr class="g-sum"><td>Plants — {varieties} varieties</td><td></td><td></td><td class="r">{plants}</td><td></td><td class="r">{money(plant_cost)}</td></tr>
  <tr class="g-sub"><td>Site works (same for every plan)</td><td></td><td></td><td></td><td></td><td class="r">+ {money(site)}</td></tr>
  <tr class="g-sub"><td>Climbing hydrangea, #2 pot, corner screen</td><td></td><td></td><td class="r">1</td><td></td><td class="r">+ {money(climber)}</td></tr>
  <tr class="g-grand"><td>Installed cost, pocket-amendment method</td><td></td><td></td><td></td><td></td><td class="r">{money(total)}</td></tr>
  </tbody></table></div>
</div>'''

# --- variation data (all varieties real, in-stock & bed-fitting from the catalog) ---
# rows: (category, name, spread_ft, qty, each_price)
VARIATIONS = {
 1: [  # core: Blue & White Gangway
   dict(vid='g1va', title='Crisp Contrast', kicker='Same idea, bolder whites & more substance',
        changes='The white-margin ribbon becomes <b>Patriot</b> — a wider, brighter, thicker-leaved margin that reads bolder down the walk (and, at 3.5 ft, needs a few fewer plants). Blue anchor and mouse-ear edge unchanged.',
        rows=[(4,'Abiqua Drinking Gourd',3,14,9.99),(6,'Patriot',3.5,12,11.99),(13,'Blue Mouse Ears',1,27,8.99)]),
   dict(vid='g1vb', title='Moonlit Edge', kicker='Same body, a two-tone sparkle at the sunny end',
        changes='The all-blue mouse-ear ribbon splits into <b>Blue Mouse Ears</b> through the shade slot plus a warm run of <b>Sun Mouse</b> where the street end catches 3–4 hrs of light — a low gold shimmer exactly where the sun can colour it.',
        rows=[(4,'Abiqua Drinking Gourd',3,14,9.99),(6,'Francee',3,13,11.99),(13,'Blue Mouse Ears',1,18,8.99),(13,'Sun Mouse',0.83,9,9.99)]),
 ],
 2: [  # core: The Light Gradient
   dict(vid='g2va', title='Brighter Street End', kicker='Livelier gold in the sun, deeper blue in the slot', gradient=True,
        changes='Swaps flat <b>August Moon</b> for ruffled, brighter <b>Dancing Queen</b> at the sunny street end and leans the shade slot bluer with more <b>Halcyon</b>. Same street→shade light logic, higher contrast.',
        rows=[(2,'Dancing Queen',3,7,14.99),(9,'Halcyon',3,8,11.99),(6,'Patriot',3.5,7,11.99),(4,'Abiqua Drinking Gourd',3,6,9.99),(13,'Blue Mouse Ears',1,21,8.99)]),
   dict(vid='g2vb', title='Gold-Center Transition', kicker='A richer light-to-shade fade with two-tone leaves', gradient=True,
        changes='Replaces the flat gold with gold-<i>centered</i> <b>Stained Glass</b> (the most sun-tolerant, and fragrant) at the street, then fades through frosted <b>First Frost</b> into blue <b>Halcyon</b> — the gradient now happens inside the leaves, not just across the bed.',
        rows=[(8,'Stained Glass',3,5,16.99),(10,'First Frost',2.5,8,14.99),(9,'Halcyon',3,7,11.99),(6,'Patriot',3.5,6,11.99),(13,'Blue Mouse Ears',1,21,8.99)]),
 ],
 6: [  # core: Collector's Run
   dict(vid='g6va', title='Vase-Forward', kicker='More upright architecture + a fragrant white show',
        changes='Trades <b>Brother Stefan</b> for fragrant, white-blushed <b>Royal Wedding</b> so the collector run also earns an August flower show, while keeping the <b>Regal Splendor</b> vases that make a narrow bed feel taller.',
        rows=[(3,'Regal Splendor',4,9,14.99),(5,'Royal Wedding',3.5,9,18.99),(8,'June',2.5,12,14.99),(10,'First Frost',2.5,9,14.99),(13,'Blue Mouse Ears',1,12,8.99)]),
   dict(vid='g6vb', title='Two-Tone Bright', kicker='Gold-centered brightness for the dark slot',
        changes='Doubles down on two-tone gold to light the deep shade: keeps the <b>Regal Splendor</b> vase anchor and <b>June</b>, adds gold-centered <b>Stained Glass</b> and frosted, gold-margined <b>Autumn Frost</b> in place of the greener picks.',
        rows=[(3,'Regal Splendor',4,9,14.99),(8,'June',2.5,12,14.99),(8,'Stained Glass',3,9,16.99),(10,'Autumn Frost',2.5,9,16.99),(13,'Blue Mouse Ears',1,12,8.99)]),
 ],
}

def build_variations_block(core_no):
    vs = VARIATIONS[core_no]
    inner = ''.join(variation_html(v['vid'], core_no, v['title'], v['kicker'], v['changes'],
                                    v['rows'], v.get('gradient', False)) for v in vs)
    return (f'<div class="g-vars" id="g{core_no}-variations">'
            f'<div class="g-vars-h"><span class="g-core-badge">★ Core pick</span>'
            f'<h4 class="g-h4" style="margin:0">Finalization variations — keep the core, compare the plant swaps</h4></div>'
            f'<p class="g-vars-lede">Two ways to take this design to a final, keeping its intent but testing '
            f'different varieties and arrangements. Each carries a render slot for the image you generate next.</p>'
            f'{inner}</div>')

# inject variations before the closing </article> of gardens 1,2,6
for core_no in (1, 2, 6):
    marker = f'id="g{core_no}"'
    start = doc.find(marker)
    # find the matching </article> (articles don't nest)
    end = doc.find('</article>', start)
    assert start != -1 and end != -1, f"garden {core_no} not found"
    block = build_variations_block(core_no)
    doc = doc[:end] + block + doc[end:]

print("variations injected for cores 1,2,6")

# ---------------------------------------------------------------- 4) design gallery grid
GALLERY_CARDS = [
 (1,'Blue &amp; White Gangway','The baseline','★ core'),
 (2,'The Light Gradient','Horticulturally correct','★ core'),
 (3,'The Colonnade','Architectural',''),
 (4,'Moonlight Walk','The showpiece',''),
 (5,'Blue Ridge',"Connoisseur's blues",''),
 (6,"Collector's Run",'Best that fit','★ core'),
]
cards = ''.join(
 f'<a class="dg-card{" dg-core" if badge else ""}" href="#g{n}">'
 f'<div class="dg-img"><img loading="lazy" src="assets/renders/design{n}.jpeg" alt="Design {n}"></div>'
 f'<div class="dg-body"><div class="dg-n">{n}</div><div><div class="dg-name">{name}</div>'
 f'<div class="dg-sub">{sub}{" · "+badge if badge else ""}</div></div></div></a>'
 for (n,name,sub,badge) in GALLERY_CARDS)
GALLERY = (
 '<div class="dg-wrap"><div class="dg-head"><h3 style="margin:0">Design gallery</h3>'
 '<p>Six reference designs. Three are your core picks (★) and carry two finalization '
 'variations each — twelve options in all. Tap any card to jump to its render, plan and shopping list.</p></div>'
 f'<div class="dg-grid">{cards}</div></div>')
# insert gallery right after the six-plans <h2>The six plans</h2> lede rule
anchor = '</div><b>$500 more</b>.'
# simpler: insert before first <article class="g-garden"
gi = doc.find('<article class="g-garden"')
doc = doc[:gi] + GALLERY + doc[gi:]
print("gallery injected")

# ---------------------------------------------------------------- 5) render kit section
RENDER_KIT = open('_render_kit.html', encoding='utf-8').read()
# place render kit as its own section right after the six-plans section (before #corner)
corner = doc.find('<section id="corner">')
assert corner != -1
doc = doc[:corner] + RENDER_KIT + doc[corner:]
print("render kit injected")

# ---------------------------------------------------------------- 6) nav links (add Designs + Render kit)
doc = doc.replace(
 '<a href="#compare">Compare all six</a>',
 '<a href="#compare">Compare all six</a><a href="#gallery">Design gallery</a>')
doc = doc.replace(
 '<a href="#corner">Wood pile &amp; corner</a>',
 '<a href="#render-kit">Render kit</a><a href="#corner">Wood pile &amp; corner</a>')
# give the six-plans section an id for the gallery anchor
doc = doc.replace('<section><div class="w">\n<h2>The six plans</h2>',
                  '<section id="gallery"><div class="w">\n<h2>The six plans</h2>', 1)

# ---------------------------------------------------------------- 7) shell: aurora + appbar + theme + title
SHELL_CSS = open('_shell.css', encoding='utf-8').read()
doc = doc.replace('</style></head>', SHELL_CSS + '</style></head>', 1)
# html data-theme + lang already present? set data-theme default light
doc = doc.replace('<html lang="en">', '<html lang="en" data-theme="light">', 1)

APPBAR = (
 '<div class="aurora" aria-hidden="true"><span></span><span></span><span></span><span></span></div>'
 '<div class="hg-appbar"><a class="hg-brand" href="../">'
 '<span class="hg-mark">🌿</span><span>The Gangway <b>Hosta</b> Garden</span></a>'
 '<div class="hg-appbar-r"><a class="hg-up" href="../">Custom ↗</a>'
 '<button class="hg-theme" id="hgTheme" type="button" aria-label="Toggle light/dark">🌙</button></div></div>')
doc = doc.replace('<body><div id="guide">', '<body>' + APPBAR + '<div id="guide">', 1)

THEME_JS = '''<script>
(function(){var root=document.documentElement,btn=document.getElementById('hgTheme');var s=null;
try{s=localStorage.getItem('custom.theme');}catch(e){}
if(!s&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)s='dark';
if(s)root.setAttribute('data-theme',s);
function p(){btn.textContent=root.getAttribute('data-theme')==='dark'?'\\u2600\\ufe0f':'\\ud83c\\udf19';}p();
btn.addEventListener('click',function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';
root.setAttribute('data-theme',n);try{localStorage.setItem('custom.theme',n);}catch(e){}p();});})();
</script>'''
doc = doc.replace('</body>', THEME_JS + '</body>', 1)

# ---------------------------------------------------------------- 8) base-data layer
# empty the static finder rows (rendered from JSON by the data module)
doc = re.sub(r'(<tbody id="selbody">).*?(</tbody>)', r'\1\2', doc, count=1, flags=re.S)

# Base-data panel — export / import / refresh, above the finder table
PANEL = ('<div class="panel dataPanel"><h3>Base data — export, import &amp; refresh</h3>'
 '<p class="g-fine" style="margin:0 0 10px">The finder below is driven by Lurvey plant data. '
 'Export it to edit or archive, import a fresh pull, or hand the '
 '<a href="data/lurvey-spec.md" target="_blank" rel="noopener">data spec</a> to a research session to re-pull. '
 '<b id="dataStatus"></b></p>'
 '<div class="ctl" style="margin:0">'
 '<button class="chip" id="dataExport" type="button">⬇ Export JSON</button>'
 '<label class="chip" for="dataFile" style="cursor:pointer">⬆ Import JSON</label>'
 '<input type="file" id="dataFile" accept="application/json,.json" hidden>'
 '<button class="chip clear" id="dataReset" type="button">Reset to shipped</button>'
 '<a class="chip" href="data/lurvey-spec.md" target="_blank" rel="noopener">📄 Spec &amp; re-pull</a>'
 '<a class="chip" href="data/lurvey-hostas.json" target="_blank" rel="noopener">Raw JSON ↗</a>'
 '</div></div>')
doc = doc.replace('<div class="panel selpanel">', PANEL + '<div class="panel selpanel">', 1)

# embed JSON + inject the data module right before the existing filter script
embed = open('_lurvey_embed.json', encoding='utf-8').read()
module = open('_data_module.html', encoding='utf-8').read().replace('__LURVEY_JSON__', embed)
doc = doc.replace('<script>\n(function(){\n var body=document.getElementById(\'selbody\')',
                  module + '<script>\n(function(){\n var body=document.getElementById(\'selbody\')', 1)

# rename the finder nav label to match the app's language
doc = doc.replace('>Selection table</a>', '>Plant finder</a>')

# update <title>
doc = doc.replace('<title>The Gangway Hosta Garden — 6 Plans for 95 Feet</title>',
                  '<title>The Gangway Hosta Garden — 6 designs + variations for 95 ft of shade</title>')

open(OUT, 'w', encoding='utf-8').write(doc)
print("WROTE", OUT, f"({len(doc)//1024} KB)")
