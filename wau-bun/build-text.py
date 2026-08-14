#!/usr/bin/env python3
"""Build per-scene passages of BOTH texts for every part of Wau-Bun.

Writes site/wau-bun/js/data-text-part{1,2,3}.js — one modern and one 1856
passage per scene id in the matching js/data-part{1,2,3}.js.

    python3 wau-bun/build-text.py [SOURCE_DIR]

SOURCE_DIR (default ./wau-bun/sources) must hold:
  waubun.txt  paragraph-per-line dump of the contemporary-English .docx
              (python: iterate word/document.xml <w:p>, one line each)
  orig.epub   Project Gutenberg ebook #12183 — the 1856 first edition

Neither source is committed: the modernization is the author's own file, and
the epub is a 500 KB public-domain artefact better fetched than vendored.

How the two texts get aligned: scene boundaries are hand-checked LINE RANGES
in waubun.txt (below). For the 1856 text, each scene's opening paragraph is
matched against the paragraphs of the same chapter by rare-word overlap, and
the scene runs from there to the NEXT MATCH IN THE CHAPTER — scenes are sorted
by where they landed, not by scene order, because a couple of scenes (Nelly
Lytle's captivity in ch. XXII) are told out of narrative order. The script
prints the match score for every boundary so a bad one cannot pass silently.

The Part 2 and 3 ranges were proposed by a monotonic alignment of each scene's
own summary against its chapter's paragraphs, then corrected by hand.
"""
import json, re, sys, zipfile
from html.parser import HTMLParser

SRC = (sys.argv[1] if len(sys.argv) > 1 else 'wau-bun/sources').rstrip('/') + '/'
OUT = 'site/wau-bun/js/data-text-part%d.js'
RETOLD = 'wau-bun/modern/'   # hand-written retellings, one <scene-id>.txt per scene

# ---------- modern text ----------
mod = open(SRC + 'waubun.txt').read().split('\n')

# scene id -> (chapter, first line, last line) in waubun.txt — hand-checked.
# One list per part; a part's list must cover its chapters with no gaps.
PART1 = [
    ('s1',  'I',    194, 198), ('s2',  'I',    199, 200), ('s3',  'I',    201, 205),
    ('s4',  'II',   209, 213), ('s5',  'II',   214, 226), ('s6',  'II',   227, 240), ('s7', 'II', 241, 241),
    ('s8',  'III',  245, 254), ('s9',  'III',  255, 287), ('s10', 'III',  288, 291),
    ('s11', 'III',  292, 301), ('s12', 'III',  302, 312),
    ('s13', 'IV',   316, 376), ('s14', 'IV',   377, 389), ('s15', 'IV',   390, 397), ('s16', 'IV', 398, 428),
    ('s17', 'V',    432, 468),
    ('s18', 'VI',   472, 488),
    ('s19', 'VII',  492, 497), ('s20', 'VII',  498, 505), ('s21', 'VII',  506, 512),
    ('s22', 'VIII', 516, 522), ('s23', 'VIII', 523, 530), ('s24', 'VIII', 531, 536), ('s25', 'VIII', 537, 558),
    ('s26', 'IX',   562, 574),
    ('s27', 'X',    578, 597), ('s28', 'X',    598, 622),
    ('s29', 'XI',   626, 665), ('s30', 'XI',   666, 674), ('s31', 'XI', 675, 683), ('s32', 'XI', 684, 691),
    ('s33', 'XII',  695, 715),
    ('s34', 'XIII', 719, 743), ('s35', 'XIII', 744, 764),
    ('s36', 'XIV',  769, 789), ('s37', 'XIV',  790, 806), ('s38', 'XIV', 807, 818),
    ('s39', 'XV',   822, 840), ('s40', 'XV',   841, 863), ('s41', 'XV', 864, 886),
    ('s42', 'XVI',  890, 907), ('s43', 'XVI',  908, 921), ('s44', 'XVI', 922, 924), ('s45', 'XVI', 925, 932),
    ('s46', 'XVII', 936, 955), ('s47', 'XVII', 956, 961), ('s48', 'XVII', 962, 980), ('s49', 'XVII', 981, 1010),
]

