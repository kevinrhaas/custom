# QUEUE — top is next. Text after the id is a label; the parser reads only T-NNNN lines.
#
# THE OWNER OWNS THIS ORDER. Agents APPEND new tickets and REMOVE done ones. Re-ranking takes
# his instruction, and the instruction is quoted in the band that acts on it.
#
# ORDERING RULE
#   1. The city gains something first — a building, a person, a trade — ordered by how much.
#   2. Then what those additions depend on, and the repairs that make them correct.
#   3. Then visible refinement: the town changing rather than growing.
#   4. An invisible ticket outranks a visible one only when it BLOCKS it, and its band says what.
#   5. Related work runs together, so a run carries the last one's context.
#
# `needs_bake: true` marks a ticket whose merge changes baked geometry.
# Labels regenerate from each ticket's `title:`. If they disagree, the ticket wins (T-0217).
# `epic:` has drifted to a default and is not load-bearing — the BANDS say where a ticket sits.
#
# RE-RANK LEDGER — the instruction behind each pass, newest first
#   2026-09-04  RESTORED. The research-first order below was clobbered and the owner put it
#               back: "the queue got massively reordered, we were working on all of the
#               research items first ... please put it back with all of the research items for
#               improving the resident and business data at the top". HOW IT WAS LOST, because
#               it will recur otherwise: tools/merge-queue.mjs ordered on "OURS keeps the
#               order", and four PRs cut BEFORE the re-rank each merged dev, so the stale
#               branch was "ours" and its old order won — then carried to dev on merge. The
#               driver's rule is corrected in the same pass: the side that actually RE-ORDERED
#               relative to the merge base wins, and if both did it refuses.
#   2026-09-04  the core dataset before more reading (quoted in full in the band below)
#   2026-09-03  "reprioritize those items in the queue you think will yield the best research"
#   2026-09-03  "dont land those tickets at the very end maybe every few you should do that consolidation"
#   2026-09-03  the Sauganash deep dive — "an early visible ticket"; and four more sources "near the top"
#   2026-09-03  the resident source sweep → consolidation → residents/households update
#   2026-08-30  "lots of nothing happened in the city which is bad" — 41 merges, 0 buildings
#   2026-08-29 (x2), 2026-08-28, 2026-08-27, 2026-08-23

# --- THE SAUGANASH — owner, 2026-09-03: "an early visible ticket to do a deep dive on the
# --- sauganash hotel ... this is an attested structure we are putting fine points on it".
# --- T-0617 read the four plates and T-0626 rebuilt the massing; both landed 2026-09-04, and
# --- T-0649 (the fifth view) with them. T-0663 is what that reading left open.

# --- ==========================================================================
# --- THE CORE DATASET BEFORE MORE READING — OWNER INSTRUCTION, 2026-09-04
# --- ==========================================================================
# --- Verbatim, because it re-ranks the file: "move any tickets that are research related
# --- that move us towards getting a best and complete resident and family and household
# --- structure household business occupation town details and composition, enclosures, etc
# --- ... into the research area at the top in a logical dependency order do the most
# --- impactful ones first and if possible do some periodic consolidations along the way tk
# --- turn the research created into actual data household et al not just research, I want to
# --- get the core research and people and household and business dataset together and then we
# --- can go back to the app and improve the look and fill out all of the business and
# --- residences from the data, so locations matter so capture those too of course, like there
# --- are business references that have addresses later and while we don't have that in 1835,
# --- you might use a documented address from later to position the business where you have
# --- limited other information or it could contribute."
# ---
# --- MEASURED ON DEV AT 2e1a972d — this band is ordered by these numbers, not by taste:
# ---   read 16,063 · spent 3,990 · UNSPENT 12,073
# ---   rulings that name a town person: 109 reached · 4 on a card · 105 UNWRITTEN
# ---   the town's 825 households / 849 persons: occupation 111 (13.1%) · works_at 50 (6.1%)
# ---     · lives_at 20 (2.4%) · resting on ONE source 788 (92.8%)
# ---
# --- THE BOTTLENECK IS SPENDING, NOT READING. Reading another volume moves none of those
# --- numbers; spending what is already adjudicated moves all of them. So: spend first, then
# --- the sources that measurably pay, and a consolidation after every few rather than at the
# --- end. The addresses are already there — fergus_1843 has 46 matches that could carry one,
# --- norris_1844 39, and all 14 norris advertiser proprietors carry a printed trade AND
# --- address. 99 adjudicated later addresses against 20 households with any address at all.

