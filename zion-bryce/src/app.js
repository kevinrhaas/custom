import {
  activityPlans,
  checklist,
  days,
  sources,
  stays,
  trailMatrix,
  trip,
  weatherPlaces
} from './data.js';

const STORAGE = {
  assignments: 'zionBryce.assignments.v1',
  checked: 'zionBryce.checked.v1',
  customItems: 'zionBryce.customItems.v1',
  completedDays: 'zionBryce.completedDays.v1',
  notes: 'zionBryce.notes.v1',
  stays: 'zionBryce.stays.v1',
  weather: 'zionBryce.weather.v1'
};

const flexibleDates = days.filter((day) => day.flexible).map((day) => day.date);
const defaultAssignments = {
  '2026-09-07': 'scout',
  '2026-09-08': 'narrows',
  '2026-09-09': 'flex'
};
const activityIds = Object.keys(activityPlans);

let assignments = normalizeAssignments(readJSON(STORAGE.assignments, defaultAssignments));
let completedDays = new Set(readJSON(STORAGE.completedDays, []));
let checkedItems = new Set(readJSON(STORAGE.checked, []));
let customItems = readJSON(STORAGE.customItems, []);
let privateStays = readJSON(STORAGE.stays, {});
let forecastData = null;
let forecastSuggestion = null;
let currentFilter = 'All';
let remainingOnly = false;
let deferredInstallPrompt = null;
let toastTimer = null;

const icon = (name) => `<svg aria-hidden="true"><use href="#i-${name}"/></svg>`;
const escapeHtml = (value) => String(value ?? '')
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

function readJSON(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : structuredClone(fallback);
  } catch (error) {
    return structuredClone(fallback);
  }
}

function writeJSON(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (error) {
    showToast('This browser could not save the change.');
    return false;
  }
}

function normalizeAssignments(candidate) {
  const values = flexibleDates.map((date) => candidate?.[date]);
  if (values.every((value) => activityIds.includes(value)) && new Set(values).size === activityIds.length) {
    return { ...candidate };
  }
  return { ...defaultAssignments };
}

function showToast(message) {
  const toast = document.querySelector('#toast');
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('show'), 2600);
}

function formatShortDate(date) {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    timeZone: 'America/Denver'
  }).format(new Date(`${date}T12:00:00-06:00`));
}

function getEffectiveDay(day) {
  if (!day.flexible) return day;
  const plan = activityPlans[assignments[day.date]];
  return {
    ...day,
    title: plan.title,
    summary: plan.strap,
    chips: plan.stats,
    schedule: plan.schedule,
    alerts: plan.alerts,
    links: plan.links,
    activity: plan.id
  };
}

function dayCardTemplate(rawDay, initiallyOpen) {
  const day = getEffectiveDay(rawDay);
  const isDone = completedDays.has(String(day.day));
  const open = initiallyOpen ? ' open' : '';
  const flexibleLabel = rawDay.flexible ? ` · ${activityPlans[assignments[rawDay.date]].short}` : '';
  return `
    <details class="day-card${isDone ? ' day-done' : ''}" data-day="${day.day}"${open}>
      <summary>
        <div class="day-summary">
          <div class="day-number"><span>DAY</span><strong>${day.day}</strong></div>
          <div class="day-heading">
            <span class="eyebrow">${escapeHtml(day.dateLabel)} · ${escapeHtml(day.route)}</span>
            <h3>${escapeHtml(day.title)}</h3>
            <p>${escapeHtml(day.summary || day.eyebrow)}</p>
            <div class="day-chips">${(day.chips || []).slice(0, 4).map((chip) => `<span class="chip">${escapeHtml(chip)}</span>`).join('')}</div>
          </div>
          <span class="day-open-cue" aria-hidden="true"></span>
        </div>
      </summary>
      <div class="day-content">
        <div class="day-meta">
          <span><strong>${escapeHtml(day.eyebrow)}</strong>${escapeHtml(flexibleLabel)}</span>
          <span>Sleep: <strong>${escapeHtml(day.stay)}</strong></span>
          <label class="day-complete">
            <input type="checkbox" data-complete-day="${day.day}" ${isDone ? 'checked' : ''}>
            <span>${icon('check')}</span><span>Mark day complete</span>
          </label>
        </div>
        <div class="timeline">
          ${(day.schedule || []).map((entry) => `
            <div class="timeline-row">
              <div class="timeline-time">${escapeHtml(entry.time)}</div>
              <div class="timeline-body"><h4>${escapeHtml(entry.title)}</h4><p>${escapeHtml(entry.detail)}</p></div>
            </div>`).join('')}
        </div>
        <div class="alert-grid">
          ${(day.alerts || []).map((alert) => `<div class="alert-box ${escapeHtml(alert.tone)}"><strong>${escapeHtml(alert.title)}</strong><p>${escapeHtml(alert.text)}</p></div>`).join('')}
        </div>
        <div class="day-links">
          ${(day.links || []).map(([label, url]) => `<a class="day-link" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${escapeHtml(label)} ${icon('external')}</a>`).join('')}
        </div>
      </div>
    </details>`;
}

