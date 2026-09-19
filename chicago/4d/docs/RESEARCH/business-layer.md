# The business layer

*T-1310, of T-1180. The place a business is written down.*

Until this layer there was nowhere to write a business. There were three derived files —
the newspaper claims, `gazetteer.json`, `register_1835.json` — and a business existed in the
scene only as a structure whose `function` and `occupants` block happened to name one. A
register row has an action and a trade string; it has no staff, no tier on anything, no
`sources[]`, and no dates beyond the first and last issue a notice ran. A resident's
`works_at` is a bare structure id, which can say *this person worked in that building* and
can never say *for which house of trade*.

The owner's ask — a complete list of the attested and inferred businesses, then reconstructed
ones beside them, with the staff of each carried as part of their proprietors' resident
profiles — had no shape to land in. `data/businesses/` is that shape.

## What is in it

One record per business, one file, `data/businesses/<id>.json`, against
`data/businesses.schema.json`. Today there are **196**, one for every business in the
scene-date register; **179** of them stand in the town on 1 July 1835 and the rest carry the
register's exclusion and its reason.

| | count |
|---|---:|
| records | 196 |
| present at the scene date | 179 |
| named proprietors and partners | 196 |
| …linked to a card the resident layer already holds | 144 |
| …the distinct people those links reach | 110 |
| households whose `works_at` now resolves to a business | 21 of 50 |

By census class — the classes of `trade_class_rulings.json`, which is the one taxonomy, so a
business counts against the December 1835 State census without a second crosswalk:

| class | n | | class | n |
|---|---:|---|---|---:|
| store | 67 | | printing office | 3 |
| other | 79 | | physician | 3 |
| lawyer | 18 | | book store | 2 |
| tavern | 9 | | druggist | 2 |
| storage and forwarding | 8 | | brewery | 1 |
| school | 7 | | iron foundry | 1 |
| not stated | 5 | | silversmith and jeweller | 1 |
| steam saw-mill | 4 | | tin and copper manufactory | 4 |

## Derived, never authored

`tools/compile_businesses.py --build` writes the 196; `--check` re-derives them and refuses a
committed copy a rebuild would not produce; `--self-test` breaks each of its eleven assertions
and requires every one to fire. Both run in `tools/check.sh`. A hand edit to a compiled record
is a red gate, for the same reason it is on the gazetteer and the register: a hand-edited
record is a place to promote a business — or a proprietor, or a premises — into the town
without an argument.

A record a human means to author goes in `data/businesses/authored/`, which the compiler
reads, validates and carries into the index untouched. That directory is where T-1182's
inferred-by-audit firms are written, and where the reconstruction band's `rcb_…` records
already are: **2 today**, both druggists, written by
`tools/reconstruct_businesses_1835.py --build` against the reconstruction order book's own
quota and re-derived by its `--check`. A reconstructed record carries
`provenance: "reconstructed"` and a `reconstruction` block — the order-book bucket that
bought it, the group and ticket that wrote it, the seed that redraws every drawn value on
it, and what retires it — and the compiler refuses one without it, refuses a compiled
record that claims one, and refuses any reconstructed record that cites a source. See
`docs/RESEARCH/business-naming-1835.md` for the style guide and `docs/LIBERTIES.md § L254`
for the invention.

## The id, and why it is not the one T-1180 named

T-1180 asks for `biz_<surname>_<trade>`. Derived over the 196 that scheme **collides 27
times**: five houses land on `biz_montgomery_other`, four on `biz_wentworth_tavern`, two on
`biz_calhoun_printing_office`. Every collision is the same question — *are these two printed
notices one house or two?* — and that is an identity ruling. It is T-1182's to make with the
sources in front of it, and a compiler that settled it by appending `_2` would be publishing
an adjudication nobody made.

So a compiled record takes the register's own id with `business_` replaced by `biz_`. It is
1:1 with the printed notice it comes from, collision-free by construction, reversible, and
`register_id` on the record says so out loud. `biz_<surname>_<trade>` and `rcb_…` stay in the
schema for records a human authors, where the identity question has an author to answer it.

## A name is attested; the link to a person is a second claim

The ladder is the resident layer's, unchanged — `attested`, `inferred`, `reconstructed`. A
printed name is attested: the paper prints it. Whether that printed name is *the same person*
as a card in `data/residents/` is a different claim, and it is the register's:

- where the register matched the name to a card, `person_id` carries that card's id and the
  basis names the action that made the match — **144 of 196**;
- where it did not, `person_id` is **null** and the basis says the town holds no card for
  them under an id this record can name — **52 of 196**.

