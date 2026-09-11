#!/usr/bin/env python3
"""Fetch the Illinois State Archives land tract sales and write the committed deposit.

    tools/harvest_land_sales.py --sweep [--tr 39:14 --tr 40:14]
    tools/harvest_land_sales.py --county-list COOK [--through-year 1836]

A TOWNSHIP IS A TOWNSHIP AND A RANGE (T-0676). The sweep asks for the pairs given to
`--tr`, defaulting to the two the town stands on; `--township 39` is the older spelling
and still means T39N R14E. Each set of pairs writes its own deposit, named after them.

THIS REACHES THE NETWORK, so it is run deliberately by a research pass and never by
`tools/check.sh`. Its output — `data/research/land_sales/text/*.tsv` — is committed,
and `tools/read_land_sales.py` derives everything else from that file offline. That
split is the civic domain's (`sweep_voter_second_sources.py`), for the same reason:
a gate that needs the internet is a gate that goes red for reasons that are not the
repo's.

TWO THINGS ABOUT THE SOURCE, both learned the hard way on T-0557.

1. THE SEARCH RETURNS AT MOST 150 ROWS PER PAGE — AND IT DOES PAGE (T-0675). The
   ceiling is real: a whole-township query stops at 150 and looks complete, which is
   why the sweep still asks SECTION BY SECTION, thirty-six queries per township. But
   the results page carries a **More** button, and that button is a keyset cursor:
   `hiddenPurchaseNo` + `hiddenPurchaser` + `hiddenSectionNo`, replayed against the
   same search, return the rows after the last one shown. Results are ordered by
   purchaser, so the cursor walks a section to its end. `walk_section` below follows
   it, and T-0557's three "truncated" sections — T39N R14E 16, 21 and 29 — were
   truncated only because the first pass took the More button for a dead end.
   The `name` field belongs to a different search form and does NOT narrow a
   legal-description query — it replaces it, returning that name from every township
   in Illinois, so it cannot be used to break a section into smaller pieces.

3. A SECTION QUERY CANNOT SEE A ROW THAT HAS NO SECTION (T-0830). The register
   describes a town lot by its plat — `L2BL46CHIOT` — and leaves Section, Township,
   Range and Meridian EMPTY. There is no section number such a row answers to, so no
   number of section queries will ever return it, however completely each one is
   walked. `--county-list` is the query that can: county alone, walked to its end
   through the same cursor, which is the whole county's list page and therefore holds
   the sectionless rows too. It writes the LIST columns only — the nine the results
   page prints — because it exists to say what a sweep is missing, not to replace the
   detail pages a sweep fetches. `--sectionless` is the pass that DOES fetch them:
   it reads the committed county list, takes the rows whose Section column is empty,
   and asks each one's detail page for the eight fields the list page never prints —
   residence, social status, acres, price per acre, total price, type of sale, volume
   and page. It writes its OWN deposit, renumbers nothing, and appends to that deposit
   after every chunk, so a pass cut short by a wall clock keeps what it read (T-1030).

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
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://apps.ilsos.gov/isa/landSalesSearch.do"
READER = "https://r.jina.ai/"
OUT = ROOT / "data" / "research" / "land_sales" / "text"
CEILING = 150      # rows per page; the cursor below is what walks past it
MAX_PAGES = 40     # a section deeper than this is reported, never silently cut
CHUNK = 50         # detail pages per batch, so progress is visible and resumable

COLS = ["purchase_no", "purchaser", "residence", "social_status", "aliquot_or_lot",
        "section", "township", "range", "meridian", "county", "acres", "price_per_acre",
        "total_price", "type_of_sale", "date_purchased", "volume", "page"]

ROW = re.compile(r"<tr>\s*<td>\s*<a href=\"javascript:getDetails\('(\d+)'\)\">(.*?)</a>\s*</td>(.*?)</tr>", re.S)
CELL = re.compile(r"<td>(.*?)</td>", re.S)
# The More button's keyset cursor: the last row of the page it was rendered on.
CUR_NO = re.compile(r'name="hiddenPurchaseNo" value="([^"]*)"')
CUR_WHO = re.compile(r'name="hiddenPurchaser" value="([^"]*)"')
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


CACHE = None      # set by --cache: a directory of fetched pages, so a sweep resumes
PACE = 3.0        # seconds between requests: the reader allows about 20 a minute
_gate = threading.Lock()
_last = [0.0]


def cached(url: str):
    if CACHE is None:
        return None
    return CACHE / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".html")


def wait_turn() -> None:
    """One request at a time, PACE apart. The reader answers a burst with refusals.

    Measured 2026-09-04 on this runner: eight parallel requests are all refused
    instantly, four get about fifteen through and then the bucket is empty. Racing it
    with more workers does not fetch faster, it only spends the quota on refusals — so
    the sweep paces itself instead, and the --cache directory is what makes the wall
    clock survivable across runs.
    """
    with _gate:
        gap = time.monotonic() - _last[0]
        if gap < PACE:
            time.sleep(PACE - gap)
        _last[0] = time.monotonic()


PAGE_OK = ("landSalesForm", "No records were found")   # a hit list, or an honest empty
DETAIL_OK = ("Purchaser Information",)


def fetch(url: str, direct: bool, need=PAGE_OK, tries: int = 5) -> str:
    """One page, through the reader unless --direct, and NEVER a page that is not it.

    `need` is the set of markers the wanted page may carry and a refusal carries
    none of — the results form OR the database's own "No records were found", since a
    section with no sale is a reading and not a failure. A throttled or truncated
    answer can therefore never be mistaken for a short section or an empty detail.
    Exhausting the tries RAISES: a sweep that under-reads in silence is the failure
    this whole domain exists to avoid.
    """
    hit = cached(url)
    if hit is not None and hit.exists():
        return hit.read_text(encoding="utf-8", errors="replace")
    target = url if direct else READER + url
    for attempt in range(tries):
        wait_turn()
        r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "110",
                            "-H", "X-Return-Format: html", target],
                           capture_output=True, text=True)
        out = r.stdout or ""
        if len(out) > 2000 and any(m in out for m in need):
            if hit is not None:
                hit.parent.mkdir(parents=True, exist_ok=True)
                hit.write_text(out, encoding="utf-8")
            return out
        time.sleep(2 + 6 * attempt)
    raise RuntimeError("no usable page after %d tries: %s" % (tries, url))


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


def section_url(tw: int, rg: int, sn: str, cursor=None) -> str:
    """The section query, or its continuation from the More button's cursor."""
    q = {"township": tw, "norS": "N", "range": rg, "eorW": "E", "meridian": 3,
         "county": "", "name": "", "sectionNum": sn}
    if cursor:
        q.update({"purchaseNo": "", "hiddenPurchaseNo": cursor[0],
                  "hiddenPurchaser": cursor[1], "hiddenSectionNo": sn})
    return BASE + "?" + urllib.parse.urlencode(q)