function renderDays({ preserveOpen = false } = {}) {
  const list = document.querySelector('#daysList');
  const openDays = preserveOpen
    ? new Set([...list.querySelectorAll('.day-card[open]')].map((card) => card.dataset.day))
    : new Set([String(currentTripDay() || 1)]);
  list.innerHTML = days.map((day) => dayCardTemplate(day, openDays.has(String(day.day)))).join('');

  list.querySelectorAll('[data-complete-day]').forEach((box) => {
    box.addEventListener('change', () => {
      const value = box.dataset.completeDay;
      if (box.checked) completedDays.add(value);
      else completedDays.delete(value);
      writeJSON(STORAGE.completedDays, [...completedDays]);
      box.closest('.day-card').classList.toggle('day-done', box.checked);
    });
  });
}

function currentTripDay() {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Denver',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  const today = formatter.format(new Date());
  const match = days.find((day) => day.date === today);
  return match?.day || null;
}

function renderCountdown() {
  const node = document.querySelector('#countdown');
  const start = new Date(`${trip.start}T00:00:00-05:00`);
  const end = new Date(`${trip.end}T23:59:59-06:00`);
  const now = new Date();
  if (now < start) {
    const count = Math.max(1, Math.ceil((start - now) / 86400000));
    node.textContent = `${count} day${count === 1 ? '' : 's'} until departure`;
  } else if (now <= end) {
    node.textContent = `Trip live · Day ${currentTripDay() || 'in progress'}`;
  } else {
    node.textContent = 'Trip complete · field guide archived';
  }
}

function renderAssignments() {
  const grid = document.querySelector('#assignmentGrid');
  grid.innerHTML = flexibleDates.map((date) => {
    const value = assignments[date];
    return `<div class="assignment-card">
      <label for="assign-${date}">${escapeHtml(formatShortDate(date))}</label>
      <select id="assign-${date}" data-assignment-date="${date}">
        ${activityIds.map((id) => `<option value="${id}" ${id === value ? 'selected' : ''}>${escapeHtml(activityPlans[id].short)}</option>`).join('')}
      </select>
      <p>${escapeHtml(activityPlans[value].strap)}</p>
    </div>`;
  }).join('');

  grid.querySelectorAll('select').forEach((select) => {
    select.addEventListener('change', () => {
      const date = select.dataset.assignmentDate;
      const previous = assignments[date];
      const next = select.value;
      const otherDate = flexibleDates.find((candidate) => candidate !== date && assignments[candidate] === next);
      assignments[date] = next;
      if (otherDate) assignments[otherDate] = previous;
      writeJSON(STORAGE.assignments, assignments);
      renderAssignments();
      renderDays({ preserveOpen: true });
      showToast('Zion day order updated.');
    });
  });
}

function renderTrailTable() {
  document.querySelector('#trailTableBody').innerHTML = trailMatrix.map((trail) => `<tr>
    <td>${escapeHtml(trail.name)}<br><small>${escapeHtml(trail.place)}</small></td>
    <td>${escapeHtml(trail.distance)}</td>
    <td>${escapeHtml(trail.gain)}</td>
    <td>${escapeHtml(trail.level)}</td>
    <td>${escapeHtml(trail.best)}</td>
    <td>${escapeHtml(trail.caveat)}</td>
  </tr>`).join('');
}

