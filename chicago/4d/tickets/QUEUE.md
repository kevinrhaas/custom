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
#   d. BAND 1 IS CLOSED TO SUCCESSORS (owner, 2026-09-15 — see the ledger). A finding from a
#      research run does NOT go into band 1 under (b), however well it belongs beside its
#      parent. It goes to PARKED RESEARCH at the foot of this file. Case (a) is unaffected —
#      adding a finding to the open ticket that owns it is still right, and is preferred.
#      This clause lapses when the owner reopens the band.
#   Only the owner moves an existing line.
#
# `needs_bake: true` marks a ticket whose merge changes baked geometry. Labels regenerate from
# each ticket's `title:`; if they disagree the ticket wins (T-0217). `epic:` is not load-bearing
# — the BANDS say where a ticket sits.
#
# RE-RANK LEDGER — the instruction behind each pass, newest first
#   2026-09-15  THE RESEARCH BAND IS CLOSED TO SUCCESSORS, on the owner's instruction: "Lots of
#               research tickets keep getting created and worked which is fine but we seem to
#               stay there, I am wondering how much more of that you will do before getting to
#               south through time , we want research to wrap soon and finish up so we can make
#               progress on south through time but I don't want you to abort the research if
#               you are close".
#               WHAT WAS MEASURED, before anything moved. Band 1 has never been empty and has
#               never been long: across the last 25 commits that touched this file it held 1, 2,
#               3 or 4 lines and never 0. It is not a backlog being worked down, it is a
#               TREADMILL — each research run closes one line and files one or two successors
#               into the same band under FILING RULE (b), which says a one-run piece goes
#               directly under the ticket it serves, INSIDE THAT BAND. So the cursor never
#               reaches band 5. T-0987, the succession programme that was the band's large sink,
#               CLOSED on its own yield rule on 2026-09-14 (#1345) and the band refilled the
#               same day anyway. The queue below band 1 is nearly empty: band 2 has 0 lines,
#               band 3 has 0, band 4 has 1 (T-1127). SOUTH THROUGH TIME IS FOUR TICKETS AWAY,
#               and always has been — the distance was never the length of the research, it was
#               the refill.
#               WHAT CHANGED. Nothing moved between bands; no line was added or dropped (64 in,
#               64 out, asserted). One RULE was added — FILING RULE (d): a finding from a
#               research run no longer enters band 1, it goes to PARKED RESEARCH at the foot of
#               this file. Case (a) is untouched and still preferred: a finding that belongs to
#               an OPEN ticket is added to it and nothing is filed.
#               WHAT IS NOT ABORTED, per the second half of the instruction. The three lines
#               standing in band 1 are worked to the end, because each is genuinely close and
#               each already carries its own stopping condition: T-1138 needs one page image and
#               rules three lines on it; T-1134 is piece 3 OF 3 of T-1130 and ends it; T-1135
#               exhausts one tax roll and is allowed to end `undecided` under U1 if the roll
#               does not carry it — "or leave the town two men of one stem" is in its own title.
#               None of them opens a programme. When they land, band 1 is EMPTY, and the next
#               line in rank order is T-1127 (band 4, the wood cut off at the new north edge),
#               then T-0465 and SOUTH THROUGH TIME.
#               T-1027, the one-letter-pairs EPIC, stays in band 6 where it already sits. It is
#               the engine that has been feeding band 1 one cluster at a time; under EPIC rule
#               (c) the loop does not work it until the owner promotes it, and this pass does
#               not promote it.
#   2026-09-14  WHAT THE GROUND LEFT BEHIND, on the owner's instruction after the day's merges:
#               "can you move any necessary tickets up like T-1127. or other of those merged
#               tickets that are important". Three lines moved, all of them findings FILED BY
#               work that landed today rather than new asks:
#                 T-1127 -> band 4, the only line in it. The wood is cut off in a straight line
#                          at the new north edge — a VISIBLE regression from ground that shipped
#                          hours ago, and it sat in band 6, whose own header says "invisible, and
#                          none of it blocks a visible ticket". It is not invisible.
#                 T-1117 -> band 1. Arthur Bronson's card says present on the scene date on the
#                          1833 tax list alone while the town's own historians print him a
#                          visitor; it reaches every card resting on that list.
#                 T-1128 -> band 1. Four adults of St Mary's register with an exact namesake in
#                          the residents layer and no ruling on either.
#               T-0464 CLOSED in the same pass and removed: its work merged as #1257 and the
#               ticket was left `claimed` — the ground reaches Twenty-Second Street, the box is
#               one 2 020 x 4 920 m field, and the drawn street standing off it is 0 m. 61 lines
#               in, 60 out; one closed with a receipt, three moved, none added, none dropped.
#               A duplicated band-3/4 comment block (21 lines, no ticket lines, no ==== borders)
#               was deleted as merge litter, and band 3's lead prose — which still named T-1067's
#               "largest hole in the modelled ground" — rewritten, since T-1067, T-1123 and
#               T-0464 have all landed and the hole is filled.
#   2026-09-13  SOUTH THROUGH TIME BACK BELOW THE VISIBLE BANDS — the owner, hours after the
#               pass below put it on top: "Move south through time so it is just before the
#               number 6 loop improvements". So it sits between VISIBLE REFINEMENT and THE
#               LOOP, which is where his 2026-09-10 instruction had placed it, and the four
#               bands that build the 1835 town run ahead of it again. It stays PROMOTED —
#               workable in rank order, not parked under EPICS — and its own 2026-09-01
#               internal order is untouched. Bands renumbered; no ticket moved between bands,
#               none added, none dropped (76 in, 76 out, asserted). The band's two standing
#               notes travel with it: the 11 February 1835 extension is unresolved so terrain
#               may cross Jackson and a chimney may not, and T-0468..T-0472 are the 1812 Fort
#               Dearborn epoch under AGENTS.md's Indigenous-history constraint.
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
#   2026-09-13  SOUTH THROUGH TIME TO THE TOP, and every unplaced ticket ranked. The owner:
#               "assess any of the unplaced tickets and assess prioritize consolidate all
#               remaining queue tickets, keep south through time first unless there are any
#               tickets you see as dependent necessary to complete first". Its two named
#               dependencies were CHECKED, not assumed, and both had landed that day:
#               T-0219 carries the heightfield through Madison (#1226) and T-0436 commits the
#               corporation's limits (#1238) — whose open question, the 11 February 1835
#               extension, T-0436's run wrote INTO T-0464 rather than filing separately, so it
#               travels with the ticket it binds. Nothing else blocks the band, and it leads.
#               The 17 unplaced tickets are placed by what each adds; SIX BANDS BECAME SIX with
#               nothing dropped (76 in, 76 out, asserted). Four withdrawn: T-1014/T-1015/T-1016
#               were filed on the way past T-0990 cohort C3 as titles with EMPTY acceptances and
#               ask T-1004's question, so they fold there under the FILING RULE's case (a) and
#               their sentences are kept verbatim in it; T-1073 reported dev's check.sh red on
#               sauganash_range_m and T-1083 (#1216) re-banked exactly that, 1066.3 -> 1001.2 —
#               verified by running the gate rather than by reading a green log, because this
#               sandbox has no numpy and that is precisely how a skip reads as a pass (T-1083).
#               NOT consolidated, deliberately: T-1021/T-1022/T-1023 are three distinct faults in
#               one Norris reader, each with 27-33 lines of measured evidence and its own
#               acceptance. Folding them would destroy the evidence, so they are placed
#               ADJACENTLY instead — ordering rule 5, so one run carries the last one's context.

