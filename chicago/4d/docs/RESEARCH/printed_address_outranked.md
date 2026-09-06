# Six houses whose printed address a later printing outranks — the adjudication

**Ticket:** T-0773 · **Derived by:** `tools/measure_placement_silence.py` ·
**Declared in:** `data/research/newspapers/identity.json` (`anchor_changes`,
`refused_anchor_changes`) · **Corpus:** the *Chicago Democrat* 1833-11 to 1835-08 and the
*Chicago American* 1835-06 to 1835-08

`compile_gazetteer.py` mints a house from the earliest printing the corpus carries and
keeps every later printing as a dated READING. T-0440 repaired the population where the
minting printing said nothing about an address and a later one did — silence does not
contradict speech, so the earliest *placing* reading is taken. It deliberately stopped
there. The other population is this one: **the live placement already places the house,
and a later printing places it more narrowly or somewhere else.** Preferring one printed
address to another is a judgement about a house that MOVED or an advertisement reset from
fresher copy, and the corpus rarely says which — so only an authored `anchor_changes` rule
may make it.

Six houses stood in that count. **One is a real move. Five are not, and each is not one
for a different reason.** Every ruling below is declared in `identity.json` and the
compiler checks its kind against the readings rather than taking this file's word.

| house | held | outranked by | ruling |
|---|---|---|---|
| `business_g_spring` | relative | corner | **anchor change** — the office moved |
| `business_j_k_botsford` | relative | corner | refused · `printed_in_the_same_weeks` |
| `business_j_s_c_hogan` | street_only | relative | refused · `silence_is_not_an_anchor` |
| `business_newberry_dole` | street_only | relative | refused · `silence_is_not_an_anchor` |
| `business_rockwell_cabinet_furniture_warehouse` | street_only | relative | refused · `after_the_scene_date` |
| `business_samuel_lewis` | street_only | relative | refused · `after_the_scene_date` |

`business_p_pruyne_co` was the seventh when the ticket was written and left the population
when T-0412 landed: the corner it was outranked by came off a building it advertised as
VENDOR, and a vendor's notice may no longer mint a placement on the vendor's own house.

---

## 1. G. Spring — the one that moved

Giles Spring, attorney and counsellor at law, advertises under **two cards** and the date
lines say so themselves.

| printings | date line | address as printed |
|---|---|---|
| 1833-12-17 … 1834-11-26 (5 readings) | Chicago, Dec. 17, 1833 | OFFICE second door west from the corner of Franklin and South Water streets |
| 1835-05-20, 1835-08-05 | Chicago, Dec. 3, 1834 | OFFICE, first door north from the Tre[mont] House, on Dearborn-street |

Two landmarks, and this project holds both: the corner of Franklin and South Water is a
crossing at the west end of South Water Street; the first Tremont House stands on the
north-west corner of Lake and Dearborn. They are not two spellings of one place.

The corpus alone brackets the move between **1834-11-26** and **1835-05-20**, which is
five and a half months. The advertisement's own new copy date, **3 December 1834**, falls
one week after the last printing of the old address and narrows it much further — a date
line states when the copy was WRITTEN, which is the earliest the new address was being
advertised and not the day the books were carried up the street. That distinction, and the
fact that nothing says the old rooms were given up, is what the rule's `cannot_say` holds.

**What the town gains.** The register moves G. Spring from `new_building` at
franklin+south_water to `street_only` on Dearborn Street, and the street-face adoption
policy seats him on a Dearborn face — his own card's street, where before he stood on a
corner his card had stopped naming eight months before the scene date. The anchor itself,
`the Tremont House`, does not yet resolve to `tremont_house_1`: the landmark matcher
requires the committed name and the paper prints a shorter one. **T-0406 is that ticket**,
and when it lands this row resolves to the structure without another reading being made.

## 2. J. K. Botsford — printed in the same weeks

`printed_in_the_same_weeks`. T-0324 read every printing of both addresses and settled
them: *"next door to Graves' Tavern"* and *"the corner of Dearborn and Lake streets"* are
**one frontage**. Both run in a single issue — 1834-04-01 c009 and c010 — six weeks after
the move a reordering would have to record; and the corner card is re-set with fresh date
lines (Feb 4, Feb 24, Apr 22) while the tavern card keeps running, which is not what a man
does with an advertisement he has forgotten to pull. Graves' Tavern **is** that corner: it
is the Mansion House, held here since 2026-08-11 on the north side of Lake Street just
east of Dearborn. An anchor rule may only be written where one anchor stops before the next
starts, so any dates one stated here would be false whatever it said about the ground.
`docs/RESEARCH/botsford_graves_1834.md` is the reading.