function weatherDescription(code) {
  if (code === 0) return 'Clear';
  if ([1, 2].includes(code)) return 'Mostly clear';
  if (code === 3) return 'Overcast';
  if ([45, 48].includes(code)) return 'Fog';
  if (code >= 51 && code <= 67) return 'Rain possible';
  if (code >= 71 && code <= 77) return 'Snow possible';
  if (code >= 80 && code <= 82) return 'Showers possible';
  if (code >= 95) return 'Storms possible';
  return 'Mixed conditions';
}

function isWetCode(code) {
  return (code >= 51 && code <= 67) || (code >= 80 && code <= 82) || code >= 95;
}

function buildForecastSuggestion(records) {
  const permutations = [
    ['scout', 'narrows', 'flex'], ['scout', 'flex', 'narrows'],
    ['narrows', 'scout', 'flex'], ['narrows', 'flex', 'scout'],
    ['flex', 'scout', 'narrows'], ['flex', 'narrows', 'scout']
  ];
  const score = (activity, record) => {
    const precip = Number(record.precip ?? 0);
    const high = Number(record.high ?? 78);
    const wet = isWetCode(Number(record.code));
    if (activity === 'narrows') return 180 - precip * 2.8 - (wet ? 95 : 0);
    if (activity === 'scout') return 130 - Math.max(0, high - 74) * 3 - precip * 1.1 - (wet ? 20 : 0);
    return 70 + precip * .35 + Math.max(0, high - 82) * 1.4 + (wet ? 20 : 0);
  };
  const ranked = permutations.map((order) => ({
    order,
    total: order.reduce((sum, activity, index) => sum + score(activity, records[flexibleDates[index]]), 0)
  })).sort((a, b) => b.total - a.total);
  return Object.fromEntries(flexibleDates.map((date, index) => [date, ranked[0].order[index]]));
}

function normalizeForecast(place, payload) {
  const records = {};
  payload.daily.time.forEach((date, index) => {
    records[date] = {
      place: place.name,
      high: payload.daily.temperature_2m_max[index],
      low: payload.daily.temperature_2m_min[index],
      precip: payload.daily.precipitation_probability_max[index] ?? 0,
      code: payload.daily.weather_code[index],
      sunrise: payload.daily.sunrise[index],
      sunset: payload.daily.sunset[index]
    };
  });
  return records;
}

