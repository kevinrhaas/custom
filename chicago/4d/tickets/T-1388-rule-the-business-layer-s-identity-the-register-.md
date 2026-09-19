---
id: T-1388
title: Rule the business layer's identity: the register's compiled records hold houses printed twice under different styles, and each colliding group is one house or two, ruled from the sources, declared in identity.json, carried by the compiler and re-counted in the census crosswalk
state: claimed
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1182
opened: 2026-09-19
closed: null
pr: null
claimed_by: run 9/19/2026, 8:37:09 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35445967238
---

Rule the business layer's identity: the register's compiled records hold houses printed twice under different styles, and each colliding group is one house or two, ruled from the sources, declared in identity.json, carried by the compiler and re-counted in the census crosswalk.

Piece 1 of 4 of **T-1182 — Audit every attested and inferred business against the research: proprietors, partners, dates, primary and secondary premises, the Dec 1835 State census classes and the August 1835 American count — and raise an inferred business for every in-window trade that has none**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (stated before working — one demonstration, never weakened to pass)

1. Every pair of business records the register's own PEOPLE put together — the same
   surname read off two notices as a proprietor or a partner — is enumerated, with the
   printings each side rests on. `compile_gazetteer.py` groups on the partner surnames of
   the trading STYLE, and 146 of the 179 present records name no partner in their style,
   so those records' identity is never put in question at all.
2. The enumeration is a committed ledger and a gate, and its count may only FALL: a pair
   that disappears is a ruling, a pair that APPEARS is a business record that landed
   beside one the town already holds without being adjudicated, and fails the gate. The
   discipline is `audit_scene_window_trades.py`'s.
3. The class the ledger turns up that the sources already settle is RULED — declared in
   identity.json as a merge, a refusal or a premises relation, each naming both spellings
   verbatim and the printings it rests on, as that file requires. Not every pair: the
   pairs whose answer needs a reading nobody has made stay in the ledger, named, which is
   the point of the ledger.
4. Nothing is removed from the town by a ruling. A merge keeps both styles, both anchors,
   every printing and every trade word either side printed.
5. The census crosswalk is re-run under the rulings and its deltas re-printed, because a
   house counted twice is a town measured wrong.
6. A report says what was found, what was ruled and what is left, and it says what the
   left-over pairs are actually asking.
