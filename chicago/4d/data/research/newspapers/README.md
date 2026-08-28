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
