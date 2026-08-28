# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-27 on his explicit
# instruction: "reorder the queue and put items added to their correct category,
# again visible progress items first" — the second such instruction, after
# 2026-08-23's "put visible things first ... if there is some non visible ticket
# that will make a big difference or dependency then fine". Absent that
# instruction, agents still only APPEND (new) and REMOVE (done) — do not re-rank
# on your own judgement.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. VISIBLE FIRST. AGENTS.md's test — when this merges, what is different in a
#      screenshot taken from the same spot? "See" means in the 3-D scene or on a card
#      a visitor opens. A gate, a metric, a source record and a refactor are not.
#   2. An INVISIBLE ticket outranks visible ones only when it BLOCKS them, and the
#      band it sits in has to say what it blocks.
#   3. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.
#
# A third owner instruction, 2026-08-28: the NEWSPAPERS band was added and placed
# after the visible bands on his explicit direction, its seeding tickets ordered
# behind the extraction that feeds them.
#
# Labels on these lines are regenerated from each ticket's own `title:` field. If a
# label and its ticket disagree, the ticket wins — one line was found mislabelled
# on 2026-08-27, damage from the `ticket.mjs restamp` bug that T-0217 records.

# --- BLOCKERS — small, and each one corrupts or blocks the work below

# --- THE TRIANGLE BUDGET — invisible, and it gates EVERY visible ticket that adds geometry

# --- THE TOWN AND ITS STREETS — visible
T-0028 — Build out the NEXT anonymous block (one per run)
T-0192 — The cross streets' own frontages get the street edge

# --- THE RIVER, THE WHARVES AND THE GROUND — visible
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier

# --- THE FORT — visible, mostly small
T-0096 — Did the second Fort Dearborn carry a flagstaff, and can anything but a retrospective plate say so

# --- FABRIC AND WHAT THE BUILDINGS ARE MADE OF — visible

# --- WHAT GROWS, AND WHAT A PHONE SEES — visible

# --- THE NEWSPAPERS — placed here by the owner, 2026-08-28: "put all that legwork
# --- after the visible things". The invisible extraction tickets at the top of this
# --- band BLOCK the visible seeding at its bottom — documented storefronts and real
# --- people replacing invented ones — which is why they sit above other invisible work.
# --- Three owner rulings govern the epic; each ticket carries them in full.
T-0258 — Reading the Democrat, part one: November 1833 to June 1834
T-0259 — Reading the Democrat, part two: July to December 1834
T-0260 — Reading the Democrat, part three: January to August 1835
T-0261 — Reading the American: June to August 1835
T-0262 — The July 1, 1835 register: who and what the papers put in the town
T-0263 — The documented storefronts take their places on South Water and Lake
T-0264 — Documented people replace the invented

# --- MEASUREMENT, GATES AND PROVENANCE — invisible, and nothing below blocks the above
T-0210 — The desktop smoke's stage 9 times out clicking the panel close, on an unmodified tree
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0156 — The interior/silhouette discriminator counts edges internal to a layer as interior
T-0155 — The changelog stamper has the same after-publish trap the ticket tool just lost
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0055 — Hold the Kinzie-view plate as a source record
T-0053 — A patched lit material silently inherits another layer's shader program
T-0037 — The liberties gate reads the whole Evidence panel, so a liberty saying 'Three of these' fails it
T-0030 — A queue card in Manager reading tickets.json
T-0170 — The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner
T-0173 — The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
T-0180 — The bake opens a content PR on every run, because the build stamp it writes is always dirty
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw. Not withdrawn by an agent.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports

# --- NEWLY FILED — appended here by `ticket.mjs new`, which writes to the END of
# --- this file. NOT yet placed by the owner, and NOT part of the band above:
# --- these are new tickets, not tickets to withdraw.
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0233 — Eight of seventeen dealt lots carry none of their run's own roofs, and nothing was measuring it
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0235 — The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0230 — Two named South Water frontages carry a reconstructed trade, so neither a signboard nor a hitching post will ever stand at them
T-0243 — The two timber-placement gates match no mesh since the lattice landed, and one of them is now red on dev
T-0244 — T-0194's twelve hitching posts draw no vertices the gate can find, on dev
T-0246 — log_jail stands on two steps of Randolph Street's new plank walk, the same OSM-kerb fault Lake and South Water answered
T-0247 — The light tier draws 83 calls against the 80-call floor restored yesterday, on an unmodified dev
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor
T-0254 — North Water Street west of the slough, and the crossing it needs
T-0255 — The dooryard planting rule reads every street in the town with no bound on reach, so a track across the river can turn a house's yard
T-0265 — The sward census fails its own gate at a phone: z10_settled_town owes xanthium_strumarium a whole slot and draws it nowhere
T-0266 — On a phone from across the river the stockade's picket rhythm falls under the pixel grid and beats
T-0267 — The fort's wall brick is a third brick, 0.47/0.26/0.20 against the sheet's 0.45/0.23/0.17
T-0268 — A building held under the standing constraint says so nowhere a visitor can see
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand
T-0272 — The West Division parcel's form values come from the archetype and cite the family band: 8 families, 11 claims outside it
T-0273 — The South Division infill parcel's form values come from the archetype and cite the family band: 9 families, 10 claims outside it
T-0274 — The inferred-household parcel's form values come from the archetype and cite the family band: 8 families, 10 claims outside it
T-0275 — Back-merge main into dev: the newspaper deposit is on main, and 60 Finder-duplicate files on main turn the dev gate red
T-0277 — The mid and forb rings' outer edges are re-priced for a density handover, now the reach statistic is honest
T-0279 — 2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev
T-0280 — The far band's grass-or-flower split is made on the forb lattice's CLAMPED share
T-0281 — The ten plant communities reach no card a visitor can open
T-0283 — The North Division's warehouse row allows one freight roof and six documented ones stand above it
T-0284 — Two slices of one batch claimed T-0256 and both built it — a claim is written where the next slice cannot see it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