async function fetchWeather() {
  const status = document.querySelector('#weatherStatus');
  const button = document.querySelector('#refreshWeather');
  button.disabled = true;
  status.textContent = 'Contacting Open-Meteo…';
  renderWeatherSkeleton();
  try {
    const results = await Promise.all(weatherPlaces.map(async (place) => {
      const start = place.dates[0];
      const end = place.dates.at(-1);
      const params = new URLSearchParams({
        latitude: place.latitude,
        longitude: place.longitude,
        daily: 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset',
        temperature_unit: 'fahrenheit',
        wind_speed_unit: 'mph',
        timezone: 'America/Denver',
        start_date: start,
        end_date: end
      });
      const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Forecast response ${response.status}`);
      return [place.id, normalizeForecast(place, await response.json())];
    }));
    forecastData = Object.fromEntries(results);
    writeJSON(STORAGE.weather, { fetchedAt: new Date().toISOString(), data: forecastData });
    status.textContent = `Updated ${new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit' }).format(new Date())} · forecast can still shift`;
  } catch (error) {
    const cached = readJSON(STORAGE.weather, null);
    if (cached?.data) {
      forecastData = cached.data;
      const age = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }).format(new Date(cached.fetchedAt));
      status.textContent = `Offline forecast from ${age}`;
    } else {
      forecastData = null;
      status.textContent = 'Forecast unavailable · use the official condition links';
    }
  } finally {
    button.disabled = false;
    renderWeather();
  }
}

function renderWeatherSkeleton() {
  document.querySelector('#weatherGrid').innerHTML = flexibleDates.map(() => '<div class="weather-skeleton" aria-hidden="true"></div>').join('');
}

function renderWeather() {
  const grid = document.querySelector('#weatherGrid');
  const zion = forecastData?.springdale;
  const apply = document.querySelector('#applyForecast');
  if (!zion || !flexibleDates.every((date) => zion[date])) {
    forecastSuggestion = null;
    apply.disabled = true;
    grid.innerHTML = flexibleDates.map((date) => `<article class="weather-card"><div class="weather-date"><span>${escapeHtml(formatShortDate(date))}</span>${icon('cloud')}</div><p>No live forecast is available for this date yet. Keep the original order as a placeholder.</p></article>`).join('');
    return;
  }
  forecastSuggestion = buildForecastSuggestion(zion);
  apply.disabled = false;
  grid.innerHTML = flexibleDates.map((date) => {
    const record = zion[date];
    const pick = activityPlans[forecastSuggestion[date]].short;
    return `<article class="weather-card">
      <div class="weather-date"><span>${escapeHtml(formatShortDate(date))}</span>${icon('cloud')}</div>
      <div class="weather-temp"><strong>${Math.round(record.high)}°</strong><span>low ${Math.round(record.low)}°</span></div>
      <p>${escapeHtml(weatherDescription(record.code))} · ${Math.round(record.precip)}% max precipitation chance</p>
      <span class="forecast-pick">Best forecast fit: ${escapeHtml(pick)}</span>
    </article>`;
  }).join('');
}

function renderRouteLedger() {
  const legs = [
    ['Las Vegas → Springdale', 'Sept 6 · ≈2 hr 45 direct · lose 1 hour', 'https://www.google.com/maps/dir/Las+Vegas,+NV/Springdale,+UT'],
    ['Springdale → Bryce', 'Sept 10 · ≈2 hours driving, plus stops', 'https://www.google.com/maps/dir/Springdale,+UT/Bryce+Canyon+National+Park'],
    ['Bryce → St. George', 'Sept 12 · ≈4 hours via Kanab + parks', 'https://www.google.com/maps/dir/Bryce+Canyon+National+Park/Kanab,+UT/Coral+Pink+Sand+Dunes+State+Park/Snow+Canyon+State+Park/St.+George,+UT'],
    ['St. George → LAS', 'Sept 13 · ≈2 hours · gain 1 hour', 'https://www.google.com/maps/dir/St.+George,+UT/Harry+Reid+International+Airport+Rent-A-Car+Center']
  ];
  document.querySelector('#routeLedger').innerHTML = legs.map((leg, index) => `<div class="route-leg">
    <span class="route-leg-index">${String(index + 1).padStart(2, '0')}</span>
    <div><h3>${escapeHtml(leg[0])}</h3><p>${escapeHtml(leg[1])}</p><a href="${escapeHtml(leg[2])}" target="_blank" rel="noreferrer">Open route ${icon('external')}</a></div>
  </div>`).join('');
}

function renderSources() {
  document.querySelector('#sourceGrid').innerHTML = sources.map((source) => `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer"><span>${escapeHtml(source.label)}</span><small>${escapeHtml(source.group)}</small></a>`).join('');
}

function renderCheckFilters() {
  const categories = ['All', ...new Set([...checklist, ...customItems].map((item) => item.category))];
  document.querySelector('#checkFilters').innerHTML = categories.map((category) => `<button class="filter-button ${currentFilter === category ? 'active' : ''}" type="button" data-filter="${escapeHtml(category)}">${escapeHtml(category)}</button>`).join('');
  document.querySelectorAll('[data-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      currentFilter = button.dataset.filter;
      renderChecklist();
    });
  });
}

function checklistItemTemplate(item, custom = false) {
  const done = checkedItems.has(item.id);
  const visible = (currentFilter === 'All' || item.category === currentFilter) && (!remainingOnly || !done);
  if (!visible) return '';
  return `<div class="check-item ${done ? 'done' : ''} ${custom ? 'custom' : ''}" data-check-row="${escapeHtml(item.id)}">
    <input id="check-${escapeHtml(item.id)}" type="checkbox" data-check-id="${escapeHtml(item.id)}" ${done ? 'checked' : ''}>
    <span class="check-box">${icon('check')}</span>
    <label class="check-copy" for="check-${escapeHtml(item.id)}"><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.note || 'Private checklist item')}</small></label>
    ${custom ? `<button class="custom-remove" type="button" data-remove-item="${escapeHtml(item.id)}" aria-label="Remove ${escapeHtml(item.label)}">${icon('trash')}</button>` : `<span class="check-category">${escapeHtml(item.category)}</span>`}
  </div>`;
}

