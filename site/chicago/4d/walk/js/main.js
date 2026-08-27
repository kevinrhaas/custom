/**
 * main.js — boot, loop, and the test harness handle.
 *
 *   ?year=1835     which scene (default 1835)
 *   ?anchor=fort   start at a named camera anchor from the scene file
 *   ?data= ?assets=  override where the dataset lives
 *   ?debug=1       print budgets to the console after boot
 *
 * `window.__chicago4d` is the harness handle. `tools/smoke_renderer.mjs` drives
 * the real page through it: it is a view onto the running scene, not a parallel
 * code path, so a test that passes means the thing a visitor loads works.
 */

import * as THREE from 'three';

import { loadScene, resolveBases } from './scene-loader.js';
import { createWorld } from './world.js';
import { createTerrain, enuToWorld } from './terrain.js';
import { createBuildings } from './buildings.js';
import { createConfidenceView } from './confidence.js';
import { createIntent, createBackendSwitch } from './controls/intent.js';
import { createPointerLockBackend, isTyping } from './controls/pointerlock.js';
import { createTouchBackend, prefersTouch } from './controls/touch.js';
import { createWalker, footprintsFrom, decksFrom, WALK } from './walker.js';
import { createFlora } from './flora.js';
import { createTrees } from './trees.js';
import { createPopup } from './popup.js';
import { createHud } from './hud.js';
import { createNavigation } from './navigation.js';
import { createStreets } from './streets.js';
import { createEnclosures } from './enclosures.js';
import { createFencedGround } from './yards.js';
import { createSignage } from './signage.js';
import { createYardGoods } from './yard.js';
import { createFrontage } from './frontage.js';
import { createWharves } from './wharves.js';
import { createBoats } from './boats.js';
import { mountExclusions } from './exclusions.js';
import { mountFauna } from './fauna.js';
import { mountResidents } from './residents.js';
import { mountGround } from './ground.js';
import { mountGateCensus } from './census.js';
import { mountLiberties } from './liberties.js';

const VERSION = '0.1.0';

/**
 * T-0150 — HOW FAR DOWN A STREET THE DERIVED FURNITURE IS DRAWN AT `light`, IN
 * METRES, AND THE MEASUREMENT THAT SET IT.
 *
 * T-0149's first piece. T-0135 walked five named stands instead of one and found
 * the town far over every ceiling at the two AXIAL views — Lake Street east from
 * Canal, and the forks from Wolf Point — because a long open sightline is where
 * the 2026-08-21 chunking cannot help: nothing is behind the camera, so no chunk
 * is culled and every one of them is a draw call the sightline has to pay. The
 * owner raised the ceilings to carry it ("raise it, I think") and opened T-0149
 * to win the floor back by TRIMMING the axial view rather than by carrying it,
 * naming a furniture distance cull as the first thing to try.
 *
 * MEASURED BEFORE IT WAS SET, at the whole stand set and at both release
 * viewports, with `tools/measure_furniture_reach.mjs` — which drives the shipped
 * cull rather than a model of it, holds the clock so the wind is not measured as
 * a change, and reports a residual of the baseline against itself (0 everywhere)
 * so the deltas below are known to be signal. Source tree, `light`:
 *
 *   desktop 1280x800        drawn whole      at 350 m       saved   frame 48^2
 *   Lake at Canal, east   998,073 / 177   745,933 /  70   252,140 / 107   0.01 / 4
 *   the forks             990,772 / 156   782,316 /  71   208,456 /  85   0.00 / 0
 *   Lake and Market       733,530 /  99   682,216 /  77    51,314 /  22   0.00 / 0
 *   the open aerial       617,538 /  83   588,198 /  66    29,340 /  17   0.03 / 6
 *   the Sauganash at 26 m 590,322 /  68   582,882 /  62     7,440 /   6   0.00 / 0
 *
 *   mobile 390x780
 *   Lake at Canal, east   966,541 / 167   717,793 /  65   248,748 / 102   0.00 / 2
 *   the forks             933,656 / 138   743,432 /  63   190,224 /  75   0.00 / 0
 *   Lake and Market       565,060 /  78   555,970 /  70     9,090 /   8   0.00 / 0
 *   the open aerial       511,561 /  65   506,891 /  59     4,670 /   6   0.00 / 3
 *   the Sauganash at 26 m 542,696 /  59   541,424 /  57     1,272 /   2   0.00 / 0
 *
 * So the worst stand at `light` goes from 998,073 triangles and 177 draw calls
 * to 745,933 and 70 — a quarter of the geometry and SIXTY PER CENT OF THE CALLS,
 * for a frame that moves by a worst cell of 4 counts out of 255 where the gates
 * that prove a whole layer is visible need 6 and a mean of 0.30.
 *
 * WHY 350 AND NOT 300, WHICH IS THE FIGURE T-0149 NAMES. Both were measured. At
 * 300 m the worst stand gives another 5,954 triangles and 3 calls — and the OPEN
 * AERIAL, the only stand in the table whose picture changes at all, doubles from
 * mean 0.03 / worst 6 to mean 0.06 / worst 13, and then runs away to 0.18 / 23 at
 * 250 m. That stand is a camera 175 m up, so its slant range reaches the whole
 * town at once and the cull arrives everywhere in the frame together; it is the
 * one view where furniture leaving is something you could see. 350 m is the knee:
 * it keeps 252,140 of the 258,094 triangles and 107 of the 110 calls that 300 m
 * would win, and halves the only cost the instrument can find.
 *
 * WHY NOT 400, WHICH COSTS THE AERIAL NOTHING AT ALL (0.01 / 6). It leaves 28,904
 * triangles and 37 calls on the table at the worst stand for a reading the aerial
 * already matches at 350. The trade was taken toward the tier's own purpose,
 * which is the machine that needs the floor.
 *
 * THE PIXEL ARGUMENT, for the record and not as the bar. This camera is 62
 * degrees over 800 CSS pixels, so a 1.2 m fence pale subtends 739 · 1.2 / d
 * pixels: 2.5 at 350 m, 2.2 at 400 m, 3.0 at 300 m. That is the intuition — a
 * pale at this range is a couple of pixels of a line — but the number above was
 * set from the frame measurement, because "how many pixels tall is a pale" and
 * "does the picture change when the fence goes" are different questions and only
 * the second one is the one being answered.
 */
const FURNITURE_REACH_LIGHT_M = 350;

/**
 * Scene detail: how much geometry the visitor asks for.
 *
 * 600 000 triangles used to be a single hard ceiling written into the release
 * gate, and it had quietly become an architectural constraint — the reason a
 * finished parcel of buildings could not be added was a number, not a machine.
 * A ceiling is the wrong instrument for that. It is now a CHOICE with three
 * settings, the gate holds each one to ITS OWN ceiling, and the town can grow
 * into the top of the range while anyone on a slow machine steps down.
 *
 * `densityScale` scales the flora and tree CAPS only — the same species in the
 * same places, fewer of them. It never changes where a plant may stand, which
 * is evidence rather than performance. Buildings, terrain and the river do not
 * scale at all: the reconstruction is not allowed to get less true because a
 * machine is slow, so what gives way is the sward, which is the only layer whose
 * count is a rendering decision rather than a claim.
 *
 * ---------------------------------------------------------------------------
 * T-0115 — WHY THE SWARD ALONE COULD NOT HOLD THE BOTTOM RUNG, AND WHAT ELSE
 * GIVES WAY NOW.
 *
 * The paragraph above is the design as written, and by August 2026 it had
 * stopped being arithmetically possible. Measured on the published mirror at
 * the release gate's own stand (`frame('sauganash_hotel', 26)`), desktop:
 *
 *   full     850,657 of 1,000,000    85 % of its ceiling
 *   balanced 769,279 of   800,000    96 %
 *   light    668,293 of   600,000   111 %  — over, and the reason for T-0115
 *
 * The ladder PROMISES a 40 % step from `full` to `light` — that is what
 * 1,000,000 → 600,000 says. It DELIVERED 21.4 %. It could not deliver more,
 * because the setting had a lever on only 39 % of the frame: flora and trees.
 * The other 61 % — terrain, buildings, streets, fences, yard goods, plank
 * walks, signboards, wharves, boats, and the sun's second pass over all of
 * them — was drawn identically at every level. **A 40 % cut cannot be taken
 * out of 39 % of a scene.** Everything the town grew after the tiers were
 * written was grown outside the tiers' reach, which is exactly how the ceiling
 * eroded: nothing was wrong with any one merge, and the control had no hold on
 * any of them.
 *
 * The ceiling is NOT re-budgeted. What is added is two more things that give
 * way at `light`, chosen by the same test the sward passes — a rendering
 * decision rather than a claim — and both of them are the SUN rather than the
 * town:
 *
 *   `shadowReachM` — how far from the visitor the sun's shadow is cast. At
 *   `light` the box steps back to the ±120 m this project shipped between
 *   R-W3b(a) and R-W5a2, and the map halves with it so the TEXEL is unchanged
 *   (world.js `setShadowRig`). Nothing a visitor stands next to gets softer;
 *   what the step costs is reach — past 120 m the town meets the ground with
 *   nothing under it — and it also quarters the shadow map's memory, which is
 *   the largest single GPU allocation this scene makes and the one a weak
 *   machine feels first.
 *
 *   `furnitureCastsShadow` — whether the DERIVED FURNITURE casts into the
 *   shadow map at all. A fence, a barrel, a plank walk, a dock and a moored
 *   hull are drawn from committed records and their PRESENCE is a claim; the
 *   stripe each one lays on the ground is lighting, and lighting is not a
 *   claim. At `light` they stand exactly where they stand, drawn exactly as
 *   they are drawn, still RECEIVING the shadows of the buildings and the timber
 *   around them — they just stop being drawn a second time for the sun.
 *   Buildings, terrain and the timber keep casting at every level: a town whose
 *   houses and trees met the ground with nothing under them is the defect
 *   R-W3b(a) exists to have fixed, and this does not reopen it. The hanging
 *   signboards keep casting too, and FURNITURE_LAYERS below says why with the
 *   measurement that decided it.
 *
 * Measured together at the same stand: desktop 668,293 → 584,761 of 600,000,
 * 55 → 49 draw calls. Recorded in docs/LIBERTIES.md L156, which is L121's
 * entry for the wood one layer over.
 *
 * ---------------------------------------------------------------------------
 * T-0067 — AND THE THIRD THING THAT GIVES WAY, WHICH IS TIMBER RATHER THAN SUN.
 *
 * T-0115's ledger left two costed findings for whoever took the fence tickets,
 * and this is the second of them: a picket pale is a 10-triangle prism whose two
 * 22 mm edge faces and 22 mm top cap are SIX of those ten — three quarters of
 * the geometry for a fortieth of the silhouette. At `light` a pale is drawn as a
 * zero-thickness double-sided plank instead (`enclosures.js` `pushBox`), which
 * is 4 triangles: same width, same height, same place, same rhythm, and a
 * thickness you could only see by standing on the fence line and looking along
 * it. It passes the same test the sward and the shadow reach pass — a rendering
 * decision rather than a claim — and it is the lever that keeps the fence
 * tickets affordable, because every pale T-0067, T-0068 and T-0069 add now costs
 * 4 triangles at `light` rather than 10.
 *
 * T-0068 extended the same plank to `balanced`, and for the tier's own sake: the
 * middle tier had never taken anything off this layer, so a pale cost the same
 * ten triangles there as at `full` and the town's fences scaled identically at
 * both. With 3.5 km of lot line on the layer that put `balanced` at 794,000 of
 * its 800,000 while `full` sat 150,000 clear of its own — a ceiling doing no
 * work. `balanced` now gives up the 22 mm, worth about 56,000 triangles, and
 * `full` still draws the prism. `enclosures.js` `PLANK_LEVELS` is where that
 * lives, and no triangle ceiling moved to pay for any of it.
 *
 * (T-0115's FIRST finding, chunking the town-wide fence mesh so the frustum can
 * cull it, is not a tier at all — it costs a visitor nothing at any level and is
 * simply how `enclosures.js` builds now.)
 *
 * ---------------------------------------------------------------------------
 * T-0135, 2026-08-22 — THE CEILINGS RE-ARGUED AGAINST THE WORST STAND, AND
 * DELIBERATELY NOT MOVED.
 *
 * Every figure above, and every figure in `BUDGET` below, was read at ONE
 * camera: `frame('sauganash_hotel', 26)`. The release gate now walks a named set
 * of five stands and holds each tier to its ceiling at the worst of them
 * (`tools/smoke_renderer.mjs` `STANDS`, where each stand's reason is written).
 * This is the first reading of that set — source tree, 1280x800, desktop:
 *
 *                              full        balanced      light      light calls
 *   Lake at Canal, east    1,320,377     1,144,787     992,617          177
 *   the forks, Wolf Point  1,318,202     1,137,646     984,612          156
 *   Lake and Market        1,112,086       943,776     729,844           99
 *   the open aerial          971,455       808,920     615,266           83
 *   the Sauganash at 26 m    960,515       815,021     587,798           68
 *   ---------------------------------------------------------------------
 *   ceiling                1,000,000       900,000     600,000       80 (floor)
 *
 * Worst draw calls, `full`: 200 at Lake at Canal against a budget of 140.
 *
 * SO THE TOWN IS 32 % OVER AT `full`, 27 % OVER AT `balanced` AND 65 % OVER AT
 * `light` at the stands a visitor can walk to — and it was over before this
 * ticket, and before any of the four parcels that raised the ceiling on
 * 2026-08-21. Nothing regressed here. What changed is that something finally
 * looked.
 *
 * THE NUMBERS ARE NOT MOVED, and that is a decision rather than an oversight.
 * AGENTS.md's own ruling has two halves and this run can only honour one of
 * them. "Just raise it" is the first half; "`light` is the floor and stays the
 * floor" is the second, and raising `light` to carry 992,617 would put the
 * bottom rung ABOVE the ceiling `full` carries today. That is not a re-budget,
 * it is the ladder ceasing to exist — and the tier a weak machine boots into is
 * the one promise in this table that is made to a person rather than to a
 * number. Raising `full` and `balanced` while `light` sat 65 % over would be
 * worse still: a ceiling moved to fit the camera that flatters it, which is the
 * exact defect T-0135 was opened to end.
 *
 * The ladder itself still works — 25 % from `full` to `light` at Lake at Canal
 * against 39 % at the reference stand — so the honest reading is that the
 * ceilings were authored as REFERENCE-STAND numbers and the scene has outgrown
 * the shape of the question, not merely its answer. The two routes T-0135 names
 * are both open (raise, or trim the axial view to fit), and choosing between
 * them is the owner's: it trades a promise about weak machines against a
 * rendering programme. Recorded here, at the definition site, per the ruling's
 * third half — MEASURE, THEN MOVE. This is the measure. The move is his.
 */
