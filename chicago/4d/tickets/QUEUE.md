# QUEUE — top is next. The parser reads only T-NNNN lines; ticket files hold evidence and acceptance.
# The owner sets the order. Work top-down, skipping a blocked or already-claimed ticket.
# Add findings to an existing ticket first. Put new one-run work beside its dependency;
# add new research readings to RESEARCH COMPLETION so the spend band can drain.
# Split multi-run epics into bounded tickets when reached; do not create a refill at the top.
# Research spend: fix identity/date/mint gates before deriving cards. THE LETTER-LIST
# RULING IS MADE (owner, 2026-09-18: option (c) on T-0660) — refusals 7 and 8 are
# mint-time rules and do not un-mint a standing record; nothing is retired, rank() is
# unchanged, and the pass SAYS a collision instead of acting on it. T-1144 is no longer
# waiting on anything and is the queue's second row; the line that told runs to skip it
# is gone with this. T-0691 shrinks to wiring its --check into check.sh.
# South Through Time: 1812 depiction follows AGENTS.md Indigenous-history review;
# ship no human figures. T-0469/T-0470/T-0471 depend on T-0468; T-0472 on T-0470.
# Prairie Avenue: T-0474 follows T-0473; T-0475/T-0477 follow T-0474;
# T-0476 follows T-0475. Respect needs_bake and other ticket-level blockers.
# Completion: preserve explicit refusals and later/out-of-town evidence; zero
# unclassified research does not mean forcing uncertain people or locations into 1835.
# T-1027 is the one-letter identity epic; Newberry and 1840 deposit work follow
# their lower resident yield. Read each ticket before splitting or claiming.
# Reconstruction (owner, 2026-09-17): BAND 2 IS OPEN NOW — it reads the layer and writes
# reports, models and an order book, and it needs no sign-off to do that. Bands 3-5 WRITE
# reconstructed people, businesses and roofs, and those wait for T-1157 to say GO.
#   The first cut gated 2-5 together, and it starved the top: band 1's rows were all in
#   flight or self-blocked, so runs fell past 59 gated tickets into SOUTH THROUGH TIME and
#   LOOP IMPROVEMENTS (T-0467, T-1154, 2026-09-17). A gate that empties the top of the
#   queue sends the loop to the bottom of it.
# Every reconstructed value carries tier, basis, seed and replaceable_by (T-1158); the order
# book (T-1166) is the quota; docs/RESEARCH/1835_reconstruction_plan.md is the map.
# Sub-bands (3A/3B/3C, 5A-5E) may be taken by different agents; within a sub-band, top first.
# Build tickets in 5C are needs_bake and hand on a successor. Native, Métis and Black residents,
# families and businesses ARE reconstructed (owner, 2026-09-17; T-1177), review_required, no figures.
# Owner, 2026-09-17: THE CITY COMES FIRST. Bands 6 (arrival and jaunts) and 7 (south
# through time) are PARKED BEHIND IT — jaunts first, then south through time. They were
# numbered 5F-5J, which read as part of the 5A-5E structures programme and is why they
# looked like city work; they are band 6 now so the ordering says what it means.
#   AND A RUN MAY NOT FALL INTO THEM. While any row in bands 1-5 is workable, that row is
# the work. If the top is gated or every row is in flight, the run SAYS SO and stops — it
# does not walk down to bands 6–9. That fall-through is how T-0467 and T-1154 were
# picked up out of the bottom of a 148-line queue on 2026-09-17 while the city waited.
# TICKET BUDGET (T-1295, owner 2026-09-17: "I don't want too many tickets and not making
# any progress"). `ticket.mjs new` REFUSES at 140 queue lines, and refuses a branch its
# fourth new ticket. Override is `--anyway --why "<reason>"` and the reason is written into
# the file. Filing is free and working is not — add a finding to the ticket it was found in
# first, which is what the line above already asks for. `split` is exempt: it replaces a
# ticket rather than adding one. An EPIC states its own cap in children (T-1236: three).
# --- 0. BLOCKING THE QUEUE (owner, 2026-09-20). These rows are first because the loop
# --- cannot judge its own work until they are done. FOUR assertions have been standing
# --- red on dev for days, and because they are red, smoke_budget reports every leg that
# --- covers them as 'already red on dev' and runs skip it — so a real regression in those
# --- parts would look exactly like the reds already there. The gate is not measuring.
# --- Below them: the deadlock that needed hands on four PRs in one evening, and the two
# --- derivation faults that cost cycles on every branch that re-derives.
# --- The old note here described the terrain fossil on #1521/#1518, cleared 2026-09-19.
T-1369 — Dev is red at desktop part 3: T-1171's drawn wife lands on an evidence-only household (hh_inf_cooper_north_04), and the placeholder label no longer agrees with its asset
T-1331 — The placeholder-label smoke check reads a field that does not exist, so parts 2-3 have been permanently red on a typo
T-1453 — Two gated writers carry a placement the coverage audit does not count, so it says 208 measured and accounts for 206 — and the one whose ordering is unrecorded cost three gate cycles today
T-1363 — rederive.mjs --run does not converge in one pass when the town model moves: the arrival stage draws from a file the sequence rebuilds after it


