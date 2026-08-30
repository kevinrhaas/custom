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

# --- THE CITY GAINS PEOPLE AND ROOFS — FOUR OWNER RULINGS, 2026-08-30, each written
# --- into its ticket with its limits. This band exists because the last 41 merges added
# --- no buildings. Ordered by how much each one adds. TAKE FROM THE TOP.
# ---   T-0379  705 letter-list names -> the town goes 237 to 942 people (ruled: all 705)
# ---   T-0429..0432  twenty roofs across four South Water blocks, one block per run
# ---   T-0416  +12 documented shops take corner sides (ruled: a corner side IS a face)
# ---   T-0183  the 27 roofs of a block the river pinches out, returned to the South balance
# ---   T-0384  Holbrook's store, read as an ordinal off the corner rather than street-only
T-0379 — The letter-list names the post office printed in a single return, and the change of scale they put to the town
T-0429 — Open blk_south_water_lasalle: 8 roofs of headroom on three free lots
T-0430 — Open blk_south_water_franklin: 4 roofs of headroom on two free lots
T-0431 — Open blk_south_water_clark: 4 roofs of headroom on two free lots
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots
T-0416 — Wm. Sabine, John Dave and the Dearborn wine store: the three storefronts the street-face policy refuses for want of a fronting roof
T-0183 — The Market and South Water corner needs one control point, and the node rule may not be able to make it
T-0384 — John Holbrook's store takes its door on South Water Street, one door from Dearborn

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed, and each one puts
# --- something in the scene or lets a documented person stand somewhere.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0375 — Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand
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
T-0409 — A change can land on dev with no changelog entry, and one did today
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
T-0438 — The run grading criterion is read two ways — the crosswalk's scheduling rank and the building's own size — and the two disagree the first time an H roof stands beside D roofs
T-0439 — blk_south_water_dearborn keeps no lot open, because the owner's business-front clause and the density standard's closing clause cannot both hold on a built-out block
T-0440 — Where the anonymous-block programme's committed ground runs out, now that the four South Water blocks T-0420 held are dealt
T-0441 — The balanced rung is full again: dev stands 1,566 triangles under a ceiling this project has twice refused to raise, and the queue's whole top band is bigger than that
