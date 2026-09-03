# Church registers — baptisms, marriages and burials

**What lives here.** Sacramental registers naming people in and around Chicago in
the scene window. St Mary's baptismal register 1833-1835 comes first, because
eleven images of it are already in the deposit and unread (T-0503).

**What is here now (T-0573).** Father St. Cyr's MARRIAGE register and his death
and burial page, both read out of the *Illinois Catholic Historical Review* vol. 4
by way of the Genealogy Trails transcription: `records/st_cyr_marriages_1834_1839.json`
(128 entries, 513 named readings) and `records/st_cyr_deaths_1834_1837.json`
(11 entries, 13 named readings), with `claims/st_cyr_register_prose.json` for what
the article says around the entries and `st_cyr_crosswalk.json` for the scene-year
pass against `data/residents/`. `tools/read_st_cyr_register.py` builds and gates
all of it. The BAPTISMS are still unread — the same article tallies 282 of them —
and that is T-0503.

**Two things a later run should not have to rediscover.** First, the page titled
"First Chicago Marriage Records" is not all Chicago: footnote 5 puts three of its
first four entries at Bear Creek, Sangamon County. Those rows carry `at_chicago:
false` themselves. Second, the article prints its own tally — 22 St. Cyr marriages,
18 Schaeffer, 87 O'Meara, 1 Plunkett — and 22+18+87+1 = 128 is the only independent
check a reading of this page can have without the book. T-0573 was written against
"87 marriages", which is O'Meara's subtotal.

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
