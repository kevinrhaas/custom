# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-09-03 on his explicit
# instruction: "Create several tickets as needed in the queue file on dev and add these to
# the top of the queue file, since other tickets below are dependent and will help."
# Same day, later: T-0524 moved into the top band on his ruling "Fix the prompt and move
# T-0524 up" — the renderer smoke asserts a resident layer that no longer exists, so no
# full smoke can be green until it is repaired.
# Same afternoon: four more source tickets (T-0554..T-0557) placed at the top of that band on
# his instruction "Keep all of these tickets to queue near the top in the section where we are
# working the resident and household data expansion".
# Then T-0562 (the Newberry Genealogical Index, now on the Internet Archive) placed with them on
# his ask of the same afternoon.
# Before that, on 2026-08-30: "lots of nothing happened in the city which is bad. any decisions
# needed, update and improve the tickets to make progress." Earlier instructions:
# 2026-08-29 x2 (the newspaper stream to the top, then dependencies on visible items),
# 2026-08-28, 2026-08-27, 2026-08-23. Absent such an instruction, agents only APPEND
# (new) and REMOVE (done) — do not re-rank on your own judgement.
#
# WHY THIS ORDER CHANGED, and it is the whole point of the pass. Between 2026-08-29 and
# 2026-08-30 the loop merged 41 PRs and added ZERO buildings: 359 structure records
# before, 359 after. It was not idle — it modified 75 structure records, 98 assets, put
# a stove pipe on every roof and moved nine shops out of the yard — but a visitor
# walking the town saw the same town. The reason was structural, and T-0301 predicted
# it: every path to a NEW building ended at a question only the owner could answer, so
# the loop did the invisible work because the visible work was all blocked. Four of
# those questions were answered on 2026-08-30 and the tickets that spend the answers
# were at the BOTTOM of a 77-line queue, where no slice would ever reach them —
# including T-0429..T-0432, which are twenty roofs, and which the previous pass left
# there because an agent may not re-rank without being asked. This pass was asked.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. THE CITY GAINS SOMETHING FIRST. A ticket that adds a building, a person or a
#      trade to the scene outranks one that measures, grades or gates. The band at the
#      top is ordered by HOW MUCH it adds.
#   2. Then what those additions depend on, and the repairs that make them correct.
#   3. VISIBLE REFINEMENT next — the town changing rather than growing.
#   4. An INVISIBLE ticket outranks a visible one only when it BLOCKS it, and its band
#      has to say what it blocks.
#   5. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.
#
# `needs_bake: true` marks a ticket whose merge changes baked geometry. Those are the
# ones that put something in the scene — several are in the top band.
#
# Labels are regenerated from each ticket's own `title:`. If a label and its ticket
# disagree, the ticket wins (T-0217 records the restamp bug that caused one).
# NOTE ON `epic:` — the field has drifted to a default (mostly META, including
# newspaper reads and street work). The BANDS, not the epic, say where a ticket
# belongs. Correcting the field is worth a run of its own.

# --- THE RESIDENT SOURCE SWEEP → CONSOLIDATION → RESIDENTS/HOUSEHOLDS UPDATE — OWNER REQUEST,
# --- 2026-09-03, placed at the top on his instruction. His ask, verbatim: "create tickets to do
# --- more resident research transcription and analysis or extract find public sources or APIs to
# --- read and find data from the following reference materials, you should see them all in
# --- GitHub — Voter Roll; Census 1830 and 1840; Fergus; Swift walker; Hh porter. And then create a
# --- final ticket that does a review and consolidation of that research. Once complete i would
# --- like to begin to do and update of the resident and household data based on all of your deep
# --- research ... identifying as many residents of chicago circa 1835 ... then i would like a
# --- summary of what the residents and households look like ... Create several tickets as needed
# --- in the queue file on dev and add these to the top of the queue file, since other tickets
# --- below are dependent and will help. I am concerned that there are only adjudicated mappings
# --- through v4 and none other and we did at least 11 slices of residents to get to households
# --- but most of your census work needs to be published, I think." And: "these
# --- Chicago_1835_Best_Resident_Set_Research_v2.xlsx v3 and v4 should be somewhere" — ruled the same
# --- day: "They are lost; rebuild." His other three rulings of 2026-09-03 (publish = reference
# --- packages + the final audit; the 31 inf_ roofs stay as anonymous stock; the grading ladder is
# --- ratified) are quoted in the tickets they bind.
# ---
# --- ORDER = DEPENDENCY. T-0491 first because dev's gate is RED and every branch inherits it.
# --- T-0492 gives the six new source domains one schema and one gate before ten runs invent ten.
# --- Then the sweeps, which may run in parallel (one source each; the 1840 images, the Fergus
# --- volume and the unresearched 237 are pre-split so no ticket needs two runs). Then the second
# --- wave that consumes them (serial mapping, the 1840 crosswalk, the directory, the calibration,
# --- cohorts 13-15, the two publish halves). T-0513 consolidates ALL of it under the ratified
# --- ladder — do not take it while any sweep ticket is open. T-0514/T-0515 write the people;
# --- T-0516 finishes the reconstructed-roof half of the retirement; T-0517/T-0518 close with the
# --- summary and the index. A ticket whose inputs are open says so in its body: work the input.
# ---   wave 0  T-0491 T-0492
# ---   wave 1  T-0493 .. T-0503   (parallel)
# ---   wave 1  also T-0554 .. T-0557, T-0562  (added 2026-09-03 pm — the owner's five further sources)
# ---   wave 2  T-0504 .. T-0512   (parallel)
# ---   wave 3  T-0513
# ---   wave 4  T-0514 T-0515 T-0516
# ---   wave 5  T-0517 T-0518

