#!/usr/bin/env python3
"""Triage aid for the retold passages: what did a passage put in that the
source never mentions?

    python3 wau-bun/check-additions.py [scene-id ...]

The retelling is allowed to re-order, compress and sharpen. It is NOT allowed
to add — no invented smell, sound, temperature, sky, or inferred feeling. That
rule is hard to eyeball across 158 scenes, so this flags the two things that go
wrong most often:

  INVENTED MOOD  a genre-tell word (dread, ominous, prickle, reek, loomed…)
              whose stem never appears anywhere in the source passage
  NUMBER      a number in one text and not the other, either direction —
              catches both invented precision and dropped detail

Both are heuristics, not verdicts: "cold" may be a fair rendering of a source
that says "the ice had made in the river". Read the hits, do not obey them.
"""
import io, os, re, sys, glob

DARK, SRC = 'wau-bun/dark/', 'wau-bun/source-scenes/'

# The tells of a voice that is reaching. STRONG words almost never belong in a
# faithful retelling of this book unless the source put them there; SOFT ones
# are ordinary narration and are reported only as background.
STRONG = """
dread menace ominous foreboding sinister eerie uncanny
prickle prickled spine crawl crawled shiver shivered
reek reeked stench stank rot rotting rotten
loomed looming hiss hissed rasp rasped
heartbeat pulse lungs
"""
SOFT = """
smell smelled smelling stink stank reek reeked odour odor stench
silence silent hush quiet stillness still
shadow shadows shadowed dark darkness black blackness gloom murk
cold colder chill chilled freezing frozen ice icy damp clammy
breath breathed breathing lungs throat chest heartbeat pulse
skin crawl crawled prickle prickled shiver shivered spine hair neck teeth gut
whisper whispered hiss hissed rasp rasped creak creaked groan
dread menace wrong ominous foreboding sinister eerie uncanny
waiting watched watching stared staring loomed looming
copper iron rust blood-warm sour rot rotting rotten
"""
STRONG = sorted(set(STRONG.split()))
SOFT = sorted(set(SOFT.split()))

def stem(w):
    for suf in ('ing', 'ed', 'es', 's'):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            return w[:-len(suf)]
    return w

def wordsof(t):
    return re.sub(r'[^a-z ]', ' ', t.lower()).split()

def body(path, skip_hash=False):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    if skip_hash:
        lines = [l for l in lines if not l.startswith('#')]
    return '\n'.join(lines)

def numbers(t):
    # [21] and the like are footnote markers, apparatus rather than content —
    # the retellings drop them on purpose, so do not count them
    t = re.sub(r'\[\d+\]', ' ', t)
    out = set(re.findall(r'\b\d[\d,]*\b', t))
    return set(n.replace(',', '') for n in out)

def check(sid):
    d, s = DARK + sid + '.txt', SRC + sid + '.txt'
    if not (os.path.exists(d) and os.path.exists(s)): return None
    dt, st = body(d), body(s, True)
    sstems = set(stem(w) for w in wordsof(st))
    new = set(w for w in wordsof(dt) if stem(w) not in sstems)
    dn, sn = numbers(dt), numbers(st)
    return (sorted(w for w in new if w in STRONG),
            sorted(w for w in new if w in SOFT),
            sorted(sn - dn), sorted(dn - sn))

ids = sys.argv[1:] or sorted(
    os.path.basename(f)[:-4] for f in glob.glob(DARK + '*.txt')
    if not f.endswith('BRIEF.md'))

flagged = 0
for sid in ids:
    r = check(sid)
    if not r: continue
    strong, soft, dropped, added = r
    if not (strong or dropped or added): continue
    flagged += 1
    print(sid)
    if strong:  print('   INVENTED MOOD:', ', '.join(strong))
    if soft:    print('   (softer, probably fine):', ', '.join(soft))
    if dropped: print('   NUMBER in source, not in retelling:', ', '.join(dropped))
    if added:   print('   NUMBER in retelling, not in source:', ', '.join(added))
print('\n%d of %d scenes flagged' % (flagged, len(ids)))
