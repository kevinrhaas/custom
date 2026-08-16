# STATUS

## Measured 2026-08-16 — the rights rule could only ever fire on a violation somebody had already written down, and 49 geometry-bearing attributes are built from sources nobody has checked

**K41**, and it moves no record. AGENTS.md rule 6 and `docs/PROVENANCE.md` say a
`check_required` source *"may be cited in text but must not have assets derived from it"*, and
PROVENANCE.md said **"the validator enforces this."** The enforcement compares two fields of
the **same source record** — `rights_status` against the source's own `asset_use` label — so it
fires only when an author has recorded the violation. **The pair has never existed here: 38 of
64 sources have unresolved rights and every one declares `cross_check` or `text_only`**, while
the three that declare `geometry` are a survey and two maps, all clear. The labels are honest;
the rule is about a derivation and the mechanism is about a declaration.

**Asked of the town instead**, using the read-sets the generators already declare
(`CONSUMED` in each `*_params.py`, the same definition `check_geometry_declarations` uses, plus
the footprint polygon `from_phase` reads): **49 geometry-bearing attributes on 21 records cite
an unresolved source** — 43 on buildings, 6 on the terrain spec — and **19 of the 20 buildings
have a baked master in the tree**. **35 of the 49 stand on unresolved support alone** and **16
of those are graded `attested`**: the Sauganash Hotel's storeys and construction, the Wolf
Point Tavern's frame addition and painted sign, the Green Tree Tavern's footprint, roof and
paint, St Mary's Church's footprint, the Western Hotel, Miller House, and the west and south
division levels on the ground.

**What this parcel refuses to decide.** Whether a dimension read out of a copyrighted page is
an "asset derived from it" is a rights reading, and this project's own documents disagree —
`docs/PLAN.md` reads it narrowly (images, *"before any derivative texture"*), AGENTS.md and
PROVENANCE.md broadly. The two readings give opposite answers for all 49, so the gate holds the
population where it is and the reading goes to the owner; three routes are written up in
ROADMAP K41.

**What shipped:** `tools/measure_rights_derivation.py` and its 49-entry bank, four assertions
(the old label test kept, plus new-fault, no-ghost and no-worsening on the bank), all five
failure modes exercised by `--self-test` in `tools/check.sh`. **The residual is named and
counted on every run:** `data/flora` carries **202** citations of an unresolved source and
`data/fauna` **30**, both rendered, neither with a declared read-set — K42.

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute per-command
ceiling). `tools/check.sh` and the mobile half of `--published` are green. **No record, asset,
parameter or renderer file changed.**

## Measured 2026-08-16 — it is 189, not 195; this runner reproduces the nightly's bytes on every one of them; and the rewrite is not scheduled, it is open

**K40**, and it moves no asset. K39 could not verify its own record the obvious way — by
regenerating a derivative and comparing bytes — because `tools/web_derivatives.sh` did not
produce the bytes on the site. It reported a **lower bound of 195** from a vertex signature
and named the exact count, the price and the decision as this parcel. All four questions are
answered from a control that runs the step itself over all 334 masters, chunked into four
3 min 21 s passes to fit the harness's ten-minute per-command ceiling. That loop is now
`tools/measure_web_reproduction.py` rather than something every parcel reinvents, and it
refuses to write into `assets/` under any flag.

**The exact count: 142 of 334 reproduce.** The 192 failures decompose with nothing left over
— **189 come back byte-for-byte under `BAKE_PALETTE=1`** (the palette-era set) and **three
were already owned by name**: K37's two placeholders that compress smaller, and
`terrain__e1834_harbor_cut.glb` at 14 bits against a 16-bit ask, which is R-W6(b).

**And the sentence the no-Blender strategy rests on is true after all.** Bake PR **#175**
(07:34 UTC) rewrites **280** derivatives and holds all 192; on the 189 the nightly's bytes
and this runner's are **md5-identical, 189 of 189**. The bake's 280 decompose exactly — 189
palette-era + 90 placeholder masters upgraded to canonical archetype bakes + 1 terrain at
16 bits — so a binary diff nobody could review now has an arithmetic. What was wrong was
never the extraction: **K36(b) carried a step change through 38 files and not 334.**

**K39's vertex signature is refuted as an identifier**, in both directions: 189 shared, **six
welded files today's step reproduces exactly** (`optimize` dedups without the palette pass)
and three failures with no weld. 195 is a number to stop quoting, and no gate is built on it.

**The price**, for the record: +48,836 bytes over the 189 (mean +258, all 189 grow), +48,328
net across the tree — **0.18 % of the 25 MB budget**. K39's sample said +197 and 30 %
reproduction; the truth is +258 and 42.5 %.

**Two decisions.** *Who moves the 189*: nobody here — an open PR already holds those exact
bytes, and this parcel neither regenerates them nor merges that PR. **#175 and #164 carry no
status checks at all** because a bot-opened PR does not trigger the dev gate; running it
against them is the janitor's job and the owner's call. *Should the record name the STEP*:
**no.** A flag string is prose and can be edited to turn a gate green; a script hash would
have invalidated all 334 entries on each of the four commits that have changed the step,
**twice on a commit that moved no byte** (38, 3, 0, 0). What the failure needed was a rule,
and it is in the step's header: **a change that moves any derivative's bytes regenerates all
334, not the ones that visibly broke.**

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green. **No
asset, record, parameter or renderer file changed.**

## Fixed 2026-08-16 — the shipped model now records the model it was made from; and 195 of them were made by a step this repository no longer has

**K39.** K38's residual was that staleness was still a **timestamp**: `tools/publish.sh`
compared mtimes, and on a fresh clone `git checkout`'s write order makes **334 of 334**
masters older than their derivatives, so the scan was silent on exactly the tree a run
starts from. A master rebuilt with the same geometry and different `_CONFIDENCE` values —
the case the script's own comment was written about — passed that scan and all eight
content assertions alike.

**What moved.** `tools/web_derivatives.sh` records `name → sha256(master)` as it produces
each derivative, into **`assets/manifest.web.json`**, beside `assets/manifest.json`: the
manifest records data → master and is written by the Blender build, this records master →
derivative and is written by the step after it. **Assertion 9** compares the recorded hash
to the master in the tree, absolute in both directions — a moved master fails, an
unrecorded derivative fails, an entry with no file fails. Exercised on the real tree, not
only in memory: one byte appended to a master makes the gate fail by name and
`tools/publish.sh` refuse before writing anything. `publish.sh` no longer scans mtimes at
all; it runs the gate. **There is deliberately no flag anywhere that rewrites the record
without regenerating the bytes** — the remedy is always `--only <name>`.

**The coupling was the real question and it is decided: the STEP writes it, every run, and
a bake carries the diff.** The record's lifecycle is the derivative's — same producer, same
run, same commit — so a nightly rewrites it in the same breath and cannot leave the dev
gate red for everyone else. It is deliberately **not** in
`tools/web_derivative_baseline.json`, which is a record of faults a person banks by hand.

**AND THE CONTROL THAT WAS SUPPOSED TO VERIFY IT DOES NOT EXIST.**
`tools/web_derivatives.sh` says it *"reproduces 331 of 334"*. Measured: **6 of 20** in a
spread sample, and **all 14 that failed come back byte-for-byte under `BAKE_PALETTE=1`**.
`optimize`'s palette pass was **welding**, K36(b) turned the pass off for draw-call reasons
that stand, and it regenerated only the 38 assets whose material identity had broken. By
vertex signature — no `npx` needed — **195 of the 241 compressed derivatives carry fewer
vertices than their masters**, 10,513 vertices in total, and that is a lower bound.

**Nothing on the site is wrong**: a weld is lossless, triangles are equal, and assertions
1–9 are green on all 195. What is false is the claim that this runner can regenerate what
the nightly ships — true for 46 of 241 — and the consequence is scheduled: **the next bake
rewrites all 195 as unwelded files**, a 195-file binary diff with no number attached to it.
**K40** owns the count, the price and the decision, and the further question K39 declined:
whether the record should name the STEP as well as the master.

**Stated, not tidied:** the record was **seeded** in this commit, not produced by a full
run, because a full run would move those 195 files. One entry was written by the step (its
derivative came back md5-identical); the other 333 rest on assertions 1–8 and on the 93
passthroughs' byte identity with their masters. It does not claim the shipped bytes came
from today's step.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's
10-minute per-command ceiling). `tools/check.sh` and the mobile half of `--published` are
green. No committed asset changed a byte.

## Fixed 2026-08-16 — a publish step could put 1.2 MB of uncompressed models into the payload and the whole gate said CHECK PASS

**K38.** K37 noticed a third writer of `assets/web/` and declined to chase it:
`tools/publish.sh` copied any master through whenever it was newer by mtime. Chased, it is
worse than the note.

**It is reachable in one command, and nothing sees it.** Two compressed masters `touch`ed —
the state the tree reaches whenever `generators/build.py` is run on its own, which is the
case the script's own comment says the copy exists for — then `tools/publish.sh`:
`fort_dearborn_palisade` **114,768 → 841,836 bytes** and `dearborn_street_drawbridge`
**71,504 → 557,196**. **+1,212,760 bytes** into the payload, written into the *tracked*
source tree and mirrored to `site/`. On that tree the derivative gate exited 0,
`check_published.mjs` exited 0, and the full `tools/check.sh` printed **CHECK PASS**.

**And it could not have been otherwise.** A master copied over its own derivative has that
master's triangles, node identity, contract attributes, bounding box (zero rungs) and
material table, and a byte count that is equal rather than larger. K36(a)'s eight assertions
watch the *transformation* `assets/gltf/ → assets/web/`; they cannot see a file that skipped
it. **A gate written against a transformation is not a gate on its output directory.**

**It is not three writers — it is three scripts and four passthrough branches**, three of
them silent: the size rule K37 decided (93 assets), `optimize`'s failure fallback,
`gltf-transform`-unavailable copying **all 334** (payload 4.54 → 20.96 MB, 4.6× against a
25 MB budget), and `publish.sh`'s mtime copy. **And mtime never compared a byte:** on a fresh
clone **334 of 334 masters are older than their derivatives**, by `git checkout`'s index
order, so the rule fires on any rebuild and is blind on the tree a run starts from.

**What moved:** no asset, no record. **Assertion 8**, absolute in both directions against the
93 passthroughs banked by name — a 94th fails whichever writer made it, and a banked one that
returns compressed fails and says to re-bank. Both `--self-test` mutations fire.
**`tools/publish.sh` is no longer a writer of `assets/web/`**: it keeps the scan, moves it
above the first write and refuses, naming each file and the `tools/web_derivatives.sh --only`
that repairs it. Verified end to end — the same two `touch`es now stop it at exit 1 with the
working tree clean.

**Stated, not tidied:** a new placeholder now needs `--write-baseline` in the commit that adds
it, because "the generator added one" and "something copied a master through" are the same
bytes and one of them is a decision. And refusing on mtime is still mtime — a master rebuilt
with the same geometry and different `_CONFIDENCE` values passes both the scan and assertions
2–7. **K39** is that residual: the step knows which master it compressed and writes it down
nowhere.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's
10-minute per-command ceiling). `tools/check.sh` and the mobile half of `--published` are
green. No committed asset changed a byte in this parcel.

## Fixed 2026-08-16 — the ninety unsqueezed files were right, and three squeezed ones were shipping bigger than the models they came from

**K37.** K36(a) reported 90 derivatives as byte-identical master copies and K36(b)'s control
found that the pipeline's own step does not reproduce them. Run over all 90, the step takes them
**520,700 → 628,028 bytes, +107,328 (+20.6 %)**, with **88 of the 90 growing**: `meshopt` writes
a compression header, a buffer-view table and an index buffer, and on a 16–60-triangle shed those
cost more than the compression saves. **The passthrough was the right answer; it was just nobody's
decision** — it fell out of `generators/inferred_placeholder.py` writing the same bytes into both
trees.

**And the class predicate is wrong in both directions.** `kind: placeholder` maps onto
"uncompressed" 90 of 90 today, and that is a coincidence of write order. Three assets that have
been through this step on every bake since it was written ship **larger** than their masters —
`fort_dearborn_root_house` +324, `lake_house_construction` +240, `fort_dearborn_magazine` +224 —
while `fort_dearborn_parade`, 5,504 bytes and 30 triangles, compresses −24.5 %, and two of the
ninety placeholders compress −9.3 %. Byte size does not predict the sign either. So the rule is
**keep whichever file is smaller, measured per asset**, and it lives in
`tools/web_derivatives.sh` rather than in a list of names.

**What moved:** three derivatives, replaced by their masters — **−788 bytes**, and they now carry
exact float positions rather than a quantised lattice. The 90 are untouched. **The gate:**
`measure_web_derivatives.py` assertion 6, absolute, **bound zero**, with a `--self-test` that
grows a derivative by one byte and confirms it fires *and* grows an epoch mesh by one byte and
confirms it does not.

**The one exclusion, by name:** `water__e1834_harbor_cut.glb` is +744 bytes (+55.0 %) under the
rule and is **not** passed through. The epoch meshes' bit depth is a geometric decision (R-W6),
the ground and waterline are what R-BUG3c, R-BUG4 and R-M1a measure against, and **R-W6(b) holds
both files** pending the owner's word on regenerating geometry outside a bake.

**Left open, stated:** the two placeholders that compress smaller stay master copies —
`inferred_placeholder.py` rewrites every placeholder into both trees on each run and would undo
them. **1,624 bytes.** And `tools/publish.sh` is a **third** writer of `assets/web/`: it copies a
master through whenever it is newer by mtime, which is a passthrough nothing decided and which
this gate cannot see. Worth a parcel.

**The gate's own self-test had been red since K36(b)** — rebanking the material ratchet empty
left one mutation with nothing to mutate, and it printed MISSED, so `--self-test` reported
SELF-TEST FAIL on a clean tree. Nothing noticed because `check.sh` ran `--gate` and never
`--self-test`. An inapplicable mutation now prints `skipped`, and `check.sh` runs the self-test
as its own step.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green. Nothing
here moves a vertex, a material or a pose.

## Fixed 2026-08-16 — the compression flag that hid 38 buildings' material names was also spending the town's draw-call budget, and half the anchors were over it

**K36(b).** K36(a) recorded the palette pass as a fault about NAMES: `gltf-transform optimize`
folds the named materials of any file carrying five or more of them into one `PaletteMaterial`
plus generated PNGs, so 38 shipped assets lost `log`, `chinking`, `board`, `roof`, `dark`,
`interior` on the way to the browser. The pass's own justification is that merging materials
saves draw calls, so the reading was that names had been traded for speed. **Neither was true.
It cost both.**

**FINDING 1 — a generated map makes an asset unbatchable.** `materialKey()` in
`renderers/web/js/buildings.js` includes `m.map?.uuid`, and a GLTFLoader mints a fresh uuid per
loaded texture, so a palette asset cannot join any batch — not the town's, and not another
palette asset's. The 38 shipped as **40 single-building batches** (40, not 38: `sauganash_hotel`
came out with three `PaletteMaterial`s, its glass and shutters refusing the merge) on top of the
town's 16. **The published town drew 56 batches. R-W5a's committed figure is 16.** With the pass
off: 56 → 16, textures in memory 55 → 41, shader programs 15 → 12.

**FINDING 2 — R-W5a's numbers were taken on the source tree.** Its *"no map of any kind"* was
true of what this repository bakes and never true of what the site serves — the identical error
K36(a) found in R-W2a's material sheet, from a different parcel, three days apart. R-W5a's
result stands (47 → 16 is real, and is what the 40 now fold back into); its "16 batches" was
never a statement about the site. `tools/measure_shipped_batches.mjs` reads the **mirror** by
default and prints which tree it read, so there is no third time to have.

**FINDING 3 — four of the eight scene anchors were over the 80-call budget on the site.** A
batch holding one building is culled with that building, so this is paid per pose and is worst
where the town is densest. At 1280×800, through the renderer's own `goTo`:

| | green_tree | forks | from_above | south_water | lake_market | s'nash_wing | f_post_office | sauganash |
|---|---|---|---|---|---|---|---|---|
| before | **102** | **96** | **84** | **82** | 71 | 68 | 66 | 62 |
| after | 70 | 68 | 63 | 69 | 63 | 61 | 60 | 59 |

Nothing had measured it: the smoke reads the counter at whatever pose it is standing in, and
`critic_shots.mjs` reports draw calls per station without asserting on them.

**The cost is 187,392 bytes** — the 38 go 318,540 → 505,932 (+58.8 %), because 197 named
materials take more room than 75 generated PNGs. That is +4.1 % on a 4.5 MB tree against a
25 MB budget. `material identity: 334 of 334`, and K36(a)'s ratchet is rebanked empty.

**`tools/web_derivatives.sh` is the structural half.** The web-derivative step is lifted out of
`tools/bake.sh` whole, so a Blender-free runner can regenerate derivatives from the committed
masters and measure them — link 2 could be *found* broken by K36(a) and not *repaired* without a
nightly. The control that makes this attributable: under `BAKE_PALETTE=1` it reproduces **243 of
334 derivatives byte-for-byte**, including all 38.

**The other 91 are two findings this parcel did not fix and did not hide.** **K37** — 90
derivatives are byte-identical master copies, and the pipeline's own step does not reproduce
them: it makes them ~21 % *bigger* (4,968 → 6,000 on the sample). Nothing states which
behaviour is intended. **(K37 is DONE 2026-08-16 — the passthrough is correct, measured over all
90 at +20.6 %, and the sample generalised; see the section above.)** **R-W6(b)** — the shipped
terrain is still **14-bit**: regenerating the
committed master at 14 bits reproduces `assets/web/terrain__e1834_harbor_cut.glb` md5 for md5,
and the 1,116-byte gap to the 16-bit file is exactly R-W6's own quoted cost. **R-W6's fix is in
the script and not in the file a visitor downloads**, so the ground is still on the 306 mm
lattice R-BUG3c found buries the road. Both are open parcels in `docs/ROADMAP.md`.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green, and the
desktop draw-call numbers above are measured at 1280×800 by the new tool.

## New 2026-08-16 — the town on the site has 75 textures, and the repository has none

**K36(a).** The geometry a visitor downloads reaches them along four links —
`data/` → `assets/gltf/` (the masters) → `assets/web/` (the shipped derivatives) →
`site/chicago/4d/` (the published mirror). Link 1 is gated by the staleness check, link 3 by
`check_published.mjs`, and **link 2 was gated by nothing at all**: no hash, no count, no
assertion tied a shipped derivative to the master it was compressed from. It is also the link
with the moving parts — two `gltf-transform` passes — and `tools/bake.sh`'s own comments record
what has already come out of them: *"a bug that collapsed every building to a two-metre box
shipped past a fully green gate — twice"*, and a `--texture-compress ktx2` flag that *"silently
turned every derivative into an uncompressed copy of its master, in every environment, since
this step was written"*. Both were found by a person reading the script.

**FINDING 1 — the shipped town is textured and the baked town is not.** `optimize`'s palette
pass folds the named materials of **38 of the 334 assets** into a single `PaletteMaterial001`
carrying generated PNGs: **75 textures exist on the site that exist in no master**, and the
names they replace — `log`, `chinking`, `board`, `roof`, `dark`, `interior` — are gone from the
file a browser loads. Among them the Sauganash Hotel, the Wolf Point Tavern and its stable, the
log jail, the estray pen, Cobweb Castle, the council house and eleven `recon_*` reconstructions.

**The split is a COUNT, and it is exact.** Every asset whose master carries **five or six**
materials is faulted — 31 of them `log_dwelling`, 6 `outbuilding`, 1 `frame_tavern` — and every
asset carrying **four or fewer** is clean, all 296 of them, with no exception in either
direction. That is the palette pass's own threshold rather than anything about logs (the tool
names its output `PaletteMaterial001` and its documented minimum is five materials). So **the
fault grows with the town on a boundary 275 assets are sitting exactly one material short of**:
an archetype that gains a fifth surface — which is precisely what R-W2b is for — moves every
asset it paints across the line. The ratchet is what makes that arrival loud.

**FINDING 2 — R-W2a's material sheet is a sheet of the masters, and it says so in the wrong
words.** `docs/RESEARCH/materials.md` opens by reasoning that *"the source and the shipped bytes
have disagreed in this project before … a sheet that inventories intentions is worth nothing to
a bake"*, and then measures `assets/gltf/**/*.glb` under the heading *"the surface census,
measured from the shipped GLBs"*. Those are the masters. Its **"nothing in the town carries a
texture of any kind"** is true of what this repository bakes and false of what the site serves,
and **R-W2b — the next pick in that lane — plans to wire an atlas onto the material names that
the publish path deletes on 38 assets.** The sheet is corrected in place; none of its five
findings moves.

**FINDING 3 — 90 assets ship uncompressed and nothing says so.** They are exactly the 90
pure-Python placeholder GLBs, which `generators/inferred_placeholder.py` writes byte-identically
into both trees; the 244 Blender-baked assets compress 5.29×. It is 508 KB, 11.4 % of the
payload, and not a problem today — the point is that the bake reports a fallback copy as a
warning line in a log nobody reads, and the only committed instrument that could notice is a
25 MB total-size budget the tree is nowhere near.

**WHAT DOES NOT MOVE, MEASURED.** Triangle counts are identical on all 334 pairs, so
`--simplify false` has held; node names, `structure_id`/`phase_id` extras and mesh names all
survive; `_CONFIDENCE` — how a visitor is told which parts we made up — reaches the site on
every asset that carries it. The world bounding box agrees to at worst **2.63 rungs** of an
asset's own extent (0.107 mm on a 2.7 m shed), and the terrain's 82.8 mm is **1.08 rungs** of
its 5,020 m box, consistent with the 76.6 mm lattice R-W6 committed. **Corrected 2026-08-16 by
K36(b): a "rung" there is `extent / 65535` by the gate's own definition, not the file's actual
lattice, and the shipped terrain is 14-bit — so 82.8 mm is consistent with a 306 mm lattice too,
and that is the one a visitor is standing on. See R-W6(b).**

**The gate is `tools/measure_web_derivatives.py --gate`, in `check.sh`, at 0.2 s and with no
decoder** — every claim above is answerable from the glTF JSON chunk. Five absolute assertions
(bijection, triangles, identity, contract attributes, bounding box) and one ratchet
(`tools/web_derivative_baseline.json`, the 38). All eight failure modes were broken deliberately
in `--self-test` and each fires. **The repair is K36(b)** — it regenerates 334 binary files, so
it is a separate parcel and it does not need Blender. **DONE 2026-08-16, and it turned out to be
about draw calls rather than names — see the top of this file.**

## New 2026-08-16 — the constraint this project puts above the work was kept by the buildings and not by the people

**K34.** AGENTS.md's standing constraint is the one sentence in this repository that outranks
the rest of it: the final removal of the Potawatomi from Chicago is **August 1835**, inside the
first target year, and it is *"not a research gap to be filled by inference"*. It is given
exactly one mechanism — **`review_required: true` on any record blocks a scene from being marked
`released`** — and nothing had ever measured what that sentence covers.

| layer | carries the flag | did it block a release? |
|---|---|---|
| `data/structures/` | **9** of 332 | yes |
| `data/residents/` households | **7** of 173 | **no** |
| `data/residents/` persons | 0 of 209 | **no — the layer was never read** |

**FINDING 1, AND IT IS ONE RECORD.** `hh_caldwell_billy` — Billy Caldwell, Sauganash, the
agency's interpreter and the namesake of the town's best-known tavern — carries this sentence
in its `research_note`, in the same words `hh_robinson_alexander` uses: *"It carries
review_required so that no scene containing it can be marked released before the consultation
the project has committed to."* **The field was `false`, and `git log -S` finds no commit in
which it was ever anything else.** The record has been promising the flag since it was written.
`touches_removal ⇒ review_required` — the one rule the validator did hold on this layer — could
not see it, because `touches_removal` was `false` too.

Both are `true` now, **on the record's own committed text and on nothing new**: the same note
already quotes Andreas putting this man at the head of the march to the Missouri. Nothing else
about the record moved, and the note now says the flags were false and that the paragraph above
them said otherwise.

**FINDING 2 — the seven households were safe by coincidence.** `validate.py`'s scene gate built
its blocked list out of `data/structures/` alone, while the error it prints on the *household*
side says any record touching the removal *"blocks a scene from being marked released"*. That
consequence did not follow. The households were covered anyway because **all 11 of their
`lives_at`/`works_at` links land on a structure that is flagged too** — a fact nothing required,
nothing measured, and nothing would have noticed the loss of. A flagged household with a null
`lives_at` and an unflagged workplace passed clean; that scene is now a committed self-test.

**FINDING 3 — the same sentence, read the other way, is a deliberate NO and not a defect.**
`chappel_infant_school`, `walker_meeting_house` and `watkins_school_house` each say
*"review_required is set false … but the call is worth a second opinion"*, and each is false.
So the gate tests **both directions** rather than "prose mentions the removal ⇒ set the flag".
A gate that could not tell finding 1 from finding 3 would have been an instrument arguing for
its own conclusion. What it leaves open is **K35**: three of the nine flagged structures state
no reason anywhere, and the building side has no field a reason could live in.

**FOUR ABSOLUTE ASSERTIONS AND NO RATCHET**, deliberately — a ratchet is the right instrument
for a fault being paid down, and this is a commitment. Prose matches field; `touches_removal`
implies `review_required` at household AND person level; the flag reaches the building
(11 of 11); and — behavioural, against the real dataset — a scene with `released` forced true
is refused for **exactly** the union of flagged ids across every layer, so a gate that restated
the rule cannot pass while the validator disagrees with it. `tools/review_constraint_baseline.json`
makes the asymmetry explicit: **adding a flag is free, clearing one fails** and names what
clearing it would mean.

**The gate was verified to fail, on four separate injections** — the Caldwell flag cleared
again, `cobweb_castle` unflagged under three households, a person given `touches_removal`
without `review_required`, and the validator reverted to structures-only. Each exits 1 with the
divergence named, and the restored tree passes.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs`
green against the published mirror. **The desktop half was NOT run and is not claimed as
passed** — it needs ~13 minutes against this harness's 10-minute per-command ceiling, which the
ROADMAP's run-budget box records. This parcel changes no renderer file, no geometry and no
coordinate.

**What it did NOT do:** it moved no building, household or coordinate, invented nothing and
regraded nothing. No liberty is owed — `docs/LIBERTIES.md` records inventions, and there is no
invention here. It did not decide whether the three unexplained structure flags need a reason
field; that is K35 and it is an owner's choice, not a gate's.

## New 2026-08-16 — there is a bridge in this scene over a watercourse the scene does not contain

**T-E5(a).** The terrain spec defers four in-town water features under one shared phrase —
*"existence documented, geometry conjectural"*. Existence is a claim about a **place**; a scene is
a **date**. Nobody had asked the second question of any of the four, and they do not answer it
alike.

| dossier zone | feature | at 1835-07-01 | what dates it |
|---|---|---|---|
| 14 | The slough | **present** (inferred) | a structure this project already stands in the scene |
| 15 | **The public-square pond** | **not established** (inferred) | nothing — and one document argues both ways |
| 16 | The Frog Pond, Lake & LaSalle | present (inferred) | a newspaper, one year late to the day |
| 17 | The Wells Street marsh | present (inferred) | the sentence that gives the slough gives what it drains |

**THE SHARPEST FINDING IS NOT THE POND.** `slough_log_bridge` — *The Slough Log Bridge, Water
Street* — is a committed structure standing on 1835-07-01, and its own `documented_range` note
quotes the source running that crossing *"until after 1840"*. Zone 14, the slough it crosses, is
deferred and undrawn. **A visitor walks onto a timber crossing laid over open prairie**, and has
been able to since the bridge landed. That is not an argument for cutting a conjectural channel —
the depth and width are still unsourced and parcel (c) still owns them. It is the proof that the
four were never on one footing, which one shared phrase implied they were.

**On the pond the answer is `not_established`, and deliberately NOT "it was not there".** One
document, `chicagology_prefire273`, carries both sides, and nobody had noticed that it does.
**FOR:** its slough sentence has the stream draining *"the pond and the marsh extending up Wells
Street"* as a live feature of a drainage system whose bridge outlives the scene by five years.
**AGAINST**, and the deferral weighed none of these three:

1. **The quotation dates nothing** — *"was then a pond"*, a past tense against an **1857** present,
   in a document this project's own source record identifies as built on **Hubbard's Chicago as he
   found it in 1818** and **Davis's 1832** drawing.
2. **The dossier's own row says the wrong season** — row 15 reads *"seasonal … water 0.5–2 ft deep
   **in spring**"*, and the scene date is **1 July**. The row stated a season; the deferral read a
   scene.
3. **Two county buildings already stand on that block, before the scene date** — the **estray
   pen**, Chicago's first public building, on the south-west corner from **March 1832**, and the
   **log jail** on the north-west corner from the **fall of 1833**. A pound is not built in a pond.

**The buildings do not refute a pond — they BOUND one, and that is the whole result.** A
whole-block pond is refused by this project's own committed records; a partial one is untouched by
them and is exactly the deliverable T-E5's third question asked for, which no source reached can
supply. So the date and the extent are **one question** and neither is settled. `existence
documented, geometry conjectural` was true of a place and was being read as though it were true of
the scene, and the geometry it called conjectural is not a detail to fill in later — it decides
whether water stands under Chicago's first public building.

**T-E5's fallback is discharged and NO LIBERTY IS OWED.** Its instruction was to write a
`docs/LIBERTIES.md` entry saying the square is drawn dry if it could not be settled honestly.
Nothing was invented, no confidence moved, and the square was **already** drawn dry and already
recorded as such in text a visitor reads. What was missing was the reason, and the reason is now in
that same visitor-facing text — the four `why` strings `ground.js` renders. Prose in the spec is
stripped from the terrain's staleness hash, so it cost no bake.

**AND IT COST SOMETHING DOWNSTREAM NOBODY WOULD HAVE GONE LOOKING FOR.**
`data/fauna/zones/f04_marsh.json` rested **three claims** on the pond quotation as in-scene
evidence — muskrat `presence` and mallard `presence` were `attested` on **that quotation alone**,
the muskrat's note reading *"direct evidence of animals present in numbers at a named location
inside the scene box"*. It is not: it is evidence about a place at an unknown time. **No grade
moved**, and that is measured rather than convenient — what carries `attested` is Andreas's *"ducks
and muskrats in the marshes"*, and the marshes he names **are** the habitat this zone plants
(`z04_marsh`'s extent is a buffer of the mapped water, the river-shore strip, and has never reached
the square). The animal is attested in the habitat the scene draws and is no longer attested at a
named block the scene draws dry; the notes now say which of the two they mean.

**The gate was verified to fail, on four separate injections.** An undated deferral, an `inferred`
grade with its reasoning blanked, a zone number nothing defers, and a source that does not resolve
— each exits 1 with the divergence named, and the restored file passes. It holds the correspondence
in **both** directions, so a fifth in-town water feature cannot be deferred undated and a dating
entry cannot outlive the deferral it grades. Which zones it covers is **declared**, not sniffed
out of the prose `why`: a regex over prose reads like a rule until a name changes under it, which
is what R-W4a was and what the smoke's own `/terrain|water/i` filter was.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs` green
against the published mirror. **The desktop half was NOT run and this is not claimed as passed** —
it needs ~13 minutes against this harness's 10-minute per-command ceiling, which the ROADMAP's run
budget section records. This parcel changes no renderer file, no geometry and no coordinate; what
it changes that a browser loads at all is four `why` strings in a sidecar and one changelog entry.

**What it did NOT do:** it modelled, moved and sized nothing — all four features remain deferred.
It edited no research dossier (those are committed verbatim, which is why the disagreement lives in
`docs/RESEARCH/public_square_pond.md`). And it did not answer **how much** of the square was wet,
which is **T-E5(b)** and needs a bake.

## New 2026-08-16 — the adoption rule nine block parcels supplied by hand is code now, and it changes nothing

**K28 is done**, and the honest headline is that **not one household, roof or coordinate moved**.
Since T-A9 on 2026-08-15, nine block parcels have refused a trade a second roof and every one of
them wrote the refusal down as *a choice rather than a rule*, because method rule 6 was silent on
three things at once. All three are decided and two of them are now gates.

**The settlement is permissive on the table and strict on the rate**, deliberately — settling all
three conservatively would have been caution dressed as method:

- **(i) tests 2 and 3 read two PROJECTIONS of the housing table, not a set of pairs.** The
  stricter pair reading is **refused**, on rule 6's own standard rather than on taste: requiring
  the pair refuses the **fourteenth labouring household** (T-A4's D1 west of the river, argued in
  exactly the projected form), which rule 6 names as one of the **four decisions its third test
  recovers** — and the same paragraph says a test that has to be told the answers is a preference.
  What the projections admit is measured, not waved at: **20 (family, division) pairs across 8
  trades** that this layer houses none of.
- **(ii) there IS a cap — one adoption per trade per block parcel.** A block is an artefact of the
  drawing rather than a unit of the town, which is the reason for the cap and not an objection to
  it: without one, the granularity of the plat sets the rate at which this census grows. It is
  also what makes (i) safe — the projections widen *which* roofs are eligible, the cap bounds *how
  fast* any of them may move a count.
- **(iii) test 1 means the trade's OWN committed text, not method rule 3's list of unbounded
  trades.** Being unbounded says where a number came from; test 1 asks whether the number is too
  low. Only the **carpenters and labourers** state it, so the laundresses' D2 and the teamsters'
  D4 are refused — **with the remedy named**: argue the floor in that trade's own argument, from
  the town, and the roofs follow.

**Both gates were proven to bite before merge**, against mutated copies of the programme rather
than by inspection: a second carpenter on `blk_south_water_wells`'s D4 and a laundress on
`blk_randolph_franklin`'s D2 — the two roofs nine parcels refused by hand — each fail with the
clause named. The floor predicate is **imported** from `tools/measure_adoption_tests.py` into the
gate rather than restated, so the report and the gate cannot drift apart about what a floor is.
That tool also no longer tells its reader the question is open, which it did in four places.

**All 21 standing block adoptions already obeyed the cap**, which is why nothing moved. The value
is that the tenth block cannot drift.

**What was and was NOT run.** `./tools/check.sh` — the dev gate — is **green**.
`node tools/smoke_renderer.mjs` was run at **mobile (390x780) only**; the desktop half **was not
run**, because a single foreground command on this runner is capped at ten minutes and the desktop
half takes about thirteen (K21, measured). This parcel changes one authored JSON's `method` prose
and two tools: **no renderer file, no record, no geometry, no coordinate, no material**. Say so
rather than implying both halves ran.

## New 2026-08-16 — one new household renamed 73 of 113 invented residents, not the 17-25 eleven parcels reported

**K20 is done.** `tools/generate_inferred_names.py` dealt each `(community, sex)` pool round **by
index**, so an invented name was a function of how many people sorted ahead of you. Eleven parcels
measured the resulting churn in passing and reported 17-to-72; every one of them was a single
sample at a single arbitrary point in a hash order. `tools/measure_name_churn.py` is the
instrument — it inserts a synthetic household **in memory**, re-runs the allocator and counts who
gets renamed — and over **240 insertions across all six trades** the distribution is not centred
near a fifth of the layer: mean **40.4** for a carpenter, **worst 73 of 113**, and only **1 of 40**
carpenter probes renamed nobody.

**The allocator is now insertion-local: worst 10 of 113 on the same 240 probes, mean 4.6.** Each
person has their own deterministic ordering of the pool and claims the least-used name they are
permitted, so a name depends on who you collide with rather than on how many people precede you.
A third of the improvement comes from **unwelding the given name from the surname**: a repeated
given name is what a town looks like and claims nothing, so it is now each person's first
preference with no ledger at all, while a surname — which reads as kinship — keeps the ledger and
the floor rule.

**The residual is the POOL, and the report proves that rather than asserting it.** Each probe
prints its bucket's pressure. At **0.14x** (pool with room) an insertion renames **at most one**
person — literally K20's acceptance criterion. At **2.03x** (36 surnames dealt to 73 men) it
renames up to ten, because there is no spare name at the floor. **Ten renames at 2.03x is a pool
that is too small; ten at 0.14x would be an allocator that is still not local.** Widening the
pools is evidence work — more named 1835 Chicagoans out of Andreas and the rolls — not a tuning
knob, and at 3x pressure the residual will climb again.

**A bug the fix exposed:** unwelding the two halves let two people draw the same pair, and the
first run shipped **two Alvah Hastings**. That is refused outright now and all 113 full names are
distinct — true by accident before, true by assertion now.

**The one-time cost is the whole layer**: **113 of 113 renamed across 101 household files**,
recorded as **L111**. It invents nothing new — same pools, same grades, same `name_basis`
citations and notes; a different invented name is the same claim about the same nobody.

**What was and was NOT run, stated rather than implied.** `./tools/check.sh` — the dev gate — is
**green**, including the new step (`measure_name_churn.py --gate`, ~2 s) and `compile_scene.py
--all --check` over the 331 regenerated sidecars. `node tools/smoke_renderer.mjs` was run at
**mobile (390x780) only, 214 passed / 0 failed**; the desktop half **was not run**, because a
single foreground command on this runner is capped at ten minutes and the desktop half takes
about thirteen (K21, measured). Nothing visual changed here — the diff is name strings in
records and sidecars, no renderer file, no geometry, no material, no coordinate — so the risk the
desktop half covers is not the risk this parcel carries. Say so rather than implying both halves
ran.

## New 2026-08-16 — the town has no chimney material, and no record anywhere says what a roof is made of

