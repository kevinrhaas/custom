# The newspaper corpus — what is here, and how to cite out of it

`corpus.json` is the register. Eighty-six issues: **seventy-three** of the *Chicago
Democrat*, 1833-11-26 to 1835-08-26, and **thirteen** of the *Chicago American*,
1835-06-08 to 1835-08-29. The scene date sits inside both runs, and a Democrat was
printed on 1835-07-01.

Two source records carry the judgements — the traps, the owner's three rulings, the
uneven transcription quality, and what each publication may and may not be used for:

- `data/sources/chicago_democrat_1833_1835.json`
- `data/sources/chicago_american_1835.json`

`data/sources/chicago_democrat_1833_11_26.json` is the per-issue record for the first
issue and **stays senior to both** for that issue: it was verified against the page
images, and a scan read outranks a transcription read.

## Citing

A claim that cannot name its column cannot be made. Resolve the issue through
`corpus.json`, quote the transcription's uncertainty brackets as they stand, and cite:

> *Chicago Democrat*, 1835-07-01, Vol. II, No. 11, issue page 3, column 4 —
> `chicago/reference/newspapers/Transcriptions/Chicago_Democrat_1833-11_to_1835-08/Chicago_Democrat_1835-07-01_Vol2_No11_Transcription.txt`, lines 812-819.

Page and column come from the transcription's own column markers — and this file has now
been wrong about how many dialects there are **twice**. The sixty-six issues the deposit
delivered as committed `.txt` carry a RULED marker in one of three shapes:

    ===== ISSUE PAGE 4 / PDF PAGE 36 / COLUMN 5 OF 6 =====
    ===== ISSUE PAGE 4 / SOURCE PDF PAGE 36 / COLUMN 5 OF 6 =====
    ===== ISSUE PAGE 4 / ORIGINAL PDF PAGE 36 / COLUMN 5 OF 6 =====

and the twenty-three extracted here from `.docx` carry the same two facts as prose
headings, the page once and each column under it:

    Newspaper Page 1 — Source PDF Page 13
    Column 1

**The middle ruled shape is the majority and it was the one nobody had.** Counted across
the deposit on 2026-08-28 while reading July 1834 (T-0289): 1,176 of the 1,266 ruled column
markers say `SOURCE PDF PAGE`, 90 say the bare `PDF PAGE`, and four say `ORIGINAL PDF
PAGE`. T-0257's resolver matched only the bare form, so it could find a column marker in
NONE of the twenty-six issues of the second half of 1834. Nothing caught it because the
gate skips the page/column assertion outright when it cannot read the text, and on `dev`
it never can — a resolver that speaks no dialect and one that speaks all three are
indistinguishable on this branch. `tools/compile_gazetteer.py` now reads all four shapes
and its self-test carries a case per ruled dialect plus a negative.

**Where the deposit is not readable, run the gate against a copy of it.** `--deposit
<path>` re-roots deposit-held citations exactly as `newspaper_corpus.py` does, so a reading
pass working on `dev` can machine-check every quote it makes against the real text from
`main` before it opens its PR. `check.sh` on `dev` then counts those claims unresolved and
reports them, which is green.

## Where the text is, and why it is in two places

| | issues | text |
|---|---|---|
| the deposit carries a committed `.txt` | 66 | cited at its `chicago/reference/...` path, never copied |
| delivered as `.docx` only | 20 primaries + 3 alternates | extracted here to `text/`, and **committed** |

The deposit is the owner's archival deposit and this project reads it only. It was
committed to `main` on 2026-08-28 and **is not on `dev`**, where this subtree is
developed — so on `dev` the sixty-six reference paths do not resolve and the
twenty-three derived ones do. `tools/newspaper_corpus.py --check` treats that as one
of three states: deposit **present** (every path resolved file by file), **absent**
(reported, and green), **partial** (always red — that state means damage). T-0275
carries the back-merge, which is not free: `main` also carries sixty Finder-duplicate
`... 2.json` / `... 2.glb` files under `site/chicago/4d/data/` that turn this repo's
gate red in twenty-three places.

## Quality is not uniform

The 1833, 1834 and January–July 1835 Democrat batches were reconciled against enlarged
page images with a second-reviewer pass. The August 1835 Democrat tail, the three `-2`
rebuilds and **the entire American run** are single-pass OCR. Where two runs cover one
issue the `-2` text is visibly worse; 1835-07-15 survives only as a `-2`, and
`corpus.json` says so on that entry. Weight a reading by the batch it came from —
`status`, `completeness` and `sole_witness_note` carry it.

