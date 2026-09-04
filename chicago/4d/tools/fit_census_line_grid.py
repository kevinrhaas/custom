#!/usr/bin/env python3
"""fit_census_line_grid.py — how many writing lines an unruled 1840 continuation
sheet carries, and which line each number stands on.

## Why this exists

The right-hand (continuation) sheets of the 1840 population schedule are ruled
VERTICALLY ONLY: `read_census_continuation.py` measured it on 33S7-9YYJ-5V and
found no horizontal rule anywhere inside the body. So a number's ROW cannot be
counted off the form, and every pass that tried to cluster the TOTAL column's own
ink got a different answer — 28 "to the nearest line" from the inventory, 31 from
one threshold, 34 from another, and a page file that had to record "29 to 31,
favouring 31" rather than a figure.

This tool does not look at the TOTAL column at all. It fits a line grid to the
ENUMERATOR'S OTHER INK — the y of every entry in the written industry columns,
which are read, closed against their own printed footings, and therefore not in
dispute — and reports which line count that ink actually supports. The TOTAL
column is then read AGAINST that grid rather than used to build it, so the row
index and the numbers are independent of each other.

## The measurement

For each candidate pitch and origin it assigns every anchor to its nearest line,
rejects any fit that puts two anchors on one line, and scores the fit by the rms
of the residuals. Reporting the best fit PER LINE COUNT is the point: a line count
is only believable if it beats the alternatives, and on 33S7-9YYJ-5V it does, by
a factor of two and a bit.

    $ python3 tools/fit_census_line_grid.py 33S7-9YYJ-5V
    lines=28  rms  19.78  pitch 83.06
    lines=29  rms  21.27  pitch 78.02
    lines=30  rms   6.64  pitch 75.86   <- best
    lines=31  rms  19.08  pitch 72.76

Anchors are read from the page file's own `column_closure` block (`entry_y`), so
the tool has no numbers typed into it and re-runs against whatever that block
holds. Two anchors within `--same-line` px of each other are one line (the
industry columns are exclusive, but two of them can carry an entry for the same
family, and on 5V three pairs do).
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def anchors_from_page(page, same_line):
    ys = []
    for col in page.get('column_closure', {}).values():
        ys.extend(col.get('entry_y') or [])
    ys.sort()
    merged = []
    for y in ys:
        if merged and y - merged[-1][-1] <= same_line:
            merged[-1].append(y)
        else:
            merged.append([y])
    return [round(sum(g) / len(g)) for g in merged]


def fit(anchors, lo, hi):
    best = {}
    for bi in range(int(lo * 100), int(hi * 100) + 1):
        b = bi / 100
        for d in range(-40, 41):
            a0 = anchors[0] + d / 2
            ns, s = [], 0.0
            for y in anchors:
                n = round((y - a0) / b)
                ns.append(n)
                s += (y - (a0 + b * n)) ** 2
            if len(set(ns)) < len(ns):
                continue
            lines = max(ns) + 1
            rms = (s / len(anchors)) ** 0.5
            if lines not in best or rms < best[lines][0]:
                best[lines] = (rms, b, a0, tuple(ns))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image_id')
    ap.add_argument('--same-line', type=int, default=30,
                    help='two anchors this close in y are the same writing line')
    ap.add_argument('--pitch-min', type=float, default=60.0)
    ap.add_argument('--pitch-max', type=float, default=90.0)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--jackknife', action='store_true',
                    help='refit with each anchor dropped in turn; a line count that '
                         'survives every drop is not resting on one entry')
    a = ap.parse_args()

    path = os.path.join(HERE, 'data/research/census_1840/pages/%s.json' % a.image_id)
    page = json.load(open(path))
    anchors = anchors_from_page(page, a.same_line)
    if len(anchors) < 6:
        sys.exit('%s: only %d anchors in column_closure — not enough to fit a grid'
                 % (a.image_id, len(anchors)))
    best = fit(anchors, a.pitch_min, a.pitch_max)
    if not best:
        sys.exit('%s: no fit assigns every anchor its own line' % a.image_id)
    win = min(best, key=lambda L: best[L][0])

    if a.jackknife:
        print('%s: jackknife over %d anchors' % (a.image_id, len(anchors)))
        agree = 0
        for i in range(len(anchors)):
            sub = anchors[:i] + anchors[i + 1:]
            b2 = fit(sub, a.pitch_min, a.pitch_max)
            w2 = min(b2, key=lambda L: b2[L][0]) if b2 else None
            agree += (w2 == win)
            print('  drop y%-5d -> lines=%s rms %5.2f' % (anchors[i], w2, b2[w2][0]))
        print('  %d of %d drops still choose lines=%d' % (agree, len(anchors), win))
        return

    if a.json:
        print(json.dumps({
            'image': a.image_id,
            'anchors': anchors,
            'best_lines': win,
            'by_line_count': {str(L): {'rms': round(best[L][0], 2), 'pitch': round(best[L][1], 2),
                                       'origin': best[L][2], 'ordinals': list(best[L][3])}
                              for L in sorted(best)},
        }, indent=1))
        return
    print('%s: %d anchors from column_closure' % (a.image_id, len(anchors)))
    for L in sorted(best):
        rms, b, a0, _ = best[L]
        print('lines=%2d  rms %6.2f  pitch %5.2f  origin %7.1f%s'
              % (L, rms, b, a0, '   <- best' if L == win else ''))


if __name__ == '__main__':
    main()