# --- ==========================================================================
# --- 1. FINISH THE RESEARCH — the reads that still yield names, and the rulings that still reach a card
# --- ==========================================================================
# --- Owner, 2026-09-10: "finish up any research items first so we can get our best and final list
# --- of residents and their best and complete profile and businesses and their structures and
# --- locations". That band had drained to its succession ticket alone; these eleven are the
# --- unplaced research findings, ranked by what each ADDS.
# ---
# --- T-0997 leads on yield: the Chicago Democrat of 29 October 1834 prints the committee of seventy
# --- a town meeting appointed against gambling — about THIRTY townspeople named in one claim, and
# --- the issue has never been extracted. T-1051 is next for the same reason: seven unread
# --- impressions of the Lake Street land-agency card. Then the corrections with the widest reach —
# --- T-1022's 294 entries, T-1025's 264 rulings that cannot say which printed line they rest on —
# --- then the card-level rulings, then T-0987, the succession programme, at the foot as before.
# ---
# --- THE THREE NORRIS TICKETS RUN TOGETHER (T-1022, T-1021, T-1023): three distinct faults in
# --- tools/read_norris_1844.py, all found by T-1018, each separately evidenced. They are adjacent
# --- rather than folded so one run carries the context of the last.
# ---
# --- Owner, 2026-09-14: "can you move any necessary tickets up like T-1127. or other of those
# --- merged tickets that are important". These two arrived at the head of this band from band 6
# --- under that instruction, and both are findings the day's merges FILED rather than new asks.
# --- T-1117 is the one with reach: #1323 struck the presence sentence from BRONSON ARTHUR's
# --- ruling because the town's own historians print him a visitor from New York who went home,
# --- and left the general question open — whether the 1833 tax list is evidence of LIVING
# --- somewhere or only of OWNING something there. Every card resting on that list alone turns
# --- on it. T-1128 is the same shape one register over: four adults of St Mary's with an exact
# --- namesake in the residents layer and no ruling on either, which is the state a
# --- consolidation cannot use, because an absent merge reads exactly like a pair nobody has
# --- looked at.
# ---
# --- THIS BAND IS CLOSING, 2026-09-15 (owner: "we want research to wrap soon and finish up so
# --- we can make progress on south through time but I don't want you to abort the research if
# --- you are close"). The three lines below ARE the band — worked to the end, none of them
# --- abandoned, each stopped by its own written condition rather than by this instruction:
# --- T-1138 needs one page image and rules three lines on it; T-1134 is piece 3 OF 3 of T-1130
# --- and ends it; T-1135 exhausts one tax roll and may end `undecided` under U1, which its own
# --- title already allows. Nothing new joins them — FILING RULE (d) sends a research run's
# --- successors to PARKED RESEARCH at the foot of this file instead. When these three land the
# --- band is EMPTY, and the cursor moves on: T-1127, then SOUTH THROUGH TIME.

