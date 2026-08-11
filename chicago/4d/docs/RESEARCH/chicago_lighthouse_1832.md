# The Chicago lighthouse of 1832

Research memo for `data/structures/chicago_lighthouse_1832.json`. Written 2026-08-11.

---

## 1. There are two towers and only one of them is in this scene

| | first tower | **second tower** |
|---|---|---|
| authorised | Act of Congress 3 March 1831, $5,000 | same appropriation |
| contractor | Samuel Jackson | Samuel Jackson |
| height | **fifty feet**, reached before it fell | **forty feet** |
| walls | **three feet thick** | *not stated* |
| shape | *not stated* | *not stated* |
| fate | **collapsed 30 October 1831, unfinished** | standing on 1835-07-01 |

Andreas, vol. 1, is the primary text for both:

> Before it was fairly completed, however, on October 30, of that year, the structure
> fell. … The walls were three feet thick, and the tower had been raised to a height of
> fifty feet. Samuel Jackson was the contractor. … **Another tower, forty feet high, was
> begun and completed by Mr. Jackson in 1832. It boasted of a fourteen-inch reflector.**

`lighthousefriends_chicago` paraphrases the same passage and adds, from its own
bibliography, that the second tower "employed four, fourteen-inch reflectors in its
bird-cage lantern room" and that it was the first light established on Lake Michigan.

**The first tower is already excluded** — see `data/exclusions.json`.

## 2. The correction this memo exists to make

`docs/research/04-structures-south.md` § 2 reads the 1832 tower as
"**forty feet high; conical stone/masonry**" and tags it `[DOC]` on Andreas,
drloihjournal and lighthousefriends jointly. `data/exclusions.json` called it "the 1832
conical masonry tower" on Andreas's authority.

**Neither "conical" nor "masonry" is in Andreas's sentence or on the lighthousefriends
page.** The only fabric detail either source carries — three-foot walls, fifty feet — is
the description of the tower **that fell down**. Whatever supports "conical", it is not
either of the two sources those entries cite.

The exclusions entry has been amended. The record grades:

- **height 12.19 m (40 ft)** — `documented`, Andreas and lighthousefriends;
- **lantern** — `documented`, lighthousefriends (a lantern; the four reflectors are *not*
  modelled, because a bird-cage lantern is a glazed drum at this level of detail);
- **construction `stone`** — `inferred`, on a real argument and not a guess: the same
  contractor built both towers under the same appropriation on the same site, and the
  first had three-foot walls, which is masonry. That the second was masonry too is
  likely; that it was any particular stone is not claimed;
- **shape, taper, cap, finish, diameter, footprint, position** — `conjectural`. **L44**
  owns them.

## 3. Position

Adjacency is documented three ways and the offset is invented.

- Andreas: "Fort Dearborn and the light-house are placed at the angle thus formed" — the
  bend where the river turned south.
- Wentworth, disposing of the reservation in 1839: the land left over "upon which the old
  light-house was located" was lots "near the Rush-Street bridge", which is at the river
  north of the fort.
- Fergus, of the 1850 view: River Street runs between the block-house and the
  light-keeper's.

All of that says *close*, and *north or west*, and *near the water*. The record puts it
about **65 m north-west of the fort's centre** on the river bank, `conjectural`, with the
uncertainty stated at nearer 60 m than the 20 m the rest of the complex carries.

## 4. Keepers

Samuel Lasby (Andreas; "Samuel C. Lasby" in the Chicago Magazine of March 1857) was the
first keeper, at $350 a year with quarters. **Who kept it on 1835-07-01 was not
established**: Wentworth names William M. Stevens as keeper when he arrived in October
1836 and no source reached covers the gap. Mark Beaubien was the last. No keeper's
dwelling is modelled — a small house beside the tower is plausible and unattested.

## 5. What would settle it

The Light-House Board's annual reports; a keeper's return; or a measured reading of the
1850 von Schneidau daguerreotype or the 1855 Hesler photograph, in both of which the tower
stands. Any of those settles the shape at once and would move most of L44 to Resolved.