const DETAIL = {
  // RAISED 2026-08-22 TO CARRY THE WORST STAND, ON THE OWNER'S RULING ("raise
  // it, I think"), and this is the entry that says what it cost. T-0135 built
  // the instrument that walks five named stands instead of one and found the
  // town 32% over at `full`, 27% at `balanced` and 65% at `light` — at
  // viewpoints the Go-to menu already offers. Nothing had regressed; the
  // ceilings were authored as reference-stand numbers and only the reference
  // stand was ever measured.
  //
  // WHAT WAS GIVEN UP, SAID PLAINLY: `light` now carries 1,050,000, which is
  // MORE than `full` promised the day before this commit. The bottom rung is
  // heavier than the old top rung, so `light` is no longer a floor a weak
  // machine can be promised — it is merely the cheapest of three expensive
  // tiers. That was the trade the owner took knowingly, and T-0149 exists to
  // win the floor back by trimming the axial view (distance culling or an LOD
  // down a long street) rather than by pretending the number is small.
  //
  // These are worst-stand numbers now, not reference-stand numbers, with about
  // 6% of headroom over the measured worst. The next parcel that breaches them
  // is breaching a bar that means something.
  //
  // T-0150, 2026-08-23 — AND THE FIRST INSTALMENT ON THAT DEBT IS PAID, THOUGH
  // NOT THE CEILINGS THEMSELVES. `furnitureReachM` below distance-culls the
  // derived furniture at `light` only, and the worst stand now reads 745,933
  // triangles and 70 draw calls where it read 998,073 and 177 — so the bottom
  // rung has stopped being the heaviest thing this project ever shipped, and
  // `light` sits 29% under its own ceiling instead of 5%. The NUMBERS in this
  // table are deliberately untouched all the same: re-lowering them is T-0147,
  // and it is a separate ticket precisely so that the trim has to be measured
  // before the ceiling is allowed to follow it down. A ceiling lowered in the
  // same breath as the trim that justified it is a ceiling nobody checked.
  full:     { triangles: 1400000, shadowReachM: 240, furnitureCastsShadow: true,
              furnitureReachM: null },
  // RE-BUDGETED 2026-08-21, 800000 -> 900000, on the owner's ruling that a
  // ceiling is a number this project chose rather than a claim about 1835.
  // Four parcels landed the same day - the street edge, the lot-line fences,
  // the fenced ground and sixty-four wagons - and stacked they read 814,860
  // here where each alone had fitted. The old figure was set before any of
  // them existed and nothing re-measured it as the town filled in. `light`
  // is UNTOUCHED at 600000 and still passes: the tier a weak machine boots
  // into keeps its floor, and this raise is spent only by machines that
  // asked for the middle setting.
  //
  // RE-BUDGETED AGAIN 2026-08-24, 1210000 -> 1225000 (T-0098), and the entry
  // above asked for exactly this to be justified: "the next parcel that
  // breaches them is breaching a bar that means something." It measured what
  // the bar means before moving it, twice, at the release smoke's own worst
  // stand (Lake Street at Canal, east down the axis, desktop 1280x800):
  //
  //   dev alone, this parcel unmounted     1,209,926 of 1,210,000   PASS by 74
  //   dev plus a twelve-stem tree stand    1,213,446 of 1,210,000   FAIL by 3,446
  //
  // SEVENTY-FOUR TRIANGLES. That is a quarter of one tree, on a frame of 1.2
  // million. The bar had not been reached by a parcel that overspent it; it had
  // been reached, full stop, and the next VISIBLE parcel of any size at all was
  // going to fail it whatever it was - which is a fact about the ceiling and not
  // about the parcel that found it. `full` was measured in the same runs with
  // 16,852 (1.2 %) of headroom, so the ladder was not uniformly full: the middle
  // rung alone had been squeezed to nothing.
  //
  // WHERE 1,225,000 COMES FROM, so it is a principle and not "enough for me":
  // it gives `balanced` the same PROPORTIONAL headroom `full` carries today
  // (about 1 %) over the measured worst stand WITH this parcel in. The ladder
  // keeps its shape; nothing was chosen to fit one record.
  //
  // WHAT WAS NOT DONE, and both halves matter. `light` IS UNTOUCHED at 1050000
  // and reads 815,777 - 22 % under its own ceiling. The floor a weak machine
  // boots into is not spent here, which is the standing constraint on every
  // re-budget this table has taken. And this raise does NOT buy room for the
  // parcel after this one: it restores about 1 % and no more, and the trim that
  // would actually win the middle rung back is still T-0149 (the axial view) and
  // T-0147 (the ceilings that follow a trim down). A ceiling raised to carry one
  // record is not a ceiling anybody should spend twice.
  // SUPERSEDED 2026-08-27, and the re-budget above is DEFERRED rather than
  // dismissed: it was careful reasoning that later measurement overtook, twice.
  //
  //   (i)  It rests on `balanced` measuring 1,213,446 at the worst stand. dev
  //        measures 1,252,802 there today, so 1,225,000 no longer clears the
  //        breach it was raised to clear. It also rests on `full` carrying
  //        1.2 % headroom; `full` is now OVER, at 1,412,120 of 1,400,000. Both
  //        halves of the proportional-headroom argument have moved.
  //   (ii) T-0209 measured what actually occupies the frame, which nobody had:
  //        `trees` draws 360,926 triangles out of 181,900 it owns -- the whole
  //        layer twice -- because trees.js submits kilometre-wide quadrant
  //        meshes whole to a +/-240 m shadow box. 180,100 triangles, 14.4 % of
  //        the frame, cast nothing any pixel of the shadow map can hold.
  //
  // Re-basing a ceiling with that still in it budgets for work the renderer
  // should not be doing, and it would be the fifth raise. So the number stays
  // at 1,210,000 and the budget question lives entirely in T-0209, which orders
  // the trim first and the ceiling after. The tree stand this parcel adds ships
  // regardless; its own smoke leg is red on dev with or without it.
  balanced: { triangles: 1210000, shadowReachM: 240, furnitureCastsShadow: true,
              furnitureReachM: null },
  light:    { triangles: 1050000, shadowReachM: 120, furnitureCastsShadow: false,
              furnitureReachM: FURNITURE_REACH_LIGHT_M },
};
const DETAIL_ORDER = ['full', 'balanced', 'light'];
/**
 * THE DRAW-CALL BUDGET, RAISED FROM 80 TO 120 ON 2026-08-21 — a conscious
 * re-budget, written down here where the number is set, and never a silent one.
 *
 * THE OWNER'S RULING, verbatim: *"ok to raise the draw call budget, if you need
 * to make that a user friendly option in settings because it wont work on some
 * machines but will on others/most then that is ok"* — and immediately after,
 * *"or just raise the budget?"*. No new setting was built: the scene-detail
 * control below IS the user-facing option, and `light` remains the floor a weak
 * machine has to hold, inside its own unchanged 600,000-triangle ceiling.
 *
 * WHY 80 STOPPED MEANING WHAT IT MEANT. It was set when every derived layer was
 * ONE mesh — one fence mesh for the whole town, one plank-walk mesh, one yard
 * mesh — and a draw call was a thing to be hoarded. T-0115 measured what that
 * cost: a mesh spanning Chicago has a bounding sphere no frustum can cull, so
 * 33,166 triangles of fence were drawn in every frame including the fences
 * behind the camera. T-0067, T-0119 and T-0069 all took the same remedy and
 * chunked their layers, which DELIBERATELY converts triangles into draw calls —
 * and the sun's own pass draws every chunk inside its ±240 m box a second time,
 * so a chunk costs two. The triangle ceilings are the tiers a visitor chooses
 * between and they are unchanged; the call count is the price of the culling
 * that keeps those ceilings reachable, and holding it at 80 would mean giving
 * back the culling.
 *
 * MEASURED, at the release gate's own stand (`frame('sauganash_hotel', 26)`),
 * desktop, published mirror: 65 calls before T-0069's street edge and **78**
 * after it — inside the old 80, and with nothing left. That is the number this
 * raise is against: not a parcel that overran, but a budget with two calls of
 * headroom in a town that is still being built. 120 is half again the measured
 * worst, which is the same order of margin the triangle ceilings carry.
 *
 * WHAT WOULD MAKE IT SMALLER AGAIN, costed and not done here (T-0115's ledger,
 * T-0127): a plank walk lies 11 cm proud of the ground and its own shadow is
 * about 4 cm wide at noon. If the ground-hugging furniture stopped casting into
 * the shadow map while the standing furniture kept casting, the frontage layer's
 * six shadow-pass calls at this stand would go for nothing a visitor can see.
 * That needs a per-mesh opt-out in `applyShadowTier` and a smoke check that
 * counts the exempt meshes rather than assuming every furniture mesh casts.
 *
 * RECONCILED 2026-08-21, and the number stands at 120. Two parcels raised this
 * ceiling the same afternoon, each measuring only itself against dev: the street
 * edge (T-0069) read 78 calls and chose 120; the lot-line fences (T-0068) read 79
 * and chose 96. Neither had seen the other. Merged they stack — dev's 65 plus
 * roughly thirteen for the walks and fourteen for the fences — so 96 would have
 * been spent almost the moment both landed, which is how a ceiling comes to be
 * re-raised twice in a week. 120 is kept because it is the number with room in
 * it, and because the argument below is about what a ceiling is FOR, not about
 * the one parcel that happened to reach it first.
 */
