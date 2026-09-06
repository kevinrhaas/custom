# QUEUE — top is next. Text after the id is a label; the parser reads only T-NNNN lines.
#
# THE OWNER OWNS THIS ORDER. Agents APPEND and REMOVE; re-ranking takes his instruction, and
# the instruction is quoted in the band that acts on it.
#
# ORDERING RULE
#   1. The city gains something first — a building, a person, a trade — ordered by how much.
#   2. Then what those additions depend on, and the repairs that make them correct.
#   3. Then visible refinement: the town changing rather than growing.
#   4. An invisible ticket outranks a visible one only when it BLOCKS one, and its band says so.
#   5. Related work runs together, so a run carries the last one's context.
#
# `needs_bake: true` marks a ticket whose merge changes baked geometry. Labels regenerate from
# each ticket's `title:`; if they disagree the ticket wins (T-0217). `epic:` is not load-bearing
# — the BANDS say where a ticket sits.
#
# RE-RANK LEDGER — the instruction behind each pass, newest first
#   2026-09-05  "Pull 802 up" — the owner, after T-0802's fault was caught live: T-0722 sat
#               `claimed` on a queue a run reads top-down for hours after PR #836 landed its
#               work. Moved into the blocking band beside T-0819.
#   2026-09-05  ...AND THE REST OF THE FILE, same instruction: "And other logical ordering
#               across the queue". Applied ORDERING RULE 4 where the bands' own text already
#               said it: the triangle ceiling gates every roof, so it now sits ABOVE the roofs
#               instead of 60 lines below them; a red dev and an unpromotable production block
#               everything, so they lead. Four bands merged into two. Nothing of the research
#               band moved.
#   2026-09-05  THE CORE DATASET, RE-ISSUED AND REBUILT. The owner repeated his 2026-09-04
#               instruction almost word for word against the newly filed tickets (quoted in the
#               band below), and asked for the comments tightened. The 09-04 band had DRAINED —
#               its groups were empty and 86 tickets sat unplaced — so the research band is
#               rebuilt from the new arrivals: 54 tickets, G1..G6, consolidations placed between
#               the groups rather than at the end. Comments cut roughly in half.
#   2026-09-05  "Rank T-0727" — under the drain band, per the site-budget ruling.
#   2026-09-05  drain the open-PR queue (band below); pace sliders + framed arrival (#907).
#   2026-09-04  RESTORED after merge-queue.mjs clobbered it: "put it back with all of the
#               research items for improving the resident and business data at the top". The
#               driver now resolves on the side that actually RE-ORDERED, and refuses if both did.
#   2026-09-04  the core dataset before more reading · the grades questioned (T-0699/0692/0693)
#   2026-09-03  best-yield research first · consolidate every few, not at the end · the Sauganash
#   2026-08-30  "lots of nothing happened in the city which is bad" — 41 merges, 0 buildings
#   2026-08-29 (x2), 2026-08-28, 2026-08-27, 2026-08-23

# --- ==========================================================================
# --- THE CORE DATASET — OWNER INSTRUCTION, 2026-09-04, RE-ISSUED 2026-09-05

# --- G1 — THE CARD MUST BE ABLE TO HOLD IT. Small repairs the spend below writes THROUGH: a card
# --- that drifts silently, or one identity split across two cards, makes every figure under it
# --- unarguable. Nothing here reads a source.






T-0723 — One identity, two town cards: Mrs Rufus Brown is folded onto her husband by the honorific strip, and N. R. Norton is Nelson R. Norton carried twice
T-0843 — Stop the cause: a minting pass must consult the identity master before it writes a card, and --check must fail when a new card's identity already has a canonical one

# --- G2 — SPEND WHAT IS ALREADY ADJUDICATED. The bottleneck, and it has not moved: rulings exist
# --- that no card carries. Nothing here reads a new source either — every one turns research
# --- already done into household, person and business DATA, which is what the owner asked for.
T-0700 — The nine ring purchasers that meet a person the town already holds are proposals nobody has ruled on

# --- CONSOLIDATION — run it HERE, not at the end. Owner, 2026-09-03: "dont land those tickets at
# --- the very end maybe every few you should do that consolidation". Pass 3 was T-0636; the run
# --- that closes G2 files pass 4 before it closes, per T-0028's succession rule.

