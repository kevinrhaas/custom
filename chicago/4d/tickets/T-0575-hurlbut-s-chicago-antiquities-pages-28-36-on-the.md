---
id: T-0575
title: Hurlbut's Chicago Antiquities pages 28-36 on the American Fur Company at Chicago, read as claims about the trade the town actually carried
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0556
opened: 2026-09-03
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Hurlbut's Chicago Antiquities pages 28-36 on the American Fur Company at Chicago, read as claims about the trade the town actually carried.

Piece 5 of 6 of **T-0556 — genealogytrails.com Cook County: inventory every section of the site, grade what it holds for 1835 Chicago, and split the extraction of residents, households, businesses, structures and occupations into tickets**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**The source.** `text/americanfurco.txt` — Henry H. Hurlbut, *Chicago Antiquities* (Chicago, 1881),
pages 28-36, transcribed in full with its spelling kept. It names Hubbard, Beaubien, Crafts and the
Kinzies as the American Fur Company's Chicago men and describes what the trade did here.

**Why it is worth a run.** It is a size argument about the town, from a named book with a page
range, about people this project already models. Hurlbut's judgement — Mackinac the great
storehouse, "Chicago was the port and point of a very limited district of distribution" — bears
directly on how much fur-trade apparatus the scene should show, which is a question the
reconstruction currently answers by feel.

**What it is not.** Prose written in 1881 about the decades before the scene. It is a CLAIMS read
into the books domain, not a records read, and it is a judgement rather than an observation: no
building moves on the strength of it without the reasoning being written into
`docs/LIBERTIES.md`.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- The chapter read into `data/research/books/claims/`, every claim with a verbatim quote the
  domain's own gate rebuilds from the committed text, a locator naming Hurlbut's page, a
  `describes_date`, and `town_finding` set honestly.
- The four named men carried to `entities[]` with no merge asserted that the crosswalk has not
  stated a rule for.
- Anything that would change a structure or an asset is proposed in the ticket, not done in it.
- `gt_005` in `data/research/genealogytrails/claims/` is the one quote already filed; supersede it
  rather than duplicating it.

**Links:** parent T-0556 · `docs/RESEARCH/jb_beaubien_homestead.md` · T-0513 waits on this.


**Where it is.** Cached, in text, at `chicago/4d/data/research/genealogytrails/text/` — this
project's own committed copy, taken 2026-09-03. Do NOT re-fetch to read it; the cache is what a
later run has to be able to trust, and `tools/read_genealogytrails.py --fetch` is how it is
refreshed if it ever must be. `data/research/genealogytrails/inventory.json` is the grade and the
count this ticket was sized from, and `README.md` beside it says what the site is and is not.

**The shape.** T-0492 fixed it: a records file for a list, a claims file for prose, a closed kind
vocabulary, `reading: transcription_mediated` (nothing here is a scan read), a `coverage.json`
declaration for what was read, and a `crosswalk.json` whose refusals are written as carefully as
its merges — surname-only is always a refusal.

**The ladder.** The owner ratified it on 2026-09-03 and it binds this ticket: a source later than
1835 alone never makes an 1835 resident. It corroborates, it enriches, and above all it DATES.
Everything read here carries `describes_date`.
