#!/usr/bin/env python3
"""Build per-scene passages of BOTH texts for Wau-Bun Part 1.

Writes site/wau-bun/js/data-text-part1.js — one modern and one 1856 passage
per scene id in js/data-part1.js.

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
the scene runs from there to the next scene's match. Every boundary in Part 1
matched at 0.88-1.0; the script prints the score for each so a bad boundary
cannot pass silently.
"""
import json, re, sys, zipfile
from html.parser import HTMLParser

SRC = (sys.argv[1] if len(sys.argv) > 1 else 'wau-bun/sources').rstrip('/') + '/'
OUT = 'site/wau-bun/js/data-text-part1.js'
RETOLD = 'wau-bun/modern/'   # hand-written retellings, one <scene-id>.txt per scene

# ---------- modern text ----------
mod = open(SRC + 'waubun.txt').read().split('\n')

# scene id -> (chapter, first line, last line) in waubun.txt — hand-checked
RANGES = [
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
    orig_ch[roman] = [s for (t, s) in blocks[i + 2:end]]

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

out = {}
report = []
for k, (sid, roman, a, b) in enumerate(RANGES):
    mp = modern_paras(a, b)
    ops = orig_ch[roman]
    # locate the original paragraph that best matches this scene's opening paragraph
    anchor = ' '.join(mp[:2])
    best_i, best_s = 0, -1.0
    for i, op in enumerate(ops):
        sc = max(score(mp[0], op), score(anchor, ' '.join(ops[i:i + 2])))
        if sc > best_s: best_i, best_s = i, sc
    rt = retold(sid)
    out[sid] = {'roman': roman, 'modern': rt or mp, 'retold': bool(rt),
                '_ostart': best_i, '_oscore': round(best_s, 3)}
    report.append((sid, roman, len(out[sid]['modern']), best_i, round(best_s, 3), bool(rt)))

# original ranges = from this scene's start to the next scene's start in the same chapter
ids = [r[0] for r in RANGES]
for i, sid in enumerate(ids):
    rec = out[sid]
    nxt = out[ids[i + 1]] if i + 1 < len(ids) else None
    end = nxt['_ostart'] if (nxt and nxt['roman'] == rec['roman']) else len(orig_ch[rec['roman']])
    rec['original'] = orig_ch[rec['roman']][rec['_ostart']:end]

def words(paras): return len(' '.join(paras).split())

print(f"{'scene':6} {'ch':6} {'mod¶':>5} {'orig¶':>6} {'match':>6} {'words':>13} {'len%':>5}  src")
short, thin = [], []
for sid, roman, nm, oi, sc, rt in report:
    rec = out[sid]
    wm, wo = words(rec['modern']), words(rec['original'])
    pct = round(100 * wm / wo) if wo else 0
    print(f"{sid:6} {roman:6} {nm:>5} {len(rec['original']):>6} {sc:>6} "
          f"{wm:>6}/{wo:<6} {pct:>4}%  {'retold' if rt else 'docx'}")
    if sc < 0.15: short.append(sid)
    # the retellings must not quietly shed detail
    if rt and pct < 90: thin.append((sid, pct))

done = sum(1 for r in report if r[5])
print(f"\nretold: {done}/{len(report)} scenes · "
      f"{words([p for r in report if r[5] for p in out[r[0]]['modern']]):,} of "
      f"{words([p for r in report for p in out[r[0]]['original']]):,} words")
if short:
    print('WEAK ANCHOR MATCHES (check these):', ', '.join(short))
if thin:
    print('RETELLINGS THAT LOST LENGTH (fix these):',
          ', '.join(f'{s} at {p}%' for s, p in thin))
    sys.exit(1)

# ---------- emit ----------
js = ['/* Wau-Bun — Part 1 full text, one passage per scene.',
      '   modern:   contemporary English. retold:true = rewritten for this app in a',
      '             plain modern voice, nothing cut; retold:false = the earlier, lighter',
      '             modernization, still awaiting its rewrite',
      '   original: the 1856 first-edition text (Project Gutenberg #12183, public domain)',
      '   Generated — do not hand-edit. Loaded on demand by the reader, never on first paint. */',
      'var WAUBUN_TEXT_PART1 = {']
for sid in ids:
    rec = out[sid]
    js.append('  %s: {' % sid)
    js.append('    retold: %s,' % ('true' if rec['retold'] else 'false'))
    js.append('    modern: %s,' % json.dumps(rec['modern'], ensure_ascii=False))
    js.append('    original: %s' % json.dumps(rec['original'], ensure_ascii=False))
    js.append('  },')
js.append('};')
open(OUT, 'w').write('\n'.join(js) + '\n')
print('\nwrote ' + OUT)
