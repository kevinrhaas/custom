#!/usr/bin/env python3
"""The Chicago post office's 1 January 1834 letter list, counted over its printings.

    tools/letter_list_printings.py            the tally and the concordance
    tools/letter_list_printings.py --json     the same, machine-readable
    tools/letter_list_printings.py --apply    write the completions into the claims
    tools/letter_list_printings.py --scan     the printed list, read at the page images
    tools/letter_list_printings.py --apply-scan  write the IMAGE readings into the claims
    tools/letter_list_printings.py --self-test  the assertions still fire

WHY THIS EXISTS. T-0312 found a letter list on page 4 of the Democrat of 1834-03-04
whose heading the segmenter had cut down the middle, and minted its names as claims
c026 and c027 of `data/research/newspapers/extracted/chicago_democrat_1834_03_04.json`.
Three things about it could not be read off that one crop, and T-0331 assigned all
three to the page images: WHICH RETURN it is (the date line survives as `34.` and
nothing else), how much of the printed list survives, and the FORENAMES, which the
crop has taken off the left edge of every line.

`data/research/newspapers/README.md` prescribes the cheaper instrument, and it is the
one this tool mechanises: **count the printings before you send for the images**
(T-0328), and **count them by the notice's own body text rather than by its heading**
(T-0350). A quarterly letter list is standing type. It ran in the Democrat week after
week until the letters were sent to the dead-letter office, and every week is a
separate impression, separately scanned, separately damaged. Eight other impressions
of this same list stand in the deposit, and between them they carry the heading, the
date line, and the forenames the March crop lost.

WHAT THE CONCORDANCE DOES NOT DO. It reads no page image, so nothing it proposes is
`scan_verified`; its witnesses are other transcriptions and its readings stay
`transcription_mediated`. It amends nothing to agree with anything: every printing
keeps its own verbatim setting, and a completion is reported with the printings that
carry it, so a reader can weigh the tally rather than take the result.

THE PAGE IMAGES, AND WHY THEY OUTRANK ALL OF IT (T-0424, 2026-09-10). The cheap
instrument was always a stand-in for the expensive one, and the expensive one has now
been run: `data/research/newspapers/letter_list_1834_01_01_scan.json` is the printed
list read off the deposit's own page scans, at 300 dpi, in two impressions in full
(1834-01-28 Vol. I No. 10 and 1834-03-04 Vol. I No. 15) and two more checked for
length. It settles the three questions T-0331 assigned to the images:

  * WHICH RETURN. `List of Letters REMAINING in the Post-Office at Chicago, Ill.
    January 1, 1834.`, over `JOHN S. C. HOGAN, P. M.` -- the heading whole, where the
    March crop kept `34.` and nothing else.
  * HOW LONG. **170 printed lines**, two alphabetical sub-columns of 85, the same in
    every impression: this is standing type and it did not move between January and
    March. 79 names were minted off the March crops and 97 off the January
    transcription, so both are FLOORS, short by 91 and 73 lines respectively.
  * THE FORENAMES the crop took off the left edge. `--scan` walks the crops' minted
    readings down the printed sub-column they came from and reports what stands at
    each position -- or, where the crop lost lines either side of a reading, the
    WINDOW of printed lines it must be one of, and no name at all.

Ruling 2 of `data/research/newspapers/README.md`: a scan_verified reading outranks a
transcription. So `--apply-scan` overwrites what `--apply` proposed, and `--apply`
refuses to touch an entity the image has already settled.

THE FINGERPRINT. Every impression of this list opens on the same name, which the
eight scans set eight ways -- `Eliphalet Atkins 2`, `ejiphalet Atkina 2`, `Jiphalet
Atkine 2`, `Et halet Atkins 2`, `Askina 2`, `liphalet Atkine 2`, `Atkina 2` -- and two
crops do not carry it at all, because the segmenter took the top of the column off.
That is why a printing is located on its BODY TEXT and not on `List of Letters`: four
of the nine headings are illegible, cut, or in another crop entirely, and the sweep
that first read this run found FOUR printings by searching for the heading where there
are NINE.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPOSIT = ROOT.parent / "reference" / "newspapers" / "Transcriptions" / \
    "Chicago_Democrat_1833-11_to_1835-08"
EXTRACTED = ROOT / "data" / "research" / "newspapers" / "extracted" / \
    "chicago_democrat_1834_03_04.json"
SCAN = ROOT / "data" / "research" / "newspapers" / "letter_list_1834_01_01_scan.json"
# The March crops are two, and each is one of the printed sub-columns: c026 took the
# left (Atkins to Harkness) and c027 the right (Hays to Wright). That is what makes a
# positional walk possible at all -- a crop's readings are in printed order within one
# sub-column, whatever it lost between them.
CLAIM_COLUMN = {"c026": "left", "c027": "right"}
# How far ahead of the cursor a surname may match before the match is refused. The
# crops lose runs of lines -- c027 loses ten between `Salmon Rutherford 3` and `James
# Steward` -- so the window cannot be tight; but an unbounded one would let a late
# surname collide with an early one and read the list out of order.
SCAN_REACH = 15

# The eight printings, each located by hand in the deposit and stated with the line
# the list's first name stands on, so every row here is checkable in one `sed -n`.
# `head` is the line the heading or its remnant stands on; `first` the line carrying
# the fingerprint name; `span` how far below `head` the printed column runs, read to
# the postmaster's signature or, where the crop lost it, to the end of the names.
# The nine printings, each located by hand in the deposit. `segments` are the line
# ranges the list occupies IN THAT ISSUE, because the segmenter cuts a printed column
# into crops and a crop rarely holds the whole list: 1834-02-18 carries the A-I half
# in one column of page 4 and the J-Z half in another, three hundred lines apart.
# Every row here is checkable in one `sed -n`.
PRINTINGS = [
    # issue date, volume/number as filed, [(head, span), ...], the fingerprint line,
    # and what the date line reads where the crop kept it
    ("1834-01-07", "Vol1_No7", [(643, 60)], 645,
     "EMAINING in the Post-Offiee at Chic / go, Ill. January [1,] 1834."),
    ("1834-01-14", "Vol1_No8", [(1063, 75)], 1067,
     "BDBEMAINING [in the Post-Office at Chica]go, Ill. Januar[y ...]"),
    ("1834-01-21", "Vol1_No9", [(1099, 60)], 1101,
     "[heading lost to the crop; the names run from the fingerprint]"),
    ("1834-01-28", "Vol1_No10", [(1107, 30)], 1113,
     "EMAINING in the Port-Offiee at Ch / go, Ill. Fammuary 1, 1604."),
    ("1834-02-04", "VolI_No11", [(2858, 90)], 2860,
     "EMAINING in the Post- / go, Ill, January 3, 1934."),
    ("1834-02-11", "VolI_No12", [(2694, 240)], 2696,
     "EMAINING [-- the rest of the heading lost to the alternating column]"),
    ("1834-02-18", "VolI_No13", [(2925, 50), (3066, 85)], 2929,
     "[the heading is in neither crop; both halves run as bare names]"),
    ("1834-02-25", "VolI_No14", [(2947, 240)], 2949,
     "REMAINISG in the Pest[-Office at Chica]go, Il January 1, 63[4]."),
    ("1834-03-04", "VolI_No15", [(3064, 220)], 3067,
     "List of L | etters / ost-Offiee at Chica- / 34."),
]

# The issue this project is trying to read. It is the last of the eight.
SUBJECT = "1834-03-04"

# A second office's 1 January 1834 return runs in the same weeks and must not be
# read into Chicago's. It is recorded here so a later sweep does not mistake it.
OTHER_OFFICE = [
    ("1834-01-21", "Vol1_No9", 937, "G in the Poston / c fica at Henne[pin]. "
     "... Ist day of Jan, 16[34]."),
    ("1834-01-28", "Vol1_No10", 957, "Hist of Letters AINING in the PontOitien "
     "at H / mi pin, Hl. on the Ist day of San. 18[34]"),
    ("1834-02-04", "VolI_No11", 2676, "EMAINING in the Post-Office at Benne[...]"),
]

NOISE = re.compile(r"[^A-Za-z']+")
# The scans confuse a small, well-known set of letter pairs and nothing else, so the
# fold is deliberately NARROW. An earlier and looser version of it -- vowels dropped,
# doubled letters collapsed -- proposed `Thomas Bonnet` for `[...]as Bennett` and
# `Howard Delaney` for `[?] Delano`, which is precisely the failure this project must
# not ship: a completion that looks right and proves nothing. Only these fold:
#   i / l / 1 / j / !   the scans' commonest single confusion
#   o / 0 , s / 5 , b / 8    figure-for-letter
#   u / v                 the long s and the worn v
#   rn -> m               the classic ligature break
# Vowels are NOT dropped and distinct letters are NOT merged, so `Bennett`, `Benton`
# and `Bonnet` stay three surnames, and `Atkins` and `Atkina` stay two settings of one.
FOLD = str.maketrans({"l": "i", "1": "i", "j": "i", "!": "i", "0": "o",
                      "5": "s", "8": "b", "v": "u"})


def fold(word):
    """A reading reduced to what the scans' own confusions leave decidable."""
    w = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    w = NOISE.sub("", w).lower().replace("rn", "m").translate(FOLD)
    return re.sub(r"(.)\1+", r"\1", w)