# --- G3 — FAMILY AND HOUSEHOLD STRUCTURE. Unblocked 2026-09-05: the owner ruled that kinship IS
# --- modelled, as the household-level kin[] block — graded, reciprocal, legal only against its
# --- declared inverses. T-0734 is the measurement that ruling exists to spend: 14 of 1,404 people
# --- carry a stated relationship to anybody, and the sources already print many more.
T-0757 — The 1830 division's recapitulation counts 53 and 88 families on leaves that carry 55 and 39: re-count both against the enumerator's column

# --- G4 — BUSINESS, OCCUPATION, AND WHERE THEY STOOD. The owner: "locations matter so capture
# --- those too ... there are business references that have addresses later and while we don't have
# --- that in 1835, you might use a documented address from later to position the business".
# --- T-0788 LEADS BECAUSE IT IS THE ENABLER — Wright numbers all 58 blocks of the Original Town,
# --- so a lot-and-block address can finally land on ground. T-0773 is the later-printing rule the
# --- ask names directly; T-0771 and T-0696 are the readers that spend it.
T-0788 — Wright numbers all 58 blocks of the Original Town and this project has read six: read the rest — the Public Square is block 39 — so a lot-and-block address can finally land

# --- CONSOLIDATION — second pass, same rule.

# --- G5 — TOWN DETAILS, COMPOSITION AND ENCLOSURES. The rest of what the owner named. Each puts
# --- something a visitor can see on the ground, off evidence already read.
T-0772 — Twelve dooryard gardens went with the retired households: should a garden follow the house or the household?

# --- G6 — THE READING, AND IT STAYS BELOW THE SPEND. Reading another volume moves none of the
# --- numbers above. Ordered by measured yield, with the crosswalk repairs first because a stale
# --- crosswalk wastes the read that follows it: civic poll/tax/voter matched 28.7%, the 1840
# --- census 1.0%, church and Newberry 0.0%.
T-0698 — The 1840 census heads crosswalk is derived against 849 residents and 17 sheets, and the town now holds 1,404 and 25
T-0581 — Moses and Kirkland's History of Chicago (1895) is the largest Chicago work the Newberry index points at that this project does not hold: read its Chicago and Cook County families for 1835 residents, households and businesses
T-0912 — Read printed 232's 31 households off M704 roll 57 leaf n167: the family TOTAL, the seven industry columns, the pensioners block and the schools and illiteracy cells
T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line
T-0762 — The 1840 census image 26-50: continuation sheet 33S7-9YYJ-VJ read line by line
T-0743 — 33S7-9YYJ-FJ read line by line: the TOTAL column, and whether the footing that refused the printed-207 pairing is 135 or 138
T-0744 — 33S7-9YYJ-L3 read line by line: the TOTAL column, and the line count the contact sheet and the strip disagree on
T-0748 — The 1840 census continuation sheet 33SQ-GYYJ-5H read line by line, off a pale exposure that hides entries at the standard ink threshold
T-0754 — 33S7-9YYJ-6H's SCHOOLS footing under No. of Scholars is written and does not read: two glyphs where a 40 would stand, and no bowl
T-0755 — The seventh SCHOOLS column of 33S7-9YYJ-6H, No. of Scholars at public charge, is in the binding gutter and is recorded unread rather than blank
T-0761 — The banded rule profile read_census_continuation.py needs: the printed rules of a continuation leaf lean up to 41 px and one profile over the whole body loses them

