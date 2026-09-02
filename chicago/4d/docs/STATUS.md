YªçŠx-®éÜj×¢ëiºÚ+Š§j[h‘éÜ¢éíß¾zÛ9ßİ¸o+^²‰¢¶×# STATUS

## In progress 2026-09-02 â€” T-0463: a third 75-name research pass

**Resident identity research now covers 225 of 848 eligible real named people (26.5%),
with no reconstructed person admitted.** The third fixed cohort contributes 16 corroborated
enrichments, 15 explicitly unmerged candidates and 44 documented no-find outcomes.
Cumulatively the public layer carries 47 corroborated findings, 45 candidates and 133
no-finds. The manifest, findings, source registry, compiler, status and continuation ticket
are kept together so a held PR can resume without changing the sample.

This pass adds dated civic, legal, commercial, church, institutional and local-history
records, including Daniel Elston, Stephen F. Gale, Russel E. Heacock and Benjamin Jones.
Regional and later matches remain candidates where a direct 1833â€“35 Chicago bridge is
missing. Name ambiguity, geography and chronology are recorded as conflicts; surnames are
search leads only and create no heritage, lineage, immigration, kinship or occupation claim.
`docs/RESEARCH/resident_identity_pass_03_75.md` records the methods, limits and next-pass
priorities. The PR remains resumable if browser smoke cannot run in the current environment.

## Shipped 2026-09-01 â€” T-0462: the next 75 real names receive deep research

**Resident identity research now covers 150 of 848 eligible real named people
(17.7%), with no reconstructed person admitted.** The second fixed, non-overlapping
cohort contributes 27 corroborated enrichments, 23 explicitly unmerged candidates and
25 documented no-find outcomes. Cumulatively the public layer carries 31 corroborated
findings, 30 candidates and 89 no-finds.

The pass used six parallel research streams and 47 newly registered sources across
contemporary statutes, a Supreme Court report, an 1843 directory, institutional
biographies and finding aids, edited papers, county and church histories and local
archives. Exact queries, source limits and conflicts are retained. Surname form was a
search lead only; it produced no heritage, lineage, immigration, kinship or occupation
claim.

The most important correction is methodological: **a waiting letter demonstrates
postal reachability, not bodily presence in Chicago**. Strong matches place Ezra
Galusha at Warrenville, George R. Makepeace near Joliet, Paul Burdick at Milwaukee,
Thomas R. Covell at Salt Creek and Chester House at House's Grove. Each remains a
candidate rather than being rewritten as a town resident.

The likely Eliza Chappel duplicate remains merge-pending-scan, as do Aaron
Parcel/Aron Parcell and Alonzo Murray/Murry spelling pairs. Ebenezer Ford gains a
strong Fort Dearborn/church candidate and an identified missing May return, but no
household was silently edited. `docs/RESEARCH/resident_identity_pass_02_75.md` records
the full assessment and continuation priorities.

## Shipped 2026-08-30 â€” T-0384: an ordinal off a corner places a store, and claims no lot

**John Holbrook's clothing store stands on South Water Street, one door east of Dearborn**,
between the Chicago American's office at the corner and Frederick Thomas's shop. Two papers
print the address â€” Democrat 1835-06-10 c010 (*"on South-Water st. one door from Dearborn
street"*) and American 1835-06-13 c012 â€” and the reading that let him be placed is the
owner's ruling of 2026-08-30: **a count of doors off a named corner is an ordinal off the
corner, not a reach of the street**. `docs/CORNER-ORDINAL.md` is the policy.

### What was in the way, and it was not the question the ticket named

T-0384 was written believing the blocker was *"may a business-front lot carry two documented
storefronts standing at the street?"* â€” PR #514's question, parked on `hold`. It was not. Under
the register as committed the advertisement read as `street_only`, so `docs/STREET-FACE-ADOPTION.md`
owed Holbrook a standing South Water roof and **there is not one free**: nineteen front the
street, five are a named household's dwelling, five are yard buildings, nine are already
adopted. He was one of seven South Water advertisements short purely on supply.

### The limit, and it is enforced in fields rather than in prose

An ordinal is **not a lot**. The record carries `lot_claim` â€” `claims_lot: false`, `lot: null`,
`placement_rule: corner_ordinal` â€” the schema permits no other value for either of the first
two, and `tools/plat_occupancy.no_lot_claim_ids` reads it: such a record is not a HOLDER of the
lot for the owner's business-front clause of 2026-08-27, so it neither entitles the lot it
stands on nor exhausts it. That is exactly what PR #514 lacked â€” standing Holbrook beside the
American's office switched the clause off, `len(holders) != 1`, and `generate_block_infill.py`
was refused a roof it had been dealt. Nothing physical is relaxed: separation, lot margins and
corridor intrusion all still bind, and `occupied_lots` still counts the roof against its
block's headroom.

The transparency runs **one way on purpose**. A lot held only by no-lot-claim records reads as
taken and the run is not dealt it â€” the conservative answer, costing nothing today because no
such lot exists. Freeing it would be a second ruling, about ground rather than evidence.

### The vocabulary is derived, which is why it does not have to be re-decided

A reading pass writes what it always wrote â€” `class: relative`, an anchor naming the cross
street, an `offset_normalized` carrying the phrase â€” and `compile_register.ordinal_off_a_corner`
reads the ordinal out of it. Three tests, each refusing a phrase the corpus actually prints:
the offset must count doors in a word translatable to a number (*"a few doors below"* is
refused), the reference must resolve to exactly one platted street, and the business's own
street must be a different one. An ordinal off a BUILDING is untouched â€” it resolves earlier,
as a landmark hop.

### The sweep, and what it found that is not this ticket's

`tools/measure_corner_ordinals.py` reports it on every run: over 86 extraction files, **28**
claims count doors, 5 name a corner of two streets and resolve as one, 20 are landmark hops or
name no platted street, and **3 are readable as an ordinal off a corner**. Those three are
Holbrook's Democrat printing and Clark, Filer & Co.'s warehouse *"five [doors east] of the
corner [of Randolph st.]"*, printed twice. Holbrook's other printing is NOT readable: the
American's transcription cuts the cross street to *"De[arborn]"* and a bracketed supply is not
a street name â€” so the Democrat's printing is what carries the placement, and it also
corroborates the street word the American's column lost.

**Clark, Filer & Co. is a finding and it is not fixed here.** Three of its printings carry the
anchor and the gazetteer's LIVE placement for the house is `class: none` with a null street, so
`resolve_anchor` is handed nothing and the row reads `unplaceable`. That is a gazetteer fault,
not this policy's; **T-0440** carries it, including the count of other houses in the same
position, which nobody has taken.

### What is unverified, stated plainly

- **Which side of Dearborn is a reading, not a source.** East is taken because the three
  addresses this block face's own papers print describe a continuous row when read eastward and
  nothing that closes when read westward. The position is graded `inferred` for that reason.
- **The metres are a convention.** L215's door-gap rule â€” a neighbouring front stands 3.048 m
  (10 ft) clear of the wall it neighbours â€” has two reasons and no source. A second ordinal
  placement anywhere in the corpus turns it from a convention used once into a rule that has to
  be argued.
- **Every dimension of the building is borrowed** from `chicago_american_office` and
  `frederick_thomas_shop` on the same face. Nothing about the premises is attested.
- **PR #514 is superseded, not merged.** It built the same store against a reading the owner has
  since ratified, but it claimed the lot and went red on the platted-parcels step; its branch is
  closed rather than left parked.

## Shipped 2026-08-31 â€” T-0442: 75 real named residents receive identity reviews

**Seventy-five of 848 eligible attested or inferred named people (8.8%) now have a
dated, reproducible identity-research outcome.** The fixed sample spans five established
profiles, every one of the twenty richer unplaced newspaper records, and fifty of the
post-office-only names split evenly between present and uncertain. No reconstructed
person is eligible.

The result is deliberately less flattering than 75 new biographies: **4 corroborated
findings, 7 candidate identities and 64 searches with no safe match**. Candidates are
published on the resident card with their supporting source, conflict and an explicit
â€œnot mergedâ€ warning. A no-find says what it is too: the reviewed search did not find a
safe bridge, not that the person did not exist.

The useful near-matches include Augustus Garrett, James Curtiss, Buckner Stith Morris
and David Brookins. Jesse W. Fell is explicitly rejected as the automatic expansion of
J. W. Fell because institutional chronologies put Jesse in Vandalia and Clinton in
1835. J. H. Collins is the strongest resolution: profession and his distinctive Caton
partnership connect the abbreviation to James H. Collins by more than the name.

No household, marriage, kinship, immigration or heritage field was invented. The
source hierarchy explicitly forbids surname-based heritage claims. The cohort,
outcomes, source resolutions and public payload re-derive in the gate; browser checks
hold both candidate and negative-result warnings on mobile and desktop.

## Shipped 2026-08-30 â€” T-0170: the last part of the gate that could not be run is halved

**Nothing a visitor sees.** `SMOKE_STAGE` has THIRTEEN parts; part 10 is halved and old parts
11-12 are 12-13. This is the last piece of T-0121 and the third re-cut of the day, after T-0346
and T-0173.

**The part was never inside the ceiling.** Profiled at 1280x800 with `SMOKE_TIMING=1` on an
**idle** runner â€” load average 0.27-1.48, zero other Chromium processes, the friendliest reading
this suite can be given â€” it was **killed at 9 m 20 s** with the street readouts and the Settings
units still to run. Third and fourth kill of the same part. T-0167's 7 m 43 s is the outlier in
the record, not the number to size a cut from.

**It had been skipped twice for want of a boundary.** This part carried no `// --- section ---`
headers at all; that is the stated reason T-0167 cut part 8 instead. Eight seams are named now,
so the next cut here is a choice from a list rather than a fresh profile.

**The first cut was measured and rejected, and it is in the record.** Cutting above R-BUG7's
flower-head census gave **5 m 05 s / 6 m 24 s** â€” a 3 m 36 s margin, and this project's own rule
(ROADMAP Â§ THE RUN BUDGET) is that a margin that thin is not a margin. Moving that one section up
into the head balances it.

| part | desktop | margin | staged | verdict |
|---|---|---|---|---|
| 10 | **5 m 59 s** | 4 m 01 s | 23 | 1 failed â€” T-0279's flower heads, 2,693 of 18,893 |
| 11 | **4 m 41 s** | 5 m 19 s | 13 | SMOKE PASS |

23 + 13 = **36**, the count the single part took. The red is inherited:
`tools/dev-smoke-state.json` records the same check red on dev at 2,526 of 18,911 on 2026-08-29,
and it does not fire at mobile at all.

**Nothing dropped, measured as an equality.** At mobile on the same tree, the pre-cut
`smoke_renderer.mjs` at the single part gives **45 passed / 0 failed / 36 staged / 9 always-on in
5 m 59 s**; the pair gives **45 / 0 / 36 / 9 in 6 m 01 s**. A pair still boots once, so the mobile
recipe does not grow a command.

**One binding crosses and it is the one that already crossed the stage split.** `streetLayer`, so
`anyStage(7, 10)` becomes `anyStage(7, 10, 11)`. The other six names the scan found below the
line (`headSupport`, `horizon`, `over`, `planted`, `popIn`, `sward`) are prose or strings in every
occurrence. The second half's prologue is `enterTown()` and `setFly(false)`.

**The readings are of THIS tree.** The cut was first measured at parts 9 and 10, before T-0173
merged and shifted the whole tail by one; every figure above was re-taken after the re-derivation
onto T-0173's numbering and agrees with the first pass to within six seconds (5 m 58 s / 4 m 38 s
then, 5 m 59 s / 4 m 41 s now). All three are filed in `tools/dev-smoke-state.json`.

**Read the margins as readings of an idle machine.** T-0215's factor of twenty is not repealed by
a cut: 4 m 01 s is a margin against the box that measured it.

## Shipped 2026-08-30 â€” T-0333: eighteen inches of stack, and the town was already inside it

**The Town of Chicago's by-law of 5 August 1835, section 18, is the first documented
DIMENSIONAL constraint this project holds on anything above a roof line**, and it is now
measured and gated. `chicago_democrat_1835_08_19#c005`, page 1 column 2, prints it line by
line: *"every stove pipe or chimney passing through the roof of any building shall extend
and be carried at least eighteen inches above the roof, and no stove pipe shall be passed
through the side or end of any building"*, under five dollars for each and every offence,
with a fire warden in every house, store and shop once a month from September to May.

### The census, and it is the whole finding

`tools/measure_stack_ordinance.py`, read off the committed masters' glTF accessor bounds
rather than off the generators that wrote them â€” the same discipline `measure_stack_fabric.py`
(T-0137) uses, and for the same reason: the generator is the thing under test.

| archetype | buildings | above its own roof |
|---|---|---|
| `frame_dwelling` | 116 | 0.780 m â€” 30.7 in |
| `log_dwelling` | 44 | 0.720 m â€” 28.3 in |
| `frame_storefront` | 36 | 0.710 m â€” 28.0 in |
| `frame_tavern` | 11 | 0.550 m â€” **21.7 in**, the tightest in the town |
| `fort_structure` | 6 | 0.780 m â€” 30.7 in |
| **town** | **213 buildings, 234 stacks** | **least 0.550 m, 3.7 in of margin** |

**Nothing was raised, moved or rebuilt, and no master was rebaked.** The ticket anticipated
this outcome in its own words â€” *"the answer may already be compliant, in which case this
ticket closes as a GATE and a provenance note rather than as geometry"* â€” and it is what the
measurement says. `docs/LIBERTIES.md` is untouched: a documented constraint the model already
satisfies is not an invention.

### What is unverified, and what is deliberately not decided

- **The clearance is measured to the RIDGE**, which is the top of the `roof` material. A
  stack standing off the ridge â€” `frame_tavern` across the frontage, `frame_storefront` on
  a shed roof â€” breaks a roof plane lower than that, so its true projection is larger than
  the figure above. The figures are a floor, not an estimate.
- **A building carrying stacks on two roofs reports its tallest.** That the ell's or the
  frame addition's stack clears its own ridge by the same margin is the ARCHETYPE's
  guarantee â€” every archetype builds each stack with one helper, relative to the ridge it
  is handed â€” and not this measurement's. Stated rather than assumed.
- **The corporation limits are not drawn and this gate makes no ruling about them.**
  Section 18 binds *"within the limits of the Corporation"*; section 22 of the same sitting
  walks those limits street by street and is **T-0334**, unbuilt. Nothing is conformed to a
  rule that may not bind it, because nothing has to move: every stack clears eighteen inches
  on both sides of a line nobody has drawn. If a record ever legitimately stands a shorter
  stack outside the limits, T-0334's boundary is what scopes this gate, and the gate's own
  failure message says so instead of inviting the next run to weaken a documented figure.
- **The by-law postdates the scene date by five weeks and is not applied retrospectively.**
  It is used as a bound the drawn town is measured against, not as a rule the 1 July town
  was held to.
- **There is no stove pipe anywhere in this model.** Every stack drawn is masonry, so
  section 18's second clause â€” no pipe out through a side or end wall â€” binds nothing that
  is drawn. That answers the ticket's second question: the archetypes do not distinguish a
  pipe from a chimney because they have only chimneys.

`docs/RESEARCH/chimneys.md` Â§ 7 holds the reading. `tools/check.sh` runs the gate and its
four self-test cases.
## Shipped 2026-08-30 â€” T-0173: the desktop gate's part 7 is halved, and both halves fit

**Not a thing a visitor sees.** It is the thing that lets a run PROVE what a visitor sees. A
steward run's single foreground command is capped at ten minutes, and part 7 stopped fitting
inside it: profiled on the steward runner with `SMOKE_TIMING=1` at load 0.81-2.86, it was killed
at **9 m 25 s** with its last two assertions unrun and `the suite body ran to completion` reporting
a FAIL that looks like a product red and is not one. That is the third desktop part to go this
way (T-0121's four, T-0167's part 8, T-0346's part 4 the same morning), and the cause is the same
one every time: the town grows and the part grows with it.

- **The cut is measured, and the measurement says where.** The profile puts **7 m 04 s of a
  9 m 25 s part in ONE block** â€” the three road-legibility stations, each of which teleports to
  its own viewpoint and reads `page.screenshot` frames through five distance bands. Around it:
  20 s of boot, 33 s of navigation and the street-layer checks, 1 m 04 s of the R-A1 aid, and the
  batch merge under that.
- **So the boundary could not be one of the file's own `// --- ` section headers**, which is what
  T-0170 had already found and left for whoever cut it: the best of them leaves **7 m 37 s against
  1 m 30 s**, which is not a cut, it is a rename. The cut falls at the STATION instead â€” the grain
  the block is actually made of. Each station teleports to its own viewpoint, takes its own frames
  and answers its own `check`, and none of them reads anything a sibling left standing.
- **Nothing crosses it.** `roadRuns` is local to the block. The movement report built from it is
  printed and never gated, and it has always compared only what the invocation measured â€” that is
  what lets `SMOKE_VIEWPORT=mobile` run without retiring desktop's half of the bank â€” so a part
  reporting on its own stations is the existing rule, not a new one. `--update-road-bands` merges
  per band and leaves untouched bands alone. R-A1's three assertions are taken STANDING AT
  `lake_market`, so that station goes into the new part with them, in the same order, unchanged.
- **Measured after the cut, at desktop, same runner and same hour:** part 7 â€” **5 m 05 s, 12
  staged, SMOKE PASS**; part 8 â€” **5 m 06 s, 8 staged, SMOKE PASS**. 12 + 8 = **20**, exactly the
  count the old part 7 was taking, which is how "never dropping a check" is demonstrated rather
  than asserted. Both halves clear the ceiling by **4 m 55 s**, against the 35 s the old part 7 was
  over it by.
- **Which of the two carries the shared street reading matters, and it is part 7.** `anyStage(7, 9)`
  becomes `anyStage(7, 10)`; `streetLayer` â€” the most expensive single evaluate in the file â€” is
  referenced in parts 7 and 10 and nowhere else, checked statically and then run. Part 8's own
  profile is the proof it does not pay for it: boot at 0 m 17 s, first station at 3 m 17 s, no gap
  where that reading would sit.
- **Parts 8-11 are renumbered 9-12**, because this cut is mid-body and T-0167's append could not be
  repeated (T-0346 hit the same wall the same day). The pairing rule survives in content and moves
  in spelling: `1+2, 3+4+5+6, 7+8, 9+10+11` becomes `1+2, 3+4+5+6, 7+8+9, 10+11+12`, ranges
  `1-2 3-6 7-9 10-12`. `chicago-4d-bake.yml`'s smoke matrix is edited in this commit, as its own
  comment demands of any renumbering; the ranges still tile 1..12 once each with no gap or overlap.
- **The renumbered legs were run, not reasoned about.** Mobile `SMOKE_STAGE=7-9` is **43 passed,
  0 failed, 34 staged** in 7 m 33 s â€” the same 43 the old `7-8` leg reported on 2026-08-30, so the
  leg carries exactly what it carried. Mobile `SMOKE_STAGE=10-12` is **168 passed, 0 failed, 159
  staged** in 9 m 33 s, which fires all three renumbered tail parts.
- **`tools/dev-smoke-state.mjs` mirrors `PARTS` and had to move with it** (11 â†’ 12), and
  `CHANGELOG_PARTS` with it (What's-new is part 11 now, not 10).

**What this does NOT close.** T-0173's acceptance names three parts and this is one of them: the
old part 4 was T-0346's, and the old part 7 â€” **now part 10** â€” is T-0170's, which is still open
and still measured over the ceiling on three separate runners. T-0173's own instruction was "do
not cut part 7 twice", and cutting a part that another ticket owns while eight slices of this lane
run at once is exactly the way to do it twice. So T-0173 closes on what it uniquely owned and
T-0170 keeps its own part, with the numbers in it re-labelled for this cut.

**Re-taken after a rebase, because dev had gained a geometry change under it.** T-0333 put a stove
pipe on every roof in the town while this branch was being measured, so the desktop pair was run
again on the rebased tree: part 7 **5 m 03 s / 12 staged** and part 8 **5 m 06 s / 8 staged**,
both SMOKE PASS, within three seconds of the first pair. `./tools/check.sh` PASS on the same tree,
and `node tools/smoke_budget.mjs --self-test` â€” T-0235's map, merged into dev the same hour â€” is
green on the new numbering.

**A caveat on every figure above, and the ROADMAP already states the rule.** These readings were
taken at load average 0.81-2.86 on a 4-core runner. T-0215 measured a factor of twenty between a
quiet box and a loaded one, so 4 m 55 s of margin is a floor on what these parts cost, not a
description of it.

## Shipped 2026-08-30 â€” T-0305: the four readings the American contradicts itself on

**What a visitor sees:** S. B. Cobb's saddlery â€” the corner shop on Lake Street in the West
Division â€” now carries an **open question** on the provenance card you get by walking up to it,
and the Evidence panel's open-questions list goes from four to five. It is the second building in
the scene whose card asks a live question rather than only grading a claim.

**The ticket was filed with a title that asserted its own answer** â€” *"need the page images"* â€”
and an empty acceptance clause. The acceptance was written first, and written so that it could
refute the title: name the four, test each against the whole 86-issue corpus rather than against
the American alone, and only then put what survives to the owner. Nothing survived the corpus
test. The title was right, and it is right for a stated reason now instead of by assertion.

**The four, and the shape of each.** `tools/measure_american_contradictions.py --gate` re-derives
them; `docs/RESEARCH/american_self_contradictions.md` quotes every printing.

| # | question | printings | the corpus |
|---|---|---|---|
| 1 | Edward Burton's tailoring shop â€” Franklin or Lake street | one card, one copy date, four settings: Franklin, Franklin, unresolved, **Lake** | `Burton` is not in the Democrat at all |
| 2 | Wm. Sabine â€” North or South Water Street | North 06-13 and 06-20, **South** 07-04 | one post-office letter-list line |
| 3 | John Dave[s] â€” the card set below Sabine's | the same two dates, the same two readings | three letter-list lines |
| 4 | S. B. Cobb's saddlery â€” which cross street | Lake legible in all three 1835 cards, the cross street lost in all three | the Democrat's 1833 *"Lake and Canal streets"* |

**Three things the run found that the ticket did not know.**

- **2 and 3 are one event, not two.** Both houses read North in both June settings and South in
  the July one. Two firms do not cross a river together between issues; a compositor resets a
  column. That does not say which reading is right â€” it does mean **one page image settles both**,
  and it is why the ask is six columns for four questions rather than eight.
- **The contradicting printing is invisible to the register.** On 1835-07-04 the three forwarding
  cards were extracted as ONE claim, filed under the third firm's name (Newberry & Dole), so
  `business_wm_sabine_storage_forwarding_and_commission_merchant` reads "North Water Street" flat
  with no disagreement recorded on it. The South reading survives only on John Davis's entity and
  in that claim's own note. **Not re-cut here**, deliberately: re-cutting a claim is a reading of
  the page, and the page is the thing that is missing.
- **Question 4 is the weakest of the four, and that is worth knowing before anyone spends a
  scan on it.** The 1833 corner is one of the few addresses in this project read off the page
  images themselves â€” `chicago_democrat_1833_11_26` carries `verified: true` â€” so the American's
  silence is not doubt about 1833. What it leaves open is the twenty months after it: whether the
  shop Cobb *"will continue the above business at"* in June 1835 is the same corner, which is
  exactly the identification the record grades `inferred`.

**A sentence that was counting, and had already gone wrong.** The Evidence panel's own account of
the open questions ended *"one of them is standing in front of you"*. That was true of four
entries and stopped being true on 2026-08-29, when the New York House became the second standing
one â€” a day before this run added a fifth. It is the same failure the hand-typed paraphrase before
it made, and the same failure the panel's own changelog entry says it fixed. It counts nothing now:
each entry carries its own `standing` flag and the chip beside it says which.

**What is left is the owner's, and it is six columns**, all in the American â€” 1835-06-13 p3 c5,
1835-07-04 p4 c4, 1835-06-27 p3 c5, 1835-08-15 p3 c6, 1835-06-08 p3 c5, 1835-07-11 p3 c6. Two of
them serve two questions each. Nothing smaller will do it: every reading above is already the best
the transcription can give, and three of the four subjects appear nowhere else in eighty-six
issues except a list of letters waiting at the post office. The ticket is `blocked-owner` on
exactly that ask.

**Held by a gate, not by memory.** Every reading is declared with the page and column it sits in
and re-derived on every `check.sh`, along with the negative half over all seventy-three Democrat
issues. Eight assertions, each proved to fire under `--self-test`. The day one of these four is
answered â€” by an image, or by an extraction pass reaching a card nobody has read â€” the build says
so.

## Shipped 2026-08-30 â€” T-0346: the desktop gate's costliest part is cut into three

**Nothing you can see changed.** This is exemption 3 of the visible-progress rule: a gate that is
blocking visible parcels. `tools/smoke_renderer.mjs` part 4 was being killed at the ten-minute
foreground ceiling a steward run's single command has, so no run could take the desktop half of its
own gate â€” and part 4 is where the draw-call and triangle ceilings are gated at the town's worst
frame, which is exactly the check a NEW BUILDING breaks. T-0385 (the New York Clothing Store in
Dearborn Street) and T-0375 (five documented tradesmen on South Water Street) both stand roofs and
both have to clear that ceiling; until today neither could demonstrate it on the runner that ships
them.

**The cost was one section of ten, and it was measured rather than guessed.** `SMOKE_TIMING=1`
under this lane's own eight-way contention, 2026-08-30, against `--published`:

| section of part 4 | reached at | left at |
|---|---|---|
| raycast pick â†’ walking â†’ bridge deck â†’ budgets â†’ life size â†’ nothing hovers | 0:18 | 1:10 |
| **the scene-detail ladder** | 1:10 | **7:27** |
| the gate and the chrome | 7:27 | 8:42 |
| the confidence menu's own clicks | 8:42 | killed at 9:20 |

Six minutes and seventeen seconds of a ten-minute part sat in ONE section. That section walks every
stand in `STANDS` at every detail tier and cannot be halved without walking the set twice â€” the
single-walk saving is what T-0135 built it around â€” so it is a part on its own rather than a
boundary nudged along.

**The cut, and what crossed it.** Two named section boundaries, both re-verified for crossing
bindings the way T-0121 and T-0167 verified theirs. Exactly one binding crossed: part 4's `stats`,
read only for `stats.budget.drawCalls`. Part 5 now reads that ceiling itself, out of `stats.budget`
rather than written into the test, so the bar still follows its definition site in `main.js` and a
scene that outgrew its budget still cannot be made green by editing this file. The ladder takes no
pose from what ran before it â€” `order` teleports to each stand itself and finishes at the reference
frame â€” so no `enterTown()` or re-framing was needed at the boundary.

- **Parts 4, 5 and 6, measured under the same load:** 1 m 09 s (17 staged checks), 6 m 46 s (16),
  3 m 13 s (6). All three SMOKE PASS at desktop against `--published`.
- **Nothing was dropped, and it is checked rather than claimed.** At mobile, where the old part 4
  still fitted the ceiling, `origin/dev`'s part 4 and this branch's parts 4-6 report the SAME
  numbers on the same tree: **51 passed, 0 failed, 42 staged-section checks, 9 always-on** â€” 6 m 17 s
  against 6 m 15 s. That is the arithmetic the audit line exists for, run as an equality.
- **Parts 5-9 are renumbered 7-11**, because these two sections sit in the MIDDLE of the body and
  T-0167's append could not be repeated. `anyStage(5, 7)` â€” the shared street reading â€” becomes
  `anyStage(7, 9)`; `streetLayer` is referenced in parts 7 and 9 and nowhere else, checked
  statically and then run: `SMOKE_VIEWPORT=mobile SMOKE_STAGE=7-8` is **43 passed, 0 failed** in
  7 m 31 s.
- **The pairing rule survives in content and moves in spelling.** `1+2, 3+4, 5+6, 7+8+9` becomes
  `1+2, 3+4+5+6, 7+8, 9+10+11` â€” the same four mobile commands carrying the same parts, ranges
  `1-2 3-6 7-8 9-11`. `chicago-4d-bake.yml`'s smoke matrix is edited in this commit, as its own
  comment demands of any renumbering; the ranges still tile 1..11 once each with no gap or overlap.
- **`tools/dev-smoke-state.mjs` mirrors `PARTS` and had to move with it** (9 â†’ 11), and
  `CHANGELOG_PARTS` with it (What's-new is part 10 now, not 8).

**One thing this leaves behind, stated rather than hidden.** Every reading already in
`tools/dev-smoke-state.json` is filed under the OLD numbering, so a reading labelled `stage: "5"`
is the part that is now 7. Nothing reads them as a bar and every one of them carries a `treeHash`
that no longer matches any tree with this file in it, so `ask` will say it was not taken on your
tree â€” but the numbering is now dated and the record's note says so.

**What this does NOT do.** It does not re-profile the whole desktop recipe under load, and it does
not resize the parts T-0346's second measurement put over the ceiling for reasons that were later
shown to be contention rather than cost (old stages 5 and 7, now 7 and 9). That is a second
demonstration and therefore a second ticket: T-0346 was split rather than shipped as a self-invented
half.
## Shipped 2026-08-30 â€” T-0369: desktop stage 8's verdict stops depending on which stages ran in front of it

**Nothing you can see changed.** This is a gate repair, taken under AGENTS.md's third
visible-progress exemption: the stage split exists so a branch can verify a subset, and a subset
that is red only because of its own composition costs every visible parcel an argument about whose
failure it is. T-0316's run re-ran `dev` twice to establish that its own change was innocent.

**The measurement, reproduced on this runner on an unmodified `dev` (published mirror):**

| command | verdict |
|---|---|
| `SMOKE_VIEWPORT=desktop SMOKE_STAGE=8` | 37 passed, 0 failed |
| `SMOKE_VIEWPORT=desktop SMOKE_STAGE=1,8` | 75 passed, **1 failed** â€” `clickChrome: .panel-tab[data-tab="settings"] is covered at its own centre by <h2>` |

- **The `<h2>` is the inspect card's, and the card is part 1's.** `clickChrome` named the tag and
  not the thing it belongs to, so the first act of this ticket was to make it walk up to the
  nearest ancestor carrying an id. The failure then reads `covered at its own centre by <h2>
  inside #popup`, which is the whole diagnosis in one line. Part 1's last page interaction is
  `boardPick` â€” twenty-five `pick()` calls proving that aiming at the Tremont House's signboard
  opens the business behind it â€” and a `pick()` that lands on a structure OPENS the card. Part 1
  never closed it. `#popup` is `position: fixed; z-index: 30; top: 58px; right: 12px`, 392 px
  wide; the HUD panel is 380 px wide at the same corner, so on 1280Ã—800 the card sits squarely on
  the panel's tab strip. Part 8's first statement clicks a tab.
- **Why it survived the split's whole existence.** Nothing between part 1 and part 7 reads panel
  chrome â€” parts 2â€“7 read the scene graph or take their own captures, and part 4 happens to close
  the card mid-part for its own reasons. Part 8 is *nothing but* panel chrome, and it is the only
  part that inherits the leak with something to lose.
- **Repaired at both ends, and only the second end makes the verdict order-independent.** Part 1
  closes the card it opened and now ASSERTS the teardown â€” `part 1 hands the page on with nothing
  standing over the chrome`, over `#popup` and `#control-help` â€” so the next part that walks away
  leaving an overlay up is named at the boundary where it happened rather than four parts later
  under another gate's name. Part 8 also clears the card in the same preamble that already
  re-opens the panel, so it no longer depends on *every* predecessor being well-behaved. Nothing
  was weakened: the added check is new, and no existing assertion moved.
- **It is NOT the same fault as T-0349, and that hypothesis is now refuted rather than open.**
  T-0369 was filed as the second instance of T-0349's shape and suggested both be answered by one
  repair. They cannot be. T-0349's own third reading names its cause exactly â€” the signboard
  gate's seventh clause counts `frontage.meshes === 62` and a run with stage 1 behind it carries
  five extra `frontage-far-merge` meshes the desktop camera's history caused. That is a census
  clause reading a distance-merge artefact; this is an overlay left standing over a control. Two
  different faults that share only the phrase "red after stage 1". T-0349 is untouched here.

**Verification.** `./tools/check.sh` PASS. `tools/smoke_renderer.mjs --published`: desktop
`SMOKE_STAGE=1,8` **105 passed / 0 failed** (was 75/1), desktop `SMOKE_STAGE=8` alone **37 passed
/ 0 failed** â€” the same verdict both ways, which is the acceptance. Mobile `SMOKE_STAGE=1,8`
**105 passed / 0 failed**. Both viewports carry the new part-1 check.

## Shipped 2026-08-29 â€” T-0358: the plat gets its block numbers, and the corpus's only address resolves

**Nothing you can see changed.** This is a dependency: the corpus's one lot-and-block address â€”
G. Spring's *"LOT No. 7, in block No. 16, one lot east of Haddock's Tavern, on Lake street"*,
printed six times in the *Chicago Democrat* â€” resolved to nothing, because
`data/traces/vectors/thompson_lots.json` keys its nineteen blocks on their bounding streets and no
committed source numbered one. Three separate readings had recorded that this was the most
placeable statement the corpus makes and that placing it was somebody else's job.

**The evidence turned out to be two numerals, not three.** `clark_reach_bulge_1834.md` Â§ 8 and
`thompson_plat_grid.md` Â§ 4 both said the owner's crop of Wright's 1834 sheet reads *"block numbers
19, 18 and 17"*. Re-read at full resolution â€” the file is 639 Ã— 719 px â€” it carries **19 and 18**,
and the map region ends at block 18's east edge; the asset's own README, written when it was
supplied, describes two. The third arrived in the retelling. Both memos are corrected, and nothing
built on them moves: two consecutive numerals fix the step and the direction as well as three would.
What changes is that a later reader can now see how far the base can be pushed, which matters
because this ticket pushes it three blocks.

- **Six blocks are numbered and everything else is refused in writing.** 19 west of 18 fixes the
  step at one, falling eastward, and fixes it *along the tier* â€” two blocks side by side differing
  by one cannot be column-major. The watercourse drawn in the street between them is the one
  already traced at local E +462â€¦+469, the east half of the La Salle corridor (centreline E +451.3;
  Wells 122 m west, Clark 123 m east), so they are Wellsâ€“La Salle and La Salleâ€“Clark. Counting:
  **21 Marketâ€“Franklin, 20 Franklinâ€“Wells, 19, 18, 17 Clarkâ€“Dearborn, 16 Dearbornâ€“State.** The other
  two tiers, the West Division, the North Division and where the run begins and ends are all refused,
  each with its reason: two numerals in one row say nothing about how the run passes to the next.
- **Block 16 is the one counted number an independent source agrees with.** Dearbornâ€“State is
  bounded south by Lake Street, and the lot scheme the same crop shows runs 5 6 7 8 west to east
  along a south row â€” so lot 7 is the third lot east of Dearborn and Haddock's Tavern, one lot west,
  is the second. That is where T-0324 had already argued the Mansion House stood, from Andreas's
  "on Lake near Dearborn" and Botsford's corner advertisements, before any of this existed. Three
  statements, three sources, one block face. **The count stays `inferred`** â€” agreement is not a
  survey â€” and 17, 20 and 21 have no such check and say so on each record.
- **Nothing was promoted and no confidence moved.** `data/traces/thompson_block_numbering.json` is
  authored and carries the reading, the identification and the refusals;
  `tools/generate_plat_lots.py` only stamps it, and re-derives the grid byte for byte as before.
  Every `plat_lot_number` is `conjectural` *including block 18's own*: a number put on a line the
  module drew is conjectural whatever the number's provenance. No modern plat reprint was consulted
  and the record says so in terms.
- **Two consequences are now measurable and neither is acted on here.** The Mansion House stands on
  lot 5, the corner lot, and the corpus puts it on lot 6 â€” a gap of **24.2 m, one lot east**, which
  is inside the along-street allowance that record already declares, so the coordinate is unchanged
  and the note now carries the number instead of the sentence. And lot 7, which carried "a large
  Dwelling-House and fine well", holds an anonymous reconstructed count-unit roof. Standing Spring's
  documented house there is the visible follow-up, filed as **T-0423**.
- **No mesh went stale and this cost no bake.** `generators/mesh_inputs.py` hashes archetype, phase
  and resolved params; a block number moves no vertex.

## Blocked 2026-08-29 â€” T-0384: Holbrook's blocker was answered by a ruling nobody carried back to the ticket

**Nothing was built and that is the finding.** T-0384 sat at row 2 of the queue, `state: open`
and `blocked_on: null`, over a body that said in prose it was blocked behind an owner ruling â€”
*may a platted business-front lot carry TWO documented storefronts standing at the street?* â€” the
question PR #514 asked and is still parked on `hold` carrying. Every run that took row 2 had to
re-derive the same conclusion before it could put the ticket down. **The question in the ticket is
now the wrong one, and answering it would not have placed the store.**

- **The register re-read the advertisement.** `business_john_holbrook` today reads `action:
  street_only`, `anchor.kind: street`, over *"[on South] Water st., one door from Dearborn
  street"*, noting *"the anchor is a reach of dearborn and names nothing narrower"*. PR #514 read
  the same printed line as an ordinal off the corner and raised a 30 Ã— 25 ft shop 3.048 m east of
  the American's office. One line, two readings, and the register's is the committed one.
- **The owner ruled the same day what a `street_only` business gets** (T-0354, L212): it adopts a
  standing roof, nothing is built for it, and every adoption declares `lot: null` and
  `claims_lot: false`. Under that ruling Holbrook never seats on a platted lot, so the lot clause
  is **moot for him**. `street_face_adoptions.json` refuses him for supply instead â€” one of seven
  South Water advertisements against nineteen fronting roofs of which five are homes, five are yard
  buildings and nine are already taken.
- **The old clause was measured rather than assumed stale.** Through `tools/plat_occupancy.py`, no
  figure authored: 19 business-front lots dealt town-wide, 5 carry a documented building, the
  2026-08-27 clause is live on 2 and already off on 3 â€” and **0 register businesses anchor on any of
  those five**. The red PR #514 reported still reproduces (a second documented holder makes
  `len(holders) != 1` in `shared_business_fronts`, the run loses its lot, the platted-parcels step
  goes red), but widening the clause today would unblock nothing at all, Holbrook included.
- **The cheaper exit needs no ruling.** `adopt_street_faces.py` re-derives on every commit, so the
  first South Water roof **T-0375** frees seats Holbrook automatically. The ticket now carries that,
  and the one-line question it is actually waiting on, in `blocked_on` where `ticket.mjs board`
  shows it to the owner.

## Shipped 2026-08-29 â€” T-0417: the street-face adoptions reach the buildings, and nine come out of the yard

**The allocation is now SPENT.** T-0354 paired 24 documented businesses with reconstructed roofs
on the streets their advertisements name, and stopped there: the pairing lived in
`data/research/newspapers/street_face_adoptions.json`, the buildings still opened as anonymous
count-units, and the policy's own file said so â€” *"Nothing here writes a card"*. Nineteen roofs on
South Water Street, Lake Street and Randolph Street now carry an `occupants` block naming the
business, its trade, the street the paper puts it on and every claim the reading rests on. It is
derived, not authored: `tools/inferred_occupancy.py` â€” the ledger the inferred-household programme
already used for exactly this â€” hands the block to whichever generator owns the roof, so
`generate_block_infill.py --check` re-derives all nineteen byte for byte.

**Twenty-four became nineteen, and that is the finding.** Nine of T-0354's adoptions had been
seated in ANCILLARY roofs â€” the privies, stables and woodsheds the anonymous parcels deal behind a
lot. **Peter Cohen, clothier, grocer and liquor dealer and the best-attested shopkeeper in the
whole corpus at eight printings, was in `recon_1835_blk_south_water_clark_a3_05`, a privy.** The
rule against it was not new and was not weakly held: `tools/generate_block_infill.py` has refused
to hang an occupant on an ancillary roof since the inferred-household programme, on the ground that
*"a yard building serves the lot it stands behind, and an adoption is a claim about who lived or
worked in a building"*. The allocation simply could not see which roofs were sheds, and nothing
noticed for a day because nothing consumed the table. **An allocation nothing spends is an
allocation nothing checks** â€” that is the transferable lesson here.

- `tools/adopt_street_faces.py` gained refusal 6, *the roof is a yard building*, and its supply
  count now reports fronting roofs less homes less yards. Four of the nine took a principal roof
  instead â€” Harmon, Loomis & Co. moved from a shed into a narrow two-storey store â€” and five had
  none left on their street, so `every roof on the face is spoken for` goes 3 â†’ 8 and the waiting
  pile 36 â†’ 41 against the register this branch was cut from. Re-derived once more on the rebase
  onto T-0400, which merged firm groups and moved `street_only` 60 â†’ 59: **19 adopted, 40 waiting,
  7 of them short purely of supply.** All of it re-derived; none of it authored, which is the point
  of deriving the allocation rather than listing it.
- **Fifteen assertions fire when broken**, up from eight: nine in `adopt_street_faces --self-test`
  (including a business seated in a yard building) and six in `inferred_occupancy --self-test`
  (an adoption that claims a lot, an order that has become a claim, nothing to cite, a roof outside
  the anonymous layer, two businesses on one roof, a claim id naming no corpus source). The ledger
  also raises if the household programme and an adoption claim one roof, which nothing upstream
  prevents.
- **No geometry moved and no mesh went stale.** `generators/mesh_inputs.py` hashes archetype,
  phase and resolved params; an `occupants` block moves no vertex, so this cost no bake.
- **L212 is revised** with the new counts and the yard refusal; `docs/STREET-FACE-ADOPTION.md`
  carries refusal 6 and a re-measured table. The derived table's `_doc` had been citing L207 for
  its own liberty and now cites L212.
- Still not written here: a SIGNBOARD. `tools/generate_business_signboards.py` refuses a `recon_*`
  record by name, so a board on one of these roofs is a change to the signage rule and needs its
  own argument rather than a quiet exception.
- **T-0416** carries the rest of T-0387 â€” Wm. Sabine, John Dave and the Dearborn Street wine store,
  all three refused for want of a roof whose lot fronts North Water or Dearborn. That is an owner
  question (is a corner side a face?) before it is a placement.

## Shipped 2026-08-29 â€” T-0354: what a business does when the paper names a street and nothing narrower

**The register could place 58 of 203 documented businesses; 24 more now stand on the street faces
their advertisements name.** (T-0354's title says 24 of 190 with 49 `street_only`. It was filed that
morning; T-0380, T-0383, T-0355, T-0399 and T-0356 all landed on `dev` before this branch merged and
the `street_only` pile went 47 â†’ 45 â†’ 60 while it was being written. Every figure here is this
branch's own re-derivation against the register as merged, and none of it is authored â€”
`tools/adopt_street_faces.py --report` reprints all of it. **The policy did not move with the
counts**, which is the argument for deriving the allocation instead of listing it.) The owner ruled on 2026-08-29, choosing between the three options the
ticket set out, that a `street_only` business *adopts a reconstructed roof already standing on that
street face*. `docs/STREET-FACE-ADOPTION.md` is that ruling written so a later run applies it
without re-deciding it, `tools/adopt_street_faces.py` derives the allocation,
`data/research/newspapers/street_face_adoptions.json` is the derived table, **L212** is the liberty,
and `tools/check.sh` re-derives all of it on every commit.

**The four limits are assertions, not promises.** No adoption claims a lot (`lot: null`,
`claims_lot: false`, and the gate refuses a record that grows a lot field of any name); the adopted
roof stays `reconstructed`, re-read from the structure's own phase on every commit; which roof on a
face is an allocation by deterministic rule and says so in every record; and order within a face is
not a claim. Each of those four is a way the ruling could be breached silently by a later run, which
is why each is a check rather than a paragraph.

**What it moves, and where the rest wait.** 60 `street_only` in the register: **24 adopted, 36
waiting.** Twenty-four name Dearborn, La Salle, Canal or North Water, where no reconstructed roof's
platted lot faces the street â€” Dearborn has eighteen roofs showing it a corner side and none showing
it a front. Nine are a second heading of a house already seated on that face. Three are short purely
of supply. South Water took 14 of its 19 fronting roofs (5 are households' dwellings); Lake took 9;
Randolph took 1.

**What is unverified or deliberately left, stated plainly.**

- **Only `lot front` is adopted, and that is a decision with a cost.** `tools/fronting_street.py`
  also answers `corner side` and `centreline band`; both are refused here, because an
  advertisement's street is where the door is and a gable end reaching a street is not a doorway.
  **Widening the reading would reach 24 more**, and `--report` prints both readings side by side so
  the number an owner ruling would change is one number, not a rewrite.
- **Three Lake Street roofs are probably one house.** Wm. G. Branchaud, W. G. Blanchard, G.
  Blanshard and F. G. Blanshard advertise one trade within five months under four transcribed
  spellings, and the gazetteer's identity layer has judged none of them. The duplicate refusal here
  matches exact surnames only â€” deciding by resemblance is the identity layer's job â€” so it caught
  one of the four and left three roofs standing. Filed as **T-0408**, with the page images named as
  the remedy.
- **The 84 `unplaceable` are untouched and T-0354's second half stays open.** The ruling does not
  reach them and this policy does not extend it; some are outside the plat entirely.
- **Nothing is spent yet.** This is the policy and the allocation. No card, signboard or frontage
  reads it â€” that is T-0263's and the seeding tickets'. No geometry moved and no triangle was added,
  so no bake was required.
- **The renderer smoke was not run and did not need to be.** This branch touches
  `data/research/`, `docs/`, `tools/` and the changelog only; no scene, structure, terrain or
  renderer file changes, and `data/research/` is not published. `tools/check.sh` â€” the dev gate â€”
  is green in full, including its own new step.

---
## Shipped 2026-08-29 â€” T-0380: the New York House stands on Lake Street near Wells

**A building this project had wrongly ruled out now stands in the town.** The New York House sat
on the EXCLUDE list of the first structures dossier on the grounds that "build date not attested in
Andreas". Andreas I p. 635 attests it plainly â€” *"built in 1834 and opened to the public the
following year by Lathrop Johnson and George Stevens, who conducted it until the fall of 1839"* â€”
and that was found on 2026-08-11, when `data/exclusions.json`'s entry was rewritten to say the
exclusion was FALSIFIED and would stay "only until a structure record replaces it". It waited
eighteen days. `data/structures/new_york_house.json` is that record, and the entry has moved from
`excluded` to the watch list, which is the category it has actually belonged to since.

**The opening month is answered from the other side.** Andreas gives no month, so on Andreas alone
whether the house was open on the scene date was an argument. The Chicago American of 13 June 1835
carries two men advertising offices AT the house â€” Dr J. B. Barnard, physician, "at the New York
House, Lake street" (p. 3 col. 3), and J. C. Bradley, a travelling dentist, "his office at the New
York House, where he will remain until after the Land Sale" (p. 3 col. 2, repeated 1835-06-20).
Both are carried on the record's `occupants` with their claims, and both readings are
transcription-mediated under the owner's ruling of 2026-08-28.

**What this unblocks.** "The New York House" is an anchor in the American's advertising, and
`tools/compile_register.py` refused two placeable businesses with the same sentence â€” *"The anchor
'the New York House' names nothing the committed town holds."* Rebuilt against the committed town
it resolves both: Bradley matches the house's occupants, and Barnard's placement now names
`new_york_house` as its landmark. That is why T-0306 was split; the remaining pieces are T-0381
and T-0382.

**What is unverified, stated plainly.**

- **The side of Wells is not evidence.** Andreas says "near Wells" and Wells has two sides. The
  house stands on the free Wells-end lot of `blk_south_water_franklin`, west of Wells, because
  that lot is empty while the eastern block's Lake face already carries three dealt roofs â€” a
  reason about this dataset, recorded at **L209** and carried as the watch-list entry's own
  question. The corner is refused in writing: the source says *near*, not *at the corner of*.
- **The form beyond two storeys and eaves-to-the-street is the type talking**, claimed at **L208**:
  the 40 Ã— 25 ft plan is the dataset's stock period rectangle, and the paint, pitch, bays, gallery
  and two stacks are the archetype's.
- **The desktop viewport of the renderer smoke was NOT run.** `docs/PIPELINE.md`'s dev gate is
  `tools/check.sh` and this suite is dispatch-plus-one-path; desktop part 4 alone exceeded the
  ten-minute ceiling on a single foreground command on a loaded runner, and the run had no room
  for the ~25-minute crawl. **Mobile was run in full, all nine parts, against the published
  mirror, and is green** â€” mobile is the release gate. Desktop part 4 also carries a standing red
  on `dev` from before this branch (`tools/dev-smoke-state.json`, 2026-08-28: the light tier's
  80-call floor at Lake and Market).
- **`tools/check.sh` is green except for the seven failures `origin/dev` already carries** â€” the
  cross-street faces, `blk_washington_clark` standing off the modelled ground, the southern
  coverage reading and three far-timber census lines. Measured on an unmodified `origin/dev`
  worktree in this run: the same seven, and no others on either side.

**Three census lines in the suite moved with the data and were updated in the same commit**, which
is what each of their own comments asks of a run that moves them: the frontage layer's post count
(15 â†’ 16), the hitching posts (14 â†’ 15, twelve at the street edge â†’ thirteen â€” a documented public
house qualifies for a post under T-0194's rule), and the Evidence panel's open questions (3 â†’ 4,
with the card's in-scene set going from one beside the Western Hotel to two).

---
## Shipped 2026-08-29 â€” T-0383: the saddlery at Lake and Canal is S. B. Cobb's alone

**The board on that shop lettered a partnership the same corpus says was dissolved four and a half
months before the scene date.** `goss_cobb_saddlery` was built in August 2026 from one advertisement
â€” the *Chicago Democrat* of 26 November 1833, "they have opened a shop in this village, on the
conner of Lake and Canal-streets" â€” and its own `documented_range` note closed by naming what would
move it: *"further issues of the Chicago Democrat or the Chicago American. One line of an 1834 or
1835 advertisement would settle the survival and might settle the corner."* T-0261 read the
American's thirteen issues on 2026-08-28. It answers one half of that sentence and refuses the
other.

| what the American prints | claim |
|---|---|
| the dissolution, dated *Chicago, Feb. 18, 1835*, one signature unread | `chicago_american_1835_06_08#c006` |
| the same notice with **OLIVER GOS[S]** now legible | `chicago_american_1835_06_13#c015` |
| *"[S]A[D]DLE, HARNESS & TRUNK M[anufa]c[tor]y. S[. ]B[. ]COB[B] [w]il[l] [c]o[nt]in[ue] the [above business] at his shop"* | `chicago_american_1835_06_13#c016` |
| the same card again, ten days AFTER the scene date | `chicago_american_1835_07_11#c008` |

**Survival is settled and the corner is not.** `documented_range` moves `reconstructed` â†’
`inferred`: four printed dates now bridge the nineteen months the old range carried forward on
nothing, the last of them past 1 July 1835. The cross street is lost in all three 1835 printings â€”
*"Lake anc Amor. streets"*, then no street names at all, then *"corner of Lake and THE Balle"* â€” so
**the building has not moved a metre**, the quadrant guard and the Canal-versus-West-Water doubt
stand exactly as written, and that question stays T-0305's, on the page images.

**What a visitor sees.** The board reads `S. B. COBB / Saddle, Harness & Trunk Manufactory / Lake &
Canal Streets` (2.30 m wide against 2.29, which is the only geometry that moved anywhere in this
change), and the card behind it is headed for Cobb instead of the firm. `occupants` is `attested`
over `chicago_american_1835`; the firm survives in `aka` and in the record's own prose, because the
1833 advertisement is the better-attested of the two facts and deleting it to record the later one
would be a loss.

**`docs/LIBERTIES.md` L78 is REVISED rather than resolved.** It covered three admissions â€” the
range, the footprint and the storey count â€” and exactly one of them has been discharged, so its
`Covers:` line drops `documented_range` and keeps the other two. Moving it to Resolved would have
exempted two live inventions from the gate that checks them.

**Not verified here, and stated.** `dev`'s own gate was red at three steps before this branch
existed â€” the dooryard plantings, the planted poplar rows and the yard goods have all drifted from
their rules since T-0307 moved North Water Street, which is **T-0377**. This diff is red at those
same three steps and no others; none of the three files names this record, this phase or this trade
anywhere in them.

## Shipped 2026-08-29 â€” T-0244: the gate could not see twelve of the fourteen hitching posts

**The geometry was right the whole time and the instrument was blind.** The frontage layer's post
probe in `tools/smoke_renderer.mjs` read `mesh?.geometry` â€” the layer's single shared `frontage`
mesh â€” with a comment saying "the posts live in the shared mesh". That was true on 2026-08-19 and
stopped being true on 2026-08-21, when T-0194 put twelve hitching posts at the town's trading
frontages. A post that names a street is STANDING timber and lands in that street's
`<record>__<street>__standing` chunk, published as a `frontage-chunk` mesh so it culls and casts
with the fences beside it and costs no draw call of its own (T-0069, T-0194). The shared mesh never
holds one. So all twelve reported a max and a min over an EMPTY vertex set â€” `-Infinity` for a
height, `Infinity` for a foot â€” and the Sauganash's two, which its own record stands and which do
fall back to the shared mesh, went on measuring correctly.

**The repair is the resolution rule, not the count.** A post is now found by WHERE IT STANDS,
across every mesh the layer draws, because which mesh a post is folded into is a draw-call decision
that may change again without the post moving â€” the same lesson T-0243's batched wood taught the
tree census two days earlier. Read at both viewports on the published mirror:

| | posts | reading |
|---|---:|---|
| the Sauganash's own record (no `street`) | 2 | 1.300 m against a recorded 1.30, foot 0.000 |
| the street edge (`street` named) | 12 | 1.300 m against a recorded 1.30, foot 0.000 |

Each box holds exactly the 72 vertices of one post's shaft and cap, with one exception stated in
the code: at the Mansion House the board crossing over Lake Street brings its near edge 0.13 m from
the post and lays 15 more vertices in the box. They move neither reading â€” a crossing deck stands
0.06 m over its ground, under the foot the min is looking for and a metre and a quarter under the
head the max is â€” and the 0.4 m box is left alone rather than tightened onto the 0.22 m cap, which
would leave 0.02 m of margin against that same crossing.

**`found` is asserted separately from the heights**, because an empty vertex set fails the height
test too and reads as a post of the wrong height rather than as a post the gate cannot see. That
distinction is what cost this defect two days.

**A second stale number in the same part, and it is the ledger rather than an assertion weakened.**
"the frontage layer lays all five records' walks" expected **83** refusals and `dev` has **84**:
T-0028 opened `blk_lake_franklin`, whose dealt warehouse stands 1.50 m off that lot's frontage line
â€” inside the 3.0 m a street fence needs, so the building IS the street wall and the fence is
refused with a written reason. Nothing else in that line moves: 5 records, 51 walks, 39 crossings,
15 posts, 35 fence runs, 899,148 vertices, no problems. The count carries its reason beside T-0241's,
T-0196's, T-0024's, T-0228's and T-0246's, as each of those did.

**Why both reached `dev`.** `docs/PIPELINE.md`: the dev gate is `check.sh` and nothing else, and
`check.sh` asks whether a record re-derives from its own rule, never whether the renderer draws it.
The renderer smoke is dispatch-plus-one-path on purpose, so a check that only Playwright runs can go
red on `dev` without blocking a merge â€” the same gap T-0242 and T-0243 record for two other layers.

**The visible parcel this unblocks (AGENTS.md Â§ VISIBLE-PROGRESS exemption 3): T-0192**, at the top
of QUEUE.md â€” the cross streets' own frontages get the street edge. It lands in this exact layer and
its demonstration is desktop part 2, which could not be read while two of that part's frontage
assertions were standing red for reasons of their own.

**Gates.** `./tools/check.sh` **PASS**. `node tools/smoke_renderer.mjs --published` stage **2** at
**both** viewports â€” desktop 1280Ã—800 and mobile 390Ã—780 â€” **82/0 each, zero page errors**. The
other standing reds on `dev` are untouched and are their own tickets: T-0243 (the tree stations),
T-0279 (flower heads over open ground), T-0247/T-0249 (the light tier's draw calls), T-0271/T-0223
(`balanced` at the forks).

**Nothing you can see changed.** No renderer, no data record and no geometry was touched â€” only the
harness that reads the geometry back.

## Shipped 2026-08-29 â€” T-0316: the large river warehouse leaves the plat

`tools/reconcile_665.py` dealt **F3, the large river warehouse**, to platted blocks. T-0028 found
it on 2026-08-28 by opening `blk_lake_franklin` and being unable to build the F3 it had been dealt:
sampled against the committed heightfield the nearest water to that block's boundary is **134 m**,
its cargo doors would open onto a residential street and its landing apron would cross a public
one. The stopgap put F3 in `tools/generate_block_infill.py`'s `REFUSED_FAMILIES`, so the recipe
DEFERS the slot with a stated reason (L203) instead of reaching for a shape â€” which keeps the roof
on the books and treats a fault in the DEAL as a fault at the block. Every future platted block
dealt an F3 would have deferred it too.

**The repair is upstream, in T-0213's shape.** A family whose own crosswalk record makes water
access a precondition of the FORM is never dealt to a platted block â€” **at any distance**, because
the constraint is the generator's and not the ground's: `generate_block_infill.py` authors no metre
outside a committed lot polygon inside four platted STREETS, and the wharf and landing ground of
the main stem is placed by `generate_river_wharves.py` against the committed bank, outside that
grid entirely.

**Which families, read off the records rather than asserted.** Two readings of the crosswalk have
to agree or the derive refuses: a keyword scan of `required_variant` and the `variants` line says
which families are even in question (**F1, F3, W5**), and `WATERSIDE_JUDGEMENT` says which of those
the record REQUIRES water for, **quoting that record's own `assumption_note` verbatim**.

| family | requires water | the record's own sentence |
|---|---|---|
| **F3** Large river warehouse | yes | "Landing apron and cargo-door arrangement must follow site access and cannot extend into water or duplicate a counted pier." |
| **W5** Sawmill, boat-repair or riverside shop | yes | "river access requires validated dry-bank terrain contact." |
| F1 Freight or storage shed | no | "Stored goods and dock relationship are not known for anonymous slots; skids belong only where terrain and route access support them." |

T-0316 asked for F1, F2 and F4 to be checked while the run was here. **F2** ("Hoist beam presence
varies; cargo type and operator are not inferred") and **F4** ("Board-stack quantity and open-side
pattern are visual variation, not inventory facts") name no water at all and are not candidates â€”
so the ticket's own guess that F4 "carries the same site logic" is **refuted by F4's record**.
Edit any of those notes, or add a family that names a wharf, and the re-derive fails by name rather
than silently re-classifying it.

**It is a permutation, and that is asserted rather than trusted.** One waterside roof on a platted
block is exchanged for a dry PRINCIPAL roof of the same trade-ness on that district's own unbounded
balance. The re-derive moves exactly one roof today:

```
waterside (T-0316): F3, W5 require water â€” F3 blk_south_water_market -> south_plat_beyond_committed_control for C2
```

No total moves: not the 662, not a district, not a family, not any unit's roof count, and not its
principal/ancillary split â€” each of those is checked in the tool. `blk_lake_franklin`'s own
deferral stands as the record of what happened; the block generator's refusal stays where T-0028
put it, now as a belt rather than the only brace.

**Gates.** `tools/check.sh` green (the full dev gate, including the `reconcile_665.py --check`
re-derive and the changelog contract). `python3 tools/measure_family_deal.py` green â€” 0 refusals,
31 off-band claims, every one already named in `tools/family_deal_baseline.json`, nothing new and
nothing grown. No renderer file, no geometry, no coordinate, no mesh, no bake: the programme
document is not loaded by the walkthrough and is not published.

## Shipped 2026-08-29 â€” T-0243: the two timber gates read a batched mesh, and one of them could never fail

**T-0243.** `tools/smoke_renderer.mjs` stage 7 held two checks on the near-field wood, and
both traversed for `/^timber__/` â€” the four merged quadrant meshes `timber__q0â€¦q3`. T-0223
replaced them on 2026-08-27 with a single `THREE.BatchedMesh` named **`timber`**, and from
that merge the regex matched nothing:

- **`every tree drawn stands at its own station`** went red on its own liveness clause
  (`meshes > 0`), on an **unmodified `dev`**. Every branch cut from dev inherited it and had
  to argue "not mine" â€” measured three times in two days.
- **`no timber is drawn out in the channel`** asserts `offshore === 0`, and an empty
  traversal yields zero offshore vertices. **It passed, green, for a fortnight, having
  asserted nothing at all about the timber.** That is the worse half, and it is the reason
  this ticket was sized as a repair rather than a rename.

**Why a rename would have been the wrong fix.** A `BatchedMesh` holds every chunk in one pair
of buffers with a per-instance transform the batch owns, so
`geometry.getAttribute('position')` read through `matrixWorld` is not a chunk's world
position. `tools/drawn_timber_census.mjs` (new) walks each instance's own geometry range
under its own matrix, through `_instanceInfo` / `_geometryInfo` / `_matricesTexture` â€” the two
structures `getBoundingBoxAt()` and `getMatrixAt()` read, walked in the page so the census
needs no THREE there. It is the same arrangement `drawn_placement_census.mjs` uses for the
building batches, deliberately: the gate and the instrument run ONE census, not two readings
of the same idea.

**It still reads a plain `timber__*` mesh.** Unwinding the batching cannot silently empty the
gate the way landing it did.

**The bars did not move, and the liveness clauses grew.** 24 m is the widest crown's reach
plus its lean; 12 m is a bank willow leaning over the channel; both were argued in T-0110's
box and neither was touched. Both now come back FROM the census (`strayBarM`, `offshoreBarM`)
rather than being written a second time in the gate. And `chunks > 0 && verts > 1000 &&
unreadable === 0` guards **both** checks now â€” the offshore half had no liveness clause at
all, which is precisely how it passed on nothing.

**And it is demonstrated to fail.** `tools/measure_drawn_timber.mjs --refute` displaces two
chunks of the live scene â€” one mirrored across the datum's east-west line (R-BUG5b's own
fault, applied to the chunk standing furthest from that line, because a chunk on the line is
its own mirror), one translated to a point the terrain mask calls water more than 16 m from
any bank â€” and requires the census to report each. Clean run, source tree, 1280Ã—800:
**152,792 vertices across 70 chunks in 1 batch against 881 stations, 0 stray (worst
measurable 15.4 m), 242 over water at all and 0 offshore.** Broken: **3,140 stray** (3,118
beyond the station hash) and **1,099 offshore**, worst 24 m. A gate this shape is believed
because it can be made to fail, not because it is green.

**What this does not do.** It repairs neither T-0244 (the twelve hitching posts draw no
vertices the gate can find) nor T-0265 (the sward census at a phone). Those are the other two
standing reds and they are their own tickets. *(T-0244 closed 2026-08-29 â€” the top section of
this file; the posts were drawn all along and the probe read one mesh of the layer's several.)*

**Nothing you can see changed.** No renderer, no data record and no geometry was touched â€”
only the harness that reads the geometry back.

## Recorded 2026-08-29 â€” T-0328's tail: the reading gets its dossier, and coverage.json stops saying 56

**T-0328 shipped in PR #510** â€” D. Weaver's building is on **Lot 2**, block 1, North Water
street, on four printings against one. The notice turned out to be a standing advertisement
running in five consecutive numbers; three of them (1834-11-26 c010, 1834-12-03 c025,
1834-12-10 c012) had never been claimed by any reading pass, and all three set Lot 2. No
transcription was amended to reach it, which is the rule T-0294 was keeping when it claimed
both disagreeing printings and edited neither.

**This entry is what that merge left behind**, and both halves are record hygiene rather than
new reading:

- **`coverage.json` was asserting a count that had stopped being true.** The December 1834
  range said *"Four issues, read through, 56 claims"* and *"none of the 56 claims is counted
  unresolved"*. The month holds **60**. Counted per commit rather than re-asserted: 56 at
  `103168a0` (T-0294), 57 at `26f03456` (T-0339), 58 at `c49d8fa5` (T-0330), 60 at `5c638546`
  (T-0328). The range now says so, and says the later four are machine-checked on `dev` like
  the original 56. The November range records its own addition and â€” the part worth keeping â€”
  **why the read missed it**: the notice stands in the alternating pair of physical columns,
  surviving as every other line, which is the shape that month's reads found hardest. That is
  a fact about the instrument and it belongs where the next reader of the month will see it.
- **`docs/RESEARCH/weaver_building_north_water_block_1.md` is new.** AGENTS.md Â§ Honesty
  rules requires a dossier where sources disagree; the reading was made and defended in the
  claim notes, which is where a reader of that claim finds it and nowhere else.

**The dossier also states what the ticket's own premise got wrong.** T-0328 rested on "2 and
9 are not a confusable pair in clean type". True, and the conclusion followed â€” but this type
is not clean: the same advertisement's copy dateline is set **12, 12, 13 and 19** across the
five weeks. The reading stands on the count of independent settings, not on any one column
being trustworthy. **T-0350** carries the dateline.

**Still `transcription_mediated`.** The acceptance asked for the digit off a page image; the
deposit holds transcriptions only, and no scan has been read. Written down rather than
passed over.

**Nothing you can see changed**, and no claim, quote, gazetteer entry or geometry was
touched â€” only the two records that describe what was read.

## Shipped 2026-08-29 â€” T-0262: the scene-date register, and what the papers can actually do to the town

**`tools/compile_register.py` turns the gazetteer into a work list.** The gazetteer is an index of
what was PRINTED â€” 1,094 claims out of 82 issues, 221 businesses, 2,201 people. It says nothing
about what the model should build. The register does: for every business an ACTION against the
committed town, for every person whether the town already holds them. It is derived, wholly, and
`check.sh` re-derives it and refuses a committed copy a rebuild would not produce â€” the same
contract `gazetteer.json` is under, for the same reason.

**Ruling 3 gains the word BEFORE.** `built_at_scene_date` in the gazetteer is `not contradicted_by`,
whatever the contradiction is dated, which struck a firm out of a July town on the strength of an
August dissolution notice. Here the veto is a contradiction dated ON OR BEFORE 1835-07-01. A later
one is recorded â€” `dissolved_after_scene_date`, one business â€” and disobeyed.

**The ticket's second exclusion was a proxy, and T-0356 replaced it with the field.** T-0262 asked
to exclude entries whose only 1835 evidence `announces_opening` after 1 July. There was no
`announces_opening` in the claim vocabulary â€” except as a bare `true` on twenty claims that no tool
read â€” so the register used the derivable proxy `first_evidence_after_scene_date`: a business whose
FIRST issue postdates the scene date evidences nothing about 1 July. Thirty-eight businesses by the
time the corpus was fully read.

**The re-read settled it, and the proxy was excluding houses the papers put in the town.** The
claim now carries `{verbatim, dating, iso, note}` and the DATING decides: a `stated` future opening
after the scene date excludes; an `effected` one is dated by the advertisement's own dateline and
bounds the opening from ABOVE, so it never excludes; an `undated` one decides nothing. Four of the
thirty-eight genuinely announce a later opening and stay out â€” Cromelien's wine branch (14 Aug),
Everts' high school for young gentlemen (10 Aug), Hunt's for young ladies (17 Aug), Lyon's
wholesale grocery (1 Sep). **Thirty-four are restored**, and five of those are printed standing in
the July town: Wm. H. Taylor's boot store over a dateline of 8 JULY 1834, Wm. H. Kennicott saying he
had practised dentistry here "for the past year", Samuel Lewis's music-school copy dated 22 June,
S. Abell's 24 June and John Holbrook's 10 June. The register's placeable count moves from 66 to 78
and its street-only count from 47 to 63.

**What replaced the proxy is not nothing.** A business first printed in August that announces no
opening now stands under ruling 3, and that is a liberty: `backdating_liberty_required`, the
forward twin of `survival_liberty_required` â€” documented only after the scene date, present on it
by assumption. Thirty-three businesses carry it, computed and never asserted. `docs/LIBERTIES.md`
carries neither class yet (T-0357 is the survival half, T-0404 the backdating half).

### The counts, which are the epic's yield measured

| businesses | 221 |
|---|---|
| present at the scene date | 190 |
| excluded â€” contradicted before 1835-07-01 | 14 |
| excluded â€” first evidence after 1835-07-01 (the proxy T-0356 retired) | 17 |
| `enrich_existing` (a committed building already carries it) | 39 |
| `new_building` (placeable against the committed town) | 24 |
| `street_only` (a street face and no closer) | 49 |
| `unplaceable` (no street the model holds) | 109 |
| standing on a survival liberty (last evidence pre-1835) | 129 |

| persons | 2,201 |
|---|---|
| `enrich` â€” already in `data/residents/` | 117 |
| `replace_invented` â€” a documented person of an invented household's trade | 113 |
| `new_resident` â€” ruling 1 | 1,971 |
| â€¦of those, known only from the letter lists | 1,555 |
| **invented households the register can retire** | **28 of 117** |

Those are the figures the epic landed on, and they are kept as landed. **Re-measured on
2026-08-29, after the whole corpus was read and after T-0356 replaced the proxy exclusion
with the field**, the same register reads:

| businesses | 242 |
|---|---|
| present at the scene date | 224 |
| excluded â€” contradicted before 1835-07-01 | 14 |
| excluded â€” opening announced after 1835-07-01 | 4 |
| `enrich_existing` | 38 |
| `new_building` | 30 |
| `street_only` | 63 |
| `unplaceable` | 111 |
| standing on a survival liberty (last evidence pre-1835) | 126 |
| standing on a backdating liberty (first evidence post-scene-date) | 33 |

| persons | 2,628 |
|---|---|
| `enrich` | 184 |
| `replace_invented` | 119 |
| `new_resident` | 2,325 |
| **invented households the register can retire** | **27** |

The retirement figure is a count of HOUSEHOLDS and it is capped per trade by construction: three
documented tailors retire at most the tailors the town invented. Reporting the matched persons
instead would report 113 people retiring 117 households, which is a number about nothing. The 28
are 4 blacksmiths, 4 grocers, 4 tavern keepers, 3 shoemakers, 2 joiners, 2 tailors and one each of
baker, butcher, cooper, dentist, harness maker, hotel keeper, merchant, painter and physician.

### Matching a firm to a building is a different question from matching a firm to a firm

The first cut of `enrich_existing` claimed 58 buildings and a good many of them were wrong, in four
distinct ways. Each is now a guard with a self-test on the case that forced it.

1. **A `proprietors` entry is routinely a whole firm style** â€” `Clark, Filer & Co.`, `H. Doty & Co.`,
   `Kinzie & Hall` â€” and taking its last word for a surname reads those three firms as `co`, `co`
   and `hall`. Two of them then matched Daniel Elston's soap works, whose occupants line ends
   `& Co.`. The partners now come from the gazetteer's own firm policy (`firm_surnames`, T-0304).
2. **A surname is not a person.** The Kinzie brothers are one surname and three businesses; matching
   on `kinzie` put R. A. Kinzie's store inside J. H. Kinzie's. Where the RECORD prints a forename
   and the PAPER prints one, they must now agree â€” and two spelled-out forenames must agree whole,
   not by initial, because `John S. Kinzie` and the James Kinzie House share a `j`. The test is
   asked of the whole record, not of the field the surname was found in, or a disagreement simply
   routes round the guard by dropping to the next tier.
3. **An `aka` is where a record keeps its loosest descriptions.** `Taylor's tavern` is a real second
   name of the Wolf Point Tavern and W. H. Taylor's boot and shoe store is a different Taylor, so
   an aka match now also requires the trades to agree. And an aka that locates a building by
   ANOTHER building â€” `the cabins near Wentworth's tavern` â€” is cut at its locative word, which is
   what stopped Elijah Wentworth's tavern on Flag Creek matching a row of log cabins at Wolf Point.
4. **An anonymous reconstructed roof cannot ALREADY carry a documented business.** `recon_*` and
   `inf_*` are excluded outright. Putting a documented firm into an invented roof is a decision
   T-0263 makes deliberately, with the adoption written down; making it by string match is how an
   invention gets laundered into the documented layer. `Kinzie Hall` had matched
   `recon_1835_north_i2_015` on the word "hall".

Every surviving `enrich_existing` carries the tier it matched on and the exact text it matched
against, so T-0263 can argue with a proposal without re-running anything.

### A name is not always one building, and the anchor path used to pretend it was

`resolve_anchor` reads the landmark a paper prints â€” "David Carver's Old Stand", "west of J.
Wright's" â€” against the committed town, and until 2026-08-29 `match_landmark` ended
`return sorted(hits)[0] if hits else None`. Where two committed records answered to one name it
took whichever id sorted first and the register wrote *"The landmark is the committed structure
X"* over it. Nothing in the file said a second record had answered to the same name; an
alphabetical tie-break came out looking like a reading.

**Thirty-five identity-word sets in the committed town are held by more than one record**, and the
figure is derived on every build â€” `compiled_from.structures_sharing_a_name` in the register, and
`tools/check.sh` prints it. Twenty-eight are anonymous count-units, where the collision is a
consequence of naming a roof "Reconstructed 2-room frame cottage 02" and no advertisement will
ever print it. **Seven are named landmarks a paper could name, and would:**

| the name | the records it answers to |
|---|---|
| `pier`, `harbour pier works` | `north_pier`, `south_pier` |
| `branch bridge`, `branch bridge first over` | `north_branch_bridge`, `south_branch_raft_bridge` |
| `house school watkins` | `north_side_school_1833`, `watkins_school_house` |
| `crossing slough water` | `north_water_slough_crossing`, `slough_log_bridge` |
| `building john let wright` | `wright_building_to_let_a`, `wright_building_to_let_b` |

The Wright pair is the case T-0386 is blocked behind and the clearest of the seven: one
advertisement, two buildings to let, one proprietor's name, and the only thing separating the two
records is the *(east)* / *(west)* this project added â€” which `words()` drops as a stop word, so
the two are one name to every reading pass that will ever run. `north` and `south` are stop words
for the same reason, which is why the piers and the branch bridges collide too.

So the anchor now has a **sixth kind, `ambiguous`**: the name was recognised, the town holds it
more than once, and the register refuses rather than picks â€” naming every rival in the note. It
never places; a business whose anchor is ambiguous falls to `street_only` or `unplaceable` on the
street the paper printed, exactly as an unresolved one does. The same refusal guards the one-hop
business match below it, because the corpus prints one house under more than one heading.

**No placement in the register moves today**, and that is the honest measure of this change: zero
of the 209 businesses print an anchor that lands on one of the thirty-five. It is a guard against a
fabrication rather than the repair of one â€” and the thing it guards is live, because the moment a
reading pass widens enough to see past a project-added disambiguator, "J. Wright's" resolves onto
two records and the old code would have picked the east one.

### The T-0257 fixtures, as the acceptance requires

`business_j_s_c_hogan` â†’ `enrich_existing`, target `hogan_store`, matched on the record's own name.
`business_peter_cohen` â†’ `street_only`, target `south_water`: the paper's anchor is "the east end of
South Water-street", which the register resolves as a REACH of a platted street â€” a real resolution
and not a placement, so it reads as its own anchor kind rather than as a failure.

### What is honestly not settled

- **One reading pass is still open.** T-0297 (August 1835, the four issues AFTER the scene date) was
  in flight in a sibling run when this was built. The register is deterministic and re-derived by
  the gate, so `--build` after that merges refreshes it; the counts above are as of the gazetteer on
  `dev` at 2026-08-29.
- **`wolf_point_tavern_stable` still takes Elijah Wentworth's Flag Creek tavern**, on an occupants
  line that reads "Elijah Wentworth in 1831, William Walters on the scene date". The match is on a
  HISTORICAL occupant of a building whose scene-date occupant the same sentence names. T-0355.
- **78 businesses stand at the scene date and are placeable nowhere.** That is the size of the
  problem the seeding tickets do not solve, and it is a fact about the papers, not about the tool.

Filed with the register in hand: **T-0354** (the `street_only` and `unplaceable` policy â€” 49 and
78), **T-0355** (the historical-occupant match), **T-0356** (`announces_opening` as a real claim
field rather than a proxy) and **T-0357** (the 129 survival liberties `docs/LIBERTIES.md` does not
yet carry). All PAPERS, all appended to the bottom of QUEUE.md â€” the owner orders it.

## Shipped 2026-08-29 â€” T-0283: the North's freight row is repaired, and the fault was a split fault

**The row allowed the North Division ONE freight roof and seven stand there.** T-0211 found the
breach on 2026-08-28, declared it as a ratchet so it could not grow, and deliberately did not repair
it: repairing it is a decision about the authored target, and the cells sum to their division's
target AND to their group's total, so no cell moves alone.

**The decision, and it is narrower than the ticket feared.** The town-wide freight total is
contradicted by nothing â€” twenty are authored, twelve stand. What is wrong is WHERE the programme
put them. So the repair is a split repair, four cells wide:

| group | division | was | now |
|---|---|---|---|
| `warehouses_freight` | north | 1 | **7** |
| `warehouses_freight` | south | 17 | **11** |
| `ordinary_dwellings` | north | 90 | **84** |
| `ordinary_dwellings` | south | 170 | **176** |

Both row totals stand (335 and 20), all four district targets stand (365 / 135 / 152 / 10),
`family_targets` is untouched and `roof_total` is untouched. Nothing that stands moves; no mesh
changes; the 662 roofs are the same 662 roofs, re-typed.

**Why the South pays and no one else.** Six of the North's seven freight roofs are documented
pre-existing records â€” Kinzie & Hunter's warehouse, the four north-bank sheds at the Dearborn reach,
the north-side brickyard â€” and the seventh, `recon_1835_north_f1_022`, was dealt by a parcel that ran
before anything measured this. Against them the South's freight cell holds seventeen authored slots
of which five stand: twelve are unbuilt and unnamed. **An authored slot yields to a documented
record** â€” the principle T-0032 established when it held the institutional row to the named census â€”
and the South's cell is the only one that can pay without moving a group total or a division target.
The compensating `ordinary_dwellings` swap is what keeps each division's own column on its target.

**What it costs, stated rather than clamped.** The South is scheduled six fewer warehouses (freight
remainder 12 â†’ 6) and six more ordinary dwellings (72 â†’ 78), and its business-front re-deal now moves
7 trade roofs where it moved 9. The North's remainder does not move by a single roof â€” but it stops
being scheduled seven houses short for a reason nothing anywhere stated:
`reconcile_665.py`'s clamp shed **7** slots from north `ordinary_dwellings` before this and sheds
**1** after. That last one is L93's anonymous school, which is not an authoring fault at all â€” it is
`measure_group_district_rows.py` and `measure_institutional_claims.py` reading one liberty
differently â€” and it moves when the liberty is retired, not before.

**The gate lost its declaration and gained a case.** `("north", "warehouses_freight")` is RETIRED
from `DECLARED_OVERSHOOT`, not lowered, and a new self-test case asserts both halves of that â€” the
row is not over AND it carries no declaration â€” because either half alone passes vacuously. The
three ratchet cases used to drive the freight declaration; a declaration of size 1 cannot fall
without disappearing, so `overshoot_findings` now takes the table it reads and the self-test hands it
a synthetic one. `--self-test` is nine cases green. The argument lives at
`district_group_matrix_note` in `data/reconstruction/1835_building_inventory.json`, beside the
`roof_total_note` that records the only other time a count in that file moved.

## Shipped 2026-08-28 â€” T-0028: `blk_lake_franklin` opens, and the warehouse it was dealt is refused rather than massed

**The first NEW platted block this programme has opened since 2026-08-23**, when T-0028 re-derived
the schedule with `tools/reconcile_665.py` and found there was nothing left to open: eleven blocks
`at_capacity`, six `open` but only on lots that already stand (T-0143's core density, a different
ticket), one `reserved`, and two `gated` on street control. That run filed T-0163, which landed on
2026-08-24, split the two refusals apart and measured them â€” and did NOT open a block. It found
`blk_south_water_clinton` was never a block at all (`never_platted`, 328 m away with 20 of 66
samples wet â€” opposite banks) and escalated `blk_south_water_market` to T-0183, where it still sits
`blocked-owner`.

**What reopened the programme was the DEAL, not control.** `blk_lake_franklin` â€” Lake, Wells,
Randolph, Franklin â€” has stood `open` with two free lots throughout. T-0188 read it on 2026-08-27
and recorded that it *"cannot carry a three-unit run as dealt"*, because the schedule dealt it
**I3**, which `generate_block_infill.py` refuses by name, alongside **F3**. T-0213 weighted the
trade families onto the business front on 2026-08-26; the I3 went with it. Re-derived today the
deal is A1, D1, D5 and F3 â€” three of four buildable â€” so the block opens.

**The arrangement is measured on both rules, and they agree.** `tools/measure_street_frontage.py`
counts 16 documented records and 8 inferred households within 25 m of Lake Street's committed
centreline against Randolph's 7 and 7 (the reconstruction column is this programme's own output and
does not vote), so Lake is the business face. `tools/measure_end_rule.py` puts lot 4 at 441.12 m
from the foot of the Dearborn Street drawbridge against lot 7's 473.20 m straight, 550.45 m against
668.96 m walked. So the free Lake lot takes the row, the free Randolph lot is left open, and inside
the run the better roof stands at the east end nearest the crossing: a deep-plan frame cottage
anchored 1.5 m off the lot's east margin, an older log dwelling abutting west of it on one party
wall, and the stable in the same lot's yard at the alley end.

**The street line was not adopted â€” it agreed, and that is worth recording.** This face carried no
frontage-declaring record before the run, so there was no built line to adopt under T-0104 and the
floor is the plat module's own 1.5 m lot margin. `temple_lake_st_building`, a documented record
placed by an entirely different parcel that declares no frontage, stands 1.492 m off the same face
at 75.73â€“82.52 m along. The run stands at 1.499 m and stops 3.90 m short of it. Seven millimetres,
by coincidence of the data rather than by anything this parcel chose. `tools/measure_street_line.py`
now reports nine block faces and every one of them is one street line.

**THE FOURTH ROOF IS REFUSED, AND THE REFUSAL IS THE FINDING.** F3 is the "Large river warehouse".
Its crosswalk entry makes water access a precondition of the FORM â€” required variant
`warehouse_river_large`, variants *"multiple cargo doors; landing apron; sparse glazing"*,
assumption note *"Landing apron and cargo-door arrangement must follow site access and cannot
extend into water or duplicate a counted pier."* This generator authors no coordinates: every metre
comes from a committed lot polygon inside a block bounded by four platted STREETS. Sampled against
the committed heightfield `e1834_harbor_cut`, the nearest water to this block's boundary is
**134 m**. So F3 joins I1, I2 and I3 in `REFUSED_FAMILIES` â€” for the opposite reason to theirs, and
the module comment now says which is which: the institutional families are refused for what an
anonymous one would CLAIM, F3 for the GROUND. The slot is deferred in the recipe with its reason
and the roof stays on the books.

**That is a stopgap and it is filed as one.** Treating a fault in the DEAL at the block means every
future platted block dealt an F3 will defer it, and three warehouse roofs will pile up as deferrals
nobody is scheduled to build. **T-0316** asks the deal to stop sending them inland, in the same
shape as T-0213 â€” and notes that F3 is absent from the generator's `FUNCTIONS` table and from the
`block` arm of `measure_family_deal.py` too, so the deal was reaching for a family the parcel shape
has never been able to name.

**Numbers.** 3 roofs (2 principal, 1 ancillary) of the block's 4 of headroom; 341 buildings standing
of 662; the block goes to 14 standing, 1 of headroom, 1 free lot. No roof is added to the town â€” the
three come out of `south_plat_beyond_committed_control`. Baked with `bake.sh --only` per structure;
`tools/check.sh` and `tools/smoke_renderer.mjs` green. Liberty **L203**. T-0028 closes on this one block
with its successor **T-0317** filed, which is what its own sizing note asks of every run: one run,
one demonstration, one successor.

## Shipped 2026-08-28 â€” T-0246: the log jail comes onto the plat, and Randolph's walk reaches its corner

**The fault is the modern-kerb read, for the fourth time.** `log_jail` was placed on 2026-08-11
from Andreas's *"northwest corner of the court-house square"*, and the square's four inside corners
were computed for that parcel from **modern OpenStreetMap intersection centres** stepped 12.2 m into
the block. That is the same derivation T-0127 found under the eleven South Water records and T-0196
found under Lake Street's four. Measured against this project's own committed line â€” the
`data/streets/1835.json` centreline offset by half the committed 80 ft corridor, which is what
`tools/generate_plat_lots.py` builds every block edge from â€” the jail's north wall stood **3.48 m
out past `blk_randolph_lasalle`'s Randolph frontage**, with its centroid inside the corridor.

**What it cost, and the second half was not obvious.** `tools/generate_frontage_works.py`'s march
refused the two steps of the square's own Randolph walk that the jail covered, 0.0 to 10.4 m along
the face. A walk refused short of its corner then takes the corner **crossing** with it â€” the rule
lays a crossing only where both walks reach the corner â€” so the LaSalle Street crossing at Randolph
was refused in turn, *"the two walks stop 34.8 m apart"*. One misplaced building was costing 10.4 m
of boards **and two board crossings**.

**The repair is this record's own method run against this project's own line.** The footprint is
translated **4.981 m** along the face's inward normal â€” dE âˆ’0.040, dN âˆ’4.981 in local ENU, so
UTM E 447538.25 N 4637126.21 becomes **E 447538.21 N 4637121.23** â€” which leaves its north wall
**1.50 m** back from the committed frontage line. The square is not subdivided, so there is no lot
line to stand off: 1.50 m is `plat_occupancy.LOT_MARGIN_M`, the plat module's own margin off a
boundary, and it is the same figure every reconciled South Water and Lake record took.

**Nothing along the street moved and no grade changed.** The along-face position, the block, the
corner and the side are untouched; the confidence stays `inferred`, because re-deriving a coordinate
from better geometry is not new evidence. The record's own 20 m working uncertainty from the
georeference is unchanged and is four times this move â€” so this reconciles two of this project's own
lines and does **not** claim to have located the jail better. The facade bearing stays 0 while the
face runs at 0.46Â°, which leaves the front wall between 1.50 and 1.55 m back across its width;
rotating a documented record is a second claim and this is a repair.

**Measured, before â†’ after.**

| | before | after |
|---|---:|---:|
| `log_jail` lap of the Randolph corridor | 3.48 m | none |
| placed phases lapping a platted corridor | 20 of 349 | **19 of 349** |
| in the DEEP mode (â‰¥ 3.48 m) | 6 | **5** |
| records lapping Randolph | 2 | **1** |
| `blk_randolph_lasalle` north walk | 10.4 â†’ 99.0 m of the face | **0.0 â†’ 99.0 m** |
| its walking decks | 6 | **7** |
| street edge, walk/crossing runs | 88 | **90** |
| street edge, walk laid | 3,160.3 m | **3,170.7 m** |
| street edge, crossings | 34 (811.0 m) | **36 (857.5 m)** |
| street edge, refusals stated | 84 | **83** |

The two new crossings are `blk_randolph_wells_north_crossing_blk_randolph_lasalle_north` (over
LaSalle Street) and `blk_lake_lasalle_south_crossing_over_randolph` (over Randolph). No refusal was
added, and no run was lost.

**What is left on Randolph, and it is not this fault.** One record still laps it:
`newberry_dole_slaughterhouse_south_branch`, 11.45 m in at the far west end, whose body is drawn
toward the street from its own anchor (K30(b)). Nothing here touches it.

**One earlier reading is now stale by five metres.** T-0224 fixed the `public_square` critic stand
by bisecting the estray pen and the log jail, and quotes the jail at **131.2 m off at 319.9Â°**. With
the jail reconciled it is **127.2 m at 320.2Â°** from the same stand. The bisector moves by 0.15Â°,
which is far inside the frame, and the stand was **not** re-derived here â€” the number is recorded as
moved rather than silently left reading as though it had not.

**The smoke's frontage census moved, and it is the ledger rather than an assertion weakened.**
`tools/smoke_renderer.mjs`'s "the frontage layer lays all five records' walks" carries a running
count with the reason for each move. Crossings 37 â†’ **39** and refusals 84 â†’ **83**; walks, posts
and fence runs do not move, because the returned steps EXTEND an existing run rather than opening
a new one. The comment says so, as T-0241, T-0196, T-0024 and T-0228 each did before it.

**Gates, and one of them is red â€” inherited, and one number is mine.** `tools/check.sh` **PASS**
(after `generate_yard_goods.py`, `compile_scene.py --all` and
`measure_corridor_intrusion.py --write-baseline`, which is the ratchet's own way to bank a repair).
`node tools/smoke_renderer.mjs --published`, run in staged legs at **both** viewports â€” mobile
390Ã—780 (1-2, 3-4, 5-6, 7-9) and desktop 1280Ã—800 (1â€¦9) â€” **zero page errors** anywhere. Every red
is on `dev` before this branch, each named to an open ticket:

| leg | red | whose |
|---|---|---|
| mobile 1-2, desktop 2 | twelve street-edge hitching posts measure `-Infinity` | **T-0244** â€” byte-identical to `dev`'s own standing record (`dev-smoke-state`, 2026-08-28T10:27) |
| mobile 7-9, desktop 7 | the tree-station assertion reads 0 of 0 vertices | **T-0243** â€” byte-identical to `dev`'s standing record |
| desktop 7 | 2,526 of 18,911 flower heads over open ground | **T-0279**, to its own figure |
| desktop 4 | the `light` tier draws 85 calls against its 80-call floor | **T-0247/T-0249** â€” **85 on a clean `origin/dev` worktree too**, so not this branch (`dev`'s stored 83 is a stale tree) |
| desktop 4 | `balanced` over its ceiling at the forks | **T-0271/T-0223** â€” and **1,160 triangles of it are mine** |

**The one number this branch moves on a red gate, stated rather than buried.** Measured on a clean
`origin/dev` worktree and on this branch, same stand (the forks, from Wolf Point), same command
(`SMOKE_VIEWPORT=desktop SMOKE_STAGE=4 node tools/smoke_renderer.mjs --published`). Re-taken after
this branch merged `origin/dev` at **`363d920b`**, so the comparison is against the base it lands
on and not the one it left; both readings were identical before and after those five commits:

| | clean `origin/dev` | this branch | delta |
|---|---:|---:|---:|
| `balanced` at the forks | 1,214,417 | **1,215,577** | **+1,160** |
| over the 1,210,000 ceiling by | 4,417 | **5,577** | +1,160 |

That is 10.4 m of plank walk, two board crossings and one more walking deck, at the street edge's
measured 42.8 triangles a metre. **The ceiling was already breached and it is not breached by this**
â€” but T-0223's complaint is precisely that content lands while the budget is over, so the increment
is recorded here rather than left for the next reading to discover. It was merged anyway on three
grounds: the dev gate is `check.sh` and nothing else (`docs/PIPELINE.md`), the breach is
owner-acknowledged and carried by four open tickets, and the alternative is leaving a documented
building drawn standing in a platted street. Nothing was weakened to pass.

**No bake.** The position lives in the sidecar the renderer reads, not in the mesh, and
`validate.py --stale` stayed green across the move.

**One side effect, and the rule is right.** `data/yard/town_trade_goods.json` re-derives with one
fewer wagon: `town_wagon_lasalle_2` stood on the verge the new LaSalle crossing now occupies, and
the yard rule refuses it â€” *"A footway is a floor and a wagon parked across it is the town's own
Ordinance 9 complaint, drawn."* 64 wagons to 63, and the refusal states itself.
## Shipped 2026-08-28 â€” T-0254: the North Water Street slough crossing, and the street west of it

**T-0226 left the North Division's river front with no roadway west of E +240 and said so.** It had
re-derived North Water Street from the committed north bank after finding 477.4 m of the old line
inside the water mask, and it stopped the derived line on the east shoulder of the attested
north-side slough because `renderers/web/js/streets.js` may not paint a ford â€” R-BUG4. The reach
west of that, to the North Branch, waited on a crossing record. This is it.

**The crossing.** `north_water_slough_crossing`, `bridge_timber`, a 12 m deck 3 m wide laid square
at local **E +183 .. +195, N +156 .. +159**. Reconstructed throughout; nothing records it. Measured
by `tools/measure_slough_crossing.py`, which now reads all three of the town's crossings:

| | open water under the deck | dry seats | walk | clearance |
|---|---|---|---|---|
| Slough Log Bridge, Water St | 3.30 m of 8.00 | 2.35 / 2.35 m | 0.83 m | 0.50 m |
| La Salle Slough Crossing | 5.55 m of 12.0 | 3.10 / 3.35 m | 0.84 m | 0.50 m |
| **North Water St Crossing** | **6.65 m of 12.0 (55 %)** | **2.60 / 2.75 m** | **0.68 m** | **0.35 m** |

**The clearance is read off the abutments, not borrowed.** The committed heightfield stands at
+0.63 m where the deck's west end lands and +0.73 m where its east end does, over a 0.00 m water
surface, so a walk surface at 0.68 m lies within 0.05 m of both banks. That is why this crossing
needs neither the graded cut its eldest sibling needed nor the fill the La Salle one did: no
approach entry was added to `terrain_spec.json` and none is wanted. Its two siblings' 0.50 m came
from the hydrology dossier's conjectural thalweg; this one's came from ground that can be measured.

**Where the deck goes, and why not on the old street line.** This slough is a **68.5 m funnel**
where it meets the main stem, narrowing to 32.4 m at N +130 and 16.2 m at N +140, with a **2.5 m
sill 0.18 m deep** at N +147.5â€“150 and a steady **5â€“7 m channel** above it. A crossing on a straight
river-front line would span 20 m of water 1.54 m deep â€” a river bridge, and the town built two of
those and remembered both by name. So the street goes round the head of the bay, as a bank road
does, and crosses where the stream is six metres wide.

**The street.** `tools/derive_north_water.py` now derives TWO reaches with the structure between
them â€” east from the deck at E +195 to E +830, west from E +183 to the North Branch at E âˆ’30 â€” and
each reach's smoothing window is clamped inside itself, because at E +190 the slough and the funnel
are one water run reaching N +165 and a window that saw it would push the street 20 m up the slough
instead of over it. **One bend stands in the water on purpose**, at the deck's midpoint [189, 157.5]:
R-BUG4 drops a panel whose centreline endpoint is wet, so the two panels the deck replaces are
dropped and the crossing carries the street. Dry bends at each shoulder would have painted a 6.65 m
ford in silence â€” the fault T-0254 was filed to avoid. `--gate` now asserts exactly one wet bend and
that it is the deck's.

**What the west reach costs, and it is not hidden.** The tool measures it:

    clearance from the waterline, northward:      12.05 m .. 41.95 m
    clearance from the waterline, perpendicular:  12.00 m .. 41.50 m

against a 12.192 m setback. The 41.5 m is **one 15 m stretch at the base of Wolf Point**, where the
bank falls 45 m of northing in 35 m of easting and the derivation's running maximum â€” which holds
the street north of every bank point within 15 m of it â€” lags the turn. The rule is doing what it
says. `SMOOTH_M` is shared with the committed east reach, so tuning it here would re-derive 590 m of
street nobody asked to move: filed as **T-0307** with three routes and an acceptance clause, not
tuned in this PR.

**What this is worth in the scene.** 250 m of roadway that has never been drawn, on the one division
whose whole waterfront street was missing, plus a third crossing beside the two that stand.
**What a reader should doubt first**, and the record says so in its own words: whether North Water
Street reached west of the slough in 1835 at all. Nothing places a building on that side of it and
the North Division's initial parcel puts its roofs north of N +105. If that street did not run, this
crossing did not stand. Recorded as **L202**.
## Shipped 2026-08-28 â€” T-0156: the flicker instrument stops overstating what it found

**A column called INTERIOR was quoted for six days as *the layer fighting itself*, and it never
meant that.** `tools/measure_tie_class.mjs` partitions a 2 mm-nudge flicker by which layer owns
each moving pixel, then splits each layer's share into its outline against the rest of the scene
and the pixels its own footprint surrounds on all eight sides. The second number was read as a
depth tie â€” the defect R-BUG6 was opened to find â€” and printed under the sentence *"the pixels
where a layer fights ITSELF"*.

`interiorOf` cannot support that reading. It knows one layer's outline against everything else and
is blind to the boundary between two surfaces OF that layer, so one crown behind another and a
chimney against its own roof both land inside it. T-0013 measured the size of the error on
2026-08-23 with a depth pass and found **94â€“98 % of the count sitting on a depth BREAK** â€” a
silhouette by any honest reading â€” and **0 % a depth reorder or a shading resample**. It changed
nothing in the instrument, deliberately: closing a ticket by rewriting the tool that measured it is
the one move this project does not allow.

**Five days later the instrument was still printing the refuted sentence**, so anybody reading the
tool rather than ROADMAP Â§ R-BUG6(c2) read the wrong claim. This ships the repair, by ADDING a
measurement rather than loosening one:

- `tools/depth_field.mjs` â€” T-0013's discriminator extracted whole (the packed-depth swap, the
  linearisation, the second-difference break test), imported by both instruments so they cannot
  answer the same question differently. The trade table in `generate_frontage_works.py` and the
  face arithmetic in `block_faces` are the same move for the same reason.
- `measure_tie_class.mjs` prints the split beside the count, names the column `SURROUNDED` â€” which
  is what it measures â€” and ends on the only total that ever meant what "interior" was taken to
  mean. Its `--out` masks now paint an internal edge and a self-fight different colours; before,
  one colour asserted the reading the depth pass refutes.

**The demonstration, both tools run the same afternoon on the same published mirror**, `from_above`,
1280Ã—800, 2 mm nudge, shadow map off, control 0 px and return 0 px: `structures` 421 surrounded â†’
**402 internal edge / 0 reorder / 0 same-surface / 19 no-depth**, and `trees` 231 â†’ **218 / 0 / 0 /
13** â€” agreeing pixel for pixel with `diagnose_interior_flicker.mjs`'s independent run. `ground`
reads 66 here against 77 there, and the gap is the tools' own layer lists rather than the
discriminator: `measure_tie_class` also carries `streets`, `flora` and `water`, which claim eleven
pixels first. **Self-fight across all six layers: 0 of 731.**

The surrounded counts are byte-identical to the run taken immediately before the change, so the
split is an addition and not a re-measurement. Against 2026-08-23 the counts moved (structures 370
â†’ 421, trees 257 â†’ 231) and the shares did not (95 / 94 / 98 % against 94 / 98 / 96 %) â€” five days
of content under a claim that survives it.

## Shipped 2026-08-28 â€” T-0224: a critic baseline standing on the public square

**T-0027 replanted a whole city block and nothing in this project could show it in a picture.** The
public square â€” the block bounded by Randolph, Clark, Washington and LaSalle, the one block
`data/reconstruction/1835_reserved_ground.json` holds was never private building ground â€” went from
wet prairie to sedge meadow on 2026-08-23, and it was verified by a zone lookup and a zero-pageerror
pass. `tools/critic_shots.mjs` had no stand on it or facing it, so the sward over the town's only
reserved block, and the county buildings standing on it, had no reading of any kind.

**The stand.** `public_square`, a pose station rather than an anchor: local `(550, -370)`, ground
0.885 m, bearing **292Â°**, pitch 0. It stands inside the block's south-east corner and looks across
its long diagonal, which is the longest run of reserved sward in the town.

**The bearing is derived, not chosen by eye.** It is the bisector of the two county buildings that
stand on 1 July 1835 â€” the estray pen at the south-west corner, **81.8 m off at 264.9Â°**, and the
log jail at the north-west corner, **131.2 m off at 319.9Â°**. They are 55.1Â° apart, so each sits
27.5Â° off centre. Both were projected through the renderer's own camera before the pose was fixed,
which is what settles the composition question the frame itself cannot: at 1280Ã—800 the camera
reports fov 55 and aspect 1.6 â€” half-FOV 39.8Â° â€” and puts them at **x = 246 and x = 1047 of 1280**;
at 390Ã—780 it reports fov 94 and aspect 0.5 â€” half-FOV 28.2Â° â€” which leaves **0.7Â° of margin** and
puts them at the extreme edges. **So the desktop row reads the ground and the two buildings, and
the mobile row reads the ground.** No stand on this block does better: its corners are 108 m apart
and the buildings sit on two of them.

**The third county building is not in the frame, and a frame that showed it would be the bug.** The
ticket names three; only two of them exist on the scene date. The first Cook County court-house was
erected on the north-east corner in the **fall** of 1835 â€” `documented_range.from` is `1835-10-01`
in `data/structures/cook_county_courthouse_1835.json`, on three independent Andreas passages â€” so it
is dated out of a 1 July scene and is absent from the registry, which the probe confirmed
(`inRegistry: false`, against `true` for the other two).

**The rows.** Shot against the committed tree, `--metrics`, source tree, full detail.

| viewport | timber all | timber centre | â€¦town's share of breaks | crown fine | crown Gâˆ’B | decile L | literal black px | RMS far/mid/near | flower load | BLOOM share of ground | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop 1280Ã—800 | 0.689 | 0.748 | 0.123 | 0.759 | 16.91 | 10.3 | 0 | 14.4 / 24.0 / 26.0 | 0.0034 | 0.0048 | 162 / 1,016,672 |
| mobile 390Ã—780 | 0.844 | 0.808 | 0.051 | 0.629 | 15.49 | 9.34 | 0 | 22.0 / 27.7 / 20.5 | 0.0007 | 0.0037 | 158 / 954,133 |

`sha256` `b08cedcd3653â€¦` desktop, `875e290b2dd1â€¦` mobile. Land/sky boundary row 401 of 800 and 391
of 780 â€” the horizon sits within a percent of the frame's own middle at both viewports, which is
what a level pitch on flat ground should give and is the cheapest available check that the pose
landed.

**What the rows say, and the one figure worth arguing with.**

- **This is the third station where flower load means anything.** Harness note 3 in *The critic
  baseline â€” 2026-08-14* holds that the flower denominator is only vegetation at the open-prairie
  stands; the near band here is reserved sward with no street, wall or roof in it, so `public_square`
  joins `prairie_south` and `prairie_west`. Desktop reads **0.0034**, which sits between those two
  (0.0031 and 0.0012 on 2026-08-14) and two orders under the 4â€“6 % brief. The block was replanted;
  it was not repopulated.
- **Mobile reads 0.0007 against desktop's 0.0034 â€” a factor of five at one stand, on one build.**
  The portrait frame is narrower and closer to the ground plane, and 103 flower-hued pixels of
  151,309 is a small numerator. Do not read the two viewports against each other here.
- **No literal black at either viewport**, against 12,063 pixels at `river_bank` and 11,015 at
  `first_post_office` in the 2026-08-14 table. The darkest decile is L 9.34â€“10.3, still under the Â§5
  floor of L â‰¥ 14, and R-W1 still owns it.
- **The town is 12.3 % of what breaks this skyline on desktop and 5.1 % on mobile.** The rest is
  timber. That is the R-W4a subtraction doing its job at a stand where the horizon is mostly the
  north and west sides of the block and the town beyond them.

**The repeat, and it is a stronger reading than the one that was planned.** `--stability` did not
finish inside the run's ten-minute-per-command ceiling, so the harness's own repeat contract was not
exercised. What replaced it is better evidence for the same question: the pair of frames was shot
TWICE, in two separate browser processes, **half an hour and five sibling merges apart** â€” the
second round after this branch was replayed onto a `dev` carrying T-0227's AO work â€” and all four
frames are **byte-identical**, `b08cedcd3653â€¦` desktop and `875e290b2dd1â€¦` mobile both times, with
every metric repeating exactly. So 2/2 at both viewports across processes, which is what the
2026-08-14 table reports for its eleven, and the run's own churn is the control. It does not assert
the â‰¤ 1 % metric-drift half of the contract by the harness's own instrument; that is the part still
owed.

**The rig now stands at fourteen stations** â€” ten scene anchors and four poses â€” against the eleven
the 2026-08-14 table records.

**Verified.** `tools/check.sh` (PASS) â€” which is the dev gate in full, per `docs/PIPELINE.md`.
`node tools/critic_shots.mjs --stations public_square --metrics` at both viewports on the source
tree, and `--published --stations public_square` at both viewports on the mirror this PR writes:
the station resolves, the declared pitch is met and `page_errors` is empty in all four. The
unfiltered `tools/smoke_renderer.mjs` was NOT run â€” it takes about 55 minutes on this runner
(T-0235) against a run ceiling of ten minutes per command, and it was started and killed at that
ceiling rather than quietly skipped. Nothing under `renderers/`, `generators/`, `data/` or
`assets/` is touched by this change; the diff is one tool, this file, the changelog and the
publish mirror's copy of it.

## Shipped 2026-08-28 â€” T-0227: the AO bake is too dark, and now something has actually looked at it

**Nothing in the town moved.** This run answers a question the project has been holding an opinion
about for months without ever having read a rendered frame that carried the thing it was judging.

**The question, and why it was open.** `bake_ao()` has said since it was written that AO on these
archetypes is a geometry problem, and quoted "mean 0.265 with 69 % of texels below half" plus "0.38
at a 0.25 m AO distance". T-0158 voided both â€” read off an sRGB-tagged buffer, and averaged over a
512Â² atlas **68.9 % of which is empty UV space**, so the 69 % was very nearly the empty fraction
itself. Worse than either fault: **until T-0158 the export shipped a uniformly black texture**, so
no AO judgement this project holds was ever made on a file that carried occlusion at all.

**What was done.** `sauganash_hotel` rebaked with `--ao` (baked mean 0.1665 â†’ exported 0.1665, 0.0 %
drift), swapped into the source tree, and shot at both Sauganash anchors and both viewports through
`tools/critic_shots.mjs --metrics` against the same tree without it. The new
`tools/measure_ao_frame.mjs` reads the building's **own visible pixels** out of those frames â€” the
structures mask (`full` vs the `__bare` capture) intersected with the pixels that moved between the
two conditions â€” so the reading is of the walls, not of the frame and not of the atlas.

| station | viewport | pixels read | mean L\* without â†’ with | L\* < 20 | literal black px |
|---|---|---|---|---|---|
| `sauganash` | desktop | 87,893 | **33.8 â†’ 11.1** | 31.1 % â†’ **88.9 %** | 0 â†’ **6,532** |
| `sauganash` | mobile | 20,010 | 33.4 â†’ 11.1 | 31.8 % â†’ 89.5 % | 0 â†’ 1,289 |
| `sauganash_wing` | desktop | 99,681 | 39.1 â†’ 17.9 | 15.4 % â†’ 64.9 % | 0 â†’ 3,781 |
| `sauganash_wing` | mobile | 17,511 | 41.9 â†’ 20.6 | 4.9 % â†’ 56.5 % | 0 â†’ 340 |

**The answer is yes, and the atlas statistic understated it.** A documented white-painted wall loses
two thirds of its lightness and puts thousands of pixels at literal 0,0,0 â€” a hole in the render,
not a shaded wall. The whole-frame critic table agrees from the other side (`literal black px`
0 â†’ 6,841, `shadow darkest decile L` 4.67 â†’ 2.00 at `sauganash` desktop), with triangles unchanged.
**"Mean 0.5358 over written texels" reads as about-half-occluded and sounds survivable; the frame
says the building goes out.** The mechanism is that glTF occlusion scales the INDIRECT term only,
and at the scene's 70.5Â° sun the street elevations a walker sees are carried by little else (Â§1
items 9â€“11) â€” occlusion near 1 there removes essentially all their light. So R-W3a keeps its cage
and loses its target: **acceptance is now a `measure_ao_frame.mjs` reading, not an atlas mean.**

**Two costs the cage parcel inherits, measured on the same asset.** The atlas is **31.1 % occupied**
(81,458 of 262,144 texels; the master 94,420 â†’ 202,292 bytes, +114 %), so two thirds of a ~107 KB
occlusion PNG is blank â€” **T-0286**. And `aoMap` is part of `materialKey` in `buildings.js`, so an
AO'd asset cannot batch with an un-AO'd one: **+2 draw calls at every station and both viewports for
one building**, against ceilings already breached â€” **T-0285**.

**What did NOT ship: the AO itself.** The bake stays off and `assets/manifest.json` keeps saying so.
Shipping an occlusion map that extinguishes a documented white wall would be a data-integrity bug in
an aesthetics costume, and the affordability questions above are R-W3a's to answer.

## Shipped 2026-08-28 â€” T-0211: the other nine group rows are cross-checked against something now

**The hole T-0032 left behind.** `data/reconstruction/1835_building_inventory.json` carries the same
662-roof aggregate three ways â€” 35 `family_targets`, a 10-group Ã— 4-division `district_group_matrix`,
and four `districts` totals â€” and the ledger asserted that all three sum to `roof_total` and that each
group's families sum to that group's row. **Nothing asserted anything about a group's split BY
DIVISION**, and the two views were authored independently. T-0032 (PR #388) found what that permits
in the `institutional_public` row and corrected that one row; the ticket it filed asks the same
question of the other nine.

**The answer is not "they are fine".** `tools/measure_group_district_rows.py` prints the full
ten-row Ã— four-division audit with the signed gap in every cell. Thirty-eight of the forty cells hold
roofs they have room for. Two do not, and both are in the North Division:

| group | division | row says | stands | over by |
|---|---|---|---|---|
| `warehouses_freight` | north | 1 | 7 | **6** |
| `institutional_public` | north | 3 | 4 | **1** |

Six of the seven North freight roofs are **documented pre-existing records** â€” Kinzie & Hunter's
warehouse, the four north-bank sheds at the Dearborn reach, the north-side brickyard â€” so the breach
is not an invention that can be removed. It is a row authored without the north bank's river-freight
fabric in view. The seventh is `recon_1835_north_f1_022`, dealt by a parcel that ran before anything
measured this. The institutional cell is a narrower thing: T-0032 set that row to the NAMED census and
`measure_institutional_claims.py` holds it there, while this counts every roof that stands â€” so the
two gates disagree by exactly `recon_1835_north_i2_015`, the one anonymous school **L93** records as a
liberty taken rather than deleted. Both readings are right for their own question.

**What the breach was costing, which nothing anywhere stated.** `reconcile_665.py` clamps the negative
away with `max(0, matrix[g][district] - built[(district, g)])`, so a row wrong by six roofs read
exactly like a row that is right. The clamp does not merely hide it â€” it re-spends it. The division's
ten clamped heads then sum to **more** than its own remainder, by exactly the overshoot, and an
unnamed loop sheds the difference from whichever group has the most head. Measured: the North
Division's **seven** overshooting roofs are paid for, in full, out of its **ordinary dwellings**. The
programme document now says so, in `remaining.district_group_rows_overshot` and
`remaining.district_group_slots_shed`.

**What is asserted, and why it is the weaker claim.** The I3 repair does not generalise. An
institutional row can be held to a census because Chicago's public buildings are enumerable; dwellings,
stores and barns are not, so "the row equals what stands" is the WRONG assertion for the other nine â€”
a row 74 roofs above what stands is the programme working as intended. The gate asserts the two things
that are true regardless:

1. **the matrix adds up in BOTH directions** â€” each row's four cells to its own `total`, and each
   division's ten cells to its own `target`. Neither was asserted anywhere before this, and the second
   is what makes the shed an identity rather than a coincidence;
2. **every division over one of its group rows declares it**, at a declared size â€” a ratchet in the
   shape `measure_band_claims.py` uses. It may fall, it may not rise, a new breach fails, and a
   declaration that outlives its breach fails too.

Neither cell is repairable by editing one number: the cells sum to their division's target *and* to
their group's total, so moving one moves four others and the 662-roof programme with them. That is a
decision about the authored target and it is filed as its own ticket. This run's job was to stop the
breach being invisible while it waits.

Verified: `tools/check.sh` (green, with the two new steps), `python3
tools/measure_group_district_rows.py --self-test` (8 cases, including the north half of the
apportionment T-0032 corrected, a grown breach, a healed one and a stale declaration). No renderer
file changed, so the frame is byte-identical.

## Shipped 2026-08-28 â€” T-0282: the shrub stratum joins the ceiling declaration, and a visitor can read it

**T-0019 declared the forb lattice's ceiling this morning and the declaration could not see half of
what it was declaring.** `flora.js` deals FOUR (stratum, side) lotteries through the same `shareOf`
against the same 0.34602 plants/mÂ² ceiling â€” forb dry, forb wet, shrub dry, shrub wet â€” and the
baseline listed forb layers only. `z06_dense_forest`'s shrub records ask **0.403 clumps per mÂ²**
against that ceiling and have been over it since **K54** named that community as the one whose shrub
density reaches the clamp. `shrubShareWet` and `shrubDensityWet` were not exported from `flora.js`
at all, so a quarter of the lattice was unreadable from outside it.

**The gate that exists to stop a layer joining the clamp in silence was itself silent about a
stratum.** It is ten layers of eighteen now, not nine of ten, and the identity of a declared line is
`(community, stratum, side)`. The gate was verified reading RED on the real tree before the
re-declare â€” `z06_dense_forest.shrub.dry is on the lattice ceiling and is NOT declared` â€” and green
after it. A declaration written before this carries no `stratum` and is read as `forb`, so the file
migrates on the next `--declare` instead of failing every line at once.

| layer | asks | draws | share of its own evidence |
|---|---|---|---|
| `z06_dense_forest` forb | 66.381 /mÂ² | 0.346 /mÂ² | **0.5 %** |
| `z04_marsh` forb, dry and wet | 22.000 /mÂ² | 0.346 /mÂ² | **1.6 %** |
| `z10_settled_town` forb | 11.866 /mÂ² | 0.346 /mÂ² | **2.9 %** |
| `z05_riverbank_timber` forb | 3.851 /mÂ² | 0.346 /mÂ² | **9.0 %** |
| `z03_sedge_meadow` forb | 1.812 /mÂ² | 0.346 /mÂ² | **19.1 %** |
| `z08_lakeshore` forb | 0.630 /mÂ² | 0.346 /mÂ² | **54.9 %** |
| `z02_mesic_prairie` forb | 0.408 /mÂ² | 0.346 /mÂ² | **84.8 %** |
| `z01_wet_prairie` forb | 0.407 /mÂ² | 0.346 /mÂ² | **85.0 %** |
| **`z06_dense_forest` shrub** | **0.403 /mÂ²** | **0.346 /mÂ²** | **85.8 %** |

**The second half is the one a visitor gets, and it is why this was worth a run rather than a
follow-up line.** T-0019 put the debt in `tools/forb_clamp_baseline.json` and in this file â€” where a
reviewer reads, and nowhere a visitor does. T-0281, filed by that run, says it plainly: *a visitor
standing in the dense forest is looking at half a per cent of the flowers the research put there and
has no way to find that out.* **`docs/LIBERTIES.md` L201** now carries the table above, what is ours
in it (the number of slots) and what is not (every density in it, straight from `data/flora`), and
it compiles into `data/liberties.json` â€” so it stands in the Evidence panel's liberties list beside
the other two hundred. That is not T-0281's full "What grows here" section and does not close it;
it is the clamp reaching the register this project already ships to visitors.

**Nothing was raised and no plant moved.** K58's other two routes buy their plants in exactly the
two communities that carry the most geometry, and the scene-detail ceiling is breached at Lake and
Canal at both viewports today (T-0203, T-0218). The frame is identical.

Verified: `tools/check.sh`, `node tools/measure_sward_draw.mjs --gate` (both assertions PASS, and
the clamp assertion shown RED first), `node tools/smoke_renderer.mjs --published` across both
viewports.

## Shipped 2026-08-28 â€” T-0225: the sward's drawn reach is read at a coverage the screen door can hold

**The defect.** `tools/smoke_renderer.mjs` part 7 reports the sward's outer boundary by binning the
view into 16 bearings and taking, in each, "the furthest plant in this bearing that is actually
DRAWN". Drawn was `flora.fadeAt(...) > 0.02`. `fadeAt` is COVERAGE since T-0035 â€” the alpha the
fragment program resolves through an ordered 4x4 Bayer matrix â€” so the reading called a plant drawn
at two per cent of a screen door that has sixteen levels in it.

**What two per cent actually renders as.** `chiBayer4` returns `(v + 0.5)/16` over `v = 0..15` and
`vChiDither` slides that whole set of sixteen thresholds by a per-instance phase, so the pixels
surviving in a 4x4 tile number `floor(16F)` or `ceil(16F)` and nothing between. Below `F = 1/16`
that is 0 or 1, and **which of the two is decided by the instance's dither phase â€” a number no
reader this side of the GPU has.** At `F = 0.02` one phase in three keeps a single pixel of the
tile and the other two keep nothing at all. The boundary the gate reported was therefore very
nearly the radius at which the placer stopped placing, which the lattice inset already guarantees.

**Measured, with the new `tools/measure_sward_reach.mjs`** â€” the same station the gate finds, the
same 16 bins, a sweep of thresholds. The gap between the PLACED boundary and the 2 % reading is
**0.54 m at `full` (27.35 â†’ 26.81 m mean) and 0.56 m at `light` (12.52 â†’ 11.96 m)**. That is the
size of the thing the statistic was measuring.

**The threshold, and why it is not a taste.** `1/16` is the smallest value at which "drawn" stops
being a property of the instance's dither phase and becomes a property of its coverage: at or above
it every instance keeps at least one pixel in every 4x4 tile it covers, whatever phase it drew. It
is the screen door's own quantum.

**The bars are re-derived, not slackened.** They are stated against the PLACED boundary (`nominal`
Â± the slot's own `fringe`) while the statistic now reads the DRAWN one. The ramp is linear
(`flora.fadeOf`: `clamp01((outer - d) / band)`), so a slot reaches coverage `F` at `outer - F Ã—
band` and the two boundaries differ by exactly `band Ã— seen` â€” 0.44 m on the desktop's 7.0 m ramp,
0.10 m on the phone's 1.6 m one. That term is a property of the statistic, so it belongs in the
bar; leaving it out would fail a sward for being read more honestly. Nothing else about the bars
moved.

**What each viewport lands at, and both readings are printed by the check itself** (T-0187's `show`
flag exists for this):

| viewport | tune | nominal Â± fringe | reach at 6.25 % | at the old 2 % | bars (min / mean) |
|---|---|---|---|---|---|
| desktop 1280Ã—800 | `full` | 26.40 Â± 3.00 m | 25.00â€“28.00, mean **26.61** | 25.00â€“28.41, mean 26.81 | 21.76 / 24.46 |
| mobile 390Ã—780 | `light` | 12.40 Â± 1.60 m | 10.32â€“13.22, mean **11.96** | 10.32â€“13.22, mean 11.96 | 9.50 / 11.50 |

Both viewports clear both bars â€” the phone by 0.82 m on the minimum and 0.46 m on the mean, the
desktop by 3.24 m and 2.15 m. **No finding about the sward falls out of this**; had one, it would
have been its own ticket rather than a wider bar. On the phone the two readings are identical to
the centimetre, which is what a 1.6 m ramp and a 6.8 cm shell between the thresholds predicts.

**What it unblocks, and that is why an invisible run was taken.** T-0187 priced spreading the mid
and forb rings' OUTER edges by density â€” the repair T-0093 made at the near/mid boundary and T-0086
at the far band's â€” and took a different route because the boundary check preferred the dither: a
spread took the mean drawn reach to 9.64 m at `light` against a bar of 11.60 m with 0.29 m unspent.
Every figure in that argument was read at 0.02. The bar is off the scale now; whether a spread can
actually clear it is unknown and unmeasured, and **T-0277** is that work. The stale half of the
`TUNE` comment in `flora.js` says so rather than continuing to assert a price taken with a broken
instrument.

**Verification.** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile SMOKE_STAGE=7` green on both
boundary checks, on one inherited red (`every tree drawn stands at its own station`, 0 of 0
vertices across 0 merged meshes â€” T-0243, standing on `dev` since 2026-08-28T00:55 by
`tools/dev-smoke-state.mjs`). Desktop part 7 was **not** taken to completion: it overran the
ten-minute foreground ceiling on a runner at load 3.6 of 4 CPU, and `dev-smoke-state` records no
desktop part-7 pass on this runner on any tree. The desktop figures above are from
`measure_sward_reach.mjs` at the gate's own station with the gate's own arithmetic, which is what
the tool was written for.

## Shipped 2026-08-28 â€” T-0019 (K58): the forb lattice's ceiling is declared, and it binds NINE layers, not six

**The clamp, stated plainly.** `forbShareOf` in `renderers/web/js/flora.js` is
`min(1, density Ã— cellÂ² / perCell)`, and that `min` is a lattice ceiling of **one plant per slot**.
`TUNE.forb` is a 3.4 m cell dealt 4 times, so a slot stands for **2.89 mÂ²** and the lattice cannot
draw more than **0.346 flowering plants per mÂ²** whatever a community's records say. K58 opened on
that, and its acceptance offered two ways out: each clamped layer either FITS or its shortfall is
declared in the census gate. Fitting is not available â€” see the last section â€” so this run declares.

**K58's own count is superseded: it is nine of the ten populated forb layers, not six, and the
figures are bigger than the ones on record.** K58 counted six at the midpoints of the recorded
ranges. T-0034 moved the forb stratum onto the TOP of every range (L182), so the asked densities
are the upper bounds now, and the two prairies and the lakeshore joined the clamp:

| community | side | records ask | lattice offers | draws |
|---|---|---:|---:|---:|
| `z06_dense_forest` | dry | 66.381 /mÂ² | 0.346 | **0.5 %** |
| `z04_marsh` | dry | 22.000 | 0.346 | 1.6 % |
| `z04_marsh` | **wet** | 22.000 | 0.346 | 1.6 % |
| `z10_settled_town` | dry | 11.866 | 0.346 | 2.9 % |
| `z05_riverbank_timber` | dry | 3.851 | 0.346 | 9.0 % |
| `z03_sedge_meadow` | dry | 1.812 | 0.346 | 19.1 % |
| `z08_lakeshore` | dry | 0.630 | 0.346 | 54.9 % |
| `z02_mesic_prairie` | dry | 0.408 | 0.346 | 84.8 % |
| `z01_wet_prairie` | dry | 0.407 | 0.346 | 85.0 % |
| `z09_sand_prairie` | dry | 0.114 | 0.114 | **100 % â€” the only one that fits** |

K58's midpoint figures for the same layers were 44.545 (`z06`), 14.5 (`z04`) and 7.760 (`z08`,
`z10`). **The marsh's WET side appears here for the first time**: `forbShareWet` is clamped exactly
as `forbShare` is, and the density behind it was not exported from `flora.js` until this run
(`communities().forbDensityWet`).

**Why nobody saw the drift.** A share reading `1.000` is one plant per slot whatever the slot is,
so a layer sitting ON the ceiling printed identically to one tuned below it, and the size of the
debt could only be recovered by re-deriving it from the records. Both movements happened under a
green tree: **K55 took the clamped count from four to six** by fixing a cover-fraction/count unit
error, and **T-0034 took it from six to nine** by dealing off the upper bound. Neither showed up
anywhere.

**The declaration and its gate.** `tools/forb_clamp_baseline.json` is the ledger: every
(community, side) the ceiling binds, the density its records ask for, and the share of that density
the lattice can carry. `node tools/measure_sward_draw.mjs --gate` now prints the whole table and
FAILS when the measured set stops matching the declaration â€” a layer joining the clamp, a layer
leaving it, the lattice ceiling moving, or an asked density moving more than half a per cent.
`--declare` rewrites the file from the measurement, so the figure is never re-typed off a console.

**The gate was shown reading red three ways before it was trusted**, which is this project's own
bar: with an empty declaration it named all nine undeclared layers; with `z04_marsh.wet` declared
at 18.0 against a measured 22.0 it called the declaration stale; with `z09_sand_prairie` declared
clamped when it is not it asked for the line to be withdrawn. Green with the committed file:
`9 clamped, 0 problem(s)`.

**What was NOT done, and it is a decision rather than an omission.** No ceiling constant moved.
`TUNE.forb.cell` and `TUNE.forb.perCell` are what they were. K58's routes out â€” a per-stratum cell,
more than one plant per slot where the record asks for it â€” all buy plants with geometry, and they
buy the most of it in `z06_dense_forest` and `z10_settled_town`, which are the two layers already
carrying the most. The `full` and `balanced` scene-detail ceilings are breached on `dev` as this is
written (T-0223, T-0229), so this is not the run to spend triangles on. The routes stay open and
they now have a number written against each of them.

## Shipped 2026-08-28 â€” T-0024: the face rule ranks dwellings, and the store steps onto the street line

**The question, and it has been open since 2026-08-15.** The face rule orders the DWELLINGS a
block parcel is dealt â€” the best take the better street, the meanest take the back one. T-A15 was
dealt the first STORE any block parcel had ever had to place, found the rule said nothing about
one, and EXTENDED the ranking to cover it: commerce above the better dwelling, on the reasoning
that a store-residence's claim on the better frontage is *"functional rather than social, the only
one of the six roofs whose purpose requires that a stranger can find it"*. It put the C2 on
Randolph, sent a D6 to the back street, and flagged its own extension as ROADMAP K32 for the next
block dealt a commercial family to follow or refute â€” the schedule still holds C1â€¦C4, F1â€¦F4, H3,
T1 and W1â€¦W5 for blocks not yet built, and a warehouse's claim on frontage is plainly not a
store's.

**Settled on reading 2 of the three the ROADMAP offered: the face rule ranks dwellings only, and a
non-dwelling is placed by its own function.** Reading 1 was to keep the ranking, reading 3 to
refuse the question and leave it to each parcel's arrangement note. Reading 2 is taken because it
is the only one of the three that can be READ OFF THE COMMITTED RECORD instead of argued.

**The reading.** Over the 48 documented buildings this project's own reconciliation credits a
non-dwelling family, by the traffic class `data/streets/1835.json` authors for the street each
stands nearest:

| letter | n | principal | ordinary | light |
|---|---|---|---|---|
| C stores | 15 | 10 | 5 | **0** |
| F warehouses | 9 | 9 | 0 | **0** |
| W workshops | 7 | 2 | 5 | **0** |
| T lodging | 8 | 3 | 4 | 1 |
| I institutions | 9 | 1 | 4 | 4 |

Not one documented store, warehouse or workshop stands on a light street â€” a zero across **31
buildings**, on the three letters a block parcel may actually be dealt. Lodging's one is the
Steamboat Hotel, 287 m from the State Street centreline, which does not front it; the institutional
families are refused to a block parcel BY NAME (L93) and no frontage rule reaches them. The second
reading is the setback: **every documented store standing on a platted street stands on its line**,
thirteen of the fifteen inside the measured street-line band, the two outside it being Robert
Kinzie's store at Wolf Point and the Miller house, both off the platted grid.

**The two clauses, authored in the recipe and refused at the generator.** (1) A non-dwelling takes
the block's better face by the committed street hierarchy, and a store, warehouse or workshop may
never take a light one. (2) A commercial roof stands ON the street line, at the closest line the
plat module's own margin allows â€” the same line the party-line runs on South Water and Lake already
stand on, rather than a second convention.

**What moved: ONE roof, and that is the finding rather than a convenience.** On `blk_randolph_clark`
reading 1 and reading 2 put the store on the same face, so the ranking could be refused without
re-dealing a block that already stands: no roof added or removed, no id, family, footprint or form
value changed, no household re-homed, no bake. What changed is the SETBACK â€” the C2 came forward
from 4.5 m to **1.50 m**, out of the 4.0â€“7.5 m band of house fronts it had been standing in. A
building whose whole argument was that a stranger must be able to find it had been placed as though
it were a cottage. One consequence follows it: the street-lining yard fence looks for a lot standing
back from its own frontage, a shop front is not one, and **24.6 m of fence comes off** that face.

**The 4.26 mm that was in the way, and it is named as what it is.** The per-lot margin gate compared
the distance from a footprint CORNER to the nearest point of the lot RING against the plat module's
1.5 m margin, while the setback a recipe authors is measured along the face normal. On a lot whose
side lines are not exactly square to its face the two differ by millimetres, so a roof authored to
stand exactly ON the margin read 1.4957 m and failed. It now carries the same 5 mm derivation
tolerance the party-line frontage gate two hundred lines above it already uses, for the same reason.
The margin is unchanged: 1.5 m is still the floor and a roof a centimetre inside it still fails.

**The gates.** `tools/generate_block_infill.py` refuses a slot that breaks either clause â€” a
light-street frontage, a face that is not the block's better one, or a commercial roof authored
behind the line â€” and `tools/measure_face_rule.py` holds the reading the clauses are taken from,
with two absolute assertions over the roofs the block parcels place and a `--self-test` that breaks
both in memory. Both run in `tools/check.sh`.

**What is reported and NOT asserted on.** The North, West and phase-one parcels ran before any of
this and place another 23 non-dwelling roofs. Seven are assigned to State Street at 150 to 550 m of
setback, which is not a frontage â€” it is the nearest committed centreline in a division with almost
no street control, and gating on those would be gating on the absence of a street. The real residual
is printed rather than fixed in passing: **two invented warehouses stand nearest Randolph at 12.9
and 14.5 m, against a documented F record that is 9 of 9 on principal streets.** Moving them is a
parcel's work on ground that is already built out, not a line in this one.

**Liberty L200.** Ticket **T-0024**, ROADMAP **K32**.

## Shipped 2026-08-28 â€” T-0025: the census that said three records were silent had read one field of a record that argues in four

**K35, opened by K34, asked what to do about three structures carrying AGENTS.md's standing
constraint with "no text anywhere in the record" saying what for. Two of the three were not
silent.** Read at K34's own commit (`23bb280b`), over the whole record rather than
`research_note`: `beaubien_barn` said it in `research_note`, `clybourn_slaughterhouse` said it in
`function.note` â€” *"flagged for review with the rest of this record's Indigenous content rather
than paraphrased away"*, in the same field that names Archibald Clybourne "the Government butcher
for the Pottawatomies" â€” and `council_house`, which K34 never named as a gap, said it in
`function.note` too. **Eight of the nine kept the convention, not six.** Only
`robert_kinzie_store` was bare.

This is not a scolding of K34; it is the reason the gate now reads what it reads. A building's
reasoning here is spread across `function.note`, `position.note`, the per-attribute notes and
`research_note`, and a policy sentence can honestly live in any of them.

**The one real gap is closed from the record's own attested business.** Andreas lists the store's
keeper among the town's Indian traders (scan p. 235) and among those licensed to sell goods (scan
p. 249); chicagology has it dealing in "groceries and Indian goods"; the record's `aka` carries
the source's own "R. A. Kinzie, Indian trader". The trade that names the building is the trade
the 1833 treaty ended, and the removal it ended in was under way six weeks after the scene date.
The paragraph states that and stops â€” no confidence moved, no source added, no liberty owed, and
the flag not lifted (lifting it is the claim that the consultation has happened, which assertion
5 already refuses).

**`tools/measure_review_constraint.py` gains assertion 6**, absolute, at every layer: a flagged
record must refer to the flag in one of the phrasings this dataset uses AND name the subject the
constraint is about, both in its own prose. Record-level, not sentence-level â€” `cobweb_castle`
opens "THE RECORD IS FLAGGED review_required BECAUSE OF WHAT THIS BUILDING WAS" and answers
itself over the next two sentences. **K35's objection to this route â€” "says something" is not
"says why" â€” stands, and the answer is that the census now PRINTS the sentence it matched under
every flagged id**, so what the gate cannot judge is at least in front of a reader. Both halves
were broken in memory against the real dataset and both fire; the restored tree passes.

**What is NOT claimed.** No visitor sees anything new: a building held under the constraint still
says so nowhere on its card, and the flag reaches the browser only as a `scene-loader.js` console
line. That is **T-0268**, filed by this unit rather than folded into it. `tools/check.sh` green
(the full gate, including `--stale`, the sidecar recompile check and the changelog contract);
`SMOKE_VIEWPORT=mobile` and the desktop smoke as recorded in the PR. No renderer file, no
geometry, no coordinate, no bake.

## Shipped 2026-08-28 â€” T-0162: the sward census stands at a phone, and its first honest phone reading is red

`tools/measure_sward_draw.mjs` has carried a `SWARD_VIEWPORT=mobile` flag since T-0018, and its own
header said why it had to exist: *"the viewport decides the ring sizes and therefore how many slots a
station deals, so the census has to be answerable at both."* It was not answerable at both. The two
runs came back **identical, row for row** â€” T-0018 measured 7,844 slots either way â€” and nobody could
see why, because both numbers were real numbers taken from a real page.

**THE WINDOW IS NOT THE DEVICE, AND THE RING SIZES ARE CUT FROM THE DEVICE.** `flora.js` sizes every
ring off `mergeTune(lowSpec && detail === 'full' ? 'light' : detail)`, and `lowSpec` is
`controls/touch.js` `prefersTouch()` â€” `(pointer: coarse)`, or a touch point under a 900 px window.
`browser.newPage({ viewport })` sets the window and nothing else: Chromium then reports
`navigator.maxTouchPoints === 0` and a fine pointer, so a 390-px page resolved `full` exactly as the
1280-px one did. The flag reached the CSS and never reached the tune.

**What it stands at now**, copied from `tools/smoke_renderer.mjs`'s own mobile context rather than
invented here (`hasTouch`, `deviceScaleFactor: 2`, and `isMobile: false` with the comment that goes
with it), so the census and the gate stand in the same place:

```
  stand: desktop 1280x800, 0 touch point(s), pointer fine   â€” detail full,  sward tune full
         ring reach: near 7 m, mid 26.4 m, forb 25.4 m
  stand: MOBILE  390x780,  1 touch point(s), pointer COARSE â€” detail light, sward tune light
         ring reach: near 4 m, mid 12.4 m, forb 12.4 m
```

**And the two censuses now differ, which is the demonstration.** Same 29 station-rows, same published
mirror, one command apart:

| | desktop 1280Ã—800 | mobile 390Ã—780 |
|---|---:|---:|
| slots dealt | **7,973** | **2,672** |
| drawn | 6,090 | 2,152 |
| refused by the two filters | 23.6 % | 19.5 % |
| pooled B/Bnull | 0.64 | 1.08 |

**THE STAND IS PRINTED AND IT IS ASSERTED.** The acceptance clause was *"no measurement is left
claiming a viewport it did not stand at"*, so the run states the stand it reached â€” window, touch
points, pointer, detail level, tune, and every layer's ring reach â€” before its first figure, and
EXITS 2 rather than print a census under a heading it did not earn. The desktop stand is asserted the
same way and for the same reason: a runner that reported a coarse pointer would deal this tool a
phone's census while its header said 1280Ã—800.

**THE FIRST HONEST PHONE READING IS RED, ON ITS FIRST RUN.** `--gate` â€” the assertion that no list
may owe a species a whole slot and draw it nowhere in the scene â€” **passes at desktop (0 pairs over
7,153 slots) and FAILS at mobile (1 pair over 2,763 slots)**:
`z10_settled_town.forb.xanthium_strumarium`, common cocklebur, owed 1.49 of a slot by the settled
town's own cover records and drawn nowhere at a phone's ring sizes. That is not a regression this
branch caused â€” it is the reading nobody had ever taken â€” and it is **T-0266**, not a fix made in
passing.

**Filed by this run:** T-0266 (the phone census's own gate is red).
## Shipped 2026-08-28 â€” T-0138: the town's two brick chimneys become one

`generators/inferred_placeholder.py` painted its stacks `placeholder_chimney_brick` at
`#89503F` â€” `0.537, 0.314, 0.247` linear, roughness 0.88 â€” a literal written in that file and
read nowhere else. T-0008 gave the 112 brick stacks on the archetype buildings the sheet's
`CHIMNEY_BRICK` at `0.45, 0.23, 0.17`, roughness 0.85. **About 20 % apart in linear red, on
buildings standing on the same streets** â€” `docs/RESEARCH/materials.md` finding 5's complaint
(a generator with no shared palette) surviving the parcel meant to end it, and named as
deliberately left alone in `chimneys.md` Â§4.

**The literal loses, and not by a coin toss.** Nothing in this repository argues for `#89503F`:
no source record, no note, no tier. `CHIMNEY_BRICK` is `frame_tavern`'s committed `BRICK_RGBA`,
read off the Petford watercolour of the Sauganash (T-0092, **L154**) â€” the one coloured witness
to any Chicago chimney â€” generalised to the town's other framed stacks on Blodgett's North Side
brick-yard, spring 1833. An `inferred` value carrying a source beats an undocumented literal, so
the literal goes and **no new number enters the sheet**. `CHIMNEY_BRICK`'s own argument is
untouched.

**The generator asks the selector, not the row.** It now calls
`materials.chimney_finish("interior")`, which is what it actually builds: a box inside the
footprint depth rising through the roof, the framed house's masonry flue. Asked the question
rather than told the answer, a placeholder cannot drift from the archetypes again.

**A log dwelling's placeholder still gets brick, and that is the massing's fault.** Â§3's
stick-and-clay daub belongs to a stack standing OUTSIDE the gable; the placeholder puts every
stack inside the roof, so the daub would be the right fabric on the wrong silhouette. Left alone
with the reason written down rather than half-fixed.

### THE HALF OF THE TICKET THAT NO LONGER EXISTS, AND SAYING SO IS MOST OF THIS ENTRY

T-0138 was written on 2026-08-22 against **"90 committed masters"**, and asked for them, their
compressed derivatives and the banked passthrough set to be regenerated in the same commit
(K38, `--write-baseline`). That was the whole reason T-0008 did not smuggle the convergence in.
Re-measured on `dev` before anything was edited:

| measurement | reading |
|---|---|
| `python3 generators/inferred_placeholder.py --check` | `0 flagged placeholder GLBs; 230 superseded by a canonical bake` |
| manifest entries with `kind: placeholder` | **0** of 349 |
| committed GLBs under `assets/` containing `placeholder_chimney_brick` | **0** |

So no master moved, no derivative moved, the passthrough baseline did not need re-banking, and
**no building repaints â€” there is no before/after frame to take, because nothing renders this
material.** The acceptance asked for one and the honest answer is that the subject of the
photograph has been baked out from under the ticket. This is T-0126's shape exactly (materials.md
Â§7): the divergence is closed at the source so it cannot walk back in the day a record outruns
the bake and a placeholder is emitted again.

**What a visitor sees, and it is one sentence.** L168's Evidence card said *"the 90 inferred
placeholders keep their own `#89503F` brick"*. That sentence was false and it is on a card
anybody can open, so it now says what happened instead. Nothing in the 3-D scene changed.

**An invisible run, declared as one.** AGENTS.md's rule is that a run changes something a visitor
can see; this one changes a card and×­µçkh‘éì¶»§q«^u½İ¸Ì‘…É­•ÍĞ…±‰•‘¼¸Q¡”™¥àÍÑ…åÌ¥¸\ÄìÑ¡”µ•¡…¹¥Í´¹…µ•¥¸+
œÄ¥Ñ•´€Ü‘½•Ì¹½ĞÍÕÉÙ¥Ù”¸((¨¨È¸Q¡”¡½É¥é½¸µÑ¥µ‰•Èµ•ÑÉ¥Œ…¹¹½ĞÑ•±°„ÑÉ••±¥¹”™É½´„Ñ½İ¹Í…Á”°…¹Ñ¡”Ñ½İ¸©ÕÍĞµ½Ù•)¥Ğ¸¨¨Q¡”É•¥Á”½Õ¹ÑÌ„¡½É¥é½¸½±Õµ¸…ÌÑ¥µ‰•É•¥˜…¹äÁ¥á•°¥¸Ñ¡”‰…¹…‰½Ù”Ñ¡”±…¹½Í­ä)±¥¹”™…±±Ì€Ì±Õµ„‰•±½Ü°½È€ÌŠ"I…‰½Ù”°Ñ¡”Í­ä•áÑÉ…Á½±…Ñ•™É½´Ñ¡”€ÈÀÉ½İÌ½Ù•È¥Ğ¸…‰±”)•¹‰É•…­¥¹œÑ¡”Í­å±¥¹”Í…Ñ¥Í™¥•ÌÑ¡…Ğ…ÌÍÕÉ•±ä…Ì…¸½…¬¸I”µÉÕ¹¹¥¹œÑ¡”¡…É¹•ÍÌ½¸Ñ½‘…äÌ)‘•Ù€ƒŠPİ¥Ñ €¨©¹¼É•¹‘•É•È¡…¹”Í¥¹”Ñ¡”‰…Í•±¥¹”¨¨€¡¥Ğ‘¥™˜€´µÍÑ…Ğ€ÈàÉ‘å„¸¹!€´´)É•¹‘•É•ÉÌ½€¥Ì¡…¹•±½œ¹©Í€°€ĞÄ±¥¹•Ì°…¹¹½Ñ¡¥¹œ•±Í”¤ƒŠP¹¥¹”ÍÑ…Ñ¥½¹ÌÉ•ÁÉ½‘Õ”Ñ¡•¥ÈÑ¥µ‰•È)™¥ÕÉ•Ì…¹€¨©ÁÉ…¥É¥•}Í½ÕÑ¡€µ½Ù•Ì™É½´€À¸ÌØĞÑ¼€À¸ĞÌØ…±°€¼€À¸ÌĞÀÑ¼€À¸ĞĞÄ•¹ÑÉ”¨¨°„€ÈÀ€”)…¥¸¸]¡…Ğ¡…¹•‰•Ñİ••¸Ñ¡”Ñİ¼ÉÕ¹Ì¥Ì€Ää…¹½¹åµ½ÕÌÉ½½™Ì€¡PµÈ…¹PµÌ¤°…¹Ñ¡”™É…µ”)Í¡½İÌÑ¡•´èÑ¡”±•™ĞÑ¡¥É½˜ÁÉ…¥É¥•}Í½ÕÑ¡€ÌÍ­å±¥¹”¥ÌÉ•ä…‰±”•¹‘Ì¸€¨©Q¡”ƒ
œ€ÔÑ…É•Ğ½˜+Š&”€äÀ€”¡½É¥é½¸Ñ¥µ‰•È½Ù•É…”…¸Ñ¡•É•™½É”‰”Í…Ñ¥Í™¥•‰ä‰Õ¥±‘¥¹œÑ¡”Ñ½İ¸¨¨°İ¡¥ ¥Ì¹½Ğ)İ¡…Ğ¥Ñ•´€Ôİ…Ì•Ù•È…‰½ÕĞ¸Hµ\Ğ½İ¹ÌÑ¡”Ñ…É•Ğì¥Ğ¹••‘Ì„‘¥ÍÉ¥µ¥¹…Ñ½È°½È„Í•½¹µ•ÑÉ¥Œ)Ñ¡…Ğµ•…ÍÕÉ•Ì½¹±ä½±Õµ¹Ìİ¥Ñ ¹¼ÍÑÉÕÑÕÉ”¥¸Ñ¡•´°‰•™½É”¥ÑÌ…•ÁÑ…¹”¹Õµ‰•Èµ•…¹Ì)…¹åÑ¡¥¹œ¸((¨¨Ì¸1…¹”€È¥ÌÍÁ•¹‘¥¹œÑ¡”‘É…Üµ…±°‰Õ‘•Ğ™…ÍÑ•ÈÑ¡…¸±…¹”€Ä…¸É•½Ù•È¥Ğ¸¨¨€¨©IM=1Y(ÈÀÈØ´Àà´ÄÔ‰äHµ\Õ„ƒŠPÍ•”Ñ¡”Ñ½À½˜Ñ¡¥Ì™¥±”¸¨¨Q¡”€¬ÄÄİ…Ì€ÄÄ¹•Üµ…Ñ•É¥…°I=UAL°Ñ¡”É½İÑ )Ñ•É´¥Ì¹½Üé•É¼°…¹¹¼ÍÑ…Ñ¥½¸¥Ì½Ù•È‰Õ‘•Ğ…Ğ•¥Ñ¡•ÈÙ¥•İÁ½ÉĞ¸Q¡”É•…‘¥¹œ‰•±½Ü¥Ì­•ÁĞ…Ì)Ñ¡”µ•…ÍÕÉ•µ•¹ĞÑ¡…Ğ™½Õ¹¥Ğ¸M…µ”Ñİ¼ÉÕ¹Ì°)Í…µ”É•¹‘•É•È°€¬ÄäÍÑÉÕÑÕÉ”É•½É‘Ì€ ÈĞÈƒŠH€ÈØÄ°€¬Ü¸ä€”¤è()ğğÍ…Õ…¹…Í¡€ğÌ¹…Í¡}İ¥¹€ğ±…­•}µ…É­•Ñ€ğ™}Á½ÍÑ}½™™¥•€ğ™½É­Í€ğÉ••¹}ÑÉ••€ğÍ½ÕÑ¡}İ…Ñ•É€ğ™É½µ}…‰½Ù•€ğÁÉ…¥É¥•}Í½ÕÑ¡€ğÁÉ…¥É¥•}İ•ÍÑ€ğÉ¥Ù•É}‰…¹­€ğ)ğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ)ğ‘•Í­Ñ½À‰…Í•±¥¹”ğ€ØÔğ€ØØğ€Üàğ€ØØğ€àÜğ€äÄğ€àÔğ€ØÜğ€ÜÌğ€äÜğ€ÔØğ)ğ‘•Í­Ñ½ÀÑ½‘…äğ€ØÔğ€ÜÜğ€àäğ€ØØğ€äàğ€ÄÀÈğ€äØğ€ØÜğ€àĞğ€ÄÀàğ€ÔØğ)ğµ½‰¥±”‰…Í•±¥¹”ğ€ØÈğ€ØÌğ€ØØğ€ØÀğ€àÈğ€ààğ€àÌğ€ØÄğ€ÜÄğ€äĞğ€Ğäğ)ğµ½‰¥±”Ñ½‘…äğ€ØÈğ€ÜÈğ€ÜÜğ€ØÀğ€àÈğ€ääğ€äĞğ€ØÄğ€àÈğ€ÄÀÔğ€Ğäğ((¨©á…Ñ±ä€¬ÄÄ‘•Í­Ñ½À…ĞÍ•Ù•¸½˜•±•Ù•¸ÍÑ…Ñ¥½¹Ì…¹•á…Ñ±ä€À…ĞÑ¡”½Ñ¡•È™½ÕÈ¨¨ƒŠP…¹)ÑÉ¥…¹±•ÌÉ½Í”‰ä½¹±ä€ÈĞÓŠLÔØÈ°Í¼Ñ¡¥Ì¥ÌÁ•Èµ½‰©•Ğ½ÍĞ°¹½Ğ•½µ•ÑÉä¸MÑ…Ñ¥½¹Ì½Ù•ÈÑ¡”(¨«Š&€àÀ¨¨‰Õ‘•Ğ¼€¨¨ĞƒŠH€Ø¨¨½¸‘•Í­Ñ½À…¹€¨¨ĞƒŠH€Ô¨¨½¸µ½‰¥±”ìÑ¡”İ½ÉÍĞ½•Ì€äÜƒŠH€ÄÀà¸Q¡”)Õ¹¥™½Éµ¥Ñä¥ÌÑ¡”Á…ÉĞ¹½‰½‘ä¡…Ì•áÁ±…¥¹•è€¬ÄÄ…Ğ‰•…É¥¹Ì€ÄÔÃ
À…Á…ÉĞ°…¹€¬À…Ğ™É½µ}…‰½Ù•€°)İ¡¥ Í••ÌÑ¡”İ¡½±”Ñ½İ¸¸€¨©MÑÉ…¥¡Ğµ±¥¹”•áÑÉ…Á½±…Ñ¥½¸½¸Ñ¡”É•µ…¥¹¥¹œ€ĞÄĞÉ½½™Ì¥Ì…‰½ÕĞ(¬ÈĞÀ‘É…Ü…±±Ì¨¨……¥¹ÍĞ„‰Õ‘•Ğ½˜€àÀ¸Q¡…Ğ¥Ì¹½Ğ„É•…Í½¸Ñ¼Í±½Ü±…¹”€È‘½İ¸ƒŠPÑ¡”É½½™Ì)…É”Ñ¡”ÁÉ½‘ÕĞƒŠP‰ÕĞÑ¡”‰Õ‘•Ğ…¹¹½Ğ‰”µ•Ğ‰äÑÕ¹¥¹œ…™Ñ•ÈÑ¡”™…Ğ°…¹Hµ\ÔÍ¡½Õ±ÑÉ•…Ğ)‰…Ñ¡¥¹œ…Ì¥ÑÌ™¥ÉÍĞÅÕ•ÍÑ¥½¸É…Ñ¡•ÈÑ¡…¸¥ÑÌ±…ÍĞ¸Q¡”™É½µ}…‰½Ù•€é•É¼¥Ì„±•…èÍ½µ•Ñ¡¥¹œ)…±É•…‘ä‘É½ÁÌÑ¡•Í”½‰©•ÑÌ…Ğ‘¥ÍÑ…¹”¸((ŒŒŒ]¡…ĞÑ¡¥Ì‘½•Ì¹½Ğ‘¼()%Ğ¡…¹•Ì¹¼½‘”°µ½Ù•Ì¹¼‰Õ¥±‘¥¹œ…¹É”µµ•…ÍÕÉ•Ì¹¼É•™•É•¹”Á¡½Ñ½É…Á ¸Q¡”ƒ
œÔÑ…É•ÑÌ)Ñ¡…Ğİ•É”Í•Ğ™É½´Ñ¡”Õ¹½µµ¥ÑÑ•€ÈÀÈØ´Àà´ÄÀÍİ••ÀÍÑ¥±°¹••É”µ…¹¡½É¥¹œ‰äµ•…ÍÕÉ¥¹œ„)É•™•É•¹”Á±…Ñ”Ñ¡É½Õ Ñ½½±Ì½É¥Ñ¥}µ•ÑÉ¥Ì¹µ©Í€°İ¡¥ ¥ÌÍÑ¥±°„½¹”µ±¥¹”©½ˆ…¹¥ÌÍÑ¥±°)¹½Ğ‘½¹”¸¹„ÉÕ‰É¥ŒÍ½É”¥Ì½¹”É•…‘•ÈÌ©Õ‘•µ•¹Ğİ¥Ñ ¥ÑÌÉ•…Í½¹¥¹œ…ÑÑ…¡•ƒŠPÑ¡”™¥á•Ì)‰•±½Ü…É”Ñ¡”‘ÕÉ…‰±”¡…±˜°¹½ĞÑ¡”¹Õµ‰•È¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄĞƒŠPÑİ¼É½½™Ì½˜Ñ•¸¥Ù•¸…¸½ÕÁ…¹Ğ°…¹Ñ¡”ÉÕ±”Ñ¡…ĞÉ•™ÕÍ•Ñ¡”½Ñ¡•È•¥¡Ğ((¨©PµÉ ¸¨¨Q¡”Á…É•°İ…Ì•áÁ•Ñ•Ñ¼…ÉÕ”…‰½ÕĞÑ¡”Ñ½İ¸ÌÑÉ…‘”µ¥à¸]¡…Ğ¥Ğ™½Õ¹¥ÌÑ¡…Ğ„)‰±½¬Á…É•°ÁÕÑÌÑ•¸‘İ•±±¥¹Ì½¸Ñ¡”Á±…Ğ™…ÍÑ•ÈÑ¡…¸…¹äÍÕ …ÉÕµ•¹Ğ…¸µ½Ù”°Í¼Ñ¡”)ÅÕ•ÍÑ¥½¸Ñ¡…Ğµ…ÑÑ•É•İ…Ì€¨©İ¡¼¥Ì…±±½İ•Ñ¼ÍÑ…ÉĞ½¹”¨¨¸Q¡”½ÕÁ…Ñ¥½¸•¹ÍÕÌ¥Ì„±…¥´…‰½ÕĞ)¡¥…¼ƒŠP€Ì°ÈØÔÁ•½Á±”¥¸€Ìäà‘İ•±±¥¹Ì°…±¥‰É…Ñ•……¥¹ÍĞ¹‘É•…ÌÌ€ÄàÌÌÉ½ÍÑ•ÈƒŠP…¹„•¹ÍÕÌ)Ñ¡…ĞÉ½İÌ•Ù•ÉäÑ¥µ”Í½µ•‰½‘ä‘É…İÌ„½ÑÑ…”¥Ì„•¹ÍÕÌ™¥ÑÑ•Ñ¼Ñ¡”µ½‘•°¸Qİ¼½˜)‰±­}É…¹‘½±Á¡}İ•±±Í€ÌÑ•¸É½½™Ì…É”…‘½ÁÑ•¥¹Ñ¼Ñ¡”¥¹™•ÉÉ•µ¡½ÕÍ•¡½±±…å•ÈìÑ¡”½Ñ¡•È•¥¡Ğ)ÍÑ…ä…¹½¹åµ½ÕÌ½Õ¹ĞµÕ¹¥ÑÌ°İ¡¥ ¥Ìİ¡…ĞÑ¡•ä…±É•…‘äİ•É”¸((¨©Q¡”ÉÕ±”¹½Ü±¥Ù•Ì¥¸Ñ¡”¡½ÕÍ•¡½±ÁÉ½É…µµ”Ì½İ¸µ•Ñ¡½‘€±¥ÍĞ¨¨°İ¡•É”Ñ¡”¹•áĞÁ…É•°İ¥±°)É•…¥Ğ¸‰±½¬É½½˜µ…ä‰”…‘½ÁÑ•½¹±äİ¡•É”	=Q Ñ•ÍÑÌÁ…ÍÌèÑ¡”ÑÉ…‘”Ì½µµ¥ÑÑ•…ÉÕµ•¹Ğ)ÍÑ…Ñ•Ì¥¸¥ÑÌ½İ¸Ñ•áĞÑ¡…Ğ¥ÑÌ½Õ¹Ğ¥Ì„€¨©™±½½ÈÉ…Ñ¡•ÈÑ¡…¸„‰½Õ¹¨¨°…¹Ñ¡”É½½˜Ì™…µ¥±ä¥Ì)½¹”Ñ¡¥Ì±…å•È€¨©…±É•…‘ä¡½ÕÍ•ÌÑ¡…ĞÑÉ…‘”¥¸¨¨¸((´€¨©Qİ¼½˜Ñİ•¹Ñäµ¹¥¹”ÑÉ…‘•ÌÁ…ÍÌÑ¡”™¥ÉÍĞÑ•ÍĞ¨¨ƒŠPÑ¡”…ÉÁ•¹Ñ•È€ ¨‰Ñ¡”Í¡½À½Õ¹Ğ¥Ì„™±½½È(€Õ¹‘•ÈÑ¡”ÑÉ…‘”°¹½Ğ„µ•…ÍÕÉ”½˜¥Ğˆ¨¤…¹Ñ¡”±…‰½ÕÉ•È€ ¨‰ÍÑ¥±°„Íµ…±°™É…Ñ¥½¸½˜İ¡…Ğ€Ì°ÈØÔ(€Á•½Á±”¥µÁ±¥•Ìˆ¨¤¸Ù•ÉåÑ¡¥¹œ•±Í”ÍÑ…Ñ•Ì„•¥±¥¹œƒŠPÑ¡”Á±…ÍÑ•É•ÈÌ…¹Ñ¡”‘É½Ù•ÈÌÍ…ä€¨‰…¹(€¹¼µ½É”ˆ¨½ÕÑÉ¥¡ĞƒŠP½È¥Ì‰½Õ¹‘•‰ä„İ½É­Í¡½À½ÈÍÑ½É”™…µ¥±äÌÉ½½˜Ñ…É•Ğ¸Qİ¼…ÁÁ…É•¹Ğ(€™ÕÉÑ¡•Èµ…Ñ¡•Ì…É”„™…±Í”Á½Í¥Ñ¥Ù”İ½ÉÑ ¹…µ¥¹œè€©™±½½È¨…ÁÁ•…ÉÌ¥¸Ñ¡”±…Õ¹‘É•ÍÌ…¹(€‰½…É‘¥¹œµ¡½ÕÍ”µ­••Á•È•¹ÑÉ¥•Ì½¹±ä¥¹Í¥‘”Ñ¡”¹‘É•…ÌÅÕ½Ñ…Ñ¥½¸€¨‰İ¥Ñ Ñ¡”™±½½È½Ù•É•(€‰•Í¥‘•Ìˆ¨¸(´€¨©Q¡”Í•½¹Ñ•ÍĞ°µ•…ÍÕÉ•……¥¹ÍĞÑ¡”±…å•È…Ì¥ĞÍÑ…¹‘Ì°Á¥­ÌÑ¡”Í…µ”Ñİ¼™…µ¥±¥•Ì¸¨¨±°€à(€½˜Ñ¡”±…å•ÈÌ…‘½ÁÑ•±…‰½ÕÉ¥¹œ¡½ÕÍ•¡½±‘Ì±¥Ù”¥¸„Ä…¹€ä½˜¥ÑÌ€ÄÀ…ÉÁ•¹Ñ•ÉÌ¥¸„ÌƒŠP(€…¹„Ä±½œ…‰¥¸…¹„Ì½¹”µÉ½½´½ÑÑ…”…É”Ñİ¼½˜Ñ¡”Í•Ù•¸‘İ•±±¥¹ÌÑ¡¥Ì‰±½¬‘•…±Ì¸(€Q¡”Ñ•ÍÑÌİ•É”‘•É¥Ù•¥¹‘•Á•¹‘•¹Ñ±ä…¹…É••½¸Ñ¡”™¥ÉÍĞ‰±½¬Ñ¡•äİ•É”…ÁÁ±¥•Ñ¼°İ¡¥ (€¥ÌÑ¡”½¹±äÉ•…Í½¸Ñ¼ÑÉÕÍĞ•¥Ñ¡•È½˜Ñ¡•´¸(´€¨©!½ÕÍ•¡½±‘Ì€ÄÔÈƒŠH€ÄÔĞ°Á•ÉÍ½¹Ì€ÄààƒŠH€ÄäÀ°…‘½ÁÑ•…¹½¹åµ½ÕÌÉ½½™Ì€àÌƒŠH€àÔ°ÍÑ…¹‘¥¹œÉ½½™Ì(€Õ¹¡…¹•…Ğ€ÈÔÄ¸¨¨Q¡¥ÌÁ…É•°‰Õ¥±Ğ¹½Ñ¡¥¹œ°µ½Ù•¹½Ñ¡¥¹œ…¹É•É…‘•¹½Ñ¡¥¹œ¸Q¡”Ñİ¼(€É½½™ÌœÁÉ•Í•¹”°Á½Í¥Ñ¥½¸…¹™½½ÑÁÉ¥¹Ğ…É”•á…Ñ±ä…Ì¥¹Ù•¹Ñ•…™Ñ•ÈÑ¡”…‘½ÁÑ¥½¸…Ì‰•™½É”¥Ğì(€İ¡…ĞÑ¡•ä…¥¸¥Ì…¸…ÉÕ•½ÕÁ…¹Ğ¥¹ÍÑ•…½˜„‰±…¹¬¸I•½É‘•…Ì€¨©0äĞ¨¨¸(´€¨©Q¡” Ä…¹ È¡½ÕÍ•Ì…É”Ñ¡”É•™ÕÍ…°İ½ÉÑ ­••Á¥¹œ¸¨¨Q¡”Í¡•‘Õ±”…±±½İÌ€Äà±…É•È¡½ÕÍ•Ì…¹(€€ÄĞµ•É¡…¹Ğ½ÈÁÉ½™•ÍÍ¥½¹…°¡½ÕÍ•Ì¥¸Ñ¡”İ¡½±”Ñ½İ¸°…¹Ñ¡•¥È½ÕÁ…¹ÑÌ…É”Ñ¡”µ½ÍĞ±¥­•±ä(€Á•½Á±”¥¸Ñ¡¥Ì‘…Ñ…Í•ĞÑ¼‰”¹…µ•…‰±”¸%¹Ù•¹Ñ¥¹œ…¸…¹½¹åµ½ÕÌµ•É¡…¹Ğ¥¹Ñ¼½¹”İ½Õ±‰É•…¬Ñ¡”(€ÁÉ½É…µµ”Ì½İ¸ÉÕ±”¹•Ù•ÈÑ¼¥¹™•È„Á•ÉÍ½¸İ¡•É”„‘½Õµ•¹Ñ•½¹”¥Ì…Ù…¥±…‰±”¸Q¡½Í”Ñİ¼İ…¹Ğ(€Pµ$ÌÌÑÉ•…Ñµ•¹ĞƒŠP„É•…‘¥¹œ½˜Ñ¡”É•½ÉƒŠP…¹¹½Ğ„‘É…Ü™É½´„•¹ÍÕÌ¸(´€¨©Q¡”…‘½ÁÑ¥½¸¥Ì…ÕÑ¡½É•½¹”…¹…Ñ•¥¸‰½Ñ ‘¥É•Ñ¥½¹Ì¸¨¨Ñ½½±Ì½•¹•É…Ñ•}‰±½­}¥¹™¥±°¹Áå€(€¹½ÜÉ•…‘ÌÑ¡”¡½ÕÍ•¡½±±•‘•ÈÑ¡É½Õ Ñ½½±Ì½¥¹™•ÉÉ•‘}½ÕÁ…¹ä¹Áå€°•á…Ñ±ä…ÌÑ¡”Ñ¡É•”(€•…É±¥•È…¹½¹åµ½ÕÌÁ…É•±Ì‘¼°Í¼¹¼•¹•É…Ñ•É•½É¥Ì¡…¹µ•‘¥Ñ•…¹Ñ¡”‘É¥™Ğ¡•¬Ñ¡…Ğ(€µ…­•ÌÑ¡•Í”Á…É•±ÌÑÉÕÍÑİ½ÉÑ¡äÍÑ¥±°‰¥¹‘Ì¸¡½ÕÍ•¡½±Á½¥¹Ñ•…Ğ…¸…¹¥±±…ÉäÉ½½˜™…¥±Ì‰ä(€¹…µ”ƒŠP„å…É‰Õ¥±‘¥¹œÍ•ÉÙ•ÌÑ¡”±½Ğ¥ĞÍÑ…¹‘Ì‰•¡¥¹°…¹¹½‰½‘ä±¥Ù•Ì¥¸„ÁÉ¥ÙäƒŠP…¹„É½½˜(€Ñ¡”±•‘•È¹…µ•ÌÑ¡…Ğ¹¼É•¥Á”‰Õ¥±‘Ì™…¥±Ì‰ä¹…µ”¸€¨©Y•É¥™¥•‰ä‘½¥¹œ•… ¸¨¨(´€¨©]¡…Ğ¥Ğ¡ÕÉ¹•…¹‘¥¹½Ğ™¥à°É•½É‘•…ÌI=5@,ÈÀ¸¨¨‘‘¥¹œÑİ¼Á•½Á±”É•¹…µ•€¨¨ÈÔ½˜(€Ñ¡”€äĞ¨¨É•½¹ÍÑÉÕÑ•É•Í¥‘•¹ÑÌ¸Q¡”¥¹Ù•¹Ñ•µ¹…µ”…±±½…Ñ½È‘•…±Ì¹…µ•ÌÉ½Õ¹•… Á½½°‰ä(€¥¹‘•àİ¥Ñ¡¥¸„‰Õ­•Ğ°Í¼…¸¥¹Í•ÉÑ¥½¸Í¡¥™ÑÌ•Ù•Éå½¹”…™Ñ•È¥Ğ¸9¼É…‘”µ½Ù•…¹•Ù•Éä¹…µ”(€É”µ‘•É¥Ù•ÌÕ¹‘•È€´µ¡•­€°‰ÕĞÑ¡”•¹•É…Ñ½ÈÌ½İ¸‘½ÍÑÉ¥¹œÍ…åÌÑ¡”…ÍÍ¥¹µ•¹Ğ¥Ì„™Õ¹Ñ¥½¸(€½˜„Á•ÉÍ½¸Ì¥İ¡•¸¥Ğ¥Ì„™Õ¹Ñ¥½¸½˜Ñ¡”İ¡½±”Á½ÁÕ±…Ñ¥½¸ƒŠP…¹•Ù•Éä™ÕÑÕÉ”‰±½¬Á…É•°(€İ¥±°É•İÉ¥Ñ”„ÅÕ…ÉÑ•È½˜Ñ¡”Ñ½İ¸Ì¥¹Ù•¹Ñ•¹…µ•Ì…Ì„Í¥‘”•™™•ĞÕ¹Ñ¥°Ñ¡…Ğ¥Ì™¥á•¸((¨©…Ñ•Ìè¨¨Ñ½½±Ì½¡•¬¹Í¡€É••¸ì¹½‘”Ñ½½±Ì½Íµ½­•}É•¹‘•É•È¹µ©Í€É••¸…Ğ€ÌäÃ\ÜàÀ…¹€ÄÈàÃ\àÀÀ°)é•É¼Á…”•ÉÉ½ÉÌ°ÉÕ¸……¥¹ÍĞÑ¡”Í½ÕÉ”ÑÉ•”…¹……¥¸İ¥Ñ €´µÁÕ‰±¥Í¡•‘€¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄĞƒŠP„‰±½¬™¥±±•¥¸°…¹Ñ¡”Ñ…‰±”¹½Ñ¡¥¹œ¡…•Ù•ÈÉ•…((¨©PµÈ¸¨¨‰±­}É…¹‘½±Á¡}İ•±±Í€ƒŠPI…¹‘½±Á °1…M…±±”°]…Í¡¥¹Ñ½¸°]•±±ÌƒŠPÍÑ½½•µÁÑä…¹¹½Ü)…ÉÉ¥•Ì€¨©Ñ•¸…¹½¹åµ½ÕÌÉ½½™Ì¨¨èÍ•Ù•¸ÁÉ¥¹¥Á…°‰Õ¥±‘¥¹Ì½¸Í•Ù•¸½˜¥ÑÌ•¥¡Ğ±½ÑÌ°Ñ¡É•”å…É)‰Õ¥±‘¥¹Ì½™˜Ñ¡”…±±•ä°Ñ¼Ñ¡”™…µ¥±äµ¥àÑ¡”€ØØÔµÉ½½˜Í¡•‘Õ±”…ÁÁ½ÉÑ¥½¹•¥Ğ¸Q¡”Ñ½İ¸ÍÑ…¹‘Ì)…Ğ€¨¨ÈĞÈÉ½½™Ì½˜€ØØÔ¨¨ì€ĞÈÌÉ•µ…¥¸…¹€¨¨äÔ½˜Ñ¡½Í”¡…Ù”µ½‘•±±•É½Õ¹¨¨¸=¹”±½Ğ¥Ì±•™Ğ)‰…É”½¸ÁÕÉÁ½Í”°…¹İ¡¥ ±½Ğ¥Ì…É‰¥ÑÉ…ÉäƒŠPÉ•½É‘•…ÌÍÕ ¥¸€¨©0äÈ¨¨°İ¥Ñ Ñ¡”™É½¹Ñ…”)…ÉÕµ•¹Ğ€¡±…É•È¡½ÕÍ•ÌÑ¼I…¹‘½±Á °É½Õ¡•È‘İ•±±¥¹ÌÑ¼]…Í¡¥¹Ñ½¸¤İÉ¥ÑÑ•¸‘½İ¸Í¼¥Ğ…¸‰”)‘¥Í…É••İ¥Ñ ¸((¨©Q¡”Á…É•°…ÕÑ¡½ÉÌ¹¼½½É‘¥¹…Ñ•Ì°…¹Ñ¡…Ğ¥ÌÑ¡”‘ÕÉ…‰±”¡…±˜¸¨¨Q¡”Ñ¡É•”•…É±¥•È¥¹™¥±°)Á…É•±Ì•… ¡…¹µİÉ½Ñ”Ñ¡•¥È½İ¸•…ÍÑ¥¹Ì…¹¹½ÉÑ¡¥¹Ì°‰•…ÕÍ”Ñ¡”Á±…Ğµ½‘Õ±”‘¥¹½Ğ•á¥ÍĞ)İ¡•¸Ñ¡•äİ•É”İÉ¥ÑÑ•¸¸Ñ½½±Ì½•¹•É…Ñ•}‰±½­}¥¹™¥±°¹Áå€É•…‘Ì•Ù•Éäµ•ÑÉ”½™˜Ñ¡”½µµ¥ÑÑ•±½Ğ)Á½±å½¹Ì½˜Ñ¡”,ÜÉ¥èÑ¡”É•¥Á”Í…åÌİ¡¥ ™…µ¥±äÍÑ…¹‘Ì½¸İ¡¥ ±½Ğ°İ¡•Ñ¡•È¥Ğ™É½¹ÑÌÑ¡”)ÍÑÉ••Ğ½ÈÑ¡”…±±•ä°…¹¡½Ü™…È‰…¬¸Q¡”‘•™•Ğ±…ÍÌ,Ü•áÁ½Í•ƒŠPÍ•Ù•¸‰Õ¥±‘¥¹ÌÍÑ…¹‘¥¹œ¥¸)Ñ¡”µ¥‘‘±”½˜Ñ¡”É½…°ÁÕĞÑ¡•É”‰ä„É•¥Á”Ñ¡…Ğ¡…¹•Ù•È…Í­•İ¡•É”Ñ¡”É½…İ…ÌƒŠP¥Ì¹½Ü)É•Ñ¥É•‰ä½¹ÍÑÉÕÑ¥½¸É…Ñ¡•ÈÑ¡…¸‰ä„…Ñ”…Ñ¡¥¹œ¥Ğ…™Ñ•Éİ…É‘Ì¸Q¡”…Ñ”ÍÑ¥±°ÉÕ¹ÌèÑ¡”)•¹•É…Ñ½ÈÑ•ÍÑÌ•Ù•Éä™½½ÑÁÉ¥¹Ğ……¥¹ÍĞ¥ÑÌ½İ¸±½Ğ±¥¹•Ì°Ñ¡”Á±…ÑÑ•½ÉÉ¥‘½ÉÌ°•Ù•Éä½Ñ¡•È)™½½ÑÁÉ¥¹Ğ¥¸Ñ¡”‘…Ñ…Í•Ğ°Ñ¡”¡•¥¡Ñ™¥•±…¹Ñ¡”…É¡•ÑåÁ”°‰•™½É”¥ĞİÉ¥Ñ•Ì„™¥±”¸((¨©Ñ…‰±”Ñ¡¥ÌÁÉ½©•Ğ¡…‰••¸…ÉÉå¥¹œ…¹¹•Ù•ÈÉ•…‘¥¹œ¸¨¨™…µ¥±å}‰…¹‘Í}™Ñ€¥¸Ñ¡”‰Õ¥±‘¥¹œ)¥¹Ù•¹Ñ½Éä¡…Ì‰…¹‘Ì™½È€ÈÄ½˜Ñ¡”ÁÉ½É…µµ”Ì€ÌÔ™…µ¥±¥•Ì¸Q¡”½Ñ¡•È€ÄĞƒŠP€¨© Ä° È° Ì°Ğ°)PÄµPÌ°\Ô°Ì°Ğ°$Äµ$Ì°4Ä¨¨ƒŠP¡…¹½¹”°Í¼Ñ¡”•…É±¥•È•¹•É…Ñ½ÉÌ½Õ±½¹±ä‰Õ¥±Ñ¡”)™…µ¥±¥•ÌÍ½µ•‰½‘ä¡…Í•Á…É…Ñ•±äÉ•ÑåÁ•¥¹Ñ¼AåÑ¡½¸°İ¡¥±”Ñ¡”Í¡•‘Õ±”İ•¹Ğ½¸…ÁÁ½ÉÑ¥½¹¥¹œ Ä)…¹ ÈÑ¼‰±½­Ì¸€ÄàÌÕ}™…µ¥±å}…É¡•ÑåÁ•}É½ÍÍİ…±¬¹©Í½¹€¡…Ì¡•±Ñ¡”™½½ÑÁÉ¥¹Ğ‰…¹°ÍÑ½É•ä)½Õ¹Ğ°•…Ù”¡•¥¡Ğ…¹Á±…•¡½±‘•È…É¡•ÑåÁ”™½È€¨©…±°€ÌÔ¨¨Ñ¡”İ¡½±”Ñ¥µ”°…¹…É••Ìİ¥Ñ )™…µ¥±å}‰…¹‘Í}™Ñ€½¸•Ù•Éä½¹”½˜Ñ¡”€ÈÄÑ¡•äÍ¡…É”¸Q¡”•¹•É…Ñ½ÈÉ•…‘ÌÑ¡”É½ÍÍİ…±¬¸€¨© Ä…¹) ÈÍÑ…¹™½ÈÑ¡”™¥ÉÍĞÑ¥µ”¨¨°…¹¹¼‰…¹¥ÌÉ•ÑåÁ•…¹åİ¡•É”¸((¨©=¹”¹Õµ‰•Èİ…Ìµ½Ù•Ñ¼™¥Ğ…¸…É¡•ÑåÁ”°…¹¥Ğ¥ÌİÉ¥ÑÑ•¸‘½İ¸¸¨¨Q¡”ÌÁÉ¥ÙäÌ…ÕÑ¡½É•)•…Ù”‰…¹ÉÕ¹Ì€Ø´Ü™Ğ…¹¥ÑÌ‰½ÑÑ½´¥Ì‰•±½Üİ¡…ĞÑ¡”½ÕÑ‰Õ¥±‘¥¹œ…É¡•ÑåÁ”¹••‘ÌÑ¼…ÉÉä¥ÑÌ)½İ¸‘½½ÈÁ±ÕÌ„¡•…‘•ÈƒŠPÉ•™ÕÍ•‰ä¹…µ”…Ğ€Ä¸àäÄ´¸Q¡”Í…µÁ±”¥Ì¹½Ü‘É…İ¸™É½´Ñ¡”Á…ÉĞ½˜Ñ¡”)…ÕÑ¡½É•‰…¹Ñ¡”…É¡•ÑåÁ”…¸‰Õ¥±€ È¸ÀÜ´°‰•Í¥‘”Á¡…Í”½¹”ÌÁÉ¥Ù¥•Ì…Ğ€È¸ÀÔ¤°…¹„™…µ¥±ä)İ¡½Í”İ¡½±”‰…¹Í¥ÑÌÕ¹‘•ÈÑ¡…Ğ™±½½È™…¥±Ì±½Õ‘±äÉ…Ñ¡•ÈÑ¡…¸‰•¥¹œÅÕ¥•Ñ±äÉ…¥Í•½ÕĞ½˜¥ÑÌ)ÑåÁ½±½ä¸((¨©¹„½µµ…¹Ñ¡…ĞÅÕ¥•Ñ±ä‘•ÍÑÉ½å•„¹¥¡ĞÌ	±•¹‘•Èİ½É¬°™½Õ¹‰äÉÕ¹¹¥¹œ¥Ğ¸¨¨)•¹•É…Ñ½ÉÌ½¥¹™•ÉÉ•‘}Á±…•¡½±‘•È¹Áå€‰Õ¥±‘ÌÑ¡”™±…•Á±…•¡½±‘•Èµ…ÍÍ¥¹œ™½È„¹•Ü…¹½¹åµ½ÕÌ)É•½É¸%ÑÌ€´µ¡•­€Á…Ñ ¡…ÌÍÑ½½…Í¥‘”Í¥¹”€ÈÀÈØ´Àà´ÄÌ™½È…¹ä…ÍÍ•ĞÑ¡”…¹½¹¥…°‰…­”¡…Ì)ÍÕÁ•ÉÍ•‘•ƒŠP­¥¹è•¹•É…Ñ•‘€¥¸Ñ¡”µ…¹¥™•ÍĞƒŠP™½ÈÑ¡”ÍÑ…Ñ•É•…Í½¸Ñ¡…Ğ‘•µ…¹‘¥¹œÑ¡”)Á±…•¡½±‘•È‰åÑ•Ì‰…¬İ½Õ±™½É‰¥Ñ¡”ÕÁÉ…‘”Ñ¡”‰…­”•á¥ÍÑÌÑ¼Á•É™½É´¸€¨©%ÑÌ	U%1Á…Ñ ‘¥)¹½Ğ¸¨¨IÕ¸½¹”™½ÈÑ•¸¹•ÜÉ•½É‘Ì°¥Ğ…±Í¼É•İÉ½Ñ”Ñ¡”€ÄÈà…±É•…‘äµ‰…­•½¹•Ìè€ÄÄÌ-½˜)…¹½¹¥…°…É¡•ÑåÁ”•½µ•ÑÉä‘½İ¸Ñ¼„€Ğ¸ä-™±…•‰½à•… °İ¥Ñ Ñ¡•¥Èµ…¹¥™•ÍĞ•¹ÑÉ¥•Ì)ÍÑ…µÁ•‰…¬Ñ¼­¥¹èÁ±…•¡½±‘•É€Í¼¹½Ñ¡¥¹œ‘½İ¹ÍÑÉ•…´½Õ±Ñ•±°Ñ¡”‘¥™™•É•¹”¸%ĞÉ•ÁÉ½‘Õ•Ì)½¸„±•…¸‘•Ù€¡•­½ÕĞ°Í¼¥Ğ¥Ì¹½Ğ„±½…°…¥‘•¹Ğ¸((¨©Ù•Éä…Ñ”ÍÑ…å•É••¸Ñ¡É½Õ ¥Ğ¨¨°İ¡¥ ¥ÌÑ¡”Á…ÉĞİ½ÉÑ ­••Á¥¹œ¸Á±…•¡½±‘•ÈÑ¡…Ğ)µ…Ñ¡•Ì¥ÑÌÉ•½É¥ÌÁÉ•¥Í•±äİ¡…ĞÑ¡”…Ñ•Ì¡•¬™½È°Í¼€ÄÈà‰Õ¥±‘¥¹Ì½±±…ÁÍ¥¹œÑ¼‰½á•Ì¥Ì)„ÍÑ…Ñ”Ñ¡”İ¡½±”ÍÕ¥Ñ”É•…É‘Ì…Ì½ÉÉ•ĞƒŠP…¹Ñ¡”ÁÕ‰±¥Í¡•Íµ½­”Á…ÍÍ•……¥¹ÍĞ¥Ğ°€ÈÀĞ…¹(ÈÀÄ…ÍÍ•ÉÑ¥½¹Ì°‰•™½É”…¹å½¹”¹½Ñ¥•¸]¡…Ğ…Õ¡Ğ¥Ğİ…ÌÉ•…‘¥¹œ„¥ĞÍÑ…ÑÕÍ€Ñ¡…Ğ¡…€ĞØÄ)™¥±•Ì¥¸¥Ğİ¡•¸Ñ¡”Á…É•°Ñ½Õ¡•Ñ•¸¸Q¡”‰Õ¥±Á…Ñ ¹½Ü…Í­ÌÑ¡”Í…µ”ÅÕ•ÍÑ¥½¸Ñ¡”¡•¬Á…Ñ )…Í­Ì…¹É•Á½ÉÑÌ‰Õ¥±Ğ€ÄÀƒŠ˜€ÄÈàÍÕÁ•ÉÍ•‘•‰ä„…¹½¹¥…°‰…­•€ìÑ¡”…Íåµµ•ÑÉä‰•Ñİ••¸„¡•¬)…¹Ñ¡”‰Õ¥±¥Ğ¡•­Ìİ…ÌÑ¡”İ¡½±”‘•™•Ğ¸Q¡”™½ÕÈ…Ñ”ÉÕ¹Ì…‰½Ù”İ•É”Ñ¡•¸É”µÉÕ¸™É½´)ÍÉ…Ñ ……¥¹ÍĞÑ¡”É•ÍÑ½É•‰…­”¸((¨©]¡…Ğ‘¥9=PÍ¡¥À°ÍÑ…Ñ•Á±…¥¹±äèÑ¡”¡½ÕÍ•¡½±‘Ì¸¨¨PµÈ…ÌİÉ¥ÑÑ•¸…±Í¼…±±•™½È¡½ÕÍ•¡½±)É•½É‘Ì¸‘½ÁÑ¥¹œÑ¡•Í”Ñ•¸É½½™Ìµ•…¹ÌÉ•ÍÑ…Ñ¥¹œÑ¡”½ÕÁ…Ñ¥½¸•¹ÍÕÌƒŠPÑ¡”¡½ÕÍ•¡½±•¹•É…Ñ½È)…Ñ•ÌÑ¡”•¹ÍÕÌ…¹Ñ¡”¡½ÕÍ•¡½±‘Ì……¥¹ÍĞ•… ½Ñ¡•È¥¸‰½Ñ ‘¥É•Ñ¥½¹ÌƒŠP…¹Ñ¡…Ğ•¹ÍÕÌ¥Ì)Ñ¡”Á½ÁÕ±…Ñ¥½¸±…å•ÈÌİ•…­•ÍĞ©½¥¹Ğ°‘•É¥Ù•™É½´™¥Ù”¥¸µ‘…Ñ…Í•Ğ…±¥‰É…Ñ¥½¹ÌÉ…Ñ¡•ÈÑ¡…¸)¥Ñ•¸I”µ…ÉÕ¥¹œ¥Ğ…Ì„Í¥‘”•™™•Ğ½˜„‰±½¬Á…É•°İ½Õ±‰”•á…Ñ±äÑ¡”­¥¹½˜Í¥±•¹Ğ)É”µ‘•¥Í¥½¸Ñ¡¥ÌÁÉ½©•ĞÉ•™ÕÍ•Ì¸€¨©Q¡”Ñ•¸É½½™Ì…É”Õ¹½ÕÁ¥•¨¨°¹¼¡½ÕÍ•¡½±¹…µ•ÌÑ¡•´°…¹)Ñ¡”İ½É¬¥ÌÅÕ•Õ•…Ì€¨©I=5@PµÉ ¨¨¸9¼¡Õµ…¸™¥ÕÉ”¥Ì‘É…İ¸€¡0Ä¤°Õ¹¡…¹•¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄĞƒŠP€ÈÌÈÉ½½™ÌÍÑ…¹½˜€ØØÔ°…¹½¹±ä€ÄÀÔ½˜Ñ¡”É•ÍĞ¡…Ù”…¹åİ¡•É”Ñ¼¼((¨©PµÄ¸¨¨Q¡”€ØØÔµÉ½½˜ÁÉ½É…µµ”¡…Ì‰••¸ÍÕ‰ÑÉ…Ñ•™É½´™½ÈÑ¡”™¥ÉÍĞÑ¥µ”¸Q¡”Ñ…É•Ğİ…Ì)…ÕÑ¡½É•¥¸‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ}‰Õ¥±‘¥¹}¥¹Ù•¹Ñ½Éä¹©Í½¹€½¸€ÈÀÈØ´Àà´ÄÄ…¹¹•Ù•Èµ½Ù•)……¥¹ÍĞİ¡…Ğİ…Ì‰Õ¥±ĞìÑ¡”™…µ¥±äÉ½ÍÍİ…±¬ÍÑ¥±°…±±•€¨¨ØÄÜÉ½½™ÌÉ•µ…¥¹¥¹œ¨¨İ¡¥±”(¨¨ÈÌÈ¨¨İ•É”ÍÑ…¹‘¥¹œ°„™¥ÕÉ”İÉ½¹œ‰äµ½É”Ñ¡…¸„Ñ¡¥É½˜Ñ¡”ÁÉ½É…µµ”°…¹Ñ¡”¹•áĞ)‰±½¬Á…É•°İ…Ì½¥¹œÑ¼Í¡•‘Õ±”……¥¹ÍĞ¥Ğ¸Q¡”É•µ…¥¹‘•È¥Ì¹½ÜI%YƒŠP)Ñ½½±Ì½É•½¹¥±•|ØØÔ¹Áå€ƒŠH‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ|ØØÕ}É½½™}ÁÉ½É…µµ”¹©Í½¹€°É”µ‘•É¥Ù•‰ä)Ñ½½±Ì½¡•¬¹Í¡€±¥­”Ñ¡”Á±…ĞÉ¥…¹Ñ¡”±¥‰•ÉÑ¥•Ì¸±•‘•È…‰½ÕĞ„Ñ½İ¸Ñ¡…ĞÉ½İÌµ½ÍĞ)¹¥¡ÑÌ…¹¹½Ğ‰”„¹Õµ‰•ÈÍ½µ•‰½‘äÑåÁ•¸((¨¨ÈĞÈÉ•½É‘Ì…É”€ÈÌÈÁ¡åÍ¥…°É½½™Ì¸¨¨Qİ•±Ù”É•½É‘Ì…É”„‘É…İ‰É¥‘”°Ñ¡É•”‰É¥‘•Ì°Ñİ¼)Á¥•ÉÌ°„Á…±¥Í…‘”°„Á…É…‘”É½Õ¹°„…ÉÉ¥Í½¸…É‘•¸°…¸½Á•¸±¥Ù•ÍÑ½¬Á½Õ¹°„½ÕÉÑ¡½ÕÍ”)Ñ¡”ÁÉ½‘ÕÑ¥½¸¡É½¹½±½äÁÕÑÌ¥¸Ñ¡”…ÕÑÕµ¸…¹„¡½Ñ•°ÍÑ¥±°„½¹ÍÑÉÕÑ¥½¸Í¡•±°ƒŠPÑ¡”)Á¡åÍ¥…°µÉ½½˜)É•½¹¥±¥…Ñ¥½¸É•‘¥ÑÌÑ¡•´İ¥Ñ ¹¼É½½˜°İ¡¥ ¥Ìİ¡…Ğ¥Ğ¥Ì™½È¸=¹”É•½É¥ÌÑİ¼…‰¥¹Ì)…¹Ñ¡”±•‘•È½Õ¹ÑÌÑ¡”±½ÜÉ•…‘¥¹œ¸	ä‘¥ÍÑÉ¥Ğè€¨©M½ÕÑ €ÄÀÀ°]•ÍĞ€ĞÄ°9½ÉÑ €àÄ°½ÉĞ€ÄÀ¨¨)……¥¹ÍĞÑ…É•ÑÌ½˜€ÌÜÀ€¼€ÄÌÔ€¼€ÄÔÀ€¼€ÄÀ¸€¨¨ĞÌÌÉ•µ…¥¸¸¨¨((¨©Q¡”¹Õµ‰•ÈÑ¡…Ğ¡…¹•Ìİ¡…Ğ±…¹”€È‘½•Ì¥Ì€ÄÀÔ¸¨¨Q¡”Á±…Ğµ½‘Õ±”É•…¡•Ì€Ää‰±½­Ì)¡½±‘¥¹œ€ÄÔÈ±½ÑÌ¸ĞÑ¡”É•Ù¥•İ•Á¡…Í”´ÄÁ…É•°Ì½İ¸‘•¹Í¥ÑäƒŠP½¹”ÁÉ¥¹¥Á…°É½½˜Á•È±½Ğ°)…¹¥±±…Éä…ĞÑ¡”ÁÉ½É…µµ”Ì½İ¸€ÄÔĞèÔÄÄƒŠPÑ¡½Í”‰±½­Ì¡…Ù”€¨¨ÄÀÔÉ½½™Ì½˜¡•…‘É½½´¨¨°…¹)Í•Ù•¸½˜Ñ¡•´°Ñ¡”İ¡½±”1…­”MÑÉ••Ğ‰•±Ğ°…É”…±É•…‘ä…Ğ½È½Ù•È¥Ğ¸Q¡”½Ñ¡•È€¨¨ÌÈàÉ½½™Ì)¡…Ù”¹¼µ½‘•±±•É½Õ¹Ñ¼ÍÑ…¹½¸¨¨è€ÈÀ¥¸‰±­}Í½ÕÑ¡}İ…Ñ•É}µ…É­•Ñ€…¹)‰±­}Í½ÕÑ¡}İ…Ñ•É}±¥¹Ñ½¹€°İ¡¥ Ñ¡”Á±…Ğµ½‘Õ±”É•™ÕÍ•Ì‰•…ÕÍ”M½ÕÑ ]…Ñ•ÈÌ½µµ¥ÑÑ•)•¹ÑÉ•±¥¹”ÍÑ½ÁÌ€ÈĞ´…¹€àÜà´Í¡½ÉĞ½˜Ñ¡•´ì€ÌÔ¡•±‰äÑ¡”]•ÍĞÉ•¥Á”Ì½İ¸…Ñ”…Ğ±½…°)ƒŠ"HÜÀÀ´ì…¹€ÈÜÌ¥¸É½Õ¹İ¥Ñ ¹¼½µµ¥ÑÑ•ÍÑÉ••Ğ½¹ÑÉ½°…Ğ…±°ƒŠP•…ÍĞ½˜MÑ…Ñ”°Í½ÕÑ ½˜)]…Í¡¥¹Ñ½¸°İ•ÍĞ½˜±¥¹Ñ½¸°…¹Ñ¡”•¹Ñ¥É”9½ÉÑ ¥Ù¥Í¥½¸°İ¡¥ Ñ¡”É¥½Ù•ÉÌ‰ä¹½Ğ„)Í¥¹±”‰±½¬¸€¨©Q¡”€ØØÔµÉ½½˜ÁÉ½É…µµ”¥Ì½Ù•É…”µ‰½Õ¹°¹½ĞÉ•¥Á”µ‰½Õ¹¸¨¨1…¹”€È¡…Ì)É½Õ¡±äÑ•¸‰±½¬Á…É•±Ì¥¸¥Ğ‰•™½É”ƒ
œLäÍÑÉ••Ğ½¹ÑÉ½°…¹Ñ¡”Ñ•ÉÉ…¥¸•áÑ•¹Í¥½¹Ì…É”Ñ¡”)½¹±äÑ¡¥¹œ±•™ĞÑ¼‘¼¸((¨©M¥à™…µ¥±äÑ…É•ÑÌ…É”…±É•…‘ä•á••‘•°‰ä¹¥¹”É½½™Ì°…¹Ñ¡…Ğ¥ÌÉ•Á½ÉÑ•É…Ñ¡•ÈÑ¡…¸)¡¥‘‘•¸¸¨¨ÄÍÑ½É•Ì°$È…¹PÈ°\Ä°\Ğ…¹\Ô…±°…ÉÉäµ½É”É½½™ÌÑ¡…¸Ñ¡”€ÈÀÈØ´Àà´ÄÄÑ…É•Ğ)…±±½İÌ°•Ù•Éä½¹”½˜Ñ¡•´•Ù¥‘•¹”Ñ¡”É•Í•…É Á±…•…™Ñ•ÈÑ¡”Ñ…É•Ğİ…ÌİÉ¥ÑÑ•¸¸)‘½Õµ•¹Ñ•É½½˜¥Ì¹½ĞÉ•µ½Ù…‰±”°Í¼Ñ¡”¹¥¹”½µ”½ÕĞ½˜Ñ¡”¥¹Ù•¹Ñ•™…µ¥±äİ¥Ñ Ñ¡”µ½ÍĞ)Í±…¬€¡Ğ¤¸Q¡”Í…µ”ÉÕ±”ÉÕ¹Ì¥¹Í¥‘”•… ‘¥ÍÑÉ¥Ğ……¥¹ÍĞÑ¡”É½ÕÀµ…ÑÉ¥àƒŠP9½ÉÑ ¡½±‘Ì)Ñ¡É•”¥¹ÍÑ¥ÑÕÑ¥½¹…°É½½™Ì…¹Ñİ¼İ…É•¡½ÕÍ•Ìµ½É”Ñ¡…¸¥ÑÌÍ¡…É”°…±°½˜Ñ¡•´…ÑÑ•ÍÑ•¸((¨©]¡…ĞÑ¡¥Ì‘½•Ì¹½Ğ‘¼¸¨¨%Ğ‰Õ¥±‘Ì¹½Ñ¡¥¹œ…¹µ½Ù•Ì¹½Ñ¡¥¹œè•Ù•Éä½Õ¹Ğ¡•É”¥Ì„)™Õ¹Ñ¥½¸½˜É•½É‘ÌÑ¡…Ğİ•É”…±É•…‘ä½µµ¥ÑÑ•¸Q¡”Á•Èµ‰±½¬™…µ¥±äµ¥à¥Ì…¸)…ÁÁ½ÉÑ¥½¹µ•¹Ğ½˜Ñ¡”‘¥ÍÑÉ¥ĞÌÉ•µ…¥¹‘•È°¹½Ğ„±…¥´Ñ¡…Ğ…¹ä‰±½¬¡•±Ñ¡½Í”™…µ¥±¥•ÌƒŠP)¥Ğ•á¥ÍÑÌÍ¼Ñ¡”Í¡•‘Õ±”…‘‘ÌÕÀ°…¹Ñ¡”‰±½¬Á…É•±ÌÑ¡…Ğ½¹ÍÕµ”¥ĞÉ…‘”•Ù•ÉäÙ…±Õ”)Ñ¡•ä•µ¥Ğ…ĞÑ¡”¥¹Ù•¹Ñ•Ñ¥•È…ÌÑ¡•ä…±İ…åÌ¡…Ù”¸Qİ¼…ÕÑ¡½É•™¥±•Ìİ•É”½ÉÉ•Ñ•İ¡•É”)Ñ¡•äÍÑ…Ñ•Í½µ•Ñ¡¥¹œÕ¹ÑÉÕ”…‰½ÕĞİ¡…Ğ¡…Ì‰••¸‰Õ¥±ĞèÑ¡”]•ÍĞÁ…É•°ÌÍÑ…ÑÕÌ(¡É•Ù¥•İ•‘}É•¥Á•}¹½Ñ}É•¹‘•É•‘€°İ¡•¸€ÈÀ½˜¥ÑÌ€ÔÔÉ½½™ÌÍÑ…¹¤°Ñ¡”É½½˜É•½¹¥±¥…Ñ¥½¸Ì)ÍÑ…ÑÕÌ€¡Á±…¹¹•‘€°İ¡•¸¥Ğ¥Ì‘½¹”…¹Ñ¡¥Ì±•‘•ÈÉ•…‘Ì¥Ğ¤°Ñ¡”9½ÉÑ É•¥Á”Ì€‰É•µ…¥¹¥¹œ(äÀÉ½½™Ìˆ€ Øä…™Ñ•ÈÉ•½¹¥±¥…Ñ¥½¸¤°…¹Ñ¡”É½ÍÍİ…±¬ÌÍÕÁ•ÉÍ•‘•€ØÄÜ¸((ŒŒQ¡”É•¹‘•É¥¹œÁÉ½É…´¥Ì±¥Ù”°…¹½Ù•É¹¥¡Ğİ½É¬¹¼±½¹•ÈÍ¡¥ÁÌÑ¼ÁÉ½‘ÕÑ¥½¸((¨¨ÈÀÈØ´Àà´ÄĞ¸¨¨Qİ¼Ñ¡¥¹Ì¡…¹•½¸Ñ¡”½İ¹•ÈÌ¥¹ÍÑÉÕÑ¥½¸°…¹Ñ½•Ñ¡•ÈÑ¡•äÍ•Ğİ¡…Ğ)Ñ½¹¥¡ĞÌ±½½À‘½•Ì¸()‘½Ì½I9I%9¹µ‘€¥Ì€¨©Q%Y¨¨€¡É•Ù¥•İ•…¹µ•É•°AH€ŒÄÀØ¤¸Q¡”\ÑÉ…¬…¹Ñ¡”À)É¥Ñ¥Œ¡…É¹•ÍÌ…É”‰Õ¥±‘…‰±”¹½ÜìÑ¡” €¡İ…±¬µ¡‘€¤…¹8€¡¹…Ñ¥Ù”•¹¥¹”¤ÑÉ…­Ì…¹•Ù•Éä)É•µ…¥¹¥¹œ=]9H%M%=9€ÍÑ…ä…Ñ••á…Ñ±ä…ÌİÉ¥ÑÑ•¸¸Q¡”…ÁÁÉ½Ù•-Q`µM½™Ñİ…É”¥¹ÍÑ…±°)±…¹‘•½¸Ñ¡”‰…­”ÉÕ¹¹•È°İ¡¥ Õ¹‰±½­Ì\ÈÌÑ•áÑÕÉ•ÌƒŠP¹½Ñ”İ¡…Ğ¥Ğ™¥á•Ìè‰…­”¹Í¡€…Í­Ì)™½È€´µÑ•áÑÕÉ”µ½µÁÉ•ÍÌ­ÑàÉ€½¹±äİ¡•¸Ñ¡”­Ñá€‰¥¹…Éä¥ÌÁÉ•Í•¹Ğ°‰•…ÕÍ”±Ñ˜µÑÉ…¹Í™½É´)…‰½ÉÑÌÑ¡”€©İ¡½±”¨½ÁÑ¥µ¥é”İ¡•¸¥Ğ¥Ì…‰Í•¹Ğ°µ•Í¡½ÁĞ¥¹±Õ‘•¸()Q¡¥Ì…ÁÀ¥Ì¹½Ü½¸„€¨©Ñİ¼µÑ¥•È‘•Ù€ƒŠHµ…¥¹€Á¥Á•±¥¹”¨¨€¡‘½Ì½A%A1%9¹µ‘€¤°Ñ¡”Ñİ¼µÑ¥•È)™½É´½˜Ñ¡”™±••ĞÁ¥±½Ğ¥¸­•Ù¥¹É¡……Ì½©½‰ÑÉ…­•È¹Á½±•…Ğ¹±¥Ù•€¸MÑ•İ…ÉÁ…É•±Ì…¹Ñ¡”)¹¥¡Ñ±ä‰…­”‰É…¹ ½™˜‘•Ù€…¹AH¥¹Ñ¼‘•Ù€ìµ•É¥¹œÑ¡•É”ÁÕ‰±¥Í¡•Ì½¹±äÑ¡”¥¹Ñ•É…Ñ¥½¸)ÁÉ•Ù¥•Ü…Ğ€¨©€½ÕÍÑ½´½¡¥…¼¼Ñ½‘•Ø½İ…±¬¼ıå•…ÈôÄàÌÕ€¨¨ƒŠP¹½¥¹‘•à°‰…¹¹•Èµµ…É­•°)‰Õ¥±¹©Í½¹€É•Á½ÉÑ¥¹œÑ¥•Èè‘•Ù€¸€¨©AÉ½‘ÕÑ¥½¸µ½Ù•Ì½¹±äİ¡•¸Ñ¡”½İ¹•È‘¥ÍÁ…Ñ¡•Ì)¡¥…¼´ÑµÁÉ½µ½Ñ”µÑ¼µÁÉ½¹åµ±€¸¨¨AÉ½µ½Ñ¥½¸¥Ì…Ñ•ì‘•Á±½ä¥Ì¹½Ğ°…¹¹•Ù•Èİ¥±°‰”¸()Qİ¼‘•™•ÑÌ…É”É•½É‘•É…Ñ¡•ÈÑ¡…¸™¥á•°‰½Ñ Á¥¹¹•‰ä…Ñ•ÌÍ¼Ñ¡•ä…¹¹½ĞÉ½Üè(¨¨Üä½˜€ÜĞÈ°ÔàÄÑ•ÉÉ…¥¸Ù•ÉÑ¥•Ì™…”‘½İ¹İ…É¨¨€ À¸ÀÄÄ€”°¥Í½±…Ñ•°¹¼Ù¥Í¥‰±”…ÉÑ•™…ĞƒŠP)I=5@Pµ	UÈ°‘¥ÍÑ¥¹Ğ™É½´Ñ¡”‰±…¬İ•‘”Ñ¡…Ğİ…Ì™¥á•Ñ½‘…ä¤°…¹€¨©Ñ¡”É¥Ù•È•‘”)™±¥­•ÉÌİ¡•¸™±å¥¹œ¨¨€¡I=5@Hµ	UÄ°…±µ½ÍĞ•ÉÑ…¥¹±ä‘•ÁÑ µ‰Õ™™•È™¥¡Ñ¥¹œ‰•Ñİ••¸Ñ¡”)İ…Ñ•ÈÁ±…¹”…¹Ñ¡”É½Õ¹É½ÍÍ¥¹œ¥Ğ°½İ¹•‰äÑ¡”Hµ\ÔÁ…É•°¤¸€©Hµ	UÄİ…Ì±½Í•(ÈÀÈØ´Àà´ÄØƒŠPÑ¡”Õ•ÍÌ¥¸Ñ¡…ĞÍ•¹Ñ•¹”İ…ÌÉ¥¡Ğ…‰½ÕĞÑ¡”™¥¡Ğ…¹İÉ½¹œ…‰½ÕĞÑ¡”½İ¹•Èè)¥Ğİ…ÌÑ¡”…µ•É„Ì¹•…ÈÁ±…¹”°¹½ĞÑ¡”İ…Ñ•Èµ…Ñ•É¥…°¸M•”Ñ¡”Ñ½À½˜Ñ¡¥Ì™¥±”¸¨((ŒŒQ¡”Í•½¹‰±½¬É•Á•…Ñ•Ñ¡”Í¡…Á”°…¹É•™ÕÍ•½¹”½˜¥ÑÌÉ½½™Ì((¨¨ÈÀÈØ´Àà´ÄĞ¸¨¨‰±­}É…¹‘½±Á¡}‘•…É‰½É¹€ƒŠPÑ¡”•…ÍÑ•É¹µ½ÍĞ‰±½¬Ñ¡”Á±…Ğµ½‘Õ±”É•…¡•Ì½¸Ñ¡”)I…¹‘½±Á Ñ¥•ÈƒŠP…ÉÉ¥•Ì€¨©¹¥¹”½˜Ñ¡”Ñ•¸É½½™ÌÑ¡”Í¡•‘Õ±”‘•…±Ğ¥Ğ¨¨¸MÑ…¹‘¥¹œÉ½½™Ì(¨¨ÈĞÈƒŠH€ÈÔÄ¨¨°É•µ…¥¹¥¹œ€¨¨ĞÈÌƒŠH€ĞÄĞ¨¨°€àØ½˜Ñ¡•´½¸É½Õ¹Ñ¡”ÁÉ½©•Ğ¡…Ì½Ù•É…”™½È¸Q¡”)•½µ•ÑÉä¡…±˜½˜PµÌİ…Ì„É•¥Á”•¹ÑÉä…¹¹½Ñ¡¥¹œ•±Í”°İ¡¥ ¥Ì•á…Ñ±äİ¡…ĞPµÈÍ…¥¥Ğ)İ½Õ±‰”¸Q¡”Ñİ¼Ñ¡¥¹Ìİ½ÉÑ É•…‘¥¹œ…É”İ¡…ĞÑ¡”É•Á•…Ğ•áÁ½Í•¸((¨©Q¡”Ñ•¹Ñ É½½˜İ…Ì¥Ù¥Œ°…¹¥Ğ¥Ì‘•™•ÉÉ•É…Ñ¡•ÈÑ¡…¸‰Õ¥±Ğ¸¨¨$ÌÉ•Í½±Ù•ÌÑ¡É½Õ Ñ¡”)™½ÉÑ}ÍÑÉÕÑÕÉ•€Á±…•¡½±‘•È°…¹•Ù•Éä‰Õ¥±‘¥¹œ­¥¹Ñ¡…Ğ…É¡•ÑåÁ”½™™•ÉÌ¥Ì„…ÉÉ¥Í½¸İ½ÉƒŠP)ÅÕ…ÉÑ•ÉÌ°‰…ÉÉ…­Ì°‰±½­¡½ÕÍ”°µ……é¥¹”°Õ…É°ÍÕÑ±•È°…ÉÑ¥±±•Éä¸5…ÍÍ¥¹œ…¸…¹½¹åµ½ÕÌÑ½İ¸)¥Ù¥Œ‰Õ¥±‘¥¹œÑ¡É½Õ ¥Ğİ½Õ±¡…Ù”ÍÑ½½„…ÉÉ¥Í½¸‰Õ¥±‘¥¹œ€ÜÔÀ´™É½´Ñ¡”™½ÉĞ¸Q¡”É½ÍÍİ…±¬)¡……±É•…‘äİÉ¥ÑÑ•¸Ñ¡”½¹‘¥Ñ¥½¸½¸¥ÑÌ½İ¸•¹ÑÉäèÑ¡”™…µ¥±ä€¨‰ÍÁ…¹ÌÕ¹±¥­”™Õ¹Ñ¥½¹ÌìÑ¡•äµÕÍĞ)É•½¹¥±”Ñ¼¹…µ•ÁÕ‰±¥ŒÉ•½É‘Ì‰•™½É”Í•±•Ñ¥¹œ½¹ÍÑÉÕÑ¥½¸ˆ¨¸M¼Ñ¡”•¹•É…Ñ½È¹½ÜÉ•™ÕÍ•Ì)$Ä°$È…¹$Ì€¨©‰ä¹…µ”¨¨°ÅÕ½Ñ¥¹œÑ¡”½µµ¥ÑÑ•Í•¹Ñ•¹”•… É•™ÕÍ…°•¹™½É•Ì°…¹„É½½˜Ñ¡”)Í¡•‘Õ±”‘•…±Ğ‰ÕĞÑ¡”Á…É•°‘¥¹½Ğ‰Õ¥±µÕÍĞ‰”¹…µ•¥¸Ñ¡”É•¥Á”İ¥Ñ ¥ÑÌÉ•…Í½¹¥¹œƒŠP„)…Ñ”Ñ¡…Ğ‰¥Ñ•Ì¥¸‰½Ñ ‘¥É•Ñ¥½¹Ì°Í¼„™…µ¥±ä…¹¹½Ğ‰”ÅÕ¥•Ñ±ä‘É½ÁÁ•…¹„‘•™•ÉÉ…°…¹¹½Ğ)‰”ÕÍ•Ñ¼¡¥‘”½¹”¸Q¡”‘¥ÍÑ¥¹Ñ¥½¸‰•¥¹œ‘É…İ¸è…¸…¹½¹åµ½ÕÌ€©‘İ•±±¥¹œ¨¥Ì„½Õ¹ĞµÕ¹¥ĞÑ½İ…É)„‘½Õµ•¹Ñ•…É•…Ñ”ì…¸…¹½¹åµ½ÕÌ€©ÁÕ‰±¥Œ‰Õ¥±‘¥¹œ¨…ÍÍ•ÉÑÌÑ¡…Ğ…¸¥¹ÍÑ¥ÑÕÑ¥½¸ÍÑ½½¡•É”…¹)±•™Ğ¹¼É•½É°…¹Ñ¡¥ÌÑ½İ¸ÌÁÕ‰±¥Œ‰Õ¥±‘¥¹Ì…É”™•Ü•¹½Õ Ñ¼‰”±¥ÍÑ•¸€¨©=¹”…¹½¹åµ½ÕÌ$È)ÍÑ¥±°ÍÑ…¹‘Ì¥¸Ñ¡”9½ÉÑ ¥Ù¥Í¥½¸¨¨™É½´„Á…É•°İÉ¥ÑÑ•¸‰•™½É”…¹ä½˜Ñ¡¥Ì°µ…ÍÍ•…Ì„•¹•É¥Œ)™É…µ”‰±½¬ì¥Ğ¥ÌÉ•½É‘•¥¸0äÌÉ…Ñ¡•ÈÑ¡…¸É•µ½Ù•°…¹¥Ğ¥Ì¹½Ğ„ÁÉ••‘•¹ĞÑ¡…Ğ•áÑ•¹‘Ì¸)I=5@€¨©Pµ$Ì¨¨¹½Ü½İ¹ÌÑ¡”É•Í•…É Ñ¡”É•™ÕÍ…°¥Ìİ…¥Ñ¥¹œ½¸¸((¨©±…Ñ•¹Ğ‘•™•Ğ™É½´Ñ¡”™¥ÉÍĞ‰±½¬°…Õ¡Ğ‰äÑ¡”Í•½¹°½¸„Ñİ¼µ•¹Ñ¥µ•ÑÉ”µ…É¥¸¸¨¨)±½Ñ}™É…µ” ¥€¡½Í”„±½ĞÌ…±±•ä•‘”…ÌÑ¡”•‘”¹•…É•ÍĞÑ¡”…±±•äÌ9QI=%ƒŠPİ¡¥ Í¥ÑÌ…Ğ)Ñ¡”‰±½¬Ì•¹ÑÉ”°Í¼½¸…¸9±½ĞÑ¡”Í¥‘”±½Ğ±¥¹”ÉÕ¹¹¥¹œ‰…¬Ñ½İ…É¥Ğ¥Ì¹•…É±ä…Ì±½Í”)…ÌÑ¡”…±±•ä•‘”¸5•…ÍÕÉ•½¸Ñ¡¥Ì‰±½¬è€¨¨Ìà¸äÌ´……¥¹ÍĞ€Ìà¸äÔ´¨¨°…¹Ñİ¼½˜¥ÑÌ™½ÕÈ•¹)±½ÑÌÁ¥­•Ñ¡”Í¥‘”±¥¹”°™É…µ¥¹œ„‰Õ¥±‘¥¹œ‰É½…‘Í¥‘”Ñ¼¥ÑÌ½İ¸ÍÑÉ••Ğ…¹½Ù•ÈÑ¡”)¹•¥¡‰½ÕÉ¥¹œ±½Ğ¸€¨©]¡…ĞÉ•Á½ÉÑ•¥Ğİ…ÌÑ¡”±½Ğµµ…É¥¸…Ñ”…Ğ€Ä¸ĞĞ´……¥¹ÍĞ„€Ä¸Ô´‰½Õ¹¨¨ƒŠP)„µ¥±±¥µ•ÑÉ”µÍ…±”½µÁ±…¥¹Ğ…‰½ÕĞ„¹¥¹•Ñäµ‘•É•”•ÉÉ½È°İ¡¥ ¥ÌÑ¡”Á…ÉĞÑ¼É•µ•µ‰•È¸5•…ÍÕÉ¥¹œ)Ñ¼Ñ¡”…±±•äÍÑÉ¥ÀÍ•Á…É…Ñ•ÌÑ¡”Í…µ”Ñİ¼•‘•Ì‰ä€À¸È´…¹€ÈØ¸Ì´°…¹„ÍÑÉÕÑÕÉ…°¡•¬¹½Ü)É¥‘•Ìİ¥Ñ ¥Ğ€¡™É½¹Ğ…¹É•…È…É”Ñ¡”Í…µ”±•¹Ñ Ñ¼İ¥Ñ¡¥¸Ñ¡”Á±…ĞÌÍ­•Üì„€ÈÀ€”‘¥Í…É••µ•¹Ğ)µ•…¹Ì½¹”¥Ì„Í¥‘”±¥¹”¤¸€¨©‰±­}É…¹‘½±Á¡}İ•±±Í€±•…É•Ñ¡”½±Ñ¥”‰ä€Ä¸Ì´¥¸€ÌÜ°Í¼¹½Ñ¡¥¹œ)PµÈ½µµ¥ÑÑ•µ½Ù•Ì¨¨ƒŠP¥Ğİ…Ì½¹”‰±½¬ÌÁÉ½Á½ÉÑ¥½¹Ì…İ…ä™É½´Ñ¡”Í…µ”™…¥±ÕÉ”°…¹¥Ğ¡…)‰••¸É••¸¸()Q½¹¥¡ĞÌ±½½À¥Ì•áÁ•Ñ•Ñ¼ÁÉ½‘Õ”€¨©½¹”Á…É•°Á•ÈÉÕ¸™É½´Ñİ¼±…¹•ÌÑ¡…Ğ…¹¹½Ğ)½±±¥‘”¨¨€¡‘½Ì½I=5@¹µ‘€ƒŠH€‰Q!=YI9%!P19Lˆ¤è±…¹”€ÄI9I%9Ñ½Õ¡•ÌÉ•¹‘•É•È…¹)Ñ½½°™¥±•Ì°±…¹”€ÈQ=]8=5A1Q%=8Ñ½Õ¡•Ì‘…Ñ„½¹±ä¸€¨©HµÀ¨¨€¡Ñ¡”É¥Ñ¥Œ¡…É¹•ÍÌ¤°€¨©PµÄ¨¨(¡Ñ¡”€ØØÔµÉ½½˜É•½¹¥±¥…Ñ¥½¸¤…¹Ñ¡”™¥ÉÍĞÑİ¼‰±½­Ì½™˜Ñ¡”É•½¹¥±•Í¡•‘Õ±”€ ¨©PµÈ¨¨°(¨©PµÌ¨¨¤…É”…±°¥¸°Í¼Ñ¡”9aPU@Á¥­Ì…É”€¨©Hµ\Ä¨¨€¡±¥¡Ğ¤…¹€¨©Hµ\Ğ¨¨€¡…Ñµ½ÍÁ¡•É”¤¥¸)±…¹”€Äì€¨©PµÓŠ˜¨¨€¡½¹”½Á•¸‰±½¬Á•ÈÉÕ¸°¹½Ü…‘½ÁÑ¥¹œ¥¸Ñ¡”Í…µ”ÉÕ¸¤…¹€¨©Pµ$Ì¨¨€¡Ñ¡”)¥Ù¥ŒÉ½½™ÌPµÌÉ•™ÕÍ•ƒŠPÉ•Í•…É °¹½Ğµ…ÍÍ¥¹œ¤¥¸±…¹”€È¸€¨©PµÉ ¨¨¥Ì¥¸Ñ½¼¸Q½‘…äÌ)½Õ¹Ğ¥Ì€¨¨ÈØÄÍÑÉÕÑÕÉ”É•½É‘ÌƒŠP€ÈÔÄÁ¡åÍ¥…°É½½™Ì½˜„€ØØÔÑ…É•ĞƒŠP€ÄÔĞ¡½ÕÍ•¡½±‘Ì°€ÄäÀ)Á•ÉÍ½¹Ì¨¨¸Ù•ÉåÑ¡¥¹œ…ÉÉ¥Ù•Ì…Ì„AH¥¹Ñ¼‘•Ù€…¹İ…¥ÑÌÑ¡•É”¸()!½¹•ÍĞÍÑ…Ñ”½˜Ñ¡”ÁÉ½©•Ğ¸Q¡¥¹ÌÑ¡…Ğ…É”Õ¹Ù•É¥™¥•ÍÑ…ä±…‰•±•Õ¹Ù•É¥™¥•ì„…Ñ”Ñ¡…Ğ)İ…ÌÍ­¥ÁÁ•¥ÌÉ•½É‘•…ÌÍ­¥ÁÁ•¸UÁ‘…Ñ•¥¸Ñ¡”Í…µ”½µµ¥Ğ…ÌÑ¡”İ½É¬¥Ğ‘•ÍÉ¥‰•Ì¸((¨©1…ÍĞÕÁ‘…Ñ•è¨¨€ÈÀÈØ´Àà´ÄĞƒ
Ü€¨©A¡…Í”è¨¨LÀ°LÄ€¡‘…ÑÕ´¤°LÈµÁ…ÉÑ¥…°€¡Ñ•ÉÉ…¥¸€¬É¥Ù•È…ĞÑ¡”)™½É­Ì¤°LĞµÁ…ÉÑ¥…°€¡™É…µ•}Ñ…Ù•É¸°±½}‘İ•±±¥¹œ°‰É¥‘•}Ñ¥µ‰•È¤°LäµÁ…ÉÑ¥…°€¡‘…Ñ•Ù¥Í¥‰±”)ÍÑÉ••Ğ±…å•È¤°LÄÀµÁ…ÉÑ¥…°€ ØØÔµÉ½½˜±•‘•È€¬€ÄÀà…¹½¹åµ½ÕÌÉ½½™Ì¤…¹HÄ€¡É•¹‘•É•È¤)½µÁ±•Ñ”¸€¨©,Ä€¡¥¹™•ÉÉ•É•Í¥‘•¹ÑÌ¤½µÁ±•Ñ”Ñ¡É½Õ Á¡…Í”Ñİ¼ì,Ü€¡Ñ¡”Á±…ÑÑ•‰±½¬…¹±½Ğ)É¥¤½µÁ±•Ñ”Ñ¡É½Õ Á¡…Í”½¹”°…¹Á¡…Í”Ñİ¼ÌÁ±…•µ•¹Ğ…Ñ”¥Ì±½Í•ƒŠP•Ù•Éä•¹•É…Ñ•)Á±…•µ•¹Ğ¥¸Ñ¡”‘…Ñ…Í•Ğ¥Ì½ÕĞ½˜Ñ¡”Á±…ÑÑ•É½…‘İ…ä…¹…±°Ñ¡É•”•¹•É…Ñ½ÉÌ•¹™½É”¥Ğì),ä€¡¹…Ù¥…Ñ¥½¸U$¤½µÁ±•Ñ”¸¨¨((¨©ÕÉÉ•¹Ğ•áÁ…¹Í¥½¸è¨¨Ñ¡”€ÄàÌÔÍ•¹”É•Í½±Ù•Ì€¨¨ÈÈÈÍÑÉÕÑÕÉ”É•½É‘Ì¨¨°…¹€¨¨ÄÔÈ¡½ÕÍ•¡½±‘Ì€¼(ÄààÁ•ÉÍ½¹Ì¨¨ÍÑ…¹‰•¡¥¹Ñ¡•´€ ÜØ‘½Õµ•¹Ñ•°€ÈÀ‘•É¥Ù•°€äÈ¥¹™•ÉÉ•¤¸€ÄÀàÉ•½É‘Ì…É”Ñ…•)¥¹™•ÉÉ•‘}…¹½¹åµ½ÕÍ€…¹‘¥ÍÁ±…ä…Ì™±…•É•Ù¥•Üµ…ÍÍ¥¹Ìì€¨¨àÌ½˜Ñ¡½Í”¹½Ü¡…Ù”…¸…ÉÕ•)½ÕÁ…¹Ğ¨¨É…Ñ¡•ÈÑ¡…¸‰•¥¹œ…¹½¹åµ½ÕÌ½Õ¹ĞµÕ¹¥ÑÌ°…¹€ÄØÈÍÑÉÕÑÕÉ•Ì¹…µ”„¡½ÕÍ•¡½±½¸Ñ¡”)‰Õ¥±‘¥¹œ…É¸Q¡•ä‰•¥»ŠQÉ…Ñ¡•ÈÑ¡…¸½µÁ±•Ñ—ŠQÑ¡”½İ¹•ÈÍÁ•¥™¥…Ñ¥½¸Ì€ØØÔµÉ½½˜Ñ…É•Ğ¸á…Ğ)…¹½¹åµ½ÕÌÁÉ•Í•¹”°™½½ÑÁÉ¥¹Ğ…¹±½ĞÁ½Í¥Ñ¥½¸É•µ…¥¸½¹©•ÑÕÉ…°°…¹Ñ¡”…‘½ÁÑ¥½¸¡…¹•Ì¹½¹”)½˜Ñ¡…Ğèİ¡…Ğ¥Ğ…‘‘Ì¥Ì„É•…Í½¸™½ÈÑ¡”É½½˜°¹½Ğ•Ù¥‘•¹”™½È¥Ğ¸€¨©9¼¥¹™•ÉÉ•Á•ÉÍ½¸¡…Ì„)¹…µ”°…¹¹½¹”Í¡½Õ±¨¨ì¹¼™¥ÕÉ”¥Ì‘É…İ¸€¡0Ä¤¸Q¡”É•µ…¥¹¥¹œ9½ÉÑ •áÁ…¹Í¥½¸¥ÌÍÑ¥±°…Ñ•)‰•¡¥¹Õ¹¥™¥•Ñ•ÉÉ…¥¸…¹¡å‘É½±½ä½Ù•É…”¸((¨©Q¡”İ•…­•ÍĞ©½¥¹Ğ¥¸Ñ¡”Á½ÁÕ±…Ñ¥½¸±…å•È°ÍÑ…Ñ•Á±…¥¹±äè¨¨¹¼Á•É¥½ÑÉ…‘”Ñ…‰±”™½È„)½µÁ…É…‰±”İ•ÍÑ•É¸Ñ½İ¸•á¥ÍÑÌ¥¸‘…Ñ„½Í½ÕÉ•Ì½€¸Ù•Éä½ÕÁ…Ñ¥½¸É…Ñ¥¼¥ÌÑ¡•É•™½É”‘•É¥Ù•)™É½´™¥Ù”¥¸µ‘…Ñ…Í•Ğ…±¥‰É…Ñ¥½¹ÌÉ…Ñ¡•ÈÑ¡…¸¥Ñ•°…¹Ñ¡”…É¥Ñ¡µ•Ñ¥Œ¥ÌİÉ¥ÑÑ•¸½ÕĞÁ•ÈÑÉ…‘”)¥¸‘½Ì½IMI ½É•Í¥‘•¹ÑÍ|ÄàÌÕ}¥¹™•ÉÉ•¹µ‘€¸Q¡…Ğ¥Ì„É•…°…À°¹½Ğ„É½Õ¹‘¥¹œ•ÉÉ½È¸((¨©]…Ñ•ÈÙ••Ñ…Ñ¥½¸½ÉÉ•Ñ¥½¸è¨¨•µ•É•¹ĞÁ±…¹ÑÌ¹½ÜÕÍ”ÑÉÕ”‘¥ÍÑ…¹”Ñ¼Í¡½É•±¥¹”…¹…É”)±¥µ¥Ñ•Ñ¼Ñ¡”Í¡…±±½Ü•¥¡Ğµµ•ÑÉ”µ…ÉÍ •‘”¸9½¸µ•µ•É•¹Ğ™±½É„…¹•Ù•Éäİ½½‘äÁ±…•µ•¹Ğ…É”)É•©•Ñ•½Ù•ÈÑ¡”ÑÉ…•İ…Ñ•Èµ…Í¬°…¹Í¥¹”€ÈÀÈØ´Àà´ÄÌÑ¡”µ¥ÉÉ½È½˜Ñ¡…ĞÉÕ±”¡½±‘ÌÑ½¼è„)ÍÁ•¥•Ìİ¡½Í”É•½É‘•ÍÕ‰ÍÑÉ…Ñ•€¥Ì½Á•¹}İ…Ñ•É€ƒŠP„Á…Ñ¡…Ğ™±½…ÑÌƒŠP¥ÌÉ•™ÕÍ••Ù•ÉäÍÑ…Ñ¥½¸)½¸‘ÉäÉ½Õ¹¸™¥ÉÍĞµÉÕ¸¹…Ù¥…Ñ¥½¸Õ¥‘”…¸‰”‘¥Íµ¥ÍÍ•…¹É•½Á•¹•)™É½´M•ÑÑ¥¹Ì¸((¨©A…É…±±•°Á¡…Í”µÑİ¼Á±…¹¹¥¹œè¨¨Ñ¡É•”¹½¸µÉ•¹‘•É•Á…É•°É•¥Á•Ì¹½Ü½Ù•È€àĞ…‘‘¥Ñ¥½¹…°M½ÕÑ )¥Ù¥Í¥½¸É½½™Ì€ ØØÁÉ¥¹¥Á…°°€Äà…¹¥±±…Éä¤°€ÔÔ]•ÍĞ¥Ù¥Í¥½¸É½½™Ì€ ĞĞÁÉ¥¹¥Á…°°€ÄÄ…¹¥±±…Éä¤)…¹€ØÀ9½ÉÑ ¥Ù¥Í¥½¸É½½™Ì€ ĞÔÁÉ¥¹¥Á…°°€ÄÔ…¹¥±±…Éä¤¸Q½•Ñ¡•Èİ¥Ñ Ñ¡”¥µÁ±•µ•¹Ñ•€ĞàÑ¡•ä)É•Í•ÉÙ”€ÈĞÜÍ±½ÑÌİ¥Ñ¡½ÕĞ•á••‘¥¹œ…¹ä€ØØÔµÉ½½˜™…µ¥±ä…À¸Q¡•äÉ•µ…¥¸Á±…¹Ì°¹½ĞÍ•¹”±…¥µÌè)Ñ¡”M½ÕÑ Í•Ğİ…¥ÑÌ™½ÈÁ¡åÍ¥…°µÉ½½˜É•½¹¥±¥…Ñ¥½¸ì€ÌÔ]•ÍĞÉ½½™Ì…±Í¼İ…¥Ğ™½È„Õ¹¥™¥•)İ•ÍÑİ…Éµ…À½Ñ•ÉÉ…¥¸•áÑ•¹Í¥½¸Ñ¼€´ÜÀÀ´°…¹Ñ¡”½ÕÑ•È9½ÉÑ Á…ÍÌİ…¥ÑÌ™½È8€¬ÜØÀ´½Ù•É…”¸(¨©5¥±•ÍÑ½¹”€ÀÍ¡¥ÁÁ•ì5¥±•ÍÑ½¹”€Ä€¡Ñ¡”™½É­Ì¤¥Ì¥¸¨¨ƒŠPÍ¥àÍÑÉÕÑÕÉ•ÌÁ±…•™É½´Ñ¡”)•½É•™•É•¹”°É•…°É½Õ¹°„ÑÉ…•É¥Ù•È°…¹Ñ¡”±¥‰•ÉÑ¥•Ì¹½ÜÉ•…‘…‰±”¥¹Í¥‘”Ñ¡”)İ…±­Ñ¡É½Õ É…Ñ¡•ÈÑ¡…¸½¹±ä¥¸Ñ¡”É•Á½Í¥Ñ½Éä¸€¨©M•Ù•¸ÍÑÉÕÑÕÉ•Ì¹½Ü°…¹Ñ¡”Í•Ù•¹Ñ ¥Ì)¹½Ğ„‰Õ¥±‘¥¹œ¨¨èÑ¡”9½ÉÑ 	É…¹ ‰É¥‘”¥ÌÑ¡”™¥ÉÍĞÉ•½É‰Õ¥±Ğ½¸Ñ¡”‰É¥‘•}Ñ¥µ‰•É€)…É¡•ÑåÁ”…¹Ñ¡”™¥ÉÍĞ¥¸Ñ¡¥Ì‘…Ñ…Í•Ğİ¡½Í”‘¥µ•¹Í¥½¹Ì½µ”™É½´•Ù¥‘•¹”É…Ñ¡•ÈÑ¡…¸™É½´)„Á±…•¡½±‘•È¸Ì½˜€ÈÀÈØ´Àà´ÄÀ¥ĞÍÑ…¹‘Ì½¸€¨©Ñİ¼‰•¹ÑÌÉ…Ñ¡•ÈÑ¡…¸™¥™Ñ••¸¥¹Ù•¹Ñ•É¥‰Ì¨¨(£
œ€ÈĞ¤ƒŠPÑ¡”™¥ÉÍĞÑ¥µ”„É•…‘¥¹œ½˜…¸…É¡¥Ù”¡…ÌÑ…­•¸Í½µ•Ñ¡¥¹œ€©½ÕĞ¨½˜Ñ¡¥Ìµ½‘•°¸(¨©¥¡ĞÍÑÉÕÑÕÉ•Ì¹½Ü°…¹Ñ¡”•¥¡Ñ ¥ÌÑ¡”™¥ÉÍĞ	U%1%9İ¡½Í”™½½ÑÁÉ¥¹Ğ¥Ì•Ù¥‘•¹”¨¨è)!½…¸ÌÍÑ½É”½¸1…­”MÑÉ••Ğ°İ¡•É”¡¥…¼ÌÁ½ÍĞ½™™¥”½Á•¹•¥¸€ÄàÌÄ°¥ÌÉ•½É‘•Ñİ¥”‰ä)¹‘É•…Ì…ÌÑİ•¹Ñä‰ä™½ÉÑäµ™¥Ù”™••Ğ€£
œ€ÈÔ¤¸%Ğ¥Ì…±Í¼Ñ¡”™¥ÉÍĞÉ•½É¡•É”İ¥Ñ ¹½Ñ¡¥¹œ)½¹©•ÑÕÉ…°¥¸¥Ğ°…¹Ñ¡”½ÉÉ•Ñ¥½¸Ñ¡…Ğ…µ”İ¥Ñ ¥Ğµ½Ù•Ñ¡”Á½ÍĞ½™™¥”Ì‘•Á…ÉÑÕÉ”™É½´)Ñ¡¥Ì‰Õ¥±‘¥¹œ‰äÑİ•¹Ñäµ½¹Ñ¡Ì¸((´´´((ŒŒQ¡”É¥Ñ¥Œ‰…Í•±¥¹”ƒŠP€ÈÀÈØ´Àà´ÄĞ((¨©I9I%9À¸Ä¥Ì¥¸…¹À¸ÈÌ¹Õµ•É¥Œ¡…±˜İ¥Ñ ¥Ğ¸¨¨Ñ½½±Ì½É¥Ñ¥}Í¡½ÑÌ¹µ©Í€ÍÑ…¹‘Ì…Ğ)•±•Ù•¸™¥á•ÍÑ…Ñ¥½¹ÌƒŠPÑ¡”•¥¡ĞÍ•¹”…¹¡½ÉÌ™É½´‘…Ñ„½Í•¹•Ì¼ÄàÌÔ¹©Í½¹€°‘É¥Ù•¸‰äÑ¡”)İ…±­Ñ¡É½Õ Ì½İ¸½Q½€Í¼Ñ¡”É¥œ…¹¹½Ğ‘É¥™Ğ™É½´Ñ¡”Ù¥•İÁ½¥¹ÑÌ„Ù¥Í¥Ñ½È¥Ì½™™•É•°)Á±ÕÌÑ¡É•”É”µ•ÍÑ…‰±¥Í¡•ÁÉ…¥É¥”µÍİ••ÀÍÑ…¹‘ÌƒŠP…Ğ‰½Ñ É•±•…Í”Ù¥•İÁ½ÉÑÌ°İ¥Ñ Ñ¡”…¹¥µ…Ñ¥½¸)±½¬¡•±™É½´‰•™½É”Ñ¡”É•¹‘•È±½½ÀÌÍ•½¹Ñ¥¬…¹Ñ¡”=4¡É½µ”¡¥‘‘•¸¸)Ñ½½±Ì½É¥Ñ¥}µ•ÑÉ¥Ì¹µ©Í€É•…‘ÌÑ¡”A9Ìİ¥Ñ ¹¼‘•Á•¹‘•¹¥•Ì…Ğ…±°°İ¡¥ µ•…¹ÌÑ¡”Í…µ”)½‘”…¸µ•…ÍÕÉ”„É•™•É•¹”Á¡½Ñ½É…Á …¹½¹”½˜½ÕÈ™É…µ•Ì¸€¨©Q¡…Ğ¡…Ì¹•Ù•È‰••¸ÑÉÕ”)¡•É”‰•™½É”¨¨°…¹¥Ğ¥ÌÑ¡”É•…Í½¸Ñ¡”¹Õµ‰•ÉÌ‰•±½Ü…É”İ½ÉÑ É•½É‘¥¹œ¸((¨©I•…Ñ¡•Í”…Ì„‰…Í•±¥¹”°¹½Ğ…Ì„Í½É•‰½…É¸¨¨½ÕÈÑ¡¥¹Ì¡…Ù”Ñ¼‰”Í…¥‰•™½É”Ñ¡”)Ñ…‰±•Ì°½ÈÑ¡•äİ¥±°‰”ÅÕ½Ñ•İÉ½¹±äè((Ä¸€¨©Q¡•ä…É”¹½Ğ½µÁ…É…‰±”Ñ¼Ñ¡”€ÈÀÈØ´Àà´ÄÀÁÉ…¥É¥”Íİ••ÀÌ™¥ÕÉ•Ì¸¨¨Q¡…Ğ¡…É¹•ÍÌİ…Ì(€€¹•Ù•È½µµ¥ÑÑ•…¹¹•¥Ñ¡•Èİ•É”¥ÑÌÍÑ…Ñ¥½¸½½É‘¥¹…Ñ•Ì°Í¼‰½Ñ Ñ¡”½‘”…¹Ñ¡”…µ•É„(€€Á½Í¥Ñ¥½¹Ì…É”¹•Ü¸]¡•É”„ƒ
œÔÑ…É•Ğİ…ÌÍ•Ğ™É½´Ñ¡”Íİ••ÀÌ¥µÁ±•µ•¹Ñ…Ñ¥½¸°Ñ¡”Ñ…É•Ğ(€€¹••‘ÌÉ”µ…¹¡½É¥¹œ‰äµ•…ÍÕÉ¥¹œ„É•™•É•¹”Á¡½Ñ½É…Á Ñ¡É½Õ Q!%L½‘”ƒŠPİ¡¥ ¥Ì¹½Ü„(€€½¹”µ±¥¹”©½ˆ…¹¥Ì¹½Ğå•Ğ‘½¹”¸(È¸€¨©Q¡”µ•…ÍÕÉ•µ•¹Ğ½¹Ù•¹Ñ¥½¹Ì…É”Ñ¡”¡…É¹•ÍÌÌ½İ¸¨¨…¹…É”ÍÑ…Ñ•¥¸Ñ¡”¡•…½˜(€€Ñ½½±Ì½É¥Ñ¥}µ•ÑÉ¥Ì¹µ©Í€èİ¡…Ğ½Õ¹ÑÌ…ÌÍ­ä°¡½ÜÑ¡”±…¹½Í­ä±¥¹”¥Ì™½Õ¹°Ñ¡”‰…¹(€€Ñ¡”¡½É¥é½¸Ñ¥µ‰•È¥Ì±½½­•™½È¥¸°…¹¡½Ü„É½İ¸Á¥á•°¥Ì¥‘•¹Ñ¥™¥•¸Q¡•ä…É”™¥á•Í¼(€€Ñ¡…ĞÑİ¼É½Õ¹‘Ì…É”½µÁ…É…‰±”ìÑ¡•ä…É”¹½Ğ±…¥µÌ…‰½ÕĞ€ÄàÌÔ¸(Ì¸€¨©±½İ•È±½…¥Ì½¹±äµ•…¹¥¹™Õ°…ĞÑ¡”½Á•¸µÁÉ…¥É¥”ÍÑ…Ñ¥½¹Ì¸¨¨%¸„™É…µ”İ¥Ñ ÍÑÉ••ÑÌ°(€€İ…±±Ì…¹É½½™Ì¥¸¥ĞÑ¡”‘•¹½µ¥¹…Ñ½È¥Ì¹½ĞÙ••Ñ…Ñ¥½¸¸(Ğ¸€¨©Q¡”É½İ¸µ•ÑÉ¥Ì¹••„É½İ¸¸¨¨™É½µ}…‰½Ù•€É•Á½ÉÑÌÑ¡•´‰•…ÕÍ”Ñ¡”¡…É¹•ÍÌÉ•Á½ÉÑÌ(€€•Ù•ÉåÑ¡¥¹œ°‰ÕĞ€Ä°ÄĞÈÉ½İ¸Á¥á•±Ì¥¸…¸…•É¥…°™É…µ”¥Ì¹½Ğ„…¹½Áäµ•…ÍÕÉ•µ•¹Ğ¸()	½Ñ ‰…Í•±¥¹”ÉÕ¹Ìİ•É”€¨¨ÄÄ¼ÄÄ‰åÑ”µ¥‘•¹Ñ¥…°‰•Ñİ••¸Ñİ¼Í•Á…É…Ñ”‰É½İÍ•ÈÁÉ½•ÍÍ•Ì¨¨…Ğ)‰½Ñ Ù¥•İÁ½ÉÑÌ°…¹•Ù•ÉäÍÑ…Ñ¥½¸ÌÁ¥Ñ µ…Ñ¡•¥ÑÌ‘•±…É…Ñ¥½¸¸((¨©‘•Í­Ñ½À€ÄÈàÃ\àÀÀ¨¨()ğÍÑ…Ñ¥½¸ğÑ¥µ‰•È…±°ğÑ¥µ‰•È•¹ÑÉ”ğÉ½İ¸™¥¹”ğÉ½İ¸Š"Iğ‘•¥±”0ğ±¥Ñ•É…°‰±…¬ÁàğI5L™…È½µ¥½¹•…Èğ™±½İ•È±½…ğ‘É…İÌ€¼ÑÉ¥…¹±•Ìğ)ğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ)ğÍ…Õ…¹…Í¡€ğ€À¸ØÌÜğ€À¸ØØØğ€À¸ÔÜäğ€ĞĞ¸äğ€Ô¸ÜØğ€Àğ€ÄÀ¸Ğ€¼€Ü¸Ô€¼€À¸àğ€À¸ÀÌÀÄğ€ØÔ€¼€ÌÌÈ°ĞÔÔğ)ğÍ…Õ…¹…Í¡}İ¥¹€ğ€À¸ĞäÌğ€À¸ĞÜÔğ€À¸ÔØØğ€ÄÜ¸Ğğ€Ä¸ÜÌğ€ØÄğ€ÄÄ¸à€¼€Ü¸À€¼€À¸äğ€À¸ÀÌàÌğ€ØØ€¼€ÌÜØ°ÔØÌğ)ğ±…­•}µ…É­•Ñ€ğ€À¸ÔÄàğ€À¸Ôààğ€À¸ÔÔÀğ€ÈĞ¸Øğ€Ìğ€Àğ€ÄÈ¸À€¼€Ô¸à€¼€Ä¸Äğ€À¸ÀÌÈÜğ€Üà€¼€ĞàĞ°ÔÔĞğ)ğ™¥ÉÍÑ}Á½ÍÑ}½™™¥•€ğ€À¸àĞÜğ€À¸äÌÜğ€À¸ÔÔÈğ€ÄÈ¸Èğ€Ô¸ÌÔğ€ÄÄÀÄÔğ€ä¸Ü€¼€à¸à€¼€ä¸äğ€À¸ÀÀÀĞğ€ØØ€¼€ÌäÌ°Øäàğ)ğ™½É­Í€ğ€À¸ÜÌäğ€À¸ÜàĞğ€À¸ÜÈÔğ€ÌÔ¸Äğ€ÈÔ¸Ôàğ€Àğ€ÄÀ¸À€¼€Ü¸Ä€¼€ÄÄ¸Ğğ€À¸ÀÀÄÌğ€àÜ€¼€ÔäØ°ØÄàğ)ğÉ••¹}ÑÉ••€ğ€À¸ÜÌÄğ€À¸ÜÌÔğ€À¸ØÜÀğ€ÈÀ¸Ìğ€ÌÀ¸ààğ€Àğ€ÄÈ¸ä€¼€Ô¸Ì€¼€À¸äğ€À¸ÀÀÄÜğ€äÄ€¼€ÔÔÌ°Ğäàğ)ğÍ½ÕÑ¡}İ…Ñ•É€€¨«Š€¨¨ğ€À¸ààäğ€À¸äÀÌğ€Ä¸ÀÀĞğ€ÈÜ¸Ğğ€È¸äÔğ€Àğ€ÄÜ¸À€¼€ÈØ¸Ü€¼€ÌÀ¸Äğ€À¸ÀÔÜÔğ€àÔ€¼€ÔÜÀ°ÜÄàğ)ğ™É½µ}…‰½Ù•€ğ€À¸ÈÄÈğ€À¸ÄàÀğ€À¸àÌÀğ€À¸Èğ€Èà¸ÈĞğ€Àğ€Ì¸à€¼€Ø¸Ü€¼€ä¸Üğ€À¸ÀÀÄäğ€ØÜ€¼€ĞÌÌ°ÀäÀğ)ğÁÉ…¥É¥•}Í½ÕÑ¡€ğ€À¸ÌØĞğ€À¸ÌĞÀğ€À¸ØàÈğ€ÈÜ¸àğ€Ì¸ÈÜğ€ÈÌÄÔğ€ÄĞ¸à€¼€Ô¸À€¼€à¸Üğ€À¸ÀÀÌÄğ€ÜÌ€¼€ÔÄÈ°ÀÄàğ)ğÁÉ…¥É¥•}İ•ÍÑ€ğ€À¸àÌÈğ€À¸àÔÀğ€À¸ØÈäğ€ÈĞ¸Äğ€ÄÌ¸ØÜğ€Àğ€ÄĞ¸Ğ€¼€ÈÄ¸à€¼€ÈÜ¸Üğ€À¸ÀÀÄÈğ€äÜ€¼€ØÄà°ØàØğ)ğÉ¥Ù•É}‰…¹­€ğ€À¸ØĞÄğ€À¸ÜÄäğ€À¸ÜĞÀğ€ĞÜ¸äğ€À¸äÌğ€ÄÈÀØÌğ€ÄÌ¸È€¼€ÈÌ¸ä€¼€Èä¸äğ€À¸ÀÀÈÈğ€ÔØ€¼€ÌÜÄ°ØäÄğ((¨©µ½‰¥±”€ÌäÃ\ÜàÀ¨¨()ğÍÑ…Ñ¥½¸ğÑ¥µ‰•È…±°ğÑ¥µ‰•È•¹ÑÉ”ğÉ½İ¸™¥¹”ğÉ½İ¸Š"Iğ‘•¥±”0ğ±¥Ñ•É…°‰±…¬ÁàğI5L™…È½µ¥½¹•…Èğ™±½İ•È±½…ğ‘É…İÌ€¼ÑÉ¥…¹±•Ìğ)ğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ´´µğ)ğÍ…Õ…¹…Í¡€ğ€À¸ÜÔØğ€À¸àÈÌğ€À¸ÔÜÈğ€ÈØ¸Ìğ€Ää¸Ğäğ€Àğ€ÄÌ¸Ô€¼€Ä¸Ø€¼€À¸Ìğ€À¸ÀÀĞÈğ€ØÈ€¼€ÌÌÀ°ÈàÌğ)ğÍ…Õ…¹…Í¡}İ¥¹€ğ€À¸ØØÜğ€À¸ÔäÈğ€À¸ØÈÔğ€ÈÈ¸Ôğ€Äà¸Üàğ€Àğ€ÄÌ¸Ğ€¼€Ä¸Ø€¼€À¸Ğğ€À¸ÀÀäÈğ€ØÌ€¼€ÌÈÌ°äĞØğ)ğ±…­•}µ…É­•Ñ€ğ€À¸ØäÜğ€À¸ÜÄäğ€À¸ÔäÜğ€ÄÔ¸äğ€ÄÔ¸ÈÄğ€Àğ€ÄÌ¸Ì€¼€È¸À€¼€À¸Ğğ€À¸ÀÄÜÜğ€ØØ€¼€ÌÜÜ°ÀÄÈğ)ğ™¥ÉÍÑ}Á½ÍÑ}½™™¥•€ğ€À¸äÄäğ€À¸äàäğ€À¸ÔĞÄğ€ÈÄ¸Äğ€Ô¸ÈØğ€ÄÜØÌğ€ÄĞ¸Ü€¼€ä¸Ğ€¼€À¸Ğğ€À¸ÀÀÀÄğ€ØÀ€¼€ÌàØ°ÔÌØğ)ğ™½É­Í€ğ€À¸ÜĞäğ€À¸ÜÌÄğ€Ä¸ÌÌÜğ€ÌÜ¸Ôğ€ÈÌ¸ĞÈğ€Àğ€ÄÄ¸Ø€¼€ÄÄ¸à€¼€ÄÀ¸Øğ€Àğ€àÈ€¼€ÔÜÌ°àĞÀğ)ğÉ••¹}ÑÉ••€ğ€À¸ÜØÜğ€À¸ÜĞØğ€À¸ÜĞÀğ€ÈÌ¸Øğ€Ìä¸ĞØğ€Àğ€Ø¸È€¼€Ä¸È€¼€À¸Ôğ€À¸ÀÀÀÈğ€àà€¼€ÔÌÜ°ØÔäğ)ğÍ½ÕÑ¡}İ…Ñ•É€€¨«Š€¨¨ğ€À¸àÌØğ€À¸àÄÄğ€À¸ÜÔÔğ€ÌÔ¸äğ€Ü¸ÔĞğ€Àğ€ÈĞ¸Ä€¼€ÌÌ¸ä€¼€ÈÔ¸Äğ€À¸ÀÄÈàğ€àÌ€¼€ÔÔÀ°ÀØÔğ)ğ™É½µ}…‰½Ù•€ğ€À¸ÄÔØğ€À¸ÄäÈğ€À¸ÜÜĞğ€Ğ¸Èğ€ÈÔ¸ÌÌğ€Àğ€Ø¸Ì€¼€ÄÄ¸ä€¼€ÄÀ¸Ôğ€À¸ÀÀÄÈğ€ØÄ€¼€ÌÜÜ°ÈÀÄğ)ğÁÉ…¥É¥•}Í½ÕÑ¡€ğ€À¸ĞØÜğ€À¸ĞäÈğ€À¸ØÄÈğ€ÌÀ¸àğ€ÄÌ¸ÜØğ€ÈØÜğ€ÄÀ¸Ì€¼€ÄÈ¸ä€¼€à¸Äğ€À¸ÀÀÄàğ€ÜÄ€¼€ĞÜØ°ÀÜĞğ)ğÁÉ…¥É¥•}İ•ÍÑ€ğ€À¸ØÜäğ€À¸ØäØğ€À¸ÜÜÈğ€ÈĞ¸Äğ€ÄÀ¸ØÔğ€Àğ€ÈÄ¸À€¼€ÌÀ¸à€¼€Ää¸Øğ€À¸ÀÀÀÌğ€äĞ€¼€ØÀÔ°ÌØØğ)ğÉ¥Ù•É}‰…¹­€ğ€À¸ÜÄÌğ€À¸ÜÜÌğ€À¸àÄĞğ€ĞÀ¸Ìğ€È¸ÜÜğ€ÈÄÔĞğ€ÈÄ¸ä€¼€ÌÌ¸È€¼€Ø¸Àğ€À¸ÀÀÀĞğ€Ğä€¼€ÌØÔ°ÌÔÌğ((¨«Š€Í½ÕÑ¡}İ…Ñ•É€¡•É”¥ÌÑ¡”IQ%IÍÑ…¹ƒŠP±½…°€ ÈØÀ°€´äÔ¥€°€‰M½ÕÑ ]…Ñ•ÈMÑÉ••Ğ°±½½­¥¹œ)•…ÍĞˆ°İ¡¥ ÍÑ½½€ÄÀÄ´Í½ÕÑ ½˜Ñ¡”•¹ÑÉ•±¥¹”½˜Ñ¡”ÍÑÉ••Ğ¥Ğ¥Ì¹…µ•™½È…¹™É…µ•„™¥•±¸¨¨)PµXÈ€ ŒÄÌÔ¤µ½Ù•Ñ¡”…¹¡½È½¸€ÈÀÈØ´Àà´ÄÔÑ¼€ ÌÈä¸à°€Ü¸À¥€°Ñ¡”]•±±ÌMÑÉ••Ğ½É¹•È°…¹•Ù•Éä)Í½ÕÑ¡}İ…Ñ•É€™¥ÕÉ”Í¡½Ğ™É½´€ÈÀÈØ´Àà´ÄØ½¹İ…É‘Ìµ•…ÍÕÉ•ÌÑ¡…ĞÍÑ…¹¥¹ÍÑ•…¸€¨©Q¡”Ñİ¼…É”¹½Ğ)½µÁ…É…‰±”…¹¹•¥Ñ¡•È¥Ì„½ÉÉ•Ñ¥½¸½˜Ñ¡”½Ñ¡•ÈƒŠPÑ¡•ä…É”Ñİ¼Á±…•Ì¸¨¨	½Ñ ÍÑ…¹‘Ìİ•É”)É”µÍ¡½Ğ½¸½¹”‰Õ¥±½¸€ÈÀÈØ´Àà´ÈÌÍ¼Ñ¡”µ½Ù”…¸‰”É•…Í•Á…É…Ñ•±ä™É½´Ñ¡”Ñ½İ¸ÌÉ½İÑ ìÍ•”(©I”µÍ¡½Ğ€ÈÀÈØ´Àà´ÈÌƒŠPÑ¡”Í½ÕÑ¡}İ…Ñ•É€‰…Í•±¥¹”É½Üµ•…ÍÕÉ•Ì„ÍÑ…¹Ñ¡…Ğ¹¼±½¹•È•á¥ÍÑÌ¨…ĞÑ¡”)Ñ½À½˜Ñ¡¥Ì™¥±”¸9¼½Ñ¡•ÈÍÑ…Ñ¥½¸¥¸Ñ¡•Í”Ñ…‰±•Ìµ½Ù•ì¹•İ‰•ÉÉå}‘½±•}İ¡…É™€€¡P´ÀÀĞÄ¤…¹)¹½ÉÑ¡}‰É…¹¡}‰É¥‘•}‘•­€€¡P´ÀÀÀÄ¤İ•É”…‘‘•Ñ¼Ñ¡”Í•¹”…™Ñ•Éİ…É‘Ì…¹¡…Ù”¹¼É½Ü¡•É”…Ğ…±°°)Í¼Ñ¡”É¥œ¹½ÜÍÑ…¹‘Ì…Ğ€¨©™½ÕÉÑ••¸¨¨ÍÑ…Ñ¥½¹Ì……¥¹ÍĞÑ¡¥ÌÑ…‰±”Ì•±•Ù•¸ƒŠPÑ¡”™½ÕÉÑ••¹Ñ ¥Ì)ÁÕ‰±¥}ÍÅÕ…É•€€¡P´ÀÈÈĞ°€ÈÀÈØ´Àà´Èà¤°„Á½Í”½¸Ñ¡”É•Í•ÉÙ•‰±½¬°İ¡½Í”Ñİ¼É½İÌ…É”…ĞÑ¡”Ñ½À½˜)Ñ¡¥Ì™¥±”¸((¨©]¡…ĞÑ¡”‰…Í•±¥¹”Í…åÌ°……¥¹ÍĞÑ¡”I9I%9ƒ
œÔÑ…É•ÑÌ¸¨¨((´€¨©!½É¥é½¸Ñ¥µ‰•È½Ù•É…”¥ÌÍ¡½ÉĞ½˜€äÀ€”¹•…É±ä•Ù•Éåİ¡•É”¨¨ƒŠP€À¸ÈÄÑ¼€À¸àä‘•Í­Ñ½À°‰•ÍĞ(€…Ğ™¥ÉÍÑ}Á½ÍÑ}½™™¥•€€ À¸àĞÜ¤…¹İ½ÉÍĞ±½½­¥¹œ‘½İ¸…ĞÑ¡”Ñ½İ¸™É½´Ñ¡”…¥È¸ƒ
œ€Ä¥Ñ•´€Ô(€ÍÑ…¹‘Ì°…¹Hµ\Ğ½İ¹Ì¥Ğ¸(´€¨©M¡…‘½İÌÍÑ¥±°±¥ÀÑ¼±¥Ñ•É…°‰±…¬¸¨¨€ÄÈ°ÀØÌÁÕÉ”€ À°À°À¥€Á¥á•±Ì…ĞÉ¥Ù•É}‰…¹­€°(€€ÄÄ°ÀÄÔ…Ğ™¥ÉÍÑ}Á½ÍÑ}½™™¥•€°€È°ÌÄÔ…ĞÁÉ…¥É¥•}Í½ÕÑ¡€½¸‘•Í­Ñ½À°…¹Ñ¡”‘…É­•ÍĞ‘•¥±”(€ÉÕ¹Ì…Ì±½Ü…Ì€¨©0€À¸äÌ¨¨……¥¹ÍĞÑ¡”ƒ
œ€Ô™±½½È½˜€¨©0ƒŠ&”€ÄĞ¨¨¸ƒ
œ€Ä¥Ñ•´€ÜÍÑ…¹‘Ì°…¹Hµ\Ä(€½İ¹Ì¥Ğ¸(´€¨©MÕ¹±¥ĞÉ½İ¹Ì…É”¹¼±½¹•È‰±Õ”¸¨¨Š"I¥ÌÁ½Í¥Ñ¥Ù”…Ğ•Ù•ÉäÍÑ…Ñ¥½¸€ ¬À¸ÈÑ¼€¬ĞÜ¸ä¤°İ•±°(€±•…È½˜Ñ¡”ƒŠ&”€¬ÄÀÑ…É•Ğ…Ğ¹¥¹”½˜•±•Ù•¸°İ¡•É”Ñ¡”Íİ••Àµ•…ÍÕÉ•ƒŠ"HÄäÑ¼ƒŠ"HÈØ¸Q¡”½±½ÕÈ(€‰ÕÌ™¥á•½¸€ÈÀÈØ´Àà´ÄÄ…É”Ñ¡”É•…Í½¸ìÑ¡¥Ì¥ÌÑ¡”™¥ÉÍĞµ•…ÍÕÉ•µ•¹ĞÑ¡…ĞÍ…åÌÍ¼¸(´€¨©É…¥¸ÍÑ¥±°½±±…ÁÍ•Ìİ¥Ñ ‘•ÁÑ °‰ÕĞ¹½ĞÕ¹¥™½Éµ±ä¨¨ƒŠPÍ…Õ…¹…Í¡€É•…‘Ì€ÄÀ¸Ğ€¼€Ü¸Ô€¼€À¸à(€™…È½µ¥½¹•…È½¸‘•Í­Ñ½À°É¥Ù•É}‰…¹­€€ÄÌ¸È€¼€ÈÌ¸ä€¼€Èä¸ä¸Q¡”ÍÑ…Ñ¥½¹ÌÑ¡…Ğ±½½¬‘½İ¸„(€ÍÑÉ••Ğ½È…É½ÍÌİ…Ñ•È¡½±Ñ¡•¥ÈÉ…¥¸ìÑ¡”½¹•Ì±½½­¥¹œ½Ù•È½Á•¸Íİ…É±½Í”¥Ğ¸ƒ
œ€Ä¥Ñ•´(€€ĞÍÑ…¹‘Ì¸(´€¨©±½İ•È±½……ĞÑ¡”ÁÉ…¥É¥”ÍÑ…Ñ¥½¹Ì¥Ì€À¸ÀÀÌÄ…¹€À¸ÀÀÄÈ¨¨……¥¹ÍĞÑ¡”¡½¹•ÍĞ€ÓŠLØ€”(€Ñ…É•Ğ¸ùùQİ¼½É‘•ÉÌ½˜µ…¹¥ÑÕ‘”Í¡½ÉÑùøƒŠP€¨©Ñ¡”…À¥Ì€Äã\Íµ…±±•ÈÑ¡…¸Ñ¡…Ğ°…¹Ñ¡¥Ì(€‰Õ±±•Ğİ…ÌİÉ½¹œ€¡Hµ\ÑŒ¡„¤°€ÈÀÈØ´Àà´ÄÔ¤¸¨¨Q¡½Í”…É”Ñ¡”€©É•¥Á”Ì¨™¥ÕÉ•Ì…¹Ñ¡”É•¥Á”(€µ¥ÍÍ•Ì€äĞ¸Ô€”½˜Ñ¡”‰±½½´…ĞÁÉ…¥É¥•}İ•ÍÑ€°½Õ¹Ñ¥¹œ€Øä¸Ü€”½˜Ñ¡”Á¥á•±Ì„™±½İ•ÈÁ…¥¹Ñ•(€…ÌÑ¡”Á±…¹Ğ¥Ğ¥Ì‰•¥¹œ½µÁ…É•……¥¹ÍĞ¸5•…ÍÕÉ•‰äÍÕ‰ÑÉ…Ñ¥½¸°Ñ¡”‰±½½´¥Ì€¨¨À¸ÀÈÄä€¼(€€À¸ÀÄàÜ€¼€À¸ÀÀÜØ¨¨…ĞÁÉ…¥É¥•}İ•ÍÑ€€¼ÁÉ…¥É¥•}Í½ÕÑ¡€€¼É¥Ù•É}‰…¹­€¸Q¡”É•¥Á”™¥ÕÉ•Ì…É”(€­•ÁĞ‰•…ÕÍ”Ñ¡”€ÈÀÈØ´Àà´ÄĞ‰…Í•±¥¹”¥Ì½¸Ñ¡•´¸(´€¨©É…Ü…±±Ì•á••Ñ¡”ƒŠ&€àÀ‰Õ‘•Ğ…Ğ™½ÕÈÍÑ…Ñ¥½¹Ì¨¨ƒŠPÁÉ…¥É¥•}İ•ÍÑ€€äÜ‘•Í­Ñ½À€¼€äĞ(€µ½‰¥±”°É••¹}ÑÉ••€€äÄ¼àà°™½É­Í€€àÜ¼àÈ°Í½ÕÑ¡}İ…Ñ•É€€àÔ¼àÌ¸€¨©Q¡¥Ì¥Ì¹•Ü¥¹™½Éµ…Ñ¥½¸°(€¹½Ğ„¹•Ü™…Õ±Ğ¨¨èÑ¡”‰Õ‘•Ğ¡…Ì½¹±ä•Ù•È‰••¸µ•…ÍÕÉ•…ĞÑ¡”ÍÁ…İ¸ÍÑ…Ñ¥½¸°İ¡•É”¥Ğ(€Á…ÍÍ•Ì…Ğ€ØÔ¼ØÈ°Í¼¹½‰½‘ä¡…ÍÑ½½…¹åİ¡•É”•±Í”İ¥Ñ Ñ¡”½Õ¹Ñ•ÈÉÕ¹¹¥¹œ¸I•½É‘•¥¸(€I=5@……¥¹ÍĞHµ\Ô°İ¡¥ ½İ¹ÌÑ¡”‘É…Üµ…±°İ½É¬¸((¨©]¡…Ğ¥Ì9=P¥¸Ñ¡¥Ì‰…Í•±¥¹”°ÍÑ…Ñ•Á±…¥¹±ä¸¨¨Q¡”€àµ…á¥ÌÉÕ‰É¥ŒÍ½É”À¸È…±Í¼…Í­Ì™½È¥Ì(¨©¹½ĞÉÕ¸¨¨¸Q¡”ÁÉ½Ñ½½°É•ÅÕ¥É•Ì„É¥Ñ¥ŒÑ¡…Ğ‘¥¹½ĞİÉ¥Ñ”Ñ¡”½‘”Õ¹‘•ÈÉ•Ù¥•Ü°…¹Ñ¡”)ÉÕ¸Ñ¡…Ğ‰Õ¥±ĞÑ¡”¡…É¹•ÍÌ…¹¹½Ğ‰”Ñ¡…ĞÉ¥Ñ¥Œİ¥Ñ¡½ÕĞµ…­¥¹œÑ¡”Í½É”µ•…¹¥¹±•ÍÌ¸%Ğ¥Ì)Á…É•±±•…ÌI=5@€¨©HµÄ¨¨…¹Ñ¡”‰…Í•±¥¹”¥Ì¥¹½µÁ±•Ñ”Õ¹Ñ¥°¥Ğ±…¹‘Ì¸((´´´((ŒŒ]¡…Ğ•á¥ÍÑÌ…¹İ½É­Ì()ğÑ¡¥¹œğÍÑ…Ñ”ğ)ğ´´µğ´´µğ)ğI•Á½Í¥Ñ½ÉäÍ…™™½±ğ€¨©‘½¹”¨¨ƒŠP™Õ±°ÑÉ•”Á•È‘½Ì½A18¹µ‘€ğ)ğM¡•µ…Ì€¡ÍÑÉÕÑÕÉ”°Í½ÕÉ”°Í•¹”¤ğ€¨©‘½¹”¨¨ƒŠPÁ¡…Í•Ì°Ñ¥•ÉÌ°É¥¡ÑÌ…Ñ¥¹œ°Í•¹”µ½İ¹•‘…Ñ•Ìğ)ğÑ½½±Ì½Ù…±¥‘…Ñ”¹Áå€ğ€¨©‘½¹”¨¨ƒŠPÍ¡•µ„°É•™•É•¹Ñ¥…°°½¹™¥‘•¹”½¹ÑÉ…Ğ°Á•ÈµÍ•¹”‘…Ñ”…Ñ•Ì°Á¡…Í”µ½Ù•É±…À°•Á½ ½Ù•É…”°É•±•…Í”‰±½­¥¹œ°±¥•¹Í”€¬É¥¡ÑÌ…Ñ¥¹œ°ÍÑ…±•¹•ÍÌ°ÁÕ‰±¥Í ‰Õ‘•Ğğ)ğÑ½½±Ì½Ñ•ÍÑ}Ù…±¥‘…Ñ”¹Áå€ğ€¨©‘½¹”¨¨ƒŠP€äØ¡•­Ì°…±°É••¸°¥¹±Õ‘¥¹œ„ÁÉ½½˜Ñ¡…Ğ…¸€ÄàÌØ‰Õ¥±‘¥¹œ¥Ì•á±Õ‘•™É½´Ñ¡”€ÄàÌÔÍ•¹”°Ñ¡…Ğ„±¥‰•ÉÑä¹…µ¥¹œ„‰Õ¥±‘¥¹œ‘½•Ì¹½Ğ½Ù•È…¸¥¹Ù•¹Ñ¥½¸¥Ğ¹•Ù•Èµ•¹Ñ¥½¹Ì°Ñ¡…Ğ…¸…ÑÑÉ¥‰ÕÑ”Ñ¡”…É¡•ÑåÁ”¹•Ù•ÈÉ•…‘Ì…¹¹½ĞÁ…ÍÌİ¥Ñ¡½ÕĞÍ…å¥¹œİ¡…ĞÑ¡”µ•Í ‘½•Ì¥¹ÍÑ•…°…¹Ñ¡…ĞÉ•İÉ¥Ñ¥¹œ„É•½ÉÌÁÉ½Í”‘½•Ì¹½ĞÉ•Á½ÉĞ¥ÑÌµ•Í …ÌÍÑ…±”İ¡¥±”¡…¹¥¹œ„Ù…±Õ”Ñ¡”•¹•É…Ñ½ÈÉ•…‘Ì‘½•Ì°…¹Ñ¡…Ğ…¸…ÑÑÉ¥‰ÕÑ”…¸…É¡•ÑåÁ”‘•±…É•Ì¥Ğ½¹ÍÕµ•Ì…ÑÕ…±±äµ½Ù•ÌÑ¡”Á…É…µ•Ñ•ÉÌİ¡•¸¥ÑÌÙ…±Õ”¡…¹•Ì°…¹Ñ¡…Ğ…¸•á±ÕÍ¥½¸…ÉÉ¥•Ì„É•…Í½¸…¹„¥Ñ…Ñ¥½¸Ñ¡…ĞÉ•Í½±Ù•Ì…¹ÍÑ½ÁÌ‰•¥¹œ…¸•á±ÕÍ¥½¸…Ğ¥ÑÌ½İ¸•…É±¥•ÍĞÍ•¹”ğ)ğÑ½½±Ì½¡•¬¹Í¡€ğ€¨©‘½¹”¨¨ƒŠP™Õ±°…Ñ”ÉÕ¹Ì¥¸€¨¨À¸ĞÌ¨¨°¹¼	±•¹‘•Èğ)ğI•Í•…É ‘½ÍÍ¥•ÉÌğ€¨©‘½¹”¨¨ƒŠP€àÉ•Á½ÉÑÌ°øÌØÀ-°½µµ¥ÑÑ•Ù•É‰…Ñ¥´¥¸‘½Ì½É•Í•…É ½€ğ)ğM½ÕÉ”É•½É‘Ìğ€¨¨ÈÔ¨¨°½˜İ¡¥ €¨¨ÄĞ¨¨…ÉÉä„]…å‰…¬Í¹…ÁÍ¡½ĞƒŠPÑ¡”Ñ¡É•”…‘‘•İ¥Ñ Ñ¡”‰É¥‘”…±°‘¼°…¹Í¼‘½•ÌÑ¡”Á½ÍĞµ½™™¥”Á…”ğ)ğMÑÉÕÑÕÉ”É•½É‘Ìğ€¨¨ÄàĞ¥¸Ñ¡”€ÄàÌÔÍ•¹”¨¨ƒŠP€ÜØÁÉ”µ•á¥ÍÑ¥¹œ•Ù¥‘•¹”É•½É‘ÌÁ±ÕÌ€ÄÀàÙ¥Í¥‰±äÑ…•…¹½¹åµ½ÕÌÉ•½µµ•¹‘•¥¹™¥±°É•½É‘ÌìÉ•½É½Õ¹Ğ…¹Á¡åÍ¥…°µÉ½½˜½Õ¹Ğ…É”Í•Á…É…Ñ•±äÉ•½¹¥±•ğ)ğQ•ÉÉ…¥¸•Á½¡ÌğÉ•¥ÍÑÉäİÉ¥ÑÑ•¸ì”ÄàÌÑ}¡…É‰½É}ÕÑ€…Ñ¥Ù”°•½µ•ÑÉä±…å•ÉÌ€¨©¹½Ğå•Ğ‰Õ¥±Ğ¨¨ğ)ğ€¨©…ÑÕ´¨¨ğ€¨©YI%%¨¨ƒŠP]É¥¡Ğµ‘•É¥Ù•°!…Ñ¡…İ…ä´…¹=M4µ¡•­•°I5L€ÄÜ¸Ô´°É”µ‘•É¥Ù…‰±”™É½´ÑÉ…•Ìğ)ğ€¨©•¹•É…Ñ½ÈÁ¥Á•±¥¹”¨¨ğ€¨©]=I-L¨¨ƒŠPÁ¥¹¹•	±•¹‘•È€Ğ¸Ô¸Ì°™É…µ•}Ñ…Ù•É¹€°€ĞäØµÑÉ¤M…Õ…¹…Í ™É½´Ñ¡”É•½É…±½¹”ğ)ğ€¨©™É…µ•}‘İ•±±¥¹€¨¨ğ€¨©	U%1P€ÈÀÈØ´Àà´ÄÄ°9<I=IUML%PeP¨¨ƒŠPÑ¡”…É¡•ÑåÁ”Ñ¡…ĞÕ¹‰±½­Ì¡½ÕÍ•Ìè€Ä¼Ä¸Ô¼ÈÍÑ½É•åÌ°­¹•”İ…±°…¹…‰±”µ•¹…ÑÑ¥Œİ¥¹‘½Ü°É•…È•±°É•…½™˜Ñ¡”™½½ÑÁÉ¥¹ĞÁ½±å½¸°ÍÑ½½À½ÈÍµ…±°É½½™•Á½É °…¹½¹ÍÑÉÕÑ¥½¹€™¥¹…±±äµ½Ù¥¹œÙ•ÉÑ¥•Ì€¡ÍÑÕµ½‘Õ±”Á±…•ÌÑ¡”½Á•¹¥¹Ì°±…Á‰½…É‰ÕÑĞ©½¥¹ÑÌ±…¹½¸ÍÑÕ±¥¹•Ì°‰É…•™É…µ•Ì•ĞÑ¡”¥ÉĞ‰…¹„‰…±±½½¸™É…µ”¡…Ì¹¼±¥¹”™½È¤¸½±‘•¸Á…É…µÌ€¬‘½Ì½IMI ½…É¡•ÑåÁ”µ™É…µ•}‘İ•±±¥¹œ¹Á¹€ì€ÈĞà´ÜÌÀÑÉ¥ÌÁ•È¡½ÕÍ”¸I=U9}=9QPèÁ•É¥µ•Ñ•É€Ù•É¥™¥•……¥¹ÍĞÑ¡”µ•Í ƒŠP•Ù•Éä•‘”½˜Ñ¡”™½½ÑÁÉ¥¹ĞÁ½±å½¸…ÉÉ¥•Ì„İ…±°…Ğè€ô€À°İ½ÉÍĞ…À€À¸Àµ´°¹½Ñ¡¥¹œ‰•±½ÜÑ¡”‰…Í”½˜Ñ¡”İ…±±Ìğ)ğ€¨©½ÕÑ‰Õ¥±‘¥¹€¨¨ğ€¨©	U%1P€ÈÀÈØ´Àà´ÄÄ°9<I=IUML%PeP¨¨ƒŠPÑ¡”¡¥¡•ÍĞµ½Õ¹ĞµÁ•Èµ•™™½ÉĞ…É¡•ÑåÁ”¥¸Ñ¡”Á±…¸°…¹Ñ¡”½¹”Ñ¡…Ğ¥Ù•ÌÑ¡”Ñ½İ¸å…É‘Ì¥¹ÍÑ•…½˜•¥¡Ğ¥Í½±…Ñ•ÁÕ‰±¥Œ¡½ÕÍ•Ì¸5%1d°¹½Ğ„Í¡…Á”è½¹ÍÑÉÕÑ¥½¹€±½œ½Á±…¹¬½±¥¡Ñ}™É…µ”‘É¥Ù•ÌÑ¡É•”‘¥™™•É•¹Ğİ…±°É½ÕÑ¥¹•Ì°Í¡•É½½™Ì…É”™¥ÉÍĞµ±…ÍÌÉ…Ñ¡•ÈÑ¡…¸„™…±±‰…¬°½Á•¹}Í¥‘•Í€ÑÕÉ¹Ì…¹äÍÕ‰Í•Ğ½˜•±•Ù…Ñ¥½¹Ì¥¹Ñ¼Á½ÍÑÌµ…¹µÁ±…Ñ”°…¹‘½½É€¥Ì¹½¹”½µ…¸½ÍÑ…‰±”½İ…½¸ƒŠP„‰½½±•…¸¥ÌÉ•™ÕÍ•İ¥Ñ „µ•ÍÍ…”Í…å¥¹œİ¡ä¸‰½…É‘}…Á}µ€…±½¹”¥ÌÑ¡”İ¡½±”‘¥™™•É•¹”‰•Ñİ••¸„ÍÑ…‰±”…¹„½É¸É¥ˆ¸¥Ù”½±‘•¸Ù…É¥…¹ÑÌ™É½´„€Ä¸ÈÔ´ÁÉ¥ÙäÑ¼„€ÄÌ´¡½Ñ•°ÍÑ…‰±”°€ÈÜÈ´ÈÀÀàÑÉ¥ÌìI=U9}=9QPèÁ•É¥µ•Ñ•É€Ù•É¥™¥•½¸10%Y……¥¹ÍĞÉ½Õ¹µÁ±…¹”LÉ…Ñ¡•ÈÑ¡…¸Ù•ÉÑ¥•Ì€¡Ñ¡”™¥ÉÍĞ¡•¬½µÁ…É•Ù•ÉÑ¥•Ì…¹ÁÉ½‘Õ•™…±Í”™…¥±ÕÉ•Ì½¸„€ÄÌ´İ…±°Ñ¡…Ğ¥Ì½¹”ÅÕ…¤¸¥Í¡…É•ÌÑ¡”ÍÑ…‰±”¡…±˜½˜0ÄÀì€¨©Ñ¡”å…É¡…±˜ÍÑ…åÌ½Á•¸¨¨ƒŠP„™•¹”±¥¹”İ¥Ñ Ñİ¼…Ñ•İ…åÌ¥Ì…¸•¹±½ÍÕÉ”°…¹‰Õ¥±‘¥¹œ¥Ğ½ÕĞ½˜…¸½ÕÑ‰Õ¥±‘¥¹œİ½Õ±‰”…±±¥¹œ„™•¹”„‰Õ¥±‘¥¹œ°Í¼0ÄÀ¹••‘Ì9II=]%9É…Ñ¡•ÈÑ¡…¸É•Í½±Ù¥¹œğ)ğ€¨©M½ÕÑ ]…Ñ•ÈMÑÉ••Ğ¨¨ğ€¨©	U%1P€ÈÀÈØ´Àà´ÄÄ¨¨ƒŠPÍ¥áÑ••¸½µµ•É¥…°É•½É‘Ì±…¹Ñ¡”Ñ½İ¸Ì‰ÕÍ¥¹•ÍÌÍÑÉ••Ğ°İ¡¥ Ñ¡”µ½‘•°¡•±¹½¹”½˜èA•¬ÌÍÑ½É”°‰½Ñ ¹•İÍÁ…Á•È½™™¥•Ì°!…Éµ½¸€˜1½½µ¥Ì°5…‘½É”	•…Õ‰¥•¸Ì±½œ¡½ÕÍ”°	…Ñ•ÌÌ…ÕÑ¥½¸É½½´°Ñ¡”	•…Õ‰¥•¸¡½µ•ÍÑ•…°½±”Ìİ…É•¡½ÕÍ”°‰½Ñ …ÉÁ•¹Ñ•ÈÍ¡½ÁÌ°É•‘•É¥¬Q¡½µ…Ì°Ñ¡”½±‰…¹¬‰Õ¥±‘¥¹œ°AÉÕå¹”€˜-¥µ‰…±°°(¸ ¸-¥¹é¥”°)½¹•Ì°…¹Q¡½µ…Ì¡ÕÉ ½¸1…­”¸=¹”™½½ÑÁÉ¥¹Ğ¥Ì•Ù¥‘•¹”€¡…ÉÁ•¹Ñ•ÈÌ€ÄØà€ÈÀ™Ğ±½œÍ¡½ÀƒŠPÑ¡”‘…Ñ…Í•ĞÌM=9É•…°™½½ÑÁÉ¥¹Ğ¤ì™¥™Ñ••¸…É”¥¹Ù•¹Ñ•¥¹Í¥‘”Ñ¡”‘½Õµ•¹Ñ•€ÔÔ™ĞM½ÕÑ ]…Ñ•È±½Ğ…À¸€¨©]¡…ĞÑ¡¥ÌÍÑÉ••Ğ­¹½İÌ¥Ì€©İ¡¼¨…¹€©İ¡•É”¨°…¹…±µ½ÍĞ¹•Ù•È€©¡½Ü‰¥œ¨¸¨¨Qİ¼É•½É‘Ì…ÉÉäÉ•Ù¥•İ}É•ÅÕ¥É•‘€€¡Ñ¡”	•…Õ‰¥•¹Ì°İ¡½Í”¡¥ÍÑ½ÉäÉÕ¹ÌÍÑÉ…¥¡Ğ¥¹Ñ¼Ñ¡”ÕÕÍĞ€ÄàÌÔÉ•µ½Ù…°…¹Ñ¡”É•Í•ÉÙ…Ñ¥½¸ÁÉ”µ•µÁÑ¥½¸¤ƒŠPİ¡¥ ‰±½­ÌÑ¡”€ÄàÌÔÍ•¹”™É½´É•±•…Í•‘€Õ¹Ñ¥°½¹ÍÕ±Ñ…Ñ¥½¸¡…ÁÁ•¹Ì¸Qİ¼Õ¹É•Í½±Ù•É•…‘Ì…É”™±…•½¸Ñ¡”É•½É‘ÌÑ¡•µÍ•±Ù•Ìèİ¡•Ñ¡•È!…Éµ½¸€˜1½½µ¥ÌÌ‰Õ¥±‘¥¹œ%LÑ¡”€©¡¥…¼•µ½É…Ğ¨Ì‰Õ¥±‘¥¹œ€¡Ñ¡•äÍ¥Ğ€ÌÜ´…Á…ÉĞ…¹¹‘É•…Ì¥Ù•Ì¹¼Í¥‘”¤°…¹İ¡•Ñ¡•ÈA¡¥±¼…ÉÁ•¹Ñ•ÈÌ1…­”MÑÉ••Ğ±½œÍ¡½ÀÍÑ¥±°ÍÑ½½…™Ñ•È¡”‰Õ¥±Ğ½¸M½ÕÑ ]…Ñ•È¥¸€ÄàÌÌğ)ğ€¨©I•¹‘•É•È¨¨ğ€¨©]1-	199Y%	1¨¨ƒŠPÑ¡É•”¹©ÌÈÀ¸ÄàÔ¸ÄÙ•¹‘½É•°Á½¥¹Ñ•Èµ±½¬€¬Ñ½Õ °½¹™¥‘•¹”Ù¥•Ü°ÁÉ½Ù•¹…¹”Á½ÁÕÀ°±¥Ù”½µÁ…ÍÌ…¹„¹½ÉÑ µÕÀ½Ù•ÉÙ¥•Ü‘•É¥Ù•™É½´Ñ¡”±½…‘•¡•¥¡Ñ™¥•±…¹ÍÑÉÕÑÕÉ”™½½ÑÁÉ¥¹ÑÌğ)ğ€¨©9…Ù¥…Ñ¥½¸¥¹‘•à¨¨ğ€¨©=5A1Q=H=55%QQQ¨¨ƒŠPM•ÑÑ¥¹ÌÍ•…É¡•Ì…±°€ÜØÍ•¹”ÍÑÉÕÑÕÉ•Ì…¹…±°™½ÕÈÙ•É¥™¥•¥¹Ñ•ÉÍ•Ñ¥½¹Ì°İ¥Ñ …±¥…Í•Ì…¹É•½É‘•±½…Ñ¥½¸Ñ•áĞì¥¹Ñ•ÉÍ•Ñ¥½¸Á½Í¥Ñ¥½¹Ì…É”½µÁ¥±•™É½´‘…Ñ„½ÑÉ…•Ì½ÍÑÉ••Ñ}½¹ÑÉ½°¹©Í½¹€É…Ñ¡•ÈÑ¡…¸½Á¥•¥¹Ñ¼É•¹‘•É•È½‘”¸½µÁ…ÍÌ°½Ù•ÉÙ¥•Üµ…À…¹Ñ¡”±¥Ù”€ÄàÌÔ½ÕÉÉ•¹ĞÍÑÉ••Ğµ¹…µ”É•…‘½ÕĞ…É”¥¹‘•Á•¹‘•¹Ñ±äÁ•ÉÍ¥ÍÑ•¹ĞÑ½±•Ì¸™½ÕÉÑ Á•ÉÍ¥ÍÑ•¹ĞÍ•ÑÑ¥¹œÍİ¥Ñ¡•Ì•Ù•ÉäÙ¥Í¥Ñ½Èµ™…¥¹œ¹…Ù¥…Ñ¥½¸µ•…ÍÕÉ•µ•¹Ğ‰•Ñİ••¸%µÁ•É¥…°€¡Ñ¡”‘•™…Õ±Ğè™Ğ°µ¤°µÁ ¤…¹5•ÑÉ¥Œ€¡´°­´°­´½ ¤İ¥Ñ¡½ÕĞ¡…¹¥¹œÑ¡”µ•ÑÉ¥ŒÍ•¹”‘…Ñ„¸Q¡”É•…‘½ÕĞÉ•Á½ÉÑÌÑ¡”½ÉÉ¥‘½ÈÕ¹‘•É™½½Ğ°…¸¥¹Ñ•ÉÍ•Ñ¥½¸İ¡•¸Ñİ¼•¹ÑÉ•±¥¹•Ì…É”¹•…È°…¹Ñ¡”¹•áĞÉ½ÍÌÍÑÉ••ĞÕÀÑ¼€ÜÀ´€¼€ÈÌÀ™Ğ…¡•…¸ğ)ğ€¨©Mµ½­”¨¨ğ€¨©AML€ÈÀÈØ´Àà´ÄĞ¨¨ƒŠPÑ½½±Ì½¡•¬¹Í¡€É••¸°…¹¹½‘”Ñ½½±Ì½Íµ½­•}É•¹‘•É•È¹µ©Í€É••¸…Ğ‰½Ñ É•±•…Í”Ù¥•İÁ½ÉÑÌ¥¸…±°™½ÕÈ½µ‰¥¹…Ñ¥½¹ÌÑ¡”…Ñ”…Í­Ì™½ÈèÍ½ÕÉ”ÑÉ•”€¨¨ÈÀĞµ½‰¥±”€¼€ÈÀÄ‘•Í­Ñ½À¨¨°ÁÕ‰±¥Í¡•µ¥ÉÉ½È€¨¨ÈÀĞ€¼€ÈÀÄ¨¨°é•É¼Á…”•ÉÉ½ÉÌÑ¡É½Õ¡½ÕĞ°İ¥Ñ Ñ¡”Ñ½İ¸…Ğ€ÈØÄÉ•½É‘Ì¸IÕ¸…Ì™½ÕÈÍ•Á…É…Ñ”™½É•É½Õ¹½µµ…¹‘Ì‰•…ÕÍ”„™Õ±°Á…ÍÌ•á••‘ÌÑ•¸µ¥¹ÕÑ•Ì¸Q¡”¡¥ÍÑ½Éä‰•±½Ü¥ÌÑ¡”É•½É½˜¡½ÜÑ¡½Í”…ÍÍ•ÉÑ¥½¹Ìİ•É”•…É¹•¸€¨©AML€ÈÀÈØ´Àà´ÄÌ°…¹™½ÈÑ¡”™¥ÉÍĞÑ¥µ”……¥¹ÍĞÑ¡”™¥±•ÌÑ¡…Ğ…ÑÕ…±±äÍ¡¥À¸¨¨Ñ½½±Ì½¡•¬¹Í¡€¥ÌÉ••¸°…¹¹½‘”Ñ½½±Ì½Íµ½­•}É•¹‘•É•È¹µ©Í€Á…ÍÍ•Ì€¨¨ÌØÄ…ÍÍ•ÉÑ¥½¹Ì¨¨…Ğ‰½Ñ É•±•…Í”Ù¥•İÁ½ÉÑÌ€ ÌäÁàÜàÀ…¹€ÄÈàÁààÀÀ¤İ¥Ñ é•É¼Á…”•ÉÉ½ÉÌƒŠPÉÕ¸Ñİ¥”°½¹”……¥¹ÍĞÑ¡”Í½ÕÉ”ÑÉ•”…¹½¹”İ¥Ñ €´µÁÕ‰±¥Í¡•‘€……¥¹ÍĞÑ¡”µ¥ÉÉ½È¸€¨©Q¡”Í•½¹ÉÕ¸¥ÌÑ¡”½¹”Ñ¡…Ğµ…ÑÑ•ÉÌ…¹¥Ğ‘¥¹½Ğ•á¥ÍĞÕ¹Ñ¥°¹½Ü¸¨¨Í¥‘•…ÈÌ±Ñ˜¼ñ¹…µ”ø¹±‰€É•Í½±Ù•ÌÑ¼Ñ¡”U9=5AIMMµ…ÍÑ•ÉÌ¥¸Ñ¡”Í½ÕÉ”ÑÉ•”…¹Ñ¼Ñ¡”µ•Í¡½ÁĞ€¬ÅÕ…¹Ñ¥Í•‘•É¥Ù…Ñ¥Ù•Ì½¸Ñ¡”Í¥Ñ”°Í¼¹½Ñ¡¥¹œÑ¡…ĞÉ…¸¡…•Ù•È±½…‘•„½µÁÉ•ÍÍ•…ÍÍ•ĞƒŠP…¹„É•¹‘•É•È‰ÕœÑ¡…Ğ½¹±ä•á¥ÍÑÌ¥¸Ñ¡”ÅÕ…¹Ñ¥Í•Á…Ñ ½±±…ÁÍ•…±°€ÈĞÈÍÑÉÕÑÕÉ•ÌÑ¼€È´‰½á•Ì½¸Ñ¡”±¥Ù”Í¥Ñ”™½ÈÍ•Ù•É…°‘…åÌ°Ñ¡É½Õ Ñİ¼…ÑÑ•µÁÑ•™¥á•Ì°İ¥Ñ Ñ¡”…Ñ”™Õ±±äÉ••¸Ñ¡”İ¡½±”Ñ¥µ”¸Q¡”Í¥é”…ÍÍ•ÉÑ¥½¸İ…Ì…±Í¼µ•…ÍÕÉ¥¹œÑ¡”Q11MP‰Õ¥±‘¥¹œ¥¸Ñ¡”Í•¹”°İ¡¥ Á…ÍÍ•Ìİ¥Ñ ½¹”½ÉÉ•Ğ‰Õ¥±‘¥¹œ…¹€ÈĞÄ‰É½­•¸½¹•Ìì¥Ğ¹½Üµ•…ÍÕÉ•Ì•Ù•ÉäÍÑÉÕÑÕÉ”……¥¹ÍĞ¥ÑÌ½İ¸É•½É°¥¹±Õ‘¥¹œ¥ÑÌ‘½Õµ•¹Ñ•İ…±°¡•¥¡Ğ¸I•¥¹ÑÉ½‘Õ¥¹œÑ¡”™…Õ±Ğ™…¥±ÌÑ¡”¹•Ü¡•­Ì‰ä¹…µ”½¸…±°€ÈĞÈ¸Ñ½½±Ì½‰…­”¹Í¡€ÉÕ¹ÌÑ¡”ÁÕ‰±¥Í¡•Íµ½­”…™Ñ•ÈÁÕ‰±¥Í ¸É…Ü…±±Ì…¹ÑÉ¥…¹±•Ì…ĞÑ¡”ÍÁ…İ¸ÍÑ…Ñ¥½¸è€¨¨Ôä€¼€ÌÌÈ°ĞÔÔ¨¨‘•Í­Ñ½À°¥¹Í¥‘”Ñ¡”€àÀ€¼€Ä°ÀÀÀ°ÀÀÀÕ±°µ‘•Ñ…¥°‰Õ‘•Ğ¸Q¡”Ñİ¼¡…±Ù•ÌÍÑ¥±°ÉÕ¸…ÌÍ•Á…É…Ñ”™½É•É½Õ¹½µµ…¹‘Ì°‰•…ÕÍ”„™Õ±°Á…ÍÌ•á••‘ÌÑ•¸µ¥¹ÕÑ•Ì¸ğ)ğ€¨©±½É„¨¨ğ€¨©Ñ¡”Íİ…É¥Ì¥¸ìÑ¡”™…±Í”™…Èµ™¥•±ÍÕÉ™…”¥Ì½ÕĞ¨¨€ ÈÀÈØ´Àà´ÄÄ¤ƒŠPÉ•¹‘•É•ÉÌ½İ•ˆ½©Ì½™±½É„¹©Í€Á±…¹ÑÌÑ¡”É…µ¥¹½¥µ…ÑÉ¥à°™½É‰Ì°•µ•É•¹ÑÌ…¹±½ÜÍ¡ÉÕ‰Ì™É½´‘…Ñ„½™±½É„½€¸)Õ±äÁ¡•¹½±½äÉ•µ…¥¹Ì•¹™½É•¥¸É•¹‘•É•È…¹‘…Ñ„¸9•…È½µ¥‘‘±”Á±…¹ÑÌÉ½½Ğ½¸Ñ¡”•á…ĞÑ•ÉÉ…¥¸ÍÕÉ™…”…¹İ…Ñ•È•µ•É•¹ÑÌ½¸Ñ¡”İ…Ñ•ÈÍÕÉ™…”¸Q¡”™½Éµ•ÈÍ½±¥…¹½Áä…ĞÁ±…¹ĞµÑ½À¡•¥¡Ğİ…ÌÑ¡”…ÁÁ…É•¹ĞÍ•½¹É½Õ¹Í••¸½¸É•…°‘•Ù¥•Ìì¥Ğ¥ÌÉ•µ½Ù•°…¹Õ¹É•Í½±Ù•‘¥ÍÑ…¹ĞÁÉ…¥É¥”½±½ÕÈ¹½ÜÍÑ…åÌ½¸Ñ¡”Í½±”Ñ•ÉÉ…¥¸ÍÕÉ™…”€¡0àÀ¤¸€¨©M¥¹”€ÈÀÈØ´Àà´ÄÌ•… ½µµÕ¹¥Ñä¥ÌÁ±…¹Ñ•…Ğ¥ÑÌ½İ¸É•½É‘•½Ù•È¹µ…ÑÉ¥á}™É…Ñ¥½¹€¨¨ƒŠP„™¥•±Ñ¡”É•½É‘Ì…ÉÉ¥•°Ñ¡”Ù…±¥‘…Ñ½È…Ñ•…¹Ñ¡”É•¹‘•É•È¡…¹•Ù•È…Í­•™½ÈƒŠP…¹•… ¥ÌÍÁ±¥Ğ‰äÑ¡”ÁÕ‰±¥Í¡•ÍÕ‰ÍÑÉ…Ñ•€½˜¥ÑÌÍÁ•¥•Ì°Í¼„™±½…Ñ¥¹œµ±•…Ù•…ÅÕ…Ñ¥Œ¥ÌÁ±…¹Ñ•½Ù•Èİ…Ñ•È…¹¹•Ù•È½¸Ñ¡”‰…¹¬¥Ğİ…ÌÍÑ…¹‘¥¹œ½¸¸ğ)ğ€¨©Q¡”É½Õ¹Ì±…¥µÌ°¥¸Ñ¡”…ÁÀ¨¨ğ€¨©‘½¹”¨¨€ ÈÀÈØ´Àà´ÄÀ¤ƒŠPÑ¡”Ù¥‘•¹”Á…¹•°Ì€©Q¡”É½Õ¹å½Ô…É”ÍÑ…¹‘¥¹œ½¸¨É•…‘ÌÉ…‘•±…¥µÌ½™˜Ñ•ÉÉ…¥¹}ÍÁ•Œ¹©Í½¹€°‘•É¥Ù•Á•ÈÍ•¹”‰ä½µÁ¥±•}Í•¹”¹Áå€…¹É”µ‘•É¥Ù•‰ä¡•¬¹Í¡€ìÑ¡”Í…µ”Í±¥”…‘‘•É•…Í½¹¥¹œ…¹•½µ•ÑÉäµÍÑ…Ñ”¡•­ÌÍ¼Ñ¡½Í”É½İÌ…É”¹¼±½¹•ÈÍ¥±•¹ĞÁÉ½µ¥Í•Ì¸ğ)ğ€¨©]¡…Ğ„Í½ÕÉ”¥Ì°¥¸Ñ¡”…ÁÀ¨¨ğ€¨©‘½¹”¨¨€ ÈÀÈØ´Àà´ÄÄ¤ƒŠP¥Ñ…Ñ¥½¹Ì¹½Ü…ÉÉäÑ¡”‘½Õµ•¹Ğ„µ½‘•É¸Á…”É•ÁÉ¥¹ÑÌ€¡ÑÉ…¹ÍÉ¥‰•Í€¤½ÈÑ¡”É•…‘¥¹œÑ¡…Ğ¥ĞÉ•ÁÉ¥¹ÑÌ¹½¹”°Á±ÕÌ•… Í½ÕÉ”Ì½İ¸İ¡…Ñ}¥Ñ}ÍÕÁÁ±¥•Í€€¼İ¡…Ñ}¥Ñ}‘½•Í}¹½Ñ}ÍÕÁÁ±å€°Í¼Ñ¡”±…‘‘•È„Ù¥Í¥Ñ½ÈÍ••Ì¥¹±Õ‘•ÌÑ¡”É•…Í½¸¥Ğ¥ÌÑ¡”±…‘‘•È¸ğ)ğ€¨©1¥‰•ÉÑ¥•Ì°¥¸Ñ¡”…ÁÀ¨¨ğ€¨©‘½¹”¨¨ƒŠPÑ¡”Ù¥‘•¹”Á…¹•°±¥ÍÑÌÑ¡”±¥‰•ÉÑ¥•Ì‘•É¥Ù•™É½´‘½Ì½1%	IQ%L¹µ‘€‰äÑ½½±Ì½½µÁ¥±•}±¥‰•ÉÑ¥•Ì¹Áå€…¹É”µ‘•É¥Ù•‰ä¡•¬¹Í¡€ìÑ¡”ÁÉ½Ù•¹…¹”Á½ÁÕÀÍ¡½İÌÑ¡”½¹•ÌÑ…­•¸İ¥Ñ Ñ¡”‰Õ¥±‘¥¹œå½Ô…É”¥¹ÍÁ•Ñ¥¹œì…¹Ñ¡”…Ñ”¡•­ÌÑ¡”‘½Õµ•¹Ğ€©™½È…ÁÌ¨¥¸‰½Ñ ‘¥É•Ñ¥½¹ÌƒŠPÉ•™ÕÍ¥¹œ…¹ä½¹©•ÑÕÉ…°Ù…±Õ”€¡™½½ÑÁÉ¥¹Ğ°Á½Í¥Ñ¥½¸°„Ñ•ÉÉ…¥¸±…¥´°½È„ÍÑ…Ñ•™½É´…ÑÑÉ¥‰ÕÑ”¤Ñ¡…Ğ¹¼±¥‰•ÉÑä…‘µ¥ÑÌÑ¼°…¹•ÅÕ…±±ä…¹ä…ÑÑ•ÍÑ•Ù…±Õ”Ñ¡”…É¡•ÑåÁ”½ÈÑ•ÉÉ…¥¸•¹•É…Ñ½È¹•Ù•ÈÉ•…‘Ì…¹¹¼±¥‰•ÉÑä½İ¹ÌÕÀÑ¼±•…Ù¥¹œ½ÕĞğ)ğ€¨©Q¡”Á±…ÑÑ•ÍÑÉ••Ğµ½‘Õ±”¨¨ğ€¨©5MUI9Y%M%	1¨¨ƒŠPÍÑÉ••Ğ½ÉÉ¥‘½ÉÌ…¹İ¥‘Ñ¡ÌÉ•µ…¥¸½µµ¥ÑÑ•¥¸‘…Ñ„½ÑÉ…•Ì½Ù•Ñ½ÉÌ½ÍÑÉ••Ñ}½ÉÉ¥‘½ÉÍ|ÄàÌĞ¹©Í½¹€°İ¥Ñ 1…­”…¹I…¹‘½±Á ¹…µ•™É½´½µµ¥ÑÑ•½¹ÑÉ½°…¹É”µ‘•É¥Ù•½™™±¥¹”‰ä¡•­}ÍÑÉ••Ñ}µ½‘Õ±•€¸‘…Ñ„½ÍÑÉ••ÑÌ¼ÄàÌÔ¹©Í½¹€¹½Ü…‘‘ÌÍ•Ù•¹Ñ••¸‘…Ñ•Á…Ñ¡Ì…¹­••ÁÌÑ¡”€àÀ™Ğ±•…°½ÉÉ¥‘½ÈÍ•Á…É…Ñ”™É½´0ÜäÌ€Ô¸à´ÄÀ¸Ô´Ù¥Í¥‰±”ÑÉ…Ù•±±•ÍÑÉ¥ÁÌ¸½µÁ¥±•}Í•¹”¹Áå€©½¥¹ÌÑ¡•¥È¥Ñ…Ñ¥½¹Ì¥¹Ñ¼Ñ¡”Í¥‘•…È¥¹‘•àìÑ¡”É•¹‘•É•È‘É…Á•ÌÑ¡•´½¸Ñ¡”É½Õ¹°±¥ÁÌÑ¡•´…Ğİ…Ñ•È…¹±•…ÉÌÙ••Ñ…Ñ¥½¸½¹±ä™É½´Ñ¡”ÑÉ…¬¸M½ÕÑ ]…Ñ•È…¹1…­”É•……ÌÁÉ¥¹¥Á…°É…‘••…ÉÑ °½É‘¥¹…ÉäÍÑÉ••ÑÌ…Ìİ½É¸¹…Ñ¥Ù”•…ÉÑ °…¹¹¼É…Ù•°°Á±…¹¬É½…‘İ…ä½È¡…ÉÁ…Ù¥¹œ¥ÌÍ¡½İ¸¸9½ÉÑ ]…Ñ•ÈÌÕÉÙ”…¹•Ù•ÉäÉÕĞ½ÑÉ…¬İ¥‘Ñ É•µ…¥¸•áÁ±¥¥Ñ±ä½¹©•ÑÕÉ…°¸ğ)ğ€¨©Q¡”±…­”Í¡½É”¨¨ğ€¨©QI°9=P	U%1P¨¨ƒŠPÍ¡½É•±¥¹”¹•½©Í½¹€èÑ¡”¡…É‰½ÕÈÉ•… °Ñ¡”€ÄàÌĞÕĞ°Ñ¡”½±Í½ÕÑ¡İ…É¡…¹¹•°°Ñ¡”Í…¹‰…È…Ì…¸¥Í±…¹…¹Ñ¡”µ…¥¹±…¹Í¡½É”°€¬ÌÄÓŠ˜¬ÄÔÜÀ½™˜]É¥¡Ğ€ÄàÌĞ¸Y•Ñ½ÉÌ½¹±äì¹¼•±•Ù…Ñ¥½¸°¹¼µ•Í °¹½Ñ¡¥¹œ•…ÍĞ½˜Ñ¡”‰½àÉ•¹‘•ÉÌå•Ğğ)ğ€¨©AÕ‰±¥Í¡•¨¨ğÍ¥Ñ”½¡¥…¼¼Ñ½€€ ÄĞ¸ÌÄ5½˜„€ÈÔ5‰Õ‘•Ğ¤€¬„Ñ¥±”½¸Ñ¡”¡¥…¼±…¹‘¥¹œÁ…”ğ)ğá±ÕÍ¥½¹Ìğ€ÄĞ‘…Ñ”µÕ…É‘•ÍÑÉÕÑÕÉ•Ì€¬„€Ğµ¥Ñ•´İ…Ñ ±¥ÍĞƒŠP€¨©¥¸Ñ¡”İ…±­Ñ¡É½Õ ¨¨Í¥¹”€ÈÀÈØ´Àà´ÄÀ€¡Ù¥‘•¹”Á…¹•°°€‰]¡…Ğ¥Ì¹½Ğ¡•É”ˆ¤°¥Ñ…Ñ¥½¹Ì©½¥¹•°…¹¹½Ü¡•±Ñ¼Ñ¡”Í…µ”¥Ñ…Ñ¥½¸ÉÕ±”…Ì„ÍÑÉÕÑÕÉ”É•½É€£
œ€ÈØ¤ğ((ŒŒ½ÉÉ•Ñ¥½¹Ìµ…‘”…™Ñ•ÈÑ¡”™¥ÉÍĞ±¥Ù”±½½¬()-•Ù¥¸½Á•¹•Ñ¡”‘•Á±½å•‰Õ¥±½¸É•…°¡…É‘İ…É”…¹™½Õ¹Ñİ¼Ñ¡¥¹Ì¡•…‘±•ÍÌÑ•ÍÑ¥¹œ¡…)µ¥ÍÍ•¸	½Ñ …É”™¥á•ì‰½Ñ …É”Ñ¡”­¥¹½˜Ñ¡¥¹œ½¹±ä„É•…°Ù¥•İ•È…Ñ¡•Ì¸((´€¨©Q¡”‰Õ¥±‘¥¹œÉ•¹‘•É•ÁÕÉ”‰±…¬½¸„É•…°AT¸¨¨Q¡”½¹™¥‘•¹”Í¡…‘•È½µÁÕÑ•(€İ•¥¡Ğ€ô˜¡Ù½¹™¥‘•¹”¤€¨Õ½¹™5½‘•€•Ù•¸İ¡•¸Ñ¡”Ù¥•Üİ…ÌÍİ¥Ñ¡•=ƒŠP…¹9…8€¨€À¸Á€(€¥ÌÍÑ¥±°9…9€°İ¡¥ Á½¥Í½¹•‘¥™™ÕÍ•½±½É€Ñ¡É½Õ Ñ¡”µ¥à¸•½µ•ÑÉäÉ•…¡¥¹œ„‰…Ñ (€İ¥Ñ¡½ÕĞ}=9%9€±•…Ù•ÌÑ¡”…ÑÑÉ¥‰ÕÑ”Õ¹‰½Õ¹°…¹…¸Õ¹‰½Õ¹…ÑÑÉ¥‰ÕÑ”¥Ì¹½ĞÉ•±¥…‰±ä(€é•É¼½¸É•…°¡…É‘İ…É”Ñ¡”İ…ä¥Ğ¥ÌÕ¹‘•È„Í½™Ñİ…É”É…ÍÑ•É¥Í•È¸Q¡”¡…¹¹•°¥Ì¹½Ü(€Í…¹¥Ñ¥Í•…ĞÑ¡”Ù•ÉÑ•àÍÑ…”…¹Ñ¡”½™˜Á…Ñ ¥ÌÕ…É‘•‰•™½É”¥ĞÉ•…‘Ì…¹åÑ¡¥¹œ¸(´€¨©İ•±°µ‘½Õµ•¹Ñ•‰Õ¥±‘¥¹œİ…ÌÉ•¹‘•É•…Ì¹•…ÈµÑ½Ñ…°Õ•ÍÍİ½É¬¸¨¨İ…±±}¡•¥¡Ñ}µ€…¹(€É½½™}ÑåÁ•€İ•É”Ñ…•½¹©•ÑÕÉ…±€İ¡¥±”Ñ¡•¥È½İ¸¹½Ñ•Ì…Ù”ÑåÁ½±½¥…°É•…Í½¹¥¹œƒŠP(€€‰Ñİ¼™Õ±°ÍÑ½É¥•Ì…ĞÑåÁ¥…°Á•É¥½™±½½È¡•¥¡Ğˆ°€‰…‰±”¥ÌÑ¡”¹•…ÈµÕ¹¥Ù•ÉÍ…°™½É´™½ÈÑ¡”(€ÑåÁ”…¹Á•É¥½ˆ¸Q¡…Ğ¥ÌÑ¡”‰É¥•˜Ì‘•™¥¹¥Ñ¥½¸½˜¥¹™•ÉÉ•‘€°¹½Ğ½˜½¹©•ÑÕÉ…±€¸]½ÉÍ”°(€Ñ¡”µ…ÍÍ¥¹œÉÕ±”Ñ½½¬Ñ¡”İ½ÉÍĞ½¹™¥‘•¹”…É½ÍÌÑ¡”™½½ÑÁÉ¥¹ĞÑ½¼°Í¼…¸Õ¹­¹½İ¸M%i(€‘¥Ñ¡•É•Ñ¡”•¹Ñ¥É”‰Õ¥±‘¥¹œ¥¹Ñ¼¡½ÍĞµ…ÍÍ¥¹œ¸M¥é”…¹¡…É…Ñ•È…É”‘¥™™•É•¹Ğ­¥¹‘Ì½˜(€¹½Ğµ­¹½İ¥¹œè]…Ôµ	Õ¸‘½Õµ•¹ÑÌ„Ñİ¼µÍÑ½É•äİ¡¥Ñ”™É…µ”‰Õ¥±‘¥¹œİ¥Ñ ‰É¥¡Ğµ‰±Õ”Í¡ÕÑÑ•ÉÌ°(€…¹¹¼Í½ÕÉ”¥Ù•Ì„‘¥µ•¹Í¥½¸¸Q¡”µ…ÍÍ¥¹œ¹½Ü™½±±½İÌÑ¡”…ÑÑÉ¥‰ÕÑ•ÌÑ¡…ĞÍ…äİ¡…ĞÑ¡”(€‰Õ¥±‘¥¹œİ…Ìì‘¥µ•¹Í¥½¹…°Õ¹•ÉÑ…¥¹Ñä¥Ì…ÉÉ¥•¥¸Ñ¡”Í¥‘•…È°İ¡•É”Ñ¡”Á½ÁÕÀÍ¡½İÌ¥Ğ¸(€U¹‘•ÉÍÑ…Ñ¥¹œİ¡…Ğİ”­¹½Ü¥Ì…ÌµÕ „µ¥ÍÉ•ÁÉ•Í•¹Ñ…Ñ¥½¸…Ì½Ù•ÉÍÑ…Ñ¥¹œ¥Ğ¸(´€¨©Q¡”ÁÉ…¥É¥”…ÁÁ•…É•Ñ¼‰”„Í•½¹Ñ•ÉÉ…¥¸±…å•È¸¨¨Q¡”™…ÈÙ••Ñ…Ñ¥½¸Í¥µÁ±¥™¥…Ñ¥½¸İ…Ì(€„Í½±¥¡½É¥é½¹Ñ…°Í¡••Ğ…ĞÁ±…¹ĞµÑ½À¡•¥¡Ğ¸=¸É•…°¡…É‘İ…É”¥Ğ¡¥‰Õ¥±‘¥¹œ™½Õ¹‘…Ñ¥½¹Ì(€…¹Á±…¹ĞÉ½½ÑÌİ¡¥±”Ñ¡”İ…±­•ÈÉ•µ…¥¹•½ÉÉ•Ñ±ä½¸Ñ¡”…ÑÕ…°¡•¥¡Ñ™¥•±‰•±½ÜƒŠPµ½ÍĞ(€±•…É±ä…ĞÑ¡”É¥Ù•È‰…¹¬…¹á¡…¹”½™™•”!½ÕÍ”¸Q¡”Í¡••Ğ¥ÌÉ•µ½Ù•°¹½ĞÁÉ½µ½Ñ•Ñ¼(€Ñ•ÉÉ…¥¸¸]…±­•È°‰Õ¥±‘¥¹Ì°ÍÑÉ••ÑÌ°ÑÉ••Ì…¹‘•Ñ…¥±•™±½É„¹½ÜÍ¡…É”½¹”•áÁ±¥¥ĞÍÕÉ™…”(€Í…µÁ±•Èì•µ•É•¹ĞÉ½½ÑÌÕÍ”Ñ¡”İ…Ñ•ÈÍÕÉ™…”¸Q¡”™…È™¥•±¥ÌÑ•ÉÉ…¥¸Ñ•áÑÕÉ”Õ¹Ñ¥°„(€Á½É½ÕÌ°Ñ•ÉÉ…¥¸µÉ½½Ñ•É•Á±…•µ•¹Ğ…¸‰”‰Õ¥±Ğ€¡0àÀ¤¸((ŒŒ]¡…Ğ‘½•Ì¹½Ğ•á¥ÍĞå•Ğ((´€¨©Q¡”™Õ±°€ØØÔµÉ½½˜¥¹Ù•¹Ñ½Éä¥Ì¹½Ğ‰Õ¥±Ğ¸¨¨M½ÕÑ €ĞàÁ±ÕÌ9½ÉÑ €ØÀ…¹½¹åµ½ÕÌÍ±½ÑÌ…É”Ù¥Í¥‰±”ìÉ•µ…¥¹¥¹œÁ…É•±Ì°½½É‘¥¹…Ñ•İ½É±•áÑ•¹Í¥½¹Ì…¹Ñ¡”€ÌÔµ™…µ¥±ä…¹½¹¥…°…É¡•ÑåÁ”±¥‰É…Éä…É”ÍÑ¥±°½Á•¸¸Q¡”É•½¹¥±¥…Ñ¥½¸…¹™…µ¥±äÉ½ÍÍİ…±¬…É”½µµ¥ÑÑ•¡…¹‘½™˜½¹ÑÉ½±Ì¸(´€¨©9¼Ñ•ÉÉ…¥¸¸¨¨Q¡”Í•¹”ÍÑ…¹‘Ì½¸„™±…ĞÁ±…¹”ìÑ¡”€ÌÀµé½¹”¡•¥¡Ñ™¥•±ÍÁ•Œ•á¥ÍÑÌ¥¸Ñ¡”(€É•Í•…É ‘½ÍÍ¥•È‰ÕĞ¡…Ì¹½Ğ‰••¸ÑÕÉ¹•¥¹Ñ¼‘…Ñ„¸Q¡¥Ì¥ÌÑ¡”¹•áĞÍÑ…”¸(´€¨©9¼™±½É„½È™…Õ¹„É•½É‘Ì¸¨¨Q¡”Á…±•ÑÑ•Ì…¹Ñ¡”Á±…•µ•¹ĞÑ…‰±”•á¥ÍĞ¥¸Ñ¡”‘½ÍÍ¥•ÉÌ½¹±ä¸(´€¨©Q•ÉÉ…¥¸…¹Ñ¡”É¥Ù•È¹½Ü•á¥ÍĞ¨¨°ÑÉ…•™É½´]É¥¡Ğ€ÄàÌĞÑ¡É½Õ Ñ¡”Í…µ”…™™¥¹”Ñ¡…Ğ(€™¥á•Ñ¡”‘…ÑÕ´¸Q½Ñ…°±…¹É•±¥•˜…É½ÍÌÑ¡”İ¡½±”€ØĞÀ´‰½à¥Ì€¨¨Ğ¸ÌÀ™Ğ¨¨ƒŠPÑ¡…Ğ¥Ì¹½Ğ„(€Í¥µÁ±¥™¥…Ñ¥½¸°¥Ğ¥ÌÑ¡”Í¥Ñ”¸Q¡”‘½ÍÍ¥•ÈÌÍÕ•ÍÑ•€ÓŠLáàÙ•ÉÑ¥…°•á…•É…Ñ¥½¸İ…Ì(€É•™ÕÍ•‰•…ÕÍ”¥Ğ½¹ÑÉ…‘¥ÑÌ‘½Ì½A=!L¹µ‘€…¹1%	IQ%L0Ì¸(´€¨©Q¡”‰…¹¬ÁÉ½™¥±”¥ÌÑ¡”±…É•ÍĞÕ¹Í½ÕÉ•…ÍÍÕµÁÑ¥½¸¥¸Ñ¡”‰Õ¥±¸¨¨9¼é½¹”¥¸Ñ¡”Ñ•ÉÉ…¥¸(€‘½ÍÍ¥•È¥Ù•Ì„‰…¹¬€©ÁÉ½™¥±”¨…Ğ…±°ìÑ¡”€Ø´™…”…¹¥ÑÌ•…Í”µ½ÕĞÍ¡…Á”İ•É”¡½Í•¸Á…ÉÑ±ä(€‰•…ÕÍ”„™±…ĞÑ½”±•…Ù•ÌÑ¡”hôÀ½¹Ñ½ÕÈƒŠPİ¡¥ %LÑ¡”‘É…İ¸İ…Ñ•É±¥¹”ƒŠP¥±°µ½¹‘¥Ñ¥½¹•(€……¥¹ÍĞÑ¡”É¥¸(´€¨©¡¥…½…É¡¥Ñ•ÑÕÉ•¡¥ÍÑ½Éä¹½µ€¥Ñ•Ì¹½Ñ¡¥¹œ¨¨™½ÈÑ¡”Ñİ¼‰•ÍĞ•±•Ù…Ñ¥½¸™¥ÕÉ•Ì¥¸Ñ¡”(€‘½ÍÍ¥•È°İ¡¥ ¥Ìİ¡ä¹¼±…¹•±•Ù…Ñ¥½¸¥¸Ñ¡¥Ì‰Õ¥±¥ÌÑ…•‘½Õµ•¹Ñ•‘€¸(´€¨©A±…•µ•¹Ğ¥ÌÉ•…°‰ÕĞ½…ÉÍ”¸¨¨±°•¥¡ĞÍÑÉÕÑÕÉ•Ì¹½Ü…ÉÉäÍÕÉÙ•å•½½É‘¥¹…Ñ•ÌÉ…Ñ¡•È(€Ñ¡…¸¹Õ±±Ì°…Ğ…‰½ÕĞƒ
ÄÈÀ´ƒŠPÑ¡”•½É•™•É•¹”Ì•ÉÉ½È°¹½Ğ…¸…‘‘¥Ñ¥½¹…°Õ•ÍÌ¸Q¡É•”½˜Ñ¡•´(€€¡]½±˜A½¥¹ĞQ…Ù•É¸°5¥±±•È!½ÕÍ”°]…±­•ÈÌµ••Ñ¥¹œ¡½ÕÍ”¤¡…Ù”¹¼ÍÕÉÙ¥Ù¥¹œ¥¹Ñ•ÉÍ•Ñ¥½¸…¹(€…É”‘•É¥Ù•™É½´Ñ¡”½¹™±Õ•¹”…¹Ñ¡”µ½‘•É¸‰…¹¬°İ¥Ñ „±…É•È…¹‘¥™™•É•¹Ñ±äÍ¡…Á•(€Õ¹•ÉÑ…¥¹ÑäÍÑ…Ñ•½¸•… ¸(´€¨©]…±­•ÈÌµ••Ñ¥¹œ¡½ÕÍ”µ…ä‰”Ñ¡”İÉ½¹œ‰Õ¥±‘¥¹œ¸¨¨Q¡”İ•ÍĞµ‰…¹¬Ñ•ÍÑ¥µ½¹ä‘•ÍÉ¥‰•Ì€ÄàÌÄ(€…¹Ñ¡”¹½ÉÑ µ‰…¹¬±…¥´¥Ì‘…Ñ•€ÄàÌĞ°İ¡¥ ¥Ìİ¡…Ğå½Ôİ½Õ±Í•”¥˜Ñ¡”Í½ÕÉ•Ì‘•ÍÉ¥‰”(€Ñİ¼‘¥™™•É•¹Ğ‰Õ¥±‘¥¹Ì…‰½ÕĞ€ÄÔÀ´…Á…ÉĞ…É½ÍÌ„É¥Ù•È¸A½Í¥Ñ¥½¸¥ÌÑ…•½¹©•ÑÕÉ…±€(€…¹Ñ¡”É•½ÉÍ…åÌÍ¼¥¸Ñ¡”™¥ÉÍĞ±¥¹”¸((ŒŒQ¡”‘…ÑÕ´¥ÌÙ•É¥™¥•()‘…Ñ„½‘…ÑÕ´¹©Í½¹€¹½Ü…ÉÉ¥•ÌÙ•É¥™¥•èÑÉÕ•€è€¨©€ĞĞÜÀÜÈ¸Ü°8€ĞØÌÜÌäÔ¸à€¡AMèÈØäÄØ¤€ô(ĞÄ¸ààØÜÈÄ°€´àÜ¸ØÌÜäÔÄ¨¨ƒŠPÑ¡”™½É­Ì©Õ¹Ñ¥½¸…Ì‘É…İ¸½¸]É¥¡Ğ€ÄàÌĞ°™¥ÑÑ•……¥¹ÍĞ•¥¡Ğ)µ½‘•É¸½¹ÑÉ½°Á½¥¹ÑÌ€¡I5L€ÄÜ¸Ô´¤°É½ÍÌµ¡•­•……¥¹ÍĞ…¸¥¹‘•Á•¹‘•¹Ñ±ä•½É•™•É•¹•)!…Ñ¡…İ…ä€ ÔÜ¸ä´…É••µ•¹Ğ¤…¹Ñ¡”µ½‘•É¸=M4É¥Ù•È©Õ¹Ñ¥½¸€ Ìä¸Ğ´¤¸Q¡”‰É¥•˜ÌÁ±…•¡½±‘•È)İ…Ì€¨¨ÈÀÌ´½™˜¨¨¸Õ±°µ•µ¼è‘½Ì½IMI ½‘…ÑÕµ}‘•É¥Ù…Ñ¥½¸¹µ‘€ìÑ¡”‘•É¥Ù…Ñ¥½¸É”µÉÕ¹Ì™É½´)½µµ¥ÑÑ•ÑÉ…•ÌÙ¥„Ñ½½±Ì½É•‘•É¥Ù•}‘…ÑÕ´¹Áå€°İ¡¥ ¡•¬¹Í¡€•¹™½É•Ì¸()MÑÉÕÑÕÉ”Á½Í¥Ñ¥½¹ÌÍÑ¥±°…ÉÉäÍåµ‰½±¥}±½…Ñ¥½¹€İ¥Ñ ¹Õ±°½½É‘¥¹…Ñ•ÌƒŠPÑ¡•ä•Ğ™¥±±•…Ì)™½½ÑÁÉ¥¹ÑÌ…É”ÑÉ…•Ñ¡É½Õ Ñ¡”™¥ÑÑ•ÑÉ…¹Í™½ÉµÌ¥¸LÈ¬°•… …ÉÉå¥¹œÑ¡”ƒ
ÄÈÀ´İ½É­¥¹œ)Õ¹•ÉÑ…¥¹Ñä½˜Ñ¡”€ÄàÌĞÍ¡••ÑÌ¥¸¥ÑÌ¹½Ñ”¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”¡…¹•±½œİ…Ì‰É½­•¸	d5I°…¹‰½Ñ Á…É•¹ÑÌİ•É”É••¸((¨©É•¹‘•É•ÉÌ½İ•ˆ½©Ì½¡…¹•±½œ¹©Í€‘¥¹½ĞÁ…ÉÍ”½¸µ…¥¹€°…¹¹•¥Ñ¡•È‘¥¥ÑÌÁÕ‰±¥Í¡•)µ¥ÉÉ½È¸¨¨Q¡”]¡…ĞÌµ¹•ÜÑ…ˆ¥µÁ½ÉÑÌ¥Ğ°Í¼Ñ¡”Ñ…ˆİ…Ì‘•…½¸Ñ¡”‘•Á±½å•Í¥Ñ”ì5…¹…•È…¹)Ñ¡”Á½±•…Ğ¹±¥Ù”±…Õ¹¡•ÈÁ…ÉÍ”Ñ¡”µ¥ÉÉ½È°Í¼Ñ¡¥ÌÁÉ½©•ĞÉ•Á½ÉÑ•¹¼É•±•…Í•Ì…Ğ…±°¸€ØĞ)•¹ÑÉ¥•Ì°‰…¬Ñ¼Ñ¡”™¥ÉÍĞ‰Õ¥±‘¥¹œ°İ•É”¥¸Ñ¡”™¥±”…¹É•…¡¥¹œ¹½‰½‘ä¸((¨©á…Ñ±ä½¹”tô±€İ…Ìµ¥ÍÍ¥¹œ¨¨ƒŠPÑ¡”Ñ•Éµ¥¹…Ñ½È½˜ØØĞ€¨‰Qİ•¹ÑäµÑ¡É•”‰Õ¥±‘¥¹Ìİ•É”ÍÑ…¹‘¥¹œ)¥¸Ñ¡”ÍÑÉ••Ğˆ¨¸Ù•Éä•¹ÑÉä‰•±½Ü¥Ğİ…Ì¹•ÍÑ•¥¹Í¥‘”Ñ¡…Ğ•¹ÑÉäÌ¥Ñ•µÍ€…ÉÉ…ä°İ¡¥ ¥Ìİ¡ä)¹½‘”É•Á½ÉÑ•Ñ¡”Íå¹Ñ…à•ÉÉ½È…Ğ±¥¹”€ÔØÔ°Ñ¡”•¹½˜Ñ¡”™¥±”°€ÔĞÀ±¥¹•Ì™É½´Ñ¡”‘…µ…”¸)Í•½¹•¹ÑÉäÉ½‘”…±½¹œİ¥Ñ „‘ÕÁ±¥…Ñ”Øè€ØÑ€èÑİ¼‰É…¹¡•Ì™¥¹¥Í¡•€ÌÌµ¥¹ÕÑ•Ì…Á…ÉĞ°•… )ÍÑ…µÁ•¥ÑÌ•¹ÑÉä½¸¥ÑÌ½İ¸‰É…¹ °…¹¹•¥Ñ¡•È­¹•ÜÑ¡”¹Õµ‰•Èİ…ÌÑ…­•¸¸((¨©Q¡”µ•¡…¹¥Í´¥ÌÑ¡”Á…ÉĞİ½ÉÑ ­••Á¥¹œ°‰•…ÕÍ”¹¼•á¥ÍÑ¥¹œ…Ñ”½Õ±¡…Ù”…Õ¡Ğ¥Ğ¸¨¨)€¹¥Ñ…ÑÑÉ¥‰ÕÑ•Í€µ•É•ÌÑ¡¥Ì™¥±”İ¥Ñ µ•É”õÕ¹¥½¹€ƒŠP„‘•±¥‰•É…Ñ”°‘½Õµ•¹Ñ•¡½¥”°‰•…ÕÍ”)Ñİ¼‰É…¹¡•Ì•… ÁÉ•Á•¹‘¥¹œ…¸•¹ÑÉä½±±¥‘”•Ù•ÉäÑ¥µ”…¹Õ¹¥½¸­••ÁÌ‰½Ñ ¥¹ÍÑ•…½˜)½¹™±¥Ñ¥¹œ¸	ÕĞÑ¡”Õ¹¥½¸‘É¥Ù•ÈÉÕ¹ÌUI%9Q!5I¸5•É”€ØÕŒá‘”Å€¡…ÌÑİ¼Á…É•¹ÑÌ°)‰”ĞäÑ€…¹€ØÁ„ÜáÁ€ì€¨©‰½Ñ Á…ÉÍ”°…¹Ñ¡”µ•É”½˜Ñ¡•´‘½•Ì¹½Ğ¸¨¨Ù•Éä…Ñ”¥¸Ñ¡¥Ì)ÁÉ½©•ĞÉÕ¹Ì½¸„½µµ¥ĞÍ½µ•‰½‘äİÉ½Ñ”¸9½Ñ¡¥¹œÉ…¸½¸Ñ¡”½µµ¥Ğ¥ĞİÉ½Ñ”¸((´€¨©Q¡”É•Á…¥È¸¨¨Q¡”Ñ•Éµ¥¹…Ñ½È¥ÌÉ•ÍÑ½É•¸Q¡”‘ÕÁ±¥…Ñ••¹ÑÉä¥Ì¹½Ü€¨©ØØÜ¨¨…¹Í¥ÑÌ…ĞÑ¡”(€Ñ½À°İ¡•É”¥ÑÌ½İ¸ÑÍ€€ ÄÈèÈØUQ°Ñ¡”¹•İ•ÍĞ¥¸Ñ¡”™¥±”¤Í…åÌ¥Ğ‰•±½¹Ì¸9¼•¹ÑÉä…¹å½¹”¡…Ì(€É•…İ…ÌÉ•¹Õµ‰•É•ƒŠPİ¡¥±”Ñ¡”™¥±”İ…Ì‰É½­•¸°¹¼•¹ÑÉäİ…ÌÉ•…‘…‰±”…Ğ…±°¸(´€¨©Ñ½½±Ì½¡•¬¹Í¡€¹½ÜÉÕ¹ÌÑ¡”¡…¹•±½œ½¹ÑÉ…Ğ¨¨°…Ì„ÍÑ•À±¥­”…¹ä½Ñ¡•È¸9QL¹µ¡…Ì(€…±İ…åÌ¥¹ÍÑÉÕÑ•…¸…•¹ĞÑ¼ÉÕ¸¡•¬µ¡…¹•±½œ¹µ©Í€‰ä¡…¹‰•™½É”µ•É¥¹œì„¡…¹µÉÕ¸¡•¬(€¥Ì•á…Ñ±äÑ¡”Ñ¡¥¹œ„µ•É”µÑ¥µ”½ÉÉÕÁÑ¥½¸•Ù…‘•Ì°…¹Ñ¡”™¥±”Ñ¡…Ğ…Ñ•Ì•Ù•Éä½µµ¥Ğ‘¥(€¹½Ğ…Ñ”Ñ¡¥Ì½¹”¸Q¡”•¹•É¥Œ€©É•¹‘•É•Èµ½‘Õ±•ÌÁ…ÉÍ”¨ÍÑ•À‘¥…Ñ ¥ĞƒŠP…ÌÁ…ÉÍ”•ÉÉ½Èè(€É•¹‘•É•ÉÌ½İ•ˆ½©Ì½¡…¹•±½œ¹©Í€°İ¡¥ ¹…µ•Ì„™¥±”…¹¹½Ğ„‘•™•Ğ¸(´€¨©Q¡”½¹ÑÉ…Ğ¡•¬É•…‘ÌÑ¡”±¥Ñ•É…°ÌM!A…ÌÑ•áĞ‰•™½É”•á•ÕÑ¥¹œ¥Ğ¨¨°‰•…ÕÍ”•á•ÕÑ¥¹œ(€¥Ğ¥ÌÑ¡”İ•…­•ÈÑ•ÍĞ¥¸Ñİ¼İ…åÌ¸Íİ…±±½İ••¹ÑÉä¥ÌÍÑ¥±°„Ù…±¥½‰©•Ğ±¥Ñ•É…°°Í¼¥Ğ¹••(€¹½ĞÉ…¥Í”„Íå¹Ñ…à•ÉÉ½È…Ğ…±°ƒŠP¥Ğ…¸Í¥µÁ±äÙ…¹¥Í ™É½´Ñ¡”…ÉÉ…äİ¥Ñ Ñ¡”™¥±”±½…‘¥¹œ(€±•…¹±ä¸¹5…¹…•È…¹Ñ¡”±…Õ¹¡•È¹•Ù•È•á•ÕÑ”Ñ¡¥Ì™¥±”ìÑ¡•äİ…±¬¥Ğ‰É…­•Ğµ…İ…É”°Í¼(€Ñ¡”Í¡…Á”%LÑ¡”½¹ÑÉ…Ğ¸Ù•Éä•¹ÑÉäµÕÍĞ½Á•¸…Ğ‰É…­•Ğ‘•ÁÑ €Äì½¹”Ñ¡…Ğ½Á•¹Ì‘••Á•È½Ğ(€Íİ…±±½İ•°…¹Ñ¡”•¹ÑÉä…‰½Ù”¥Ğ¥ÌÑ¡”½¹”Ñ¡…Ğ±½ÍĞ¥ÑÌÑ•Éµ¥¹…Ñ½È¸Y•É¥™¥•……¥¹ÍĞÑ¡”É•…°(€½ÉÉÕÁÑ•™¥±”™É½´µ…¥¹€è€¨‰±¥¹”€ÈÔè•¹ÑÉäØØĞ½Á•¹Ì…Ğ‰É…­•Ğ‘•ÁÑ €Ì°¹½Ğ€ÄƒŠP¥Ğ¥Ì¹•ÍÑ•(€¥¹Í¥‘”•¹ÑÉäØØĞ€¡±¥¹”€Äà¤°İ¡¥ ¥Ìµ¥ÍÍ¥¹œ¥ÑÌtô±€ˆ¨¸Q¡”¡•…‘•È½Õ¹Ğ™É½´Ñ¡”Ñ•áĞİ…±¬(€¥Ì…±Í¼½µÁ…É•……¥¹ÍĞ!91=¹±•¹Ñ¡€°İ¡¥ ¥Ìİ¡…Ğ…Ñ¡•ÌÑ¡”Í¥±•¹Ğ¡…±˜¸(´€¨©]¡…ĞÑ¡¥ÌÍÑ¥±°‘½•Ì¹½Ğ½Ù•È¸¨¨Q¡”¡•¬¹½ÜÉÕ¹Ì‰•™½É”•Ù•Éä½µµ¥Ğ…¹‰•™½É”•Ù•Éä(€µ•É”…¸…•¹ĞÁ•É™½ÉµÌ°‰ÕĞ¹½Ñ¡¥¹œ¥¸Ñ¡¥ÌÍÕ‰ÑÉ•”ÉÕ¹Ì½¸„µ•É”½µµ¥Ğ¥ÑÍ•±˜ƒŠPÑ¡”(€É•Á½Í¥Ñ½ÉäÌ$¥Ì½ÕÑÍ¥‘”¡¥…¼¼Ñ‘€…¹½ÕÑÍ¥‘”Ñ¡¥Ì±…¹”ÌÍ½Á”¸¡Õµ…¸µ•É”½¸¥Ñ!Õˆ(€…¸ÍÑ¥±°ÁÕ‰±¥Í „Õ¹¥½¸µ½ÉÉÕÁÑ•¡…¹•±½œ¸Q¡”¹…ÉÉ½ÜÙ•ÉÍ¥½¸½˜Ñ¡…Ğ¡…é…É¥Ì¹½Ü±½Õ(€Ñ¡”µ½µ•¹Ğ…¹å½¹”ÉÕ¹ÌÑ¡”…Ñ”ìÑ¡”•¹•É…°Ù•ÉÍ¥½¸¥ÌÉ•½É‘•¥¸I=5@ƒ
œ,ÄÈ¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”¡½É¥é½¸Ñ¥µ‰•Èİ…Ì‰•¥¹œ‘•±•Ñ•‰ä¥ÑÌ½İ¸Ñ•áÑÕÉ”((¨©LÙ„¥Ñ•´€Ô°‰½Ñ µ•¡…¹¥ÍµÌÑ¡”¥Ñ•´¹…µ•Ì¸¨¨Q¡”™…ÈµÑ¥µ‰•È‰…¹‘É…İÌÑ¡”‘½ÍÍ¥•ÈÌ‰½‘¥•Ì)½˜İ½½‘Ì…ĞÑ¡É•”°™½ÕÈ…¹Í¥àµ¥±•Ì…Ì„Í¥±¡½Õ•ÑÑ”½¸„É¥¹œ°‰É½­•¸ÕÀÉ½İ¸‰äÉ½İ¸İ¥Ñ )Í­ä½Á•¹•Ñ¡É½Õ Ñ¡”ÍÑ…¹ƒŠP­€ÉÕ¹Ì‘½İ¸Ñ¼…‰½ÕĞ€À¸ÀÈ¥¸„…À¸Ğ™½ÕÈ¡Õ¹‘É•µ•ÑÉ•Ì°)İ¡•É”Ñ¡”‰…¹¥Ì™½ÉÑäÁ¥á•±ÌÑ…±°°Ñ¡…Ğ¥ÌÑ•áÑÕÉ”¸=¸„Í¥àµµ¥±”‰½‘äİ¡½Í”•¹Ñ¥É”Í¥±¡½Õ•ÑÑ”)¥Ì½¹”½ÈÑİ¼Á¥á•±Ì¥Ğ¥Ì„€¨©‘•±•Ñ¥½¸¨¨°…¹Ñ¡”‰…¹İ…Ì…ÉÉå¥¹œ‰½Ñ ™…¥±ÕÉ•Ì…Ğ½¹”¸((´€¨©5•…ÍÕÉ•…ĞÑ¡”ÍÁ…İ¸ÍÑ…Ñ¥½¸°İ¥Ñ Ñ¡”Á¥á•°™±½½ÈÉ•µ½Ù•…¹Ñ¡•¸¥¸Á±…”¸¨¨€ÈàÄ½˜€äÀÀ(€‰•…É¥¹Ì…ÉÉä„Ñ¥µ‰•È‰½‘ä¸]¥Ñ¡½ÕĞÑ¡”™±½½ÈÑ¡”µ½‘Õ±…Ñ¥½¸‘É•Ü€¨¨ÈÔÄ½˜€ÈàÀ¨¨É•Í½±Ù…‰±”(€‰•…É¥¹Ì…Ğ„Á¥á•°½Èµ½É”½¸Ñ¡”Á¡½¹”…¹€¨¨ÈØÜ½˜€ÈàÄ¨¨½¸Ñ¡”‘•Í­Ñ½ÀƒŠPİ½ÉÍĞÍ¥±¡½Õ•ÑÑ”(€€¨¨À¸ÄàÁà¨¨…¹€¨¨À¸ÌÄÁà¨¨°•½µ•ÑÉäÍ½±Ù•…¹İÉ¥ÑÑ•¸¥¹Ñ¼Ñ¡”‰Õ™™•È…¹Ñ½¼Ñ¡¥¸Ñ¼±…¹(€…¹åİ¡•É”¸]¥Ñ ¥Ğè€¨¨ÈàÀ¼ÈàÀ…¹€ÈàÄ¼ÈàÄ¨¨°İ½ÉÍĞ€¨¨Ä¸ÀÀÁà¨¨¸Q¡”‰…¹ÌÑÉ¥…¹±”½Õ¹Ğ¥Ì(€€¨¨ÔØÈ°Õ¹¡…¹•¨¨ƒŠPÑ¡”™±½½Èµ½Ù•ÌÙ•ÉÑ¥•Ì…¹¹•Ù•ÈÑ¡•¥È¹Õµ‰•È¸(´€¨©Q¡”™±½½È¥Ì½¸Ñ¡”IMU1P°¹½Ğ„…À½¸­€¨¨°Í¼¥Ğ‰¥¹‘Ì½¹±äİ¡•É”Á¥á•±Ì…É”Í…É”è„(€€ĞÀÀ´ÑÉ••±¥¹”¥Ì€ĞÀÁàÑ…±°…¹­••ÁÌ¥ÑÌ…ÁÌÑ¼Ñ¡”±…ÍĞÁ•È•¹Ğ¸]¡•É”„‰½‘äÌÉ…Ü(€Í¥±¡½Õ•ÑÑ”¥Ì¥ÑÍ•±˜ÍÕˆµÁ¥á•°Ñ¡”µ½‘Õ±…Ñ¥½¸¥ÌÍÕÁÁÉ•ÍÍ•½ÕÑÉ¥¡Ğ°‰•…ÕÍ”„Ñ•áÑÕÉ”Ñ¡…Ğ(€…¹¹½Ğ‰”‘É…İ¸…¸½¹±äÍÕ‰ÑÉ…Ğ¸(´€¨©Q¡”‰…¹¥ÌÑ¡•É•™½É”¹½ÜÍ½±Ù•……¥¹ÍĞÑ¡”±¥Ù”Ù¥•İÁ½ÉĞ¸¨¨µ…¥¸¹©Í€Á…ÍÍ•Ì(€Á¥á•±ÍA•ÉI…‘¥…¹€½™˜Ñ¡”É•¹‘•É•ÈÍ¥é”…¹Ñ¡”…µ•É„Ì½İ¸™¥•±ƒŠP€ĞÜÔÁà½É…½¸„Á¡½¹”…Ğ(€¥ÑÌ€äÓ
À±…µÀ……¥¹ÍĞ€àÌÌÁà½É…½¸„‘•Í­Ñ½À…Ğ€Ô×
À°„™…Ñ½È½˜€Ä¸ÜÔÑ¡”½±™¥á•™¥•±½Ğ(€İÉ½¹œ¥¸Ñ¡”‘¥É•Ñ¥½¸Ñ¡…Ğ½Ù•ÈµÕÑÌ„Á¡½¹”¸Ù¥•İÁ½ÉĞ¡…¹”É”µÍ½±Ù•ÌÑ¡”‰…¹•á…Ñ±ä…Ì(€İ…±­¥¹œ‘½•Ì¸(´€¨©Q¡”½±½ÕÈİ…Ì½¹”±¥¹”½˜…É¥Ñ¡µ•Ñ¥Œ…¹Íİ•É¥¹œ„ÅÕ•ÍÑ¥½¸Ñ¡”É•¹‘•É•È¹•Ù•È…Í­Ì¸¨¨(€¡…é•¥ÍÁ±…å1¥¹•…È ¥€É…¸Ñ¡”¡…é”½±½ÕÈÑ¡É½Õ LÑ¼É•… Ñ¡”‰…¹Ì‘¥ÍÁ±…äÙ…±Õ”¸Q¡”(€‰…¹¥ÌÑ½¹•5…ÁÁ•è™…±Í”°™½œè™…±Í•€ƒŠP¥ÑÌ™É…µ•¹Ğ¥Ì½Á…ÅÕ”ƒŠH½±½ÉÍÁ…•€°Í¼„±¥¹•…È(€Ù•ÉÑ•à½±½ÕÈ‘¥ÍÁ±…åÌ…ÌÑ¡”¡•à¥Ğ‘•½‘•Ì™É½´ƒŠPİ¡¥±”Ñ¡”™½•É½Õ¹¥Ì(€½Á…ÅÕ”ƒŠHÑ½¹•µ…ÁÁ¥¹œƒŠH½±½ÉÍÁ…”ƒŠH™½€İ¥Ñ ™½½±½É€ÕÁ±½…‘•¥¸Ñ¡”=UQAUP½±½ÕÈÍÁ…”°(€½¹Ù•É¥¹œ½¸Ñ¡…ĞÍ…µ”±¥Ñ•É…°¡•à¸=¹”‘•½‘”•… ¸Q¡”Ñ½¹”ÕÉÙ”İ…Ì…ÁÁ±¥•Ñ¼½¹”•¹(€…¹Ñ¼¹½Ñ¡¥¹œ¥Ğ¡…Ñ¼µ…Ñ è€¨¨ÄØÉ•…¹€ÄÈÉ••¸¨¨½™˜Ñ¡”É½Õ¹¥ĞÑ½Õ¡•Ì°€Øä¥¸‰±Õ”(€…ĞÁÉ…¥É¥•}İ•ÍÑ€¸	½Ñ •¹‘ÌÉ•Á½ÉĞ€¨¨Œàá„ÍŒÀ¨¨¹½Ü¸¹Ñ¡”½±Ù…±Õ”İ…Ì€¨©0€ÄÜÀ……¥¹ÍĞ„(€¡½É¥é½¸Í­ä½˜0€ÄØÈ¨¨ƒŠP„‰…¹€©Á…±•È¨Ñ¡…¸¥ÑÌ½İ¸Í­ä°İ¡¥ ¥Ìİ¡…Ğ„‘¥ÍÑ…¹ĞÑÉ••±¥¹”(€¹•Ù•È¥Ìì¥Ğ¥Ì0€ÄÔä¹½Ü°Ñ¡É•”‰•±½Ü¸(´€¨©Q¡”…Ñ”¥Ì•Ù•ÉäÉ•Í½±Ù…‰±”‰•…É¥¹œ°¹½Ğ„Á•É•¹Ñ…”¸¨¨€äÀ€”‰…Èİ½Õ±¡…Ù”Á…ÍÍ•Ñ¡”(€‘•Í­Ñ½À¡…±˜½˜Ñ¡”‘•™•Ğ€ ÈØÜ¼ÈàÄ¥Ì€äÔ€”¤¸Q¡É•”¹•Ü…ÍÍ•ÉÑ¥½¹Ì…Ğ‰½Ñ Ù¥•İÁ½ÉÑÌèÑ¡”‰…¹(€…¹Í•¹”¹™½œ¹½±½É€…É”½¹”½±½ÕÈ°¹¼É•Í½±Ù…‰±”‰•…É¥¹œ¥Ì‘É…İ¸Õ¹‘•ÈÑ¡”™±½½È°…¹Ñ¡”(€‰…¹İ…ÌÍ½±Ù•……¥¹ÍĞQ!%LÙ¥•İÁ½ÉĞƒŠP„™±½½Èµ•…ÍÕÉ•¥¸Á¥á•±Ì¥Ìµ•…¹¥¹±•ÍÌ……¥¹ÍĞ„(€¡…Éµ½‘•™¥•±¸Y•É¥™¥•Ñ¡•ä‰¥Ñ”‰äÉ•µ½Ù¥¹œÑ¡”™±½½Èè‰½Ñ Ù¥•İÁ½ÉÑÌ™…¥°°İ¥Ñ Ñ¡”(€½Õ¹ÑÌ…¹Ñ¡”İ½ÉÍĞÁ¥á•°¹…µ•¸(´€¨©]¡…ĞÑ¡¥Ì‘½•Ì9=P±…¥´¸¨¨Q¡”™¥¹‘¥¹œ‰•¡¥¹¥Ñ•´€Ô¥ÌÁ¡½Ñ½É…Á¡¥ŒƒŠP€¨ÌÄ€”½˜¡½É¥é½¸(€½±Õµ¹Ì…ÉÉä…¹äÑ¥µ‰•È°€Ì¸Ø€”…É½ÍÌÑ¡”•¹ÑÉ…°Ñİ¼µÑ¡¥É‘Ì¨ƒŠP…¹¥Ğİ…ÌÑ…­•¸İ¥Ñ „Í¡½Ğ(€¡…É¹•ÍÌÑ¡…Ğ¥Ì¹½Ğ¥¸Ñ¡”É•±•…Í”…Ñ”¸€¨©%Ğ¡…Ì¹½Ğ‰••¸É”µµ•…ÍÕÉ•¨¨°Í¼¹¼½±Õµ¸™¥ÕÉ”(€¥ÌÅÕ½Ñ•¡•É”¸]¡…Ğ¥Ìµ•…ÍÕÉ•¥ÌÑ¡…ĞÑ¡”•½µ•ÑÉä¥Ğİ…Ìµ•…ÍÕÉ¥¹œ¥Ì¹¼±½¹•È‰•¥¹œ(€Ñ¡É½İ¸…İ…ä°…¹Ñ¡…ĞÑ¡”‰…¹¥Ì‘…É­•ÈÑ¡…¸¥ÑÌÍ­äÉ…Ñ¡•ÈÑ¡…¸Á…±•È¸‘½Ì½1%	IQ%L¹µ‘€(€0ÌÔ¥ÌÉ•Ù¥Í•¥¸‰½Ñ ‘¥É•Ñ¥½¹ÌìÑ¡”€À¸àÈ¡…é”…À¥Ğ•á¥ÍÑÌÑ¼½¹™•ÍÌ¥ÌÕ¹Ñ½Õ¡•°…¹(€Ñ¡”‘¥ÍÑ…¹”½µÁÉ•ÍÍ¥½¸¥Ğ‰ÕåÌ¥ÌÕ¹¡…¹•¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”Íİ…É•¹‘•½¸„ÍÑÉ…¥¡Ğ±¥¹”°…¹Ñ¡”±¥¹”İ…Ì…É¥Ñ¡µ•Ñ¥Œ((¨©É¥¹œ¥Ì„¥É±”…‰½ÕĞÑ¡”İ…±­•È°Í¼¥ÑÌ½ÕÑ•È•‘”¥Ì„½¹ÍÑ…¹ĞÍÉ••¸É½Ü¸¨¨Q¡”)Ñ¡É•”µÉ¥Ñ¥ŒÁÉ…¥É¥”Íİ••Àµ•…ÍÕÉ•¥Ğ…¹¹…µ•Ñ¡”É½ÜèQU9¹µ¥¹É…‘¥ÕÌ€ô€ÈÜ¸Á€ÁÉ•‘¥Ñ•É½Ü(ĞĞà¸à…¹Ñ¡”™É…µ”Í¡½İ•½¹”…Ğ€ĞÔÀ°ÍÑÉ…¥¡Ğ…É½ÍÌ…±°€ÄÈàÀ½±Õµ¹Ì¸Q¡…Ğ¥ÌI=5@ƒ
œLÙ„)¥Ñ•´€Ì°…¹Ñ¡”É•…Í½¸¥Ğ¥Ì…É¥Ñ¡µ•Ñ¥ŒÉ…Ñ¡•ÈÑ¡…¸„É•¹‘•É¥¹œ…ÉÑ•™…Ğ¥ÌÑ¡”Í¥Ñ”è€Ğ¸ÌÀ™Ğ½˜)É•±¥•˜…É½ÍÌÑ¡”İ¡½±”€ØĞÀ´‰½à°Í¼„™¥á•‘¥ÍÑ…¹”É•…±±ä‘½•Ì±…¹½¸„™¥á•É½Ü¸Q¡”…Ñ”)¹½Üµ•…ÍÕÉ•Ì¥ĞÑ¡”İ…äÑ¡”™¥¹‘¥¹œİ…ÌÍÑ…Ñ•ƒŠP‰¥¸Ñ¡”Ù¥•Ü‰ä‰•…É¥¹œ°…Í¬•… ‰¥¸¡½Ü™…È)¥ÑÌ½İ¸Íİ…ÉÉ•…¡•Ì°½¹Ù•ÉĞÑ¡”‘¥ÍÑ…¹”Ñ¼Ñ¡”É½Ü¥Ğ±…¹‘Ì½¸¸€¨©=¸Ñ¡”É¥¹œ…Ì¥ĞÍÑ½½)Ñ¡½Í”É½İÌÍÁ…¹¹•€Ä¸ĞÁà¸¨¨()Ù•Éä±…ÑÑ¥”Í±½Ğ¹½Ü…ÉÉ¥•Ì¥ÑÌ½İ¸½ÕÑ•ÈÉ…‘¥ÕÌèÑ¡”±…å•ÈÌ¹½µ¥¹…°½¹”Á±ÕÌ„)İ½É±µ…¹¡½É•½™™Í•Ğ½˜ÕÀÑ¼€¨«
ÄÌ´¨¨…Ğ™Õ±°‘•Ñ…¥°€£
ÄÄ¸Ø´½¸„Á¡½¹”°…‰½ÕĞ…¸•¥¡Ñ ½˜Ñ¡”)É¥¹œ…Ğ•Ù•Éä‘•Ñ…¥°Í•ÑÑ¥¹œ¤°™É½´Íµ½½Ñ €Ğ´Ù…±Õ”µ¹½¥Í”±½‰•Ìİ¥Ñ „Á•ÈµÍ±½Ğ‘¥Ñ¡•È½Ù•È)Ñ¡•´¸5•…ÍÕÉ•…™Ñ•Èè€¨¨Ô¸äÁà¨¨½˜ÍÁÉ•……Ğ€ÄÈàÃ\àÀÀ…¹€¨¨ÄÜ¸ĞÁà¨¨…Ğ€ÌäÃ\ÜàÀ°Ñ¡”Íİ…É)É•…¡¥¹œ€ÈÔ¸ÃŠLÈà¸Ğ´…‰½ÕĞ„¹½µ¥¹…°€ÈØ¸Ğ¸((´€¨©]¥‘•¹¥¹œÑ¡”™…‘”İ½Õ±¹½Ğ¡…Ù”İ½É­•°…¹Ñ¡”É•…Í½¸¥Ìİ½ÉÑ ­••Á¥¹œ¸¨¨Q¡”‰…¹¥Ì(€…±É•…‘ä€Ü´°İ¡¥ ¥Ì€ÄàÁà½˜™É…µ”…ĞÑ¡…Ğ‘¥ÍÑ…¹”¸Q¡”±¥¹”¥Ì¹½ĞÑ¡”É…µÀƒŠP¥Ğ¥Ìİ¡•É”(€Ñ¡”É…µÀÉ•…¡•Ìé•É¼°…¹„İ¥‘•ÈÉ…µÀÍÑ¥±°É•…¡•Ìé•É¼•Ù•Éåİ¡•É”…Ğ½¹”¸]¡…ĞÉ•µ½Ù•Ì„(€±¥¹”¥Ì„‰½Õ¹‘…ÉäÑ¡…Ğ¥Ì¥¸„‘¥™™•É•¹ĞÁ±…”¥¸•… ‘¥É•Ñ¥½¸¸(´€¨©%Ğ¥Ì¹•…É±ä™É•”°‰ä½¹ÍÑÉÕÑ¥½¸É…Ñ¡•ÈÑ¡…¸‰ä±Õ¬¸¨¨QÉ¥…¹±•Ì…É”Á…¥™½È‰äÑ¡”(€1QQ%°¹½Ğ‰äÑ¡”™…‘”°Í¼„Í±½ĞÑ¡”™É¥¹”ÁÕÍ¡•Ì‰•å½¹É•… ¥Ì‘É½ÁÁ•…ĞÉ•‰Õ¥±(€¥¹ÍÑ•…½˜‘É…İ¸…Ğé•É¼¡•¥¡Ğ°…¹Ñ¡”±…ÑÑ¥”É•Ü‰äÑ¡”…µÁ±¥ÑÕ‘”Ñ¼…ÉÉäÑ¡”½¹•Ì¥Ğ(€ÁÕÍ¡•Ì¥¸ƒŠPİ¥Ñ „Íåµµ•ÑÉ¥Œ½™™Í•ĞÑ¡”µ•…¸½ÍĞ¥ÌÉ…‘¥ÕÏ
È€¬Ù…É¥…¹•€°¹½Ğ(€€¡É…‘¥ÕÌ€¬…µÁ±¥ÑÕ‘”§
É€¸5•…ÍÕÉ•½…Ğ€ÄÈàÃ\àÀÀ…ĞÑ¡É•”™¥á•ÍÑ…Ñ¥½¹Ìè½Á•¸ÁÉ…¥É¥”(€€¨¨ÄÜĞ€ÌØÌƒŠH€ÄÜØ€ØÔØ¨¨ÑÉ¥…¹±•Ì€ ¬Ä¸Ì€”°€Ì€ÜĞÈƒŠH€Ì€àÔÀ™±½É„¥¹ÍÑ…¹•Ì¤°Í•ÑÑ±•Ñ½İ¸(€€¨¨Ìàä€ÌØäƒŠH€Ìàä€ÈÔÌ¨¨€£Š"HÀ¸ÀÌ€”¤°É¥Ù•È‰…¹¬€¨¨ÌÔÀ€ÄÀäƒŠH€ÌÔÀ€ÄÀÔ¨¨€£Š"HĞ¤¸É…Ü…±±ÌÕ¹¡…¹•(€…Ğ€ÌÜ€¼€ØØ€¼€ÜÈ¸Q¡”½ÍĞ±…¹‘Ìİ¡•É”Ñ¡”Íİ…É¥Ì‘•¹Í”…¹¹½İ¡•É”•±Í”°İ¡¥ ¥ÌÑ¡”É¥¡Ğ(€Í¡…Á”™½È¥Ğ¸(´€¨©]½É±Á½Í¥Ñ¥½¸°¹½Ğ…µ•É„‘¥ÍÑ…¹”¸¨¨Q¡”½™™Í•Ğ¥Ì„™Õ¹Ñ¥½¸½˜Ñ¡”É½Õ¹…±½¹”°Í¼Ñ¡”(€É…••‘”‘½•Ì¹½ĞÍİ¥´…ÌÑ¡”İ…±­•Èµ½Ù•Ì…¹¥ÌÑ¡”Í…µ”•‘”İ¡¥¡•Ù•Èİ…äÑ¡•ä™…”ƒŠP(€Ñ¡”Á½Àµ¥¸‘•™•Ğ½¹”É¥¹œ™ÕÉÑ¡•È½ÕĞ°…Ù½¥‘•É…Ñ¡•ÈÑ¡…¸ÑÉ…‘•™½È¸Q¡”…Ñ”…Í­ÌÑ¡”(€Á±…•È€¡™±½É„¹™É¥¹•Ñ€¤¥¹ÍÑ•…½˜É”µ‘•É¥Ù¥¹œÑ¡”¹½¥Í”°…¹É•ÅÕ¥É•Ì¹¥¹”Á½¥¹ÑÌÑ¼…¹Íİ•È(€¥‘•¹Ñ¥…±±ä™É½´Ñİ¼…µ•É…Ì€ĞÀ´…Á…ÉĞ¸(´€¨©Q¡”™±½İ•ÉÌ¡…Ñ¼½µ”İ¥Ñ Ñ¡”É…ÍÌ¸¨¨Q¡”™½ÉˆÉ¥¹œ•¹‘Ìİ¥Ñ¡¥¸„µ•ÑÉ”½˜Ñ¡”µ¥É¥¹œ°(€Í¼„™É¥¹”½¸Ñ¡”µ…ÑÉ¥à…±½¹”İ½Õ±¡…Ù”±•™ĞÑ¡”‰É¥¡Ñ•ÍĞ½‰©•ÑÌ¥¸Ñ¡”™¥•±‘É…İ¥¹œÑ¡”(€±¥¹”Ñ¡”É…ÍÌ¹¼±½¹•È‘½•Ì¸%Ğ¥Ì…Ñ•½¸¥ÑÌI%9LÉ…Ñ¡•ÈÑ¡…¸½¸¥ÑÌ‘É…İ¸•‘”è…Ğ(€€Ì¸Ğ´•±±Ì„€Ì¸Ü×
À‰¥¸¡½±‘Ì½¹”½ÈÑİ¼™½É‰Ì°Í¼€‰Ñ¡”™ÕÉÑ¡•ÍĞ½¹”‘É…İ¸ˆ¥Ì„Í…µÁ±¥¹œ(€ÍÑ…Ñ¥ÍÑ¥Œ°…¹µ•…ÍÕÉ•Ñ¡…Ğİ…ä¥ĞÉ•Á½ÉÑ•„¹¥¹”µµ•ÑÉ”¡½±”¥¸É½Õ¹Ñ¡…Ğ¡…Ì¹½¹”¸(´€¨©Q¡”Á½Àµ¥¸…Ñ”¡…Ñ¼‰”µ…‘”¥¹ÍÑ…¹”µ…İ…É”Ñ¼ÍÑ…ä¡½¹•ÍĞ¸¨¨%Ğ…Í­•Ñ¡”±…å•ÈÌ¹½µ¥¹…°(€É¥¹œ¡½Ü™…‘•…¸…ÉÉ¥Ù¥¹œÁ±…¹Ğİ…Ì°…¹„¹½µ¥¹…°É¥¹œ…¹Íİ•ÉÌ€©é•É¼¨ƒŠP„™É•”Á…ÍÌƒŠP™½È(€•á…Ñ±äÑ¡”Á±…¹ÑÌÑ¡”™É¥¹”ÁÕÍ¡•Ì™ÕÉÑ¡•ÍĞ½ÕĞ¸%ĞÉ•…‘Ì•… ¥¹ÍÑ…¹”Ì½İ¸…¡¥I¥¹€(€¹½Ü¸M…µ”‰½Õ¹°Í…µ”µ•…ÍÕÉ•€À¸À€”…ÉÉ¥Ù…°¡•¥¡Ğ¸(´€¨©Y•É¥™¥•Ñ¡”…Ñ”‰¥Ñ•Ì¨¨°‰äÁÕÑÑ¥¹œÑ¡”™É¥¹”‰…¬Ñ¼é•É¼èÑ¡”‰½Õ¹‘…ÉäÍÁÉ•…™…±±ÌÑ¼(€€¨¨Ä¸ĞÁà¨¨……¥¹ÍĞ„‰…È½˜€Ğ°Ñ¡”™½ÉˆÉ¥¹ÌÍÁ…¸€À¸ÀÀ´°…¹Ñ¡”İ½É±µ…¹¡½É¥¹œ¡•¬(€É•Á½ÉÑÌ¹¼Ù…É¥…Ñ¥½¸…Ğ…±°¸Q¡É•”™…¥±ÕÉ•Ì°½¸Ñ¡”½‘”Ñ¡…ĞÍ¡¥ÁÁ•å•ÍÑ•É‘…ä¸(´€¨©]¡…ĞÑ¡¥Ì‘½•Ì¹½Ğ‘¼¸¨¨%Ğ‘½•Ì¹½Ğ•áÑ•¹Ñ¡”Íİ…É¸0àÀÍÑ¥±°½İ¹ÌÑ¡”½µÁÉ•ÍÍ¥½¸ƒŠPÑ¡”(€Ñ•ÉÉ…¥¸Ì½İ¸½±½ÕÈ…ÉÉ¥•Ì•Ù•ÉåÑ¡¥¹œÁ…ÍĞÑ¡”É¥¹œƒŠP…¹Ñ¡”µ¥µ™¥•±Ñ…É•ÑÌ¥¸LÙ„¥Ñ•µÌ(€€Ä°€È…¹€ÓŠLÜ…É”Õ¹Ñ½Õ¡•¸Q¡¥ÌÉ•µ½Ù•Ì„±¥¹”Ñ¡”•å”É•…‘Ì…Ì…¸½‰©•Ğ¥¸Ñ¡”İ½É±ì¥Ğ(€‘½•Ì¹½ĞÁÕĞÙ••Ñ…Ñ¥½¸İ¡•É”Ñ¡•É”¥Ì¹½¹”¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠP„™…‘”™Õ¹Ñ¥½¸Ñ¡…Ğİ…ÌÁÉ½‘Õ¥¹œ„ÍÑ•À((¨©Q¡”ÑÉ…¹Í¥Ñ¥½¸Ñ¡”½İ¹•È…Í­•™½È¡…‰••¸Ñ¡•É”…±°…±½¹œ°Í…µÁ±•½¹”Á•ÈÍÑÉ¥‘”¸¨¨(‰É…ÍÌ…¹™±½İ•ÉÌ…ÁÁ•…È½ÕĞ½˜Ñ¡”É½Õ¹…Ìå½Ôİ…±¬Ñ½İ…É‘ÌÑ¡•´ˆ€¡,Ì¤É•…±¥­”„µ¥ÍÍ¥¹œ)™•…ÑÕÉ”°…¹™±½É„¹©Í€¡…ÌÍ…±••Ù•ÉäÁ±…¹Ğ‘½İ¸½Ù•ÈÑ¡”½ÕÑ•È‰…¹½˜¥ÑÌÉ¥¹œÍ¥¹”Ñ¡”)±…å•Èİ…ÌİÉ¥ÑÑ•¸¸Q¡”‘•™•Ğ¥ÌÑ¡”IQ°¹½ĞÑ¡”…‰Í•¹”èÑ¡”É…µÀİ…Ì•Ù…±Õ…Ñ•½¸Ñ¡”AT…Ğ)±…ÑÑ¥”µÉ•‰Õ¥±Ñ¥µ”…¹‰…­•¥¹Ñ¼Ñ¡”¥¹ÍÑ…¹”Ì¡•¥¡Ğ°…¹Ñ¡”±…ÑÑ¥”É•‰Õ¥±‘Ì½¹±ä•Ù•Éä)QU9¹ÍÑ•À¹¹•…É€µ•ÑÉ•Ìİ…±­•¸€Ä¸È´½˜ÍÑ•À……¥¹ÍĞÑ¡”¹•…ÈÉ¥¹œÌ€È¸È´‰…¹µ•…¹Ì„Á±…¹Ğ)İ•¹Ğ™É½´¹½Ñ¡¥¹œÑ¼€¨¨ÔÔ€”½˜™Õ±°¡•¥¡Ğ¥¸„Í¥¹±”™É…µ”¨¨°½¹”Á•ÈÍÑÉ¥‘”°™½É•Ù•È¸™…‘”)Ñ¡…Ğ½¹±äÕÁ‘…Ñ•Ìİ¡•¸Ñ¡”Ñ¡¥¹œ¥Ğ¥Ì™…‘¥¹œ¥ÌÉ•‰Õ¥±Ğ¥Ì„ÍÑ•À™Õ¹Ñ¥½¸İ•…É¥¹œ„É…µÀÌ¹…µ”°)…¹¥Ğ¥Ì¥¹Ù¥Í¥‰±”¥¸É•Ù¥•ÜÁÉ•¥Í•±ä‰•…ÕÍ”Ñ¡”É…µÀÉ•…‘Ì½ÉÉ•Ñ±ä½¸Ñ¡”Á…”¸()Q¡”É…µÀ¹½ÜÉÕ¹ÌÁ•È™É…µ”¥¸Ñ¡”Ù•ÉÑ•àÍ¡…‘•È……¥¹ÍĞ…µ•É…A½Í¥Ñ¥½¹€¸]¡…ĞÑ¡…Ğ½ÍĞ°…¹)İ¡…Ğ¥Ğ‰½Õ¡Ğ°¥Ì¥¸I=5@ƒ
œ,ÌìÑ¡É•”Ñ¡¥¹Ì‰•±½¹œ¡•É”¸((´€¨©™±½İ•È¡•……¹¹½Ğ©ÕÍĞÍ¡É¥¹¬ƒŠP¥Ğ¡…ÌÑ¼½µ”‘½İ¸¸¨¨%ÑÌ½É¥¥¸¥ÌÁ…ÉÑİ…äÕÀ„ÍÑ•´°Í¼(€Í…±¥¹œ¥¸Á±…”±•…Ù•Ì¥Ğ¥¸Ñ¡”…¥È½Ù•È„Á±…¹ĞÑ¡…Ğ¥Ì¹¼±½¹•ÈÕ¹‘•È¥Ğ¸…¡¥I¥Í•€…¹„(€İ½É±µÍÁ…”‘•Í•¹Ğ…ÁÁ±¥•…™Ñ•ÈÑ¡”¥¹ÍÑ…¹”ÑÉ…¹Í™½É´€¡Ñ¡”¥¹ÍÑ…¹”µ…ÑÉ¥à…ÉÉ¥•Ì„É•…°(€É½Ñ…Ñ¥½¸™½ÈÑ¥±Ñ•¡•…‘Ì°Í¼¥Ğ…¹¹½Ğ‰”™½±‘•¥¹Ñ¼Ñ¡”±½…°½™™Í•Ğ¤¸(´€¨©Q¡”™…‘”€ğ€À¸ÌÕ€¡•……Ñ”İ…Ì¥ÑÍ•±˜Ñ¡”İ½ÉÍĞÁ½À¥¸Ñ¡”™¥•±¨¨°‰•¥¹œ„ÍÑ•À¥¸Ñ¡”(€µ¥‘‘±”½˜„É…µÀ½¸Ñ¡”‰É¥¡Ñ•ÍĞ½‰©•Ğ¥¸Ñ¡”™É…µ”¸!•…‘Ì¡…Ù”Ñ¡•¥È½İ¸¥¹Í•ĞÉ¥¹œ¹½Ü°…¹(€Ñ¡”Í…µ”¡•…‘Ì…É”‘É…İ¸èÑ¡”É¥¹œÉ•…¡•Ìé•É¼•á…Ñ±äİ¡•É”Ñ¡”Á±…¹ĞÌÉ…µÀÁ…ÍÍ•Ì€À¸ÌÔ¸(´€¨©Q¡”Õ…É…¹Ñ•”¥Ì•½µ•ÑÉ¥Œ°¹½Ğ•µÁ¥É¥…°¸¨¨Q¡”±…ÑÑ¥”¥Ì¥¹Í•Ğ™É½´Ñ¡”™…‘”É¥¹œ‰äÑ¡”(€É•‰Õ¥±ÍÑ•À°Í¼„Á±…¹Ğ¥Ì…±İ…åÌÁ±…•°…Ğé•É¼¡•¥¡Ğ°‰•™½É”¥Ğ¥Ì¹•…È•¹½Õ Ñ¼‰”İ½ÉÑ (€…¹ä¸Q¡”É•Í¥‘Õ…°¥Ì½¹”™É…µ”½˜½Ù•ÉÍ¡½½ĞƒŠPÑ¡”É•‰Õ¥±™¥É•Ì½¸Ñ¡”™É…µ”Ñ¡…Ğ…ÉÉ¥•ÌÑ¡”(€İ…±­•ÈÁ…ÍĞÑ¡”ÍÑ•ÀƒŠPİ¡¥ ¥Ì€À¸ÀÈĞ´…Ğ€ØÀ™ÁÌ°…‰½ÕĞ€Ä€”½˜„Á±…¹ĞÌ¡•¥¡Ğ°…¹¥Ğ¥Ì(€İÉ¥ÑÑ•¸‘½İ¸É…Ñ¡•ÈÑ¡…¸É½Õ¹‘•…İ…ä¸Q¡”¹•…ÈÉ¥¹œÌÙ¥Í¥‰±”É…‘¥ÕÌ¥Ì€À¸Ø´Í¡½ÉÑ•ÈÑ¡…¸¥Ğ(€İ…Ì°İ¡¥ ¥ÌÑ¡”ÁÉ¥”½˜Ñ¡”¥¹Í•Ğ…¹¥Ì±•™Ğ…Ì„½Ù•É…”ÅÕ•ÍÑ¥½¸¥¸,Ì¸(´€¨©Q¡”…Ñ”¹½Üİ…±­Ì¸¨¨Qİ•¹Ñä€À¸ÄÔ´Á…•Ì…Ğ€ÌäÃ\ÜàÀ…¹€ÄÈàÃ\àÀÀ°¡•­¥¹œ•Ù•ÉäÁ±…¹ĞÑ¡…Ğ(€…ÁÁ•…ÉÌ¥¸™É½¹Ğ½˜Ñ¡”İ…±­•Èèµ•…ÍÕÉ•İ½ÉÍĞ…ÉÉ¥Ù…°€¨¨À¸À€”¨¨½˜™Õ±°¡•¥¡Ğ……¥¹ÍĞ„€ÄÀ€”(€‰…È°Á±ÕÌ„¡•¬½¸Ñ¡”É¥¹œ•½µ•ÑÉäÍ¼Ñ¡”µ…É¥¸…¹¹½Ğ‰”ÑÕ¹•…İ…ä±…Ñ•È¸QÉ¥…¹±•Ì(€€ÔØĞ€àÈÄ‘•Í­Ñ½À……¥¹ÍĞ€ÔØĞ€ØàÄ‰•™½É”ƒŠP„É½Õ¹‘¥¹œ•ÉÉ½È°…¹¹¼¹•Ü…ÍÍ•Ğ¸((¨©¹Ñ¡”…Ñ”İ…Ìµ•…ÍÕÉ¥¹œÑ¡”İ•…Ñ¡•È¸¨¨IÕ¹¹¥¹œÑ¡”‰…Í•±¥¹”‰•™½É”Ñ½Õ¡¥¹œ…¹åÑ¡¥¹œÑÕÉ¹•)ÕÀ…¸Õ¹É•±…Ñ•É•è€¨‰ÑÕÉ¹¥¹œ¥Ğ½™˜É•ÍÑ½É•ÌÑ¡”É•¹‘•Èˆ¨™…¥±•…‰½ÕĞ€¨©Ñİ¼ÉÕ¹Ì¥¸Ñ¡É•”½¸)µ…¥¸¨¨°…Ğ€ÌäÃ\ÜàÀ°İ¥Ñ „İ½ÉÍĞµ•±°‘•±Ñ„½˜€ä……¥¹ÍĞ„‰…È½˜€à¸Q¡”…ÍÍ•ÉÑ¥½¸½µÁ…É•ÌÑİ¼)…ÁÑÕÉ•Ì½˜Ñ¡”Í…µ”Í•¹”Ñ¼‘•¥‘”İ¡•Ñ¡•ÈÍİ¥Ñ¡¥¹œÑ¡”½¹™¥‘•¹”Ù¥•Ü½™˜±•…Ù•Ì…¹åÑ¡¥¹œ)‰•¡¥¹ƒŠP…¹Ñ¡”İ¥¹‰±½İÌ‰•Ñİ••¸Ñ¡•´°…Ğ€ÇŠLÌ™ÁÌÕ¹‘•ÈÑ¡”Í½™Ñİ…É”É…ÍÑ•É¥Í•È°Í¼µ½ÍĞ½˜)Ñ¡”É•Í¥‘Õ…°¥Ğİ…Ìµ•…ÍÕÉ¥¹œİ…ÌÍİ…å¥¹œÉ…ÍÌ¸Q¡”Ñ½±•É…¹”¡……±É•…‘ä‰••¸İ¥‘•¹•½¹”™½È)•á…Ñ±äÑ¡…ĞÉ•…Í½¸°İ¡¥ ¥ÌÑ¡”Ñ•±°è„…Ñ”İ¡½Í”‰…È¥ÌÍ•Ğ‰ä¥ÑÌ½İ¸¹½¥Í”¥Ì„…Ñ”Ñ¡…Ğ)İ¥±°‰”İ¥‘•¹•……¥¸¸µ…¥¸¹©Í€…¥¹Ì„¡…É¹•ÍÌµ½¹±äÍ•Ñ¹¥µ…Ñ¥½¹!½±‘€ƒŠP­••À‘É…İ¥¹œ°…‘Ù…¹”)¹½Ñ¡¥¹œƒŠP…¹Ñ¡”Ñ¡É•”…ÁÑÕÉ•Ì…É”Ñ…­•¸Õ¹‘•È¥Ğ¸Q¡”É•Í¥‘Õ…°¥ÌÉ•…‘‰…¬¹½¥Í”¹½Ü°Í¼Ñ¡”)‰…È€¨©Ñ¥¡Ñ•¹•¨¨™É½´µ•…¸€À¸Ô€¼İ½ÉÍĞ€àÑ¼µ•…¸€À¸Ä€¼İ½ÉÍĞ€Ì°…¹Ñ¡”…ÍÍ•ÉÑ¥½¸…‰½Ù”¥Ğ( ©½¹™¥‘•¹”Ù¥•Ü¡…¹•ÌÑ¡”É•¹‘•È¨¤½ĞÍÑÉ¥Ñ±ä¡…É‘•È°‰•…ÕÍ”Íİ…ä…¸¹¼±½¹•ÈÍÕÁÁ±ä…¹ä)½˜Ñ¡”‘¥™™•É•¹”¥Ğ¡…ÌÑ¼™¥¹¸Qİ¼½¹Í•ÕÑ¥Ù”™Õ±°ÉÕ¹ÌÉ••¸…Ğ‰½Ñ Ù¥•İÁ½ÉÑÌ¸()Q¡…Ğ±½Í•ÌÑ¡”‘•‰ĞÑ¡”‰…­”µ…Ñ”•¹ÑÉä‰•±½ÜÉ•½É‘Ì…Ì½İ•èÑ¡”™±½É„±½¬¥Ì™É½é•¸‘ÕÉ¥¹œ)…ÁÑÕÉ”°…¹Ñ¡”‰½Õ¹İ…ÌÑ¥¡Ñ•¹•É…Ñ¡•ÈÑ¡…¸İ¥‘•¹•¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”¹¥¡Ñ±ä‰…­”¡…‰••¸É•™½È‘…åÌ°…¹¹½‰½‘ä½Õ±Í•”¥Ğ((¨©Q¡”Á±…•¡½±‘•È…Ñ”™½É‰…‘”Ñ¡”ÕÁÉ…‘”Ñ¡”‰…­”•á¥ÍÑÌÑ¼Á•É™½É´¸¨¨•¹•É…Ñ½ÉÌ½‰Õ¥±¹Áå€)İÉ¥Ñ•Ì…ÍÍ•ÑÌ½±Ñ˜¼ñ¥ù}|ñÁ¡…Í”ø¹±‰€™½È…¹äÉ•½Éİ¡½Í”…É¡•ÑåÁ”¡…Ì„•¹•É…Ñ½È°…¹•Ù•Éä)É•½¹|©€É•½É¡…Ì½¹”ƒŠPÍ¼Ñ¡”…¹½¹¥…°	±•¹‘•È‰…­”±…¹‘Ì½¸•á…Ñ±äÑ¡”™¥±•¹…µ”)•¹•É…Ñ½ÉÌ½¥¹™•ÉÉ•‘}Á±…•¡½±‘•È¹Áå€±…¥µÌ°…¹Ñ¡”…Ñ”Ñ¡•¸É•©•Ñ•Ñ¡”É•…°‰…­”™½È¹½Ğ)‰•¥¹œÑ¡”ÁÕÉ”µAåÑ¡½¸Á±…•¡½±‘•È¥Ğİ…Ì‰Õ¥±ĞÑ¼É•Á±…”¸Í•½¹½¹™±¥ĞÉ½‘”…±½¹œè)Ñ½½±Ì½‰…­”¹Í¡€ÉÕ¹Ì±Ñ˜µÑÉ…¹Í™½É´½Ù•È…ÍÍ•ÑÌ½İ•ˆ½€°Í¼‘•µ…¹‘¥¹œ‰åÑ”µ•ÅÕ…±¥Ñäİ¥Ñ Ñ¡”)µ…ÍÑ•È…ÍÍ•ÉÑ•Ñ¡…Ğ½µÁÉ•ÍÍ¥½¸¹•Ù•È¡…ÁÁ•¹Ì¸€¨©]¡…Ğµ…‘”¥Ğ¥¹Ù¥Í¥‰±”¥ÌÑ¡”Í¡…Á”İ½ÉÑ )É•µ•µ‰•É¥¹œ¨¨ƒŠPÑ¡”…Ñ”Á…ÍÍ•½¸•Ù•Éä‘•Ù•±½Á•Èµ…¡¥¹”…¹™…¥±•½¸•Ù•Éä$ÉÕ¹¹•È°‰•…ÕÍ”)Ñ¡”‘¥™™•É•¹”İ…Ìİ¡•Ñ¡•È¹Áá€½Õ±É•… Ñ¡”¹•Ñİ½É¬¸É••¸±½…°…Ñ”İ…ÌÉ•Á½ÉÑ¥¹œ½¸„)Á¥Á•±¥¹”¥Ğİ…Ì¹½ĞÉÕ¹¹¥¹œ¸Q¡”…Ñ”¹½Ü½µÁ…É•Ì½¹±äÑ¡”µ…ÍÑ•È……¥¹ÍĞÑ¡”É•½É°É•ÅÕ¥É•Ì)Ñ¡”‘•É¥Ù…Ñ¥Ù”µ•É•±äÑ¼•á¥ÍĞ°…¹ÍÑ…¹‘Ì…Í¥‘”™½È…¹ä…ÍÍ•Ğİ¡½Í”µ…¹¥™•ÍĞ•¹ÑÉäÍ…åÌ)­¥¹è•¹•É…Ñ•‘€°±•…Ù¥¹œÑ¡…ĞÑ¼Ñ¡”½É‘¥¹…ÉäÍÑ…±•¹•ÍÌ¡•¬¸((¨©Ñ½½±Ì½ÁÕ‰±¥Í ¹Í¡€İ…Ì…¸…ÕµÕ±…Ñ½È°¹½Ğ„µ¥ÉÉ½È¸¨¨%Ğ½Á¥•™¥±•Ì¥¸…¹¹•Ù•ÈÑ½½¬…¹ä)½ÕĞ°Í¼„É•Ñ¥É•…ÍÍ•ĞÍ¡¥ÁÁ•™½É•Ù•Èè€ÄÀà}}É•½µµ•¹‘•‘|ÄàÌÔ¹±‰€Á±…•¡½±‘•ÉÌ°½ÉÁ¡…¹•İ¡•¸)Ñ¡”ÁÉ½É…µµ”İ…ÌÉ•¹…µ•°İ•É”ÍÑ¥±°‰•¥¹œÍ•ÉÙ•Ñ¼Ù¥Í¥Ñ½ÉÌ±½¹œ…™Ñ•È¹½Ñ¡¥¹œÉ•™•É•¹•)Ñ¡•´¸•±•Ñ¥¹œ„™¥±”™É½´Ñ¡”Í½ÕÉ”ÑÉ•”İ…Ì¹½Ğ„Ñ¡¥¹œÑ¡”ÁÕ‰±¥Í¡•Í¥Ñ”½Õ±•áÁÉ•ÍÌ¸)¥á•‰ä±•…É¥¹œÑ¡”ÁÕ‰±¥Í¡•‘…Ñ„½±Ñ™€‰•™½É”½Áå¥¹œìÁ…å±½…€Ää¸ÄØƒŠH€Äà¸ÔÔ5…ĞÑ¡”Ñ¥µ”¸((¨©-¹½İ¸™±…­ä…Ñ”°‘•±¥‰•É…Ñ•±ä¹½ĞÍ¥±•¹•¸¨¨µ½‰¥±”€ÌäÁàÜàÀèÑÕÉ¹¥¹œ¥Ğ½™˜É•ÍÑ½É•ÌÑ¡”)É•¹‘•É€½µÁ…É•Ì„™É…µ”…ÁÑÕÉ•‰•™½É”Ñ¡”½¹™¥‘•¹”Ñ½±”İ¥Ñ ½¹”…ÁÑÕÉ•…™Ñ•È°İ¡¥±”Ñ¡”)™±½É„¥ÌÍÑ¥±°Íİ…å¥¹œ¸=‰Í•ÉÙ•™…¥±¥¹œÑİ¥”…Ğİ½ÉÍĞµ•±°‘•±Ñ„€ÄÄ……¥¹ÍĞ„‰½Õ¹½˜€à…¹)Á…ÍÍ¥¹œ½¸Ñ¡”Ñ¡¥ÉÉÕ¸İ¥Ñ ¹¼½‘”¡…¹”¸Q¡”‰½Õ¹¡…Ì9=P‰••¸İ¥‘•¹•ƒŠP„É•±•…Í”…Ñ”)±½½Í•¹•Õ¹Ñ¥°¥ĞÍÑ½ÁÌ½µÁ±…¥¹¥¹œ¥Ì¹½Ğ„…Ñ”¸Q¡”™¥à¥ÌÑ¼™É••é”Ñ¡”™±½É„±½¬‘ÕÉ¥¹œ)…ÁÑÕÉ”°…¹¥Ğ¥Ì½İ•¸€¨©A…¥€ÈÀÈØ´Àà´ÄÌ¨¨ƒŠPÍ•”Ñ¡”™±½É„µ™…‘”•¹ÑÉä…‰½Ù”è…ÁÑÕÉ•Ì¹½ÜÉÕ¸)Õ¹‘•ÈÍ•Ñ¹¥µ…Ñ¥½¹!½±‘€…¹Ñ¡”‰½Õ¹Ñ¥¡Ñ•¹•Ñ¼„İ½ÉÍĞ•±°½˜€Ì¸((ŒŒ¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÑİ¼‘•™•ÑÌÑ¡”½İ¹•ÈÁ¡½Ñ½É…Á¡•°…¹İ¡…ĞÑ¡•äÑ…Õ¡Ğ((¨©Q¡”±…É¬MÑÉ••Ğ¡•…‘±…¹İ…ÌÑ¡”µ…ÀÌ½İ¸±•ÑÑ•É¥¹œ¸¨¨¥á•€ÈÀÈØ´Àà´ÄÌ¸]¡…Ğµ…­•Ì¥Ğ)İ½ÉÑ É•½É‘¥¹œ¥ÌÑ¡…ĞÑ¡”ÑÉ…”¡…‰••¸€©‰•±¥•Ù•¨……¥¹ÍĞ„µ•…ÍÕÉ•µ•¹ĞÑ¡…Ğ‘¥Í…É••)İ¥Ñ ¥ĞèÑ¡”M½ÕÑ ]…Ñ•È•½É•™•É•¹”¹½Ñ”É•½É‘•€Üä¸Ø´½˜É•Í¥‘Õ…°…Ğ±…É¬……¥¹ÍĞ(Äà¸Ü´…Ğ•…É‰½É¸…¹…ÑÑÉ¥‰ÕÑ•Ñ¡”Íİ¥¹œÑ¼Á…Á•ÈÍÑÉ•Ñ ¸	½Ñ ¹Õµ‰•ÉÌİ•É”É¥¡Ğ…¹Ñ¡”)•áÁ±…¹…Ñ¥½¸İ…ÌİÉ½¹œ¸€ØÀ´±½…°‘¥Í…É••µ•¹Ğ‰•Ñİ••¸Ñİ¼¥¹‘•Á•¹‘•¹Ğµ•Ñ¡½‘Ì¥Ì„‘•™•Ğ)É•Á½ÉĞ°¹½Ğ…¸•ÉÉ½È‰…È¸((¨©•¹•É…Ñ½ÉÌ½Ñ•ÉÉ…¥¹}•¸¹Áä€´µ±‰€¡…‰••¸Õ¹ÉÕ¹¹…‰±”Í¥¹”Ñ•ÉÉ…¥¹}¥¹ÁÕÑÍ€İ…Ì)•áÑÉ…Ñ•¸¨¨Ñ•ÉÉ…¥¹}¥¹ÁÕÑÍ}Í¡„ ¥€¥Ì…±±•‰•™½É”µ…¥¸ ¥€¥¹Í•ÉÑ••¹•É…Ñ½ÉÌ½€½¸)ÍåÌ¹Á…Ñ¡€ìÉÕ¸…ÌÁåÑ¡½¸Ì•¹•É…Ñ½ÉÌ½Ñ•ÉÉ…¥¹}•¸¹Áå€Ñ¡…ĞÁ…Ñ ¥ÌÍåÌ¹Á…Ñ¡lÁu€‰ä…¥‘•¹Ğ°)ÉÕ¸Õ¹‘•È‰±•¹‘•È€´µÁåÑ¡½¹€¥Ğ¥Ì¹½Ğ°…¹Ñ¡”1¡…±˜‘¥•½¸5½‘Õ±•9½Ñ½Õ¹‘ÉÉ½É€¸Q¡”)¥¹Í•ÉĞµ½Ù•Ñ¼¥µÁ½ÉĞÑ¥µ”¸9½Ñ¡¥¹œ…Õ¡Ğ¥Ğ‰•…ÕÍ”Ñ½½±Ì½‰…­”¹Í¡€‘½•Ì¹½Ğ‰Õ¥±Ñ•ÉÉ…¥¸)…¹Ñ¡”Ñ•ÉÉ…¥¸1¥Ì„É…É”°‘•±¥‰•É…Ñ”¥¹Ù½…Ñ¥½¸¸€¨©Q¡”¡•¥¡Ñ™¥•±…¹Ñ¡”1…É”¹½Ü)‰…¬¥¸ÍÑ•À¨¨ìÑ¡”½µµ¥ÑÑ•1‰•™½É”Ñ¡¥ÌÉÕ¸İ…Ì‰…­•…Ğ€´µ‘•¥µ…Ñ”µ‘•œ€À¸ÀÑ€…¹Ñ¡”)½¹”…™Ñ•È…Ğ€À¸ÀÍ€€¡Í•”,ÄĞ¤¸((¨©Q¡”ÑÉ•”µÁ±…•µ•¹Ğ…Ñ”…¹Ñ¡”É¥Ù•Èµ…Í¬…É”Ñİ¼‘¥™™•É•¹ĞÅÕ•ÍÑ¥½¹Ì¸¨¨¥Í]…Ñ•É€…Í­Ì(‰¥ÌÑ¡¥ÌÑ¡”É¥Ù•Èˆ…¹¥ÑÌÑ¡É•Í¡½±¥Ì€ÄÀÀµ´Õ¹‘•ÈÑ¡”‘…ÑÕ´°İ¡¥ ¥Ì½ÉÉ•Ğ™½ÈÑ¡…Ğ)ÅÕ•ÍÑ¥½¸…¹İ…ÌÍ¥±•¹Ñ±äİÉ½¹œ™½È€‰µ…ä„ÍÑ•´ÍÑ…¹¡•É”ˆ¸Q¡”É•±•…Í”…Ñ”¡…„É••¸)¡•¬½¸Ñ¡”™¥ÉÍĞÅÕ•ÍÑ¥½¸İ¡¥±”Ñ¡”½İ¹•È¡…„Á¡½Ñ½É…Á ½˜Ñ¡”Í•½¹™…¥±¥¹œ¸	½Ñ )¡•­Ì…É”¹½ÜÁÉ•Í•¹Ğ¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”Á±…ÑÑ•É¥•á¥ÍÑÌ°…¹¥Ğ™½Õ¹Í•Ù•¸‰Õ¥±‘¥¹Ì¥¸Ñ¡”É½…((¨©,ÜÁ¡…Í”½¹”¸¨¨Q¡”‰±½¬…¹±½ĞÉ¥¥Ì•¹•É…Ñ•É…Ñ¡•ÈÑ¡…¸ÑÉ…•è)Ñ½½±Ì½•¹•É…Ñ•}Á±…Ñ}±½ÑÌ¹Áå€½™™Í•ÑÌÑ¡¥ÌÁÉ½©•ĞÌ½µµ¥ÑÑ•ÍÑÉ••Ğ•¹ÑÉ•±¥¹•Ì‰ä¡…±˜Ñ¡”)Á±…ÑÑ•½ÉÉ¥‘½È°¥¹Ñ•ÉÍ•ÑÌÑ¡•´°…¹‘¥Ù¥‘•ÌÑ¡”É•ÍÕ±Ğ¥¹Ñ¼±½ÑÌƒŠP€Ää‰±½­Ì°€ÄÔÈ±½ÑÌ°)É”µ‘•É¥Ù•‰åÑ”™½È‰åÑ”‰äÑ½½±Ì½¡•¬¹Í¡€¸QÉ…¥¹œÑ¡”€ÄàÌĞÍ¡••ÑÌ¥¹ÍÑ•…İ½Õ±¡…Ù”‰…­•)Ñ¡•¥È€Ì¸ßŠLĞ¸Ô€”Á…Á•ÈÍÑÉ•Ñ ¥¹Ñ¼•Ù•Éä‰±½¬™…”¸Q¡”‰±½­Ì…É”¥¹™•ÉÉ•‘€‰•…ÕÍ”Ñ¡•¥È)¥¹ÁÕÑÌ…É”ìÑ¡”±½Ğ±¥¹•Ì…¹Ñ¡”…±±•äÁ½Í¥Ñ¥½¸…É”½¹©•ÑÕÉ…±€…¹ÍÑ…äÑ¡…Ğİ…ä°‰•…ÕÍ”)™½ÕÈ±½ÑÌÑ¼„™…”¥Ì„É•…‘¥¹œ½˜=9‰±½¬€¡‰±½¬€Äà½¸Ñ¡”½İ¹•ÈÌ±…É¬µÉ•… É½À¤¸9¼±½Ğ)…¹¹¼‰±½¬¥Ì¹Õµ‰•É•ƒŠPÑ¡¥ÌÁÉ½©•Ğ¡…Ì¹•Ù•ÈÉ•…Q¡½µÁÍ½¸Ì¹Õµ‰•É¥¹œ½™˜„Í¡••Ğ¸((¨©Q¡”É¥¥µµ•‘¥…Ñ•±äÁ…¥™½È¥ÑÍ•±˜…Ì„¡•¬¸¨¨=˜€ÈÈÈÁ±…•ÍÑÉÕÑÕÉ•Ì°€àÀÍÑ…¹¥¹Í¥‘”„)•¹•É…Ñ•‰±½¬°€ÄÈÀÍÑ…¹½ÕÑÍ¥‘”Ñ¡”€Ää‰±½­Ì¥Ğ½Ù•ÉÌ°…¹€ÈÈÍÑ…¹¥¹Í¥‘”„Á±…ÑÑ•ÍÑÉ••Ğ)½ÉÉ¥‘½È¸5½ÍĞ½˜Ñ¡½Í”€ÈÈ…É”İ¥Ñ¡¥¸„µ•ÑÉ”½ÈÑİ¼½˜„½ÉÉ¥‘½È•‘”°İ¡¥ Í…åÌ¹½Ñ¡¥¹œ)……¥¹ÍĞ„ƒ
ÄÈÀ´•½É•™•É•¹”ƒŠP‰ÕĞ€¨©Í•Ù•¸Í¥Ğ€Ø¸ÔÑ¼€ÄÈ¸Ä´¥¸°İ¡¥ ¥ÌÑ¡”µ¥‘‘±”½˜Ñ¡”)É½…¨¨°…¹•Ù•Éä½¹”½˜Ñ¡•´¥Ì„½¹©•ÑÕÉ…±€Á±…•µ•¹Ğ™É½´Ñ¡”¥¹™•ÉÉ•µÍÑÉÕÑÕÉ”)ÁÉ½É…µµ”¸Q¡”Á±…•µ•¹Ğ…Ñ”Ñ¡…ĞÁÕĞÑ¡•´Ñ¡•É”Ñ•ÍÑÌ™½È½Ù•É±…Àİ¥Ñ ½Ñ¡•È‰Õ¥±‘¥¹Ì°™½È)İ…Ñ•È°…¹™½Èµ½‘•±±•É½Õ¹ì¥Ğ¡…Ì¹•Ù•ÈÑ•ÍÑ•™½ÈÑ¡”ÍÑÉ••Ğ¸9½Ñ¡¥¹œ‘½Õµ•¹Ñ•¥Ì¥¸Ñ¡”)É½…¸((¨©9½Ñ¡¥¹œİ…Ìµ½Ù•¥¸Ñ¡¥ÌÍ±¥”°½¸ÁÕÉÁ½Í”¸¨¨I•Á½Í¥Ñ¥½¹¥¹œ•¹•É…Ñ•ÍÑÉÕÑÕÉ•ÌÉ”µ‘•É¥Ù•Ì)Ñ¡”¡½ÕÍ•¡½±±•‘•È°Í¼¥Ğ‰•±½¹ÌÑ¼Ñ¡”Á…É•°Ñ¡…Ğ½İ¹ÌÑ¡½Í”™¥±•Ì€¡I=5@,ÄÁ¡…Í”Ñ¡É•”¤)É…Ñ¡•ÈÑ¡…¸Ñ¼Ñ¡”Í±¥”Ñ¡…Ğ‘¥Í½Ù•É•Ñ¡”ÁÉ½‰±•´¸Q¡”™¥¹‘¥¹œ¥ÌÉ•½É‘•İ¥Ñ Ñ¡”Í•Ù•¸)É•½É‘Ì¹…µ•°¥¸‘½Ì½IMI ½Ñ¡½µÁÍ½¹}Á±…Ñ}É¥¹µ‘€ƒ
œ€Ü…¹I=5@,Ü¸((¨©]¡…ĞÑ¡”É¥¥Ì¡½¹•ÍĞ…‰½ÕĞ¹½Ğ‰•¥¹œ¨¨è€Ää‰±½­Ì½˜Ñ¡”Á±…ĞÌ€Ôà°¹¼9½ÉÑ ¥Ù¥Í¥½¸€¡¥ÑÌ)ÍÑÉ••Ğ½¹ÑÉ½°¥Ìİ¡…Ğƒ
œLäÉ•½É‘Ì…Ì½İ•¤°¹¼±½Ğ‘•ÁÑ ™É½´…¹äÍ½ÕÉ”ƒŠPÑ¡”‘•ÁÑ¡Ì…É”)É•Í¥‘Õ…±Ì½˜Ñ¡”‰±½¬ƒŠP…¹¹½Ñ¡¥¹œÉ•¹‘•É•¸‰±­}Í½ÕÑ¡}İ…Ñ•É}µ…É­•Ñ€°½¹”½˜Ñ¡”µ½ÍĞ‰Õ¥±ĞµÕÀ)‰±½­Ì¥¸Ñ¡”Ñ½İ¸°¥ÌÉ•™ÕÍ•½ÕÑÉ¥¡Ğ‰•…ÕÍ”Ñ¡”ÍÑÉ••Ğ±…å•È‘½•Ì¹½Ğ…ÉÉäM½ÕÑ ]…Ñ•Èİ•ÍĞ)½˜€¬ÄÀÀ¸Q¡…ĞÉ•™ÕÍ…°¥ÌÑ¡”ÍÑÉ••Ğ½¹ÑÉ½°½İ•°…ÉÉ¥Ù¥¹œ™É½´„‘¥™™•É•¹Ğ‘¥É•Ñ¥½¸¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠPÑİ•¹ÑäµÑ¡É•”‰Õ¥±‘¥¹Ì½ÕĞ½˜Ñ¡”É½…°…¹Ñ¡”Á½¥¹ĞÑ•ÍĞÑ¡…Ğ½Õ±¹½ĞÍ•”Ñ¡•´((¨©,ÄÁ¡…Í”Ñ¡É•”€¡„¤€¼,ÜÁ¡…Í”Ñİ¼€¡„¤¸¨¨Q¡”É¥™½Õ¹Í•Ù•¸ÍÑÉÕÑÕÉ•ÌÍÑ…¹‘¥¹œ€Ø¸×ŠLÄÈ¸Ä´)¥¹Í¥‘”„Á±…ÑÑ•ÍÑÉ••Ğ½ÉÉ¥‘½È…¹±•™ĞÑ¡•´Ñ¡•É”½¸ÁÕÉÁ½Í”°‰•…ÕÍ”µ½Ù¥¹œ„•¹•É…Ñ•)‰Õ¥±‘¥¹œÉ”µ‘•É¥Ù•ÌÑ¡”¡½ÕÍ•¡½±±•‘•È¸Q¡¥ÌÍ±¥”µ½Ù•ÌÑ¡•´…¹Í¡ÕÑÌÑ¡”¡½±”Ñ¡•ä…µ”)Ñ¡É½Õ èÑ½½±Ì½Á±…Ñ}½ÉÉ¥‘½ÉÌ¹Áå€¡½±‘ÌÑ¡”½ÉÉ¥‘½È•½µ•ÑÉä™½È	=Q Ñ¡”É•Á½ÉĞÑ¡…Ğ™½Õ¹Ñ¡”)ÁÉ½‰±•´…¹Ñ¡”Á±…•µ•¹Ğ…Ñ”Ñ¡…Ğ¡…ÌÑ¼Í…Ñ¥Í™ä¥Ğ°Í¼Ñ¡”Ñİ¼…¹¹½Ğ…¹Íİ•È‘¥™™•É•¹Ñ±äƒŠPÑ¡”)Í…µ”…ÉÕµ•¹Ğ•¹•É…Ñ½ÉÌ½µ•Í¡}¥¹ÁÕÑÌ¹Áå€Í•ÑÑ±•Ì™½ÈÑ¡”ÍÑ…±•¹•ÍÌ¡…Í ¸Q¡”…Ñ”É•™ÕÍ•Ì…¹ä)•¹•É…Ñ•™½½ÑÁÉ¥¹ĞÑ¡…ĞÉ•…¡•Ì¥¹Í¥‘”„½ÉÉ¥‘½È¸€¨¨ÈÌ½˜Ñ¡”€ÌàÉ•¥Á”•¹ÑÉ•Ìµ½Ù•¨¨€¡µ•‘¥…¸(ÄÈ¸À´°İ½ÉÍĞ€ÈÄ¸ä´¤ì¥¸µ½ÉÉ¥‘½È•¹ÑÉ•Ì…É½ÍÌÑ¡”Í•¹”™•±°€¨¨ÈÈƒŠH€ÄÀ¨¨°…¹¹½¹”½˜Ñ¡”Ñ•¸)¥Ì„•¹•É…Ñ•Á±…•µ•¹Ğ¸((¨©Q¡”Í•Ù•¸İ•É”Ñ¡”±½Õ•¹½˜Ñİ•¹ÑäµÑ¡É•”°…¹Ñ¡”Á½¥¹ĞÑ•ÍĞ¥Ìİ¡ä¹½‰½‘ä­¹•Ü¸¨¨•¹ÑÉ”)¥Ì½¹”Á½¥¹Ğ…¹„‰Õ¥±‘¥¹œ¥Ì„É•Ñ…¹±”ÕÀÑ¼€ÄÄ´…É½ÍÌ°Í¼„‰Õ¥±‘¥¹œ…¸™É½¹Ğ„ÍÑÉ••Ğ)İ¥Ñ ¥ÑÌ•¹ÑÉ”±•…È½˜Ñ¡”½ÉÉ¥‘½È…¹¡…±˜¥ÑÌ‘•ÁÑ ¥¹Í¥‘”¥Ğ¸Q¡…Ğ¥Ì•á…Ñ±äİ¡…ĞÑ¡”)É•¥Á”¡…‰Õ¥±Ğè¥ĞÉ•…Ñ¡”€àÀ™Ğ™É½¹Ñ…”‰…¹‘Ì…Ì•¹ÑÉ”µ±¥¹•ÌÑ¼Í¥Ğ=8É…Ñ¡•ÈÑ¡…¸…Ì•‘•Ì)Ñ¼Í¥Ğ	!%9°…¹Ñ¡”İ¡½±”1…­”MÑÉ••ĞÍ¡½ÀÉ½ÜÍÑ½½İ¥Ñ ¥ÑÌ™É½¹Ğ¡…±˜¥¸Ñ¡”ÍÑÉ••Ğ…¹¥ÑÌ)•¹ÑÉ”İ¥Ñ¡¥¸„µ•ÑÉ”½˜Ñ¡”­•Éˆ±¥¹”¸½Õ¹Ñ¥¹œ™½½ÑÁÉ¥¹ÑÌ¥¹ÍÑ•…½˜•¹ÑÉ•Ì™¥¹‘Ì€¨¨ÔØ¨¨)ÍÑÉÕÑÕÉ•Ìİ¥Ñ Í½µ”Á…ÉĞ¥¸„½ÉÉ¥‘½È‰•™½É”Ñ¡¥ÌÍ±¥”…¹€¨¨ÌÌ¨¨…™Ñ•È¥Ğ¸((¨©Q¡É•”½˜Ñ¡”µ½Ù•Ì½Õ±¹½ĞÍ¥µÁ±äÍÑ•À‰…¬¸¨¨Á¡åÍ¥¥…¹Í}½™™¥•€Í¹…ÁÁ•¥¹Ñ¼Ñ¡”¥ÉÍĞ)AÉ•Í‰åÑ•É¥…¸¡ÕÉ °¥¹™}Á…­•É}‘İ•±±¥¹€¥¹Ñ¼„É•Í•ÉÙ•Á¡…Í”´ÈÍ±½Ğ°¥¹™}½½Á•É…•}Í½ÕÑ¡€)¥¹Ñ¼Ñ¡”M½ÕÑ 	É…¹ ƒŠPÍ¼•… İ•¹ĞÑ¼Ñ¡”¹•…É•ÍĞÁ½Í¥Ñ¥½¸±•…É¥¹œÑ¡”½ÉÉ¥‘½È°•Ù•Éä)½µµ¥ÑÑ•™½½ÑÁÉ¥¹Ğ‰ä€Ì´°Ñ¡”Ñİ¼Õ¹¥¹ÍÑ…¹Ñ¥…Ñ•Á¡…Í”´ÈÉ•¥Á•Ì…¹Ñ¡”¡•¥¡Ñ™¥•±Ì‘Éä)½Ù•É•É½Õ¹¸Q¡”Á¡åÍ¥¥…¸Ì½™™¥”¥Ì€ÄÜ¸Ü´™É½´İ¡•É”¥Ğİ…Ì‰•…ÕÍ”Ñ¡”¹•…É•ÍĞ™É•”)É½Õ¹Ñ¼¥ÑÌ1…­”MÑÉ••Ğ™É½¹Ñ…”¥Ì„±½Ğ‰…¬™É½´¥Ğ¸€¨©9½Ñ¡¥¹œİ…ÌÉ•É…‘•¸¨¨Q¡•Í”)Á½Í¥Ñ¥½¹Ìİ•É”½¹©•ÑÕÉ…±€‰•™½É”…¹…É”½¹©•ÑÕÉ…±€…™Ñ•Èì±•…É¥¹œÑ¡”É½…‘İ…ä¥Ì¹½Ğ)ÍÑ…¹‘¥¹œ½¸„É•½Ù•É•±½Ğ°…¹Ñ¡”É•¥Á”Í…åÌÍ¼İ¡•É”¥ĞÕÍ•Ñ¼Í…äÑ¡”•¹ÑÉ•Ìİ•É”‰…¹)…ÍÍ¥¹µ•¹ÑÌ…±½¹”¸((¨©]¡…Ğ¥Ì±•™Ğ¥¸Ñ¡”É½…¥Ìµ½ÍÑ±ä¹½Ğ„‘•™•Ğ°…¹½¹”Á…ÉĞ½˜¥Ğ¥Ì„µ•…ÍÕÉ•µ•¹Ğ¸¨¨½ÕÈ)…¹½¹åµ½ÕÌÉ½½™Ì™É½´Ñ¡”¥¹™¥±°•¹•É…Ñ½ÉÌ¥¹¡•É¥ĞÑ¡¥Ì…Ñ”İ¡•¸Ñ¡…ĞÁ…É•°¹•áĞÉÕ¹Ì¸Q¡”)½Ñ¡•È€Èä…É”¡…¹µÁ±…•É•½É‘Ìİ¥Ñ „™É½¹Ñ…”…ÉÕµ•¹Ğ‰•¡¥¹Ñ¡•´°…¹€¨©Ñ¡¥ÉÑ••¸…É”½¸)M½ÕÑ ]…Ñ•ÈMÑÉ••Ğ¨¨ƒŠPİ¡•É”°İ…±­¥¹œ¹½ÉÑ ™É½´Ñ¡”½µµ¥ÑÑ••¹ÑÉ•±¥¹”°Ñ¡”ÑÉ…•€ÄàÌĞ)İ…Ñ•É±¥¹”¥Ì€¨¨ÄÀ¸ÜÔ´…İ…ä…Ğ€¬ÄàÀ……¥¹ÍĞ„€ÄÈ¸Ää´¡…±˜µ½ÉÉ¥‘½È¨¨¸Q¡”Á±…ÑÑ•€àÀ™ĞÍÑÉ••Ğ)Ñ¡•É”ÉÕ¹Ì€Ä¸Ğ´¥¹Ñ¼Ñ¡”É¥Ù•È°…¹Ñ¡”ÍÁ…É”¥ÌÕ¹‘•È€Ì´…Ğ™½ÕÈµ½É”½˜•±•Ù•¸ÍÑ…Ñ¥½¹Ì¸=¸)Ñ¡…ĞÉ•… „‰Õ¥±‘¥¹œ½¸Ñ¡”¹½ÉÑ Í¥‘”½˜M½ÕÑ ]…Ñ•È…¹¹½Ğ‰”‰½Ñ ½ÕÑÍ¥‘”Ñ¡”±•…°½ÉÉ¥‘½È)…¹½¸‘Éä±…¹ƒŠPÍ¼Ñ¡”‘¥Í…É••µ•¹Ğ¥Ì‰•Ñİ••¸Ñ¡”Á±…Ğµ½‘Õ±”…¹Ñ¡”‘É…İ¸‰…¹¬°…¹¥Ğİ…¹ÑÌ)„É•…‘¥¹œ½˜Ñ¡”ÑÉ…Ù•±±•İ…äÉ…Ñ¡•ÈÑ¡…¸Ñ¡¥ÉÑ••¸¹Õ‘•É•½É‘Ì¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”±…ÍĞ™½ÕÈ½ÕĞ½˜Ñ¡”É½…°…¹Ñ¡”É½ÜÑ¡…Ğİ…Ì…¥µ•…ĞÑ¡”ÍÑÉ••ÑÌ((¨©,ÜÁ¡…Í”Ñİ¼€¡ˆ¤¸¨¨Q¡”™½ÕÈ…¹½¹åµ½ÕÌÉ½½™ÌÑ¡”ÁÉ•Ù¥½ÕÌÍ±¥”‘•±¥‰•É…Ñ•±ä±•™Ğ¥¸„Á±…ÑÑ•)½ÉÉ¥‘½È…É”½ÕĞ½˜¥Ğ°…¹‰½Ñ ¥¹™¥±°•¹•É…Ñ½ÉÌ¹½Ü…Í¬Ñ¡”½ÉÉ¥‘½ÈÅÕ•ÍÑ¥½¸Ñ¡É½Õ Ñ¡”Í…µ”)Ñ½½±Ì½Á±…Ñ}½ÉÉ¥‘½ÉÌ¹Áå€Ñ¡”¡½ÕÍ•¡½±•¹•É…Ñ½È…¹Ñ¡”É¥É•Á½ÉĞÉ•…¸€¨©9¼•¹•É…Ñ•)Á±…•µ•¹Ğ…¹åİ¡•É”¥¸Ñ¡¥Ì‘…Ñ…Í•ĞÍÑ…¹‘Ì¥¸„Á±…ÑÑ•ÍÑÉ••Ğ½ÉÉ¥‘½È¸¨¨½½ÑÁÉ¥¹ÑÌİ¥Ñ Í½µ”)Á…ÉĞ¥¹Í¥‘”½¹”è€¨¨ÌÌƒŠH€Èä¨¨ìÑ¡”€Èä…É”¡…¹µÁ±…•É•½É‘Ìİ¥Ñ „™É½¹Ñ…”…ÉÕµ•¹Ğ…¹…É”¹½Ğ)Ñ¡¥ÌÍ±¥”ÌÑ¼µ½Ù”¸Y•É¥™¥•Ñ¡”…Ñ”‰¥Ñ•Ì‰äÁÕÑÑ¥¹œ½¹”É•½É‰…¬İ¡•É”¥Ğİ…Ìè¥Ğ™…¥±Ì)İ¥Ñ Ñ¡”É•½É¹…µ•…¹Ñ¡”‘•ÁÑ µ•…ÍÕÉ•¸((¨©Q¡”™½ÕÈİ•É”½¹”É½ÜÌÍÁ…¥¹œ¸¨¨Q¡”Á…É•°Ì•¥¡Ğ…¹¥±±…Éä‰Õ¥±‘¥¹Ì¡…±½…°Ù…±Õ•Ì½˜(ÌÄĞ°€ĞÌà°€ÔØÀ°€ØàÜ°€àÄÀ…¹€ÌÄÔ°€ÔÔä°€àÀäƒŠP„€¨¨ÄÈÌ´Á¥Ñ °İ¡¥ ¥ÌÑ¡”‰±½¬Á¥Ñ ¨¨ƒŠPÍ¼½¹”)å…É‰Õ¥±‘¥¹œÍÑ½½…ĞÑ¡”•…ÍÑ•É¸•‘”½˜•Ù•Éä‰±½¬°„‰Õ¥±‘¥¹œÌİ¥‘Ñ ™É½´Ñ¡”¹•áĞÍÑÉ••Ğ°)•¥¡ĞÑ¥µ•Ì½Ù•È¸Q¡”•¹•É…Ñ½ÈÑ¡…ĞİÉ½Ñ”Ñ¡•´Ñ•ÍÑ•¹½Ñ¡¥¹œè¹½Ğ½Ù•É±…À°¹½Ğİ…Ñ•È°¹½Ğ)É½Õ¹°¹½ĞÑ¡”ÍÑÉ••Ğ¸((¨©!…±˜½˜Ñ¡•´Á…ÍÍ•°…¹İ¡äÑ¡•äÁ…ÍÍ•¥ÌÑ¡”Á…ÉĞİ½ÉÑ ­••Á¥¹œ¸¨¨Q¡”™½ÕÈÑ¡…Ğ¥¹ÑÉÕ‘•(£Š"HÄ¸ÀÌÑ¼ƒŠ"HĞ¸ÌÈ´¥¹Í¥‘”Ñ¡”É½…‘İ…ä¤…É”Ñ¡”™½ÕÈ±…É•ÍĞ…¹¥±±…Éä™½½ÑÁÉ¥¹ÑÌ¥¸Ñ¡”Á…É•°ìÑ¡”)™½ÕÈÑ¡…Ğ±•…É•¥Ğ…É”Ñ¡É•”ÁÉ¥Ù¥•Ì…¹„Íµ…±°Í¡•°±•…È‰ä€¨¨Ä¸ÓŠLÈ¸Ä´……¥¹ÍĞÑ¡¥Ì)‘…Ñ…Í•ĞÌ½İ¸ƒ
ÄÈÀ´•½É•™•É•¹”¨¨¸Q¡•äİ•É”¹½ĞÁ±…•±•…È½˜Ñ¡”ÍÑÉ••Ğ°Ñ¡•äİ•É”Ñ½¼Íµ…±°)Ñ¼É•… ¥ĞƒŠPÍ¼„™¥à…¥µ•½¹±ä…ĞÑ¡”™½ÕÈ™…¥±ÕÉ•Ìİ½Õ±¡…Ù”½ÉÉ•Ñ•™½ÕÈ¹Õµ‰•ÉÌ…¹±•™Ğ)Ñ¡”ÉÕ±”Ñ¡…ĞÁÉ½‘Õ•Ñ¡•´¸±°•¥¡Ğµ½Ù•¥¹ÍÑ•…°‰ä½¹”…ÉÕµ•¹Ğè•… ¹½ÜÍÑ…¹‘Ì‘¥É•Ñ±ä)‰•¡¥¹Ñ¡”•…ÍÑ•É¹µ½ÍĞÁÉ¥¹¥Á…°É½½˜½˜¥ÑÌ½İ¸‰±½¬°€ÈĞ´‰…¬™½ÈÑ¡”É•…Èå…É‘Ì…¹€ÈÄ´™½È)Ñ¡”Í•ÉÙ¥”å…É‘Ì°‰•…ÕÍ”„É•…Èå…É‰•±½¹ÌÑ¼„±½Ğ…¹„±½Ğ‰•±½¹ÌÑ¼„¡½ÕÍ”¸€ÄßŠLÌÈ´½˜)µ½Ù•µ•¹Ğ¸((¨©9½Ñ¡¥¹œİ…ÌÉ•É…‘•…¹¹½Ñ¡¥¹œİ…Ì…‘½ÁÑ•¸¨¨Q¡•Í”Á½Í¥Ñ¥½¹Ìİ•É”½¹©•ÑÕÉ…±€‰•™½É”…¹)…É”½¹©•ÑÕÉ…±€…™Ñ•Èì±•…É¥¹œÑ¡”É½…‘İ…ä¥Ì¹½ĞÍÑ…¹‘¥¹œ½¸„É•½Ù•É•±½Ğ°…¹ÍÑ…¹‘¥¹œ)‰•¡¥¹…¸…¹½¹åµ½ÕÌÉ½½˜¥Ì¹½Ğ•Ù¥‘•¹”½˜Í•ÉÙ¥¹œ¥Ğ¸Q¡”¡½ÕÍ•¡½±±•‘•È­•åÌ½¸ÍÑÉÕÑÕÉ”¥)É…Ñ¡•ÈÑ¡…¸½¸Á½Í¥Ñ¥½¸°Í¼Ñ¡”€àÌ…‘½ÁÑ•É½½™Ì­•ÁĞÑ¡•¥È¡½ÕÍ•¡½±‘Ì…É½ÍÌÑ¡”µ½Ù”ƒŠPİ¡¥ ¥Ì)İ¡…Ğµ…‘”Ñ¡”½ÕÁ±¥¹œÑ¡”ÁÉ•Ù¥½ÕÌÍ±¥”¥Ñ•„É”µ‘•É¥Ù…Ñ¥½¸É…Ñ¡•ÈÑ¡…¸„É”µ…ÉÕµ•¹Ğ¸Q¡”)9½ÉÑ Á…É•°…ÉÉ¥•ÌÑ¡”Í…µ”…Ñ”…¹¥Ğ‰¥¹‘Ì¹½Ñ¡¥¹œÑ½‘…äèÑ¡”É¥½Ù•ÉÌ¹¼9½ÉÑ ¥Ù¥Í¥½¸)‰±½¬°‰•…ÕÍ”Ñ¡…ĞÍÑÉ••Ğ½¹ÑÉ½°¥Ìİ¡…Ğƒ
œLäÍÑ¥±°É•½É‘Ì…Ì½İ•¸•Ñ…¥°è)‘½Ì½IMI ½Ñ¡½µÁÍ½¹}Á±…Ñ}É¥¹µ‘€ƒ
œ€İˆ¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠP½¹”İ…äÑ¼¼Í½µ•İ¡•É”°É…‘•ì…¹Ñ¡”¡…±˜½˜Ñ¡”…Ñ”Ñ¡…Ğİ…Ì¹½ĞÉÕ¹¹¥¹œ((¨©,ä¸¨¨Y¥•İÁ½¥¹ÑÌ…¹Ñ¡”Á±…”Í•…É İ•É”Ñİ¼±¥ÍÑÌ½˜Ñ¡”Í…µ”É½Õ¹¥¹Í¥‘”M•ÑÑ¥¹Ì¸)Q¡•ä…É”¹½Ü½¹”¼Ñ½€Ñ…ˆ°Í•½¹¥¸Ñ¡”ÍÑÉ¥À…™Ñ•È½¹ÑÉ½±Ì°½Á•¹•‰ä€ñ­‰ùğ½­‰øè€à)…ÕÑ¡½É•Ù¥•İÁ½¥¹ÑÌ°€ĞÙ•É¥™¥•©Õ¹Ñ¥½¹Ì°€ÈÈÈÍÑÉÕÑÕÉ•Ì°‰Õ¥±Ğ™É½´Ñ¡”Í•¹”°Ñ¡”¥¹‘•à…¹)Ñ¡”É•¥ÍÑÉäÉ…Ñ¡•ÈÑ¡…¸™É½´„µ•¹ÔÍ½µ•‰½‘äµ…¥¹Ñ…¥¹Ì¸€‰Ñ¸µ¡•±Á€¥Ì„¡…µ‰ÕÉ•È¸((¨©Q¡”Á…É•°…Í­•™½È‘½Õµ•¹Ñ••¹ÑÉ¥•Ì½¹±ä°…¹Ñ¡…ĞÑÕÉ¹•½ÕĞÑ¼‰”Ñ¡”İÉ½¹œ±¥ÍĞ¸¨¨)9¼ÍÑÉÕÑÕÉ”Á½Í¥Ñ¥½¸¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ¥ÌÉ…‘•‘½Õµ•¹Ñ•‘€ƒŠP€¨¨ÔĞ…É”¥¹™•ÉÉ•‘€…¹€ÄØà)½¹©•ÑÕÉ…±€¨¨ƒŠPÍ¼‘½Õµ•¹Ñ•µ½¹±äİ½Õ±¡…Ù”Í¡¥ÁÁ•™½ÕÈ©Õ¹Ñ¥½¹Ì¸Ù•ÉäÍÑÉÕÑÕÉ”É•ÍÕ±Ğ)¥¹ÍÑ•……ÉÉ¥•Ì¥ÑÌ½İ¸Á±…•µ•¹Ğ¹Á½Í¥Ñ¥½¹}½¹™¥‘•¹•€°¥¸Ñ¡”Í…µ”Ñ¡É•”İ½É‘Ì…¹Ñ¡É•”)½±½ÕÉÌÑ¡”‰Õ¥±‘¥¹œ…ÉÕÍ•Ì°…¹Ñ¡”Ñ…ˆÌÍÕµµ…Éä±¥¹”½Õ¹ÑÌÑ¡”É…‘•Ì™É½´Ñ¡”±¥ÍĞ¥Ğ)Á…¥¹ÑÌ¸]¡…ĞÍÕÉÙ¥Ù•Ì…‰½ÕĞ„‰Õ¥±‘¥¹œ¥ÌÕÍÕ…±±ä„ÍÑÉ••Ğ…¹„Í¥‘”½˜¥Ğ°Í¼„İ•±°µ‘½Õµ•¹Ñ•)Ñ…Ù•É¸İ¥Ñ „½¹©•ÑÕÉ…°Á½Í¥Ñ¥½¸¥ÌÑ¡”¹½Éµ…°…Í”¡•É”É…Ñ¡•ÈÑ¡…¸„™…¥±ÕÉ”ƒŠP…¹Ñ¡”µ•¹Ô)¹½ÜÍ…åÌİ¡¥ ¥Ìİ¡¥ …ĞÑ¡”µ½µ•¹ĞÑ¡”Ù¥Í¥Ñ½È¡½½Í•Ìİ¡•É”Ñ¼¼¸Q¡”…Ñ”½µÁ…É•Ì•Ù•Éä)¡¥À……¥¹ÍĞÑ¡”É•½É¥Ğ©ÕµÁÌÑ¼ì„µ•¹ÔÑ¡…ĞÉ…‘•„Á½Í¥Ñ¥½¸µ½É”­¥¹‘±äÑ¡…¸Ñ¡”É•½É)‘½•Ìİ½Õ±‰”Ñ¡¥ÌÁÉ½©•ĞÌİ½ÉÍĞ­¥¹½˜‰Õœ¸((¨©Qİ¼‘•™•ÑÌÑ¡”¹•Ü…ÍÍ•ÉÑ¥½¹Ì…Õ¡Ğ¥¸Ñ¡•¥È½İ¸Í±¥”¸¨¨Q¡”™¥Ù”µÑ…ˆÍÑÉ¥À™¥ÑÑ•€ÌØÀÁà)½¹±ä‰ä™±•àµÍ¡É¥¹­¥¹œ±…‰•±Ì½ÕĞÁ…ÍĞÑ¡•¥È½İ¸‰ÕÑÑ½¹ÌƒŠP½¹”Ñ¥‘äÉ½Ü°µ•…ÍÕÉ•°…¹„µ•ÍÌÑ¼)±½½¬…ĞìÑ¡”‘•Í­Ñ½ÀÁ…¹•°¥Ì€ÌàÀÁà¹½Ü°Ñ…ˆÁ…‘‘¥¹œ¥Ì€ØÁà…¹µ½‰¥±”ÑåÁ”€ÄÄ¸ÔÁà°±•…Ù¥¹œ)…‰½ÕĞ€ÈÀÁà½˜Í±…¬…Ğ‰½Ñ Ù¥•İÁ½ÉÑÌ°…¹Ñ¡”…Ñ”µ•…ÍÕÉ•ÌÉ½İÌ°½Ù•É™±½Ü…¹ÍÅÕ••é”…Ğ‰½Ñ ¸)Í¥áÑ Ñ…ˆ‘½•Ì¹½Ğ™¥Ğ…¹İ¥±°™…¥°Ñ¡•É”¸Q¡”½¹™¥‘•¹”¡¥ÁÌ…±Í¼É•¹‘•É•¥‘•¹Ñ¥…±±ä)É•ä°‰•…ÕÍ”„Á±…¥¸€¹©ÕµÀµÉ•ÍÕ±ĞÍµ…±±€ÉÕ±”½ÕÑÉ…¹­Ì€¹½¹˜µ¥¹™•ÉÉ•‘€½¸ÍÁ•¥™¥¥ÑäìÑ¡”)…Ñ”¹½ÜÉ•ÅÕ¥É•ÌÑ¡”É…‘•ÌÑ¼‘¥™™•È‰ä½±½ÕÈ…Ìİ•±°…Ì‰äİ½É¸((¨©Q¡”‘•Í­Ñ½À¡…±˜½˜Ñ½½±Ì½Íµ½­•}É•¹‘•É•È¹µ©Í€¡…¹½Ğ‰••¸ÉÕ¹¹¥¹œ°…¹¥Ğ¥Ì¹½Ğ±•…È™½È)¡½Ü±½¹œ¸¨¨%Ğ…‰½ÉÑ••Ù•ÉäÉÕ¸…ĞÑ¡”™¥ÉÍĞ±¥¬½¸Ñ¡”µ•¹Ô‰ÕÑÑ½¸ƒŠP½¸µ…¥¹€…Ìİ•±°…Ì½¸)Ñ¡¥Ì‰É…¹ °É•ÁÉ½‘Õ¥‰±äƒŠP…¹•Ù•Éä‘•Í­Ñ½À…ÍÍ•ÉÑ¥½¸…™Ñ•ÈÑ¡…ĞÁ½¥¹Ğ°É½Õ¡±ä„Ñ¡¥É½˜Ñ¡”)ÍÕ¥Ñ”°Í¥µÁ±ä¹•Ù•È•á•ÕÑ•İ¡¥±”Ñ¡”ÉÕ¸É•Á½ÉÑ•„™…¥±ÕÉ”Ñ¡…ĞÉ•…±¥­”„‰É½­•¸½¹ÑÉ½°¸)9½Ñ¡¥¹œİ…Ì½Ù•É¥¹œÑ¡”‰ÕÑÑ½¸è•±•µ•¹ÑÉ½µA½¥¹Ñ€É•ÑÕÉ¹•Ñ¡”‰ÕÑÑ½¸¥ÑÍ•±˜…Ğ¥ÑÌ½İ¸•¹ÑÉ”°)İ¥Ñ ¹¼Á½¥¹Ñ•È±½¬°Ñ¡”Á…”Ù¥Í¥‰±”…¹™½ÕÍ•¸Q¡”…ÕÍ”¥ÌÑ¡”Í•¹”Ì½İ¸İ•¥¡Ğ¸Ğ(ÔÌÌ€ÀÀÀÑÉ¥…¹±•Ì½¸„Í½™Ñİ…É”É•¹‘•É•È½¹”…¹¥µ…Ñ¥½¸™É…µ”Ñ…­•Ì€¨¨À¸ĞÛŠLÄ¸ÄÀÌ€¡µ•…ÍÕÉ•¤¨¨°)…¹A±…åİÉ¥¡ĞÌ±¥¬İ…¥ÑÌ™½ÈÑ¡”•±•µ•¹ĞÑ¼¡½±ÍÑ¥±°…É½ÍÌ™É…µ•Ì‰•™½É”¥Ğİ¥±°¡¥ĞµÑ•ÍĞ)¥Ğ°Í¼€ÌÀÌ½˜‘•™…Õ±Ğ…Ñ¥½¸‰Õ‘•Ğİ…Ì‰•¥¹œÍÁ•¹Ğ½¸™É…µ•ÌÉ…Ñ¡•ÈÑ¡…¸½¸Ñ¡”Á…”¸Q¡”)‰Õ‘•Ğ¥Ì¹½Ü€äÀÌƒŠPÉ½½´™½È„Í±½Üµ…¡¥¹”°¹½ĞÁ•Éµ¥ÍÍ¥½¸™½È„‰É½­•¸½¹ÑÉ½°°Í¥¹”„±¥¬)Ñ¡…Ğ¹•Ù•È±…¹‘ÌÍÑ¥±°™…¥±Ì¸€¨©Q¡¥Ì¥Ì„ÍÑ…¹‘¥¹œ¡…é…É°¹½Ğ„™¥á•½¹”¨¨èÑ¡”Í…µ”ÍÑ…ÉÙ…Ñ¥½¸)İ¥±°É•ÑÕÉ¸…ÌÑ¡”Ñ½İ¸É½İÌ€¡I=5@,ÄĞ…±É•…‘äÉ•½É‘Ì€Ø€”½˜ÑÉ¥…¹±”¡•…‘É½½´¤°…¹Ñ¡”)¹•áĞÍåµÁÑ½´İ¥±°……¥¸±½½¬±¥­”„U$‰ÕœÉ…Ñ¡•ÈÑ¡…¸„‰Õ‘•Ğ¸™Õ±°Ñİ¼µÙ¥•İÁ½ÉĞÁ…ÍÌ¹½Ü)Ñ…­•ÌÕÁİ…É‘Ì½˜Ñ•¸µ¥¹ÕÑ•Ì¡•É”ìM5=-}Y%]A=IPõµ½‰¥±•ñ‘•Í­Ñ½Á€ÉÕ¹Ì½¹”¡…±˜İ¡¥±”)¥Ñ•É…Ñ¥¹œ…¹ÁÉ¥¹ÑÌÑ¡…Ğ¥Ğ¥Ì¹½ĞÑ¡”…Ñ”¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠP„¹Õµ‰•ÈÑ¡…Ğİ…ÌİÉ¥ÑÑ•¸°Ù…±¥‘…Ñ•°Í¡¥ÁÁ•…¹¹•Ù•ÈÉ•…((¨©,Ì°½Ù•É…”¸¨¨Ù•Éä™±½É„é½¹”É•½É…ÕÑ¡½ÉÌ½Ù•È¹µ…ÑÉ¥á}™É…Ñ¥½¹€ƒŠP¡½ÜµÕ ½˜Ñ¡”)É½Õ¹Ñ¡…Ğ½µµÕ¹¥ÑäÌµ…ÑÉ¥à½Ù•ÉÌƒŠPİ¥Ñ „‰…É•}Í½¥±}™É…Ñ¥½¹€‰•Í¥‘”¥Ğ¸Ñ½½±Ì½Ù…±¥‘…Ñ”¹Áå€)¡…Ì…Ñ•‰½Ñ Í¥¹”Ñ¡”É•½É‘Ìİ•É”İÉ¥ÑÑ•¸°…¹¥¹‘•à¹©Í½¹€‘•¹½Éµ…±¥Í•ÌÑ¡”‰…É”µÍ½¥°™¥ÕÉ”)ÍÁ•¥™¥…±±äÍ¼Ñ¡”É½Õ¹Í¡…‘•È…¸™•Ñ ¥Ğ½¹”¸€¨©É•¹‘•É•ÉÌ½İ•ˆ½©Ì½™±½É„¹©Í€¡…¹•Ù•È…Í­•)™½È•¥Ñ¡•È¸¨¨±°Ñ•¸½µµÕ¹¥Ñ¥•Ìİ•É”Á±…¹Ñ•…ĞÑ¡”Í¥¹±”±…ÑÑ¥”‘•¹Í¥Ñä0ÌÈÑÕ¹•½¸±½Í•)İ•ĞÁÉ…¥É¥”°Í¼„Í•ÑÑ±•Ñ½İ¸İ¡½Í”½İ¸É•½ÉÍ…åÌ€¨¨ĞÔ€”½˜¥ÑÌÉ½Õ¹¥Ì‰…É”¨¨İ…Ì‘É…İ¸İ¥Ñ )Ñ¡”É½Õ¹±½Í•°…¹Í¼İ•É”Ñ¡”Í¡…‘•É¥Ù•É‰…¹¬Õ¹‘•ÉÍÑ½Éä€ À¸ĞÔ¤°Ñ¡”™½É•ÍĞ™±½½È€ À¸ÌÔ¤…¹)Ñ¡”±…­•Í¡½É”Í…¹€ À¸ÌÔ¤¸()Q¡”™É…Ñ¥½¸¥Ì¹½ÜÑ¡”ÁÉ½‰…‰¥±¥ÑäÑ¡…Ğ„µ…ÑÉ¥à±…ÑÑ¥”Í±½Ğ…ÉÉ¥•Ì„Á±…¹ĞƒŠP¹•…ÈÑÕ™ÑÌ…¹)µ¥…É‘Ì…±¥­”°‰•…ÕÍ”Ñ¡¥¹¹¥¹œ½¹”…¹¹½ĞÑ¡”½Ñ¡•Èİ½Õ±ÁÕĞ„Í•…´•á…Ñ±ä…ĞÑ¡”É½ÍÍ½Ù•È)İ¡•É”Ñ¡”¡…¹”½˜É•ÁÉ•Í•¹Ñ…Ñ¥½¸¥Ìµ•…¹ĞÑ¼‰”¥¹Ù¥Í¥‰±”¸%Ğ¥ÌÑ¡”Í…µ”ÉÕ±”Ñ¡”™½Éˆ±…å•È)¡…Ì…±İ…åÌ…ÁÁ±¥•Ñ¼¥ÑÌ½İ¸É•½É‘•‘•¹Í¥Ñ¥•Ì°½¸Ñ¡”™¥•±Ñ¡”µ…ÑÉ¥à±…å•È¥¹½É•¸((´€¨©]•ĞÁÉ…¥É¥”¥ÌÕ¹Ñ½Õ¡•¨¨°‰•…ÕÍ”¥ĞÉ•½É‘Ì€Ä¸ÀÀ…¹€Ä¸ÀÀ¥ÌÑ¡”…¹¡½È¸9½Ñ¡¥¹œÑ¡”(€Ñ¡É•”µÉ¥Ñ¥ŒÁÉ…¥É¥”Íİ••ÀÑÕ¹•¡…Ìµ½Ù•°…¹Ñ¡”¡…¹”…¸½¹±ä•Ù•È€©É•µ½Ù”¨¥¹ÍÑ…¹•Ì¸(€5•…ÍÕÉ•…Ğ€ÄÈàÃ\àÀÀ……¥¹ÍĞµ…¥¹€…ĞÑ¡É•”™¥á•ÍÑ…Ñ¥½¹Ìèİ•ĞÁÉ…¥É¥”€¨¨ÌØÀ€äÜäÑÉ¥Ì……¥¹ÍĞ(€€ÌØÀ€àØÌ¨¨€ ¬À¸ÀÌ€”°İ¡¥ ¥ÌÑ¡”É•Í¡Õ™™±•É…¹‘½´‘É…Ü°¹½Ğ¹•Ü•½µ•ÑÉä¤°Í•ÑÑ±•Ñ½İ¸(€€¨¨ĞÈä€ÈàÄ……¥¹ÍĞ€ĞĞÄ€ØàÌ¨¨€£Š"HÈ¸à€”°€Ì€ÈÜà™±½É„¥¹ÍÑ…¹•Ì……¥¹ÍĞ€Ì€àĞÈ¤°µ…ÉÍ •‘”(€€¨¨Èää€ÄØÄ……¥¹ÍĞ€ÌÀà€ÈÌÔ¨¨€£Š"HÈ¸ä€”¤¸Q¡”Í•¹”•ÑÌ±¥¡Ñ•È•á…Ñ±äİ¡•É”„É•½ÉÍ…åÌÑ¡”(€É½Õ¹¥Ì‰…É”¸(´€¨©5•…ÍÕÉ•°…É½ÍÌÑ¡”•¥¡Ğ½µµÕ¹¥Ñ¥•ÌÑ¡…Ğ¡…Ù”„±•…¸Í…µÁ±¥¹œÍÑ…Ñ¥½¸¨¨èÁ±…¹Ñ•‘•¹Í¥Ñä(€¹½ÜÍÁ…¹Ì€¨¨È¸ÈÇŠLØ¸äÀÑÕ™ÑÌÁ•È·
È¨¨İ¡•É”¥Ğİ…Ì½¹”™¥ÕÉ”•Ù•Éåİ¡•É”°…¹Ñ¡”¥µÁ±¥•(€™Õ±°µ½Ù•È‘•¹Í¥Ñä…É••Ì…Ğ€¨¨Ø¸ÌÇŠLà¸ÄÔ¨¨……¥¹ÍĞ„±…ÑÑ¥”…ÉÉå¥¹œ€Ü¸ÌÀ¸(´€¨©Q¡”…Ñ”…Í­Ì‰½Ñ ¡…±Ù•Ì¨¨°‰•…ÕÍ”…¹Íİ•É¥¹œ½¹±äÑ¡”™¥ÉÍĞ¥Ì¡½ÜÑ¡¥Ìİ•¹ĞÕ¹¹½Ñ¥•è(€Ñ¡…Ğ•… ½µµÕ¹¥ÑäÌ…ÕÑ¡½É•¹Õµ‰•ÈÉ•…¡•ÌÑ¡”É•¹‘•É•È€¡É”µ™•Ñ¡•™É½´Ñ¡”É•½É‘Ì°¹½Ğ(€½µÁ…É•……¥¹ÍĞ„½Áä½˜Ñ¡”É•¹‘•É•È¤°…¹Ñ¡…ĞÑ¡”Íİ…É½¸Ñ¡”É½Õ¹™½±±½İÌ¥Ğ¸Q¡”(€Í•½¹…ÍÍ•ÉÑ¥½¸™…¥±Ì¥¸Ñ¡”½Ñ¡•È‘¥É•Ñ¥½¸Ñ½¼ƒŠP¥˜•Ù•Éä½µµÕ¹¥Ñäİ•¹Ğ‰…¬Ñ¼½¹”(€‘•¹Í¥Ñä°Ñ¡”Á•Èµ·
ÈÍÁÉ•…İ½Õ±½±±…ÁÍ”Ñ½İ…É€Ä…¹Ñ¡”¥µÁ±¥•™¥ÕÉ•Ìİ½Õ±™…¸½ÕĞ(€…É½ÍÌÑ¡”€À¸Ì×ŠLÄ¸ÀÀÑ¡”É•½É‘Ì¥Ù”¸(´€¨©=¹”…¹Ñ¤µÙ…Õ¥ÑäÕ…Éµ½Ù•…¹Ñ¡”Ñ½±•É…¹”‘¥¹½Ğ¸¨¨€¨‰‘•Ñ…¥±•™±½É„É½½ÑÌÍ¡…É”Ñ¡”(€Ñ•ÉÉ…¥¸…¹İ…Ñ•ÈÍÕÉ™…•Ìˆ¨É•ÅÕ¥É•Ì„µ¥¹¥µÕ´Í…µÁ±”Í¼Ñ¡…ĞÁ±…¹Ñ¥¹œ¹½Ñ¡¥¹œ…¹¹½ĞÉ•Á½ÉĞ„(€Á•É™•Ğİ½ÉÍĞ•ÉÉ½Èì¥ÑÌÍÑ…Ñ¥½¸ÍÑ…¹‘Ì¥¸Ñ¡”Í•ÑÑ±•Ñ½İ¸°…¹Ñ¡”µ½‰¥±”½¹”Ñ¡•É”¹½Ü¡½±‘Ì(€€ØÜÉ½½Ñ•Á±…¹ÑÌ……¥¹ÍĞ…‰½ÕĞ€ÄÔÀ‰•™½É”¸Q¡”Õ…É¥Ì€ÔÀìÑ¡”€Å”´Ô´É½½ĞÑ½±•É…¹”¥Ì(€Õ¹Ñ½Õ¡•¸Q¡…Ğ¹Õµ‰•È¥Ì„ÁÉ½Á•ÉÑä½˜Ñ¡”‘…Ñ…Í•Ğ¹½ÜÉ…Ñ¡•ÈÑ¡…¸½˜Ñ¡”É•¹‘•É•È¸((¨©Qİ¼™¥¹‘¥¹Ìµ•…ÍÕÉ•½¸Ñ¡”İ…ä°…¹¹½Ğ™¥á•Ñ¡•¸¸	½Ñ ™¥á•€ÈÀÈØ´Àà´ÄÌƒŠPÍ•”‰•±½Ü¸¨¨LÙ„)¥Ñ•´€äÉ•…‘ÌÑ¡”É¥Ù•É}‰…¹­€Í¡½Ğ……¥¹ÍĞé½¹”€ÄÌ½É‘É…ÍÌƒŠP‰ÕĞÉ½Õ¹İ¥Ñ¡¥¸•¥¡Ğµ•ÑÉ•Ì½˜)İ…Ñ•È¥ÌÑ¡”5IM é½¹”‰ä•áÑ•¹Ğ°…¹Ñ¡”Í¡½ĞÌÍİ…É¥Ì•¹Ñ¥É•±äèÀÑ€½èÄÁ€İ¥Ñ ¹¼èÀÅ€¥¸)¥Ğ…Ğ…±°¸¹Ñ¡”€‰øÈÔ´ÍÁÉ¥Ìˆ…É”‰•ÑÑ•È•áÁ±…¥¹•‰äÍÁ•¥•ÌÑ¡…¸‰ä‘•¹Í¥Ñäè)¹ÕÁ¡…É}…‘Ù•¹…€…¹¹åµÁ¡…•…}½‘½É…Ñ…€…É”™±½…Ñ¥¹œµ±•…Ù•…ÅÕ…Ñ¥ÌÉ•½É‘•…Ğ€À¸ÀÇŠLÀ¸ÄÀ´İ¡½Í”)½İ¸…ÁÁ•…É…¹•€Ñ•áĞÍ…åÌÑ¡•ä™±½…Ğ¥¸½Á•¸İ…Ñ•È°…¹Ñ¡•äİ•É”€¨¨Ø¸Ô€”½˜Ñ¡”ÑÕ™ÑÌÍÑ…¹‘¥¹œ)½¸Ñ¡…Ğ‘Éä‰…¹¬¨¨°‰•…ÕÍ”É½±”è•µ•É•¹Ñ€İ…Ì…±°Ñ¡”É•¹‘•É•È½Õ±Í•”¸¥á¥¹œÑ¡…Ğ¥Ì„‘…Ñ„)™¥•±¥¸Ñ¡”ÁÕ‰±¥Í¡•Ù½…‰Õ±…Éä‰•™½É”¥Ğ¥Ì„±¥¹”¥¸Ñ¡”É•¹‘•É•ÈƒŠP„É•¹‘•É•ÈÑ¡…Ğ‘•¥‘•)İ¡¥ Á±…¹ÑÌ™±½…Ğ‰äÉ•…‘¥¹œÑ¡•¥È¡•¥¡ÑÌİ½Õ±‰”Õ•ÍÍ¥¹œ…Ğ•á…Ñ±äÑ¡”Á½¥¹ĞÑ¡¥ÌÁÉ½©•Ğ)É•™ÕÍ•ÌÑ¼¸((ŒŒ9•Ü€ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”Á…‘Ìİ•É”ÍÑ…¹‘¥¹œ½¸Í½¥°°…¹ÁÉ½Í”İ…ÌÑ¡”½¹±äÑ¡¥¹œÑ¡…ĞÍ…¥Í¼((¨©,Ì°Ñ¡”Í•½¹™¥¹‘¥¹œ¸¨¨İ…Ñ•È±¥±ä…¹„…ÑÑ…¥°İ•É”Ñ¡”Í…µ”É•½ÉÑ¼Ñ¡”Á±…•Èè‰½Ñ )É½±”è•µ•É•¹Ñ€°…¹Ñ¡”É½±”¥Ìİ¡…ĞÍÑ…Ñ¥½¸ ¥€É•…¸M¼Ñ¡”µ…ÉÍ ½µµÕ¹¥Ñäİ…ÌÁ±…¹Ñ•)¥‘•¹Ñ¥…±±ä½¸‰½Ñ Í¥‘•Ì½˜¥ÑÌ½İ¸İ…Ñ•É±¥¹”°…¹¹ÕÁ¡…É}…‘Ù•¹…€…¹¹åµÁ¡…•…}½‘½É…Ñ…€ƒŠP(À¸ÀÇŠLÀ¸ÄÀ´°™½É´èµ…Ñ}ÁÉ½ÍÑÉ…Ñ•€°…ÁÁ•…É…¹•€€‰™±½…Ñ¥¹œÁ…‘Ì¥¸½Á•¸İ…Ñ•ÈˆƒŠPÍÑ½½…Ì…¹­±”´)¡¥ µ…ÑÌÉ½½Ñ•¥¸Ñ¡”Í½¥°½˜Ñ¡”‘Éä‰…¹¬¸€¨©Q¡”•Ù¥‘•¹”İ…Ì¥¸Ñ¡”É•½É…¹Õ¹É•…‘…‰±”‰ä)…¹åÑ¡¥¹œ‰ÕĞ„Á•ÉÍ½¸¸¨¨()‘…Ñ„½™±½É„½¥¹‘•à¹©Í½¹€¹½ÜÁÕ‰±¥Í¡•Ì„ÍÕ‰ÍÑÉ…Ñ•Í€Ù½…‰Õ±…Éä…¹•Ù•ÉäÉ½±”è•µ•É•¹Ñ€É•½É)ÍÑ…Ñ•Ì½¹”è()ğÙ…±Õ”ğ¡…‰¥Ğğµ…ä‰”Á±…¹Ñ•ğ)ğ´´µğ´´µğ´´µğ)ğÍ½¥±€ğÉ½½Ñ•É½Õ¹…‰½Ù”Ñ¡”İ…Ñ•ÈìÑ¡”‘•™…Õ±Ğİ¡•¸Ñ¡”™¥•±¥Ì…‰Í•¹Ğğ‘ÉäÉ½Õ¹½¹±äğ)ğÍ…ÑÕÉ…Ñ•‘}Í½¥±€ğÑ¡”•µ•É•¹Ğ¡…‰¥ĞƒŠPİ•ĞÉ½Õ¹=HÍÑ…¹‘¥¹œİ…Ñ•È°™½±¥…”…‰½Ù”Ñ¡”ÍÕÉ™…”ğ‰½Ñ Í¥‘•Ìğ)ğ½Á•¹}İ…Ñ•É€ğÉ½½Ñ•‰•±½ÜÑ¡”ÍÕÉ™…”°±•…Ù•Ì™±½…Ñ¥¹œ=8¥Ğğ½Ù•Èİ…Ñ•È½¹±äğ((´€¨©Q¡”Ù…±¥‘…Ñ½ÈÉ•™ÕÍ•ÌÑ¡”Õ¹Á±…¹Ñ…‰±”É•½É¨¨°¹½Ğ©ÕÍĞÑ¡”Õ¹­¹½İ¸İ½Éè…¸½Á•¹}İ…Ñ•É€(€ÍÁ•¥•Ì¥¸„é½¹”İ¡½Í”•áÑ•¹Ğ¹•Ù•ÈÉ•…¡•Ìİ…Ñ•ÈƒŠP½È„‰Õ™™•ÈÑ¡…ĞÍÑ…ÉÑÌ…ĞÑ¡”‰…¹¬É…Ñ¡•È(€Ñ¡…¸…ĞÑ¡”İ…Ñ•É±¥¹”ƒŠP¥Ì…¸•ÉÉ½È°‰•…ÕÍ”„É•½ÉÑ¡…Ğ…¸¹•Ù•È‰”‘É…İ¸¥Ì„±…¥´Ñ¡”(€İ…±­Ñ¡É½Õ ‘½•Ì¹½Ğµ…­”¸M¥à¹•ÜÍ•±˜µÑ•ÍÑÌ¥¸Ñ½½±Ì½Ñ•ÍÑ}Ù…±¥‘…Ñ”¹Áå€¸(´€¨©Q¡”½µµÕ¹¥Ñä¥ÌÍÁ±¥Ğ°¹½ĞÑ¡”Í±½Ğ‘É½ÁÁ•¸¨¨™±½É„¹©Í€Á¥­Ì™É½´Ñ¡”ÍÕ‰Í•Ğ±•…°½¸Ñ¡”(€Í¥‘”½˜Ñ¡”İ…Ñ•É±¥¹”¥Ğ¥ÌÁ±…¹Ñ¥¹œ°İ¥Ñ Ñ¡”İ•¥¡ÑÌÉ•¹½Éµ…±¥Í•½Ù•ÈÑ¡…ĞÍÕ‰Í•Ğ¸I•™ÕÍ¥¹œ(€Ñ¡”Í±½Ğ…™Ñ•ÈÑ¡”Á¥¬İ½Õ±¡…Ù”‰••¸½¹”±¥¹”Í¡½ÉÑ•È…¹İ½Õ±¡…Ù”Ñ¡¥¹¹•Ñ¡”‘Éäµ…ÉÍ (€•‘”‰äÑ¡”±¥±¥•Ìœ€Ø¸Ô€”Í¡…É”ìµ…ÑÉ¥á}™É…Ñ¥½¹€€À¸ÜÔ‘½•Ì¹½ĞÍÑ½Àµ•…¹¥¹œ€À¸ÜÔ‰•…ÕÍ”Ñİ¼(€½˜Ñ¡…Ğ½µµÕ¹¥ÑäÌÍÁ•¥•Ì™±½…Ğ¸(´€¨©5•…ÍÕÉ•°…Ğ€ÄÈàÃ\àÀÀ¸¨¨¸€à´Íİ••À½˜Ñ¡”µ½‘•±±•‰½àè€¨¨Èää‘Éäµ…ÉÍ µ•‘”ÍÑ…Ñ¥½¹Ì¨¨(€€ ÈàäÁ±…¹Ñ…‰±”…Ğ…±°¤…¹€¨¨ÈàØ½Ù•Èİ…Ñ•È¨¨¸	½Ñ ±¥±¥•Ìİ•É”±•…°…Ğ…±°€Èàä‘ÉäÍÑ…Ñ¥½¹Ì(€…¹…É”¹½Ü±•…°…Ğ¹½¹”ìÑ¡”…ÑÑ…¥°¥ÌÕ¹¡…¹•…Ğ€Èàä‘Éä€¼€ÈÜÌİ•Ğ¸ĞÑ¡”µ…ÉÍ µ•‘”(€ÍÑ…Ñ¥½¸¹•…É•ÍĞÑ¡”™½É­ÌÑ¡”Íİ…É¡½±‘Ì¥ÑÌ‘•¹Í¥ÑäƒŠP€¨¨È€ĞàÌƒŠH€È€ĞàÄÉ½½Ñ•¥¹ÍÑ…¹•Ì°(€€ĞÜ€ÔÔÄƒŠH€ĞÜ€ĞÌÔÑÉ¥…¹±•Ì¨¨ƒŠP…¹Ñ¡”Ñİ¼¡•…‘}É…å€¡•…‘ÌÑ¡…ĞÍÑ½½½¸Ñ¡…Ğ‘Éä‰…¹¬°İ¡¥ (€…É”Ñ¡”±¥±ä‰±½½µÌ°…É”½¹”¸İ•ĞµÁÉ…¥É¥”½¹ÑÉ½°ÍÑ…Ñ¥½¸¥Ì¥‘•¹Ñ¥…°¸(´€¨©Q¡”…Ñ”…Í­ÌÑ¡”Á±…•È°¹½Ğ„½Áä½˜¥ÑÌÉÕ±•Ì¸¨¨™±½É„¹ÍÑ…Ñ¥½¹=˜¡”°¸°ÍÁ•¥•Í%¥€ÉÕ¹Ì(€Ñ¡”Í…µ”ÍÑ…Ñ¥½¸ ¥€Ñ¡”Í…ÑÑ•ÈÉÕ¹ÌìÑ¡”Íµ½­”Íİ••ÁÌÑ¡”‰½àİ¥Ñ ¥Ğ…Ğ‰½Ñ Ù¥•İÁ½ÉÑÌ…¹(€…ÍÍ•ÉÑÌ¹¼™±½…Ñ¥¹œµ±•…Ù•…ÅÕ…Ñ¥Œ¡…Ì„‘ÉäÍÑ…Ñ¥½¸°Ñ¡…ĞÑ¡”±¥±¥•ÌÍÑ¥±°¡…Ù”İ•Ğ½¹•Ì°…¹(€Ñ¡…ĞÑ¡”…ÑÑ…¥°ÍÑ¥±°ÍÑ…¹‘Ì½¸‰½Ñ Í¥‘•ÌƒŠPÑ¡…Ğ±…ÍĞ½¹”‰•…ÕÍ”„Á±…•ÈÑ¡…Ğ¡…É•™ÕÍ•(€€©•Ù•ÉåÑ¡¥¹œ¨½¸Ñ¡…Ğ‰…¹¬İ½Õ±½Ñ¡•Éİ¥Í”É•……Ì„Á…ÍÌ¸(´€¨©]¡…ĞÑ¡¥Ì‘½•Ì¹½Ğ±…¥´¸¨¨Q¡…ĞÑ¡”±¥±¥•Ì…É”…ĞÑ¡”™½É­Ì…Ğ…±°¥ÌÍÑ¥±°¥¹™•ÉÉ•‘€™É½´„(€É•¥½¹…°™±½É„€¡Íİ¥¹­}İ¥±¡•±µ|ÄääÑ€¤°…Ğ„Ñ½­•¸‘•¹Í¥Ñä°…¹İ¡•É”Ñ¡”Á…‘ÌÍ¥Ğİ¥Ñ¡¥¸Ñ¡”(€•¥¡Ğµµ•ÑÉ”µ…ÉÍ •‘”¥ÌÑ¡”Í…ÑÑ•ÈÌ°¹½Ğ„Í½ÕÉ”Ì¸Q¡”¡…¹”µ½Ù•Ì„ÍÁ•¥•Ì™É½´É½Õ¹(€¥Ğ…¹¹½Ğ½ÕÁäÑ¼É½Õ¹¥Ğ…¸ì¥Ğ¥Ì¹½Ğ¹•Ü•Ù¥‘•¹”Ñ¡…Ğ¥Ğİ…ÌÑ¡•É”¸((ŒŒ-¹½İ¸İ•…­¹•ÍÍ•Ì°ÍÑ…Ñ•Á±…¥¹±ä((Á„¸€¨©Q¡”…Ñ”Ñ¡…Ğ•á¥ÍÑÌÑ¼…Ñ „‰Õ¥±‘¥¹œÍÑ…¹‘¥¹œ½¸¹½Ñ¡¥¹œÉ•Á½ÉÑ•„Á•É™•Ğ(€€€±…¹‘¥¹œ™½È„™½ÉĞ€àÌÈ´Á…ÍĞÑ¡”•‘”½˜Ñ¡”İ½É±¸¨¨½ÕÉÑ••¸ÍÑÉÕÑÕÉ•Ìİ•¹Ğ¥¸½¸€ÈÀÈØ´Àà´ÄÄ…Ğ(€€€±½…°€¬ÄÄÌÃŠ˜¬ÄÄàÀìÑ¡””ÄàÌÑ}¡…É‰½É}ÕÑ€¡•¥¡Ñ™¥•±ÍÑ½ÁÌ…Ğ€¬ÌÈÀ¸Q¡…ĞµÕ ¥Ì0ĞÀÌ(€€€ÁÉ½‰±•´…Ğ™½ÕÈÑ¥µ•ÌÑ¡”‘¥ÍÑ…¹”…¹¥Ğ¥Ì¡½¹•ÍÑ±ä‘•±…É•½¸•Ù•ÉäÉ•½É¸€¨©Q¡”Á…ÉĞ(€€€Ñ¡…Ğ¥Ì„‘•™•Ğ¥¸Ñ¡”µ…¡¥¹•ÉäÉ…Ñ¡•ÈÑ¡…¸¥¸Ñ¡”‘…Ñ„¨¨èÑ½½±Ì½¡•¥¡Ñ™¥•±¹Áå€±…µÁÌ(€€€½ÕÑÍ¥‘”Ñ¡”‰½à°Í¼Ñ¡”É½Õ¹µ½¹Ñ…Ğ¡•¬Í…µÁ±•Ñ¡”±…µÁ••‘”™½ÈÑ¡”ÍÑÉÕÑÕÉ”Ì(€€€‰…Í”9™½È•Ù•ÉäÁ½¥¹Ğ½˜¥ÑÌ½ÕÑ±¥¹”°½ĞÑ¡”Í…µ”¹Õµ‰•ÈÑİ¥”°…¹½¹±Õ‘•Ñ¡…ĞÑ¡”(€€€™½ÉĞµ••ÑÌÑ¡”É½Õ¹¸Ù•ÉäÍÑÉÕÑÕÉ”0ĞÀ½Ù•ÉÌİ…Ì…Õ¡Ğ½¹±ä‰•…ÕÍ”Ñ¡”±…µÁ••‘”(€€€Ù…É¥•Ì…±½¹œ„İ…±°…¹ÁÉ½‘Õ•„…ÀìÑ¡”™½ÉĞİ…Ì™…È•¹½Õ ½ÕĞ…¹ÍÅÕ…É”•¹½Õ ½¸Ñ¼(€€€ÁÉ½‘Õ”¹½¹”¸Q¡”…Ñ”½Õ±Í•”‰Õ¥±‘¥¹ÌÑ¡…Ğİ•É”¹•…É±äÉ¥¡Ğ…¹İ…Ì‰±¥¹Ñ¼½¹”Ñ¡…Ğ(€€€İ…Ì½µÁ±•Ñ•±äİÉ½¹œ¸!•¥¡Ñ™¥•±¹½Ù•ÉÌ ¥€¹½Ü…Í­Ìİ¡•Ñ¡•ÈÑ¡•É”¥Ì…¹äÉ½Õ¹Ñ¡•É”…Ğ(€€€…±°‰•™½É”…Í­¥¹œ¡½Ü¡¥ ¥Ğ¥Ì°Ñ¡”Í¡•µ„…ÉÉ¥•Ì…¸½ÕÑÍ¥‘•}µ½‘•±±•‘}É½Õ¹‘€ÍÑ…Ñ”(€€€‰•Í¥‘”…ÁÁÉ½…¡}¹½Ñ}µ½‘•±±•‘€°…¹Ñ¡”‘•±…É…Ñ¥½¸¥Ì¡•­•……¥¹ÍĞÑ¡”µ•…ÍÕÉ•µ•¹Ğ¥¸(€€€‰½Ñ ‘¥É•Ñ¥½¹Ì¸QÕÉ¹¥¹œ¥Ğ½¸¥µµ•‘¥…Ñ•±ä™±…•Ñİ¼ÍÑÉÕÑÕÉ•Ì¥¸½Ñ¡•ÈÁ…É•±ÌÑ¡…Ğ(€€€¹½Ñ¡¥¹œ¡……Õ¡Ğ¸€¨©LÉ”Á…É•°€¡ˆ¤Ñ¡•¸±…¹‘•Ñ¡”Í…µ”‘…ä¨¨…¹Ñ¡”™¥•±¹½ÜÉ•…¡•Ì€¬ÄÜÀÀ°Í¼Ñİ•±Ù”½˜(€€€Ñ¡”™½ÕÉÑ••¸™½ÉĞÍÑÉÕÑÕÉ•Ì±…¹…¹Ñ¡•¥È‘•±…É…Ñ¥½¹Ì…É”½¹”¸Qİ¼‘¼¹½Ğ°™½È„(€€€‘¥™™•É•¹Ğ…¹‰•ÑÑ•ÈÉ•…Í½¸èÑ¡”™½ÉĞÍ¥ÑÌ½¸„Á±…Ñ•…ÔÑ¡…Ğ™…±±ÌÑ¼Ñ¡”É¥Ù•È‰•Ñİ••¸(€€€8€¬ÈĞÔ…¹8€¬ÈÜÀ°…¹Ñ¡”ÍÑ½­…‘”Ì¹½ÉÑ İ…±°…¹Ñ¡”½µµ…¹‘…¹ĞÌÅÕ…ÉÑ•ÉÌÉ½ÍÌÑ¡”(€€€Ñ½À½˜Ñ¡…Ğ™…±°‰ä€Ä¸ĞÀ´…¹€À¸ĞØ´¸€¨©9¼ÕĞ°™¥±°°É•Ù•Ñµ•¹Ğ½È™½Õ¹‘…Ñ¥½¸¥Ìµ½‘•±±•(€€€…¹åİ¡•É”¥¸Ñ¡¥ÌÁÉ½©•Ğ¨¨°…¹Ñ¡”É•…°İ½É¬Á±…¥¹±ä¡…½¹”¸0ĞØİ…ÌÉ•İÉ¥ÑÑ•¸Ñ¡”Í…µ”(€€€‘…äÑ¼Í…äÍ¼¸Q¡”‰±¥¹‘¹•ÍÌÑ¡”™½ÉĞ•áÁ½Í•¥Ì™¥á•É•…É‘±•ÍÌ½˜İ¡•Ñ¡•È…¹åÑ¡¥¹œ(€€€ÕÉÉ•¹Ñ±ä¹••‘ÌÑ¡”¹•ÜÍÑ…Ñ”¸((ÀÀ¸€¨©Q¡”ÁÉ…¥É¥”±½Í•Ì„‰±¥¹Í¥‘”µ‰äµÍ¥‘”……¥¹ÍĞ„)Õ±äÁ¡½Ñ½É…Á °¥¸Õ¹‘•È„Í•½¹°(€€€…¹İ”¹½Ü­¹½Ü•á…Ñ±äİ¡ä¸¨¨™½ÕÈµÁ…É•°Íİ••À½¸€ÈÀÈØ´Àà´ÄÀÁÕĞ•… Á¥•”½˜Ñ¡”(€€€Ù••Ñ…Ñ¥½¸Ñ¡É½Õ ¥ÑÌ½İ¸‰Õ¥±‘•Èµ…¹µÉ¥Ñ¥Œ±½½À……¥¹ÍĞÙ•É¥™¥•Á¡½Ñ½É…Á¡Ì½˜(€€€ÍÕÉÙ¥Ù¥¹œ%±±¥¹½¥ÌÑ…±±É…ÍÌ°İ¥Ñ „‰±¥¹½…ÌÑ¡”©Õ‘•µ•¹Ğ¸Q¡É•”É¥Ñ¥ÌÉ…¸½¸½¹”(€€€¥‘•¹Ñ¥…°Í¡½ĞÍ•Ğ¸±°Ñ¡É•”±½ÍĞ¸Qİ¼½˜Ñ¡•´°½¸‘¥™™•É•¹ĞÉ•™•É•¹•Ì…¹‘¥™™•É•¹Ğ(€€€™É…µ¥¹Ì°±½ÍĞ½¸Ñ¡”€¨©Í…µ”¨¨™•…ÑÕÉ”¸]¡…Ğ™½±±½İÌ¥ÌÑ¡”µ•…ÍÕÉ•ÍÑ…Ñ”°É•½É‘•(€€€‰•…ÕÍ”¥Ğ¥Ìµ½É”ÕÍ•™Õ°Ñ¡…¸Ñ¡”ÍÕµµ…Éä€‰¹••‘Ìİ½É¬ˆè((€€€€´€¨©Q¡”µ¥µ™¥•±Í¡••Ğ¥Ì‘¥Í…É‘•…ĞøĞÔÔ´¸¨¨…¹½ÁäÉ¥¹Ì™É½´€È¸Ô´Ñ¼€ĞÔÌ´Í¥Ğ…Ğ(€€€€€Ñ¡”Íİ…ÉÑ½Àì™É½´€ÔÄÄ¸à´½ÕÑİ…É•Ù•ÉäÉ¥¹œ‘É½ÁÌÑ¼ä€ô€À¸ÀÕ€İ¥Ñ …5…Í¬€ô€Á€…¹(€€€€€Ñ¡”Í¡…‘•È‘¥Í…É‘Ì¥Ğ¸Q¡”Ù••Ñ…Ñ•ÍÕÉ™…”Ñ¡•É•™½É”•¹‘Ìİ¡•É”Ñ¡”™½œ¥Ì½¹±ä(€€€€€€ÈÜ€”°…¹Ñ¡”€äÌ€”¡…é”İ½É±¹©Í€‘•Í¥¹Ì™½È…Ğ€ÄÈäÀ´¥Ì¹•Ù•ÈÉ•¹‘•É•½¹Ñ¼…¹ä(€€€€€Ù••Ñ…Ñ•Á¥á•°¸€¨©±°Ñ¡É•”Á…É•±Ì¡…Ù”‰••¸½¹Ù•É¥¹œ½¸„½±½ÕÈ¹¼Ù¥Í¥‰±”(€€€€€ÍÕÉ™…”¥¸Ñ¡”Í•¹”É•…¡•Ì¸¨¨Q¡¥Ì½¹”™…ĞÁÉ½‘Õ•ÌÑ¡”‰±¥¹Ñ•±°¥¸‰½Ñ Á…¥ÉÌ°(€€€€€Ñ¡”µ¥ÍÍ¥¹œ…•É¥…°É••ÍÍ¥½¸°Ñ¡”½±±…ÁÍ•É…¥¸…¹Ñ¡”É¥¹œÍ•…´‰•±½Ü¸(€€€€´€¨©Q¡•É”¥Ì¹¼…•É¥…°É••ÍÍ¥½¸½¸™±…ĞÉ½Õ¹…¹Ñ¡•É”ÍÑÉÕÑÕÉ…±±ä…¹¹½Ğ‰”¸¨¨Ğ„(€€€€€€Ä¸Øà´•å”İ¥Ñ „€Ô×
ÀÙ•ÉÑ¥…°™¥•±½Ù•È€àÀÀÉ½İÌ°„É½Õ¹Á½¥¹Ğ…Ğ‘¥ÍÑ…¹”€©¨(€€€€€±…¹‘Ì€ÄÈäÀ¸ä½‘€Áà‰•±½ÜÑ¡”¡½É¥é½¸ƒŠPÍ¼Ñ¡”•¹Ñ¥É”™½œÉ…µÀ™É½´€ÄÀ€”Ñ¼€äÌ€”±¥Ù•Ì(€€€€€‰•Ñİ••¸É½İÌ€ĞÀÈ…¹€ĞÀØ¸M¥àÁ¥á•±Ì½˜…Ñµ½ÍÁ¡•É”¥¸…¸€àÀÀµÁ¥á•°™É…µ”¸=¹±äÙ•ÉÑ¥…°(€€€€€ÍÑÉÕÑÕÉ”…ÉÉ¥•¥¹Ñ¼Ñ¡”‘¥ÍÑ…¹”…¸‰ÕäÉ••ÍÍ¥½¸¡•É”ì•áÁ½¹•¹Ñ¥…°‘¥ÍÑ…¹”™½œ(€€€€€…¹¹½Ğ¸(€€€€´€¨©É¥¹œÍ•…´‘É…İÌ„ÍÑÉ…¥¡Ğ±¥¹”…É½ÍÌÑ¡”™É…µ”¸¨¨QU9¹µ¥¹É…‘¥ÕÌ€ô€ÈÜ¸Àµ€°…¹(€€€€€½¸™±…ĞÉ½Õ¹„½¹ÍÑ…¹ĞÉ…‘¥ÕÌµ…ÁÌÑ¼„½¹ÍÑ…¹ĞÍÉ••¸É½ÜƒŠPÁÉ•‘¥Ñ•€ĞĞà¸à°(€€€€€µ•…ÍÕÉ•…ĞÉ½Ü€ĞÔÀ¥¸ÁÉ…¥É¥•}Í½ÕÑ¡€°É…é½ÈµÍÑÉ…¥¡Ğ…É½ÍÌ…±°€ÄÈàÀ½±Õµ¹Ì¸(€€€€´€¨©É…¥¸½±±…ÁÍ•Ìİ¥Ñ ‘•ÁÑ İ¡•É”Ñ¡”Á¡½Ñ½É…Á¡Ìœ¥Ì™±…Ğ¸¨¨€×\Ô¡¥ µÁ…ÍÌI5L¥¸(€€€€€‰…¹‘Ì‘½İ¸™É½´Ñ¡”±…¹½Í­ä‰½Õ¹‘…Éäè½ÕÉÌ€ÄÌ¸à€¼€ÄĞ¸Ø€¼€ÈÄ¸È°‰½Ñ É•™•É•¹•Ì(€€€€€€Äà¸à€¼€ÌÄ¸Ğ€¼€Ìä¸Ì…¹€Ìä¸Ì€¼€ĞÄ¸Ü€¼€ĞÄ¸Ì¸(€€€€´€¨©Q¡”¡½É¥é½¸Ñ¥µ‰•È¥Ì¹•…É±ä…‰Í•¹Ğ¸¨¨Q¥µ‰•È¥Ì‘•Ñ•Ñ•¥¸€¨¨ÌÄ€”¨¨½˜¡½É¥é½¸(€€€€€½±Õµ¹Ì½Ù•É…±°…¹€Ì¸Ø€”…É½ÍÌÑ¡”•¹ÑÉ…°Ñİ¼µÑ¡¥É‘Ì°……¥¹ÍĞ€¨¨ÄÀÀ€”¨¨½˜½±Õµ¹Ì¥¸(€€€€€•Ù•Éä‰…¹½˜Ñ¡”É•™•É•¹”¥¹±Õ‘¥¹œ¥ÑÌ™…¥¹Ñ•ÍĞ¸Q¡”€ËŠLĞÁà‰…¹€©¡•¥¡Ğ¨¥Ì¡½¹•ÍĞ(€€€€€…É¥Ñ¡µ•Ñ¥ŒìÑ¡”•µÁÑ¥¹•ÍÌ¥Ì¹½Ğ¸É½Õ¹Ñ¡…ĞÉ•Á½ÉÑ•É”µÑ½¹¥¹œÑ¡¥Ì‰…¹¡…¥¸™…Ğ(€€€€€É•‘Õ•¥ÑÌ‘•Ñ•Ñ¥½¸½Ù•È™É½´€ÈÄ¸Ä€”Ñ¼€À¸ä€”°…¹Ñ¡”Ñ…É•Ğ¥Ğİ…Ì¥Ù•¸(€€€€€€¡]•‰•È€À¸ÀÌÛŠLÀ¸ÀØÜ¤‘½•Ì¹½Ğ•á¥ÍĞ¥¸Ñ¡”É•™•É•¹”…Ğ…¹äÑ¡É•Í¡½±ƒŠPÑ¡…Ğ•ÉÉ½Èİ…Ì(€€€€€Ñ¡”‰É¥•˜Ì°¹½ĞÑ¡”‰Õ¥±‘•ÈÌ¸(€€€€´€¨©É½İ¹ÌÉ•……Ì‰½Õ±‘•ÉÌ¸¨¨¥¹”µ‘•Ñ…¥°É…Ñ¥¼€À¸ÈÏŠLÀ¸ÌĞ……¥¹ÍĞÑ¡”Á¡½Ñ½É…Á Ì(€€€€€€À¸ØÇŠLÀ¸ØĞƒŠP½ÕÈÉ½İ¹Ì…Ğ€ÈÃŠLØÀ´…ÉÉäÑ¡”™¥¹”µÍ…±”Ñ•áÑÕÉ”½˜„Á¡½Ñ½É…Á Ì(€€€€€­¥±½µ•ÑÉ”µ‘¥ÍÑ…¹ĞÑÉ••±¥¹”¸M¡…‘½İÌ±¥ÀÑ¼±¥Ñ•É…°€ À°À°À¥€İ¡•É”Ñ¡”Á¡½Ñ½É…Á Ì(€€€€€‘…É­•ÍĞ‘•¥±”¥Ì0€ÄÓŠLÈÜ°…¹ÍÕ¹±¥ĞÉ½İ¸Ñ½ÁÌ…É”€¨©‰±Õ”¨¨€¡Š"IƒŠ"HÄäÑ¼ƒŠ"HÈØ¤İ¡•É”(€€€€€Ñ¡”Á¡½Ñ½É…Á Ì…É”İ…É´É••¸€ ¬ÄÌÑ¼€¬ÈĞ¤¸(€€€€´€¨©Q¡”Í¡½ĞÍ•Ğ¡…Ì½¹±ä½¹”½Á•¸µÁÉ…¥É¥”Ù¥•Ü¸¨¨ÁÉ…¥É¥•}Í½ÕÑ¡€ÍÑ…¹‘Ì€Ì¸ĞØ´™É½´„(€€€€€ÑÉÕ¹¬İ¥Ñ €ÈÌ¸Ğ€”½Á•¸Í­ä……¥¹ÍĞÁÉ…¥É¥•}İ•ÍÑ€Ì€äÔ¸Ğ€”¸Q¡…ĞÍ•½¹…¹±”•á¥ÍÑÌ(€€€€€ÁÉ•¥Í•±ä…ÌÑ¡”½¹ÑÉ½°Ñ¡…ĞÍ•Á…É…Ñ•Ì„ÑÕ¹•Ù¥•Ü™É½´„™¥á•½¹”°Í¼(€€€€€ÁÉ…¥É¥•}İ•ÍÑ€¡…Ì‰••¸ÑÕ¹•……¥¹ÍĞ¥ÑÍ•±˜İ¥Ñ ¹¼½¹ÑÉ½°¸(€€€€´€¨©É¥Ù•É}‰…¹­€™…¥±Ì¥ÑÌ½İ¸‰É¥•˜…¹Ñ¡”™…Õ±Ğ¥ÌÑ¡”É•¹‘•É•È°¹½ĞÑ¡”‘…Ñ„¸¨¨i½¹”€Ä(€€€€€ÍÁ•¥™¥•Ì½É‘É…ÍÌ…Ğ€Ä¸ËŠLÈ¸À´…¹€ĞÃŠLÔÔ€”½Ù•Èİ¥Ñ ‰…É•}Í½¥±}™É…Ñ¥½¸è€À¸Á€ìÑ¡”(€€€€€™É…µ”Í¡½İÌøÈÔ´ÍÁÉ¥Ì½¸Ù¥Í¥‰±”‰…É”Í½¥°¥¸¹•…ÈµÉ½İÌ¸((€€€Qİ¼Ñ¡¥¹Ì…µ”½ÕĞ½˜Ñ¡”Íİ••À±•…¸…¹Í¡½Õ±‰”Í…¥…ÌÁ±…¥¹±ä…ÌÑ¡”™…¥±ÕÉ•Ì¸Q¡”(€€€€¨©)Õ±äÁ¡•¹½±½ä¥Ì½ÉÉ•Ğ…ĞÍ½ÕÉ”¨¨ƒŠP•Ù•Éäİ…É´µÍ•…Í½¸É…ÍÌÙ••Ñ…Ñ¥Ù”İ¥Ñ „¹Õ±°(€€€¥¹™±½É•Í•¹”°…ÑÑ…¥°™ÉÕ¥Ñ¥¹œ…¹‰É½İ¸°É…µÀ±•…™±•ÍÌ°…¹„±¥Ù”Õ…ÉÑ¡…ĞÍÕÁÁÉ•ÍÍ•Ì(€€€…¹É•Á½ÉÑÌ…¹äÉ•½ÉÑ¡…Ğ½¹ÑÉ…‘¥ÑÌ¥ÑÍ•±˜¸¹Ñ¡”€¨©™±½É„‘…Ñ…Í•Ğ¥ÌÑ¡”½¹”Á…É•°(€€€„É¥Ñ¥ŒÁ…ÍÍ•İ¥Ñ¡½ÕĞÉ•Í•ÉÙ…Ñ¥½¸¨¨¸Q¡”É•¹‘•É•È¥Ìİ¡…Ğ¥Ì™…¥±¥¹œ¥Ğ¸((€€€Qİ¼µ•Ñ¡½‘½±½¥…°½ÉÉ•Ñ¥½¹Ìİ½ÉÑ ­••Á¥¹œ°‰½Ñ ½˜İ¡¥ ¥¹Ù…±¥‘…Ñ”¹Õµ‰•ÉÌÑ¡¥Ì(€€€ÁÉ½©•Ğ¡…ÌÅÕ½Ñ•è((€€€€´€¨©Q¡”ÁÉ¥µ…ÉäÉ•™•É•¹”İ…ÌÑ¡”İÉ½¹œÁ¡½Ñ½É…Á ¸¨¨‘ÕÁ…•}Ñ…±±É…ÍÍ|ÈÀÄà´ÀÜ´ÈĞ¹©Á€¥Ì(€€€€€Ñ¥Ñ±•€ˆ©I•ÍÑ½É•¨Ñ…±±É…ÍÌÁÉ…¥É¥”ˆ…¹‘•ÍÉ¥‰•…Ì„€‰AÉ…¥É¥”Á±…¹Ñ¥¹œˆ½¸„™½Éµ•È(€€€€€…É¥Õ±ÑÕÉ…°™¥•±ƒŠP„Í••µ¥à½¸Á±½İ•É½Õ¹°…¹É•ÍÑ½É…Ñ¥½¹Ì…É”‰½Õ¡Ğ™½È‰•¥¹œ(€€€€€™½ÉˆµÉ¥ ¸Q¡”¹•Ù•ÈµÁ±½İ•]½½‘İ½ÉÑ ÍÑ…¹¥ÌÑ¡”‰•ÑÑ•È…¹…±½Õ”™½ÈÕ¹µ…¹…•€ÄàÌÔ(€€€€€ÁÉ…¥É¥”¸ùù5•…ÍÕÉ•™±½İ•È±½…èÁ±…¹Ñ¥¹œ€ÄÈ¸äÄ€”°Ù¥É¥¸É•µ¹…¹Ğ€Ä¸ÜçŠLÔ¸ÔĞ€”¸Q¡”¡½¹•ÍĞ(€€€€€Ñ…É•Ğ¥Ì€¨¨ÓŠLØ€”°¹½Ğ€ÄÌ¸àä€”¨¨¹ùø€¨©Q!=IIQ%=8]LI%!P9%QL9U5	ILI(€€€€€]%Q!I]8°€ÈÀÈØ´Àà´ÄÔ‰äHµ\ÑŒ¡ˆÄ¤¸¨¨9•¥Ñ¡•È±…ÕÍ”ÍÕÉÙ¥Ù•Ì¡•­¥¹œ¸€¨©9¼¹•Ù•ÈµÁ±½İ•(€€€€€É•µ¹…¹ĞÁ¡½Ñ½É…Á ¥Ì½µµ¥ÑÑ•Ñ¼Ñ¡¥ÌÉ•Á½Í¥Ñ½Éä…¹¹¼Í½ÕÉ”É•½É‘•ÍÉ¥‰•Ì½¹”¨¨ƒŠP(€€€€€Ñ¡”Á¡É…Í”½ÕÉÌ½¹”¥¸‘…Ñ„½Í½ÕÉ•Ì½€°¥¹Í¥‘”Ñ¡”É•½É½˜Ñ¡”Á±…¹Ñ¥¹œ°¥Ñ¥¹œ(€€€€€¹½Ñ¡¥¹œƒŠPÍ¼Ñ¡”€Ä¸ÜçŠLÔ¸ÔĞ€”¡…±˜¥ÌÕ¹Í½ÕÉ•¸¹€ÄÈ¸äÄ€”‘½•Ì¹½ĞÉ•ÁÉ½‘Õ”èÑ¡”(€€€€€½µµ¥ÑÑ•É•¥Á”É•…‘Ì€¨¨Ô¸ÔĞ€”¨¨½¸Ñ¡…Ğ™É…µ”°€Ü¸ÀÈ€”½¸¥ÑÌ¹•…É•ÍĞÅÕ…ÉÑ•È…¹€ÈÔ¸àÈ€”(€€€€€İ¥Ñ ¥ÑÌÑİ¼Ñ•ÍÑÌÉ•½É‘•É•¸€¨©Q¡•É”¥ÌÑ¡•É•™½É”¹¼€ÓŠLØ€”Ñ…É•Ğ¨¨°…¹Ñ¡¥Ì™¥±”µÕÍĞ(€€€€€¹½Ğ‰”É•……ÌÍ•ÑÑ¥¹œ½¹”¸¹½‘”Ñ½½±Ì½µ•…ÍÕÉ•}‰±½½µ}Ñ…É•Ğ¹µ©Í€ÁÉ¥¹ÑÌ…±°½˜¥Ğì(€€€€€I=5@ƒ
œHµ\ÑŒ¡ˆÄ¤…ÉÉ¥•ÌÑ¡”É•…Í½¹¥¹œ…¹Ñ¡”Ñ¡É•”É½ÕÑ•Ì½ÕĞ¸(€€€€´€¨©Qİ¼É½Õ¹‘Ìİ•É”©Õ‘•…ĞÑ¡”İÉ½¹œ±½½¬µ…¹±”¸¨¨Q¡”Í¡½Ğ¡…É¹•ÍÌÍ•Ğ¹¼Á¥Ñ İ¡¥±”(€€€€€Ñ¡”É•™•É•¹”Á¡½Ñ½É…Á¡•È¡…Ñ¥±Ñ•‘½İ¸øÄË
À°Í¼•Ù•Éä€‰¹•…É•ÍĞÅÕ…ÉÑ•Èˆ¹Õµ‰•È(€€€€€½µÁ…É•Ñ¡”Á¡½Ñ½É…Á …Ğ€È´……¥¹ÍĞ½ÕÈÉ•¹‘•È…Ğ€Ğ´ƒŠP…¹¹•…Èµ™¥•±Ù••Ñ…Ñ¥½¸İ…Ì(€€€€€•á…Ñ±äİ¡…ĞÑ¡½Í”É½Õ¹‘Ìİ•É”ÑÕ¹¥¹œ¸Q¡”¡…É¹•ÍÌ¥Ì¹½ÜÁ¥Ñ µµ…Ñ¡•…¹ÁÉ¥¹ÑÌ¥ÑÌ(€€€€€Á¥Ñ ¸½ÉÉ•Ñ¥¹œ¥Ğµ…­•ÌÑ¡”…À€©İ½ÉÍ”¨è€À¸ÀÜ€”……¥¹ÍĞ„Ù¥É¥¸É•µ¹…¹ĞÌ€È¸äÜ€”¸(€€€€´¡Õ”½Í…ÑÕÉ…Ñ¥½¸Ñ•ÍĞ…¹¹½ĞÍ•Á…É…Ñ”)Õ±ä™É½´=Ñ½‰•È¡•É”ƒŠPÑ¡”=Ñ½‰•È¹•…Ñ¥Ù”(€€€€€½¹ÑÉ½°±…¹‘Ì€©‰•Ñİ••¸¨Ñ¡”Ñİ¼)Õ±äÁ¡½Ñ½É…Á¡Ì¸Q¡…Ğµ•ÑÉ¥ŒÍ¡½Õ±¹½Ğ‰”ÅÕ½Ñ•‰ä(€€€€€…¹å½¹”°¥¹±Õ‘¥¹œÑ¡¥Ì™¥±”¸((À¸€¨©Q¡”™½Éµ•ÈÍ±½ÜµÉ•¹‘•É•Èİ…±­¥¹œ™…¥±ÕÉ”¥ÌÉ•Í½±Ù•İ¥Ñ¡½ÕĞİ•…­•¹¥¹œ¥ÑÌ‘¥ÍÑ…¹”‰…È¸¨¨(€€5½Ù•µ•¹Ğ¹½Ü½¹ÍÕµ•ÌÕÀÑ¼„ÅÕ…ÉÑ•ÈµÍ•½¹½˜É•…°™É…µ”Ñ¥µ”¥¸Ñ•ÉÉ…¥¸µ…¹µ½±±¥Í¥½¸(€€ÍÕ‰ÍÑ•ÁÌ¹¼±…É•ÈÑ¡…¸€À¸ÀÔÌ¸Í½™Ñİ…É”É•¹‘•É•È‘É…İ¥¹œ½¹±äÑİ¼™É…µ•ÌÁ•ÈÍ•½¹¹¼(€€±½¹•ÈÑÕÉ¹Ì„€Ä¸ĞÔ´½Ìİ…±¬¥¹Ñ¼„É…İ°°İ¡¥±”Ñ¡”Í¡½ÉĞÍÕ‰ÍÑ•ÁÌÉ•Ñ…¥¸‰…¹¬…¹‰Õ¥±‘¥¹œ(€€½±±¥Í¥½¸…ÕÉ…ä¸Q¡”™½É•É½Õ¹Íµ½­”ÉÕ¸Á…ÍÍ•ÌÑ¡”Í…µ”İ…±¬µ‘¥ÍÑ…¹”…ÍÍ•ÉÑ¥½¸…Ğ(€€‰½Ñ €ÌäÃ\ÜàÀ…¹€ÄÈàÃ\àÀÀ¸ÕÉÉ•¹Ğ™Õ±°µÍ•¹”‰Õ‘•ÑÌ…É”€Ğä€¼€ÔÌ‘É…Ü…±±Ì…¹€ÌÜà°ØĞÜ€¼(€€€Ğää°ÌĞÌÑÉ¥…¹±•ÌÉ•ÍÁ•Ñ¥Ù•±äìÑ¡”‘•Í­Ñ½ÀÉ•¹‘•É•ÈÉ•µ…¥¹ÌÍ±½Ü…Ğ€È™ÁÌÕ¹‘•ÈMİ¥™ÑM¡…‘•È°(€€‰ÕĞ•±…ÁÍ•µÑ¥µ”İ…±­¥¹œ¥Ì¹¼±½¹•È½ÕÁ±•Ñ¼Ñ¡…Ğ™É…µ”½Õ¹Ğ¸((Ä¸€¨©=¹”ÍÑÉÕÑÕÉ”É•½É‘½•Ì¹½ĞÁÉ½Ù”Ñ¡”Í¡•µ„¸¨¨Q¡”M…Õ…¹…Í •á•É¥Í•ÌÁ¡…Í•Ì°„(€€‰Õ¥±‘¥¹œµ½Ù”°…¹Ñ¡”™Õ±°½¹™¥‘•¹”É…¹”°‰ÕĞÑ¡”µ½‘•°¡…Ì¹½Ğµ•Ğ„™½ÉĞ°„‰É¥‘”°½È(€€„É½Ü½˜ÍÑ½É•™É½¹ÑÌå•Ğ¸áÁ•ĞÍ¡•µ„ÁÉ•ÍÍÕÉ”…Ğ5¥±•ÍÑ½¹”€Ä¸(È¸€¨©½¹ÍÑÉÕÑ¥½¸è‰…±±½½¹}™É…µ•€½¸Ñ¡”M…Õ…¹…Í ¥ÌÁÉ½‰…‰±äİÉ½¹œ¨¨…¹¥Ì™±…•…ÌÍÕ (€€¥¸Ñ¡”É•½É¸	…±±½½¸™É…µ¥¹œÁ½ÍÑ‘…Ñ•ÌÑ¡”€ÄàÌÄ‰Õ¥±‘¥¹œ‰ä„å•…È¸1•™ĞÙ¥Í¥‰±”É…Ñ¡•È(€€Ñ¡…¸Í¥±•¹Ñ±äÍİ…ÁÁ•°‰•…ÕÍ”ÍÕ‰ÍÑ¥ÑÕÑ¥¹œ½¹”Õ•ÍÌ™½È…¹½Ñ¡•È¥Ì¹½Ğ„™¥à¸(Ì¸€¨©Q¡”M…Õ…¹…Í …±±•ÉäÉ•…‘¥¹œİ…ÌÉ•Ù¥Í•½¸‘…ä½¹”¨¨°™É½´€‰…±±•Éä°½¹©•ÑÕÉ…°ˆÑ¼(€€€‰¹¼…±±•Éä°¥¹™•ÉÉ•ˆ°…™Ñ•È½Á•¹¥¹œÑ¡”Ñİ¼É•ÑÉ½ÍÁ•Ñ¥Ù”¥µ…•ÌÑ¡”É•Á¼…±É•…‘ä¡•±¸(€€	½Ñ Í¡½Ü¹¼Ù•É…¹‘„…¹‰½Ñ Í¡½ÜÑ¡”€ÄàÈä±½œ…‰¥¸ÍÕÉÙ¥Ù¥¹œ…Ì…¸…ÑÑ…¡•İ¥¹œ¸Q¡”(€€¥µ…•Ì…É”¹½Ğ¥¹‘•Á•¹‘•¹Ğ½˜•… ½Ñ¡•È°Í¼Ñ¡¥Ì¥Ì¥¹™•É•¹”°¹½Ğ‘½Õµ•¹Ñ…Ñ¥½¸ƒŠP…¹Ñ¡”(€€™É…µ•}Ñ…Ù•É¹€…É¡•ÑåÁ”¹½Ü¡…ÌÑ¼ÍÕÁÁ½ÉĞ…¸…ÑÑ…¡•±½œİ¥¹œ¸(Ğ¸€¨©Qİ¼Í½ÕÉ•Ì¡…Ù”¹¼İ•ˆ…É¡¥Ù”¸¨¨‘É±½¥¡}¡½Ñ•±Í€¡…Ì¹¼]…å‰…¬Í¹…ÁÍ¡½Ğ…¹Ñ¡”(€€Ù…±¥‘…Ñ½Èİ…É¹Ì…‰½ÕĞ¥Ğ½¸•Ù•ÉäÉÕ¸ìÑ¡”İ…É¹¥¹œ¥Ì½ÉÉ•Ğ…¹ÍÑ…¹‘ÌÕ¹Ñ¥°Í½µ•½¹”(€€…É¡¥Ù•ÌÑ¡”Á…”¸]…Ôµ	Õ¸Ì…É¡¥Ù•‘}ÕÉ°Á½¥¹ÑÌ…Ğ„Í…¹¹••‘¥Ñ¥½¸½˜Ñ¡”‰½½¬É…Ñ¡•È(€€Ñ¡…¸Ñ¡”ÑÉ…¹ÍÉ¥ÁÑ¥½¸…ÑÕ…±±äÉ•…‘ÕÉ¥¹œÉ•Í•…É ƒŠP¹½Ñ•¥¸Ñ¡”Í½ÕÉ”É•½É¸(Ô¸€¨©M•Ù•É…°É•Í•…É ±…¥µÌ…É”Í¹¥ÁÁ•Ğµ‘•É¥Ù•¸¨¨•¹å±½Á•‘¥„¹¡¥…½¡¥ÍÑ½Éä¹½É€É•ÑÕÉ¹•(€€€ÔÀÌÑ¡É½Õ¡½ÕĞÑ¡”É•Í•…É Í•ÍÍ¥½¸°…¹„™•Ü¥Ñ…Ñ¥½¹Ì¥¸Ñ¡”‘½ÍÍ¥•ÉÌÉ•ÍĞ½¸Í•…É µ¥¹‘•à(€€Í¹¥ÁÁ•ÑÌÉ…Ñ¡•ÈÑ¡…¸É•ÑÉ¥•Ù•Á…•Ì¸Q¡•äµÕÍĞ‰”É”µ™•Ñ¡•‰•™½É”…¹ä½˜Ñ¡•´¥ÌÁÉ½µ½Ñ•(€€Ñ¼‘½Õµ•¹Ñ•‘€¸(Ø¸€¨©Q¡”½¹±•ä½MÑ•±é•ÈÉ¥¡ÑÌÅÕ•ÍÑ¥½¸¥Ì½Á•¸¸¨¨5…É­•¡•­}É•ÅÕ¥É•‘€ì¹¼…ÍÍ•Ğµ…ä‰”(€€‘•É¥Ù•™É½´¥ĞÕ¹Ñ¥°„MÑ…¹™½É½ÁåÉ¥¡ĞI•¹•İ…°…Ñ…‰…Í”¡•¬¥ÌÉ•½É‘•¸(Ü¸€¨©Q¡”€ÄàÌÔ±…­”ÍÑ…”¥Ì„Õ•ÍÌ¸¨¨€ÔàÀƒ
Ä€Ä¸Ô™ĞM0°Ñ…•½¹©•ÑÕÉ…°°…¹Ñ¡”•¹Ñ¥É”(€€Ù•ÉÑ¥…°‘…ÑÕ´¡…¹Ì½™˜¥Ğ¸(à¸€¨©%aƒŠPÑ¡”İ¡¥Ñ”Á…¥¹Ğ¹½ÜÉ•…‘Ì…Ìİ¡¥Ñ”¸¨¨Q¡”•…É±¥•È‘¥…¹½Í¥Ì¥¸Ñ¡¥Ì™¥±”€¡„İ•…¬(€€Í­ä½¹ÑÉ¥‰ÕÑ¥½¸…Ğ„É…é¥¹œÍÕ¸…¹±”¤İ…ÌİÉ½¹œ°…¹İÉ½¹œ¥¸„İ…äİ½ÉÑ É•½É‘¥¹œèÑ¡”(€€Ñ…¸İ…±°İ…Ì„MQ1AU	1%M!MMP°…¸½±‘•È‰…­”Ñ¡…ĞÍÑ¥±°…ÉÉ¥•Ñ¡”½Ù•Èµ‘…É¬<(€€Ñ•áÑÕÉ”¸Qİ¼Í•Á…É…Ñ”…ÕÍ•ÌÑ¡•¸ÑÕÉ¹•ÕÀ‰•¡¥¹¥Ğ¸ÁÕ‰±¥Í ¹Í¡€Í¡¥ÁÁ•™É½´(€€…ÍÍ•ÑÌ½İ•ˆ½€°İ¡¥ ½¹±ä‰…­”¹Í¡€É•™É•Í¡•Ì°Í¼ÉÕ¹¹¥¹œÑ¡”•¹•É…Ñ½È‘¥É•Ñ±äÉ•ÁÕ‰±¥Í¡•(€€Ñ¡”ÁÉ•Ù¥½ÕÌµ•Í Í¥±•¹Ñ±äƒŠP¹½ÜÕ…É‘•°…¹¥ĞÍ…åÌÍ¼İ¡•¸¥Ğ½Á¥•Ì„µ…ÍÑ•ÈÑ¡É½Õ ¸(€€¹Ñ¡”Í­äµ‘•É¥Ù•A5I4•¹Ù¥É½¹µ•¹Ğİ…Ì½Ù•ÉÉ¥‘¥¹œ…±‰•‘¼½ÕÑÉ¥¡Ğèµ•…ÍÕÉ•°„‰É½İ¸±½œ(€€İ…±°É•¹‘•É•…Ğ…¸H½É…Ñ¥¼½˜€Ä¸Àà……¥¹ÍĞÑ¡”€Ä¸ÜÔ¥ÑÌ½İ¸‰…Í”½±½ÕÈÍÁ•¥™¥•Ì°İ¥Ñ (€€•Ù•ÉäÍÕÉ™…”½¹Ù•É¥¹œ½¸Ñ¡”Í­ä½±½ÕÈİ¡…Ñ•Ù•È¥Ğİ…Ìµ…‘”½˜¸½È„ÁÉ½©•Ğİ¡½Í”(€€±…¥´¥ÌÑ¡…Ğ„‘½Õµ•¹Ñ•İ¡¥Ñ”İ…±°É•…‘Ì…Ìİ¡¥Ñ”°Ñ¡…Ğ¥Ì„‘…Ñ„µ¥¹Ñ•É¥Ñä‰Õœİ•…É¥¹œ(€€…¸…•ÍÑ¡•Ñ¥Ì½ÍÑÕµ”¸Q¡”•¹Ù¥É½¹µ•¹Ğ¥Ì½¹”ì„¡•µ¥ÍÁ¡•É”™¥±°İ¥Ñ „İ…É´É½Õ¹‰½Õ¹”(€€Á±ÕÌÑ¡”ÍÕ¸¹½Ü…ÉÉäÑ¡”±¥¡Ñ¥¹œ°…¹¡Õ”¥ÌÁÉ•Í•ÉÙ•€¡±½œH½€Ä¸ÌÀ¤¸I•Ù¥Í¥Ğİ¥Ñ „(€€ÁÉ½Á•É±ä•áÁ½Í•!I$É…Ñ¡•ÈÑ¡…¸„A5I4½˜…¸…¹…±åÑ¥ŒÍ­ä¸(ä¸€¨©<¥Ì‰…­•‰ÕĞÍİ¥Ñ¡•½™˜°‘•±¥‰•É…Ñ•±ä¸¨¨Q¡”‰…­”Á…Ñ İ½É­Ì•¹Ñ¼•¹…¹¥Ìİ¥É•(€€…Ì„É•…°±Q½±ÕÍ¥½¸Ñ•áÑÕÉ”°‰ÕĞÑ¡”…É¡•ÑåÁ”Ì±…Á‰½…É½ÕÉÍ•Ì…¹İ¥¹‘½ÜÉ•Ù•…±Ì(€€Í¥Ğ„•¹Ñ¥µ•ÑÉ”½™˜Ñ¡”İ…±°…¹½±Õ‘”•… ½Ñ¡•Èè„µ•…ÍÕÉ•‰…­”½µ•Ì½ÕĞ…Ğµ•…¸€À¸ÈØÔ(€€İ¥Ñ €Øä”½˜Ñ•á•±Ì‰•±½Ü¡…±˜°…¹Ñ¡”‰Õ¥±‘¥¹œÉ•¹‘•ÉÌ‰É½İ¸¸M¡½ÉÑ•¹¥¹œÑ¡”<‘¥ÍÑ…¹”(€€½¹±äÉ•…¡•Ì€À¸Ìà¸%Ğ¹••‘Ì„±½ÜµÁ½±ä<…”°¹½Ğ„ÑÕ¹¥¹œÑİ•…¬¸€¨©m	½Ñ ™¥ÕÉ•ÌY=%ƒŠP(€€P´ÀÄÔà°€ÈÀÈØ´Àà´ÈÜì…¹Ñ¡”•áÁ½ÉĞİ…ÌÍ¡¥ÁÁ¥¹œ„‰±…¬Ñ•áÑÕÉ”İ¡•¸Ñ¡¥Ìİ…ÌİÉ¥ÑÑ•¸°Í¼(€€€‰É•¹‘•ÉÌ‰É½İ¸ˆİ…Ì¹½Ğ„É•…‘¥¹œ½˜<¸Q¡”½¹±ÕÍ¥½¸ÍÕÉÙ¥Ù•Ì½¸„É•¹‘•É•™É…µ”è(€€P´ÀÈÈÜ°€ÈÀÈØ´Àà´Èà°…ĞÑ¡”Ñ½À½˜Ñ¡¥Ì™¥±”¹t¨¨€´µ…½€­••ÁÌÑ¡”Á…Ñ (€€•á•É¥Í•…¹…ÍÍ•ÑÌ½µ…¹¥™•ÍĞ¹©Í½¹€É•½É‘Ì¡½¹•ÍÑ±äÑ¡…ĞÑ¡”Í¡¥ÁÁ•…ÍÍ•Ğ¡…Ì¹½¹”¸(ÄÀ¸€¨©±Ñ˜µÑÉ…¹Í™½Éµ€‘¥¹½ĞÉÕ¸¨¨°Í¼…ÍÍ•ÑÌ½İ•ˆ½€ÕÉÉ•¹Ñ±ä¡½±‘Ì½Á¥•Ì½˜Ñ¡”(€€€Õ¹½µÁÉ•ÍÍ•µ…ÍÑ•ÉÌÉ…Ñ¡•ÈÑ¡…¸µ•Í¡½ÁĞ½-Q`È‘•É¥Ù…Ñ¥Ù•Ì¸!…Éµ±•ÍÌ…Ğ€ĞĞ-ì¥ĞµÕÍĞİ½É¬(€€€‰•™½É”Ñ¡”Ñ½İ¸Í…±•Ì¸(ÄÄ¸€¨©%aƒŠPÑ¡”±¥‰•ÉÑ¥•Ì…É”¹½Ü…ÑÑ…¡•Ñ¼Ñ¡•¥È‰Õ¥±‘¥¹Ì¸¨¨Q¡”ÁÉ½Ù•¹…¹”Á½ÁÕÀÉ•…‘Ì(€€€ÍÕ‰©•ÑÍ€…¹Í¡½İÌÑ¡”±¥‰•ÉÑ¥•ÌÑ…­•¸İ¥Ñ Ñ¡”‰Õ¥±‘¥¹œ‰•¥¹œ¥¹ÍÁ•Ñ•èÑ¡”M…Õ…¹…Í Ì(€€€™½ÕÈ°0ä½¸Ñ¡”É••¸QÉ•”°0Ü½0à½¸Ñ¡”Ñ¡É•”]½±˜A½¥¹ĞÁ±…•µ•¹ÑÌ¸	½Ñ Ù¥•İÌÉ•¹‘•È™É½´(€€€½¹”‘•É¥Ù•É•½ÉÑ¡É½Õ ½¹”•¹ÑÉäÉ•¹‘•É•È°Í¼Ñ¡”Á…¹•°…¹Ñ¡”…É…¹¹½Ğ‘•ÍÉ¥‰”Ñ¡”(€€€Í…µ”±¥‰•ÉÑä‘¥™™•É•¹Ñ±ä°…¹Ñ¡”Íµ½­”…ÍÍ•ÉÑÌÑ¡”‘¥ÍÉ¥µ¥¹…Ñ¥¹œ…Í”ƒŠP„Í•½¹‰Õ¥±‘¥¹œ(€€€•ÑÌ¥ÑÌ½İ¸Í•Ğ°¹½ĞÑ¡”İ¡½±”±¥ÍĞ°…¹„Í•¹”µİ¥‘”±¥‰•ÉÑä¥Ì¹½ĞÁ¥¹¹•Ñ¼…¹ä‰Õ¥±‘¥¹œ¸(€€€€¨©½µÁ±•Ñ•¹•ÍÌ¥Ì¹½Ü•¹™½É•™½È½¹”±…ÍÌ½˜¥¹Ù•¹Ñ¥½¸°…¹½¹±ä½¹”¸¨¨Ù…±¥‘…Ñ”¹Áå€(€€€ÉÕ¹ÌÑ¡”¥¹Ù•ÉÍ”¡•¬è•Ù•ÉäÁ¡…Í”İ¡½Í”™½½ÑÁÉ¥¹Ñ€½ÈÁ½Í¥Ñ¥½¹€¥Ì½¹©•ÑÕÉ…±€µÕÍĞ‰”(€€€±…¥µ•‰ä„±¥‰•ÉÑäÌ½Ù•ÉÌé€™¥•±ƒŠPÍÑÉÕÑÕÉ•}¥‘l¹Á¡…Í•}¥‘t¹…ÍÁ•Ñ€°‘•±…É•‰äÑ¡”(€€€‘½Õµ•¹ĞÉ…Ñ¡•ÈÑ¡…¸¥¹™•ÉÉ•™É½´¥ÑÌİ½É‘¥¹œ¸M¥àÍÕ ¥¹Ù•¹Ñ¥½¹Ì•á¥ÍĞ¥¸Ñ¡”½µµ¥ÑÑ•(€€€‘…Ñ„€¡™¥Ù”™½½ÑÁÉ¥¹ÑÌ°Á±ÕÌ]…±­•ÈÌÁ½Í¥Ñ¥½¸¤ìÍ¥à‘•±…É…Ñ¥½¹Ì½Ù•ÈÑ¡•´¸Q¡”Í•±˜µÑ•ÍĞ(€€€…ÍÍ•ÉÑÌÑ¡”‘¥ÍÉ¥µ¥¹…Ñ¥¹œ…Í”°…¹Ñ¡…Ğ…Í”½ĞÍÑÉ¥Ñ•Èè…¸•¹ÑÉäİ¡½Í”ÁÉ½Í”¥Ì€©…‰½ÕĞ¨(€€€™½½ÑÁÉ¥¹ÑÌ…¹Á±…•µ•¹Ğ°…¹İ¡¥ ¹…µ•ÌÑ¡”‰Õ¥±‘¥¹œ°¹¼±½¹•È½Ù•ÉÌ…¹åÑ¡¥¹œ…Ğ…±°¸(€€€Q¡”±…¥µÌ…É”¡•­•Ñ¡”½Ñ¡•Èİ…äÑ½¼ƒŠP„Ñ½­•¸¹…µ¥¹œ¹¼ÍÕ ÍÑÉÕÑÕÉ”°¹¼ÍÕ Á¡…Í”°(€€€½È…¸…ÑÑÉ¥‰ÕÑ”Ñ¡…Ğ¥Ì¹½Ğ½¹©•ÑÕÉ…°™…¥±ÌÑ¡”…Ñ”°Í¼…¸½Ù•Èµ±…¥´¥Ì…Ì±½Õ…Ì„…À¸(€€€¹ÑÉ¥•ÌÕ¹‘•È€¨©I•Í½±Ù•¨¨…É”•á•µÁĞ™É½´Ñ¡…Ğ±…ÍĞÉÕ±”°İ¡¥ ¥Ìİ¡…Ğ±•ÑÌ…¸…ÁÁ•¹µ½¹±ä(€€€‘½Õµ•¹ĞÍÕÉÙ¥Ù”¥ÑÌ½İ¸‘…Ñ„‰•¥¹œ½ÉÉ•Ñ•¸€¨©Q¡”ÉÕ±”¹½Ü½Ù•ÉÌÍÑ…Ñ•™½É´…Ìİ•±°…Ì(€€€‘É…İ¸•½µ•ÑÉä¨¨€ ÈÀÈØ´Àà´ÄÀ¤èÑ¡”…ÍÁ•ĞÙ½…‰Õ±…Éä¥Ì•Ù•Éä…ÑÑ•ÍÑ•Ù…±Õ”¥¸„É•½ÉƒŠP(€€€™½½ÑÁÉ¥¹Ñ€°Á½Í¥Ñ¥½¹€°‘½Õµ•¹Ñ•‘}É…¹•€°Ñ¡”ÍÑÉÕÑÕÉ”µ±•Ù•°™Õ¹Ñ¥½¹€½½ÕÁ…¹ÑÍ€°…¹(€€€™½É´¸ñ…ÑÑÈù€•¹Õµ•É…Ñ•™É½´Ñ¡”‘…Ñ„É…Ñ¡•ÈÑ¡…¸™É½´„±¥ÍĞ°Í¼„¹•Ü…É¡•ÑåÁ”…ÑÑÉ¥‰ÕÑ”(€€€¥Ì¥¹Í¥‘”Ñ¡”ÉÕ±”Ñ¡”‘…ä¥Ğ…ÁÁ•…ÉÌ¸]¥‘•¹¥¹œ¥Ğ™½Õ¹™½ÕÈ¥¹Ù•¹Ñ¥½¹Ìİ¥Ñ ¹¼…‘µ¥ÍÍ¥½¸ƒŠP(€€€Ñ¡”M…Õ…¹…Í €ÄàÈä…‰¥¸Ìİ…±°¡•¥¡Ğ…¹É½½˜ÑåÁ”°‰½Ñ A1!=1H¥¸Ñ¡•¥È½İ¸¹½Ñ•Ì°(€€€…¹…±±•Éäè™…±Í•€½¸Ñ¡”É••¸QÉ•”…¹Ñ¡”]•ÍÑ•É¸°İ¡•É”™…±Í”¥ÌÑ¡”…É¡•ÑåÁ”Ì(€€€‘•™…Õ±ĞÉ…Ñ¡•ÈÑ¡…¸„™¥¹‘¥¹œ¸Q•¸½¹©•ÑÕÉ…°Ù…±Õ•Ì°Ñ•¸‘•±…É…Ñ¥½¹Ì¸€¨©]¡…Ğ¥ÌÍÑ¥±°(€€€Õ¹•¹™½É•¥Ì½µ¥ÍÍ¥½¹Ì…¹Í¥µÁ±¥™¥…Ñ¥½¹Ì¨¨°…¹Ñ¡…Ğ¥ÌÑ¡”¡…É¡…±˜è…¸¥¹Ù•¹Ñ¥½¸¡…Ì„(€€€É•½ÉÑ¼Á½¥¹Ğ…Ğ…¹…¸½µ¥ÍÍ¥½¸‘½•Ì¹½Ğ°Í¼Ñ¡”]•ÍÑ•É¸ÌÕ¹µ½‘•±±•ÍÑ…‰±”å…É€¡0ÄÀ¤(€€€…¹Ñ¡”É••¸QÉ•”ÌÍ¥‘”…‘‘¥Ñ¥½¹Ì€¡0ä¤…É”½Ù•É•‰äÁÉ½Í”…±½¹”¸9¼µ•¡…¹¥Í´…¸…Ñ „(€€€±¥‰•ÉÑäÑ…­•¸Ñ¡…Ğ¹½‰½‘ä¹½Ñ¥•Ñ…­¥¹œ¸M¥à½˜Í¥àÍÑÉÕÑÕÉ•Ì…ÉÉä…Ğ±•…ÍĞ½¹”±¥‰•ÉÑä°(€€€Í¼Ñ¡”Á½ÁÕÀÌ•µÁÑäÍÑ…Ñ”É•µ…¥¹ÌÕ¹•á•É¥Í•‰äÉ•…°‘…Ñ„¸(ÄÈ¸€¨©Q¡”½µ¥ÍÍ¥½¸¡…±˜¥Ì•¹™½É•¹½ÜÑ½¼°…¹Íİ¥Ñ¡¥¹œ¥Ğ½¸™½Õ¹„‘½Õµ•¹Ñ•™•…ÑÕÉ”(€€€Ñ¡…Ğİ…Ì¹•Ù•È‰Õ¥±Ğ¸¨¨Q¡”¥¹Ù•¹Ñ¥½¸ÉÕ±”É•…‘Ì„½¹©•ÑÕÉ…±€Ñ…œ…¹‘•µ…¹‘Ì…¸(€€€…‘µ¥ÍÍ¥½¸¸¸½µ¥ÍÍ¥½¸±•…Ù•Ì¹¼Ñ…œè•Ù¥‘•¹”İ¥Ñ ¹¼•½µ•ÑÉä¥¸™É½¹Ğ½˜¥Ğ±½½­Ì•á…Ñ±ä(€€€±¥­”•Ù¥‘•¹”İ¥Ñ •½µ•ÑÉä¥¸™É½¹Ğ½˜¥Ğ°İ¡¥ ¥Ìİ¡äÁÉ½Í”İ…ÌÑ¡”½¹±äÑ¡¥¹œ¡½±‘¥¹œ¥Ğ(€€€Õ¹Ñ¥°¹½Ü¸Q¡”±…¥´Ñ¡•É•™½É”½µ•Ì™É½´Ñ¡”•¹•É…Ñ½ÈƒŠP•… €©}Á…É…µÌ¹Áå€‘•±…É•ÌÑ¡”(€€€™½É´…ÑÑÉ¥‰ÕÑ•Ì¥ÑÌ™É½µ}Á¡…Í•€…ÑÕ…±±äÉ•…‘Ì€¡=9MU5€¤°…¹•Ù•Éä…ÑÑÉ¥‰ÕÑ”½ÕÑÍ¥‘”(€€€Ñ¡…ĞÍ•ĞµÕÍĞÍ…ä½¸Ñ¡”É•½Éİ¡…ĞÑ¡”µ•Í ‘½•Ì¥¹ÍÑ•…è…‰Í•¹Ñ€°Í¥µÁ±¥™¥•‘€°½È(€€€É•½É‘}½¹±å€™½ÈÍ½µ•Ñ¡¥¹œÑ¡…Ğİ…Ì¹•Ù•È„‰Õ¥±¥¹ÍÑÉÕÑ¥½¸¸Q¡”™¥ÉÍĞÑİ¼½İ”(€€€‘½Ì½1%	IQ%L¹µ‘€„½Ù•ÉÌé€Ñ½­•¸•á…Ñ±ä…Ì…¸¥¹Ù•¹Ñ¥½¸‘½•Ì°…¹Ñ¡”Á½ÁÕÀµ…É­Ì(€€€Ñ¡½Í”É½İÌÍ¼„Ù¥Í¥Ñ½ÈÍ••Ì¥Ğ…¹¹½Ğ½¹±äÑ¡”É•Á½Í¥Ñ½Éä¸€¨©Qİ•¹Ñäµ½¹”…ÑÑÉ¥‰ÕÑ•Ì…É½ÍÌ(€€€Í¥à‰Õ¥±‘¥¹ÌÑÕÉ¹•½ÕĞÑ¼É•… ¹¼Ù•ÉÑ•à¸¨¨5½ÍĞ…É”‰•¹¥¸µ‰ÕĞµÉ•…°Í¥µÁ±¥™¥…Ñ¥½¹ÌƒŠP„(€€€¡¥µ¹•ä½Õ¹Ğ¹¼…É¡•ÑåÁ”É•…‘Ì°½¹”İ¥¹‘½ÜÉ¡åÑ¡´½¸…±°Ñ¡É•”™É…µ”Ñ…Ù•É¹Ì°İ…±°ÍÕÉ™…•Ì(€€€™¥á•‰äÑ¡”…É¡•ÑåÁ”É…Ñ¡•ÈÑ¡…¸Ñ¡”É•½É¸=¹”¥Ì¹½Ğ¸€¨©Q¡”]½±˜A½¥¹ĞQ…Ù•É¸Ì™É…µ”(€€€•áÑ•¹Í¥½¸…¹¥ÑÌÁ…¥¹Ñ•İ½±˜Í¥¸…É”‰½Ñ ‘½Õµ•¹Ñ•‘€…¹‰½Ñ …‰Í•¹Ğ™É½´Ñ¡”µ½‘•°¨¨è(€€€Ñ¡”É•½ÉÍÁ•±±ÌÑ¡•´™É…µ•}•áÑ•¹Í¥½¹€…¹Í¥¹…•€°Ñ¡”±½}‘İ•±±¥¹€…É¡•ÑåÁ”É•…‘Ì(€€€™É…µ•}…‘‘¥Ñ¥½¹€…¹Í¥¹€°…¹™É½µ}Á¡…Í•€™¥±±Ì…¸…‰Í•¹Ğ…ÑÑÉ¥‰ÕÑ”İ¥Ñ „‘•™…Õ±Ğ°Í¼(€€€Ñ¡”Ñİ¼‰•ÍĞµ…ÑÑ•ÍÑ•™•…ÑÕÉ•Ì½˜Ñ¡”¡½ÕÍ”İ•É”‘É½ÁÁ•¥¸Í¥±•¹”…¹Ñ¡”Á½ÁÕÀÍ¡½İ•Ñ¡”(€€€ÁÉ½©•ĞÌÍÑÉ½¹•ÍĞ½¹™¥‘•¹”¡¥À½Ù•È‰½Ñ ¸Q¡…Ğ¥ÌÑ¡”½¹™¥‘•¹”µ½‘•°İ½É­¥¹œ…Ì(€€€‘•Í¥¹•…¹ÍÑ¥±°µ¥Í±•…‘¥¹œ°İ¡¥ µ…­•Ì¥ĞÑ¡”Í¡…ÉÁ•ÍĞ…ÉÕµ•¹Ğ™½ÈÑ¡¥ÌÉÕ±”Ñ¡…ĞÑ¡”(€€€ÁÉ½©•Ğ¡…ÌÁÉ½‘Õ•¸€¨©I•Á…¥É•€ÈÀÈØ´Àà´ÄÀ°¥¸½¹”Í±¥”İ¥Ñ ¥ÑÌ‰…­”¨¨€¡Í•”€Äà‰•±½Ü¤¸(€€€5¥±±•ÈÌ¡½ÕÍ”İ…ÌÑ¡”Í…µ”Í¡…Á”¥¸µ¥¹¥…ÑÕÉ”ƒŠP¥ÑÌÉ•½ÉÍ…åÌÑİ¼¡¥µ¹•åÌ…¹(€€€±½}‘İ•±±¥¹€‰Õ¥±Ğ½¹”ƒŠP…¹¥Ì€¨©É•Á…¥É•€ÈÀÈØ´Àà´ÄÀ°¥¸½¹”Í±¥”İ¥Ñ ¥ÑÌ‰…­”¨¨(€€€€¡Í•”€Ää‰•±½Ü¤¸]¡…Ğ¥ÌÍÑ¥±°Õ¹•¹™½É•¥Ìİ¡…Ğ¹¼É•½Éµ•¹Ñ¥½¹Ì…Ğ…±°ƒŠP(€€€Ñ¡”]•ÍÑ•É¸ÌÕ¹µ½‘•±±•ÍÑ…‰±”å…É¥Ì¹½Ü±…¥µ•°‰ÕĞ„±¥‰•ÉÑä¹½‰½‘ä¹½Ñ¥•Ñ…­¥¹œ(€€€É•µ…¥¹ÌÕ¹…Ñ¡…‰±”‰ä…¹äµ•¡…¹¥Í´¸(ÄÌ¸€¨©Q¡”‘½Õµ•¹Ğ…¹Ñ¡”‘…Ñ„¡…‘É¥™Ñ•°…¹İÉ¥Ñ¥¹œÑ¡”±…¥´‘½İ¸™½Õ¹¥Ğ¸¨¨0ÄÈÍÑ¥±°(€€€É•…€‰Á½Í¥Ñ¥½¸Ñ…•¥¹™•ÉÉ•‘€ˆ™½ÈÑ¡”]…±­•Èµ••Ñ¥¹œ¡½ÕÍ”ìÑ¡”É•½Éİ…Ì‘½İ¹É…‘•Ñ¼(€€€½¹©•ÑÕÉ…±€½¸€ÈÀÈØ´Àà´Àä…¹¹½Ñ¡¥¹œ…ÉÉ¥•Ñ¡”¡…¹”‰…¬¸Q¡”­•åİ½ÉÉÕ±”İ…Ì(€€€¥¹‘¥™™•É•¹ĞÑ¼Ñ¡”‘¥Í…É••µ•¹ĞƒŠPÑ¡”•¹ÑÉäÍ…åÌ€‰Á±…•ˆ°Ñ¡”Ù…±Õ”İ…Ì½¹©•ÑÕÉ…°°…¹Ñ¡”(€€€µ…Ñ ¡•±™½È„É•…Í½¸Ñ¡…Ğ¡…¹½Ñ¡¥¹œÑ¼‘¼İ¥Ñ İ¡•Ñ¡•ÈÑ¡”Ñİ¼…É••¸•±…É¥¹œÑ¡”(€€€±…¥´™½É•Ñ¡”½µÁ…É¥Í½¸¸0ÄÈ¹½Ü…ÉÉ¥•Ì„I•Ù¥Í•±¥¹”Í…å¥¹œÍ¼°…¹Ñ¡”ÍÑ…±”Í•¹Ñ•¹”(€€€ÍÑ…åÌèÑ¡”™¥±”¥Ì…ÁÁ•¹µ½¹±ä°…¹„Í¥±•¹Ñ±ä½ÉÉ•Ñ•…‘µ¥ÍÍ¥½¸¥Ì¹½Ğ½¹”¸(ÄÔ¸€¨©%aƒŠPÑ¡”ÍÑ…±•¹•ÍÌ…Ñ”•á¥ÍÑ•¥¸Ñ¡”‘½Õµ•¹Ñ…Ñ¥½¸…¹¹½İ¡•É”•±Í”¸¨¨9QL¹µ‘€(€€€¡…ÌÍ…¥Í¥¹”Ñ¡”Í…™™½±Ñ¡…Ğ€‰„ÍÑ…±”½µµ¥ÑÑ•1¥Ì„¡•¬™…¥±ÕÉ”°¹½Ğ„İ…É¹¥¹œˆ°(€€€…¹…ÍÍ•ÑÌ½µ…¹¥™•ÍĞ¹©Í½¹€¡…Ì…ÉÉ¥•…¸¥¹ÁÕÑÍ}Í¡„ÈÔÙ€Á•È…ÍÍ•ĞÍ¥¹”Ñ¡”™¥ÉÍĞ‰…­”¸(€€€9½Ñ¡¥¹œ•Ù•ÈÉ•½µÁÕÑ•¥Ğ¸ÉÕ¹}ÍÑ…±•}¡•­€…Í­•½¹±äİ¡•Ñ¡•È•… 1…ÁÁ•…É•¥¸Ñ¡”(€€€µ…¹¥™•ÍĞ°Í¼„É•½É½Õ±‰”•‘¥Ñ•¥¹Ñ¼„‘¥™™•É•¹Ğ‰Õ¥±‘¥¹œ…¹Ñ¡”Ñ½İ¸İ½Õ±­••À(€€€É•¹‘•É¥¹œÑ¡”½±½¹”İ¥Ñ Ñ¡”…Ñ”É••¸ƒŠPÑ¡”•á…Ğ™…¥±ÕÉ”µ½‘”Ñ¡”LÔÉ•Á…¥ÉÌ…É”ÅÕ•Õ•(€€€™½È°Õ¹Õ…É‘•¸Q¡”¡•¬¹½ÜÉ•½µÁÕÑ•Ì•Ù•Éä½µµ¥ÑÑ•…ÍÍ•ĞÌ¥¹ÁÕÑÌ…¹™…¥±Ì½¸(€€€‘¥Í…É••µ•¹Ğ°…¹Ñ¡”É•¥Á”±¥Ù•Ìİ¥Ñ Ñ¡”•¹•É…Ñ½ÉÌ€¡•¹•É…Ñ½ÉÌ½µ•Í¡}¥¹ÁÕÑÌ¹Áå€°(€€€Ñ•ÉÉ…¥¹}•¸¹Ñ•ÉÉ…¥¹}¥¹ÁÕÑÍ}Í¡…€¤Í¼Ñ¡”Í¥‘”Ñ¡…ĞİÉ¥Ñ•ÌÑ¡”¡…Í …¹Ñ¡”Í¥‘”Ñ¡…Ğ¡•­Ì(€€€¥Ğ…¹¹½Ğ‘É¥™Ğ¸(€€€€¨©Mİ¥Ñ¡¥¹œ¥Ğ½¸É•ÅÕ¥É•É•‘•™¥¹¥¹œÑ¡”¡…Í °‰•…ÕÍ”Ñ¡”½±½¹”İ…ÌÕ¹ÕÍ…‰±”¸¨¨%Ğ¡…Í¡•(€€€Ñ¡”İ¡½±”Á¡…Í”É•½ÉÁ±ÕÌ•Ù•Éä€¹Áå€Õ¹‘•È•¹•É…Ñ½ÉÌ½€°İ¡¥ µ•…¹Ğ…±°Í¥à‰Õ¥±‘¥¹Ì(€€€É•…ÍÑ…±”™½ÈÉ•…Í½¹ÌÑ¡…Ğ…¹¹½Ğµ½Ù”„Ù•ÉÑ•àèÑ¡”•½µ•ÑÉäé€‘•±…É…Ñ¥½¹Ì…‘‘•½¸(€€€€ÈÀÈØ´Àà´ÄÀ°…¹„=9MU5€½¹ÍÑ…¹Ğ…‘‘•Ñ¼½¹”…É¡•ÑåÁ”ÌÁ…É…µ•Ñ•Èµ½‘Õ±”¥¹Ù…±¥‘…Ñ¥¹œ(€€€Ñ¡”½Ñ¡•ÉÌœ‰Õ¥±‘¥¹Ì¸¡…Í Ñ¡…ĞÉ¥•ÌÍÑ…±”½Ù•È„É•İÉ¥ÑÑ•¸¹½Ñ”•ÑÌ‘¥Í‰•±¥•Ù•°…¹„(€€€‘¥Í‰•±¥•Ù•…Ñ”¥Ìİ½ÉÍ”Ñ¡…¸¹½¹”¸%Ğ¹½Ü¡…Í¡•Ìİ¡…ĞÑ¡”‰Õ¥±‘•È…¸Í•”ƒŠPÑ¡”€©É•Í½±Ù•¨(€€€Á…É…µ•Ñ•ÉÌ°Ñ¡”±…ÍÌÌ‘•É¥Ù•ÁÉ½Á•ÉÑ¥•Ì°Ñ¡”½¹™¥‘•¹”™±½…ÑÌ°…¹Ñ¡”‰åÑ•Ì½˜Ñ¡”(€€€‰Õ¥±‘•È°½µµ½¸½€°‰Õ¥±¹Áå€…¹Ñ¡”	±•¹‘•ÈÁ¥¸¸A…É…µ•Ñ•Èµµ½‘Õ±”‰åÑ•Ì…É”‘•±¥‰•É…Ñ•±ä(€€€½ÕĞèÑ¡…Ğµ½‘Õ±”Ìİ¡½±”•™™•Ğ½¸Ñ¡”µ•Í ¥ÌÑ¡”½‰©•Ğ¥ĞÉ•ÑÕÉ¹Ì°…¹Ñ¡”½‰©•Ğ¥Ì(€€€¡…Í¡•¥¸µ½É”‘•Ñ…¥°Ñ¡…¸¥ÑÌÍ½ÕÉ”İ½Õ±¥Ù”¸(€€€€¨©Q¡”•¥¡Ğ½µµ¥ÑÑ•¡…Í¡•Ìİ•É”É”µÍÑ…µÁ•İ¥Ñ¡½ÕĞ„‰…­”°…¹Ñ¡…Ğ¥Ì„±…¥´°Í¼¡•É”¥Ì(€€€Ñ¡”ÁÉ½½˜¸¨¨U¹‘•ÈÑ¡”¹•ÜÉ•¥Á”°•Ù•Éä¥¹ÁÕĞÑ¼…±°Í¥à‰Õ¥±‘¥¹Ì¥Ì‰åÑ”µ¥‘•¹Ñ¥…°Ñ¼İ¡…Ğ(€€€¥Ğİ…Ì…ĞÑ¡”±…ÍĞ‰…­”€¡ŒÌäÔÍÉ€¤ƒŠP¡•­•‰äÉÕ¹¹¥¹œÑ¡”¹•ÜÉ•¥Á”¥¹Í¥‘”„İ½É­ÑÉ•”½˜(€€€Ñ¡…Ğ½µµ¥Ğ…¹‘¥™™¥¹œÑ¡”¥¹ÁÕĞ‘½Õµ•¹ÑÌ°¹½Ğ‰ä¥¹ÍÁ•Ñ¥½¸¸Q¡”Í¥¹±”‘¥™™•É•¹”¥Ì(€€€‰Õ¥±¹Áå€°İ¡½Í”½¹±ä¡…¹”¥¸Ñ¡¥ÌÍ±¥”¥Ì‘•±•…Ñ¥¹œÑ¡”¡…Í Ñ¼Ñ¡”¹•Üµ½‘Õ±”¸Q•ÉÉ…¥¸(€€€É”µÍÑ…µÁ•™½ÈÑ¡”Í…µ”É•…Í½¸èÑ•ÉÉ…¥¹}•¸¹Áå€¡…Í¡•Ì¥ÑÌ½İ¸‰åÑ•Ì…¹…¥¹•…¸•áÑÉ…Ñ•(€€€™Õ¹Ñ¥½¸¸9¼µ•Í İ…ÌÉ••¹•É…Ñ•…¹¹½¹”¹••‘•Ñ¼‰”¸µ…¹¥™•ÍĞ¹©Í½¹€¹½ÜÉ•½É‘Ì(€€€¥¹ÁÕÑÍ}Í¡•µ•€°…¹Ñ¡”…Ñ”É•™ÕÍ•Ì„µ…¹¥™•ÍĞÍÑ…µÁ•Õ¹‘•È„Í¡•µ”¥Ğ‘½•Ì¹½Ğ½µÁÕÑ”(€€€É…Ñ¡•ÈÑ¡…¸½µÁ…É¥¹œÑİ¼¡…Í¡•ÌÑ¡…Ğµ•…¸‘¥™™•É•¹ĞÑ¡¥¹Ì¸(€€€]¡…ĞÑ¡¥ÌÍÑ¥±°‘½•Ì¹½Ğ…Ñ ¥ÌÍÑ…Ñ•¥¸µ•Í¡}¥¹ÁÕÑÌ¹Áå€è¥Ğ½µÁ…É•Ì¥¹ÁÕÑÌ°¹½Ğ½ÕÑÁÕĞ¸(€€€å±•Ì<¥Ì¹½Ğ‰¥ĞµÉ•ÁÉ½‘Õ¥‰±”…É½ÍÌ¡…É‘İ…É”°İ¡¥ ¥Ìİ¡ä™É•Í¡¹•ÍÌ¥Ì‘•™¥¹•½¸¥¹ÁÕÑÌ(€€€…Ğ…±°ƒŠP„¡…¹µ•‘¥Ñ•1‰•¡¥¹…¸Õ¹Ñ½Õ¡•É•½ÉÁ…ÍÍ•Ì°…¹¹½Ñ¡¥¹œ¡•É”…¸Í•”¥Ğ¸(ÄØ¸€¨©Q¡”¹¥¡Ñ±ä‰…­”ÁÕÍ¡•Ì¥ÑÌ‰É…¹ …¹…¹¹½Ğ½Á•¸¥ÑÌAH¸¨¨¡¥…¼´Ñµ‰…­”¹åµ±€•¹‘Ì(€€€‰äÉ•…Ñ¥¹œ„ÁÕ±°É•ÅÕ•ÍĞ…¹Ñ¡…ĞÍÑ•À¡…Ì‰••¸™…¥±¥¹œ½¸„É•Á½Í¥Ñ½ÉäÍ•ÑÑ¥¹œƒŠP(€€€€‰¥Ñ!ÕˆÑ¥½¹Ì¥Ì¹½ĞÁ•Éµ¥ÑÑ•Ñ¼É•…Ñ”½È…ÁÁÉ½Ù”ÁÕ±°É•ÅÕ•ÍÑÌˆƒŠPÍ¼•Ù•Éä‰…­”Í¥¹”(€€€Ñ¡”İ½É­™±½Üİ…ÌİÉ¥ÑÑ•¸¡…Ì±•™Ğ¥ÑÌ•½µ•ÑÉä½¸…¸½ÉÁ¡…¸ÍÑ•İ…É½‰…­”´©€‰É…¹ Ñ¡…Ğ(€€€¹½Ñ¡¥¹œµ•É•Ì¸¥¡ĞÍÕ ‰É…¹¡•Ì•á¥ÍĞ¸Q¡¥ÌÍ±¥”İ½É­•…É½Õ¹¥Ğ‰ä™•Ñ¡¥¹œÑ¡”‰…­”(€€€‰É…¹ …¹™…ÍĞµ™½Éİ…É‘¥¹œ½¹Ñ¼¥Ğ°İ¡¥ ¥Ì™¥¹”™½È…¸…•¹ĞÑ¡…Ğ¥Ìİ…Ñ¡¥¹œ°…¹¹¼ÕÍ”(€€€…Ğ…±°™½ÈÑ¡”¹¥¡Ñ±ä¸Q¡”™¥à¥Ì½¹”¡•­‰½à¥¸Ñ¡”É•Á½Í¥Ñ½ÉäÌÑ¥½¹ÌÍ•ÑÑ¥¹Ì°½È„(€€€AP½¸Ñ¡…ĞÍÑ•ÀìÑ¡”İ½É­™±½Ü±¥Ù•Ì½ÕÑÍ¥‘”¡¥…¼¼Ñ½€…¹¥ÌÑ¡•É•™½É”½ÕÑÍ¥‘”Ñ¡¥Ì(€€€±…¹”ÌÍ½Á”Ñ¼•‘¥Ğ°Í¼¥Ğ¥ÌÉ•½É‘•¡•É”É…Ñ¡•ÈÑ¡…¸™¥á•¸(ÄÜ¸€¨©É…µ”É…Ñ”™¥ÕÉ•Ì…É”µ•…¹¥¹±•ÍÌ¡•É”¸¨¨€ËŠLä™ÁÌÕ¹‘•È¡•…‘±•ÍÌMİ¥™ÑM¡…‘•È¥ÌÍ½™Ñİ…É”(€€€É…ÍÑ•É¥Í…Ñ¥½¸°¹½Ğ„ATµ•…ÍÕÉ•µ•¹Ğ¸É…Ü…±±Ì€ ÄÈ¤…¹ÑÉ¥…¹±•Ì€ Ä°ÀÀØ¤…É”É•…°¸((Äà¸€¨©%aƒŠPÑ¡”]½±˜A½¥¹ĞQ…Ù•É¸¡…Ì¥ÑÌ™É…µ”¡…±˜…¹¥ÑÌİ½±˜Í¥¸¸¨¨Q¡”‘•™•ĞÑ¡”(€€€½µ¥ÍÍ¥½¸…Ñ”™½Õ¹½¸€ÈÀÈØ´Àà´ÄÀ¥ÌÉ•Á…¥É•Ñ¡”Í…µ”‘…ä°É•½É…¹µ•Í ¥¸½¹”½µµ¥Ğè(€€€™É…µ•}•áÑ•¹Í¥½¹€ƒŠH™É…µ•}…‘‘¥Ñ¥½¹€°Í¥¹…•€ƒŠHÍ¥¹€°Ñ¡”Ñİ¼¹…µ•Ì±½}‘İ•±±¥¹€(€€€…ÑÕ…±±äÉ•…‘Ì¸Q¡”‰Õ¥±‘¥¹œÑ¡…Ğ¹…µ•]½±˜A½¥¹Ğ¹½Ü¡…Ì„‰½…É¡…¹¥¹œ½ÕÑÍ¥‘”¥Ğ¸(€€€€¨©Q¡”É•¹…µ”İ…ÌÑ¡”Íµ…±±•È¡…±˜¸¨¨™É…µ•}…‘‘¥Ñ¥½¸èÑÉÕ•€…¹¹½Ñ¡¥¹œ•±Í”İ½Õ±¡…Ù”±•Ğ(€€€Ñ¡”…É¡•ÑåÁ”Á¥¬Ñ¡”‰…äÌÍ¥‘”°İ¥‘Ñ °‘•ÁÑ …¹ÍÑ½É•ä½Õ¹Ğ™É½´¥ÑÌ‘•™…Õ±ÑÌƒŠP„(€€€Ñİ¼µÍÑ½É•ä™É…µ”‰±½¬…É½ÍÌÑ¡”É¥Ù•È™É½¹Ğ½˜„Ñ…Ù•É¸Ñ¡”Í½ÕÉ•Ì‘•ÍÉ¥‰”…Ì±½ÜƒŠPÍ¼„(€€€‘½Õµ•¹Ñ•™•…ÑÕÉ”İ½Õ±¡…Ù”…ÉÉ¥Ù•…Ğ…¸¥¹Ù•¹Ñ•Í¥é”İ¥Ñ ¹½Ñ¡¥¹œ…‘µ¥ÑÑ¥¹œ¥Ğ°İ¡¥ ¥Ì(€€€Ñ¡”Í…µ”™…¥±ÕÉ”Ñ¡¥ÌÉ•Á…¥È•á¥ÍÑÌÑ¼•¹°½¹”±•Ù•°‘½İ¸¸Q¡”É•½ÉÑ¡•É•™½É”ÍÑ…Ñ•Ì…±°(€€€™½ÕÈèÍ¥‘”•¹‘€…¹İ¥‘Ñ €Ğ´½˜Ñ¡”€ÄÈ´™É½¹Ñ…”…¹‘•ÁÑ €Ü´…±°€¨©½¹©•ÑÕÉ…°¨¨°ÍÑ½É•ä(€€€½Õ¹Ğ€Ä€¨©¥¹™•ÉÉ•¨¨‰äÑ¡”Í…µ”…ÉÕµ•¹ĞÑ¡”ÍÑ½É•ä½Õ¹Ğ…‰½Ù”¥ĞÕÍ•Ì¸0ÈĞ…‘µ¥ÑÌÑ¡”Ñ¡É•”(€€€½¹©•ÑÕÉ…°½¹•Ìì0ÈÀµ½Ù•ÌÑ¼I•Í½±Ù•…ÉÉå¥¹œ‰½Ñ ÍÁ•±±¥¹ÌÑ¡…Ğ¹¼±½¹•ÈÉ•Í½±Ù”°(€€€‰•…ÕÍ”„Í¥±•¹Ñ±ä½ÉÉ•Ñ•…‘µ¥ÍÍ¥½¸¥Ì¹½Ğ½¹”¸(€€€€¨©]¡…ĞÑ¡”Í¥¸¥Ìè„‰±…¹¬‰½…É¸¨¨Q¡”‰É…­•Ğ°Ñ¡”…É´°Ñ¡”‰½…É…¹¥ÑÌÁÉ½Á½ÉÑ¥½¹Ì…É”(€€€Ñ¡”…É¡•ÑåÁ”Ì¥¹Ù•¹Ñ¥½¸°…¹Ñ¡”Á…¥¹Ñ•İ½±˜¥Ì¹½Ğ‘É…İ¸ƒŠP¹¼‘•ÍÉ¥ÁÑ¥½¸½˜¥ĞÍÕÉÙ¥Ù•Ì°(€€€…¹„İ½±˜Á…¥¹Ñ•™É½´¥µ…¥¹…Ñ¥½¸İ½Õ±‰”Ñ¡”µ½ÍĞ½¹ÍÁ¥Õ½ÕÌ¥¹Ù•¹Ñ¥½¸¥¸Ñ¡”Í•¹”½¸(€€€Ñ¡”½¹”½‰©•Ğ•Ù•ÉäÙ¥Í¥Ñ½Èİ¥±°İ…±¬ÕÀÑ¼¸0ÈÔÍ…åÌÍ¼¸(€€€€¨©Qİ¼±¥µ¥ÑÌİ½ÉÑ ÍÑ…Ñ¥¹œ¸¨¨Q¡”½¹™¥‘•¹”Ñ¥¹Ğ½¸Ñ¡”‰…ä™½±±½İÌİ¡…ĞÑ¡”‰…ä%L(€€€€¡‘½Õµ•¹Ñ•Ñ¡…Ğ¥Ğ•á¥ÍÑ•°¥¹™•ÉÉ•Ñ¡…Ğ¥Ğİ…Ì±½Ü¤°¹½Ğ¥ÑÌÕ¹­¹½İ¸Í¥é”ƒŠPÑ¡”ÉÕ±”Í•Ğ(€€€™½ÈÑ¡”M…Õ…¹…Í °İ¡¥ µ•…¹ÌÑ¡”Ñ¥¹Ğ…±½¹”İ¥±°¹½ĞÑ•±°„Ù¥Í¥Ñ½ÈÑ¡”İ¥‘Ñ ¥Ì„Õ•ÍÌ…¹(€€€½¹±äÑ¡”Á½ÁÕÀÌ±¥‰•ÉÑä¡¥Àİ¥±°¸¹Ñ¡”İ¡½±”É•Á…¥ÈÉ•ÍÑÌ½¸„™½½ÑÁÉ¥¹ĞÑ¡…Ğ¥Ì¥ÑÍ•±˜„(€€€Á±…•¡½±‘•Èè€Ğ´½˜…¸¥¹Ù•¹Ñ•€ÄÈ´¥Ì„™É…Ñ¥½¸½˜„Õ•ÍÌ¸((Ää¸€¨©%aƒŠPÑ¡”¡¥µ¹•ä½Õ¹Ğ¥Ì„¹Õµ‰•ÈÑ¡”…É¡•ÑåÁ•ÌÉ•…°…¹Ñ¡”Ñ¡¥Éµ¥ÍÍÁ•±±¥¹œ¥Ì¹½Ü(€€€„Ñ•ÍĞ¸¨¨Ù•ÉäÉ•½ÉÍÑ…Ñ•Ì¡¥µ¹•åÍ€ì¹•¥Ñ¡•È…É¡•ÑåÁ”É•…Ñ¡”Ù…±Õ”¸™É…µ•}Ñ…Ù•É¹€(€€€‰Õ¥±ĞÑİ¼ÍÑ…­Ìİ¡…Ñ•Ù•ÈÑ¡”É•½ÉÍ…¥…¹±½}‘İ•±±¥¹€‰Õ¥±Ğ½¹”°Í¼M…µÕ•°5¥±±•ÈÌ(€€€¡½ÕÍ”ƒŠPÉ•½ÉÑİ¼°µ½‘•°½¹”ƒŠPÍÑ½½„ÍÑ…¬Í¡½ÉĞ™É½´¥ÑÌ™¥ÉÍĞ‰…­”¸	½Ñ …É¡•ÑåÁ•ÌÑ…­”(€€€Ñ¡”½Õ¹Ğ¹½Ü¸Q¡”Á…¥È½¸„™É…µ”‰±½¬­••ÁÌ¥ÑÌ•á…ĞÁ½Í¥Ñ¥½¹Ì€ À¸ÈÈ…¹€À¸Üà½˜Ñ¡”(€€€™É½¹Ñ…”°É•…½™˜Ñ¡”M…Õ…¹…Í ‘•Á¥Ñ¥½¹Ì¤Í¼Ñ¡…ĞÁ…É…µ•Ñ•É¥Í¥¹œÑ¡”¹Õµ‰•È‘¥¹½ĞÅÕ¥•Ñ±ä(€€€µ½Ù”„‰Õ¥±‘¥¹œİ¡½Í”½Õ¹Ğİ…Ì…±É•…‘äÉ¥¡Ğì„±½œ‰Õ¥±‘¥¹œÌÍ•½¹ÍÑ…¬½•Ì½¸Ñ¡”™É…µ”(€€€…‘‘¥Ñ¥½¸É…Ñ¡•ÈÑ¡…¸Ñ¡”™…È…‰±”°‰•…ÕÍ”€©Ñ¡”É•½ÉÌ½İ¸É•…Í½¸¨™½È½Õ¹Ñ¥¹œÑİ¼¥Ì€‰„(€€€ÍÑ…¬¥¸•… •±•µ•¹Ğˆ°…¹¡½¹½ÕÉ¥¹œÑ¡”¹Õµ‰•Èİ¡¥±”½¹ÑÉ…‘¥Ñ¥¹œ¥ÑÌ…ÉÕµ•¹Ğ¥Ì¹½Ğ(€€€¡½¹½ÕÉ¥¹œ¥Ğ¸0ÈÄµ½Ù•ÌÑ¼I•Í½±Ù•…¹Ñ¡”Í¥àÉ•½É‘Ì‘É½ÀÑ¡”•½µ•ÑÉäè€Í¥µÁ±¥™¥•€(€€€‘•±…É…Ñ¥½¸Ñ¡…Ğİ…ÌÑÉÕ”Õ¹Ñ¥°Ñ¡¥Ì±…¹‘•¸(€€€€¨©Q¡”±½}‘İ•±±¥¹€¡…±˜İ…ÌÑ¡”]½±˜A½¥¹Ğ‘•™•Ğ„Ñ¡¥ÉÑ¥µ”¸¨¨Q¡”Á…É…µ•Ñ•Èİ…Ì(€€€¡¥µ¹•å€°„‰½½±•…¸ì¹¼É•½É¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ¡…Ì•Ù•È½¹Ñ…¥¹•Ñ¡…Ğİ½É°Í¼™É½µ}Á¡…Í•€(€€€Ñ½½¬¥ÑÌ‘•™…Õ±Ğ½¸•Ù•Éä±½œ‰Õ¥±‘¥¹œ…¹¹½Ñ¡¥¹œ½µÁ±…¥¹•¸Q¡É•”½ÕÉÉ•¹•Ì½˜½¹”(€€€™…¥±ÕÉ”¥Ì„Á…ÑÑ•É¸É…Ñ¡•ÈÑ¡…¸‰…±Õ¬°Í¼¥Ğ¹½Ü¡…Ì„¡•¬¥¹ÍÑ•…½˜…¹½Ñ¡•È(€€€‘¥Í½Ù•É•ÈèÑ•ÍÑ}½¹ÍÕµ•‘}…ÑÑÉ¥‰ÕÑ•Í}…ÑÕ…±±å}É•…¡}Ñ¡•}Á…É…µ•Ñ•ÉÍ€Á•ÉÑÕÉ‰Ì•Ù•ÉäÍÑ…Ñ•(€€€Ù…±Õ”¥ÑÌ…É¡•ÑåÁ”‘•±…É•Ì¥Ğ=9MU5L…¹É•ÅÕ¥É•ÌÑ¡”É•Í½±Ù•Á…É…µ•Ñ•ÉÌÑ¼¡…¹”ƒŠP€ÔÔ(€€€…ÑÑÉ¥‰ÕÑ•Ì•á•É¥Í•…É½ÍÌÑ¡”Í¥àÉ•½É‘Ì°İ¥Ñ „A…É…µÉÉ½É€½Õ¹Ñ•…ÌÉ•…°Í¥¹”(€€€É•™ÕÍ¥¹œ„Ù…±Õ”¥ÌÑ¡”±½Õ‘•ÍĞÁ½ÍÍ¥‰±”ÁÉ½½˜½˜¡…Ù¥¹œÍ••¸¥Ğ¸Q¡”½ÁÁ½Í¥Ñ”‘¥É•Ñ¥½¸€¡…¸(€€€…ÑÑÉ¥‰ÕÑ”ÍÑ…Ñ•…¹€©¹½Ğ¨‘•±…É•¤İ…Ì…±É•…‘äÑ¡”½µ¥ÍÍ¥½¸…Ñ”ìÑ¡¥Ì±½Í•ÌÑ¡”‘¥É•Ñ¥½¸(€€€İ¡•É”Ñ¡”‘•±…É…Ñ¥½¸¥ÑÍ•±˜¥ÌÑ¡”™…±Í”½¹”°İ¡¥ ¥ÌÑ¡”İ½ÉÍ”½˜Ñ¡”Ñİ¼°‰•…ÕÍ”…¸(€€€…ÑÑÉ¥‰ÕÑ”¥¹Í¥‘”=9MU5¥Ì•áÕÍ•™É½´…‘µ¥ÑÑ¥¹œ…¹åÑ¡¥¹œ¸(€€€€¨©]¡…Ğ¥Ğ‘½•Ì¹½Ğ™¥à°…¹Ñ¡…Ğ¥ÌÑ¡”µ½É”¥¹Ñ•É•ÍÑ¥¹œ¡…±˜¸¨¨Q¡”½Õ¹Ğ¥Ì¥¹™•ÉÉ•‘€½¸(€€€•Ù•Éä‰Õ¥±‘¥¹œ…¹¹½Ñ¡¥¹œ•±Í”…‰½ÕĞ„ÍÑ…¬¥ÌÉ•½É‘•…¹åİ¡•É”ƒŠP¹½Ğ½¹”Í½ÕÉ”‘•ÍÉ¥‰•Ì(€€€„¡¥µ¹•ä½¸…¹ä½˜Ñ¡•Í”Í¥à¸A½Í¥Ñ¥½¸°¥ÉÑ °¡•¥¡Ğ…‰½Ù”Ñ¡”É¥‘”…¹µ…Ñ•É¥…°…É”…±°(€€€Ñ¡”…É¡•ÑåÁ”Ì°Í¼Ñ¡”½¹™¥‘•¹”¡¥À„Ù¥Í¥Ñ½ÈÉ•…‘Ì½¸Ñ¡…ĞÉ½ÜÉ…‘•Ì½¹±ä€©¡½Üµ…¹ä¨¸(€€€0ÈØ¥Ì¹•Ü…¹¥ÌÑ¡”½¹±äÁ±…”Ñ¡…Ğ‘¥ÍÑ¥¹Ñ¥½¸¥Ì±•¥‰±”¸((ÈÀ¸€¨©%aƒŠP5¥±±•ÈÌ™É…µ”É…¹”¥Ì‘¥µ•¹Í¥½¹•‰äÑ¡”É•½É°…¹™¥á¥¹œ¥Ğ™½Õ¹Ñ¡”ÍÑ½É•åÌ(€€€½¸Ñ¡”İÉ½¹œ¡…±˜½˜Ñ¡”¡½ÕÍ”¸¨¨Q¡”ÅÕ•Õ•‘•™•Ğİ…Ì0ÈĞÌ½¹”‰Õ¥±‘¥¹œ½Ù•Èè(€€€™É…µ•}…‘‘¥Ñ¥½¹€¥Ì‘½Õµ•¹Ñ•‘€½¸µ¥±±•É}¡½ÕÍ•€ƒŠP€‰„Ñİ¼µÍÑ½Éä¡½ÕÍ”…‘‘•Ñ¼Ñ¡”…‰¥¸°(€€€™É½¹Ñ¥¹œÑ¡”É¥Ù•ÈˆƒŠP…¹Ñ¡”É•½ÉÍÑ…Ñ•¹¼Í¥‘”°¹¼İ¥‘Ñ °¹¼‘•ÁÑ …¹¹¼ÍÑ½É•ä½Õ¹Ğ°(€€€Í¼±½}‘İ•±±¥¹€ÍÕÁÁ±¥•…±°™½ÕÈ™É½´¥ÑÌ‘•™…Õ±ÑÌ¸I•Á…¥É•€ÈÀÈØ´Àà´ÄÀ°É•½É…¹µ•Í ¥¸(€€€½¹”½µµ¥Ğ¸Qİ¼½˜Ñ¡”™½ÕÈÑÕÉ¸½ÕĞÑ¼‰”€¨©…ÑÑ•ÍÑ•¨¨°İ¡¥ ¥ÌÑ¡”‘¥™™•É•¹”‰•Ñİ••¸Ñ¡¥Ì(€€€‰Õ¥±‘¥¹œ…¹Ñ¡”]½±˜A½¥¹Ğ‰…äèÑ¡”Í¥‘”¥Ì™É½¹Ñ€‰•…ÕÍ”Ñ¡”Í½ÕÉ”Í…åÌ€©™É½¹Ñ¥¹œÑ¡”(€€€É¥Ù•È¨°…¹Ñ¡”É…¹”¥ÌÑİ¼ÍÑ½É•åÌ‰•…ÕÍ”Ñ¡”Í½ÕÉ”Í…åÌ€©„Ñİ¼µÍÑ½Éä¡½ÕÍ”¨¸=¹±äÑ¡”(€€€İ¥‘Ñ …¹‘•ÁÑ …É”¥¹Ù•¹Ñ•°…¹Ñ¡•ä…É”É•…½™˜Ñ¡¥ÌÉ•½ÉÌ½İ¸™½½ÑÁÉ¥¹ĞÁ½±å½¸ƒŠPÑ¡”(€€€É¥Ù•Èµ™É½¹Ñ¥¹œ±¥µˆ¥Ì€äƒ\€Ø´ƒŠPÉ…Ñ¡•ÈÑ¡…¸Á¥­•…™É•Í °Í¼Ñ¡”µ•Í …É••Ìİ¥Ñ Ñ¡”Á±…¸(€€€Ñ¡”É•½É…±É•…‘ä‘É…İÌ¸0ÈÜ…‘µ¥ÑÌÑ¡•´ìÑ¡•ä¥¹¡•É¥ĞÑ¡”Á½±å½¸Ì¥¹Ù•¹Ñ¥½¸°İ¡¥ ¥Ì(€€€Ñ½Ñ…°¸(€€€€¨©Q¡”ÍÑ½É•ä½Õ¹Ğİ…ÌÑ¡”É•…°‘•™•Ğ…¹¥Ğİ…Ì¹½Ğ½¸Ñ¡”ÅÕ•Õ”¸¨¨ÍÑ½É¥•Í€İ…Ì€È°(€€€‘½Õµ•¹Ñ•‘€°İ¥Ñ ¥ÑÌ½İ¸¹½Ñ”Í…å¥¹œ¥¸…Ìµ…¹äİ½É‘ÌÑ¡…ĞÑ¡”Ñİ¼ÍÑ½É•åÌ‘•ÍÉ¥‰•Ñ¡”(€€€É¥Ù•Èµ™É½¹Ñ¥¹œÉ…¹”…¹¹½ĞÑ¡”İ¡½±”‰Õ¥±‘¥¹œƒŠP‰ÕĞ±½}‘İ•±±¥¹€É•…‘ÌÍÑ½É¥•Í€…ÌÑ¡”(€€€1==IÌ½Õ¹Ğ¸M¼Ñ¡”‘½Õµ•¹Ñ•±…¥´İ…ÌÍÁ•¹Ğ½¸Ñ¡”…‰¥¸°Ñ¡”É…¹”™•±°‰…¬Ñ¼„(€€€€Ğ¸Ü´‘•™…Õ±Ğ°…¹Ñ¡”µ½‘•°ÍÑ½½„Ñİ¼µÍÑ½É•ä±½œ…‰¥¸€¨©‰•¡¥¹„Í¡½ÉÑ•È™É…µ”‰±½¬¨¨è(€€€Ñ¡”½µÁ½Í¥Ñ¥½¸¥¹Ù•ÉÑ•°Í••¸™É½´Ñ¡”•á…ĞÍÁ½Ğ…É½ÍÌÑ¡”İ…Ñ•Èİ¡•É”Ñ¡”€ÄàÌÌ‘•ÍÉ¥ÁÑ¥½¸(€€€½˜¥Ğİ…ÌİÉ¥ÑÑ•¸¸Q¡…Ğ¥ÌÑ¡”™É…µ•}•áÑ•¹Í¥½¹€½Í¥¹…•€½¡¥µ¹•å€™…¥±ÕÉ”¥¸¥ÑÌÍÕ‰Ñ±•È(€€€™½É´ƒŠP¹½Ğ„¹…µ”Ñ¡”…É¡•ÑåÁ”½Õ±¹½Ğ™¥¹°‰ÕĞ„¹…µ”¥Ğ™½Õ¹…¹É•……Ì‰•¥¹œ…‰½ÕĞ„(€€€‘¥™™•É•¹Ğ¡…±˜½˜Ñ¡”‰Õ¥±‘¥¹œ¸9¼ÍÁ•±±¥¹œ¡•¬…Ñ¡•ÌÑ¡…Ğ°…¹¹•¥Ñ¡•È‘½•Ì(€€€Ñ•ÍÑ}½¹ÍÕµ•‘}…ÑÑÉ¥‰ÕÑ•Í}…ÑÕ…±±å}É•…¡}Ñ¡•}Á…É…µ•Ñ•ÉÍ€°İ¡¥ ÁÉ½Ù•Ì½¹±äÑ¡…Ğ„Ù…±Õ”µ½Ù•Ì(€€€€©Í½µ•Ñ¡¥¹œ¨¸Q¡”Ñİ¼µÍÑ½É•ä±…¥´¹½ÜÍ¥ÑÌ½¸™É…µ•}…‘‘¥Ñ¥½¹}ÍÑ½É¥•Í€°Ñ¡”…‰¥¸ÌÍÑ½É¥•Í€(€€€¥Ì€Ä¥¹™•ÉÉ•‘€€¡¹¼Í½ÕÉ”¥Ù•ÌÑ¡”±½œÁ…ÉĞ„¡•¥¡ĞìÑ¡”€ÄàÌÌÙ¥•ÜÌ€‰„Ñİ¼µÍÑ½Éä‰Õ¥±‘¥¹œ(€€€…¹…‘©½¥¹¥¹œ±½œ…‰¥¸ˆ½¹±äÉ•…‘Ì…Ì„½¹ÑÉ…ÍĞ¥˜Ñ¡”…‰¥¸İ…Ì±½İ•È¤°Ñ¡”€Ô¸È´µ½Ù•ÌÑ¼(€€€™É…µ•}…‘‘¥Ñ¥½¹}¡•¥¡Ñ}µ€°…¹İ…±±}¡•¥¡Ñ}µ€‰•½µ•ÌÑ¡”…‰¥¸Ì€È¸Ø´ƒŠPÑ¡”¹Õµ‰•ÈÑ¡¥Ì(€€€É•½É¡…Ì¹…µ•™½È¥ĞÍ¥¹”¥Ğİ…ÌİÉ¥ÑÑ•¸°Í¥ÑÑ¥¹œ¥¸„¹½Ñ”É…Ñ¡•ÈÑ¡…¸¥¸„™¥•±¸(€€€0ÄÌµ½Ù•ÌÑ¼I•Í½±Ù•è¹•¥Ñ¡•È½µÁ½Í¥Ñ”‰Õ¥±‘¥¹œ¥Ì„Í¥¹±”•áÑÉÕÍ¥½¸…¹äµ½É”¸(€€€€¨©]¡…Ğ‘¥¹½Ğ•Ğ‰•ÑÑ•È¸¨¨Q¡”…É¡•ÑåÁ”µ…ÍÍ•ÌÑ¡”™½½ÑÁÉ¥¹ĞÌ‰½Õ¹‘¥¹œ‰½à°Í¼Ñ¡”±½œ(€€€½É”½µ•Ì½ÕĞÑ¡”™Õ±°€ä´İ¥‘”É…Ñ¡•ÈÑ¡…¸Ñ¡”Á½±å½¸Ì€Ø´…¹Ñ¡”€Ìƒ\€Ô´É”µ•¹ÑÉ…¹Ğ(€€€½É¹•È‰•¡¥¹Ñ¡”É…¹”¥Ì™¥±±•¥¸¸MÑ…Ñ¥¹œÑ¡”É…¹”Ì½İ¸¹Õµ‰•ÉÌ¥Ìİ¡…Ğµ…­•ÌÑ¡…Ğ(€€€Ù¥Í¥‰±”ƒŠPÑ¡”‘•™…Õ±ÑÌÁÉ½‘Õ•…¸¥¹Ù•ÉÑ•µPµ…Ñ¡¥¹œ¹•¥Ñ¡•ÈÑ¡”Á½±å½¸¹½ÈÑ¡”Í½ÕÉ•ÌƒŠP(€€€…¹0ÈÜÉ•½É‘Ì¥Ğ¸¹Ñ¡”İ¡½±”É•Á…¥ÈÍÑ¥±°É•ÍÑÌ½¸„Á±…•¡½±‘•Èè€äƒ\€Ø½˜…¸¥¹Ù•¹Ñ•(€€€€äƒ\€ÄÄ¸((ÈÄ¸€¨©Q¡”™¥ÉÍĞ‰É¥‘”°…¹Ñ¡”™¥ÉÍĞÉ•½Éİ¡½Í”Í¥é”¥Ì¹½Ğ„Á±…•¡½±‘•È¸¨¨Q¡”9½ÉÑ 	É…¹ (€€€É½ÍÍ¥¹œ…Ğ-¥¹é¥”MÑÉ••ĞƒŠP¡¥…¼Ì™¥ÉÍĞ‰É¥‘”°‰Õ¥±Ğ€ÄàÌÈ°É•Á±…•€ÄàÌäƒŠP¥Ì¹½Ü„(€€€É•½É°„‰…­”…¹„ÁÕ‰±¥Í¡•µ•Í °½¸Ñ¡”‰É¥‘•}Ñ¥µ‰•É€…É¡•ÑåÁ”Ñ¡…Ğ¡…‰••¸İÉ¥ÑÑ•¸(€€€…¹¹•Ù•ÈÕÍ•¸Qİ¼½˜¥ÑÌ¹Õµ‰•ÉÌ…É”•Ù¥‘•¹”É…Ñ¡•ÈÑ¡…¸¥¹Ù•¹Ñ¥½¸°İ¡¥ ¥Ì¹•Ü¡•É”è(€€€€¨©Ñ•¸™••Ğİ¥‘”¨¨¥Ì¡…É±•Ì±•…Ù•ÈÌ°É•…±±•¥¸Ñ¡”€©¡¥…¼QÉ¥‰Õ¹”¨½˜€Èä=Ğ€ÄàäÌ‰ä„(€€€µ…¸İ¡¼¡…‘É¥Ù•¸„Ñ•…´…É½ÍÌ¥Ğ°…¹Ñ¡”€¨¨ÜÄ¸àÌ´ÍÁ…¸¨¨¥Ìµ•…ÍÕÉ•‰•Ñİ••¸Ñ¡”Ñİ¼(€€€ÑÉ…•€ÄàÌĞİ…Ñ•É±¥¹•Ì…±½¹œÑ¡”-¥¹é¥”…±¥¹µ•¹ĞÉ…Ñ¡•ÈÑ¡…¸¡½Í•¸ƒŠP¥Ğ…É••Ìİ¥Ñ Ñ¡”(€€€É•… Ì‘É…™Ñ•µ•…¸İ¥‘Ñ Ñ¼…‰½ÕĞ„µ•ÑÉ”°İ¡¥ ¥ÌÑ¡”¡•¬Ñ¡…Ğ¥ĞÉ•…‘ÌÑ¡”µ…À…ĞÑ¡¥Ì(€€€ÍÑ…Ñ¥½¸¥¹ÍÑ•…½˜…Ù•É…¥¹œ¥Ğ¸Q¡É•”Í½ÕÉ”É•½É‘Ìİ•É”…‘‘•°…±°Ñ¡É•”İ¥Ñ ]…å‰…¬(€€€Í¹…ÁÍ¡½ÑÌ¸(€€€€¨©]¡…Ğ¥Ì¥¹Ù•¹Ñ•¥ÌÑ¡”µ¥‘‘±”½˜Ñ¡”‰É¥‘”°…¹¥Ğ¥ÌÑ¡”µ½ÍĞ½¹ÍÁ¥Õ½ÕÌÑ¡¥¹œ¥¸¥Ğ¸¨¨(€€€±•…Ù•È‘•ÍÉ¥‰•ÌÑ¡”•¹‘ÌƒŠP€‰Ñ¡”…‰ÕÑµ•¹ÑÌİ•É”‰Õ¥±Ğ½˜¡•…Ùä±½Ì¥¸Ñ¡”Í¡…±±½Üİ…Ñ•È¹•…È(€€€Ñ¡”‰…¹­ÌˆƒŠP…¹¹½‰½‘ä‘•ÍÉ¥‰•Ìİ¡…ĞÍÑ½½‰•Ñİ••¸Ñ¡•´¸M½µ•Ñ¡¥¹œ¡…Ñ¼…ÉÉä€ÜÄ¸àÌ´½˜(€€€±½œÍÑÉ¥¹•È°Í¼Ñ¡”…É¡•ÑåÁ”Ì‘•™…Õ±Ğ€Ğ¸Ô´ÍÁ…¥¹œÁÕÑÌ€¨©™¥™Ñ••¸É¥‰Ì¥¸Ñ¡”É¥Ù•È¨¨°„(€€€É•Õ±…È½±½¹¹…‘”„Ù¥Í¥Ñ½Èİ¥±°É•……Ì„™…Ğ…‰½ÕĞÑ¡”‰É¥‘”¸%Ğ¥Ì„™…Ğ…‰½ÕĞÑ¡”(€€€…É¡•ÑåÁ”¸0Èä…‘µ¥ÑÌ¥Ğ°…¹Ñ¡”½¹™¥‘•¹”Ñ¥¹Ğ…¹¹½ĞèÑ¡”Ñ¥¹ĞÉ…‘•Ìİ¡…Ğ„É¥ˆ€©¥Ì¨°(€€€¹½Ğ¡½Üµ…¹äÑ¡•É”İ•É”¸Q¡”ÍÁ…¸¥Ğ‘¥Ù¥‘•Ì¥Ì¥ÑÍ•±˜Ñ¡”‘É…İ¸İ…Ñ•É±¥¹”µÑ¼µİ…Ñ•É±¥¹”(€€€‘¥ÍÑ…¹”°…¹Ñ¡”…‰ÕÑµ•¹ÑÌÍÑ½½¥¹Í¥‘”Ñ¡…Ğ±¥¹”‰ä…¸Õ¹É•½É‘•…µ½Õ¹Ğ¸(€€€€¨©Qİ¼Í½ÕÉ•Ì½¹ÑÉ…‘¥Ğ•… ½Ñ¡•È…‰½ÕĞÑ¡”Ñ¡¥¹œ…¹‰½Ñ …É”­•ÁĞ¸¨¨¹‘É•…Ì¡…Ì¥Ğ(€€€€‰™½Éµ•½˜ÍÑÉ¥¹•ÉÌ…¹½¹±ä™¥ÑÑ•™½È™½½ĞÁ…ÍÍ•¹•ÉÌˆ…¹€‰ÕÍ•±•ÍÌ™½ÈÑ•…µÌˆ…Ì±…Ñ”…Ì(€€€Ñ¡”ÍÕµµ•È½˜€ÄàÌÌì±•…Ù•ÈÉ•µ•µ‰•É•‘É¥Ù¥¹œ…É½ÍÌ¥Ğ°…¹½¸€ÄàÕœ€ÄàÌÔ„ÁÉ½•ÍÍ¥½¸½˜(€€€¡Õ¹‘É•‘ÌÉ½ÍÍ•¥Ğ¸%Ğİ…ÌÉ•‰Õ¥±Ğ½Èİ¥‘•¹•¥¸‰•Ñİ••¸…¹¹½Ñ¡¥¹œÉ•…¡•Í…åÌİ¡•¸½È(€€€¡½Ü¸Q¡”É•½ÉÑ…­•ÌÑ¡”€ÄàÌÔÉ•…‘¥¹œƒŠP™½ÕÈÍÑÉ¥¹•ÉÌ°„™Õ±°µİ¥‘Ñ ‘•¬ƒŠP…¹Í…åÌ½¸¥ÑÌ(€€€½İ¸™…”Ñ¡…Ğ…¸€ÄàÌÌÍ•¹”İ½Õ±İ…¹ĞÑ¡”½Ñ¡•È½¹”¸(€€€€¨©½ÉÉ•Ñ¥½¸Ñ¼Ñ¡¥ÌÁÉ½©•ĞÌ½İ¸‘½ÍÍ¥•È…µ”½ÕĞ½˜İÉ¥Ñ¥¹œ¥Ğ¸¨¨(€€€‘½Ì½É•Í•…É ¼ÀÌµÍÑÉÕÑÕÉ•Ìµ¹½ÉÑ ¹µ‘€ƒ
œÔÑ…Ì‰½Ñ €‰…‰½ÕĞ€ÄÀ™Ğİ¥‘”ˆ…¹€‰±•…É¥¹œÑ¡”İ…Ñ•È(€€€‰ä…‰½ÕĞ€Ø™Ğˆ…Ì‘½Õµ•¹Ñ•¸=¹±äÑ¡”İ¥‘Ñ ÍÕÉÙ¥Ù•ÌèÑ¡”Á…•Ì…ÉÉå¥¹œÑ¡”İ¥‘Ñ °Ñ¡”(€€€…‰ÕÑµ•¹ÑÌ°Ñ¡”ÍÑÉ¥¹•ÉÌ°Ñ¡”€ÄàÌÈ‘…Ñ”…¹Ñ¡”€ÄàÌäÉ•Á±…•µ•¹ĞÍ…ä¹½Ñ¡¥¹œ…‰½ÕĞ„¡•¥¡Ğ(€€€…‰½Ù”Ñ¡”İ…Ñ•È°…¹„‘¥É•ĞÍ•…É ½˜Ñ¡”Í…µ”¡½ÍĞ™½ÈÑ¡”Á¡É…Í¥¹œÉ•ÑÕÉ¹Ì¹½Ñ¡¥¹œ¸Q¡”(€€€™¥ÕÉ”¥Ì­•ÁĞ°±•…É…¹•}µ€¥ÌÑ…•¥¹™•ÉÉ•‘€°…¹‰É¥‘•}Ñ¥µ‰•É}Á…É…µÌ¹Áå€Ì‘½ÍÑÉ¥¹œ(€€€¥Ì½ÉÉ•Ñ•Í¼Ñ¡”½¹ÍÑ…¹ĞÌ¹…µ”ÍÑ½ÁÌ…ÍÍ•ÉÑ¥¹œİ¡…Ğ¥Ğ…¹¹½ĞÍ¡½Ü¸(€€€€¨©Q¡”½¹ÑÉ…ĞÌİ…Ñ•Èµ…¹¡½ÈÉÕ±”¥Ìİ¥É•É…Ñ¡•ÈÑ¡…¸İÉ¥ÑÑ•¸¸¨¨‘½Ì½1µ=9QIP¹µ‘€¡…Ì(€€€Í…¥Í¥¹”Ñ¡”…É¡•ÑåÁ”İ…Ì‘É…™Ñ•Ñ¡…Ğ„ÍÑÉÕÑÕÉ”½Ù•Èİ…Ñ•È…¹¡½ÉÌä€ô€Á€…ĞÑ¡”‘•Í¥¸(€€€İ…Ñ•ÈÍÕÉ™…”…¹Ñ¡…ĞÑ¡”É•¹‘•É•ÈµÕÍĞÁ±…”¥Ğ……¥¹ÍĞÑ¡”İ…Ñ•ÈÁ±…¹”ì¹½Ñ¡¥¹œ¥µÁ±•µ•¹Ñ•(€€€¥Ğ°…¹¹½Ñ¡¥¹œ¹••‘•Ñ¼Õ¹Ñ¥°Ñ¡•É”İ…Ì„‰É¥‘”¸Q¡”…É¡•ÑåÁ”‘•±…É•ÌYIQ%1}9!=I€°(€€€½µÁ¥±•}Í•¹”¹Áå€½Á¥•Ì¥ĞÑ¼Á±…•µ•¹Ğ¹Ù•ÉÑ¥…±}…¹¡½É€°…¹Ñ¡”É•¹‘•É•ÈÁ±…•Ìİ…Ñ•É€(€€€…Ğ„±¥Ñ•É…°é•É¼ƒŠPÑ¡…ĞÁ±…¹”¥Ìé•É¼‰äÑ¡”‘•™¥¹¥Ñ¥½¸½˜Ñ¡”Ù•ÉÑ¥…°‘…ÑÕ´¸Q¡”Íµ½­”(€€€…ÍÍ•ÉÑÌÑ¡”€¨©‘¥™™•É•¹”¨¨‰•Ñİ••¸Ñ¡”Ñİ¼…¹¡½ÉÌ°¹½Ğä€ôôô€Á€è½Ù•È‘Éä±…¹Ñ¡•ä…É•”°(€€€Í¼„Ñ•ÍĞÑ¡…ĞÁ…ÍÍ•Ñ¡•É”İ½Õ±ÁÉ½Ù”¹½Ñ¡¥¹œ¸(€€€€¨©]É¥Ñ¥¹œÑ¡…Ğ…ÍÍ•ÉÑ¥½¸™½Õ¹Ñİ¼Ñ¡¥¹ÌÑ¡”½‘”İ…ÌÉ¥¡Ğ…‰½ÕĞ…¹Ñ¡”‘•ÍÉ¥ÁÑ¥½¸İ…Ì(€€€¹½Ğ¸¨¨¥ÉÍĞ°Í…µÁ±¥¹œ…ĞÑ¡”É•½ÉÌÁ±…•µ•¹Ğ½É¥¥¸ÁÉ½Ù•Ì¹½Ñ¡¥¹œ•¥Ñ¡•ÈèÑ¡…Ğ½É¥¥¸¥Ì(€€€Ñ¡”Á½±å½¸Ì€ À°€À¤°™½ÈÑ¡¥Ì‰É¥‘”Ñ¡”İ•ÍĞ•¹°İ¡¥ Í¥ÑÌ•á…Ñ±ä½¸Ñ¡”ÑÉ…•İ…Ñ•É±¥¹”(€€€İ¡•É”Ñ¡”É½Õ¹É½ÍÍ•Ìé•É¼ƒŠPé•É¼……¥¹ÍĞé•É¼°…¹Ñ¡”¡•¬Á…ÍÍ•Ìİ¡…Ñ•Ù•ÈÑ¡”É•¹‘•É•È(€€€‘½•Ì¸%ĞÍ…µÁ±•ÌÑ¡”‘•¬Ìµ¥‘Á½¥¹Ğ¹½Ü¸M•½¹°Ñ¡”™…¥±ÕÉ”µ½‘”¥ÌÑ¡”½ÁÁ½Í¥Ñ”½˜Ñ¡”(€€€½‰Ù¥½ÕÌ½¹”¸Ñ•ÉÉ…¥¸¹¡•¥¡Ğ ¥€‘½•Ì¹½ĞÉ•Á½ÉĞÑ¡”¡…¹¹•°‰•½Ù•Èİ…Ñ•Èì¥ĞÉ•Á½ÉÑÌ„(€€€€¨©İ…‘¥¹œ‰…ÉÉ¥•È…Ğ€¬Ğ´¨¨°ÁÕĞÑ¡•É”Ñ¼ÍÑ½ÀÑ¡”İ…±­•ÈÍÑÉ½±±¥¹œ¥¹Ñ¼Ñ¡”É¥Ù•È¸‰É¥‘”(€€€±•™Ğ½¸Ñ¡”Ñ•ÉÉ…¥¸…¹¡½ÈÑ¡•É•™½É”‘½•Ì¹½ĞÍ¥¹¬½ÕĞ½˜Í¥¡ĞƒŠP¥Ğ¡…¹Ì™½ÕÈµ•ÑÉ•Ì…‰½Ù”(€€€Ñ¡”İ…Ñ•È°İ¡¥ ¥ÌÑ¡”¡…É‘•È™…¥±ÕÉ”Ñ¼É•…°…¹¥Ğ¥Ìİ¡…ĞÑ¡”Íµ½­”¹½ÜÁ¥¹Ì¸(€€€€¨©e½Ô…¹¹½Ğİ…±¬…É½ÍÌ¥Ğ°…¹Ñ¡…Ğ¥ÌÍÑ…Ñ•É…Ñ¡•ÈÑ¡…¸™…­•¸¨¨Q¡”İ…±­•È™½±±½İÌÑ¡”(€€€Ñ•ÉÉ…¥¸°Í¼Ñ¡”‘•¬¥ÌÍ•¹•Éäå½ÔÁ…ÍÌÕ¹‘•ÈÉ…Ñ¡•ÈÑ¡…¸„É½ÕÑ”ì¥ÑÌ™½½ÑÁÉ¥¹Ğ¥Ì•á±Õ‘•(€€€™É½´Ñ¡”½±±¥Í¥½¸Á½±å½¹Ì°‰•…ÕÍ”ÑÉ•…Ñ¥¹œ„‘•¬…Ì„İ…±°İ½Õ±ÁÕĞ…¸¥¹Ù¥Í¥‰±”‰…ÉÉ¥•È(€€€…É½ÍÌÑ¡”É¥Ù•Èİ¥Ñ ¹½Ñ¡¥¹œÙ¥Í¥‰±”…Ğ¡•…¡•¥¡ĞÑ¼•áÁ±…¥¸¥Ğ¸İ…±­…‰±”‘•¬¹••‘ÌÑ¡”(€€€İ…±­•ÈÑ¼±•…É¸…‰½ÕĞÍÕÉ™…•Ì…‰½Ù”Ñ¡”É½Õ¹°İ¡¥ ¥Ì¥ÑÌ½İ¸Õ¹¥Ğ½˜İ½É¬¸((ÈÈ¸€¨©Q¡”‰É¥‘”…ÉÉ¥Ù•Ì¹½İ¡•É”°…¹Ñ¡”…Ñ”Ñ¡…ĞÍ…åÌÍ¼¥Ì¹•Ü¸¨¨Q¡É•”ÉÕ±•Ì¹½Ü…Í¬(€€€İ¡•Ñ¡•È„É•½É¥Ì¡½¹•ÍĞèÑ¡”½¹™¥‘•¹”µ½‘•°É…‘•Ìİ¡…Ğ„Ù…±Õ”±…¥µÌ°Ñ¡”±¥‰•ÉÑ¥•Ì(€€€½Ù•É…”¡•¬‘•µ…¹‘Ì…¸…‘µ¥ÍÍ¥½¸™½È…¹åÑ¡¥¹œ¥¹Ù•¹Ñ•°…¹Ñ¡”•½µ•ÑÉä‘•±…É…Ñ¥½¹Ì(€€€‘•µ…¹½¹”™½È…¹åÑ¡¥¹œÍÑ…Ñ•…¹¹½Ğ‰Õ¥±Ğ¸9½¹”½˜Ñ¡•´…¸Í•”„ÍÑÉÕÑÕÉ”Ñ¡…Ğİ…Ì(€€€‰Õ¥±Ğ™…¥Ñ¡™Õ±±ä½¹Ñ¼É½Õ¹Ñ¡…Ğ¥Ì¹½ĞÕ¹‘•É¹•…Ñ ¥Ğ°‰•…ÕÍ”€¨©¹½Ñ¡¥¹œ¥¸Ñ¡”É•½É¥Ì(€€€İÉ½¹œ¨¨¸Ù•Éä¹…µ”É•Í½±Ù•Ì°•Ù•ÉäÙ…±Õ”É•…¡•Ì„Ù•ÉÑ•à°•Ù•Éä½¹™¥‘•¹”¡¥À¥Ì•…É¹•°(€€€…¹Ñ¡”9½ÉÑ 	É…¹ ‰É¥‘”ÍÑ¥±°ÍÑ…¹‘Ì€È¸ĞÈ´±•…È½˜Ñ¡”Ñ•ÉÉ…¥¸…Ğ‰½Ñ ±…¹‘¥¹Ì¸(€€€¡•­}É½Õ¹‘}½¹Ñ…Ñ€±½Í•ÌÑ¡…Ğ‘¥É•Ñ¥½¸¸… …É¡•ÑåÁ”‘•±…É•Ìİ¡•É”¥ĞÑ½Õ¡•ÌÑ¡”(€€€É½Õ¹ƒŠPÁ•É¥µ•Ñ•É€™½È„‰Õ¥±‘¥¹œ€¡Ñ¡”™½½ÑÁÉ¥¹Ğ½ÕÑ±¥¹”°…ĞÑ¡”‰…Í”½˜Ñ¡”İ…±±Ì¤…¹(€€€•¹‘Í€™½È„É½ÍÍ¥¹œ€¡Ñ¡”Ñİ¼•¹•‘•Ì°…Ğ‘•¬¡•¥¡Ğ¤ƒŠP…¹Ù…±¥‘…Ñ”¹Áå€µ•…ÍÕÉ•ÌÑ¡…Ğ(€€€½ÕÑ±¥¹”……¥¹ÍĞÑ¡”½µµ¥ÑÑ•¡•¥¡Ñ™¥•±Ñ¡É½Õ Ñ½½±Ì½¡•¥¡Ñ™¥•±¹Áå€¸€¨©Q¡”Ñ½±•É…¹”¥Ì(€€€¹½Ğ„¹•Ü¹Õµ‰•Èè¥Ğ¥ÌÑ¡”İ…±­•ÈÌ€À¸ÌÔ´ÍÑ•ÀµÕÀÉÕ±”¨¨°‰•…ÕÍ”Ñ¡”ÅÕ•ÍÑ¥½¸Ñ¡”…Ñ”(€€€…Í­Ì¥Ì±¥Ñ•É…±±äÑ¡”İ…±­•ÈÌÅÕ•ÍÑ¥½¸°…¹„ÍÑÉÕÑÕÉ”„Ù¥Í¥Ñ½È½Õ±¹½ĞÍÑ•À½¹Ñ¼¡…Ì(€€€¹½Ğµ•ĞÑ¡”É½Õ¹¸(€€€€¨©]¡…Ğ¥Ğ™½Õ¹¥ÌÑ¡”½¹±äÑ¡¥¹œ¥Ğ™½Õ¹°…¹Ñ¡…Ğ¥Ìİ½ÉÑ ÍÑ…Ñ¥¹œÑ½¼¸¨¨Q¡”Í¥à(€€€‰Õ¥±‘¥¹Ì±…¹èÑ¡•¥Èİ½ÉÍĞ½É¹•ÈÍ¥ÑÌ€À¸ÄØ´½™˜€¡Ñ¡”]½±˜A½¥¹ĞQ…Ù•É¸°½Ù•ÈÑ¡”‰…¹¬(€€€™…±°¤°İ•±°¥¹Í¥‘”„ÍÑ•À¸Q¡”‰É¥‘”‘½•Ì¹½Ğ°…¹…¹¹½Ğİ¥Ñ Ñ¡”‘…Ñ„…Ì¥ĞÍÑ…¹‘ÌƒŠPÑ¡”(€€€‘•¬Í¥ÑÌ…Ğ€È¸ÈÈ´€¡±•…Ù•ÈÌ¥¹™•ÉÉ•Í¥àµ™½½Ğ±•…É…¹”Á±ÕÌÑ¡”ÍÑÉ¥¹•È…¹Á±…¹¬‘•ÁÑ (€€€Õ¹‘•È¥Ğ¤…¹Ñ¡”¡¥¡•ÍĞ±…¹…¹åİ¡•É”¥¸Ñ¡”€ØĞÀ´‰½à¥Ì€Ä¸ÌÄ´°Í¼Ñ¡•É”¥Ì¹¼É½Õ¹¥¸(€€€Ñ¡¥Ì•Á½ ™½È¥ĞÑ¼…ÉÉ¥Ù”…Ğ¸Q¡”É•½É‘•±…É•ÌÉ½Õ¹‘}½¹Ñ…Ğè…ÁÁÉ½…¡}¹½Ñ}µ½‘•±±•‘€(€€€…¹0ÌÀ…‘µ¥ÑÌ¥ĞìÑ¡”Á½ÁÕÀÍ¡½İÌÑ¡”¡¥À½¸Ñ¡”‰Õ¥±‘¥¹œ‰•¥¹œ¥¹ÍÁ•Ñ•°Í¼Ñ¡”(€€€…‘µ¥ÍÍ¥½¸É•…¡•Ì„Ù¥Í¥Ñ½È…¹¹½Ğ½¹±ä„É•Ù¥•İ•È¸(€€€€¨©Q¡”…ÁÁÉ½… ¥Ì¹½Ğµ½‘•±±•‰•…ÕÍ”¹½Ñ¡¥¹œ‘•ÍÉ¥‰•Ì½¹”¸¨¨¹‘É•…Ì¥Ù•ÌÑ¡”ÍÑÉ¥¹•ÉÌ°(€€€±•…Ù•È¥Ù•ÌÑ¡”İ¥‘Ñ …¹Ñ¡”±½œ…‰ÕÑµ•¹ÑÌ€‰¥¸Ñ¡”Í¡…±±½Üİ…Ñ•È¹•…ÈÑ¡”‰…¹­Ìˆ°…¹¹¼(€€€Í½ÕÉ”É•…¡•Í…åÌ¡½Ü„Á•ÉÍ½¸½È„Ñ•…´½Ğ™É½´Ñ¡”‰…¹¬½¹Ñ¼Ñ¡”‘•¬¸¸•µ‰…¹­µ•¹Ğ(€€€İ½Õ±‰”„Í•½¹¥¹Ù•¹Ñ¥½¸ÍÑ…­•½¸Ñ¡”±•…É…¹”™¥ÕÉ”ƒŠPİ¡¥ ¥Ì¥ÑÍ•±˜½¹±ä(€€€¥¹™•ÉÉ•‘€…¹Õ¹Í½ÕÉ•¥¸Ñ¡”‘½ÍÍ¥•ÈÑ¡…ĞÍÕÁÁ±¥•¥ĞƒŠP…¹Õ¹±¥­”0ÈäÌ™¥™Ñ••¸É¥‰Ì¥Ğ(€€€¥ÌÑ¡”¥¹Ù•¹Ñ¥½¸„Ù¥Í¥Ñ½Èİ½Õ±İ…±¬½Ù•ÈÉ…Ñ¡•ÈÑ¡…¸±½½¬…Ğ¸(€€€€¨©Íµ…±±•ÈÑ¡¥¹œ…µ”½ÕĞ½˜İÉ¥Ñ¥¹œ¥Ğ°…¹¥Ğ¥Ì„İ…É¹¥¹œ…‰½ÕĞÑ¡”ÍÑ…±•¹•ÍÌ¡…Í ¸¨¨(€€€Q¡”½¹Ñ…Ğ¡•¥¡Ğİ…Ì™¥ÉÍĞİÉ¥ÑÑ•¸…Ì„ÁÉ½Á•ÉÑå€½¸	É¥‘•Q¥µ‰•ÉA…É…µÍ€°…¹(€€€µ•Í¡}¥¹ÁÕÑÌ¹Áå€¡…Í¡•Ì•Ù•ÉäÁÉ½Á•ÉÑä„Á…É…µ•Ñ•È±…ÍÌ‘•É¥Ù•ÌƒŠPÍ¼„¹Õµ‰•È¹¼‰Õ¥±‘•È(€€€É•…‘Ì¥µµ•‘¥…Ñ•±äÉ”µÍÑ…±•Ñ¡”‰É¥‘”¸Q¡…Ğ¥Ì•á…Ñ±äÑ¡”™…±Í”Á½Í¥Ñ¥Ù”ƒ
œ€ÄÔÉ•İÉ½Ñ”Ñ¡”(€€€¡…Í Ñ¼•¹°…ÉÉ¥Ù¥¹œ™É½´„¹•Ü‘¥É•Ñ¥½¸èÑ¡”ÉÕ±”€‰„‘•É¥Ù•ÁÉ½Á•ÉÑä¥Ì„µ•Í ¥¹ÁÕĞˆ¥Ì(€€€É¥¡Ğ…‰½ÕĞ½¹ÍÑ…¹ÑÌ…¹İÉ½¹œ…‰½ÕĞ…•ÍÍ½ÉÌ¸%Ğ¥Ì„µ½‘Õ±”µ±•Ù•°(€€€É½Õ¹‘}½¹Ñ…Ñ}è¡Á…É…µÌ¥€¥¹ÍÑ•…°…¹Ñ¡”‘½ÍÑÉ¥¹œÍ…åÌİ¡äÍ¼Ñ¡”¹•áĞ½¹”‘½•Ì¹½Ğ(€€€É•‘¥Í½Ù•È¥Ğ¸(€€€€¨©]¡…Ğ¥ĞÍÑ¥±°…¹¹½ĞÍ•”¨¨¥Ì„ÍÑÉÕÑÕÉ”ÍÑ…¹‘¥¹œ½¸É½Õ¹Ñ¡…Ğ•á¥ÍÑÌ…¹¥ÌİÉ½¹œƒŠP(€€€Ñ¡”¡•¬½µÁ…É•Ì„µ•Í ……¥¹ÍĞÑ¡”¡•¥¡Ñ™¥•±°…¹‰½Ñ …¸…É•”½¸„ÍÕÉ™…”¹¼(€€€Í½ÕÉ”ÍÕÁÁ½ÉÑÌ¸((ÈÌ¸€¨©½ÕÈ…ÑÑÉ¥‰ÕÑ•Ì½˜Ñ¡”‰É¥‘”…É”¹½Ü‰•¡¥¹Ñ¡•¥È•Ù¥‘•¹”°…¹Ñ¡”•Ù¥‘•¹”İ…Ì„(€€€™½½Ñ¹½Ñ”Õ¹‘•È„Á…É…É…Á Ñ¡¥ÌÁÉ½©•Ğ¡…ÌÅÕ½Ñ•™½Èİ••­Ì¸¨¨Q¡”É•½ÉÌ½İ¸µ•µ¼±¥ÍÑ•(€€€™½ÕÈ½Á•¸Ñ¡É•…‘Ì½¸€ÈÀÈØ´Àà´ÄÀìÑİ¼İ•É”ÁÕ±±•Ñ¡”Í…µ”‘…ä…¹½¹”½˜Ñ¡•´Á…¥™½È(€€€•Ù•ÉåÑ¡¥¹œ¸€¨©¹‘É•…ÌÁÉ¥¹ÑÌ°…ĞÑ¡”™½½Ğ½˜ÁÀ¸€ØÌÄ´ØÌÈ°„ÍÑ…Ñ•µ•¹ĞÍ¥¹•‰ä™½ÕÈµ•¸İ¡¼(€€€ÕÍ•Ñ¡”‰É…¹ ‰É¥‘•Ì¨¨ƒŠP(¸¸…Ñ½¸°)½¡¸	…Ñ•Ì°¡…É±•Ì±•…Ù•È…¹)½¡¸9½‰±”°…É••(€€€…Ğ„µ••Ñ¥¹œ½˜½±Í•ÑÑ±•ÉÌ±…Ñ”¥¸Ñ¡”™…±°½˜€ÄààÌ…¹¡…¹‘•Ñ¼Ñ¡”•‘¥Ñ½ÉÌ‰ä	…Ñ•Ì¸(€€€%Ğ¥ÌÑ¡”½¹±ä‘•ÍÉ¥ÁÑ¥½¸…¹å‰½‘äİÉ½Ñ”½˜¡½ÜÑ¡•Í”É½ÍÍ¥¹Ìİ•É”ÁÕĞÑ½•Ñ¡•Èè(€€€…‰ÕÑµ•¹ÑÌ½˜±½Ì¥¸Ñ¡”Í¡…±±½Üİ…Ñ•È¹•…ÈÑ¡”‰…¹­Ì°€¨©Ñİ¼€‰‰•¹ÑÌˆ½˜™½ÕÈ¡•…Ùä±½Ì(€€€É•ÍÑ¥¹œ½¸Ñ¡”‰½ÑÑ½´¥¸‘••Á•Èİ…Ñ•È¨¨°ÍÑÉ¥¹•ÉÌ½˜¡•…Ùä±½Ì™É½´Ñ¡”…‰ÕÑµ•¹ÑÌÑ¼Ñ¡”(€€€‰•¹ÑÌ…¹‰•Ñİ••¸Ñ¡•´°€¨©ÁÕ¹¡•½¹Ì½ÈÍÁ±¥Ğ±½Ì™½È„™±½½È¨¨°…‰½ÕĞÑ•¸™••Ğİ¥‘”°(€€€€¨©İ¥Ñ¡½ÕĞÉ…¥±¥¹Ì™½ÈÑ¡”™¥ÉÍĞ™•Üå•…ÉÌ°…™Ñ•Èİ¡¥ Õ…É‘Ì½ÈÉ…¥±¥¹Ìİ•É”…‘‘•¨¨°…¹(€€€€¨©…‰½ÕĞÍ¥à™••Ğ…‰½Ù”Ñ¡”İ…Ñ•È°€‰Í¼Ñ¡…ĞÑ•…µÌÁ…ÍÍ•Õ¹‘•ÈÑ¡•´½¸Ñ¡”¥”™É••±ä¸ˆ¨¨(€€€M½ÕÉ”É•½Éè½±‘}Í•ÑÑ±•ÉÍ}‰É¥‘•Í|ÄààÍ€°Ñ¥•È€È¸(€€€€¨©]¡…Ğ¥Ğ½ÉÉ•ÑÌ°…¹¹½¹”½˜¥Ğ¥Ì½ÉÉ•Ñ•å•Ğ¸¨¨Á¥•É}ÍÁ…¥¹}µ€ÁÕÑÌ™¥™Ñ••¸É¥‰Ì¥¸(€€€Ñ¡”É¥Ù•È½¸Ñ¡”…É¡•ÑåÁ”Ì‘•™…Õ±ĞìÑ¡”±•ÑÑ•ÈÍ…åÌÑİ¼‰•¹ÑÌ¸Á¥•É}­¥¹‘€¥ÌÉ¥‰€°…¹(€€€Ñ¡¥ÌÉ•½É…ÉÕ•¥ÑÌİ…äÑ¡•É”‰äÑÉ•…Ñ¥¹œÑ¡”-¥¹é¥”MÑÉ••ĞÁ…”ÌÑåÁ”µİ½É€‰	•¹Ğˆ…Ì(€€€µ½‘•É¸•‘¥Ñ½É¥…°±…ÍÍ¥™¥…Ñ¥½¸ƒŠP¥Ğ¥ÌÑ¡”Í•ÑÑ±•ÉÌœ½İ¸İ½É°…¹±•…Ù•È°Ñ¡”•å•İ¥Ñ¹•ÍÌ(€€€Ñ¡…Ğ…ÉÕµ•¹Ğ±•…¹•½¸°Í¥¹•¥Ğ¸±•…É…¹•}µ€İ…Ì‘•µ½Ñ•Ñ¼¥¹™•ÉÉ•‘€¡•É”™½Èİ…¹Ğ½˜(€€€„Á…”ìÑ¡”Á…”•á¥ÍÑÌ°…¹Ñ¡”‘½ÍÍ¥•ÈÌm=u€Ñ…œİ…ÌÉ¥¡Ğ¸Q¡”‘•¬¥ÌÑ¡”…É¡•ÑåÁ”Ì(€€€…¹Ñ¡”±•ÑÑ•ÈÍÑ…Ñ•Ì¥Ğ¸€¨©Ù•Éä½¹”½˜Ñ¡½Í”¥Ì„µ•Í ¥¹ÁÕĞ¨¨°Í¼Ñ¡”É•½É…¹¹½Ğµ½Ù”(€€€İ¥Ñ¡½ÕĞÑ¡”1µ½Ù¥¹œİ¥Ñ ¥Ğ°…¹Ñ¡¥Ì½µµ¥Ğ‘•±¥‰•É…Ñ•±ä¡…¹•Ì¹¼Ù…±Õ”…¹¹¼(€€€½¹™¥‘•¹”Ñ…œè¥Ğ±…¹‘ÌÑ¡”Í½ÕÉ”°Ñ¡”µ•µ¼°Ñ¡”±¥‰•ÉÑ¥•ÌÕÁ‘…Ñ•Ì…¹Ñ¡”¹½Ñ•ÌÑ¡…ĞÍ…ä(€€€½¸•… …ÑÑÉ¥‰ÕÑ”Ì½İ¸™…”Ñ¡…Ğ¥Ğ¥Ì‰•¡¥¹¥ÑÌ•Ù¥‘•¹”¸€¨©Q¡”É•Á…¥È…¹¥ÑÌ‰…­”…É”(€€€½¹”Í±¥”…¹¥Ğ¥ÌÑ¡”¹•áĞ½¹”¸¨¨€¡%Ğİ…Ì°…¹¥Ğ±…¹‘•Ñ¡”Í…µ”‘…äƒŠPƒ
œ€ÈĞ¸¤(€€€€¨©Q¡”İ½É¬½É‘•È¨¨°Í¼Ñ¡”¹•áĞÍ±¥”‘½•Ì¹½Ğ¡…Ù”Ñ¼É”µ‘•É¥Ù”¥Ğè‰É¥‘•}Ñ¥µ‰•É€‰Õ¥±‘Ì(€€€¥¹Ñ•Éµ•‘¥…Ñ”ÍÕÁÁ½ÉÑÌ™É½´„ÍÁ…¥¹œ°…¹Ñ¡”•Ù¥‘•¹”¥Ì„½Õ¹Ğ…¹„™½É´°¹½Ğ„ÍÁ…¥¹œƒŠP(€€€Ñİ¼‰•¹ÑÌ…ĞÑ¡”Ñ¡¥É‘Ì½˜„€ÜÄ¸àÌ´ÍÁ…¸¥Ì„‘¥™™•É•¹ĞÁ…É…µ•Ñ•É¥Í…Ñ¥½¸°¹½Ğ„‘¥™™•É•¹Ğ(€€€¹Õµ‰•È°Í¼Ñ¡”…É¡•ÑåÁ”¡…¹•Ì‰•™½É”Ñ¡”É•½É‘½•Ì¸Á¥•É}­¥¹‘€İ…¹ÑÌ„‰•¹Ñ€Ù…±Õ”(€€€€¡™½ÕÈ¡•…Ùä±½ÌÍÑ…¹‘¥¹œ½¸Ñ¡”‰½ÑÑ½´¤‰•Í¥‘”É¥‰€¸±•…É…¹•}µ€µ½Ù•ÌÑ¼‘½Õµ•¹Ñ•‘€(€€€İ¥Ñ Ñ¡¥ÌÍ½ÕÉ”¸É…¥±¥¹€ÍÑ…åÌ™…±Í•€…¹¥ÑÌ¹½Ñ”¡…¹•Ì™É½´…¸…ÉÕµ•¹Ğ™É½´Í¥±•¹”(€€€Ñ¼„É•…‘¥¹œ½˜€‰Ñ¡”™¥ÉÍĞ™•Üå•…ÉÌˆ¸0Èäµ½Ù•ÌÑ¼€¨©I•Í½±Ù•¨¨İ¡•¸Ñ¡”µ•Í Í¡½İÌÑİ¼(€€€ÍÕÁÁ½ÉÑÌ°…¹¹½Ğ‰•™½É”¸(€€€€¨©Qİ¼¹•…Ñ¥Ù”™¥¹‘¥¹Ì…µ”İ¥Ñ ¥Ğ°…¹Ñ¡•ä½ÍĞ…ÌµÕ Ñ¼•ÍÑ…‰±¥Í …ÌÑ¡”Á½Í¥Ñ¥Ù”(€€€½¹”¸¨¨9•¥Ñ¡•È€ÄàÌĞÍ¡••Ğ‘É…İÌÑ¡¥Ì‰É¥‘”¸	½Ñ İ•É”¥¹ÍÁ•Ñ•…ĞÑ¡”É½ÍÍ¥¹œÌ½İ¸™¥ÑÑ•(€€€Á¥á•°É…Ñ¡•ÈÑ¡…¸‰ä•å”ƒŠP¥¹Ù•ÉĞ•… Í¡••ĞÌ½µµ¥ÑÑ•@…™™¥¹”…ĞÑ¡”É•½ÉÌ‘•¬±¥¹”°(€€€™•Ñ Ñ¡…Ğ%%%É•¥½¸ƒŠP…¹½¸‰½Ñ °Ñ¡”ÍÑÉ••ĞÍÑ½ÁÌ…ĞÑ¡”İ…Ñ•É±¥¹”è„Á±…ÑÑ•ÍÑÉ••Ğ¥Ì„(€€€‘•‘¥…Ñ¥½¸°¹½Ğ„ÍÑÉÕÑÕÉ”¸Q¡”Ñ¡É•…Ñ¡”µ•µ¼É…Ñ•µ½ÍĞÁÉ½µ¥Í¥¹œ°€‰Ñ¡”€ÄàÌĞ¼ÄàÌÔ]…‰…¹Í¥„(€€€…¹-¥¹é¥”Ì‘‘¥Ñ¥½¸Á±…Ğˆ°ÑÕÉ¹Ì½ÕĞÑ¼‰”¡…Ñ¡…İ…å|ÄàÌÑ€°„Í¡••Ğ…±É•…‘ä¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ(€€€…¹…±É•…‘ä•½É•™•É•¹•°İ¡¥ ¥Ì¥ÑÌ½İ¸Íµ…±°±•ÍÍ½¸…‰½ÕĞ½Á•¸µÑ¡É•…±¥ÍÑÌ¸¹½¸(€€€!…Ñ¡…İ…ä„¡…Ñ¡•°±…‘‘•Èµ±¥­”µ…É¬Í¥ÑÌ¥¸Ñ¡”¡…¹¹•°İ¥Ñ¡¥¸€ÌÔ´½˜Ñ¡”É½ÍÍ¥¹œ…¹É•…‘Ì(€€€½¹Ù¥¹¥¹±ä…Ì„Á±…¹¬µ…¹µÍÑÉ¥¹•È‰É¥‘”Íåµ‰½°…Ğµ½‘•É…Ñ”é½½´ì…Ğ™Õ±°É•Í½±ÕÑ¥½¸¥Ğ¥Ì(€€€Ñ¡”±•ÑÑ•È€¨© ¨¨½˜€‰	I9 ˆ°±•ÑÑ•É•‘½İ¸Ñ¡”İ…Ñ•È¸%Ğ¥ÌİÉ¥ÑÑ•¸‘½İ¸¡•É”Í¼Ñ¡…Ğ¥Ğ¥Ì(€€€™½Õ¹½¹”É…Ñ¡•ÈÑ¡…¸‘¥Í½Ù•É•Ñİ¥”¸((ÈĞ¸€¨©%aƒŠPÑİ¼‰•¹ÑÌ°¹½Ğ™¥™Ñ••¸É¥‰Ì°…¹Ñ¡”É•Á…¥È¡…¹•„Á…É…µ•Ñ•ÈÉ…Ñ¡•ÈÑ¡…¸„(€€€¹Õµ‰•È¸¨¨ƒ
œ€ÈÌÌİ½É¬½É‘•È±…¹‘•Ñ¡”Í…µ”‘…ä¥Ğİ…ÌİÉ¥ÑÑ•¸°É•½É…¹…É¡•ÑåÁ”…¹‰…­”(€€€¥¸½¹”½µµ¥Ğ¸Á¥•É}ÍÁ…¥¹}µ€¥Ì½¹”™É½´‰É¥‘•}Ñ¥µ‰•É€…¹™É½´Ñ¡”É•½Éì(€€€Á¥•É}½Õ¹Ğè€É€€¡‘½Õµ•¹Ñ•‘€¤É•Á±…•Ì¥Ğ°Á¥•É}­¥¹‘€¥Ì‰•¹Ñ€°±•…É…¹•}µ€¥ÌÁÉ½µ½Ñ•(€€€Ñ¼‘½Õµ•¹Ñ•‘€½¸Ñ¡”€ÄààÌÍÑ…Ñ•µ•¹Ğ°…¹Ñ¡”™±½½ÈÑ¡”…É¡•ÑåÁ”¡…‰••¸ÍÕÁÁ±å¥¹œ¥¸(€€€Í¥±•¹”¥ÌÍÑ…Ñ•…Ì‘•­}­¥¹èÁÕ¹¡•½¹€¸Q¡”É¥Ù•È…ÉÉ¥•ÌÑ¡É•”ÍÁ…¹Ìİ¡•É”¥Ğ…ÉÉ¥•(€€€Í¥áÑ••¸¸(€€€€¨©Q¡”Á…É…µ•Ñ•Èİ…ÌÑ¡”™…Õ±Ğ°¹½ĞÑ¡”Ù…±Õ”¸¨¨¸…É¡•ÑåÁ”Ñ¡…Ğ‘¥Ù¥‘•Ì„ÍÁ…¸‰ä„ÍÁ…¥¹œ(€€€…¸½¹±ä•Ù•ÈÁÉ½‘Õ”„½±½¹¹…‘”°…¹„ÍÁ…¥¹œ¥Ì„‰Õ¥±‘•ÈÌ½¹Ù•¹¥•¹”Ñ¡…Ğ¹¼İ¥Ñ¹•ÍÌ(€€€İ½Õ±•Ù•ÈÉ•½É¸]¡…Ğ„µ…¸İ¡¼‘É½Ù”„Ñ•…´…É½ÍÌ„‰É¥‘”É•µ•µ‰•ÉÌ¥Ì€©¡½Üµ…¹ä¨ÍÑ½½(€€€¥¸Ñ¡”İ…Ñ•È…¹€©İ¡…ĞÑ¡•äİ•É”µ…‘”½˜¨ƒŠPÍ¼Ñ¡”¥¹ÁÕĞ¥Ì¹½Ü„½Õ¹Ğ…¹„™½É´°…¹Ñ¡”(€€€ÍÁ…¥¹œÍÕÉÙ¥Ù•Ì½¹±ä…ÌA%I}MA%9}11	-}5€°Ñ¡”Ñ¡¥¹œ„‰É¥‘”™…±±Ì‰…¬Ñ¼İ¡•¸(€€€¹½‰½‘ä‘•ÍÉ¥‰•¥ÑÌµ¥‘‘±”¸¡…¹¥¹œ€Ğ¸ÔÑ¼€ÈÌ¸äĞİ½Õ±¡…Ù”™¥á•Ñ¡¥Ì‰É¥‘”…¹±•™ĞÑ¡”(€€€¹•áĞ½¹”Ñ¼‰”™½Õ¹‰äÑ¡”Í…µ”…¥‘•¹Ğ¸(€€€€¨©]¡…ĞÑ¡”½¹™¥‘•¹”Ù¥•Ü¹½ÜÍ…åÌ°…¹¥ĞÍ…åÌµ½É”Ñ¡…¸¥Ğ‘¥¸¨¨±•…É…¹•}µ€¥Ì½¹”½˜(€€€Ñ¡”…ÑÑÉ¥‰ÕÑ•ÌÑ¡…ĞÍ…åÌİ¡…ĞÑ¡¥ÌÍÑÉÕÑÕÉ”]L€¡„‰É¥‘”Ì‘½Õµ•¹Ñ•‘•ÍÉ¥ÁÑ¥½¸€©¥Ì¨(€€€‘¥µ•¹Í¥½¹…°ƒŠPÍ•”‰É¥‘•}Ñ¥µ‰•É}Á…É…µÍ€¤°Í¼ÁÉ½µ½Ñ¥¹œ¥ĞÑ…­•ÌÑ¡”‘•¬…¹Ñ¡”ÍÑÉ¥¹•ÉÌ(€€€½ÕĞ½˜Ñ¡”¡…±˜µ‘¥Ñ¡•É•ÍÑ…Ñ”Ñ¡”¥¹™•ÉÉ•‘€Ñ…œÁÕĞÑ¡•´¥¸°…¹Ñ¡”‰•¹ÑÌ½µ”½ÕĞÍ½±¥(€€€‰•…ÕÍ”‰½Ñ Ñ¡•¥È½Õ¹Ğ…¹Ñ¡•¥È™½É´…É”…ÑÑ•ÍÑ•¸Q¡…Ğ¥ÌÑ¡”™¥ÉÍĞÑ¥µ”¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ(€€€Ñ¡…Ğ•Ù¥‘•¹”¡…Ìµ…‘”Í½µ•Ñ¡¥¹œ€©±•ÍÌ¨‘¥Ñ¡•É•¸(€€€€¨©¹İ¡…Ğ¥ĞÍÑ¥±°…¹¹½ĞÍ…ä¥Ìİ¡•É”Ñ¡•äÍÑ½½¸¨¨Q¡”±•ÑÑ•È±½…Ñ•ÌÑ¡”‰•¹ÑÌ‰ä‘•ÁÑ ƒŠP(€€€€‰É•ÍÑ¥¹œ½¸Ñ¡”‰½ÑÑ½´°¥¸‘••Á•Èİ…Ñ•ÈˆƒŠPİ¡¥ ¥Ì„±½…Ñ½ÈÑ¡¥ÌÁÉ½©•Ğ…¹¹½ĞÕÍ”è¹¼(€€€Í½ÕÉ”¥Ù•ÌÑ¡”¡…¹¹•°Ì‰•ÁÉ½™¥±”…¹¹½Ñ¡¥¹œ‰•±½ÜÑ¡”İ…Ñ•É±¥¹”¥Ìµ½‘•±±•¸Q¡•ä…É”(€€€‰Õ¥±Ğ…ĞÑ¡”Ñ¡¥ÉÁ½¥¹ÑÌ‰•…ÕÍ”Ñ¡…Ğ¥Ìİ¡…Ğ„‰Õ¥±‘•Èİ½Õ±‘¼İ¥Ñ Ñ¡É•”É½Õ¡±ä•ÅÕ…°(€€€ÉÕ¹Ì¸M¼Ñ¡”¡¥À½¸Á¥•É}½Õ¹Ñ€É…‘•Ì¡½Üµ…¹ä…¹„Ù¥Í¥Ñ½ÈÍ••Ì•á…Ñ±äİ¡•É”°İ¡¥ ¥Ì(€€€Ñ¡”¡¥µ¹•åÍ€Í¥ÑÕ…Ñ¥½¸½˜ƒ
œ€Ää…ÉÉ¥Ù¥¹œ…Ğ„‘¥™™•É•¹ĞÍÑÉÕÑÕÉ”¸€¨©0ÌÄ¨¨¥Ìİ¡•É”¥Ğ¥Ì(€€€…‘µ¥ÑÑ•°…¹¥Ğ…ÉÉ¥•Ì„Í•½¹½µ¥ÍÍ¥½¸Ñ¡”É•Á…¥ÈÉ•…Ñ•èÑ¡É•”ÍÁ…¹Ìµ…­”•… ÍÑÉ¥¹•È(€€€ÉÕ¸€ÈÌ¸ä´°±½¹•ÈÑ¡…¸…¹äÑ¥µ‰•È…¹å‰½‘äİ…Ìµ½Ù¥¹œ°Í¼Ñ¡½Í”ÉÕ¹Ìİ•É”ÍÁ±¥•Í½µ•İ¡•É”(€€€…¹¹½Ñ¡¥¹œÍ…åÌİ¡•É”¸Q¡”µ•Í Í¡½İÌ½¹”±½œÁ•È‰…ä¸€¨©0Èäµ½Ù•ÌÑ¼I•Í½±Ù•¨¨ƒŠP…¹½¹±ä(€€€¹½Ü°‰•…ÕÍ”Ñ¡”•¹ÑÉä¥ÑÍ•±˜Í…¥¥Ğİ½Õ±ÍÑ…äÕ¹Ñ¥°Ñ¡”µ•Í Í¡½İ•Ñİ¼ÍÕÁÁ½ÉÑÌ¸(€€€€¨©=¹”±¥µ¥Ğ½˜Ñ¡”µ•Í ¥Ìİ½ÉÑ ÍÑ…Ñ¥¹œ½¸¥ÑÌ½İ¸¨¨°‰•…ÕÍ”¥Ğ¥ÌÑ¡”µ½ÍĞÍÁ•¥™¥ŒÁ¡É…Í”(€€€¥¸Ñ¡”Í½ÕÉ”¸€©I•ÍÑ¥¹œ½¸Ñ¡”‰½ÑÑ½´¨¥Ìİ¡…Ğ‘¥ÍÑ¥¹Õ¥Í¡•Ì„‰•¹Ğ™É½´„‘É¥Ù•¸Á¥±”‰•¹Ğ°(€€€…¹…‰½Ù”Ñ¡”İ…Ñ•É±¥¹”Ñ¡”Ñİ¼…É”Ñ¡”Í…µ”Á¥ÑÕÉ”ì}±½}‰•¹Ñ€‘¥™™•ÉÌ™É½´}Á¥±•}‰•¹Ñ€‰ä(€€€™½ÕÈ¡•…Ùä±½Ì……¥¹ÍĞÑ¡É•”±¥¡Ğ½¹•Ì°İ¡¥ ¥Ìİ¡…Ğ„Ù¥Í¥Ñ½È…¸…ÑÕ…±±äÍ•”¸Q¡”É•ÍĞ(€€€½˜Ñ¡”‘¥ÍÑ¥¹Ñ¥½¸±¥Ù•Ì¥¸Ñ¡”É•½É…¹¥¸Ñ¡¥Ì™¥±”¸((ÈÔ¸€¨©Q¡”™¥ÉÍĞ‰Õ¥±‘¥¹œİ¡½Í”™½½ÑÁÉ¥¹Ğ¥Ì•Ù¥‘•¹”°…¹„½ÉÉ•Ñ¥½¸Ñ¼½ÕÈ½İ¸‘½ÍÍ¥•ÈÑ¡…Ğ(€€€¡…¹•Ìİ¡…Ğ¥Ğ¥Ì¸¨¨¡½…¹}ÍÑ½É•€ƒŠPÑ¡”±½œÍÑ½É”…ĞÑ¡”İ•ÍĞ•¹½˜Ñ¡”1…­”MÑÉ••Ğ‰±½¬(€€€¥¸İ¡¥ Ñ¡”U¹¥Ñ•MÑ…Ñ•Ì½Á•¹•„Á½ÍĞ½™™¥”…Ğ¡¥…¼½¸€ÌÄ5…É €ÄàÌÄƒŠP¥ÌÑ¡”•¥¡Ñ (€€€ÍÑÉÕÑÕÉ”…¹Ñ¡”™¥ÉÍĞ	U%1%9¡•É”İ¡½Í”½ÕÑ±¥¹”¥Ì¹½Ğ„Á±…•¡½±‘•È¸¹‘É•…Ì¥Ù•Ì¥ÑÌ(€€€Í¥é”Ñİ¥”°¥¸Ñİ¼¥¹‘•Á•¹‘•¹Ñ±äİÉ¥ÑÑ•¸Á…ÍÍ…•Ìè€‰Q¡”‰Õ¥±‘¥¹œİ…ÌÑİ•¹Ñä‰ä™½ÉÑäµ™¥Ù”™••Ğ(€€€¥¸Í¥é”°İ…ÌÁ…ÉÑ¥Ñ¥½¹•½™˜Í¼…ÌÑ¼Í•ÉÙ”…Ì„Á½ÍĞµ½™™¥”½¸½¹”Í¥‘”°…¹…ÌÑ¡”ÍÑ½É”½˜(€€€	É•İÍÑ•È°!½…¸€˜¼¸°½¸Ñ¡”½Ñ¡•Èˆ°…¹€‰Ñ¡”ÍÑ½É”½¹±ä½ÕÁ¥•…¸…É•„½˜™½ÉÑäµ™¥Ù”‰ä(€€€Ñİ•¹Ñä™••Ğˆ¸€ĞÔƒ\€ÈÀ™Ğ¥Ì€ÄÌ¸ÜÄØƒ\€Ø¸ÀäØ´…¹Ñ¡”™½½ÑÁÉ¥¹Ğ¥ÌÑ…•‘½Õµ•¹Ñ•‘€°İ¡¥ (€€€¹¼‰Õ¥±‘¥¹œ™½½ÑÁÉ¥¹Ğ¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ¡…Ì‰••¸‰•™½É”¸€¨©]¡…Ğ¥Ì‘½Õµ•¹Ñ•¥ÌÑ¡”M%i…¹(€€€¹½ĞÑ¡”Á±…¸¨¨èİ¡¥ …á¥ÌÉÕ¹Ì…±½¹œÑ¡”ÍÑÉ••Ğ¥Ì¹½‰½‘äÌ•Ù¥‘•¹”°Í¼Ñ¡…Ğ…ÍÍ¥¹µ•¹ĞÍ¥ÑÌ(€€€½¸Ñ¡”™……‘”‰•…É¥¹œ¥¸Ñ¡”Á½Í¥Ñ¥½¸¹½Ñ”°İ¡•É”É½Ñ…Ñ¥¹œÑ¡”‰Õ¥±‘¥¹œ¥Ìİ¡…Ğ¡…¹•Ì¥Ğ¸(€€€€¨©Q¡¥Ì¥Ì…±Í¼Ñ¡”™¥ÉÍĞÉ•½É¡•É”İ¥Ñ ¹½Ñ¡¥¹œ½¹©•ÑÕÉ…°¥¸¥Ğ¨¨°İ¡¥ ¥Ì¹½Ğ„‰½…ÍĞƒŠP(€€€¥Ğµ•…¹Ì¥ÑÌ…ÁÌ…É”…ÁÌ¥¸Ñ¡”Í½ÕÉ•ÌœÁÉ•¥Í¥½¸É…Ñ¡•ÈÑ¡…¸¡½±•Ì™¥±±•‰ä¥¹Ù•¹Ñ¥½¸¸(€€€%Ğ‘½•Ìµ•…¸Ñ¡”Á½ÁÕÀÌ•µÁÑä€‰]¡…Ğİ”µ…‘”ÕÀ¡•É”ˆÍÑ…Ñ”¥Ì™¥¹…±±ä•á•É¥Í•‰äÉ•…°‘…Ñ„°(€€€İ¡¥ ƒ
œ€ÄÄÉ•½É‘•…ÌÕ¹•á•É¥Í•¸(€€€€¨©Q¡”½ÉÉ•Ñ¥½¸¥ÌÑ¡”µ½É”ÕÍ•™Õ°¡…±˜¸¨¨‘½Ì½É•Í•…É ¼ÀÌµÍÑÉÕÑÕÉ•Ìµ¹½ÉÑ ¹µ‘€ƒ
œ€Ğ‘…Ñ•Ì(€€€Ñ¡”Á½ÍĞ½™™¥”Ìµ½Ù”Ñ¼Ñ¡”É…¹­±¥¸…¹M½ÕÑ ]…Ñ•È…‘‘É•ÍÌ™É½´€È9½Ù•µ‰•È€ÄàÌÈ°Ñ¡”‘…ä(€€€!½…¸ÍÕ••‘•	…¥±•ä…ÌÁ½ÍÑµ…ÍÑ•È°…¹…±±ÌÑ¡…ĞÑ¡”€ÄàÌÔ½™™¥”¸¹‘É•…ÌÍ…åÌÑİ¥”Ñ¡…Ğ(€€€Ñ¡”½™™¥”İ…ÌÍÑ¥±°…Ğ1…­”…¹M½ÕÑ ]…Ñ•ÈÑ¡É½Õ €ÄàÌÌ…¹µ½Ù•€¨©…‰½ÕĞ)Õ±ä€ÄàÌĞ¨¨¸Q¡”(€€€‘½ÍÍ¥•ÈÌ½¹±ÕÍ¥½¸ÍÕÉÙ¥Ù•Ì…¹¥ÑÌ¡É½¹½±½ä‘½•Ì¹½ĞèÑ¡”€ÄàÌÈ‘…Ñ”¥ÌÑ¡”Á½ÍÑµ…ÍÑ•ÈÌ°(€€€¹½ĞÑ¡”‰Õ¥±‘¥¹œÌ¸Q¡”½¹™±…Ñ¥½¸¥ÌÑÉ…•…‰±”Ñ¼Ñ¡”ÕÉÉ•äÁ…”Ñ¡”‘½ÍÍ¥•ÈÕÍ•°İ¡¥ (€€€µ…­•ÌÑ¡”…ÁÁ½¥¹Ñµ•¹Ğ…¹Ñ¡”µ½Ù”½¹”Í•¹Ñ•¹”ƒŠP…¹İ¡¥ …±Í¼ÍÕÁÁ±¥•ÌÑ¡”€‰Í½ÕÑ İ•ÍĞ(€€€½É¹•ÈˆÑ¡…Ğ¹‘É•…Ì¹•Ù•È¥Ù•Ì¸M½ÕÉ”É•½É¡¥…½±½å}™¥ÉÍÑ}Á½ÍÑ}½™™¥•€Í…åÌ½¸¥ÑÌ(€€€½İ¸™…”İ¡•É”¥Ğ¥Ì™½±±½İ•…¹İ¡•É”¥Ğ¥Ì¹½Ğ¸€¨©Q¡”½¹Í•ÅÕ•¹”™½ÈÑ¡”Í•¹”¨¨è½¸(€€€€ÄàÌÔ´ÀÜ´ÀÄÑ¡¥Ì‰Õ¥±‘¥¹œ¥Ì„ÍÑ½É”Ñ¡…ĞÕÍ•Ñ¼‰”Ñ¡”Á½ÍĞ½™™¥”°…¹Ñ¡”Ñ½İ¸Ì…ÑÕ…°(€€€Á½ÍĞ½™™¥”¥Ì„‘¥™™•É•¹Ğ°Õ¹µ½‘•±±•‰Õ¥±‘¥¹œ…‰½ÕĞ€ÄÀÀ´•…ÍĞ°½˜İ¡¥ ¹½Ñ¡¥¹œÍÕÉÙ¥Ù•Ì(€€€‰ÕĞ„ÍÑÉ••Ğ©Õ¹Ñ¥½¸ƒŠP¥Ğİ½Õ±‰”Ñ¡”µ½ÍĞ¥¹Ù•¹Ñ•‰Õ¥±‘¥¹œ¥¸Ñ¡”‘…Ñ…Í•Ğ…¹¥Ğ¥Ì(€€€İÉ¥ÑÑ•¸‘½İ¸É…Ñ¡•ÈÑ¡…¸‰Õ¥±Ğ€¡‘½Ì½IMI ½¡½…¹}ÍÑ½É”¹µ‘€ƒ
œ€Ğ¤¸(€€€€¨©Q¡”İ•…¬Á½¥¹Ğ¥ÌÍÕÉÙ¥Ù…°°¹½Ğ•½µ•ÑÉä°…¹¥Ğ¥ÌÍÑ…Ñ•½¸Ñ¡”É•½É¸¨¨Q¡”‰Õ¥±‘¥¹œ¥Ì(€€€…ÑÑ•ÍÑ•ÍÑ…¹‘¥¹œÑ¼…‰½ÕĞ)Õ±ä€ÄàÌĞ…¹¹¼Í½ÕÉ”É•…¡•™½±±½İÌ¥ĞÁ…ÍĞÑ¡…Ğì¥Ğ¥ÌÁ±…•(€€€¥¸„Í•¹”Í•Ğ•±•Ù•¸µ½¹Ñ¡Ì±…Ñ•È½¸Ñ¡”½¹Ñ¥¹Õ¥Ñä…ÉÕµ•¹Ğ°İ¥Ñ Ñ¡”½Õ¹Ñ•Èµ…ÉÕµ•¹ĞƒŠP(€€€1…­”…¹M½ÕÑ ]…Ñ•Èİ…ÌÑ¡”½É¹•Èµ½ÍĞ•áÁ½Í•Ñ¼Ñ¡”€ÄàÌÔ‰½½´ƒŠP¥¸Ñ¡”Í…µ”¹½Ñ”¸%˜(€€€•Ù¥‘•¹”ÑÕÉ¹ÌÕÀÑ¡…Ğ¥Ğ…µ”‘½İ¸™¥ÉÍĞ°¥Ğ‰•±½¹Ì¥¸•á±ÕÍ¥½¹Ì¹©Í½¹€…¹Ñ¡¥ÌÉ•½É(€€€±•…Ù•ÌÑ¡”Í•¹”¸(€€€€¨©=¹”Íµ…±±•ÈÑ¡¥¹œ…µ”½ÕĞ½˜Ñ¡”Í…µ”Á…”…¹¥ÌÉ•½É‘•É…Ñ¡•ÈÑ¡…¸…Ñ•½¸¸¨¨ÕÉÉ•ä(€€€¡…ÌQ¡½µÁÍ½¸Ì€ÄàÌÀÁ±…Ğ±…å¥¹œ½ÕĞÍÑÉ••ÑÌ€‰Õ¹¥™½Éµ±ä€ØØ™••Ğİ¥‘”ˆì•Ù•ÉäÁ½Í¥Ñ¥½¸¥¸Ñ¡¥Ì(€€€‘…Ñ…Í•Ğ½™™Í•ÑÌ‰ä¡…±˜½˜…¸€¨¨àÀ™Ğ¨¨ÍÑÉ••Ğ°™É½´Ñ¡”İ¥‘Ñ¡Ì…¹¹½Ñ…Ñ•½¸!…Ñ¡…İ…ä€ÄàÌĞ¸(€€€Q¡”‘¥™™•É•¹”¥Ì€È¸Ä´°…¸½É‘•È½˜µ…¹¥ÑÕ‘”¥¹Í¥‘”Ñ¡”•½É•™•É•¹”Ì½İ¸•ÉÉ½È°Í¼¹½Ñ¡¥¹œ(€€€µ½Ù•ÌƒŠP‰ÕĞÑ¡”Ñİ¼…¹¹½Ğ‰½Ñ ‰”É¥¡Ğ…‰½ÕĞÑ¡”Í…µ”ÍÑÉ••Ğ°…¹Ñ¡”É•½¹¥±¥…Ñ¥½¸İ½ÉÑ (€€€Ñ•ÍÑ¥¹œ¥ÌÑ¡…ĞÑ¡•ä…É”¹½Ğ…‰½ÕĞÑ¡”Í…µ”ÍÑÉ••Ğ¸M•”‘½Ì½IMI ½¡½…¹}ÍÑ½É”¹µ‘€ƒ
œ€Ô¸((ÈØ¸€¨©]¡…Ğİ…Ì±•™Ğ½ÕĞ¥ÌÉ•…‘…‰±”¥¸Ñ¡”İ…±­Ñ¡É½Õ °…¹•¹™½É¥¹œ¥Ğ™½Õ¹Ñ¡”½¹”™¥±”(€€€İ¡•É”ÉÕ±”½¹”İ…Ì¹•Ù•È¡•­•¸¨¨‘…Ñ„½•á±ÕÍ¥½¹Ì¹©Í½¹€ƒŠP™½ÕÉÑ••¸É•Í•…É¡•(€€€ÍÑÉÕÑÕÉ•Ìİ¥Ñ Ñ¡”•Ù¥‘•¹”Ñ¡…Ğ‘…Ñ•ÌÑ¡•´°Á±ÕÌ„™½ÕÈµ¥Ñ•´İ…Ñ ±¥ÍĞƒŠP¡…Ì•á¥ÍÑ•(€€€Í¥¹”Ñ¡”Í…™™½±…¹¡…Ì‰••¸É•…‰ä…•¹ÑÌ½¹±ä¸Ù¥Í¥Ñ½ÈÍÑ…¹‘¥¹œ¥¸…¸•µÁÑä±½Ğ(€€€…¹¹½Ğ‘¥ÍÑ¥¹Õ¥Í Ñ¡É•”‘¥™™•É•¹ĞÍÑ…Ñ•µ•¹ÑÌè¹½‰½‘äÉ•Í•…É¡•Ñ¡¥Ì°Ñ¡”•Ù¥‘•¹”(€€€‘…Ñ•Ì¥Ğ…™Ñ•ÈÑ¡”Í•¹”°½È¥Ğ¡……±É•…‘ä½µ”‘½İ¸¸Q¡”™¥ÉÍĞ¥Ì„…À¥¸Ñ¡”İ½É¬(€€€…¹Ñ¡”½Ñ¡•ÈÑİ¼…É”™¥¹‘¥¹ÌÑ¡…Ğ½ÍĞÉ•Í•…É Ñ¼•ÍÑ…‰±¥Í ¸Q¡”Ù¥‘•¹”Á…¹•°¹½Ü(€€€…ÉÉ¥•ÌÑ¡•´Õ¹‘•È€¨©]¡…Ğ¥Ì¹½Ğ¡•É”¨¨°‘•É¥Ù•Á•ÈÍ•¹”‰ä½µÁ¥±•}Í•¹”¹Áå€İ¥Ñ (€€€Ñ¡”¥Ñ…Ñ¥½¹Ì©½¥¹•°‰•±½ÜÑ¡”±¥‰•ÉÑ¥•Ì…¹¥¸Ñ¡”Í…µ”€ñ‘•Ñ…¥±Ìù€•¹ÑÉä°‰•…ÕÍ”(€€€Ñ¡•ä…É”Ñ¡”Í…µ”­¥¹½˜‘¥Í±½ÍÕÉ”¸(€€€€¨©Q¡”¡¥À¥ÌÑ¡”É•½ÉÌ™¥•±°¹•Ù•È„Á¡É…Í”‘•É¥Ù•™É½´…¸…‰Í•¹”¸¨¨Q•¸•¹ÑÉ¥•Ì(€€€…ÉÉä•…É±¥•ÍÑ}Í•¹•€…¹Í¡½Ü€‰¹½ĞÕ¹Ñ¥°€ÄàÌÜˆì­¥¹é¥•}¡½ÕÍ•€…¹½Õ¥±µ•ÑÑ•}…‰¥¹€(€€€İ•É”•á±Õ‘•‰•…ÕÍ”Ñ¡•äİ•É”=9°…ÉÉä¹¼ÍÕ ™¥•±°…¹•Ğ¹¼¡¥ÀƒŠPÍÑ…µÁ¥¹œ(€€€½¹”½¸Ñ¡•´İ½Õ±‰”…¸¥¹Ù•¹Ñ¥½¸½¸Ñ¡”Á…¹•°Ñ¡…Ğ•á¥ÍÑÌÑ¼…‘µ¥Ğ¥¹Ù•¹Ñ¥½¹Ì¸Q¡”(€€€Íµ½­”…ÍÍ•ÉÑÌÑ¡…Ğ‘¥ÍÉ¥µ¥¹…Ñ¥¹œÁ…¥ÈÉ…Ñ¡•ÈÑ¡…¸„½Õ¹Ğ°…¹…ÍÍ•ÉÑÌÑ¡…Ğ„‰Õ¥±‘¥¹œ(€€€Ñ¡”Ù¥Í¥Ñ½È…¸İ…±¬ÕÀÑ¼¥Ì€©¹½Ğ¨½¸Ñ¡”±¥ÍĞ°İ¡¥ „Í•Ñ¥½¸‘ÕµÁ¥¹œÑ¡”İ¡½±”(€€€‘…Ñ…Í•Ğİ½Õ±ÍÑ¥±°¡…Ù”Á…ÍÍ•¸(€€€€¨©Q¡”±¥ÍĞÍÑ…Ñ•Ìİ¡…Ğ¥Ğ¥Ì¹½Ğ¨¨°…¹Ñ¡…ĞÍ•¹Ñ•¹”¥Ì„Íµ½­”…ÍÍ•ÉÑ¥½¸Ñ½¼è•¥¡Ğ½˜(€€€É½Õ¡±ä™½ÉÑäÉ•Í•…É¡•ÍÑÉÕÑÕÉ•ÌÍÑ…¹°Í¼„™½ÕÉÑ••¸µ¥Ñ•´±¥ÍĞ½˜…‰Í•¹•Ìİ¥Ñ ¹¼(€€€ÍÕ ¹½Ñ”É•…‘Ì…Ì€‰Ñ¡¥Ì¥Ìİ¡…Ğ¥Ìµ¥ÍÍ¥¹œˆ°İ¡¥ İ½Õ±‰”Ñ¡”±…É•ÍĞ™…±Í”±…¥´Ñ¡”(€€€Á…¹•°½Õ±µ…­”¸(€€€€¨©Qİ¼ÉÕ±•Ì…ÉÉ¥Ù•İ¥Ñ ¥Ğ°…¹Ñ¡”™¥ÉÍĞ¥Ì•µ‰…ÉÉ…ÍÍ¥¹œ¥¸Ñ¡”ÕÍ•™Õ°İ…ä¸¨¨9QL¹µ(€€€ÉÕ±”€Ä¥ÌÑ¡…Ğ•Ù•ÉäÍ½ÕÉ•}¥‘€É•Í½±Ù•Ì¥¸‘…Ñ„½Í½ÕÉ•Ì½€ì•á±ÕÍ¥½¹Ì¹©Í½¹€İ…ÌÑ¡”(€€€½¹”™¥±”İ¡•É”¹½Ñ¡¥¹œ•¹™½É•¥Ğ°‰•…ÕÍ”Õ¹Ñ¥°¹½Ü¹½Ñ¡¥¹œÉ•…¥ĞƒŠP„¥Ñ…Ñ¥½¸Ñ¡•É”(€€€½Õ±¡…Ù”¹…µ•„Í½ÕÉ”Ñ¡…Ğ¹•Ù•È•á¥ÍÑ•…¹Ñ¡”…Ñ”İ½Õ±¡…Ù”ÍÑ…å•É••¸¸(€€€¡•­}•á±ÕÍ¥½¹Í€¡½±‘Ì¥ĞÑ¼Ñ¡”Í…µ”ÍÑ…¹‘…É…Ì„ÍÑÉÕÑÕÉ”É•½Éè„Í±Õœ¥°„(€€€¹…µ”°„ÍÑ…Ñ•É•…Í½¸€¡…¸•á±ÕÍ¥½¸İ¥Ñ¡½ÕĞ½¹”¥Ì„‘•±•Ñ¥½¸İ¥Ñ „™¥±•¹…µ”¤°…¹…Ğ(€€€±•…ÍĞ½¹”¥Ñ…Ñ¥½¸Ñ¡…ĞÉ•Í½±Ù•Ì¸Q¡”½µµ¥ÑÑ•™¥±”Á…ÍÍ•ÌÕ¹¡…¹•ìÑ¡”Ù…±Õ”¥ÌÑ¡…Ğ(€€€Ñ¡”¹•áĞ•¹ÑÉä…¹¹½Ğ¸Q¡”Í•½¹¥ÌÑ¡”‘…Ñ”…Ñ”É•…‰…­İ…É‘Ìè…¸•¹ÑÉä‘…Ñ¥¹œ„(€€€‰Õ¥±‘¥¹œÑ¼€ÄàÌÜ¥Ì„½ÉÉ•Ğ•á±ÕÍ¥½¸™É½´€ÄàÌÔ…¹„]I=9½¹”™É½´€ÄàÌÜ°…¹¹¼(€€€½µÁ…É¥Í½¸……¥¹ÍĞÑ¡”É•½É‘Ì…¸…Ñ ¥Ğ‰•…ÕÍ”…¸•á±Õ‘•ÍÑÉÕÑÕÉ”¡…Ì¹¼É•½É(€€€Ñ¼½µÁ…É”İ¥Ñ ¸%¸„å•…ÈµÁ…É…µ•Ñ•É¥é•ÁÉ½©•ĞÑ¡…Ğ¥Ì•á…Ñ±äÑ¡”¡•¬İ½ÉÑ ¡…Ù¥¹œ(€€€‰•™½É”Ñ¡”Í•½¹Í•¹”•á¥ÍÑÌÉ…Ñ¡•ÈÑ¡…¸…™Ñ•È¸(€€€€¨©Q¡”İ…Ñ ±¥ÍĞ¥Ì‘•±¥‰•É…Ñ•±ä¹½ĞÍ¡½İ¸¸¨¨%ÑÌ™½ÕÈ¥Ñ•µÌ…É”ÍÑÉÕÑÕÉ•Ìİ¡½Í”€ÄàÌÔ(€€€ÍÑ…ÑÕÌ¥ÌÕ¹•ÉÑ…¥¸É…Ñ¡•ÈÑ¡…¸Í•ÑÑ±•°…¹½¹”½˜Ñ¡•´€¡İ•ÍÑ•É¹}¡½Ñ•±€¤¥ÌÍÑ…¹‘¥¹œ¥¸(€€€Ñ¡”Í•¹”ƒŠPÁÕÑÑ¥¹œÑ¡•´Õ¹‘•È€‰İ¡…Ğ¥Ì¹½Ğ¡•É”ˆİ½Õ±‰”™…±Í”…‰½ÕĞÑ¡”½¹”Ñ¡¥¹œÑ¡”(€€€Í•Ñ¥½¸¥Ì™½È¸Q¡•¥ÈÕ¹•ÉÑ…¥¹Ñä‰•±½¹Ì½¸Ñ¡”É•½É‘Ì…¹¥¸Ñ¡”ÁÉ½Ù•¹…¹”Á½ÁÕÀ°(€€€İ¡¥ ¥Ì„‘¥™™•É•¹ĞÍ±¥”…¹¥Ì¹½ĞÅÕ•Õ•¸(ÈÜ¸€¨©Q¡”Í¥‘•…ÉÌ…É”É”µ‘•É¥Ù•‰äÑ¡”…Ñ”¹½Ü°İ¡¥ Ñ¡•äİ•É”¹½Ğ¸¨¨½µÁ¥±•}Í•¹”¹Áå€(€€€İÉ¥Ñ•Ìİ¡…ĞÑ¡”É•¹‘•É•ÈÉ•…‘Ì…¹Ñ¡”½ÕÑÁÕÑÌ…É”½µµ¥ÑÑ•Í¼Ñ¡”Í¥Ñ”¹••‘Ì¹¼‰Õ¥±(€€€ÍÑ•ÀƒŠP…¸…ÉÉ…¹•µ•¹ĞÑ¡…Ğ½¹±ä¡½±‘Ì¥˜‘É¥™Ğ¥Ì„™…¥±ÕÉ”¸9½Ñ¡¥¹œÉ•½µÁÕÑ•Ñ¡•´°Í¼(€€€„É•½É•‘¥Ñ•İ¥Ñ¡½ÕĞ„É•½µÁ¥±”Í¡¥ÁÁ•„İ…±­Ñ¡É½Õ ÅÕ½Ñ¥¹œÑ¡”ÁÉ•Ù¥½ÕÌ‘…Ñ…Í•Ğ(€€€İ¥Ñ •Ù•Éä¥Ñ…Ñ¥½¸ÍÑ¥±°±½½­¥¹œ…ÕÑ¡½É¥Ñ…Ñ¥Ù”¸€´µ¡•­€É”µ‘•É¥Ù•ÌÑ¼µ•µ½Éä…¹(€€€½µÁ…É•Ìì¡•¬¹Í¡€ÉÕ¹Ì¥Ğ°Ñ¡”Í…µ”İ…ä¥Ğ…±É•…‘äÉ”µ‘•É¥Ù•±¥‰•ÉÑ¥•Ì¹©Í½¹€¸Q¡”(€€€•¥¡Ğ½µµ¥ÑÑ•Í¥‘•…ÉÌ…¹Ñ¡”¥¹‘•àİ•É”‰åÑ”µ¥‘•¹Ñ¥…°½¸Ñ¡”™¥ÉÍĞÉÕ¸°Í¼Ñ¡¥Ì(€€€Íİ¥Ñ¡•½¸İ¥Ñ ¹¼É•Á…¥È‰•¡¥¹¥Ğ¸]¡…Ğ¥Ğ‘½•Ì9=P¡•¬¥ÌÑ¡”‘¥É•Ñ¥½¸Ñ¡”(€€€ÍÑ…±•¹•ÍÌ…Ñ”½Ù•ÉÌƒŠPÑ¡…ĞÑ¡”1µ…Ñ¡•ÌÑ¡”É•½ÉƒŠP…¹¹•¥Ñ¡•È½˜Ñ¡•´…¸Í•”„(€€€É•½ÉÑ¡…Ğ¥ÌİÉ½¹œ…‰½ÕĞÑ¡”Ñ½İ¸¸((ŒŒ9•áĞ((¨©LÔƒŠPµ½É”ÍÑÉÕÑÕÉ”É•½É‘Ì¨¨°İ¡¥ ¥Ì¹½ÜÑ¡”‰¥¹‘¥¹œ½¹ÍÑÉ…¥¹ĞèÍ•Ù•¸ÍÑÉÕÑÕÉ•ÌÍÑ…¹)İ¡•É”Ñ¡”Í½ÕÉ•Ì‘•ÍÉ¥‰”É½Õ¡±ä™½ÉÑä°…¹½¹”½˜Ñ¡”Í•Ù•¸¥Ì„‰É¥‘”¸9½Ñ”Ñ¡”½ÕÁ±¥¹œ‘¥Í½Ù•É•½¸€ÈÀÈØ´Àà´ÄÀ°‰•…ÕÍ”¥ĞÍ•ÑÌ)Ñ¡”Í¡…Á”½˜Ñ¡”İ½É¬èÑ½½±Ì½½µÁ¥±•}Í•¹”¹Áå€İÉ¥Ñ•Ì…¸…ÍÍ•Ñ€Á…Ñ ™½È•Ù•ÉäÍÑÉÕÑÕÉ”Ñ¡…Ğ)É•Í½±Ù•Ì¥¹Ñ¼Ñ¡”Í•¹”°Í¼„É•½É½µµ¥ÑÑ•İ¥Ñ¡½ÕĞ¥ÑÌ1µ…­•ÌÑ¡”É•¹‘•É•È™•Ñ „™¥±”)Ñ¡…Ğ¥Ì¹½ĞÑ¡•É”ƒŠP„€ĞÀĞÑ¡”Íµ½­”½ÉÉ•Ñ±ä™…¥±Ì½¸¸€¨©ÍÑÉÕÑÕÉ”É•½É…¹¥ÑÌ‰…­”…É”½¹”)Õ¹¥Ğ¸¨¨¸…•¹Ğİ¥Ñ¡½ÕĞ	±•¹‘•È…¸ÁÉ•Á…É”Ñ¡”É•½É…¹Ñ¡”É•Í•…É µ•µ¼°‰ÕĞÑ¡”Á…¥È¡…Ì)Ñ¼±…¹Ñ½•Ñ¡•È°Í¼Ñ¡”‰…­”İ½É­™±½ÜÌAH¥ÌÁ…ÉĞ½˜Ñ¡”Í…µ”Í±¥”É…Ñ¡•ÈÑ¡…¸„™½±±½ÜµÕÀ¸(¨©Q¡…Ğ½ÕÁ±¥¹œ¥Ì¹½Ü•¹™½É•É…Ñ¡•ÈÑ¡…¸É•µ•µ‰•É•¨¨€ ÈÀÈØ´Àà´ÄÀ¤è•‘¥Ñ¥¹œ„Ù…±Õ”„)•¹•É…Ñ½ÈÉ•…‘Ìµ…­•ÌÑ¡”½µµ¥ÑÑ•1ÍÑ…±”…¹¡•¬¹Í¡€™…¥±ÌÕ¹Ñ¥°Ñ¡”É”µ‰…­”±…¹‘Ìİ¥Ñ )¥Ğ¸%Ğİ…ÌÑ¡•¸•á•É¥Í•™½ÈÉ•…°‰äÑ¡”]½±˜A½¥¹ĞÉ•Á…¥ÈÑ¡”Í…µ”‘…äƒŠPÑ¡”É•¹…µ”ÑÕÉ¹•Ñ¡”)Ñ…Ù•É¸Ì…ÍÍ•ĞÍÑ…±”½¸Ñ¡”ÍÁ½Ğ…¹Ñ¡”‰É…¹ ½Õ±¹½Ğ¼É••¸Õ¹Ñ¥°Ñ¡”‰…­”±…¹‘•½¸¥Ğ°)İ¡¥ ¥ÌÑ¡”İ¡½±”Á½¥¹Ğ½˜İÉ¥Ñ¥¹œÑ¡”¡•¬°…¹……¥¸Ñ¡”Í…µ”‘…ä‰ä5¥±±•ÈÌÍ•½¹¡¥µ¹•ä°)…¹„Ñ¡¥ÉÑ¥µ”‰ä¡¥Ì™É…µ”É…¹”¸(¨©Q¡”É•Á…¥È±¥ÍĞÉ•™¥±±•¥ÑÍ•±˜™É½´Ñ¡”…É¡¥Ù”É…Ñ¡•ÈÑ¡…¸™É½´Ñ¡”…Ñ•Ì°…¹•µÁÑ¥•……¥¸)Ñ¡”Í…µ”‘…ä¨¨€ ÈÀÈØ´Àà´ÄÀ°ƒ
œ€ÈÌƒŠHƒ
œ€ÈĞ¤¸Ù•ÉäÁÉ•Ù¥½ÕÌ•¹ÑÉä½¸¥Ğİ…Ì™½Õ¹‰ä„¡•¬è„)µ¥ÍÍÁ•±±•…ÑÑÉ¥‰ÕÑ”°„¹…µ”É•……Ì‰•¥¹œ…‰½ÕĞÑ¡”İÉ½¹œ¡…±˜½˜„‰Õ¥±‘¥¹œ¸Q¡…Ğ½¹”İ…Ì™½Õ¹)‰äÉ•…‘¥¹œ„Á…”°…¹¥Ğ¥Ì¹½Ü€¨©=9¨¨ƒŠPÑ¡”É•½É°Ñ¡”…É¡•ÑåÁ”…¹Ñ¡”‰…­”±…¹‘•)Ñ½•Ñ¡•È°Á¥•É}½Õ¹Ğè€É€É•Á±…•Á¥•É}ÍÁ…¥¹}µ€°…¹Ñ¡”ÅÕ•Õ”¥Ì•µÁÑä……¥¸¸]¡…Ğ¥Ğ±•…Ù•Ì)‰•¡¥¹¥Ì„Í¡…Á”İ½ÉÑ É•ÕÍ¥¹œÉ…Ñ¡•ÈÑ¡…¸„Ñ…Í¬èİ¡•¸•Ù¥‘•¹”…¹…¸…É¡•ÑåÁ”‘¥Í…É•”°¡•¬)İ¡•Ñ¡•ÈÑ¡”…É¡•ÑåÁ”¥Ì…Í­¥¹œ™½ÈÑ¡”İÉ½¹œ€©­¥¹¨½˜¹Õµ‰•È‰•™½É”¡…¹¥¹œÑ¡”¹Õµ‰•È¥Ğ¡…Ì¸)Q¡”½±‘•È…½Õ¹Ğ½˜Ñ¡”ÅÕ•Õ”°ÍÑ¥±°ÑÉÕ”½˜•Ù•ÉåÑ¡¥¹œ‰•™½É”Ñ¡¥Ì•¹ÑÉäèQ¡”±…ÍĞ•¹ÑÉäƒŠP)µ¥±±•É}¡½ÕÍ•€É•½É‘¥¹œ„‘½Õµ•¹Ñ•‘€™É…µ”É…¹”İ¥Ñ ¹¼Í¥‘”°İ¥‘Ñ °‘•ÁÑ ½ÈÍÑ½É•ä½Õ¹ĞƒŠP)±…¹‘•€ÈÀÈØ´Àà´ÄÀİ¥Ñ ¥ÑÌ‰…­”€£
œ€ÈÀ¤°…¹¥Ğİ…ÌÑ¡”™½ÕÉÑ …¹±…ÍĞ½˜Ñ¡”™…Õ±ÑÌÑ¡”½µ¥ÍÍ¥½¸)…Ñ”½Á•¹•¸Q¡É•”½˜Ñ¡”™½ÕÈİ•É”ÍÁ•±±¥¹œìÑ¡”™½ÕÉÑ İ…Ì„¹…µ”É•……Ì‰•¥¹œ…‰½ÕĞÑ¡”İÉ½¹œ)¡…±˜½˜„Ñİ¼µÁ…ÉĞ‰Õ¥±‘¥¹œ°İ¡¥ ¹¼ÍÁ•±±¥¹œ¡•¬İ½Õ±¡…Ù”…Õ¡Ğ¸9½Ñ¡¥¹œ¹•Ü¥ÌÅÕ•Õ•)‰•¡¥¹¥Ğ°Í¼€¨©LÔ¥Ì…‘‘¥Ñ¥½¹Ì……¥¸¨¨è•¥¡Ğ…É¡•ÑåÁ•Ì…¹…‰½ÕĞ™½ÉÑäÉ•Í•…É¡•ÍÑÉÕÑÕÉ•Ì)……¥¹ÍĞÑ¡”Í¥àÑ¡…ĞÍÑ…¹¸((¨©LäƒŠPÍÑÉ••ÑÌ°É½…‘Ì…¹Á…Ñ¡Ì¨¨°€¨©%IMPY%M%	1M1%=9€ÈÀÈØ´Àà´ÄÄ¸¨¨M•Ù•¹Ñ••¸‘…Ñ•)•…ÉÑ ÑÉ…Ù•±İ…åÌ…É”½µÁ¥±•™É½´‘…Ñ„½ÍÑÉ••ÑÌ¼ÄàÌÔ¹©Í½¹€°‘É…Á•É…Ñ¡•ÈÑ¡…¸™±…ÑÑ•¹•°…¹)¥‘•¹Ñ¥™¥•±¥Ù”İ¥Ñ Ñ¡•¥È€ÄàÌÔ…¹€ÈÀÈØ¹…µ•Ì¸Q¡”•…É±¥•ÈÍ•¹Ñ•¹”¡•É”Í…å¥¹œ€‰¹½Ñ¡¥¹œİ…Ì)É…‘•Õ¹Ñ¥°€ÄàÔÔ´Ôàˆ½¹™ÕÍ•Ñ¡”±…Ñ•ÈI…¥Í¥¹œ½˜¡¥…¼İ¥Ñ •…É±äÍÑÉ••Ğİ½É¬…¹İ…Ì)İÉ½¹œèM½ÕÑ ]…Ñ•Èİ…Ì½É‘•É•Á¥Ñ¡•‰äÁÉ¥°€ÄàÌĞ…¹É…‘•™½È‘É…¥¹…”Ñ¡…Ğ)Õ±äìM½ÕÑ )]…Ñ•È…¹1…­”İ•É”Ñ¡”Ñİ¼•…É±äÁÉ¥¹¥Á…°¥µÁÉ½Ù•É½ÕÑ•Ì¸]¡…ĞÉ•µ…¥¹Ì¥ÌÑ¡”¹½ÉÑ µÍ¥‘”)½¹ÑÉ½°½•áÑ•¹ĞÉ•Í•…É °…¹äÍ•Á…É…Ñ•±ä…ÑÑ•ÍÑ•Á±…¹¬™½½Ñİ…±­Ì°…¹•Ù¥‘•¹”Ñ¡…Ğ½Õ±É•Á±…”)Ñ¡”½¹©•ÑÕÉ…°ÑÉ…Ù•±±•İ¥‘Ñ¡Ì…¹ÉÕĞÁ…ÑÑ•É¹ÌÉ•½É‘•¥¸0Üä¸M•”I=5@ƒ
œLä¸((¨©LÕ„ƒŠP½ÉĞ•…É‰½É¸¨¨ƒŠP€¨©=9€ÈÀÈØ´Àà´ÄÄ¨¨°‰½Ñ …Ñ•Ì±•…É•‰•™½É”…¹ä•½µ•ÑÉä¸(¨©Q¡”™½½ÑÁÉ¥¹Ğ¡…Ì„Í½ÕÉ”¸¨¨¸!…ÉÉ¥Í½¸)È¸ÌÍÕÉÙ•ä½˜Ñ¡”µ½ÕÑ ½˜Ñ¡”¡¥…¼I¥Ù•È™½È)Ñ¡”¡…É‰½ÕÈİ½É­Ì°€ÈĞ•‰ÉÕ…Éä€ÄàÌÀ°…ÁÁÉ½Ù•‰ä]¥±±¥…´!½İ…É°T¹L¸¥Ù¥°¹¥¹••È°É•ÁÉ½‘Õ•)¥¸¹‘É•…ÌÙ½°¸€ÄÀ¸€ÄÄÌ…¹±¥ÍÑ•¥¸Ñ¡…ĞÙ½±Õµ”Ì½İ¸Ñ…‰±”½˜µ…ÁÌ…Ì€‰½ÉĞ•…É‰½É¸¥¸(ÄàÌÀ´ÌÈˆ¸%Ğ‘É…İÌÑ¡”™½ÉĞ%8A18ƒŠPÍÅÕ…É”•¹±½ÍÕÉ”°İ½É­Ì…ĞÑ¡É•”…¹±•Ì°™½ÕÈÉ…¹•Ì°Ñİ¼)…Ñ•Ì°Ñİ¼‰Õ¥±‘¥¹Ì™±…¹­¥¹œÑ¡”Í½ÕÑ …Ñ”ƒŠP…¹¥ÑÌ…ÉÉ…¹•µ•¹Ğ¥Ì½ÉÉ½‰½É…Ñ•‰Õ¥±‘¥¹œ‰ä)‰Õ¥±‘¥¹œ‰äÕÉ‘½¸!Õ‰‰…ÉÌ€ÄàÈÜİ…±¬É½Õ¹Ñ¡”¥¹Í¥‘”€¡¹‘É•…ÌÀ¸€ÈØĞ¤¸I•½É‘•…Ì)¡…ÉÉ¥Í½¹|ÄàÌÁ}É¥Ù•É}µ½ÕÑ¡€¸€¨©Q¡”Á±…Ñ”¡…Ì¹¼Í…±”‰…È¨¨°Í¼Ñ¡”Í…±”¥Ì‘•É¥Ù•™É½´Ñ¡”½¹”)ÍÑ…Ñ•‘¥µ•¹Í¥½¸¥¸Ñ¡”İ¡½±”½µÁ±•àƒŠPÑ¡”½µµ…¹‘…¹ĞÌÅÕ…ÉÑ•ÉÌ…Ğ€‰…‰½ÕĞ€ÈÔà€ÔÀ™Ğˆ¥¸Ñ¡”(ÄàÔÔÁ¡½Ñ½É…Á ­•äƒŠP¥Ù¥¹œ€Ä¸ÄÀ™Ğ½Áà…¹„ÍÑ½­…‘”…‰½ÕĞ€ÔÌ´€ ÄÜĞ™Ğ¤ÍÅÕ…É”…Ğ€¨«
ÄÈÀ€”¨¨¸)Qİ¼¡•­Ì½¸Ñ¡”Í…µ”Á±…Ñ”…É•”Ñ¼€Ô€”…¹€ÄÄ€”¸€¨©Q¡”…ÉÉ¥Í½¸¥ÌÍ•ÑÑ±•¨¨è¡•±)½¹Ñ¥¹Õ½ÕÍ±ä™É½´)Õ¹”€ÄàÌÈÑ¼€Èä••µ‰•È€ÄàÌØ°5…¨¸)½¡¸É••¹”€ÕÑ %¹™…¹ÑÉäµ½ÍĞ±¥­•±ä)½µµ…¹‘¥¹œ½¸Ñ¡”Í•¹”‘…Ñ”°ÍÑÉ•¹Ñ …™Ñ•È€ÄàÌÌÕ¹…ÑÑ•ÍÑ•¸½ÕÉÑ••¸É•½É‘Ì°Ñİ¼¹•Ü)…É¡•ÑåÁ•Ì€¡Á…±¥Í…‘•€°™½ÉÑ}ÍÑÉÕÑÕÉ•€¤°™½ÕÉÑ••¸‰…­•Ì°øÄÜ°ÀÀÀÑÉ¥…¹±•Ì¸¥Ù”•á±ÕÍ¥½¹Ì)İ•¹Ğ¥¸İ¥Ñ ¥Ğ°™½ÕÈ½˜Ñ¡•´İÉ½¹œµ™½ÉĞ™¥¹‘¥¹Ì¸M•”‘½Ì½IMI ½™½ÉÑ}‘•…É‰½É¸¹µ‘€¸(¨©]¡…Ğ¥Ğ‘¥9=PÍ•ÑÑ±”…¹İ¡…Ğ¥Ì¹½ÜÑ¡”‰¥¹‘¥¹œ½¹ÍÑÉ…¥¹ĞèÑ¡•É”¥Ì¹¼É½Õ¹Õ¹‘•È¥Ğ¸¨¨((¨©LÉ”ƒŠP•áÑ•¹Ñ¡”É½Õ¹•…ÍĞÑ¼Ñ¡”±…­”¸¨¨I…¥Í•Ñ¼Ñ¡”Ñ½À½˜Ñ¡”Ñ•ÉÉ…¥¸İ½É¬½¸(ÈÀÈØ´Àà´ÄÀ…Ğ-•Ù¥¸Ì‘¥É•Ñ¥½¸°…™Ñ•È™É•”µ™±äµ…‘”¥ĞÙ¥Í¥‰±”™É½´Ñ¡”…¥ÈèÑ¡”µ½‘•±±•)‰½àÍÑ½ÁÌ…Ğ±½…°€¬ÌÈÀ°İ¡¥±”Ñ¡”½ÉĞ•…É‰½É¸Í¥Ñ”¥Ì…Ğ€¬ÄÄÈÜ…¹Ñ¡”€ÄàÌÔÍ¡½É”¥Ì)…‰½ÕĞ„­¥±½µ•ÑÉ”™ÕÉÑ¡•ÈÍÑ¥±°¸½ÉĞ•…É‰½É¸…¹Ñ¡”¡…É‰½ÕÈİ½É­Ì…¹¹½Ğ‰”Á±…•Õ¹Ñ¥°)Ñ¡”É½Õ¹Õ¹‘•ÈÑ¡•´•á¥ÍÑÌ¸Q¡”Í¡½É•±¥¹”¥ÑÍ•±˜¥Ì„ÁÉ½Ù•¹…¹”ÁÉ½‰±•´‰•™½É”¥Ğ¥Ì„)µ½‘•±±¥¹œ½¹”ƒŠP•Ù•ÉåÑ¡¥¹œ•…ÍĞ½˜É½Õ¡±ä5¥¡¥…¸Ù•¹Õ”¥Ì±…Ñ•È±…¹‘™¥±°°Í¼Ñ¡”•‘”)µÕÍĞ½µ”½™˜]É¥¡Ğ€ÄàÌĞ°¹½Ğ½™˜„µ½‘•É¸½…ÍĞ¸M•”I=5@ƒ
œLÉ”¸((¨©A…É•°€¡„¤¥Ì‘½¹”…¹Á…É•°€¡ˆ¤¥ÌÑ¡”¹•áĞÍ±¥”¸¨¨Q¡”Í¡½É”¥Ì¹½ÜÑÉ…•(¡Ñ½½±Ì½ÑÉ…•}Í¡½É•±¥¹”¹Áå€ƒŠHÍ¡½É•±¥¹”¹•½©Í½¹€°µ•µ¼)‘½Ì½IMI ½Í¡½É•±¥¹•}¡…É‰½É|ÄàÌĞ¹µ‘€¤…¹¥Ğµ½Ù•Ñİ¼¹Õµ‰•ÉÌ½™˜•ÍÑ¥µ…Ñ”…¹½¹Ñ¼)µ•…ÍÕÉ•µ•¹ĞèÑ¡”µ…¥¹±…¹Í¡½É”É•…¡•Ì±½…°€¨©€¬ÄÈÔÜ¨¨…¹Ñ¡”Í…¹‰…ÈÌ•…ÍĞ•‘”(¨©€¬ÄĞäÜ¨¨°Í¼Ñ¡”É½…‘µ…ÀÌÁÉ½Á½Í•€¬ÄÔÀÀ‰½àİ½Õ±¡…Ù”±¥ÁÁ•Ñ¡”‰…È‰ä€Ì´…¹Ñ¡”)‰½àÍ¡½Õ±‰”€¨¨¬ÄÔØÀ¨¨¸Qİ¼¥¹‘•Á•¹‘•¹ĞÍ•µ•¹Ñ…Ñ¥½¹Ì½˜Ñ¡”Í…µ”Í¡••Ğ°¥¸‘¥™™•É•¹Ğİ¥¹‘½İÌ)İ¥Ñ ‘¥™™•É•¹Ğ‰…­É½Õ¹ÍÑ…Ñ¥ÍÑ¥Ì°…É•”¥¸Ñ¡•¥È€àÀ´½Ù•É±…ÀÑ¼€¨¨À¸ÇŠLÔ¸Ü´¨¨½¸Ñ¡”Í½ÕÑ )‰…¹¬…¹€¨¨À¸×ŠLÄ¸Ì´¨¨½¸Ñ¡”¹½ÉÑ ƒŠPİ½ÉÑ ÍÑ…Ñ¥¹œ‰•…ÕÍ”¥Ğ¥Ì•Ù¥‘•¹”Ñ¡…ĞÑ¡”ÑÉ…”É•…‘Ì)Ñ¡”‘É…Õ¡ÑÍµ…¸Ì±¥¹”…¹¹½Ğ¥ÑÌ½İ¸Ñ¡É•Í¡½±‘Ì¸]¡…Ğ¥ÌÍÑ¥±°…‰Í•¹Ğè€¨©¹¼•±•Ù…Ñ¥½¸•á¥ÍÑÌ)…¹åİ¡•É”•…ÍĞ½˜€¬ÌÈÀ¨¨°Ñ¡”‰…È¥¹±Õ‘•¸‰…È¥Ì„ÍÕÉ™…”„½ÕÁ±”½˜™••Ğ½˜±…­”ÍÑ…”)µ½Ù•Ì…¹¹¼Í½ÕÉ”¥Ù•Ì¥ÑÌ¡•¥¡Ğ°Í¼Ñ¡”¹Õµ‰•Èİ¥±°¡…Ù”Ñ¼‰”…ÉÕ•¥¸Ñ¡”Ñ•ÉÉ…¥¸ÍÁ•Œ)É…Ñ¡•ÈÑ¡…¸Á¥­•¸U¹Ñ¥°Ñ¡”¡•¥¡Ñ™¥•±…¹¥ÑÌ‰…­”±…¹Ñ½•Ñ¡•È°¹½Ñ¡¥¹œ•…ÍĞ½˜Ñ¡”)ÕÉÉ•¹Ğ‰½àÉ•¹‘•ÉÌ…¹Ñ¡”…•É¥…°Ù¥•ÜÌ•‘”¥ÌÕ¹¡…¹•¸((¨©LÈÉ•µ…¥¹‘•È¨¨ƒŠPÉ½œA½¹°Ñ¡”]•±±ÌMÑÉ••Ğµ…ÉÍ °…¹Ñ¡”É•ÍĞ½˜Ñ¡”¡å‘É½±½ä‰•å½¹)Ñ¡”Í¥¹±”ÑÉ…•Í±½Õ •¹ÑÉ•±¥¹”¸((¨©LØƒŠP™±½É„…¹™…Õ¹„É•½É‘Ì¨¨°İ¡¥ ¥Ì…±Í¼İ¡…Ğİ½Õ±É•Ñ¥É”±¥‰•ÉÑä0ÈÌÁÉ½µ¥Í”èÑ¡”)Á…±•ÑÑ•Ì…¹Á±…•µ•¹ĞÑ…‰±•Ì•á¥ÍĞ¥¸Ñ¡”‘½ÍÍ¥•ÉÌ…¹¹½Ñ¡¥¹œ¡…Ì‰••¸ÑÕÉ¹•¥¹Ñ¼‘…Ñ„¸()9•Ü™¥¹‘¥¹Ì™½ÈLÈ™É½´Ñ¡”‘…ÑÕ´İ½É¬è!…Ñ¡…İ…ä…ÉÉ¥•ÌÍÕÉÙ•ä‰•…É¥¹Ì…¹±½Ğ‘¥µ•¹Í¥½¹Ì( ‰8¸ÔÇ
Á¸ˆ…±½¹œÑ¡”µ…¥¸ÍÑ•´°€àÀµ™ĞÍÑÉ••ÑÌ…¹¹½Ñ…Ñ•¤ì‰½Ñ €ÄàÌĞÍ¡••ÑÌ…É”…¹¥Í½ÑÉ½Á¥…±±ä)ÍÑÉ•Ñ¡•€ Ì¸Ü”€¼€Ğ¸Ô”¤°Í¼ÍÑÉ••Ğ•½µ•ÑÉäÍ¡½Õ±‰”•¹•É…Ñ•…¹…±åÑ¥…±±ä™É½´Ñ¡”Á±…Ğ)‘¥µ•¹Í¥½¹Ì…¹Í¹…ÁÁ•Ñ¼Ñ¡”™¥ÑÑ•½¹ÑÉ½°°¹•Ù•ÈÑÉ…•É…Ü™É½´Á¥á•±Ì¸(