# --- GROUP 1 — SPEND WHAT IS ADJUDICATED. Nothing here reads a new source. T-0602 (the
# --- measurement), T-0418 and T-0638 (a vocabulary and a surname slot the spend runs INTO),
# --- T-0632/T-0633 and T-0514/T-0634 have all landed; this is what remains of the group.

# --- GROUP 2 — THE SOURCES THAT PAY, AND THE LOCATIONS THEY CARRY. Measured match rates:
# --- civic poll/tax/voter 28.7%, 1840 census 1.0%, church 0.0%, Newberry 0.0%. What predicts
# --- yield is a list the town made of its own named inhabitants. The land sales are the
# --- largest untouched source of POSITION in the project, and T-0676/T-0679 are what T-0610
# --- and T-0666 left unfinished.
T-0679 — Fergus 1839's Fort Dearborn lot sale has 62 rows with no lot number and 22 with no price: settle the destroyed numerals off the page images

# --- GROUP 3 — COMPOSITION, FAMILIES, BUSINESSES, ENCLOSURES: the four the owner named.
# --- T-0589 is the town's civic account; T-0507 the household composition calibration;
# --- T-0597 a family relation two records refuse to state. T-0637 is last on a real
# --- dependency — joining 289 fence runs before the addresses land joins them to 20 houses.
T-0597 — James Kinzie and John Harris Kinzie are half brothers and the two household records do not say so
T-0440 — Clark, Filer & Co.'s live placement is empty while three printings put its warehouse five doors east of Randolph

# --- GROUP 4 — THE REMAINDER AND THE CLOSE-OUT. The summary sits after consolidation pass 3
# --- on purpose: it should describe a town whose cards are current.
T-0508 — 237 named residents have no research row: cohort 13 of 79
T-0509 — 237 named residents have no research row: cohort 14 of 79

# --- GROUP 5 — THE REST OF THE SOURCES, by their own measured yield, kept below the spend
# --- and NOT withdrawn. The 1830 schedule leads: the only pre-1835 enumeration, few leaves left.
T-0581 — Moses and Kirkland's History of Chicago (1895) is the largest Chicago work the Newberry index points at that this project does not hold: read its Chicago and Cook County families for 1835 residents, households and businesses

# --- The 1840 census reads — 1.0% match. coverage.json is a completeness contract, so these
# --- stay; they are behind sources paying twenty times better. T-0536 is this domain's gate debt.
T-0559 — The 1840 census printed pages 229 and 231: two independent cell readings disagree on 45 of 61 lines — reconcile them against the sheets, column by column
T-0497 — Dalton Data Bank holds a free 1840 Chicago head-of-household index by ward, and the repo cites it without reading it
T-0536 — The census_1840 domain declares its 25 read images in its own images[] shape, which the shared research-domain gate does not read
T-0671 — The anchor-offset test that places 5V's last unassigned_ink stroke, salvaged from the closed PR #746
T-0647 — 33S7-9YYJ-5V's six 'reference pair' readings are 11 and the digit key from a sheet that closes says they are 4

# --- The Newberry index — 319 leads, 0 merges, 719 refusals and nothing else. Volume 4's
# --- re-OCR is measured to recover 7.7x the cards. T-0600/T-0601 are its reading defects.
T-0619 — Volume 4 read by OCR, pages 1-306: the shards
T-0770 — Volume 4's OCR reading stitched, re-parsed and re-sampled, now that every band is in
T-0601 — A column sliver is kept as a second, truncated copy of a card the neighbouring pass read in full, and nothing counts how many