T-1138 — Geo. Square or Geo. Saver: the three contested lines of the 1 April 1834 return need the page image before any card on them can be ruled

# --- ==========================================================================
# --- 2. THE TOWN, BUILT FROM THE RESEARCH — businesses, their structures and where they stood
# --- ==========================================================================
# --- Owner: "apply the research and spend it to create residents and their business and residences
# --- as reasonably accurate as we can". The roofs and placements that led this band have landed;
# --- what stands here is what the walkthrough cannot yet say about a house and who was in it.




# --- ==========================================================================
# --- 3. THE GROUND — the Wright 1834 sheet, the mouth, and the west and north banks
# --- ==========================================================================
# --- THE HOLE THIS BAND LED WITH IS FILLED, 2026-09-14. It read "T-1067 LEADS this band now and is
# --- the largest hole in the modelled ground: it stops at n +400 m and the whole of Kinzie's
# --- Addition stands north of it — eleven committed streets and 54 blocks on ground the heightfield
# --- does not cover." T-1067 landed (#1317), then T-1123 carried the north wall to n +1120 (#1319)
# --- and T-0464 the south wall to Twenty-Second Street (#1257). The modelled ground is now one box
# --- 2 020 x 4 920 m, Cermak to Kinzie's Addition, and the drawn street standing off it is 0 m.
# --- What the extension LEFT is the next work, and it is visible rather than structural: T-1127,
# --- moved into band 4 below, is the wood cut off in a straight line at the new north edge.