function renderChecklist() {
  renderCheckFilters();
  const allItems = [...checklist.map((item) => ({ ...item, custom: false })), ...customItems.map((item) => ({ ...item, custom: true }))];
  const visibleMarkup = allItems.map((item) => checklistItemTemplate(item, item.custom)).join('');
  document.querySelector('#checklist').innerHTML = visibleMarkup || '<div class="advisory blue"><div><strong>Nothing left in this view.</strong><p>Switch filters or show completed items.</p></div></div>';

  document.querySelectorAll('[data-check-id]').forEach((box) => {
    box.addEventListener('change', () => {
      if (box.checked) checkedItems.add(box.dataset.checkId);
      else checkedItems.delete(box.dataset.checkId);
      writeJSON(STORAGE.checked, [...checkedItems]);
      renderChecklist();
    });
  });
  document.querySelectorAll('[data-remove-item]').forEach((button) => {
    button.addEventListener('click', () => {
      const id = button.dataset.removeItem;
      customItems = customItems.filter((item) => item.id !== id);
      checkedItems.delete(id);
      writeJSON(STORAGE.customItems, customItems);
      writeJSON(STORAGE.checked, [...checkedItems]);
      renderChecklist();
      showToast('Private item removed.');
    });
  });
  updateProgress();
}

function updateProgress() {
  const total = checklist.length + customItems.length;
  const validIds = new Set([...checklist, ...customItems].map((item) => item.id));
  const done = [...checkedItems].filter((id) => validIds.has(id)).length;
  document.querySelector('#progressText').textContent = `${done} of ${total} done`;
  document.querySelector('#progressBar').style.width = total ? `${Math.round(done / total * 100)}%` : '0%';
  document.querySelector('#showRemaining').textContent = remainingOnly ? 'Show all' : 'Show remaining';
}

function renderStays() {
  document.querySelector('#stayGrid').innerHTML = stays.map((stay) => `<article class="stay-card">
    <div class="stay-card-top"><div><span class="eyebrow">${escapeHtml(stay.nights)}</span><h3>${escapeHtml(stay.name)}</h3><p class="stay-place">${escapeHtml(stay.place)}</p></div><a href="${escapeHtml(stay.map)}" target="_blank" rel="noreferrer">Map</a></div>
    <p>${escapeHtml(stay.note)}</p>
    <label for="stay-${escapeHtml(stay.id)}">Private confirmation / room note<input id="stay-${escapeHtml(stay.id)}" data-stay-id="${escapeHtml(stay.id)}" value="${escapeHtml(privateStays[stay.id] || '')}" autocomplete="off" spellcheck="false"></label>
  </article>`).join('');
  document.querySelectorAll('[data-stay-id]').forEach((input) => {
    input.addEventListener('input', () => {
      privateStays[input.dataset.stayId] = input.value;
      writeJSON(STORAGE.stays, privateStays);
    });
  });
}

function switchView(name, { updateHash = true, scroll = true } = {}) {
  const allowed = ['plan', 'swap', 'route', 'pack', 'notes'];
  const view = allowed.includes(name) ? name : 'plan';
  document.querySelectorAll('[data-view]').forEach((section) => { section.hidden = section.dataset.view !== view; });
  document.querySelectorAll('[data-view-target]').forEach((button) => {
    const active = button.dataset.viewTarget === view;
    button.classList.toggle('active', active);
    if (active) button.setAttribute('aria-current', 'page');
    else button.removeAttribute('aria-current');
  });
  if (updateHash) history.replaceState(null, '', view === 'plan' ? location.pathname : `#${view}`);
  if (scroll) {
    const nav = document.querySelector('.view-nav');
    const section = document.querySelector(`[data-view="${view}"]`);
    const top = window.matchMedia('(max-width: 720px)').matches
      ? Math.max(0, section.offsetTop - 12)
      : nav.offsetTop;
    window.scrollTo({ top, behavior: 'smooth' });
  }
}

