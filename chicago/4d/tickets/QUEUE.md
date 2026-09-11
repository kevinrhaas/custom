# QUEUE — top is next. Text after the id is a label; the parser reads only T-NNNN lines.
#
# THE OWNER OWNS THIS ORDER. Agents insert beside related work and remove; re-ranking takes
# his instruction, and the instruction is quoted in the band that acts on it.
#
# ORDERING RULE
#   1. The city gains something first — a building, a person, a trade — ordered by how much.
#   2. Then what those additions depend on, and the repairs that make them correct.
#   3. Then visible refinement: the town changing rather than growing.
#   4. An invisible ticket outranks a visible one only when it BLOCKS one, and its band says so.
#   5. Related work runs together, so a run carries the last one's context.
#
# FILING RULE — owner, 2026-09-10, after this file reached 195 lines with the bottom third
# never worked: "I don't want you to keep adding a whole bunch of tickets below your current
# one and working them … I want fewer tickets to work."
#   a. If an open ticket already owns the question, ADD the finding to it. File nothing.
#   b. If it is a real one-run piece of the goal: `ticket.mjs new "…" --after T-NNNN` puts it
#      directly under the ticket it serves, inside that band. Placing is not re-ranking.
#   c. If finishing it would take more than five tickets, it is an EPIC: one ticket under
#      EPICS at the foot of this file, carrying the list. The loop does not work an epic
#      until the owner promotes it out of that band.
#   Only the owner moves an existing line.
#
# `needs_bake: true` marks a ticket whose merge changes baked geometry. Labels regenerate from
# each ticket's `title:`; if they disagree the ticket wins (T-0217). `epic:` is not load-bearing
# — the BANDS say where a ticket sits.
#
# RE-RANK LEDGER — the instruction behind each pass, newest first
#   2026-09-10  "move the south through time section below section 5 and above section 6" — the
#               owner, hours after the reorganisation below. It is a PROMOTION as well as a move:
#               under EPICS the loop does not work a programme until he promotes it, and it now
#               stands as band 6, workable in rank order. Its fourteen tickets keep his 09-01
#               order. Nothing else moved; the loop band renumbered 6 to 7.
#   2026-09-10  THE WHOLE FILE, ON THE OWNER'S INSTRUCTION: "reorganize the queue to finish up
#               any research items first so we can get our best and final list of residents and
#               their best and complete profile and businesses and their structures and
#               locations … Keep research first so we can finish that and then all the most
#               visible tickets next … See if there are any duplicate or superseded tickets that
#               can be closed … I want fewer tickets to work." Audited against dev 768afe625:
#               195 lines → 152. Thirty-one withdrawn as superseded or already landed (eight
#               were one publish.sh fault, eight were "dev is red" reports on a dev whose gate
#               is green), twelve folded into nine survivors that asked the same question. The
#               research spend is CAUGHT UP — every ruling that reached a card is on a card,
#               1,282 of 1,282 — so the research band is what is left to spend, the few reads
#               with yield, and T-0987 (the directories, a succession ticket at its foot, filed
#               the same day on his answer). The 1840 census cluster goes to an EPIC: 965 heads adjudicated, 13
#               matched, and the remaining leaves carry industry counts and no names. The
#               triangle ceiling no longer gates roofs (every tier inside, balanced by 81,292),
#               so the roofs band moves up. The FILING RULE above is the same instruction.
#   2026-09-07  THE SAND BAR, over three walkthrough screenshots. First instruction "place that
#               ticket at top of queue"; then his own correction, "that land is showing when it's
#               reconstructed, the tip of the stretch is still off, not as big a deal ... file
#               this ticket in the appropriate place" — so it sits with T-0799/T-0800 instead.
#               Filed as T-0939 and T-0940 after a THIRD id collision: the numbers first used
#               were taken on dev by other runs while this was being written.
#   2026-09-07  "put several tickets at the top of the queue ... whatever is needed so they fire
#               first to merge and close the open PRs ... We want to close as many as you can" —
#               the owner. 22 PRs stood open. A new band LEADS the file: T-0857 first because it
#               is why each of the others costs a lap, then the closures in order of how many PRs
#               a run can retire. The lane went to ONE slice in the same instruction ("1
#               continuous lane"), which is the other half of the fix — two slices meant every
#               landing invalidated the other in-flight branch. Nothing below this band moved.
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
# --- 1. FINISH THE RESEARCH — OWNER INSTRUCTION, 2026-09-10. THIS BAND RUNS FIRST.
# --- ==========================================================================
# --- "finish up any research items first so we can get our best and final list of residents
# --- and their best and complete profile and businesses and their structures and locations".
# ---
# --- WHAT "FINISH" MEANS HERE, MEASURED. measure_research_spend.py: every unit in all nine
# --- sources is READ — 20,739 of them — 7,634 are spent onto a person of 1835, and 1,282 rulings
# --- reached a card with 1,282 written. Nothing adjudicated is unspent. The 13,105 unspent units
# --- are mostly names with no 1835 person to reach (the Newberry index, 4,199 at 0.0% match;
# --- the directories, 7,229 post-1835 arrivals) or figures without names (the census, 84). So
# --- this band is: the spends and identity rulings that still put a person, a trade or a place
# --- on a card, ordered by what each adds; the handful of reads that still yield names; and
# --- T-0987 at its foot, the one open-ended programme, worked a stretch at a time. When it is
# --- empty, the research is finished for this pass and the town below is built from it.
# ---
# --- T-0962 LEADS because it is the honesty check on the sentence above: the spend meter cannot
# --- see a resident_crosswalk in every domain, so "1,282 of 1,282" may be an undercount of what
# --- is still unwritten. Run it, then spend whatever it exposes, here.