# --- T-0524 sat here on the owner's ruling of 2026-09-03 — the smoke assertions that still
# --- described the reconstructed residents T-0489 retired, which made every full smoke on
# --- dev red. CLOSED in PR #696: parts 3 and 13 are green in both viewports. The band is
# --- kept as the record of why it was ranked here, not as a slot for anything else.

# --- FOUR MORE SOURCES — OWNER REQUEST, 2026-09-03 (afternoon), placed here on his instruction:
# --- "Keep all of these tickets to queue near the top in the section where we are working the
# --- resident and household data expansion, this is overall expansion because while you are
# --- parsing for residents and household people you might as well improve the business and
# --- structure and occupation and other surrounding data and attributes that will help us
# --- render the most complete reconstruction possible of chicago 1835". His four sources: the
# --- Old Settlers' receptions (chicagology 063), Norris's 1844 directory (HathiTrust), the
# --- Genealogy Trails Cook County site, and the Illinois land-sales database. They are wave-1
# --- sweeps: parallel with the others, and T-0513 (consolidation) waits on them like the rest.
# --- T-0562 joined them the same afternoon on his ask "make sure you have a resident household business
# --- city data improvement ticket for https://archive.org/details/chicago1835-newberry-genealogical-index
# --- if you do not already i am starting to move the research corpus to the internet archive".
# --- SPEND WHAT IS ALREADY READ — OWNER REQUEST, 2026-09-03 (evening). He asked, of the
# --- 1840 census reading tickets: "i see lots of research being done and some apparent findings
# --- from parsing but there are not outputs or updates to the household and resident data it
# --- seems, should i be concerned?" He was right. Measured that evening by the new
# --- tools/measure_research_spend.py: census_1840 held 562 names read off the sheets and a
# --- crosswalk of `passes: [], merges: [], refusals: []`. Four of 828 household records carried
# --- an 1840 link. Every reading ticket had been green; nothing had crossed into the town.
# ---
# --- THE MECHANISM, because it will recur otherwise. The wave order below is right and was
# --- never abandoned: wave 1 reads, wave 2 consumes. But wave 1 IS OPEN-ENDED — every new
# --- source the owner adds lands at the TOP of it (T-0554..T-0557 and T-0562 on 2026-09-03 am,
# --- then T-0566..T-0588) — so wave 2 was pushed down by every addition and never came up.
# --- Ten more 1840 reading tickets sat above T-0504/T-0505, which would have roughly doubled
# --- the unread-and-unruled pile before anything was ruled on.
# ---
# --- So the two wave-2 tickets that spend the 1840 names come up here, ahead of reading more.
# --- This is exemption-free under the visible-progress rule: T-0505 puts named people on cards.
# --- Dependency-safe: both consume names already on disk. T-0514/T-0515 (which WRITE the
# --- people) are deliberately NOT moved — they are wave 4 and sit behind T-0513, which may not
# --- be taken while any sweep ticket is open. The rest of the wave order below stands.
# --- CONSOLIDATION RUNS ALONGSIDE THE READS, NOT AFTER THEM — owner, 2026-09-03 (evening):
# --- "dont land those tickets at the very end maybe every few you should do that consolidation".
# ---
# --- THE RULE THIS BAND EXISTS TO ENFORCE: after every few source tickets close, the next run is a
# --- consolidation pass, not another source. Not at the end — there is no end. Wave 1 is open-ended
# --- by design (the owner adds sources as he finds them), so anything sequenced AFTER 'all sweeps'
# --- is sequenced after never. T-0513 carried exactly that bar and stood 31 tickets deep while the
# --- queue grew above it; T-0514/T-0515, which write the people, sat behind it.
# ---
# --- The scale, counted across the layer: 742 of 825 household records cite exactly ONE source, 70
# --- cite two, 13 cite three, and nothing cites more. Ninety per cent of the town rests on a single
# --- source while the crosswalks hold rulings nobody has spent. hh_carpenter_philo.json is the
# --- worked example, not the scope: it cites andreas_1884_v1 alone while the crosswalks have ruled
# --- six for the same man — poll 1833, tax 1833, poll 1834, the newspaper person, and two bridge
# --- tiers at VERY LIKELY 1835. The slot exists, the evidence is adjudicated, never introduced.
# ---
# --- T-0513 is now INCREMENTAL: it consolidates what is CLOSED and runs again. A pass that finds
# --- nothing newly closed says so and costs a run nothing. tools/measure_research_spend.py now
# --- measures BOTH hops — read vs ruled, and ruled vs ON A CARD. The second reads 109 rulings
# --- reaching a town person and 0 reaching their card; this band is what moves that number.
# --- …and T-0598 sits with it because it is what makes the consolidation MECHANICAL. T-0513 can
# --- only spend a ruling onto a card if the ruling says what it rests on; 103 of the 109 that
# --- reach a town person do not (civic's voter crosswalk: 99 matches, zero source ids). Without
# --- T-0598 the consolidation is a human rereading each crosswalk and inferring what it meant,
# --- which is the manual step this whole programme exists to stop relying on.

