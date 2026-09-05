---
id: T-0808
title: The three questions the parked PRs are waiting on: the site budget, kinship, and the planform of record at the forks
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Three PRs are parked on questions only the owner can answer, and they are the ONLY three
in a 21-PR backlog that are genuinely blocked on a decision. Every other parked PR was
waiting on dev's red gate, which is green again. Answer these three and the backlog is
fully drainable.

**Nothing is invented before an answer. Each question states the options and what each
one costs; none of them is a missing number, which AGENTS.md says to derive rather than
ask about.**

---

**1. The published tree is at its 32 MB ceiling** — T-0730, blocking
[#841](https://github.com/kevinrhaas/custom/pull/841); [#836](https://github.com/kevinrhaas/custom/pull/836)
is a worked answer to option (b).

> The published tree is out of headroom under the 32 MB budget and every run in the lane
> now fails `check.sh` on bookkeeping bytes. Which do you want: **(a)** raise
> `SITE_BUDGET_MB`; **(b)** stop publishing `changelog.js` twice — 1.35 MB of verbatim
> duplicate; **(c)** ship only the newest N changelog entries to the site and keep the
> whole literal in the renderer?

(c) touches the fleet changelog contract, which is why nothing was written. (b) costs
nothing and is already built and measured in #836 — T-0807 lands it first for that reason.
The question that survives (b) is whether (a) is also wanted, because 1.35 MB buys weeks,
not months, at the rate the mirror grows.

---

**2. Does this reconstruction model kinship across households at all?** — T-0787 (the
kin ticket, whose id now collides with dev's Wright-sheet T-0787 and must be restamped),
blocking [#822](https://github.com/kevinrhaas/custom/pull/822) and
[#839](https://github.com/kevinrhaas/custom/pull/839).

> Should this reconstruction model kinship across households at all, and if so in what
> shape — **(a)** a `kin[]` block on the person, **(b)** a separate edge file, or
> **(c)** nothing, and the prose stands by design?

[#839](https://github.com/kevinrhaas/custom/pull/839) is a worked, validated
demonstration of (a) — it exists precisely so the answer can be given against something
real rather than in the abstract. James Kinzie and John Harris Kinzie being half-brothers
is the case in hand.

---

**3. Which is the planform of record at Wolf Point?** — T-0685, blocking
[#886](https://github.com/kevinrhaas/custom/pull/886).

> Thompson 1830 puts the North Branch 27–43 m (east bank) and 35–60 m (west bank) west of
> the committed Wright 1834 line, and 20 m wider; the main stem agrees inside the declared
> ±20 m. **Moving the bank re-derives every waterline in the project**, so nothing was
> moved.

The measurement and what each answer costs are in the ticket and in
`docs/RESEARCH/thompson_forks_georeference.md`. This is the expensive one: the answer
"Thompson" re-derives the heightfield, the terrain and water GLBs, the landings, the
plantings and the sidecars — the same cascade T-0686 (#882) ran for a 30 m seam.

---

**Acceptance:** each of the three questions carries a written answer in its own ticket
(T-0730, the restamped kin ticket, T-0685), quoted verbatim where the owner gave one, with
the reasoning that follows from it. Each of #841, #822, #839 and #886 is then either
merged, re-scoped, or closed with the answer named — none of them is left parked. If an
answer costs a re-derivation, its cascade is filed as its own ticket before this one
closes, sized in runs.

**This ticket is `blocked-owner` by construction** and stays out of a claim until the
answers exist. `ticket.mjs block --owner` is not used here only because that removes the
line from QUEUE.md, and the owner put this band at the top.