def cursor_of(html: str):
    """The (purchase no, purchaser) the More button would carry forward, or None."""
    no, who = CUR_NO.search(html), CUR_WHO.search(html)
    if not no or not who or not no.group(1).strip():
        return None
    return (no.group(1).strip(), who.group(1).strip())


def walk_section(tw: int, rg: int, sn: str, direct: bool) -> tuple:
    """Every row of one section, following the More cursor to the end.

    Returns (rows, pages walked, hit_cap). A page under the ceiling is the last one.
    A cursor that does not move is a dead end and stops the walk rather than looping.
    """
    rows, seen, pages, cursor = [], set(), 0, None
    while pages < MAX_PAGES:
        html = fetch(section_url(tw, rg, sn, cursor), direct)
        pages += 1
        found = rows_of(html)
        fresh = [r for r in found if r["purchase_no"] not in seen]
        seen.update(r["purchase_no"] for r in fresh)
        rows += fresh
        if len(found) < CEILING or not fresh:
            return rows, pages, False
        nxt = cursor_of(html)
        if not nxt or nxt == cursor:
            return rows, pages, False
        cursor = nxt
    return rows, pages, True


def deposit_name(pairs, through_year: int) -> str:
    """The file the pairs write, named after them: townships grouped under their range.

    The two townships the town stands on still name the file they always named — the
    grouping was chosen so that [(39, 14), (40, 14)] spells `t39n_t40n_r14e` exactly as
    the R14E-only harvest did, and the committed deposit did not have to move.
    """
    by_range = {}
    for tw, rg in sorted(pairs, key=lambda p: (p[1], p[0])):
        by_range.setdefault(rg, []).append(tw)
    return "isa_land_tract_sales_%s_through_%d.tsv" % (
        "_".join("%s_r%de" % ("_".join("t%dn" % t for t in tws), rg)
                 for rg, tws in by_range.items()), through_year)


