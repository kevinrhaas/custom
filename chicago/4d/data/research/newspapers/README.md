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

Page and column come from the transcription's own
`===== ISSUE PAGE n / PDF PAGE m / COLUMN k OF 6 =====` markers, which every issue in
both runs carries.

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

## What the papers are read INTO

Two files, and only one of them is written by hand.

| | |
|---|---|
| `extracted/<issue_id>.json` | **hand-made**, one per issue, holding `claims[]` |
| `gazetteer.json` | **generated** by `tools/compile_gazetteer.py --build`, never hand-edited |

    tools/compile_gazetteer.py --build       recompile the gazetteer
    tools/compile_gazetteer.py --check       the gate (runs in tools/check.sh)
    tools/compile_gazetteer.py --self-test   the gate's assertions still fire

The gate recompiles the gazetteer in memory and compares **bytes** with what is
committed, so hand-editing the compiled file is not a matter of etiquette — it turns
the build red. The compile is deterministic: sorted keys, sorted lists, no clock.

### A claim

`quote` is verbatim and includes the transcriber's own square-bracketed uncertainty
notes; it is never smoothed. `normalized` sits **beside** it and never replaces it —
interleaved columns unshuffled, `rn`/`m`-class confusions corrected, and any word
*restored* rather than read written in **angle** brackets, so the two kinds of
bracket can never be mistaken for each other. Every claim also carries `locator`
(issue page, column, line range, per the citing convention above), `entities[]` with
each name as printed **and** a normalization guess, `reading:
transcription_mediated` — structurally, so no claim can omit it — and, where the
advertisement has its own dateline, `ad_copy_date`: the date the copy was *placed*,
which is what evidence windows are built from and is often months older than the
issue it appears in.

A claim may also carry `corroborations[]`, pointing at a second witness for the same
issue. Nothing may be *cited* from a witness with no page/column markers; a
corroboration is how such a witness earns its keep, and the gate enforces the
difference.

### The identity policy

There is **no fuzzy matching** anywhere in the compiler. Two mentions become one
person because an extraction gave them the same `id` — which is a merge, and a merge
must be explained. Two spellings under one id need a `merge_rule` naming both and
stating the judgement, or the compile fails; if they share a surname and disagree on
initials the rule must additionally say `cross_initial: true`.

### The worked fixture

`extracted/chicago_democrat_1835_07_01.json` — eight claims from the scene-date
Democrat, chosen because between them they exercise every field. Two of them are
worth knowing about:

- **Peter Cohen**, dry goods, groceries, clothing and liquors, South Water Street,
  advertisement dated *Chicago, Nov. 3, 1834* and still running eight months later.
  His placement is `relative`, anchored on Newberry & Dole. The reconciled
  transcription's column cut removes the words that make it precise — it has only
  `low Mesers. Newberry and Dole's` — and the `-2` alternate witness, worse
  everywhere else, happens to carry the line whole. Read together they say **next
  door below**, not the *a few doors below* the ticket that commissioned this work
  quoted from memory.
- **J. S. C. Hogan** advertises a store *one door below the Post Office* — the
  offset word again supplied by the alternate — and signs the post-office letter
  list in the same issue as `HOGAN, P. M.` The anchor and the man are one person,
  which is the sort of thing the gazetteer exists to hold onto.

Cohen's entry compiles with `survival_liberty: true`: his existence is documented,
his survival to 1835-07-01 is assumed, per the owner's third ruling. That becomes an
entry in `docs/LIBERTIES.md` when a storefront is actually placed in the town, which
is not this ticket.