Those denominators were 209 until T-1401. Thirteen of the printings were a SECOND STYLE of a
person the same record already named — "J. D. Caton" and "J. Dean Caton" are one partner of
Collins & Caton, and Giles Spring was printed three ways — so the layer was counting the
register's typography as the town's partners. `compile_businesses.fold_printed_styles` folds
them on `person_id`, never on the name, and the styles are kept on `also_printed_as[]`: the
fold removes a second COUNT of one man and no evidence at all. Twelve pairs, thirteen
printings, and the 52 names the resident layer holds no card for are untouched — a printing
that resolves to nobody cannot be folded onto anybody.

A null there is a finding, not a gap to be filled by guessing. It is also the queue for
T-1189, which staffs every business with real persons.

`proprietor_community` is `unattested` on all 196, and stays that way until a source speaks.
Reading a community off a surname is exactly the move the resident layer refuses; T-1177 is
where the Native, Métis, Black, Irish and German businesses are identified from evidence.

## The limits are data now

61 of the register's businesses are `street_only` and 62 are `unplaceable`: the paper gives a
street and no house, or no anchor at all. Those are not missing locations. They are locations
whose resolution the evidence stops short of — and they were carried in prose, inside an
`action_note`, where nothing could count them.

Each is now a `locations[]` entry whose `kind` names the limit and whose `limit_reason` quotes
the register's reason:

| kind | n | what it means |
|---|---:|---|
| `premises` | 30 | matched onto a roof the town holds. `attested` where the register matched the structure's occupants line, `inferred` where it matched only its name |
| `anchored` | 26 | the paper anchors the house against a landmark the town holds, and the town holds no roof of the house's own (the register's `new_building`) |
| `street_only` | 61 | a platted street and nothing narrower |
| `unplaceable` | 83 | no anchor the town can resolve — 79 at the scene date, plus the 4 earlier sitings of the houses that moved |

So *how many of the town's businesses can we actually place?* is a query now, not a
re-reading. The four houses that moved keep their earlier siting as a second, dated,
non-primary location rather than losing it to the current one.

### The anchor is an id (T-1401)

`anchored` is the one kind that names something and could not reach it. The landmark lived
only inside `limit_reason`'s sentence — *"The register places this house against
`tremont_house_1`…"* — so the Tremont House's own card could not say which houses stood
against it, and the Businesses view's `anchored` branch rendered a landmark title no record
supplied. Parsing that sentence for an id would have been a reading made by a regular
expression, and the crosswalk rightly refused it.

The register had the id all along, in its own `action_target` field. `compile_businesses.anchor_of`
resolves it there, and every anchored location carries an `anchor` block — `kind`, `id`,
`title`, and the two street ids of a corner. All 26 resolve:

| anchor kind | n | example |
|---|---:|---|
| `structure` | 15 | Andrews & Eells, against `tremont_house_1` |
| `business` | 7 | Collins & Caton, against `business_brewster_hogan_co` |
| `corner` | 4 | Russell E. Heacock, at Franklin and Lake |

A landmark the town does not hold is a REFUSAL in the compiler, not a null carried forward,
and the same is true of a `business_` id the register does not carry.

**The anchor is not a premises, and nothing may read it as one.** `structure_id` stays null
on all 26: the anchor says what the house stood next to, which is exactly as far as the
register went. The gate says so both ways — an anchored location with no resolved anchor is
refused, and one carrying a `structure_id` is refused as well.

## What this layer does NOT do

- **It reconstructs nothing.** Every one of the 196 records is the register's own reading,
  restated with its tier made explicit and its limits made queryable. The reconstruction
  bands are T-1182 and after.
- **`staff` is empty on all 196.** The newspapers name owners and almost never a clerk. That
  is a true reading of the register, not an omission: T-1183 rules the staffing model and
  T-1189 fills it.
- **It does not change a resident record.** `works_at` on a household still names a
  structure. The crosswalk in `index.json` says which businesses stood in that structure —
  two entries where two houses share a roof, because the evidence does not choose between
  them and the compiler must not either.
- **It is not on screen yet.** T-1181 is the Businesses view and T-1180's building card. A
  card that reads a layer no gate had ever re-derived would show a reader a number nobody had
  checked; the layer and its gate come first.

## Where the pointers go, and who refuses them

| pointer | refused by |
|---|---|
| register row → `business_record_id` | `compile_register.py --check`: a row whose record the layer lacks |
| record → `register_id` | `compile_businesses.py --check`: a record a rebuild does not produce |
| record location → `structure_id` | `tools/validate.py`: a structure id `data/structures/` does not hold |
| index → its own record files | `tools/validate.py` |
| `works_at` crosswalk → a business | `tools/validate.py`: a dangling business id |

## Links

`data/businesses.schema.json` · `tools/compile_businesses.py` ·
`data/research/newspapers/README.md` · `data/research/newspapers/trade_class_rulings.json` ·
`docs/PROVENANCE.md` § the business record · T-1180 · T-1310 · T-1311