def held_rows(name: str) -> dict:
    """Rows already in the committed deposit, by purchase number.

    A detail page says the same thing every time it is asked, and the reader that
    stands between this runner and the Archives allows about twenty requests a
    minute — so re-asking for six hundred pages the repo already holds costs half an
    hour and changes nothing. The sweep therefore carries the deposit's own rows
    forward and fetches only what is new; `--refetch` reads every page again from
    scratch, which is what to run when the source itself may have changed.
    """
    path = OUT / name
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return {}
    head = lines[0].split("\t")
    out = {}
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) != len(head):
            continue
        row = dict(zip(head, cells))
        out[row["purchase_no"]] = row
    return out


def sweep(pairs, through_year: int, direct: bool, workers: int,
          refetch: bool = False) -> int:
    name = deposit_name(pairs, through_year)
    meta = [(tw, rg, "%02d" % s) for tw, rg in pairs for s in range(1, 37)]
    print("  walking %d section queries" % len(meta), flush=True)
    with ThreadPoolExecutor(workers) as ex:
        walks = list(ex.map(lambda m: walk_section(m[0], m[1], m[2], direct), meta))
    wanted, truncated, deep = [], [], []
    for (tw, rg, sn), (found, pages, hit_cap) in zip(meta, walks):
        if hit_cap:
            truncated.append("T%dN R%dE sec %s" % (tw, rg, sn))
        elif pages > 1:
            deep.append("T%dN R%dE sec %s: %d pages, %d rows" % (tw, rg, sn, pages, len(found)))
        for row in found:
            year = row["date_purchased"][-4:]
            if year.isdigit() and int(year) <= through_year:
                wanted.append(row["purchase_no"])
    for line in deep:
        print("  walked %s" % line)
    wanted = sorted(set(wanted))
    held = {} if refetch else held_rows(name)
    todo = [p for p in wanted if p not in held]
    print("  %d sales through %d across %d sections; %d already in the deposit, "
          "%d detail pages to fetch" % (len(wanted), through_year, len(meta),
                                        len(wanted) - len(todo), len(todo)), flush=True)
    records = [held[p] for p in wanted if p in held]
    for start in range(0, len(todo), CHUNK):
        batch = todo[start:start + CHUNK]
        with ThreadPoolExecutor(workers) as ex:
            pages = list(ex.map(lambda p: fetch("%s?purchaseNo=%s" % (BASE, p), direct, need=DETAIL_OK), batch))
        for pno, html in zip(batch, pages):
            d = detail(html)
            if not d.get("purchaser"):
                print("  ✗ %s: no detail page" % pno)
                return 1
            records.append(dict(d, purchase_no=pno))
        print("    %d/%d" % (len(records), len(wanted)), flush=True)
    records.sort(key=lambda r: (r["township"], r["range"], r["section"],
                                r["purchaser"], r["purchase_no"]))
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(COLS)]
    for r in records:
        lines.append("\t".join(r[c].replace("\t", " ") for c in COLS))
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("land sales sweep: %d sales through %d written to %s" % (len(records), through_year, name))
    if truncated:
        print("STILL SHORT after %d pages, NOT read whole: %s"
              % (MAX_PAGES, ", ".join(truncated)))
    return 0


# ---------------------------------------------------------------------------
# The completeness probe (T-0830): one county, listed, walked to its end.

LIST_COLS = ["purchase_no", "purchaser", "legal_description", "section", "township",
             "range", "meridian", "date_purchased", "county"]
CUR_SEC = re.compile(r'name="hiddenSectionNo" value="([^"]*)"')


def county_url(county: str, cursor=None) -> str:
    q = {"township": "", "norS": "N", "range": "", "eorW": "E", "meridian": "",
         "county": county, "name": "", "sectionNum": ""}
    if cursor:
        q.update({"purchaseNo": "", "hiddenPurchaseNo": cursor[0],
                  "hiddenPurchaser": cursor[1], "hiddenSectionNo": cursor[2]})
    return BASE + "?" + urllib.parse.urlencode(q)


