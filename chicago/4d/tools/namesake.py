#!/usr/bin/env python3
"""Which of several people of a surname does a reading name? (T-0697)

The land-sales resident crosswalk proposes that a purchaser in the Illinois
tract-sales register is a person the town already holds. Its rule, written when
the residents layer held 848 names, was: the surname agrees, EXACTLY ONE person
of that surname exists, and the forename agrees. The middle clause is a COUNT OF
NAMESAKES, and a count of namesakes is not evidence about the reading in hand —
it is a fact about the rest of the town. So the rule fires LESS as the town grows
truer: T-0514 seated 531 people and the register's rulings went DOWN, nine
matches turning ambiguous against six becoming possible for the first time, with
nothing new read (T-0670, where this was found).

THE RULING, and it is two answers.

  THE FORENAME DECIDES, ACROSS THE RIVALS. A reading is put to EVERY person of
  the surname and named onto the ONE it agrees with, on the merge rules this
  project already ratified in `data/research/residents/identity_master.json` and
  restated nowhere else: M1 the same name, M2 an initial attaching to the one
  full forename carrying it, M3 a middle initial present on one side and absent
  on the other WITH NO RIVAL CARRYING A DIFFERENT ONE, R3 an initial with two or
  more rivals, R4 two different full forenames behind one initial. Two survivors
  or none, and the reading is refused with the rivals NAMED — which is what the
  old rule did to all of them, and is right when it is the forename saying so.

  NO SECOND DISCRIMINATOR MAY BREAK WHAT IS LEFT. T-0697 asked whether a purchase
  date inside the person's own bounds, a trade, or a lot the person is otherwise
  placed on could pick a side. All three are refused, and the reasons are in
  REFUSED_DISCRIMINATORS below rather than in prose, so a later run reviving one
  argues with a record. This is the same shape as the directories' ruling
  (T-0696, `tools/tiebreak.py`), which allowed a trade to NARROW a tie and
  refused a premises and a year — and it lands harder here because the register
  prints no trade at all.

THE TERMS, written out so they read back without the code:

  1. A SUFFIX IS NOT A NAME. `JR`, `SR`, `ESQ` are dropped from both sides before
     anything is compared, and so are the firm words the register sets after a
     name — `ET CO`, `AND CO`, `AS` — which are not forenames and must never be
     read as a middle initial.
  2. A MIDDLE INITIAL IS THE FIRST LETTER OF THE SECOND GIVEN WORD, whether that
     word is an initial or a name in full: `Walter Loomis` carries L. Two middle
     initials that disagree REFUSE the pair (R4's reasoning at one letter's
     remove) — `KING JOHN R` is not John Lyle King.
  3. M3'S GUARD IS THE WHOLE OF M3. Where the pair agrees only because one side
     is silent about a middle initial, ANY OTHER rival of the surname whose
     forename also agrees and whose middle initial differs REFUSES the reading:
     `WRIGHT JOHN F` is not John Wright while John S. Wright stands beside him.
  4. A SUFFIX SAYS WHICH MAN OF THE NAME IS MEANT, and a card that does not carry
     one cannot answer it. `CHURCH THOS JR` is the son of a Thomas Church, and the
     town holds one Thomas Church who is not said to be either — so the reading is
     REFUSED rather than named onto him. The same word does the same work between
     two readings of one person, in `collide`.
  5. THE GRADE IS THE READING'S, NOT THE RIVALRY'S. A full forename agreeing in
     full is `forename_agrees`; an initial standing for it is `initial_agrees`,
     the weaker grade, exactly as before. Naming one of several rivals does not
     make a reading stronger, and it does not make it weaker either.
  6. A REFUSAL NAMES THE RIVALS. An absent match reads exactly like a pair
     nobody looked at, and the old rule's "there are 5" said which count refused
     the reading without ever saying which five people.

Run it directly for its self-test: `python3 tools/namesake.py --self-test`.
"""
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import name_agreement  # noqa: E402  (the forename rule this imports rather than restates)

SUFFIXES = ("JR", "SR", "JUN", "SEN", "ESQ", "2D", "II", "III")

# What the register sets AFTER a purchaser's name when the buyer is a firm or an
# agent. None is a forename and none may be read as a middle initial.
FIRM_WORDS = ("ET", "CO", "AND", "COMPANY", "AS", "AGENT", "TRUSTEE", "HEIRS", "OF", "&")

