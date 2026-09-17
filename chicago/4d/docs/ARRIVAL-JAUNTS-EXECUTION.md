# Arrival and jaunts — execution plan

Owner-directed ticket plan, 17 September 2026. **Planning is complete; implementation is queued.**
The owner approved **summer 1835** wording; the scene date stays 1835-07-01.

[Architecture and acceptance contracts](ARRIVAL-JAUNTS-ARCHITECTURE.md) · [25 content briefs](JAUNTS-INITIAL-LIBRARY.md) · [Queue](../tickets/QUEUE.md)

## Where this work sits

The five subsections sit after reconstruction convergence (T-1215) and immediately
before South Through Time. All previous ticket ordering is preserved. The owner
explicitly requested this multi-ticket plan here; the normal rule to park unrequested
large epics at the foot does not apply to this promoted work. No existing research,
business or boot-budget ticket is duplicated. Every new ticket is open, owner-requested,
and M (one run, tight); none is claimed or completed by this planning PR.

Work top-down after checking remote claims and named predecessors. A preceding band
is not permission to bypass a held claim. Shared compiler/engine files land first;
content batches then own separate JSON files and can be allocated independently.
Do not change engine behavior in a content batch merely to fit a story. Each ticket
owns its focused tests; the final two tickets are integration checks with corrections.

Finish each subsection. Only if a genuine remaining piece cannot fit should a focused
successor be inserted beside its dependency in this band. Update this mapping, keep
subsections below 15 tickets, and do not send unfinished work to the bottom or close
an incomplete ticket. The existing claims, sizing, provenance, preflight and dev-only
merge workflow remain in force.

## 5F. Arrival And Sources — Measured Loading, Time Rollback, Source Library, Free Start (7 tickets)

| Ticket | Bounded delivery | Prerequisites |
|---|---|---|
| [T-1246](../tickets/T-1246-expose-real-boot-phases-and-yield-long-scene-bui.md) | Expose real boot phases and yield long scene-building tasks | Existing dev |
| [T-1247](../tickets/T-1247-roll-the-year-back-into-a-restrained-time-machin.md) | Roll the year back into a restrained time-machine arrival | T-1246 |
| [T-1248](../tickets/T-1248-compile-the-sources-used-and-their-reconstructio.md) | Compile the sources used and their reconstruction backlinks | Existing dev |
| [T-1275](../tickets/T-1275-give-the-loading-journey-160-varied-source-and-r.md) | Give the loading journey 160 varied source and reconstruction statuses | T-1247, T-1248 |
| [T-1276](../tickets/T-1276-move-city-statistics-into-a-browsable-sources-an.md) | Move city statistics into a browsable Sources and City summary | T-1248 |
| [T-1277](../tickets/T-1277-share-one-destination-search-for-go-to-and-explo.md) | Share one destination search for Go to and Explore Myself | Existing dev |
| [T-1278](../tickets/T-1278-land-on-a-warm-mobile-welcome-with-jaunts-and-ex.md) | Land on a warm mobile welcome with Jaunts and Explore Myself | T-1247, T-1276, T-1277 |

## 5G. Jaunts Engine — Content Contract, Navigation, Travel, Choices, History And Menu (7 tickets)

| Ticket | Bounded delivery | Prerequisites |
|---|---|---|
| [T-1253](../tickets/T-1253-define-validated-jaunt-json-and-render-a-real-pi.md) | Define validated jaunt JSON and render a real pilot preview | T-1248, T-1277, T-1278 |
| [T-1279](../tickets/T-1279-make-the-pilot-jaunt-playable-with-persistent-st.md) | Make the pilot jaunt playable with persistent stop navigation | T-1253 |
| [T-1280](../tickets/T-1280-offer-live-jaunt-travel-modes-and-honest-quick-p.md) | Offer live jaunt travel modes and honest quick-play estimates | T-1279 |
| [T-1256](../tickets/T-1256-support-bounded-choices-inventory-and-alternate-.md) | Support bounded choices, inventory and alternate jaunt endings | T-1279 |
| [T-1257](../tickets/T-1257-connect-jaunt-stops-and-travel-to-optional-histo.md) | Connect jaunt stops and travel to optional historical context | T-1279, T-1280, T-1276 |
| [T-1258](../tickets/T-1258-collect-era-themed-keepsakes-in-a-five-family-ch.md) | Collect era-themed keepsakes in a five-family Chicago daybook | T-1256, T-1257 |
| [T-1259](../tickets/T-1259-finish-the-scalable-jaunts-menu-and-integrated-s.md) | Finish the scalable Jaunts Menu and integrated start experience | T-1279, T-1280, T-1258, T-1278 |

## 5H. Priority Jaunts — Six Short Stories, Fully Authored And Playable (6 tickets)

