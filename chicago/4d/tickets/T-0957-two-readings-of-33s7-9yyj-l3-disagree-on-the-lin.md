---
id: T-0957
title: Two readings of 33S7-9YYJ-L3 disagree on the line count and on the printed footing: 27 lines and 115, or 28 lines and 113
state: open
epic: PAPERS
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-07
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

`#1015` and `#1014` are two independent passes over the same leaf — 33S7-9YYJ-L3, the 1840
census — and they disagree on three figures at once. #1014 merged; #1015 was parked under
`hold` and is closed by T-0930 with this ticket carrying its reading, so the disagreement
survives the branch.

| | on `dev` (#1014, T-0744) | on `#1015`'s branch |
|---|---|---|
| lines ruled with an entry | **27** | **28** |
| records committed to the page file | **27** | **30** |
| printed footing | **115**, `documented` | **113**, `inferred` |
| lines committed to the closure | 21, summing **71** | 19, summing **111** |
| lines left unread | 6 | 7 |
| the matched-pair figure | six lines carry it; the key reads them as 4s | `total_matched_pair: null`, the pairs not named |
| the 33S7-9YYJ-PC pairing | refusal held by TWO keys, population key unchanged at 115 | `pairing_test: null` |

**What separates them, in the branch's own words.** The 113 rests on the last glyph of the
footing being *"a hook and flag over a descender that ends in a bowl at the bottom-left"* —
the same character the COMMERCE column's printed footing carries, and that column's four
entries fix its own footing at 3. So the branch identifies the glyph against a footing the
leaf itself proves, and reads 113. The 115 rests on `pairing_key_26_50.json`, which read the
same cell in T-0656 and describes three glyphs *"a plain slant; a second plain slant; then a
bowl under a long flat top stroke that runs to the cell's right rule"*, at 10x, and is
`documented`.

**Neither closes the column, and the branch says so** — `"THE COLUMN DOES NOT CLOSE, EITHER
WAY, AND NOTHING HERE IS ADJUSTED TO MAKE IT."` 21 committed lines sum to 71 against 115,
leaving a mean of 7.3 for six unread lines where the committed ones average 3.4; 19 lines
sum to 111 against 113, leaving 2 for seven lines that each carry ink. **The second residual
is the harder one to believe**, and that is a fact about the branch's reading, not about the
leaf.

**Why this is not a stalemate.** The two passes disagree on how many lines the leaf rules,
which is prior to the footing: 27 or 28 is settleable off the image alone at the ruling, and
whichever answer wins constrains the sum. `33S7-9YYJ-L3.json` on `dev` is the record in
force; nothing here amends it.

**Acceptance**

1. The line count is settled off the exposure at the ruling — 27 or 28 — with the extra
   line named and shown, or shown not to exist.
2. The footing glyph is read again against the commerce column's own footing, since that is
   the branch's whole argument, and the answer states which of 115 / 113 the character is.
3. Whichever way it falls, `pairing_key_26_50.json`, the page file's `closure` and the
   33S7-9YYJ-PC refusal are brought into line with each other in the same commit — the
   refusal on `dev` is currently held by a key this ticket may move.
4. If the column still does not close, that stays written down. Nothing is adjusted to make
   it close.
