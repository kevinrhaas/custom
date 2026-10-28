// Chicago Voter — Ballot Match. A short, adaptive scenario survey that fills in
// every race on the ballot (Ward 30 · Precinct 04 · ballot style 124) and says
// why. All the research lives in data.js; the survey in questions.js. No build
// step, no network calls, nothing leaves the browser.

import { ELECTION, AXES, RACES } from './data.js';
import { QUESTIONS, LIGHTNING_PROMPT } from './questions.js';

const KEY = 'chivoter.v1';
const THEME_KEY = 'chivoter.theme';
const MIN_AXIS_Q = 5;          // ask at least this many scenario questions
const STOP_VALUE = 0.55;       // stop when no question could move more than this
const JUDGES_AT = 4;           // the judges question comes in as the 5th card

const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const Q = Object.fromEntries(QUESTIONS.map((q) => [q.id, q]));
const RACE = Object.fromEntries(RACES.map((r) => [r.id, r]));

// ---------------------------------------------------------------- state
function fresh() {
  return { v: 1, phase: 'intro', answers: {}, order: [], skipped: [], variants: {}, shuffles: {},
    hist: [], picks: {}, judgePicks: {}, direct: {}, lightningDone: false, sharpen: false };
}
let S = load();
function load() {
  try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && s.v === 1) return Object.assign(fresh(), s); } catch (e) { /* private mode */ }
  return fresh();
}
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* ignore */ } }

// ---------------------------------------------------------------- profile
// The voter's position on each axis is the weighted mean of what their answers
// set; `conf` is how much weight sits behind it (1 = one full answer).
function profile(st = S) {
  const sum = {}, conf = {}, src = {};
  const party = { D: 0, R: 0, T: 0 };
  let partyAnswered = false, policy = null;
  for (const qid of st.order) {
    const q = Q[qid]; const a = st.answers[qid]; if (!q || !a) continue;
    const opt = q.options.find((o) => o.id === a.opt); if (!opt) continue;
    for (const [ax, raw] of Object.entries(opt.set || {})) {
      const [v, w] = Array.isArray(raw) ? raw : [raw, 1];
      sum[ax] = (sum[ax] || 0) + v * w; conf[ax] = (conf[ax] || 0) + w;
      if (w >= 0.99 || !src[ax]) src[ax] = { q: qid, short: opt.short, label: opt.label };
    }
    if (opt.party) { partyAnswered = true; Object.assign(party, { D: 0, R: 0, T: 0 }, opt.party); src.party = { q: qid, short: opt.short }; }
    if (opt.policy) { policy = opt.policy; src.policy = { q: qid, short: opt.short }; }
  }
  const u = {}; for (const ax in sum) u[ax] = sum[ax] / conf[ax];
  return { u, conf, src, party, partyAnswered, policy };
}

const partyKey = (p) => (p === 'D' ? 'D' : p === 'R' ? 'R' : p === 'NP' || !p ? null : 'T');

// ---------------------------------------------------------------- scoring
function scoreCand(c, race, P) {
  let s = 0, max = 0; const parts = [];
  for (const [ax, w] of Object.entries(race.weights || {})) {
    const cv = c.axes && c.axes[ax];
    if (!cv || cv.v == null || !P.conf[ax]) continue;
    const k = w * Math.min(1, P.conf[ax]);
    const sim = 1 - Math.abs(P.u[ax] - cv.v) / 2;   // +1 same spot … -1 opposite ends
    s += k * sim; max += k; parts.push({ ax, k, sim, why: cv.why });
  }
  const pk = partyKey(c.party);
  if (race.partyWeight && P.partyAnswered) {
    const pv = pk ? (P.party[pk] || 0) : 0;
    s += race.partyWeight * pv; max += race.partyWeight;
    if (pv) parts.push({ ax: 'party', k: race.partyWeight, sim: pv, why: c.partyName ? `the ${c.partyName} candidate` : '' });
  }
  const pct = max ? Math.round(clamp(50 + 50 * s / max, 0, 100)) : null;
  return { c, s, max, pct, parts };
}

function judgeVote(j, policy) {
  // → 'yes' | 'no' | 'blank'
  if (!policy) return null;
  if (policy === 'skip') return 'blank';
  if (policy === 'all') return 'yes';
  if (policy === 'bar') return j.flag === 'concern' ? 'no' : 'yes';
  if (policy === 'strict') return j.flag === 'concern' || j.flag === 'caution' ? 'no' : j.flag === 'unknown' ? 'blank' : 'yes';
  return null;
}

