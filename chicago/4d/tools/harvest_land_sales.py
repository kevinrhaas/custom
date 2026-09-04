#!/usr/bin/env python3
"""Fetch the Illinois State Archives land tract sales and write the committed deposit.

    tools/harvest_land_sales.py --sweep [--township 39 --township 40] [--range 14]

THIS REACHES THE NETWORK, so it is run deliberately by a research pass and never by
`tools/check.sh`. Its output — `data/research/land_sales/text/*.tsv` — is committed,
and `tools/read_land_sales.py` derives everything else from that file offline. That
split is the civic domain's (`sweep_voter_second_sources.py`), for the same reason:
a gate that needs the internet is a gate that goes red for reasons that are not the
repo's.

TWO THINGS ABOUT THE SOURCE, both learned the hard way on T-0557.

1. THE SEARCH RETURNS AT MOST 150 ROWS AND HAS NO PAGING. A whole-township query
   silently stops at 150 and looks complete. So the sweep asks SECTION BY SECTION,
   thirty-six queries per township, and any section that comes back with exactly 150
   rows is reported as TRUNCATED rather than read. The `name` field belongs to a
   different search form and does NOT narrow a legal-description query — it replaces
   it, returning that name from every township in Illinois, so it cannot be used to
   break a section into smaller pieces. T-0677 went back over the form and confirmed
   there is no fourth axis: the page offers section/township/range/meridian,
   township/range/meridian, and county — which it says "cannot be used in combination
   with any other search criteria" — and the result page carries no paging, offset or
   sort parameter. SECTION IS THE FINEST GRAIN THE SOURCE OFFERS, so a truncated
   section needs a different source, not a cleverer query. T-0678 holds that.

2. THE SITE REFUSES DATACENTRE ADDRESSES. Every user agent from this runner's Azure
   address gets a bare 403 from the WAF. The sweep therefore fetches through the
   public r.jina.ai reader, which returns the origin's own HTML unchanged; the
   `--direct` flag asks for the origin instead, for anyone running this from a
   machine the site will talk to. Which route was used is recorded in the source
   record, and it changes nothing about what the page says.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://apps.ilsos.gov/isa/landSalesSearch.do"
READER = "https://r.jina.ai/"
OUT = ROOT / "data" / "research" / "land_sales" / "text"
CEILING = 150

COLS = ["purchase_no", "purchaser", "residence", "social_status", "aliquot_or_lot",
        "section", "township", "range", "meridian", "county", "acres", "price_per_acre",
        "total_price", "type_of_sale", "date_purchased", "volume", "page"]

ROW = re.compile(r"<tr>\s*<td>\s*<a href=\"javascript:getDetails\('(\d+)'\)\">(.*?)</a>\s*</td>(.*?)</tr>", re.S)
CELL = re.compile(r"<td>(.*?)</td>", re.S)
LABELS = [("purchaser", "Purchaser"), ("residence", "Residence"),
          ("social_status", "Social Status"), ("aliquot_or_lot", "Aliquot Parts or Lot"),
          ("section", "Section Number"), ("township", "Township"), ("range", "Range"),
          ("meridian", "Meridian"), ("county", "County of Purchase"), ("acres", "Acres"),
          ("price_per_acre", "Price per Acre"), ("total_price", "Total Price"),
          ("type_of_sale", "Type of Sale"), ("date_purchased", "Date of Purchase"),
          ("volume", "Volume"), ("page", "Page")]
STOP = {label for _, label in LABELS} | {"Legal Description", "Details of Sale",
                                         "Purchaser Information", "Search Criteria:"}


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


# A sweep is 36 section queries plus one detail page per sale, and the reader proxy
# drops a page now and then for reasons that have nothing to do with the register. The
# cache is what stops a dropped page costing the whole sweep its work again: it is a
# scratch directory outside the repo (`--cache`, default $LAND_SALES_CACHE or none),
# never committed, and it holds only pages that came back whole.
CACHE = os.environ.get("LAND_SALES_CACHE") or ""


def _ok(html: str) -> bool:
    return len(html) > 2000 and ("Search Criteria" in html or "landSalesSearch" in html)


def fetch(url: str, direct: bool, tries: int = 4) -> str:
    slot = None
    if CACHE:
        slot = Path(CACHE) / (hashlib.sha1(url.encode()).hexdigest() + ".html")
        if slot.exists():
            cached = slot.read_text(encoding="utf-8", errors="replace")
            if _ok(cached):
                return cached
    target = url if direct else READER + url
    out = ""
    for attempt in range(tries):
        r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "110",
                            "-H", "X-Return-Format: html", target],
                           capture_output=True, text=True)
        out = r.stdout or ""
        if _ok(out):
            if slot is not None:
                slot.parent.mkdir(parents=True, exist_ok=True)
                slot.write_text(out, encoding="utf-8")
            return out
        time.sleep(3 + 4 * attempt)
    return out


def rows_of(html: str) -> list:
    found = []
    for m in ROW.finditer(html):
        cells = [clean(c) for c in CELL.findall(m.group(3))]
        if len(cells) < 7:
            continue
        found.append({"purchase_no": m.group(1), "purchaser": clean(m.group(2)),
                      "date_purchased": cells[5]})
    return found


def detail(html: str) -> dict:
    flat = [x for x in (re.sub(r"\s+", " ", c).strip()
                        for c in re.sub(r"\x01+", "\x01", re.sub(r"<[^>]+>", "\x01", html)).split("\x01"))
            if x]
    out = {}
    for key, label in LABELS:
        try:
            i = flat.index(label)
        except ValueError:
            out[key] = ""
            continue
        nxt = flat[i + 1] if i + 1 < len(flat) else ""
        out[key] = "" if (nxt in STOP or nxt.startswith("Quick Links")) else nxt
    return out


def sweep(townships, rng: int, through_year: int, direct: bool, workers: int) -> int:
    urls, meta = [], []
    for tw in townships:
        for s in range(1, 37):
            sn = "%02d" % s
            urls.append("%s?township=%d&norS=N&range=%d&eorW=E&meridian=3&county=&name=&sectionNum=%s"
                        % (BASE, tw, rng, sn))
            meta.append((tw, sn))
    with ThreadPoolExecutor(workers) as ex:
        pages = dict(zip(urls, ex.map(lambda u: fetch(u, direct), urls)))
    # A SECTION PAGE THE PROXY DROPPED LOOKS EXACTLY LIKE A SECTION WITH NO SALES —
    # `rows_of` finds no rows in an error body and the sweep would write the section
    # off as read and empty. So every section query is checked for a page that is
    # actually the search's own, retried on its own, and the sweep refuses to write a
    # deposit while one is still missing.
    for _ in range(3):
        missing = [u for u in urls if not _ok(pages[u])]
        if not missing:
            break
        print("  … re-fetching %d section page(s) the reader dropped" % len(missing))
        time.sleep(10)
        with ThreadPoolExecutor(max(1, workers // 2)) as ex:
            pages.update(zip(missing, ex.map(lambda u: fetch(u, direct), missing)))
    missing = [m for m, u in zip(meta, urls) if not _ok(pages[u])]
    if missing:
        print("  ✗ %d section page(s) never came back — nothing written: %s"
              % (len(missing), ", ".join("T%dN R%dE sec %s" % (tw, rng, sn)
                                         for tw, sn in missing)))
        return 1
    wanted, truncated = [], []
    for (tw, sn), url in zip(meta, urls):
        html = pages[url]
        found = rows_of(html)
        if len(found) >= CEILING:
            truncated.append("T%dN R%dE sec %s" % (tw, rng, sn))
        for row in found:
            year = row["date_purchased"][-4:]
            if year.isdigit() and int(year) <= through_year:
                wanted.append(row["purchase_no"])
    wanted = sorted(set(wanted))
    def detail_page(pno: str) -> str:
        return fetch("%s?purchaseNo=%s" % (BASE, pno), direct)

    with ThreadPoolExecutor(workers) as ex:
        pages = dict(zip(wanted, ex.map(detail_page, wanted)))
    # A page the proxy dropped is not a page the register does not have, so a miss is
    # retried on its own before the sweep gives up on it. It gives up loudly: a sweep
    # that wrote a deposit missing a sale it had already seen in a summary row would be
    # a hole that looks like a complete read.
    for _ in range(3):
        missing = [p for p in wanted if not detail(pages[p]).get("purchaser")]
        if not missing:
            break
        print("  … re-fetching %d detail page(s) the reader dropped" % len(missing))
        time.sleep(10)
        with ThreadPoolExecutor(max(1, workers // 2)) as ex:
            pages.update(zip(missing, ex.map(detail_page, missing)))
    records = []
    for pno in wanted:
        d = detail(pages[pno])
        if not d.get("purchaser"):
            print("  ✗ %s: no detail page after four attempts — nothing written" % pno)
            return 1
        records.append(dict(d, purchase_no=pno))
    records.sort(key=lambda r: (r["township"], r["section"], r["purchaser"], r["purchase_no"]))
    OUT.mkdir(parents=True, exist_ok=True)
    name = "isa_land_tract_sales_t%s_r%de_through_%d.tsv" % (
        "_t".join("%dn" % t for t in townships), rng, through_year)
    lines = ["\t".join(COLS)]
    for r in records:
        lines.append("\t".join(r[c].replace("\t", " ") for c in COLS))
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("land sales sweep: %d sales through %d written to %s" % (len(records), through_year, name))
    if truncated:
        print("TRUNCATED at the database's %d-row ceiling, NOT read whole: %s"
              % (CEILING, ", ".join(truncated)))
    return 0


def main(argv=None) -> int:
    global CACHE
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--township", action="append", type=int, default=None)
    ap.add_argument("--range", dest="rng", type=int, default=14,
                    help="range east of the third principal meridian (default 14)")
    ap.add_argument("--through-year", type=int, default=1836)
    ap.add_argument("--direct", action="store_true",
                    help="fetch the origin rather than the r.jina.ai reader")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cache", default=CACHE,
                    help="scratch directory for fetched pages, outside the repo")
    args = ap.parse_args(argv)
    CACHE = args.cache
    if not args.sweep:
        ap.print_help()
        return 2
    return sweep(args.township or [39, 40], args.rng, args.through_year, args.direct,
                 args.workers)


if __name__ == "__main__":
    sys.exit(main())
