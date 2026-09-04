#!/usr/bin/env python3
"""Does a printed forename agree with a resident's forename? (T-0670)

The directory crosswalks match a later entry to a person of 1835 on the folded
SURNAME plus the FIRST INITIAL of the given name. That rule was written when the
residents layer held 848 names, and it was safe then because a surname plus an
initial was very nearly unique in a town that size. T-0514 minted 532 more
people, and the rule then declared merges onto people it had never had an anchor
for — `Abbott, Thomas L.` onto Titus H. Abbott, `Hogan, Michael` onto Mary
Hogan, `Bristol, Calvin D.` onto Charles L. Bristol. Every one of them agrees on
the initial and disagrees on the name behind it.

The tightening, written out so it reads back without the code:

  Where BOTH readings print a FULL forename and the two full forenames disagree,
  the match is REFUSED. An initial standing against a full name is untouched and
  stays a match — that is the case the initial rule exists to serve, and it is
  most of what it catches.

  Two full forenames AGREE when any of these holds, and each is a thing a
  compositor or a scanner actually did to these two volumes:
    same          — they fold to the same string.
    prefix        — one is a prefix of the other ("Alex."/Alexander).
    contraction   — the pair is in CONTRACTIONS below, which is the printers'
                    own list of contractions as they stand in these volumes.
                    It is written out rather than inferred: a rule that guesses
                    which letters an abbreviation may drop merges Ruel Rose onto
                    Russell Rose, and Ruel is a name, not a contraction.
    spelling      — both are at least five letters and they differ by one
                    (Absalom/Absolom, Shubal/Shubael). Five is the floor because
                    at four letters one letter separates Mary from Mark.

  A refusal is FILED, never dropped: the crosswalk reports the resident, the
  entry as printed and both forenames, so the reading can be argued with. Where
  the printed forename is GARBLED — the scanner's `C!;as.` for Chas., `Iia` for
  Ira — the refusal says so, because that is a transcription defect and not a
  disagreement between two people (T-0695).

This module is the rule; the crosswalks import it rather than restate it.
Run it directly for its self-test: `python3 tools/name_agreement.py --self-test`.
"""
import re
import sys

TITLES = ("mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj")
SUFFIXES = ("jr", "sr", "jun", "sen", "esq", "2d")

# The surname fold, plus the one confusion that shows up in the GIVEN names of
# these two volumes and not in the surnames: an `m` scanned as two strokes and
# read back as `in` — Norris's "Allen, Win." for Wm., "Taylor, Win.H." for
# Wm. H. It is the same confusion the surname fold already carries the other way
# round as `rn` -> `m`, and it is applied to both sides of every comparison.
FOLD = [(r"[^a-z]", ""), (r"^mc", "mac"), (r"ii", "n"), (r"rn", "m"),
        (r"in", "m"), (r"vv", "w"), (r"1", "l"), (r"0", "o")]

# The contractions as these two volumes print them. Read off the entries, not
# invented: each one stands in Fergus 1843 or Norris 1844 against a man the
# other volume or the residents layer names in full. Keys and values are folded.
CONTRACTIONS = {
    "wm": "william", "wilm": "william",
    "jas": "james", "jno": "john", "jn": "john",
    "thos": "thomas", "chas": "charles", "cas": "charles",
    "geo": "george", "robt": "robert", "danl": "daniel", "saml": "samuel",
    "benj": "benjamin", "richd": "richard", "edwd": "edward",
    "nathl": "nathaniel", "michl": "michael", "patk": "patrick",
    "fredk": "frederick", "alexr": "alexander", "matw": "matthew",
    "andw": "andrew", "hy": "henry", "jos": "joseph",
}

# Anything outside these is junk the printer did not set: the scanner's `>`, `!`,
# `;`, a stray digit. A forename carrying one is a GARBLED reading, and a refusal
# against a garbled reading is a transcription defect, not two different people.
CLEAN = re.compile(r"^[A-Za-z'’.\-]+$")


def fold(name):
    """Fold a name the way the crosswalks fold a surname."""
    s = (name or "").lower()
    for pat, rep in FOLD:
        s = re.sub(pat, rep, s)
    return s


def tokens(given):
    """The given name's words. Split on whitespace, commas and full stops, so
    the scanner's run-together `Win.H` reads as two words and the hyphenated
    `A-rthur` reads as one."""
    out = []
    for raw in re.split(r"[\s,.]+", given or ""):
        if not raw:
            continue
        bare = re.sub(r"[^A-Za-z]", "", raw).lower()
        if not bare or bare in TITLES or bare in SUFFIXES:
            continue
        out.append(raw)
    return out