function evalRace(race, P, st = S) {
  if (race.kind === 'retention' || race.kind === 'judge') {
    const list = race.kind === 'retention' ? race.judges : race.candidates;
    const votes = list.map((j) => {
      const o = st.judgePicks[j.id];
      let vote = o || judgeVote(j, P.policy);
      if (race.kind === 'judge' && vote === 'no') vote = 'blank';   // an open seat has no No oval
      return { j, vote, locked: !!o };
    });
    const decided = votes.filter((v) => v.vote).length;
    return { race, votes, conf: P.policy || decided ? 'policy' : 'nodata', decided: decided === votes.length };
  }
  if (race.kind === 'measure') {
    const yes = { axes: race.yes || {} };
    const no = { axes: Object.fromEntries(Object.entries(race.yes || {}).map(([k, v]) => [k, { v: v.v == null ? null : -v.v, why: v.why }])) };
    const w = race.weights || Object.fromEntries(Object.keys(race.yes || {}).map((k) => [k, 1]));
    const rr = { weights: w };
    const sy = scoreCand(yes, rr, P), sn = scoreCand(no, rr, P);
    const direct = st.direct[race.id]; const lock = st.picks[race.id];
    let pick = null, conf = 'nodata', lean = 0;
    if (sy.max) { lean = (sy.s - sn.s) / (2 * sy.max); pick = lean > 0 ? 'yes' : lean < 0 ? 'no' : null; conf = Math.abs(lean) >= 0.45 ? 'strong' : Math.abs(lean) >= 0.2 ? 'lean' : 'close'; }
    if (direct) { pick = direct; conf = 'direct'; }
    if (lock) { pick = lock; conf = 'locked'; }
    return { race, pick, conf, lean, parts: lean >= 0 ? sy.parts : sn.parts, decided: !!pick };
  }
  // candidate race
  const scored = race.candidates.map((c) => scoreCand(c, race, P)).sort((a, b) => b.s - a.s || (a.c.ballot - b.c.ballot));
  const n = race.voteFor || 1;
  const lock = st.picks[race.id];
  let picks, conf;
  const any = scored.some((x) => x.max > 0);
  if (race.candidates.length === 1) {
    const x = scored[0];
    picks = [x.c.id];
    conf = 'unopposed';
    if (x.max > 0 && x.pct < 35) { picks = []; conf = 'unopposed-blank'; }
  } else if (!any) {
    picks = []; conf = 'nodata';
  } else {
    picks = scored.slice(0, n).map((x) => x.c.id);
    const cut = scored[n - 1], next = scored[n];
    const margin = next ? (cut.s - next.s) / Math.max(cut.max, 0.0001) : 1;
    conf = margin >= 0.5 ? 'strong' : margin >= 0.18 ? 'lean' : 'close';
  }
  if (lock) { picks = Array.isArray(lock) ? lock : [lock]; conf = 'locked'; }
  return { race, scored, picks, conf, decided: picks.length > 0 || conf === 'unopposed-blank' };
}

function evaluate(st = S) {
  const P = profile(st);
  const out = {}; for (const r of RACES) out[r.id] = evalRace(r, P, st);
  return { P, E: out };
}

function uncertainty(ev) {
  if (ev.conf === 'nodata') return 1;
  if (ev.conf === 'close') return 0.8;
  if (ev.conf === 'lean') return 0.45;
  if (ev.conf === 'strong') return 0.12;
  return 0;
}

// How much could asking q still change the ballot?
function questionValue(q, P, E) {
  if (q.kind) return 0;
  let v = 0;
  for (const r of RACES) {
    if (r.kind === 'retention' || r.kind === 'judge') continue;
    const ev = E[r.id]; const unc = uncertainty(ev);
    if (!unc) continue;
    for (const ax of q.axes) {
      const w = (r.weights || (r.kind === 'measure' && r.yes && r.yes[ax] ? { [ax]: 1 } : {}))[ax];
      if (!w) continue;
      let spread;
      if (r.kind === 'measure') { const y = r.yes && r.yes[ax]; spread = y && y.v != null ? Math.abs(y.v) / 2 : 0; }
      else {
        const vals = r.candidates.map((c) => c.axes && c.axes[ax] && c.axes[ax].v).filter((x) => x != null);
        spread = vals.length > 1 ? (Math.max(...vals) - Math.min(...vals)) / 4 : 0;
      }
      v += w * spread * unc * (1 - Math.min(1, P.conf[ax] || 0)) * (r.importance || 1);
    }
  }
  return v;
}

function lightningNeeded(E) {
  return RACES.filter((r) => r.kind === 'measure' && !S.direct[r.id] && !S.picks[r.id] &&
    (r.lightning || ['nodata', 'close'].includes(E[r.id].conf)));
}

function partisanUnsettled(E) {
  return RACES.some((r) => r.partyWeight && r.kind === 'pick' && ['nodata', 'close', 'lean'].includes(E[r.id].conf));
}

// The next card to show, or null when the survey is done.
function nextStep() {
  const { P, E } = evaluate();
  const asked = new Set([...S.order, ...S.skipped]);
  const axisAsked = S.order.filter((id) => !Q[id].kind).length + S.skipped.filter((id) => !Q[id].kind).length;
  if (!asked.has('judges') && S.order.length + S.skipped.length >= JUDGES_AT) return { q: Q.judges };
  const cands = QUESTIONS.filter((q) => !q.kind && !asked.has(q.id))
    .map((q) => ({ q, v: questionValue(q, P, E) })).sort((a, b) => b.v - a.v);
  if (cands.length && (S.sharpen || axisAsked < MIN_AXIS_Q || cands[0].v >= STOP_VALUE)) return { q: cands[0].q, value: cands[0].v };
  if (!asked.has('judges')) return { q: Q.judges };
  if (!asked.has('label') && partisanUnsettled(E)) return { q: Q.label };
  if (!S.lightningDone && lightningNeeded(E).length) return { lightning: lightningNeeded(E) };
  return null;
}

function remainingEstimate() {
  // a cheap simulation: how many more cards if every answer were the middle option
  let n = 0; const snap = JSON.stringify(S);
  const sim = JSON.parse(snap);
  const saved = S; S = sim;
  for (let i = 0; i < 20; i++) {
    const st = nextStep(); if (!st) break; n++;
    if (st.lightning) break;
    const q = st.q; S.order.push(q.id); S.answers[q.id] = { opt: q.options[1].id };
  }
  S = saved; return n;
}

