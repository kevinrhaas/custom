# The trades the papers print, and the words `data/residents/` has for them

**T-0418.** `data/residents/` speaks a CLOSED occupation vocabulary and
`tools/compile_register.py` is the whole of the translation into it. That table is
deliberately a table rather than a matcher — a fuzzy trade match would silently retire an
invented household on a word that happened to collide, which is exactly the fault T-0376
found when every milliner in the corpus was being compiled as a MILLER. The cost of the
closed table is that a trade nobody has added is a trade the register cannot read.

On 2026-08-29 that cost was **thirty-three documented people**, each refused by
`tools/mint_placed_residents.py` under a sentence that named no decision:

> the corpus prints a trade the residents vocabulary has no word for (tinsmith)

The refusal itself is right — minting a printed tinsmith as trade-less loses the trade the
corpus prints, and this project records what is missing rather than filling it. What was
wrong is that the sentence was a to-do written into the town's data, and nothing counted
it. This file is the ruling on all thirty-three, and `tools/mint_placed_residents.py
--gate` is what stops the queue re-forming.

## The four principles

They are stated here once and cited by every row below.

1. **An office exercised somewhere other than this town is not a Chicago occupation.**
   The vocabulary already carries offices — `postmaster`, `justice_of_the_peace`,
   `county_clerk`, `indian_agent`, `sub_agent`, `lighthouse_keeper` — so the question
   settled here is not *may an office be an occupation*; the project answered that years
   of records ago. It is **where the office was held.** The Postmaster General of the
   United States is named in this town's post-office notices and sat at Washington.
2. **An appointment made for ONE proceeding is not a trade.** An appraiser is appointed by
   the county court over one estate; a judge of election serves one poll; an administratrix
   holds a capacity in one probate. Each of those men and women had a trade on the day
   after, and the corpus does not print it.
3. **A word that names no particular trade may not be resolved into one.** "Agent" and
   "mechanic" are the two, and both are exactly the milliner-compiled-as-miller fault under
   another word: mapping "mechanic" to `labourer` or `builder` gives a man a trade the
   paper never gives him.
4. **Owning a thing is not practising a trade.**

## The words the vocabulary gained

Fourteen, all period-correct and all printed in this corpus. `data/residents/index.json`
carries them; `compile_register.TRADE_TO_OCCUPATION_T0418` is the needle table.

| printed trade | word | who prints it |
|---|---|---|
| army officer (and the duties printed beside it — Major commanding the post, post adjutant, acting commissary of subsistence, regimental adjutant) | `army_officer` *(already in the vocabulary; it had no needle)* | 9, incl. J. Green, E. Kirby Smith, L. T. Jamison, Lieut. James Allen |
| bookseller, booksellers | `bookseller` | 5, incl. Aaron Russell, Benj. H. Clift |
| stationer, stationers | `stationer` | 4, the same shops |
| founder | `founder` | 5, incl. Byram King, G. W. Keeney, M. and Wm. Jones |
| harbour agent | `harbour_agent` | J. Allen |
| insurance agent, fire insurance agent | `insurance_agent` | 4, incl. Hiram Hugunin, E. K. Hubbard |
| justice of the peace | `justice_of_the_peace` *(already in the vocabulary; no needle)* | 9, incl. Stephen M. Salisbury, James Walker, C. C. Van Horn |
| keeper of the Exchange Coffee House | `coffee_house_keeper` | George Smith |
| land agent, house and land agent, house and lot agent | `land_agent` | 7, incl. W. G. Blanchard, F. G. Blanshard, Gholson Kercheval |
| master mariner | `master_mariner` | Hiram Hugunin |
| postmaster | `postmaster` *(already in the vocabulary; the only needle was "post office")* | 11, incl. Levi F. Arnold, Thomas Galaher, John S. C. Hogan |
| provision dealer | `provision_dealer` | 6, incl. Silvester Marsh, Daniel Elston |
| refectory keeper, restorator keeper | `refectory_keeper` | J. A. Collett |
| Register of the Land Office, register, United States Land Office | `land_office_register` | James Whitlock |
| sheriff, Sheriff of Cook County | `sheriff` | Silas W. Sherman, Stephen Forbes |
| tinsmith | `tinsmith` | 4, incl. J. K. Botsford, W. Keeney |
| ventriloquist | `ventriloquist` | R. Kenworthy |

**Two of these words are carried and not yet spent.** `stationer` and `master_mariner` are
in the vocabulary and no person record uses either, because every man who prints them also
prints a trade the settled table already had a word for and that word wins (below). They
are kept rather than dropped: the printed trade has a word, which is what this ticket
asked for, and the next transcription may print one of them alone.