def read(date, vol):
    path = DEPOSIT / ("Chicago_Democrat_%s_%s_Transcription.txt" % (date, vol))
    if not path.exists():
        return None
    return path.read_text(encoding="utf8", errors="replace").split("\n")


def region(lines, segments):
    out = []
    for head, span in segments:
        out += list(enumerate(lines[head - 1:head - 1 + span], start=head))
    return out


# A name as the list sets it: an optional forename or initials, then a surname, then
# an optional count of letters waiting ("Atkins 2"). The transcriptions run names
# together inside one line where the Vision reading merged a column, so this is
# matched repeatedly across a line rather than anchored to it.
NAME = re.compile(
    r"(?:(?P<fore>(?:[A-Z][a-z']{1,12}|[A-Z]{1,2}\.?|[A-Z][a-z]{0,3}\.)"
    r"(?:\s*[A-Z]\.?)?)\s+)?"
    r"(?P<sur>(?:M'|Mc|Van\s?|De\s?)?[A-Z][A-Za-z']{2,14})"
    r"(?:\s+(?P<n>[23456]))?")


def settings(lines, segments):
    """Every name-shaped reading in one printing's regions, with its line."""
    out = []
    for ln, text in region(lines, segments):
        for m in NAME.finditer(text):
            sur = m.group("sur")
            if len(fold(sur)) < 4:
                continue
            out.append({"line": ln, "surname": sur,
                        "forename": (m.group("fore") or "").strip(),
                        "count": m.group("n"), "as_set": m.group(0).strip()})
    return out