PART2 = [
    ('p2s1',  'XVIII', 1014, 1023), ('p2s2',  'XVIII', 1024, 1034), ('p2s3',  'XVIII', 1035, 1041),
    ('p2s4',  'XVIII', 1042, 1050), ('p2s5',  'XVIII', 1051, 1057), ('p2s6',  'XVIII', 1058, 1067),
    ('p2s7',  'XVIII', 1068, 1077), ('p2s8',  'XVIII', 1078, 1082), ('p2s9',  'XVIII', 1083, 1089),
    ('p2s10', 'XVIII', 1090, 1096), ('p2s11', 'XVIII', 1097, 1101),
    ('p2s12', 'XIX',   1105, 1110), ('p2s13', 'XIX',   1111, 1111), ('p2s14', 'XIX',   1112, 1125),
    ('p2s15', 'XIX',   1126, 1135), ('p2s16', 'XIX',   1136, 1140), ('p2s17', 'XIX',   1141, 1145),
    ('p2s18', 'XIX',   1146, 1157), ('p2s19', 'XIX',   1158, 1173), ('p2s20', 'XIX',   1174, 1184),
    ('p2s21', 'XIX',   1185, 1188), ('p2s22', 'XIX',   1189, 1198), ('p2s23', 'XIX',   1199, 1212),
    ('p2s24', 'XX',    1216, 1221), ('p2s25', 'XX',    1222, 1226), ('p2s26', 'XX',    1227, 1232),
    ('p2s27', 'XX',    1233, 1238), ('p2s28', 'XX',    1239, 1267),
    ('p2s29', 'XXI',   1271, 1292),
    # ch. XXII tells the captivity out of order: the village (s33) is narrated
    # before the flashback to the two hiding children (s32), so these two ranges
    # run backwards on purpose.
    ('p2s30', 'XXII',  1296, 1311), ('p2s31', 'XXII',  1312, 1321), ('p2s33', 'XXII',  1322, 1326),
    ('p2s32', 'XXII',  1327, 1342), ('p2s34', 'XXII',  1343, 1348), ('p2s35', 'XXII',  1349, 1352),
    ('p2s36', 'XXII',  1353, 1367), ('p2s37', 'XXII',  1368, 1388),
    ('p2s38', 'XXIII', 1393, 1417), ('p2s39', 'XXIII', 1418, 1435), ('p2s40', 'XXIII', 1436, 1446),
]

