# QUEUE — top is next. The parser reads only T-NNNN lines; ticket files hold evidence and acceptance.
# The owner sets the order. Work top-down, skipping a blocked or already-claimed ticket.
# Add findings to an existing ticket first. Put new one-run work beside its dependency;
# add new research readings to RESEARCH COMPLETION so the spend band can drain.
# Split multi-run epics into bounded tickets when reached; do not create a refill at the top.
# Research spend: fix identity/date/mint gates before deriving cards. T-0662/T-1144
# need the blocked T-0660 -> T-0691 letter-list ruling; do not invent its outcome.
# South Through Time: 1812 depiction follows AGENTS.md Indigenous-history review;
# ship no human figures. T-0469/T-0470/T-0471 depend on T-0468; T-0472 on T-0470.
# Prairie Avenue: T-0474 follows T-0473; T-0475/T-0477 follow T-0474;
# T-0476 follows T-0475. Respect needs_bake and other ticket-level blockers.
# Completion: preserve explicit refusals and later/out-of-town evidence; zero
# unclassified research does not mean forcing uncertain people or locations into 1835.
# T-1027 is the one-letter identity epic; Newberry and 1840 deposit work follow
# their lower resident yield. Read each ticket before splitting or claiming.
# --- 1. RESEARCH SPEND — truth, safe derivation, roles, profiles, and locations
T-1155 — The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity
T-1121 — The minted person hugunin_leonard_c stores the name 'Leonard, C. Hugunin' with the comma one word to the left, so the surname-first rule reads Leonard as the surname though the record id and the gazetteer's other printing both say Hugunin
T-1136 — The far leg of the presence bracket reads a bare year at the year's END, so a death on 8 April 1835 closes the bracket over 1 July
T-1129 — Four residents rest only on a Bear Creek, Sangamon County marriage, and their cards say the church list names them at Chicago
T-0856 — read_census_1830.py --check is not in check.sh, and dev was red on it: the 1830 crosswalk had drifted off the folded household tree unseen
T-0662 — check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated
T-1145 — Replace the one-occupation resident field with dated plural roles and migrate every matched trade, profession and civic office without back-projecting later evidence
T-1146 — Spend matched household and person-profile research into structured relationships, names, sex, dates and life events, with every withheld fact legible
T-1108 — Three generators refuse together and none is gated: inf_cooperage_south_branch stands 2.1 m inside the platted Market Street corridor
T-1147 — Spend every defensible home, workplace and business-location finding, preserve the 123 location limits, and close research with zero unclassified attested or inferred fact
T-1144 — Converge the resident layer after the standing truth tickets: zero synthesis and mint drift, no false Chicago resident, and no 1835 claim above its dated evidence
# --- 2. SOUTH THROUGH TIME — dated terrain, Fort Dearborn, and Prairie Avenue
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
# --- 3. LOOP IMPROVEMENTS — scene budgets, gates, build cost, and rendering
T-1154 — The five downtown stands are over every scene-detail ceiling at both viewports, and the town has been over since some point after 6 September
T-1156 — Wire measure_boot_payload.mjs --check into the nightly gate so the 12 MB boot budget refuses without a human
T-0437 — The bake smoke clones a 3.2 GB monorepo to test one subtree, and that checkout has killed seven legs at the cap
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
T-0252 — Decide once whether a baked town carries the nine renderer-drawn layers, or none of them
T-0285 — An asset carrying its own AO map cannot batch with the town: +2 draw calls for one building
T-0286 — The AO unwrap leaves 68.9 per cent of every atlas empty, and the map is priced as if it were full
T-0364 — Two byte-identical copies of changelog.js are 7.2 per cent of the published payload, and they grow on every release
T-0053 — A patched lit material silently inherits another layer's shader program
T-0371 — The lattice path's block rotation is dead code that measure_rank_bias.mjs's drift guard pins in place
T-0433 — T-0346's measured costs for the new desktop parts 4, 5 and 6 were never filed, and the two places they are written down disagree
T-0030 — A queue card in Manager reading tickets.json
# --- 4. RESEARCH COMPLETION — remaining readings, identity epics, and deposit closeout
T-1153 — Rule the 28 readings of the 1 April 1834 return where the page and the extraction set a name differently, and lift the two lines no claim carries
T-1140 — C12's roll exhaustion reaches a forename only, and five one-letter SURNAME pairs are the shape it would decide
T-1027 — EPIC: the 68 one-letter card pairs the exact candidate test cannot see, ruled on pages one cluster at a time
T-0835 — The Newberry leads re-parse to 8 fewer cards from unchanged card text, so the parser moved under leads.json and the fingerprint gate could not see it
T-0958 — The Newberry bleed-in test withholds 15 cards under a 15-character run and 43 under a unique-prefix run: one corpus, two rules, and only one is on dev
T-0761 — The banded rule profile read_census_continuation.py needs: the printed rules of a continuation leaf lean up to 41 px and one profile over the whole body loses them
T-0984 — The remaining eight filled continuations of images 51-74 read one leaf per run, and blank 33SQ-GYYJ-BH recorded swept-and-empty
T-0957 — Two readings of 33S7-9YYJ-L3 disagree on the line count and on the printed footing: 27 lines and 115, or 28 lines and 113
T-0942 — The SCHOOLS block of 33S7-9YYJ-L3 carries ink and is unread: the landed reading took the TOTAL column and the footer row and swept nothing to their right
T-0926 — The fifteen: 33SQ-GYYJ-5H's TOTAL column reads 139 against a footed 154, and the residue sits among fifteen inferred figures
T-0934 — A second exposure of 33S7-9YYJ-6H's right edge: the No. of Scholars footing lost its evidence to the gutter and the deposit holds one image
T-0944 — Printed 232's continuation foots 198 against a column that reads 193: T-0642's footing key no longer closes on the one pairing made outside the deposit
T-0971 — The two open columns of printed 240: a repeated two-stroke figure on four cells that closes m_20_30 at 41 or m_30_40 at 13, never both