# --- ==========================================================================
# --- WHAT BLOCKS EVERYTHING ELSE — ordering rule 4, and these are the cases
# --- ==========================================================================
# --- An invisible ticket outranks a visible one only when it BLOCKS one. These block ALL of them,
# --- and each band below used to state that about itself while sitting under the work it gated.
# --- T-0819 first: the promotion workflow cannot push its back-merge, so PRODUCTION CANNOT BE
# --- PROMOTED AT ALL. Then dev's standing red — T-0728, T-0729 and T-0781 are three reports of the
# --- same failure set on an untouched checkout, and T-0763 is why they were hard to tell apart.
# --- T-0802 IS HERE ON EVIDENCE, NOT ON THEORY — owner, 2026-09-05: "Pull 802 up". It was caught
# --- live the same day: T-0722 FIXED the 32 MB ceiling in PR #836, that PR merged, and the ticket
# --- still read `state: claimed, pr: null` hours later — sitting workable at the top of a queue
# --- a run reads top-down. That is the seventy-minute failure of 2026-08-19 (run 943's #258 left
# --- open, run 944 rebuilding T-0062 from scratch) with the branch guard closed and the OTHER
# --- hole open: `claim` checks for a rival BRANCH, and nothing checks a ticket against the PRs
# --- that already landed. It blocks nothing by itself; it silently duplicates whatever it
# --- touches, which is worse, and it is why this band is the right place for it.
T-0819 — The dev ruleset blocks chicago-4d-promote-to-prod's back-merge: it pushes to dev as github-actions[bot] and the bypass list is empty, so production cannot be promoted
T-0802 — A ticket whose PR merged can sit 'claimed' forever, because nothing compares ticket state against the PRs that landed
T-0857 — GitHub's merge never runs this repo's merge drivers, so every PR reads as conflicting and auto-merge can never fire
T-0728 — dev's own gate is red before any branch touches it: three research cohorts are stale and seven household records no longer re-derive from the ladder
T-0729 — dev's gate is red on an untouched dev again: 0 platted cross-street faces, blk_washington_clark off the ground, the southern coverage claim and the far-timber census
T-0781 — tools/check.sh has been red on dev since before 2026-09-05: four checks fail on an untouched checkout
T-0763 — check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them
T-0825 — dev is red at desktop part 2: the town's wagons vary in type and in the way they stand — 23 farm_box, 17 cart, 23 covered, 6 distinct headings

# --- THE TRIANGLE AND DRAW-CALL BUDGET — MOVED ABOVE THE ROOFS IT GATES. Its own text has always
# --- said "it gates every ticket above that adds a roof", and it was sitting sixty lines BELOW them.
# --- Measured on the closed #599: dev had 1,566 triangles of `balanced` headroom and four roofs cost
# --- 2,174 — so the next visible parcel of any size fails whatever it is. T-0441 held that
# --- measurement and its three options and NEVER REACHED DEV; it dies with that branch and wants
# --- re-filing by whoever takes this band.
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor
T-0672 — The three ceilings were raised for one parcel on 2026-09-03 and light's floor was spent: re-measure once #432 lands and take every tier back down
T-0673 — The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured

# --- THE CITY GAINS ROOFS — owner rulings, 2026-08-30. Each puts a building a visitor can walk to.
# --- Gated by the band above; the owner's standing priority is the dataset first (see the top band),
# --- so these sit here rather than at the head of the file.
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street

# --- THE REPAIRS THE SEEDING READS — identity, anchors, placements. They add no buildings; the
# --- buildings above cannot be placed CORRECTLY without them.
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

# --- THE WRIGHT 1834 SHEET — owner ask, 2026-09-05. T-0788, T-0797 and T-0798 are in G4 above,
# --- because they are what makes an address land; these are the rest, in his own dependency order.
T-0789 — Kinzie's Addition is on the sheet whole — 54 numbered blocks, 13 named streets, the Kinzie Block and the river-front water lots — and the North Division carries four streets
T-0790 — Wabansia, surveyed 1831, is drawn whole north of Kinzie Street — eight streets, some 79 blocks and a water-lot tract on the North Branch — and the town has none of it
T-0792 — The legend's nine coloured tracts are the town's survey history — who surveyed what ground, when, for whom — and the project has no tract layer
T-0794 — The two branches run to the sheet's edges and the town's traces stop at the box: the South Branch through the School Section and the North Branch through Wabansia, off Wright
T-0795 — Every watercourse Wright draws, counted on the new sheet: the three Main Branch sloughs re-checked, and any the BPL tracing windows never covered
T-0796 — The small tract north of Kinzie Street lettered Michigan St — small parcels and an alley where every neighbour is whole blocks, and a road curving north through it — is unidentified: which survey, which legend swatch, and what the sources call it
T-0799 — Trace the whole east edge off the full sheet: both piers, the cut, the sand bar to its tip, the old channel to where Wright closes it, and the shore to the sheet's bottom margin — one run, no window
T-0800 — The mouth as built: the piers as phased structures at their 1835 length, the bar's height argued, the reservation's blue edge and the lighthouse checked, and the epoch re-baked closed
T-0801 — The pre-fire viewer at /chicago/pre-fire/viewer/ shows 1834 through Hathaway only: put the Wright sheet beside it as the year's second view, with its provenance row, its checksum, and the mirror re-copied