# The three discriminators T-0697 asked about, all refused, each with the reason
# kept beside the refusal rather than in a paragraph somewhere.
REFUSED_DISCRIMINATORS = {
    "purchase_date": "A purchase date tested against the person's arrival refuses nobody. "
                     "A man may enter ground in a county he has not yet moved to, and in "
                     "this register most of them did: 318 of the 387 ring sales fall in "
                     "1835, a year behind the town's own lots, and the register states a "
                     "residence on 32 of them. So an arrival AFTER the purchase does not "
                     "refuse a rival and an arrival BEFORE it does not name him.",
    "trade": "The register prints no trade. Its only column near one is Social Status, "
             "which is blank on 874 of 953 rows and elsewhere a single letter — I, F, A — "
             "that is a status code and not an occupation. There is nothing to compare, "
             "which is why the directories' answer (T-0696, a trade may NARROW a tie) has "
             "no counterpart here.",
    "placement": "Preferring the rival the town has already placed on the ground is how a "
                 "reconstruction invents a fact — T-0696 refused a premises for this "
                 "reason and it holds harder here, because a tract is not a dwelling. The "
                 "register records an entry, not a residence, and `ground.json` puts a "
                 "tract on the map without claiming anybody stood on it.",
    "residence_column": "The register's Residence column cannot separate two townspeople: "
                        "it reads COOK, a state, or UNKNOWN, and every rival of a surname "
                        "in the residents layer is a person of Cook County already.",
}


def _words(given):
    """The given-name words of a reading: suffixes, firm words and titles dropped.

    The titles come from `name_agreement.TITLES` rather than a second list here —
    `Mrs Rufus Brown` prints no forename of her own, and a rule that read `Mrs` as
    one would name her onto any reading at all.
    """
    out = []
    for raw in str(given or "").replace(".", " ").split():
        w = raw.strip(",").upper()
        if not w or w in SUFFIXES or w in FIRM_WORDS:
            continue
        if w.lower() in name_agreement.TITLES:
            continue
        out.append(w)
    return out


def suffix_of(given):
    """`JR`, `SEN` — the word that says WHICH man of the name, or None."""
    for raw in str(given or "").replace(".", " ").split():
        w = raw.strip(",").upper()
        if w in SUFFIXES:
            return "SR" if w in ("SEN", "SR") else ("JR" if w in ("JUN", "JR") else w)
    return None


def middle_initial(given):
    """The first letter of the second given word, or None where there is none."""
    words = _words(given)
    return words[1][0] if len(words) > 1 else None


def _first(given):
    words = _words(given)
    return words[0] if words else ""


def forenames_agree(reading, resident):
    """(agrees?, grade, why) for one reading against one person of the surname.

    The FIRST given word only; the middle initial is rule 2's business. An
    initial on either side attaches to a full forename beginning with it (M2),
    and two full forenames are put to `name_agreement.agrees`, which is the
    tightening T-0670 made for the directories and refuses Thomas L. onto Titus H.
    """
    a, b = _first(reading), _first(resident)
    if not a or not b:
        return False, None, "one side prints no forename of its own"
    if len(a) == 1 or len(b) == 1:
        if a[0] == b[0]:
            return True, "initial_agrees", "an initial standing for the forename (M2)"
        return False, None, "the initials differ"
    ok, why = name_agreement.agrees(a, b)
    if ok:
        return True, "forename_agrees", "the forenames agree in full — %s (M1)" % why
    return False, None, "two full forenames that do not agree (R4)"