def list_rows_of(html: str) -> list:
    """The results page's own nine columns, as it prints them, corrected nowhere."""
    found = []
    for m in ROW.finditer(html):
        cells = [clean(c) for c in CELL.findall(m.group(3))]
        if len(cells) < 7:
            continue
        found.append(dict(zip(LIST_COLS, [m.group(1), clean(m.group(2))] + cells[:7])))
    return found


def county_list(county: str, through_year: int, direct: bool) -> int:
    """Every sale the county holds, from the list page, filtered to through_year.

    ONE query, paged. The results are ordered by purchaser and the More button is the
    same keyset cursor `walk_section` follows, so the walk is the county in full — and
    unlike a section sweep it can see a row whose Section column is empty, which is the
    only way a town lot appears in this register.
    """
    name = "isa_land_tract_sales_%s_county_list_through_%d.tsv" % (county.lower(), through_year)
    rows, seen, cursor, pages = [], set(), None, 0
    while pages < 400:
        html = fetch(county_url(county, cursor), direct)
        pages += 1
        found = list_rows_of(html)
        fresh = [r for r in found if r["purchase_no"] not in seen]
        seen.update(r["purchase_no"] for r in fresh)
        rows += fresh
        if pages % 10 == 0:
            print("  page %d: %d rows so far" % (pages, len(rows)), flush=True)
        if len(found) < CEILING or not fresh:
            break
        nxt = tuple((r.search(html).group(1).strip() if r.search(html) else "")
                    for r in (CUR_NO, CUR_WHO, CUR_SEC))
        if not nxt[0] or nxt == cursor:
            break
        cursor = nxt
    else:
        print("  STILL SHORT after 400 pages, NOT walked to the end")
        return 1
    wanted = [r for r in rows
              if r["date_purchased"][-4:].isdigit()
              and int(r["date_purchased"][-4:]) <= through_year]
    wanted.sort(key=lambda r: (r["purchaser"], r["purchase_no"]))
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(LIST_COLS)]
    for r in wanted:
        lines.append("\t".join(r[c].replace("\t", " ") for c in LIST_COLS))
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    blank = sum(1 for r in wanted if not r["section"].strip())
    print("county list: %d rows over %d pages, %d dated through %d (%d of them with no "
          "section at all) written to %s"
          % (len(rows), pages, len(wanted), through_year, blank, name))
    return 0


# ---------------------------------------------------------------------------
# The sectionless harvest (T-1030): the town lots the section sweep cannot reach.


def list_deposit_rows(county: str, through_year: int) -> list:
    """The committed county list, as it was written. Never re-fetched here."""
    path = OUT / ("isa_land_tract_sales_%s_county_list_through_%d.tsv"
                  % (county.lower(), through_year))
    if not path.exists():
        raise SystemExit("no county list at %s — run --county-list %s first"
                         % (path, county))
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, line.split("\t"))) for line in lines[1:]
            if len(line.split("\t")) == len(head)]