function setupNavigation() {
  document.querySelectorAll('[data-view-target]').forEach((button) => button.addEventListener('click', () => switchView(button.dataset.viewTarget)));
  switchView(location.hash.replace('#', '') || 'plan', { updateHash: false, scroll: Boolean(location.hash) });
  window.addEventListener('hashchange', () => switchView(location.hash.replace('#', '') || 'plan', { updateHash: false }));
}

function setupTheme() {
  const modes = ['system', 'dark', 'light'];
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const apply = (mode) => {
    const resolved = mode === 'system' ? (media.matches ? 'dark' : 'light') : mode;
    document.documentElement.dataset.theme = resolved;
    document.documentElement.dataset.themeMode = mode;
    document.querySelector('#themeLabel').textContent = mode[0].toUpperCase() + mode.slice(1);
    document.querySelector('#themeButton').setAttribute('aria-label', `Theme: ${mode}`);
    const themeColor = resolved === 'dark' ? '#141210' : '#f3f0ea';
    document.querySelector('meta[name="theme-color"]').setAttribute('content', themeColor);
  };
  let mode = document.documentElement.dataset.themeMode || 'system';
  apply(mode);
  document.querySelector('#themeButton').addEventListener('click', () => {
    mode = modes[(modes.indexOf(mode) + 1) % modes.length];
    try { localStorage.setItem('custom.theme', mode); } catch (error) {}
    apply(mode);
  });
  media.addEventListener?.('change', () => { if (mode === 'system') apply(mode); });
}

function setupNetworkStatus() {
  const node = document.querySelector('#netStatus');
  const paint = () => {
    node.classList.toggle('online', navigator.onLine);
    node.classList.toggle('offline', !navigator.onLine);
    node.querySelector('.net-label').textContent = navigator.onLine ? 'Online' : 'Offline';
  };
  window.addEventListener('online', paint);
  window.addEventListener('offline', paint);
  paint();
}

function nextDate(date) {
  const value = new Date(`${date}T00:00:00Z`);
  value.setUTCDate(value.getUTCDate() + 1);
  return value.toISOString().slice(0, 10);
}

function icsDate(date) {
  return date.replaceAll('-', '');
}

function icsEscape(value) {
  return String(value).replaceAll('\\', '\\\\').replaceAll('\n', '\\n').replaceAll(',', '\\,').replaceAll(';', '\\;');
}