# --- THE GROUND IS WRONG WEST AND NORTH OF THE RIVER — owner fault reports, 2026-08-31,
# --- against the Thompson plat. Two of five West Division streets exist; Carroll and Fulton
# --- exist nowhere; west-side spacing is 112.1 m against a South Division 119.2-123.4 m. Whether
# --- the whole grid sits one street west — is `canal` really Clinton — is unmeasured, and every
# --- building west of the river turns on it. T-0685/T-0686/T-0687 are the bank measurements
# --- T-0453 left behind when it closed.
T-0447 — North Water Street's west end runs across Wolf Point, which the Thompson plat does not give it
T-0685 — Georeference the Thompson 1830 plat at the forks and measure its bank against the Wright 1834 line for the owner's ruling
T-0686 — The traced South Branch bank walks a dry seam in Wright's wash for 30 m, and repairing it moves the waterline
T-0687 — hydrology.geojson's two confidence strings no longer match the generator that says it is generated
T-0451 — Only one north-south street stands north of the river, where the Thompson plat carries the North Division's whole grid

# --- THE CITY GAINS ROOFS — owner rulings, 2026-08-30. Twenty roofs across four South Water
# --- blocks, one block per run. Take from the top.
T-0429 — Open blk_south_water_lasalle: 8 roofs of headroom on three free lots
T-0431 — Open blk_south_water_clark: 4 roofs of headroom on two free lots
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots

# --- MORE BUILDINGS AND TRADES, ALREADY RUNNABLE — no ruling needed; each puts something in
# --- the scene or lets a documented person stand somewhere.
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0414 — The street-face adoption refuses W. Montgomery a roof for being the bootmaker, and identity.json already ruled they are two houses
T-0412 — A building offered FOR SALE mints a placement reading on the vendor's own firm, so P. Pruyne & Co.'s store carries a corner it never stood on
T-0415 — John Wright's two buildings to let are named (east) and (west) and stand the other way round

# --- THE REPAIRS THE SEEDING READS — identity, anchors, placements. They add no buildings;
# --- they decide whether the ones above land on the right names and corners.
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

# --- THE LOT GRID QUESTION — measure, THEN ask. T-0009's ruling left the South Water corridor
# --- 8.58 m off its own block faces. The roof bands above are NOT blocked on it: if the answer
# --- later moves the grid, roofs move with their lots, which is how the grid works.
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

# --- SOUTH THROUGH TIME — owner epic, 2026-09-01. T-0219's ground continued south through the
# --- 1812 battle corridor and the 1880s Prairie Avenue district: shared infrastructure, then
# --- 1812, then the later urban terrain. The 1812 work follows AGENTS.md's Indigenous-history
# --- constraint — terrain, structures and documentary geography proceed; human depiction is not
# --- inferred.
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

# --- THE TRIANGLE AND DRAW-CALL BUDGET — invisible, and it gates every ticket above that adds
# --- geometry. The two AO tickets are the measured headroom. T-0672/T-0673 are the 2026-09-03
# --- raise and its receipt: T-0672 takes every tier back down once #432 lands.
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor
T-0672 — The three ceilings were raised for one parcel on 2026-09-03 and light's floor was spent: re-measure once #432 lands and take every tier back down
T-0673 — The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured

# --- A GATE THAT LIES. T-0450 corrects SMOKE-BUDGET.md, which compared a per-leg cap with a
# --- whole-gate total. ITS WORK MERGED as #674 on 2026-09-04 but the ticket was never closed —
# --- it still reads `claimed` with no pr. Same for T-0426 (#675) and T-0444 (#681, which says
# --- in its own words that acceptance 1 is answered but not done). Verify each against its
# --- acceptance and close or release it; do not re-do work that is already on dev.