# --- ORDERED BY MEASURED YIELD — owner, 2026-09-03 (evening): "go ahead and reprioritize those
# --- items in the queue you think will yield the best research results, those ones at the top".
# ---
# --- This band is not a hunch. Every closed crosswalk on dev was counted, and the match rate
# --- differs by more than an order of magnitude by WHAT KIND of source it is:
# ---
# ---   source                       era                    ruled  matched   match %
# ---   civic poll/tax/voter lists    1833-1835              345      99      28.7%
# ---   1840 census heads             1840 (later)           498       5       1.0%
# ---   St Cyr church register        1834-1839              531       0       0.0%
# ---   Newberry index vol 1          index to later works   319       0       0.0%
# ---
# --- THE CATEGORY THAT WINS IS NARROWER THAN 'CONTEMPORARY', and the church row is why this was
# --- measured rather than guessed: the first draft of this band led with St Mary's baptismal
# --- register on the reasoning that 1833-35 beats 1840. St Cyr's register IS 1834-39, was read in
# --- full, and matched NOBODY — 434 of its 531 entries are unmatched. What actually predicts yield
# --- is a LIST THE TOWN MADE OF ITS OWN NAMED INHABITANTS, dated 1833-1836. Poll books, tax lists
# --- and land purchases name householders under their own names; a register names the Catholic
# --- families of a parish, and an index names works.
# ---
# --- So the promotions, in order, and each says which clause of the ratified ladder it feeds:
# ---   T-0557  land sales through 1836 — a government list of NAMED PURCHASERS at Chicago; the
# ---           closest thing in the queue to the civic lists that scored 28.7%.
# ---   T-0498  the 1830 named schedule — the only pre-1835 enumeration of the settlement, and
# ---           still unread; the repo holds county aggregates and no names.
# ---   T-0501  Hubbard — a resident naming his contemporaries with trade or address, which the
# ---   T-0499  ratified ladder admits as `inferred` in as many words. Fergus 26-29 is the same
# ---   T-0500  clause and is already deposited as 1.24 MB of unread OCR.
# ---   T-0506  the 1839 directory — later evidence, but nearer 1835 than the 1843/44 volumes.
# ---   T-0503  St Mary's baptismal register — on the ladder (baptism 1833-35) and deposited, so
# ---           it is here and not at the top: the measured church yield says it will not lead.
# ---
# --- WHAT MOVED DOWN, and it is a real call rather than a tidy-up. Eleven more 1840 census sheet
# --- reads and Newberry volumes 2-4 now sit below this band. Together they are ~8,000 more cards
# --- and, at their own measured rates, on the order of ten more matches. They are NOT withdrawn:
# --- the 1840 deposit's coverage.json is a completeness contract and the Newberry leads are real.
# --- They are simply no longer ahead of sources that pay ten to thirty times better per run.
# --- THE SAUGANASH DEEP DIVE — OWNER REQUEST, 2026-09-03, placed at the top on his
# --- instruction: "we need also an early visible ticket to do a deep dive on the sauganash
# --- hotel". He reported it from the dev preview: "there is an extra log structure you have in
# --- front and i think there is a structure missing but you have it on the front and they have
# --- it on the rear in pictures, and it looks like the full height of the main building and
# --- similar design as the main building appears to be almost the same size, it connects from
# --- the back and side in the images ... this is an attested structure we are putting fine
# --- points on it". And on the finish: "you are missing a fair amount of detail, like the door,
# --- the windows, the roof, etc." He deposited four views at
# --- chicago/reference/images/chicago/sauganash-hotel/ and supplied a plan sketch (transcribed
# --- in T-0616). VISIBLE work on the town's most-looked-at corner: T-0617 reads the plates,
# --- T-0626 spends the reading. Split from T-0616 because reading four plates and rebuilding
# --- the massing are two demonstrations. (T-0626 was filed as T-0618 and restamped: dev's own
# --- #749 had minted a T-0618 of its own for the Newberry volume-4 OCR reader.)

