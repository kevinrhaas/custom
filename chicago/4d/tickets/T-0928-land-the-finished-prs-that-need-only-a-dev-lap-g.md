---
id: T-0928
title: Land the finished PRs that need only a dev lap: gated units sitting open because dev moved under them
state: open
epic: PIPELINE
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

These PRs are finished units. They are gated green and they are open only because `dev`
moved under them and GitHub cannot merge a branch whose generated files need this repo's
merge drivers (**T-0857**, which is why that ticket leads this band).

`#940`, `#951`, `#967`, `#971`, `#1012`, `#1017`.

**The lap, and it is mechanical:**

```
git checkout <branch> && git merge origin/dev     # the drivers resolve the generated files
cd chicago/4d
# if the merge brought data or a tool change, run the cascade in order:
python3 tools/consolidate_resident_evidence.py --build
python3 tools/mint_civic_residents.py --build && python3 tools/mint_civic_residents.py --regrade
python3 tools/compile_liberties.py && python3 tools/compile_register.py --build
# ... the readers, the crosswalks, the spends, the exports ...
python3 tools/consolidate_town_cards.py --apply && python3 tools/town_census.py
python3 tools/compile_scene.py --all
node tools/ticket.mjs board && node tools/ticket.mjs check
node tools/stamp-changelog.mjs && node tools/check-changelog.mjs
bash tools/publish.sh && bash tools/check.sh
```

**Land them ONE AT A TIME, and merge immediately when the gate goes green.** With the lane
at one slice, `dev` only moves when this run moves it, so a lap taken and pushed is a lap
that lands. Two slices is what made this a treadmill: every landing invalidated the other
in-flight branch, and a branch could be lapped four times without ever being mergeable.

**Binary conflicts are not conflicts.** The four `.xlsx` workbooks under
`chicago/reference/resident-research/` are cascade output. Take `dev`'s side and let
`export_resident_research_package --all --build` and `export_resident_audit --build`
rebuild them. Never hand-resolve one.

**A duplicate ticket id is the other lap-killer.** `tools/ticket.mjs check` catches it and
`restamp` repairs it; the ticket keeps its queue place, but anything that CITES the old
number — a card note, a doc line, the changelog — has to move with it, and the gate cannot
see those. Grep for the old id before committing.

**Acceptance:**

1. Each of the six is merged, or a written reason says why it could not be.
2. Every merge is preceded by a green `tools/check.sh` on the merged tree — the seven `FAIL`
   lines the gate prints for the cross-street faces, the southern ground and the far-timber
   census are its own negative-control self-tests and are expected; `CHECK PASS` and exit 0
   are the signal.
3. No changelog entry is landed twice. If `dev` already announced the work, drop the
   branch's entry rather than double-announcing it.
