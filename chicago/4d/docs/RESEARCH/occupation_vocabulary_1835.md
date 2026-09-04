# The trades the residents vocabulary had no word for (T-0418)

`data/residents/` speaks a CLOSED occupation vocabulary, declared in the
`vocabulary` block of `data/residents/index.json`, and
`tools/compile_register.py`'s `TRADE_TO_OCCUPATION` is the whole of the translation
from the prose a newspaper prints into it. The table is deliberately a table rather
than a matcher: a fuzzy trade match would silently retire an invented household on a
word that happened to collide, which is how every milliner in this corpus was once
compiled as a grain MILLER (T-0376).

The cost of a closed vocabulary is that a trade with no word in it reads back as
`occupation: null` — indistinguishable from a person the papers never gave a trade at
all. T-0373's pass refused 36 people on exactly that account: the papers DO print
their trade, and the vocabulary could not say it. This note is the adjudication of
every one of those printed phrases. Sixteen of them gained a word, three of them
already had one and only wanted a needle to reach it, and ten are refused with the
reason set out below.

## The rule that shapes both halves

**A word may fill a null; it may never displace a reading the register already
makes.** The T-0418 needles are a SECOND table (`TRADE_TO_OCCUPATION_T0418`), asked
only after the established one has failed across every trade the corpus prints for a
person and the trade of his firm. Without that ordering the additions would have cost
more than they bought: John Watkins, who kept the town's first school and also sold
books, would have stopped being a `schoolteacher`; E. K. Hubbard, printed both as a
merchant and as agent for the Howard Fire Insurance Company, would have stopped
retiring the merchant household the town invented for want of him. Neither is a
near-miss — both trades are printed for both men — but a ticket about people the
register reads NOTHING for has no business rewriting people it already reads.

Re-derived under that rule the change is purely additive: 52 people and 14 businesses
went from `null` to a word, no reading changed, and every action count in
`register_1835.json` (`enrich` / `new_resident` / `replace_invented`) is untouched.

## The sixteen words gained

| printed | word | who, in the 36 |
|---|---|---|
| bookseller | `bookseller` | Aaron Russell |
| stationer | `stationer` | (Russell's second trade; reached where it stands alone) |
| tinsmith, sheet iron worker | `tinsmith` | J. K. Botsford, W. Keeney |
| founder | `founder` | M. Jones, Wm. Jones |
| stove dealer, stove and hollow ware | `stove_dealer` | the Joneses' second trade |
| provision dealer | `provision_dealer` | Edward Simons, Silvester Marsh |
| keeper of the Exchange Coffee House | `coffee_house_keeper` | George Smith |
| refectory keeper, restorator keeper | `refectory_keeper` | J. A. Collett |
| insurance agent | `insurance_agent` | Hiram Hugunin |
| master mariner | `master_mariner` | (Hugunin's second trade) |
| harbour agent | `harbour_agent` | J. Allen, whose record places him at the Piers of the Chicago Harbor |
| house and land agent, house and lot agent | `land_agent` | W. G. Blanchard |
| Register of the (United States) Land Office | `land_office_register` | James Whitlock |
| sheriff, Sheriff of Cook County | `sheriff` | Stephen Forbes, Silas W. Sherman |
| militia officer | `militia_officer` | Josiah Stillman |

Two of these are offices rather than trades, and the ticket asked first whether
`data/residents/` should carry an office at all. **It already does, and has since the
vocabulary was written**: `justice_of_the_peace`, `postmaster`, `county_clerk`,
`indian_agent`, `sub_agent` and `lighthouse_keeper` are all offices, held by men whose
livelihood at Chicago they were. The precedent settles the question for the town's own
offices — a sheriff of Cook County held that office at the county seat, which was this
town — so it did not need to go to the owner. It does NOT settle it for an office held
somewhere else, which is the first refusal below.

## The three words that already existed and had no needle

`justice_of_the_peace`, `postmaster` and `army_officer` were in the vocabulary from
the beginning; nothing in `TRADE_TO_OCCUPATION` ever reached them. (`postmaster` had
one needle, `post office`, which the phrase "postmaster" does not contain.) Adding the
three needles is what gives Cornelius C. Van Horn, Stephen M. Salisbury and James
Walker their bench; L. F. Arnold his post office; and E. Kirby Smith, J. Green,
L. T. Jamison and Lieut. Allen their commissions.

## The ten refusals, and why each one stands

They are recorded in code as `TRADE_NOT_IN_VOCABULARY` in
`tools/compile_register.py`, matched on the WHOLE printed phrase rather than as a
substring — a refusal is a ruling about one phrase, and a substring refusal of "agent"
would quietly retire the insurance agent, the harbour agent and the land agent three
rows above it. The set is checked BEFORE both tables, which is what keeps the
Postmaster General of the United States out of the `postmaster` needle.

**An office of another government seat.** This is the vocabulary of the town's
RESIDENTS. A word here is an invitation to the mint pass to raise a Chicago household
for a man the same record places elsewhere, and the mint's placement refusal cannot be
relied on to catch him — it fires on a place the gazetteer records, and two of these
three carry no place at all.

- `postmaster general` — W. T. Barry, Postmaster General of the United States, whose
  name reaches the Democrat of 17 September 1834 from Washington.
- `governor of illinois` — Joseph Duncan, whose own gazetteer record places him at
  Vandalia.
- `judge of the fifth judicial circuit` — Richard M. Young, a circuit bench and not a
  Chicago livelihood.

**A single act, not a living.**

- `appraiser` — Timothy J. Clark, Richard M. Sweet and Jeremiah Walker are the three
  men named in ONE notice, of 26 November 1833, to appraise ONE estate. Nobody was an
  appraiser for a living.
- `administratrix` — Harriet Bradford's role in one probate, in one notice.
- `judge of election` — E. Peacock's one day's duty at one poll.

**Named, but not named as anything.**

- `agent` — Col. Samuel Miller is "Agent" and the notice says of what: nothing. (His
  record also places him at Michigan City, so the mint refuses him twice over.)
- `mechanic` — Wm. Payne. "Mechanic" is the papers' word for any skilled hand, and
  choosing which hand would be invention of exactly the kind this project exists not
  to make.

**A property relation, not a trade.**

- `steamboat owner` — J. F. Wight. The notice gives the vessel he owned, not the work
  he did. If this reconstruction is to carry vessel ownership it belongs on the boat's
  own record in `data/boats/`, joined to the man, rather than inside his trade.

**An itinerant.**

- `ventriloquist` — R. Kenworthy has one notice, of 11 June 1834, one night's
  entertainment, and no second issue that puts him in the town at all.

## What this note does not settle

The 36 are the people the register reads a trade for and cannot say. Sweeping the
whole gazetteer the same way finds **131** people in that position, so about 95 printed
trades are still unread — ship, schooner and sloop masters (a large and coherent
group), clergymen and Baptist pastors, livery stable keepers, hatters, brewers,
carriage and sleigh makers, confectioners, pedlars, land office receivers, town
clerks and trustees, and the state and federal offices that belong with the refusals
above. They are the same shape of question and not this ticket's list; they are filed
as their own ticket.