# --- THE GROUND WEST AND NORTH OF THE RIVER — owner fault reports, 2026-08-31. T-0827 is what
# --- T-0451 left open: the committed market line is fitted to N Wacker Drive and stands 9.1 m off
# --- the plat's own module, so the suspect is the parent line rather than the North Division.
T-0689 — The West Division's lot dimensions and lot-counts are still unread off the Thompson plat, and T-0444 closed without them
T-0768 — West Water Street north of Lake: the 1839 directory attests the reach, and a bank offset there runs through the Wolf Point cluster
T-0770 — south_branch_raft_bridge glosses West Water Street as 'now Canal Street', and the committed canal stands a plat module west of it
T-0827 — The committed market line is fitted to N Wacker Drive and stands 9.1 m off the Thompson plat's own module

# --- THE LOT GRID QUESTION — measure, THEN ask.
T-0419 — The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither
T-0421 — Canal Street's three control points spread 2.33 m, so its corridor cannot be centred on any of them
T-0422 — The widened counterfactual deals a roof per street, and every roof a widening adds already fronts another street

# --- VISIBLE REFINEMENT — the town changing rather than growing.
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

# --- SOUTH THROUGH TIME — owner epic, 2026-09-01. One ticket per epoch, in order.
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

# --- ==========================================================================
# --- THE LOOP'S OWN HEALTH — the drain band and the pipeline, merged
# --- ==========================================================================
# --- Owner instruction, 2026-09-05: "we have a whole lot of PRs that get left open on dev ... add a
# --- ticket or tickets to queue in the correct order to work and close and merge correctly open PRs?"
# ---
# --- Measured 16:00Z: 21 PRs open, 21 of 21 CONFLICTING, on the same six GENERATED files every time.
# --- changelog.js, which HAS a merge driver, conflicted on 0 of 21 — that contrast is T-0813, and
# --- #910 has since landed its first half. WHAT ACTUALLY DRAINED THE PILE was not laps: T-0815 closed
# --- five PRs dev had outrun, and the lane then drained itself the moment #836 took the published
# --- tree off the 32 MB wall and dev's gate went green. 21 open at 16:00Z, 6 by 19:15Z. The
# --- constraint was never "nobody is merging" — it was two stop-the-world faults and a janitor blind
# --- to both, which is why T-0809 outranks the remaining laps.
T-0809 — The janitor gates the branch un-merged and drops a conflict in silence, and the lane outruns its own merge lap
T-0806 — Drain lap 2: the four census and books PRs, whose real tail is their coverage declarations
T-0808 — The owner's three rulings — the site budget, kinship, and the planform of record at the forks — carried into the tickets that asked
T-0727 — Budget the walkthrough's boot payload, which is what a visitor actually downloads, rather than the whole published tree
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0437 — The bake smoke clones a 3.2 GB monorepo to test one subtree, and that checkout has killed seven legs at the cap
T-0674 — A bot-opened PR never runs the dev gate before merge, and two of them broke dev
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0301 — Every visible ticket at the top of the queue is parked on hold or in flight, and five straight invisible runs merged under it
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down