// ---------------------------------------------------------------- explanations
function axisName(ax) { return (AXES[ax] && AXES[ax].name) || ax; }

function reasonsFor(ev, P) {
  const r = ev.race;
  if (r.kind === 'measure') {
    if (ev.conf === 'locked') return ['You chose this yourself.'];
    if (ev.conf === 'direct') return ['You answered this one directly in the lightning round.'];
    if (!ev.pick) return [];
    return ev.parts.filter((p) => p.sim > 0.2).sort((a, b) => b.k * b.sim - a.k * a.sim).slice(0, 2)
      .map((p) => `You picked <b>${esc((P.src[p.ax] || {}).short || axisName(p.ax))}</b>. ${esc(p.why || '')}`);
  }
  if (r.kind === 'retention' || r.kind === 'judge') return [];
  if (ev.conf === 'locked') return ['You chose this yourself.'];
  if (ev.conf === 'unopposed') return [`Unopposed. Your vote is a formality, and you can leave it blank.`];
  if (ev.conf === 'unopposed-blank') return [`Unopposed, but a poor match for your answers (${ev.scored[0].pct}%). Leaving it blank is allowed.`];
  const out = [];
  for (const id of ev.picks) {
    const x = ev.scored.find((y) => y.c.id === id); if (!x) continue;
    const top = x.parts.filter((p) => p.sim > 0.25).sort((a, b) => b.k * b.sim - a.k * a.sim).slice(0, 2);
    for (const p of top) {
      if (p.ax === 'party') out.push(`You said you'd <b>${esc((P.src.party || {}).short)}</b>; ${esc(x.c.name)} is ${esc(p.why)}.`);
      else out.push(`You picked <b>${esc((P.src[p.ax] || {}).short || axisName(p.ax))}</b>. ${esc(x.c.short || x.c.name)}: ${esc(p.why)}`);
    }
  }
  return out.slice(0, r.voteFor > 1 ? 4 : 2);
}

const CONF_LABEL = {
  strong: ['Strong match', 'ok'], lean: ['Leaning', 'lean'], close: ['Close call', 'warn'], nodata: ['Not yet', 'mute'],
  unopposed: ['Unopposed', 'mute'], 'unopposed-blank': ['Unopposed · blank', 'mute'], locked: ['Your pick', 'lock'],
  direct: ['You said', 'lock'], policy: ['Your judge rule', 'ok'],
};

function pickLabel(ev) {
  const r = ev.race;
  if (r.kind === 'measure') return ev.pick ? (ev.pick === 'yes' ? 'Yes' : ev.pick === 'no' ? 'No' : 'Leave blank') : '—';
  if (r.kind === 'retention') {
    if (!ev.votes.some((v) => v.vote)) return '—';
    const y = ev.votes.filter((v) => v.vote === 'yes').length, n = ev.votes.filter((v) => v.vote === 'no').length;
    const b = ev.votes.length - y - n;
    return [y && `Yes on ${y}`, n && `No on ${n}`, b && `${b} blank`].filter(Boolean).join(' · ');
  }
  if (r.kind === 'judge') {
    if (!ev.votes.some((v) => v.vote)) return '—';
    if (ev.votes.length === 1) return ev.votes[0].vote === 'yes' ? ev.votes[0].j.name : 'Leave blank';
    const y = ev.votes.filter((v) => v.vote === 'yes').length;
    return y === ev.votes.length ? `Vote all ${y}` : y ? `Vote ${y} · ${ev.votes.length - y} blank` : 'Leave all blank';
  }
  if (ev.conf === 'unopposed-blank') return 'Leave blank';
  if (!ev.picks.length) return '—';
  return ev.picks.map((id) => r.candidates.find((c) => c.id === id)).map((c) => c.short || c.name).join(', ');
}

// ---------------------------------------------------------------- rendering
const app = $('#app');
const ballotPane = $('#ballot');

function render() {
  document.body.dataset.phase = S.phase;
  if (S.phase === 'intro') renderIntro();
  else if (S.phase === 'q') renderStep();
  else renderDone();
  renderBallot();
  save();
}

function renderIntro() {
  const resumable = S.order.length > 0;
  const nRaces = RACES.filter((r) => r.kind !== 'retention').length;
  const nJudges = RACES.filter((r) => r.kind === 'retention').reduce((a, r) => a + r.judges.length, 0);
  app.innerHTML = `
  <section class="intro card-pop">
    <div class="kicker">${esc(ELECTION.dateLabel)} · ${esc(ELECTION.precinct)}</div>
    <h1>Your ballot,<br><span class="grad">matched.</span></h1>
    <p class="lead">Answer about ten quick scenarios. Every race on your ballot fills in as you go, from U.S. Senate down to the water district,
    the school board, the ${nJudges} judges and the six public questions, and each pick tells you which answer put it there.</p>
    <div class="intro-facts">
      <div><b>${nRaces}</b><span>races & questions</span></div>
      <div><b>${nJudges}</b><span>judges</span></div>
      <div><b>~10</b><span>questions</span></div>
      <div><b>4 min</b><span>start to finish</span></div>
    </div>
    <div class="cta-row">
      <button class="btn btn-primary btn-lg" id="start">${resumable ? 'Pick up where you left off →' : 'Start the survey →'}</button>
      ${resumable ? '<button class="btn btn-ghost" id="restart">Start over</button>' : ''}
      <button class="btn btn-ghost" id="browse">Just browse the ballot</button>
    </div>
    <p class="fine">${esc(ELECTION.ballotStyle)}. Every candidate profile is researched and cited, as of ${esc(ELECTION.asOf)}.
    This is a mirror of your own answers, not an endorsement. Nothing you answer leaves this browser.</p>
  </section>`;
  $('#start').onclick = () => { S.phase = 'q'; render(); };
  if ($('#restart')) $('#restart').onclick = () => { S = fresh(); S.phase = 'q'; render(); };
  $('#browse').onclick = () => openBallotSheet();
}

