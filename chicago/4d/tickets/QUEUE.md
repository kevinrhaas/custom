# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-29 (second pass that day)
# on his explicit instruction: "any tickets you recommend prioritizing in the queue
# because of dependencies on visual items? You can improve reorganize the queue, keep
# the newspaper stream near the top until we complete it for now." Earlier instructions:
# 2026-08-29 (first pass — the newspaper stream to the top), 2026-08-28 (the NEWSPAPERS
# band after the visible bands, now superseded), 2026-08-27 and 2026-08-23 (visible
# progress first). Absent such an instruction, agents only APPEND (new) and REMOVE (done)
# — do not re-rank on your own judgement.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. A RED DEV GATE OUTRANKS EVERYTHING. While check.sh fails on an unmodified dev,
#      every branch is red before it changes a line and every run pays T-0215's cost
#      proving its red is inherited. One ticket, and it is the top of the file.
#   2. THE NEWSPAPER STREAM RUNS NEXT until it is finished (owner, 2026-08-29): identity
#      hygiene cleans what the register mints, the seeding policy decides how much of the
#      town the papers can reach, and the seeding itself is the visible payoff.
#   3. VISIBLE NEXT. AGENTS.md's test — when this merges, what is different in a
#      screenshot taken from the same spot? "See" means in the 3-D scene or on a card
#      a visitor opens. A gate, a metric, a source record and a refactor are not.
#   4. An INVISIBLE ticket outranks visible ones only when it BLOCKS them, and the
#      band it sits in has to say what it blocks.
#   5. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.
#
# Labels on these lines are regenerated from each ticket's own `title:` field. If a
# label and its ticket disagree, the ticket wins — one line was found mislabelled
# on 2026-08-27, damage from the `ticket.mjs restamp` bug that T-0217 records.
#
# NOTE ON `epic:` — 55 of the 74 tickets queued on 2026-08-29 carried epic META,
# including newspaper reads, storefront placements and street work. The field has
# drifted to a default and the BANDS below, not the epic, are what say where a ticket
# belongs. Correcting the field is worth a run of its own; nothing here depends on it.

# --- DEV IS RED. TAKE THIS FIRST — measured on an unmodified origin/dev at 9b6e3276,
# --- 2026-08-29: three check.sh steps fail, all on one cause, left by the most recent
# --- merge (#536). Every branch cut from dev inherits it.

# --- THE NEWSPAPER STREAM (a) IDENTITY HYGIENE — the owner keeps this stream near the
# --- top until it is done. These come FIRST inside it because the register and the
# --- seeding SPEND the gazetteer: a firm minted twice, a surname that can never join its
# --- forename, or a tavern minted as a person becomes a wrong building once seeded.
# --- Cheap (mostly S/XS) and each one makes the seeding below more accurate.

# --- THE NEWSPAPER STREAM (b) THE POLICY THAT DECIDES HOW MUCH TOWN THE PAPERS REACH.
# --- T-0354 shipped in #551 on 2026-08-29: the owner's ruling — a street-only
# --- business adopts a reconstructed roof already standing on that street face, never
# --- claiming a lot — is now docs/STREET-FACE-ADOPTION.md, derived by
# --- tools/adopt_street_faces.py and gated in check.sh. T-0357 is its companion.

# --- THE NEWSPAPER STREAM (c) THE VISIBLE SEEDING — documented storefronts and people
# --- standing in the model. This is the payoff the whole epic was for. T-0358 sits here
# --- rather than with the streets because the corpus's ONLY lot-and-block address cannot
# --- be used until the Thompson plat's block numbering is committed.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0375 — Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand

# --- THE NEWSPAPER STREAM (d) WAITING ON THE OWNER'S PAGE IMAGES — each needs scans
# --- opened that live outside the repository. Workable the day the images are supplied;
# --- until then a run should take something above instead.
T-0318 — The January 1834 letter list: the third printing repairs the A-H half, and the images are needed only for the rest
T-0305 — Four readings the American contradicts itself on need the page images: the tailor's street, which Water street two forwarding houses stood in, and the corner of Cobb's saddlery

# --- THE TOWN GROWS AGAIN — UNBLOCKED BY THE OWNER, 2026-08-29. T-0365 measured that
# --- the anonymous-block programme had NO unblocked ground left: every platted block with
# --- headroom was gated on T-0009 or T-0183, both blocked-owner. Both are now answered
# --- (the rulings are written into the tickets), which frees ~20 roofs on four South Water
# --- blocks and 27 more on blk_south_water_market — the largest visible win available.
# --- AND THE 27 ARE NOT THERE, measured 2026-08-30 by T-0183 (PR #573): closing South
# --- Water's west end onto Market emits blk_south_water_market as a bowtie, and carried as
# --- far north as the committed waterline allows the block has 2.8 m of depth at Market
# --- against the 24.384 m one platted lot fronts. It is a wedge the South Branch pinches
# --- out, and T-0183 is back with the owner on what to do with it. The ~20 roofs T-0009
# --- freed are unaffected.
T-0365 — The anonymous-block programme has no unblocked ground left: every block with headroom is on the South Water reach T-0009 holds open

# --- THE RUNS CANNOT PROVE THEMSELVES — invisible, and it blocks the EVIDENCE every
# --- visible ticket owes. T-0346 is the sharp one: desktop stage 4 no longer fits the
# --- ten-minute foreground ceiling, so no steward run can complete it at all, and three
# --- PRs tonight had to say so instead of reporting a result. The two order-dependent
# --- gates below make a green run and a red run of the same tree.
T-0346 — Desktop smoke stage 4 no longer fits the ten-minute foreground ceiling, so no steward run can take the whole desktop gate
T-0349 — The signboard gate is red when stage 1 runs before it and green when stage 2 runs alone
T-0369 — Desktop stage 8's panel walk is red when stage 1 runs before it and green when stage 8 runs alone
T-0235 — The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap
T-0173 — The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured
T-0170 — The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner

