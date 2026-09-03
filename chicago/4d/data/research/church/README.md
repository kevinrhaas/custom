# Church registers — baptisms, marriages and burials

**What lives here.** Sacramental registers naming people in and around Chicago in
the scene window. St Mary's baptismal register 1833-1835 comes first, because
eleven images of it are already in the deposit and unread (T-0503).

**Shape: `records`.** A register is a LIST: one entry is one record. `as_read`
keeps the clerk's Latin, his abbreviations and his spelling exactly as they stand;
`normalized` is this project's spelling of the same person. The two are never
merged — a register's Latin forms are the evidence a later crosswalk reasons from.

**Sponsors and parents are names, and names are people.** An entry that names a
child, two parents and two sponsors carries five readings, not one. Record each,
with its role in `notes`.

**A baptism is not a residence.** It documents that a person was present at a font
on a date. Where the register places them in the town, that is a separate claim
with its own reasoning, and it belongs in `crosswalk.json` or in the resident
record's own note — not in this row.

**Hand-authored:** `records/`, `coverage.json`, `crosswalk.json`.
**Generated:** nothing here yet; `data/research/domains.json` is, and is gated.

**Coverage.** Declare the IMAGES read, by image id. Eleven is the deposit's size
for St Mary's; a twelfth image found later is an undeclared item, which is not a
fault. A declared image nothing reaches IS.

**Reading grade.** A reading made off the page image is `scan_verified` and
outranks a `transcription_mediated` one. Register hands are hard; say which you
did.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`.