T-0500 — Fergus' Historical Series Nos. 26-29 sit as 1.24 MB of raw OCR with no text, no register and no claim read out of them: second half by page index



# --- The Newberry index SPEND, created 2026-09-03 (evening) on the owner's "and yes create a
# --- newberry spend ticket". Placed immediately above the three volume reads it depends on the
# --- absence of: volume 1 offered 319 leads and made 0 merges, and T-0578/T-0579/T-0580 would add
# --- roughly 8,000 more cards on top of a pile nothing has drawn from once. Move it if you would
# --- rather read all four volumes first — this placement is the same call as T-0504/T-0505 above.


T-0654 — The 1840 census image 33S7-9YYJ-B2 read line by line and closed against its own printed column totals
T-0527 — The 1840 census images 26-50: names and cells of the left sheets printed 227, 239 and 241
T-0657 — The 1840 census images 26-50: continuation sheets 33S7-9YYJ-FJ, -K2 and -L3 read line by line
T-0658 — The 1840 census images 26-50: continuation sheets 33S7-9YYJ-V4, -VJ and 33S7-9YYN-3CF6 read line by line
T-0659 — The 1840 census images 26-50: continuation sheets 33SQ-GYYJ-5H and 33SQ-GYYJ-9CZ read line by line
T-0529 — The 1840 census image 33S7-9YYJ-V2, printed 237, is a continuation sheet whose TOTAL column carries three-figure numbers and is not a household page
T-0496 — The 1840 census deposit is 75 page images and 210 heads on seven printed pages are the only names read from it: images 51-75
T-0497 — Dalton Data Bank holds a free 1840 Chicago head-of-household index by ward, and the repo cites it without reading it
T-0502 — H. H. Porter's Short Autobiography is a 66 MB scan with a garbled text layer, and nothing says whether it carries 1835 Chicago at all

T-0507 — 964 IPUMS 1840 households carry age-band and industry composition, and no calibration summary exists for the household reconstruction
T-0508 — 237 named residents have no research row: cohort 13 of 79
T-0509 — 237 named residents have no research row: cohort 14 of 79
T-0510 — 237 named residents have no research row: cohort 15 of 79
T-0511 — The pilot, pass 2 and pass 3 cohorts have no reference package while T-0478 to T-0486 do
T-0512 — T-0490 promised chicago/reference/resident-research/final/audit/ and closed without it


T-0514 — About half the voter-list men are in no resident record: mint residents from the consolidated civic, census, church and book evidence
T-0515 — 727 projected residents rest on a letter list alone: regrade every one a second source corroborates and attach its evidence
T-0516 — 31 inf_ roofs still stand as inferred_household for 101 households that no longer exist, and about 140 records name them in prose

T-0517 — What the residents and households look like: the summary the owner asked for, and residents_1835.md still documents the pre-rename model
T-0518 — The census, voter and research packages are on dev and indexed nowhere: index them and close the publish ask

# --- DEV'S OWN SMOKE IS RED, AND EVERY PR INHERITS IT — 2026-08-31.
# --- 2,693 of 18,893 drawn flower heads stand over nothing at desktop width. The
# --- same count, pose and worst offender appear on dev at 54921610 and on PR #560
# --- at ab4dad40, so no branch caused it. It is first here because a red dev makes
# --- every other ticket's gate unreadable: a run cannot tell its own failure from
# --- the one it inherited, and #591 and #432 may already be blocked by nothing but
# --- this. Fix it and their smoke may simply pass.