# --- VISIBLE: THE GROUND, THE FORT, AND WHAT THE ORDINANCES PUT ON EVERY ROOF.
# --- T-0219 is parked on PR #432. T-0333 and T-0334 are two ordinances the papers
# --- yielded that nothing draws yet — a stove pipe on every roof in the town, and the
# --- hay-stacking boundary.
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier
T-0333 — Every stove pipe in the town owes eighteen inches above its roof, and the ordinance of 5 August 1835 says so
T-0334 — The hay-stacking ordinance walks a six-vertex boundary round the built town, and nothing draws or tests it
T-0266 — On a phone from across the river the stockade's picket rhythm falls under the pixel grid and beats
T-0332 — The sheet's one brick is called chimney_brick, and a wall now reads it

# --- VISIBLE: WHAT GROWS, WHAT A PHONE SEES, AND THE CARDS A VISITOR OPENS
T-0277 — The mid and forb rings' outer edges are re-priced for a density handover, now the reach statistic is honest
T-0279 — 2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev
T-0280 — The far band's grass-or-flower split is made on the forb lattice's CLAMPED share
T-0302 — The .lib-body grid resolves toward max-content under all six other Evidence sections, and only the plants section is fixed
T-0268 — A building held under the standing constraint says so nowhere a visitor can see

# --- THE TRIANGLE AND DRAW-CALL BUDGET — invisible, and it gates EVERY visible ticket
# --- that adds geometry. The town is about to gain 47 roofs and 49 trades from the two
# --- bands above, so this is where the room for them comes from: the two AO tickets are
# --- the measured headroom, and T-0364 is 7.2 per cent of the published payload.
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

# --- THE PIPELINE AND ITS RUNNERS — invisible; the loop's own health. T-0238 gained a
# --- second data point on 2026-08-29: T-0377 and T-0388 are the same defect filed twice
# --- by two runs that could not see each other, this time through `new` and not `claim`.
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0301 — Every visible ticket at the top of the queue is parked on hold or in flight, and five straight invisible runs merged under it
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw WITH THE EVIDENCE written into
# --- the ticket; never on a guess. All five were measured green on an unmodified dev at
# --- 9b6e3276 on 2026-08-29. T-0377 and T-0388 are twins of each other and one withdrawal
# --- closes both; the withdrawing run still owes which merge repaired them and whether
# --- the poplar row they predicted losing actually left the town.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand
T-0377 — Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
T-0388 — Three derived records have drifted from their own generators on an unmodified dev, so every branch's gate is red

# --- NEWLY FILED — `ticket.mjs new` appends to the END of this file, so new tickets
# --- land under this line. NOT yet placed by the owner.
T-0395 — The New York House's footprint is graded reconstructed but its note cites a source, and the gate warns
T-0396 — Newberry & Dole's partner is read as Oliver Newberry in 1834 and Walter L. Newberry in 1835, and the corpus cannot say which stood in the firm
T-0391 — Are 'Eagle Hotel' and 'the Eagle Hotel (Steele's)' one house, and no issue prints both
T-0407 — The same blacksmith notice is read as 'Matthias Nason & Co.' in one impression, and the partner-surname guard can never merge it
T-0408 — Four spellings of one Lake Street trade take four separate roofs, and the identity layer has judged none of them
T-0406 — 'the Tremont House' resolves to nothing, because the committed record is named 'Tremont House (the first)'
T-0403 — The Democrat's office keeps its 1834 corner through a merge, and the paper moved along South Water Street before the scene date
T-0404 — 33 documented businesses will stand on a backdating liberty and LIBERTIES.md carries none of them
T-0405 — Adding one signboard repaints every board alphabetically after it, and some lose a line
T-0409 — A change can land on dev with no changelog entry, and one did today
T-0410 — The Howard fire-insurance agency passes between three houses, and the gazetteer has no relation that can hold it
T-0411 — A newspaper and its own printing office are two businesses, and the partner-surname guard can never join them
T-0412 — A building offered FOR SALE mints a placement reading on the vendor's own firm, so P. Pruyne & Co.'s store carries a corner it never stood on
T-0413 — Six of T-0401's surname traps are one house on the printings, and the merge is unwritten
T-0414 — The street-face adoption refuses W. Montgomery a roof for being the bootmaker, and identity.json already ruled they are two houses
T-0415 — John Wright's two buildings to let are named (east) and (west) and stand the other way round
T-0419 — The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither
T-0420 — Open the four South Water blocks T-0009 has unblocked: 20 roofs of headroom on franklin, lasalle, clark and dearborn
T-0421 — Canal Street's three control points spread 2.33 m, so its corridor cannot be centred on any of them
T-0422 — The widened counterfactual deals a roof per street, and every roof a widening adds already fronts another street
T-0418 — The 36 documented tradespeople whose trade the residents vocabulary has no word for
T-0423 — G. Spring's large dwelling-house and fine well stands on lot 7 of block 16, where an anonymous roof stands now
T-0398 — A firm's own style stands in its proprietor list, because a claim read the signature where a person was wanted
T-0424 — The 1 January 1834 letter list's printed length, and the names all nine printings lost, need the page images
T-0425 — A letter-list household's arrival bound is dated by the printing it was extracted from, not by the return, so nine printings of one list give nine different bounds
T-0428 — The 1 April 1834 letter list has three positions no printing reads, and only the page images can say how long it was