def choose(reading, candidates):
    """Name the ONE person of a surname a reading meets, or refuse with the rivals.

    `reading` is the purchaser's given name as read; `candidates` is a list of
    `{"key", "given", "name"}`, one per person of that surname in the residents
    layer. Returns `{"named", "grade", "why", "rivals"}` — `named` is the key of
    the one person the reading names, or None.
    """
    mine = middle_initial(reading)
    rivals, agreeing = [], []
    for c in candidates:
        ok, grade, why = forenames_agree(reading, c["given"])
        theirs = middle_initial(c["given"])
        row = {"key": c["key"], "name": c.get("name") or c["given"],
               "forename_agrees": ok, "why": why,
               "middle_initial": theirs, "reading_middle_initial": mine}
        if ok and mine and theirs and mine[0] != theirs[0]:
            row["outcome"] = "refused_on_the_middle_initial"
            row["why"] = ("the forenames agree and the middle initials do not — %s against "
                          "%s (rule 2)" % (mine[0], theirs[0]))
        elif ok:
            row["outcome"] = "survives"
            agreeing.append((c, grade, theirs))
        else:
            row["outcome"] = "refused_on_the_forename"
        rivals.append(row)

    if len(agreeing) != 1:
        why = ("the forename names %d of the %d %s of this surname, and a reading is named "
               "onto exactly one or onto none%s"
               % (len(agreeing), len(candidates),
                  "person" if len(candidates) == 1 else "people",
                  " (R3)" if len(agreeing) > 1 and len(_first(reading)) == 1 else ""))
        return {"named": None, "grade": None, "why": why, "rivals": rivals}

    winner, grade, theirs = agreeing[0]
    # Rule 4 — a suffix on one side only. It says WHICH man of the name the register
    # meant, and a card that carries none cannot answer it.
    mine_sfx, their_sfx = suffix_of(reading), suffix_of(winner["given"])
    if mine_sfx != their_sfx:
        for row in rivals:
            if row["key"] == winner["key"]:
                row["outcome"] = "refused_on_the_suffix"
        return {
            "named": None, "grade": None,
            "why": ("the reading carries the suffix %s and %s carries %s, and a suffix says "
                    "which man of the name is meant"
                    % (mine_sfx or "none", winner.get("name") or winner["given"],
                       their_sfx or "none")),
            "rivals": rivals,
        }
    # Rule 3 — M3's guard. The pair agrees only because one side is silent about a
    # middle initial, so any OTHER rival whose forename agrees and whose middle
    # initial differs refuses the reading rather than losing to it.
    if (mine is None) != (theirs is None):
        for row in rivals:
            if row["key"] == winner["key"] or not row["forename_agrees"]:
                continue
            other = row["middle_initial"]
            if other and other[0] != (mine or theirs)[0]:
                row["outcome"] = "refuses_the_reading_under_m3"
                return {
                    "named": None, "grade": None,
                    "why": ("the middle initial is on one side only and %s carries a "
                            "different one, so M3's guard refuses the reading"
                            % row["name"]),
                    "rivals": rivals,
                }
    return {"named": winner["key"], "grade": grade,
            "why": ("the forename names %s of the %d %s of this surname"
                    % (winner.get("name") or winner["given"], len(candidates),
                       "person" if len(candidates) == 1 else "people")),
            "rivals": rivals}


def collide(readings):
    """Two readings named onto ONE person: are they the same man, or two?

    `readings` is a list of `{"key", "given"}` — every purchaser spelling that
    `choose` named onto the same resident. They are the SAME man where the
    forenames agree, the middle initials do not conflict, and no suffix says
    which of two men of the name is meant. Otherwise the resident's own reading
    is too thin to say which purchaser he is, and EVERY reading in the group is
    refused with the rivals named — never the first one kept and the rest thrown
    away, which would be the count of namesakes again, wearing a hat.

    `PRUYNE P`, `PRUYNE P AND CO` and `PRUYNE PETER` are one man. `BOND HARVEY`
    and `BOND HEMAN` both meet an `H Bond` and are two. `WENTWORTH ELIJAH` and
    `WENTWORTH ELIJAH SEN` are the Wolf Point father and son, and the town holds
    one card: two, until a source says which.
    """
    conflicts = []
    for i, a in enumerate(readings):
        for b in readings[i + 1:]:
            ok, _grade, _why = forenames_agree(a["given"], b["given"])
            ma, mb = middle_initial(a["given"]), middle_initial(b["given"])
            sa, sb = suffix_of(a["given"]), suffix_of(b["given"])
            if not ok:
                conflicts.append((a["key"], b["key"], "the forenames do not agree"))
            elif ma and mb and ma[0] != mb[0]:
                conflicts.append((a["key"], b["key"],
                                  "the middle initials differ — %s against %s" % (ma[0], mb[0])))
            elif sa != sb and (sa or sb):
                conflicts.append((a["key"], b["key"],
                                  "a suffix says which man of the name is meant — %s against %s"
                                  % (sa or "none", sb or "none")))
    if not conflicts:
        return {"same_man": True, "why": None, "conflicts": []}
    return {
        "same_man": False,
        "why": ("two readings this rule named onto one person are not the same man: %s"
                % "; ".join("%s against %s (%s)" % c for c in conflicts)),
        "conflicts": [{"a": a, "b": b, "why": w} for a, b, w in conflicts],
    }


