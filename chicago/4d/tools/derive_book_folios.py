#!/usr/bin/env python3
"""Read the printed folios off a Moses and Kirkland volume's OCR — T-0826.

THE FOLIO RULE IS RE-DERIVED HERE AND NOT ASSUMED. T-0581 established that volume 1
prints its own page numbers into the OCR and that the number is READ off the nearest
preceding running head rather than counted, with verso heads even and recto heads
odd as the check. T-0826's acceptance requires that rule re-derived for volume 2
rather than carried over, because a second volume of the same work need not be set
the same way. This script is that derivation, and it reports the evidence:

  --audit   the whole folio sequence, its parity, and every numeral the parity
            check refuses
  --at N    the printed page a given line of the committed text stands on

WHAT THE DERIVATION FOUND FOR VOLUME 2 (1895, the same UIUC copy, scanned in the
same batch): THE RULE HOLDS, and it holds in the stronger of the two possible
ways. A head is a line of small caps — 'HISTORY OF CHICAGO.' on a verso, the
chapter's own title on a recto — with the folio alone on a line within six lines of
it. Volume 2's verso heads carry 'HISTORY OF CHICAGO.'; 319 of them survive, 271
with their numeral, and 256 of those 271 are EVEN. All fifteen odd ones fall inside
an otherwise-even run and the parity check refuses every one: the numeral at the
head above line 5884 reads '43' between 38, 40 and 44, 46, and eleven of the fifteen
are the OCR setting a 3 where the page prints a 2. That is the same fault, caught
the same way, as the '93' volume 1's parity refused at its line 13147.

So a locator in this volume names a page the same way one in volume 1 does, and
where a head's numeral did not survive at all (48 of the 319) the page is carried
between two read folios and the locator says so on itself.

usage:
  derive_book_folios.py --text <path> --audit
  derive_book_folios.py --text <path> --at <line> [--at <line> ...]
"""
import argparse, re, sys
from pathlib import Path

BARE = re.compile(r'^\s*(\d{1,3})\s*$')
VERSO_HEAD = re.compile(r'H[I1l]ST[O0]R[YT7] +[O0][FE] +CH[I1]C *A *G *[O0]', re.I)
NEAR = 6  # the folio stands alone within this many lines above its head


def verso_heads(lines):
    """Every verso running head, with the numeral printed above it where it survived.

    Returns (head_line, numeral_line or None, numeral or None) in document order.
    """
    out = []
    for i, l in enumerate(lines, 1):
        if not VERSO_HEAD.search(l):
            continue
        found = (None, None)
        for j in range(i - 1, max(0, i - NEAR - 1), -1):
            m = BARE.match(lines[j - 1])
            if m:
                found = (j, int(m.group(1)))
                break
        out.append((i, found[0], found[1]))
    return out


def parity_corrected(heads):
    """Apply the parity check: a verso folio is EVEN, and an odd one is the OCR and
    not the page — but only where the run says which even page it must be.

    The candidate is n-1 or n+1, and it is accepted only if exactly one of them
    falls strictly between the nearest surviving numerals either side. That refusal
    matters: the head above line 80964 reads '39' between 638 and 640, so neither 38
    nor 40 can be the page, the numeral is a lost digit rather than a flipped one,
    and the honest answer is that this page is carried between two read folios. A
    rule that always corrected would have printed page 38 six hundred pages late.
    """
    raw = [(h, j, n) for h, j, n in heads]
    rows = []
    for k, (h, j, n) in enumerate(raw):
        if n is None:
            rows.append((h, j, None, 'numeral did not survive the OCR'))
            continue
        if n % 2 == 0:
            rows.append((h, j, n, 'read'))
            continue
        prev = next((x[2] for x in reversed(raw[:k]) if x[2] is not None), None)
        nxt = next((x[2] for x in raw[k + 1:] if x[2] is not None), None)
        fits = [c for c in (n - 1, n + 1)
                if c % 2 == 0
                and (prev is None or c > prev)
                and (nxt is None or c < nxt)]
        if len(fits) == 1:
            rows.append((h, j, fits[0], f"parity-corrected from the OCR's {n}"))
        else:
            rows.append((h, j, None,
                         f"odd numeral {n} refused by the parity check and not "
                         f"correctable inside the run ({prev} .. {nxt})"))
    return rows