def load_printings():
    found, missing = [], []
    for date, vol, segments, first, dateline in PRINTINGS:
        lines = read(date, vol)
        if lines is None:
            missing.append(date)
            continue
        found.append({"date": date, "vol": vol, "segments": segments,
                      "first": first, "dateline": dateline,
                      "fingerprint": lines[first - 1].strip()[:80],
                      "settings": settings(lines, segments)})
    return found, missing


def subject_names():
    """The names T-0312 minted off the 1834-03-04 crops, in printed order.

    ALWAYS THE CROP'S OWN READING. Once `--apply-scan` has run, `normalized` holds
    what the page images print; `crop_reading` holds what the crop said, and that is
    what every instrument here is about. The concordance exists to weigh
    transcriptions against each other, and it would be measuring the page's answer
    against itself if it read the repaired field; the scan alignment would be reading
    its own output back in. So the crop's reading is what this returns, and the page
    reading is offered beside it under its own name."""
    doc = json.loads(EXTRACTED.read_text(encoding="utf8"))
    out = []
    for claim in doc["claims"]:
        if claim["id"] not in ("c026", "c027"):
            continue
        for ent in claim.get("entities", []):
            crop = ent.get("crop_reading")
            out.append({"claim": claim["id"], "as_printed": ent["as_printed"],
                        "normalized": crop or ent["normalized"],
                        "crop_reading": crop,
                        "page_reading": ent["normalized"] if crop else None})
    return out


CUT = re.compile(r"\[\?\]|\[…\]|\[\.\.\.\]")


def within_one(a, b):
    """True when two folded readings differ by at most one letter."""
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) <= 1
    short, long = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(long)):
        if long[:i] + long[i + 1:] == short:
            return True
    return False


def cluster(keys, items):
    """Single-linkage clustering of readings at edit distance one."""
    groups = []
    for key, item in zip(keys, items):
        joined = [g for g in groups if any(within_one(key, k) for k in g["keys"])]
        if not joined:
            groups.append({"keys": [key], "items": [item]})
            continue
        head = joined[0]
        head["keys"].append(key)
        head["items"].append(item)
        for other in joined[1:]:
            head["keys"] += other["keys"]
            head["items"] += other["items"]
            groups.remove(other)
    return {i: g["items"] for i, g in enumerate(groups)}


COUNT = re.compile(r"\s(\d)\s*$")


def count_of(normalized):
    """The `2` in `Atkins 2` -- how many letters wait for that name."""
    m = COUNT.search(re.sub(r"\[[^\]]*\]", " ", normalized).strip())
    return " " + m.group(1) if m else ""


def surname_of(normalized):
    """The surname out of a minted reading like `[?] E. Benton` or `[…]as Bennett`."""
    text = re.sub(r"\[[^\]]*\]", " ", normalized)
    text = re.sub(r"\b(or)\b", " ", text)
    words = [w for w in re.split(r"[\s;]+", text.strip()) if w]
    words = [w for w in words if not re.fullmatch(r"[A-Z]\.?|[0-9]|", w)]
    return words[-1].strip(".,;") if words else ""