T-1002 — Three duplicate-card pairs the candidate test cannot see, because each differs by ONE letter: Madore/Medore Beaubien, Clybourn/Clybourne Archibald, Russel/Russell E. Heacock
T-1013 — Norris prints a firm as 'Jones, B. & Co.' and the firm test only looks before the comma, so 33 firm entries are read as people
T-0901 — A garbled forename on the 1835 side, not the printed one: 'Willınm Bandle' carries a dotless i and refuses its own Fergus 1843 entry
T-0826 — Moses and Kirkland's History of Chicago volume 2 is neither held nor read, and every ABSENT verdict T-0581 recorded is an absence from volume 1 only
T-0910 — Block 4's lot 40 is inside C. Walker's brace on printed page 47 and reaches the reading with no bidder at all
T-0846 — The four other spend passes can write the same paragraph onto a card twice, and their gates cannot see it
T-0830 — The Dalton Data Bank prints two Cook County land purchases of June 1836 that the tract-sales sweep does not hold
T-0987 — The directories' ties and refusals, adjudicated one stretch per run — the 196 ties surname-plus-initial cannot decide, the 1,100 initial-absent refusals a page image can overturn, and every trade and 1839-44 address that lands spent onto the card and the street face; the run that closes this files the next stretch before it closes
# --- T-0987 IS A SUCCESSION TICKET — owner, 2026-09-10: "Directories as a succession ticket at
# --- the end of band 1." The three directories are transcribed in full; what remains is not
# --- reading but adjudication — ~196 ties, ~1,100 initial-absent refusals, ~410 could-carry
# --- trades and addresses — and it is the "documented address from later" he named for
# --- positioning a business. One stretch per run; the run that closes a stretch files the
# --- next one `--after T-0987` before it closes, so this line is the programme's cursor.

# --- ==========================================================================
# --- 2. WHAT THE VISIBLE BAND WOULD TRIP ON — ordering rule 4, and only these three
# --- ==========================================================================
# --- dev IS red on one line at both viewports: the town's wagons stand on 6 headings and the
# --- smoke asks for 8 (desktop 2-3 and mobile 1-4, filed 2026-09-06/07). Every visible PR below
# --- inherits that red in its smoke. T-0836 says why the rule caps at 6 and T-0688 is the
# --- repair; they are one run. T-0763 is why eight "dev is red" tickets were filed on a green
# --- dev and withdrawn today: check.sh's negative-control self-tests print FAIL lines that
# --- look exactly like a failing step.
T-0836 — The town's wagons stand on 6 distinct headings and the smoke asks for 8, so dev is red at both viewports on a layer no branch has touched
T-0688 — The wagon-variety gate counts street bearings, so re-deriving a street took it from 9 buckets to 7 and it is at its floor of 8
T-0763 — check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them

