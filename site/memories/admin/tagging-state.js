const has = (map, id) => Object.hasOwn(map, id);
const entry = (map, id) => has(map, id) ? map[id] : undefined;
function same(a, b) {
  if (!a || !b) return a === b;
  const canonical = (value) => JSON.stringify({ tags: value.tags || [], people: value.people || [], caption: Object.hasOwn(value, 'caption') ? value.caption : null });
  return canonical(a) === canonical(b);
}

// Keep independent changes made in another browser, including removals. A
// conflicting edit is returned for human review instead of silently winning.
export function reconcileApproved(latest, local, baseline = { version: 1, photos: {} }) {
  const photos = Object.assign(Object.create(null), latest.photos);
  const conflicts = [];
  for (const id of new Set([...Object.keys(baseline.photos), ...Object.keys(local.photos)])) {
    const before = entry(baseline.photos, id);
    const here = entry(local.photos, id);
    const remote = entry(latest.photos, id);
    if (same(here, before)) continue;
    if (same(remote, before) || same(remote, here)) {
      if (here) photos[id] = here;
      else delete photos[id];
    } else conflicts.push({ id, local: here, published: remote });
  }
  return { approved: { version: 1, photos }, conflicts };
}