PART3 = [
    ('p3s1',  'XXIV',    1450, 1455), ('p3s2',  'XXIV',    1456, 1461), ('p3s3',  'XXIV',    1462, 1473),
    ('p3s4',  'XXIV',    1474, 1502), ('p3s5',  'XXIV',    1503, 1515),
    ('p3s6',  'XXV',     1519, 1530), ('p3s7',  'XXV',     1531, 1547), ('p3s8',  'XXV',     1548, 1574),
    ('p3s9',  'XXV',     1575, 1602),
    ('p3s10', 'XXVI',    1606, 1611), ('p3s11', 'XXVI',    1612, 1628), ('p3s12', 'XXVI',    1629, 1641),
    ('p3s13', 'XXVI',    1642, 1648),
    ('p3s14', 'XXVII',   1652, 1659), ('p3s15', 'XXVII',   1660, 1664), ('p3s16', 'XXVII',   1665, 1670),
    ('p3s17', 'XXVII',   1671, 1676), ('p3s18', 'XXVII',   1677, 1682),
    ('p3s19', 'XXVIII',  1686, 1697), ('p3s20', 'XXVIII',  1698, 1706), ('p3s21', 'XXVIII',  1707, 1723),
    ('p3s22', 'XXVIII',  1724, 1732),
    ('p3s23', 'XXIX',    1736, 1784),
    ('p3s24', 'XXX',     1788, 1860),
    ('p3s25',  'XXXI',   1864, 1875), ('p3s26',  'XXXI',   1876, 1882), ('p3s26a', 'XXXI',   1883, 1887),
    ('p3s26b', 'XXXI',   1888, 1901), ('p3s26c', 'XXXI',   1902, 1912), ('p3s26d', 'XXXI',   1913, 1923),
    ('p3s27',  'XXXII',  1927, 1938), ('p3s28',  'XXXII',  1939, 1940), ('p3s29',  'XXXII',  1941, 1947),
    ('p3s29a', 'XXXII',  1948, 1958), ('p3s29b', 'XXXII',  1959, 1963), ('p3s29c', 'XXXII',  1964, 1969),
    ('p3s29d', 'XXXII',  1970, 1976), ('p3s29e', 'XXXII',  1977, 1983),
    ('p3s30',  'XXXIII', 1987, 1997), ('p3s31',  'XXXIII', 1998, 2005), ('p3s31a', 'XXXIII', 2006, 2011),
    ('p3s31b', 'XXXIII', 2012, 2017), ('p3s31c', 'XXXIII', 2018, 2028), ('p3s31d', 'XXXIII', 2029, 2042),
    ('p3s32', 'XXXIV',   2047, 2049), ('p3s33', 'XXXIV',   2050, 2055), ('p3s34', 'XXXIV',   2056, 2072),
    ('p3s35', 'XXXIV',   2073, 2075), ('p3s36', 'XXXIV',   2076, 2096), ('p3s37', 'XXXIV',   2097, 2125),
    ('p3s38', 'XXXV',    2129, 2135), ('p3s39', 'XXXV',    2136, 2138), ('p3s40', 'XXXV',    2139, 2152),
    ('p3s41', 'XXXV',    2153, 2164), ('p3s42', 'XXXV',    2165, 2178),
    ('p3s43', 'XXXVI',   2182, 2188), ('p3s44', 'XXXVI',   2189, 2195), ('p3s45', 'XXXVI',   2196, 2208),
    ('p3s46', 'XXXVI',   2209, 2224),
    ('p3s47', 'XXXVII',  2228, 2239), ('p3s48', 'XXXVII',  2240, 2244), ('p3s49', 'XXXVII',  2245, 2247),
    ('p3s50', 'XXXVII',  2248, 2264),
    ('p3s51', 'XXXVIII', 2268, 2273), ('p3s52', 'XXXVIII', 2274, 2277), ('p3s53', 'XXXVIII', 2278, 2280),
    ('p3s54', 'XXXVIII', 2281, 2284), ('p3s55', 'XXXVIII', 2285, 2293), ('p3s56', 'XXXVIII', 2294, 2302),
]

PARTS = [(1, PART1), (2, PART2), (3, PART3)]

STRAY = 'The Project Gutenberg eBook of Wau-Bun'
SEP = re.compile(r'^[\*\s\u2022]+$')
SPEAKER = re.compile(r'^(?:[A-Z][A-Z\-\u00c9 ]{2,}\.|CHORUS|BOURGEOIS)')
ENDS = tuple('.!?"\u201d\'\u2019:;)')

def modern_paras(a, b):
    """The .docx carries hard line-wraps in places, so a 'paragraph' can arrive
    as several fragments. Re-join a fragment to the one before it when that one
    did not end a sentence — except for song/dialogue lines with a speaker tag."""
    raw = []
    for i in range(a - 1, b):
        t = mod[i].strip()
        if not t or t.startswith('[Heading') or t.startswith(STRAY) or SEP.match(t):
            continue
        raw.append(t)
    out = []
    for t in raw:
        if out and not out[-1].rstrip().endswith(ENDS) and not SPEAKER.match(t):
            out[-1] = out[-1].rstrip() + ' ' + t
        else:
            out.append(t)
    return out

# ---------- original text ----------
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out = []; s.buf = []; s.tag = None
    def handle_starttag(s, t, a):
        if t in ('p', 'h1', 'h2', 'h3'): s.flush(); s.tag = t
    def handle_endtag(s, t):
        if t in ('p', 'h1', 'h2', 'h3'): s.flush()
    def handle_data(s, d): s.buf.append(d)
    def flush(s):
        t = ' '.join(''.join(s.buf).split()); s.buf = []
        if t: s.out.append((s.tag or 'p', t))
        s.tag = None

z = zipfile.ZipFile(SRC + 'orig.epub')
blocks = []
for f in sorted(n for n in z.namelist() if n.endswith('.txt.xhtml')):
    p = P(); p.feed(z.read(f).decode('utf-8', 'replace')); p.flush(); blocks.extend(p.out)

