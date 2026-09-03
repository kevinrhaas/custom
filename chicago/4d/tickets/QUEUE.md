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
T-0460 — The plank walk meets the dirt road in a jagged sawtooth, and it is the first thing a visitor sees
# --- T-0426 IS RULED AND T-0461 IS WHAT THE RULING LEFT — 2026-08-31. The fence
# --- stays where the lot fronts (L160 read literally); the post follows the door,
# --- and that half has landed. What is left is that the Tremont House's goods sit
# --- on lot 7 while its own placement point falls 1.5 m outside it, so PR #562 is
# --- parked on T-0461 and on nothing else.
T-0426 — A shop addressed on a cross street improves the lot the plat fronts elsewhere, so 24.7 m of board fence lands across the Tremont House's goods
T-0461 — The Tremont House's goods are laid on lot 7, which its own placement point falls outside — one building's goods on another lot's frontage
T-0459 — Signboards are mounted over doors and windows, when the same wall has blank face to put them on
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
T-0430 — Open blk_south_water_franklin: 4 roofs of headroom on two free lots
T-0431 — Open blk_south_water_clark: 4 roofs of headroom on two free lots
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed, and each one puts
# --- something in the scene or lets a documented person stand somewhere.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0423 — G. Spring's large dwelling-house and fine well stands on lot 7 of block 16, where an anonymous roof stands now
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

# --- RESIDENT / HOUSEHOLD EVIDENCE SYNTHESIS — OWNER REQUEST, 2026-09-02.
# --- The twelve completed research cohorts are inputs. Run in dependency order: adjudicate,
# --- promote attested facts, promote inferred/projected residents while retiring reconstructed
# --- people, then audit the census/research synthesis.
T-0521 — dev's own check.sh gate is red in ten steps since the 1840 census merge, so no branch can prove itself