def plausible_step(rows, max_step=40):
    """Refuse a folio whose STEP from the last one kept cannot be a run of pages.

    Parity cannot catch an even misread, and the volume has them: the head above
    line 34064 reads '392' where the run goes 288, 290, ..., 298, 300, and the one
    above 34489 reads '200' in the same stretch. Both are even, both pass the parity
    check, and both are wrong. What refuses them is the one thing the page order
    guarantees — CONSECUTIVE VERSO HEADS ARE TWO PAGES APART, so a surviving head's
    folio is 2 more than the last one kept, or more than that by twice the number of
    heads whose numerals the OCR lost in between. A step that is negative, odd, or
    larger than forty pages is not a page run, and the pages around it are carried
    between the two nearest folios that are.
    """
    kept = []
    out = []
    for h, j, folio, how in rows:
        if folio is None:
            out.append((h, j, None, how))
            continue
        last = kept[-1] if kept else None
        if last is not None:
            step = folio - last
            if step <= 0 or step % 2 or step > max_step:
                out.append((h, j, None,
                            f'numeral {folio} refused: a step of {step} from the '
                            f'last read folio {last} is not a run of pages'))
                continue
        kept.append(folio)
        out.append((h, j, folio, how))
    return out


def audit(lines):
    heads = verso_heads(lines)
    rows = plausible_step(parity_corrected(heads))
    withnum = [r for r in rows if r[2] is not None]
    corrected = [(h, j) for (h, j, f, how) in rows if how.startswith('parity')]
    refused = [(h, j, how) for (h, j, f, how) in rows if how.startswith('odd numeral')]
    print(f"lines: {len(lines)}")
    print(f"verso running heads: {len(heads)}")
    print(f"  with a numeral above them: {len(withnum)}")
    print(f"  numeral lost to the OCR:   {len(heads) - len(withnum)}")
    raw = [n for _, _, n in heads if n is not None]
    print(f"raw verso numerals: even {sum(1 for n in raw if n % 2 == 0)}, odd {sum(1 for n in raw if n % 2)}")
    print(f"the parity check rejects all {sum(1 for n in raw if n % 2)} odd numerals.")
    print(f"{len(corrected)} are correctable inside their run:")
    for h, j in corrected:
        k = [x for x, r in enumerate(rows) if r[0] == h][0]
        nb = [rows[x][2] for x in range(max(0, k - 2), min(len(rows), k + 3))]
        rawn = [r for r in heads if r[0] == h][0][2]
        print(f"  line {j}: OCR {rawn} -> {rows[k][2]}   run {nb}")
    print(f"{len(refused)} are not, so those pages are carried between read folios:")
    for h, j, how in refused:
        print(f"  line {j}: {how}")
    return 0


def at(lines, line_no):
    """The printed page a line of the committed text stands on.

    Between two consecutive verso heads there is exactly one verso page and one
    recto page, so a line after a verso head at folio V is on V or V+1; the recto
    head printing V+1 decides which where it survived. Where the run skips a head
    the page is CARRIED between two read folios and this says so.
    """
    rows = [r for r in plausible_step(parity_corrected(verso_heads(lines))) if r[2] is not None]
    before = [r for r in rows if r[1] < line_no]
    after = [r for r in rows if r[1] > line_no]
    if not before:
        n = after[0][2] if after else None
        return ('on a page before the first read verso folio'
                + (f' ({n} at line {after[0][1]})' if n else ''))
    h, j, folio, how = before[-1]
    note = '' if how == 'read' else f' ({how})'
    if after and after[0][2] != folio + 2:
        return (f'carried between read folios {folio}{note} at line {j} and '
                f'{after[0][2]} at line {after[0][1]}')
    hi = after[0][1] if after else len(lines)
    recto = None
    for i in range(h + 1, min(hi, line_no)):
        m = BARE.match(lines[i - 1])
        if m and int(m.group(1)) == folio + 1:
            recto = i
    if recto:
        return f'printed page {folio + 1} (recto head read at line {recto})'
    return f'printed page {folio} or {folio + 1}{note}, read off the verso head at line {j}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--text', required=True)
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--at', type=int, action='append', default=[])
    a = ap.parse_args()
    lines = Path(a.text).read_text(encoding='utf-8', errors='replace').split('\n')
    if a.audit:
        audit(lines)
    for L in a.at:
        print(f"line {L}: {at(lines, L)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