starts = [(s.strip(), i) for i, (t, s) in enumerate(blocks)
          if t in ('h2', 'h3') and re.match(r'^CHAPTER\s+[IVXL]+\.?$', s.strip(), re.I) and i > 100]
orig_ch = {}
for n, (name, i) in enumerate(starts):
    end = starts[n + 1][1] if n + 1 < len(starts) else len(blocks)
    roman = re.match(r'^CHAPTER\s+([IVXL]+)', name, re.I).group(1).upper()
    body = []
    for (t, s) in blocks[i + 2:end]:
        if t in ('h1', 'h2', 'h3'): break   # the last chapter runs straight into APPENDIX
        if s.startswith(STRAY) or SEP.match(s): continue   # page headers, scene rules
        body.append(s)
    orig_ch[roman] = body

def norm(s):
    return re.sub(r'[^a-z ]', ' ', s.lower())
def sig(s):
    return set(w for w in norm(s).split() if len(w) > 3)
def score(a, b):
    A, B = sig(a), sig(b)
    if not A or not B: return 0.0
    return len(A & B) / len(A | B)

def retold(sid):
    """A hand-written contemporary retelling of this scene, if one exists:
    wau-bun/modern/<sid>.txt, paragraphs separated by blank lines. These take
    the place of the light .docx modernization as the 'modern' text."""
    try:
        raw = open(RETOLD + sid + '.txt').read()
    except IOError:
        return None
    paras = [' '.join(b.split()) for b in re.split(r'\n\s*\n', raw) if b.strip()]
    return paras or None

CHAP = {}
for _i, _l in enumerate(mod):
    # two of the real headings (II and VIII) have no trailing period, and the
    # table of contents up front repeats every one of them — so match loosely
    # and let the later, real heading win
    _m = re.match(r'\[Heading1\] CHAPTER ([IVXLivxl]+)\.?$', _l.strip())
    if _m: CHAP[_m.group(1).upper()] = _i + 1        # 1-based line of the heading
CHAP_ORDER = [k for k, v in sorted(CHAP.items(), key=lambda kv: kv[1])]
APPENDIX = next(i + 1 for i, l in enumerate(mod) if l.startswith('[Heading1] APPENDIX'))

def chapter_lines(roman):
    """Every content line of a chapter in waubun.txt (1-based), headings, page
    headers and * * * * * rules excluded."""
    a = CHAP[roman] + 1
    k = CHAP_ORDER.index(roman)
    b = (CHAP[CHAP_ORDER[k + 1]] if k + 1 < len(CHAP_ORDER) else APPENDIX) - 1
    out = []
    for i in range(a, b + 1):
        t = mod[i - 1].strip()
        if not t or t.startswith('[Heading') or t.startswith(STRAY) or SEP.match(t): continue
        out.append(i)
    return out

def check_coverage(number, ranges):
    """The whole point of this app is that no part of the book is left out, so
    prove it: every paragraph of every chapter must land in exactly one scene,
    in both texts."""
    bad = []
    seen = {}
    for sid, roman, a, b in ranges:
        for i in range(a, b + 1):
            if seen.get(i): bad.append('line %d is in both %s and %s' % (i, seen[i], sid))
            seen[i] = sid
    for roman in dict.fromkeys(r[1] for r in ranges):
        missing = [i for i in chapter_lines(roman) if i not in seen]
        if missing:
            bad.append('ch. %s: %d paragraph(s) in no scene, first at line %d'
                       % (roman, len(missing), missing[0]))
    return bad