# --- ==========================================================================
# --- 4. VISIBLE REFINEMENT — the town changing rather than growing
# --- ==========================================================================
# --- Owner, 2026-09-14: "can you move any necessary tickets up like T-1127. or other of those
# --- merged tickets that are important". T-1127 leads this band and is the newest visible fault
# --- in the town: the ground reached Kinzie's Addition hours ago (T-1123, #1319) and the stem
# --- budget now binds against a wider field, so the wood stops dead in a straight line at the
# --- north edge. It was filed into band 6 — "invisible, and none of it blocks a visible ticket"
# --- — which is the one thing it is not. A straight edge on the timber is what a visitor sees.
# ---
# --- Also standing: the frontage layer leans on a confidence grade alone to keep street furniture
# --- off an unoccupied invented building, because the hitching rule omits the anonymity clause
# --- the signboard rule applies.



# --- ==========================================================================
# --- 5. SOUTH THROUGH TIME — owner epic, 2026-09-01; PROMOTED, and it sits below the 1835 town
# --- ==========================================================================
# --- Owner, 2026-09-13: "Move south through time so it is just before the number 6 loop
# --- improvements" — so the four bands that build the 1835 town run ahead of it, and it runs
# --- ahead of the loop's own machinery. It is still PROMOTED out of EPICS (2026-09-10), which
# --- means it is workable in rank order like any other band, and its 2026-09-01 internal order
# --- is the owner's own.
# ---
# --- ITS DEPENDENCIES ARE SATISFIED, checked 2026-09-13 rather than assumed: T-0219 carried the
# --- modelled ground through Madison (#1226, 09-12) — the precondition T-0464's own text names —
# --- and T-0436 committed the corporation's limits (#1238, 09-13). Nothing blocks this band; it
# --- sits here because the owner ranked the 1835 town above it, not because it is held.
# ---
# --- THE ONE OPEN QUESTION TRAVELS WITH T-0464 and is not a separate ticket: the corporation's
# --- south leg is JACKSON STREET, and the extension of 11 February 1835 is recorded and NOT
# --- resolved — the act's text is not in this corpus and Andreas misprints its year. T-0436's run
# --- wrote that into T-0464 itself. Terrain may cross Jackson; a CHIMNEY may not, until it is
# --- answered, or the eighteen-inch gate starts conforming buildings to a by-law that may never
# --- have bound them.
# ---
# --- READ THIS BEFORE T-0468..T-0472. These five are the 1812 Fort Dearborn epoch, and AGENTS.md's
# --- standing constraint governs every one of them: do not improvise Native presence,
# --- representation, dialogue or depiction; it is not a research gap to be filled by inference.
# --- T-0470 (the evacuation route and battle-location confidence zone) and T-0472 (the interpretive
# --- scene) are that subject directly. v1 ships NO human figures, uniformly. A run reaching these
# --- builds terrain, structures and documented geography, sets review_required with its reason in
# --- its own words, and takes the depiction question to the owner rather than answering it.
# ---
# --- T-0466 is the tiling and culling plan for the four-kilometre field T-0464 builds. The owner's
# --- order puts it third and it is left there — but a run taking T-0464 should READ it first rather
# --- than size the field twice.