# --- WHAT A VISITOR ACTUALLY SEES — OWNER REPORTS, 2026-08-31. BOTH HAVE LANDED and
# --- the band is kept only to say so: T-0460, the plank walk's sawtooth against the
# --- dirt road, on 2026-09-03 (#676); T-0459, twenty signs mounted flat over doors
# --- and windows, on 2026-09-03 (#678). This band was the answer to the queue's own
# --- complaint that 41 merges added nothing a visitor could see, and it is answered.
# --- T-0426 IS RULED AND T-0461 IS WHAT THE RULING LEFT — 2026-08-31. The fence
# --- stays where the lot fronts (L160 read literally); the post follows the door,
# --- and that half has landed. What is left is that the Tremont House's goods sit
# --- on lot 7 while its own placement point falls 1.5 m outside it, so PR #562 is
# --- parked on T-0461 and on nothing else.
T-0426 — A shop addressed on a cross street improves the lot the plat fronts elsewhere, so 24.7 m of board fence lands across the Tremont House's goods
# --- T-0450 sits beside T-0448 because both make a gate unreadable: one leaves dev red
# --- so a run cannot tell its own failure from an inherited one, and this one misstates
# --- the cap three tickets measure their margins against. T-0181 (PR #591) is arguing
# --- against the wrong bound until it is fixed.
T-0450 — SMOKE-BUDGET.md compares a per-leg cap with a whole-gate total, and calls one runner a different machine from the other
# --- T-0454 is beside T-0450 for the same reason: it makes a gate's own instruction
# --- untrue. The gate says re-bake a stale asset; the bake, run on that exact tree,
# --- rebuilds nothing. PR #597 is blocked on this and nothing else.
T-0454 — The gate calls a GLB stale and the bake declines to rebuild it, so a stale asset cannot be cleared by baking

# --- THE WEST DIVISION IS WRONG ON THE GROUND — OWNER FAULT REPORT, 2026-08-31.
# --- Reported from the dev preview against the Thompson plat sheet. Three of its
# --- findings are already measured from the committed files: only TWO of the plat's
# --- five north-south West Division streets exist, carroll and fulton exist nowhere,
# --- and the one west-side spacing this project holds is 112.1 m against a South
# --- Division band of 119.2-123.4 m. The fourth — whether the whole grid sits one
# --- street west, so that `canal` is really Clinton — is a MEASUREMENT nobody has
# --- taken yet, and every building west of the river depends on the answer.
# --- This outranks the roof bands: those add buildings to ground that is correct,
# --- and this asks whether a quarter of the town is standing in the wrong place.
T-0444 — Measure the west bank of the South Branch and step the plat's sequence from it: is the line drawn as Canal really Clinton?
T-0445 — West Water, Jefferson and Des Plaines: the three West Division streets the plat carries and no committed file holds
T-0446 — Carroll and Fulton: two platted tiers the West Division has no street between
T-0447 — North Water Street's west end runs across Wolf Point, which the Thompson plat does not give it

# --- THE NORTH DIVISION AND THE WATER — OWNER MARK-UP OF THE DEV PREVIEW, 2026-08-31.
# --- Ordered by dependency, not by size. T-0453 is FIRST because both the street
# --- tickets measure against the bank, and the bank is what is in question: every
# --- planform in this project is traced from Wright 1834 and the owner reads the
# --- Thompson plat differently at Wolf Point. It also carries a named defect — a
# --- single vertex on the South Branch 9.4 m off its own neighbours, the worst in
# --- the feature. T-0451 is the North Division's missing grid: ONE north-south
# --- street stands north of the river where the plat carries a whole division.
# --- T-0452 is the sloughs: the plat draws three, this holds one, as a bare
# --- centreline with no banks — and they cross the ground T-0451 wants to plat.
T-0453 — The river banks are traced from Wright 1834 and the owner reads the Thompson plat differently at Wolf Point
T-0451 — Only one north-south street stands north of the river, where the Thompson plat carries the North Division's whole grid
T-0452 — The plat draws three sloughs off the Main Branch; this reconstruction holds one, as a centreline with no banks