# --- ==========================================================================
# --- 3. THE TOWN, BUILT FROM THE RESEARCH — businesses, their structures and where they stood
# --- ==========================================================================
# --- Owner: "apply the research and spend it to create residents and their business and
# --- residences as reasonably accurate as we can". The standing gap, from town_census.json:
# --- 367 buildings of 667, 29 people housed of 3,265, 1,318 households with no dwelling; 206
# --- businesses, 60 street-only and 71 unplaceable. Roofs and placements first, ordered by
# --- what each puts on the ground; then the identity and anchor repairs those placements
# --- cannot be correct without. The triangle ceiling no longer gates any of this — every tier is
# --- inside its ceiling on dev — so T-0432's four roofs lead, as the owner ruled on 2026-08-30.
T-0432 — Open blk_south_water_dearborn: 4 roofs of headroom on two free lots
T-0385 — The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
T-0895 — The John-Dean house: an army contractor built a five-room house at the foot of Randolph Street in 1815, Beaubien bought it in 1817 for $1,000, and this project models nothing there
T-0894 — Two sources put the Factory House just SOUTH of Fort Dearborn and jb_beaubien_homestead stands north of it: that bearing is all that is left of the identity question, and form.stories waits on it
T-0893 — The Beaubien homestead's phase id and start date still say 1817, and Andreas's own pages say the factory building reached Beaubien in 1822
T-0884 — The register sells Russel Heacock lot 7 of block 117 and his committed house stands 7 m outside block 118: one of the two is out by more than the construction admits
T-0947 — Two reconciliations of the same T-0812 ruling put the Steamboat Hotel 36 m apart: dev carries one and PR #975 the other, with no test that would have caught it
T-0946 — The placement derivation module cannot express a frontage on a street that is not axis-aligned, so the north bank's houses all read not_derivable
T-0948 — A printing that named a street and no anchor, superseded by one of the same house that names one: T-0440 one rank up
T-0949 — The five T-0773 refusals are prose on dev and machine-checked only on a closed branch: the corner-crossing guard, REFUSED_ANCHOR_KINDS and the declared refusals never landed
T-0861 — Eight newspaper claims print a street in their prose and their placement record carries none, so the reading ranks as an address that names no ground
T-0869 — Clark, Filer & Co. advertise a warehouse five doors east of a corner the plat does not have: is the Democrat's 'Randolph st.' a mis-set cross street, or a firm naming a corner it did not stand on?
T-0887 — A well layer, drawn renderer-side: the fort's well is measured to a coordinate and this project has no way to draw one
T-0886 — The water at the foot of Randolph Street is the old channel behind the bar, not the lake: date the channel's 1835 state or find the carts' way across
T-0403 — The Democrat's office keeps its 1834 corner through a merge, and the paper moved along South Water Street before the scene date
T-0411 — A newspaper and its own printing office are two businesses, and the partner-surname guard can never join them
T-0410 — The Howard fire-insurance agency passes between three houses, and the gazetteer has no relation that can hold it
T-0413 — Six of T-0401's surname traps are one house on the printings, and the merge is unwritten
T-0408 — Four spellings of one Lake Street trade take four separate roofs, and the identity layer has judged none of them
T-0398 — A firm's own style stands in its proprietor list, because a claim read the signature where a person was wanted
T-0396 — Newberry & Dole's partner is read as Oliver Newberry in 1834 and Walter L. Newberry in 1835, and the corpus cannot say which stood in the firm
T-0391 — Are 'Eagle Hotel' and 'the Eagle Hotel (Steele's)' one house, and no issue prints both
T-0407 — The same blacksmith notice is read as 'Matthias Nason & Co.' in one impression, and the partner-surname guard can never merge it
T-0404 — 33 documented businesses will stand on a backdating liberty and LIBERTIES.md carries none of them
T-0405 — Adding one signboard repaints every board alphabetically after it, and some lose a line
T-0230 — Two named South Water frontages carry a reconstructed trade, so neither a signboard nor a hitching post will ever stand at them
T-0449 — Four South Water frontage entries declare lots their runs never reach, and each hides its block's headroom
T-0834 — The 665 schedule sizes a block's principal room in party-line units and the generator places by whole lots, and on a business front the two disagree