function chooseVariant(q) {
  if (S.variants[q.id] == null) S.variants[q.id] = Math.floor(Math.random() * q.variants.length);
  if (!S.shuffles[q.id]) {
    const ids = q.options.map((o) => o.id);
    // shuffle, but keep scale questions readable: either as written or reversed,
    // so the options still run in order from one end to the other
    S.shuffles[q.id] = q.kind ? ids : (Math.random() < 0.5 ? ids : ids.slice().reverse());
  }
  return q.variants[S.variants[q.id]];
}

function renderStep() {
  const st = nextStep();
  if (!st) { S.phase = 'done'; return render(); }
  if (st.lightning) return renderLightning(st.lightning);
  const q = st.q; const v = chooseVariant(q);
  const n = S.order.length + S.skipped.length + 1;
  const left = remainingEstimate();
  const pct = Math.round(100 * (n - 1) / (n - 1 + left));
  const opts = S.shuffles[q.id].map((id) => q.options.find((o) => o.id === id));
  const prev = S.answers[q.id];
  app.innerHTML = `
  <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><span style="width:${pct}%"></span></div>
  <div class="qmeta"><span>Question ${n}</span><span>${left <= 1 ? 'last one' : `about ${left - 1} more`}</span></div>
  <section class="qcard card-pop" aria-live="polite">
    <div class="qemoji" aria-hidden="true">${q.emoji}</div>
    <div class="kicker">${esc(q.topic)}</div>
    <h2>${esc(v.title)}</h2>
    <p class="scenario">${esc(v.scenario)}</p>
    <div class="opts" role="list">
      ${opts.map((o, i) => `<button class="opt${prev && prev.opt === o.id ? ' sel' : ''}" data-opt="${o.id}" role="listitem">
        <span class="opt-key">${'ABCD'[i]}</span><span class="opt-text">${esc(o.label)}</span></button>`).join('')}
    </div>
    <div class="qfoot">
      ${S.hist.length ? '<button class="link" id="back">← Back</button>' : '<span></span>'}
      <button class="link" id="skip">Skip this one</button>
    </div>
  </section>
  <p class="why-asked">${q.kind === 'judges' ? 'Asked because it decides every judge on side B.' : q.kind === 'party' ? 'Asked because a few partisan races are still close on the issues.' : esc(whyAsked(q))}</p>`;
  app.querySelectorAll('.opt').forEach((b) => b.onclick = () => answer(q, b.dataset.opt));
  $('#skip').onclick = () => { S.skipped.push(q.id); S.hist.push(q.id); render(); };
  if ($('#back')) $('#back').onclick = back;
}

function whyAsked(q) {
  const { P, E } = evaluate();
  const hits = RACES.filter((r) => r.kind !== 'retention' && r.kind !== 'judge' && uncertainty(E[r.id]) > 0.3 && (r.weights || r.yes || {})[q.axes[0]]);
  if (!hits.length) return '';
  const names = hits.slice(0, 3).map((r) => r.short || r.title);
  return `This one sorts out ${names.join(', ')}${hits.length > 3 ? ` and ${hits.length - 3} more` : ''}.`;
}

function answer(q, optId) {
  const before = evaluate().E;
  S.skipped = S.skipped.filter((id) => id !== q.id);
  if (!S.answers[q.id]) S.order.push(q.id);
  S.hist = S.hist.filter((id) => id !== q.id).concat(q.id);
  S.answers[q.id] = { opt: optId, variant: S.variants[q.id] };
  const after = evaluate().E;
  const moved = RACES.filter((r) => pickLabel(before[r.id]) !== pickLabel(after[r.id]) && pickLabel(after[r.id]) !== '—');
  render();
  if (moved.length) toast(moved);
}

function back() {
  if (S.phase === 'done') S.phase = 'q';
  const lastQ = S.hist.pop();
  if (!lastQ) return render();
  S.order = S.order.filter((id) => id !== lastQ);
  S.skipped = S.skipped.filter((id) => id !== lastQ);
  delete S.answers[lastQ];
  S.lightningDone = false;
  render();
}

function renderLightning(list) {
  app.innerHTML = `
  <div class="progress"><span style="width:96%"></span></div>
  <div class="qmeta"><span>Lightning round</span><span>last step</span></div>
  <section class="qcard card-pop">
    <div class="qemoji" aria-hidden="true">⚡</div>
    <div class="kicker">Public questions</div>
    <h2>${esc(LIGHTNING_PROMPT)}</h2>
    <div class="lightning">
      ${list.map((r) => `<div class="lrow">
        <div class="ltext"><b>${esc(r.title)}</b><span>${esc(r.lightningAsk || r.wording)}</span></div>
        <div class="seg" role="group" aria-label="${esc(r.title)}">
          <button data-m="${r.id}" data-v="yes" class="${S.direct[r.id] === 'yes' ? 'on' : ''}">Yes</button>
          <button data-m="${r.id}" data-v="no" class="${S.direct[r.id] === 'no' ? 'on' : ''}">No</button>
          <button data-m="${r.id}" data-v="" class="${!S.direct[r.id] ? 'on' : ''}" title="Leave it to my answers">Unsure</button>
        </div></div>`).join('')}
    </div>
    <div class="qfoot"><button class="link" id="back">← Back</button><button class="btn btn-primary" id="ldone">See my ballot →</button></div>
  </section>`;
  app.querySelectorAll('.seg button').forEach((b) => b.onclick = () => {
    if (b.dataset.v) S.direct[b.dataset.m] = b.dataset.v; else delete S.direct[b.dataset.m];
    b.parentElement.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    save(); renderBallot();
  });
  $('#ldone').onclick = () => { S.lightningDone = true; render(); };
  $('#back').onclick = back;
}

