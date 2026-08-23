---
id: T-0018
title: Does a spatial filter eat the sward stratification
state: done
epic: FLORA
requested_by: loop
seen: false
effort: M
legacy_id: K49(e)
parent: null
opened: 2026-08-17
closed: 2026-08-23
pr: 337
claimed_by: run 8/23/2026, 3:36:59 PM CT
blocked_on: null
needs_bake: false
---

K49(d) left one explanation stated and unproven: a spatial filter running after the deal
selects a biased set of ranks, making two census rows worse. Prove or refute it. Deep
history: § K49(e) (~4784).

**Acceptance:** the mechanism demonstrated red/green on a controlled deal, or refuted with
the alternative named.
---

## REFUTED 2026-08-23 — and the alternative is precision, not accuracy

**The mechanism is refuted, and it could not have been true.** `tools/measure_rank_bias.mjs` —
new, 0.4 s, no browser. Position → rank is `feistel(idx, half, blockHash)`, and `blockHash` is
`hash3(bc, br, salt ^ STRAT_SALT)` — **re-keyed in every block**. A spatial rule does not know that
key, so the ranks it accepts are an arbitrary subset, independently re-drawn block by block. Pooled
over blocks they are uniform. Bias would require the filter to correlate with a hash of the block's
own coordinates.

Over 400 independent layer keys, χ² on 15 df against uniform (critical value 37.7 at p = 0.001):

| arm | slots kept | rank χ² | mix dev /100 |
|---|---|---|---|
| `none` | 100.0 % | 0.0 | 0.83 |
| `halfplane` — a waterline | 61.6 % | **2.0** | 3.33 |
| `disc` — a building footprint | 58.8 % | **4.1** | 5.01 |
| `stripe` — a street corridor | 72.1 % | **2.3** | 3.22 |
| `blind` — rank-blind control | 64.9 % | 4.7 | 4.54 |
| **`rank_low` — reads the rank** | 56.3 % | **100,800** | 60.46 |
| `independent` — pre-K49(d) | 100.0 % | 0.0 | 5.83 |

The three real shapes are indistinguishable from the rank-blind control. **The instrument goes red
by four orders of magnitude when there is something to catch.**

**The alternative, named:** a filter costs the STRATIFICATION, not the accuracy. The surviving `u`
are no longer equally spaced, so the deal slides back towards an independent draw at about the rate
it thins — 0.83 unfiltered, 3.2–5.0 at ~60 % kept, 5.83 independent. **So K49(d)'s standing
instruction is the opposite of the truth and is struck from `flora.js`:** reach for `stratum` in a
filtered layer; filtered, it still beats an independent draw.

**The row that opened the ticket is a draw, not a fault.** `z05_riverbank_timber` reading the wet
prairie draws 44 slots and deviates 5.24. One block thinned to about that count, over 400 keys,
deviates **5.89–7.17 slots on average**. 5.24 is below all three means. K49(e)'s residual is closed,
not carried.

**It measures the shipped code and refuses to measure a copy.** Every primitive is extracted from
`renderers/web/js/flora.js` at run time by slicing its source; `scatter`'s inline arithmetic is
held by six verbatim-line assertions. Both guards were demonstrated firing, `rc=2` and named. The
self-test is wired into `tools/check.sh`, so the control pair runs on every gate.

Full write-up, including what the second guard does not catch: `docs/STATUS.md` under
*Refuted 2026-08-23*.
