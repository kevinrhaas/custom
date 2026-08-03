let model;
const $ = (id) => document.getElementById(id);
const cleanYear = (value) => { const m = String(value || '').match(/\d{4}/); return m ? Number(m[0]) : null; };

function activeInYear(row, year) {
  const built = cleanYear(row.year_completed) ?? cleanYear(row.year_started);
  const gone = cleanYear(row.year_demolished);
  return built !== null && built <= year && (gone === null || gone >= year);
}

function closestMap(year) {
  return [...model.maps].sort((a,b) => {
    const da = Math.abs(Number(a.reference_year)-year), db = Math.abs(Number(b.reference_year)-year);
    return da-db || Number(b.reference_year)-Number(a.reference_year);
  })[0];
}

function currentEvent(events, year) {
  const eligible = events.filter(e => (cleanYear(e.effective_start) ?? -Infinity) <= year && (cleanYear(e.effective_end) ?? Infinity) >= year);
  return eligible.sort((a,b) => (cleanYear(b.effective_start) ?? 0)-(cleanYear(a.effective_start) ?? 0))[0];
}

function render() {
  const year = Number($('year').value); $('yearOutput').value = year; $('yearOutput').textContent = year;
  const nearest = closestMap(year);
  const variants = model.maps.filter(m => m.reference_year === nearest.reference_year);
  const variant = $('mapVariant');
  const prior = variant.value;
  variant.innerHTML = variants.map(m => `<option value="${escapeHtml(m.map_id)}">${escapeHtml(m.title)}</option>`).join('');
  variant.value = variants.some(m => m.map_id === prior) ? prior : variants[0].map_id;
  const map = variants.find(m => m.map_id === variant.value) || nearest;
  $('mapTitle').textContent = map.title; $('mapYear').textContent = `shows ${map.reference_year}`;
  $('mapImage').src = `../${map.local_image_path.replace('maps/','maps/')}`;
  $('mapImage').alt = `${map.title}, reference year ${map.reference_year}`;
  $('mapLink').href = map.source_url;
  $('mapMeta').textContent = `${map.map_type.replaceAll('_',' ')} · created ${map.map_date} · ${map.credit_line} · ${map.rights_statement.replaceAll('_',' ')}`;
  $('mapNote').textContent = map.notes;

  const extent = currentEvent(model.cityExtentEvents, year);
  $('extentName').textContent = extent?.name || 'No dated city extent';
  $('extentNote').textContent = extent ? `${extent.legal_or_source_description}. Geometry: ${extent.geometry_status.replaceAll('_',' ')}.` : 'Chicago was not yet incorporated; consult the period map and landscape event.';
  const land = currentEvent(model.landformEvents, year);
  $('landName').textContent = land?.feature || 'No dated landscape event';
  $('landNote').textContent = land?.description || 'No specific event is currently cataloged for this year.';

  const query = $('search').value.toLowerCase().trim();
  let rows = model.buildings.filter(r => activeInYear(r, year));
  $('activeCount').textContent = rows.length.toLocaleString();
  if (query) rows = rows.filter(r => [r.canonical_name,r.address_historical,r.building_type].join(' ').toLowerCase().includes(query));
  rows.sort((a,b) => a.canonical_name.localeCompare(b.canonical_name));
  $('buildingRows').innerHTML = rows.map(r => `<tr><td><strong>${escapeHtml(r.canonical_name)}</strong>${r.needs_review==='true'?' <small>⚑ review</small>':''}</td><td>${escapeHtml(r.year_completed||r.year_started||'—')}</td><td>${escapeHtml((r.building_type||'—').replaceAll('_',' '))}</td><td>${escapeHtml(r.address_historical||'—')}</td><td>${escapeHtml(r.fire_fate_1871||'—')}</td><td>${escapeHtml(r.confidence)}</td></tr>`).join('');
}

function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }

fetch('data.json').then(r => r.json()).then(data => {
  model = data; $('year').addEventListener('input',render); $('search').addEventListener('input',render); $('mapVariant').addEventListener('change',render);
  document.querySelectorAll('[data-year]').forEach(b => b.addEventListener('click',() => { $('year').value=b.dataset.year; render(); }));
  render();
}).catch(error => { document.body.insertAdjacentHTML('beforeend',`<p>Could not load viewer data: ${escapeHtml(error.message)}</p>`); });