# --- ==========================================================================
# --- 4. THE GROUND — the Wright 1834 sheet, the mouth, and the west and north banks
# --- ==========================================================================
# --- Owner ask, 2026-09-05, in his own dependency order, with the sand bar's four tickets first
# --- because they are owner-reported from the walkthrough: T-0799 traces it, T-0800 argues its
# --- height, T-0939 stops it running to the horizon, T-0940 makes its surface sand; T-0799 runs
# --- first if any two are picked up. Then the additions Wright draws whole and the town lacks,
# --- then the bank and plat corrections, then the measurements that decide the lot-grid fork.
T-0799 — Trace the whole east edge off the full sheet: both piers, the cut, the sand bar to its tip, the old channel to where Wright closes it, and the shore to the sheet's bottom margin — one run, no window
T-0800 — The mouth as built: the piers as phased structures at their 1835 length, the bar's height argued, the reservation's blue edge and the lighthouse checked, and the epoch re-baked closed
T-0939 — The 1.55 km terrain skirt carries the sand bar's 80 m cross-section south at a dead-constant +1.21 m, so the bar never ends and Wright's hook never forms
T-0940 — The sand bar renders as mesic-prairie green with scrub on it, though z08_lakeshore and z09_sand_prairie cover it and declare sand at 55 and 18 per cent bare soil
T-0789 — Kinzie's Addition is on the sheet whole — 54 numbered blocks, 13 named streets, the Kinzie Block and the river-front water lots — and the North Division carries four streets
T-0790 — Wabansia, surveyed 1831, is drawn whole north of Kinzie Street — eight streets, some 79 blocks and a water-lot tract on the North Branch — and the town has none of it
T-0794 — The two branches run to the sheet's edges and the town's traces stop at the box: the South Branch through the School Section and the North Branch through Wabansia, off Wright
T-0796 — The small tract north of Kinzie Street lettered Michigan St — small parcels and an alley where every neighbour is whole blocks, and a road curving north through it — is unidentified: which survey, which legend swatch, and what the sources call it
T-0768 — West Water Street north of Lake: the 1839 directory attests the reach, and a bank offset there runs through the Wolf Point cluster
T-0827 — The committed market line is fitted to N Wacker Drive and stands 9.1 m off the Thompson plat's own module
T-0770 — south_branch_raft_bridge glosses West Water Street as 'now Canal Street', and the committed canal stands a plat module west of it
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier
T-0255 — The dooryard planting rule reads every street in the town with no bound on reach, so a track across the river can turn a house's yard
T-0858 — The other 34 Original Town numerals are unread because the street grid stops: Wright's Washington-Madison tier, the North Division and the West Division past Clinton
T-0877 — The School Section's twelve north-south lines are read and not committed: Des Plaines, Jefferson, Clinton, Canal, Market, Wells and Clark run south of Madison and five more tiers carry no name
T-0959 — The School Section's tier lines are level and 4th on dev and skewed and 5th on the rival reading: settle the ordinal and the skew against Wright's sheet
T-0878 — Wright's 1834 registration is three per cent long in y: the School Section's mile measures 1658.65 m north-south and 1603.04 m east-west on the same fit
T-0862 — The Wright NARA registration that every Wright-band ticket is built on has no gate: nothing verifies its raster, its checksum or its fit
T-0792 — The legend's nine coloured tracts are the town's survey history — who surveyed what ground, when, for whom — and the project has no tract layer
T-0795 — Every watercourse Wright draws, counted on the new sheet: the three Main Branch sloughs re-checked, and any the BPL tracing windows never covered
T-0689 — The West Division's lot dimensions and lot-counts are still unread off the Thompson plat, and T-0444 closed without them
T-0801 — The pre-fire viewer at /chicago/pre-fire/viewer/ shows 1834 through Hathaway only: put the Wright sheet beside it as the year's second view, with its provenance row, its checksum, and the mirror re-copied
T-0891 — The Fort Cemetery's polygon cannot enter 1835_no_build_ground.json until measure_no_build_ground.py can resolve a ring read off a plate
T-0419 — The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither
T-0421 — Canal Street's three control points spread 2.33 m, so its corridor cannot be centred on any of them
T-0422 — The widened counterfactual deals a roof per street, and every roof a widening adds already fronts another street