def self_test():
    fired = []

    def named(reading, cands):
        return choose(reading, [{"key": k, "given": g, "name": g} for k, g in cands])

    # The finding: a count of namesakes refused a reading its own forename decides.
    r = named("PHILO", [("philo", "Philo"), ("benjamin", "Benjamin"), ("ann", "Ann")])
    if r["named"] != "philo":
        fired.append("a full forename must name the one rival it agrees with, got %r" % r["named"])

    # M3's guard: a middle initial on one side only, with a rival carrying another.
    r = named("JOHN F", [("plain", "John"), ("s", "John S.")])
    if r["named"] is not None:
        fired.append("M3's guard must refuse JOHN F while John S. stands beside John")

    # …and the same reading is named where no rival carries a different one.
    r = named("JOHN F", [("plain", "John"), ("mary", "Mary")])
    if r["named"] != "plain":
        fired.append("M3 must name John where no rival carries a different middle initial")

    # Rule 2: two middle initials that disagree refuse the pair.
    r = named("JOHN R", [("lyle", "John Lyle")])
    if r["named"] is not None:
        fired.append("KING JOHN R must not be named onto John Lyle King")

    # M2: an initial attaches to the one full forename carrying it, and to no more.
    r = named("E H", [("edward", "Edward H."), ("mary", "Mary")])
    if r["named"] != "edward" or r["grade"] != "initial_agrees":
        fired.append("an initial must attach at the weaker grade, got %r" % (r["grade"],))
    r = named("J", [("john", "John"), ("james", "James")])
    if r["named"] is not None:
        fired.append("R3: an initial with two rivals must be refused, not guessed at")

    # Rule 4: a suffix on one side only refuses, rather than naming the one card.
    r = named("THOS JR", [("thomas", "Thomas")])
    if r["named"] is not None:
        fired.append("CHURCH THOS JR must not be named onto a Thomas Church carrying no suffix")

    # A title is not a forename.
    r = named("JEREMIAH", [("mrs", "Mrs Rufus")])
    if r["named"] is not None:
        fired.append("a reading must not be named onto a person who prints no forename")

    # A refusal names the rivals it was refused against.
    r = named("JOHN", [("a", "William"), ("b", "Mary")])
    if r["named"] is not None or len(r["rivals"]) != 2:
        fired.append("a refusal must name every rival it was put to")

    # The collision rule.
    same = collide([{"key": "a", "given": "P"}, {"key": "b", "given": "PETER"},
                    {"key": "c", "given": "P AND CO"}])
    if not same["same_man"]:
        fired.append("the three Pruyne spellings are one man")
    two = collide([{"key": "a", "given": "HARVEY"}, {"key": "b", "given": "HEMAN"}])
    if two["same_man"]:
        fired.append("Harvey and Heman Bond are two men, not one H Bond")
    suffixed = collide([{"key": "a", "given": "ELIJAH"}, {"key": "b", "given": "ELIJAH SEN"}])
    if suffixed["same_man"]:
        fired.append("a suffix says which man of the name is meant, and must not be folded away")
    mids = collide([{"key": "a", "given": "JOHN K"}, {"key": "b", "given": "JOHN A"}])
    if mids["same_man"]:
        fired.append("two middle initials that differ are two men")

    # The refused discriminators stay refused, and stay explained.
    for name in ("purchase_date", "trade", "placement", "residence_column"):
        if len(REFUSED_DISCRIMINATORS.get(name, "")) < 80:
            fired.append("the %s refusal must carry its reason" % name)

    if fired:
        for line in fired:
            print("  " + line, file=sys.stderr)
        print("namesake --self-test: %d case(s) failed" % len(fired), file=sys.stderr)
        return 1
    print("namesake --self-test: 9 naming cases and 4 collision cases hold")
    return 0


if __name__ == "__main__":
    sys.exit(self_test())
