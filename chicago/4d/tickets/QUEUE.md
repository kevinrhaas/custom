# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-29 on his explicit
# instruction — the FOURTH such instruction: "update the queue and reorganize, keep
# the visible items first and or any dependencies that are needed for visible items,
# organize it so it makes logical sense and does the most impactful things first ...
# We want to finish up the newspaper stream so keep that nearest the top." Earlier
# instructions: 2026-08-27 ("reorder the queue and put items added to their correct
# category, again visible progress items first"), 2026-08-23 ("put visible things
# first ... if there is some non visible ticket that will make a big difference or
# dependency then fine"), 2026-08-28 (the NEWSPAPERS band placed after the visible
# bands). The 2026-08-29 instruction supersedes 2026-08-28's placement of that band.
# Absent such an instruction, agents still only APPEND (new) and REMOVE (done) — do
# not re-rank on your own judgement.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. THE NEWSPAPER STREAM RUNS FIRST until it is finished (owner, 2026-08-29):
#      reads feed the register, ledger hygiene cleans what the register mints, the
#      register feeds the seeding, and the seeding is the visible payoff.
#   2. VISIBLE NEXT. AGENTS.md's test — when this merges, what is different in a
#      screenshot taken from the same spot? "See" means in the 3-D scene or on a card
#      a visitor opens. A gate, a metric, a source record and a refactor are not.
#   3. An INVISIBLE ticket outranks visible ones only when it BLOCKS them, and the
#      band it sits in has to say what it blocks.
#   4. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.
#
# Labels on these lines are regenerated from each ticket's own `title:` field. If a
# label and its ticket disagree, the ticket wins — one line was found mislabelled
# on 2026-08-27, damage from the `ticket.mjs restamp` bug that T-0217 records.

# --- THE NEWSPAPER STREAM — first by the owner, 2026-08-29: "we want to finish up
# --- the newspaper stream". Order inside the band is the dependency chain:
# --- (a) the three remaining reads — 1835 first, it is the scene year;
# --- (b) ledger hygiene the register depends on — dedupe people and firms BEFORE
# ---     T-0262 mints them into the town, reconcile the placement conflicts the
# ---     reads surfaced;
# --- (c) the register itself, then the VISIBLE seeding it unblocks — documented
# ---     storefronts standing in the model, documented people replacing invented.
T-0336 — The 31 July 1835 letter list, standing in all four August Democrats
T-0263 — The documented storefronts take their places on South Water and Lake
T-0306 — The American names six Chicago storefronts with usable placements and none of them is standing in the model yet
T-0373 — The documented people the papers name with no trade at all, and the town does not hold
T-0374 — letter_list_only reaches the visitor's card, and the 1,536 names known only from the post office

# --- NEWSPAPERS, WAITING ON THE PAGE IMAGES — each needs the owner's scans opened,
# --- which live outside the repository. Workable the day the images are supplied;
# --- until then a run should take something above instead.
T-0318 — The January 1834 letter list: the third printing repairs the A-H half, and the images are needed only for the rest
T-0321 — The 1 April 1834 Chicago letter list is 179 names and nineteen lines of debris stand where more did
T-0331 — The March 1834 letter list lost its date line and both its crops failed Vision; the page images can say which return it is
T-0305 — Four readings the American contradicts itself on need the page images: the tailor's street, which Water street two forwarding houses stood in, and the corner of Cobb's saddlery

# --- STANDING REDS — invisible, but each one is red on an UNMODIFIED dev today, so
# --- every branch's smoke inherits it and every PR has to argue "not mine". Fixing
# --- these buys every ticket below a clean verdict.

# --- THE TOWN AND ITS STREETS — visible. T-0192 left this band on 2026-08-29,
# --- blocked-tech: its code half shipped (the rule reads all four block faces now,
# --- so a cross street CAN be laid), and all seven cross streets were then measured
# --- over all three ceilings. PR #418, which parked Market Street alone, is closed.
T-0272 — The West Division parcel's form values come from the archetype and cite the family band: 8 families, 11 claims outside it
T-0273 — The South Division infill parcel's form values come from the archetype and cite the family band: 9 families, 10 claims outside it
T-0274 — The inferred-household parcel's form values come from the archetype and cite the family band: 8 families, 10 claims outside it

# --- THE RIVER, THE WHARVES AND THE GROUND — visible. T-0219 is parked on PR #432.
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier

# --- THE FORT — visible, small
T-0266 — On a phone from across the river the stockade's picket rhythm falls under the pixel grid and beats

