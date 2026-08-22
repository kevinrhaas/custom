#!/usr/bin/env python3
"""Generate the town's business signboards — what each one says, and how it hangs.

WHAT THIS IS. `docs/ROADMAP.md` K5 (b) asked for *"signboards on businesses"* and ticket
T-0039 built the layer: a plank on a bracket, hung off a wall this project had already
drawn, on every frontage a rule selected. Every one of those boards was BLANK, and every
one was hung the same way, because L25 and L130 read the absence of any recorded WORDING
as a reason to paint nothing at all.

T-0066 OVERRULES THAT, on the owner's instruction of 2026-08-18, verbatim: *"you can and
should put the name of the location on the sign board. the sign boards should have
variation in color and style and signage font and color, some signs may hang from an
awning and others may be on the building or painted on the face of the building. you
need to add more signage and be period correct and it is fine if they are
reconstructions."* The standing ruling on invention applies: *"you are totally fine to be
liberal with adding reconstructed items when i ask for things, you can just label and
mark them as such."* So this record now carries, for every board:

  * the WORDING — what a signwriter lettered on that frontage: see SIGN_WORDING below;
  * a MOUNTING — bracket-hung over the footway, hung under an awning, fixed flat on the
    building, standing on a post at the street edge, or the name painted straight onto
    the face of the building;
  * a STYLE — ground colour, letter colour, letterform and panel, from a table of the
    combinations the trade actually used, assigned so that no two boards within
    `NEIGHBOUR_M` of each other share a mounting, a style or a ground colour.

`docs/LIBERTIES.md` **L159** is the claim for the mounting and the style, and **L166**
for the wording.

T-0130 CORRECTS THE WORDING, and the correction is the owner's, 2026-08-21, verbatim:
*"philo would not have referred to his own place as log drug store, it would be philo
carpenter, drugs and medicines, or druggist or whatever he would have referred to himself
as on the sign, that may be different than the name of the building for us, the sign may
read differently historically."* And, of the next one: *"same with hogan's store."* And,
widening it to the set: *"i guess do a pass on all those signs and make sure they feel
right for the era."*

T-0066 painted the STRUCTURE RECORD'S OWN `name` on the board, less a trailing
parenthetical, and this docstring used to defend that: *"the card a visitor opens by
tapping the board has to say what the board says."* THAT COLLAPSED TWO DIFFERENT OBJECTS.

  * A record's `name` is OUR LABEL FOR A BUILDING — descriptive, disambiguating, written
    so a modern reader knows which structure is meant: "Philo Carpenter's Log Drug Store",
    "Hogan's Store", "Tremont House (the first)". The word "log" is in there because the
    walls are log. No druggist painted the construction of his own shop on his own board.
  * A SIGNBOARD carries what the TRADE lettered — the proprietor or the firm, and the
    trade he practised, in the register a signwriter actually worked in.

So the two fields are now separate and are allowed to differ. The structure keeps its
`name` for the card and the search box; the board carries `sign_text` out of
SIGN_WORDING. What the two must still agree about is WHO THIS IS: every entry declares a
`sign_identity` — the proprietor, the firm or the house — and this file refuses to build
unless that identity appears in the board AND in the card. `tools/smoke_renderer.mjs`
asserts the same thing at run time, over every sign and at the Tremont's own board. That
is a CORRECTION of T-0066's string-equality assertion, not a relaxation of it.

THE RULE THAT CHOOSES A FRONTAGE, and every clause is doing work. A structure gets a
sign iff

  1. it is a NAMED record — the id does not begin `inf_` or `recon_` and the name does
     not begin "Reconstructed". The archetype tables already carry this rule in as many
     words: *never invent business, sign text or goods for an anonymous slot*. An
     anonymous roof dealt a trade by a schedule has no proprietor to announce, and now
     that the boards carry NAMES the clause matters more than it did when they were
     blank: there would be no name to paint;
  2. its `function` is a trade this project will announce. Two classes of them now:
     a PUBLIC TRADE, whose customer was a stranger arriving on foot off the street (a
     public house, a lodging house, a shop counter, the auction room, the printing
     offices that also sold over one) — these get a BOARD; and, added by T-0066, a
     WORKS OR WAREHOUSE trade, whose custom came by name and by cart — these get the
     firm's name PAINTED ON THE BUILDING and never a board swinging over a footway
     nobody walked. Stables, churches, schools, the court-house, the jail, the agency
     house and the fort stay outside both lists;
  3. that function is `attested` or `inferred`. A `reconstructed` trade gets no sign —
     inventing a sign for an invented business is invention squared;
  4. it is standing on the scene date (it is in `data/sidecars/1835/index.json`);
  5. it does not already carry a sign. One record does, and duplicating it would put
     two boards on the Wolf Point Tavern;
  6. it does not already carry a NAMED board on a post at its corner on the frontage
     layer (the Green Tree — T-0082, L135);
  7. and, for the works and warehouse class only, its name carries a PROPRIETOR — a
     possessive or an ampersand. A works painted whose it was. A building this project
     names by a later nickname ("The Old Bank Building") has no proprietor to paint,
     and painting the nickname would put a twentieth-century label on an 1835 wall.

WHERE THE SIGN GOES is then DERIVED, not placed. `docs/GLB-CONTRACT.md` fixes the frame:
polygon `u` → +X, polygon `v` → −Z, and `rotation_deg` is the FACADE BEARING, so the
front wall is the footprint's own max-`v` edge and the direction it faces is the bearing
itself. A hanging board hangs to one side of that edge's centre and clear of the eave;
a wall board and a painted name are centred on it. A POST is the one mounting that
stands in the street rather than on the building, so it is refused — in writing, and the
next mounting in the cycle is taken — wherever the fronting street's own travelled track
comes too close, or wherever the frontage layer already lays a plank walk outside that
wall. That test is `data/streets/1835.json`'s, the same one
`tools/generate_frontage_works.py` uses.

    python3 tools/generate_business_signboards.py            write the record
    python3 tools/generate_business_signboards.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STRUCTURES = DATA / "structures"
STREETS = DATA / "streets" / "1835.json"
FRONTAGE = DATA / "frontage"
OUT = DATA / "signage" / "town_business_signboards.json"

# Clause 2, first class. Trades whose customer was a stranger off the street. The
# value on the left is `function.value` as the structure records write it; the phrase
# on the right is why a sign belongs on that door and is quoted into the record.
PUBLIC_TRADES = {
    "tavern_inn": "a public house takes its custom from the road",
    "hotel": "a public house takes its custom from the road",
    "boarding_house": "lodging is sold to arrivals who have to find the door",
    "store": "a counter open to the street",
    "store_residence": "a counter open to the street, with the keeper living over it",
    "store_and_dwelling": "a counter open to the street, with the keeper living over it",
    "dwelling_and_store": "a counter open to the street, with the keeper living over it",
    "grocery_and_provision_store": "a counter open to the street",
    "drug_store": "a counter open to the street",
    "forwarding_and_commission_store": "a counting-room a shipper has to find from the wharf",
    "auction_room": "a sale room whose whole trade is being found on the day",
    "saddlery_and_harness_shop": "a craft shop selling finished goods over a counter",
    "printing_office": "an office that took job work and subscriptions from callers",
    "printing_office_and_store": "an office that took job work and sold over a counter",
    "physicians_office": "a consulting room a stranger has to be able to find",
    "shop": "a shop front on a street of stores",
}

# Clause 2, second class — added 2026-08-21 with T-0066. A works or a warehouse did not
# hang a board over a footway; it painted the firm's name on the front, where a carter
# and a shipper could read it off the river or off the road. That is the distinction
# L130's excluded-trades note drew when it left these frontages mute, and the answer to
# it is a DIFFERENT MOUNTING rather than a different silence.
WORKS_TRADES = {
    "blacksmith_shop": "a smith's shop, named on its front for the carter who needs one",
    "forwarding_commission_warehouse": "a warehouse names its firm for the shipper on the river",
    "warehouse_and_slaughter_yard": "a warehouse names its firm for the shipper on the river",
    "slaughterhouse_packing": "a packing house names the firm the drover is delivering to",
    "packing_house": "a packing house names the firm the drover is delivering to",
    "tannery": "a tan-yard names its master for the trade that brings him hides",
    "soap_candle_manufactory": "a manufactory names the firm whose goods leave by the cart-load",
    "brickyard": "a brickyard names its owner for the builder ordering by the thousand",
}

# Which cycle of mountings a trade draws from. Two frontages of the same class in the
# same street get DIFFERENT mountings because the cycle advances; two of different
# classes differ because the cycles do not start in the same place.
TRADE_CLASS = {
    **{t: "house" for t in ("tavern_inn", "hotel", "boarding_house")},
    **{t: "counter" for t in (
        "store", "store_residence", "store_and_dwelling", "dwelling_and_store",
        "grocery_and_provision_store", "drug_store", "shop",
        "saddlery_and_harness_shop")},
    **{t: "office" for t in (
        "printing_office", "printing_office_and_store", "auction_room",
        "forwarding_and_commission_store", "physicians_office")},
    **{t: "works" for t in WORKS_TRADES},
}

# THE MOUNTINGS, and why each class draws from the cycle it does.
#
#  * a PUBLIC HOUSE is read from up the road by somebody who has not arrived yet, so its
#    name goes where it is seen furthest — under a hood over the door, out on a bracket,
#    or on a post at the street edge (which is exactly what the Green Tree does, images 6
#    and 7 of the owner's brief, and what T-0082 already drew there);
#  * a COUNTER is read from the footway by somebody already outside it, so a bracket
#    board over the walk, a board fixed on the front, an awning board, or the name
#    straight on the boards of the building — the Tremont street scene (image 5) shows a
#    whole row of painted fronts;
#  * an OFFICE or a sale room is a door among doors and mostly took a modest board on the
#    building itself;
#  * a WORKS paints its front and never hangs anything (see WORKS_TRADES above).
MOUNTING_CYCLE = {
    "house": ["awning_board", "bracket_board", "post_board"],
    "counter": ["bracket_board", "wall_board", "awning_board", "facade_painted"],
    "office": ["wall_board", "bracket_board", "facade_painted"],
    "works": ["facade_painted"],
}

# THE STYLES. Ground, letters, letterform and panel — the combinations an American
# signwriter of the 1830s worked in. Nothing here is a Chicago record: no wording,
# device or colour of any sign in this town survives, so the whole table is
# reconstruction and is graded as one (L159). What it is NOT is arbitrary: black
# grounds with gilt letters, white lead grounds with black, ochre (the cheapest
# pigment on any colourman's shelf), Venetian red, Prussian blue and Brunswick green
# are the trade's ordinary stock, and the letterforms are the four the period's
# specimen books actually sell — the signwriter's roman, the fat face that is the
# 1830s display letter, the Egyptian slab that arrives with it, and the plain block.
# `aspect` is the board's width-to-height and is part of the variation: two boards on
# one street should not be the same rectangle either.
STYLES = [
    {"id": "gold_on_black", "ground": "#141009", "letter": "#c9a227",
     "face": "signwriter", "panel": "plain", "aspect": 1.85,
     "note": "gilt letters on a black ground, shaded — the commonest painted board of the trade"},
    {"id": "black_on_white", "ground": "#e8e1cf", "letter": "#191410",
     "face": "fat_face", "panel": "double_rule", "aspect": 2.10,
     "note": "black on a white lead ground, the cheapest board a signwriter could sell"},
    {"id": "cream_on_green", "ground": "#1d3226", "letter": "#e7ddc0",
     "face": "signwriter", "panel": "single_rule", "aspect": 1.70,
     "note": "cream on a Brunswick-green ground"},
    {"id": "black_on_ochre", "ground": "#c19a52", "letter": "#1a1309",
     "face": "egyptian", "panel": "plain", "aspect": 2.35,
     "note": "black Egyptian on a yellow-ochre ground"},
    {"id": "cream_on_red", "ground": "#7c3020", "letter": "#efe3c8",
     "face": "fat_face", "panel": "single_rule", "aspect": 1.95,
     "note": "cream fat face on Venetian red"},
    {"id": "white_on_blue", "ground": "#22344f", "letter": "#e9e6dc",
     "face": "grotesque", "panel": "plain", "aspect": 2.20,
     "note": "white block letters on a Prussian-blue ground"},
    {"id": "gold_on_green", "ground": "#16261c", "letter": "#c8a63c",
     "face": "signwriter", "panel": "oval", "aspect": 1.75,
     "note": "gilt letters in an oval field on a dark green ground"},
    {"id": "black_on_timber", "ground": "#cbc2b1", "letter": "#241a10",
     "face": "grotesque", "panel": "plain", "aspect": 2.00,
     "note": "black on a bare weathered board — the tone L130 hung the town's blank boards in"},
    {"id": "red_on_white", "ground": "#e9e2d1", "letter": "#8c2f1f",
     "face": "egyptian", "panel": "oval", "aspect": 1.80,
     "note": "vermilion Egyptian on a white ground"},
    {"id": "white_on_brown", "ground": "#4a3121", "letter": "#e6dccb",
     "face": "fat_face", "panel": "double_rule", "aspect": 2.45,
     "note": "white fat face on a chocolate-brown ground"},
]

# Clause 3.
TRADE_GRADES = {"attested", "documented", "inferred"}

# --- WHAT THE BOARDS SAY (T-0130) -------------------------------------------
#
# THE REGISTER, taken from the advertisements themselves rather than from a modern eye:
# the PROPRIETOR OR FIRM first and largest, the TRADE beneath it, and the PLACE last and
# smallest. Carpenter's 1835 advertisement heads itself "PHILO CARPENTER, Wholesale &
# Retail Druggist, … South Water Street, Chicago"; Brewster, Hogan & Co.'s reads
# "BREWSTER, HOGAN & CO. Forwarding & Commission MERCHANTS, Chicago—Illinois". Both put
# the man or the firm on the top line in the largest letter, the trade in a second face
# beneath, and the place last. That hierarchy is the record's (`sign_lines` carries the
# role of each line) and `renderers/web/js/signage.js` letters it.
#
# PERIOD SPELLING IS THEIRS AND IS KEPT. "Stationary" for stationery, "Sattinetts",
# "Merselles", the em-dashed "Chicago—Illinois" — a board that modernises its own
# spelling stops feeling like 1835, which is half of what the owner asked for.
#
# WHERE THE 1833 AND 1835 COPY DIFFER, THE 1835 WINS. The scene is 1 July 1835 and firms
# rewrote their lines: Carpenter advertises "DRUGS AND MEDICINES" in 1833 and calls
# himself "Wholesale & Retail Druggist" by 1835.
#
# THE TIERS, AND WHY NOT ONE OF THEM IS `attested` YET. The owner supplied seven pages of
# 1833-35 Chicago newspaper advertising as IMAGES IN CONVERSATION on 2026-08-21 and ruled,
# verbatim: *"I will give you all those data sources later in a more comprehensive form
# proceed where you can and label reconstruction or inferred with a note as you like"*.
# So a wording taken off those pages is graded `inferred` — reasoned from a document about
# THIS PARTICULAR FIRM — and every one of those notes says what the advertisement says,
# where it came from, that the transcription is not yet a citation, and that it is to be
# UPGRADED TO `attested` when the page images land in `data/sources/assets/`. A
# transcription in a ticket is not a source record, and this file will not pretend it is.
# A wording with no surviving advertisement is `reconstructed` and built out of the trade
# vocabulary those same pages evidence.
PENDING = (
    "TRANSCRIBED FROM OWNER-SUPPLIED PAGE IMAGES, 2026-08-21, WHICH ARE NOT YET COMMITTED "
    "to data/sources/assets/, so this is graded `inferred` rather than `attested` on the "
    "owner's own ruling of that day: \"I will give you all those data sources later in a "
    "more comprehensive form proceed where you can and label reconstruction or inferred "
    "with a note as you like\". UPGRADE THIS VALUE TO `attested` when the pages are "
    "committed as a source record and this note can cite one."
)

# The device Carpenter's own advertisement names. A device belongs to a shop only where
# that shop's own advertisement names one — see the note.
DEVICES = {
    "golden_mortar": {
        "id": "golden_mortar",
        "label": "a mortar and pestle, gilt",
        "colour": "#d9b036",
        "shade": "#7a5c14",
        "confidence": "inferred",
        "note": (
            "A CHICAGO SIGNBOARD DESCRIBED BY ITS OWN OWNER, IN PRINT, IN THE SCENE YEAR. "
            "Philo Carpenter's 1835 advertisement heads itself \"PHILO CARPENTER, "
            "Wholesale & Retail Druggist, AT THE SIGN OF THE GOLDEN MORTAR, South Water "
            "Street, Chicago\". A mortar and pestle is the druggist's universal device, "
            "and a Detroit house advertising on the same pages \"at the sign of the Large "
            "Pitcher\" shows the convention was live and ordinary. So this board carries "
            "the device PAINTED rather than the phrase lettered: the sign is what he "
            "described, not a sentence about it. THIS IS THE OPPOSITE CASE TO L25, WHICH "
            "STANDS UNTOUCHED — L25 withholds the Wolf Point wolf because that IMAGE was "
            "never described, and here the owner of the shop describes his own board. "
            "What is invented is the DRAUGHTSMANSHIP: the outline is a plain bowl, rim "
            "and pestle, no ornament and no ground line. " + PENDING
        ),
    },
}

# HOW MANY LINES EACH MOUNTING CARRIES. A signwriter letters what fits: a plank swinging
# over a footway takes the man and his trade, and a board fixed flat on a wall or a name
# painted across a whole front has room for the street as well. This is why `sign_text`
# is resolved AFTER the mounting is chosen and not before.
LINES_BY_MOUNTING = {
    "bracket_board": 2,
    "awning_board": 2,
    "post_board": 2,
    "wall_board": 3,
    "facade_painted": 3,
}

# EVERY BOARD IN THE TOWN, in the trade's own words where they survive.
#
#   name         line 1 — the proprietor, the firm or the house, largest
#   trade        line 2 — the trade, in the period's own words
#   trade_short  line 2 where the mounting has room for two lines only
#   place        line 3 — the street or the town, smallest, where the board has room
#   identity     the token the board and the card must BOTH carry (see _norm)
#   grade        `inferred` (a firm's own advertisement) or `reconstructed`
#   device       a painted device, where the firm's own advertisement names one
#   sources      COMMITTED source records only — the owner's 2026-08-21 pages are not
#                committed and are described in `why` instead
#   why          what the evidence says, quoted, and what would upgrade the grade
SIGN_WORDING = {
    "bates_auction_room": {
        "name": "J. BATES, JR.", "trade": "Auctioneer", "identity": "Bates",
        "grade": "inferred",
        "why": (
            "His own advertisement signs itself \"J. BATES, JR.\" over the single trade "
            "word \"Auctioneer\" — the whole of a sale-room's copy, because an auctioneer "
            "sells his name. The record's own label, \"John Bates Jr.'s Auction Room\", "
            "describes the building for a modern reader; the board carries the man. "
            + PENDING
        ),
    },
    "brickyard_north_side": {
        "name": "T. K. BLODGETT", "trade": "Brick Maker", "identity": "Blodgett",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this yard is in the pages read. Andreas names Tyler K. "
            "Blodgett and calls him \"undoubtedly the first brick-maker\", and the "
            "record's own occupants block carries him, so the board is built in the "
            "register the pages evidence — proprietor, then trade — out of the trade's "
            "own word. Reconstructed: nobody records that this yard announced itself at "
            "all, let alone in these words."
        ),
    },
    "brown_boarding_house": {
        "name": "RUFUS BROWN", "trade": "Boarding House", "identity": "Brown",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this house is in the pages read. \"Boarding House\" is "
            "the period's own term and the record's own function; the proprietor is the "
            "record's. Reconstructed."
        ),
    },
    "carpenter_south_water_store": {
        "name": "PHILO CARPENTER", "trade": "Wholesale & Retail Druggist",
        "trade_short": "Druggist", "place": "South Water Street",
        "identity": "Carpenter", "grade": "inferred", "device": "golden_mortar",
        "why": (
            "HIS OWN 1835 WORDS, AND THE SCENE IS 1835. The advertisement heads itself "
            "\"PHILO CARPENTER, Wholesale & Retail Druggist, AT THE SIGN OF THE GOLDEN "
            "MORTAR, South Water Street, Chicago\" and goes on \"has just received and now "
            "offers for sale, one of the largest and best selected assortments of DRUGS "
            "AND MEDICINES, Paints, Oils, & Dye-Stuffs, ever offered in the State of "
            "Illinois\". Man, trade, street — in that order, which is the order the board "
            "letters. THIS IS THE FRONTAGE THE ADVERTISEMENT PLACES ON SOUTH WATER STREET, "
            "so it is this board and not his older Lake Street shop that carries the "
            "golden mortar. The 1833 copy for the same man reads \"DRUGS AND MEDICINES\" "
            "and is used on that older shop, because firms rewrote their lines and this "
            "project models the later day. " + PENDING
        ),
    },
    "chicago_american_office": {
        "name": "CHICAGO AMERICAN", "trade": "Printing Office",
        "identity": "Chicago American", "grade": "reconstructed",
        "why": (
            "The paper was twenty-three days old on the scene date and no advertisement "
            "of its own is in the pages read. A newspaper office announced the PAPER — the "
            "Democrat's own imprint does exactly that — so the board carries the title and "
            "the trade, in the register the pages evidence. T. O. Davis's name is on the "
            "record and deliberately not on the board: a paper's office was known by its "
            "paper. Reconstructed."
        ),
    },
    "chicago_democrat_office": {
        "name": "CHICAGO DEMOCRAT", "trade": "Printing Office",
        "place": "South Water & Clark Streets", "identity": "Chicago Democrat",
        "grade": "inferred", "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "THE PAPER'S OWN IMPRINT, in a source this repository already holds and whose "
            "page images are committed: \"THE DEMOCRAT, Is published every Tuesday, in the "
            "village of Chicago, Cook co. Ill. in the building on the corner of South Water "
            "and Clark-streets.\" That is the office naming itself and its junction, which "
            "is what a board carries. Note precisely what it does NOT settle and the board "
            "does not claim: WHICH of the four corners, which the record argues separately "
            "and which the pencilled \"S. W.\" in that page's margin is a later reader's "
            "gloss on rather than evidence for. Graded `inferred` rather than `attested` "
            "because the imprint is a masthead and not a description of a signboard."
        ),
    },
    "clybourn_slaughterhouse": {
        "name": "A. CLYBOURNE", "trade": "Slaughtering & Packing",
        "identity": "Clybourne", "grade": "reconstructed",
        "why": (
            "No advertisement for this plant is in the pages read. Andreas has Clybourne "
            "killing for the garrison from 1827 and packing commercially from 1833, and "
            "\"packing\" is the trade's own word in this town — Newberry & Dole's own "
            "advertising uses it. The record's label calls the building a \"Log "
            "Slaughter-House\", which is this project describing walls; a drover reading "
            "the front needed the firm and the trade. Reconstructed."
        ),
    },
    "dole_warehouse_south": {
        "name": "GEO. W. DOLE", "trade": "Forwarding & Commission Merchant",
        "trade_short": "Forwarding & Commission", "identity": "Dole",
        "grade": "reconstructed",
        "why": (
            "The firm NEWBERRY & DOLE advertises in both 1833 and 1835 and its warehouse "
            "on the north bank carries that firm's own line. THIS building is Dole's own "
            "1832 warehouse and slaughter yard on the south side, and no advertisement in "
            "the pages read is signed by Dole alone — so the trade words are the firm's "
            "and the single-partner line is ours. Reconstructed for that reason rather "
            "than for any doubt about the trade."
        ),
    },
    "elston_soap_candle_manufactory": {
        "name": "DANIEL ELSTON & CO.", "trade": "Chicago Soap and Candle Manufactory",
        "trade_short": "Soap & Candle Manufactory", "identity": "Elston",
        "grade": "inferred", "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "The firm's own advertisement heads itself \"Chicago Soap and Candle "
            "Manufactory\" over \"DANIEL ELSTON & CO.\", and pays cash for tallow and for "
            "house ashes. It is in the committed issue of 26 November 1833 as well as in "
            "the owner's pages — with one caveat that travels with the name and is the "
            "committed source record's own: the word after the ampersand is OBLITERATED BY "
            "AN INK BLOT, and \"Co.\" is a reasonable expansion rather than a reading. "
            "Graded `inferred` for that, and because an advertisement is not a description "
            "of a board."
        ),
    },
    "exchange_coffee_house": {
        "name": "EXCHANGE COFFEE HOUSE", "trade": "Public House",
        "identity": "Exchange", "grade": "reconstructed",
        "why": (
            "No advertisement for this house is in the pages read. \"Public House\" is E. "
            "Wentworth's own trade line on the 1833 page and is the period's word for what "
            "this building was; the house name is the one Mark Beaubien's successors "
            "christened it with in 1834. A coffee house of these years lodged and fed "
            "people, and the record's own note says so. Reconstructed."
        ),
    },
    "goss_cobb_saddlery": {
        "name": "GOSS & COBB", "trade": "Saddle & Harness Making",
        "place": "Lake & Canal Streets", "identity": "Goss",
        "grade": "inferred", "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "THE FIRM'S OWN WORDS, OFF A COMMITTED PAGE IMAGE, read from the scan on "
            "2026-08-11 and quoted verbatim in this building's own record: \"[Saddle & "
            "H]arness Making. GOSS & COBB, respectfully inform the inhabitants of Chicago "
            "and the neighboring settlements, that they have opened a shop in this "
            "village, on the conner of Lake and Canal-streets\". Heading, firm, address — "
            "which is the whole of the board. THIS IS THE FIRST WORDING IN THE SET THAT "
            "COULD BE UPGRADED: its page is already committed at "
            "data/sources/assets/chicago_democrat_1833_11_26/, and what keeps it "
            "`inferred` is that an advertisement heading is still not a description of a "
            "signboard."
        ),
    },
    "h_jones_store": {
        "name": "JONES", "trade": "Grocery & Provision Store",
        "identity": "Jones", "grade": "inferred",
        "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "The advertisement is headed \"Grocery & Provision Store\" and signed by Jones "
            "— which is the board, in the order the trade wrote it. THE INITIAL IS "
            "DELIBERATELY NOT PAINTED, and that is this record refusing to decide "
            "something its own source record refuses to decide: Andreas writes \"H. "
            "Jones\", the advertisement in the committed issue reads \"B. JONES\", and the "
            "structure record carries the surname and not the initial because B and H are "
            "among the easiest letters to confuse in a display face of this period on a "
            "damaged sheet. A board that picked one would be the signage layer settling a "
            "question the dataset has left open."
        ),
    },
    "harmon_loomis_store": {
        "name": "HARMON, LOOMIS & CO.", "trade": "Dry Goods, Groceries & Hardware",
        "trade_short": "Dry Goods & Groceries", "identity": "Harmon",
        "grade": "inferred",
        "why": (
            "THE 1835 LINE, PREFERRED OVER THE 1833 ONE. The firm advertises in 1835 as "
            "\"HARMON, LOOMIS & CO.\" under the head \"New Goods!\", offering \"Dry Goods, "
            "Groceries and Hard Ware\"; the 1833 pages carry the same house as \"C. & I. "
            "HARMON\" with \"Dry Goods, Crockery, Hardware, Wet and Dry Groceries\" and "
            "again as \"HARMON, LOOMIS & CO.\". The later name is the one standing on the "
            "scene date, and the record's own `aka` already carries both. " + PENDING
        ),
    },
    "hogan_store": {
        "name": "BREWSTER, HOGAN & CO.", "trade": "Forwarding & Commission Merchants",
        "trade_short": "Forwarding & Commission", "place": "Chicago—Illinois",
        "identity": "Hogan", "grade": "inferred",
        "why": (
            "THE IDENTITY IS CORRECTED, NOT JUST THE WORDING. The firm's own advertisement "
            "reads \"BREWSTER, HOGAN & CO. Forwarding & Commission MERCHANTS, "
            "Chicago—Illinois\", and adds dry goods and groceries below. Our label, "
            "\"Hogan's Store\", is a shorthand for one partner; the building's own record "
            "already knows better and lists \"Brewster, Hogan & Co.'s store\" in its `aka` "
            "and names the firm in its change note — the log store was partitioned, post "
            "office on one side and this firm's store on the other. THE PAGES ALSO "
            "DISTINGUISH A SECOND HOGAN and this board is not him: \"J. S. C. HOGAN\", "
            "\"Dry Goods, Groceries, Hardware, Crockery and Glass Ware\", \"South Water "
            "Street, one door below Dearborn\" — a different trade at a different address "
            "from this building at the Lake Street junction. Whether the model should ALSO "
            "carry J. S. C. Hogan's South Water store is a placement question and is "
            "raised, not silently answered. " + PENDING
        ),
    },
    "jh_kinzie_forwarding_store": {
        "name": "JOHN H. KINZIE", "trade": "Forwarding & Commission Merchant",
        "trade_short": "Forwarding & Commission", "place": "Agent, Troy & Erie Line",
        "identity": "Kinzie", "grade": "inferred",
        "why": (
            "His own line, and the 1835 form of it: \"JOHN H. KINZIE, Forwarding & "
            "Commission Merchant … Agent for the Troy & Erie Line\", the 1833 pages "
            "carrying the same man as a \"Storage, Forwarding & Commission Merchant\" for "
            "the same line. The agency is on the third line because that is what a "
            "shipper walking the street needed to read; it is the place line's slot and "
            "it does the place line's job. " + PENDING
        ),
    },
    "kinzie_hunter_warehouse": {
        "name": "KINZIE & HUNTER", "trade": "Forwarding & Commission Merchants",
        "trade_short": "Forwarding & Commission", "identity": "Kinzie",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this firm is in the pages read. The record's own "
            "function is `forwarding_commission_warehouse` and its note says the trade is "
            "held by association with the neighbouring dock rather than by any statement — "
            "Andreas separately has a Kinzie, Hunter & Co. in the LUMBER trade in these "
            "years. So the trade words are the town's own, the firm is the record's, and "
            "the whole line is reconstructed. If the lumber reading is right the board "
            "should read \"Lumber Dealer & Commission Merchant\", which is David Carver's "
            "own 1835 line and is the form to reach for; that is a research question, not "
            "a wording one."
        ),
    },
    "madore_beaubien_house": {
        "name": "MADORE BEAUBIEN", "trade": "Dry Goods & Groceries",
        "identity": "Beaubien", "grade": "reconstructed",
        "why": (
            "No advertisement for him is in the pages read. He was licensed as a merchant "
            "in 1831 — the year the building went up — and the record's own `aka` carries "
            "\"Madore Beaubien's store\", so the board carries the man and the plainest of "
            "the town's own counter trades. The record's label, \"Madore Beaubien's Log "
            "House\", is this project naming a building by its walls. Reconstructed."
        ),
    },
    "mansion_house": {
        "name": "MANSION HOUSE", "trade": "Public House", "identity": "Mansion",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this house is in the pages read, though the 1833 pages "
            "locate Matthias Mason's smithy \"nearly opposite Graves' Tavern\", which is "
            "this building under its keeper's name. \"Public House\" is E. Wentworth's own "
            "1833 trade line. The house name is the one the record carries at the scene "
            "date, when Markle rather than Graves had it. Reconstructed."
        ),
    },
    "mason_blacksmith_shop": {
        "name": "MATTHIAS MASON & CO.", "trade": "Blacksmithing",
        "identity": "Mason", "grade": "inferred",
        "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "The firm's own advertisement is headed \"Blacksmithing Business\" over "
            "\"MATTHIAS MASON & CO.\", on \"Main-street, nearly opposite Graves' Tavern\". "
            "The board takes the firm and the trade word and NOT the address: "
            "\"Main-street\" is a street name this project does not otherwise hold, "
            "recorded as a finding in docs/RESEARCH/residents_1835.md § 7, and lettering "
            "it here would be the signage layer asserting a street the streets layer does "
            "not carry."
        ),
    },
    "miller_house": {
        "name": "MILLER HOUSE", "trade": "Store", "identity": "Miller",
        "grade": "reconstructed",
        "why": (
            "The hardest board in the set, and the wording is deliberately thin. The "
            "record's function on the scene date is a store with the keeper living over "
            "it; its occupants are NOT attested at that date; Samuel Miller had removed to "
            "the place that became Michigan City and the tavern had reverted to store use "
            "after 1832. So there is no proprietor to letter, and the board carries the "
            "name the settlement knew the building by — \"Miller House\", \"Miller's "
            "Tavern\", \"Fork Tavern\" are its own `aka` — over the plainest period word "
            "for what it was doing. Inventing a keeper or a stock would be worse than a "
            "thin board. Reconstructed."
        ),
    },
    "miller_tannery": {
        "name": "JOHN MILLER", "trade": "Tannery", "identity": "Miller",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this tan-yard is in the pages read. The function is the "
            "best-attested thing about the building — \"a log house … that he used as a "
            "tannery, Chicago's first recorded factory\" — and the proprietor is named. "
            "The board carries the two and drops the walls. Reconstructed."
        ),
    },
    "newberry_dole_slaughterhouse_south_branch": {
        "name": "NEWBERRY & DOLE", "trade": "Slaughtering & Packing",
        "place": "South Branch", "identity": "Newberry", "grade": "reconstructed",
        "why": (
            "The FIRM's own advertised line is the forwarding one and it is lettered on "
            "their warehouse. For this plant the pages give nothing: what is recorded is "
            "Andreas's sentence about a slaughter-house on the South Branch where three "
            "hundred cattle and fourteen hundred hogs were packed in its first season. So "
            "the firm is theirs and the trade line is ours, out of the town's own word for "
            "the trade. Reconstructed."
        ),
    },
    "newberry_dole_warehouse": {
        "name": "NEWBERRY & DOLE",
        "trade": "Storage, Forwarding & Commission Merchants",
        "trade_short": "Forwarding & Commission", "place": "Agents, Merchants Line",
        "identity": "Newberry", "grade": "inferred",
        "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "THE 1835 LINE, PREFERRED OVER THE 1833 ONE, and the 1833 one is in a "
            "committed source: \"NEWBERRY & DOLE, Forwarding & Commission MERCHANTS\" in "
            "the issue of 26 November 1833, which this project's own record calls \"the "
            "first contemporary document in this dataset and about as good as evidence of "
            "a trade gets, since the advertiser was paying for it and his customers had to "
            "be able to find him\". By 1835 the firm advertises as \"Storage, Forwarding "
            "and Commission Merchants\" and \"Agents for the Merchants Line\", and the "
            "agency goes on the third line because that is what a shipper needed off the "
            "river. " + PENDING
        ),
    },
    "peck_store": {
        "name": "P. F. W. PECK", "trade": "Dry Goods, Groceries & Hardware",
        "trade_short": "Dry Goods & Groceries", "place": "South Water Street",
        "identity": "Peck", "grade": "inferred",
        "why": (
            "The 1833 pages carry \"P. F. PECK\" at the corner of LaSalle and South Water "
            "with staple articles, salt, flour, butter and feathers, and the same man "
            "reports the town's prices current for the Democrat. The record independently "
            "has him \"advertising dry goods, hardware and groceries through 1834-35\", "
            "which is the trade line the board takes; the street is his own. Graded "
            "`inferred` and not better because the goods line is assembled from the record "
            "and the page rather than lifted whole off one advertisement. " + PENDING
        ),
    },
    "philo_carpenter_log_shop": {
        "name": "PHILO CARPENTER", "trade": "Drugs and Medicines",
        "trade_short": "Druggist", "identity": "Carpenter", "grade": "inferred",
        "sources": ["chicago_democrat_1833_11_26"],
        "why": (
            "HIS 1833 WORDS ON HIS 1832 SHOP, and the split is deliberate. The "
            "advertisement dated 22 November 1833 in the committed issue reads \"PHILO "
            "CARPENTER, CHICAGO—ILL. Will keep constantly on hand, a general assortment of "
            "DRUGS AND MEDICINES, Oils, Paints, Dye-Stuffs, &c. &c.\" — name first, trade "
            "second, which is the board. By 1835 he has rewritten himself as a \"Wholesale "
            "& Retail Druggist\" AT THE SIGN OF THE GOLDEN MORTAR on South Water Street, "
            "and that later line and that device go on the South Water frontage, not on "
            "this one. A FINDING THIS BOARD RAISES RATHER THAN BURIES: this record's own "
            "occupants block says NO SOURCE REACHED NAMES ANYONE IN THIS BUILDING IN 1835 "
            "and its change note calls the log shop's survival doubtful once he had the "
            "South Water store. If the shop had passed to another keeper by 1 July 1835, "
            "this board names the wrong man — which is a research question for the "
            "structure record, not a wording that can be fixed here. " + PENDING
        ),
    },
    "pierce_blacksmith_shop": {
        "name": "A. PIERCE", "trade": "Blacksmithing", "place": "Lake & Canal Streets",
        "identity": "Pierce", "grade": "reconstructed",
        "why": (
            "A FINDING RAISED RATHER THAN ADOPTED. The 1833 pages carry \"PIERCE & "
            "ABBOTT\" under the head \"New Blacksmith Shop\", which is very probably this "
            "smithy — but this project's record names Asahel Pierce alone as builder and "
            "proprietor and says nothing about a partner, and a signage layer is not the "
            "place to add one to a structure record. So the board letters the man the "
            "record carries, in the register the pages evidence, graded `reconstructed`; "
            "if the structure record adopts the partnership the board should become "
            "\"PIERCE & ABBOTT\" and rise to `inferred` with it. The street is the "
            "record's own `aka`."
        ),
    },
    "pruyne_kimball_drugstore": {
        "name": "PRUYNE & KIMBALL", "trade": "Druggists",
        "place": "South Water Street", "identity": "Pruyne",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this partnership is in the pages read, and the trade "
            "word is borrowed rather than theirs: \"Druggist\" is Carpenter's own 1835 "
            "self-description, which is what makes it the right period word for the "
            "town's second drug store. Andreas gives the partnership and the street and "
            "nothing else. A NEAR-MISS WORTH RAISING: the 1835 pages carry \"P. PRYNE & "
            "CO.\" twice, both times in the grocery and dry-goods line rather than the "
            "drug line — whether that is the same Pruyne is a research question this "
            "board does not answer. Reconstructed."
        ),
    },
    "robert_kinzie_store": {
        "name": "R. A. KINZIE", "trade": "Dry Goods & Groceries", "identity": "Kinzie",
        "grade": "reconstructed",
        "why": (
            "No advertisement for him is in the pages read. The record has a storehouse "
            "dealing in groceries and Indian goods and its keeper among the town's "
            "licensed traders, and it warns that the trade's continuity past the 1833 "
            "treaty is not attested. The board therefore carries the counter trade the "
            "town's own advertising uses and says nothing about the Indian trade, which "
            "the record will not stand behind at the scene date. Reconstructed."
        ),
    },
    "sauganash_hotel": {
        "name": "SAUGANASH HOTEL", "trade": "Public House", "identity": "Sauganash",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this house is in the pages read. \"Public House\" is E. "
            "Wentworth's own 1833 trade line. The house name is the one the town used and "
            "the record carries; its earlier names, Eagle Exchange Tavern and Chicago "
            "Hotel, are in its `aka` and belong to earlier years. Reconstructed."
        ),
    },
    "steamboat_hotel": {
        "name": "JOHN DAVIS", "trade": "Steam-Boat Hotel",
        "place": "North Water Street", "identity": "Steamboat Hotel",
        "grade": "inferred",
        "why": (
            "THE PAGES AND THE RECORD SAY THE SAME THING INDEPENDENTLY, which is the "
            "strongest agreement in the set. The 1835 pages carry \"JOHN DAVIS, Steam-Boat "
            "Hotel, North Water Street\"; Andreas, separately, has \"The Steamboat Hotel, "
            "on North Water Street, near Kinzie, was kept in 1835 by John Davis\". Man, "
            "house, street — the board is the advertisement. The hyphen is the "
            "advertisement's own spelling and is kept. " + PENDING
        ),
    },
    "thomas_church_store": {
        "name": "THOMAS CHURCH", "trade": "Dry Goods & Groceries", "identity": "Church",
        "grade": "reconstructed",
        "why": (
            "No advertisement for him is in the pages read. The source names him as the "
            "BUILDER of the first store building on Lake Street and says nothing about who "
            "kept it or what it sold — the record says so in as many words. So the board "
            "carries the name the record carries over the plainest of the town's own "
            "counter trades, and it is reconstructed twice over: the wording is ours, and "
            "so is the assumption that the builder was the keeper."
        ),
    },
    "tremont_house_1": {
        "name": "TREMONT HOUSE", "trade": "Public House", "identity": "Tremont House",
        "grade": "reconstructed",
        "why": (
            "No advertisement for the house is in the pages read, though attorneys on them "
            "give their offices as \"opposite the Tremont House\", which is the house being "
            "used as a landmark by strangers — exactly what a hotel's board is for. "
            "\"Public House\" is E. Wentworth's own 1833 trade line. The record's "
            "parenthetical, \"(the first)\", is this project telling itself which of three "
            "Tremonts it models and was never on a board. Ira Couch kept it and is "
            "deliberately not lettered: an inn of this town announced its HOUSE. "
            "Reconstructed."
        ),
    },
    "western_hotel": {
        "name": "WESTERN HOTEL", "trade": "Public House", "identity": "Western Hotel",
        "grade": "reconstructed",
        "why": (
            "No advertisement for this house is in the pages read. \"Public House\" is E. "
            "Wentworth's own 1833 trade line, and this is the west-side wagon-trade house "
            "— \"the stopping place for all the farmers town from the west\" — whose "
            "custom came off the road and had to read the board from it. W. H. Stow built "
            "it and kept it, and is not lettered for the same reason Ira Couch is not. "
            "Reconstructed."
        ),
    },
}

# What a wording may be graded. `attested` is deliberately absent: see PENDING.
WORDING_GRADES = {"inferred", "reconstructed"}

# Clause 6, added 2026-08-18 with ticket T-0082 and kept by T-0066. A frontage whose OWN
# reference view shows a board on a POST at the corner does not also get a second board
# hung on its wall by this rule. The Green Tree is the only one: images 6 and 7 of the
# owner's brief (data/sources/assets/owner_brief_2026_08_18/README.md) both show one
# board at this inn, both put it on a post, and image 7 says GREEN TREE is on it — which
# is now drawn, lettered, by the frontage layer (data/frontage/green_tree_frontage.json,
# docs/LIBERTIES.md L135). That board is the town's exemplar for the post mounting this
# record now uses elsewhere; drawing a second sign here would be the town making the same
# claim twice.
POST_BOARD_IDS = {
    "green_tree_tavern": (
        "it carries a NAMED board on its own post at the street corner instead. "
        "Images 6 and 7 of data/sources/assets/owner_brief_2026_08_18/README.md both "
        "show ONE board at this inn, post-mounted at the corner and lettered GREEN "
        "TREE; it is drawn from data/frontage/green_tree_frontage.json by "
        "renderers/web/js/frontage.js (T-0082, docs/LIBERTIES.md L135). That board is "
        "the exemplar this record's own post mounting is copied from. A second sign "
        "here would be this layer drawing the same claim a second time."
    ),
}

# HOW A SIGN IS DRAWN, and why these numbers are here rather than in a renderer. The
# bracket board's arm, drop and hangers are still the wolf sign's own geometry, copied
# from generators/archetypes/log_dwelling.py::_sign, so the town has one convention for
# hanging a board. Everything T-0066 adds — the awning hood, the wall board's cap, the
# post's stand, the painted band — is invented here in every dimension and the record
# carries each number so the renderer can draw it and this file can bound its reach.
ARM_M = 1.15            # the bracket arm, out of the wall
DROP_M = 0.20           # hangers, arm to board
BOARD_T_M = 0.05
OFFSET_M = 1.7          # a hanging board sits this far off the facade's centre
END_CLEAR_M = 0.6       # and never closer than this to the end of the wall
EAVE_CLEAR_M = 0.30
MAX_HEIGHT_M = 2.55

AWNING_PROJECTION_M = 1.45   # the hood over the door, out of the wall
AWNING_DROP_M = 0.34         # its outer edge below its inner one — the fall of a hood
AWNING_MARGIN_M = 0.45       # hood wider than the board it shelters, each side
WALL_BOARD_PROUD_M = 0.02    # a board fixed flat on the front stands this far off it
BAND_PROUD_M = 0.03          # a name painted on the boards, this far proud to draw
BAND_FOOT_M = 2.30           # and its foot this high, clear of any door head
BAND_EAVE_CLEAR_M = 0.25     # unless the wall has not the height, then under the eave
POST_STAND_M = 1.90          # a post stands this far out from the facade
POST_CLEAR_M = 1.00          # and must leave this much between it and the track edge
POST_ARM_M = 1.30

# The board's own size. A board is as long as its name needs and no longer, inside the
# range the mounting allows and inside the frontage it hangs on.
BOARD_SIZE = {
    "bracket_board": {"base": 0.72, "min": 0.88, "max": 1.46, "aspect_mul": 1.00},
    "awning_board": {"base": 0.84, "min": 1.02, "max": 1.66, "aspect_mul": 1.18},
    "wall_board": {"base": 1.00, "min": 1.24, "max": 2.30, "aspect_mul": 1.45},
    "post_board": {"base": 0.88, "min": 1.10, "max": 1.58, "aspect_mul": 1.05},
    "facade_painted": {"base": 1.70, "min": 2.10, "max": 4.30, "aspect_mul": 2.30},
}
PER_LETTER_M = 0.030
BOARD_H_MIN_M = 0.34
BOARD_H_MAX_M = 1.15
FACADE_MIN_FRONTAGE_M = 3.0   # under this a painted band has nowhere to run

# T-0130: a board is now sized off its LONGEST LINE rather than off the whole string,
# because the wording is a hierarchy of two or three lines and not one run of words. Two
# corrections come with that.
#
#  * A second and third line want width as well as height — a firm and a trade set one
#    over the other read wider than either alone — so each extra line adds this much.
#  * They want height too, but ONLY where the board is fixed to the building. A board
#    hung over a footway cannot grow downwards without hanging into the people walking
#    under it, and its head is already fixed by the eave; a board fixed flat on a wall
#    and a name painted across a front have the whole elevation to grow into.
LINE_WIDTH_BONUS_M = 0.30
LINE_H_MUL = {1: 1.00, 2: 1.22, 3: 1.42}
LINE_H_MOUNTINGS = {"wall_board", "facade_painted"}

# A PAINTED DEVICE NEEDS BOARD, and it must not take it off the lettering. Exactly one
# board in this town carries one, and it gets this much extra plank to stand in — added
# to the ceiling as well as to the want, because "as long as its name needs and no
# longer" becomes "as long as its name and its device need" when a shop has both.
DEVICE_W_M = 0.38
DEVICE_SHARE = 0.30       # of the board's face, reserved for the device, left-hand end

# Two signs closer together than this must not share a mounting, a style or a ground
# colour. 40 m is about a platted lot and a half — near enough that a walker sees both
# at once, which is the test the owner set: *no two are alike on a street*.
NEIGHBOUR_M = 40.0

# The post's street test, borrowed whole from tools/generate_frontage_works.py so that
# two layers deciding "may something stand in this street" decide it the same way.
STREET_REACH_M = 22.0
FRONTAGE_DOMINANCE = 0.5

# Clause 5 and the log_dwelling default, mirrored: `wall_height_m` is optional on a
# record and the archetype resolves 2.5 m for one storey, 4.6 m for more. A board
# hung off a wall this project never measured is hung off the same number the wall
# itself is drawn at, which is the only way the two can agree.
DEFAULT_WALL_M = {1: 2.5, None: 2.5}
DEFAULT_WALL_MULTI_M = 4.6


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: float, places: int = 3) -> float:
    """Round toward a stable decimal so `--check` diffs bytes, not float noise."""
    return round(x + 0.0, places) + 0.0


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _rank(sid: str, n: int) -> int:
    """A stable integer for a structure id, for the style preference order.

    hashlib rather than `hash()`: Python randomises string hashing per process, and a
    record that re-derives differently on the next run is not a derivation.
    """
    return int(hashlib.sha1(sid.encode("utf-8")).hexdigest()[:8], 16) % n


def _to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres.

    docs/GLB-CONTRACT.md: polygon `u` → +X, polygon `v` → −Z, ENU `local_e` → +X and
    `local_n` → −Z, and the node's yaw is `-rotation_deg` about +Y. Composing those
    three lines is this function and nothing else; it is verified against the Green
    Tree, whose record says its front is on Canal to the west and whose rotation is
    270, by `--check` refusing any drift in the numbers below.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def _front_edge(polygon: list) -> tuple[float, float, float]:
    """The front wall: the footprint's max-`v` edge, as (u_min, u_max, v).

    Rotation 0 faces north and +v is north, so the wall a bearing points out of is
    the one at the largest v. Both L-shaped footprints in the set (Miller House, the
    Western Hotel) reach their full u-extent at that v, so the general case and the
    rectangle agree; a footprint that did not would be caught by the guard below.
    """
    vmax = max(p[1] for p in polygon)
    on = [p[0] for p in polygon if abs(p[1] - vmax) < 1e-6]
    if len(on) < 2:
        return 0.0, 0.0, vmax
    return min(on), max(on), vmax


def _nearest_on_path(pt, path) -> tuple[float, tuple[float, float]]:
    """(distance, foot) from a point to an open polyline in local ENU metres."""
    x, y = pt
    best = (float("inf"), (x, y))
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
        fx, fy = x1 + t * dx, y1 + t * dy
        d = math.hypot(x - fx, y - fy)
        if d < best[0]:
            best = (d, (fx, fy))
    return best


def _streets() -> dict:
    doc = _load(STREETS)
    out = {}
    for s in doc.get("streets", []):
        out[s["id"]] = {
            "name": s.get("name_1835") or s["id"],
            "path": [tuple(p) for p in s.get("path_local_enu_m", [])],
            "track_w": float(s.get("track_width_m") or 7.0),
        }
    return out


def _street_facing(mid, normal, streets: dict):
    """Which street a wall faces: the nearest centreline that lies IN FRONT of it.

    The same two tests `tools/generate_frontage_works.py::_street_facing` makes, for
    the same reason: a rear wall can be as close to a street as a front wall is to
    another one, and a street that runs BESIDE a wall rather than in front of it is
    not the street that wall's sign stands in.
    """
    best = (None, {}, float("inf"))
    for sid, st in streets.items():
        if len(st["path"]) < 2:
            continue
        d, foot = _nearest_on_path(mid, st["path"])
        outward = (foot[0] - mid[0]) * normal[0] + (foot[1] - mid[1]) * normal[1]
        if outward <= 0 or d > STREET_REACH_M:
            continue
        if outward < FRONTAGE_DOMINANCE * d:
            continue
        if d < best[2]:
            best = (sid, st, d)
    return best


def _frontage_walled() -> set:
    """Buildings the frontage layer already lays a plank walk outside of.

    A post stands where a walk lies. Rather than working out which of the two moves,
    this refuses the post at those frontages and takes the next mounting in the cycle
    — a refusal that is written into the record instead of being a silent nudge.
    """
    out = set()
    if not FRONTAGE.is_dir():
        return out
    for path in sorted(FRONTAGE.glob("*.json")):
        if path.name == "index.json":
            continue
        doc = _load(path)
        for walk in doc.get("walks", []):
            if walk.get("belongs_to"):
                out.add(walk["belongs_to"])
    return out


def _norm(s: str) -> str:
    """Letters and digits only, upper case — the form identities are compared in.

    "Steam-Boat Hotel" on a board and "Steamboat Hotel" on a card are the same house
    written two ways, and the advertisement's own hyphen is kept on the board because
    period spelling is part of the point. So the comparison drops everything that is not
    a letter or a digit rather than asking the two objects to agree on punctuation.
    """
    return "".join(ch for ch in s.upper() if ch.isalnum())


def _sign_wording(sid: str, name: str, mounting: str) -> dict:
    """What is lettered on THIS board, and why it is not the record's own name.

    THE TWO OBJECTS ARE DIFFERENT AND T-0066 COLLAPSED THEM. A record's `name` is this
    project's label for a STRUCTURE — "Philo Carpenter's Log Drug Store" — and a board
    carries what a signwriter lettered for a TRADE. Read the SIGN_WORDING table above for
    the register and the tiers; this function only picks how much of an entry fits the
    mounting the rule has already chosen, and holds the one invariant that survives the
    separation: the board and the card must agree about WHO this is.

    Raises rather than falling back. A frontage the rule newly selects and the table does
    not word would otherwise quietly go back to carrying the museum caption, which is the
    exact defect this replaced.
    """
    entry = SIGN_WORDING.get(sid)
    if entry is None:
        raise SystemExit(
            f"SIGN WORDING MISSING: {sid} is selected for a board and "
            f"tools/generate_business_signboards.py has no wording for it. Add an entry "
            f"to SIGN_WORDING — the proprietor or firm, the trade in the period's own "
            f"words, the tier and the reason. Do NOT let it fall back to the record's "
            f"name: that is the defect T-0130 corrected.")
    grade = entry["grade"]
    if grade not in WORDING_GRADES:
        raise SystemExit(f"SIGN WORDING GRADE: {sid} is graded {grade!r}; only "
                         f"{sorted(WORDING_GRADES)} are available (see PENDING).")

    room = LINES_BY_MOUNTING[mounting]
    lines = [{"text": entry["name"], "role": "name"}]
    trade = entry.get("trade_short") if room < 3 and entry.get("trade_short") \
        else entry.get("trade")
    if trade:
        lines.append({"text": trade, "role": "trade"})
    if room >= 3 and entry.get("place"):
        lines.append({"text": entry["place"], "role": "place"})
    text = " / ".join(ln["text"] for ln in lines)

    # THE INVARIANT THAT REPLACES STRING EQUALITY. The board and the card are allowed to
    # differ — that is the whole correction — but a visitor who reads a name off a plank
    # and then taps the plank must not be shown a different business. So the entry names
    # the identity and this refuses to build unless it is in both objects.
    ident = entry["identity"]
    if _norm(ident) not in _norm(text):
        raise SystemExit(f"SIGN IDENTITY: {sid}'s board reads {text!r} and does not "
                         f"carry its declared identity {ident!r}.")
    if _norm(ident) not in _norm(name):
        raise SystemExit(f"SIGN IDENTITY: {sid}'s card reads {name!r} and does not "
                         f"carry its declared identity {ident!r} — the board and the "
                         f"card would disagree about whose business this is.")
    # No board carries this project's own way of describing a building.
    if "LOG" in [w.strip(",.").upper() for w in text.split()]:
        raise SystemExit(f"SIGN WORDING: {sid}'s board reads {text!r}. No signwriter "
                         f"painted the construction of a shop on its own board.")

    why = entry["why"]
    if room < 3 and entry.get("place"):
        why += (f" The board is a {mounting.replace('_', ' ')}, which carries "
                f"{room} lines, so the place line — \"{entry['place']}\" — is not "
                f"lettered here: a signwriter letters what fits.")
    if room < 3 and entry.get("trade_short"):
        why += (f" For the same reason the trade is shortened from "
                f"\"{entry['trade']}\" to \"{entry['trade_short']}\".")

    out = {
        "lines": lines,
        "text": text,
        "identity": ident,
        "grade": grade,
        "why": why,
        "sources": list(entry.get("sources") or []),
    }
    if entry.get("device"):
        # `share` is how much of the board's face the device stands in, and it is on the
        # record rather than in the renderer for the same reason every other dimension
        # here is: a board's proportions are the record's business.
        out["device"] = dict(DEVICES[entry["device"]], share=DEVICE_SHARE)
    return out


def _candidates() -> tuple[list, list]:
    """Every frontage the rule selects, with its trade class — and every refusal."""
    index = _load(SIDECARS / "index.json")
    standing = [s["id"] for s in index.get("structures", [])]
    picked: list[dict] = []
    refused: list[dict] = []

    for sid in standing:
        sc_path = SIDECARS / f"{sid}.json"
        if not sc_path.exists():
            continue
        sc = _load(sc_path)
        attrs = sc.get("attributes") or {}
        fn = attrs.get("function") or {}
        trade = fn.get("value")
        if trade not in PUBLIC_TRADES and trade not in WORKS_TRADES:
            continue                                            # clause 2
        name = sc.get("name") or ""
        if sid.startswith(("inf_", "recon_")) or name.startswith("Reconstructed"):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "an anonymous slot. The archetype tables' own rule — never invent "
                "business, sign text or goods for an anonymous slot — and this record "
                "keeps it. Now that a board carries a NAME there is not even one to "
                "paint.")})
            continue                                            # clause 1
        grade = fn.get("confidence")
        if grade not in TRADE_GRADES:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"the trade itself is {grade}. A sign for a business this project "
                "reconstructed would be an invention resting on an invention.")})
            continue                                            # clause 3

        if sid in POST_BOARD_IDS:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": POST_BOARD_IDS[sid]})
            continue                                            # clause 6

        struct = _load(STRUCTURES / f"{sid}.json")
        already = [ph.get("id") for ph in struct.get("phases", [])
                   if (ph.get("form") or {}).get("sign")]
        if already:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "it already has one. This is the single record in the dataset that "
                "ATTESTS a sign, and the board hangs in its GLB already "
                f"(phase {already[0]}, docs/LIBERTIES.md L25). A second board here "
                "would be this layer duplicating the only real one.")})
            continue                                            # clause 5

        if trade in WORKS_TRADES and not ("'s" in name or "&" in name):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"'{name}' carries no proprietor — no possessive and no ampersand. A "
                "works painted WHOSE it was, and this project names this building by a "
                "later nickname rather than by a firm; painting the nickname would put "
                "a modern label on an 1835 wall.")})
            continue                                            # clause 7

        place = sc.get("placement") or {}
        poly = (sc.get("footprint") or {}).get("polygon") or []
        if len(poly) < 3:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": "no footprint polygon — no wall to put a sign on."})
            continue
        u0, u1, vmax = _front_edge(poly)
        if u1 - u0 < 1.2:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "the front wall is under 1.2 m of frontage — narrower than the board.")})
            continue

        picked.append({
            "sid": sid, "name": name, "trade": trade, "grade": grade,
            "sc": sc, "place": place, "poly": poly,
            "u0": u0, "u1": u1, "vmax": vmax,
            "cls": TRADE_CLASS[trade],
        })

    picked.sort(key=lambda c: c["sid"])
    refused.sort(key=lambda r: r["structure_id"])
    return picked, refused


def _reach(mounting: str, w: float, geom: dict) -> float:
    """The furthest, ON THE GROUND PLAN, any vertex of this sign may sit from its
    own anchor.

    Carried on the record so the smoke can hold every sign to ITS OWN bound rather
    than to one number wide enough for the largest mounting — a transposed axis is
    metres out, and a per-sign bound catches it on the smallest board too. Horizontal
    only, because that is the mistake it is looking for: a sign hung at the wrong
    HEIGHT is caught by the wall-base rule and by the eye, and a sign hung on the
    wrong AXIS is caught here.

    The 0.12 m is the renderer's own small timber — hanger straps, the strut under a
    bracket, the knee brace under a post arm, the cap over a wall board. Those are
    how a sign is DRAWN rather than a claim about any shop, so they stay in
    renderers/web/js/signage.js, and this leaves them room.
    """
    if mounting == "bracket_board":
        out = ARM_M
        along = w / 2.0
    elif mounting == "awning_board":
        out = AWNING_PROJECTION_M
        along = max(w, geom["awning_width_m"]) / 2.0
    elif mounting == "wall_board":
        out = WALL_BOARD_PROUD_M + BOARD_T_M
        along = w / 2.0
    elif mounting == "post_board":
        out = POST_STAND_M + geom["post_square_m"]
        along = POST_ARM_M * 0.55 + w / 2.0
    else:                                          # facade_painted
        out = BAND_PROUD_M
        along = w / 2.0
    return math.hypot(out, along) + 0.12


def build_record() -> tuple[list, list]:
    picked, refused = _candidates()
    streets = _streets()
    walled = _frontage_walled()

    # Clause 2's cycle index: a frontage's rank inside its own trade class, in id
    # order, so the cycle advances down a class rather than down the town.
    class_rank: dict[str, int] = {}
    for cand in picked:
        cand["rank"] = class_rank.get(cand["cls"], 0)
        class_rank[cand["cls"]] = cand["rank"] + 1

    signs: list[dict] = []
    for cand in picked:
        sid = cand["sid"]
        place = cand["place"]
        poly = cand["poly"]
        u0, u1, vmax = cand["u0"], cand["u1"], cand["vmax"]
        frontage = u1 - u0
        mid = (u0 + u1) / 2.0
        attrs = cand["sc"].get("attributes") or {}

        stories = ((attrs.get("stories") or {}).get("value"))
        wall = (attrs.get("wall_height_m") or {}).get("value")
        wall_from = "the record"
        if wall is None:
            wall = DEFAULT_WALL_M.get(stories, DEFAULT_WALL_MULTI_M) \
                if stories in DEFAULT_WALL_M else DEFAULT_WALL_MULTI_M
            wall_from = ("the archetype's default, because the record carries no "
                         "wall height — the same number the wall itself is drawn at")
        head = min(wall - EAVE_CLEAR_M, MAX_HEIGHT_M)

        # The centre of the front wall, in ENU, and the way it faces — the two things
        # every mounting test below needs.
        bearing = place.get("rotation_deg") or 0.0
        rad = math.radians(bearing)
        normal = (math.sin(rad), math.cos(rad))          # outward, in ENU
        mid_enu = _to_enu(mid, vmax, place)

        # --- the mounting -----------------------------------------------------
        cycle = MOUNTING_CYCLE[cand["cls"]]
        near = [s for s in signs
                if math.hypot(s["anchor_local_enu_m"][0] - mid_enu[0],
                              s["anchor_local_enu_m"][1] - mid_enu[1]) <= NEIGHBOUR_M]
        taken_mount = {s["mounting"] for s in near}
        mount_notes: list[str] = []
        mounting = cycle[cand["rank"] % len(cycle)]
        for step in range(len(cycle)):
            trial = cycle[(cand["rank"] + step) % len(cycle)]
            if trial == "post_board":
                if sid in walled:
                    mount_notes.append(
                        "a post was refused here because the frontage layer already "
                        "lays a plank walk outside this wall, and a post stands where "
                        "the walk lies")
                    continue
                st_id, st, dist = _street_facing(mid_enu, normal, streets)
                if st_id is None:
                    mount_notes.append(
                        "a post was refused here because no street lies in front of "
                        "this wall within "
                        f"{STREET_REACH_M:.0f} m — a post here would stand in a yard")
                    continue
                reach = dist - POST_STAND_M - st["track_w"] / 2.0
                if reach < POST_CLEAR_M:
                    mount_notes.append(
                        f"a post was refused here because the {st['name']} track "
                        f"reaches to within {reach + POST_CLEAR_M:.2f} m of where the "
                        "post would stand")
                    continue
            if trial == "facade_painted" and frontage < FACADE_MIN_FRONTAGE_M:
                mount_notes.append(
                    f"a painted name was refused here because the front wall is "
                    f"{frontage:.2f} m — under the {FACADE_MIN_FRONTAGE_M:.1f} m a band "
                    "needs to run")
                continue
            if trial in taken_mount and step + 1 < len(cycle):
                mount_notes.append(
                    f"a {trial.replace('_', ' ')} is what this frontage's place in the "
                    f"{cand['cls']} cycle asks for, and a sign within "
                    f"{NEIGHBOUR_M:.0f} m already hangs that way — so the cycle "
                    "advances rather than repeating a neighbour")
                continue                       # a neighbour already hangs one this way
            mounting = trial
            break

        # --- the style --------------------------------------------------------
        taken_style = {s["style"]["id"] for s in near}
        taken_ground = {s["style"]["ground"] for s in near}
        start = _rank(sid, len(STYLES))
        style = STYLES[start]
        for relax in (0, 1):
            found = None
            for k in range(len(STYLES)):
                s = STYLES[(start + k) % len(STYLES)]
                if s["id"] in taken_style:
                    continue
                if relax == 0 and s["ground"] in taken_ground:
                    continue
                found = s
                break
            if found:
                style = found
                break

        # --- WHAT IT SAYS, which the mounting has to be known to answer -------
        # A signwriter letters what fits, so the wording is resolved AFTER the mounting
        # rather than before it: a plank swinging over a footway takes the man and his
        # trade, and a name painted across a whole front has room for his street too.
        word = _sign_wording(sid, cand["name"], mounting)
        text = word["text"]
        n_lines = len(word["lines"])
        longest = max(len(ln["text"]) for ln in word["lines"])

        # --- the sign's own size ----------------------------------------------
        size = BOARD_SIZE[mounting]
        extra = DEVICE_W_M if word.get("device") else 0.0
        w = _clamp(size["base"] + PER_LETTER_M * longest
                   + LINE_WIDTH_BONUS_M * (n_lines - 1) + extra,
                   size["min"], size["max"] + extra)
        if mounting == "facade_painted":
            w = min(w, frontage - 1.2)
        else:
            w = min(w, frontage - 2 * END_CLEAR_M)
        w = max(w, 0.7)
        tall = LINE_H_MUL[n_lines] if mounting in LINE_H_MOUNTINGS else 1.0
        h = _clamp(w / (style["aspect"] * size["aspect_mul"]) * tall,
                   BOARD_H_MIN_M, BOARD_H_MAX_M)

        # --- where it sits on the wall ----------------------------------------
        # A hanging board sits to one side of the door; a wall board and a painted
        # band are centred on the front, which is where a painted name goes.
        if mounting in ("bracket_board", "awning_board", "post_board"):
            u = mid + OFFSET_M
            if u > u1 - END_CLEAR_M:
                u = max(mid, u1 - END_CLEAR_M)
        else:
            u = mid
        e, n = _to_enu(u, vmax, place)
        quad = [_to_enu(uu, vv, place) for uu, vv in (
            (min(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), max(p[1] for p in poly)),
            (min(p[0] for p in poly), max(p[1] for p in poly)))]

        geom: dict = {}
        if mounting == "bracket_board":
            geom["arm_m"] = ARM_M
            geom["hanger_drop_m"] = DROP_M
        elif mounting == "awning_board":
            geom["awning_projection_m"] = AWNING_PROJECTION_M
            geom["awning_drop_m"] = AWNING_DROP_M
            geom["awning_width_m"] = _round(
                min(w + 2 * AWNING_MARGIN_M, max(w + 0.2, frontage - 0.8)), 2)
            geom["hanger_drop_m"] = DROP_M
        elif mounting == "wall_board":
            geom["proud_m"] = WALL_BOARD_PROUD_M
        elif mounting == "post_board":
            geom["stand_m"] = POST_STAND_M
            geom["arm_m"] = POST_ARM_M
            geom["hanger_drop_m"] = DROP_M
            # The pole's height is invented inside a hand's range of the Green Tree's
            # 3.60 m, varied by the same stable rank the style uses so that two posts
            # in one street are not the same stick.
            geom["post_height_m"] = _round(3.30 + 0.12 * (_rank(sid, 5)), 2)
            geom["post_square_m"] = 0.16
        else:
            geom["proud_m"] = BAND_PROUD_M

        # THE DATUM, and it is not the same one for every mounting. A sign fixed to
        # a building is measured from the base of that building's walls — the LOWEST
        # of a 5x5 grid of terrain samples under the footprint, which is where
        # buildings.js puts the walls, and any other rule floats a board off its own
        # wall on sloping ground. A POST is not on the building: it stands in the
        # street, on the ground under itself, so its head is measured from there and
        # `arm_height_m` says nothing about it.
        head_y = _round(head, 2)
        datum = ("the base of this building's walls — the lowest of a 5x5 terrain "
                 "grid over the footprint, as buildings.js sets it")
        if mounting == "facade_painted":
            # A PAINTED NAME GOES ABOVE THE DOOR HEAD, which a hung board does not
            # have to think about. `head` is the eave-clear height a BOARD hangs at
            # — 2.55 m at most, because a board is a thing at human height over the
            # footway — and a band painted there lands across the doorway of every
            # frontage that has one, behind any surround that stands proud of the
            # wall. So a band sits with its foot at BAND_FOOT_M, clear of a door
            # head, and drops back under the eave only where the wall has not the
            # height for both. Nothing here is a record's: it is where paint goes
            # on a front, which is a drawing decision.
            top = min(BAND_FOOT_M + h, wall - BAND_EAVE_CLEAR_M)
            head_y = _round(max(top, h + 0.4), 2)
        if mounting == "post_board":
            datum = ("the ground under the post itself, sampled where it stands: the "
                     "post is in the street, not on the building. `post_height_m` is "
                     "its head over that ground and `arm_height_m` does not apply")

        sign = {
            "structure_id": sid,
            "name": cand["name"],
            "sign_text": text,
            "sign_lines": word["lines"],
            "sign_identity": word["identity"],
            "sign_text_from": word["why"],
            "sign_text_confidence": word["grade"],
            "sign_text_sources": word["sources"],
            "trade": cand["trade"],
            "trade_confidence": cand["grade"],
            "trade_class": cand["cls"],
            "why_a_board": PUBLIC_TRADES.get(cand["trade"])
            or WORKS_TRADES[cand["trade"]],
            "confidence": "reconstructed",
            "mounting": mounting,
            "mounting_note": "; ".join(mount_notes) or None,
            "style": style,
            "anchor_local_enu_m": [_round(e, 2), _round(n, 2)],
            "facade_bearing_deg": _round(bearing, 1),
            "arm_height_m": head_y,
            "height_datum": datum,
            "board_w_m": _round(w, 2),
            "board_h_m": _round(h, 2),
            "board_thickness_m": BOARD_T_M,
            "geometry": geom,
            "reach_m": _round(_reach(mounting, w, geom), 2),
            "wall_height_m": _round(float(wall), 2),
            "wall_height_from": wall_from,
            "frontage_m": _round(frontage, 2),
            "ground_quad_local_enu_m": [[_round(p[0], 2), _round(p[1], 2)]
                                        for p in quad],
        }
        # A DEVICE ONLY WHERE THE SHOP'S OWN ADVERTISEMENT NAMES ONE. Exactly one does.
        if word.get("device"):
            sign["sign_device"] = word["device"]
        signs.append(sign)

    return signs, refused


def record(signs: list, refused: list) -> dict:
    mounts: dict[str, int] = {}
    tiers: dict[str, int] = {}
    for s in signs:
        mounts[s["mounting"]] = mounts.get(s["mounting"], 0) + 1
        g = s["sign_text_confidence"]
        tiers[g] = tiers.get(g, 0) + 1
    return {
        "_doc": (
            "The town's business signs. NOT structure records and NOT geometry that "
            "comes out of Blender: a board is a plank on a bracket, a hood, a post or "
            "a wall this project has already drawn, and a painted name is paint on a "
            "wall it has already drawn, so all of it is derived from the committed "
            "footprint and placement and drawn at load by "
            "renderers/web/js/signage.js — the same argument that lets the enclosure "
            "layer draw a fence from a perimeter. Generated by "
            "tools/generate_business_signboards.py and re-derived byte for byte by "
            "tools/check.sh, because 'which frontage gets a sign, what it says, how it "
            "hangs and what colour it is' is a rule and a rule has to be auditable."
        ),
        "id": "town_business_signboards",
        "name": "Signs on the town's business frontages",
        "kind": "signage",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same frame "
            "data/enclosures/ and the sidecars' placement.local_e / local_n use."
        ),
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": ["drloih_wolf_point", "chicago_democrat_1833_11_26"],
            "note": (
                "NO SOURCE STATES THAT ANY OF THESE PARTICULAR BUILDINGS CARRIED A "
                "SIGN, and this record never says one does. What is held is the "
                "bound: one Chicago business of these years is attested to have hung "
                "a sign — the Wolf Point Tavern's painted wolf, by about 1833 — and "
                "the town's first newspaper, 26 November 1833, is full of businesses "
                "trading under names at named addresses, in a settlement whose own "
                "sources describe its houses being known BY their signs (the Wolf "
                "Point house is 'under the sign of the Travelers' Home'; the Exchange "
                "Coffee House's later 'Illinois Exchange' is recorded as a change of "
                "sign). A named trade on a public street announced itself, and how it "
                "did so in 1830s America is not in dispute. That is a reconstruction "
                "in this project's third tier, not an attestation, and it is graded "
                "and claimed as one: docs/LIBERTIES.md L130 for the fact of a sign, "
                "L159 for its wording, its mounting and its colours. THE GREEN TREE "
                "PLATE IS NOT PART OF THE ARGUMENT — docs/ROADMAP.md K5 (b) cites its "
                "hanging sign, but data/sources/chm_green_tree_1859.json records that "
                "the image has never been seen and is unverified, so it underwrites "
                "nothing here."
            ),
        },
        "lettering": {
            "value": ("what the trade wrote — the proprietor or firm, the trade, and "
                      "the place, in the period's own words and spelling"),
            "confidence": "reconstructed",
            "geometry": "canvas texture, drawn at load",
            "tiers": {k: tiers[k] for k in sorted(tiers)},
            "note": (
                "DRAWN SINCE 2026-08-21, AND RE-WORDED THE SAME DAY. This block used to "
                "read 'NOT DRAWN, AND THAT IS THE WHOLE DISCIPLINE OF THIS LAYER', on "
                "L25's reasoning generalised: no source gives the wording of any sign in "
                "this town, so every board stayed a blank plank. The owner's instruction "
                "of 2026-08-18 overruled it — 'you can and should put the name of the "
                "location on the sign board … it is fine if they are reconstructions' — "
                "and T-0066 then painted THE RECORD'S OWN `name` on every board. "
                "T-0130 CORRECTS THAT, on the owner's word of 2026-08-21: 'philo would "
                "not have referred to his own place as log drug store, it would be philo "
                "carpenter, drugs and medicines, or druggist or whatever he would have "
                "referred to himself as on the sign, that may be different than the name "
                "of the building for us, the sign may read differently historically' — "
                "and, widening it, 'i guess do a pass on all those signs and make sure "
                "they feel right for the era'. A record's `name` is OUR LABEL FOR A "
                "BUILDING ('Philo Carpenter's Log Drug Store'); a board carries what a "
                "signwriter lettered. The two are now separate fields and are allowed to "
                "differ. What they must still agree about is WHO: every sign declares a "
                "`sign_identity` that appears in the board AND in the card, the "
                "generator refuses to build without it, and tools/smoke_renderer.mjs "
                "asserts it at run time over every sign. THE REGISTER is the "
                "advertisements' own — proprietor or firm first and largest, the trade "
                "beneath, the place last and smallest — carried per line in `sign_lines` "
                "and lettered in that hierarchy by renderers/web/js/signage.js. Period "
                "spelling is theirs and is kept. THE TIERS: a wording taken off a firm's "
                "own advertisement is `inferred`; one built out of the evidenced trade "
                "vocabulary for a business that left no advertisement is "
                "`reconstructed`. NOT ONE IS `attested` YET, and each note says why and "
                "what would change it — the seven 1833-35 newspaper pages behind these "
                "wordings were supplied as images in conversation on 2026-08-21 and are "
                "not committed to data/sources/assets/, so they are transcriptions and a "
                "transcription is not a citation. The owner's ruling of that day is the "
                "authority for proceeding anyway: 'I will give you all those data sources "
                "later in a more comprehensive form proceed where you can and label "
                "reconstruction or inferred with a note as you like.' The LETTERFORM, "
                "the colours and the panel remain `style`, a table of the combinations "
                "the trade worked in rather than of anything Chicago recorded "
                "(docs/LIBERTIES.md L159; L166 for the wording). ONE DEVICE IS NOW "
                "PAINTED and it is the one a Chicago tradesman described himself: "
                "Carpenter's golden mortar, `sign_device` — see its own note. No other "
                "board carries an image, and L25 is untouched: it withholds the Wolf "
                "Point wolf because that IMAGE was never described, which is the "
                "opposite case to a shop whose own advertisement names its sign."
            ),
        },
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                "Five mountings, chosen by the trade's class and de-conflicted against "
                "every sign within "
                f"{NEIGHBOUR_M:.0f} m so that no two neighbours hang alike: "
                "`bracket_board` (the wolf sign's own geometry — a plank hung by two "
                "straps 0.20 m under a 1.15 m bracket arm, 1.7 m to one side of the "
                "facade's centre and clear of the eave), `awning_board` (the same "
                f"plank under a hood {AWNING_PROJECTION_M} m deep that falls "
                f"{AWNING_DROP_M} m to its outer edge), `wall_board` (a board fixed "
                "flat on the front under a cap), `post_board` (a pole at the street "
                f"edge {POST_STAND_M} m out from the wall, with a cross-arm and the "
                "board under it — the Green Tree's own arrangement, T-0082) and "
                "`facade_painted` (the name straight onto the boards of the building, "
                "no board at all — what image 5 of the owner's brief shows across the "
                f"Tremont's row, standing with its foot {BAND_FOOT_M} m up so it "
                "clears a door head, or lower where the wall has not the height for "
                f"that and {BAND_EAVE_CLEAR_M} m of eave besides). Not one of those "
                "numbers is a record's. A sign's "
                "SIZE is derived from the length of its own name inside the range its "
                "mounting allows and inside the frontage it stands on; its `aspect` "
                "comes from its style, so two boards on one street are not the same "
                "rectangle either."
            ),
            "mountings": {k: mounts[k] for k in sorted(mounts)},
        },
        "rule": {
            "note": (
                "A named record (not inf_/recon_, not 'Reconstructed'), a trade this "
                "project will announce — a PUBLIC TRADE whose customer arrived on foot "
                "off the street, which gets a board, or a WORKS OR WAREHOUSE trade "
                "whose custom came by name and by cart, which gets its firm painted on "
                "the front — that trade attested or inferred rather than "
                "reconstructed, standing on the scene date, no sign on the record "
                "already, no named board already standing on a post at its corner on "
                "the frontage layer, and (for a works only) a proprietor in its own "
                "name. Read the clauses and their reasons in "
                "tools/generate_business_signboards.py."
            ),
            "public_trades": sorted(PUBLIC_TRADES),
            "works_trades": sorted(WORKS_TRADES),
            "mounting_cycles": MOUNTING_CYCLE,
            "lines_by_mounting": LINES_BY_MOUNTING,
            "styles": [s["id"] for s in STYLES],
            "neighbour_m": NEIGHBOUR_M,
            "wording_note": (
                "WHAT A BOARD MAY SAY, and it is a rule rather than a list somebody "
                "liked. Every board is worded from SIGN_WORDING in "
                "tools/generate_business_signboards.py: the proprietor or firm, the "
                "trade in the period's own words, and the place — in that order, which "
                "is the order the advertisements themselves use. The generator refuses "
                "to build a board for a frontage the table does not word, refuses one "
                "whose declared `sign_identity` is not in both the board and the card, "
                "and refuses one that carries the word 'log' — the three ways the old "
                "behaviour could come back. How much of an entry is lettered depends on "
                "the mounting: `lines_by_mounting` above, because a signwriter letters "
                "what fits and a plank swinging over a footway holds less than a name "
                "painted across a whole front."
            ),
            "excluded_trades_note": (
                "Stables, churches, schools, the court-house, the jail, the agency "
                "house, the fort and every dwelling are outside both trade lists. A "
                "stable is the yard of the house that owns it and announces nothing of "
                "its own; the rest are not trades. Frederick Thomas's shop is refused "
                "one clause further down, because its own record says no source reached "
                "says what he sold."
            ),
        },
        "signs": signs,
        "refused": refused,
        "research_note": (
            "THE FIRST THING TO DO, AND IT IS ALREADY HALF DONE: COMMIT THE SEVEN PAGES. "
            "The wordings graded `inferred` above are transcribed from 1833-35 Chicago "
            "newspaper pages the owner supplied as IMAGES IN CONVERSATION on 2026-08-21 "
            "— one carrying 'Chicago, Dec. 31, 1833' with a 'CHICAGO PRICES CURRENT … "
            "Reported for the Democrat by P. F. Peck' that identifies the Chicago "
            "Democrat, one 'Chicago, Dec. 4, 1833', and several of 1835 carrying an "
            "'ARRIVALS OF VESSELS AT CHICAGO, 1835' table and a Post Office list of "
            "letters remaining 'on the 31st day of March, 1835'. Drop those images into "
            "data/sources/assets/ with a source record and EVERY `inferred` WORDING HERE "
            "BECOMES A CANDIDATE FOR `attested`, one board at a time, each note already "
            "saying what its page says. Goss & Cobb's is the nearest: its page is "
            "committed already. WHAT WOULD MOVE THE REST — the fact of a sign, its "
            "colours and its mounting — is unchanged: a Chicago or Cook County sign "
            "ordinance of the 1830s; an insurance, tax or sale description naming a shop "
            "sign; any of the pre-fire photographs of a surviving 1830s frontage "
            "actually being opened at its holding institution (the Green Tree 1859 "
            "plate, ICHi-040230, is the nearest and is unseen); or a traveller's account "
            "of walking South Water Street."
        ),
        "findings": [
            "J. S. C. HOGAN advertises in 1835 from 'South Water Street, one door below "
            "Dearborn' in dry goods, groceries, hardware, crockery and glass ware. The "
            "model carries ONE Hogan building, the log store at the Lake Street junction, "
            "which its own record identifies as Brewster, Hogan & Co.'s. The pages "
            "distinguish the two businesses and the model does not — a placement "
            "question, raised rather than silently answered.",
            "PIERCE & ABBOTT advertise a 'New Blacksmith Shop' on the 1833 pages. This "
            "project's record names Asahel Pierce alone as builder and proprietor. If the "
            "partnership is his, the board should read PIERCE & ABBOTT and rise from "
            "`reconstructed` to `inferred`; a signage generator is not the place to add a "
            "partner to a structure record.",
            "P. PRYNE & CO. appears twice on the 1835 pages, both times in groceries and "
            "dry goods, never in drugs. The model carries Pruyne & Kimball as a drug "
            "store on Andreas's word. Whether these are the same Pruyne is unresolved and "
            "the board says nothing about it.",
            "Two 1835 advertisements locate themselves BY A NEIGHBOUR — Wm. H. Taylor's "
            "boot store 'a few rods north of Newberry & Dole's', J. Curtiss's office "
            "'first door west of Jones, King & Co.' — and a third 'opposite the Tremont "
            "House'. Those are checkable against this model's own placements and are a "
            "wayfinding gift for whoever takes the placement sweep.",
            "Firms the pages name and the model does not yet carry at all: WM. H. TAYLOR "
            "(boot, shoe and leather), J. H. MULFORD (watches and jewelry), DAVID CARVER "
            "(lumber dealer and commission merchant), MAGIE & WILKINSON (boots, shoes and "
            "hats), F. J. CONANT (clothing warehouse), Doct. WM. H. KENNICOTT (medicine "
            "and dentistry), and a bench of attorneys. Each is a placement question, not "
            "a wording one, and none has been invented a building here.",
            "Out-of-town houses advertise on the same pages — Patterson, Gardner & Mather "
            "of Detroit 'at the sign of the Large Pitcher', Cromelien, Brothers & Co. of "
            "New York. They are useful as REGISTER and must never be hung in Chicago. The "
            "Large Pitcher is quoted in the golden mortar's note for exactly that reason: "
            "it shows the convention was ordinary, and it belongs to Detroit.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
    signs, refused = build_record()
    text = json.dumps(record(signs, refused), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists():
            print(f"SIGNBOARD DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"SIGNBOARD DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the "
                  f"rule in tools/generate_business_signboards.py")
            return 1
        print(f"verified {len(signs)} business signs "
              f"({len(refused)} frontage(s) refused with a reason)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(signs)} business signs "
          f"({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