# --- ==========================================================================
# --- 5. VISIBLE REFINEMENT — the town changing rather than growing
# --- ==========================================================================
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
T-0520 — The archetype builders compute their own opening rectangles beside the ones facade_openings states, and only a town-wide rebake can join them
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0055 — Hold the Kinzie-view plate as a source record

# --- ==========================================================================
# --- 6. SOUTH THROUGH TIME — owner epic, 2026-09-01, PROMOTED OUT OF EPICS 2026-09-10
# --- ==========================================================================
# --- Owner, 2026-09-10: "move the south through time section below section 5 and above section
# --- 6". It was under EPICS, which the loop does not work until the owner promotes one — this
# --- is that promotion, so these fourteen are workable in rank order like any other band.
# --- One ticket per epoch, in his own order: the shared south terrain first, then 1812, then
# --- the 1880s. Nothing here touches the 1835 town; it stands below every band that does.
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
# --- 7. THE LOOP, ITS GATES AND ITS MEASUREMENTS — invisible, and none of it blocks a visible ticket
# --- ==========================================================================
# --- Ordering rule 4 in the other direction: nothing here outranks the bands above. The
# --- triangle-and-draw-call tickets are here now rather than gating the roofs, because every
# --- tier is inside its ceiling; they are measurement until a breach is measured again.
T-0802 — A ticket whose PR merged can sit 'claimed' forever, because nothing compares ticket state against the PRs that landed
T-0848 — Two smoke checks fail only when mobile stages 9-12 run together — the facade-tone and shadow-reach sensitivity deltas collapse in a combined range
T-0690 — dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4
T-0809 — The janitor gates the branch un-merged and drops a conflict in silence, and the lane outruns its own merge lap
T-0833 — Make a drain lap a tool: tools/drain.mjs, which refuses on any conflict outside the build products
T-0852 — tools/ticket.mjs inflight has a three-hour cold window, so a run that claims and then reads for four hours is invisible to the next run
T-0870 — The pilot and passes 2-5 run their per-person membership assertions on the --gate path, so a member whose letter_list_only flag moves in the tree kills the build instead of being reported
T-0871 — The residents-manifest rebuild has no self-test and silently accepts any flag: nothing proves its assertions fire, and --write typo'd is a green check
T-0896 — Drain the 18 --check-capable tools tools/check.sh never runs: gate each or record why it cannot be gated
T-0856 — read_census_1830.py --check is not in check.sh, and dev was red on it: the 1830 crosswalk had drifted off the folded household tree unseen
T-0662 — check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down
T-0727 — Budget the walkthrough's boot payload, which is what a visitor actually downloads, rather than the whole published tree
T-0437 — The bake smoke clones a 3.2 GB monorepo to test one subtree, and that checkout has killed seven legs at the cap
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0438 — The letter-list cohort is 2.54 MiB of the published tree, and it is now the largest single item in it
T-0537 — The web derivatives are stamped by an unpinned gltf-transform, so a release upstream restamps all 372 of them
T-0776 — A full tools/web_derivatives.sh rewrites 348 derivatives with identical byte counts: the derivative step is not reproducible
T-0777 — assets/manifest.web.json's $note is rewritten with escaped em-dashes, so its own generator does not reproduce what dev committed
T-0829 — A repeated string in a provenance or coverage list is the same merge artefact as a repeated id, and nothing asserts it
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0371 — The lattice path's block rotation is dead code that measure_rank_bias.mjs's drift guard pins in place
T-0053 — A patched lit material silently inherits another layer's shader program
T-0030 — A queue card in Manager reading tickets.json
T-0433 — T-0346's measured costs for the new desktop parts 4, 5 and 6 were never filed, and the two places they are written down disagree
T-0968 — A green deploy is not proof the site is reachable: /chicago/4d/dev/ served a 404 for hours while every deploy reported success, and nothing checks a URL after publishing
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0253 — May an invented building stand on the river margin of a platted street corridor
T-0672 — The three ceilings were raised for one parcel on 2026-09-03 and light's floor was spent: re-measure once #432 lands and take every tier back down
T-0673 — The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured

# --- ==========================================================================
# --- EPICS — future improvements. THE LOOP DOES NOT WORK THESE until the owner promotes one.
# --- ==========================================================================
# --- Owner, 2026-09-10: "if you come across any epic tickets to create like you need to create
# --- more than 5 to complete a ticket then add those to an epic at the bottom of the queue for
# --- future improvements." TWO stand here — South Through Time was the third and the owner
# --- promoted it to band 6 on 2026-09-10. Each is a coherent programme whose tickets belong
# --- together, and neither adds a resident, a trade or a roof to the 1835 town.

# --- EPIC: THE 1840 CENSUS DEPOSIT, READ TO COMPLETENESS — 0 residents. 965 named heads are
# --- adjudicated: 13 matched, 17 candidates, 935 refused (249 unreadable, 411 surnames absent
# --- from 1835). Every left sheet with names has a page file. What remains is continuation
# --- sheets carrying industry and school counts, footing disputes on figures, and one leaf read
# --- three ways. Real, careful work, and it houses nobody. Owner, 2026-09-10: "I think in general
# --- you've tended to create a lot of tickets like all of those census tickets and I am sad".
T-0984 — The remaining eight filled continuations of images 51-74 read one leaf per run, and blank 33SQ-GYYJ-BH recorded swept-and-empty
T-0761 — The banded rule profile read_census_continuation.py needs: the printed rules of a continuation leaf lean up to 41 px and one profile over the whole body loses them
T-0957 — Two readings of 33S7-9YYJ-L3 disagree on the line count and on the printed footing: 27 lines and 115, or 28 lines and 113
T-0942 — The SCHOOLS block of 33S7-9YYJ-L3 carries ink and is unread: the landed reading took the TOTAL column and the footer row and swept nothing to their right
T-0926 — The fifteen: 33SQ-GYYJ-5H's TOTAL column reads 139 against a footed 154, and the residue sits among fifteen inferred figures
T-0934 — A second exposure of 33S7-9YYJ-6H's right edge: the No. of Scholars footing lost its evidence to the gutter and the deposit holds one image
T-0944 — Printed 232's continuation foots 198 against a column that reads 193: T-0642's footing key no longer closes on the one pairing made outside the deposit
T-0971 — The two open columns of printed 240: a repeated two-stroke figure on four cells that closes m_20_30 at 41 or m_30_40 at 13, never both

# --- EPIC: THE NEWBERRY INDEX — 4,199 of 6,658 cards unread at a measured 0.0% match rate.
T-0958 — The Newberry bleed-in test withholds 15 cards under a 15-character run and 43 under a unique-prefix run: one corpus, two rules, and only one is on dev
T-0835 — The Newberry leads re-parse to 8 fewer cards from unchanged card text, so the parser moved under leads.json and the fingerprint gate could not see it

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-0995 — Eleven cards carry a Second Presbyterian roll line that is matched to two or three townspeople each, and not one of them says so
T-0997 — The Chicago Democrat of 29 October 1834 prints the committee of seventy a town meeting appointed against gambling, and the issue has never been extracted: about thirty townspeople named in one claim
T-0999 — Nothing in the gate can see a ruling that is simply GONE: a smaller resident_rulings.json is a legal one, and #1055 lost forty judgements under a green check.sh
T-1003 — The 1840 head crosswalk gathers its 1835 bearers by surname and folds it exactly, so a ruled card merge is invisible to it: Ed. Kimberley fell to L2 when T-1001 landed
T-1004 — Erastus Bowen's card gathers two men: Fergus 1843 prints the city collector and an Erastus Selden Bowen who was sixteen in 1835
T-1005 — Seven cards are flagged letter_list_only while carrying press readings that are not letter lists — Chas. H. Chapman carries three

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-1014 — The card for Nehemiah King gathers every 'N. King' reading in the corpus, and Fergus 1839 prints a Nathaniel King clerking for Tuthill King
T-1015 — The card for Anson H. Taylor carries a press reading of 'Anson W. Taylor' and an 'A. W. Taylor' militia row, against an Anson H. everywhere else
T-1016 — THOMPSON JOHN L was proposed onto a card with no middle initial while the layer holds Lieut J L Thompson, and the same card carries a death notice for Gen. John Leverett Thompson
T-1017 — Is buying at the town's OWN school-section sale a check on a town-side name, or still a bare name? SKINNER JOSEPH and RUSSELL SAMUEL both turn on it