// ---------------------------------------------------------------- the ballot panel
function groups() {
  const g = []; for (const r of RACES) { let x = g.find((y) => y.name === r.group); if (!x) g.push(x = { name: r.group, races: [] }); x.races.push(r); }
  return g;
}

function renderBallot() {
  const { E } = evaluate();
  const all = RACES.length; const done = RACES.filter((r) => E[r.id].decided).length;
  $('#ballotCount').textContent = `${done}/${all}`;
  ballotPane.innerHTML = `
  <div class="bp-head"><div><div class="kicker">Ballot so far</div><b>${done} of ${all} filled in</b></div>
    <button class="icon-btn bp-close" aria-label="Close" data-close>✕</button></div>
  <div class="bp-meter"><span style="width:${Math.round(100 * done / all)}%"></span></div>
  ${groups().map((g) => `<div class="bp-group"><div class="bp-gname">${esc(g.name)}</div>
    ${g.races.map((r) => { const ev = E[r.id]; const [cl, tone] = CONF_LABEL[ev.conf] || ['', 'mute'];
      return `<button class="bp-row" data-race="${r.id}">
        <span class="bp-office">${esc(r.short || r.title)}</span>
        <span class="bp-pick${pickLabel(ev) === '—' ? ' empty' : ''}">${esc(pickLabel(ev))}</span>
        <span class="chip ${tone}">${esc(cl)}</span></button>`; }).join('')}
  </div>`).join('')}`;
  ballotPane.querySelectorAll('[data-race]').forEach((b) => b.onclick = () => openRace(b.dataset.race));
  const c = ballotPane.querySelector('[data-close]'); if (c) c.onclick = closeBallotSheet;
}

function openBallotSheet() { document.body.classList.add('sheet-open'); ballotPane.focus(); }
function closeBallotSheet() { document.body.classList.remove('sheet-open'); }

// ---------------------------------------------------------------- race detail
const dlg = $('#race');
function openRace(id) {
  const r = RACE[id]; const { P, E } = evaluate(); const ev = E[id];
  const reasons = reasonsFor(ev, P);
  const [cl, tone] = CONF_LABEL[ev.conf] || ['', 'mute'];
  let body = '';
  if (r.kind === 'measure') body = measureBody(r, ev);
  else if (r.kind === 'retention' || r.kind === 'judge') body = judgesBody(r, ev, P);
  else body = candidatesBody(r, ev);
  dlg.innerHTML = `<div class="dlg-in">
    <div class="dlg-head"><div><div class="kicker">${esc(r.group)}</div><h3>${esc(r.title)}</h3>${r.es ? `<div class="es">${esc(r.es)}</div>` : ''}</div>
      <button class="icon-btn" data-x aria-label="Close">✕</button></div>
    ${r.context ? `<p class="ctx">${esc(r.context)}</p>` : ''}
    <div class="rec"><div class="rec-top"><span>Your ballot</span><span class="chip ${tone}">${esc(cl)}</span></div>
      <div class="rec-pick">${esc(pickLabel(ev))}</div>
      ${reasons.length ? `<ul class="reasons">${reasons.map((x) => `<li>${x}</li>`).join('')}</ul>` : ev.conf === 'nodata' ? '<p class="mute-t">Answer a few more questions and this fills in, or choose below.</p>' : ''}
      ${S.picks[id] ? '<button class="link" data-unlock>Undo my choice, let my answers decide</button>' : ''}
    </div>
    ${body}
  </div>`;
  dlg.querySelector('[data-x]').onclick = () => dlg.close();
  const ul = dlg.querySelector('[data-unlock]'); if (ul) ul.onclick = () => { delete S.picks[id]; render(); openRace(id); };
  dlg.querySelectorAll('[data-choose]').forEach((b) => b.onclick = () => choose(r, b.dataset.choose));
  dlg.querySelectorAll('[data-jv]').forEach((b) => b.onclick = () => {
    const [jid, v] = b.dataset.jv.split('|');
    if (v === 'auto') delete S.judgePicks[jid]; else S.judgePicks[jid] = v;
    render(); openRace(id);
  });
  dlg.querySelectorAll('[data-filter]').forEach((b) => b.onclick = () => {
    dlg.querySelectorAll('[data-filter]').forEach((x) => x.classList.toggle('on', x === b));
    dlg.querySelectorAll('.judge').forEach((el) => { el.hidden = b.dataset.filter === 'flag' && !el.classList.contains('flagged'); });
  });
  if (!dlg.open) dlg.showModal();
  dlg.scrollTop = 0;
}

function choose(r, val) {
  if (r.kind === 'measure') { S.picks[r.id] = val; }
  else if ((r.voteFor || 1) > 1) {
    const { E } = evaluate(); let cur = S.picks[r.id] || E[r.id].picks.slice();
    cur = cur.includes(val) ? cur.filter((x) => x !== val) : [...cur, val].slice(-(r.voteFor));
    S.picks[r.id] = cur;
  } else S.picks[r.id] = val;
  render(); openRace(r.id);
}