// 120 -> 140 for the same reason and on the same day: the four parcels above
// read 121 calls together, one past a ceiling reconciled hours earlier from two
// parcels that had each measured only themselves. Chunking is what spends calls
// - it trades a draw call for the frustum's right to skip geometry - so the
// number climbs as layers learn to cull. 140 carries the measured 121 with room
// rather than the single call that would have to be re-argued tomorrow.
//
// T-0135, 2026-08-22 — AND 140 IS NOT MOVED EITHER, FOR THE REASON THE TABLE IN
// `DETAIL` ABOVE GIVES. Read at the release gate's new stand set rather than at
// the Sauganash alone, the worst frame is 200 calls at `full` down Lake Street
// from Canal, and 177 at `light` against a floor of 80 that has stood since
// before any layer was chunked. Every raise this ceiling has taken — 80 to 120
// to 140, all on 2026-08-21 — was argued against a camera that reads 121, so
// the honest thing to say is not "140 is too low by 60" but "nobody has ever
// budgeted this scene; they budgeted one view of it." Moving the number today
// would be the fourth raise in two days and the first one aimed at a reading
// taken specifically to show that raising to fit the reading is the bug. The
// gate is red at the worst stand on purpose. See T-0135.
// 140 -> 215 on the same ruling and the same measurement: the worst stand draws
// 200 calls at `full` where the reference stand drew 121. Chunking is what
// spends calls down a long street, and T-0149 is where that gets traded back.
const BUDGET = { drawCalls: 215, triangles: DETAIL.full.triangles };

/**
 * THE DERIVED FURNITURE — which layers `furnitureCastsShadow` governs, by the
 * name each one gives its own group.
 *
 * What they have in common is the thing that makes the rule defensible: every
 * one is small timber (or a small hull) built at load from a committed record
 * rather than baked, standing ON the town rather than being the town.
 * `structures`, `terrain`, `streets`, `trees` and `flora` are deliberately not
 * in this list — the first three are the reconstruction itself, and the last
 * two already give way through their own density.
 *
 * AND `signage` IS NOT IN IT EITHER, which is the one exception and was decided
 * by a measurement rather than by taste. A hanging board is the only furniture
 * in this town whose whole function is to be READ, from the street, at a few
 * metres — and the shadow it throws is what lifts it off the wall it is bolted
 * to. Dropping it from the shadow map cost exactly that: with the boards no
 * longer casting, hiding the whole signage layer moved the release gate's own
 * 12-cell signature at the Tremont's footway by mean 0.28 against its 0.30 bar,
 * where the same measurement reads 0.72 with the shadow in — so the shadow was
 * most of what the board was contributing to the frame. Keeping the boards
 * casting cost 1,380 triangles of this tier's 84,912-triangle saving: 1.6 % of
 * the saving, 0.2 % of the tier, for the only piece of furniture the visitor is
 * meant to look directly at. It costs 1,106 since T-0066 gave the signs their
 * names — a painted band is two triangles where a bracket board is sixty, and
 * the lettering itself is a texture atlas rather than geometry.
 */
const FURNITURE_LAYERS = ['enclosures', 'yard', 'frontage', 'wharves', 'boats'];

/**
 * THE NEAR PLANE, AND WHY IT MOVES WITH ALTITUDE — ROADMAP R-BUG1.
 *
 * The owner reported the river's edge flickering when flying, and it is the
 * depth buffer running out of numbers. A perspective depth buffer spends its
 * precision near the camera: the smallest depth difference it can tell apart at
 * a distance z is about z² / (near · 2^bits). At the fixed 0.1 m near this
 * camera used to carry, two surfaces 350 m away had to be **10 cm** apart in
 * depth before the buffer could say which was in front — and the river's edge
 * is the one place in this scene where two surfaces are exactly co-planar by
 * design (`terrain.js`: the bank line IS where the ground crosses y = 0, so the
 * waterline can never drift out of step with the traced river). Inside that
 * band the winner is decided by rounding, and a camera that moves two
 * millimetres re-rolls it. That is the shimmer.
 *
 * Moving the near plane out with altitude fixes the CAUSE rather than picking a
 * winner. The alternative — a `polygonOffset` on the water — would settle the
 * tie by biasing the water toward the camera, and at 350 m one depth step is
 * ~10 cm of ground: the drawn waterline would climb the bank by up to that
 * much, which breaks the invariant the design exists to guarantee. Precision
 * costs nothing and moves no edge.
 *
 * `min` is the walking value and is unchanged: `altitude` is the eye's height
 * above the ground under it and is 0 on foot, so a walker gets exactly the
 * camera they had before. `divisor` keeps the near plane at a twenty-fifth of
 * the way to the ground — two orders inside anything the visitor could fly
 * close to — and `max` caps it so that a low pass beside a building cannot clip
 * its wall. `step` quantises the value so the projection matrix is rebuilt on a
 * change worth having rather than every frame.
 */
const NEAR = { min: 0.1, max: 8, divisor: 25, step: 0.05 };

/** The visitor's stored choice, read straight from the HUD's own settings blob so
 *  the two cannot disagree about which level is selected. Returns '' when they
 *  have never chosen, which is what lets the device guess stand. */
function readDetailPreference() {
  try {
    const raw = window.localStorage.getItem('chicago4d.settings');
    const level = raw ? JSON.parse(raw).detail : '';
    return DETAIL[level] ? level : '';
  } catch {
    return '';
  }
}

const params = new URLSearchParams(location.search);
const YEAR = (params.get('year') || '1835').replace(/[^0-9a-z_-]/gi, '');
const DEBUG = params.get('debug') === '1';

const canvas = document.getElementById('view');
const gate = document.getElementById('gate');
const gateBtn = document.getElementById('gate-btn');
const gateSub = document.getElementById('gate-sub');
const gateBar = document.getElementById('gate-bar');

/**
 * Loading progress, driven by the boot's REAL stages rather than by a timer.
 * A timer-driven bar tells a visitor nothing except that time is passing, which
 * they already know; this one only moves when something has actually finished,
 * so a bar that stops IS the diagnosis.
 */
function progress(pct, label) {
  if (gateSub && label) gateSub.textContent = label;
  if (!gateBar) return;
  const fill = gateBar.firstElementChild;
  if (fill) fill.style.width = `${Math.max(0, Math.min(100, pct))}%`;
  gateBar.setAttribute('aria-valuenow', String(Math.round(pct)));
  if (pct >= 100) gateBar.classList.add('done');
}
const hudRoot = document.getElementById('hud');
const popupRoot = document.getElementById('popup');

const problems = [];

/** The harness handle. Populated as boot proceeds so a failure is still legible. */
const api = {
  version: VERSION,
  three: THREE.REVISION,
  year: YEAR,
  ready: false,
  error: null,
  scene: null,
  datum: null,
  registry: new Map(),
  player: { e: 0, n: 0, y: 0, bearingDeg: 0, pitchDeg: 0, speed: 0, moving: false,
            altitude: 0, flying: false },
  problems,
  budget: BUDGET,
  // The town's own two numbers, as the gate showed them (T-0036). Null until the
  // census resolves, and null forever if it could not be read — the smoke asserts
  // the DISPLAYED figures against this, so a silent failure reads as one.
  census: null,
};
window.__chicago4d = api;

boot().catch((err) => {
  api.error = String(err?.message || err);
  problems.push(`boot: ${api.error}`);
  if (gateSub) gateSub.textContent = `Could not load the scene — ${api.error}`;
  if (gateBtn) gateBtn.textContent = 'Failed to load';
  console.error('[4D Chicago] boot failed', err);
});