**R-W2a**, the material sheet, is written: `docs/RESEARCH/materials.md`. It is measured out of
the shipped GLBs rather than read off the generators, because the source and the bytes have
disagreed here before. **334 assets carry 1,353 material slots, resolving to 32 names, 41 base
colours and 18 roughness values.** Every one is `metallicFactor 0`, `doubleSided`, `OPAQUE`,
and carries no map of any kind — §1 item 9's "zero textures anywhere" is confirmed at the byte
level, not quoted.

**Two findings block texturing outright, and neither is a rendering problem.**

- **The chimney is not a material in this project.** `frame_dwelling`, `frame_storefront` and
  `log_dwelling` all build their stacks with `M_ROOF`, so **219 chimney stacks on 199 buildings
  are painted with the roof's colour**, `0.34, 0.30, 0.27` at roughness 0.90. The 90 inferred
  placeholders, meanwhile, ship a real `placeholder_chimney_brick`. The town has a brick
  chimney material and the archetype buildings do not use it — and `log_dwelling`'s own
  docstring argues that a frontier stack is stick-and-clay or fieldstone, a different object
  from a framed house's brick stack, which renders identically to it. Opened as **R-W2c**, and
  it opens with a research question rather than a palette.
- **No record states a roof covering.** 315 records state a roof *type* and 309 a pitch;
  **zero** say what the roof is made of. The board roof `outbuilding` argues for is separated
  from a shingle field by **0.03 of roughness and nothing else** — identical colour, identical
  name, in the shipped bytes. The repository's one direct attestation, the North Side school's
  "sheeted and shingled roof", is read by nothing. Roofs cannot be textured until an attribute
  exists to select the covering, and that is a schema change across 315 records.

**And one documented fact is committed, correct, and rendered by nothing.** `cobweb_castle`
carries `cladding: clapboard_part_way_up`, **`attested`**, sourced to `andreas_1884_v1` —
David McKee's "the agency-house being afterward clapboarded part way up". It is a
`log_dwelling`, which does not read `cladding` at all, and the value is not even in
`CLADDINGS`. `cladding` is stated on 27 records and read on 22.

**R-G1's "there is no roughness variation anywhere" is corrected, and the correction changes
what W2 builds.** Between surfaces there are already 18 argued values spanning 0.15 to 1.00.
What does not exist is variation *within* a surface: every square metre of every wall has one
roughness, which is why nothing reads as painted, weathered or wet. **The deliverable is a
roughness map, not better constants** — do not spend a round re-tuning the 18 numbers.

**What was NOT run, stated rather than implied.** This parcel changed no code, no parameter
and no record, so `node tools/smoke_renderer.mjs` was **not** run at either viewport and
`tools/publish.sh` produced no mirror change beyond the changelog. `./tools/check.sh` passed
green, and it is the dev gate. Nothing here has been rendered, because there is nothing here
to render.

## New 2026-08-16 — a building has been taken out of the town, and the town's public buildings are three

**T-I3(a).** The programme schedules six civic or public-service roofs and every generator has
refused to mass one since L93, on the ground that the archetype behind the family speaks only
garrison words. The refusal is now the research instead. **On 1835-07-01 the town's public
buildings with a roof are three — `log_jail`, `council_house`, `chicago_lighthouse_1832` — and
this project already had all three.** `estray_pen` is public and roofless. The enumeration is
`docs/RESEARCH/civic_public_buildings_1835.md`, and every citation in it is Andreas: **no new
source was needed and none was invented.**

**The finding is the fourth building. The court-house was not built yet.** 332 structures resolved
into the 1835 scene and 331 do; `cook_county_courthouse_1835` is re-dated to the fall and resolves
into 1836 instead. Its record said, at length and honestly, that nothing it had reached fixed a
month, and reasoned from a flat prior over a twelve-month window that the building was about half
likely to be standing. **The window was never twelve months.** Andreas's town-period narrative:
*"During the fall of the year (1835,) a one-story and basement brick court-house was erected on
the northeast corner of the square, on Clark and Randolph streets"* (scan p. 369). His chronology
lists it under 1835 at **November** (scan p. 1317). And the county Recorder *"removed his office
toward the end of October to the new building recently erected by the county on the public
square"* (scan p. 305). Three statements — a narrative, an index and a biography — and not one is
earlier than the fall.

**The dataset had already said so, in another file, for four days.** The physical-roof reconciliation gives this record `roof_count: 0` with the reasoning *"Production chronology places construction in fall 1835; no courthouse roof should stand on 1 July"* — committed 2026-08-12, one day after the structure record that stood the building on the square. So from 12 August one document in this dataset held the court-house unbuilt while another drew it, and nothing read the two together; the walkthrough's own release notes even carried the reconciliation's reading out to visitors — *"a courthouse that was not built until the autumn"* — while the walkthrough drew it. **The one that was right is the one with no citation at all.** The reconciliation's "production chronology" cites nothing; the record cites Andreas and says the opposite, because what it cited was a caption.

**The citation the record had was a picture.** It cited *"a section headed 'THE FIRST
COURT-HOUSE.' at scan p. 373"*. Scan p. 373 is a PLATE; those words are an engraving's caption,
printed under *"Copyright secured by A. T. Andreas, 1884."* The paragraph that carries the date is
four scan pages earlier. This is the second time in this project a citation has resolved to a
heading rather than to a sentence, and it is the whole cause: every gate here asks whether a
building is inside its lot, clear of the roadway, on permitted ground and clear of its neighbours.
The gate that asks whether it existed yet is the date gate, and a range authored from a caption
passes it perfectly.

**Two of the record's own hedges are settled and both say it was better than it knew.** It warned
that Andreas's north-east siting "is the 1837 BUILDING" and might be contaminating an 1835 record
— Andreas gives that corner to this one, in the sentence that dates it. It ruled out brick because
"the first brick building in Chicago is 1837" — that is the first brick HOUSE, and Andreas calls
this court-house brick. **Neither is applied. Both need the bake**, because a changed form value
stales the mesh; they are recorded on the record as amendments.

**No anonymous roof may claim to be a public building, and that is now asserted.**
`tools/measure_institutional_claims.py` runs in `check.sh` against every committed record rather
than only the ones a generator is about to write — **absolute zero** for the worship and civic
families, because they are enumerable, and a **ratchet at one** for the schools, naming the single
anonymous North Division school L93 records rather than deletes. All three halves were broken
deliberately before the gate was trusted.

**What a slot would have been spent on is not a building.** The crosswalk says the family spans
*"jail/blockhouse; engine/service; adapted offices"*, and every adapted office in Chicago that
summer was a room in somebody's private premises. The United States Land Office was open from May
1835 and transacting Beaubien's pre-emption four weeks before the scene date — and it was rooms on
the east side of Lake Street, with Andreas noting that the Register and Receiver *"were usually at
their private offices"*. The post office was a counter in Hogan's store. The county's own officers
were private until late October. Three guards added to `data/exclusions.json`, and
`first_fire_engine_house` amended because it dated the ENGINE while the HOUSE is later still.

**What is NOT done, and it is the number.** Three of the six I3 slots are a count of nothing, and
the target still says six. The inventory's arithmetic is closed — family targets sum into
district-group rows, rows into district targets, districts into `roof_total: 665`, and
`reconcile_665.py` asserts all three — so the three cannot simply be removed. The two exits are
two different claims about the town (662 roofs, or three roofs that were not civic), the research
settles neither, and choosing one would invent exactly the kind of aggregate this parcel just
removed. **T-I3(b), blocked on the owner.** Also unmoved: `estray_pen`'s phase id still reads
`pen_1833` after its year was corrected to 1832, because a phase id is half of a baked asset's
filename.

## 2026-08-16 — the buildings in the streets are drawn wrong, not placed wrong, and the town's georeference is exonerated

**K30(b)**, the attributing half, and it moved nothing. K30(a) measured 29 buildings lapping
a platted corridor and left the deep cluster without a cause. The cause is now a command,
`tools/measure_corridor_intrusion.py --reflect`.

**The suspect this project named is refuted, by arithmetic.** South Water is georeferenced
through modern Wacker Drive, which was built on made ground, so a displaced centreline would
displace every record on that street alike. It does not: the 13 deep South Water anchors
stand **11.64–15.30 m** from the committed centreline against a platted half-width of
**12.192 m**. The corridor and the placements agree to about a metre, the disagreement has
**both signs**, and a displacement that explained a 4.51–8.17 m intrusion would have to be
4.51–8.17 m.

**The cause is two conventions that were never reconciled.** The derivation convention puts
a record's point on its FRONTAGE — the position notes say *"offset 12.2 m, half an 80 ft
platted street"*. The drawing convention puts local `(0, 0)` at the polygon's minimum corner,
so the body grows north and east from that point; **331 of the 333 committed footprints do
it.** A south-side building with its point on the south kerb is therefore drawn into the
roadway **by its own full depth**. All 13 deep South Water records declare the south side and
all 13 are drawn northward from the kerb; across the whole table, **all 17 deep records have
their body drawn toward the street from their own anchor**. Reflecting each body about its
own point takes **12 of the 17 under 1 m**, five of them to exactly zero. K30(a)'s recentring
was the wrong operation on the right suspect — it moves a body half its depth, and cannot
clear a fault whose size *is* its depth.

**The shallow tail is answered and is not to be fixed.** Once a body is drawn on the correct
side of its own point, what is left in the roadway **is how far that point stands inside the
corridor** — to within **0.10 m** over the six records the law covers. So the two terms are
separable and unequal: the drawing term is a building's depth, 4.51–8.17 m; the point term is
**0.35–1.69 m**, which is what a derived corridor and a hand-traced centreline disagree by.
`tremont_house_1`, `exchange_coffee_house` and `western_hotel` are their point's penetration
and nothing else, and their bodies are **already drawn correctly** — reflecting them sends
them 12 m into the road, which is the check that the law is about the point. Twelve nudged
buildings would have bought nothing.

**A bridge in a street is not a building in a street.** `slough_log_bridge` is now
categorised as street furniture — derived from its own archetype *and* function, never from
a list of ids — and its row stays in the table, in the baseline and under the ratchet. The
exemption's obvious abuse is to relabel a store as a bridge, so the gate refuses any category
change; `peck_store` was disguised as a `bridge_timber` crossing before the rule was trusted
and the gate caught it.

**What is NOT done.** Nothing was redrawn. The repair changes footprints, so it changes every
affected mesh and needs a bake the improve runner cannot do — that is **K30(c)**. Three deep
records are not the frontage fault and are named rather than averaged in:
`newberry_dole_warehouse`, whose point is 7.00 m inside the corridor and whose own note says
its bank is disputed; `hogan_store`, derived to the Lake/Market junction at the wedge; and
`temple_building`, which improves but does not clear. **No coordinate, dimension, footprint or
confidence moved, and nothing was invented.**

## 2026-08-16 — 29 buildings are drawn standing in the town's own streets, and every one of them was placed by hand

**K30(a)**, the measuring half. T-A9 found three documented stores inside the South Water
Street corridor and T-A12 found two more, and the entry that collected them asked for the
distribution rather than the anecdotes. It is a command now —
`tools/measure_corridor_intrusion.py` — and `tools/check.sh` runs it.

**29 of the town's 332 placed phases lap one of the 13 platted corridors.** 16 have their
centroid in one, which is T-A7's test; 9 have their authored position point in one. South
Water carries 14 of the 29 and the deepest at **12.10 m**, but the set spans **eight**
streets — Randolph, Clark, State, Lake, Dearborn, Wells and Canal as well — so
"all of them are on South Water" does not survive the full measurement.

**Every one of the 29 is a `research`-layer record.** Zero of the anonymous reconstruction
roofs and zero of the inferred-household roofs lap any corridor. Every generator has asked
`plat_corridors.intrusion()` before placing anything since K7, and this parcel commits that
as an **absolute** assertion rather than a ratchet: a generated roof in a roadway is a
regression. Both halves of the gate were broken deliberately before being trusted.

**The depths are bimodal, and the gap is the finding.** Nothing at all sits between 1.98 m
and 3.48 m: 17 records deep, 12 shallow. **13 of the 17 deep are South Water.** The shallow
tail is spread over six streets at ≤ 1.98 m, which is what a derived corridor and a traced
centreline can honestly disagree by — T-A7's "a metre or two proud of its own frontage". The
deep cluster is not that, and it has no attributed cause yet. *(K30(b), the entry above,
attributed it the same day: the cause is the drawing convention, and the shallow tail's
"metre or two" is now measured at 0.35–1.69 m rather than described.)*

**Two numbers that were quoted and do not reproduce.** T-A7's *fourteen* records with their
centroid in a roadway is **16** — measured at `52641c46`, the commit that states it, as well
as today, and it is the same 16 both times, so the layer has not grown. And two of the four
buildings T-A7 names are printed against the wrong street, because a centroid at an
intersection is inside **two** corridors and nothing said which to report.

**The one systematic cause that could be tested here was tested and is refuted.** The
position sits at the footprint polygon's origin, which is a vertex on 332 of 333 records, so
a building derived to a street corner is drawn with a corner on that point — a good enough
mechanism that 20 of the 29 anchors stand on legal ground while the body reaches into the
street. Centring every footprint on its own anchor clears 5, improves 14 and makes **10
worse**, the Tremont House by 7.59 m. `--recentre` keeps the refutation runnable.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs`, for the usual reason
— the harness's ten-minute per-command ceiling (ROADMAP, "the run budget"). `tools/check.sh`
passed and the mobile half passed against the published mirror. This parcel ships no data,
renderer or scene change, so there is nothing in it a browser could load differently: **no
record, coordinate, dimension or confidence moved**, and no building was touched.

## New 2026-08-16 — every card's dossier link was a 404 on the deployed site, and 30 of them should never have been links

**K26.** Each building card ends with a link to the research write-up behind the building, and
`popup.js` composed it as a path relative to the walkthrough. `tools/publish.sh` leaves `docs/`
out of the payload by design, so **all 332 links 404'd on the deployed site** — measured, not
reasoned about: `…github.io/custom/chicago/4d/docs/RESEARCH/sauganash_hotel.md` returns 404 and
the same dossier on GitHub returns 200. The link resolved in the source tree, which is the one
place it was ever clicked.

**The link is now absolute and goes to GitHub**, which renders markdown; `main` rather than `dev`,
because that is the branch a visitor's copy was promoted from (0 of the 55 distinct dossier paths
currently linked are dev-only, so the lag is nil today).

**The 30 are the finding the parcel did not predict.** The compiler asserted
`docs/RESEARCH/<id>.md` by convention and never asked whether the file existed — right about 302
records, wrong about 30, every one a *documented* building whose write-up has not been done (the
courthouse, the log jail, the estray pen, St Mary's, the Temple Building, the Presbyterian church,
Kinzie & Hunter's warehouse). Those cards now say *no dossier written for this building yet* and
offer no anchor. The 30 remain a research debt and `tools/check_dossier_links.py` names them every
run.

**Why it survived:** the smoke asserted the card's TEXT contained the path, which was true on every
run while every link was broken. It now reads the `href` and asserts it leaves this origin, with
`temple_building` as the discriminating no-link case. `validate.py` had gated the *open question*
dossier pointer's existence since it was written; the building card's pointer never had it.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs`, for the usual reason — the
harness's ten-minute per-command ceiling (ROADMAP, "the run budget"). `tools/check.sh` passed and
the mobile half passed against the published mirror, **219 passed / 0 failed**. The two new
assertions were additionally run at 1280×800 against the same mirror by an ad-hoc script — both
green, zero page errors, in 7.5 s — so what is unverified at desktop is the rest of the suite, not
this parcel's own claims. That number is worth noting on its own: booting the published walk-
through and reading two cards at desktop costs seconds, and the desktop half's thirteen minutes
are its road-contrast and horizon captures. A test-name filter would let it run as two commands
that each fit.

**No geometry, dimension, coordinate or confidence moved**: 30 sidecars lose a path that pointed
at nothing, and the rest are untouched.

## New 2026-08-16 — the ground still stands over the road it carries, and the fix costs 1,116 bytes

**R-W6**, which expected to prove the horizontal artefact invisible and instead measured it on
South Water Street. R-BUG3c repaired the 306 mm VERTICAL lattice by reading heights back off the
heightfield at load; the same quantiser moves E and N, nothing corrects that, and a vertex
conformed at a displaced position holds the field's height for the wrong place.

**Measured at all 259,689 of the field's own sample points, after `conformGroundToField()`, by
interpolating the containing triangle in plan** — `tools/measure_terrain_horizontal.mjs`, with the
14-bit rebuild coming back **byte-for-byte identical to the file in `assets/web/`**, so the
numbers are the shipping ones:

| encoding | KB | lattice | plan displacement | drawn surface vs field (rms / p99 / max) | past the 22 mm road lift |
|---|---|---|---|---|---|
| master | 6296 | float | — | 1.3 / 3.8 / **7.7 mm** | — |
| **shipped, 14-bit** | 671 | 306.4 mm | **273.1 mm** | 2.1 / 7.9 / **46.3 mm** | **87** (44 dry) |
| **16-bit — taken** | 672 | 76.6 mm | 52.0 mm | 1.4 / 3.8 / **12.9 mm** | **0** |
| uncompressed | 6296 | float | 0.0 mm | 1.3 / 3.8 / **7.7 mm** | 0 |

**The closest over-budget sample stands 1.9 m from South Water Street's centreline** — inside a
10.5 m travelled track — **30.2 mm above the field, carrying a road lifted 22 mm.** That is
R-BUG3c's failure mode surviving its own fix, on the street the owner reported it from, at 1/5
the amplitude and on 0.03 % of the town. The mechanism is slope, not size: the 87 samples sit at
a median slope of **18 %**, and flat platted prairie cannot show this at any bit depth.

