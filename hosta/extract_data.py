#!/usr/bin/env python3
"""Extract the 74-variety Lurvey catalog from the finder table into structured
JSON (the refreshable 'base data'). Writes site/hosta/data/lurvey-hostas.json."""
import re, json, html as H, os

doc = open("hosta_gangway_guide_v3.html", encoding="utf-8").read()
sel = re.search(r'<tbody id="selbody">(.*?)</tbody>', doc, re.S).group(1)
rows = re.findall(r'<tr\b([^>]*)>(.*?)</tr>', sel, re.S)

def A(attrs, k):
    m = re.search(k + r'="([^"]*)"', attrs); return m.group(1) if m else ""
def txt(s): return H.unescape(re.sub(r'<[^>]+>', '', s)).strip()

records = []
for at, body in rows:
    def cell(cls):
        m = re.search(r'<td class="' + cls + r'"[^>]*>(.*?)</td>', body, re.S)
        return m.group(1) if m else ""
    nm = cell("c-nm")
    a = re.search(r'<a href="([^"]*)"[^>]*>(.*?)</a>', nm)
    url = a.group(1) if a else ""
    name = txt(a.group(2)) if a else ""
    img = re.search(r'<img[^>]*src="([^"]*)"', nm)
    note = re.search(r'<div class="nt">(.*?)</div>', nm)
    ft = cell("c-ft"); zn = cell("c-zn"); pr = cell("c-pr")
    fitm = re.search(r'<span class="fit (\w)">(.*?)</span>', ft)
    znm = re.search(r'<span class="zn (\w)">(.*?)</span>', zn)
    stockm = re.search(r'<span class="b (\w+)">(.*?)</span>', pr)
    sizes = [{"label": txt(re.sub(r'\$[\d.]+', '', s[1])).strip() or txt(s[1]),
              "text": txt(s[1]), "inStock": s[0] == "in"}
             for s in re.findall(r'<span class="sz (in|out)">(.*?)</span>', pr)]
    catlabel = txt(cell("c-cat"))
    records.append({
        "category": int(A(at, "data-cat")),
        "categoryLabel": catlabel,
        "name": name,
        "url": url,
        "image": img.group(1) if img else "",
        "star": "star" in nm,
        "note": txt(note.group(1)) if note else "",
        "color": txt(cell("c-col")),
        "leafSize": txt(cell("c-sz")),
        "spacing": txt(cell("c-sp")),
        "light": txt(cell("c-li")),
        "spreadFt": float(A(at, "data-w") or 0),
        "heightIn": int(A(at, "data-h") or 0),
        "fit": A(at, "data-fits"),
        "fitLabel": txt(fitm.group(2)) if fitm else "",
        "fitClass": fitm.group(1) if fitm else "",
        "zone": A(at, "data-zone"),
        "zoneLabel": txt(znm.group(2)) if znm else "",
        "zoneClass": znm.group(1) if znm else "",
        "price": float(A(at, "data-price") or 0),
        "inStock": A(at, "data-stock") == "1",
        "stockLabel": txt(stockm.group(2)) if stockm else "",
        "sizes": sizes,
        "plansUsed": int(A(at, "data-plans") or 0),
        "search": txt(A(at, "data-q")),
    })

out = {
    "$schema": "lurvey-hostas/v1",
    "source": "https://lurveys.com/shop/?_sf_s=Hosta",
    "retailer": "Lurvey Home & Garden Supply",
    "pulledAt": "2026-07-16",
    "note": "Prices are standard-pot list, pre-tax. Stock reflects the day of the pull. "
            "Regenerate with the spec in lurvey-spec.md.",
    "count": len(records),
    "records": records,
}
os.makedirs("../site/hosta/data", exist_ok=True)
json.dump(out, open("../site/hosta/data/lurvey-hostas.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
# compact copy for embedding in the page
json.dump(out, open("_lurvey_embed.json", "w", encoding="utf-8"),
          separators=(",", ":"), ensure_ascii=False)
print(f"extracted {len(records)} records")
# quick sanity: categories present
cats = sorted(set(r["category"] for r in records))
print("categories:", cats)
print("with star:", sum(1 for r in records if r["star"]),
      "| out of stock:", sum(1 for r in records if not r["inStock"]))