# --- CLEANUP — MANY TICKETS, FEW FAULTS. Verify, keep what is still true, and withdraw the rest
# --- WITH THE EVIDENCE. THE 32 MB BAND IS DONE, 2026-09-05, on the owner's "do it if those
# --- tickets are useless now": T-0725, T-0731, T-0774 and T-0803 were four more reports of the
# --- one ceiling and are withdrawn — measured 30.412 MB of 32 with 1.588 MB of headroom and
# --- zero duplicate published files over 64 KB, which is the condition #836's new rule gates.
# --- T-0722 was NOT withdrawn: its work LANDED in #836 while the ticket still read `claimed,
# --- pr: null`, which is T-0802's fault caught live, so it closed as done. T-0804 stays open —
# --- it is a live proposal (1.99 MB from minifying the mirror) with an owner question attached,
# --- not a report of the ceiling. The eight below it are an older band of the same shape.
T-0804 — Minifying the published mirror's JSON is a measured 1.99 MB: decide whether the record must stay readable at its own URL
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand
T-0377 — Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
T-0388 — Three derived records have drifted from their own generators on an unmodified dev, so every branch's gate is red
T-0522 — The dev gate has been red on 10 legs since PR #670 merged the recovered census bridge
T-0612 — dev's gate is red: two merged readings raised no ceiling, and every branch after them inherits the failure
T-0683 — Ten check.sh checks and six part-13 smoke assertions are red on dev after PR #670, on five independent causes

# --- MEASUREMENT, GATES AND PROVENANCE — invisible, and nothing here blocks a visible ticket. The
# --- red-gate reports moved up to the blocking band; these are the rest.
T-0688 — The wagon-variety gate counts street bearings, so re-deriving a street took it from 9 buckets to 7 and it is at its floor of 8
T-0776 — A full tools/web_derivatives.sh rewrites 348 derivatives with identical byte counts: the derivative step is not reproducible
T-0777 — assets/manifest.web.json's $note is rewritten with escaped em-dashes, so its own generator does not reproduce what dev committed
T-0829 — A repeated string in a provenance or coverage list is the same merge artefact as a repeated id, and nothing asserts it
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
T-0662 — check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated

# --- NEWLY FILED — `ticket.mjs new` appends here. NOT yet placed by the owner.
T-0438 — The letter-list cohort is 2.54 MiB of the published tree, and it is now the largest single item in it
T-0439 — Two pixel-sensitivity checks fail when parts 9-12 run together and pass when part 9 runs alone
T-0449 — Four South Water frontage entries declare lots their runs never reach, and each hides its block's headroom
T-0520 — The archetype builders compute their own opening rectangles beside the ones facade_openings states, and only a town-wide rebake can join them
T-0537 — The web derivatives are stamped by an unpinned gltf-transform, so a release upstream restamps all 372 of them
T-0690 — dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0833 — Make a drain lap a tool: tools/drain.mjs, which refuses on any conflict outside the build products

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0830 — The Dalton Data Bank prints two Cook County land purchases of June 1836 that the tract-sales sweep does not hold

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0834 — The 665 schedule sizes a block's principal room in party-line units and the generator places by whole lots, and on a business front the two disagree
T-0835 — The Newberry leads re-parse to 8 fewer cards from unchanged card text, so the parser moved under leads.json and the fingerprint gate could not see it
T-0836 — The town's wagons stand on 6 distinct headings and the smoke asks for 8, so dev is red at both viewports on a layer no branch has touched

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0844 — Six duplicate-card clusters the evidence does not decide: Hunt, Kennicott, Saunders, Walker, T. Temple and John S. Kinzie
T-0846 — The four other spend passes can write the same paragraph onto a card twice, and their gates cannot see it
T-0848 — Two smoke checks fail only when mobile stages 9-12 run together — the facade-tone and shadow-reach sensitivity deltas collapse in a combined range
T-0849 — Hurlbut names Gurdon Hubbard's parents and the dataset has nowhere to put them: kin[] rows point at a household in this town, and Elizur and Abigail Hubbard have none
T-0852 — tools/ticket.mjs inflight has a three-hour cold window, so a run that claims and then reads for four hours is invisible to the next run
T-0854 — The card John S. Kinzie is named from a digit: the Democrat prints 'JOHN 8. KINZIE' beside John Harris Kinzie's own trade, and the owner's R3 referral was argued on an initial the source never printed

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0841 — The keeper of the St Cyr register is graded G5, not G2c: may the officiant of a parish register be graded on it?
T-0842 — Van Den Bogart and Van der Bogart: one man printed two ways, or two men? A card was minted for the second