# --- MEASUREMENT, GATES AND PROVENANCE — invisible; nothing here blocks anything above.
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

# --- THE PIPELINE AND ITS RUNNERS — the loop's own health. T-0437 is here because a 3.2 GB
# --- clone has killed seven smoke legs; T-0674 is the owner's 2026-09-04 ruling that a
# --- bot-opened PR must run the dev gate before it merges.
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0437 — The bake smoke clones a 3.2 GB monorepo to test one subtree, and that checkout has killed seven legs at the cap
T-0674 — A bot-opened PR never runs the dev gate before merge, and two of them broke dev
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0301 — Every visible ticket at the top of the queue is parked on hold or in flight, and five straight invisible runs merged under it
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw WITH THE EVIDENCE in the ticket, never
# --- on a guess. T-0377 and T-0388 are twins; one withdrawal closes both. T-0522, T-0612 and
# --- T-0683 all report a red dev from early September, and dev is green.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0271 — The balanced ceiling is breached at the forks by 5,290 triangles on an unmodified dev, and both open tickets name a different stand
T-0377 — Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
T-0388 — Three derived records have drifted from their own generators on an unmodified dev, so every branch's gate is red
T-0522 — The dev gate has been red on 10 legs since PR #670 merged the recovered census bridge
T-0612 — dev's gate is red: two merged readings raised no ceiling, and every branch after them inherits the failure
T-0683 — Ten check.sh checks and six part-13 smoke assertions are red on dev after PR #670, on five independent causes