**The decision, made by measurement rather than preference.** The terrain keeps shipping
quantised — the uncompressed file buys 12.9 mm → 7.7 mm for 5.8 MB, and 7.7 mm is DECIMATION
every row carries — at **16 bits on the epoch meshes only**: +1,116 bytes, against +105.7 KB
(+2.4 %) measured for raising the whole payload to buy nothing measurable, because precision is
per-mesh and every asset that is not the terrain or the water already lands inside 4.8 mm
(median 0.5 mm). Two corrections ride with it: R-BUG3c's *"E and N move by up to 153 mm"* was
arithmetic and the measured figure is **273.1 mm** in plan; and 15 bits is *bigger* than 16.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs` — the ten-minute
per-command ceiling. The mobile half was run against a published mirror carrying the 16-bit
ground: **218 passed, 0 failed**. **No GLB ships with this parcel**: `assets/web/` belongs to the
nightly bake, so the ground a visitor loads stays 14-bit until `chicago-4d-bake.yml` next runs.

## New 2026-08-15 — 623 invented details cited a band the specification never wrote, and 42 of them were unfindable

**K33**, the other half of K25's subject, and it is worse in kind: not a value outside its band but
a value with **no band to be inside**. K25(a) opened it at 581 from the prose census. The measured
figure is **623 values on 227 of 249 records** — `paint` 220, `chimneys` 93, `board_gap_m` 69,
`plan` 46, `door`/`door_side` 37 each, `bays` 35, `porch` 23, `goods_door`/`goods_door_side` 8 each,
`gallery` 4, `shopfront` 1 — **and `roof_pitch_deg` 42.**

**The 42 are the finding, and the reason they were missed is structural.** Five families — A3, A4,
A5, W4, W5 — write their roof as *"gable or shed"*: a form with no slope in it. Every one of their
records still carried a note saying the pitch was a type-level choice within the family band.
K25(a)'s banded half could not see them because **a value with no band is never tested against
one**, so the tool walked past exactly the records where the fault is total rather than partial.
The generous keyword was a floor on the prose census; the *classification* was a second floor
nobody had named.

**Route 2 (split the note) was chosen, and route 3 was measured as unavailable.** Grading these a
level lower would stale 249 committed GLBs — `generators/mesh_inputs.py` hashes the confidence
FLOATS into the mesh input recipe, which is the same wall T-V1(b) and K25(b) sit behind. **Prose is
not hashed**, so the honest repair and the affordable one are the same repair here. That is a
coincidence and is written up as one, because next time it will not be.

**The note negates the lede rather than dropping a citation.** Every affected value is prefixed by
a generator paragraph reading *"the spec is cited because the invention is bounded by it"* — the
exact untrue claim — so a silent removal would have left the false impression standing. The
replacement opens `NOT BOUNDED BY THE SPECIFICATION, and the sentence above about the invention
being bounded does not hold for this value`, names the family and the field, and says the value is
the reconstruction generator's type default. Each parcel's own closing clause is kept verbatim.

**`tools/band_notes.py` is the single predicate**, imported by all five generators that author the
sentence and by `tools/measure_band_claims.py` that audits it — `family_bands.py`'s lesson, applied
before it could bite again. The assertion runs in `--gate` and `--strict` and is **absolute: no
baseline, no allowance**, deliberately unlike the K25 ratchet beside it, because a prose repair
costs no bake and can block nothing. **Proved in three directions before being trusted:** 623 red
against the pre-repair data, 0 after, and a hand-planted fresh offender caught. An unclassified
field carrying a citation also fails, so the next invented fitting cannot inherit one by default.

**Residual, stated rather than tidied:** `sources` on these 623 values still lists the spec while
the note now says the spec does not bound them. The spec IS the source of the family assignment
behind the archetype default, so it is not simply wrong — but the two fields no longer agree, and
that wants a decision rather than a sweep. **No value moved and no geometry moved:** 623 note
strings, one new tool, five generator call sites, one gate assertion.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes **no
geometry, no dimension and no renderer code** — only note prose, which is stripped from every mesh
input hash in this project.

## New 2026-08-15 — it is 98 values, not 54, and 24 causes, not 98 — and roof pitch had never been measured

**K25(a)**, the measurement half. The parcel was scoped from an eave count taken on 193 records.
Asked properly — every reconstructed record in the dataset and every form value the crosswalk
authors a testable band for — **1135 values were tested against a band and 98 are outside it, on
80 of 249 records**: **54 eaves, 38 roof pitches, 4 storey counts, 2 footprints, 0 roof forms.**
The eave figure of 54 survived the widening by coincidence, and T-V1(a)'s 40 is its anonymous half.
**Roof pitch had never been measured by anything in this project**, and it is the second-largest
fault in the dataset's provenance.

**The 98 are 24 causes.** Thirteen (family, value) pairs hold all 54 eaves and **six degree
constants hold all 38 pitches**: 2.78 m against D3's 8–9 ft on 20 records, 2.05 m against D2's
7–8 ft on 10 and against **W4's 9–18 ft on 3** (the worst, +2.27 ft), 18.0° against D2's 4:12 floor
on 21. **Seven metre values account for all 54 eaves** — 2.05, 2.75, 2.78, 3.25, 5.05, 5.20, 5.35 —
which is the archetype table, not a measurement of anything. The generator picks the value from the
**archetype** and the note cites the **family**.

**Pitch is a unit mismatch and nothing else.** The crosswalk authors rise:run; the generator authors
whole degrees. 4:12 is 18.435° and the shed constant is 18.0°, so 21 D2 sheds sit **0.10 of a 1:12
step** under a floor they would have cleared had the value been authored in the band's own units.
All 38 are within one step.

**The sub-1-ft question K25 left open is decided: they are failures.** 46 of 54 eaves are within a
foot and nearness is exactly what a retyped constant looks like. The only slack in the tool is
1.5 mm for the metre round-trip.

**A second fault, reported and not gated.** The same sentence is on values the specification does
not bound at all — **`paint` on 227 records, 220 against a family that never mentions paint;
`board_gap_m` on 99 against a specification that names no board gap anywhere; `chimneys` on 150,
93 silent.** There is no band to be inside. The instrument is a keyword and therefore a floor, so
it prints rather than fails, and it is opened as **K33** with the decision it needs stated.

**`tools/measure_band_claims.py --gate` runs on every `check.sh`, as a ratchet.** The strict
assertion **fails today and is meant to** (`--strict`, exit 1, 98 findings); what gates is the
committed census in `tools/band_claims_baseline.json` — a new offender, or a committed one whose
value moved, fails. **Both halves were broken on purpose and proved to fail** before being trusted:
a planted 4.9 m D1 wall is caught as NEW, and repairing `recon_1835_north_d3_002` without rewriting
the baseline is caught as an unrecorded repair. The fault may shrink and may not grow.

**K25(b) is blocked exactly where T-V1(b) is blocked** — every offender is on a canonically baked
parcel, and the repair cannot pass the gate it must pass to reach the branch the bake reads. **No
dimension moved here.**

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes **no data,
no geometry and no renderer code**: what ships is one new tool, its committed census, one gate step
and documentation.

## New 2026-08-15 — the twins are all in one parcel, and 40 notes are wrong about their own source

**T-V1(a)**, the measurement half. R-G1 blamed `south_water` for a horizon of one gable repeated,
and that row had already been fixed twice before this parcel was claimed: the phase-one South
parcel samples its footprints, and all twelve `phase3` platted-block parcels sample footprint and
eave. Measured across all **218** anonymous roofs, **every twin in the town is in one parcel** —
`phase2_north_division_initial`, written before the sampling rule existed. Sixty roofs, twenty-three
families, **24 distinct massings; 36 of the 60 share a footprint AND an eave with another roof of
their own family**.

**THE CENSUS FOUND SOMETHING BIGGER THAN THE TWINS.** Every invented dimension carries the note
*"Type-level choice within the &lt;family&gt; band"*, and that sentence is the entire defence for the
invention. **40 of the 218 eaves are outside the band their own note cites** — 18 in `phase1_south`,
17 in `phase2_north`, 5 in `phase2_west`. The phase-one parcel is the sharp case: it samples its
FOOTPRINT and carries the sentence saying so, while its eave is still one constant per family. So a
record can hold a true sentence about its plan and a false one about its wall, in the same note
style, and nothing distinguished them. This is ROADMAP **K25**'s fault measured on a second layer;
**none of the 40 is fixed here.**

**`tools/measure_massing_variety.py --gate` runs on every `check.sh`.** Its subject is a sentence
the data itself makes: the 138 records that say `sampled deterministically` are held to it — inside
the band, unique within family and parcel. **Both clauses were broken on purpose and proved to
fail** before being trusted. Everything else it reports and does not fail, and the tool's docstring
says why in as many words: *do not read a pass here as "the town is a distribution"*.

**One real bug, fixed.** The eave floor that keeps an invented outbuilding tall enough to carry its
own door was `DOOR_HEADROOM_M = 2.05` — a **man** door — applied to every door-carrying family,
including the wagon doors on W1, W2, W5, F1 and A2. A wagon door is 3.00 m in the clear. It never
bit because those families stood at a retyped 3.42 m; the moment the North parcel sampled its band,
`recon_1835_north_w1_*` failed by name at 2.821 m with no header. `eave_floor(family, door)` now
asks `outbuilding_params.DOOR_SIZE_M` instead of carrying a hand-copied constant — the same fault
this parcel is about, in miniature. The 90 block records are **byte-identical** across the change.
The sampling rule itself moved to `tools/family_bands.py`, which both generators now import.

**T-V1(b) IS WRITTEN, MEASURED AND CANNOT LAND HERE — read its ROADMAP box before touching any
dimension on a baked record.** Wiring the North generator to `family_bands` was implemented and run:
every placement gate passed (no collision, no corridor intrusion, nothing off the terrain, nothing
over the 0.35 m relief contract), and it takes **36 twins to 0, 24 distinct massings to 60, and 17
out-of-band eaves to 0**. It was reverted because the sixty North GLBs are canonical Blender bakes:
changing a dimension stales all sixty, `validate.py --all` is the dev gate, there is no Blender on
this runner, and `chicago-4d-bake.yml` bakes **from `dev`** — so the fix cannot pass the gate it must
pass to reach the branch the bake reads. **That circle stands in front of K25(b) and every parcel
that would move a dimension on the 128 canonically-baked roofs.** Three routes are written up for
the owner; choosing one is a policy question and an overnight run did not make it.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the harness
caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP, "the run
budget"). `tools/check.sh` and the mobile half both passed. **This parcel changes no data, no
geometry and no renderer code**: what ships is two new tools, one gate step, an import in the block
generator whose 90 records are byte-identical, and documentation.

## New 2026-08-15 — sixteen refusals were made against candidacies this layer never actually had

**T-A3h**, the backfill of `blk_randolph_dearborn` — the one block that landed before rule 6 had its
third test, and so the one block never asked who lived on it. The adoptions are the two the parcel
predicted: the **D3** on lot 0 to a twentieth carpenter's household, the **D1** on lot 3 to a
twenty-third labouring one. Inferred households **99 → 101**, persons **111 → 113**, adopted
anonymous roofs **102 → 104**, and **standing roofs unchanged at 322** — nothing was built, moved or
regraded. Recorded in **L109**.

**THE FINDING IS ABOUT THE ROOFS IT REFUSED.** The block also deals a **D4** and a **D2**, and both
print ADOPTABLE — the carpenters' "second roof" and the labourers', exactly as at eight blocks
before it. Nobody had asked what those verdicts are made of. This layer houses **one** carpenter in
a D4 and that household stands in the **North** Division; it houses **four** labourers in a D2 and
all four stand in the **North** or the **West**. Every carpenter and every labourer it houses in the
**South** Division lives in a D3 or a D1. **Neither second roof is a (family, division) pair this
layer has ever housed.**

**It passes because rule 6 says its three tests are independent, in as many words.** Test 2 reads
the set of families and test 3 the set of divisions, so a roof is admitted on a family taken out of
one division and a division taken out of another family. `tools/measure_adoption_tests.py --pairs`,
added here, prints the cost: **20 pairs across 8 trades are admitted by the projections and housed by
nothing**, and test 1 leaves exactly **two** of them adoptable — the carpenters' D4/south and the
labourers' D2/south, which are precisely the two roofs every second-roof refusal has been about.
Sixteen refusals across nine blocks were refusals of a candidacy assembled from evidence that is
never about the same roof twice.

**THE STRICTER READING IS NOT TAKEN, AND THE REASON IS COMMITTED RATHER THAN ASSERTED.** Requiring
the pair would refuse the **fourteenth labouring household** — T-A4's D1 in the West Division,
adopted when this layer housed labourers west of the river only in D2 shanties, and argued in
exactly the projected form. Rule 6 names that adoption as one of the four its third test *recovers*,
so a pair reading breaks the calibration the rule rests on. The tool reports a `pair housed` column
and gates nothing; **ROADMAP K28 now has three things to settle rather than two**, and the cap
question it was opened for may be a question about an empty set.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes no renderer
code and no geometry; what a browser loads that is new is two `occupants` blocks and the names on
67 invented persons.

## Fixed 2026-08-15 — a quarter of the modelled land was never open to a builder, and nothing said so

**T-E2**, lane 3's first parcel after T-E1 registered the 1830 sheet. Two grounds outside the plat
are now refused: the **United States Reservation** east of State Street and the **sand bar across
the river mouth**.

**The number is the argument.** Of the **121.18 ha** of modelled land standing above the water
surface in this scene, **32.10 ha — 26.5 %** is one or the other: the reservation 22.57 ha, the bar
9.53 ha. Every gate this project had asked whether a placement cleared its neighbours, its lot
lines, the platted roadway, the modelled terrain and the relief. None of them asked whether the
ground was ever for sale. L107 found that hole inside the plat five days' work ago and closed it
for blocks; this is the same hole where it is four times bigger.

**Nothing moved, because nothing was there yet — and that is luck, not a rule.** Seventeen
structure records stand on the two grounds and all seventeen keep their places: the fort's stockade,
parade and eleven buildings, the garrison garden, the 1832 lighthouse, Beaubien's homestead and
barn, and the south pier, which touches both. **Zero anonymous roofs.** Every recipe so far has been
keyed to a platted block, and the reservation was never platted, so the ground was spared by the
order the work happened in. The gate lands green on the day it is written, and both of its
assertions were proved to fail before it was trusted: removing one permission fails it by name, and
shrinking the bar polygon to a sliver fails the under-coverage count with 11,100 cells.

**THE REFUSAL IS DOCUMENTED; THE BOUNDARY IS INFERRED, DERIVED, AND HONESTLY SHORT.** Andreas gives
the reservation as 75.69 acres, the southwest fractional quarter of Section 10 — unplatted, outside
the town's own eastern boundary, and under Beaubien's five-week-old pre-emption claim on the scene
date. Not one vertex of the polygon is authored: its west and south sides are the quarter's two
survey lines resolved from the single control point `wright_1834_gcps.json` **G1**, whose own note
has said since the datum work that Madison's line continues east as the reservation's south
boundary; its third side is the committed waterline the trace already calls the reservation's lake
shore. **The derived polygon comes to 65.70 acres against the documented 75.69 — 13.2 % short — and
it is not tuned to close the gap.** The candidates (a meander line east of the 1834 waterline, the
trace's own +/-20 m, a shore trace that leaves its window south of Madison) are named and none is
measured.

**So the polygon is a floor, and the floor is checked rather than trusted.** The gate re-counts, on
every `check.sh`, the cells of modelled land above the water surface that stand east of the west
line, north of Madison, south of the main stem and inside neither polygon. Today that count is
**zero** — the polygons reach every square metre of ground the terrain models there. **T-E3 extends
the terrain east and south, and that is the parcel this assertion exists to catch.**

**Still open, and honestly open:** four structures the 1830 plate draws — Mark Beaubien's,
Elijah Wentworth's cabin, La Framboise's cabin and store, Porter's log cabin — have no record, no
exclusion and no tested survival to 1835-07-01. T-E2 lists them as open questions rather than
inventing dispositions, in the new disposition table at the foot of
`docs/RESEARCH/chicago_1830_claims.md`. **Mark Beaubien's is the one inside the modelled area.**
The reservation's own residue is recorded too: the 562 cells the first pass flagged as
unclassified turned out to be entirely the waterline tolerance band, every one of them between
-0.10 m and 0.00 m, and none of them ground.

## New 2026-08-15 — the town's public square was being offered to invented houses, and two documented ones were already standing on it

**T-A16.** `blk_randolph_lasalle` — Randolph, Clark, Washington, LaSalle — was claimed as the last
open block entry on its row and **was not built**. It is **the public square**: Andreas calls it
*the square* and *the court-house square*, this project's own ground control names its corners
*NW / SE corner of the Public Square block*, and it carries the estray pen (its south-west corner,
March 1833, Chicago's first public building), the log jail (north-west, fall 1833) and the first
Cook County court-house (1835). The 665-roof programme was dealing it four invented private roofs —
an `A1`, a `D3`, a `D4` and a `D5`. The block is now **reserved**: no lots, no roofs, a refusal in
the block generator, and a gate in `check.sh`. **Standing roofs unchanged at 322; remaining 343, 1
of them on covered ground** (was 5 — the square held four of the five). The plat grid drops from
152 lots to **144**. Recorded in **L107**.

**EVERY PLACEMENT GATE THIS PROJECT HAS PASSED THE TWO BUILDINGS THAT WERE STANDING ON IT, AND THAT
IS THE HEADLINE.** `wright_building_to_let_a` and `_b`, John Wright's two documented cottages to
let, were placed in *"the South Division band the recipes use for ordinary dwellings"* and that band
ran across the square. Their placement was tested for clearance from other buildings, for its own
lot lines, for the platted roadway and for buildable ground — every question this project knew how
to ask about a position, and **not one of them was whether the ground was for sale**. They have been
moved: each takes the nearest free platted lot no committed block recipe has already spoken for, 83 m
and 69 m, onto the Randolph frontage of the two blocks facing the square. The pair is split, and the
split is stated — the only ground that kept them on one block was 200 m further off and faced two
different streets, and one advertisement offering two buildings never said they shared a holding.

**The defect is upstream of the schedule.** `tools/generate_plat_lots.py` subdivides every block it
can build, because that is what the Thompson module says a block is; it has no way to ask whether a
block was ever offered in lots. So the reservation withdraws the **lot lines** and not merely the
schedule's permission to use them, and `lots_per_face_withheld` records what the module would have
drawn so the withdrawal is visible rather than looking like a generator failure.

**THE RESERVATION IS `inferred` AND IS NOT PROMOTED.** No source this project holds states that the
square was reserved from sale. What it holds is the block's name, the county's three buildings on
it, the dossier's own reading of the rest of it — *"open, unimproved, fenced or unfenced prairie
block"* — and one period description of the ground itself: *"Our public Square was then a pond,
where the Indians had trapped the muskrat, and where the first settlers hunted ducks."* The grade
stays where the evidence puts it, and `tools/measure_reserved_ground.py` prints what a refutation
would change.

**THE POND IS DOCUMENTED AND IS NOT MODELLED — T-E5.** The terrain carries no standing water on this
block and the marsh flora zone is a buffer of the mapped water, so the square renders as dry prairie
with three public buildings on it. That is a second false statement about the same ground. It is
opened rather than closed here, with the three questions that have to be settled before any ground
moves.

**The eleventh K20 measurement is 0 of 111** carried-over invented persons renamed, against 12-of-110
at T-A15 and a range of 7 %–72 % over the nine before it. Zero for a structural reason: **this parcel
inserts and removes no person**, so the allocator has nothing to shift. That is the first evidence in
nine measurements about *what* perturbs it.

**Unverified here:** the desktop half of `tools/smoke_renderer.mjs` — this parcel changes data, tools
and docs only, and the desktop half does not fit the runner's ten-minute per-command ceiling (see
ROADMAP § THE RUN BUDGET). `tools/check.sh` and the mobile half of the smoke were both run green
against the published mirror.

## New 2026-08-15 — the block opposite the courthouse, and two of yesterday's three adoption candidacies do not reproduce

**T-A15.** `blk_randolph_clark` — Randolph, Dearborn, Washington, Clark — now carries **eight
anonymous roofs**: a store-residence, five dwellings, a woodshed and a privy, on six of its seven
free lots, with lot 1 left open and lot 0 held by the inferred gunsmith's shop. **Standing roofs
314 → 322; remaining 351 → 343, 5 of them on covered ground** (was 13). Inferred households 98 → 99,
inferred persons 110 → 111. Recorded in **L106**. **The recipe cleared every placement gate on its
first run** — the eighth block in a row. The block stands across Clark Street from the public square
(county courthouse, both Wright buildings to let, the estray pen) with Dearborn Street, the bridge
street, for its east face; it is the first block parcel dealt **both** larger house families at once
and the first to stand a **`C2` store-residence**. One adoption: the `D1` log cabin on lot 3 becomes
the twenty-second inferred labouring household.

**TWO OF T-A14's THREE ADOPTION CANDIDACIES DO NOT REPRODUCE, AND THIS IS THE HEADLINE.** The entry
directly below records that its `D2` passes all three of method rule 6's tests for the
**laundresses** and its `D4` for the **teamsters**. Tests 2 and 3 hold for both. **Test 1 does
not**: rule 6 asks whether the trade's *own argument* states in its committed text that its count is
a floor rather than a bound, and neither of those arguments contains any such statement — the only
occurrence of the word in the laundress argument is Andreas's *"with the floor covered besides"*, a
plank floor in a boarding house. Only the **carpenters** and the **labourers** state it.
`tools/measure_adoption_tests.py` is committed so the next parcel **runs** rule 6 rather than
recalling it, and prints the sentence each verdict rests on. The T-A14 entry below and L105 are left
standing verbatim; what is corrected is the method. **K28's question narrows**: not "may a trade
that has not asked for a roof be given one" but "does test 1 mean the trade's own text, or method
rule 3's list of unbounded trades" — two readings that disagree for exactly two trades. Run on this
block's `D2`, exactly one trade passes: the labourers, taking a second roof, refused for the eighth
time on the same conservative reading.

**The face rule reproduced exactly — the first time that can be said.** `tools/
measure_street_frontage.py randolph washington` returns Randolph 7 research / 7 inferred-household
against Washington 1 / 0, the same 14 against 1 T-A14 measured on the same pair, from a command
rather than from a memory. The third layer read 18 and 12 and is excluded, not merged.

**The face rule ranks dwellings, and this block had a store, so the rule was EXTENDED — see K32.**
A store-residence's claim on the better frontage was taken to be functional rather than social, so
the `C2` took Randolph's third free lot and the `D6` that would have had it went to the head of the
back street. That is an invention about 1835 commerce made by an agent; it is flagged rather than
left to repeat, and **K29 is circling the same question from the other side**.

**THE END RULE IS EXHAUSTED ON THIS ROW — see K31.** Distance to the Dearborn Street drawbridge runs
**318.3 / 321.1 / 325.8 m** across the Randolph frontage and 376.4 → 388.2 m behind. Far/near on the
front face is **1.02×** against T-A14's 1.11, T-A13's 1.13 and T-A12's 2.93, and the absolute spread
is **7.5 m** — under a third of one lot's 24.6 m frontage. The cause is geometric: the bridge bears
**10.4° east of north** from the block centre while the face runs east–west, so the criterion sees
only **18 %** of any along-street displacement. It was followed anyway on T-A13's reasoning, and on
this block a stronger criterion agrees with it (lot 6 is the corner on Dearborn, the bridge street),
which is exactly what K31 must not assume holds elsewhere. **Do not quote the end rule as if it
ordered anything on the Randolph–Washington row without re-measuring it.**

**Unverified here:** the desktop half of `tools/smoke_renderer.mjs` — this parcel changes data and
docs only, and the desktop half does not fit the runner's ten-minute per-command ceiling (see
ROADMAP § THE RUN BUDGET). `tools/check.sh` and the mobile half of the smoke were both run green
against the published mirror.

## New 2026-08-15 — a block with no front, and the face rule's first measurement does not reproduce

**T-A14.** `blk_randolph_franklin` — Randolph, Wells, Washington, Franklin — now carries **eight
anonymous roofs**, six principal, a stable and a privy, on six of its seven free lots, with lot 1
left open and lot 2 held by Harmon's log cabin. **Standing roofs 306 → 314; remaining 359 → 351, 13
of them on covered ground** (was 21). Inferred households 96 → 98, inferred persons 108 → 110.
Recorded in L105. **The recipe cleared every placement gate on its first run** — the seventh block in
a row — and it is the first block parcel of this shape to commit a tool, for the reason below. It is
the first block on the row **two streets back**, and the first **neither of whose faces the town's
record calls a front**.

**T-A13'S FACE-RULE MEASUREMENT DOES NOT REPRODUCE, AND THIS IS THE HEADLINE.** The entry directly
below reports **Lake 12, Randolph 2, South Water 9** for "every documented or inferred structure
whose footprint centroid stands within 25 m of a street's committed centreline". No filter
recoverable from this repository produces those numbers — the stated one gives **Lake 17 / Randolph 7
/ South Water 14** on the research layer alone — and the filter actually used was never written down.
The judgement it supported survives every filter tried (Lake is the better face by a wide margin);
what failed is **reproducibility**, which on a project whose product is provenance is the more
serious of the two. `tools/measure_street_frontage.py` is committed so the next parcel runs the
measurement rather than remembering it. **The T-A13 entry below is left standing verbatim**, and so
is L104: LIBERTIES.md is append-only and what is corrected is the method.

**The count reports its three evidence layers separately and never sums them.** The anonymous roofs
the block parcels themselves place stood at **15 on Randolph and 9 on Washington** when this
arrangement was chosen and read **18 and 12** the moment the parcel built — a face rule counting that
layer reads the programme's own output back as evidence. Excluded, this block's answer is **14
against 1**: Randolph carries 7 research-layer records and 7 inferred-household buildings, and
**Washington Street's entire documented 1835 frontage is the estray pen**, the town's pound for stray
animals.

**The end rule's spread has thinned for a second block running.** Distance to the Dearborn Street
drawbridge runs **527.8 m** at lot 6 to **584.0 m** at lot 0 on the Randolph frontage and **568.5 m**
at lot 7 to **621.0 m** at lot 1 behind. The far end of the front face stands **1.11×** as far from
the bridge as the near end, against T-A13's 1.13 and T-A12's 2.93, and the front face's absolute
spread is **56.2 m** against T-A13's 68.2 m. Followed anyway on T-A13's reasoning, and recorded as
closer to arbitrary than ordered.

**The "second roof" question has been the wrong question for six blocks.** The D4 and D2 that every
block since T-A9 has refused as *second* roofs for the carpenters and labourers are also the
**first** roofs of the **teamsters** and the **laundresses** — the other two of method rule 2's four
unbounded trades, each housed in that one family and no other, each already in the South Division,
each passing all three of rule 6's tests on those roofs. **Sixteen anonymous D2 and D4 roofs stand in
the South Division under exactly that description.** K28 is settling a larger question than it was
opened on: not whether a trade may take a second roof, but whether rule 6 may hand a roof to a trade
that never asked for one.

**The ninth K20 measurement is 61 of 108** carried-over invented persons renamed, against 67-of-106
at T-A13 and 7-of-102 at T-A11. Seven measurements span 7 % to 72 % with nothing fixed or broken
between them. K20 still owns the fix.

**Unverified here:** the desktop half of `smoke_renderer.mjs` does not fit this runner's ten-minute
per-command ceiling and was not run; the mobile half was, and `tools/check.sh` — which is the dev
gate — passed. See the run-budget box in ROADMAP.

## New 2026-08-15 — the first block off the business front, and the rule that arranged the row stops meaning anything on it

**T-A13.** `blk_lake_market` — Lake, Franklin, Randolph, Market — now carries **seven anonymous
roofs**, five principal, a stable and a privy, on five of its six free lots, with lot 3 left open and
lots 0 and 1 held by the Sauganash Hotel with Philo Carpenter's log drug store, and by the packer's
dwelling. **Standing roofs 299 → 306; remaining 366 → 359, 21 of them on covered ground** (was 28).
Inferred households 94 → 96, inferred persons 106 → 108. Recorded in L104. **The recipe cleared every
placement gate on its first run and no tool changed** — the sixth block in a row. It is the **first
block of this parcel shape that is not on South Water Street**; every open entry left in the schedule
is on Randolph.

**The face rule was asserted five times and is measured here, because neither of this block's faces
is South Water.** Five parcels sent their better dwellings to "the business front" and named that
front by the street's documented use — which says nothing about a block bounded by Lake and Randolph.
Counting every documented or inferred structure whose footprint centroid stands within **25 m** of a
street's committed centreline: **Lake 12, Randolph 2, South Water 9.** Lake's twelve are the
Sauganash, the Green Tree, the Exchange Coffee House, the Tremont, the Mansion House, both churches,
Hogan's store, Goss & Cobb's saddlery, Pierce's blacksmith shop, Dole's south warehouse and
Carpenter's log shop; Randolph's two are the log jail and the Western Hotel. The rule now rests on a
measurement rather than a habit, **and it is still an invention**: no source says a better dwelling
stood on the better street.

**The end rule's order survives and its meaning does not, and that is the finding.** T-A11's
criterion — distance to the Dearborn Street drawbridge — runs **532.2 m** at lot 6 to **600.4 m** at
lot 0 on the Lake frontage and **576.3 m** at lot 7 to **640.0 m** at lot 1 behind, ordering the lots
exactly as it has on every block of the row. What changed is the size of the difference. On T-A12's
block the far end stood **2.93×** as far from the bridge as the near end; here, **1.13×**. The
absolute spread of the front face is **68.2 m** against T-A12's 70.2 m — the same block, moved half a
kilometre. **The criterion is now separating two lots a resident would have called the same distance
from the bridge.** It was followed anyway, because changing criteria on the block where the first
stops flattering the answer is how an invention starts to look like a finding — but the arrangement
on this block is closer to arbitrary than on any block of the row, and L104 says so.

**K30 gets its first control measurement, and it is a factor of twenty to forty.** K30 has five
documented buildings standing 4.5–8.2 m inside the platted South Water corridor and asks whether
that is one bad stretch of street or a uniform grid bias. The first two documented roofs measured
against a **different** corridor are on this block: the **Sauganash Hotel intrudes 0.19 m** into the
Lake corridor and **Philo Carpenter's log drug store 0.22 m** — inside the plat's own precision of
standing on the kerb line. Two cases are not a survey; they are the control K30 did not have, and
they point away from a uniform bias. Nothing was moved.

**Two documented roofs share lot 0 and the derived occupancy table names the smaller one.** The
Sauganash puts 94.33 m² of its 96.0 m² on the lot and the log shop 28.58 m² of its 29.7 m²; the
source says the shop stood against the Sauganash's public bar and the footprints touch at 0.00 m, so
the record agrees with itself. `plat_occupancy` names the first holder by id — the log shop — so
**the town's most-documented building is not the one that table credits with its own corner.** It
cost this parcel nothing and it will mislead anyone reading that table for what stands where.

**Unverified here:** the desktop half of `smoke_renderer.mjs` does not fit this runner's ten-minute
per-command ceiling and was not run; the mobile half was, and `tools/check.sh` — which is the dev
gate — passed. See the run-budget box in ROADMAP.

## New 2026-08-15 — the business front is built end to end, and the rule that filled it points the other way on its last block

**T-A12.** `blk_south_water_dearborn` — South Water, State, Lake, Dearborn — now carries **six
anonymous roofs**, five principal and one privy, on five of its six free lots, with lot 7 (the
Lake-and-State corner) left open and lots 1 and 6 held by the Mansion House and the Chappel infant
school. **Standing roofs 293 → 299; remaining 372 → 366, 28 of them on covered ground** (was 34).
Inferred households 92 → 94, inferred persons 104 → 106. Recorded in L103. **The recipe cleared
every placement gate on its first run and no tool changed** — the fifth block in a row. State Street
is the platted town's eastern limit, so **the South Water row is closed**: every block of the
business front is now built, and every open entry left in the schedule is one street back or
further.

**The rule that arranged all five blocks reverses direction on the last one, and that is the
finding.** Four parcels put their better roofs "nearer the town-centre end"; T-A11 stopped asserting
that as a compass direction and measured it — the distance to the **Dearborn Street drawbridge**,
the only crossing of the main stem in July 1835. On the four blocks before this one the bridge lay
east, so the compass and the criterion agreed and nothing separated them. This block's bridge end is
its **west** end: lot 0's frontage is **36.4 m** from it, lots 2 and 4 are **57.7 m** and **81.7 m**,
lot 6 is **106.6 m**, and the back street runs **126.4 m** at lot 1 to **161.1 m** at lot 7. The
parcel follows the committed criterion rather than the compass, which is the whole point of having
replaced one with the other — and the lot left open is again the farthest of the eight from the only
bridge in town.

**A third criterion was tried and is recorded as UNDECIDABLE, which is worth more than a third
number.** A single landmark is a thin basis, so the parcel asked where the *mass* of documented
building is. The footprint-weighted centroid of all **83 documented roofs (19,145 m²)** lands at
local **E 939, N 123**, east of this block, making lot 6 nearest at **189.9 m** against lot 0's
**250.8 m**. Excluding the Fort Dearborn reservation — 13 roofs, **10,460 m²** — moves it to
**E 737, N 88** and reverses the answer: **95.0 m** at lot 0 against **115.9 m** at lot 6. The
criterion therefore turns entirely on whether a military reservation counts as part of the town,
which is a judgment and not a measurement, and its whole spread across the north tier without the
fort is **20.9 m** against the bridge's **70.2 m**.

**K30 is now half-measured and all five of its cases are on one street.** Both of this block's
documented South Water buildings stand in the platted roadway — the **Chicago American office**
**6.91 m** in and **Frederick Thomas's shop 6.25 m**, **148.6 m²** of documented roof on ground the
plat calls street. With T-A9's three (4.5 m, 6.6 m, 8.2 m) that is five documented buildings, all on
South Water, all between 4.5 and 8.2 m in. That is the shape of a centreline or width error on one
stretch, not of a uniform bias across the grid — which is the distribution K30 was opened to find.
Nothing was moved: a position with a source outranks a corridor this project derived.

**Two further confirmations, both of things earlier parcels had to argue.** T-A7's lap case has a
**fifth** instance and it is the largest that costs a lot nothing — the American office laps lot 0 by
**10.74 m²** with **0.00 m²** inside the buildable inset. And T-A11's refusal of the lateral offset
is confirmed independently and more cleanly: from the committed placement, 1.5 m further west buys
**0.01 m** of clearance for 0.76 m of lot-line margin and 3.0 m buys **0.22 m** for 2.26 m, where
half a metre of extra setback buys **0.50 m** and costs neither. The parcel's closest approach is
**7.01 m** against a 3 m gate.

**The row closes with K28 open, and the count is four blocks of five.** The D4 and the D2 this block
was dealt each pass rule 6's three tests read literally and both are refused on the same
conservative reading. One block of the row dealt neither floor trade a second roof, one dealt it to
the carpenters alone, and three dealt it to both. **The seventh K20 measurement is 59 of 104**,
against 7-of-102, 72-of-100, 19-of-98 and 32-of-96 — five readings spanning 7 % to 72 % with nothing
fixed or broken between them.

## New 2026-08-15 — the fourth business-front block, and the first time the row's "better end" is a measurement

**T-A11.** `blk_south_water_clark` — South Water, Dearborn, Lake, Clark — now carries **five
anonymous roofs**, four principal and one privy, on four of its five free lots, with lot 1 (the
Lake-and-Clark corner) left open and lots 0, 6 and 7 held by Harmon & Loomis's store, John Bates
Jr.'s auction room and the first Tremont House. **Standing roofs 288 → 293; remaining 377 → 372,
34 of them on covered ground** (was 39). Inferred households 90 → 92, inferred persons 102 → 104.
Recorded in L102. **The recipe cleared every placement gate on its first run and no tool changed**
— the fourth block in a row.

**THE ROW HAS PUT ITS BETTER ROOFS "NEARER THE TOWN-CENTRE END" THREE TIMES AND NEVER SAID WHAT WAS
AT THAT END.** This block's east end is Dearborn Street, and the **Dearborn Street drawbridge** —
the only crossing of the main stem in July 1835, already a committed structure record, its south
abutment at the foot of Dearborn on South Water — measures the claim: **35.6 m** from lot 6's
frontage, 55.5 m from lot 4's, 78.1 m from lot 2's, **101.7 m** from lot 0's, and on the back
street 126.3 m at lot 7 out to **158.2 m at lot 1**, which is the lot left open. No source says a
better house stood nearer the bridge, so the arrangement is as invented as it was; what changed is
that it is invented against a re-derivable number instead of a compass direction.

**AND THE FACE HALF OF THE SAME RULE MEETS ITS FIRST COUNTER-EXAMPLE.** Three parcels have called
South Water the valuable frontage and Lake the back street. The largest documented footprint on
this block is on Lake: the first **Tremont House at 139.3 m²**, against 92.9 m² for the auction
room, 92.9 m² for Harmon & Loomis's store and 46.5 m² for Pruyne & Kimball's drug store. The rule
is kept — it is a typology for where anonymous dwellings of different tiers go — but it is now
recorded as *not* a claim about which street was worth more, before four blocks of repetition
turned it into one.

**T-A7's lap case has a fourth instance and it is the first that costs a lot nothing at all.** The
drug store laps lot 2 by **4.66 m²**, and **0.00 m² of it is inside the buildable inset**: the
whole lap lies in the 1.5 m margin strip. Two of the store's corners are 0.70 m and 0.65 m inside
the platted lot line and the other two are 5.4 m out in the road, a **5.55 m** intrusion into the
South Water corridor. With L100's 22.1 m² of buildable lap, Kinzie's 9.7 m² and
`recon_1835_west_018`'s 11.9 m², the case now spans its whole range.

**THE OFFSET THAT ANSWERED THE LAST BLOCK'S LAP DOES ALMOST NOTHING HERE, AND THE MEASUREMENT SAYS
WHY.** T-A10 moved a shanty west to clear Church's store. On lot 2 the same move buys **0.03 m at
1.5 m of offset and 0.33 m at 3.0 m** — the 3 m version costing 1.26 m of lot-line margin — where
half a metre of extra setback buys **0.50 m** by itself. Church's store stood deep inside its lot;
this one stands in the roadway, so only the setback changes the distance. The cottage is set back
7.5 m and clears it by **6.83 m** against a 3 m gate, the closest approach in the parcel. The
lateral offsets left in the recipe are jitter and are labelled jitter.

**FIVE SOUTH DIVISION HOUSEHOLDS LIVE IN A D5, THREE BLOCKS RUNNING HAVE BEEN DEALT ONE, AND NO
PARCEL HAD EVER RECORDED WHY NONE OF THEM TAKES IT.** Rule 6's family and division tests pass on
this block's D5 for the baker, the butcher, the blacksmith and both clerks. All five fail test one
— their committed arguments do not call their counts floors, and two of them cap themselves
outright ("only one, because a bakehouse serves a great many people and nothing attests a second").
A refusal nobody writes down is indistinguishable from a rule nobody applied, so it is written down
now.

**K28 GETS A THIRD PRECEDENT INSTEAD OF A SECOND.** The D4 on lot 2 passes all three tests for the
carpenters exactly as T-A9's and T-A10's did, and was refused again on the conservative reading.
Three for three is the ordinary shape of a South Division block, not a recurring edge — the
question should be settled rather than collect a fourth. The labourers were dealt no D2 here, the
first block since T-A8 where their second-roof question did not arise.

**THE SIXTH K20 MEASUREMENT IS THE SMALLEST EVER RECORDED: 7 of 102** carried-over invented persons
renamed, against 72-of-100 at T-A10, 19-of-98 at T-A9, 32-of-96 at T-A8 and 25-of-94 at T-A2h.
Nothing was fixed in between. It is the hash-position mechanism L101 identified, confirmed from the
other end of its range, and it is not evidence that the churn is under control. K20 still owns the
fix.

## New 2026-08-15 — the third business-front block, and the name churn is three times worse than reported

**T-A10.** `blk_south_water_lasalle` — South Water, Clark, Lake, LaSalle — now carries **seven
anonymous roofs**, five principal and two yard buildings, on five of its six free lots, with lot 1
(the Lake-and-LaSalle corner) left open, lot 6 held by the Chicago Democrat's office and lot 5 by
Thomas Church's store. **Standing roofs 281 → 288; remaining 384 → 377, 39 of them on covered
ground** (was 46). Inferred households 88 → 90, inferred persons 100 → 102. Recorded in L101. **The
recipe cleared every placement gate on its first run and no tool changed** — the third block in a
row.

**THE FIRST BLOCK OF THE ROW THAT ARRIVED WITH A DOCUMENTED ROOF ON BOTH FACES.** The frontage
argument T-A8 opened and T-A9 tested — best dwellings to South Water, meanest to Lake — has so far
been free to apply, because the back street was empty on both earlier blocks. Church's store stands
on this one's Lake frontage. The arrangement was applied anyway, so a log cabin and a plank shanty
now stand on a frontage that already carries a documented store. Same invention, less room; L101
says so rather than letting the pattern read as automatic.

**T-A7's `west_018` case has a third and much larger instance, measured here.** Church's store is
seated on lot 5 by test one — **59.3 m² of 92.9 m² there against 33.6 m² on lot 3** — but **22.1 m²
of the lot 3 lap is inside lot 3's buildable inset**, so a lot the schedule reads as free carries a
documented building across its frontage corner. Against 9.7 m² (Kinzie, none of it buildable) and
11.9 m² (`recon_1835_west_018`), this is the biggest yet, and unlike Kinzie's it is *inside* the
buildable part. It is 2.4 % of the lot's buildable area, so the lot still took a roof: the shanty is
offset west, away from the store, and clears it by **7.56 m** against a 3 m gate — the closest
approach anywhere in this parcel. No rule changed and nothing was moved; the number is recorded so
the next parcel to meet the case has three data points instead of two.

**K28 IS NO LONGER A ONE-OFF, WHICH IS THE ARGUMENT FOR SETTLING IT.** T-A9 found rule 6 silent on
how many roofs of one block a trade may take and reported it as a case no block had offered before.
This block offered the identical case: four of its five dwellings pass all three tests for one trade
or the other, the D3 *and* the D4 for carpenters, the D1 *and* the D2 for labourers. Two consecutive
blocks have now dealt both floor trades both of the families they are housed in, so this is what a
five-or-six-dwelling block in the South Division looks like rather than a coincidence. One adoption
per trade was taken again, on T-A9's reading and recorded as a choice.

**AND THE K28 ID IS USED TWICE IN THIS REPOSITORY.** ROADMAP `K28` is the rule-6 question above;
the published-mirror gate that landed as PR #147 also shipped under the name K28 and has no ROADMAP
entry of its own. Both are real work and neither is wrong — the collision is in the label. A
disambiguation line is added at the ROADMAP heading so every existing citation resolves; renumbering
landed work is not a block parcel's call. This is the same defect T-A9 found in L99's pointer, in the
opposite direction.

**THE FIFTH K20 MEASUREMENT IS THE ONE THAT BREAKS THE "A FIFTH OF THE LAYER" DESCRIPTION.**
Inserting two households renamed **72 of the 100 carried-over invented persons**, against 19-of-98
(T-A9), 32-of-96 (T-A8), 25-of-94 (T-A2h) and 17-of-33-touched (T-A5). No grade moved, every
`name_basis` kept its pool citation, and `check.sh` re-derives all 102 — this is churn, not a
provenance failure. The mechanism is not random: `tools/generate_inferred_names.py` deals names
round-robin through each community-and-sex pool in a stable hash order of person id, so one new
person landing early in a large bucket renames everything after it. The spread from 19 to 72 is
purely where the new ids hashed. K20's fix still belongs in its own parcel; this is the fifth block
to ride along on it, and the first where the side effect is larger than the parcel.

## Fixed 2026-08-15 — the general case behind R-BUG3c-b: nothing checked what actually ships

**K28.** #145 fixed the terrain quantiser and ended on one line: *do not measure the file you built,
measure the file you ship.* It also said plainly what it had not done — "Nothing else in this
project measures a published artefact against its own source, and nobody has looked for the next
instance of it." This is that gate.

**The invariant is total, which is what makes it cheap.** `tools/publish.sh` is almost entirely
`cp`: the mirror is meant to be the repository, rearranged. So **every published file must be
byte-identical to its source**, unless it is on a declared list — and each entry on that list has to
say what transforms the bytes and **name the gate that measures the SHIPPED form**. That second
column is the whole point: it is the question nobody asked about the terrain, now written down
beside every place it applies.

Current state: **521 files byte-identical, 296 transformed under 4 declared rules, 0 unmapped.**

**It found two unchecked files on its first run**, which is the argument for it.

- **`build.json` was two days stale.** It claimed version `8909332` built `2026-08-13T19:18:05Z`
  while the mirror beside it was from today at a different commit. Nothing in `publish.sh` ever
  rewrote it — it had been written once, by hand. `tools/test_dev_preview.mjs` and `docs/PIPELINE.md`
  both read it, so both were reading a stale claim about what shipped. `publish.sh` now regenerates
  it every run from the same two variables the visible build stamp uses, so the machine-readable
  twin and the human-readable one cannot disagree.
- **The mirror's `index.html`** is written once from a heredoc and traced to nothing. It is a
  redirect stub with no claim in it, so it needs no gate — but that is now recorded, so if it ever
  grows a claim the absence is visible.

**The gate was verified to fail.** A single trailing newline appended to the published
`data/datum.json` fails it with the divergence named and the source path quoted; restoring the file
passes. A check that has never failed is not a check — the same standard K27 was held to earlier
today.

**What this does NOT do, stated so it is not assumed.** It compares BYTES for copies. It does not
verify that a declared *transform* preserves what the transform is supposed to preserve — that is
per-transform work, and it is exactly what #145 had to do by hand for the terrain. The 293 GLB
derivatives are declared, not checked; **R-W6** already asks whether the same quantiser moves E and
N by up to 153 mm and whether the terrain should ship quantised at all, and nobody has looked.

## FIXED 2026-08-15 — the ground you see IS the ground the town is anchored to now, and neither surface had moved

**R-BUG3c-b**, the half (a) refused to guess at. The 9.6–13.1 cm disagreement (a) measured is real,
and **neither the drawn mesh nor the sampler was wrong**. The gap is introduced *between* them, by
the publish step, after the only gate that measures it.

`generators/terrain_gen.py` ray-casts its decimated ground against the heightfield and refuses to
export past **30 mm**. Its master honours that to **2.5 mm** — as exact as the field it is built
from. The file a browser loads is the derivative `gltf-transform optimize` writes afterwards in
`tools/bake.sh`, and that quantises POSITION to **14 bits under one uniform node scale**. The scale
is set by the widest axis; this mesh is **5,020 m wide** (a 2,020 m box plus 1.5 km of skirt each
side) and **8.6 m tall**, so the vertical rungs are **306 mm** apart. Measured on the shipped bytes:
**rms 85 mm, max 228 mm**.

**No setting fixes it, and that was measured rather than assumed.** 16 bits — the maximum the format
offers — still lands on a 76.6 mm lattice. Only turning compression off meets the tolerance, at
**6.45 MB against 688 KB**.

**The fix is not a fudge and deliberately not `LIFT_M`.** The renderer reads the ground's heights
back off the heightfield as it loads (`conformGroundToField()`), so the surface a visitor sees and
the surface everything is placed on are the same surface by construction. All **124,141** vertices
move, by up to **227.6 mm**; the residual is **0.24 µm**, which is float32 storage.

**Three gates missed this and all three missed it the same way: they compare the render to another
render.** A quantised ground looks perfectly correct. Two gates now hold a measurement instead —
`check.sh` asserts the committed master and reports the derivative, and the smoke asserts the
surface actually DRAWN against the sampler, green at both viewports.

**Unflattering, and worth keeping in view.** This is the third parcel on one owner report. R-BUG3
fixed a real contrast fault and declared the bug closed; the owner reproduced it the same day.
R-BUG3c-a measured the cause and fixed nothing, which is the only reason this fix is the right one
rather than a nudge to `LIFT_M` that would have left buildings, collision and flora still wrong. The
lesson is one line: **do not measure the file you built, measure the file you ship.** Nothing else
in this project measures a published artefact against its own source, and nobody has looked for the
next instance of it.

**Still open, and honestly open:** the same quantiser moves E and N by up to **153 mm** and nothing
corrects that. It is invisible on a decimated prairie as far as anyone has checked — and nobody has
actually checked. That is **R-W6**, along with whether the terrain should ship quantised at all.
## MEASURED 2026-08-15 — the drawn terrain and the heightfield are DIFFERENT DATA, not a decimation

**R-BUG3c-b.** R-BUG3c-a found the drawn ground sitting 9.6–13.1 cm above `terrain.surfaceHeight()`
at the owner's pose. This asks which of the two moved, by testing the drawn mesh's **own vertices**
against the sampler — 5,962 vertices across 30 terrain meshes, water excluded.

Three outcomes were possible and they are mutually exclusive. Near-zero everywhere would mean the
mesh IS the heightfield, decimated, and the burial is an interpolation artefact of coarse triangles.
A constant offset would mean a datum shift. Random would mean different data.

| | |
|---|---|
| min / max | **−3.077 m / +2.744 m** |
| 5th / 95th percentile | −2.465 / +1.519 |
| median | +0.026 |
| mean ± sd | +0.087 ± **1.036** |
| vertices within 5 mm | **182 of 5,962 (3.1 %)** |

**It is the third outcome.** The spread is METRES, not centimetres, so this is not coarse-triangle
interpolation; and the standard deviation is 1.04 m against a mean of 0.09 m, so it is not a datum
shift either. **The baked terrain GLB and `heightfield.bin` are different surfaces**, roughly
co-located — the median is 26 mm — and locally disagreeing by up to three metres.

**The 13 cm at the owner's pose was the local value of a much larger disagreement.** Everything
anchored to the sampler — roads, flora, buildings, collision — is placed against a surface that
differs from the drawn one by up to 3 m somewhere in the scene.

**Still not established, and this is now the whole question: which one is authoritative.** One of
these was generated from a terrain spec the other no longer matches, or one is stale. Until that is
settled nothing should be moved: raising `LIFT_M`, re-baking, or regenerating the heightfield could
each be the change that destroys the correct surface. The next step is to re-derive both from the
committed terrain spec and see which reproduces.

## New 2026-08-15 — the second business-front block, and the second roof each trade was refused

**T-A9.** `blk_south_water_wells` — South Water, LaSalle, Lake, Wells — now carries **eight
anonymous roofs**, six principal and two yard buildings, on six of its seven free lots, with lot 1
(the Lake-and-Wells corner) left open and lot 6 held by Rufus Brown's boarding house. **Standing
roofs 273 → 281; remaining 392 → 384, 46 of them on covered ground** (was 54). Inferred households
86 → 88, inferred persons 98 → 100. Recorded in L100. **The recipe cleared every placement gate on
its first run and no tool changed** — the second block in a row to do so, which is what T-A8 said a
block parcel should now look like.

**THE FINDING IS THAT RULE 6 DOES NOT SAY WHAT IT WAS ASSUMED TO SAY, AND IT IS OPENED AS K28.**
Read literally, **four** of this block's six dwellings pass all three adoption tests for one trade
or the other — the D3 *and the D4* for carpenters (one carpenter household stands in a D4, in the
North Division), the D1 *and the D2* for labourers (four stand in D2s). The rule is silent on how
many roofs of one block a single trade may take, because no block before this one dealt a trade two
of its families. One adoption per trade was taken and the other two refused, on the reading that
rule 6's own opening sentence — the mix is a claim about the town, not about what has been drawn —
forbids one block's deal from raising a trade's count twice. **That is a choice and is recorded as
one**, in both census arguments and in L100, so the next parcel meets an argument it can disagree
with rather than a precedent it has to guess at. K28 is raised to make it code.

**Three documented stores on this block stand INSIDE the platted South Water corridor** — Jones's
grocery by **4.5 m**, Philo Carpenter's store by **6.6 m**, Peck's store by **8.2 m**; two of the
three lap no lot of the block at all. T-A7 established that pre-plat records can stand "a metre or
two proud" of their frontage and measured what that does to occupancy; the intrusion itself had
never been measured. It cost this parcel nothing — the nearest invented roof to any of the three is
**7.99 m** against a 3 m gate — so it is opened as **K30** rather than touched inside a block
parcel. Three named buildings are drawn standing in a street, and either the street, the positions
or 1835 South Water Street is what is wrong.

**L99's commercial-frontage parcel did not exist.** That entry says the question was opened as a
ROADMAP parcel; the ID it names was already carrying the confidence-band parcel, so there has been
a liberty with no work item behind it. It is opened properly as **K29**, and this block is its
second instance: the programme dealt a log cabin and a plank shanty to the town's busiest
commercial frontage for the second time running, and three South Water blocks are still open.

**A fourth measurement of K20:** inserting two households renamed **19 of the 98 carried-over
invented persons**, against 32-of-96 at T-A8, 25-of-94 at T-A2h and 17-of-33-touched at T-A5. No
grade moved and every `name_basis` kept its pool citation, so this is churn rather than a
provenance failure — for the fourth block in a row.

## Fixed 2026-08-15 — the changelog's merge driver was corrupting the file, silently, every time

**K27.** `.gitattributes` merged `js/changelog.js` with `merge=union` so that two branches each
shipping an entry would not conflict. The stated hazard was "two branches editing the same existing
entry", called rare; the everyday prepend was called safe. **That is backwards.**

Union is a LINE union and a changelog entry is not a line. When both sides prepend, the shared
closing `    ] },` is common context and survives **once** — so the first entry swallows the second
and the literal is left with an unclosed bracket. The result is still valid JavaScript, so
`node --check` passes it and nothing downstream notices.

**Measured: five consecutive merges in one day** (#126, #132, #136, #139 and R-BUG4) each produced
exactly this corruption and each needed the same manual repair — rebuild from the base copy and
re-stamp. Union did not prevent a single conflict. It converted five loud conflicts into five silent
corruptions that had to be repaired by hand regardless.

The changelog merges normally now. Two branches that both ship an entry conflict, loudly, at the
merge, and the resolution is the obvious one: keep both, newest first, re-run
`tools/stamp-changelog.mjs`.

**And a claim in that comment needed correcting, though not the way I first wrote it.** The comment
said "the contract check catches that — versions must be strictly decreasing". I recorded that as
never written. **That was wrong: the rule exists in `check-changelog.mjs` and always has.** What it
cannot do is report — it sits after the module load, and the shape walk above it exits the moment a
bracket is unbalanced. The merge that duplicates a version is the same merge that breaks the shape,
so every run died on the shape first and the duplicate was never named; the hand repair then rebuilt
the file from a base copy and took the duplicate with it. A correct check, unreachable in precisely
the case it was written for.

The version rule is now enforced in the **text scan** as well, which runs before that exit, so a
duplicate is named even when the literal will not load — and gaps in the numbering are reported too,
because a gap means an entry was dropped in a merge. Verified to fail on an injected duplicate
before being committed.

**The same `merge=union` line and the same exposure exist in the other fleet apps** (polecat-platform
docs/SHELL-API.md § the fleet changelog contract). This repo is fixed; the fleet is not.

## MEASURED 2026-08-15 — the ground you see is not the ground the town is anchored to

**R-BUG3c-a.** The owner reproduced the invisible near-field road with the R-BUG3 fix in. The cause
is now measured, and it is not the streets at all.

At the reported pose, the DRAWN ground sits **9.6 to 13.1 cm above `terrain.surfaceHeight()`**, the
sampler that roads, plants, buildings and collision are all placed with — over the whole hundred
metres, not just near the camera. `LIFT_M`, the road's lift above that sampler, is **22 mm**. The
roadway is under the visible ground along its entire length here, and so is anything else rooted by
the same sampler, which is why the grass tufts disappear with it.

**Why the road still shows beyond about seven metres:** the polygon offset wins at range and loses
up close, because depth-buffer resolution is finest near the camera. The crossover is a function of
distance alone — which is why the boundary is a clean horizontal line at a constant radius, the one
feature of the owner's screenshots that no other explanation accounted for.

**A visitor stands 13 cm sunk into the terrain they can see.** Eye at 2.455 over a sampler reading
0.775 is the recorded 1.68 m of eye height; the drawn ground under that same point is 0.906.

**What is NOT established: which of the two is wrong.** The drawn surface is a baked GLB, the
sampler reads `heightfield.bin`, both descend from the same terrain spec, and this measurement says
only that they disagree. Raising `LIFT_M` would hide a datum disagreement behind a fudge and leave
buildings and collision wrong. Landed as a measurement, red, with no fix — which is what the parcel
asked for and what saved R-BUG2 from a fix that would have made things worse.

## New 2026-08-15 — five invented houses on the town's business front, and the share-out that put them there

**T-A8**, and it is the first block parcel since T-A5 that actually built a block: T-A6 and T-A7
each set out to fill one in and finished up repairing the arithmetic that decides what a block may
be dealt. `blk_south_water_franklin` — South Water, Wells, Lake, Franklin — now carries **seven
anonymous roofs**, five principal and two yard buildings, on five of its six free lots, with lot 1
(the Lake-and-Franklin corner) left open. **Standing roofs 266 → 273; remaining 399 → 392, 54 of
them on covered ground** (was 61). Inferred households 84 → 86, inferred persons 96 → 98; totals
158 households and 194 people. Recorded in L99.

**The recipe cleared every placement gate on its first run and no tool changed**, which is the
shape T-A2 predicted these would settle into and which T-A6 and T-A7 both interrupted.

**THE FINDING IS ABOUT THE SHARE-OUT, NOT ABOUT THIS BLOCK, AND IT IS OPENED AS K25.** This is the
first block this lane has filled on South Water Street — the town's business front, where every
documented roof on or beside the block is commercial: the Temple Building, the Exchange Coffee
House, J. H. Kinzie's forwarding store, Newberry & Dole's warehouse west and H. Jones's store east.
The 665-roof programme dealt it **five ordinary dwellings, one of them a D2 plank shanty**, because
`tools/reconcile_665.py` apportions families by DISTRICT and has no notion of what a street was
for. The block was built as dealt — the apportionment is the programme's claim and overriding it by
hand on the day it produces an awkward result is how a reconstruction becomes a picture somebody
liked — but the defect is now written down in three places rather than absorbed silently, and it
will recur on `blk_south_water_wells`, `blk_south_water_lasalle`, `blk_south_water_clark`,
`blk_south_water_dearborn` and `blk_lake_market`: **six of the ten open blocks front a commercial
street.**

**T-A7's second test is vindicated by measurement, which is what this block was in a position to
do.** T-A7 left lot 2 schedulable because Kinzie's store laps it only inside the 1.5 m margin
strip. If that had been too generous, this parcel is where it would have failed. It did not: the
lot 2 roof stands **7.3 m** from Kinzie's store against a 3.0 m separation gate, and every other
roof this parcel places is further from its own nearest neighbour than that.

**Both adoptable trades passed rule 6 on one block, for the first time since the rule took its
third test.** Exactly two trades' committed arguments call their own counts a floor — carpenter and
labourer — and this block was dealt a D3 and a D1 in the South Division, which is precisely the
family each is already housed in there. Both were adopted (13th carpenter, 15th labourer). Adopting
only one, as every parcel before this did, would have been a preference rather than the rule
choosing.

**K20 measured a third time, and it is the worst reading yet.** Inserting two households renamed
**28 of the 84 carried-over inferred households and 32 of the 96 carried-over invented persons** —
a third of the layer — against 25-of-94 at T-A2h and 17-of-33-touched at T-A5. No grade moved, no
`name_basis` lost its pool citation, and `check.sh` re-derives all 98, so this is churn rather than
a provenance failure. K20's own text says the fix belongs in its own parcel; it has now ridden
along with a block three times, and it is the reason this PR's diff is 47 files wide for a change
whose real content is seven buildings.

**AND IT DOES NOT SHIP. THE DESKTOP DRAW-CALL BUDGET IS EXCEEDED AND THIS PARCEL IS WHAT EXCEEDED
IT.** `tools/check.sh` is green. The mobile viewport is green — 419 assertions, zero page errors.
The desktop viewport fails four assertions for one reason. Measured on the published mirror at
1280×800, both runs full and in the foreground:

| | draw calls | budget | verdict |
|---|---|---|---|
| `dev@52641c4` (baseline) | **75** | 80 | pass |
| this branch, +7 roofs | **84** | 80 | **fail**, and the three per-tier detail ceilings with it |

**Seven roofs cost nine draw calls.** R-G1 projected +11 per 19 records; the observed rate here is
steeper, and it was spent against five calls of headroom. This is **R-W5a**, arriving earlier than
its own straight line predicted, and the operational consequence is blunt: **lane 2 cannot land
another block until R-W5a lands.** Nine open blocks remain and not one of them is smaller than the
one that broke it.

**Three things were NOT done to make it green**, listed because each is a tempting shortcut. The
budget was not raised — an assertion moved to admit what it was measuring is not a gate. Roofs were
not dropped — the schedule deals seven, and building five to satisfy a frame rate is fitting the
town to the renderer. R-W5a was not fixed in this run — it is a lane 1 parcel with a lane 1 PR
already in flight, and batching the scene is a unit of its own.

**One renderer-adjacent fix IS in this branch, because the parcel could not be diagnosed without
it.** `tools/smoke_renderer.mjs` filtered terrain problems with `/terrain|water/i` against the
whole message, so `blk_south_water_franklin` — the first block whose id contains the word — turned
two ordinary placeholder-asset notes into a reported terrain load failure. Anchored to
`/^\s*(terrain|water)\b/i`, which is what the code's own comment always claimed, and verified
against real `terrain <epoch>: …` and `water: …` messages in both directions. Five of the ten open
blocks are `blk_south_water_*`.

**What this parcel did NOT do.** It did not re-apportion the schedule (K25), it did not fix the
name allocator (K20), it did not fix the draw-call budget (R-W5a), and it did not answer whether
one open lot per block is the right vacancy — the question T-A6 left standing and nothing here
touches.
## Fixed 2026-08-15 — a wet corner was deleting whole panels of road, dry half included

**R-BUG4**, owner-reported from South Water Street as a clean-edged green quadrilateral punched
through the roadway. `streets.js` dropped a panel outright when the centreline **or any of its four
corners** fell on water. The comment said the edge test kept a bank road from painting over water
where its legal corridor reached it — the right aim and the wrong instrument, because deleting the
panel takes the dry half with it.

It clips at the waterline now, each end trimmed on each side independently by bisection out from
the dry centreline. Asymmetric on purpose: a bank road is wet on one side only, and shrinking it
symmetrically would throw the dry verge away as well. The centreline test is unchanged — a road
whose centre is in the river is a crossing, and a crossing is a bridge's job.

**Measured on the built geometry:** 4,843 panels have a dry centreline, **all 4,843 now reach the
ribbon**, 28 clipped at the waterline, 0 dropped as sub-metre slivers, **62.7 m of roadway
recovered**. The `13 quads / ~30 m` first recorded for this bug was read off a truncated probe
listing and was **half the true figure**; a sorted table read from its tail is not a total, and the
number in the roadmap and changelog is now the measured one.

The gate asserts the invariant rather than the number — every panel with a dry centreline reaches
the ribbon, the only permitted absences being sub-metre slivers, which are counted and printed —
and it asserts that clipping actually happens, so a later simplification back to deleting the panel
fails in CI rather than in a screenshot.

## REOPENED 2026-08-15 — the owner reproduced the invisible road WITH the fix in, and it is not the streets

Reported again the same evening, mobile, Lake Street approaching Franklin — after the entry below
declared it solved. Reproduced at that exact pose. **Forced fully opaque, depth-writing, at the
marker pass's own polygon offset, the ribbon still reaches only row 937 of 1560: the bottom 40 %
of the frame holds no roadway at any opacity.** And it is not a streets fault — per-row detail
energy falls from 1.0-2.4 above row 1000 to 0.2 below row 1120, so the road, the grass tufts and
the ground texture all vanish together at one radius. The geometry is present (32 street vertices
within 10 m); something is burying it. Recorded as **R-BUG3c**, top of the rendering queue, with
the untested hypothesis named and the instruction to measure the drawn terrain against
`terrain.surfaceHeight()` before changing anything.

**The gate went green because its new station stands AT a crossing** — one of the few places the
near ground is intact — and the owner was 172 ft short of one. Third time on this bug that the
answer was where the gate was pointed, and the parcel that wrote that lesson down repeated it.

A second, separate fault came out of the same reports (**R-BUG4**): `addRecord` drops a whole road
quad when ANY of its four corners is water, dry half included. **13 quads / ~30 m of roadway
deleted while the centreline is dry land**; Kinzie loses 14.2 % of itself. Clip at the waterline,
do not discard.

## New 2026-08-15 — the horizon-timber figure was scoring the town's roofs, and the fix for it is subtraction rather than a colour test

**R-W4a.** RENDERING § 5 asks for **≥ 90 %** horizon-timber column coverage. The number answering
that question counted **any** break in the skyline above the land/sky line, and a gable end breaks
a skyline as surely as an oak — R-G1 caught `prairie_south` moving 0.364 → 0.436 on nineteen new
roofs with no renderer change. **Corrected, `prairie_south` reads 0.295 desktop where it read
0.632, and 62 % of what was counted as timber there was the town** (409 of 1053 measured columns
broke on a roof and on nothing else). Across the 22 station-viewports the mean falls **0.672 →
0.582**, and the number meeting the target falls **1 → 0**. Full table in `docs/ROADMAP.md`
§ R-W4a.

**The discriminator this project had written down does not work, and that was measured rather
than argued.** R-G1 proposed the crown-hue channel — "a whitewashed gable is not green". At the
first hit pixel of every broken column, desktop: grey gables at `prairie_south` sit at ΔG−B
**+22.4**, hazed timber at `prairie_west` ranges **+0.1 to +17.5**. The two populations overlap
completely, because the horizon sky is strongly blue-dominant and every non-sky pixel clears a +3
G−B test — the channel was a not-sky detector, so the old figure was testing the same condition
twice. **No colour test can separate them in principle here**: L17 makes extinction total by
1500 m, so distant timber and a distant wall both converge on the fog colour.

**What replaced it takes the town away instead of guessing.** The harness photographs each
station twice from the identical pose — once as the visitor sees it, once with the `structures`
group hidden — and measures the horizon in the second frame. Timber by construction: no
threshold, no hue, nothing to tune, and **the figure cannot move when a block lands**. The old
number is kept at its old value under a name that says what it counts (skyline breaks), so
2026-08-14's baseline is still comparable and no past figure was silently redefined.

**Two properties of the new figure that must be quoted with it.** It rises at six of the
22 station-viewports, because a building can stand in front of timber and hide it — it answers
*is the horizon timbered*, not *can the visitor see timber past the town*, which is the right
question for a target derived from photographs of a treeline. And `from_above` is an aerial pose
whose band is not a horizon at all (0.212 / 0.156, town share 0 %): do not average it in without
saying so.

**Unverified / not claimed:** nothing about the renderer changed, so no scene claim moves with
this. The cost of the second capture is measured (13 min 12 s for the full both-viewport run,
against ~12 min without it) and `--no-mask` opts out. Putting the town back was checked rather
than assumed: 5, 9 and 51 differing pixels of 1,024,000 across the change, inside the harness's
own cross-process residual, with the `--stability` contract passing byte-identical.

## Partly fixed 2026-08-15 — the road at a crossing, the two stations that never stood on one, and a gate that abstained exactly when it should have shouted

## New 2026-08-15 — the road gate can now see contrast as well as lightness, and the photograph it was told to calibrate against has no road in it

**R-M1a.** The owner ruled on 2026-08-14 that the road gate should score exposure-invariant
**contrast** and keep an absolute **floor** — both bars, not a replacement — after R-W1
legitimately changed the scene's exposure, preserved the road/ground ratio to within 0.4 %, and
lost a gate it had not regressed. Both numbers are now measured at every road band, at both
viewports. **Neither is gated**, and that split is deliberate: the parcel's own acceptance names
three builds to smoke and the lane allows a parcel two, so it was split into *land the
measurement* and *set the bars* before it was claimed. A gate that moves at the same moment as
its own baseline has no baseline.

**The measurement is verified against a number this project committed before the code to compute
it existed.** R-W1's parked working recorded Weber **0.1217** at `from_above`, desktop,
100–250 m, taken by hand at the point of use on `dev@d762a19`. `weberContrast()` reads **0.1217
at n 11** against R-W1's n=11, eleven commits later. The 250–600 m band moved 0.0940 → 0.0999
(+6.3 %) with ΔL\* 2.36 → 2.4 in step, which is R-BUG3's alpha-and-opaque work reaching a band
R-BUG3 predicted it would leave untouched — small, real, and R-M1b's to explain.

**The finding that matters more than the baseline: Weber has no ceiling as its background goes
dark, and one band already demonstrates it.** `lake_market`, desktop, 100–250 m reads
**`weber 8.8023` over a ground of `L* 3.0`**, where the same band on mobile reads 0.1339 over
L\* 53.5. Nothing is wrong with the road there — ΔL\* is 18.0 at 100 % perceptible. The road's
projected probes on that viewport simply land against something almost black, and a ratio whose
denominator is the light in the background is unbounded when the background has none. **A median
Weber over a band can therefore be set by its darkest probes rather than by its roads.** That is
the precise failure the owner's ruling anticipated by pairing the ratio with a floor instead of
swapping one bar for the other, and it is the number the bars would have been fitted against had
they been set in the same change as the baseline.

**And R-M1's threshold source does not exist.** The parcel says to derive the bars by measuring
"what contrast a real dirt track holds against real prairie" in the R-REF1 photograph.
**There is no dirt track in that photograph.** `tools/measure_reference.py` now surveys the land
region and prints it: the widest contiguous bare-earth run anywhere below the horizon is
**332 px = 8.2 % of the frame width, at −38.2°** — the bottom edge of the frame, at the
photographer's own feet, and it is dry stems and litter between plants rather than a surface. The
widest run with no green excess at all is 11.1 % at −0.4°, which is the hazed treeline and is not
ground. The soil-like *fraction* is 3 % over the whole land region and rises to 18.5 % in the
bottom 5°, which is exactly why a fraction cannot decide this and a run length can: a track
crossing that frame would be contiguous across a large part of its width at some elevation, and
nothing in it is.

This is the second time this project has been handed a target that its own reference cannot
supply. The first is recorded above under the 2026-08-10 prairie sweep — a horizon-timber brief
specifying "Weber 0.036–0.067", of which STATUS says it *"does not exist in the reference at any
threshold — that error was the brief's, not the builder's."* Nothing R-REF1 actually landed is
weakened by this: all four sky readings, the horizon band and the canopy contrast still
reproduce, and they are what `world.js` and `trees.js` quote. **R-M1b is therefore blocked on a
threshold source, not on effort**, and the three honest options — a second cited photograph that
does show a track, a cited published detection threshold labelled as a claim about eyes rather
than roads, or R-M1a's own baseline frozen and labelled provisional — are written out in
`docs/ROADMAP.md` § R-M1b for the owner to choose between. Do not pick a number and call it
derived.

## Fixed 2026-08-15 — the town was paying a draw call per colour of paint, and the next 399 roofs now cost none

**R-W5a.** The draw-call budget was the one thing both overnight lanes were waiting on: R-G1
measured **+11 draw calls for 19 new roofs**, straight-lining to about **+240 against a budget of
80** over the 399 roofs still to come, and it had already parked a block of houses (T-A8, PR #132).
It is not a growth problem any more. It is **zero**.

**The cause, and it was hiding in plain sight.** `buildings.js` sorts the town into one
`BatchedMesh` per distinct material, and the key included the base colour. Every one of the 47
batches was the same `MeshStandardMaterial` in every respect a renderer distinguishes — metalness
0, **no map of any kind**, `DoubleSide`, opaque, `alphaTest` 0, smooth-shaded. The only fields that
differed were `color`, with **39 distinct values across 47 batches**, and `roughness`, with 16. The
town was spending forty-seven draw calls to render two numbers, and buying another one every time a
block landed carrying a paint nothing else in town used. **R-G1's "+11" was 11 new material
GROUPS, not 11 objects** — which is precisely why it was uniform at bearings 150° apart: the cost
counts paints in frame, not buildings.

**The fix carries colour per vertex and is arithmetically identical, which is the only reason it is
allowed here.** `material.color` is already in the renderer's linear working space; three's
`<color_fragment>` multiplies `diffuseColor.rgb` by the `color` attribute with no colour-space
conversion of its own; and the confidence view's tint was already applied *after* that chunk. So
the shader does the same product in a different order, and a documented white wall still renders at
the value its record claims, to the bit. Roughness is additionally compared at three decimals,
which merges the bespoke masters' float32 `0.8999999761581421` with the generated infill's `0.9`.

**`tools/critic_shots.mjs`, source tree, both viewports, before and after on the same `dev`:**

| draw calls | `sauganash` | `s'nash_wing` | `lake_market` | `f_post_office` | `forks` | `green_tree` | `south_water` | `from_above` | `prairie_south` | `prairie_west` | `river_bank` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop before | 75 | 78 | 90 | 66 | 98 | 103 | 96 | 72 | 95 | **109** | 56 |
| desktop after | 56 | 58 | 60 | 57 | 68 | 70 | 66 | 59 | 62 | **75** | 52 |
| mobile before | 72 | 74 | 78 | 60 | 82 | 99 | 94 | 72 | 93 | **106** | 49 |
| mobile after | 54 | 55 | 58 | 51 | 64 | 68 | 64 | 59 | 61 | **73** | 47 |

