
---

**THE SIBLING MINT IS THE SAME, AND IT IS WORSE. Measured by T-1141, 2026-09-15**, under
the fourth acceptance clause above ("the same question is asked of the sibling mints").

T-1141 needed two names lifted into the letter-list pool, which is a two-entity change to
one extraction, and ran the pass that owns that pool to find out what the refusals would
do with them:

    python3 tools/mint_letter_list_residents.py     # the writer, not --check
    744 files changed, 3356 insertions(+), 25932 deletions(-)

That is on the COMMITTED TREE WITH NO EDIT OF ANY KIND — the run above was repeated after
`git checkout -- .` and produced the same 744 files. So this is not the two-entity change
propagating; the committed town is simply not what its own writer writes, and the writer
is the one that loses the difference. Whole households are DELETED (`hh_abbott_constant`,
`hh_allen_william`, `hh_young_gideon` among them) and `data/residents/index.json` is
rewritten across 4,943 lines.

What makes it worse than the civic case rather than merely equal: `--check` is green on
that same tree, and `check.sh` runs `--gate` and `--self-test` and neither notices. So the
pass has a `--check` that passes on a tree its own `--build` would not produce, which is
the failure this ticket names, one layer further out. A run that touches the letter-list
pool for any reason at all — a lift, a re-read, one corrected name — cannot run the writer
without taking those 25,932 deletions with it, and has no way to tell which of them are
this pass's own output and which are another pass's findings standing on the same cards.

T-1141 stopped there rather than ship it, and its own two tails wait on this ticket: the
lift of `P. Cook` and `Jeter Foster` into the pool, and the movement of the 28 readings the
page overturns. Both are one small edit and one run of a writer that cannot currently be
run.
