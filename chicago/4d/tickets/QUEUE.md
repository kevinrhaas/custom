# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-30 on his explicit
# instruction: "lots of nothing happened in the city which is bad. any decisions
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

# --- DEV'S OWN SMOKE IS RED, AND EVERY PR INHERITS IT — 2026-08-31.
# --- 2,693 of 18,893 drawn flower heads stand over nothing at desktop width. The
# --- same count, pose and worst offender appear on dev at 54921610 and on PR #560
# --- at ab4dad40, so no branch caused it. It is first here because a red dev makes
# --- every other ticket's gate unreadable: a run cannot tell its own failure from
# --- the one it inherited, and #591 and #432 may already be blocked by nothing but
# --- this. Fix it and their smoke may simply pass.

# --- WHAT A VISITOR ACTUALLY SEES — OWNER REPORTS, 2026-08-31. Both are visible
# --- faults at walking distance, and the owner asked for T-0460 SOONER THAN MOST:
# --- the plank walk's sawtooth against the dirt road is among the first things in
# --- view. T-0459 is 20 signs mounted flat on facades by a generator that mentions
# --- doors sixteen times and never once as geometry. Both are cheap beside the
# --- ground work below, and this band is the answer to the queue's own complaint
# --- that 41 merges added nothing a visitor could see.
# --- T-0426 IS RULED AND T-0461 IS WHAT THE RULING LEFT — 2026-08-31. The fence
# --- stays where the lot fronts (L160 read literally); the post follows the door,
# --- and that half has landed. What is left is that the Tremont House's goods sit
# --- on lot 7 while its own placement point falls 1.5 m outside it, so PR #562 is
# --- parked on T-0461 and on nothing else.
# --- T-0450 sits beside T-0448 because both make a gate unreadable: one leaves dev red
# --- so a run cannot tell its own failure from an inherited one, and this one misstates
# --- the cap three tickets measure their margins against. T-0181 (PR #591) is arguing
# --- against the wrong bound until it is fixed.
# --- T-0454 is beside T-0450 for the same reason: it makes a gate's own instruction
# --- untrue. The gate says re-bake a stale asset; the bake, run on that exact tree,
# --- rebuilds nothing. PR #597 is blocked on this and nothing else.

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
T-0451 — Only one north-south street stands north of the river, where the Thompson plat carries the North Division's whole grid