# --- NEWLY FILED — `ticket.mjs new` appends here. NOT yet placed by the owner.
T-0438 — The letter-list cohort is 2.54 MiB of the published tree, and it is now the largest single item in it
T-0439 — Two pixel-sensitivity checks fail when parts 9-12 run together and pass when part 9 runs alone
T-0449 — Four South Water frontage entries declare lots their runs never reach, and each hides its block's headroom
T-0520 — The archetype builders compute their own opening rectangles beside the ones facade_openings states, and only a town-wide rebake can join them
T-0537 — The web derivatives are stamped by an unpinned gltf-transform, so a release upstream restamps all 372 of them
T-0690 — dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0689 — The West Division's lot dimensions and lot-counts are still unread off the Thompson plat, and T-0444 closed without them
T-0691 — The letter-list cohort is 76 households out of step with its own derivation, and check.sh never looks

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0694 — M'Cormick & Moon read as a Chicago hatter although their own notice gives No. 109 Jefferson Avenue, Detroit

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0677 — Thirty-five land purchasers are matched to households and not one is on the card: spend the land-sales resident crosswalk, tract, date and price
T-0678 — The old_settlers domain holds 18 merges and 57 death-notice matches naming a town person, is registered in no domains.json, and reaches neither hop of the spend measure
T-0681 — T-0666's Fort Dearborn lot crosswalk matches 11 bidders to residents and 3 of them are on no card: spend the lot sale onto the people it names
T-0692 — 18 residents graded inferred on two or more sources carry no ladder_rule at all: the consolidation never reached them
T-0693 — Edward Richards Allen's card says occupation none_recorded while the same file quotes him as a druggist twice: say what is known and when, not nothing
T-0695 — A garbled printed forename refuses a match the reader can still make: C!;as. for Chas., J>ctij for John, Iia for Ira
T-0696 — The directory crosswalks want a second discriminator: a trade separates 6 of the 33 contested groups and an 1835 premises 8, and the rule has none
T-0697 — The land-sales resident crosswalk stops binding when a surname stops being unique: 531 new people cost it three rulings with nothing new read
T-0698 — The 1840 census heads crosswalk is derived against 849 residents and 17 sheets, and the town now holds 1,404 and 25
T-0700 — The nine ring purchasers that meet a person the town already holds are proposals nobody has ruled on
T-0713 — The platted street lines are graded inferred; the owner rules them attested from the Thompson plat
T-0714 — The 1840 census crosswalk is 235 named heads stale on dev and no gate says so: 498 on disk against 733 read from the pages
T-0715 — data/residents/index.json rows go stale for any household no minting pass owns, and only validate.py notices
T-0716 — Test the one candidate T-0663 left standing: is the Eliza Chappel shore drawing William Mark Young's 'Chicago's First School House' of about 1925
T-0717 — The first Catholic church still stood at State and Lake in June 1837, and st_marys_church.json ends its phase on 1836-12-31
T-0718 — Is jb_beaubien_homestead the Factory House or the house Beaubien moved to: John Dean is the hinge, and the SW-versus-NE corner turns on it
T-0727 — Twelve dooryard gardens went with the retired households: should a garden follow the house or the household?
T-0728 — The publish budget has 944 bytes left, and 2.8 MB of it is changelog.js kept twice
T-0733 — 103 people carry a conflicting-evidence flag the final audit can see and no ruling reaches
T-0734 — 14 of 1,404 people have a stated relationship to anybody else: the kinship the sources already print

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0736 — Printed 232's continuation leaf is not in this deposit: find it in FamilySearch collection 1786457 or on the National Archives microfilm, and read the 31 households' industry, pension and schools cells
T-0740 — The Newberry leads have drifted from the layers beneath them: a plain --parse rewrites leads.json by 6,039 lines and leaves five leads unruled
T-0754 — 33S7-9YYJ-6H's SCHOOLS footing under No. of Scholars is written and does not read: two glyphs where a 40 would stand, and no bowl
T-0755 — The seventh SCHOOLS column of 33S7-9YYJ-6H, No. of Scholars at public charge, is in the binding gutter and is recorded unread rather than blank

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0743 — 33S7-9YYJ-FJ read line by line: the TOTAL column, and whether the footing that refused the printed-207 pairing is 135 or 138
T-0744 — 33S7-9YYJ-L3 read line by line: the TOTAL column, and the line count the contact sheet and the strip disagree on
T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line
T-0753 — Hurlbut gives Gurdon Hubbard a birth and a Montreal origin, and the household record holds neither

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0748 — The 1840 census continuation sheet 33SQ-GYYJ-5H read line by line, off a pale exposure that hides entries at the standard ink threshold
T-0765 — A page number in a citation is read as the state: ', 111,' after a digit run, 65 kept cards across the four volumes
T-0766 — The Illinois abbreviation still matches on the wreck of a word — 'Eng.', an author's initials, a France card — and those are the bad keeps the four precision samples have left

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0757 — The 1830 division's recapitulation counts 53 and 88 families on leaves that carry 55 and 39: re-count both against the enumerator's column
T-0758 — The Harrison plan names six things on the fort's ground that this model has never drawn: Well, Wash house, Big Barn with Cupola, Shop, Out Buildings and the Fort Cemetery
T-0759 — Chicago drank from the lake by cart in 1835 and the town has no waterman: the hogshead cart, the watering place at the foot of Randolph and the barrel at the door

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0761 — The banded rule profile read_census_continuation.py needs: the printed rules of a continuation leaf lean up to 41 px and one profile over the whole body loses them
T-0762 — The 1840 census image 26-50: continuation sheet 33S7-9YYJ-VJ read line by line
T-0763 — check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them
T-0764 — A cohort manifest's starting_* snapshot is rewritten every time the manifest is regenerated, so the freeze records today's tree rather than the day it was fixed
T-0770 — south_branch_raft_bridge glosses West Water Street as 'now Canal Street', and the committed canal stands a plat module west of it
T-0768 — West Water Street north of Lake: the 1839 directory attests the reach, and a bank offset there runs through the Wolf Point cluster
T-0767 — dev's gate is red on the Newberry lead crosswalk: 56 leads anchor to cards T-0600 struck, and acquisition_list.json no longer re-derives