## This is research, not payload

`tools/publish.sh` copies named subdirectories of `data/` and this is not one of them.
The gate asserts that nothing under `data/research/` has reached `site/chicago/4d/`,
so the corpus can grow without spending the published tree's size budget.

## Rebuilding

    tools/newspaper_corpus.py --build --deposit <path to Transcriptions>

Deterministic: the same deposit produces byte-identical `corpus.json` and `text/`.
`--deposit` exists because the deposit is on another branch; paths are always
*recorded* at their canonical `chicago/reference/...` home whatever `--deposit` says.

## Reading out of it — claims, and the gazetteer they compile into

`corpus.json` says where a passage IS. These say what was read out of it (T-0257).

| | |
|---|---|
| `extracted/<issue_id>.json` | one file per issue, holding `claims[]` — hand-authored |
| `identity.json` | the only place two differently-spelled names may become one person |
| `coverage.json` | the ranges a reading pass has DECLARED it read, and the gate holds it to them |
| `gazetteer.json` | **generated** by `tools/compile_gazetteer.py --build` — never hand-edited |

    tools/compile_gazetteer.py --build       recompile the gazetteer
    tools/compile_gazetteer.py --check       the gate (in check.sh)
    tools/compile_gazetteer.py --self-test   its assertions still fire

**A declared range may not have a hole in it.** The failure a reading pass is prone to is
not a bad claim — the quote gate catches those — but a MISSING ISSUE: fourteen of fifteen
read, and nothing anywhere saying which one was skipped. Counting extraction files cannot
answer it, because the count that should have been is exactly the thing in question. So a
pass names the range it read in `coverage.json` and `--check` resolves that range against
`corpus.json` and refuses any issue inside it with no extraction file. Declaring is what
makes the assertion: an issue nobody has declared is simply not read yet and is not a
fault, and a range is only widened by the pass that widens the reading (T-0295).

**A claim quotes verbatim and normalizes beside it, never instead.** `quote` is the
transcription's own text including its uncertainty brackets; `normalized` is the reading
after OCR judgment — interleaved columns unshuffled, `rn/m`-class confusions corrected.
The gate reassembles `quote` out of the transcription line by line and refuses any claim
whose text differs by a character, so a smoothed quote fails rather than passing quietly.

**Interleaving is the normal case.** The segmenter frequently alternates two physical
columns line by line, so one advertisement occupies a SUBSET of a line range with another
woven through it. `locator.lines` is the range cited; `locator.lines_of_claim` names the
lines the quote is built from, and the gate checks the subset lies inside the range.

**`[…]` marks absence, `[word]` marks a supply.** Text the column edge cut away is a gap,
not an invitation. The worked fixture leaves *'a few doors below'* unsupplied for exactly
that reason and says where a fuller witness might be found.

**The owner's three rulings live in fields, not in prose.** `letter_list_only` on a person
(a listed name mints a resident candidate, and the weaker evidence stays distinguishable);
`reading` required on every claim (`transcription_mediated`, or `scan_verified` where a
scan was read and outranks it); and `built_at_scene_date` / `survival_liberty_required`
computed on a business — documented businesses stand in the 1835 town unless a claim
contradicts them, and one last seen before 1835 stands on a stated liberty.

**Identity never coalesces by accident.** The gazetteer is keyed on the whole normalized
name, so `Cohen, P.` and `Cohen, J.` are two people. A merge is declared in
`identity.json` with a `merge_rule` naming both spellings; same surname with different
initials never merges, rule or no rule.

The scene-date Democrat, `extracted/chicago_democrat_1835_07_01.json`, is both the worked
fixture (claims c001-c003, T-0257 — Peter Cohen and J. S. C. Hogan on South Water Street,
and one letter-list name) and the first issue read through (c004-c021, T-0295).

**It is read from the deposit `primary`, not from the `-2` rebuild `dev` can open**, and
the reason is the letter list: the primary sets it legibly at name level and the alternate
does not. So its quotes are verified with

    tools/compile_gazetteer.py --check --deposit <a materialised deposit>

and the committed gate on `dev` reports them unresolved-but-green until T-0275 lands. The
segmenter cut each printed column in half and alternates the halves line by line, so nearly
every claim there is `interleaved`, and most bracketed supplies are read off the OTHER half
of the same printed lines — each claim's note names the lines they came from.