def concordance():
    """For every name the 1834-03-04 crops minted, the other printings' settings.

    A completion is proposed only when TWO OR MORE of the seven other printings set
    the same forename against the same surname. One witness is reported and never
    proposed -- a single scan is a single scan -- and where the printings disagree
    the disagreement is reported instead of a winner, because two Bennetts and two
    Bowens really do stand in this list.
    """
    printings, missing = load_printings()
    subject = [p for p in printings if p["date"] == SUBJECT]
    witnesses = [p for p in printings if p["date"] != SUBJECT]
    minted = subject_names()
    # WHERE THE LIST CARRIES TWO OF A SURNAME, NEITHER IS COMPLETED. Two Bennetts,
    # two Miners and two Temples stand in this return, and a crop that has taken the
    # forename off both cannot say which line is which. Completing them from the
    # concordance would put the same man in the list twice, which is the failure mode
    # T-0299 exists to stop, so the ambiguity is reported instead.
    doubled = {k for k in [fold(surname_of(n["normalized"])) for n in minted]
               if [fold(surname_of(n["normalized"])) for n in minted].count(k) > 1}
    rows = []
    for name in minted:
        sur = surname_of(name["normalized"])
        tail = count_of(name["normalized"])
        key = fold(sur)
        agreeing = []
        hits = []
        if len(key) >= 4:
            for w in witnesses:
                for s in w["settings"]:
                    if fold(s["surname"]) == key and s["forename"]:
                        hits.append({"date": w["date"], "line": s["line"],
                                     "as_set": s["as_set"],
                                     "forename": s["forename"]})
        # Forenames are clustered rather than bucketed, because two scans of one
        # setting differ by a letter as readily as two settings do: `Wim. H.` and
        # `Wm. H.`, `Semel` and `Samuel`. Single linkage at edit distance one, on
        # the folded forename, joins those and joins nothing further -- `Hiram`
        # and `Thomas` are four apart, `A. H.` and `Philip` five.
        groups = cluster([fold(h["forename"]) for h in hits], hits)
        # distinct PRINTINGS, not distinct readings: two transcriptions of one
        # impression are one witness (README, the two cautions).
        strong = [g for g in groups.values()
                  if len({h["date"] for h in g}) >= 2]
        proposal = disagree = None
        twice = key in doubled
        if twice:
            pass
        elif len(strong) == 1:
            # The cluster's readings differ in the scans' own way, so the one
            # emitted is the MODAL reading; a tie goes to the shortest, because
            # OCR inserts letters more often than it drops them (`Wim.` for `Wm.`),
            # and a remaining tie to the earliest printing.
            # ONLY THE FORENAME IS TAKEN. The 1834-03-04 crop cut the left edge,
            # so its SURNAMES are intact and are the thing matched on; taking the
            # witness's surname too would import that scan's own damage -- `John
            # Wiison`, `Eiam Tuller` -- into a name the subject page states plainly.
            # The forename emitted is the MODAL reading in the cluster; a tie goes to
            # the shortest, because OCR inserts letters oftener than it drops them
            # (`Wim.` for `Wm.`), and a remaining tie to the alphabetically first.
            reads = [h["forename"] for h in strong[0]]
            fore = min(sorted(set(reads)), key=lambda r: (-reads.count(r), len(r)))
            # The count of letters waiting -- `Elliot 3`, `Wilson 6` -- is the
            # SUBJECT page's own reading and is carried through untouched; the
            # witnesses' counts are their own printings' and are not imported.
            proposal = ("%s %s%s" % (fore, sur, tail)).strip()
            agreeing = sorted({h["date"] for h in strong[0]})
        elif len(strong) > 1:
            disagree = sorted({("%s %s%s" % (g[0]["forename"], sur, tail)).strip()
                               for g in strong})
        rows.append({
            "claim": name["claim"], "as_printed": name["as_printed"],
            "normalized": name["normalized"], "surname": sur, "surname_key": key,
            "cut": bool(CUT.search(name["normalized"])),
            "witnesses": hits,
            "printings_agreeing": agreeing,
            "proposal": proposal,
            "printings_disagree": disagree,
            "surname_twice_in_list": twice,
        })
    return {"printings": printings, "missing": missing, "subject_present": bool(subject),
            "other_office": OTHER_OFFICE, "rows": rows}



# ---------------------------------------------------------------------------
# THE PAGE IMAGES (T-0424)
# ---------------------------------------------------------------------------

TRAILING_COUNT = re.compile(r"\s+[2-9]\s*$")


def printed_surname(as_printed):
    """The surname a printed line carries.

    The line is set `forename surname [count]`, and three shapes need saying so:
    the count of letters waiting is not part of the name; `& Co.` is not a surname;
    and `Lamira & Laura Carrier` is two people sharing one surname, so the LAST word
    is the surname in every case, including that one."""
    text = TRAILING_COUNT.sub("", as_printed)
    text = re.sub(r"\s*&\s*Co\.?\s*$", "", text)
    words = [w.strip(".,;") for w in re.split(r"[\s]+", text) if w.strip(".,;")]
    return words[-1] if words else ""


def scan_candidates(name):
    """Every surname a minted reading could be offering, folded.

    A minted reading states its surname three ways and no one of them is reliable
    on its own: `[uncertain: John Monroe]` hides its surname INSIDE the bracket, so
    `surname_of` -- which strips brackets, and must, for `[…]ell Baldwin` -- returns
    nothing; `[uncertain: … Foster]` hides it the same way; and `| Monreou` keeps the
    page's own spelling in `as_printed` where the normalisation guessed another. All
    three are offered, and a match on any of them is a match."""
    # IDEMPOTENCE, AND WHY `crop_reading` EXISTS. Once `--apply-scan` has run,
    # `normalized` holds what the PAGE prints, so an alignment that read `normalized`
    # would be reading its own output back in -- and it measurably was: the second
    # run of an earlier draft settled three fewer readings than the first. The crop's
    # own reading is therefore KEPT, in `crop_reading`, and that is what is matched
    # on. It is worth keeping for its own sake as well: it is what T-0312 could see,
    # and overwriting it would have thrown the damage away with the repair.
    crop = name.get("crop_reading") or name["normalized"]
    out = set()
    for text in (re.sub(r"\[[^\]]*\]", " ", crop),
                 crop.replace("[", " ").replace("]", " "),
                 name["as_printed"]):
        text = TRAILING_COUNT.sub("", re.sub(r"[^\w'&.\s]+", " ", text))
        text = re.sub(r"\s*&\s*Co\.?\s*$", "", text.strip())
        words = [w.strip(".,;'") for w in text.split() if w.strip(".,;'")]
        words = [w for w in words if not re.fullmatch(r"[A-Za-z]\.?|\d+|uncertain|or", w)]
        # The floor is on the word, not on its fold. `Webb` folds to `web` and `Nats`
        # to `nats`, and a floor on the fold silently threw the four-letter surnames
        # away -- which is how `[?] Webb` came back unplaced beside a printed `Loiza
        # Webb` two lines from the cursor.
        if words and len(words[-1]) >= 4:
            out.add(fold(words[-1]))
    return out