# --- 1. RESEARCH SPEND — truth, safe derivation, roles, profiles, and locations
# --- 2. 1835 TOWN ANALYSIS — the known population profiled, the town modelled, the order book (OPEN NOW)
T-1439 — The order book reports a false delta of ten institutional roofs: programme_deltas reads the town model's institutional HIGH end, which includes the fort's ten principal roofs, against district_group_matrix.institutional_public alone — and the boarding-house row beside it compares that matrix with a figure read off the same matrix, so it can never disagree
T-1420 — build_order_book_1835.py hands the west ground units to T-1192, which is now split: the owner list needs its live successor T-1414 (and the same sweep for any other ticket id the order book names that has since closed or split)
# --- 3A. RECONSTRUCT RESIDENTS — programme, then complete the known people (attributes, arrival, families, re-admissions)
T-1448 — Mint the staffing shortfall to the model's typical band: the 105 reconstructed hands 96 houses are still short, written as a stage of the resident reconstruction programme into cards of their own, each carrying its house, its role and where it slept, and nothing already committed written to
T-1459 — Re-cut the order book's unfilled remainder to the adult sex ratio the town model already states, and reopen the 10-19 trade band the 1840 schedule drew out — the 78 filled buckets and their 1,370 drawn persons do not move
T-1489 — Carry a reconstructed employment seat back onto the card of the person who holds it: the six mint-owned resident directories re-derive whole, so workplaces[] stops at households/ and 91 of the 124 seated people say nothing about work on their own card
T-1379 — The borderline roster keys the resident layer by the name a source prints, so a read name a crosswalk merged into a differently-spelt card is offered for re-admission beside the card that already holds the person
T-1383 — The two women the St Mary's priest wrote down as Indigenous are the only adults on their own entries the borderline roster ruled ineligible, so the town carries their husbands and children and not them
T-1395 — The name reader calls one named woman a group: 'The Harmon daughter later known as Mrs A. G. Burley' trips the COLLECTIVE article rule, so her age band carries a refusal written for a collective row
T-1374 — The Indian Agency establishment of 1835: the agent, sub-agent, interpreter and agency blacksmith as the sources name them, and the Native and Metis employees and families the records only count, through T-1177's review rules
T-1294 — hh_inf_joiner_north_02 stands in the tree and no pass derives it: the register deal seats four roofs where its own docstring says five, and J. W. Reed's household is owned by nobody
T-1299 — Admit the ten scene-reaching press roles into the 1835 occupation field by making the four generators that own it agree
T-1354 — The six documented departures from Chicago, read against present_on_scene_date: whether a man recorded leaving in 1835 was at the town on 1 July, each ruled with the removal beside the other sources rather than out of one volume
# --- 3B. RECONSTRUCT RESIDENTS — fill the model: trades, women and children, lodgers, garrison, cohorts, transients
# --- 3C. RECONSTRUCT RESIDENTS — converge
# --- 4. BUSINESSES — the authored layer and view, the audit, staffing model, five reconstruction groups, staff, converge
T-1469 — Spend the trade and premises enrichments against the finished business layer: every corroborated_enrichment naming a trade, a shop, a tavern, a store or the premises one was kept at reaches a structured field on its record or is refused with its reason
T-1470 — Spend the firm notices and the civic and business ledger domains: every unit carrying a business block reconciled against the layer that now exists, minted nowhere and refused where the reading does not reach
T-1471 — Answer the tavern identity question the roof programme is owed: whether the register's 15 scene-date tavern records are that many HOUSES, with the fold or the refusal to fold on the records and the inns_taverns group re-cut or left alone on the measurement