T-0465 — Trace the South Branch and early lakefront through the expanded field
T-0466 — Build a south-terrain tiling and culling plan for a four-kilometre field
T-1143 — The southern stands stand over every scene-detail ceiling, and no ground tiling moves it
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
# --- 6. THE LOOP, ITS GATES AND ITS MEASUREMENTS — invisible, and none of it blocks a visible ticket
# --- ==========================================================================
# --- Ordering rule 4 in the other direction: nothing here outranks the bands above.
# ---
# --- T-0999 LEADS IT, and it is the one entry here that guards another band's work: nothing in the
# --- gate can see a ruling that is simply GONE. A smaller resident_rulings.json is a legal one, and
# --- #1055 lost forty hand-authored judgements under a green check.sh — the research band above
# --- writes exactly that file. T-1029 follows: three derived artefacts stale on dev with nothing
# --- re-deriving them.



T-1129 — Four residents rest only on a Bear Creek, Sangamon County marriage, and their cards say the church list names them at Chicago
T-1108 — Three generators refuse together and none is gated: inf_cooperage_south_branch stands 2.1 m inside the platted Market Street corridor
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
# --- future improvements." THREE stand here. South Through Time was the fourth and is now
# --- band 1. None of these adds a resident, a trade or a roof to the 1835 town.

# --- EPIC: THE 1840 CENSUS DEPOSIT, READ TO COMPLETENESS — 0 residents. 965 named heads are
# --- adjudicated: 13 matched, 17 candidates, 935 refused (249 unreadable, 411 surnames absent
# --- from 1835). What remains is continuation sheets carrying industry and school counts,
# --- footing disputes on figures, and one leaf read three ways. Real, careful work, and it
# --- houses nobody. Owner, 2026-09-10: "I think in general you've tended to create a lot of
# --- tickets like all of those census tickets and I am sad".
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

# --- EPIC: THE ONE-LETTER CARD PAIRS — 68 pairs the exact candidate test cannot see, measured
# --- by tools/measure_card_fuzzy_candidates.py. The list mixes real printed spelling variations
# --- (Foot/Foote, Lloyd/Loyd, Pearson/Pearsons, Pruyne/Pryne) with cards minted off scanner
# --- wreckage, and with pairs that are simply two people one letter apart — John Hale against
# --- John Vale, Mark Noble against Mary Noble. No distance separates the first kind from the
# --- last. Distinct from T-1004, which is one card holding two men a volume already separates.
T-1027 — EPIC: the 68 one-letter card pairs the exact candidate test cannot see, ruled on pages one cluster at a time

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-1115 — consolidate_resident_evidence strips a name's brackets before mint_civic_residents' uncertainty guard can see them, so a surname the page cut in half mints a household: H. G. Hub[…] becomes The Hub household
T-1118 — A bake whose ref merged mid-run still spends the whole bake before the PR is withheld

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-1121 — The minted person hugunin_leonard_c stores the name 'Leonard, C. Hugunin' with the comma one word to the left, so the surname-first rule reads Leonard as the surname though the record id and the gazetteer's other printing both say Hugunin

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-1136 — The far leg of the presence bracket reads a bare year at the year's END, so a death on 8 April 1835 closes the bracket over 1 July
T-1137 — A change to the civic mint's derived note silently deletes every other pass's findings appended to the same card

# --- ==========================================================================
# --- PARKED RESEARCH — filed after the wrap, worked only when the owner reopens band 1
# --- ==========================================================================
# --- FILING RULE (d), owner 2026-09-15. Band 1 kept refilling from itself: a research run
# --- would close one line and file its successors directly beneath, under rule (b), so the
# --- queue cursor never left the band. Successors land HERE now. This is a park, not a
# --- deletion and not a ranking — the findings keep their evidence and their acceptance, and
# --- they are worked when the owner says research reopens. Two things still do NOT come here:
# --- a finding that belongs to an OPEN ticket goes onto that ticket under rule (a), which is
# --- still the preferred answer; and a finding that is not research at all is banded normally.
# --- Empty is the correct state of this section.

# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were
# --- appended here rather than guessed into a band. Rank them or leave them.
T-1140 — C12's roll exhaustion reaches a forename only, and five one-letter SURNAME pairs are the shape it would decide