# --- THE CITY GAINS PEOPLE AND ROOFS — FOUR OWNER RULINGS, 2026-08-30, each written
# --- into its ticket with its limits. This band exists because the last 41 merges added
# --- no buildings. Ordered by how much each one adds. TAKE FROM THE TOP.
# ---   T-0379  705 letter-list names -> the town goes 237 to 942 people (ruled: all 705)
# ---   T-0429..0432  twenty roofs across four South Water blocks, one block per run
# ---   T-0416  +12 documented shops take corner sides (ruled: a corner side IS a face)
# ---   T-0183  the 27 roofs of a block the river pinches out, returned to the South balance
# ---   T-0384  Holbrook's store, read as an ordinal off the corner rather than street-only
T-0429 — Open blk_south_water_lasalle: 8 roofs of headroom on three free lots
T-0431 — Open blk_south_water_clark: 4 roofs of headroom on two free lots
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed, and each one puts
# --- something in the scene or lets a documented person stand somewhere.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0418 — The 36 documented tradespeople whose trade the residents vocabulary has no word for
T-0414 — The street-face adoption refuses W. Montgomery a roof for being the bootmaker, and identity.json already ruled they are two houses
T-0412 — A building offered FOR SALE mints a placement reading on the vendor's own firm, so P. Pruyne & Co.'s store carries a corner it never stood on
T-0415 — John Wright's two buildings to let are named (east) and (west) and stand the other way round

# --- THE LOT GRID QUESTION — measure, THEN ask. Carrying out T-0009's ruling left the
# --- South Water corridor 8.58 m north of its own block faces, with a strip belonging to
# --- neither. T-0419's acceptance is the right shape (measure the strip on the ground,
# --- put the fork to the owner with costs, move nothing until he answers) and the four
# --- block tickets above are NOT blocked on it. Note the risk plainly: if the answer
# --- later moves the lot grid, roofs built on those lots move with their lots — which is
# --- how the grid works, and is not a reason to build nothing meanwhile.
T-0419 — The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither
T-0421 — Canal Street's three control points spread 2.33 m, so its corridor cannot be centred on any of them
T-0422 — The widened counterfactual deals a roof per street, and every roof a widening adds already fronts another street

# --- THE REPAIRS THE SEEDING READS — identity, anchors and placements. These do not add
# --- buildings themselves; they decide whether the buildings above land on the right
# --- names and the right corners. Cheap, and each one is a wrong building avoided.
T-0406 — 'the Tremont House' resolves to nothing, because the committed record is named 'Tremont House (the first)'
T-0403 — The Democrat's office keeps its 1834 corner through a merge, and the paper moved along South Water Street before the scene date
T-0396 — Newberry & Dole's partner is read as Oliver Newberry in 1834 and Walter L. Newberry in 1835, and the corpus cannot say which stood in the firm
T-0391 — Are 'Eagle Hotel' and 'the Eagle Hotel (Steele's)' one house, and no issue prints both
T-0407 — The same blacksmith notice is read as 'Matthias Nason & Co.' in one impression, and the partner-surname guard can never merge it
T-0408 — Four spellings of one Lake Street trade take four separate roofs, and the identity layer has judged none of them
T-0410 — The Howard fire-insurance agency passes between three houses, and the gazetteer has no relation that can hold it
T-0411 — A newspaper and its own printing office are two businesses, and the partner-surname guard can never join them
T-0413 — Six of T-0401's surname traps are one house on the printings, and the merge is unwritten
T-0398 — A firm's own style stands in its proprietor list, because a claim read the signature where a person was wanted
T-0395 — The New York House's footprint is graded reconstructed but its note cites a source, and the gate warns
T-0404 — 33 documented businesses will stand on a backdating liberty and LIBERTIES.md carries none of them
T-0405 — Adding one signboard repaints every board alphabetically after it, and some lose a line
T-0425 — A letter-list household's arrival bound is dated by the printing it was extracted from, not by the return, so nine printings of one list give nine different bounds
T-0424 — The 1 January 1834 letter list's printed length, and the names all nine printings lost, need the page images
T-0428 — The 1 April 1834 letter list has three positions no printing reads, and only the page images can say how long it was
T-0318 — The January 1834 letter list: the third printing repairs the A-H half, and the images are needed only for the rest

# --- VISIBLE REFINEMENT — the town changing rather than growing: the ground it stands
# --- on, the ordinances the papers yielded, the fort, what grows, and the cards a
# --- visitor opens. T-0219 is parked on PR #432.
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier

