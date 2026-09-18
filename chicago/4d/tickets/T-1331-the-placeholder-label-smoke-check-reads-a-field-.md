---
id: T-1331
title: The placeholder-label smoke check reads a field that does not exist, so parts 2-3 have been permanently red on a typo
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The placeholder-label smoke check reads a field that does not exist, so parts 2-3 have been permanently red on a typo.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1330, 2026-09-18**, running `SMOKE_VIEWPORT=desktop SMOKE_STAGE=3` against a
diff that touches nine resident cards and no asset at all.

`tools/smoke_renderer.mjs:7218` reads `placeholder.whereholderFlag`. The object built twenty
lines above it has `placeholderFlag`; there is no `whereholderFlag` on it and never was. So the
assertion is `undefined === (placeholder.recommended === true)`, which for an asset that is not
a placeholder is `undefined === false` — false, always, on every tree.

    FAIL desktop 1280x800: the placeholder label agrees with the asset it describes —
    {"real":false,"realFlag":false,"recommended":false,"placeholderFlag":false,
     "grade":"reconstructed","reconstructionFlag":true,"flagNamesTheGrade":true}

The check is the half its own comment says was missing — "placeholder massing is claimed when
the asset IS one, and — the half that was missing — never claimed when it is not". It has never
once made that test. It is on `origin/dev` today and a run can confirm it without a browser:
`git show origin/dev:chicago/4d/tools/smoke_renderer.mjs | grep whereholderFlag`.

**Why it matters more than a typo.** A permanently red check in parts 2-3 is a red every run
has to triage before it can read its own result, and `dev-smoke-state.json` records only the
FIRST failure of a leg — so this one has been hiding behind
`the invented-name programme left nothing behind on this layer` and does not appear in the
standing record at all. Two reds, one recorded.

**Acceptance:** the field name is corrected; the check then passes on a tree where the asset is
a real bake AND fails when a real bake is given a placeholder label (prove the second by
breaking it, in the file's own style); the leg is re-run and filed with
`tools/dev-smoke-state.mjs record`. If correcting it turns the assertion red for a real reason,
that is the finding and this ticket says so rather than deleting the check.

**Not this ticket:** `the invented-name programme left nothing behind on this layer`, the other
standing red in this leg (3 reconstructed people in the manifest, 0 on `hh_inf_cooper_north_04`).