**Batches 47 → 16; station-viewports over the ≤ 80 budget 11 of 22 → 0 of 22.** A new roof of any
colour now joins an existing batch, so T-A8 and the 399 roofs behind it cost nothing.

**What it cost, stated in numbers rather than reassurance.** Triangles are **identical to the
triangle at all 22 station-viewports** — nothing was dropped to buy the calls. The frames are *not*
byte-identical: 2 of 22 hash the same, and the rest differ on **0.013 % of pixels**, in 7–195
scattered components whose largest is 56 px, all on building silhouettes — depth ties at coincident
surfaces resolving the other way under a changed draw order. Worst single pixel 93/255;
**whole-frame mean |Δ| 0.003–0.005 of one 8-bit count**. No surface anywhere is repainted.

**What it does not do.** It does not touch the water surface, post-processing or dynamic resolution
(R-W5b, still open, still carrying R-BUG1's river flicker), and it leaves 16 batches where 1 is
reachable — the roughness half needs a shader patch and is written up as **R-W5a2** with its
numbers already measured. The budget is met with 5 calls of headroom at the worst station and the
growth term is zero, so that half buys margin, not a fix.

## Fixed 2026-08-15 — the road at your feet, the two stations that never stood on one, and a gate that abstained exactly when it should have shouted

**R-BUG3, owner-reported on mobile, on the dev preview with R-BUG2's fix already in:** standing on
Franklin Street approaching Randolph, the wheel ruts read in the mid-distance and *"it should not
be invisible when I am standing on it."* True. The near band now scores **3.1 L\* with 80 % of
probes perceptible** on mobile and 3.2 / 60 % on desktop, against **1.5 / 30 %** before, measured
on the published mirror. Every band past 40 m is untouched by the near-field fix.

**The parcel's first move measured nothing, and that is the finding.** It said: add a `[2, 40]`
band, expect it to fail, and that failure is the acceptance. Added, and the band collected **one
probe** at `south_water` and **none** at `from_above` — because **neither gated station stands on
a road**. `south_water` is **101 m from the centreline it is named after** (that is T-V2, now
measured rather than suspected) and 17 m from the nearest one; `from_above` is 175 m up. The window
was wrong in two dimensions, distance and pose, and the failing gate could only show one of them.
There is now a third station: `lake_market`, reached the way a visitor reaches it — by clicking a
verified street-control intersection in the Go to tab — which then turns to look along the
centreline underfoot, a bearing read off the committed path. The arrival pose alone was not enough
either: the shipped jump faces a fixed bearing, which at a crossing points diagonally into the
block and put **zero** road probes inside 100 m.

**The prime suspect is refuted, and no grass was cleared.** The parcel named near-field sward
occlusion as most likely, with an explicit non-licence against widening a clearing corridor to win
a score. The harness now re-shoots its road markers with the sward and the trees hidden, so an
occluded probe is distinguishable from an absent one — and in the near band **all ten probes are
marked either way**. Nothing is hiding the road. `flora.js` is untouched, no recorded ground cover
moved, and the non-licence never had to be tested. Every band now reports the discrimination
(`seen N of M projected, K clear of flora`), because telling occlusion from flatness is the
distinction three gates in a row failed to draw.

**The fault, stated more precisely than "the alpha is too low".** An alpha here is a **coverage
fraction** — what share of the ground is bare earth rather than grass — and that is the right
picture of a mixture only where one pixel spans many patches of it. At a walker's feet one pixel
spans one patch, which in life is either earth or grass, and the blend paints a uniform wash of
grass-with-a-hint-of-dirt instead. The harness measures both ends of it: the same near probes with
the ribbon forced **fully opaque** score **3.4 L\***, so the contrast was sitting in the ribbon's
own colour and the shipped alpha was spending under half of it. The near field also has less to spend — the
ground underfoot is genuinely darker than at range, **L\* 51.0 against 52.7–56.3**. The fix scales
alpha by 2.4 inside 15 m, fading to nothing by 40 m. Recorded as **L98**.

**The durable half is the gating rule.** A band gated on *how many probes were SEEN* gates itself
out at precisely the moment the thing it measures goes wrong: a road nobody can see reports n=0,
which is indistinguishable from a stretch with no road in it, and the check passes by abstention.
Bands are now gated on how many probes were **PROJECTED** — on screen, and therefore owed a
picture. This is the third time this one bug has been a question of what the gate was pointed at,
and the first fix that makes the gate fail loudly rather than quietly decline to answer.

**A second fault, found by the new station and fixed with it.** At desktop, 100–250 m from the
crossing, the ribbon scored **0.0 L\*** while the marker pass was frontmost — R-BUG2's fault 1
again, its polygon offset having been tuned until the bands *at the two stations then gated*
passed. Deepened to the marker pass's own values, that band reads **18.0 L\* at 100 %
perceptible**. And the opaque diagnostic had to be fixed before it could be believed: its first
form let the terrain paint back over the ribbon and reported a 0.0 ceiling under a healthy road.
It writes depth now, as the marker pass always did. A diagnostic that lies quietly is worse than
no diagnostic, and this one lied in the direction of *nothing to see here* — the same direction as
every other instrument in this bug's history.

**What is not fixed.** The near band has the least headroom of any band a walker actually stands
in: its ceiling fully opaque is **3.4 L\* on mobile and 4.3 on desktop**, against 5.9–6.9 at the
same station's 40–100 m and at both aerial bands — and **20 % of near probes on mobile, 40 % on
desktop, cannot clear the perceptibility threshold even at full opacity**. (Not "the lowest of any
band", which an earlier draft of this said: at that station the 600–4000 m band is lower still, and
that is a road at a kilometre rather than one underfoot.) Opacity has nearly run out as an
instrument here. L98 names the honest
successor: a textured coverage, earth and grass resolved as patches at the scale a near pixel can
show, so the eye integrates the recorded fraction rather than the blender pre-mixing it. That
belongs to **R-W2**, where the 1.4 texture score already lives.
## New 2026-08-15 — a refusal nobody could tell apart from an unanswered question

**K21.** Rule 6 of the household programme lets a block roof be adopted by an argued household
only if three tests pass, and the second asks whether the roof's family is one this layer already
houses that trade in. **For four trades that question had no answer at all.** `brickmaker`,
`packer`, `sawyer` and `wheelwright` live exclusively on the 31 roofs this layer *raises* rather
than adopts, and those records named no family in any field a gate could read — eight further
trades were partly in the same position, 17 households in total. T-A5 refused the sawyer adoption
on that silence and said at the time that it could not tell the refusal from an unanswered
question.

**The answer was a transcription, not a decision.** Every one of the 31 buildings was dealt a
crosswalk family by the programme, and every one has always *said* so in prose — the footprint note
reads "a 16 x 22 ft rectangle from the **D3** family band", and each form value cites the same
band. The band was committed in two places and readable in neither. Writing it into
`reconstruction.family` therefore **invents nothing and owes `docs/LIBERTIES.md` nothing**; rule 6
gains no fourth clause, and no trade is granted a pass — a trade whose families are readable can
still fail the test.

| | before | after |
|---|---:|---:|
| census trades resolving rule 6's family test | 25 of 29, four of them not at all | **29 of 29** |
| trade-family pairs the test can compare against | — | **44** |
| households standing on a roof that names no family | 17 | **0** |

**The durable half is the gate.** `tools/generate_inferred_households.py` fails if any roof a
household *lives or works in* names no family in the crosswalk — over both links, because a shop's
family is as much a claim about the town as a cottage's. The test cannot go silent again without a
gate saying so.

**The parcel's own suspicion was refuted.** It flagged `inf_sawyer_dwelling_b` massing as an
`outbuilding` while `_a` masses as a `frame_dwelling`. They differ because **they were dealt
different families**, D3 and D2, and each resolves through its own family's committed archetype —
the record's existence note says so in as many words. The real split is five W4 shops massed two
ways, all of them one-storey, which W4's own licence does not explain.

**And underneath that, the finding worth more than the parcel.** Reading each committed form value
against its family's band shows **54 of 193 reconstructed roofs sit outside the band their own note
cites** — 39 of 162 anonymous, 15 of 31 bespoke, worst `inf_laundry_north` at 280 sq ft against an
A5 band of 48–192. The cause is that the form generators choose values by **archetype** and attach
a note citing the **family**. A note that cites a band is the defence for the invention; where the
value is outside it the note is wrong about its own source. That is **K25**, split so the
measurement lands before anything moves.

**Two gates caught what reading would not have.** `reconcile_665.py` classified roofs by whether a
reconstruction block was *present*, so all 31 silently moved from `inferred_household_programme` to
`generated` — totals unchanged, attribution wrong. And `compile_scene.py` sent every
reconstruction-block record to the anonymous-infill dossier; the household layer has its own and now
points at it. Which surfaced **K26**: `publish.sh` deliberately keeps `docs/` out of the payload, so
on the deployed site **all 276 building cards link to a 404**.

## New 2026-08-15 — the photograph the sky is calibrated against is now in the repository, and it checks out

**R-REF1.** `renderers/web/js/world.js` derives its sky exposure, the whole of its
horizon-restore fit and the colour distance converges on from readings taken off one
photograph, quoted in the comments as `bar/dupage_tallgrass_2018-07-24.jpg`. **That file was
in no checkout.** `git ls-files` returned nothing for it on 2026-08-14, which made every sky
number in the renderer a quotation that could be read and not checked — and it was blocking
two parcels, R-W1 (whose targets §5 asks to be re-anchored by measuring a reference through
this code) and R-M1 (whose road-contrast thresholds are supposed to be derived from what a
real dirt track holds against real prairie, rather than picked to fit today's build).

**It is committed, and it is the right file.** Cassi Saari, *Restored tallgrass prairie in
DuPage County, Illinois*, 24 July 2018, Wikimedia Commons, at
`data/sources/assets/saari_2018_dupage_tallgrass/dupage_tallgrass_2018-07-24.jpg` with source
record `saari_2018_dupage_tallgrass`. Identification did not rest on the filename: the
Commons description is *"Prairie planting on former agricultural field in DuPage County"* —
the same restoration-not-remnant finding the 2026-08-10 sweep made about this photograph —
and the file's own EXIF says Samsung SM-G930V, **2018-07-24 09:32:25**, 26 mm equivalent,
orientation upright.

**The proof is that the numbers come back out of it.** `python3 tools/measure_reference.py`,
new with this parcel, re-measures the readings `world.js` quotes:

| reading | quoted in `world.js` | re-measured 2026-08-15 |
|---|---|---|
| 12 px above the sky/land step (the `HORIZON_RESTORE` fit target and the haze colour) | (136,163,192) | **(137,162,187)** |
| sky at ~14.4° above the horizon | (101,153,209) | **(97,151,208)** |
| sky at 8° | (125,165,205) | **(119,163,206)** |
| sky at 4° | (137,166,200) | **(133,166,201)** |

Nothing in the renderer was touched to make these agree, and the residual — a few units in
red and blue — is the one the code predicts: the tool averages the full frame width, the
original readings were taken at the shot's own view azimuth, and `world.js` records that the
model's horizon *brightness* is azimuth-dependent even where its hue is not.

**A second confirmation arrived unasked.** The 26 mm equivalent gives 57.0 px/deg vertically
and the sky/land step sits at row 820 of 3024, which puts the camera pitch at **−12.1°**. The
2026-08-10 prairie sweep had already established, from an entirely different direction, that
"the reference photographer had tilted down ~12°" — a correction that invalidated two rounds
of tuning at the time. Two derivations of the same number that never saw each other. The
useful form of it is that the frame is now **solved**: `elevation(row) = (820 − row) / 57.0`
degrees, reaching 14.4° above the horizon and 38.7° below. Any reading taken from this
photograph can now state the elevation it was taken at, which is what both of this project's
reference disagreements turned out to be about.

**The rights are recorded rather than assumed, and they are not permissive.** CC BY-SA 4.0,
attribution required. The file is committed **byte-for-byte unmodified** — SHA-1
`0da00f1178e7790b04c05364d78f7cb6a43992ae`, checked against the SHA-1 the Commons API reports
for the file page — so what this repository redistributes is the licensed work and not an
adaptation, and ShareAlike is not triggered by its presence. **Deriving from it would trigger
it**: a crop, a resample, a texture or a LUT is an adaptation that CC BY-SA 4.0 requires be
released under CC BY-SA 4.0. The project derives nothing from it (it is measured, never
sampled), `tools/publish.sh` does not copy `data/sources/`, and `assets/LICENSES.md` now
carries the clearance as an explicit, reasoned exception to its CC0/CC-BY-only default.

**One figure did not reproduce, and is left standing as a question rather than closed.**
`world.js` gives the bar's most distant land as (118,146,145); the 12 px immediately below the
step measure (106,130,140), because a naive band on that row lands partly on the far treeline
rather than on open sward. The original reading states no recipe, so this is a recipe
mismatch, not a contradiction — whoever needs that number next should define where it comes
from before quoting it.

**What this parcel did NOT do:** change a single rendered pixel. No renderer file was touched,
no threshold moved, no target re-anchored. R-W1 and R-M1 own those, and both are now unblocked.

## New 2026-08-15 — a lot was called free because a building's centroid was in the road

**T-A7.** T-A6 (below) made a block's room a function of its free lots. This is about how a lot
was known to be free: *no committed footprint has its centroid inside it*. The centroid is a
proxy for the building, and it fails on exactly the records the plat grid was built to correct —
a building placed from typed coordinates before the plat module existed can stand a metre or two
proud of its own street frontage, which puts its centroid in the ROADWAY and therefore in no lot
of any block. **Fourteen committed records were in that position.** Measured at `dev@968e389`:

| the building | block | lot | of itself on that lot | in the buildable part |
|---|---|---|---|---|
| **Temple Building** | `blk_south_water_franklin` | 0 | 18.6 m², 27 % | 4.2 m² |
| **Harmon & Loomis's store** | `blk_south_water_clark` | 0 | 29.2 m², 31 % | 9.5 m² |
| **Chicago Democrat office** | `blk_south_water_lasalle` | 6 | 31.2 m², 34 % | 11.4 m² |
| **Cook County courthouse** | `blk_randolph_lasalle` | 6 | 5.1 m², 13 % | 0.4 m² |
| `recon_1835_south_d5_034` | `blk_lake_dearborn` | 3 | 25.5 m², 36 % | 15.1 m² |

Four of the five are named, documented buildings, and the schedule was offering their lots to
anonymous invented roofs. **The claimed block is the sharpest case**: `blk_south_water_franklin`
was dealt six principal roofs for what it called seven free lots, and the Temple Building is on
one of them.

**The rule now has two tests, and each answers a different way of being wrong.** They live in
`tools/plat_occupancy.py`, which is the ONLY implementation — `tools/reconcile_665.py` and
`tools/generate_block_infill.py` both import it, where T-A6 had left them with a copy each.

1. **A building stands on the lot most of it is on**, by measured area. The same claim the
   centroid made, made about the building instead of about a point inside it. On the committed
   dataset it is purely additive: **no record changes lot**, occupied lots go 79 → 84, and
   nothing that read taken became free.
2. **It occupies that lot only where it reaches the lot's buildable part** — the lot inset by
   the 1.5 m every new roof must keep from its own lot lines. **J. H. Kinzie's store earns this
   test**: 9.7 m² of it lies on `blk_south_water_franklin` lot 2 and *none* inside the buildable
   inset, so a roof still fits there clear of it and the schedule may still deal one. Without
   test two the town would lose roofs it can honestly have.

**The ledger had the same defect from the other side.** A roof was attributed to a block by its
position POINT, so three buildings whose point is in the roadway were counted as standing in no
block at all: the **Exchange Coffee House** (which holds nine tenths of a lot of the claimed
block), **Harmon & Loomis's store** and the **Tremont House**. Their roofs were never subtracted
from the headroom of the block they physically stand in. A roof standing on a block's lot stands
in that block.

**What it cost.** Schedulable-on-covered-ground **66 → 61**; gated on coverage **333 → 338**.
Standing roofs are unchanged at 266, remaining at 399 — nothing was built or removed. Four blocks
lose a free lot each and `blk_south_water_clark` also gains two standing roofs, so its deal drops
from 7 to 5.

**What it measured and deliberately did not call occupancy.** `recon_1835_west_018` laps 11.9 m²
onto `blk_randolph_clinton` lot 2, where T-A4 stands a principal roof. Test one seats it on lot 4,
where 82 % of it is, so that placement stands. A rule that called every lap an occupation would
have condemned a committed, gated placement over a corner of a building, and whether two roofs
may stand three metres apart across a conjectural side lot line is the separation gate's question
— which it passed. Recorded here so the silence is not mistaken for nobody having looked.

**What this parcel did NOT do:** build a block. T-A7 claimed `blk_south_water_franklin` and found
it could not be built honestly; it returns to the queue with a corrected deal — 7 roofs, 5
principal and 2 ancillary, on six free lots.

## New 2026-08-15 — half the open blocks were scheduled roofs their own lots could not hold

**T-A6.** The 665-roof schedule counted a block's room in ROOFS and never in LOTS, and a principal
roof needs a free lot. Measured across the ten open blocks at `dev@f6f2bcb`, against the placement
gates in `tools/generate_block_infill.py` that would have refused them:

| block | lots | free | dealt principal | what the recipe would have hit |
|---|---|---|---|---|
| `blk_south_water_clark` | 8 | 6 | **7** | **unwritable** — no seventh free lot exists |
| `blk_lake_market` | 8 | 6 | **7** | **unwritable** — no seventh free lot exists |
| `blk_south_water_wells` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_franklin` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_clark` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_dearborn` | 8 | 3 | **0** (one ancillary) | **unwritable** — a yard building behind no roof |

**Five of the ten, and three distinct failures, not one.** Two blocks were dealt more principal
roofs than they had lots, which no recipe could have written down at all. Three were dealt exactly
as many as they had free, which is writable and *worse*: it silently spends the vacancy the parcel
recipe's own placement rule promises — *"a block at capacity is a claim about 1835 that the
evidence does not support; the schedule's capacity is a ceiling"* — so the first parcel to take one
would have filled a block to capacity while passing every gate. And `blk_randolph_dearborn`, the
T-A3h backfill, was dealt a single yard building and no principal roof to stand it behind: the same
blindness seen from the other end, because an ancillary roof's gate is that it serves a principal
roof the same parcel built.

**Why it was invisible.** Occupancy was counted in roofs — `standing_roofs` — so two roofs on one
lot and two roofs on two lots subtracted the same amount of headroom. The block generator has
derived true lot occupancy since T-A4 and the schedule never did, so the two halves of the same
question were being answered by different arithmetic. Nothing shipped wrong: the gates that would
have caught each of these are real and would have fired. **The defect was that they fire at the
END of a parcel** — after a run has claimed a block, read the schedule and written a recipe.

**The fix is that the deal now knows what a lot is.** `tools/reconcile_665.py` derives lot
occupancy by the *same rule the generator uses* — footprint centroid against the committed lot
polygon — and a block's room becomes `principal = min(free lots − 1, roof headroom)` with
`ancillary` bounded by both the 154:511 ratio and the principals themselves. The deal offers a
token a unit cannot take to the next unit instead of dropping it, so every marginal still closes,
and a new assertion fails the build if any unit is ever dealt past its room.

**What it cost, and the number is the point.** Schedulable-on-covered-ground **71 → 66**; gated on
coverage **328 → 333**. Five roofs moved from "buildable now" to "waiting on coverage" because
they never had anywhere to stand. **All ten open blocks are now buildable and every one of them
keeps a lot open**, which is the state T-A7 onward can be run from without re-deriving this.

**What this parcel did NOT do:** build a block. T-A6 claimed `blk_randolph_franklin` and found it
was one of the three that could not be built honestly; the block is released back to the queue with
a corrected mix (6 principal + 2 ancillary, one lot open) for the next run to take.

## New 2026-08-15 — the card adds its own claims up, and 204 of 279 buildings have nothing attested about them

**K23b**, the substantive half of the owner's report and the sequel to K23a below. Every
provenance card now opens with **`What did we include, and where did it come from?`** — three
rows, one per level, naming the claims that stand at each and saying where they came from.

**It is a partition, which is the whole of why it can be gated.** Every graded claim the card
renders lands in exactly one row, so the release check is a RECOUNT rather than a look: pick
every building at both viewports, tally the confidence chips off the RENDERED card, and require
the section's three numbers to be those numbers. **276 of 276 loaded buildings agree.** The
recount reuses the older chip-coverage gate's own selector on purpose — two definitions of "a
claim on this card" is how a summary would come to disagree with the card while both gates
stayed green.

**The dataset, counted for the first time this way.** 279 records carry **3,675 graded claims —
199 `attested`, 509 `inferred`, 2,967 `reconstructed`.** **204 of the 279 have no attested claim
at all**, so a row that rendered only when it had something would go silent on three quarters of
the town at the exact moment a visitor needs telling. It says *"Nothing about this building is
attested by a source."* instead.

**A citation means a different thing at each level.** `From` on an attested claim; `Bounded by`
on an invented one — 193 anonymous roofs cite the reconstruction spec and Andreas on every
attribute, and one `sources:` label over all three rows would have printed a nineteenth-century
history as attribution for a building nobody claims stood there.

**Two findings that are not the section.**

- **69 buildings have inventions that nothing is recorded as bounding.** Of the 270 records with
  at least one `reconstructed` claim, 69 cite nothing on any of them, so their `Bounded by` line
  reads *"Nothing is cited as bounding these."* The bottom tier requires a note and not a source
  — deliberately — but nobody had ever counted the consequence. The Sauganash Hotel is one of the
  69. Visible now rather than fixed; whether those should acquire a bound is research.
- **Attested is not built, on 14 records.** The Western Hotel's stables are attested by a
  pre-fire account and there is nothing of them in the model. A summary of what was *included*
  that counted them under "attested" and stopped would name something that is not there, so the
  row repeats the mark the table below already carries: *Not in the model: stables*.

## New 2026-08-15 — 193 buildings were named a grade better than their own record, and the release gate was holding it in place

**K23a**, owner-reported from a card on the dev preview. The heading read **"Inferred A1 stable
#07"** and every chip beneath it read **RECONSTRUCTED**. The heading was the wrong one, on
**193 structure records** — every anonymous roof this project has ever generated.

**It is the residue of a fix that worked.** The v76 merge of 2026-08-13 moved 9,076 values onto
`attested / inferred / reconstructed` and re-graded 1,694 that had claimed to be reasoning when
they were invention. It moved the DATA. The PROSE is hardcoded in the generators, and it did not
move — so `inferred` went from being the BOTTOM tier (where "Inferred A1 stable" was honest) to
the MIDDLE one, *reasoned from evidence about this particular thing*, which an anonymous
count-unit is precisely not. **Nothing about any building changed here**: not a position, a
dimension, a source or a grade. Only what the card calls them.

**Scale, exactly, so a later sweep can tell drift from a fresh fault.** 193 names; 162
`symbolic_location` strings; 193 `research_note` openers partitioning cleanly into 142
`RECOMMENDED / GENERATED`, 31 `INFERRED BUILDING` and 20 `INFERRED / GENERATED`; every
`change_note` on an anonymous roof; the card's own reconstruction flag; and the household and
person labels of the K1 layer. **`recommended` is the word this project renamed away from BY NAME
on 2026-08-13** and then printed on 142 cards for a fortnight.

**Five generators, not the two the parcel listed — and a sixth stage that is not a generator.**
`generate_inferred_names.py` runs AFTER the household programme and rewrites the household's own
label. Regenerating households without it deletes every invented resident's name and
`name_basis` — the whole of K18 — and **the household programme's `--check` cannot see this**,
because it overlays the naming pass before comparing. `--check` is green either way. The order is
`generate_inferred_households.py` then `generate_inferred_names.py`, and it is now written into
ROADMAP K23a where the next person will look.

**The gate was enforcing the fault.** `smoke_renderer.mjs` asserted the household label matched
`/inferred/`. So the thing that should have caught this was requiring it. That assertion is
pinned to the head's own `grade` now, and a new whole-registry check fails the release on any
name opening with a grade its record does not carry, or with any of the three retired words —
with the fault planted in the same pass, so a gate scanning a clean tree cannot be mistaken for
a gate scanning nothing.

**Two things outside the app were worse than the cards.** `docs/PROVENANCE.md` — the page you
send someone to when they ask what the grades mean — still defined `documented / inferred /
conjectural`, so a record written by following it **fails the build**. And `validate.py`'s own
errors named the wrong tier: a sourceless `attested` value reported *"documented requires at
least one source_id"*. Both corrected; ROADMAP K16, which proposed a third vocabulary that never
shipped, is **CLOSED as superseded**.

**Still open, and it is the half the owner cared most about.** K23b — *say what was INCLUDED at
each level and where it came from* — is untouched. The names are no longer wrong; the cards still
do not tell a visitor that a building's footprint, height, roof form and position were all
invented and only its block was reasoned.

## New 2026-08-14 — the block where two layers of this reconstruction met on the same ground, and the adoption rule grew a third test

**T-A5.** `blk_randolph_market` — Randolph, Franklin, Washington, Market — is the first South
Division block of the Randolph row and now carries **eight anonymous roofs**: four dwellings, one
per lot on four of the six free lots, and four yard buildings off the block alley. **Standing roofs
258 → 266; remaining 407 → 399, 71 of them on ground the project has coverage for.** Households
**155 → 156**, persons **191 → 192**. Recorded in **L97**. The parcel authors no coordinates: every
metre is read off the committed K7 lot polygons, which is what has made every block since T-A2 a
recipe entry rather than a geometry argument. The recipe cleared every one of the generator's
placement gates on its first run — no lot-line, separation, corridor, relief or occupancy failure
to iterate against — which is what the accumulated gates of T-A2 through T-A4 were for.

**The block was already built on by THIS project's other half.** L95 recorded the first
partly-built block and the roofs in its way came from the pre-plat West Division density recipe.
Here the two standing roofs are `inf_sawyer_dwelling_a` and `_b` — the dwellings of the occupation
census's own two sawyer households, placed from typed local-ENU coordinates before the plat module
existed. The layer that argues who the town held and the layer that fills its blocks have now
collided, and the T-A4 machinery absorbed it without a change: occupancy derived from the committed
footprints, lots 4 and 6 refused a second principal roof, headroom spent on the six free lots.

**Where the vacancy falls was decided by arithmetic, and the parcel says so rather than dressing it
up.** Both standing roofs sit on the Randolph face, so the two lots free there are exactly the two
the frontage-value typology wants for the better cottages, and the programme's alternating vacancy
has nowhere to fall but Washington. Had the schedule dealt one roof fewer the pattern would have
read as deliberate. `arrangement_note` and L97 both state it.

### The third adoption test — the question T-A4 left open, settled

T-A2h's rule 6 had **two** tests: the trade's committed argument must call its count a floor, and
the roof's family must be one this layer already houses that trade in. T-A4 met a case neither
covered — a D3 carpenter roof on the first West Division block, when all eleven carpenter
households stood north or south — and refused it **by hand**, leaving the question to T-A5.

**Rule 6 now has three tests**, the third being the roof's **division**. It is the family test made
about the other axis of the same table: where a trade lived is as much a claim about the town as
what it lived in. **It was checked against every adoption decision taken before it and recovers all
four** — T-A2h's carpenter adopted, T-A2h's labourer adopted, T-A4's labourer adopted, T-A4's
carpenter refused. A test that had to be told those answers would be a preference; one that
recovers them is a rule. This block's D3 on lot 7 passes all three, so a twelfth carpenter household
is inferred (carpenter 11 → 12) and the other seven roofs stay anonymous count-units.

### What the test cannot answer, and it is not about the trades — **K21**

The sawyers whose two roofs stand on this very block **pass test 1** — their argument reads "two
sawyer households are inferred, **the smallest number that answers the demand**" — and fail test 2
for a reason that has nothing to do with sawyers: their dwellings are bespoke
`inf_sawyer_dwelling_*` records carrying no `reconstruction.family` at all, so the question "which
family does this layer house that trade in" has nothing to read. **Four trades of twenty-nine are
housed that way and only that way** — brickmaker, packer, sawyer, wheelwright — and eight more are
partly so. For those four the second test is **silent, not negative**, and silence is currently
being read as refusal. That is the conservative direction and it is not the same thing. Opened as
ROADMAP K21.

### K20 measured again, from a one-household insertion

Inserting a single household renamed **17 of the 33** carried-over invented persons in the touched
household files, because the name allocator deals by index. T-A2h's two-person insertion renamed
25 of 94; this is the same defect at the same rate and it is still open. Nothing about anybody's
argued history changed — only the invented name attached to it. The churn is why this parcel's diff
touches 24 household files for one addition.

## Fixed 2026-08-14 — the roads were invisible, every street check was green, and the prime suspect was innocent

R-BUG2, owner-reported: *"the town roads seem to disappear in places and when you fly over them
you lose them."* True at both viewports. **Two independent faults**, and the mechanism the parcel
named as most likely turned out to be the one thing that was helping.

**The gate could not see any of it, and that is the first thing that was wrong.**
`tools/smoke_renderer.mjs` asserted seventeen street records, ~100 000 vertices, drape error under
1e-5 m, no vertex over water — all true, all green, all beside the point. **Draped is not seen.**
Nothing in this repository asked whether a road reached the screen.

**What the new check does.** `roadContrast()` holds the scene at two anchors a visitor is offered —
`south_water` at eye height down an open street, `from_above` at the aerial anchor — and takes
three frames: the real render **R**, the same geometry drawn as an opaque marker with a
deliberately deeper polygon offset **M**, and the scene with the streets hidden **O**. A probe on a
committed centreline counts only where **M** reached the screen, so roads genuinely hidden behind a
building, a tree or a rise leave the sample rather than scoring as faults, while a road losing the
depth fight to the terrain stays in it. The score is `|L*(R) − L*(O)|` on the critic harness's own
`labL`. Bars: median **ΔL\* ≥ 1.8** and **≥ 55 %** of probes at ΔL\* ≥ 2 per band, gated to 600 m.

**Measured with the fault in — both bars fail, which is the acceptance:** `south_water` 250–600 m
**0.3 L\*, 14 % perceptible**; `from_above` 100–250 m **1.1 L\*, 0 % of eleven probes**. With the
fix, desktop: `south_water` **4.2 / 3.9 / 4.0** across 40–100, 100–250, 250–600 m at 70 / 89 / 92 %,
`from_above` **2.9 / 2.4** at 91 / 63 %.

**Fault 1 — the depth fight, and it is the reported "in places".** A road is earth painted flat on
the terrain at the same height, held in front by one unit of polygon offset. Depth precision
degrades with distance, so past ~250 m the terrain won in patches. `−4 / −8` alone took the failing
band to **3.3 L\* / 71 %**. No vertex moved; `worstDrape` still gates at 1e-5 m.

**Fault 2 — the road was 4 % opaque, and it is the reported loss from the air.** At the aerial
anchor the ribbon is wide, unoccluded and wins depth, and it still scored 1.1 / 0 % — *neither* the
offset *nor* the thin-ribbon rule moved that band at all. A lightly worn track's alpha was
`0.08 + ruts*0.54 − crown*0.04`: 8 % earth over 92 % prairie away from the ruts, 4 % at the crown.
Baselines raised to **0.54 / 0.38 / 0.28**, modulation shape and class ordering untouched, recorded
as **L96** amending L79 — which already recorded these numbers as invention rather than measurement.

**Refuted — mip-averaged alpha falling under `alphaTest`.** The parcel's prime suspect, and the
shape of the v74 treeline bug. Turning mipmaps off made **every** band worse (`south_water`
250–600 m: 22 % of probes reaching the screen with mips, **6 %** without). The mip chain is holding
a sub-pixel ribbon together, not erasing it. `minFilter` is unchanged, and the instruction to
measure before choosing is what stopped a "fix" that would have made this worse.

**Not acted on:** `transparent: true` with `alphaTest` does sort a town-wide mesh on a meaningless
bounding-sphere centre, and the opaque queue measured slightly better — but an unblended
alpha-tested fragment draws at full strength, which would make every road solid and delete the
graded/worn/light distinction the dataset carries. If the sort ever bites, the answer is
per-record `renderOrder`, not opacity.

**What this cost the gate to learn:** `from_above` is an aerial anchor, and leaving the camera
there broke the horizon-timber check downstream — it reads the band the tree solver builds around
the camera and reported nought of nought covered bearings. A measurement that moves the camera owes
the next one its pose back.

## New 2026-08-14 — the first block across the river, on ground that was already partly built

**T-A4.** `blk_randolph_clinton` — Randolph, Canal, Washington, Clinton — is the first West
Division block the plat module reaches and now carries **seven anonymous roofs**: four dwellings on
four lots, three yard buildings off the alley. The town stands at **258 roofs of 665**; 407 remain
and **79 of those have modelled ground**. One lot is left bare on purpose. The geometry half was a
recipe entry and nothing else, exactly as T-A2 predicted for the third time running — what this
block cost was in the gates, and it is the first one that could have found this.

**Three roofs were already standing on it, and nothing could see them.** Every block parcel so far
arrived at empty ground, so treating all eight lots as free was correct twice and would have been
wrong here: `recon_1835_west_018`, `_019` and `_021` sit inside this block, placed from typed
coordinates months before the plat module existed, and **no record of theirs names a lot** because
there were no lots to name. The one-principal-per-lot check reads only the records the parcel
builds, so an occupied lot and a free one were the same thing to it, and **the separation gate does
not close the difference: two principal roofs twelve metres apart on one twenty-five-metre lot pass
every test in the file.** A second house on somebody's lot would not have looked like a defect from
any direction — the town would simply have been slightly denser than the ground it stands on.

**The fix derives the answer rather than asking for it.** Which lots are taken is read off the
committed footprints of the records that stand there; a recipe that had to be told would be a
second opinion about the same ground, which is the defect the plat module was built to retire. Two
gates ride with it. A yard building must stand on a lot this parcel gave a principal roof, because
a yard building behind somebody else's house is a claim about their household. And **every lot of
the block must now be built on, already occupied, or named open with its reasoning** — those three
were counted in three places and nothing made them meet, so a lot could have been called open in
the recipe with a house standing on it, which is a false statement about the town in the file that
documents the town. All five refusals were verified by committing each one deliberately.

**Two things this block exposed by not being South.** The visitor-facing location line on every
generated record read *"South Division"* as a literal — true of every record that had ever existed
and wrong on all seven of these, which is the shape of defect only a first case finds. And the
665-roof ledger attributed **every anonymous roof in the West Division to the Wolf Point recipe**,
because until today that was the same set: it read the seven new roofs as seven of that recipe's
own placements emitted out of order and refused to derive at all. It counts by the programme phase
each record names now, and the West recipe's remainder holds at **35**, unchanged, with seven West
roofs standing beside it.

**One household adopted, one refused, and the refusal is about the rule rather than the roof.** The
block deals a D1 and a D3 — the two families T-A2h's rule admits. The D1 log cabin is adopted: the
labourer's count is a floor by its own committed text, D1 is the family this layer houses nine of
its eleven housed labourers in, and this layer **already places two labouring households in the
West Division**, so nothing crosses a division line the programme had not already argued.
Households **154 → 155**, persons **190 → 191**. The D3 carpenter is refused: rule 6's two tests
are silent on division and all eleven carpenter households stand north or south, so a twelfth west
of the river would be a new claim about where the town's carpenters lived, arriving as a side
effect of a block parcel — the exact failure mode rule 6 exists to prevent. **Whether the rule
takes a division test is now ROADMAP T-A5's to settle**, once, rather than each parcel's to decide
again. No human figure is drawn (L1), unchanged.

## New 2026-08-14 — the baseline scored: **4.18 of 10**, and two of the three headline numbers were measuring the wrong thing

**R-G1.** The scored half of G0.2 is in, and the bar it was measured against is the one §0 says
can actually be held: eight axes, 1–10, five named stations, written justification, a specific
fix for every axis under 8, against this project's own reference set — the twelve pre-fire
pictorial plates and the verified tallgrass photographs — and never against a commercial game
frame. Pass is **mean ≥ 8.0 with no axis below 7**. The baseline is **4.18**, and **every one of
the eight axes is below 7**. That is the number later phases have to beat, and it is recorded
before W1 touches the renderer precisely so that there is something to beat.

**The protocol's independence condition is satisfied and worth stating.** This parcel wrote no
code at all — `git diff --stat` for it is three documents and a changelog entry — and the run
that built `tools/critic_shots.mjs` and `tools/critic_metrics.mjs` was a different one. The
scorer read the frames.

### The scores

| station | light | material | texture | geometry | atmosphere | post | composition | history | mean |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 3 | 3 | 1 | 5 | 4 | 4 | 6 | 7 | **4.13** |
| `first_post_office` | 3 | 4 | 1 | 6 | 4 | 4 | 7 | 8 | **4.63** |
| `south_water` | 3 | 3 | 1 | 3 | 4 | 4 | 4 | 5 | **3.38** |
| `prairie_west` | 5 | 5 | 2 | 5 | 4 | 4 | 6 | 7 | **4.75** |
| `river_bank` | 2 | 3 | 2 | 4 | 5 | 3 | 6 | 7 | **4.00** |
| **axis mean** | **3.2** | **3.6** | **1.4** | **4.6** | **4.2** | **3.8** | **5.8** | **6.8** | **4.18** |

Desktop 1280×800. The mobile set was captured and measured in the same run and is **not
scored** — the rubric is a reading of frames and five stations at one viewport is what the
protocol asks for; a second viewport would double the reading without changing which phase owns
anything. Six stations (`sauganash_wing`, `lake_market`, `forks`, `green_tree`, `from_above`,
`prairie_south`) were read for context and deliberately not scored.

**Texture at 1.4 is the floor of the whole exercise and it is not a surprise** — §1 item 9 says
there are zero texture maps on 244 assets, and the frames show it: clapboard is *geometry*, a
roof is one flat value, chinking is a second flat value, and the only texture in a town frame is
the ground. **Historical accuracy at 6.8 is the ceiling**, and it is the axis this project is
actually good at: at `first_post_office` the footprint is Andreas twice over, the position is
surveyed, and the unresolved reads are carried on the record instead of being resolved into the
geometry. The gap between 1.4 and 6.8 is the shape of this project — the research is ahead of
the rendering by five points on a ten-point scale.

### Why each axis scored what it did, and the one fix that moves it

Every axis is below 8, so every axis carries a fix and a phase. The fixes are written into
`docs/ROADMAP.md` against the parcel that owns them.

**Lighting & shadow — 3.2 → W1.** The only cast shadow legible in the five frames is each
chimney's, on the roof beside it. The directional light casts and the ground receives, so the
shadow map is not switched off — it is geometry: at 12:30 on 1 July at
41.89° N the sun stands **70.5°** up and a shadow is **0.354 ×** the height of what throws it, so
a house's shadow lies under its own eaves and a walker's frame carries almost no shadow
information. The scene note chose that hour deliberately, to light the south elevation the
records call white, and the trade is sound — but its cost has never been written down, and it is
this: **form has to be carried by something other than shadow, and the two candidates are both
switched off** (AO is `baked_ao: false` on all 244 assets, §1 item 10; environment lighting is
built and not installed, §1 item 11). Against that, `HemisphereLight` at **2.4** under a
`DirectionalLight` at **3.0** is a 0.44 fill ratio, which flattens what little modelling the
angle leaves. *Fix: W1 installs the exposed HDRI, and the hemisphere and bounce come DOWN in the
same change — the trap already written on the parcel. Nothing here argues for moving the hour.*

**Material realism — 3.6 → W2 (no-Blender half).** Every surface is one flat colour. A roof, a
whitewashed clapboard wall, a hewn log and its chinking, and a chimney differ only in hue —
there is no roughness variation anywhere in the town, so nothing reads as painted, weathered or
wet. The Wau-Bun blue shutters at `sauganash` sit at the same value as the glazing beside them.
*Fix: the material sheet W2's no-Blender half is already scoped to write — which surfaces exist,
what each is made of, and which archetype parameter selects it.*

**Texture detail & tiling — 1.4 → W2.** Zero texture maps on 244 assets; the ground is the only
textured surface in a town frame and its near field is a grazing-angle smear. The axis cannot
rise until W2's bake half lands. *Fix: W2, both halves; nothing else moves this.*

**Geometric detail & silhouette — 4.6 → W2/W3, and one item for lane 2.** Massing is good — the
`sauganash` ell and knee wall, `first_post_office`'s eave overhang and log ends, `river_bank`'s
cordgrass — and openings are where the silhouette fails: no reveal, no sill, no sash, no muntin
anywhere in the set, so the 6-over-6 rhythm the Green Tree plate documents does not exist. The
worse failure is at `south_water`, and it is a **data** failure rather than a rendering one: the
horizon row of the business street is one gable stamped a dozen times at even spacing, where the
research knows a store, an auction room, two newspaper offices and a warehouse. *Fix: openings to
W3's cage work and W2's params; the repeated stamp to lane 2 — the anonymous placeholder massing
needs per-record variation in width, pitch and eave height drawn from the family band it already
carries.*

**Atmosphere — 4.2 → W4.** The sky is a cloudless gradient at every station, and the 200–1500 m
band holds nothing for the haze to act on, so the far treeline meets its sky with no separation
at four of the five. The one place it works is `river_bank`, where the far shore genuinely
recedes — the 2026-08-13 far-timber fix is visible in the frame. *Fix: W4, items 1–6, plus a sky
that is not a single gradient.*

**Post-processing — 3.8 → W5.** Tone mapping and nothing else. Visible stair-stepping on the
`sauganash` ridge and along the water/vegetation boundary at `river_bank`, where the water plane
also shows rectangular stepping against the emergent stand. *Fix: W5's SMAA pass, and R-BUG1 is
in the same frame.*

**Composition — 5.8 → the anchors, not a phase.** Four of the five stations frame their subject
honestly. `south_water` does not: 60 % of its frame is foreground grass and the business street
it is named for is a 40-pixel band on the horizon. An anchor a visitor is offered should show the
thing it is named after. *Fix: `south_water`'s anchor in `data/scenes/1835.json` wants a position
on the street rather than in the field south of it — one record, no code, and it is the cheapest
point on this whole table.*

**Historical accuracy — 6.8 → mostly earned, one real deduction.** `first_post_office` scores 8:
evidence footprint, surveyed position, unresolved reads carried on the record. The deduction is
at `south_water` (5) for the same repeated stamp — uniformity that no source claims, understating
what the research knows — and at `prairie_west` (7) for the flower load. **CORRECTED 2026-08-15
by R-W4c(a): the "two orders of magnitude" this paragraph used to claim was a measurement error,
and it was 18× too big.** `0.0012` is what the flower-load recipe reports, and that recipe misses
94.5 % of the bloom at this station — its hue cut at 50° puts a yellow coneflower in with the
grass. Measured by hiding the flower heads and subtracting, the render's true bloom here is
**2.19 %** of hued ground. Against the 4–6 % target that is a factor of two to three, which is
still a real deduction and still not fixed. Read ROADMAP R-W4c(a) before quoting either number —
in particular, the 4–6 % target was itself derived with the blind recipe and is **not yet on the
same scale** as the 2.19 %. *Fix: R-W4c(b) for the flower load, which must re-derive the target
first; lane 2 for the stamp.*

### The three findings that are not scores

**1. Two of the three numbers §1 item 7 rests on are measuring the canopy, not shadow.** The
baseline recorded "shadows still clip to literal black — 12,063 pure `(0,0,0)` pixels at
`river_bank`, 11,015 at `first_post_office`" and a darkest ground decile as low as **L 0.93**.
Both are real measurements and both are attributed to the wrong surface. Connected components of
the literal-black mask, with their bounding boxes:

| station | literal black | components | of it in components lying **entirely above** the median land/sky row |
|---|---|---|---|
| `first_post_office` | 11,015 | 9 | **100 %** (largest 8,376 px, x957–1144 y42–117 — the crown at top right) |
| `river_bank` | 12,063 | 14 | **94 %** (six crown clusters, all y ≤ 230, boundary row 369) |
| `prairie_south` | 2,315 | 10 | **99.7 %** (all y ≤ 261, boundary row 395) |
| `sauganash_wing` | 61 | 1 | **100 %** (one crown edge) |

Not one literal-black pixel in the desktop set is on shaded ground. They are the shaded side of
the near-tree canopy — the `timber` `MeshStandardMaterial`, vertex-coloured, quantising to zero
where a leaf faces away from a 70.5° sun. The darkest-decile figure is the same surface reached
a second way: the metric finds "ground" as everything below the per-column land/sky line, and in
a column carrying a tree that line is the *top of the crown*, so the crown counts as ground.
Measured at `river_bank`: **63,711 pixels at L < 2, of which 95.7 % lie above the median land/sky
row**; the decile pool is ~55,000, so the L 0.93 reading is a canopy measurement end to end.
`south_water` 92.7 %, `first_post_office` 88.6 %. **`sauganash_wing` and `lake_market` are the
exceptions** — their near-black is 90–94 % *below* that row and is a different population, not
diagnosed here.

Consequence, and it changes what W1 does: **raising the shadow floor will not move either
number.** What lights a leaf facing away from the sun is the environment term W1 exists to
install, or a floor on the crown's darkest albedo. The fix stays in W1; the mechanism named in
§1 item 7 does not survive.

**2. The horizon-timber metric cannot tell a treeline from a townscape, and the town just moved
it.** The recipe counts a horizon column as timbered if any pixel in the band above the land/sky
line falls 3 luma below, or 3 G−B above, the sky extrapolated from the 20 rows over it. A gable
end breaking the skyline satisfies that as surely as an oak. Re-running the harness on today's
`dev` — with **no renderer change since the baseline** (`git diff --stat 282dd9a..HEAD --
renderers/` is `changelog.js`, 41 lines, and nothing else) — nine stations reproduce their timber
figures and **`prairie_south` moves from 0.364 to 0.436 all / 0.340 to 0.441 centre**, a 20 %
gain. What changed between the two runs is 19 anonymous roofs (T-A2 and T-A3), and the frame
shows them: the left third of `prairie_south`'s skyline is grey gable ends. **The § 5 target of
≥ 90 % horizon timber coverage can therefore be satisfied by building the town**, which is not
what item 5 was ever about. R-W4 owns the target; it needs a discriminator, or a second metric
that measures only columns with no structure in them, before its acceptance number means
anything.

**3. Lane 2 is spending the draw-call budget faster than lane 1 can recover it.** **RESOLVED
2026-08-15 by R-W5a — see the top of this file.** The +11 was 11 new material GROUPS, the growth
term is now zero, and no station is over budget at either viewport. The reading below is kept as
the measurement that found it. Same two runs,
same renderer, +19 structure records (242 → 261, +7.9 %):

| | `sauganash` | `s'nash_wing` | `lake_market` | `f_post_office` | `forks` | `green_tree` | `south_water` | `from_above` | `prairie_south` | `prairie_west` | `river_bank` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop baseline | 65 | 66 | 78 | 66 | 87 | 91 | 85 | 67 | 73 | 97 | 56 |
| desktop today | 65 | 77 | 89 | 66 | 98 | 102 | 96 | 67 | 84 | 108 | 56 |
| mobile baseline | 62 | 63 | 66 | 60 | 82 | 88 | 83 | 61 | 71 | 94 | 49 |
| mobile today | 62 | 72 | 77 | 60 | 82 | 99 | 94 | 61 | 82 | 105 | 49 |

**Exactly +11 desktop at seven of eleven stations and exactly 0 at the other four** — and
triangles rose by only 244–562, so this is per-object cost, not geometry. Stations over the
**≤ 80** budget go **4 → 6** on desktop and **4 → 5** on mobile; the worst goes 97 → 108. The
uniformity is the part nobody has explained: +11 at bearings 150° apart, and +0 at `from_above`,
which sees the whole town. **Straight-line extrapolation on the remaining 414 roofs is about
+240 draw calls** against a budget of 80. That is not a reason to slow lane 2 down — the roofs
are the product — but the budget cannot be met by tuning after the fact, and R-W5 should treat
batching as its first question rather than its last. The `from_above` zero is a lead: something
already drops these objects at distance.

### What this does not do

It changes no code, moves no building and re-measures no reference photograph. The §5 targets
that were set from the uncommitted 2026-08-10 sweep still need re-anchoring by measuring a
reference plate through `tools/critic_metrics.mjs`, which is still a one-line job and is still
not done. And a rubric score is one reader's judgement with its reasoning attached — the fixes
below are the durable half, not the number.

## New 2026-08-14 — two roofs of ten given an occupant, and the rule that refused the other eight

**T-A2h.** The parcel was expected to argue about the town's trade mix. What it found is that a
block parcel puts ten dwellings on the plat faster than any such argument can move, so the
question that mattered was **who is allowed to start one**. The occupation census is a claim about
Chicago — 3,265 people in 398 dwellings, calibrated against Andreas's 1833 roster — and a census
that grows every time somebody draws a cottage is a census fitted to the model. Two of
`blk_randolph_wells`'s ten roofs are adopted into the inferred-household layer; the other eight
stay anonymous count-units, which is what they already were.

**The rule now lives in the household programme's own `method` list**, where the next parcel will
read it. A block roof may be adopted only where BOTH tests pass: the trade's committed argument
states in its own text that its count is a **floor rather than a bound**, and the roof's family is
one this layer **already houses that trade in**.

- **Two of twenty-nine trades pass the first test** — the carpenter (*"the shop count is a floor
  under the trade, not a measure of it"*) and the labourer (*"still a small fraction of what 3,265
  people implies"*). Everything else states a ceiling — the plasterer's and the drover's say *"and
  no more"* outright — or is bounded by a workshop or store family's roof target. Two apparent
  further matches are a false positive worth naming: *floor* appears in the laundress and
  boarding-house-keeper entries only inside the Andreas quotation *"with the floor covered
  besides"*.
- **The second test, measured against the layer as it stands, picks the same two families.** All 8
  of the layer's adopted labouring households live in a D1 and 9 of its 10 carpenters in a D3 —
  and a D1 log cabin and a D3 one-room cottage are two of the seven dwellings this block deals.
  The tests were derived independently and agreed on the first block they were applied to, which
  is the only reason to trust either of them.
- **Households 152 → 154, persons 188 → 190, adopted anonymous roofs 83 → 85, standing roofs
  unchanged at 251.** This parcel built nothing, moved nothing and regraded nothing. The two
  roofs' presence, position and footprint are exactly as invented after the adoption as before it;
  what they gain is an argued occupant instead of a blank. Recorded as **L94**.
- **The H1 and H2 houses are the refusal worth keeping.** The schedule allows 18 larger houses and
  14 merchant or professional houses in the whole town, and their occupants are the most likely
  people in this dataset to be nameable. Inventing an anonymous merchant into one would break the
  programme's own rule never to infer a person where a documented one is available. Those two want
  T-I3's treatment — a reading of the record — and not a draw from a census.
- **The adoption is authored once and gated in both directions.** `tools/generate_block_infill.py`
  now reads the household ledger through `tools/inferred_occupancy.py`, exactly as the three
  earlier anonymous parcels do, so no generated record is hand-edited and the drift check that
  makes these parcels trustworthy still binds. A household pointed at an ancillary roof fails by
  name — a yard building serves the lot it stands behind, and nobody lives in a privy — and a roof
  the ledger names that no recipe builds fails by name. **Verified by doing each.**
- **What it churned and did not fix, recorded as ROADMAP K20.** Adding two people renamed **25 of
  the 94** reconstructed residents. The invented-name allocator deals names round each pool by
  index within a bucket, so an insertion shifts everyone after it. No grade moved and every name
  re-derives under `--check`, but the generator's own docstring says the assignment is a function
  of a person's id when it is a function of the whole population — and every future block parcel
  will rewrite a quarter of the town's invented names as a side effect until that is fixed.

**Gates:** `tools/check.sh` green; `node tools/smoke_renderer.mjs` green at 390×780 and 1280×800,
zero page errors, run against the source tree and again with `--published`.

## New 2026-08-14 — a block filled in, and the table nothing had ever read

**T-A2.** `blk_randolph_wells` — Randolph, LaSalle, Washington, Wells — stood empty and now
carries **ten anonymous roofs**: seven principal buildings on seven of its eight lots, three yard
buildings off the alley, to the family mix the 665-roof schedule apportioned it. The town stands
at **242 roofs of 665**; 423 remain and **95 of those have modelled ground**. One lot is left
bare on purpose, and which lot is arbitrary — recorded as such in **L92**, with the frontage
argument (larger houses to Randolph, rougher dwellings to Washington) written down so it can be
disagreed with.

**The parcel authors no coordinates, and that is the durable half.** The three earlier infill
parcels each hand-wrote their own eastings and northings, because the plat module did not exist
when they were written. `tools/generate_block_infill.py` reads every metre off the committed lot
polygons of the K7 grid: the recipe says which family stands on which lot, whether it fronts the
street or the alley, and how far back. The defect class K7 exposed — seven buildings standing in
the middle of the road, put there by a recipe that had never asked where the road was — is now
retired by construction rather than by a gate catching it afterwards. The gate still runs: the
generator tests every footprint against its own lot lines, the platted corridors, every other
footprint in the dataset, the heightfield and the archetype, before it writes a file.

**A table this project had been carrying and never reading.** `family_bands_ft` in the building
inventory has bands for 21 of the programme's 35 families. The other 14 — **H1, H2, H3, C4,
T1-T3, W5, F3, F4, I1-I3, M1** — had none, so the earlier generators could only build the
families somebody had separately retyped into Python, while the schedule went on apportioning H1
and H2 to blocks. `1835_family_archetype_crosswalk.json` has held the footprint band, storey
count, eave height and placeholder archetype for **all 35** the whole time, and agrees with
`family_bands_ft` on every one of the 21 they share. The generator reads the crosswalk. **H1 and
H2 stand for the first time**, and no band is retyped anywhere.

**One number was moved to fit an archetype, and it is written down.** The A3 privy's authored
eave band runs 6-7 ft and its bottom is below what the outbuilding archetype needs to carry its
own door plus a header — refused by name at 1.891 m. The sample is now drawn from the part of the
authored band the archetype can build (2.07 m, beside phase one's privies at 2.05), and a family
whose whole band sits under that floor fails loudly rather than being quietly raised out of its
typology.

**And a command that quietly destroyed a night's Blender work, found by running it.**
`generators/inferred_placeholder.py` builds the flagged placeholder massing for a new anonymous
record. Its `--check` path has stood aside since 2026-08-13 for any asset the canonical bake has
superseded — `kind: generated` in the manifest — for the stated reason that demanding the
placeholder bytes back would forbid the upgrade the bake exists to perform. **Its BUILD path did
not.** Run once for ten new records, it also rewrote the 128 already-baked ones: 113 KB of
canonical archetype geometry down to a 4.9 KB flagged box each, with their manifest entries
stamped back to `kind: placeholder` so nothing downstream could tell the difference. It reproduces
on a clean `dev` checkout, so it is not a local accident.

**Every gate stayed green through it**, which is the part worth keeping. A placeholder that
matches its record is precisely what the gates check for, so 128 buildings collapsing to boxes is
a state the whole suite regards as correct — and the published smoke passed against it, 204 and
201 assertions, before anyone noticed. What caught it was reading a `git status` that had 461
files in it when the parcel touched ten. The build path now asks the same question the check path
asks and reports `built 10 … 128 superseded by a canonical bake`; the asymmetry between a check
and the build it checks was the whole defect. The four gate runs above were then re-run from
scratch against the restored bake.

**What did NOT ship, stated plainly: the households.** T-A2 as written also called for household
records. Adopting these ten roofs means restating the occupation census — the household generator
gates the census and the households against each other in both directions — and that census is
the population layer's weakest joint, derived from five in-dataset calibrations rather than
cited. Re-arguing it as a side effect of a block parcel would be exactly the kind of silent
re-decision this project refuses. **The ten roofs are unoccupied**, no household names them, and
the work is queued as **ROADMAP T-A2h**. No human figure is drawn (L1), unchanged.

## New 2026-08-14 — 232 roofs stand of 665, and only 105 of the rest have anywhere to go

**T-A1.** The 665-roof programme has been subtracted from for the first time. The target was
authored in `data/reconstruction/1835_building_inventory.json` on 2026-08-11 and never moved
against what was built; the family crosswalk still called **617 roofs remaining** while
**232** were standing, a figure wrong by more than a third of the programme, and the next
block parcel was going to schedule against it. The remainder is now DERIVED —
`tools/reconcile_665.py` → `data/reconstruction/1835_665_roof_programme.json`, re-derived by
`tools/check.sh` like the plat grid and the liberties. A ledger about a town that grows most
nights cannot be a number somebody typed.

**242 records are 232 physical roofs.** Twelve records are a drawbridge, three bridges, two
piers, a palisade, a parade ground, a garrison garden, an open livestock pound, a courthouse
the production chronology puts in the autumn and a hotel still a construction shell — the
physical-roof
reconciliation credits them with no roof, which is what it is for. One record is two cabins
and the ledger counts the low reading. By district: **South 100, West 41, North 81, Fort 10**
against targets of 370 / 135 / 150 / 10. **433 remain.**

**The number that changes what lane 2 does is 105.** The plat module reaches 19 blocks
holding 152 lots. At the reviewed phase-1 parcel's own density — one principal roof per lot,
ancillary at the programme's own 154:511 — those blocks have **105 roofs of headroom**, and
seven of them, the whole Lake Street belt, are already at or over it. The other **328 roofs
have no modelled ground to stand on**: 20 in `blk_south_water_market` and
`blk_south_water_clinton`, which the plat module refuses because South Water's committed
centreline stops 24 m and 878 m short of them; 35 held by the West recipe's own gate at local
E −700 m; and 273 in ground with no committed street control at all — east of State, south of
Washington, west of Clinton, and the entire North Division, which the grid covers by not a
single block. **The 665-roof programme is coverage-bound, not recipe-bound.** Lane 2 has
roughly ten block parcels in it before § S9 street control and the terrain extensions are the
only thing left to do.

**Six family targets are already exceeded, by nine roofs, and that is reported rather than
hidden.** C1 stores, I2 and T2, W1, W4 and W5 all carry more roofs than the 2026-08-11 target
allows, every one of them evidence the research placed after the target was written. A
documented roof is not removable, so the nine come out of the invented family with the most
slack (D4). The same rule runs inside each district against the group matrix — North holds
three institutional roofs and two warehouses more than its share, all of them attested.

**What this does not do.** It builds nothing and moves nothing: every count here is a
function of records that were already committed. The per-block family mix is an
apportionment of the district's remainder, not a claim that any block held those families —
it exists so the schedule adds up, and the block parcels that consume it grade every value
they emit at the invented tier as they always have. Two authored files were corrected where
they stated something untrue about what has been built: the West parcel's status
(`reviewed_recipe_not_rendered`, when 20 of its 55 roofs stand), the roof reconciliation's
status (`planned`, when it is done and this ledger reads it), the North recipe's "remaining
90 roofs" (69 after reconciliation), and the crosswalk's superseded 617.

## The rendering program is live, and overnight work no longer ships to production

**2026-08-14.** Two things changed on the owner's instruction, and together they set what
tonight's loop does.

`docs/RENDERING.md` is **ACTIVE** (reviewed and merged, PR #106). The W track and the G0
critic harness are buildable now; the H (`walk-hd`) and N (native engine) tracks and every
remaining `OWNER DECISION` stay gated exactly as written. The approved KTX-Software install
landed on the bake runner, which unblocks W2's textures — note what it fixes: `bake.sh` asks
for `--texture-compress ktx2` only when the `ktx` binary is present, because gltf-transform
aborts the *whole* optimize when it is absent, meshopt included.

This app is now on a **two-tier `dev` → `main` pipeline** (`docs/PIPELINE.md`), the two-tier
form of the fleet pilot in `kevinrhaas/jobtracker.polecat.live`. Steward parcels and the
nightly bake branch off `dev` and PR into `dev`; merging there publishes only the integration
preview at **`/custom/chicago/4d/dev/walk/?year=1835`** — noindex, banner-marked,
`build.json` reporting `tier: dev`. **Production moves only when the owner dispatches
`chicago-4d-promote-to-prod.yml`.** Promotion is gated; deploy is not, and never will be.

Two defects are recorded rather than fixed, both pinned by gates so they cannot grow:
**79 of 742,581 terrain vertices face downward** (0.011 %, isolated, no visible artefact —
ROADMAP T-BUG2, distinct from the black wedge that was fixed today), and **the river edge
flickers when flying** (ROADMAP R-BUG1, almost certainly depth-buffer fighting between the
water plane and the ground crossing it, owned by the R-W5 parcel).

## The second block repeated the shape, and refused one of its roofs

**2026-08-14.** `blk_randolph_dearborn` — the easternmost block the plat module reaches on the
Randolph tier — carries **nine of the ten roofs the schedule dealt it**. Standing roofs
**242 → 251**, remaining **423 → 414**, 86 of them on ground the project has coverage for. The
geometry half of T-A3 was a recipe entry and nothing else, which is exactly what T-A2 said it
would be. The two things worth reading are what the repeat exposed.

**The tenth roof was civic, and it is deferred rather than built.** I3 resolves through the
`fort_structure` placeholder, and every building kind that archetype offers is a garrison word —
quarters, barracks, blockhouse, magazine, guard, sutler, artillery. Massing an anonymous town
civic building through it would have stood a garrison building 750 m from the fort. The crosswalk
had already written the condition on its own entry: the family *"spans unlike functions; they must
reconcile to named public records before selecting construction"*. So the generator now refuses
I1, I2 and I3 **by name**, quoting the committed sentence each refusal enforces, and a roof the
schedule dealt but the parcel did not build must be named in the recipe with its reasoning — a
gate that bites in both directions, so a family cannot be quietly dropped and a deferral cannot
be used to hide one. The distinction being drawn: an anonymous *dwelling* is a count-unit toward
a documented aggregate; an anonymous *public building* asserts that an institution stood here and
left no record, and this town's public buildings are few enough to be listed. **One anonymous I2
still stands in the North Division** from a parcel written before any of this, massed as a generic
frame block; it is recorded in L93 rather than removed, and it is not a precedent that extends.
ROADMAP **T-I3** now owns the research the refusal is waiting on.

**A latent defect from the first block, caught by the second, on a two-centimetre margin.**
`lot_frame()` chose a lot's alley edge as the edge nearest the alley's CENTROID — which sits at
the block's centre, so on an END lot the side lot line running back toward it is nearly as close
as the alley edge. Measured on this block: **38.93 m against 38.95 m**, and two of its four end
lots picked the side line, framing a building broadside to its own street and over the
neighbouring lot. **What reported it was the lot-margin gate at 1.44 m against a 1.5 m bound** —
a millimetre-scale complaint about a ninety-degree error, which is the part to remember. Measuring
to the alley strip separates the same two edges by 0.2 m and 26.3 m, and a structural check now
rides with it (front and rear are the same length to within the plat's skew; a 20 % disagreement
means one is a side line). **`blk_randolph_wells` cleared the old tie by 1.3 m in 37, so nothing
T-A2 committed moves** — it was one block's proportions away from the same failure, and it had
been green.

Tonight's loop is expected to produce **one parcel per run from two lanes that cannot
collide** (`docs/ROADMAP.md` → "THE OVERNIGHT LANES"): lane 1 RENDERING touches renderer and
tool files, lane 2 TOWN COMPLETION touches data only. **R-G0** (the critic harness), **T-A1**
(the 665-roof reconciliation) and the first two blocks off the reconciled schedule (**T-A2**,
**T-A3**) are all in, so the NEXT UP picks are **R-W1** (light) and **R-W4** (atmosphere) in
lane 1; **T-A4…** (one open block per run, now adopting in the same run) and **T-I3** (the
civic roofs T-A3 refused — research, not massing) in lane 2. **T-A2h** is in too. Today's
count is **261 structure records — 251 physical roofs of a 665 target — 154 households, 190
persons**. Everything arrives as a PR into `dev` and waits there.


Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-14 · **Phase:** S0, S1 (datum), S2-partial (terrain + river at the
forks), S4-partial (frame_tavern, log_dwelling, bridge_timber), S9-partial (dated visible
street layer), S10-partial (665-roof ledger + 108 anonymous roofs) and R1 (renderer)
complete. **K1 (inferred residents) complete through phase two; K7 (the platted block and lot
grid) complete through phase one, and phase two's placement gate is closed — every generated
placement in the dataset is out of the platted roadway and all three generators enforce it;
K9 (navigation UI) complete.**

**Current expansion:** the 1835 scene resolves **222 structure records**, and **152 households /
188 persons** stand behind them (76 documented, 20 derived, 92 inferred). 108 records are tagged
`inferred_anonymous` and display as flagged review massings; **83 of those now have an argued
occupant** rather than being anonymous count-units, and 162 structures name a household on the
building card. They begin—rather than complete—the owner specification's 665-roof target. Exact
anonymous presence, footprint and lot position remain conjectural, and the adoption changes none
of that: what it adds is a reason for the roof, not evidence for it. **No inferred person has a
name, and none should**; no figure is drawn (L1). The remaining North expansion is still gated
behind unified terrain and hydrology coverage.

**The weakest joint in the population layer, stated plainly:** no period trade table for a
comparable western town exists in `data/sources/`. Every occupation ratio is therefore derived
from five in-dataset calibrations rather than cited, and the arithmetic is written out per trade
in `docs/RESEARCH/residents_1835_inferred.md`. That is a real gap, not a rounding error.

**Water vegetation correction:** emergent plants now use true distance to shoreline and are
limited to the shallow eight-metre marsh edge. Non-emergent flora and every woody placement are
rejected over the traced water mask, and since 2026-08-13 the mirror of that rule holds too: a
species whose recorded `substrate` is `open_water` — a pad that floats — is refused every station
on dry ground. A first-run navigation guide can be dismissed and reopened
from Settings.

**Parallel phase-two planning:** three non-rendered parcel recipes now cover 84 additional South
Division roofs (66 principal, 18 ancillary), 55 West Division roofs (44 principal, 11 ancillary)
and 60 North Division roofs (45 principal, 15 ancillary). Together with the implemented 48 they
reserve 247 slots without exceeding any 665-roof family cap. They remain plans, not scene claims:
the South set waits for physical-roof reconciliation; 35 West roofs also wait for a unified
westward map/terrain extension to E -700 m, and the outer North pass waits for N +760 m coverage.
**Milestone 0 shipped; Milestone 1 (the forks) is in** — six structures placed from the
georeference, real ground, a traced river, and the liberties now readable inside the
walkthrough rather than only in the repository. **Seven structures now, and the seventh is
not a building**: the North Branch bridge is the first record built on the `bridge_timber`
archetype and the first in this dataset whose dimensions come from evidence rather than from
a placeholder. As of 2026-08-10 it stands on **two bents rather than fifteen invented cribs**
(§ 24) — the first time a reading of an archive has taken something *out* of this model.
**Eight structures now, and the eighth is the first BUILDING whose footprint is evidence**:
Hogan's store on Lake Street, where Chicago's post office opened in 1831, is recorded twice by
Andreas as twenty by forty-five feet (§ 25). It is also the first record here with nothing
conjectural in it, and the correction that came with it moved the post office's departure from
this building by twenty months.

---

## The critic baseline — 2026-08-14

**RENDERING G0.1 is in and G0.2's numeric half with it.** `tools/critic_shots.mjs` stands at
eleven fixed stations — the eight scene anchors from `data/scenes/1835.json`, driven by the
walkthrough's own `goTo` so the rig cannot drift from the viewpoints a visitor is offered,
plus three re-established prairie-sweep stands — at both release viewports, with the animation
clock held from before the render loop's second tick and the DOM chrome hidden.
`tools/critic_metrics.mjs` reads the PNGs with no dependencies at all, which means the same
code can measure a reference photograph and one of our frames. **That has never been true
here before**, and it is the reason the numbers below are worth recording.

**Read these as a baseline, not as a scoreboard.** Four things have to be said before the
tables, or they will be quoted wrongly:

1. **They are not comparable to the 2026-08-10 prairie sweep's figures.** That harness was
   never committed and neither were its station coordinates, so both the code and the camera
   positions are new. Where a §5 target was set from the sweep's implementation, the target
   needs re-anchoring by measuring a reference photograph through THIS code — which is now a
   one-line job and is not yet done.
2. **The measurement conventions are the harness's own** and are stated in the head of
   `tools/critic_metrics.mjs`: what counts as sky, how the land/sky line is found, the band
   the horizon timber is looked for in, and how a crown pixel is identified. They are fixed so
   that two rounds are comparable; they are not claims about 1835.
3. **Flower load is only meaningful at the open-prairie stations.** In a frame with streets,
   walls and roofs in it the denominator is not vegetation.
4. **The crown metrics need a crown.** `from_above` reports them because the harness reports
   everything, but 1,142 crown pixels in an aerial frame is not a canopy measurement.

Both baseline runs were **11/11 byte-identical between two separate browser processes** at
both viewports, and every station's pitch matched its declaration.

**desktop 1280×800**

| station | timber all | timber centre | crown fine | crown G−B | decile L | literal black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 0.637 | 0.666 | 0.579 | 44.9 | 5.76 | 0 | 10.4 / 7.5 / 0.8 | 0.0301 | 65 / 332,455 |
| `sauganash_wing` | 0.493 | 0.475 | 0.566 | 17.4 | 1.73 | 61 | 11.8 / 7.0 / 0.9 | 0.0383 | 66 / 376,563 |
| `lake_market` | 0.518 | 0.588 | 0.550 | 24.6 | 3 | 0 | 12.0 / 5.8 / 1.1 | 0.0327 | 78 / 484,554 |
| `first_post_office` | 0.847 | 0.937 | 0.552 | 12.2 | 5.35 | 11015 | 9.7 / 8.8 / 9.9 | 0.0004 | 66 / 393,698 |
| `forks` | 0.739 | 0.784 | 0.725 | 35.1 | 25.58 | 0 | 10.0 / 7.1 / 11.4 | 0.0013 | 87 / 596,618 |
| `green_tree` | 0.731 | 0.735 | 0.670 | 20.3 | 30.88 | 0 | 12.9 / 5.3 / 0.9 | 0.0017 | 91 / 553,498 |
| `south_water` | 0.889 | 0.903 | 1.004 | 27.4 | 2.95 | 0 | 17.0 / 26.7 / 30.1 | 0.0575 | 85 / 570,718 |
| `from_above` | 0.212 | 0.180 | 0.830 | 0.2 | 28.24 | 0 | 3.8 / 6.7 / 9.7 | 0.0019 | 67 / 433,090 |
| `prairie_south` | 0.364 | 0.340 | 0.682 | 27.8 | 3.27 | 2315 | 14.8 / 5.0 / 8.7 | 0.0031 | 73 / 512,018 |
| `prairie_west` | 0.832 | 0.850 | 0.629 | 24.1 | 13.67 | 0 | 14.4 / 21.8 / 27.7 | 0.0012 | 97 / 618,686 |
| `river_bank` | 0.641 | 0.719 | 0.740 | 47.9 | 0.93 | 12063 | 13.2 / 23.9 / 29.9 | 0.0022 | 56 / 371,691 |

**mobile 390×780**

| station | timber all | timber centre | crown fine | crown G−B | decile L | literal black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 0.756 | 0.823 | 0.572 | 26.3 | 19.49 | 0 | 13.5 / 1.6 / 0.3 | 0.0042 | 62 / 330,283 |
| `sauganash_wing` | 0.667 | 0.592 | 0.625 | 22.5 | 18.78 | 0 | 13.4 / 1.6 / 0.4 | 0.0092 | 63 / 323,946 |
| `lake_market` | 0.697 | 0.719 | 0.597 | 15.9 | 15.21 | 0 | 13.3 / 2.0 / 0.4 | 0.0177 | 66 / 377,012 |
| `first_post_office` | 0.919 | 0.989 | 0.541 | 21.1 | 5.26 | 1763 | 14.7 / 9.4 / 0.4 | 0.0001 | 60 / 386,536 |
| `forks` | 0.749 | 0.731 | 1.337 | 37.5 | 23.42 | 0 | 11.6 / 11.8 / 10.6 | 0 | 82 / 573,840 |
| `green_tree` | 0.767 | 0.746 | 0.740 | 23.6 | 39.46 | 0 | 6.2 / 1.2 / 0.5 | 0.0002 | 88 / 537,659 |
| `south_water` | 0.836 | 0.811 | 0.755 | 35.9 | 7.54 | 0 | 24.1 / 33.9 / 25.1 | 0.0128 | 83 / 550,065 |
| `from_above` | 0.156 | 0.192 | 0.774 | 4.2 | 25.33 | 0 | 6.3 / 11.9 / 10.5 | 0.0012 | 61 / 377,201 |
| `prairie_south` | 0.467 | 0.492 | 0.612 | 30.8 | 13.76 | 267 | 10.3 / 12.9 / 8.1 | 0.0018 | 71 / 476,074 |
| `prairie_west` | 0.679 | 0.696 | 0.772 | 24.1 | 10.65 | 0 | 21.0 / 30.8 / 19.6 | 0.0003 | 94 / 605,366 |
| `river_bank` | 0.713 | 0.773 | 0.814 | 40.3 | 2.77 | 2154 | 21.9 / 33.2 / 6.0 | 0.0004 | 49 / 365,353 |

**What the baseline says, against the RENDERING §5 targets.**

- **Horizon timber coverage is short of 90 % nearly everywhere** — 0.21 to 0.89 desktop, best
  at `first_post_office` (0.847) and worst looking down at the town from the air. § 1 item 5
  stands, and R-W4 owns it.
- **Shadows still clip to literal black.** 12,063 pure `(0,0,0)` pixels at `river_bank`,
  11,015 at `first_post_office`, 2,315 at `prairie_south` on desktop, and the darkest decile
  runs as low as **L 0.93** against the § 5 floor of **L ≥ 14**. § 1 item 7 stands, and R-W1
  owns it.
- **Sunlit crowns are no longer blue.** G−B is positive at every station (+0.2 to +47.9), well
  clear of the ≥ +10 target at nine of eleven, where the sweep measured −19 to −26. The colour
  bugs fixed on 2026-08-11 are the reason; this is the first measurement that says so.
- **Grain still collapses with depth, but not uniformly** — `sauganash` reads 10.4 / 7.5 / 0.8
  far/mid/near on desktop, `river_bank` 13.2 / 23.9 / 29.9. The stations that look down a
  street or across water hold their grain; the ones looking over open sward lose it. § 1 item
  4 stands.
- **Flower load at the prairie stations is 0.0031 and 0.0012** against the honest 4–6 %
  target. ~~Two orders of magnitude short~~ — **the gap is 18× smaller than that, and this
  bullet was wrong (R-W4c(a), 2026-08-15).** Those are the *recipe's* figures and the recipe
  misses 94.5 % of the bloom at `prairie_west`, counting 69.7 % of the pixels a flower painted
  as the plant it is being compared against. Measured by subtraction, the bloom is **0.0219 /
  0.0187 / 0.0076** at `prairie_west` / `prairie_south` / `river_bank`. The recipe figures are
  kept because the 2026-08-14 baseline is on them.
- **Draw calls exceed the ≤ 80 budget at four stations** — `prairie_west` 97 desktop / 94
  mobile, `green_tree` 91/88, `forks` 87/82, `south_water` 85/83. **This is new information,
  not a new fault**: the budget has only ever been measured at the spawn station, where it
  passes at 65/62, so nobody had stood anywhere else with the counter running. Recorded in
  ROADMAP against R-W5, which owns the draw-call work.

**What is NOT in this baseline, stated plainly.** The 8-axis rubric score G0.2 also asks for is
**not run**. The protocol requires a critic that did not write the code under review, and the
run that built the harness cannot be that critic without making the score meaningless. It is
parcelled as ROADMAP **R-G1** and the baseline is incomplete until it lands.

---

## What exists and works

| thing | state |
|---|---|
| Repository scaffold | **done** — full tree per `docs/PLAN.md` |
| Schemas (structure, source, scene) | **done** — phases, tiers, rights gating, scene-owned dates |
| `tools/validate.py` | **done** — schema, referential, confidence contract, per-scene date gates, phase-overlap, epoch coverage, release blocking, license + rights gating, staleness, publish budget |
| `tools/test_validate.py` | **done** — 96 checks, all green, including a proof that an 1836 building is excluded from the 1835 scene, that a liberty naming a building does not cover an invention it never mentions, that an attribute the archetype never reads cannot pass without saying what the mesh does instead, and that rewriting a record's prose does not report its mesh as stale while changing a value the generator reads does, and that an attribute an archetype declares it consumes actually moves the parameters when its value changes, and that an exclusion carries a reason and a citation that resolves and stops being an exclusion at its own earliest scene |
| `tools/check.sh` | **done** — full gate runs in **0.4 s**, no Blender |
| Research dossiers | **done** — 8 reports, ~360 KB, committed verbatim in `docs/research/` |
| Source records | **25**, of which **14** carry a Wayback snapshot — the three added with the bridge all do, and so does the post-office page |
| Structure records | **184 in the 1835 scene** — 76 pre-existing evidence records plus 108 visibly tagged anonymous recommended infill records; record count and physical-roof count are separately reconciled |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| **Datum** | **VERIFIED** — Wright-derived, Hathaway- and OSM-checked, RMS 17.5 m, re-derivable from traces |
| **Generator pipeline** | **WORKS** — pinned Blender 4.5.3, `frame_tavern`, 496-tri Sauganash from the record alone |
| **`frame_dwelling`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the archetype that unblocks houses: 1/1.5/2 storeys, knee wall and gable-end attic window, rear ell read off the footprint polygon, stoop or small roofed porch, and `construction` finally moving vertices (stud module places the openings, clapboard butt joints land on stud lines, braced frames get the girt band a balloon frame has no line for). Golden params + `docs/RESEARCH/archetype-frame_dwelling.png`; 248-730 tris per house. `GROUND_CONTACT: perimeter` verified against the mesh — every edge of the footprint polygon carries a wall at z = 0, worst gap 0.0 mm, nothing below the base of the walls |
| **`outbuilding`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the highest-count-per-effort archetype in the plan, and the one that gives the town yards instead of eight isolated public houses. A FAMILY, not a shape: `construction` log/plank/light_frame drives three different wall routines, shed roofs are first-class rather than a fallback, `open_sides` turns any subset of elevations into posts-and-plate, and `door` is none/man/stable/wagon — a boolean is refused with a message saying why. `board_gap_m` alone is the whole difference between a stable and a corn crib. Five golden variants from a 1.25 m privy to a 13 m hotel stable, 272-2008 tris; `GROUND_CONTACT: perimeter` verified on ALL FIVE against ground-plane EDGES rather than vertices (the first check compared vertices and produced false failures on a 13 m wall that is one quad). Discharges the stable half of L10; **the yard half stays open** — a fence line with two gateways is an enclosure, and building it out of an outbuilding would be calling a fence a building, so L10 needs NARROWING rather than resolving |
| **South Water Street** | **BUILT 2026-08-11** — sixteen commercial records land the town's business street, which the model held none of: Peck's store, both newspaper offices, Harmon & Loomis, Madore Beaubien's log house, Bates's auction room, the Beaubien homestead, Dole's warehouse, both Carpenter shops, Frederick Thomas, the old bank building, Pruyne & Kimball, J. H. Kinzie, Jones, and Thomas Church on Lake. One footprint is evidence (Carpenter's 16 x 20 ft log shop — the dataset's SECOND real footprint); fifteen are invented inside the documented 55 ft South Water lot cap. **What this street knows is *who* and *where*, and almost never *how big*.** Two records carry `review_required` (the Beaubiens, whose history runs straight into the August 1835 removal and the reservation pre-emption) — which blocks the 1835 scene from `released` until consultation happens. Two unresolved reads are flagged on the records themselves: whether Harmon & Loomis's building IS the *Chicago Democrat*'s building (they sit 37 m apart and Andreas gives no side), and whether Philo Carpenter's Lake Street log shop still stood after he built on South Water in 1833 |
| **Renderer** | **WALKABLE AND NAVIGABLE** — three.js r0.185.1 vendored, pointer-lock + touch, confidence view, provenance popup, live compass and a north-up overview derived from the loaded heightfield and structure footprints |
| **Navigation index** | **COMPLETE FOR COMMITTED DATA** — Settings searches all 76 scene structures and all four verified intersections, with aliases and recorded location text; intersection positions are compiled from `data/traces/street_control.json` rather than copied into renderer code. Compass, overview map and the live 1835/current street-name readout are independently persistent toggles. A fourth persistent setting switches every visitor-facing navigation measurement between Imperial (the default: ft, mi, mph) and Metric (m, km, km/h) without changing the metric scene data. The readout reports the corridor underfoot, an intersection when two centrelines are near, and the next cross street up to 70 m / 230 ft ahead. |
| **Smoke** | **PASS 2026-08-14** — `tools/check.sh` green, and `node tools/smoke_renderer.mjs` green at both release viewports in all four combinations the gate asks for: source tree **204 mobile / 201 desktop**, published mirror **204 / 201**, zero page errors throughout, with the town at 261 records. Run as four separate foreground commands because a full pass exceeds ten minutes. The history below is the record of how those assertions were earned. **PASS 2026-08-13, and for the first time against the files that actually ship.** `tools/check.sh` is green, and `node tools/smoke_renderer.mjs` passes **361 assertions** at both release viewports (390x780 and 1280x800) with zero page errors — run twice, once against the source tree and once with `--published` against the mirror. **The second run is the one that matters and it did not exist until now.** A sidecar's `gltf/<name>.glb` resolves to the UNCOMPRESSED masters in the source tree and to the meshopt + quantised derivatives on the site, so nothing that ran had ever loaded a compressed asset — and a renderer bug that only exists in the quantised path collapsed all 242 structures to 2 m boxes on the live site for several days, through two attempted fixes, with the gate fully green the whole time. The size assertion was also measuring the TALLEST building in the scene, which passes with one correct building and 241 broken ones; it now measures every structure against its own record, including its documented wall height. Reintroducing the fault fails the new checks by name on all 242. `tools/bake.sh` runs the published smoke after publish. Draw calls and triangles at the spawn station: **59 / 332,455** desktop, inside the 80 / 1,000,000 Full-detail budget. The two halves still run as separate foreground commands, because a full pass exceeds ten minutes. |
| **Flora** | **the sward is in; the false far-field surface is out** (2026-08-11) — `renderers/web/js/flora.js` plants the graminoid matrix, forbs, emergents and low shrubs from `data/flora/`. July phenology remains enforced in renderer and data. Near/middle plants root on the exact terrain surface and water emergents on the water surface. The former solid canopy at plant-top height was the apparent second ground seen on real devices; it is removed, and unresolved distant prairie colour now stays on the sole terrain surface (L80). **Since 2026-08-13 each community is planted at its own recorded `cover.matrix_fraction`** — a field the records carried, the validator gated and the renderer had never asked for — and each is split by the published `substrate` of its species, so a floating-leaved aquatic is planted over water and never on the bank it was standing on. |
| **The ground's claims, in the app** | **done** (2026-08-10) — the Evidence panel's *The ground you are standing on* reads graded claims off `terrain_spec.json`, derived per scene by `compile_scene.py` and re-derived by `check.sh`; the same slice added reasoning and geometry-state checks so those rows are no longer silent promises. |
| **What a source is, in the app** | **done** (2026-08-11) — citations now carry the document a modern page reprints (`transcribes`) or the reading that it reprints none, plus each source's own `what_it_supplies` / `what_it_does_not_supply`, so the ladder a visitor sees includes the reason it is the ladder. |
| **Liberties, in the app** | **done** — the Evidence panel lists the liberties derived from `docs/LIBERTIES.md` by `tools/compile_liberties.py` and re-derived by `check.sh`; the provenance popup shows the ones taken with the building you are inspecting; and the gate checks the document *for gaps* in both directions — refusing any conjectural value (footprint, position, a terrain claim, or a stated form attribute) that no liberty admits to, and equally any attested value the archetype or terrain generator never reads and no liberty owns up to leaving out |
| **The platted street module** | **MEASURED AND VISIBLE** — street corridors and widths remain committed in `data/traces/vectors/street_corridors_1834.json`, with Lake and Randolph named from committed control and re-derived offline by `check_street_module`. `data/streets/1835.json` now adds seventeen dated paths and keeps the 80 ft legal corridor separate from L79's 5.8-10.5 m visible travelled strips. `compile_scene.py` joins their citations into the sidecar index; the renderer drapes them on the ground, clips them at water and clears vegetation only from the track. South Water and Lake read as principal graded earth, ordinary streets as worn native earth, and no gravel, plank roadway or hard paving is shown. North Water's curve and every rut/track width remain explicitly conjectural. |
| **The lake shore** | **TRACED, NOT BUILT** — `shoreline.geojson`: the harbour reach, the 1834 cut, the old southward channel, the sand bar as an island and the mainland shore, E +314…+1570 off Wright 1834. Vectors only; no elevation, no mesh, nothing east of the box renders yet |
| **Published** | `site/chicago/4d/` (14.31 MB of a 25 MB budget) + a tile on the Chicago landing page |
| Exclusions | 14 date-guarded structures + a 4-item watch list — **in the walkthrough** since 2026-08-10 (Evidence panel, "What is not here"), citations joined, and now held to the same citation rule as a structure record (§ 26) |

## Corrections made after the first live look

Kevin opened the deployed build on real hardware and found two things headless testing had
missed. Both are fixed; both are the kind of thing only a real viewer catches.

- **The building rendered pure black on a real GPU.** The confidence shader computed
  `weight = f(vConfidence) * uConfMode` even when the view was switched OFF — and `NaN * 0.0`
  is still `NaN`, which poisoned `diffuseColor` through the mix. A geometry reaching a batch
  without `_CONFIDENCE` leaves the attribute unbound, and an unbound attribute is not reliably
  zero on real hardware the way it is under a software rasteriser. The channel is now
  sanitised at the vertex stage and the off path is guarded before it reads anything.
- **A well-documented building was rendered as near-total guesswork.** `wall_height_m` and
  `roof_type` were tagged `conjectural` while their own notes gave typological reasoning —
  "two full stories at typical period floor height", "gable is the near-universal form for the
  type and period". That is the brief's definition of `inferred`, not of `conjectural`. Worse,
  the massing rule took the worst confidence across the footprint too, so an unknown SIZE
  dithered the entire building into ghost massing. Size and character are different kinds of
  not-knowing: Wau-Bun documents a two-storey white frame building with bright-blue shutters,
  and no source gives a dimension. The massing now follows the attributes that say what the
  building was; dimensional uncertainty is carried in the sidecar, where the popup shows it.
  Understating what we know is as much a misrepresentation as overstating it.
- **The prairie appeared to be a second terrain layer.** The far vegetation simplification was
  a solid horizontal sheet at plant-top height. On real hardware it hid building foundations
  and plant roots while the walker remained correctly on the actual heightfield below — most
  clearly at the river bank and Exchange Coffee House. The sheet is removed, not promoted to
  terrain. Walker, buildings, streets, trees and detailed flora now share one explicit surface
  sampler; emergent roots use the water surface. The far field is terrain texture until a
  porous, terrain-rooted replacement can be built (L80).

## What does not exist yet

- **The full 665-roof inventory is not built.** South 48 plus North 60 anonymous slots are visible; remaining parcels, coordinated world extensions and the 35-family canonical archetype library are still open. The reconciliation and family crosswalk are committed handoff controls.
- **No terrain.** The scene stands on a flat plane; the 30-zone heightfield spec exists in the
  research dossier but has not been turned into data. This is the next stage.
- **No flora or fauna records.** The palettes and the placement table exist in the dossiers only.
- **Terrain and the river now exist**, traced from Wright 1834 through the same affine that
  fixed the datum. Total land relief across the whole 640 m box is **4.30 ft** — that is not a
  simplification, it is the site. The dossier's suggested 4–8x vertical exaggeration was
  refused because it contradicts `docs/EPOCHS.md` and LIBERTIES L3.
- **The bank profile is the largest unsourced assumption in the build.** No zone in the terrain
  dossier gives a bank *profile* at all; the 6 m face and its ease-out shape were chosen partly
  because a flat toe leaves the Z=0 contour — which IS the drawn waterline — ill-conditioned
  against the grid.
- **`chicagoarchitecturehistory.com` cites nothing** for the two best elevation figures in the
  dossier, which is why no land elevation in this build is tagged `documented`.
- **Placement is real but coarse.** All eight structures now carry surveyed coordinates rather
  than nulls, at about ±20 m — the georeference's error, not an additional guess. Three of them
  (Wolf Point Tavern, Miller House, Walker's meeting house) have no surviving intersection and
  are derived from the confluence and the modern bank, with a larger and differently shaped
  uncertainty stated on each.
- **Walker's meeting house may be the wrong building.** The west-bank testimony describes 1831
  and the north-bank claim is dated 1834, which is what you would see if the sources describe
  two different buildings about 150 m apart across a river. Position is tagged `conjectural`
  and the record says so in the first line.

## The datum is verified

`data/datum.json` now carries `verified: true`: **E 447072.7, N 4637395.8 (EPSG:26916) =
41.886721, -87.637951** — the forks junction as drawn on Wright 1834, fitted against eight
modern control points (RMS 17.5 m), cross-checked against an independently georeferenced
Hathaway (57.9 m agreement) and the modern OSM river junction (39.4 m). The brief's placeholder
was **203 m off**. Full memo: `docs/RESEARCH/datum_derivation.md`; the derivation re-runs from
committed traces via `tools/rederive_datum.py`, which `check.sh` enforces.

Structure positions still carry `symbolic_location` with null coordinates — they get filled as
footprints are traced through the fitted transforms in S2+, each carrying the ±20 m working
uncertainty of the 1834 sheets in its note.

## Fixed 2026-08-13 — the changelog was broken BY A MERGE, and both parents were green

**`renderers/web/js/changelog.js` did not parse on `main`, and neither did its published
mirror.** The What's-new tab imports it, so the tab was dead on the deployed site; Manager and
the polecat.live launcher parse the mirror, so this project reported no releases at all. 64
entries, back to the first building, were in the file and reaching nobody.

**Exactly one `] },` was missing** — the terminator of v64 *"Twenty-three buildings were standing
in the street"*. Every entry below it was nested inside that entry's `items` array, which is why
node reported the syntax error at line 565, the end of the file, 540 lines from the damage. A
second entry rode along with a duplicate `v: 64`: two branches finished 33 minutes apart, each
stamped its entry on its own branch, and neither knew the number was taken.

**The mechanism is the part worth keeping, because no existing gate could have caught it.**
`.gitattributes` merges this file with `merge=union` — a deliberate, documented choice, because
two branches each prepending an entry collide every time and union keeps both instead of
conflicting. But the union driver runs DURING THE MERGE. Merge `65c8de1` has two parents,
`cbe494c` and `60a78d0`; **both parse, and the merge of them does not.** Every gate in this
project runs on a commit somebody wrote. Nothing ran on the commit git wrote.

- **The repair.** The terminator is restored. The duplicated entry is now **v67** and sits at the
  top, where its own `ts` (12:26 UTC, the newest in the file) says it belongs. No entry anyone has
  read was renumbered — while the file was broken, no entry was readable at all.
- **`tools/check.sh` now runs the changelog contract**, as a step like any other. AGENTS.md has
  always instructed an agent to run `check-changelog.mjs` by hand before merging; a hand-run check
  is exactly the thing a merge-time corruption evades, and the file that gates every commit did
  not gate this one. The generic *renderer modules parse* step did catch it — as `parse error:
  renderers/web/js/changelog.js`, which names a file and not a defect.
- **The contract check reads the literal's SHAPE as text before executing it**, because executing
  it is the weaker test in two ways. A swallowed entry is still a valid object literal, so it need
  not raise a syntax error at all — it can simply vanish from the array with the file loading
  cleanly. And Manager and the launcher never execute this file; they walk it bracket-aware, so
  the shape IS the contract. Every entry must open at bracket depth 1; one that opens deeper got
  swallowed, and the entry above it is the one that lost its terminator. Verified against the real
  corrupted file from `main`: *"line 25: entry v64 opens at bracket depth 3, not 1 — it is nested
  inside entry v64 (line 18), which is missing its `] },`"*. The header count from the text walk
  is also compared against `CHANGELOG.length`, which is what catches the silent half.
- **What this still does not cover.** The check now runs before every commit and before every
  merge an agent performs, but nothing in this subtree runs on a merge commit itself — the
  repository's CI is outside `chicago/4d` and outside this lane's scope. A human merge on GitHub
  can still publish a union-corrupted changelog. The narrow version of that hazard is now loud
  the moment anyone runs the gate; the general version is recorded in ROADMAP § K12.

## Fixed 2026-08-13 — the horizon timber was being deleted by its own texture

**S6a item 5, both mechanisms the item names.** The far-timber band draws the dossier's bodies
of woods at three, four and six miles as a silhouette on a ring, broken up crown by crown with
sky opened through the stand — `k` runs down to about 0.02 in a gap. At four hundred metres,
where the band is forty pixels tall, that is texture. On a six-mile body whose entire silhouette
is one or two pixels it is a **deletion**, and the band was carrying both failures at once.

- **Measured at the spawn station, with the pixel floor removed and then in place.** 281 of 900
  bearings carry a timber body. Without the floor the modulation drew **251 of 280** resolvable
  bearings at a pixel or more on the phone and **267 of 281** on the desktop — worst silhouette
  **0.18 px** and **0.31 px**, geometry solved and written into the buffer and too thin to land
  anywhere. With it: **280/280 and 281/281**, worst **1.00 px**. The band's triangle count is
  **562, unchanged** — the floor moves vertices and never their number.
- **The floor is on the RESULT, not a cap on `k`**, so it binds only where pixels are scarce: a
  400 m treeline is 40 px tall and keeps its gaps to the last per cent. Where a body's raw
  silhouette is itself sub-pixel the modulation is suppressed outright, because a texture that
  cannot be drawn can only subtract.
- **The band is therefore now solved against the live viewport.** `main.js` passes
  `pixelsPerRadian` off the renderer size and the camera's own field — 475 px/rad on a phone at
  its 94° clamp against 833 px/rad on a desktop at 55°, a factor of 1.75 the old fixed field got
  wrong in the direction that over-cuts a phone. A viewport change re-solves the band exactly as
  walking does.
- **The colour was one line of arithmetic answering a question the renderer never asks.**
  `hazeDisplayLinear()` ran the haze colour through ACES to reach the band's display value. The
  band is `toneMapped: false, fog: false` — its fragment is `opaque → colorspace`, so a linear
  vertex colour displays as the hex it decodes from — while the fogged ground is
  `opaque → tonemapping → colorspace → fog` with `fogColor` uploaded in the OUTPUT colour space,
  converging on that same literal hex. One decode each. The tone curve was applied to one end
  and to nothing it had to match: **16 red and 12 green** off the ground it touches, 69 in blue
  at `prairie_west`. Both ends report **#88a3c0** now. And the old value was **L 170 against a
  horizon sky of L 162** — a band *paler* than its own sky, which is what a distant treeline
  never is; it is L 159 now, three below.
- **The gate is every resolvable bearing, not a percentage.** A 90 % bar would have passed the
  desktop half of the defect (267/281 is 95 %). Three new assertions at both viewports: the band
  and `scene.fog.color` are one colour, no resolvable bearing is drawn under the floor, and the
  band was solved against THIS viewport — a floor measured in pixels is meaningless against a
  hard-coded field. Verified they bite by removing the floor: both viewports fail, with the
  counts and the worst pixel named.
- **What this does NOT claim.** The finding behind item 5 is photographic — *31 % of horizon
  columns carry any timber, 3.6 % across the central two-thirds* — and it was taken with a shot
  harness that is not in the release gate. **It has not been re-measured**, so no column figure
  is quoted here. What is measured is that the geometry it was measuring is no longer being
  thrown away, and that the band is darker than its sky rather than paler. `docs/LIBERTIES.md`
  L35 is revised in both directions; the 0.82 haze cap it exists to confess is untouched, and
  the distance compression it buys is unchanged.

## Fixed 2026-08-13 — the sward ended on a straight line, and the line was arithmetic

**A ring is a circle about the walker, so its outer edge is a constant screen row.** The
three-critic prairie sweep measured it and named the row: `TUNE.mid.radius = 27.0` predicted row
448.8 and the frame showed one at 450, straight across all 1280 columns. That is ROADMAP § S6a
item 3, and the reason it is arithmetic rather than a rendering artefact is the site: 4.30 ft of
relief across the whole 640 m box, so a fixed distance really does land on a fixed row. The gate
now measures it the way the finding was stated — bin the view by bearing, ask each bin how far
its own sward reaches, convert the distance to the row it lands on. **On the ring as it stood
those rows spanned 1.4 px.**

Every lattice slot now carries its own outer radius: the layer's nominal one plus a
world-anchored offset of up to **±3 m** at full detail (±1.6 m on a phone, about an eighth of the
ring at every detail setting), from smooth 4 m value-noise lobes with a per-slot dither over
them. Measured after: **5.9 px** of spread at 1280×800 and **17.4 px** at 390×780, the sward
reaching 25.0–28.4 m about a nominal 26.4.

- **Widening the fade would not have worked, and the reason is worth keeping.** The band is
  already 7 m, which is 18 px of frame at that distance. The line is not the ramp — it is where
  the ramp reaches zero, and a wider ramp still reaches zero everywhere at once. What removes a
  line is a boundary that is in a different place in each direction.
- **It is nearly free, by construction rather than by luck.** Triangles are paid for by the
  LATTICE, not by the fade, so a slot the fringe pushes beyond reach is dropped at rebuild
  instead of drawn at zero height, and the lattice grew by the amplitude to carry the ones it
  pushes in — with a symmetric offset the mean cost is `radius² + variance`, not
  `(radius + amplitude)²`. Measured A/B at 1280×800 at three fixed stations: open prairie
  **174 363 → 176 656** triangles (+1.3 %, 3 742 → 3 850 flora instances), settled town
  **389 369 → 389 253** (−0.03 %), river bank **350 109 → 350 105** (−4). Draw calls unchanged
  at 37 / 66 / 72. The cost lands where the sward is dense and nowhere else, which is the right
  shape for it.
- **World position, not camera distance.** The offset is a function of the ground alone, so the
  ragged edge does not swim as the walker moves and is the same edge whichever way they face —
  the pop-in defect one ring further out, avoided rather than traded for. The gate asks the
  placer (`flora.fringeAt`) instead of re-deriving the noise, and requires nine points to answer
  identically from two cameras 40 m apart.
- **The flowers had to come with the grass.** The forb ring ends within a metre of the mid ring,
  so a fringe on the matrix alone would have left the brightest objects in the field drawing the
  line the grass no longer does. It is gated on its RINGS rather than on its drawn edge: at
  3.4 m cells a 3.75° bin holds one or two forbs, so "the furthest one drawn" is a sampling
  statistic, and measured that way it reported a nine-metre hole in ground that has none.
- **The pop-in gate had to be made instance-aware to stay honest.** It asked the layer's nominal
  ring how faded an arriving plant was, and a nominal ring answers *zero* — a free pass — for
  exactly the plants the fringe pushes furthest out. It reads each instance's own `aChiRing`
  now. Same bound, same measured 0.0 % arrival height.
- **Verified the gate bites**, by putting the fringe back to zero: the boundary spread falls to
  **1.4 px** against a bar of 4, the forb rings span 0.00 m, and the world-anchoring check
  reports no variation at all. Three failures, on the code that shipped yesterday.
- **What this does not do.** It does not extend the sward. L80 still owns the compression — the
  terrain's own colour carries everything past the ring — and the mid-field targets in S6a items
  1, 2 and 4–7 are untouched. This removes a line the eye reads as an object in the world; it
  does not put vegetation where there is none.

## Fixed 2026-08-13 — a fade function that was producing a step

**The transition the owner asked for had been there all along, sampled once per stride.**
"Grass and flowers appear out of the ground as you walk towards them" (K3) read like a missing
feature, and `flora.js` has scaled every plant down over the outer band of its ring since the
layer was written. The defect is the RATE, not the absence: the ramp was evaluated on the CPU at
lattice-rebuild time and baked into the instance's height, and the lattice rebuilds only every
`TUNE.step.near` metres walked. 1.2 m of step against the near ring's 2.2 m band means a plant
went from nothing to **55 % of full height in a single frame**, once per stride, forever. A fade
that only updates when the thing it is fading is rebuilt is a step function wearing a ramp's name,
and it is invisible in review precisely because the ramp reads correctly on the page.

The ramp now runs per frame in the vertex shader against `cameraPosition`. What that cost, and
what it bought, is in ROADMAP § K3; three things belong here.

- **A flower head cannot just shrink — it has to come down.** Its origin is partway up a stem, so
  scaling in place leaves it in the air over a plant that is no longer under it. `aChiRise` and a
  world-space descent applied after the instance transform (the instance matrix carries a real
  rotation for tilted heads, so it cannot be folded into the local offset).
- **The `fade < 0.35` head gate was itself the worst pop in the field**, being a step in the
  middle of a ramp on the brightest object in the frame. Heads have their own inset ring now, and
  the same heads are drawn: the ring reaches zero exactly where the plant's ramp passes 0.35.
- **The guarantee is geometric, not empirical.** The lattice is inset from the fade ring by the
  rebuild step, so a plant is always placed, at zero height, before it is near enough to be worth
  any. The residual is one frame of overshoot — the rebuild fires on the frame that carries the
  walker past the step — which is 0.024 m at 60 fps, about 1 % of a plant's height, and it is
  written down rather than rounded away. The near ring's visible radius is 0.6 m shorter than it
  was, which is the price of the inset and is left as a coverage question in K3.
- **The gate now walks.** Twenty 0.15 m paces at 390×780 and 1280×800, checking every plant that
  appears in front of the walker: measured worst arrival **0.0 %** of full height against a 10 %
  bar, plus a check on the ring geometry so the margin cannot be tuned away later. Triangles
  564 821 desktop against 564 681 before — a rounding error, and no new asset.

**And the gate was measuring the weather.** Running the baseline before touching anything turned
up an unrelated red: *"turning it off restores the render"* failed about **two runs in three on
main**, at 390×780, with a worst-cell delta of 9 against a bar of 8. The assertion compares two
captures of the same scene to decide whether switching the confidence view off leaves anything
behind — and the wind blows between them, at 1–3 fps under the software rasteriser, so most of
the residual it was measuring was swaying grass. The tolerance had already been widened once for
exactly that reason, which is the tell: a gate whose bar is set by its own noise is a gate that
will be widened again. `main.js` gains a harness-only `setAnimationHold` — keep drawing, advance
nothing — and the three captures are taken under it. The residual is readback noise now, so the
bar **tightened** from mean 0.5 / worst 8 to mean 0.1 / worst 3, and the assertion above it
(*confidence view changes the render*) got strictly harder, because sway can no longer supply any
of the difference it has to find. Two consecutive full runs green at both viewports.

That closes the debt the bake-gate entry below records as owed: the flora clock is frozen during
capture, and the bound was tightened rather than widened.

## Fixed 2026-08-13 — the nightly bake had been red for days, and nobody could see it

**The placeholder gate forbade the upgrade the bake exists to perform.** `generators/build.py`
writes `assets/gltf/<id>__<phase>.glb` for any record whose archetype has a generator, and every
`recon_*` record has one — so the canonical Blender bake lands on exactly the filename
`generators/inferred_placeholder.py` claims, and the gate then rejected the real bake for not
being the pure-Python placeholder it was built to replace. A second conflict rode along:
`tools/bake.sh` runs gltf-transform over `assets/web/`, so demanding byte-equality with the
master asserted that compression never happens. **What made it invisible is the shape worth
remembering** — the gate passed on every developer machine and failed on every CI runner, because
the difference was whether `npx` could reach the network. A green local gate was reporting on a
pipeline it was not running. The gate now compares only the master against the record, requires
the derivative merely to exist, and stands aside for any asset whose manifest entry says
`kind: generated`, leaving that to the ordinary staleness check.

**`tools/publish.sh` was an accumulator, not a mirror.** It copied files in and never took any
out, so a retired asset shipped forever: 108 `__recommended_1835.glb` placeholders, orphaned when
the programme was renamed, were still being served to visitors long after nothing referenced
them. Deleting a file from the source tree was not a thing the published site could express.
Fixed by clearing the published `data/gltf` before copying; payload 19.16 → 18.55 MB at the time.

**Known flaky gate, deliberately not silenced.** `mobile 390x780: turning it off restores the
render` compares a frame captured before the confidence toggle with one captured after, while the
flora is still swaying. Observed failing twice at worst-cell delta 11 against a bound of 8 and
passing on the third run with no code change. The bound has NOT been widened — a release gate
loosened until it stops complaining is not a gate. The fix is to freeze the flora clock during
capture, and it is owed. **Paid 2026-08-13** — see the flora-fade entry above: captures now run
under `setAnimationHold` and the bound tightened to a worst cell of 3.

## Fixed 2026-08-13 — two defects the owner photographed, and what they taught

**The Clark Street headland was the map's own lettering.** Fixed 2026-08-13. What makes it
worth recording is that the trace had been *believed* against a measurement that disagreed
with it: the South Water georeference note recorded 79.6 m of residual at Clark against
18.7 m at Dearborn and attributed the swing to paper stretch. Both numbers were right and the
explanation was wrong. A 60 m local disagreement between two independent methods is a defect
report, not an error bar.

**`generators/terrain_gen.py --glb` had been unrunnable since `terrain_inputs` was
extracted.** `terrain_inputs_sha()` is called before `main()` inserted `generators/` on
`sys.path`; run as `python3 generators/terrain_gen.py` that path is `sys.path[0]` by accident,
run under `blender --python` it is not, and the GLB half died on `ModuleNotFoundError`. The
insert moved to import time. Nothing caught it because `tools/bake.sh` does not build terrain
and the terrain GLB is a rare, deliberate invocation. **The heightfield and the GLB are now
back in step**; the committed GLB before this run was baked at `--decimate-deg 0.04` and the
one after at `0.03` (see K14).

**The tree-placement gate and the river mask are two different questions.** `isWater` asks
"is this the river" and its threshold is 100 mm under the datum, which is correct for that
question and was silently wrong for "may a stem stand here". The release gate had a green
check on the first question while the owner had a photograph of the second failing. Both
checks are now present.

## New 2026-08-13 — the platted grid exists, and it found seven buildings in the road

**K7 phase one.** The block and lot grid is generated rather than traced:
`tools/generate_plat_lots.py` offsets this project's committed street centrelines by half the
platted corridor, intersects them, and divides the result into lots — 19 blocks, 152 lots,
re-derived byte for byte by `tools/check.sh`. Tracing the 1834 sheets instead would have baked
their 3.7–4.5 % paper stretch into every block face. The blocks are `inferred` because their
inputs are; the lot lines and the alley position are `conjectural` and stay that way, because
four lots to a face is a reading of ONE block (block 18 on the owner's Clark-reach crop). No lot
and no block is numbered — this project has never read Thompson's numbering off a sheet.

**The grid immediately paid for itself as a check.** Of 222 placed structures, 80 stand inside a
generated block, 120 stand outside the 19 blocks it covers, and 22 stand inside a platted street
corridor. Most of those 22 are within a metre or two of a corridor edge, which says nothing
against a ±20 m georeference — but **seven sit 6.5 to 12.1 m in, which is the middle of the
road**, and every one of them is a `conjectural` placement from the inferred-structure
programme. The placement gate that put them there tests for overlap with other buildings, for
water, and for modelled ground; it has never tested for the street. Nothing documented is in the
road.

**Nothing was moved in this slice, on purpose.** Repositioning generated structures re-derives
the household ledger, so it belongs to the parcel that owns those files (ROADMAP K1 phase three)
rather than to the slice that discovered the problem. The finding is recorded with the seven
records named, in `docs/RESEARCH/thompson_plat_grid.md` § 7 and ROADMAP K7.

**What the grid is honest about not being**: 19 blocks of the plat's 58, no North Division (its
street control is what § S9 records as owed), no lot depth from any source — the depths are
residuals of the block — and nothing rendered. `blk_south_water_market`, one of the most built-up
blocks in the town, is refused outright because the street layer does not carry South Water west
of E +100. That refusal is the street control owed, arriving from a different direction.

## New 2026-08-13 — twenty-three buildings out of the road, and the point test that could not see them

**K1 phase three (a) / K7 phase two (a).** The grid found seven structures standing 6.5–12.1 m
inside a platted street corridor and left them there on purpose, because moving a generated
building re-derives the household ledger. This slice moves them and shuts the hole they came
through: `tools/plat_corridors.py` holds the corridor geometry for BOTH the report that found the
problem and the placement gate that has to satisfy it, so the two cannot answer differently — the
same argument `generators/mesh_inputs.py` settles for the staleness hash. The gate refuses any
generated footprint that reaches inside a corridor. **23 of the 38 recipe centres moved** (median
12.0 m, worst 21.9 m); in-corridor centres across the scene fell **22 → 10**, and none of the ten
is a generated placement.

**The seven were the loud end of twenty-three, and the point test is why nobody knew.** A centre
is one point and a building is a rectangle up to 11 m across, so a building can front a street
with its centre clear of the corridor and half its depth inside it. That is exactly what the
recipe had built: it read the 80 ft frontage bands as centre-lines to sit ON rather than as edges
to sit BEHIND, and the whole Lake Street shop row stood with its front half in the street and its
centre within a metre of the kerb line. Counting footprints instead of centres finds **56**
structures with some part in a corridor before this slice and **33** after it.

**Three of the moves could not simply step back.** `physicians_office` snapped into the First
Presbyterian Church, `inf_packer_dwelling` into a reserved phase-2 slot, `inf_cooperage_south`
into the South Branch — so each went to the nearest position clearing the corridor, every
committed footprint by 3 m, the two uninstantiated phase-2 recipes and the heightfield's dry
covered ground. The physician's office is 17.7 m from where it was because the nearest free
ground to its Lake Street frontage is a lot back from it. **Nothing was regraded.** These
positions were `conjectural` before and are `conjectural` after; clearing the roadway is not
standing on a recovered lot, and the recipe says so where it used to say the centres were band
assignments alone.

**What is left in the road is mostly not a defect, and one part of it is a measurement.** Four
anonymous roofs from the infill generators inherit this gate when that parcel next runs. The
other 29 are hand-placed records with a frontage argument behind them, and **thirteen are on
South Water Street** — where, walking north from the committed centreline, the traced 1834
waterline is **10.75 m away at E +180 against a 12.19 m half-corridor**. The platted 80 ft street
there runs 1.4 m into the river, and the spare is under 3 m at four more of eleven stations. On
that reach a building on the north side of South Water cannot be both outside the legal corridor
and on dry land — so the disagreement is between the plat module and the drawn bank, and it wants
a reading of the travelled way rather than thirteen nudged records.

## New 2026-08-13 — the last four out of the road, and the row that was aimed at the streets

**K7 phase two (b).** The four anonymous roofs the previous slice deliberately left in a platted
corridor are out of it, and both infill generators now ask the corridor question through the same
`tools/plat_corridors.py` the household generator and the grid report read. **No generated
placement anywhere in this dataset stands in a platted street corridor.** Footprints with some
part inside one: **33 → 29**; the 29 are hand-placed records with a frontage argument and are not
this slice's to move. Verified the gate bites by putting one record back where it was: it fails
with the record named and the depth measured.

**The four were one row's spacing.** The parcel's eight ancillary buildings had local E values of
314, 438, 560, 687, 810 and 315, 559, 809 — a **123 m pitch, which is the block pitch** — so one
yard building stood at the eastern edge of every block, a building's width from the next street,
eight times over. The generator that wrote them tested nothing: not overlap, not water, not
ground, not the street.

**Half of them passed, and why they passed is the part worth keeping.** The four that intruded
(−1.03 to −4.32 m inside the roadway) are the four largest ancillary footprints in the parcel; the
four that cleared it are three privies and a small shed, clear by **1.4–2.1 m against this
dataset's own ±20 m georeference**. They were not placed clear of the street, they were too small
to reach it — so a fix aimed only at the four failures would have corrected four numbers and left
the rule that produced them. All eight moved instead, by one argument: each now stands directly
behind the easternmost principal roof of its own block, 24 m back for the rear yards and 21 m for
the service yards, because a rear yard belongs to a lot and a lot belongs to a house. 17–32 m of
movement.

**Nothing was regraded and nothing was adopted.** These positions were `conjectural` before and
are `conjectural` after; clearing the roadway is not standing on a recovered lot, and standing
behind an anonymous roof is not evidence of serving it. The household ledger keys on structure id
rather than on position, so the 83 adopted roofs kept their households across the move — which is
what made the coupling the previous slice cited a re-derivation rather than a re-argument. The
North parcel carries the same gate and it binds nothing today: the grid covers no North Division
block, because that street control is what § S9 still records as owed. Detail:
`docs/RESEARCH/thompson_plat_grid.md` § 7b.

## New 2026-08-13 — one way to go somewhere, graded; and the half of the gate that was not running

**K9.** Viewpoints and the place search were two lists of the same ground inside Settings.
They are now one `Go to` tab, second in the strip after Controls, opened by <kbd>G</kbd>: 8
authored viewpoints, 4 verified junctions, 222 structures, built from the scene, the index and
the registry rather than from a menu somebody maintains. `#btn-help` is a hamburger.

**The parcel asked for documented entries only, and that turned out to be the wrong list.**
No structure position in this dataset is graded `documented` — **54 are `inferred` and 168
`conjectural`** — so documented-only would have shipped four junctions. Every structure result
instead carries its own `placement.position_confidence`, in the same three words and three
colours the building card uses, and the tab's summary line counts the grades from the list it
paints. What survives about a building is usually a street and a side of it, so a well-documented
tavern with a conjectural position is the normal case here rather than a failure — and the menu
now says which is which at the moment the visitor chooses where to go. The gate compares every
chip against the record it jumps to; a menu that graded a position more kindly than the record
does would be this project's worst kind of bug.

**Two defects the new assertions caught in their own slice.** The five-tab strip fitted 360 px
only by flex-shrinking labels out past their own buttons — one tidy row, measured, and a mess to
look at; the desktop panel is 380 px now, tab padding is 6 px and mobile type 11.5 px, leaving
about 20 px of slack at both viewports, and the gate measures rows, overflow and squeeze at both.
A sixth tab does not fit and will fail there. The confidence chips also rendered identically
grey, because a plain `.jump-result small` rule outranks `.conf-inferred` on specificity; the
gate now requires the grades to differ by colour as well as by word.

**The desktop half of `tools/smoke_renderer.mjs` had not been running, and it is not clear for
how long.** It aborted every run at the first click on the menu button — on `main` as well as on
this branch, reproducibly — and every desktop assertion after that point, roughly a third of the
suite, simply never executed while the run reported a failure that read like a broken control.
Nothing was covering the button: `elementFromPoint` returned the button itself at its own centre,
with no pointer lock, the page visible and focused. The cause is the scene's own weight. At
533 000 triangles on a software renderer one animation frame takes **0.46–1.10 s (measured)**,
and Playwright's click waits for the element to hold still across frames before it will hit-test
it, so 30 s of default action budget was being spent on frames rather than on the page. The
budget is now 90 s — room for a slow machine, not permission for a broken control, since a click
that never lands still fails. **This is a standing hazard, not a fixed one**: the same starvation
will return as the town grows (ROADMAP K14 already records 6 % of triangle headroom), and the
next symptom will again look like a UI bug rather than a budget. A full two-viewport pass now
takes upwards of ten minutes here; `SMOKE_VIEWPORT=mobile|desktop` runs one half while
iterating and prints that it is not the gate.

## New 2026-08-13 — a number that was written, validated, shipped and never read

**K3, coverage.** Every flora zone record authors `cover.matrix_fraction` — how much of the
ground that community's matrix covers — with a `bare_soil_fraction` beside it. `tools/validate.py`
has gated both since the records were written, and `index.json` denormalises the bare-soil figure
specifically so the ground shader can fetch it once. **`renderers/web/js/flora.js` had never asked
for either.** All ten communities were planted at the single lattice density L32 tuned on closed
wet prairie, so a settled town whose own record says **45 % of its ground is bare** was drawn with
the ground closed, and so were the shaded riverbank understory (0.45), the forest floor (0.35) and
the lakeshore sand (0.35).

The fraction is now the probability that a matrix lattice slot carries a plant — near tufts and
mid cards alike, because thinning one and not the other would put a seam exactly at the crossover
where the change of representation is meant to be invisible. It is the same rule the forb layer
has always applied to its own recorded densities, on the field the matrix layer ignored.

- **Wet prairie is untouched**, because it records 1.00 and 1.00 is the anchor. Nothing the
  three-critic prairie sweep tuned has moved, and the change can only ever *remove* instances.
  Measured at 1280×800 against `main` at three fixed stations: wet prairie **360 979 tris against
  360 863** (+0.03 %, which is the reshuffled random draw, not new geometry), settled town
  **429 281 against 441 683** (−2.8 %, 3 278 flora instances against 3 842), marsh edge
  **299 161 against 308 235** (−2.9 %). The scene gets lighter exactly where a record says the
  ground is bare.
- **Measured, across the eight communities that have a clean sampling station**: planted density
  now spans **2.21–6.90 tufts per m²** where it was one figure everywhere, and the implied
  full-cover density agrees at **6.31–8.15** against a lattice carrying 7.30.
- **The gate asks both halves**, because answering only the first is how this went unnoticed:
  that each community's authored number reaches the renderer (re-fetched from the records, not
  compared against a copy of the renderer), and that the sward on the ground follows it. The
  second assertion fails in the other direction too — if every community went back to one
  density, the per-m² spread would collapse toward 1 and the implied figures would fan out
  across the 0.35–1.00 the records give.
- **One anti-vacuity guard moved and the tolerance did not.** *"detailed flora roots share the
  terrain and water surfaces"* requires a minimum sample so that planting nothing cannot report a
  perfect worst error; its station stands in the settled town, and the mobile cone there now holds
  67 rooted plants against about 150 before. The guard is 50; the 1e-5 m root tolerance is
  untouched. That number is a property of the dataset now rather than of the renderer.

**Two findings measured on the way, and not fixed then. Both fixed 2026-08-13 — see below.** S6a
item 9 reads the `river_bank` shot against zone 1's cordgrass — but ground within eight metres of
water is the MARSH zone by extent, and the shot's sward is entirely `z04`/`z10` with no `z01` in
it at all. And the "~25 cm sprigs" are better explained by species than by density:
`nuphar_advena` and `nymphaea_odorata` are floating-leaved aquatics recorded at 0.01–0.10 m whose
own `appearance` text says they float in open water, and they were **6.5 % of the tufts standing
on that dry bank**, because `role: emergent` was all the renderer could see. Fixing that is a data
field in the published vocabulary before it is a line in the renderer — a renderer that decided
which plants float by reading their heights would be guessing at exactly the point this project
refuses to.

## New 2026-08-13 — the pads were standing on soil, and prose was the only thing that said so

**K3, the second finding.** A water lily and a cattail were the same record to the placer: both
`role: emergent`, and the role is what `station()` read. So the marsh community was planted
identically on both sides of its own waterline, and `nuphar_advena` and `nymphaea_odorata` —
0.01–0.10 m, `form: mat_prostrate`, `appearance` "floating pads in open water" — stood as ankle-
high mats rooted in the soil of the dry bank. **The evidence was in the record and unreadable by
anything but a person.**

`data/flora/index.json` now publishes a `substrates` vocabulary and every `role: emergent` record
states one:

| value | habit | may be planted |
|---|---|---|
| `soil` | rooted ground above the water; the default when the field is absent | dry ground only |
| `saturated_soil` | the emergent habit — wet ground OR standing water, foliage above the surface | both sides |
| `open_water` | rooted below the surface, leaves floating ON it | over water only |

- **The validator refuses the unplantable record**, not just the unknown word: an `open_water`
  species in a zone whose extent never reaches water — or a buffer that starts at the bank rather
  than at the waterline — is an error, because a record that can never be drawn is a claim the
  walkthrough does not make. Six new self-tests in `tools/test_validate.py`.
- **The community is split, not the slot dropped.** `flora.js` picks from the subset legal on the
  side of the waterline it is planting, with the weights renormalised over that subset. Refusing
  the slot after the pick would have been one line shorter and would have thinned the dry marsh
  edge by the lilies' 6.5 % share; `matrix_fraction` 0.75 does not stop meaning 0.75 because two
  of that community's species float.
- **Measured, at 1280×800.** An 8 m sweep of the modelled box: **299 dry marsh-edge stations**
  (289 plantable at all) and **286 over water**. Both lilies were legal at all 289 dry stations
  and are now legal at none; the cattail is unchanged at 289 dry / 273 wet. At the marsh-edge
  station nearest the forks the sward holds its density — **2 483 → 2 481 rooted instances,
  47 551 → 47 435 triangles** — and the two `head_ray` heads that stood on that dry bank, which
  are the lily blooms, are gone. A wet-prairie control station is identical.
- **The gate asks the placer, not a copy of its rules.** `flora.stationOf(e, n, speciesId)` runs
  the same `station()` the scatter runs; the smoke sweeps the box with it at both viewports and
  asserts no floating-leaved aquatic has a dry station, that the lilies still have wet ones, and
  that the cattail still stands on both sides — that last one because a placer that had refused
  *everything* on that bank would otherwise read as a pass.
- **What this does not claim.** That the lilies are at the forks at all is still `inferred` from a
  regional flora (`swink_wilhelm_1994`), at a token density, and where the pads sit within the
  eight-metre marsh edge is the scatter's, not a source's. The change moves a species from ground
  it cannot occupy to ground it can; it is not new evidence that it was there.

## Known weaknesses, stated plainly

0a. **The gate that exists to catch a building standing on nothing reported a perfect
    landing for a fort 832 m past the edge of the world.** Fourteen structures went in on 2026-08-11 at
    local E +1130…+1180; the `e1834_harbor_cut` heightfield stops at E +320. That much is L40's
    problem at four times the distance and it is honestly declared on every record. **The part
    that is a defect in the machinery rather than in the data**: `tools/heightfield.py` clamps
    outside the box, so the ground-contact check sampled the clamped edge for the structure's
    base AND for every point of its outline, got the same number twice, and concluded that the
    fort meets the ground. Every structure L40 covers was caught only because the clamped edge
    varies along a wall and produced a gap; the fort was far enough out and square enough on to
    produce none. The gate could see buildings that were nearly right and was blind to one that
    was completely wrong. `Heightfield.covers()` now asks whether there is any ground there at
    all before asking how high it is, the schema carries an `outside_modelled_ground` state
    beside `approach_not_modelled`, and the declaration is checked against the measurement in
    both directions. Turning it on immediately flagged two structures in other parcels that
    nothing had caught. **S2e parcel (b) then landed the same day** and the field now reaches E +1700, so twelve of
    the fourteen fort structures land and their declarations are gone. Two do not, for a
    different and better reason: the fort sits on a plateau that falls to the river between
    N +245 and N +270, and the stockade's north wall and the commandant's quarters cross the
    top of that fall by 1.40 m and 0.46 m. **No cut, fill, revetment or foundation is modelled
    anywhere in this project**, and the real work plainly had one. L46 was rewritten the same
    day to say so. The blindness the fort exposed is fixed regardless of whether anything
    currently needs the new state.

00. **The prairie loses a blind side-by-side against a July photograph, in under a second,
    and we now know exactly why.** A four-parcel sweep on 2026-08-10 put each piece of the
    vegetation through its own builder-and-critic loop against verified photographs of
    surviving Illinois tallgrass, with a blind A/B as the judgement. Three critics ran on one
    identical shot set. All three lost. Two of them, on different references and different
    framings, lost on the **same** feature. What follows is the measured state, recorded
    because it is more useful than the summary "needs work":

    - **The mid-field sheet is discarded at ~455 m.** Canopy rings from 2.5 m to 453 m sit at
      the sward top; from 511.8 m outward every ring drops to `y = 0.05` with `aMask = 0` and
      the shader discards it. The vegetated surface therefore ends where the fog is only
      27 %, and the 93 % haze `world.js` designs for at 1290 m is never rendered onto any
      vegetated pixel. **All three parcels have been converging on a colour no visible
      surface in the scene reaches.** This one fact produces the blind tell in both pairs,
      the missing aerial recession, the collapsed grain and the ring seam below.
    - **There is no aerial recession on flat ground and there structurally cannot be.** At a
      1.68 m eye with a 55° vertical field over 800 rows, a ground point at distance *d*
      lands `1290.9/d` px below the horizon — so the entire fog ramp from 10 % to 93 % lives
      between rows 402 and 406. Six pixels of atmosphere in an 800-pixel frame. Only vertical
      structure carried into the distance can buy recession here; exponential distance fog
      cannot.
    - **A ring seam draws a straight line across the frame.** `TUNE.mid.radius = 27.0 m`, and
      on flat ground a constant radius maps to a constant screen row — predicted 448.8,
      measured at row 450 in `prairie_south`, razor-straight across all 1280 columns.
    - **Grain collapses with depth where the photographs' is flat.** 5×5 high-pass RMS in
      bands down from the land/sky boundary: ours 13.8 / 14.6 / 21.2, both references
      18.8 / 31.4 / 39.3 and 39.3 / 41.7 / 41.3.
    - **The horizon timber is nearly absent.** Timber is detected in **31 %** of horizon
      columns overall and 3.6 % across the central two-thirds, against **100 %** of columns in
      every band of the reference including its faintest. The 2–4 px band *height* is honest
      arithmetic; the emptiness is not. A round that reported re-toning this band had in fact
      reduced its detection cover from 21.1 % to 0.9 %, and the target it was given
      (Weber 0.036–0.067) does not exist in the reference at any threshold — that error was
      the brief's, not the builder's.
    - **Crowns read as boulders.** Fine-detail ratio 0.23–0.34 against the photograph's
      0.61–0.64 — our crowns at 20–60 m carry the fine-scale texture of a photograph's
      kilometre-distant treeline. Shadows clip to literal `(0,0,0)` where the photograph's
      darkest decile is L 14–27, and sunlit crown tops are **blue** (G−B −19 to −26) where
      the photograph's are warm green (+13 to +24).
    - **The shot set has only one open-prairie view.** `prairie_south` stands 3.46 m from a
      trunk with 23.4 % open sky against `prairie_west`'s 95.4 %. That second angle exists
      precisely as the control that separates a tuned view from a fixed one, so
      `prairie_west` has been tuned against itself with no control.
    - **`river_bank` fails its own brief and the fault is the renderer, not the data.** Zone 1
      specifies cordgrass at 1.2–2.0 m and 40–55 % cover with `bare_soil_fraction: 0.0`; the
      frame shows ~25 cm sprigs on visible bare soil in near-rows.

    Two things came out of the sweep clean and should be said as plainly as the failures. The
    **July phenology is correct at source** — every warm-season grass vegetative with a null
    inflorescence, cattail fruiting and brown, ramp leafless, and a live guard that suppresses
    and reports any record that contradicts itself. And the **flora dataset is the one parcel
    a critic passed without reservation**. The renderer is what is failing it.

    Two methodological corrections worth keeping, both of which invalidate numbers this
    project has quoted:

    - **The primary reference was the wrong photograph.** `dupage_tallgrass_2018-07-24.jpg` is
      titled "*Restored* tallgrass prairie" and described as a "Prairie planting" on a former
      agricultural field — a seed mix on plowed ground, and restorations are bought for being
      forb-rich. The never-plowed Woodworth stand is the better analogue for unmanaged 1835
      prairie. ~~Measured flower load: planting 12.91 %, virgin remnant 1.79–5.54 %. The honest
      target is **4–6 %, not 13.89 %**.~~ **THE CORRECTION WAS RIGHT AND ITS NUMBERS ARE
      WITHDRAWN, 2026-08-15 by R-W4c(b1).** Neither clause survives checking. **No never-plowed
      remnant photograph is committed to this repository and no source record describes one** —
      the phrase occurs once in `data/sources/`, inside the record of the planting, citing
      nothing — so the 1.79–5.54 % half is unsourced. And 12.91 % does not reproduce: the
      committed recipe reads **5.54 %** on that frame, 7.02 % on its nearest quarter and 25.82 %
      with its two tests reordered. **There is therefore no 4–6 % target**, and this file must
      not be read as setting one. `node tools/measure_bloom_target.mjs` prints all of it;
      ROADMAP § R-W4c(b1) carries the reasoning and the three routes out.
    - **Two rounds were judged at the wrong look-angle.** The shot harness set no pitch while
      the reference photographer had tilted down ~12°, so every "nearest quarter" number
      compared the photograph at 2 m against our render at 4 m — and near-field vegetation was
      exactly what those rounds were tuning. The harness is now pitch-matched and prints its
      pitch. Correcting it makes the gap *worse*: 0.07 % against a virgin remnant's 2.97 %.
    - A hue/saturation test cannot separate July from October here — the October negative
      control lands *between* the two July photographs. That metric should not be quoted by
      anyone, including this file.

0. **The former slow-renderer walking failure is resolved without weakening its distance bar.**
   Movement now consumes up to a quarter-second of real frame time in terrain-and-collision
   substeps no larger than 0.05 s. A software renderer drawing only two frames per second no
   longer turns a 1.45 m/s walk into a crawl, while the short substeps retain bank and building
   collision accuracy. The foreground smoke run passes the same walk-distance assertion at
   both 390×780 and 1280×800. Current full-scene budgets are 49 / 53 draw calls and 378,647 /
   499,343 triangles respectively; the desktop renderer remains slow at 2 fps under SwiftShader,
   but elapsed-time walking is no longer coupled to that frame count.


1. **One structure record does not prove the schema.** The Sauganash exercises phases, a
   building move, and the full confidence range, but the model has not met a fort, a bridge, or
   a row of storefronts yet. Expect schema pressure at Milestone 1.
2. **`construction: balloon_frame` on the Sauganash is probably wrong** and is flagged as such
   in the record. Balloon framing postdates the 1831 building by a year. Left visible rather
   than silently swapped, because substituting one guess for another is not a fix.
3. **The Sauganash gallery reading was revised on day one**, from "gallery, conjectural" to
   "no gallery, inferred", after opening the two retrospective images the repo already held.
   Both show no veranda and both show the 1829 log cabin surviving as an attached wing. The
   images are not independent of each other, so this is inference, not documentation — and the
   `frame_tavern` archetype now has to support an attached log wing.
4. **Two sources have no web archive.** `drloih_hotels` has no Wayback snapshot and the
   validator warns about it on every run; the warning is correct and stands until someone
   archives the page. Wau-Bun's archived_url points at a scanned edition of the book rather
   than the transcription actually read during research — noted in the source record.
5. **Several research claims are snippet-derived.** `encyclopedia.chicagohistory.org` returned
   503 throughout the research session, and a few citations in the dossiers rest on search-index
   snippets rather than retrieved pages. They must be re-fetched before any of them is promoted
   to `documented`.
6. **The Conley/Stelzer rights question is open.** Marked `check_required`; no asset may be
   derived from it until a Stanford Copyright Renewal Database check is recorded.
7. **The 1835 lake stage is a guess.** 580 ± 1.5 ft ASL, tagged conjectural, and the entire
   vertical datum hangs off it.
8. **FIXED — the white paint now reads as white.** The earlier diagnosis in this file (a weak
   sky contribution at a grazing sun angle) was wrong, and wrong in a way worth recording: the
   tan wall was a STALE PUBLISHED ASSET, an older bake that still carried the over-dark AO
   texture. Two separate causes then turned up behind it. `publish.sh` shipped from
   `assets/web/`, which only `bake.sh` refreshes, so running the generator directly republished
   the previous mesh silently — now guarded, and it says so when it copies a master through.
   And the sky-derived PMREM environment was overriding albedo outright: measured, a brown log
   wall rendered at an R/B ratio of 1.08 against the 1.75 its own base colour specifies, with
   every surface converging on the sky colour whatever it was made of. For a project whose
   claim is that a documented white wall reads as white, that is a data-integrity bug wearing
   an aesthetics costume. The environment is gone; a hemisphere fill with a warm ground bounce
   plus the sun now carry the lighting, and hue is preserved (log R/B 1.30). Revisit with a
   properly exposed HDRI rather than a PMREM of an analytic sky.
9. **AO is baked but switched off, deliberately.** The bake path works end to end and is wired
   as a real glTF occlusion texture, but the archetype's clapboard courses and window reveals
   sit a centimetre off the wall and occlude each other: a measured bake comes out at mean 0.265
   with 69% of texels below half, and the building renders brown. Shortening the AO distance
   only reaches 0.38. It needs a low-poly AO cage, not a tuning tweak. `--ao` keeps the path
   exercised and `assets/manifest.json` records honestly that the shipped asset has none.
10. **`gltf-transform` did not run**, so `assets/web/` currently holds copies of the
    uncompressed masters rather than meshopt/KTX2 derivatives. Harmless at 44 KB; it must work
    before the town scales.
11. **FIXED — the liberties are now attached to their buildings.** The provenance popup reads
    `subjects` and shows the liberties taken with the building being inspected: the Sauganash's
    four, L9 on the Green Tree, L7/L8 on the three Wolf Point placements. Both views render from
    one derived record through one entry renderer, so the panel and the card cannot describe the
    same liberty differently, and the smoke asserts the discriminating case — a second building
    gets its own set, not the whole list, and a scene-wide liberty is not pinned to any building.
    **Completeness is now enforced for one class of invention, and only one.** `validate.py`
    runs the inverse check: every phase whose `footprint` or `position` is `conjectural` must be
    claimed by a liberty's `Covers:` field — `structure_id[.phase_id].aspect`, declared by the
    document rather than inferred from its wording. Six such inventions exist in the committed
    data (five footprints, plus Walker's position); six declarations cover them. The self-test
    asserts the discriminating case, and that case got stricter: an entry whose prose is *about*
    footprints and placement, and which names the building, no longer covers anything at all.
    The claims are checked the other way too — a token naming no such structure, no such phase,
    or an attribute that is not conjectural fails the gate, so an over-claim is as loud as a gap.
    Entries under **Resolved** are exempt from that last rule, which is what lets an append-only
    document survive its own data being corrected. **The rule now covers stated form as well as
    drawn geometry** (2026-08-10): the aspect vocabulary is every attested value in a record —
    `footprint`, `position`, `documented_range`, the structure-level `function`/`occupants`, and
    `form.<attr>` enumerated from the data rather than from a list, so a new archetype attribute
    is inside the rule the day it appears. Widening it found four inventions with no admission —
    the Sauganash 1829 cabin's wall height and roof type, both PLACEHOLDER in their own notes,
    and `gallery: false` on the Green Tree and the Western, where false is the archetype's
    default rather than a finding. Ten conjectural values, ten declarations. **What is still
    unenforced is omissions and simplifications**, and that is the hard half: an invention has a
    record to point at and an omission does not, so the Western's unmodelled stable yard (L10)
    and the Green Tree's side additions (L9) are covered by prose alone. No mechanism can catch a
    liberty taken that nobody noticed taking. Six of six structures carry at least one liberty,
    so the popup's empty state remains unexercised by real data.
12. **The omission half is enforced now too, and switching it on found a documented feature
    that was never built.** The invention rule reads a `conjectural` tag and demands an
    admission. An omission leaves no tag: evidence with no geometry in front of it looks exactly
    like evidence with geometry in front of it, which is why prose was the only thing holding it
    until now. The claim therefore comes from the generator — each `*_params.py` declares the
    form attributes its `from_phase` actually reads (`CONSUMED`), and every attribute outside
    that set must say on the record what the mesh does instead: `absent`, `simplified`, or
    `record_only` for something that was never a build instruction. The first two owe
    `docs/LIBERTIES.md` a `Covers:` token exactly as an invention does, and the popup marks
    those rows so a visitor sees it and not only the repository. **Twenty-one attributes across
    six buildings turned out to reach no vertex.** Most are benign-but-real simplifications — a
    chimney count no archetype reads, one window rhythm on all three frame taverns, wall surfaces
    fixed by the archetype rather than the record. One is not. **The Wolf Point Tavern's frame
    extension and its painted wolf sign are both `documented` and both absent from the model**:
    the record spells them `frame_extension` and `signage`, the `log_dwelling` archetype reads
    `frame_addition` and `sign`, and `from_phase` fills an absent attribute with a default, so
    the two best-attested features of the house were dropped in silence and the popup showed the
    project's strongest confidence chip over both. That is the confidence model working as
    designed and still misleading, which makes it the sharpest argument for this rule that the
    project has produced. **Repaired 2026-08-10, in one slice with its bake** (see 18 below).
    Miller's house was the same shape in miniature — its record says two chimneys and
    `log_dwelling` built one — and is **repaired 2026-08-10, in one slice with its bake**
    (see 19 below). What is still unenforced is what no record mentions at all —
    the Western's unmodelled stable yard is now claimed, but a liberty nobody noticed taking
    remains uncatchable by any mechanism.
13. **The document and the data had drifted, and writing the claim down found it.** L12 still
    read "position tagged `inferred`" for the Walker meeting house; the record was downgraded to
    `conjectural` on 2026-08-09 and nothing carried the change back. The keyword rule was
    indifferent to the disagreement — the entry says "placed", the value was conjectural, and the
    match held for a reason that had nothing to do with whether the two agreed. Declaring the
    claim forced the comparison. L12 now carries a Revised line saying so, and the stale sentence
    stays: the file is append-only, and a silently corrected admission is not one.
15. **FIXED — the staleness gate existed in the documentation and nowhere else.** `AGENTS.md`
    has said since the scaffold that "a stale committed GLB is a check failure, not a warning",
    and `assets/manifest.json` has carried an `inputs_sha256` per asset since the first bake.
    Nothing ever recomputed it. `run_stale_check` asked only whether each GLB appeared in the
    manifest, so a record could be edited into a different building and the town would keep
    rendering the old one with the gate green — the exact failure mode the S5 repairs are queued
    for, unguarded. The check now recomputes every committed asset's inputs and fails on
    disagreement, and the recipe lives with the generators (`generators/mesh_inputs.py`,
    `terrain_gen.terrain_inputs_sha`) so the side that writes the hash and the side that checks
    it cannot drift.
    **Switching it on required redefining the hash, because the old one was unusable.** It hashed
    the whole phase record plus every `.py` under `generators/`, which meant all six buildings
    read stale for reasons that cannot move a vertex: the `geometry:` declarations added on
    2026-08-10, and a `CONSUMED` constant added to one archetype's parameter module invalidating
    the others' buildings. A hash that cries stale over a rewritten note gets disbelieved, and a
    disbelieved gate is worse than none. It now hashes what the builder can see — the *resolved*
    parameters, the class's derived properties, the confidence floats, and the bytes of the
    builder, `common/`, `build.py` and the Blender pin. Parameter-module bytes are deliberately
    out: that module's whole effect on the mesh is the object it returns, and the object is
    hashed in more detail than its source would give.
    **The eight committed hashes were re-stamped without a bake, and that is a claim, so here is
    the proof.** Under the new recipe, every input to all six buildings is byte-identical to what
    it was at the last bake (`c3953d2`) — checked by running the new recipe inside a worktree of
    that commit and diffing the input documents, not by inspection. The single difference is
    `build.py`, whose only change in this slice is delegating the hash to the new module. Terrain
    re-stamped for the same reason: `terrain_gen.py` hashes its own bytes and gained an extracted
    function. No mesh was regenerated and none needed to be. `manifest.json` now records
    `inputs_scheme`, and the gate refuses a manifest stamped under a scheme it does not compute
    rather than comparing two hashes that mean different things.
    What this still does not catch is stated in `mesh_inputs.py`: it compares inputs, not output.
    Cycles AO is not bit-reproducible across hardware, which is why freshness is defined on inputs
    at all — a hand-edited GLB behind an untouched record passes, and nothing here can see it.
16. **The nightly bake pushes its branch and cannot open its PR.** `chicago-4d-bake.yml` ends
    by creating a pull request and that step has been failing on a repository setting —
    "GitHub Actions is not permitted to create or approve pull requests" — so every bake since
    the workflow was written has left its geometry on an orphan `steward/bake-*` branch that
    nothing merges. Eight such branches exist. This slice worked around it by fetching the bake
    branch and fast-forwarding onto it, which is fine for an agent that is watching, and no use
    at all for the nightly. The fix is one checkbox in the repository's Actions settings, or a
    PAT on that step; the workflow lives outside `chicago/4d/` and is therefore outside this
    lane's scope to edit, so it is recorded here rather than fixed.
17. **Frame rate figures are meaningless here.** 2–9 fps under headless SwiftShader is software
    rasterisation, not a GPU measurement. Draw calls (12) and triangles (1,006) are real.

18. **FIXED — the Wolf Point Tavern has its frame half and its wolf sign.** The defect the
    omission gate found on 2026-08-10 is repaired the same day, record and mesh in one commit:
    `frame_extension` → `frame_addition`, `signage` → `sign`, the two names `log_dwelling`
    actually reads. The building that named Wolf Point now has a board hanging outside it.
    **The rename was the smaller half.** `frame_addition: true` and nothing else would have let
    the archetype pick the bay's side, width, depth and storey count from its defaults — a
    two-storey frame block across the river front of a tavern the sources describe as low — so a
    documented feature would have arrived at an invented size with nothing admitting it, which is
    the same failure this repair exists to end, one level down. The record therefore states all
    four: side `end` and width 4 m of the 12 m frontage and depth 7 m all **conjectural**, storey
    count 1 **inferred** by the same argument the storey count above it uses. L24 admits the three
    conjectural ones; L20 moves to Resolved carrying both spellings that no longer resolve,
    because a silently corrected admission is not one.
    **What the sign is: a blank board.** The bracket, the arm, the board and its proportions are
    the archetype's invention, and the painted wolf is not drawn — no description of it survives,
    and a wolf painted from imagination would be the most conspicuous invention in the scene on
    the one object every visitor will walk up to. L25 says so.
    **Two limits worth stating.** The confidence tint on the bay follows what the bay IS
    (documented that it existed, inferred that it was low), not its unknown size — the rule set
    for the Sauganash, which means the tint alone will not tell a visitor the width is a guess and
    only the popup's liberty chip will. And the whole repair rests on a footprint that is itself a
    placeholder: 4 m of an invented 12 m is a fraction of a guess.

19. **FIXED — the chimney count is a number the archetypes read, and the third misspelling is now
    a test.** Every record states `chimneys`; neither archetype read the value. `frame_tavern`
    built two stacks whatever the record said and `log_dwelling` built one, so Samuel Miller's
    house — record two, model one — stood a stack short from its first bake. Both archetypes take
    the count now. The pair on a frame block keeps its exact positions (0.22 and 0.78 of the
    frontage, read off the Sauganash depictions) so that parameterising the number did not quietly
    move a building whose count was already right; a log building's second stack goes on the frame
    addition rather than the far gable, because *the record's own reason* for counting two is "a
    stack in each element", and honouring the number while contradicting its argument is not
    honouring it. L21 moves to Resolved and the six records drop the `geometry: 'simplified'`
    declaration that was true until this landed.
    **The `log_dwelling` half was the Wolf Point defect a third time.** The parameter was
    `chimney`, a boolean; no record in this dataset has ever contained that word, so `from_phase`
    took its default on every log building and nothing complained. Three occurrences of one
    failure is a pattern rather than bad luck, so it now has a check instead of another
    discoverer: `test_consumed_attributes_actually_reach_the_parameters` perturbs every stated
    value its archetype declares it CONSUMES and requires the resolved parameters to change — 55
    attributes exercised across the six records, with a `ParamError` counted as read, since
    refusing a value is the loudest possible proof of having seen it. The opposite direction (an
    attribute stated and *not* declared) was already the omission gate; this closes the direction
    where the declaration itself is the false one, which is the worse of the two, because an
    attribute inside CONSUMED is excused from admitting anything.
    **What it does not fix, and that is the more interesting half.** The count is `inferred` on
    every building and nothing else about a stack is recorded anywhere — not one source describes
    a chimney on any of these six. Position, girth, height above the ridge and material are all
    the archetype's, so the confidence chip a visitor reads on that row grades only *how many*.
    L26 is new and is the only place that distinction is legible.

20. **FIXED — Miller's frame range is dimensioned by the record, and fixing it found the storeys
    on the wrong half of the house.** The queued defect was L24's one building over:
    `frame_addition` is `documented` on `miller_house` — "a two-story house added to the cabin,
    fronting the river" — and the record stated no side, no width, no depth and no storey count,
    so `log_dwelling` supplied all four from its defaults. Repaired 2026-08-10, record and mesh in
    one commit. Two of the four turn out to be **attested**, which is the difference between this
    building and the Wolf Point bay: the side is `front` because the source says *fronting the
    river*, and the range is two storeys because the source says *a two-story house*. Only the
    width and depth are invented, and they are read off this record's own footprint polygon — the
    river-fronting limb is 9 × 6 m — rather than picked afresh, so the mesh agrees with the plan
    the record already draws. L27 admits them; they inherit the polygon's invention, which is
    total.
    **The storey count was the real defect and it was not on the queue.** `stories` was `2,
    documented`, with its own note saying in as many words that the two storeys described the
    river-fronting range and not the whole building — but `log_dwelling` reads `stories` as the
    LOG CORE's count. So the documented claim was spent on the cabin, the range fell back to a
    4.7 m default, and the model stood a two-storey log cabin **behind a shorter frame block**:
    the composition inverted, seen from the exact spot across the water where the 1833 description
    of it was written. That is the `frame_extension`/`signage`/`chimney` failure in its subtler
    form — not a name the archetype could not find, but a name it found and read as being about a
    different half of the building. No spelling check catches that, and neither does
    `test_consumed_attributes_actually_reach_the_parameters`, which proves only that a value moves
    *something*. The two-storey claim now sits on `frame_addition_stories`, the cabin's `stories`
    is 1 `inferred` (no source gives the log part a height; the 1833 view's "a two-story building
    and adjoining log cabin" only reads as a contrast if the cabin was lower), the 5.2 m moves to
    `frame_addition_height_m`, and `wall_height_m` becomes the cabin's 2.6 m — the number this
    record has named for it since it was written, sitting in a note rather than in a field.
    L13 moves to Resolved: neither composite building is a single extrusion any more.
    **What did not get better.** The archetype masses the footprint's bounding box, so the log
    core comes out the full 9 m wide rather than the polygon's 6 m and the 3 × 5 m re-entrant
    corner behind the range is filled in. Stating the range's own numbers is what makes that
    visible — the defaults produced an inverted-T matching neither the polygon nor the sources —
    and L27 records it. And the whole repair still rests on a placeholder: 9 × 6 of an invented
    9 × 11.

21. **The first bridge, and the first record whose size is not a placeholder.** The North Branch
    crossing at Kinzie Street — Chicago's first bridge, built 1832, replaced 1839 — is now a
    record, a bake and a published mesh, on the `bridge_timber` archetype that had been written
    and never used. Two of its numbers are evidence rather than invention, which is new here:
    **ten feet wide** is Charles Cleaver's, recalled in the *Chicago Tribune* of 29 Oct 1893 by a
    man who had driven a team across it, and the **71.83 m span** is measured between the two
    traced 1834 waterlines along the Kinzie alignment rather than chosen — it agrees with the
    reach's drafted mean width to about a metre, which is the check that it reads the map at this
    station instead of averaging it. Three source records were added, all three with Wayback
    snapshots.
    **What is invented is the middle of the bridge, and it is the most conspicuous thing in it.**
    Cleaver describes the ends — "the abutments were built of heavy logs in the shallow water near
    the banks" — and nobody describes what stood between them. Something had to carry 71.83 m of
    log stringer, so the archetype's default 4.5 m spacing puts **fifteen cribs in the river**, a
    regular colonnade a visitor will read as a fact about the bridge. It is a fact about the
    archetype. L29 admits it, and the confidence tint cannot: the tint grades what a crib *is*,
    not how many there were. The span it divides is itself the drawn waterline-to-waterline
    distance, and the abutments stood inside that line by an unrecorded amount.
    **Two sources contradict each other about the thing and both are kept.** Andreas has it
    "formed of stringers and only fitted for foot passengers" and "useless for teams" as late as
    the summer of 1833; Cleaver remembered driving across it, and on 18 Aug 1835 a procession of
    hundreds crossed it. It was rebuilt or widened in between and nothing reached says when or
    how. The record takes the 1835 reading — four stringers, a full-width deck — and says on its
    own face that an 1833 scene would want the other one.
    **A correction to this project's own dossier came out of writing it.**
    `docs/research/03-structures-north.md` §5 tags both "about 10 ft wide" and "clearing the water
    by about 6 ft" as documented. Only the width survives: the pages carrying the width, the
    abutments, the stringers, the 1832 date and the 1839 replacement say nothing about a height
    above the water, and a direct search of the same host for the phrasing returns nothing. The
    figure is kept, `clearance_m` is tagged `inferred`, and `bridge_timber_params.py`'s docstring
    is corrected so the constant's name stops asserting what it cannot show.
    **The contract's water-anchor rule is wired rather than written.** `docs/GLB-CONTRACT.md` has
    said since the archetype was drafted that a structure over water anchors `y = 0` at the design
    water surface and that the renderer must place it against the water plane; nothing implemented
    it, and nothing needed to until there was a bridge. The archetype declares `VERTICAL_ANCHOR`,
    `compile_scene.py` copies it to `placement.vertical_anchor`, and the renderer places `water`
    at a literal zero — that plane is zero by the definition of the vertical datum. The smoke
    asserts the **difference** between the two anchors, not `y === 0`: over dry land they agree,
    so a test that passed there would prove nothing.
    **Writing that assertion found two things the code was right about and the description was
    not.** First, sampling at the record's placement origin proves nothing either: that origin is
    the polygon's (0, 0), for this bridge the west end, which sits exactly on the traced waterline
    where the ground crosses zero — zero against zero, and the check passes whatever the renderer
    does. It samples the deck's midpoint now. Second, the failure mode is the opposite of the
    obvious one. `terrain.height()` does not report the channel bed over water; it reports a
    **wading barrier at +4 m**, put there to stop the walker strolling into the river. A bridge
    left on the terrain anchor therefore does not sink out of sight — it hangs four metres above
    the water, which is the harder failure to read, and it is what the smoke now pins.
    **You cannot walk across it, and that is stated rather than faked.** The walker follows the
    terrain, so the deck is scenery you pass under rather than a route; its footprint is excluded
    from the collision polygons, because treating a deck as a wall would put an invisible barrier
    across the river with nothing visible at head height to explain it. A walkable deck needs the
    walker to learn about surfaces above the ground, which is its own unit of work.

22. **The bridge arrives nowhere, and the gate that says so is new.** Three rules now ask
    whether a record is honest: the confidence model grades what a value claims, the liberties
    coverage check demands an admission for anything invented, and the geometry declarations
    demand one for anything stated and not built. None of them can see a structure that was
    built faithfully onto ground that is not underneath it, because **nothing in the record is
    wrong**. Every name resolves, every value reaches a vertex, every confidence chip is earned,
    and the North Branch bridge still stands 2.42 m clear of the terrain at both landings.
    `check_ground_contact` closes that direction. Each archetype declares where it touches the
    ground — `perimeter` for a building (the footprint outline, at the base of the walls) and
    `ends` for a crossing (the two end edges, at deck height) — and `validate.py` measures that
    outline against the committed heightfield through `tools/heightfield.py`. **The tolerance is
    not a new number: it is the walker's 0.35 m step-up rule**, because the question the gate
    asks is literally the walker's question, and a structure a visitor could not step onto has
    not met the ground.
    **What it found is the only thing it found, and that is worth stating too.** The six
    buildings land: their worst corner sits 0.16 m off (the Wolf Point Tavern, over the bank
    fall), well inside a step. The bridge does not, and cannot with the data as it stands — the
    deck sits at 2.22 m (Cleaver's inferred six-foot clearance plus the stringer and plank depth
    under it) and the highest land anywhere in the 640 m box is 1.31 m, so there is no ground in
    this epoch for it to arrive at. The record declares `ground_contact: approach_not_modelled`
    and L30 admits it; the popup shows the chip on the building being inspected, so the
    admission reaches a visitor and not only a reviewer.
    **The approach is not modelled because nothing describes one.** Andreas gives the stringers,
    Cleaver gives the width and the log abutments "in the shallow water near the banks", and no
    source reached says how a person or a team got from the bank onto the deck. An embankment
    would be a second invention stacked on the clearance figure — which is itself only
    `inferred` and unsourced in the dossier that supplied it — and unlike L29's fifteen cribs it
    is the invention a visitor would walk over rather than look at.
    **A smaller thing came out of writing it, and it is a warning about the staleness hash.**
    The contact height was first written as a `@property` on `BridgeTimberParams`, and
    `mesh_inputs.py` hashes every property a parameter class derives — so a number no builder
    reads immediately re-staled the bridge. That is exactly the false positive § 15 rewrote the
    hash to end, arriving from a new direction: the rule "a derived property is a mesh input" is
    right about constants and wrong about accessors. It is a module-level
    `ground_contact_z(params)` instead, and the docstring says why so the next one does not
    rediscover it.
    **What it still cannot see** is a structure standing on ground that exists and is wrong —
    the check compares a mesh against the heightfield, and both can agree on a surface no
    source supports.

23. **Four attributes of the bridge are now behind their evidence, and the evidence was a
    footnote under a paragraph this project has quoted for weeks.** The record's own memo listed
    four open threads on 2026-08-10; two were pulled the same day and one of them paid for
    everything. **Andreas prints, at the foot of pp. 631-632, a statement signed by four men who
    used the branch bridges** — J. D. Caton, John Bates, Charles Cleaver and John Noble, agreed
    at a meeting of old settlers late in the fall of 1883 and handed to the editors by Bates.
    It is the only description anybody wrote of how these crossings were put together:
    abutments of logs in the shallow water near the banks, **two "bents" of four heavy logs
    resting on the bottom in deeper water**, stringers of heavy logs from the abutments to the
    bents and between them, **puncheons or split logs for a floor**, about ten feet wide,
    **without railings for the first few years, after which guards or railings were added**, and
    **about six feet above the water, "so that teams passed under them on the ice freely."**
    Source record: `old_settlers_bridges_1883`, tier 2.
    **What it corrects, and none of it is corrected yet.** `pier_spacing_m` puts fifteen cribs in
    the river on the archetype's default; the letter says two bents. `pier_kind` is `crib`, and
    this record argued its way there by treating the Kinzie Street page's type-word "Bent" as
    modern editorial classification — it is the settlers' own word, and Cleaver, the eyewitness
    that argument leaned on, signed it. `clearance_m` was demoted to `inferred` here for want of
    a page; the page exists, and the dossier's `[DOC]` tag was right. The deck is the archetype's
    and the letter states it. **Every one of those is a mesh input**, so the record cannot move
    without the GLB moving with it, and this commit deliberately changes no value and no
    confidence tag: it lands the source, the memo, the liberties updates and the notes that say
    on each attribute's own face that it is behind its evidence. **The repair and its bake are
    one slice and it is the next one.** (It was, and it landed the same day — § 24.)
    **The work order**, so the next slice does not have to re-derive it: `bridge_timber` builds
    intermediate supports from a spacing, and the evidence is a count and a form, not a spacing —
    two bents at the thirds of a 71.83 m span is a different parameterisation, not a different
    number, so the archetype changes before the record does. `pier_kind` wants a `bent` value
    (four heavy logs standing on the bottom) beside `crib`. `clearance_m` moves to `documented`
    with this source. `railing` stays `false` and its note changes from an argument from silence
    to a reading of "the first few years". L29 moves to **Resolved** when the mesh shows two
    supports, and not before.
    **Two negative findings came with it, and they cost as much to establish as the positive
    one.** Neither 1834 sheet draws this bridge. Both were inspected at the crossing's own fitted
    pixel rather than by eye — invert each sheet's committed GCP affine at the record's deck line,
    fetch that IIIF region — and on both, the street stops at the waterline: a platted street is a
    dedication, not a structure. The thread the memo rated most promising, "the 1834/1835 Wabansia
    and Kinzie's Addition plat", turns out to be `hathaway_1834`, a sheet already in this dataset
    and already georeferenced, which is its own small lesson about open-thread lists. And on
    Hathaway a hatched, ladder-like mark sits in the channel within 35 m of the crossing and reads
    convincingly as a plank-and-stringer bridge symbol at moderate zoom; at full resolution it is
    the letter **H** of "BRANCH", lettered down the water. It is written down here so that it is
    found once rather than discovered twice.

24. **FIXED — two bents, not fifteen cribs, and the repair changed a parameter rather than a
    number.** § 23's work order landed the same day it was written, record and archetype and bake
    in one commit. `pier_spacing_m` is gone from `bridge_timber` and from the record;
    `pier_count: 2` (`documented`) replaces it, `pier_kind` is `bent`, `clearance_m` is promoted
    to `documented` on the 1883 statement, and the floor the archetype had been supplying in
    silence is stated as `deck_kind: puncheon`. The river carries three spans where it carried
    sixteen.
    **The parameter was the fault, not the value.** An archetype that divides a span by a spacing
    can only ever produce a colonnade, and a spacing is a builder's convenience that no witness
    would ever record. What a man who drove a team across a bridge remembers is *how many* stood
    in the water and *what they were made of* — so the input is now a count and a form, and the
    spacing survives only as `PIER_SPACING_FALLBACK_M`, the thing a bridge falls back to when
    nobody described its middle. Changing 4.5 to 23.94 would have fixed this bridge and left the
    next one to be found by the same accident.
    **What the confidence view now says, and it says more than it did.** `clearance_m` is one of
    the attributes that says what this structure WAS (a bridge's documented description *is*
    dimensional — see `bridge_timber_params`), so promoting it takes the deck and the stringers
    out of the half-dithered state the `inferred` tag put them in, and the bents come out solid
    because both their count and their form are attested. That is the first time in this dataset
    that evidence has made something *less* dithered.
    **And what it still cannot say is where they stood.** The letter locates the bents by depth —
    "resting on the bottom, in deeper water" — which is a locator this project cannot use: no
    source gives the channel's bed profile and nothing below the waterline is modelled. They are
    built at the third points because that is what a builder would do with three roughly equal
    runs. So the chip on `pier_count` grades how many and a visitor sees exactly where, which is
    the `chimneys` situation of § 19 arriving at a different structure. **L31** is where it is
    admitted, and it carries a second omission the repair created: three spans make each stringer
    run 23.9 m, longer than any timber anybody was moving, so those runs were spliced somewhere
    and nothing says where. The mesh shows one log per bay. **L29 moves to Resolved** — and only
    now, because the entry itself said it would stay until the mesh showed two supports.
    **One limit of the mesh is worth stating on its own**, because it is the most specific phrase
    in the source. *Resting on the bottom* is what distinguishes a bent from a driven pile bent,
    and above the waterline the two are the same picture; `_log_bent` differs from `_pile_bent` by
    four heavy logs against three light ones, which is what a visitor can actually see. The rest
    of the distinction lives in the record and in this file.

25. **The first building whose footprint is evidence, and a correction to our own dossier that
    changes what it is.** `hogan_store` — the log store at the west end of the Lake Street block
    in which the United States opened a post office at Chicago on 31 March 1831 — is the eighth
    structure and the first BUILDING here whose outline is not a placeholder. Andreas gives its
    size twice, in two independently written passages: "The building was twenty by forty-five feet
    in size, was partitioned off so as to serve as a post-office on one side, and as the store of
    Brewster, Hogan & Co., on the other", and "the store only occupied an area of forty-five by
    twenty feet". 45 × 20 ft is 13.716 × 6.096 m and the footprint is tagged `documented`, which
    no building footprint in this dataset has been before. **What is documented is the SIZE and
    not the plan**: which axis runs along the street is nobody's evidence, so that assignment sits
    on the facade bearing in the position note, where rotating the building is what changes it.
    **This is also the first record here with nothing conjectural in it**, which is not a boast —
    it means its gaps are gaps in the sources' precision rather than holes filled by invention.
    It does mean the popup's empty "What we made up here" state is finally exercised by real data,
    which § 11 recorded as unexercised.
    **The correction is the more useful half.** `docs/research/03-structures-north.md` § 4 dates
    the post office's move to the Franklin and South Water address from 2 November 1832, the day
    Hogan succeeded Bailey as postmaster, and calls that the 1835 office. Andreas says twice that
    the office was still at Lake and South Water through 1833 and moved **about July 1834**. The
    dossier's conclusion survives and its chronology does not: the 1832 date is the postmaster's,
    not the building's. The conflation is traceable to the Currey page the dossier used, which
    makes the appointment and the move one sentence — and which also supplies the "south west
    corner" that Andreas never gives. Source record `chicagology_first_post_office` says on its
    own face where it is followed and where it is not. **The consequence for the scene**: on
    1835-07-01 this building is a store that used to be the post office, and the town's actual
    post office is a different, unmodelled building about 100 m east, of which nothing survives
    but a street junction — it would be the most invented building in the dataset and it is
    written down rather than built (`docs/RESEARCH/hogan_store.md` § 4).
    **The weak point is survival, not geometry, and it is stated on the record.** The building is
    attested standing to about July 1834 and no source reached follows it past that; it is placed
    in a scene set eleven months later on the continuity argument, with the counter-argument —
    Lake and South Water was the corner most exposed to the 1835 boom — in the same note. If
    evidence turns up that it came down first, it belongs in `exclusions.json` and this record
    leaves the scene.
    **One smaller thing came out of the same page and is recorded rather than acted on.** Currey
    has Thompson's 1830 plat laying out streets "uniformly 66 feet wide"; every position in this
    dataset offsets by half of an **80 ft** street, from the widths annotated on Hathaway 1834.
    The difference is 2.1 m, an order of magnitude inside the georeference's own error, so nothing
    moves — but the two cannot both be right about the same street, and the reconciliation worth
    testing is that they are not about the same street. See `docs/RESEARCH/hogan_store.md` § 5.

26. **What was left out is readable in the walkthrough, and enforcing it found the one file
    where rule one was never checked.** `data/exclusions.json` — fourteen researched
    structures with the evidence that dates them, plus a four-item watch list — has existed
    since the scaffold and has been read by agents only. A visitor standing in an empty lot
    cannot distinguish three different statements: nobody researched this, the evidence
    dates it after the scene, or it had already come down. The first is a gap in the work
    and the other two are findings that cost research to establish. The Evidence panel now
    carries them under **What is not here**, derived per scene by `compile_scene.py` with
    the citations joined, below the liberties and in the same `<details>` entry, because
    they are the same kind of disclosure.
    **The chip is the record's field, never a phrase derived from an absence.** Ten entries
    carry `earliest_scene` and show "not until 1837"; `kinzie_house` and `ouilmette_cabin`
    were excluded because they were GONE, carry no such field, and get no chip — stamping
    one on them would be an invention on the panel that exists to admit inventions. The
    smoke asserts that discriminating pair rather than a count, and asserts that a building
    the visitor can walk up to is *not* on the list, which a section dumping the whole
    dataset would still have passed.
    **The list states what it is not**, and that sentence is a smoke assertion too: eight of
    roughly forty researched structures stand, so a fourteen-item list of absences with no
    such note reads as "this is what is missing", which would be the largest false claim the
    panel could make.
    **Two rules arrived with it, and the first is embarrassing in the useful way.** AGENTS.md
    rule 1 is that every `source_id` resolves in `data/sources/`; `exclusions.json` was the
    one file where nothing enforced it, because until now nothing read it — a citation there
    could have named a source that never existed and the gate would have stayed green.
    `check_exclusions` holds it to the same standard as a structure record: a slug id, a
    name, a stated reason (an exclusion without one is a deletion with a filename), and at
    least one citation that resolves. The committed file passes unchanged; the value is that
    the next entry cannot. The second is the date gate read backwards: an entry dating a
    building to 1837 is a correct exclusion from 1835 and a WRONG one from 1837, and no
    comparison against the records can catch it because an excluded structure has no record
    to compare with. In a year-parameterized project that is exactly the check worth having
    before the second scene exists rather than after.
    **The watch list is deliberately not shown.** Its four items are structures whose 1835
    status is uncertain rather than settled, and one of them (`western_hotel`) is standing in
    the scene — putting them under "what is not here" would be false about the one thing the
    section is for. Their uncertainty belongs on the records and in the provenance popup,
    which is a different slice and is not queued.
27. **The sidecars are re-derived by the gate now, which they were not.** `compile_scene.py`
    writes what the renderer reads and the outputs are committed so the site needs no build
    step — an arrangement that only holds if drift is a failure. Nothing recomputed them, so
    a record edited without a recompile shipped a walkthrough quoting the previous dataset
    with every citation still looking authoritative. `--check` re-derives to memory and
    compares; `check.sh` runs it, the same way it already re-derived `liberties.json`. The
    eight committed sidecars and the index were byte-identical on the first run, so this
    switched on with no repair behind it. What it does NOT check is the direction the
    staleness gate covers — that the GLB matches the record — and neither of them can see a
    record that is wrong about the town.

## Next

**S5 — more structure records**, which is now the binding constraint: seven structures stand
where the sources describe roughly forty, and one of the seven is a bridge. Note the coupling discovered on 2026-08-10, because it sets
the shape of the work: `tools/compile_scene.py` writes an `asset` path for every structure that
resolves into the scene, so a record committed without its GLB makes the renderer fetch a file
that is not there — a 404 the smoke correctly fails on. **A structure record and its bake are one
unit.** An agent without Blender can prepare the record and the research memo, but the pair has
to land together, so the bake workflow's PR is part of the same slice rather than a follow-up.
**That coupling is now enforced rather than remembered** (2026-08-10): editing a value a
generator reads makes the committed GLB stale and `check.sh` fails until the re-bake lands with
it. It was then exercised for real by the Wolf Point repair the same day — the rename turned the
tavern's asset stale on the spot and the branch could not go green until the bake landed on it,
which is the whole point of writing the check, and again the same day by Miller's second chimney,
and a third time by his frame range.
**The repair list refilled itself from the archive rather than from the gates, and emptied again
the same day** (2026-08-10, § 23 → § 24). Every previous entry on it was found by a check: a
misspelled attribute, a name read as being about the wrong half of a building. That one was found
by reading a page, and it is now **DONE** — the record, the archetype and the bake landed
together, `pier_count: 2` replaced `pier_spacing_m`, and the queue is empty again. What it leaves
behind is a shape worth reusing rather than a task: when evidence and an archetype disagree, check
whether the archetype is asking for the wrong *kind* of number before changing the number it has.
The older account of the queue, still true of everything before this entry: The last entry —
`miller_house` recording a `documented` frame range with no side, width, depth or storey count —
landed 2026-08-10 with its bake (§ 20), and it was the fourth and last of the faults the omission
gate opened. Three of the four were spelling; the fourth was a name read as being about the wrong
half of a two-part building, which no spelling check would have caught. Nothing new is queued
behind it, so **S5 is additions again**: eight archetypes and about forty researched structures
against the six that stand.

**S9 — streets, roads and paths**, **FIRST VISIBLE SLICE DONE 2026-08-11.** Seventeen dated
earth travelways are compiled from `data/streets/1835.json`, draped rather than flattened, and
identified live with their 1835 and 2026 names. The earlier sentence here saying "nothing was
graded until 1855-58" confused the later Raising of Chicago with early street work and was
wrong: South Water was ordered pitched by April 1834 and graded for drainage that July; South
Water and Lake were the two early principal improved routes. What remains is the north-side
control/extent research, any separately attested plank footwalks, and evidence that could replace
the conjectural travelled widths and rut patterns recorded in L79. See ROADMAP § S9.

**S5a — Fort Dearborn** — **DONE 2026-08-11**, both gates cleared before any geometry.
**The footprint has a source.** F. Harrison Jr.'s survey of the mouth of the Chicago River for
the harbour works, 24 February 1830, approved by William Howard, U.S. Civil Engineer, reproduced
in Andreas vol. 1 p. 113 and listed in that volume's own table of maps as "Fort Dearborn in
1830-32". It draws the fort IN PLAN — square enclosure, works at three angles, four ranges, two
gates, two buildings flanking the south gate — and its arrangement is corroborated building by
building by Gurdon Hubbard's 1827 walk round the inside (Andreas p. 264). Recorded as
`harrison_1830_river_mouth`. **The plate has no scale bar**, so the scale is derived from the one
stated dimension in the whole complex — the commandant's quarters at "about 25 x 50 ft" in the
1855 photograph key — giving 1.10 ft/px and a stockade about 53 m (174 ft) square at **±20 %**.
Two checks on the same plate agree to 5 % and 11 %. **The garrison is settled**: held
continuously from June 1832 to 29 December 1836, Maj. John Greene 5th Infantry most likely
commanding on the scene date, strength after 1833 unattested. Fourteen records, two new
archetypes (`palisade`, `fort_structure`), fourteen bakes, ~17,000 triangles. Five exclusions
went in with it, four of them wrong-fort findings. See `docs/RESEARCH/fort_dearborn.md`.
**What it did NOT settle and what is now the binding constraint: there is no ground under it.**

**S2e — extend the ground east to the lake.** Raised to the top of the terrain work on
2026-08-10 at Kevin's direction, after free-fly made it visible from the air: the modelled
box stops at local E +320, while the Fort Dearborn site is at E +1127 and the 1835 shore is
about a kilometre further still. Fort Dearborn and the harbour works cannot be placed until
the ground under them exists. The shoreline itself is a provenance problem before it is a
modelling one — everything east of roughly Michigan Avenue is later landfill, so the edge
must come off Wright 1834, not off a modern coast. See ROADMAP § S2e.

**Parcel (a) is done and parcel (b) is the next slice.** The shore is now traced
(`tools/trace_shoreline.py` → `shoreline.geojson`, memo
`docs/RESEARCH/shoreline_harbor_1834.md`) and it moved two numbers off estimate and onto
measurement: the mainland shore reaches local **E +1257** and the sand bar's east edge
**E +1497**, so the roadmap's proposed +1500 box would have clipped the bar by 3 m and the
box should be **+1560**. Two independent segmentations of the same sheet, in different windows
with different background statistics, agree in their 80 m overlap to **0.1–5.7 m** on the south
bank and **0.5–1.3 m** on the north — worth stating because it is evidence that the trace reads
the draughtsman's line and not its own thresholds. What is still absent: **no elevation exists
anywhere east of E +320**, the bar included. A bar is a surface a couple of feet of lake stage
moves and no source gives its height, so the number will have to be argued in the terrain spec
rather than picked. Until the heightfield and its bake land together, nothing east of the
current box renders and the aerial view's edge is unchanged.

**S2 remainder** — Frog Pond, the Wells Street marsh, and the rest of the hydrology beyond
the single traced slough centreline.

**S6 — flora and fauna records**, which is also what would retire liberty L2's promise: the
palettes and placement tables exist in the dossiers and nothing has been turned into data.

New findings for S2 from the datum work: Hathaway carries survey bearings and lot dimensions
("N.51°E." along the main stem, 80-ft streets annotated); both 1834 sheets are anisotropically
stretched (3.7% / 4.5%), so street geometry should be generated analytically from the plat
dimensions and snapped to the fitted control, never traced raw from pixels.