# --- SOUTH THROUGH TIME — OWNER EPIC, 2026-09-01. Continue T-0219's ground south
# --- through the 1812 Fort Dearborn battle corridor and the 1880s Prairie Avenue
# --- district. Shared geographic infrastructure comes first, then the 1812 natural
# --- landscape/first fort/route, then the later urban terrain, grid and mansion district.
# --- The 1812 work follows AGENTS.md's Indigenous-history review constraint: terrain,
# --- structures and documentary geography may proceed, but human depiction is not inferred.
T-0464 — Extend the shared south terrain from Madison through Cermak
T-0465 — Trace the South Branch and early lakefront through the expanded field
T-0466 — Build a south-terrain tiling and culling plan for a four-kilometre field
T-0467 — Add south-scene camera anchors, navigation and map extents
T-0468 — Create an e1812 natural terrain epoch for the Fort Dearborn battle landscape
T-0469 — Reconstruct the first Fort Dearborn complex as it stood in August 1812
T-0470 — Map the 15 August 1812 evacuation route and battle-location confidence zone
T-0471 — Build the 1812 lakeshore prairie, vegetation and landscape features
T-0472 — Build the 1812 interpretive scene with Indigenous-history review gates
T-0473 — Create an 1880s South Side terrain and urban-ground epoch
T-0474 — Reconstruct the 1880s Prairie Avenue street, parcel and service grid
T-0475 — Build the Prairie Avenue landmark mansion core
T-0476 — Fill the 1880s Prairie Avenue corridor with documented residences and outbuildings
T-0477 — Build the 1880s Prairie Avenue streetscape, vegetation and urban furniture

T-0435 — 30 of the 47 cat-and-clay stacks stand against an eave wall, and both the archetype and the fabric argument say gable
T-0334 — The hay-stacking ordinance walks a six-vertex boundary round the built town, and nothing draws or tests it
T-0436 — The corporation's limits have no committed geometry, and the fire ordinance binds only inside them
T-0266 — On a phone from across the river the stockade's picket rhythm falls under the pixel grid and beats
T-0332 — The sheet's one brick is called chimney_brick, and a wall now reads it
T-0277 — The mid and forb rings' outer edges are re-priced for a density handover, now the reach statistic is honest
T-0279 — 2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev
T-0280 — The far band's grass-or-flower split is made on the forb lattice's CLAMPED share
T-0302 — The .lib-body grid resolves toward max-content under all six other Evidence sections, and only the plants section is fixed
T-0268 — A building held under the standing constraint says so nowhere a visitor can see

# --- THE TRIANGLE AND DRAW-CALL BUDGET — invisible, and it gates EVERY visible ticket
# --- that adds geometry. The band at the top of this file is about to add twenty roofs,
# --- twelve shops and seven hundred people, so this is where the room for them comes
# --- from: the two AO tickets are the measured headroom.
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor

# --- MEASUREMENT, GATES AND PROVENANCE — invisible, and nothing below blocks the above
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0230 — Two named South Water frontages carry a reconstructed trade, so neither a signboard nor a hitching post will ever stand at them
T-0371 — The lattice path's block rotation is dead code that measure_rank_bias.mjs's drift guard pins in place
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0055 — Hold the Kinzie-view plate as a source record
T-0053 — A patched lit material silently inherits another layer's shader program
T-0037 — The liberties gate reads the whole Evidence panel, so a liberty saying 'Three of these' fails it
T-0030 — A queue card in Manager reading tickets.json
T-0255 — The dooryard planting rule reads every street in the town with no bound on reach, so a track across the river can turn a house's yard
T-0433 — T-0346's measured costs for the new desktop parts 4, 5 and 6 were never filed, and the two places they are written down disagree

# --- THE SMOKE AND ITS RUNNER — the evidence every ticket above owes. T-0346 cut the
# --- costliest desktop part into three so a run can take it; these are what remains.
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured

# --- THE PIPELINE AND ITS RUNNERS — invisible; the loop's own health
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0301 — Every visible ticket at the top of the queue is parked on hold or in flight, and five straight invisible runs merged under it
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw WITH THE EVIDENCE written into
# --- the ticket; never on a guess. T-0377 and T-0388 are twins of each other and one
# --- withdrawal closes both.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand
T-0377 — Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
T-0388 — Three derived records have drifted from their own generators on an unmodified dev, so every branch's gate is red