def suffix_match(name, printed):
    """True when the crop's fragment is the tail of this printed line.

    The March segmenter cut the column's LEFT edge, so what a damaged reading keeps
    is the END of the line. `[…]as Bennett` is therefore not merely a Bennett: it is
    the Bennett whose forename ends in `as`, and the printed list holds three."""
    a, b = fold(name["as_printed"]), fold(printed)
    return bool(a) and len(a) >= 4 and b.endswith(a)


def load_scan():
    doc = json.loads(SCAN.read_text(encoding="utf8"))
    columns = {"left": [], "right": []}
    for line in doc["lines"]:
        columns[line["column"]].append(line)
    return doc, columns


NOT_A_LIST_LINE = ("occupations", "associated_places")


def is_list_line(entity):
    """A letter-list line yields a name and nothing else.

    c027's last entity is not a line of the list at all: it is the postmaster's
    signature, `JOHN S. C. HOGAN, P. M.`, and it carries an occupation and a place
    because T-0312 read him as a person of the town. Walking it down the column
    would hand it the last printed line -- the window either side of it is one wide,
    so the positional pass would place it on `Samuel Wright` with no surname evidence
    at all, which is exactly the confident wrong answer this instrument must not
    give."""
    return not any(k in entity for k in NOT_A_LIST_LINE)


def scan_alignment():
    """Each of the March crops' minted readings, against the printed line it stands on.

    TWO PASSES, and the second is the one that earns the tool. The first walks each
    crop's readings DOWN its own printed sub-column with a cursor that never goes
    back, matching on surname, so a reading is placed only at or after the line the
    reading before it was placed on. The second pass takes what the first could not
    match -- a reading whose surname the scan destroyed, `[…]ward`, `[?] Leena` --
    and looks at the GAP its neighbours leave. Where the gap is one line, the reading
    is that line and nothing else it could be: `[…]ward` sits between `D. S. Haight`
    and `Geo. Johnson`, and the printed list has exactly one line there, `Edward
    Hill`. Where the gap is wider the window is reported and NO NAME IS PROPOSED,
    because three candidate lines are three candidates."""
    doc, columns = load_scan()
    extracted = json.loads(EXTRACTED.read_text(encoding="utf8"))
    signatures = {(c["id"], e["as_printed"])
                  for c in extracted["claims"] if c["id"] in CLAIM_COLUMN
                  for e in c.get("entities", []) if not is_list_line(e)}
    minted = [n for n in subject_names()
              if (n["claim"], n["as_printed"]) not in signatures]
    rows = [{"claim": n["claim"], "as_printed": n["as_printed"],
             "normalized": n["normalized"], "column": CLAIM_COLUMN.get(n["claim"]),
             "cut": bool(CUT.search(n["normalized"])),
             "line": None, "printed": None, "by": None, "window": None,
             "shared_line": False}
            for n in minted]
    cursor = {"left": 0, "right": 0}
    for row, name in zip(rows, minted):
        col = row["column"]
        if col is None:
            continue
        keys = scan_candidates(name)
        lines = columns[col]
        window = range(cursor[col], min(len(lines), cursor[col] + SCAN_REACH))
        hits = [j for j in window
                if any(k == fold(printed_surname(lines[j]["as_printed"]))
                       or within_one(k, fold(printed_surname(lines[j]["as_printed"])))
                       for k in keys)]
        if hits:
            # Where the surname alone offers more than one line, the fragment's own
            # tail decides -- and only when it decides ALONE. Two candidates that both
            # end in the fragment are still two candidates.
            tails = [j for j in hits if suffix_match(name, lines[j]["as_printed"])]
            j = tails[0] if len(tails) == 1 else hits[0]
            row["line"] = lines[j]["line"]
            row["printed"] = lines[j]["as_printed"]
            row["by"] = "surname"
            cursor[col] = j + 1
    # Pass two: the gaps.
    for col in ("left", "right"):
        placed = [r for r in rows if r["column"] == col]
        for i, row in enumerate(placed):
            if row["line"] is not None:
                continue
            lo = next((placed[k]["line"] for k in range(i - 1, -1, -1)
                       if placed[k]["line"] is not None), 0) + 1
            hi = next((placed[k]["line"] for k in range(i + 1, len(placed))
                       if placed[k]["line"] is not None), len(columns[col]) + 1) - 1
            if hi < lo:
                # The readings either side of this one were placed on adjacent
                # printed lines, so the gap between them is empty and there is no
                # window to report. That happens when a crop sets ONE printed line as
                # TWO readings and the neighbour takes the placement. No reading in
                # c026 or c027 is in this state today; the branch is here so that one
                # arriving is reported as itself rather than as a lost line.
                row["shared_line"] = True
                continue
            row["window"] = [lo, hi]
            if lo == hi:
                row["line"] = lo
                row["printed"] = columns[col][lo - 1]["as_printed"]
                row["by"] = "position"
    return {"scan": doc, "columns": columns, "rows": rows}