# --- THE CITY GAINS PEOPLE AND ROOFS — FOUR OWNER RULINGS, 2026-08-30, each written
# --- into its ticket with its limits. This band exists because the last 41 merges added
# --- no buildings. Ordered by how much each one adds. TAKE FROM THE TOP.
# ---   T-0379  705 letter-list names -> the town goes 237 to 942 people (ruled: all 705)
# ---   T-0429..0432  twenty roofs across four South Water blocks, one block per run
# ---   T-0416  +12 documented shops take corner sides (ruled: a corner side IS a face)
# ---   T-0183  the 27 roofs of a block the river pinches out, returned to the South balance
# ---   T-0384  Holbrook's store, read as an ordinal off the corner rather than street-only
T-0431 — Open blk_south_water_clark: 4 roofs of headroom on two free lots
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed, and each one puts
# --- something in the scene or lets a documented person stand somewhere.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street

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
T-0449 — Four South Water frontage entries declare lots their runs never reach, and each hides its block's headroom
T-0437 — The bake smoke clones a 3.2 GB monorepo to test one subtree, and that checkout has killed seven legs at the cap

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
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
T-0497 — Dalton Data Bank holds a free 1840 Chicago head-of-household index by ward, and the repo cites it without reading it
T-0508 — 237 named residents have no research row: cohort 13 of 79
T-0509 — 237 named residents have no research row: cohort 14 of 79
T-0520 — The archetype builders compute their own opening rectangles beside the ones facade_openings states, and only a town-wide rebake can join them
T-0522 — The dev gate has been red on 10 legs since PR #670 merged the recovered census bridge
T-0536 — The census_1840 domain declares its 25 read images in its own images[] shape, which the shared research-domain gate does not read
T-0537 — The web derivatives are stamped by an unpinned gltf-transform, so a release upstream restamps all 372 of them
T-0559 — The 1840 census printed pages 229 and 231: two independent cell readings disagree on 45 of 61 lines — reconcile them against the sheets, column by column
T-0581 — Moses and Kirkland's History of Chicago (1895) is the largest Chicago work the Newberry index points at that this project does not hold: read its Chicago and Cook County families for 1835 residents, households and businesses
T-0612 — dev's gate is red: two merged readings raised no ceiling, and every branch after them inherits the failure
T-0662 — check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated
T-0672 — The three ceilings were raised for one parcel on 2026-09-03 and light's floor was spent: re-measure once #432 lands and take every tier back down
T-0673 — The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured
T-0674 — A bot-opened PR never runs the dev gate before merge, and two of them broke dev
T-0812 — The Steamboat Hotel's placement reads Kinzie Street at local N +276 and the committed kinzie record is at N +252.8
T-0688 — The wagon-variety gate counts street bearings, so re-deriving a street took it from 9 buckets to 7 and it is at its floor of 8

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0677 — Thirty-five land purchasers are matched to households and not one is on the card: spend the land-sales resident crosswalk, tract, date and price
T-0678 — The old_settlers domain holds 18 merges and 57 death-notice matches naming a town person, is registered in no domains.json, and reaches neither hop of the spend measure
T-0681 — T-0666's Fort Dearborn lot crosswalk matches 11 bidders to residents and 3 of them are on no card: spend the lot sale onto the people it names
T-0683 — Ten check.sh checks and six part-13 smoke assertions are red on dev after PR #670, on five independent causes
T-0685 — Georeference the Thompson 1830 plat at the forks and measure its bank against the Wright 1834 line for the owner's ruling
T-0689 — The West Division's lot dimensions and lot-counts are still unread off the Thompson plat, and T-0444 closed without them
T-0690 — dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4
T-0691 — The letter-list cohort is 76 households out of step with its own derivation, and check.sh never looks
T-0693 — Edward Richards Allen's card says occupation none_recorded while the same file quotes him as a druggist twice: say what is known and when, not nothing
T-0694 — M'Cormick & Moon read as a Chicago hatter although their own notice gives No. 109 Jefferson Avenue, Detroit
T-0695 — A garbled printed forename refuses a match the reader can still make: C!;as. for Chas., J>ctij for John, Iia for Ira
T-0696 — The directory crosswalks want a second discriminator: a trade separates 6 of the 33 contested groups and an 1835 premises 8, and the rule has none
T-0697 — The land-sales resident crosswalk stops binding when a surname stops being unique: 531 new people cost it three rulings with nothing new read
T-0698 — The 1840 census heads crosswalk is derived against 849 residents and 17 sheets, and the town now holds 1,404 and 25
T-0700 — The nine ring purchasers that meet a person the town already holds are proposals nobody has ruled on
T-0714 — The 1840 census crosswalk is 235 named heads stale on dev and no gate says so: 498 on disk against 733 read from the pages
T-0715 — data/residents/index.json rows go stale for any household no minting pass owns, and only validate.py notices
T-0716 — Test the one candidate T-0663 left standing: is the Eliza Chappel shore drawing William Mark Young's 'Chicago's First School House' of about 1925
T-0717 — The first Catholic church still stood at State and Lake in June 1837, and st_marys_church.json ends its phase on 1836-12-31
T-0718 — Is jb_beaubien_homestead the Factory House or the house Beaubien moved to: John Dean is the hinge, and the SW-versus-NE corner turns on it
T-0720 — 864 people carry a rung the ladder already ruled and no pass has written onto their card, 76 of them attested: spend the proposal onto the cards the civic mint does not own
T-0721 — Three town cards are named from an OCR misreading of an initial — 8. G. Abbot, A. 8. Perry, James I1. Gabbs — so no identity can be built from them
T-0722 — The published tree is at the 32 MB Pages ceiling on dev alone, so any PR that adds a byte cannot go green
T-0723 — One identity, two town cards: Mrs Rufus Brown is folded onto her husband by the honorific strip, and N. R. Norton is Nelson R. Norton carried twice
T-0724 — The splitter's four-token forename cap turns away Rev. John Mary Irenaeus St Cyr, the parish priest whose own register is rung G2c
T-0725 — The published tree is 900 bytes under the 32 MB ceiling on dev, so the next PR that adds anything at all fails the gate
T-0727 — Budget the walkthrough's boot payload, which is what a visitor actually downloads, rather than the whole published tree
T-0728 — dev's own gate is red before any branch touches it: three research cohorts are stale and seven household records no longer re-derive from the ladder
T-0729 — dev's gate is red on an untouched dev again: 0 platted cross-street faces, blk_washington_clark off the ground, the southern coverage claim and the far-timber census
T-0731 — The published site is 845 bytes under its 32 MB budget on dev, so the next changelog entry fails the gate
T-0732 — James Kinzie's card says he is half brother to Robert A. Kinzie too, in prose, citing nothing — and there are two Robert Kinzie households
T-0733 — 103 people carry a conflicting-evidence flag the final audit can see and no ruling reaches
T-0734 — 14 of 1,404 people have a stated relationship to anybody else: the kinship the sources already print
T-0736 — Printed 232's continuation leaf is not in this deposit: find it in FamilySearch collection 1786457 or on the National Archives microfilm, and read the 31 households' industry, pension and schools cells
T-0743 — 33S7-9YYJ-FJ read line by line: the TOTAL column, and whether the footing that refused the printed-207 pairing is 135 or 138
T-0744 — 33S7-9YYJ-L3 read line by line: the TOTAL column, and the line count the contact sheet and the strip disagree on
T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line
T-0748 — The 1840 census continuation sheet 33SQ-GYYJ-5H read line by line, off a pale exposure that hides entries at the standard ink threshold
T-0753 — Hurlbut gives Gurdon Hubbard a birth and a Montreal origin, and the household record holds neither
T-0754 — 33S7-9YYJ-6H's SCHOOLS footing under No. of Scholars is written and does not read: two glyphs where a 40 would stand, and no bowl
T-0755 — The seventh SCHOOLS column of 33S7-9YYJ-6H, No. of Scholars at public charge, is in the binding gutter and is recorded unread rather than blank
T-0757 — The 1830 division's recapitulation counts 53 and 88 families on leaves that carry 55 and 39: re-count both against the enumerator's column
T-0758 — The Harrison plan names six things on the fort's ground that this model has never drawn: Well, Wash house, Big Barn with Cupola, Shop, Out Buildings and the Fort Cemetery
T-0759 — Chicago drank from the lake by cart in 1835 and the town has no waterman: the hogshead cart, the watering place at the foot of Randolph and the barrel at the door
T-0761 — The banded rule profile read_census_continuation.py needs: the printed rules of a continuation leaf lean up to 41 px and one profile over the whole body loses them
T-0762 — The 1840 census image 26-50: continuation sheet 33S7-9YYJ-VJ read line by line
T-0763 — check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them
T-0764 — A cohort manifest's starting_* snapshot is rewritten every time the manifest is regenerated, so the freeze records today's tree rather than the day it was fixed
T-0765 — A page number in a citation is read as the state: ', 111,' after a digit run, 65 kept cards across the four volumes
T-0766 — The Illinois abbreviation still matches on the wreck of a word — 'Eng.', an author's initials, a France card — and those are the bad keeps the four precision samples have left
T-0768 — West Water Street north of Lake: the 1839 directory attests the reach, and a bank offset there runs through the Wolf Point cluster
T-0769 — A card body can OPEN with the TAIL of the card in the column to its left, so a locality is matched on text that is not on the card
T-0770 — south_branch_raft_bridge glosses West Water Street as 'now Canal Street', and the committed canal stands a plat module west of it
T-0771 — Clark, Filer & Co.'s 'five doors east of the corner of Randolph st.' names one street in the anchor and the other in the placement, so the corner-ordinal reader never sees a corner
T-0772 — Twelve dooryard gardens went with the retired households: should a garden follow the house or the household?
T-0773 — Seven houses hold a printed address that a later printing outranks, and only an anchor_changes rule may reorder them
T-0774 — The publish budget has 944 bytes left, and 2.8 MB of it is changelog.js kept twice
T-0776 — A full tools/web_derivatives.sh rewrites 348 derivatives with identical byte counts: the derivative step is not reproducible
T-0777 — assets/manifest.web.json's $note is rewritten with escaped em-dashes, so its own generator does not reproduce what dev committed
T-0778 — Block 5 lot 5 of the Fort Dearborn sale has no claim at all: the row map never gathered it, and the printed page 47 brace covers it
T-0779 — The bidder column of Fergus 1839's Fort Dearborn sale is still the OCR's: three ditto marks it mapped no ink for, and the names it mangled
T-0781 — tools/check.sh has been red on dev since before 2026-09-05: four checks fail on an untouched checkout
T-0783 — The 16-by-30-foot house at Lasalle and Lake is a documented Chicago building with a corner and a footprint, and the town places it nowhere
T-0787 — The Wright 1834 sheet has arrived whole at 600 dpi and nothing can cite it yet: register the National Archives reproduction beside the BPL master, in its own pixel space, with the scale bar as the check
T-0788 — Wright numbers all 58 blocks of the Original Town and this project has read six: read the rest — the Public Square is block 39 — so a lot-and-block address can finally land
T-0789 — Kinzie's Addition is on the sheet whole — 54 numbered blocks, 13 named streets, the Kinzie Block and the river-front water lots — and the North Division carries four streets
T-0790 — Wabansia, surveyed 1831, is drawn whole north of Kinzie Street — eight streets, some 79 blocks and a water-lot tract on the North Branch — and the town has none of it
T-0792 — The legend's nine coloured tracts are the town's survey history — who surveyed what ground, when, for whom — and the project has no tract layer
T-0794 — The two branches run to the sheet's edges and the town's traces stop at the box: the South Branch through the School Section and the North Branch through Wabansia, off Wright
T-0795 — Every watercourse Wright draws, counted on the new sheet: the three Main Branch sloughs re-checked, and any the BPL tracing windows never covered
T-0796 — The small tract north of Kinzie Street lettered Michigan St — small parcels and an alley where every neighbour is whole blocks, and a road curving north through it — is unidentified: which survey, which legend swatch, and what the sources call it
T-0797 — The School Section's grid and streets: 142 blocks numbered off the sheet, four named and eight unnamed tiers with the unworn status the owner read, and the three Reserved blocks tested against the 1833 sale
T-0798 — Spend the 125 land-sale rows onto the School Section's numbered blocks: purchaser onto ground, dated to the sale
T-0799 — Trace the whole east edge off the full sheet: both piers, the cut, the sand bar to its tip, the old channel to where Wright closes it, and the shore to the sheet's bottom margin — one run, no window
T-0800 — The mouth as built: the piers as phased structures at their 1835 length, the bar's height argued, the reservation's blue edge and the lighthouse checked, and the epoch re-baked closed
T-0801 — The pre-fire viewer at /chicago/pre-fire/viewer/ shows 1834 through Hathaway only: put the Wright sheet beside it as the year's second view, with its provenance row, its checksum, and the mirror re-copied
T-0802 — A ticket whose PR merged can sit 'claimed' forever, because nothing compares ticket state against the PRs that landed
T-0803 — The published tree is 936 bytes under the 32 MiB budget, so no PR that publishes anything can pass validate.py again
T-0804 — Minifying the published mirror's JSON is a measured 1.99 MB: decide whether the record must stay readable at its own URL
T-0810 — The OCR re-read of Newberry volume 4 has never been checked for column slivers: T-0601's pass ran over the text-layer reading the re-read replaced