# --- NEWLY FILED — `ticket.mjs new` appends to the END of this file, so new tickets
# --- land under this line. NOT yet placed by the owner.
T-0438 — The letter-list cohort is 2.54 MiB of the published tree, and it is now the largest single item in it
T-0439 — Two pixel-sensitivity checks fail when parts 9-12 run together and pass when part 9 runs alone
T-0440 — Clark, Filer & Co.'s live placement is empty while three printings put its warehouse five doors east of Randolph
T-0449 — Four South Water frontage entries declare lots their runs never reach, and each hides its block's headroom
T-0522 — The dev gate has been red on 10 legs since PR #670 merged the recovered census bridge
T-0520 — The archetype builders compute their own opening rectangles beside the ones facade_openings states, and only a town-wide rebake can join them
T-0536 — The census_1840 domain declares its 25 read images in its own images[] shape, which the shared research-domain gate does not read
T-0537 — The web derivatives are stamped by an unpinned gltf-transform, so a release upstream restamps all 372 of them
T-0542 — Andreas dates the third town election twice — July 1835 and 5 August 1835 — and which one the 1835 poll list is decides whether 85 men stood on the scene date
T-0543 — The continuation half of printed pages 230 and 232 is on a right sheet nobody has identified, and it is not in images 26-50
T-0559 — The 1840 census printed pages 229 and 231: two independent cell readings disagree on 45 of 61 lines — reconcile them against the sheets, column by column
T-0577 — The Calumet Club's FIRST old-settlers reception, 27 May 1879: the registry of 149 settlers and their years of arrival, off the page images of Early Chicago (archive.org earlychicagorece00calu)
T-0581 — Moses and Kirkland's History of Chicago (1895) is the largest Chicago work the Newberry index points at that this project does not hold: read its Chicago and Cook County families for 1835 residents, households and businesses
T-0582 — The Chicago cards of the Newberry index also point at Moses's Illinois, historical and statistical (1888-92), the La Salle Book Co. Cook County volumes (1900, 1909), Wood's Chicago 1881 and Hurlbut's Chicago antiquities (1881), and none of the four is in this project's sources
T-0583 — The register of the Second Presbyterian Church of Chicago, 1842-92 (Grant), is cited on Newberry index cards for Chicago families and is not in this project's sources: find it, and read it back to the people who were here in 1835
T-0589 — Fergus's 1843 directory, page 1: the civic account — officers, courts, churches, societies, newspapers, fire and military companies, schools, the 1843 ward population count and the port's exports and imports for 1842-3
T-0592 — The fine well on lot 7 of block 16 is documented and the town has no well to draw it with
T-0593 — A documented 'large Dwelling-House' stands on a 5.36 x 6.38 m D3 count-unit, and the block's family mix was dealt before the address resolved
T-0594 — Hubbard's arrival year is graded 'reconstructed' citing nothing, and Hurlbut prints the sentence it wanted: Montreal 13 May 1818, Mackinaw 4 July, Chicago the last day of October or first of November
T-0595 — jb_beaubien_homestead has no origin: Hurlbut says it was the United States Factory House, bought from the government in 1822 and moved into by Beaubien
T-0596 — About 130 named articles of the Chicago Indian trade, itemised in the American Fur Company's own book: rule on what the town may show and letter nothing without it
T-0597 — James Kinzie and John Harris Kinzie are half brothers and the two household records do not say so
T-0600 — The Newberry index reads a state banner as a card body, and a wrecked call number as ', Ill.' — four and one of forty sampled cards
T-0601 — A column sliver is kept as a second, truncated copy of a card the neighbouring pass read in full, and nothing counts how many
T-0602 — The research-spend ratchet counts a precision sample as reading, and an unanchored refusal as nothing
T-0605 — The 1830 schedule's district runs on past leaf n584 and those leaves are unread: finish Peoria & Putnam & territory attached
T-0609 — The 1835 land purchasers hold tracts and the structures hold footprints, and nothing joins them: resolve every land_sales tract to the ground and write land_owner onto the structures it reaches
T-0610 — Three sections of T39N R14E were truncated at the land-sales database's 150-row ceiling, and the ring townships are unread: finish the Illinois land tract sales around Chicago
T-0611 — Fergus 1839, the appendices: the city register, the 1837 charter election and its list of voters for mayor, the Fort Dearborn Addition lot sales and the population table
T-0619 — Volume 4 read by OCR, pages 1-306: the shards
T-0620 — Volume 4 read by OCR, pages 307-612: the shards
T-0621 — Volume 4 read by OCR, pages 613-918: the shards, then stitch, re-parse and re-sample the volume
T-0629 — 33S7-9YYJ-6H: the slaves, pensioners, deaf/dumb/blind/insane and schools blocks, and the 1 and 40 at the head of the schools block
T-0647 — 33S7-9YYJ-5V's six 'reference pair' readings are 11 and the digit key from a sheet that closes says they are 4
T-0649 — Settle whether the Eliza Chappel shore drawing is a fifth view of the Sauganash's log annex, by reading its lighthouse
T-0650 — The Illinois Catholic Historical Review says where St Cyr's first church stood, and nothing has read it out
T-0652 — 33S7-9YYJ-8D's six two-stroke totals, re-read against 6H's footing: its column over-runs its printed 106 by 15