def scan_report(res):
    doc, rows = res["scan"], res["rows"]
    c = doc["counts"]
    print("THE PRINTED LIST, READ AT THE PAGE IMAGES -- %s\n" % doc["title"])
    print("  %s" % doc["heading_as_printed"])
    print("  %s\n" % doc["foot_as_printed"].split("*")[0].strip())
    for imp in doc["impressions_read"]:
        print("  %-32s %-14s page %d col %d   scan page %-3d %s"
              % (imp["issue"], imp["volume"], imp["issue_page"], imp["column"],
                 imp["scan_page"], imp["archive_file"]))
    print("\n  PRINTED LENGTH  %d lines -- two sub-columns of %d, the same in every"
          % (c["printed_lines"], doc["setting"]["lines_per_column"]))
    print("                  impression read. %d personal names: %d lines name one"
          % (c["personal_names"], c["lines_naming_one_person"]))
    print("                  person, %d names two, %d name a firm."
          % (c["lines_naming_two_people"], c["firm_lines"]))
    minted = len([r for r in rows if r["column"]])
    print("\n  AGAINST IT: %d names were minted off the 1834-03-04 crops (T-0312) and"
          % minted)
    print("  97 off the 1834-01-28 transcription (T-0310). Both are floors: the")
    print("  crops are short by %d printed lines, the transcription by %d."
          % (c["printed_lines"] - minted, c["printed_lines"] - 97))
    cut = [r for r in rows if r["cut"] and r["column"]]
    settled = [r for r in cut if r["line"] is not None]
    print("\n  THE %d CUT READINGS, at the image:" % len(cut))
    print("    %3d settled -- %d on the surname the crop kept, %d on position alone"
          % (len(settled), len([r for r in settled if r["by"] == "surname"]),
             len([r for r in settled if r["by"] == "position"])))
    print("    %3d not settled: the crop lost lines either side and the window "
          "holds more than one\n" % (len(cut) - len(settled)))
    for r in cut:
        where = "%s %-2s" % (r["column"][0].upper(), r["line"] or "?")
        if r["line"] is not None:
            print("  -> %-26s %s  %s%s"
                  % (r["normalized"][:26], where, r["printed"],
                     "   (by position)" if r["by"] == "position" else ""))
        elif r["shared_line"]:
            print("  ~  %-26s %s  the crop set one printed line as two readings; "
                  "the neighbouring one holds it" % (r["normalized"][:26], where))
        else:
            lo, hi = r["window"] or (0, 0)
            print("  ?  %-26s %s  one of printed lines %d-%d, and the page cannot "
                  "say which" % (r["normalized"][:26], where, lo, hi))


def apply_scan(res):
    """Write the IMAGE readings into claims c026 and c027.

    `as_printed` never moves: it is the March crop's own damaged setting and it is
    the evidence that the repair was needed. `crop_reading` keeps what T-0312 made
    of it, so the repair is legible as a repair and the alignment has something
    stable to match on. `normalized` becomes what the page prints, `read_at_image` names the impressions it was read in, `printed_line`
    says where in the printed column it stands, and any `completed_from` the
    concordance had written is REMOVED -- a completion proposed from other
    transcriptions is superseded by the page, not corroborated by it.

    THE `reading` FIELD GOES BOTH WAYS AT ONCE, because that is the truth of it.
    The CLAIM was read at the page image, so the claim is `scan_verified`. Three of
    its seventy-eight readings the image still cannot settle -- the crop lost the
    printed lines either side of each, and the window left holds three candidates --
    and those keep `transcription_mediated` on their own entity, naming the window.
    Re-running is a no-op.
    """
    doc = json.loads(EXTRACTED.read_text(encoding="utf8"))
    by_printed = {(r["claim"], r["as_printed"]): r for r in res["rows"]}
    impressions = [i["issue"] for i in res["scan"]["impressions_read"][:2]]
    changed = 0
    for claim in doc["claims"]:
        if claim["id"] not in CLAIM_COLUMN:
            continue
        unsettled = []
        for ent in claim.get("entities", []):
            row = by_printed.get((claim["id"], ent["as_printed"]))
            if row is None:
                continue                      # the postmaster's signature
            ent.setdefault("crop_reading", ent["normalized"])  # once, and never again
            if row["line"] is None:
                ent["reading"] = "transcription_mediated"
                ent["reading_note"] = (
                    "The crop set one printed line as two readings and the reading "
                    "beside this one holds that line."
                    if row["shared_line"] else
                    "The image places this reading no closer than printed lines "
                    "%d-%d of the %s column: the crop lost the lines either side "
                    "of it and the page cannot say which is this one."
                    % (row["window"][0], row["window"][1], row["column"]))
                unsettled.append(ent["as_printed"])
                continue
            # THE TRAILING NUMERAL IS NOT PART OF THE NAME. `Eliphalet Atkins 2`
            # means two letters were waiting for him, and the gazetteer keys people
            # on the whole normalized name -- so carrying it through would have put
            # `William Elliot` and `William Elliot 3` in this town as two men, which
            # it measurably did: four people stood twice before this line was here.
            # The count is kept, under its own name, because it is evidence about
            # correspondence and it is the page's own reading.
            printed = TRAILING_COUNT.sub("", row["printed"])
            waiting = row["printed"][len(printed):].strip()
            if ent.get("normalized") != printed:
                changed += 1
            ent["normalized"] = printed
            if waiting:
                ent["letters_waiting"] = int(waiting)
            else:
                ent.pop("letters_waiting", None)
            ent.pop("completed_from", None)
            ent["reading"] = "scan_verified"
            ent["read_at_image"] = impressions
            ent["printed_line"] = "%s %d" % (row["column"], row["line"])
        claim["reading"] = "scan_verified"
        claim["reading_note"] = (
            "READ AT THE PAGE IMAGES (T-0424): %s page 4 column 2, and the same "
            "standing type at %s. The printed list is 170 lines in two alphabetical "
            "sub-columns of 85, and every entity below carries the line it stands "
            "on. %s"
            % (impressions[1], impressions[0],
               "Every reading in this claim is settled at the image."
               if not unsettled else
               "%d of this claim's readings are NOT settled at the image and keep "
               "`transcription_mediated` on their own entity, with the reason: %s."
               % (len(unsettled), "; ".join("`%s`" % u for u in unsettled))))
    EXTRACTED.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf8")
    print("%d readings settled at the image; %d rewritten this run"
          % (len([r for r in res["rows"] if r["line"] is not None]), changed))