# --- WHAT GROWS, WHAT A PHONE SEES, AND THE CARDS A VISITOR OPENS — visible
T-0277 — The mid and forb rings' outer edges are re-priced for a density handover, now the reach statistic is honest
T-0279 — 2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev
T-0280 — The far band's grass-or-flower split is made on the forb lattice's CLAMPED share
T-0302 — The .lib-body grid resolves toward max-content under all six other Evidence sections, and only the plants section is fixed
T-0268 — A building held under the standing constraint says so nowhere a visitor can see

# --- THE TRIANGLE AND DRAW-CALL BUDGET — invisible, and it gates EVERY visible
# --- ticket that adds geometry; the two AO tickets are where the next headroom is.
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor

# --- MEASUREMENT, GATES AND PROVENANCE — invisible, and nothing below blocks the above
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0230 — Two named South Water frontages carry a reconstructed trade, so neither a signboard nor a hitching post will ever stand at them
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0055 — Hold the Kinzie-view plate as a source record
T-0053 — A patched lit material silently inherits another layer's shader program
T-0037 — The liberties gate reads the whole Evidence panel, so a liberty saying 'Three of these' fails it
T-0030 — A queue card in Manager reading tickets.json
T-0255 — The dooryard planting rule reads every street in the town with no bound on reach, so a track across the river can turn a house's yard

# --- THE PIPELINE AND ITS RUNNERS — invisible; the loop's own health
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0235 — The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap
T-0173 — The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured
T-0170 — The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner
T-0180 — The bake opens a content PR on every run, because the build stamp it writes is always dirty
T-0301 — Every visible ticket at the top of the queue is parked on hold or in flight, and five straight invisible runs merged under it
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw with the evidence written
# --- into the ticket; never withdrawn on a guess. T-0271 joined on 2026-08-29:
# --- #456's measurement showed balanced GREEN at 1,203,871 of 1,210,000 after it
# --- merged, and all three of these predate that merge.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand

# --- NEWLY FILED — `ticket.mjs new` appends to the END of this file, so new tickets
# --- land under this line. NOT yet placed by the owner.
T-0332 — The sheet's one brick is called chimney_brick, and a wall now reads it
T-0337 — One man is two proprietors of Russell & Clift, and the gazetteer has no rule that can join them
T-0338 — Thirty-one groups of firms share a partner surname and only one of them has been judged
T-0340 — The bookseller's sign-name and its partners' firm-name are three gazetteer entries for one house
T-0345 — Mason's blacksmith shop is anchored on Graves' Tavern until 16 July 1834 and on the Tremont House from 10 September, and the register holds both as standing placements
T-0346 — Desktop smoke stage 4 no longer fits the ten-minute foreground ceiling, so no steward run can take the whole desktop gate
T-0341 — A bare surname can never be joined to its forename: the family rule reads 'no initials' as 'different initials'
T-0348 — The identity policy cannot merge an unread initial with a read one, and the best witness reads seventeen of them
T-0349 — The signboard gate is red when stage 1 runs before it and green when stage 2 runs alone
T-0350 — D. Weaver's advertisement is dated Nov. 12 in two printings and Nov. 19 in the one the ledger believed
T-0354 — The register can only place 24 of 190 documented businesses; 49 more reach a street face and 78 reach nothing
T-0355 — A firm matches a building on an occupant the same sentence dates to 1831
T-0356 — The claim vocabulary cannot say an advertisement announces an opening, so 17 businesses are excluded on a proxy
T-0357 — 129 documented businesses will stand on a survival liberty and LIBERTIES.md carries none of them
T-0358 — The Thompson plat's block NUMBERING is uncommitted, so the corpus's only lot-and-block address cannot be placed
T-0359 — The gazetteer mints tavern names as people, so Maddock's Tavern and Haddock's Tavern cannot be reconciled
T-0369 — Desktop stage 8's panel walk is red when stage 1 runs before it and green when stage 8 runs alone
T-0371 — The lattice path's block rotation is dead code that measure_rank_bias.mjs's drift guard pins in place
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0365 — The anonymous-block programme has no unblocked ground left: every block with headroom is on the South Water reach T-0009 holds open
T-0333 — Every stove pipe in the town owes eighteen inches above its roof, and the ordinance of 5 August 1835 says so
T-0334 — The hay-stacking ordinance walks a six-vertex boundary round the built town, and nothing draws or tests it
T-0375 — Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand
T-0372 — North Water Street's two tight spots are 5.5 m and 8.5 m from water, and the setback rule cannot see either
T-0377 — Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
T-0388 — The 36 documented tradespeople whose trade the residents vocabulary has no word for
T-0390 — Three of the nine desktop smoke stages no longer fit the ten-minute run ceiling