async function boot() {
  const bases = resolveBases();
  const coarse = prefersTouch();

  /**
   * MULTISAMPLING, ON EVERY DEVICE INCLUDING A PHONE (T-0157).
   *
   * This read `antialias: !coarse` from Milestone 0 — the first commit of this
   * renderer, before there was a town to look at — so every touch device drew
   * the whole reconstruction with no multisampling at all. Nobody had ever
   * measured what that costs a phone: T-0013 established that all 627
   * interior-flickering pixels at `from_above` are edges and that only sample
   * density touches them, but every one of its readings was taken at 1280×800
   * on the DESKTOP boot, where MSAA was already absorbing most of it.
   *
   * `tools/measure_phone_aa.mjs` measures the phone, at 390×780 in a context
   * with `hasTouch` — which the release gate uses and which `TIE_VIEWPORT=mobile`
   * does not, so the older instrument had been booting the desktop renderer in a
   * narrow window. Published mirror, 2 mm nudge, shadow map off, control and
   * return-to-pose both 0 px:
   *
   *              flicker px      HARD FLIPS (a pixel that moved ≥ 64 of 255)
   *   from_above   1056 → 2482        25 → 0
   *   lake_market  4843 → 7310       124 → 0
   *
   * READ THE SECOND COLUMN, AND NOTE THAT THE FIRST ONE ARGUES THE OTHER WAY.
   * The flicker COUNT — the number T-0013 and three boxes of ROADMAP quote —
   * goes UP by 135 % aerial and 51 % at eye height when MSAA is switched on,
   * because a partial resample touches more pixels than a whole flip does. A run
   * that had measured only the count would have refused this. What actually
   * happens is that the SEVERITY collapses: the worst per-pixel movement falls
   * 105 → 28 aerial and 140 → 37 at Lake and Market, the mean 15.6 → 6.8 and
   * 14.8 → 6.4, and every one of the 149 pixels that were swapping surface
   * outright stops doing it. That is precisely the difference between an edge
   * that crawls and an edge that is resolved.
   *
   * WHAT IT COSTS, AND THE HONEST LIMIT OF THAT FIGURE. Timed over the ten scene
   * anchors the release gate walks, clock held, A/B/A: **+56 % of a frame**
   * (24,457 → 43,283 ms summed, against a mean-of-A baseline), with the runner
   * itself drifting +26 % between its two A passes — so the true reading is
   * "roughly half a frame again", not a digit. It is measured through ANGLE's
   * SwiftShader, a SOFTWARE rasteriser, which resolves every sample on the CPU
   * with no tile memory: that is the harshest possible witness for this change
   * and the figure is an UPPER bound. **The cost on real phone silicon was not
   * measured and is not claimed.**
   *
   * The floor is untouched and the escape hatch already ships. A phone still
   * boots into the `light` scene-detail tier, unchanged; and Render quality in
   * Settings drops the pixel ratio to 1, which cuts the multisampled pixel count
   * by 56 % — measured at 4 stations rather than asserted, see STATUS.md.
   */
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: 'high-performance',
    stencil: false,
  });
  /**
   * The boot-time ratio. Note that this is superseded a few hundred lines below
   * by `renderer.setPixelRatio(Math.min(dpr, hud.settings.quality))` once the
   * visitor's stored settings are read, and the shipped default of `quality` is
   * **1.5 on both platforms** — so the `: 2` here reaches a fresh visitor's
   * screen for the handful of frames before the HUD mounts and nowhere else.
   * T-0157's premise held that a phone was capped at 1.5 "rather than 2"; what
   * the renderer actually reports is 1.5 on a phone at dpr 2 and 1.0 on a
   * desktop at dpr 1, which is the phone supersampling MORE than the desktop.
   */
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, coarse ? 1.5 : 2));

  const scene3d = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(62, 1, NEAR.min, 3000);

  progress(8, 'Reading the scene…');
  // The gate's two numbers (T-0036). Started here and NOT awaited: it is one
  // small JSON beside a scene load that fetches hundreds of files, and the row
  // it fills sits above the progress bar — a visitor should be reading how big
  // the town is while the town loads, not after. It fails soft to a hidden row,
  // so nothing downstream depends on it and no rejection reaches the boot chain.
  const census = mountGateCensus({ dataBase: bases.dataBase }).then((c) => {
    api.census = c;
    return c;
  }).catch(() => null);
  const loaded = await loadScene(YEAR, bases);
  progress(30, 'Placing the buildings…');
  problems.push(...loaded.problems);
  api.scene = loaded.scene;
  api.datum = loaded.datum;
  api.registry = loaded.registry;

  const world = createWorld({
    renderer, scene: scene3d, sceneJson: loaded.scene, datum: loaded.datum, lowSpec: coarse,
  });

  const confidence = createConfidenceView();

  // The ground, the river, and the heightfield the walker stands on, all from
  // the scene's terrain epoch. Awaited: everything after this asks it how high
  // the ground is, and a flat answer would place every building at the datum.
  const terrain = await createTerrain({
    dataBase: bases.dataBase,
    assetBase: bases.assetBase,
    epochId: loaded.scene.terrain_epoch,
    confidence,
    problems,
  });
  scene3d.add(terrain.group);
  progress(55, 'Laying the ground and the river…');

  const buildings = createBuildings({ registry: loaded.registry, confidence, terrain });
  problems.push(...buildings.problems);
  scene3d.add(buildings.group);

  const footprints = footprintsFrom(loaded.registry);
  // The bridge decks, which are the one walkable surface the heightfield does not
  // carry — the wall you are kept out of and the deck you stand on are the same
  // polygon read two ways, so both come off the same footprints. T-0001.
  const decks = decksFrom(loaded.registry);
  const spawn = anchorFor(loaded.scene, params.get('anchor')) ?? loaded.scene.spawn ?? {};
  const walker = createWalker({ camera, terrain, footprints, decks, spawn });
  walker.apply();

  // The dated street layer is a skin on the heightfield, never a replacement
  // for it.  Mount it before vegetation so the travelled strips can clear only
  // the plants that would otherwise grow through the visible wagon tracks.
  const streets = createStreets({
    terrain,
    records: loaded.index?.streets ?? [],
    confidence,
  });
  scene3d.add(streets.group);

  // WHICH DETAIL LEVEL, resolved here rather than beside the vegetation because
  // the fence layer is the first thing that needs it: a pale is 10 triangles at
  // `full` and 4 at `light` (T-0067), so the level has to be known before the
  // first fence is built. A phone starts at `light` and a desktop at `full`; the
  // visitor's own choice, once made, outranks the guess and is what
  // `hud.settings.detail` carries.
  let detailLevel = DETAIL[readDetailPreference()] ? readDetailPreference()
    : (coarse ? 'light' : 'full');
  const detailOpts = () => ({ detail: detailLevel });

  // The town's fence lines — yards, pens, garden pickets. An enclosure takes a
  // PERIMETER rather than a footprint and is roofless, which is why it is not a
  // structure record and carries no GLB: docs/LIBERTIES.md L10 and L60 have both
  // been waiting on exactly that shape, and this is the half of it that needs no
  // bake. Mounted after the streets so a frontage fence is drawn against the
  // travelled way it stands on, and before the vegetation because the ground
  // inside one now decides what may grow there — see the fenced ground below.
  const enclosures = await createEnclosures({
    dataBase: bases.dataBase, terrain, confidence, problems, ...detailOpts(),
  });
  scene3d.add(enclosures.group);
  api.enclosures = enclosures;

  /**
   * THE GROUND INSIDE THOSE FENCES (T-0067). The owner: *"everplace that is
   * fenced in would have a different ground, the wagon yard would probably be
   * dirty dusty ground and fences around properties inside the fence would not
   * be wild prairie but curated lawn and garden or animal pens."* Three of the
   * four enclosure records said the same thing about themselves, in their own
   * `ground` blocks, with `geometry: "absent"`.
   *
   * It is its own layer and its own scene child rather than a second mesh inside
   * `enclosures` for two reasons that are both about policy rather than tidiness:
   * a ground treatment casts no shadow and must not be swept into
   * FURNITURE_LAYERS' traverse, and hiding the FENCE (which several gates do) must
   * not take the ground with it. It takes the enclosure records straight off the
   * layer above rather than re-fetching them.
   */
  const yards = createFencedGround({
    records: enclosures.records, terrain, confidence, problems,
  });
  scene3d.add(yards.group);
  api.yards = yards;

  // The boards the businesses hung out over the footway. Like a fence, a
  // signboard is derived geometry rather than baked geometry — a plank on a
  // bracket hanging off a wall the GLBs already draw — so it needs no bake
  // either (T-0039). Mounted after the buildings it hangs on, and its height is
  // measured from the same wall base `buildings.js` anchors them at.
  const signage = await createSignage({
    dataBase: bases.dataBase, terrain, confidence, problems,
  });
  scene3d.add(signage.group);
  api.signage = signage;

  // The goods a working town left standing on its own ground — barrels and
  // cases on the footway at the taverns and the stores, and one wagon in the
  // yard a source calls a wagon yard (T-0040). Derived geometry like the fences
  // and the boards, so it needs no bake either. Mounted AFTER the signage
  // because the two are derived from the same wall and deliberately share it:
  // the board hangs 1.7 m one side of the facade's centre and the goods pile
  // from the other end. Unlike a board, a barrel stands on the TERRAIN rather
  // than on the building's wall base — it is resting on the ground it is on.
  const yard = await createYardGoods({
    dataBase: bases.dataBase, terrain, confidence, problems,
  });
  scene3d.add(yard.group);
  api.yard = yard;

  // The frontage works — the plank walks along a building's street walls, the
  // board crossing over the road and the named board on its post at the corner
  // (T-0082). Derived geometry like the fences, the boards and the goods, so it
  // needs no bake — but it is the first layer derived from a building AND a
  // street at once: where a walk may lie is decided by the travelled track's own
  // half-width out of data/streets/1835.json. Mounted after the yard because the
  // two divide one building's ground between them — the yard layer owns what
  // stands on its own lot and this owns what lies in the street outside it.
  const frontage = await createFrontage({
    dataBase: bases.dataBase, terrain, confidence, problems,
  });
  scene3d.add(frontage.group);
  api.frontage = frontage;
  /**
   * A walk that RIDES a committed deck registers its planks as a surface the
   * walker stands on (T-0119): the river walk's crossing footway lies over the
   * State slough's water at the mouth, where the terrain answers with the
   * wading barrier and only a deck may carry a visitor. The walker holds
   * `decks` by reference, so appending here is enough — and the planting
   * composition below picks the same rectangles up with the rest of `decks`.
   */
  for (const d of frontage.walkableDecks ?? []) decks.push(d);

  // The river docks at the two forwarding warehouses whose own records state
  // one (T-0041). Derived geometry like the fences, the boards and the goods, so
  // it needs no bake — but it is the first of these layers that stands OVER THE
  // WATER, and that is where its one hard rule comes from: the deck top is the
  // terrain's own height at the landward edge and each crib bent is stepped down
  // to the bed under it, so nothing here floats and nothing is drawn on a number
  // authored beside the mesh instead of taken from it. Mounted after the yard
  // for reading order; the two never touch, because the goods stand on the
  // town's trading frontages and the docks are out on the bank.
  const wharves = await createWharves({
    dataBase: bases.dataBase, terrain, confidence, problems,
  });
  scene3d.add(wharves.group);
  api.wharves = wharves;

  // The boats on the river (T-0063) — the owner's ask, verbatim: "you can add
  // boats correct for the era! they would exist." Derived at load like the
  // docks, but AUTHORED rather than ruled: no rule can derive where a moored
  // schooner lay, so data/boats/ states each hull and docs/LIBERTIES.md L146
  // claims the invention. An afloat hull rides the water plane at its own
  // draft and a beached one sits on the terrain; the layer refuses a boat its
  // own water cannot carry. Mounted after the wharves for reading order — the
  // two share the river and deliberately never touch: the wharf record draws
  // no vessel at its decks, and the boats ride the open reaches.
  const boats = await createBoats({
    dataBase: bases.dataBase, terrain, confidence, problems,
  });
  scene3d.add(boats.group);
  api.boats = boats;

  /**
   * What the PLANTERS treat as built ground: the buildings' footprints plus the
   * wharf decks. A deck is a floor, and a forb growing up through the planks
   * reads as a hole in the model. Kept as its own array rather than pushed into
   * `footprints`, which the walker holds by reference and the picker resolves by
   * structure id — a second polygon under a building's id would answer for the
   * building itself.
   */
  const planting = footprints.concat(
    wharves.keepOut, boats.keepOut,
    // The plank walks and crossings (T-0085/T-0124): a sidewalk is as much a
    // floor as a wharf deck, and the sward was rooting straight through it.
    frontage.keepOut,
    // And the walkable decks the registry itself carries (the bridges, the
    // slough crossing): their polygons already exist for the walker; the
    // planting layer now refuses them too, so nothing grows up between the
    // planks of a bridge deck either.
    decks,
  );
  progress(68, 'Planting the prairie…');

  // ---- vegetation ------------------------------------------------------- //
  // Awaited, like the terrain and for the same reason: the sward is what the
  // ground looks like from standing height, and a walkthrough that opened its
  // gate onto a bare plane and grew a prairie a second later would be showing
  // the visitor a loading state and calling it 1835. Missing records degrade to
  // NOTHING planted plus a recorded problem — never to an invented community.
  // (`detailLevel` is resolved much earlier — up beside the fences, which need
  // it to know what a pale costs.)
  /**
   * Vertical pixels per radian of field, for the horizon band — the one layer
   * whose correctness is measured in pixels, because it draws an angular
   * silhouette and a crown that subtends less than one cannot be textured, only
   * deleted. In CSS pixels, which is what the release viewports (390×780 and
   * 1280×800) are stated in; the device ratio would make the same frame answer
   * differently on a phone for no reason the eye can see.
   */
  const _size = new THREE.Vector2();
  const pixelsPerRadian = () => {
    renderer.getSize(_size);
    return _size.y / (camera.fov * Math.PI / 180);
  };
  BUDGET.triangles = DETAIL[detailLevel].triangles;

  /**
   * T-0115 — the half of a detail level that is the SUN rather than the town.
   *
   * Separate from `applyDetail` below because it is instant and reversible:
   * nothing is rebuilt, no record is re-read, and switching back restores the
   * frame exactly. It is applied here at boot as well as on every change, so a
   * phone — which starts at `light` without anybody touching the control —
   * boots into the same rig a desktop gets by choosing it.
   */
  function applyShadowTier(level) {
    const want = DETAIL[level] ?? DETAIL.full;
    world.setShadowRig(want.shadowReachM);
    const casts = want.furnitureCastsShadow !== false;
    for (const name of FURNITURE_LAYERS) {
      const group = scene3d.getObjectByName(name);
      // A layer that drew nothing (a record that failed to load, a fence whose
      // every post stood in water) simply has no group, and that is not an
      // error here — the problem is already recorded where it happened.
      if (!group) continue;
      // T-0127 — THE PER-MESH OPT-OUT T-0115'S LEDGER COSTED, and it is a
      // property of the MESH rather than of the layer because within one layer
      // the two halves differ: `frontage.js` marks the plank-walk and board-
      // crossing chunks `groundHugging` and leaves the street-lining fences on
      // their own meshes without it. A walk lies 0.11 m proud of the ground and
      // its own cast shadow is about 0.04 m wide at noon on 1 July, so drawing
      // 2.9 km of boards into the shadow map buys nothing a visitor can see and
      // costs their whole triangle count and one draw call per chunk, at the two
      // tiers that cast at all. The fences (1.37 m, about half a metre of real
      // shadow along the walk they stand behind) keep casting. `light` casts no
      // furniture at all, so nothing here changes it.
      group.traverse((o) => {
        if (!o.isMesh) return;
        o.castShadow = casts && !o.userData.groundHugging;
      });
    }
    return { reachM: want.shadowReachM, furnitureCastsShadow: casts };
  }
  applyShadowTier(detailLevel);

  /**
   * T-0150 — THE FURNITURE'S REACH: how far down a long street the derived
   * furniture is drawn at all.
   *
   * The second half of what a scene-detail level does to the furniture, and the
   * first half that is about DISTANCE rather than about the sun. T-0135 walked
   * five named stands instead of one and found the town far over every ceiling
   * at the two axial views — Lake Street east from Canal, and the forks from
   * Wolf Point — because a long open sightline is exactly where the 2026-08-21
   * chunking cannot help: nothing is behind the camera, so no chunk is skipped
   * and every one of them is a draw call. The owner raised the ceilings to
   * carry it and opened T-0149 to win the floor back by TRIMMING that view; this
   * is the first of its three pieces.
   *
   * WHAT IS TRIMMED, AND WHY IT IS THE FURNITURE. `FURNITURE_LAYERS` is already
   * the set this project has argued is small timber standing ON the town rather
   * than being the town — the same set whose shadows `light` gives up. A fence
   * pale is 1.2 m of silhouette, and this camera is 62 degrees over 800 CSS
   * pixels, so it subtends 739 · 1.2 / d pixels: about 9 at 100 m, 4.4 at 200 m
   * and 3.0 at 300 m. Beyond the reach set below it is drawn at a scale where
   * the geometry has nothing left to say and the draw call is the whole cost.
   *
   * WHAT IS NOT TRIMMED, and each for its own reason. `structures`, `terrain`,
   * `streets` and the woody layer are the reconstruction itself and are never
   * distance-culled here. `signage` is out for the reason it is out of the
   * shadow policy — a board exists to be read — and it is a rounding error in
   * this frame besides. `flora` already has its own falloff. And the reach is
   * `null` at `full` and `balanced`: this is the bottom rung buying its floor
   * back, not a cheapening of the tier a visitor chose deliberately.
   *
   * IT IS A RENDERING DECISION AND NOT A CLAIM, which is the test everything in
   * this block has to pass. Nothing is moved, nothing is re-graded, nothing is
   * un-built: every fence stands exactly where its record puts it, is drawn
   * exactly as it is drawn the moment you walk toward it, and the confidence
   * view, the census and the cards all read the layer whole. What changes is
   * only whether a mesh whose members are three pixels tall is submitted.
   *
   * The cull is per CHUNK, which is what makes it worth having: the layers were
   * chunked in August 2026 so the frustum could skip what is behind you, and a
   * chunk is therefore already the unit that can be dropped without splitting a
   * fence run in half. A chunk is kept while any part of its bounding sphere is
   * inside the reach, so the boundary falls beyond the far edge of what is drawn
   * rather than through it.
   */
  const furniture = { reachM: null, spheres: [], drawn: 0, culled: 0 };
  /** Re-read the furniture meshes and bank each one's WORLD bounding sphere.
   *  Called wherever a furniture layer may have been rebuilt — the fence layer
   *  rebuilds its meshes in place when the level changes (T-0067), and a stale
   *  list would cull spheres belonging to geometry that no longer exists. */
  function collectFurniture() {
    furniture.spheres.length = 0;
    for (const name of FURNITURE_LAYERS) {
      const group = scene3d.getObjectByName(name);
      if (!group) continue;
      group.updateWorldMatrix(true, true);
      group.traverse((o) => {
        if (!o.isMesh || !o.geometry) return;
        if (!o.geometry.boundingSphere) o.geometry.computeBoundingSphere();
        const sph = o.geometry.boundingSphere?.clone();
        if (!sph) return;
        sph.applyMatrix4(o.matrixWorld);
        furniture.spheres.push({ mesh: o, c: sph.center, r: sph.radius });
      });
    }
  }
  /** The reach in force, from the level — and every mesh made visible again on
   *  the way back up the ladder, so switching down and up returns the frame the
   *  visitor had rather than a permanently thinner one. */
  function applyFurnitureReach(level) {
    const want = DETAIL[level] ?? DETAIL.full;
    collectFurniture();
    furniture.reachM = typeof want.furnitureReachM === 'number'
      ? want.furnitureReachM : null;
    updateFurnitureReach();
    return furniture.reachM;
  }
  /** Per frame, before the render: hide what is out of reach. Cheap by
   *  construction — one distance against a banked sphere per chunk, no matrix
   *  work and no allocation, over the couple of hundred meshes the five layers
   *  come to. */
  function updateFurnitureReach() {
    const reach = furniture.reachM;
    let drawn = 0;
    let culled = 0;
    // `eye` and `sph` rather than `p` and `s`: `tools/validate.py`'s sidecar
    // contract follows the local names a sidecar block is bound to, and a `p`
    // or an `s` here is read as `placement` and `sidecar` and reported missing.
    // The scanner says as much where it is defined; this is the one-minute
    // rename it asks for.
    const eye = camera.position;
    for (const sph of furniture.spheres) {
      let far = false;
      if (reach !== null) {
        const dx = sph.c.x - eye.x;
        const dy = sph.c.y - eye.y;
        const dz = sph.c.z - eye.z;
        far = Math.sqrt(dx * dx + dy * dy + dz * dz) - sph.r > reach;
      }
      sph.mesh.visible = !far;
      if (far) culled++; else drawn++;
    }
    furniture.drawn = drawn;
    furniture.culled = culled;
  }
  applyFurnitureReach(detailLevel);

  /**
   * WHERE THE SWARD MAY NOT GROW (T-0067), composed rather than replacing the
   * street's own answer. Two things block a prairie plant now: the travelled
   * track it would grow through, and a FENCE it would grow inside — the wagon
   * yard's dust, the pound's trodden earth, a dooryard's kept green are all
   * ground somebody worked, and none of them is 1.5 m of bluestem.
   *
   * THE TREES ARE DELIBERATELY NOT BLOCKED and the difference is the whole
   * reason this is composed here rather than pushed into `planting`. The
   * dooryard plantings (T-0074) and the Sauganash's own three stems stand INSIDE
   * these fences BY RECORD; a block-list entry that reached the woody layer
   * would delete every one of them and file a problem for each, which is this
   * ticket undoing another one. The sward is the only layer that gives way.
   */
  const swardBlocked = (e, n) => streets.blocksGrowth(e, n) || yards.suppressesSward(e, n);

  let flora = await createFlora({
    dataBase: bases.dataBase, terrain, footprints: planting,
    growthBlocked: swardBlocked,
    confidence, problems, ...detailOpts(),
  });
  scene3d.add(flora.group);
  let trees = await createTrees({
    dataBase: bases.dataBase, terrain, footprints: planting,
    growthBlocked: streets.blocksGrowth,
    confidence, problems, pixelsPerRadian, streetRecords: loaded.index?.streets ?? [],
    // Which sward a point stands in, so the woody layer plants the lakeshore
    // poplars on the ground the beach is actually drawn on rather than carrying
    // a second copy of the zone extents (ROADMAP K45(b) change one). Both call
    // sites build the sward first, and a dead `flora` would answer null, which
    // plants no dune rather than planting one somewhere invented.
    zoneAt: (e, n) => flora.zoneAt(e, n),
    ...detailOpts(),
  });
  scene3d.add(trees.group);

  /**
   * Rebuild the two layers that scale, in place. Both are planted from a FIXED
   * seed, so the same setting always yields the same prairie — changing detail
   * and changing back gives you the town you had, not a reshuffled one.
   */
  let detailPending = null;
  async function applyDetail(level) {
    if (!DETAIL[level] || level === detailLevel) return;
    detailLevel = level;
    BUDGET.triangles = DETAIL[level].triangles;
    // The fence's half of the level, first: `light` draws a pale as a plank and
    // the other two as a prism (T-0067), and the layer rebuilds its own meshes
    // in place from records it has already loaded. It is done BEFORE the shadow
    // tier because every mesh is new after a rebuild and starts out casting —
    // `applyShadowTier` below is what settles that, and settling it first would
    // settle it on meshes that are about to be thrown away.
    enclosures.setDetail?.(level);
    // The sun's half of the level takes effect on THIS frame rather than after
    // the replanting: it costs nothing to apply, and a visitor who turns the
    // setting down on a machine that is struggling should get the cheap half of
    // the answer immediately instead of behind two layer rebuilds.
    applyShadowTier(level);
    // And the reach, for the same reason and in the same breath: the fence layer
    // has just rebuilt its meshes, so the banked spheres are re-read here rather
    // than left pointing at geometry that has been disposed (T-0150).
    applyFurnitureReach(level);
    // Serialise: a visitor clicking through the options faster than the rebuild
    // would otherwise interleave two plantings into one scene.
    const run = (detailPending ?? Promise.resolve()).then(async () => {
      scene3d.remove(flora.group);
      flora.dispose?.();
      flora = await createFlora({
        dataBase: bases.dataBase, terrain, footprints: planting,
        growthBlocked: swardBlocked,
        confidence, problems, ...detailOpts(),
      });
      scene3d.add(flora.group);

      scene3d.remove(trees.group);
      trees.dispose?.();
      trees = await createTrees({
        dataBase: bases.dataBase, terrain, footprints: planting,
        growthBlocked: streets.blocksGrowth,
        confidence, problems, pixelsPerRadian, streetRecords: loaded.index?.streets ?? [],
        zoneAt: (e, n) => flora.zoneAt(e, n),
        ...detailOpts(),
      });
      scene3d.add(trees.group);
      api.flora = flora;
      api.trees = trees;
      confidence.set(confidence.enabled);
    });
    detailPending = run.catch(() => {});
    return run;
  }

  // No `docBase` override: a dossier is read at one absolute address from every
  // tier, because the relative one resolved only in the source tree — the tree
  // nobody visits — and 404'd on the deployed site and its preview alike
  // (ROADMAP K26, popup.js DOSSIER_BASE).
  const popup = createPopup(popupRoot);
  const navigation = createNavigation({
    root: hudRoot, terrain, registry: loaded.registry, streets,
  });
  const hud = createHud({
    root: hudRoot,
    scene: loaded.scene,
    registry: loaded.registry,
    intersections: loaded.index?.intersections ?? [],
    isTouch: prefersTouch(),
    resolvedDetail: detailLevel,
    onConfidence: (on) => confidence.set(on),
    onFly: (on) => { intent.flying = !!on; },
    onGoTo: (target) => goToTarget(target),
    // Hiding a level removes it from the view outright — see confidence.setHidden.
    onHideLevel: (level, hide) => confidence.setHidden(level, hide),
    onSetting: (key, value) => {
      if (key === 'speed') {
        // Keep the run multiplier the walker was tuned with rather than pinning
        // a fixed run speed, so the two stay in proportion at any setting.
        WALK.speed = value;
        WALK.sprintSpeed = value * 2.28;
      } else if (key === 'eyeHeight') {
        // Applied to the standing eye immediately, not on the next step: a
        // slider you have to walk away from before it does anything reads as
        // broken, and this one exists because the default view felt too low.
        WALK.eyeHeight = value;
        walker.resettle();
      } else if (key === 'fov') {
        camera.fov = value;
        camera.updateProjectionMatrix();
      } else if (key === 'roadAid') {
        // R-A1. A uniform on the shared street materials — no recompile, and
        // the next frame carries it.
        streets.setLegibilityAid(value);
      } else if (key === 'brightness') {
        // K24. One scalar on the tone mapper — no recompile, no relight, and
        // the next frame carries it.
        world.setBrightness(value);
      } else if (key === 'quality') {
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, value));
      } else if (key === 'detail') {
        applyDetail(value);
      } else if (key === 'compass') {
        navigation.setCompassVisible(value);
      } else if (key === 'overviewMap') {
        navigation.setMapVisible(value);
      } else if (key === 'streetNames') {
        navigation.setStreetVisible(value);
      } else if (key === 'units') {
        navigation.setUnits(value);
      }
    },
  });

  // The liberties the scene takes, in the Evidence panel. Awaited rather than
  // fired and forgotten: it is one small JSON, and a visitor who opens the panel
  // in the first second should not find it empty. A failure here degrades the
  // panel and records a problem; it does not stop the walkthrough.
  api.liberties = await mountLiberties({
    mount: document.getElementById('liberties'),
    noteMount: document.getElementById('liberties-note'),
    dataBase: bases.dataBase,
    registry: loaded.registry,
    problems,
  });
  // The same list, filtered to the building being inspected, in the provenance
  // popup. One fetch feeds both views: the panel says what the scene made up,
  // the card says what THIS building made up, and neither can drift from the
  // markdown they are both quoting.
  popup.setLiberties(api.liberties.liberties);

  // And what the GROUND claims, which no building can carry either: the surface
  // every one of them stands on is graded as carefully as they are, and said so
  // nowhere a visitor could read it.
  api.ground = await mountGround({
    mount: document.getElementById('ground'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });

  // And WHO was living here. This layer had a reader already — a household
  // travels in its building's sidecar and the building card names it — which
  // is exactly why nobody noticed that a household with no attested residence
  // and no attested workplace attaches to no building and so reached no card
  // anywhere: ROADMAP K52. Nothing of it is drawn; this is the record, on a card.
  api.residents = await mountResidents({
    mount: document.getElementById('residents'),
    noteMount: document.getElementById('residents-note'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });

  // And what was LIVING here, which no building carries at all. The animal
  // records were researched to the scene date, graded, cited — and read by
  // nothing: ROADMAP K42 measured that no renderer source opened the directory
  // and the publish step did not copy it, so the layer stopped at the
  // repository. Nothing of it is drawn; this is the record, on a card.
  api.fauna = await mountFauna({
    mount: document.getElementById('fauna'),
    noteMount: document.getElementById('fauna-note'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });

  // And what was researched and left out, which no building can carry because
  // the buildings that would carry it are the ones not standing here.
  // …and the third category, which neither of those can hold: researched, and
  // still open. One of the four is standing in the scene, so it cannot go on the
  // not-here list without that list becoming false.
  api.exclusions = await mountExclusions({
    mount: document.getElementById('exclusions'),
    uncertainMount: document.getElementById('uncertain'),
    // …and what each of the two lists says it is, in the compiled document's own
    // words rather than a paraphrase typed into the markup beside it.
    standardMount: document.getElementById('exclusions-note'),
    uncertainStandardMount: document.getElementById('uncertain-note'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });
  // And the open questions again, filtered to the building being inspected —
  // exactly as the liberties are, and for the same reason. One of the four is
  // standing in the scene, and the panel's entry for it promises that the
  // provenance card shows the claim carrying the doubt; the card is where a
  // visitor who walked up to that building would think to ask.
  popup.setOpenQuestions(api.exclusions.uncertain);

  // Apply the visitor's stored settings before the first frame, so nothing
  // visibly snaps a moment after load.
  // The visitor's stored level choices, before the first frame — otherwise a
  // returning visitor who had hidden the reconstructed town sees it flash in.
  hud.applyHidden();

  WALK.speed = hud.settings.speed;
  WALK.sprintSpeed = hud.settings.speed * 2.28;
  WALK.eyeHeight = hud.settings.eyeHeight;
  camera.fov = hud.settings.fov;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, hud.settings.quality));
  streets.setLegibilityAid(hud.settings.roadAid);
  world.setBrightness(hud.settings.brightness);
  navigation.setCompassVisible(hud.settings.compass);
  navigation.setMapVisible(hud.settings.overviewMap);
  navigation.setStreetVisible(hud.settings.streetNames);
  navigation.setUnits(hud.settings.units);

  // ---- input ------------------------------------------------------------ //

  const intent = createIntent();
  const backends = createBackendSwitch(intent);

  const pointerlock = createPointerLockBackend({
    intent,
    domElement: canvas,
    onLockChange: (locked) => {
      hud.setLocked(locked);
      if (!locked) hud.say('Pointer released — click the view to look around again');
    },
  });

  const touch = createTouchBackend({
    intent,
    domElement: canvas,
    ui: {
      layer: document.getElementById('touch-layer'),
      stick: document.getElementById('stick'),
      knob: document.getElementById('stick-knob'),
      risePad: document.getElementById('rise-pad'),
      riseUp: document.getElementById('rise-up'),
      riseDown: document.getElementById('rise-down'),
    },
    onViewport: () => resize(),
  });

  let gateOpen = true;

  // Exactly one backend is live. Whichever device the visitor actually uses
  // wins, switched by the first real event of that kind — a laptop with a
  // touchscreen must not end up driving both.
  backends.activate(coarse ? touch : pointerlock);
  window.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'touch') backends.activate(touch);
    else if (e.pointerType === 'mouse') backends.activate(pointerlock);
  }, { capture: true });
  window.addEventListener('keydown', (e) => {
    // Not while typing. This capture handler switches the whole control backend
    // to keyboard-and-mouse, and the first keystroke into the Go-to search box
    // was doing exactly that — taking a visitor who had been tapping their way
    // around a phone and handing them a control scheme with no on-screen stick.
    if (isTyping(e.target)) return;
    if (!e.metaKey && !e.ctrlKey) backends.activate(pointerlock);
  }, { capture: true });

  canvas.addEventListener('click', () => {
    if (backends.active === pointerlock && !pointerlock.isLocked && !gateOpen) pointerlock.lock();
  });

  // Escape closes an open inspection card (T-0108). Escape is ALSO the
  // browser's own pointer-lock release, which no page may intercept — so this
  // cooperates rather than fights: while the pointer is locked the browser
  // eats the keystroke and unlocks, and the press that reaches us is the one
  // with nothing else to do. Acting only when a card is open leaves Escape's
  // meaning everywhere else untouched.
  window.addEventListener('keydown', (e) => {
    if (e.code !== 'Escape' || isTyping(e.target)) return;
    if (popup.openId) popup.close();
  });

  // ---- picking ---------------------------------------------------------- //

  function inspect(ndc = null) {
    let hit = buildings.pickAt(ndc, camera);
    /**
     * A fence can be the thing you are aiming at. The estray pen's geometry
     * lives on the enclosure layer now (T-0051), and it is still a structure
     * record with a card behind it — so a pick that misses every roof, or lands
     * on one standing further away than the fence in front of it, resolves
     * against the enclosures too. An enclosure with no structure behind it (the
     * wagon yard) answers null and the aim falls through to the roof, which is
     * the same behaviour as before this layer existed.
     */
    const fence = enclosures.pickAt(ndc, camera);
    if (fence && (!hit || fence.distance < hit.distance)) {
      const record = loaded.registry.get(fence.id);
      if (record) hit = { ...fence, record };
    }
    /**
     * And so can a signboard, which is the whole function of one: it hangs a
     * metre out from the wall, so at a shop door it is the nearest thing to the
     * crosshair, and the board a visitor aims at should open the business
     * behind it rather than whatever the ray finds past it (T-0039).
     */
    const board = signage.pickAt(ndc, camera);
    if (board && (!hit || board.distance < hit.distance)) {
      const record = loaded.registry.get(board.id);
      if (record) hit = { ...board, record };
    }
    /**
     * And so can a barrel at a shop door, which is where a visitor's crosshair
     * actually lands when they walk up to a frontage: the goods stand half a
     * metre out from the wall, so they are nearer than it. A barrel opens the
     * business whose door it stands at, and the wagon opens the hotel whose
     * yard it stands in (T-0040).
     */
    const goods = yard.pickAt(ndc, camera);
    if (goods && (!hit || goods.distance < hit.distance)) {
      const record = loaded.registry.get(goods.id);
      if (record) hit = { ...goods, record };
    }
    /**
     * And so can the walk under a visitor's feet, or the board on its post at
     * the corner — which is the whole function of a sign: it stands out at the
     * street edge, so from the road it is nearer to the crosshair than the inn
     * behind it. Both open the building whose frontage they are (T-0082).
     */
    const frontageHit = frontage.pickAt(ndc, camera);
    if (frontageHit && (!hit || frontageHit.distance < hit.distance)) {
      // The registry answers for a building's frontage; a record that is its
      // own subject — the river plank walk (T-0119) — carries its card on the
      // layer, the same arrangement the boats keep.
      const record = loaded.registry.get(frontageHit.id) ?? frontageHit.record;
      if (record) hit = { ...frontageHit, record };
    }
    /**
     * And so can a wharf, which is the largest thing on any of these derived
     * layers: it reaches out over the water in front of the warehouse, so from
     * the bank it is nearer to the crosshair than the shed it belongs to. A dock
     * opens the warehouse it serves (T-0041).
     */
    const dock = wharves.pickAt(ndc, camera);
    if (dock && (!hit || dock.distance < hit.distance)) {
      const record = loaded.registry.get(dock.id);
      if (record) hit = { ...dock, record };
    }
    /**
     * And so can a boat, which is the one pickable thing here that belongs to
     * no structure at all: a hull answers with its OWN card record, built by
     * the boat layer from data/boats/ — type, size, state and what bounded the
     * invention — rather than through the registry (T-0063).
     */
    const boat = boats.pickAt(ndc, camera);
    if (boat && boat.record && (!hit || boat.distance < hit.distance)) {
      hit = { ...boat };
    }
    if (!hit) {
      popup.close();
      hud.say('Nothing there — aim at a building');
      return null;
    }
    popup.show(hit.record);
    return hit;
  }

  /** Programmatic pick: by structure_id, by NDC point, or down the crosshair. */
  function pick(target) {
    if (typeof target === 'string') {
      const record = loaded.registry.get(target);
      if (!record) return null;
      return popup.show(record) ? { id: target, record } : null;
    }
    if (target && typeof target.x === 'number' && typeof target.y === 'number') {
      return inspect(new THREE.Vector2(target.x, target.y));
    }
    return inspect(null);
  }

  /** Stand back and look at a structure — used by anchors and by the harness. */
  function frame(id, distance = 26) {
    const point = focusPoint(id);
    if (!point) return false;
    walker.lookAt(point, distance);
    return true;
  }

  function focusPoint(id) {
    const fp = footprints.find((f) => f.id === id);
    const record = loaded.registry.get(id);
    // A structure drawn by the enclosure layer has neither an obstruction
    // polygon nor a wall height any more, and both of the defaults below are
    // wrong for it: the placement is the pen's south-west CORNER, and 5 m of
    // assumed wall aims the crosshair nearly two metres over a fence that is
    // 1.83 m tall. So take the perimeter's own centre and its own height — the
    // Go-to menu still lists the pen, and it has to stand you in front of it.
    const fence = record?.sidecar?.drawn_by
      ? (enclosures.records ?? []).find((r) => r.structure_id === id)
      : null;
    let e; let n;
    if (fence) {
      const pts = (fence.runs ?? []).flatMap((r) => r.path_local_enu_m ?? []);
      if (!pts.length) return null;
      e = pts.reduce((a, p) => a + p[0], 0) / pts.length;
      n = pts.reduce((a, p) => a + p[1], 0) / pts.length;
      const h = fence.form?.height_m?.value ?? 1.5;
      return enuToWorld(e, n, terrain.surfaceHeight(e, n) + h * 0.55);
    }
    if (fp) {
      e = fp.pts.reduce((a, p) => a + p[0], 0) / fp.pts.length;
      n = fp.pts.reduce((a, p) => a + p[1], 0) / fp.pts.length;
    } else {
      const p = record?.sidecar?.placement;
      if (!p) return null;
      e = p.local_e ?? 0;
      n = p.local_n ?? 0;
    }
    const wallH = record?.sidecar?.attributes?.wall_height_m?.value ?? 5;
    return enuToWorld(e, n, terrain.surfaceHeight(e, n) + wallH * 0.55);
  }

  /** One route for the complete search: frame a structure, stand at a verified
   * intersection, or use one of the authored scene viewpoints. */
  function goToTarget(target) {
    if (!target?.kind) return false;
    if (target.kind === 'anchor') return api.goTo?.(target.id) ?? false;
    hud.setFly(false, { announce: false });
    walker.setFlying(false);
    if (target.kind === 'structure') return frame(target.id);
    if (target.kind === 'intersection'
        && Number.isFinite(target.local_e) && Number.isFinite(target.local_n)) {
      walker.teleport({
        local_e: target.local_e, local_n: target.local_n, yaw_deg: 0,
      });
      return true;
    }
    return false;
  }

  // ---- gate ------------------------------------------------------------- //

  function openWorld() {
    if (!gateOpen) return;
    gateOpen = false;
    gate?.setAttribute('hidden', '');
    hud.show();
    hud.restore();
    const controlHelpOpen = hud.showControlHelp({ auto: true });
    // The gate doubles as the audio-unlock gesture: browsers only allow an
    // AudioContext to start from one, and ambience lands in a later slice.
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx && !api.audio) { api.audio = new Ctx(); api.audio.resume?.(); }
    } catch { /* no audio is fine; a thrown error is not */ }
    if (backends.active === pointerlock && !controlHelpOpen) pointerlock.lock();
    hud.say(backends.name === 'touch'
      ? 'Left thumb walks · drag the right side to look · tap a building'
      : 'W A S D to walk · E to inspect what you are looking at');
  }
  gateBtn?.addEventListener('click', openWorld);

  // ---- resize ----------------------------------------------------------- //

  function resize() {
    const vv = window.visualViewport;
    const w = Math.max(1, Math.round(vv?.width ?? window.innerWidth));
    const h = Math.max(1, Math.round(vv?.height ?? window.innerHeight));
    renderer.setSize(w, h, true);
    camera.aspect = w / h;
    // Hor+ : hold the horizontal field of view and let the vertical follow, so a
    // portrait phone does not end up looking down a drinking straw.
    const hFov = 76 * Math.PI / 180;
    const vFov = 2 * Math.atan(Math.tan(hFov / 2) / camera.aspect);
    camera.fov = THREE.MathUtils.clamp(vFov * 180 / Math.PI, 55, 94);
    camera.updateProjectionMatrix();
    document.documentElement.style.setProperty('--vh', `${h}px`);
  }
  window.addEventListener('resize', resize);
  window.addEventListener('orientationchange', resize);
  window.visualViewport?.addEventListener('resize', resize);
  resize();

  // ---- loop ------------------------------------------------------------- //

  const clock = new THREE.Clock();
  let frames = 0;
  let fpsMark = performance.now();
  let fps = 0;
  /** Set by capture(); read back at the end of the frame it asked for. */
  let pendingCapture = null;
  /**
   * Harness only, default off: keep drawing, advance nothing. The gate compares
   * two captures of the same scene to decide whether the confidence view left
   * anything behind, and the wind blows between them — which is a comparison of
   * the weather, not of the tint. Holding the clock takes that variable out
   * instead of widening the tolerance around it.
   */
  let animationHold = false;

  /**
   * Hold the near plane at a twenty-fifth of the eye's height above the ground,
   * quantised, between `NEAR.min` and `NEAR.max`. See the NEAR block at the top
   * of this file for why the depth buffer needs it and why the water material
   * must not be biased instead. Returns the value in force, for the harness.
   */
  function setNearFor(altitude) {
    const wanted = THREE.MathUtils.clamp(
      Math.round(((altitude || 0) / NEAR.divisor) / NEAR.step) * NEAR.step,
      NEAR.min, NEAR.max);
    if (Math.abs(camera.near - wanted) > 1e-6) {
      camera.near = wanted;
      camera.updateProjectionMatrix();
    }
    return camera.near;
  }

  function tick() {
    // Keep visual simulation stable, but do not make a visitor crawl in direct
    // proportion to a slow renderer. At 2 fps the former 0.05 s clamp advanced
    // walking by only 0.10 s per real second. Movement now consumes up to a
    // quarter-second of real frame time in <= 0.05 s collision/terrain steps.
    // The clock is read either way, so releasing a hold does not deliver the
    // whole held interval as one enormous frame.
    const elapsed = Math.min(clock.getDelta(), 0.25);
    const frameDt = animationHold ? 0 : elapsed;
    const dt = Math.min(frameDt, 0.05);

    backends.active?.update?.(dt);
    terrain.update(dt);
    const asked = intent.takeInteract();
    // The inspect KEY toggles: the reach that opened the card also closes it
    // (T-0108). A click or tap always re-inspects — aiming at a second
    // building with a card open should open that building, not shut the first.
    if (asked && asked.source === 'key' && popup.openId) popup.close();
    else if (asked) inspect(asked.point ? new THREE.Vector2(asked.point.x, asked.point.y) : null);
    const walkSteps = Math.max(1, Math.ceil(frameDt / 0.05));
    const walkDt = frameDt / walkSteps;
    for (let i = 0; i < walkSteps; i++) walker.update(walkDt, intent);
    // Before the render, after the walker: the near plane is a function of where
    // the eye ended up this frame (R-BUG1, and the NEAR block above).
    setNearFor(walker.state.altitude);
    world.follow(camera.position);
    // After the camera has finished moving and before anything is submitted:
    // what the furniture's reach hides is a function of where the eye ended up
    // this frame (T-0150).
    updateFurnitureReach();
    flora.update(dt, camera);
    trees.update(dt, camera);

    renderer.render(scene3d, camera);

    // Read back inside the frame that drew it. Outside the loop the drawing
    // buffer has already been composited and cleared, and readPixels quietly
    // returns the PREVIOUS frame — which makes a toggle look like it changed
    // nothing at all.
    if (pendingCapture) {
      const { grid, resolve } = pendingCapture;
      pendingCapture = null;
      resolve(readbackSignature(renderer, grid));
    }

    const st = walker.state;
    api.player.e = st.e;
    api.player.n = st.n;
    api.player.y = st.eyeY;
    api.player.bearingDeg = walker.bearingDeg;
    api.player.pitchDeg = st.pitch * 180 / Math.PI;
    api.player.speed = st.speed;
    api.player.moving = st.speed > 0.001;
    api.player.altitude = st.altitude;
    api.player.flying = st.flying;
    hud.setAltitude(st.altitude);
    navigation.update({ e: st.e, n: st.n, bearingDeg: walker.bearingDeg });

    // Wall-clock, not the clamped dt: a clamped dt reports a healthy 20 fps on
    // a machine that is actually drawing three frames a second.
    frames++;
    const now = performance.now();
    if (now - fpsMark >= 500) {
      fps = (frames * 1000) / (now - fpsMark);
      frames = 0;
      fpsMark = now;
    }
  }
  renderer.setAnimationLoop(tick);

  // ---- harness ---------------------------------------------------------- //

  Object.assign(api, {
    renderer, camera, scene3d, world, terrain, buildings, walker, intent, popup, hud,
    confidence,
    backends, streets, flora, trees, navigation,
    // Where the dataset was loaded from, so a gate can re-read an authored
    // record and ask whether what it says reached the renderer — rather than
    // comparing the renderer against a copy of itself.
    dataBase: bases.dataBase,
    detailLevels: DETAIL,
    detailOrder: DETAIL_ORDER,
    // The setter side only. `detail` and `furnitureShadows` are LIVE readings
    // and are defined with the other live ones below — FOUND BY T-0115, and it
    // is the trap the K24 note twenty lines down already names: a getter
    // written in this literal is invoked ONCE by Object.assign and its value
    // copied, so `api.detail` had been frozen at whatever level the page booted
    // into ever since it was added. Nothing looked wrong, which is the trouble
    // with it — the smoke's "the level the visitor started on is restored"
    // check was comparing a constant with the constant it was made from and
    // could not fail. The rule was written down; it had simply not been applied
    // to this one.
    setDetail(level) { return applyDetail(level); },
    setConfidenceView(on) { return hud.setConfidence(!!on, { announce: false }); },
    // R-A1. The gates measure the DEFAULT, so they need to be able to read this
    // back as well as set it: "the aid is off unless a visitor moved it" is an
    // assertion, not a comment.
    setRoadAid(v) { return streets.setLegibilityAid(v); },
    // K24. The setter side only. Every LIVE reading — roadAid, brightness,
    // exposure — is defined below, because a getter written in this literal is
    // read once by Object.assign and frozen. See the note there.
    setBrightness(v) { return world.setBrightness(v); },
    // T-0002. Not a visitor setting — the town's facade tones are what the town
    // looks like. It is here because a gate has to be able to turn the tone off
    // to prove it is on (R-BUG6(a)), and the reading below is defined with the
    // other live ones for the reason K24 gives.
    setFacadeWeathering(v) { return buildings.setWeathering(v); },
    setFly(on) { return hud.setFly(!!on, { announce: false }); },
    get flying() { return walker.state.flying; },
    get altitude() { return walker.state.altitude; },
    pick,
    frame,
    goToTarget,
    goTo(anchorId) {
      const a = anchorFor(loaded.scene, anchorId);
      if (!a) return false;
      // Set the MODE through the HUD, not on the walker: intent.flying is the
      // one master, and a walker flipped directly would be reverted on the very
      // next frame when update() reconciled it against an intent still reading
      // false. The HUD's setter is what writes the intent.
      const aerial = typeof a.altitude_m === 'number';
      hud.setFly(aerial, { announce: false });
      walker.teleport({
        local_e: a.local_e,
        local_n: a.local_n,
        yaw_deg: a.yaw_deg,
        altitude_m: aerial ? a.altitude_m : null,
        pitch_deg: typeof a.pitch_deg === 'number' ? a.pitch_deg : null,
      });
      return true;
    },
    stats() {
      const info = renderer.info;
      return {
        drawCalls: info.render.calls,
        triangles: info.render.triangles,
        programs: info.programs?.length ?? 0,
        geometries: info.memory.geometries,
        textures: info.memory.textures,
        batches: buildings.batches.length,
        structures: loaded.registry.size,
        bytes: loaded.bytes,
        fps: Math.round(fps),
        // R-BUG1: the near plane is no longer a constant, so a harness asking
        // why an edge is or is not stable can read the number that decides it.
        cameraNear: camera.near,
        budget: BUDGET,
        withinBudget: info.render.calls <= BUDGET.drawCalls
          && info.render.triangles <= BUDGET.triangles,
      };
    },
    /**
     * A pixel signature of the next rendered frame. Resolves from inside the
     * render loop, so it always measures a frame that includes whatever you
     * just changed — and it needs no `preserveDrawingBuffer`, which means the
     * test measures the same renderer configuration a visitor gets.
     */
    capture(grid = 12) {
      return new Promise((resolve, reject) => {
        pendingCapture = { grid, resolve };
        setTimeout(() => {
          if (pendingCapture?.resolve === resolve) {
            pendingCapture = null;
            reject(new Error('capture: no frame rendered within 10 s'));
          }
        }, 10000);
      });
    },
    /** T-0150, HARNESS ONLY and never a visitor setting: drive the furniture's
     *  reach directly, so `tools/measure_furniture_reach.mjs` can sweep candidate
     *  reaches at one page load and a gate can prove the cull is the thing doing
     *  the saving. `null` restores "draw it all". The live reading is
     *  `furnitureReach` below, defined with the other getters for the reason the
     *  K24 note gives. */
    setFurnitureReach(m) {
      furniture.reachM = typeof m === 'number' && Number.isFinite(m) ? m : null;
      updateFurnitureReach();
      return furniture.reachM;
    },
    /** Force one frame — for tests that must not race the animation loop. */
    step() { tick(); },
    /** Keep rendering, advance nothing — for tests comparing two frames of the
     *  same scene. Never set by the application. */
    setAnimationHold(on) { animationHold = !!on; return animationHold; },
    walkBudget: WALK,
  });

  // Live getters, defined rather than assigned: Object.assign COPIES the value
  // a getter returns at assignment time, which would have frozen these at their
  // boot-time answer and made every later reading wrong.
  //
  // K24 FOUND THAT THE NOTE ABOVE WAS TRUE AND THAT THE LITERAL HAD BEEN
  // ACQUIRING GETTERS ANYWAY. `get roadAid()` shipped inside the Object.assign
  // literal with R-A1 and was frozen at 0 from the moment it was written. Its
  // two gates both assert `=== 0` — off at boot, and back to 0 when dropped —
  // so a constant 0 passed both, and the third gate (raising it changes the
  // frame) reads a frame signature and never touched the getter. The control
  // itself was always live; the READBACK was the dead thing, which is R-A1's
  // own finding one level in: an assertion that can only ever see one value is
  // not an assertion. The brightness aid caught it because `exposure` is the
  // first of these readings whose expected value MOVES.
  //
  // So the rule, and it is why this block is the only place a live reading may
  // be written: anything on the harness whose answer changes after boot is
  // defined HERE. A getter in the literal above is a frozen snapshot.
  Object.defineProperties(api, {
    /** The level the visitor is actually on, now rather than at boot (T-0115). */
    detail: { get: () => detailLevel, enumerable: true },
    /**
     * T-0115. What the level's shadow half actually DID to the scene, read off
     * the scene rather than off the table that asked for it — R-A1's rule about
     * assertions again: a gate that reads `DETAIL[level]` back is reading its
     * own intent, and the failure worth catching is a policy that reaches the
     * table and not the meshes. `casting` counts the furniture meshes still
     * drawn for the sun, so 0 is the claim `light` makes and anything else is
     * the bug — including a NEW furniture layer mounted outside the policy,
     * which is the way this will most likely be broken.
     */
    furnitureShadows: {
      get: () => {
        let meshes = 0;
        let casting = 0;
        // T-0127 — COUNTED, NOT ASSUMED. Before the per-mesh opt-out above, the
        // gate could read "every furniture mesh casts" as a single equality.
        // With an exemption in the layer that equality is false by design, so
        // the exempt meshes are counted here and the gate asserts
        // casting === meshes - groundHugging. A layer that silently stopped
        // casting would still fail; an exemption nobody declared cannot hide in
        // the difference.
        let groundHugging = 0;
        for (const name of FURNITURE_LAYERS) {
          const group = scene3d.getObjectByName(name);
          if (!group) continue;
          group.traverse((o) => {
            if (!o.isMesh) return;
            meshes += 1;
            if (o.userData.groundHugging) groundHugging += 1;
            if (o.castShadow) casting += 1;
          });
        }
        return { layers: FURNITURE_LAYERS.slice(), meshes, casting, groundHugging };
      },
      enumerable: true,
    },
    /**
     * T-0150. What the level's REACH half did to the scene, read off the meshes
     * for the same reason `furnitureShadows` is: the failure worth catching is a
     * reach that reaches `DETAIL` and not the frame. `hidden` counts the
     * furniture meshes the reach is holding back at this instant, so it is a
     * function of WHERE THE VISITOR STANDS as well as of the level — 0 at every
     * level with a null reach, and 0 at `light` too if the whole town happens to
     * be inside it.
     */
    furnitureReach: {
      get: () => {
        let meshes = 0;
        let hidden = 0;
        for (const name of FURNITURE_LAYERS) {
          const group = scene3d.getObjectByName(name);
          if (!group) continue;
          group.traverse((o) => {
            if (!o.isMesh) return;
            meshes += 1;
            if (!o.visible) hidden += 1;
          });
        }
        return { reachM: furniture.reachM, layers: FURNITURE_LAYERS.slice(),
                 meshes, hidden, banked: furniture.spheres.length };
      },
      enumerable: true,
    },
    confidenceView: { get: () => confidence.enabled, enumerable: true },
    controlBackend: { get: () => backends.name, enumerable: true },
    footprints: { get: () => footprints, enumerable: false },
    decks: { get: () => decks, enumerable: false },
    roadAid: { get: () => streets.legibilityAid, enumerable: true },
    brightness: { get: () => world.brightness, enumerable: true },
    exposure: { get: () => renderer.toneMappingExposure, enumerable: true },
    facadeWeathering: { get: () => buildings.weathering, enumerable: true },
  });

  // Settle the gate census before declaring ready. It was started before the
  // scene load and has had every one of those seconds; awaiting it here means
  // `api.census` is either the document or null by the time anything — a gate,
  // a visitor, the smoke — asks, rather than being a race the harness would
  // have to poll around.
  await census;

  progress(100, 'Ready');
  api.ready = true;
  if (gateBtn) { gateBtn.disabled = false; gateBtn.textContent = 'Tap to walk'; }
  if (gateSub) {
    const n = loaded.registry.size;
    gateSub.textContent = `${n} structure${n === 1 ? '' : 's'} · ${world.describe()}`;
  }

  if (DEBUG) {
    console.info('[4D Chicago]', api.stats(), world.describe());
    if (problems.length) console.warn('[4D Chicago] problems:\n - ' + problems.join('\n - '));
  }
}