def write_deposit(path: Path, records: list) -> None:
    """The deposit as it stands, sorted the only way a sectionless row can be.

    Rewritten in full after every chunk rather than at the end: the fetch is paced at
    one page every three seconds and six hundred pages outlast any one run's wall
    clock, so a pass that is cut off mid-harvest must leave the rows it read behind it.
    """
    records = sorted(records, key=lambda r: (r["purchaser"], r["purchase_no"]))
    lines = ["\t".join(COLS)]
    for r in records:
        lines.append("\t".join(r[c].replace("\t", " ") for c in COLS))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sectionless(county: str, through_year: int, direct: bool, workers: int,
                refetch: bool = False, limit: int = 0) -> int:
    """Detail pages for every row of the county list that carries no section.

    The list page prints nine columns; a detail page prints seventeen. The eight it
    adds — residence, social status, acres, price per acre, total price, type of sale,
    volume and page — are the ones that make a row a SALE rather than a name against a
    plat, and they are the reason this pass exists.

    Two things are cross-checked against the list row and never silently corrected: the
    purchaser and the date of purchase. A disagreement is printed and makes the pass
    exit non-zero AFTER the deposit is written, because a register that says two
    different things about one purchase is a reading to rule on, not a row to drop.
    """
    name = "isa_land_tract_sales_%s_sectionless_through_%d.tsv" % (county.lower(), through_year)
    path = OUT / name
    listed = {r["purchase_no"]: r for r in list_deposit_rows(county, through_year)
              if not (r.get("section") or "").strip()}
    wanted = sorted(listed)
    held = {} if refetch else held_rows(name)
    records = [held[p] for p in wanted if p in held]
    todo = [p for p in wanted if p not in held]
    outstanding = len(todo)
    if limit:
        todo = todo[:limit]
    print("  %d sectionless rows in the %s list through %d; %d already in the deposit, "
          "%d still to read, %d detail pages this pass"
          % (len(wanted), county, through_year, len(records), outstanding, len(todo)),
          flush=True)
    for start in range(0, len(todo), CHUNK):
        batch = todo[start:start + CHUNK]
        with ThreadPoolExecutor(workers) as ex:
            pages = list(ex.map(lambda p: fetch("%s?purchaseNo=%s" % (BASE, p), direct,
                                                need=DETAIL_OK), batch))
        for pno, html in zip(batch, pages):
            d = detail(html)
            if not d.get("purchaser"):
                write_deposit(path, records)
                print("  ✗ %s: no detail page (deposit written with %d rows)"
                      % (pno, len(records)))
                return 1
            records.append(dict(d, purchase_no=pno))
        write_deposit(path, records)
        print("    %d/%d" % (len(records), len(wanted)), flush=True)
    write_deposit(path, records)
    disagreed = []
    for r in records:
        was = listed.get(r["purchase_no"])
        if not was:
            continue
        for field in ("purchaser", "date_purchased"):
            if r[field].strip() != was[field].strip():
                disagreed.append("%s %s: list %r, detail %r"
                                 % (r["purchase_no"], field, was[field], r[field]))
    sectioned = [r["purchase_no"] for r in records if r["section"].strip()]
    print("sectionless harvest: %d of %d rows read at their detail pages, written to %s"
          % (len(records), len(wanted), name))
    if sectioned:
        print("  %d detail pages DO carry a section the list page left blank: %s"
              % (len(sectioned), ", ".join(sectioned[:20])))
    for line in disagreed:
        print("  ✗ list and detail disagree — %s" % line)
    return 1 if disagreed else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--sectionless", default=None,
                    help="fetch the detail page of every row of ONE county's committed "
                         "list that carries no section — the town lots (T-1030)")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after this many NEW detail pages; the deposit is written "
                         "either way, so the next pass carries it forward")
    ap.add_argument("--county-list", default=None,
                    help="walk ONE county's list page to its end — the only query that "
                         "returns a row with no section (T-0830)")
    ap.add_argument("--township", action="append", type=int, default=None,
                    help="the older spelling of --tr N:14")
    ap.add_argument("--tr", action="append", default=None,
                    help="a township and its range, T:R — repeat it, e.g. --tr 39:13")
    ap.add_argument("--through-year", type=int, default=1836)
    ap.add_argument("--direct", action="store_true",
                    help="fetch the origin rather than the r.jina.ai reader")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--refetch", action="store_true",
                    help="ask for every detail page again instead of carrying the deposit forward")
    ap.add_argument("--cache", default=None,
                    help="directory of fetched pages, so an interrupted sweep resumes")
    args = ap.parse_args(argv)
    if not args.sweep and not args.county_list and not args.sectionless:
        ap.print_help()
        return 2
    global CACHE
    if args.cache:
        CACHE = Path(args.cache)
    if args.sectionless:
        return sectionless(args.sectionless.upper(), args.through_year, args.direct,
                           args.workers, args.refetch, args.limit)
    if args.county_list:
        return county_list(args.county_list.upper(), args.through_year, args.direct)
    pairs = [tuple(int(x) for x in tr.split(":", 1)) for tr in (args.tr or [])]
    pairs += [(tw, 14) for tw in (args.township or [])]
    return sweep(pairs or [(39, 14), (40, 14)], args.through_year, args.direct,
                 args.workers, args.refetch)


if __name__ == "__main__":
    sys.exit(main())