**`restorator keeper` takes `refectory_keeper`, and that is a judgement.** The two are one
trade under two printed names, and the man who proves it is the one who prints both:
J. A. Collett advertised as a refectory keeper and as a restorator keeper. The word is his
own, so this is not a near miss.

## The rule that keeps a new word from taking a settled one

`best_occupation` asks the SETTLED table across every trade a person is printed with, and
only then the table this ticket added. Without that ordering, adding `insurance_agent`
would have quietly stopped **E. K. Hubbard** being the documented merchant who retires an
invented merchant's household — the gazetteer sorts his trades alphabetically, "insurance
agent" sorts before "merchant", and the register would have changed its mind about him
with nothing in the diff to say why. A T-0418 word fills a gap; it never contests.

The same ordering is why `stove dealer`, `sheet iron worker` and `stove manufacturer` cost
nothing: the men who print them also print `founder` or `tinsmith`.

## The printed roles that were refused a word, and why

`compile_register.TRADE_RULED_NOT_AN_OCCUPATION` holds these with their reasons, matched on
the WHOLE printed phrase rather than on a substring — which is the only way "postmaster
general" can be refused while "postmaster" is kept.

| printed role | principle | why |
|---|---|---|
| postmaster general | 1 | the cabinet office, held at Washington by W. T. Barry. This town's post office is `postmaster`, and its keeper is not the officer its notices are signed under. |
| Governor of Illinois | 1 | a state office, exercised at Vandalia. The corpus prints Joseph Duncan's proclamations here; it does not put him in the town. |
| Secretary of State of Illinois | 1 | the same reading (A. B. Field). |
| Secretary of War | 1 | a cabinet office at Washington (Lewis Cass). |
| Judge of the fifth Judicial Circuit · circuit judge | 1 | a judge who rode a circuit of many counties (Richard M. Young, Sidney Breese). Real office, not a livelihood carried on here. |
| judge of election | 2 | one poll (E. Peacock). |
| appraiser | 2 | one probate, by appointment of the county court. Four men are printed as appraisers in this corpus and not one of them is printed as anything else. |
| administratrix | 2 | a capacity in one estate, and the only thing the corpus prints of Harriet Bradford. It is the standing in which she advertised, not her work. |
| militia officer | 2 | a commission held beside a livelihood, in a militia that mustered a few days a year (Josiah Stillman). The corpus prints no livelihood for him. |
| agent | 3 | agent for whom, or for what, is not printed (Samuel Miller). |
| mechanic | 3 | in 1835 the general word for a skilled tradesman — the "mechanics" of a town were its whole artisan class. It names no particular trade (Wm. Payne). |
| steamboat owner | 4 | the corpus prints J. F. Wight's boat and not his work. |
| sheet iron worker · stove manufacturer · stove dealer · stove and hollow ware dealer | — | the stove trade's several printed names. Every man who prints one also prints `founder` or `tinsmith`, which are the words this vocabulary carries; a man printed only as a DEALER in stoves is left without a word rather than made a founder. |

**Eleven people are held by these rulings**, and they are held with a reason now rather than
with a to-do: `tools/mint_placed_residents.py --report` prints "the corpus prints a role
this project has ruled is not an occupation" beside each of them.

## What this deliberately does not do

- **It does not reach the vessel masters.** Thirteen men in this corpus are printed as a
  ship, schooner or sloop master and nothing else. `master_mariner` is the right word for
  the rank and the reason they are not minted is not a vocabulary gap at all — they are
  known from arrivals-and-clearances lists, which say a vessel entered this port and not
  that her master lived in this town. Most are refused before the trade is ever reached, on
  a single printed surname. Deciding whether a lake captain who cleared Chicago is of the
  town is a residency question and is its own ticket.
- **It does not add a word for the Land Office's RECEIVER.** `land_office_register` is one
  of the office's two officers and E. D. Taylor is printed as the other. A needle on "land
  office" alone would have made a receiver a register, which is precisely the near miss
  this file exists to refuse, so the two needles name the register in full and the receiver
  waits for its own row.
- **It does not promote anybody.** Every person these words unblock is minted by the pass
  that already owned him, under that pass's own refusals, and arrives without a dwelling,
  a division or a family. The PERSON is `attested` — a paper prints his name and his trade.
  Everything the household says around him is written as unattested, because it is.

**Sources.** `data/research/newspapers/gazetteer.json` (the printed trades, with the claim
behind each), `data/research/newspapers/register_1835.json` (the compiled reading),
`data/residents/index.json` § `vocabulary.occupations` (the closed set).