T-0862 — The Wright NARA registration that every Wright-band ticket is built on has no gate: nothing verifies its raster, its checksum or its fit
T-0861 — Eight newspaper claims print a street in their prose and their placement record carries none, so the reading ranks as an address that names no ground
T-0869 — Clark, Filer & Co. advertise a warehouse five doors east of a corner the plat does not have: is the Democrat's 'Randolph st.' a mis-set cross street, or a firm naming a corner it did not stand on?

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0866 — The card rename of T-0721 broke the register's link to two townspeople: Abbot and Gabbs are proposed as new residents the town does not hold

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0867 — The Fergus 1843 crosswalk reads 'none_recorded' as a trade, so could_carry_occupation is 0 where Norris's fixed twin reports 63
T-0868 — Norris 1844 normalizes 'Jones, B. & Co. dry goods and groceries' as a person, not a firm, so the firm filter never sees it
T-0871 — The residents-manifest rebuild has no self-test and silently accepts any flag: nothing proves its assertions fire, and --write typo'd is a green check

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0872 — Eight cards already carry a later trade in the 1835 occupation field, landed before T-0837 gated it
T-0873 — publish.sh minifies the four resident cards the synthesizer writes pretty, so the first republish after a synthesis spend turns the drift ratchet red
T-0877 — The School Section's twelve north-south lines are read and not committed: Des Plaines, Jefferson, Clinton, Canal, Market, Wells and Clark run south of Madison and five more tiers carry no name
T-0878 — Wright's 1834 registration is three per cent long in y: the School Section's mile measures 1658.65 m north-south and 1603.04 m east-west on the same fit

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0874 — publish.sh minifies four resident mirror files that the T-0838 synthesizer ratchet expects verbatim, so every publishing PR is one revert away from red
T-0880 — publish.sh minifies four resident mirror files the synthesizer writes pretty, and the drift ratchet fails on the reformat
T-0884 — The register sells Russel Heacock lot 7 of block 117 and his committed house stands 7 m outside block 118: one of the two is out by more than the construction admits
T-0887 — A well layer, drawn renderer-side: the fort's well is measured to a coordinate and this project has no way to draw one

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0886 — The water at the foot of Randolph Street is the old channel behind the bar, not the lake: date the channel's 1835 state or find the carts' way across

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0890 — tools/web_derivatives.sh compresses with an unpinned `npx --yes @gltf-transform/cli`, so a runner with a newer CLI rewrites the generator string in all 380 web assets

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0891 — The Fort Cemetery's polygon cannot enter 1835_no_build_ground.json until measure_no_build_ground.py can resolve a ring read off a plate
T-0892 — The synthesizer drift ratchet turns red the moment anybody publishes: its T-0838 baseline names the data/ paths and not their site/ mirrors
T-0893 — The Beaubien homestead's phase id and start date still say 1817, and Andreas's own pages say the factory building reached Beaubien in 1822
T-0894 — Two sources put the Factory House just SOUTH of Fort Dearborn and jb_beaubien_homestead stands north of it: that bearing is all that is left of the identity question, and form.stories waits on it
T-0895 — The John-Dean house: an army contractor built a five-room house at the foot of Randolph Street in 1815, Beaubien bought it in 1817 for $1,000, and this project models nothing there
T-0896 — Drain the 18 --check-capable tools tools/check.sh never runs: gate each or record why it cannot be gated
T-0898 — The published residents mirror has two writers that disagree on its shape, and publish.sh losing the race turns the T-0838 drift ratchet red
T-0899 — Ira Couch's card has not learned the 1840 candidate ruled onto him: spend it, and drop the write-hop ceiling back to zero
T-0900 — Couch, Iia — the Tremont House entry both readings of Norris 1844 fail on: read the printed token off the page image
T-0901 — A garbled forename on the 1835 side, not the printed one: 'Willınm Bandle' carries a dotless i and refuses its own Fergus 1843 entry
T-0902 — publish.sh and the resident synthesizer write four mirror files in two different shapes, so whichever ran last decides whether check.sh is green
T-0905 — publish.sh minifies four resident mirror files that synthesize_resident_research.py writes expanded, so whichever ran last decides whether check.sh is green

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0910 — Block 4's lot 40 is inside C. Walker's brace on printed page 47 and reaches the reading with no bidder at all