def build(ranges):
    """Align one part: modern paragraphs by line range, 1856 paragraphs by
    matching each scene's opening against its chapter."""
    out, report = {}, []
    for sid, roman, a, b in ranges:
        mp = modern_paras(a, b)
        if not mp:
            sys.exit('empty modern range for %s (%d-%d)' % (sid, a, b))
        ops = orig_ch[roman]
        # locate the original paragraph that best matches this scene's opening
        anchor = ' '.join(mp[:2])
        best_i, best_s = 0, -1.0
        for i, op in enumerate(ops):
            sc = max(score(mp[0], op), score(anchor, ' '.join(ops[i:i + 2])))
            if sc > best_s: best_i, best_s = i, sc
        rt = retold(sid)
        out[sid] = {'roman': roman, 'modern': rt or mp, 'retold': bool(rt),
                    '_ostart': best_i, '_oscore': round(best_s, 3)}
        report.append((sid, roman, len(out[sid]['modern']), best_i, round(best_s, 3), bool(rt)))

    # 1856 ranges: each scene runs to the NEXT MATCH within its chapter. Sort by
    # where the scenes landed rather than by scene order — ch. XXII narrates two
    # of its scenes out of story order, and their ranges legitimately run back.
    by_ch = {}
    for sid, roman, _, _ in ranges:
        by_ch.setdefault(roman, []).append(sid)
    for roman, sids in by_ch.items():
        sids = sorted(sids, key=lambda x: out[x]['_ostart'])
        for i, sid in enumerate(sids):
            st = out[sid]['_ostart']
            end = out[sids[i + 1]]['_ostart'] if i + 1 < len(sids) else len(orig_ch[roman])
            out[sid]['original'] = orig_ch[roman][st:end]
    return out, report

def words(paras): return len(' '.join(paras).split())

fail = False
for number, ranges in PARTS:
    out, report = build(ranges)
    ids = [r[0] for r in ranges]
    gaps = check_coverage(number, ranges)
    print('\n=== PART %d ===' % number)
    print(f"{'scene':6} {'ch':8} {'mod¶':>5} {'orig¶':>6} {'match':>6} {'words':>13} {'len%':>5}  src")
    short, thin, empty = [], [], []
    for sid, roman, nm, oi, sc, rt in report:
        rec = out[sid]
        wm, wo = words(rec['modern']), words(rec['original'])
        pct = round(100 * wm / wo) if wo else 0
        print(f"{sid:6} {roman:8} {nm:>5} {len(rec['original']):>6} {sc:>6} "
              f"{wm:>6}/{wo:<6} {pct:>4}%  {'retold' if rt else 'docx'}")
        if sc < 0.15: short.append(sid)
        if not rec['original']: empty.append(sid)
        if rt and pct < 90: thin.append((sid, pct))   # retellings must not shed detail

    done = sum(1 for r in report if r[5])
    print(f"part {number}: {len(report)} scenes · retold {done} · "
          f"{words([p for r in report for p in out[r[0]]['modern']]):,} modern words vs "
          f"{words([p for r in report for p in out[r[0]]['original']]):,} of 1856")
    if gaps:
        print('  BOOK NOT FULLY COVERED:'); fail = True
        for g in gaps: print('    ' + g)
    else:
        print('  coverage: every paragraph of ch. %s lands in exactly one scene'
              % '-'.join([ranges[0][1], ranges[-1][1]]))
    if short: print('  WEAK ANCHOR MATCHES (check these):', ', '.join(short)); fail = True
    if empty: print('  EMPTY 1856 PASSAGE (check these):', ', '.join(empty)); fail = True
    if thin:
        print('  RETELLINGS THAT LOST LENGTH (fix these):',
              ', '.join(f'{s} at {p}%' for s, p in thin)); fail = True

    # ---------- emit ----------
    js = ['/* Wau-Bun — Part %d full text, one passage per scene.' % number,
          '   modern:   contemporary English. retold:true = rewritten for this app in a',
          '             plain modern voice, nothing cut; retold:false = the earlier, lighter',
          '             modernization, still awaiting its rewrite',
          '   original: the 1856 first-edition text (Project Gutenberg #12183, public domain)',
          '   Generated — do not hand-edit. Loaded on demand by the reader, never on first paint. */',
          'var WAUBUN_TEXT_PART%d = {' % number]
    for sid in ids:
        rec = out[sid]
        js.append('  %s: {' % sid)
        js.append('    retold: %s,' % ('true' if rec['retold'] else 'false'))
        js.append('    modern: %s,' % json.dumps(rec['modern'], ensure_ascii=False))
        js.append('    original: %s' % json.dumps(rec['original'], ensure_ascii=False))
        js.append('  },')
    js.append('};')
    open(OUT % number, 'w').write('\n'.join(js) + '\n')
    print('  wrote ' + OUT % number)

if fail: sys.exit(1)