## 3. J. S. C. Hogan and Newberry & Dole — silence is not an anchor

`silence_is_not_an_anchor`. In both, the reading the house is placed by names **no anchor
at all** and the reading that outranks it names one. One anchor is not a change, and
dressing the silent printing up as the first of two would assert that the anchor CHANGED
on a date when what changed is how much of the address the card printed.

* **J. S. C. Hogan** — 1834-03-25 gives South Water Street and stops; 1834-06-11 gives
  nothing; *"in South Water Street, one [door from] the Post Office"* runs from 1834-08-13
  to the scene date.
* **Newberry & Dole** — the live reading names neither an anchor nor a street the model
  holds, and the register reads it `unplaceable` on exactly that ground; 1834-05-14 reads
  *"opposite to Fort Dearborn"*. The substance here is larger than a reordering.
  `docs/RESEARCH/dole_warehouse_south.md` carries a standing guard: **Newberry & Dole's
  forwarding warehouse stood on the NORTH bank**, immediately east of where the Rush Street
  bridge later stood, and is NOT the George W. Dole warehouse this project models south of
  the river — *"do not merge the two, and do not move this one to the river."* "Opposite to
  Fort Dearborn" agrees with that north bank and would place a building the town does not
  hold at all: a structure to argue for, not an anchor to reorder. T-0396 holds this firm's
  other open question and nothing here touches it.

**What is genuinely owed** is the question T-0440 answered one rank lower: may a printing
that named a street and no anchor be superseded by a printing of the same house that names
one? That is a rule about SILENCE and not a judgement between two addresses. **T-0860**
carries it.

## 4. Rockwell and Samuel Lewis — after the scene date

`after_the_scene_date`. AGENTS.md rule 3: an address first printed after 1 July 1835 was
not up on 1 July 1835, and this town is not placed on the strength of it.

* **Rockwell's cabinet furniture warehouse** — *"the stand formerly occupied by Clark &
  Co."* is printed once, 1835-07-04, three days after the scene date. The live placement is
  the 1835-06-27 reading, South Water Street and nothing narrower.
* **Samuel Lewis** — every printing runs after the scene date and the one that outranks the
  rest is the last of them, 1835-08-12: *"call at [h]i[s] room [in] South [Wa]ter street,
  (A. Garrett's Auction Room)"*, six weeks outside the scene.

What is missing in both is not a judgement between two printed addresses. It is a printing
inside the scene — and if the corpus ever carries one, each refusal fails its own kind's
guard rather than going quietly out of date.

---

## What the mechanism now says

`tools/measure_placement_silence.py` no longer prints one number for this population. It
prints three: **ruled** by an authored change, **refused** with a checked kind, and
**waiting** on a judgement nobody has made. The last is the only one the queue was ever
asking about, and it is 0.

Two repairs fell out of writing the first rule, both of which had been invisible because
Mason & Co. — the only anchor change before this — has two anchors on ONE street and one
reading apiece:

1. **A reading could be silently dropped from a history.** The lookup a declaration was
   matched against was keyed on the anchor STRING, and `absorb_reading` keeps a class
   apart from a class, so G. Spring's corner — printed once as a relative offset and once
   as a corner under the same words — kept whichever came last. Guard 4, whose whole job is
   to refuse a dropped printing, saw the string claimed and passed. The window it printed
   was 1834-05-28 to 1834-10-15 for a corner the papers carried from December 1833 to
   November 1834.
2. **A house's `street` did not move with its anchor.** `compile_register` reads that field
   for `street_id`, so an anchor change across town left the register placing the house on
   the street it had left. It now takes the live reading's own street, under the same two
   limits the T-0440 pass takes it under, and writes down what it replaced.

And one in the register: a reading that lost the word *corner* — G. Spring's `Franklin and
South Water streets` of 1834-05-28 — resolves to a reach of one of the streets its own
crossing is made of. That is a coarser reading of one place, not a second place, and the
"one landmark is one place" guard no longer calls it one. A street the window's corners do
not cross still fails it, and so do two structures, two businesses or two different
corners.