/**
 * Reduce the current drawing buffer to a small comparable signature: a mean, a
 * lit fraction, and a coarse grid of cell luminances. Small enough to hand back
 * over a debug protocol, specific enough that a shader change moves it.
 */
function readbackSignature(renderer, grid) {
  const gl = renderer.getContext();
  const w = renderer.domElement.width;
  const h = renderer.domElement.height;
  const px = new Uint8Array(w * h * 4);
  gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);

  const cells = new Array(grid * grid).fill(0);
  const counts = new Array(grid * grid).fill(0);
  let sum = 0;
  let lit = 0;
  let n = 0;
  for (let y = 0; y < h; y += 2) {
    const row = Math.min(grid - 1, ((h - 1 - y) * grid / h) | 0);   // readPixels is bottom-up
    for (let x = 0; x < w; x += 2) {
      const i = (y * w + x) * 4;
      const lum = 0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2];
      sum += lum;
      n++;
      if (lum > 8) lit++;
      const c = row * grid + Math.min(grid - 1, (x * grid / w) | 0);
      cells[c] += lum;
      counts[c]++;
    }
  }
  return {
    width: w,
    height: h,
    mean: sum / (n || 1),
    litFraction: lit / (n || 1),
    cells: cells.map((v, i) => Math.round(v / (counts[i] || 1))),
  };
}

/** Look up a named camera anchor in the scene file. */
function anchorFor(scene, id) {
  if (!id || !Array.isArray(scene?.anchors)) return null;
  return scene.anchors.find((a) => a.id === id) ?? null;
}
