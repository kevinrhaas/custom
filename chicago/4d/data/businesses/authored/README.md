# `data/businesses/authored/`

Business records a human wrote, as opposed to the 196 in the directory above, which
`tools/compile_businesses.py --build` compiles out of the newspaper register and rewrites
whole on every build.

A record here is read, validated and carried into `index.json` untouched. It must:

- carry `provenance: "authored"` or `"reconstructed"` — never `"compiled_from_register"`,
  which `--check` refuses, because that word means *a rebuild produces this file* and a
  rebuild does not produce this one;
- validate against `../../businesses.schema.json` like any other record;
- satisfy the same semantic rules the compiled records do — a tier that cites nothing, a
  `person_id` the resident layer does not hold, a limit with no reason, or two primary
  locations are each refused here exactly as they are there.

It is empty today. T-1182 writes the inferred-by-audit firms into it; T-1184 and the
reconstruction band write the `rcb_…` records. `docs/RESEARCH/business-layer.md` is the page.