function downloadBlob(name, contents, type) {
  const url = URL.createObjectURL(new Blob([contents], { type }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = name;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadCalendar() {
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  const events = days.map((rawDay) => {
    const day = getEffectiveDay(rawDay);
    return [
      'BEGIN:VEVENT',
      `UID:zion-bryce-day-${day.day}@custom.polecat`,
      `DTSTAMP:${stamp}`,
      `DTSTART;VALUE=DATE:${icsDate(day.date)}`,
      `DTEND;VALUE=DATE:${icsDate(nextDate(day.date))}`,
      `SUMMARY:${icsEscape(`Day ${day.day} · ${day.title}`)}`,
      `DESCRIPTION:${icsEscape(`${day.route}\n${day.summary || ''}\nSleep: ${day.stay}`)}`,
      'END:VEVENT'
    ].join('\r\n');
  });
  events.push([
    'BEGIN:VEVENT',
    'UID:zion-bryce-painted-pony@custom.polecat',
    `DTSTAMP:${stamp}`,
    'DTSTART;TZID=America/Denver:20260912T190000',
    'DTEND;TZID=America/Denver:20260912T210000',
    'SUMMARY:Painted Pony reservation',
    'LOCATION:2 W St George Blvd #22\\, St. George\\, UT',
    'DESCRIPTION:Arrive by 6:40 PM. Reservation is at 7:00 PM.',
    'END:VEVENT'
  ].join('\r\n'));
  const calendar = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'PRODID:-//Custom//Zion Bryce Field Guide//EN', ...events, 'END:VCALENDAR'].join('\r\n');
  downloadBlob('zion-bryce-2026.ics', calendar, 'text/calendar;charset=utf-8');
  showToast('Trip calendar downloaded.');
}

async function shareTrip() {
  const data = { title: 'Zion + Bryce Canyon Loop', text: 'Nine-day Zion and Bryce Canyon field guide · Sept 5–13, 2026', url: trip.publicUrl };
  try {
    if (navigator.share) await navigator.share(data);
    else {
      await navigator.clipboard.writeText(trip.publicUrl);
      showToast('Trip link copied.');
    }
  } catch (error) {
    if (error.name !== 'AbortError') showToast('Could not share the link.');
  }
}

function exportPrivateBackup() {
  const backup = {
    app: 'Zion + Bryce Canyon Field Guide',
    exportedAt: new Date().toISOString(),
    assignments,
    completedDays: [...completedDays],
    checkedItems: [...checkedItems],
    customItems,
    stays: privateStays,
    notes: document.querySelector('#tripNotes').value
  };
  downloadBlob('zion-bryce-private-backup.json', `${JSON.stringify(backup, null, 2)}\n`, 'application/json');
  showToast('Private backup downloaded.');
}

function setupActions() {
  document.querySelector('#calendarButton').addEventListener('click', downloadCalendar);
  document.querySelector('#shareButton').addEventListener('click', shareTrip);
  document.querySelector('#printButton').addEventListener('click', () => window.print());
  document.querySelector('#expandDays').addEventListener('click', () => document.querySelectorAll('.day-card').forEach((card) => { card.open = true; }));
  document.querySelector('#collapseDays').addEventListener('click', () => document.querySelectorAll('.day-card').forEach((card) => { card.open = false; }));
  document.querySelector('#refreshWeather').addEventListener('click', fetchWeather);
  document.querySelector('#applyForecast').addEventListener('click', () => {
    if (!forecastSuggestion) return;
    assignments = { ...forecastSuggestion };
    writeJSON(STORAGE.assignments, assignments);
    renderAssignments();
    renderDays({ preserveOpen: true });
    showToast('Forecast-fit order applied. Check official conditions next.');
  });
  document.querySelector('#showRemaining').addEventListener('click', () => {
    remainingOnly = !remainingOnly;
    renderChecklist();
  });
  document.querySelector('#addItemForm').addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.querySelector('#newItem');
    const label = input.value.trim();
    if (!label) return;
    customItems.push({ id: `private-${Date.now()}`, category: 'Private', label, note: 'Added on this device' });
    writeJSON(STORAGE.customItems, customItems);
    input.value = '';
    currentFilter = 'All';
    renderChecklist();
    showToast('Private item added.');
  });
  document.querySelector('#exportNotes').addEventListener('click', exportPrivateBackup);
  document.querySelector('#clearPrivate').addEventListener('click', () => {
    const confirmed = window.confirm('Clear private notes, confirmations and checklist progress from this browser? This cannot be undone unless you exported a backup.');
    if (!confirmed) return;
    Object.values(STORAGE).forEach((key) => localStorage.removeItem(key));
    location.reload();
  });

  const notes = document.querySelector('#tripNotes');
  notes.value = readJSON(STORAGE.notes, '');
  let noteTimer;
  notes.addEventListener('input', () => {
    document.querySelector('#notesStatus').textContent = 'Saving…';
    window.clearTimeout(noteTimer);
    noteTimer = window.setTimeout(() => {
      writeJSON(STORAGE.notes, notes.value);
      document.querySelector('#notesStatus').textContent = 'Saved locally';
    }, 300);
  });
}

function setupInstall() {
  const button = document.querySelector('#installButton');
  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    button.hidden = false;
  });
  button.addEventListener('click', async () => {
    if (!deferredInstallPrompt) return;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    button.hidden = true;
  });
  window.addEventListener('appinstalled', () => showToast('Field guide installed for offline use.'));
}

async function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return;
  try {
    await navigator.serviceWorker.register('./sw.js');
  } catch (error) {
    console.warn('Offline registration failed', error);
  }
}

function init() {
  setupTheme();
  setupNetworkStatus();
  renderCountdown();
  renderDays();
  renderAssignments();
  renderTrailTable();
  renderRouteLedger();
  renderSources();
  renderChecklist();
  renderStays();
  setupNavigation();
  setupActions();
  setupInstall();
  renderWeatherSkeleton();
  fetchWeather();
  registerServiceWorker();
}

init();