function srcList(sources) {
  if (!sources || !sources.length) return '';
  return `<div class="srcs"><span>Sources</span>${sources.map((s, i) => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${i + 1}. ${esc(s.title || hostOf(s.url))}</a>`).join('')}</div>`;
}
function hostOf(u) { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return u; } }

function candidatesBody(r, ev) {
  const rows = ev.scored.slice().sort((a, b) => (b.max ? b.s : -9) - (a.max ? a.s : -9) || a.c.ballot - b.c.ballot);
  return `<div class="cands">${rows.map((x) => { const c = x.c; const on = ev.picks.includes(c.id);
    return `<details class="cand${on ? ' on' : ''}"${on && r.candidates.length < 4 ? ' open' : ''}>
      <summary>
        <span class="num">${c.ballot}</span>
        <span class="cname"><b>${esc(c.name)}</b>${c.runningMate ? `<i>& ${esc(c.runningMate)}</i>` : ''}<em>${esc(c.partyName || '')}${c.incumbent ? ' · incumbent' : ''}</em></span>
        <span class="match">${x.pct == null ? '' : `<b>${x.pct}%</b><span>match</span>`}</span>
      </summary>
      <div class="cbody">
        ${c.bio ? `<p>${esc(c.bio)}</p>` : ''}
        ${c.quals ? `<h4>Qualifications</h4><p>${esc(c.quals)}</p>` : ''}
        ${c.positions && Object.keys(c.positions).length ? `<h4>Positions</h4><dl>${Object.entries(c.positions).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>` : ''}
        ${c.endorse && c.endorse.length ? `<h4>Endorsements</h4><p>${c.endorse.map(esc).join(' · ')}</p>` : ''}
        ${c.gaps && c.gaps.length ? `<h4>Gaps & concerns</h4><ul class="gaps">${c.gaps.map((g) => `<li>${esc(g)}</li>`).join('')}</ul>` : ''}
        ${x.parts.length ? `<h4>How you line up</h4><ul class="align">${x.parts.filter((p) => p.ax !== 'party').map((p) => `<li class="${p.sim > 0.25 ? 'agree' : p.sim < -0.25 ? 'disagree' : 'meh'}"><b>${esc(axisName(p.ax))}</b> ${esc(p.why || '')}</li>`).join('')}</ul>` : ''}
        ${srcList(c.sources)}
        <button class="btn ${on ? 'btn-ghost' : 'btn-primary'} btn-sm" data-choose="${c.id}">${on ? ((r.voteFor || 1) > 1 ? 'Remove from my three' : 'This is my pick') : ((r.voteFor || 1) > 1 ? 'Add to my three' : 'Vote for this candidate instead')}</button>
      </div></details>`; }).join('')}</div>
    ${r.writeIn ? '<p class="mute-t">This race also has a write-in line.</p>' : ''}`;
}

function measureBody(r, ev) {
  return `<div class="measure">
    <blockquote>${esc(r.wording)}</blockquote>
    <div class="mfacts"><span class="chip mute">${r.binding ? 'Binding' : 'Advisory, not binding'}</span>${r.jurisdiction ? `<span class="chip mute">${esc(r.jurisdiction)}</span>` : ''}</div>
    ${r.sponsor ? `<p><b>Who put it here:</b> ${esc(r.sponsor)}</p>` : ''}
    <div class="yn"><div><h4>A Yes vote</h4><p>${esc(r.yesMeans)}</p></div><div><h4>A No vote</h4><p>${esc(r.noMeans)}</p></div></div>
    ${r.facts && r.facts.length ? `<h4>Facts</h4><ul>${r.facts.map((f) => `<li>${esc(f)}</li>`).join('')}</ul>` : ''}
    <div class="yn"><div><h4>For</h4><ul>${(r.for || []).map((f) => `<li>${esc(f)}</li>`).join('')}</ul></div><div><h4>Against</h4><ul>${(r.against || []).map((f) => `<li>${esc(f)}</li>`).join('')}</ul></div></div>
    ${srcList(r.sources)}
    <div class="seg big">${['yes', 'no', 'blank'].map((v) => `<button data-choose="${v}" class="${ev.pick === v ? 'on' : ''}">${v === 'blank' ? 'Leave blank' : v === 'yes' ? 'Yes' : 'No'}</button>`).join('')}</div>
  </div>`;
}

function judgesBody(r, ev, P) {
  const flagged = ev.votes.filter((v) => v.j.flag === 'concern' || v.j.flag === 'caution').length;
  const pol = P.policy ? `Your rule: <b>${esc(P.src.policy.short)}</b>.` : 'Answer the judges question, or set each judge by hand.';
  return `${r.note ? `<p class="ctx">${esc(r.note)}</p>` : ''}
  <p class="ctx">${pol} ${flagged ? `${flagged} ${flagged === 1 ? 'judge has' : 'judges have'} a flag.` : ''}</p>
  ${r.kind === 'retention' ? `<div class="seg filt"><button data-filter="all" class="on">All ${ev.votes.length}</button><button data-filter="flag">Flagged only (${flagged})</button></div>` : ''}
  <div class="judges">${ev.votes.map(({ j, vote, locked }) => `
    <details class="judge${j.flag === 'concern' || j.flag === 'caution' ? ' flagged' : ''}">
      <summary>
        <span class="num">${j.yes || j.ballot}</span>
        <span class="cname"><b>${esc(j.name)}</b><em>${esc(j.seat || j.assignment || '')}</em></span>
        <span class="jv ${vote || 'none'}">${vote ? (vote === 'yes' ? 'Yes' : vote === 'no' ? 'No' : 'Blank') : '—'}${locked ? ' ✎' : ''}</span>
      </summary>
      <div class="cbody">
        <p class="flagline flag-${esc(j.flag)}">${esc(FLAG[j.flag] || j.flag)}${j.why ? ` · ${esc(j.why)}` : ''}</p>
        ${j.bio ? `<p>${esc(j.bio)}</p>` : ''}
        ${j.ratings ? `<dl>${Object.entries(j.ratings).filter(([, v]) => v).map(([k, v]) => `<dt>${esc(BAR[k] || k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>` : ''}
        ${srcList(j.sources)}
        <div class="seg">${(r.kind === 'judge' ? ['yes', 'blank', 'auto'] : ['yes', 'no', 'blank', 'auto']).map((v) => `<button data-jv="${j.id}|${v}" class="${(v === 'auto' && !locked) || (locked && vote === v) ? 'on' : ''}">${v === 'auto' ? 'Use my rule' : v === 'blank' ? 'Blank' : v[0].toUpperCase() + v.slice(1)}</button>`).join('')}</div>
      </div></details>`).join('')}</div>`;
}
const FLAG = { concern: '⚠ Flagged', caution: '◐ Mixed ratings', clean: '✓ Rated qualified', unknown: '? No ratings found' };
const BAR = { cba: 'Chicago Bar Association', ccl: 'Chicago Council of Lawyers', isba: 'Illinois State Bar Association', alliance: 'Alliance of Bar Associations', other: 'Other', iw: 'Injustice Watch' };

// ---------------------------------------------------------------- results
function archetype(P) {
  const u = P.u; const e = u.econ ?? 0, s = u.safety ?? 0, ch = u.change ?? 0, f = u.federal ?? 0;
  if (e <= -0.8 && ch >= 0.8) return ['🔥', 'The Reform Insurgent', 'Progressive on the money and impatient with the old guard. You want the system shaken, not just steered.'];
  if (e <= -0.8 && s >= 0.8) return ['🧱', 'The Pragmatic Progressive', 'Tax the top and fund the basics, but you want the streets safe now, not after the next study.'];
  if (e <= -0.8) return ['🌊', 'The Lakefront Progressive', 'Public money for public goods, a Chicago that stands up to Washington, and rights written into law.'];
  if (e >= 0.8 && ch >= 0.8) return ['🧨', 'The Outsider Fiscal Hawk', 'Lower taxes, fewer insiders, and someone finally reading the bills before they pass.'];
  if (e >= 0.8 || (s >= 1 && f >= 1)) return ['🏡', 'The Bungalow Belt Conservative', 'Taxes down, police up, and a government that sticks to the basics and does them well.'];
  if (ch >= 0.8) return ['🦟', 'The Independent Gadfly', 'No party owns you. You vote the person, and you like a little disruption.'];
  if (ch <= -0.8) return ['⚓', 'The Steady Hand', 'Experience matters, and so do good results. You’d rather fix the machine than smash it.'];
  return ['⚖️', 'The Split-Ticket Pragmatist', 'Somewhere in the middle on purpose. You weigh each race on its own.'];
}

function renderDone() {
  const { P, E } = evaluate();
  const [emo, name, line] = archetype(P);
  const more = QUESTIONS.filter((q) => !S.answers[q.id] && !S.skipped.includes(q.id));
  const undecided = RACES.filter((r) => !E[r.id].decided);
  app.innerHTML = `
  <section class="done card-pop">
    <div class="arch"><span class="arch-emo">${emo}</span><div><div class="kicker">Your civic type</div><h2>${esc(name)}</h2><p>${esc(line)}</p></div></div>
    <div class="cta-row">
      <button class="btn btn-primary" id="print">Print my cheat sheet</button>
      <button class="btn btn-ghost" id="share">Copy a link to my answers</button>
      ${more.length ? `<button class="btn btn-ghost" id="more">Sharpen it (${more.length} more question${more.length > 1 ? 's' : ''})</button>` : ''}
      <button class="btn btn-ghost" id="again">Start over</button>
    </div>
    ${undecided.length ? `<p class="fine">${undecided.length} race${undecided.length > 1 ? 's are' : ' is'} still open. Tap ${undecided.length > 1 ? 'them' : 'it'} below to choose.</p>` : ''}
    <p class="fine">You can bring this sheet into the booth. Illinois lets you take notes in with you. Tap any race to see every candidate, the sources, and why it landed where it did.</p>
  </section>
  <section class="sheet" id="sheet">
    <div class="sheet-head"><b>My ballot · ${esc(ELECTION.precinct)}</b><span>${esc(ELECTION.dateLabel)} · ${esc(ELECTION.ballotStyle)}</span></div>
    ${groups().map((g) => `<div class="sg"><h3>${esc(g.name)}</h3>${g.races.map((r) => sheetRow(r, E[r.id], P)).join('')}</div>`).join('')}
    <p class="fine">Made with Chicago Voter · Ballot Match. Numbers are the ballot line numbers printed next to each oval.</p>
  </section>`;
  $('#print').onclick = () => window.print();
  $('#share').onclick = share;
  $('#again').onclick = () => { if (confirm('Clear your answers and start over?')) { S = fresh(); render(); } };
  if ($('#more')) $('#more').onclick = () => { S.skipped = []; S.sharpen = true; S.phase = 'q'; render(); };
  app.querySelectorAll('[data-race]').forEach((b) => b.onclick = () => openRace(b.dataset.race));
}

function sheetRow(r, ev, P) {
  if (r.kind === 'retention') {
    return `<div class="srow judgesrow" data-race="${r.id}"><div class="soff">${esc(r.title)}</div>
      <div class="jgrid">${ev.votes.map(({ j, vote }) => `<span class="jcell ${vote || 'none'}${j.flag === 'concern' ? ' fl' : ''}"><i>${vote === 'yes' ? j.yes : vote === 'no' ? j.no : '–'}</i>${esc(j.name)}<b>${vote === 'yes' ? 'Yes' : vote === 'no' ? 'No' : '—'}</b></span>`).join('')}</div></div>`;
  }
  if (r.kind === 'judge') {
    return ev.votes.map(({ j, vote }) => `<div class="srow" data-race="${r.id}"><div class="soff">${esc(j.seat || r.title)}</div>
      <div class="spick">${vote === 'yes' ? `<span class="oval">${j.ballot}</span>${esc(j.name)}` : '<span class="mute-t">Leave blank</span>'}</div></div>`).join('');
  }
  if (r.kind === 'measure') {
    return `<div class="srow" data-race="${r.id}"><div class="soff">${esc(r.title)}</div>
      <div class="spick">${ev.pick === 'yes' || ev.pick === 'no' ? `<span class="oval">${ev.pick === 'yes' ? 'Yes' : 'No'}</span>` : '<span class="mute-t">Blank</span>'}</div></div>`;
  }
  const picks = ev.picks.map((id) => r.candidates.find((c) => c.id === id));
  return `<div class="srow" data-race="${r.id}"><div class="soff">${esc(r.short || r.title)}${(r.voteFor || 1) > 1 ? ` <em>(vote for ${r.voteFor})</em>` : ''}</div>
    <div class="spick">${picks.length ? picks.map((c) => `<span class="oval">${c.ballot}</span>${esc(c.name)}${c.runningMate ? ` & ${esc(c.runningMate)}` : ''}`).join('<br>') : '<span class="mute-t">Blank</span>'}</div></div>`;
}

function share() {
  const a = S.order.map((id) => `${id}.${S.answers[id].opt}`).join(',');
  const d = Object.entries(S.direct).map(([k, v]) => `${k}.${v[0]}`).join(',');
  const url = `${location.origin}${location.pathname}#a=${a}${d ? `&d=${d}` : ''}`;
  const done = () => toastText('Link copied. It carries your answers, not your name.');
  if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, () => prompt('Copy this link:', url));
  else prompt('Copy this link:', url);
}

function fromHash() {
  const h = new URLSearchParams(location.hash.slice(1)); const a = h.get('a'); if (!a) return;
  const st = fresh();
  for (const pair of a.split(',')) { const [id, opt] = pair.split('.'); if (Q[id] && Q[id].options.some((o) => o.id === opt)) { st.order.push(id); st.answers[id] = { opt }; } }
  for (const pair of (h.get('d') || '').split(',').filter(Boolean)) { const [id, v] = pair.split('.'); if (RACE[id]) st.direct[id] = v === 'y' ? 'yes' : 'no'; }
  if (!st.order.length) return;
  st.hist = st.order.slice(); st.phase = 'done'; st.lightningDone = true; S = st;
  history.replaceState(null, '', location.pathname);
}

// ---------------------------------------------------------------- toasts
let toastTimer;
function toast(moved) {
  const items = moved.slice(0, 3).map((r) => `<li><span>${esc(r.short || r.title)}</span> → <b>${esc(pickLabel(evaluate().E[r.id]))}</b></li>`).join('');
  showToast(`<div class="t-k">Your ballot moved</div><ul>${items}</ul>${moved.length > 3 ? `<div class="t-more">+${moved.length - 3} more</div>` : ''}`);
  $('#ballotBtn').classList.remove('pulse'); void $('#ballotBtn').offsetWidth; $('#ballotBtn').classList.add('pulse');
}
function toastText(t) { showToast(esc(t)); }
function showToast(html) {
  const el = $('#toast'); el.innerHTML = html; el.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 3200);
}

// ---------------------------------------------------------------- chrome
function initTheme() {
  let t = null; try { t = localStorage.getItem(THEME_KEY); } catch (e) { /* */ }
  if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.dataset.theme = t;
  const b = $('#themeToggle'); b.textContent = t === 'dark' ? '☀️' : '🌙';
  b.onclick = () => {
    const n = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = n; b.textContent = n === 'dark' ? '☀️' : '🌙';
    try { localStorage.setItem(THEME_KEY, n); } catch (e) { /* */ }
  };
}

$('#ballotBtn').onclick = () => (document.body.classList.contains('sheet-open') ? closeBallotSheet() : openBallotSheet());
$('#scrim').onclick = closeBallotSheet;
$('#homeLink').onclick = (e) => { e.preventDefault(); S.phase = 'intro'; render(); };
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeBallotSheet();
  if (S.phase === 'q' && !dlg.open && /^[a-d1-4]$/i.test(e.key) && !e.metaKey && !e.ctrlKey) {
    const i = 'abcd1234'.indexOf(e.key.toLowerCase()) % 4; const b = app.querySelectorAll('.opt')[i]; if (b) b.click();
  }
});
dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });

initTheme();
fromHash();
render();

// exposed for the smoke test
window.__voter = { evaluate, nextStep, RACES, QUESTIONS, get state() { return S; } };