| Ticket | Bounded delivery | Prerequisites |
|---|---|---|
| [T-1260](../tickets/T-1260-publish-outfit-for-the-west-as-a-five-minute-jau.md) | Publish Outfit for the West as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |
| [T-1261](../tickets/T-1261-publish-taverns-of-chicago-as-a-five-minute-jaun.md) | Publish Taverns of Chicago as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |
| [T-1262](../tickets/T-1262-publish-new-in-chicago-as-a-five-minute-jaunt.md) | Publish New in Chicago as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |
| [T-1263](../tickets/T-1263-publish-shopping-south-water-street-as-a-five-mi.md) | Publish Shopping South Water Street as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |
| [T-1264](../tickets/T-1264-publish-across-wolf-point-as-a-five-minute-jaunt.md) | Publish Across Wolf Point as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |
| [T-1265](../tickets/T-1265-publish-fort-dearborn-errand-as-a-five-minute-ja.md) | Publish Fort Dearborn Errand as a five-minute jaunt | T-1259, T-1256, T-1257, T-1258 |

## 5I. Everyday Jaunts — Nineteen Additional Outings In Five Bounded Content Batches (5 tickets)

| Ticket | Bounded delivery | Prerequisites |
|---|---|---|
| [T-1266](../tickets/T-1266-publish-news-mail-lodging-and-work-jaunts.md) | Publish news, mail, lodging and work jaunts | T-1259, T-1256, T-1257, T-1258 |
| [T-1267](../tickets/T-1267-publish-land-freight-household-supplies-and-clot.md) | Publish land, freight, household supplies and clothing jaunts | T-1259, T-1256, T-1257, T-1258 |
| [T-1268](../tickets/T-1268-publish-harness-candles-building-materials-and-l.md) | Publish harness, candles, building materials and leather jaunts | T-1259, T-1256, T-1257, T-1258 |
| [T-1269](../tickets/T-1269-publish-schooling-social-visits-and-careful-news.md) | Publish schooling, social visits and careful news reading jaunts | T-1259, T-1256, T-1257, T-1258 |
| [T-1270](../tickets/T-1270-publish-harbor-prairie-arrival-and-a-quiet-strol.md) | Publish harbor, prairie arrival and a quiet stroll jaunts | T-1259, T-1256, T-1257, T-1258 |

## 5J. Arrival And Jaunts Complete — Content Convergence And Published Mobile Acceptance (2 tickets)

| Ticket | Bounded delivery | Prerequisites |
|---|---|---|
| [T-1271](../tickets/T-1271-reconcile-and-time-the-complete-25-jaunt-library.md) | Reconcile and time the complete 25-jaunt library | T-1260, T-1261, T-1262, T-1263, T-1264, T-1265, T-1266, T-1267, T-1268, T-1269, T-1270 |
| [T-1272](../tickets/T-1272-verify-arrival-jaunts-and-source-browsing-on-the.md) | Verify arrival, jaunts and source browsing on the published mobile app | T-1271, T-1275, T-1276, T-1278, T-1259 |

## Requirements accounted for

| Owner requirement | Tickets / proof |
|---|---|
| Measured stages, responsive long work, year rollback tied to readiness | T-1246, T-1247 |
| Varied source cards/facts, roughly 100–250 statuses, rare humor, no forced wait | T-1275 |
| Warm summer 1835 welcome and Tap to enter, mobile controls | T-1278, T-1272 |
| One shared Go to / Explore Myself picker, safe start, no jaunt state | T-1277, T-1278, T-1259 |
| City totals moved out of welcome; full searchable source/usage library | T-1248, T-1276 |
| Data-driven JSON, provenance, more than 50 through content | T-1253, T-1259, T-1271 |
| Persistent Previous / Next / End / Menu and immediate End-to-menu | T-1279, T-1272 |
| Mode choice before and during play; real ETA; skip boring travel | T-1280 |
| Optional mechanics, conditions, endings, no forced game on every outing | T-1256, T-1271 |
| Deep cards and optional transit history without extending the main path | T-1257 |
| Era-themed keepsakes, five families and cross-category progression | T-1258, T-1271 |
| Six named priority jaunts and nineteen varied everyday jaunts | T-1260, T-1261, T-1262, T-1263, T-1264, T-1265, T-1266, T-1267, T-1268, T-1269, T-1270 |
| About five minutes, normally 4–8 stops, measured paths | T-1271 |
| Published mobile/desktop, fast/slow/failure/reduced-motion cases and budgets | T-1272 |

## Planning validation and implementation handoff

The proposed routes were checked against the compiled scene and authored anchors,
not merely against files existing in `data/structures/`. These are **content briefs**,
not a claim that every suggested transaction or present-tense role is documented.
Each content ticket verifies the relevant claim and locator when it is authored.
Known traps are called out in the briefs: the future courthouse is excluded, the Lake
House is construction, Hogan's mail role is historical, and fort service functions
and access must not be silently strengthened.

No new geometry or human figures are required by this plan. Missing source precision
can be bounded and labeled reconstructed; restricted depiction/rights constraints
still apply. Code checks on this planning change do not validate a future runtime.
The published integration ticket is responsible for that evidence after implementation.