# --- 5A. STRUCTURES — ground: north and west streets and alleys, terrain extent, the lot grid beyond the river
T-1479 — Move blk_lake_clinton and blk_randolph_clinton onto the West Division grid: blocks 28 and 45 re-cut in the sheet's own arrangement, with the structures seated on their lots re-seated

# --- 5B. STRUCTURES — seating: placement policy, roof programme re-derived, anonymous roofs redealt, everyone seated
T-1429 — The nearest-street reading crosses the river: a bank test for nearest_frontage, so a roof is not credited with a corridor on the far side of the water
T-1444 — Release generate_west_infill's 35 held slots onto the extended ground: the terrain gate retired, the placements instantiated and baked
T-1492 — Seat the reach: the address book's reconstructed rungs — a block face for a street-only row, a division band where only the division is known, the policy's band where nothing is — seeded, tier-marked, and every household's division re-derived from its row so the People view's division filter fills
T-1493 — Go to the seat: the Go-to button carries a visitor to the lot or the block face a household or firm is seated on, not only to a named roof
T-1484 — Carry the North Division parcel's nine roofs across that surface: the recipe's family, suffix, inventory_class and totals re-dealt, generate_north_infill re-deriving byte for byte, the assets renamed, the household workplaces resolved, rebaked and published
T-1481 — Migrate the phase-one South parcel's eleven refamilied roofs whose id moves, on the North parcel's executor: generate_inferred_infill re-deriving byte for byte, the assets and the measured reference list carried across, rebaked and published
T-1482 — Migrate the three platted blocks' six refamilied roofs, whose ancillary slots cross the principal/ancillary line: generate_block_infill's claimed principal/ancillary mix re-dealt rather than field-edited, the ids carried across the reference list, rebaked and published — with the screenshot from Lake and Clark
T-1495 — Migrate the North Division parcel's 9 refamilied roofs whose id moves: the recipe's suffix, family, inventory class and authored footprint re-dealt against the new bands, the parcel's group and family totals recomputed, every file naming an old id moved with it, rebaked and published
T-1496 — Re-deal the three platted blocks' 6 refamilied roofs across the principal/ancillary line: generate_block_infill gates a block's claimed schedule and refuses a second principal roof on a lot that already has one, so an ancillary yard building moved into a dwelling family is a re-deal of the block's mix, not a field edit; with the screenshot from Lake and Clark
T-1199 — Seat every reconstructed household, business, lodging house and camp by the placement policy into the extended lot grid: multiple buildings per main-street lot, single roofs on the back streets, labourers on the small lots and fringes, the noxious trades on the branches — deterministic, order-book-counted
# --- 5C. STRUCTURES — build, one district per run, baked, successor handed on (frame budget measured before every push)
T-1200 — Build the South Water Street river front to its seats: the forwarding houses, warehouses, stores and store-residences on the party lines from Market to State, the freight sheds and landings behind, every roof with its firm and its keeper
T-1201 — Build the Lake Street and Dearborn–Clark–LaSalle core to its seats: the store fronts and store-residences, the hotels' neighbours, the professional offices over shops, the mechanics' shops on State and Dearborn, the cottages behind them
T-1202 — Build the Randolph–Washington tier and the public square's neighbours to their seats: the professional and merchant houses (H1/H2), the churches and schools the civic band established, the log jail and the estray pen as they stand, the dwellings falling southward
T-1203 — Build the South Division's outer ground to its seats: the Fort Dearborn Addition and Michigan Street tract dwellings, the Clark–State cottages south of Washington where the ground allows, the packing and slaughter yards on the South Branch, the country places outside the plat
T-1204 — Build the fort reach and the lakefront to their seats: the sutler's, the garrison's outbuildings and the Agency establishment as the dossiers allow, the lighthouse keeper's, the pier-works yard at the river mouth, the Lake House's neighbours on the north bank east end
T-1205 — Build the North Division's Kinzie band to its seats: the Kinzie properties' neighbours, the North Water bank's forwarding and heavy trades, the Wolcott–Kinzie core's stores and taverns, the brickyard and the school, the dwellings between Kinzie and Michigan
T-1206 — Build Kinzie's Addition and the north tier to their seats: the labourers' and mechanics' cabins, shanties and small cottages on the addition's small lots, the scattered better houses on the Rush–Pine fringe, the open ground left honestly open
T-1207 — Build the West Division's Wolf Point and Canal Street approach to their seats: the taverns' yards and stables, the grocery and blacksmith on the approach, the ferry and the bridge heads, the cabins and boarding houses of the forks
T-1208 — Build the West Division's outer clusters and Wabansia to their seats: the three looser clusters toward the Des Plaines edge, the Wabansia cabins on the North Branch, the farms and barns on the prairie edge, the held 35 slots released on the extended ground
T-1209 — Build the boarding houses to their beds: the H1–H3 houses the lodging model sized, each with the window rhythm, service wing and stovepipes its capacity implies, its stable and privies, on the seats near the landings and approaches — and re-size the named hotels' outbuildings to their guests
# --- 5D. STRUCTURES — finish: fabric by household, plank walks, yards, signs, camps
T-1210 — Deal building fabric, finish and weathering by who lived and worked there: a physician's or forwarder's house painted and glazed, a tradesman's cottage weathered clapboard, a labourer's cabin unpainted and patched — the rule set on the material sheet, applied to every dwelling and business, no attested finish moved
T-1211 — Plank sidewalks, stoops, hitching posts and street crossings for every business face, varied by the business — a forwarding house's wide decked walk, a store's board walk and stoop, a smithy's bare ground and rail, a tavern's posts and mounting block — extended to the new fronts town-wide
T-1212 — Yards for every household: lot-line and dooryard fences, gardens, woodpiles, wells, privies and stables assigned by household type, wagons and barrels and trade goods at the shops by trade — the enclosure, yard and outbuilding layers extended to the reconstructed town
T-1213 — Signboards for every business that would have hung one: the reconstructed firms' names and trades in period lettering and forms, the attested signs untouched, the signless trades left signless by rule
T-1214 — Build the camps of the summer of 1835: a tent and wagon-camp archetype, the encampments on the grounds the transient ticket evidenced — the land-sale crowd south of the fort, the immigrants' wagons at the west approach, the pier gang at the river mouth — bounded, labelled, and empty of figures
# --- 5E. STRUCTURES — converge: every person housed, every business roofed, the town complete
T-1215 — Converge the reconstructed town: every person housed, every business roofed, every roof occupied or its use stated, the census's dwellings ratio met, the programme reconciled, the budgets re-measured and set — the completion report a visitor can open
# Arrival/jaunts: read docs/ARRIVAL-JAUNTS-EXECUTION.md; honor ticket dependencies.
# Finish each subsection; unavoidable successors stay beside their dependency, not at the tail.
# --- 6A. ARRIVAL AND SOURCES — measured loading, time rollback, source library, free start
T-1292 — Move the town census off the loader into an Evidence → City summary topic
T-1247 — Roll the year back into a restrained time-machine arrival
T-1248 — Compile the sources used and their reconstruction backlinks
T-1275 — Give the loading journey 160 varied source and reconstruction statuses
T-1276 — Browse every source the reconstruction used, with its counts and used-for links
T-1277 — Share one destination search for Go to and Explore Myself
T-1278 — Land on a warm mobile welcome with Jaunts and Explore Myself
# --- 6B. JAUNTS ENGINE — content contract, navigation, travel, choices, history and menu
T-1253 — Define validated jaunt JSON and render a real pilot preview
T-1279 — Make the pilot jaunt playable with persistent stop navigation
T-1280 — Offer live jaunt travel modes and honest quick-play estimates
T-1256 — Support bounded choices, inventory and alternate jaunt endings
T-1257 — Connect jaunt stops and travel to optional historical context
T-1258 — Collect era-themed keepsakes in a five-family Chicago daybook
T-1259 — Finish the scalable Jaunts Menu and integrated start experience
# --- 6C. PRIORITY JAUNTS — six short stories, fully authored and playable
T-1260 — Publish Outfit for the West as a five-minute jaunt
T-1261 — Publish Taverns of Chicago as a five-minute jaunt
T-1262 — Publish New in Chicago as a five-minute jaunt
T-1263 — Publish Shopping South Water Street as a five-minute jaunt
T-1264 — Publish Across Wolf Point as a five-minute jaunt
T-1265 — Publish Fort Dearborn Errand as a five-minute jaunt
# --- 6D. EVERYDAY JAUNTS — nineteen additional outings in five bounded content batches
T-1266 — Publish news, mail, lodging and work jaunts
T-1267 — Publish land, freight, household supplies and clothing jaunts
T-1268 — Publish harness, candles, building materials and leather jaunts
T-1269 — Publish schooling, social visits and careful news reading jaunts
T-1270 — Publish harbor, prairie arrival and a quiet stroll jaunts
# --- 6E. ARRIVAL AND JAUNTS COMPLETE — content convergence and published mobile acceptance
T-1271 — Reconcile and time the complete 25-jaunt library
T-1272 — Verify arrival, jaunts and source browsing on the published mobile app
# --- 7. SOUTH THROUGH TIME — dated terrain, Fort Dearborn, and Prairie Avenue
T-1286 — Cross-check the derived 1812 pre-cut shore against the Harrison 1830 trace, and record what the two readings disagree about
T-1243 — Author the e1830_natural terrain spec and generate the 1812 heightfield and the ground and water meshes across the Fort-to-Eighteenth-Street corridor
T-0469 — Reconstruct the first Fort Dearborn complex as it stood in August 1812
T-0470 — Map the 15 August 1812 evacuation route and battle-location confidence zone
T-0471 — Build the 1812 lakeshore prairie, vegetation and landscape features
T-0472 — Build the 1812 interpretive scene with Indigenous-history review gates
T-1250 — Trace the 1880s Illinois Central lake edge and fill shore_1880s_ic_edge from a sourced period sheet
T-1251 — The e1871_postfire terrain spec: the graded, filled and raised South Side ground as an authored zone table
T-1252 — Generate and bake the e1871_postfire heightfield over the Prairie Avenue reach
T-0474 — Reconstruct the 1880s Prairie Avenue street, parcel and service grid
T-0475 — Build the Prairie Avenue landmark mansion core
T-0476 — Fill the 1880s Prairie Avenue corridor with documented residences and outbuildings
T-0477 — Build the 1880s Prairie Avenue streetscape, vegetation and urban furniture
# --- 8. UNREAL DELIVERY — repeatable native builds, web parity, then streaming
# Programme: T-1356; docs/unreal/README.md. Owner-ranked here on 2026-09-18.
# Remote-workable preparation (still subject to the city-first ordering above):
T-1357 — Publish a versioned Chicago scene bundle from every successful scheduled asset bake
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
# LOCAL / QUALIFIED UNREAL ONLY — NOT WORKABLE BY THE REMOTE WEB WORKER.
# HOLD references below are comments, not claimable queue entries. Tickets are blocked-tech.
# HOLD T-1472 — on-demand latest-validated Mac build/release; qualified Mac + release access.
# HOLD T-1473 — sinking buildings/terrain contact; qualified Unreal + matched web/source views.
# HOLD T-1358 — after T-1357 and current Unreal/GPU capability receipt.
# HOLD T-1360 — after T-0252, T-1357, T-1358; Unreal visual/collision receipt required.
# HOLD T-1474 — flora corridor; after shared exports/import and placement, Unreal visual/performance proof.
# HOLD T-1475 — map/search/place inspection; runtime provenance and Unreal input/route validation.
# HOLD T-1359 — streaming corruption; affected Mac/Unreal/browser access, after native priorities.
# HOLD T-1361 — after T-1358/T-1359, approved licensed build runner, GPU host, budget and credentials.
# Coordinator: unblock only when all dependencies AND current executor capability are proven;
# immediately assign/claim on that eligible executor; otherwise retain blocked-tech.
# Return unblocked work to this band in the displayed order; do not leave local work open
# for the general loop. The held epic is a tracker, never a claimable task.
# --- 9. LOOP IMPROVEMENTS — scene budgets, gates, build cost, and rendering
T-1222 — Read the letter-list mint's 798-file drift and give the pass a check the gate can run at its own place in the pipeline
T-1341 — ticket.mjs --check REPAIRS the mirror it is checking, so on any branch that adds a ticket the gate's queue step mutates tickets.json while the pool reads it — the T-0856 check-that-repairs fault, one tool over
T-1344 — Splitting a ticket that has a live branch puts two runs on one acceptance: the in-flight run retargets onto a child while the child also enters the queue for a fresh claim, and neither claim contends with the other
T-1345 — step_isolation exempts gitignored build products by a hand-kept path list, when git check-ignore can classify them: a write to an ignored path is a build product and a write to a tracked one is a tree mutation, and the gate should ask rather than be told
T-1355 — The four derived research reports conflict on every merge: decide whether they come off the PR surface the way T-0937 and T-0938 took the board and the mirror, with the reading written down
T-1362 — The lap re-derives only when it merges, so a branch already current with dev stays stale against a gate dev just added: #1487 sat red on four manifest-owned files while the lap said 'already current — nothing to lap'
T-1380 — A squash merge dropped a shipped release note and re-used its version: v971 named 'Six dates that would not stick' on dev at 06:06 and names 'How many people each tavern and boarding house could sleep' at 06:31, and the first entry is gone from the file the launcher and Manager parse
T-1282 — The lap cannot re-derive a resident household card, so any PR that conflicts on hh_*.json is refused whole
T-1118 — A bake whose ref merged mid-run still spends the whole bake before the PR is withheld
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down
T-0673 — The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured
T-0672 — The three ceilings were raised for one parcel on 2026-09-03 and light's floor was spent: re-measure once #432 lands and take every tier back down
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0438 — The letter-list cohort is 2.54 MiB of the published tree, and it is now the largest single item in it
T-0777 — assets/manifest.web.json's $note is rewritten with escaped em-dashes, so its own generator does not reproduce what dev committed
T-0776 — A full tools/web_derivatives.sh rewrites 348 derivatives with identical byte counts: the derivative step is not reproducible
T-0829 — A repeated string in a provenance or coverage list is the same merge artefact as a repeated id, and nothing asserts it
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0253 — May an invented building stand on the river margin of a platted street corridor
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0053 — A patched lit material silently inherits another layer's shader program
T-0371 — The lattice path's block rotation is dead code that measure_rank_bias.mjs's drift guard pins in place
T-0433 — T-0346's measured costs for the new desktop parts 4, 5 and 6 were never filed, and the two places they are written down disagree
T-0030 — A queue card in Manager reading tickets.json
# --- 10. RESEARCH COMPLETION — remaining readings, identity epics, and deposit closeout
T-1219 — The three re-spelled cards still say in prose that the papers print the reading T-1139 overturned: hh_fraser_wm_h reads 'Wm. H. Frazer' and its own note says the papers print 'Wm. H. Fraser'
T-1281 — Is the Democrat's 'A. Sweet' of 4 June 1834 Alanson Sweet or the Alon[s]on Sweet of the same column
T-1315 — Spend the three dated birth and age enrichments T-1301 routed to T-1168: robinson_alexander, kimberly_edmund_s and maxwell_philip each carry a sourced birth date or age no field held when the reading was made, and both fields exist now
T-1335 — Spend the kin the church registers, the papers' family columns and the completed resident enrichments state — the 166 units T-1320's book pass was never scoped for, plus the two book relatives it left unruled: ties written onto held cards, nobody minted
T-1273 — Write every committed home and workplace reconciliation row as an associated_with row on the record it belongs to, changing no value, confidence or source
T-1274 — Move the renderers and tools off the singular lives_at/works_at once the plural rows carry every claim, and retire the pair