def first_word(given):
    """The first word of the given name that is not a title — as printed."""
    t = tokens(given)
    return t[0] if t else ""


def initial(given):
    """The first initial, unchanged from the rule the crosswalks already use."""
    w = first_word(given)
    for ch in w:
        if ch.isalpha():
            return ch.lower()
    return ""


def is_full_forename(given):
    """A full forename, as against an initial: more than one letter."""
    return len(fold(first_word(given))) > 1


def garbled(given):
    """The printed forename carries a character no compositor set."""
    w = first_word(given)
    return bool(w) and not CLEAN.match(w)


def _one_letter_apart(a, b):
    if abs(len(a) - len(b)) > 1:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 1


def agrees(given_a, given_b):
    """(agree?, why) for the first forename of each reading.

    True with `initial` where either side prints only an initial — that case is
    the rule the crosswalks already make and this module does not touch it.
    """
    if not is_full_forename(given_a) or not is_full_forename(given_b):
        return True, "initial"
    a, b = fold(first_word(given_a)), fold(first_word(given_b))
    if a == b:
        return True, "same"
    if a.startswith(b) or b.startswith(a):
        return True, "contraction (prefix)"
    if CONTRACTIONS.get(a) == b or CONTRACTIONS.get(b) == a:
        return True, "contraction (printed)"
    if min(len(a), len(b)) >= 5 and _one_letter_apart(a, b):
        return True, "spelling variant"
    return False, "two full forenames that differ"


def refusal(resident_given, printed_given):
    """The record filed when the two full forenames disagree, or None."""
    ok, _ = agrees(resident_given, printed_given)
    if ok:
        return None
    bad = garbled(printed_given) or garbled(resident_given)
    return {
        "forename_1835": first_word(resident_given),
        "forename_printed": first_word(printed_given),
        "garbled_reading": bad,
        "rule": ("Both readings print a full forename and the two disagree: %r "
                 "against %r. An initial standing against a full name is a match; "
                 "two full names that differ are not.%s"
                 % (first_word(resident_given), first_word(printed_given),
                    " The printed forename is garbled, so this is a transcription "
                    "defect rather than two people (T-0695)." if bad else "")),
    }


CASES = [
    # (1835 reading, printed reading, agree?, what it is)
    ("Titus H", "Thomas L.", False, "the finding: T-0670's own example"),
    ("Mary", "Michael", False, "Hogan"),
    ("Pitman", "Peter H.", False, "Fisher"),
    ("Charles L", "Calvin D.", False, "Bristol"),
    ("Hanna E", "Henry", False, "Brown"),
    ("James", "John", False, "Burke"),
    ("Ruel", "Russell", False, "Rose — Ruel is a name, not a contraction of Russell"),
    ("Mary", "Mark T.", False, "Green — one letter apart, and four letters is too few"),
    ("F.", "Francis", True, "an initial against a full name stays a match"),
    ("William", "W.", True, "and the other way round"),
    ("Absolom", "Absalom", True, "a spelling"),
    ("Shubal Davis", "Shubael D.", True, "a spelling"),
    ("Alexander", "Alex.", True, "a contraction the prefix rule reads"),
    ("William", "Wm.", True, "a contraction the volumes print"),
    ("William", "Win.", True, "and the same one as the scanner read it"),
    ("William H", "Win.H", True, "run together, as Norris prints it"),
    ("Charles", "C!;as.", True, "garbled, but the contraction is still legible"),
    ("Mrs. Margaret", "Mary", False, "a title is not a forename"),
]


def self_test():
    fired = []
    for a, b, want, why in CASES:
        got, reason = agrees(a, b)
        if got != want:
            fired.append("%r vs %r: expected %s (%s), got %s (%s)"
                         % (a, b, want, why, got, reason))
    assert garbled("C!;as."), "a scanner artefact must read as garbled"
    assert not garbled("A-rthur"), "a hyphen is not an artefact"
    assert refusal("Titus H", "Thomas L.")["forename_printed"] == "Thomas"
    assert refusal("F.", "Francis") is None
    if fired:
        for line in fired:
            print("  " + line, file=sys.stderr)
        print("name_agreement --self-test: %d case(s) failed" % len(fired), file=sys.stderr)
        return 1
    print("name_agreement --self-test: %d cases hold" % len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else self_test())