def report(res):
    print("THE PRINTINGS -- the Chicago post office's 1 January 1834 return,")
    print("counted by its own body text, in the Chicago Democrat:\n")
    for p in res["printings"]:
        print("  %s  %-10s lines %-22s %s"
              % (p["date"], p["vol"],
                 ",".join("%d+%d" % seg for seg in p["segments"]),
                 p["fingerprint"][:44]))
        print("      date line: %s" % p["dateline"])
    if res["missing"]:
        print("\n  NOT RESOLVED HERE (no deposit on this checkout): %s"
              % ", ".join(res["missing"]))
        return
    print("\n  %d printings, every issue from Vol. I No. 7 to No. 15 without a"
          % len(res["printings"]))
    print("  break. The 1834-03-04 crop T-0312 read is the LAST of them,")
    print("  not a return of its own.\n")
    print("A SECOND OFFICE runs its own 1 January 1834 return in the same weeks")
    print("and is NOT Chicago's:")
    for date, vol, line, text in res["other_office"]:
        print("  %s  %-10s line %-5d  %s" % (date, vol, line, text))
    rows = res["rows"]
    cut = [r for r in rows if r["cut"]]
    done = [r for r in cut if r["proposal"]]
    split = [r for r in cut if r["printings_disagree"]]
    twice = [r for r in cut if r["surname_twice_in_list"]]
    lone = [r for r in cut if not r["proposal"] and not r["printings_disagree"]
            and not r["surname_twice_in_list"] and r["witnesses"]]
    none = [r for r in cut if not r["witnesses"]
            and not r["surname_twice_in_list"]]
    print("\nTHE CONCORDANCE -- %d names minted off the 1834-03-04 crops, %d of them"
          % (len(rows), len(cut)))
    print("cut on the left edge:")
    print("  %3d completed by two or more printings setting the same forename"
          % len(done))
    print("  %3d left alone because the printings disagree" % len(split))
    print("  %3d left alone: no two printings set the same forename" % len(lone))
    print("  %3d left alone: the list carries two of that surname" % len(twice))
    print("  %3d with no witness at all in the other eight printings\n" % len(none))
    for r in cut:
        if r["proposal"]:
            print("  -> %-26s %s   (%d printings)"
                  % (r["normalized"][:26], r["proposal"],
                     len(r["printings_agreeing"])))
        elif r["surname_twice_in_list"]:
            print("  == %-26s two of this surname stand in the list; the crop "
                  "cannot say which" % r["normalized"][:26])
        elif r["printings_disagree"]:
            print("  != %-26s the printings disagree: %s"
                  % (r["normalized"][:26], "; ".join(r["printings_disagree"])))
        else:
            print("  ?  %-26s %s" % (r["normalized"][:26],
                                     "no two printings agree" if r["witnesses"]
                                     else "no witness"))
        for w in r["witnesses"][:4]:
            print("        %s line %-5d  %s" % (w["date"], w["line"], w["as_set"]))


def self_test():
    """The assertions this tool's findings rest on."""
    ok = True

    def check(label, cond):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + label)
        ok = ok and bool(cond)

    check("the fold closes the scans' own letter confusions",
          fold("Elliot") == fold("Eliiot") == fold("E1liot")
          and fold("Miner") == fold("Miner"))
    check("the fold keeps three surnames the loose version merged",
          len({fold("Bennett"), fold("Benton"), fold("Bonnet")}) == 3
          and fold("Delano") != fold("Delaney"))
    check("a surname is read out of a minted reading with its forename cut",
          surname_of("[…]ell Baldwin") == "Baldwin"
          and surname_of("[?] E. Benton") == "Benton")
    check("a name-shaped reading is found where the scan ran a column together",
          any(s["surname"] == "Anderson" for s in
              settings(["Eliphalet Atkins 2 J..W. Anderson Constant Abbott"],
                       [(1, 1)])))
    res = concordance()
    if res["missing"]:
        print("  skip  the deposit is not on this checkout; "
              "the corpus assertions cannot run here")
        return ok
    check("nine printings resolve", len(res["printings"]) == 9)
    check("the 1834-03-04 crop is one of them", res["subject_present"])
    # The printings are identified by their BODY TEXT, so the assertion is about
    # the body and not the heading: three of the eight headings are cut or
    # illegible, and one crop (1834-01-28) has lost the A's off the top of the
    # column altogether, so no single name stands in all eight.
    subject_surnames = {r["surname_key"] for r in res["rows"] if len(r["surname_key"]) >= 4}
    shared = [len({fold(s["surname"]) for s in p["settings"]} & subject_surnames)
              for p in res["printings"] if p["date"] != SUBJECT]
    check("every other printing shares at least six surnames with the subject's list",
          shared and min(shared) >= 6)
    cut = [r for r in res["rows"] if r["cut"]]
    check("the crops' cut names are the bulk of what T-0312 minted",
          len(cut) >= 30)
    check("the concordance repairs some of them and invents none",
          0 < len([r for r in cut if r["proposal"]]) <= len(cut))
    check("no name is both proposed and reported as disagreed",
          not any(r["proposal"] and r["printings_disagree"] for r in res["rows"]))
    check("no completion is handed to two lines of the same surname",
          len([r["proposal"] for r in res["rows"] if r["proposal"]])
          == len({r["proposal"] for r in res["rows"] if r["proposal"]}))
    scan = scan_alignment()
    doc = scan["scan"]
    check("the page images carry the whole printed list, 170 lines in two columns of 85",
          doc["counts"]["printed_lines"] == 170
          and len(scan["columns"]["left"]) == len(scan["columns"]["right"]) == 85)
    check("the printed length is a count and not a floor: it exceeds every minting",
          doc["counts"]["printed_lines"] > 97
          and doc["counts"]["printed_lines"] > len(subject_names()))
    check("a letters-waiting count never reaches a person's name",
          not [e for c in json.loads(EXTRACTED.read_text(encoding="utf8"))["claims"]
               if c["id"] in CLAIM_COLUMN for e in c.get("entities", [])
               if re.search(r"\s[2-9]$", e["normalized"])])
    check("a printed surname is read off the line, past the count and past `& Co.`",
          printed_surname("Eliphalet Atkins 2") == "Atkins"
          and printed_surname("Jesse B. Winn & Co.") == "Winn"
          and printed_surname("Lamira & Laura Carrier") == "Carrier")
    aligned = [r for r in scan["rows"] if r["column"]]
    check("every minted reading is walked against the sub-column its crop came from",
          len(aligned) == len(subject_names()) - 1 and len(aligned) == 78)
    check("the walk never goes backwards inside a sub-column",
          all(all(a < b for a, b in zip(
              [r["line"] for r in aligned if r["column"] == col and r["line"]],
              [r["line"] for r in aligned if r["column"] == col and r["line"]][1:]))
              for col in ("left", "right")))
    check("the image settles the readings the concordance had to leave alone",
          len([r for r in aligned if r["cut"] and r["line"]]) >= 25)
    check("a reading whose neighbours leave a window of one is placed, and a wider "
          "window is refused",
          any(r["by"] == "position" for r in aligned)
          and all(r["window"] and r["window"][0] != r["window"][1]
                  for r in aligned if r["cut"] and r["line"] is None))
    check("a crop keeps the tail of its line, so `[…]as Bennett` is the Bennett "
          "whose forename ends in `as`",
          any(r["printed"] == "Thomas Bennett" and "as Bennett" in r["normalized"]
              for r in aligned))
    check("the image contradicts the concordance where the concordance guessed",
          any(r["printed"] == "Miranda Miner 2" for r in aligned)
          and any(r["printed"] == "Chester Marshall 2" for r in aligned))
    check("the two Temples, two Miners and two Bennetts are separated by position",
          {r["printed"] for r in aligned if r["printed"]
           and r["printed"].endswith(("Temple", "Temple 3"))}
          == {"Peter Temple 3", "Lewis Temple"})
    check("edit distance one joins two scans of one setting and not two names",
          within_one(fold("Wim."), fold("Wm."))
          and within_one(fold("Russell"), fold("Russel"))
          and not within_one(fold("Hiram"), fold("Thomas"))
          and not within_one(fold("Delano"), fold("Delaney")))
    return ok


def apply(res):
    """Write the concordance's completions into claims c026 and c027.

    Only `normalized` moves. `as_printed` keeps the 1834-03-04 setting verbatim, so
    the completion is visible as a completion beside the damage it repairs, and
    `completed_from` names the printings that carry it. Re-running is a no-op.
    """
    doc = json.loads(EXTRACTED.read_text(encoding="utf8"))
    by_printed = {}
    for r in res["rows"]:
        by_printed.setdefault((r["claim"], r["as_printed"]), r)
    changed = 0
    for claim in doc["claims"]:
        if claim["id"] not in ("c026", "c027"):
            continue
        for ent in claim.get("entities", []):
            row = by_printed.get((claim["id"], ent["as_printed"]))
            if not row or not row["cut"] or not row["proposal"]:
                continue
            # RULING 2: a scan_verified reading outranks a transcription, so a
            # reading the page images already settled is never rewritten from the
            # concordance -- not even when the concordance agrees with it.
            if ent.get("read_at_image"):
                continue
            dates = row["printings_agreeing"]
            if ent["normalized"] != row["proposal"]:
                changed += 1
            ent["normalized"] = row["proposal"]
            ent["completed_from"] = dates
    EXTRACTED.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf8")
    print("%d readings completed from the concordance; %d rewritten this run"
          % (sum(1 for r in res["rows"] if r["cut"] and r["proposal"]), changed))


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        sys.exit(0 if self_test() else 1)
    if "--scan" in args:
        scan_report(scan_alignment())
        return
    if "--apply-scan" in args:
        apply_scan(scan_alignment())
        return
    res = concordance()
    if "--apply" in args:
        if res["missing"]:
            sys.exit("the deposit is not on this checkout; nothing to apply")
        apply(res)
    elif "--json" in args:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        report(res)


if __name__ == "__main__":
    main()
