// Chicago Voter — Ballot Match. A short, adaptive scenario survey that fills in
// every race on the ballot (Ward 30 · Precinct 04 · ballot style 124) and says
// why. All the research lives in data.js (generated from cited research); the
// survey lives in questions.js. No build step, no network calls, and nothing
// leaves the browser.
//
// The matching borrows AutoSelector's Mind Reader: each answer quietly nudges
// every candidate's affinity, and a report after every answer says exactly
// what moved and why. The oval field (one oval per mark on the ballot) is its
// whittle-dot field turned into a ballot that fills itself in.

import { ELECTION, AXES, RACES } from './data.js';
import { QUESTIONS, LIGHTNING_PROMPT } from './questions.js';

const KEY = 'chivoter.v1';
const THEME_KEY = 'chivoter.theme';
const MIN_AXIS_Q = 5;          // ask at least this many scenario questions
const STOP_VALUE = 0.55;       // then stop once no question could move more than this
const JUDGES_AT = 4;           // the judges question arrives as the 5th card

// the 'L' line color for each section of the ballot
const LINE = {
  'Federal & statewide': 'var(--red)', 'Congress & Springfield': 'var(--purple)', 'Water Reclamation District': 'var(--blue)',
  'Cook County': 'var(--brown)', 'Judges: open seats': 'var(--orange)', 'Board of Education': 'var(--green)',
  'Public questions': 'var(--pink)', 'Judges: retention': 'var(--yellow)',
};
const LINE_NAME = {
  'Federal & statewide': 'Red Line', 'Congress & Springfield': 'Purple Line', 'Water Reclamation District': 'Blue Line',
  'Cook County': 'Brown Line', 'Judges: open seats': 'Orange Line', 'Board of Education': 'Green Line',
  'Public questions': 'Pink Line', 'Judges: retention': 'Yellow Line',
};
// each survey topic rides the line of the section it moves most
const Q_LINE = { econ: 'var(--red)', safety: 'var(--brown)', federal: 'var(--purple)', social: 'var(--red)', change: 'var(--brown)',
  taxfair: 'var(--brown)', green: 'var(--blue)', union: 'var(--green)', judges: 'var(--yellow)', label: 'var(--orange)' };

const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const STAR = '<svg aria-hidden="true"><use href="#star"/></svg>';
const Q = Object.fromEntries(QUESTIONS.map((q) => [q.id, q]));
const RACE = Object.fromEntries(RACES.map((r) => [r.id, r]));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------------------------------------------------------------- state
function fresh() {
  return { v: 1, phase: 'intro', answers: {}, order: [], skipped: [], hist: [], variants: {}, shuffles: {},
    picks: {}, judgePicks: {}, direct: {}, lightningDone: false, sharpen: false, report: null };
}
let S = load();
function load() {
  try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && s.v === 1) return Object.assign(fresh(), s); } catch (e) { /* private mode */ }
  return fresh();
}
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* ignore */ } }

// ---------------------------------------------------------------- profile
// The voter's spot on each axis is the weighted mean of what their answers set;
// `conf` is how much weight sits behind it (1 = one full answer).
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
      if (w >= 0.99 || !src[ax]) src[ax] = { q: qid, short: opt.short };
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
  if (race.partyWeight && P.partyAnswered) {
    const pk = partyKey(c.party); const pv = pk ? (P.party[pk] || 0) : 0;
    s += race.partyWeight * pv; max += race.partyWeight;
    if (pv) parts.push({ ax: 'party', k: race.partyWeight, sim: pv, why: c.partyName ? `the ${c.partyName} candidate` : '' });
  }
  if (c.withdrawn) s -= 99;   // still printed on the ballot, never recommended
  const pct = max ? Math.round(clamp(50 + 50 * Math.max(s, -max) / max, 0, 100)) : null;
  return { c, s, max, pct: c.withdrawn ? null : pct, parts };
}

function judgeVote(j, policy) {
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
    const decided = votes.every((v) => v.vote);
    return { race, votes, conf: votes.some((v) => v.vote) ? 'policy' : 'nodata', decided };
  }
  if (race.kind === 'measure') {
    const yes = { axes: race.yes || {} };
    const no = { axes: Object.fromEntries(Object.entries(race.yes || {}).map(([k, v]) => [k, { v: -v.v, why: v.why }])) };
    const rr = { weights: race.weights || Object.fromEntries(Object.keys(race.yes || {}).map((k) => [k, 1])) };
    const sy = scoreCand(yes, rr, P), sn = scoreCand(no, rr, P);
    const direct = st.direct[race.id]; const lock = st.picks[race.id];
    let pick = null, conf = 'nodata', lean = 0;
    if (sy.max && !race.lightning) {
      lean = (sy.s - sn.s) / (2 * sy.max);
      pick = lean > 0.02 ? 'yes' : lean < -0.02 ? 'no' : null;
      conf = Math.abs(lean) >= 0.45 ? 'strong' : Math.abs(lean) >= 0.2 ? 'lean' : 'close';
    }
    if (direct) { pick = direct; conf = 'direct'; }
    if (lock) { pick = lock; conf = 'locked'; }
    return { race, pick, conf, lean, parts: lean >= 0 ? sy.parts : sn.parts, decided: !!pick };
  }
  // candidate race
  const scored = race.candidates.map((c) => scoreCand(c, race, P)).sort((a, b) => b.s - a.s || (a.c.ballot - b.c.ballot));
  const n = race.voteFor || 1;
  const live = race.candidates.filter((c) => !c.withdrawn);
  const lock = st.picks[race.id];
  let picks, conf;
  const any = scored.some((x) => x.max > 0);
  if (live.length === 1 && race.candidates.length === 1) {
    const x = scored[0]; picks = [x.c.id]; conf = 'unopposed';
    if (x.max > 0 && x.pct < 35) { picks = []; conf = 'unopposed-blank'; }
  } else if (!any) {
    picks = []; conf = 'nodata';
  } else {
    picks = scored.slice(0, n).filter((x) => !x.c.withdrawn).map((x) => x.c.id);
    const cut = scored[n - 1], next = scored[n];
    const margin = next && !next.c.withdrawn ? (cut.s - next.s) / Math.max(cut.max, 0.0001) : 1;
    conf = margin >= 0.5 ? 'strong' : margin >= 0.18 ? 'lean' : 'close';
  }
  if (lock) { picks = Array.isArray(lock) ? lock : [lock]; conf = 'locked'; }
  return { race, scored, picks, conf, decided: picks.length > 0 || conf === 'unopposed-blank' };
}

function evaluate(st = S) {
  const P = profile(st);
  const E = {}; for (const r of RACES) E[r.id] = evalRace(r, P, st);
  return { P, E };
}

function uncertainty(ev) {
  return { nodata: 1, close: 0.8, lean: 0.45, strong: 0.12 }[ev.conf] || 0;
}

// How much could asking q still change the ballot?
function questionValue(q, P, E) {
  if (q.kind) return 0;
  let v = 0;
  for (const r of RACES) {
    if (r.kind === 'retention' || r.kind === 'judge' || r.lightning) continue;
    const unc = uncertainty(E[r.id]); if (!unc) continue;
    for (const ax of q.axes) {
      const w = r.kind === 'measure' ? (r.yes && r.yes[ax] ? 1 : 0) : (r.weights || {})[ax];
      if (!w) continue;
      let spread;
      if (r.kind === 'measure') spread = Math.abs(r.yes[ax].v) / 2;
      else {
        const vals = r.candidates.filter((c) => !c.withdrawn).map((c) => c.axes && c.axes[ax] && c.axes[ax].v).filter((x) => x != null);
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

// The next card, or null when the survey is done.
function nextStep(st = S) {
  const { P, E } = evaluate(st);
  const asked = new Set([...st.order, ...st.skipped]);
  const axisAsked = [...asked].filter((id) => Q[id] && !Q[id].kind).length;
  if (!asked.has('judges') && asked.size >= JUDGES_AT) return { q: Q.judges };
  const cands = QUESTIONS.filter((q) => !q.kind && !asked.has(q.id))
    .map((q) => ({ q, v: questionValue(q, P, E) })).sort((a, b) => b.v - a.v);
  if (cands.length && (st.sharpen || axisAsked < MIN_AXIS_Q || cands[0].v >= STOP_VALUE)) return { q: cands[0].q, value: cands[0].v };
  if (!asked.has('judges')) return { q: Q.judges };
  if (!asked.has('label') && partisanUnsettled(E)) return { q: Q.label };
  if (!st.lightningDone && lightningNeeded(E).length) return { lightning: true };
  return null;
}

// a dry run: how many more cards if every answer came from the middle
function remainingEstimate() {
  const sim = JSON.parse(JSON.stringify(S)); let n = 0;
  for (let i = 0; i < 20; i++) {
    const st = nextStep(sim); if (!st) break; n++;
    if (st.lightning) break;
    sim.order.push(st.q.id); sim.answers[st.q.id] = { opt: st.q.options[1].id };
  }
  return n;
}

// ---------------------------------------------------------------- explanations
const axisName = (ax) => (AXES[ax] && AXES[ax].name) || ax;

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
  if (ev.conf === 'unopposed') return ['Unopposed. Your vote is a formality, and you can leave it blank.'];
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
  if (r.kind === 'measure') return ev.pick ? ({ yes: 'Yes', no: 'No', blank: 'Leave blank' }[ev.pick]) : '—';
  if (r.kind === 'retention' || r.kind === 'judge') {
    if (!ev.votes.some((v) => v.vote)) return '—';
    if (ev.votes.length === 1) return { yes: r.kind === 'judge' ? ev.votes[0].j.name : 'Yes', no: 'No', blank: 'Leave blank' }[ev.votes[0].vote];
    const y = ev.votes.filter((v) => v.vote === 'yes').length, n = ev.votes.filter((v) => v.vote === 'no').length;
    const b = ev.votes.length - y - n;
    if (r.kind === 'judge') return y === ev.votes.length ? `Vote all ${y}` : y ? `Vote ${y} · ${b} blank` : 'Leave all blank';
    return [y && `Yes on ${y}`, n && `No on ${n}`, b && `${b} blank`].filter(Boolean).join(' · ');
  }
  if (ev.conf === 'unopposed-blank') return 'Leave blank';
  if (!ev.picks.length) return '—';
  return ev.picks.map((id) => r.candidates.find((c) => c.id === id)).map((c) => c.short || c.name).join(', ');
}

// every oval on the ballot, in order: { line, on, no }
function ovals(E) {
  const out = [];
  for (const r of RACES) {
    const ev = E[r.id]; const line = LINE[r.group];
    if (r.kind === 'retention' || r.kind === 'judge') ev.votes.forEach((v, i) => out.push({ key: `${r.id}:${i}`, line, on: v.vote === 'yes', no: v.vote === 'no' }));
    else if (r.kind === 'measure') out.push({ key: r.id, line, on: !!ev.pick && ev.pick !== 'blank' });
    else for (let i = 0; i < (r.voteFor || 1); i++) out.push({ key: `${r.id}:${i}`, line, on: i < ev.picks.length });
  }
  return out;
}

// ---------------------------------------------------------------- rendering
const app = $('#app');
const ballotPane = $('#ballot');
let lastFilled = null;   // oval keys filled at the last render, to pop the new ones

function render(opts = {}) {
  document.body.dataset.phase = S.phase;
  if (S.phase === 'intro') renderIntro();
  else if (S.phase === 'q') renderStep();
  else renderDone(opts.celebrate);
  renderBallot(opts.flash || []);
  save();
}

function ovalField(E, cls = '') {
  const list = ovals(E);
  const html = list.map((o) => `<i style="--line:${o.line}" class="${o.on ? 'on' : o.no ? 'no' : ''}${lastFilled && (o.on || o.no) && !lastFilled.has(o.key) ? ' pop' : ''}"></i>`).join('');
  return `<div class="ovalfield ${cls}" aria-hidden="true">${html}</div>`;
}

function renderIntro() {
  const resumable = S.order.length > 0;
  const nRaces = RACES.filter((r) => r.kind === 'pick').length;
  const nJudges = RACES.filter((r) => r.kind === 'retention' || r.kind === 'judge').reduce((a, r) => a + (r.judges || r.candidates).length, 0);
  const nMeasures = RACES.filter((r) => r.kind === 'measure').length;
  const groupsList = [...new Set(RACES.map((r) => r.group))];
  app.innerHTML = `
  <section class="intro card-pop">
    <div class="kicker">${esc(ELECTION.dateLabel)} · ${esc(ELECTION.precinct)}</div>
    <h1>Your ballot,<br>matched <span class="star-inline">${STAR}</span></h1>
    <p class="lead">About ten quick scenarios, and your whole ballot fills itself in as you answer: U.S. Senate down to the water district,
    Chicago’s first elected school board president, the public questions and every judge. Each pick shows you which answer put it there.</p>
    <div class="intro-facts">
      <div style="--line:var(--red)"><b>${nRaces}</b><span>races</span></div>
      <div style="--line:var(--pink)"><b>${nMeasures}</b><span>public questions</span></div>
      <div style="--line:var(--yellow)"><b>${nJudges}</b><span>judges</span></div>
      <div style="--line:var(--blue)"><b>~10</b><span>questions, 4 min</span></div>
    </div>
    <div class="lines">${groupsList.map((g) => `<span style="--line:${LINE[g]}">${esc(g)}</span>`).join('')}</div>
    <div class="cta-row">
      <button class="btn btn-primary btn-lg" id="start">${resumable ? 'Pick up where you left off →' : 'All aboard →'}</button>
      ${resumable ? '<button class="btn btn-ghost" id="restart">Start over</button>' : ''}
      <button class="btn btn-ghost" id="browse">Just browse the ballot</button>
    </div>
    <p class="fine">${esc(ELECTION.ballotStyle)} · ${esc(ELECTION.districts)}. Every profile is researched and cited, current as of ${esc(ELECTION.asOf)}.
    The picks mirror your own answers; they aren’t an endorsement. Nothing you answer leaves this browser.</p>
  </section>`;
  $('#start').onclick = () => { S.phase = 'q'; render(); };
  if ($('#restart')) $('#restart').onclick = () => { S = fresh(); S.phase = 'q'; render(); };
  $('#browse').onclick = () => openBallotSheet();
}

function chooseVariant(q) {
  if (S.variants[q.id] == null) S.variants[q.id] = Math.floor(Math.random() * q.variants.length);
  if (!S.shuffles[q.id]) {
    const ids = q.options.map((o) => o.id);
    // a scale reads best in order, so it runs one way or the other, never scrambled
    S.shuffles[q.id] = q.kind ? ids : (Math.random() < 0.5 ? ids : ids.slice().reverse());
  }
  return q.variants[S.variants[q.id]];
}

function track(n, left) {
  const total = Math.max(n + left - 1, 1);
  const stops = Array.from({ length: total + 1 }, (_, i) => i);
  const at = (i) => `calc(6px + (100% - 12px) * ${i / total})`;
  return `<div class="track" aria-hidden="true">
    <div class="rail"></div><div class="rail-done" style="width:calc((100% - 12px) * ${(n - 1) / total})"></div>
    ${stops.map((i) => `<span class="stop${i < n ? ' done' : ''}" style="left:${at(i)}"></span>`).join('')}
    <span class="train" style="left:${at(n - 1)}"><svg><use href="#train"/></svg></span>
  </div>`;
}

function reportCard() {
  const rp = S.report; if (!rp || !rp.moved.length) return '';
  const q = Q[rp.q]; const opt = q && q.options.find((o) => o.id === rp.opt);
  return `<div class="report">
    <button class="rp-head" aria-expanded="false" id="rpHead">
      <span class="rp-n">${rp.moved.length}</span>
      <span class="rp-t">${rp.moved.length === 1 ? 'race moved' : 'races moved'} on your ballot</span>
      <span class="rp-why">Why? ▾</span>
    </button>
    <div class="rp-detail" hidden>
      ${opt ? `<p>You picked <b>${esc(opt.short)}</b>. That moved:</p>` : ''}
      <ul>${rp.moved.slice(0, 8).map((m) => `<li style="--line:${LINE[RACE[m.id].group]}"><i></i><span><b>${esc(RACE[m.id].short || RACE[m.id].title)}</b>: ${m.from !== '—' ? `<span class="from">${esc(m.from)}</span> → ` : ''}${esc(m.to)}</span></li>`).join('')}</ul>
      ${rp.moved.length > 8 ? `<p>…and ${rp.moved.length - 8} more. Open “Ballot so far” to see them all.</p>` : ''}
    </div>
  </div>`;
}

function renderStep() {
  const st = nextStep();
  if (!st) { S.phase = 'done'; return render({ celebrate: true }); }
  if (st.lightning) return renderLightning(lightningNeeded(evaluate().E));
  const q = st.q; const v = chooseVariant(q);
  const n = S.hist.length + 1;
  const left = remainingEstimate();
  const opts = S.shuffles[q.id].map((id) => q.options.find((o) => o.id === id));
  const prev = S.answers[q.id];
  const { E } = evaluate();
  const line = Q_LINE[q.id] || 'var(--red)';
  const axisDone = S.hist.filter((id) => !Q[id].kind).length;
  app.innerHTML = `
  ${track(n, left)}
  <div class="qmeta"><span>Stop ${n}</span><span>${left <= 1 ? 'last stop' : `about ${left - 1} more stop${left - 1 > 1 ? 's' : ''}`}</span></div>
  ${ovalField(E, 'mini')}
  ${reportCard()}
  <section class="qcard card-pop" aria-live="polite" style="--line:${line}">
    <div class="qsign"><span class="bullet">${q.emoji}</span><span class="stn"><small>Now arriving</small>${esc(q.topic)}</span><span class="qn">${n}</span></div>
    <div class="qbar"></div>
    <div class="qbody">
      <h2>${esc(v.title)}</h2>
      <p class="scenario">${esc(v.scenario)}</p>
      <div class="opts" role="list">
        ${opts.map((o, i) => `<button class="opt${prev && prev.opt === o.id ? ' sel' : ''}" data-opt="${o.id}" role="listitem">
          <span class="opt-key">${'ABCD'[i]}</span><span class="opt-text">${esc((v.labels && v.labels[o.id]) || o.label)}</span></button>`).join('')}
      </div>
      <div class="qfoot">
        <div class="grp">
          ${S.hist.length ? '<button class="link" id="back">↶ Undo last</button>' : ''}
          ${q.variants.length > 1 ? '<button class="link" id="swap">↻ Ask it another way</button>' : ''}
        </div>
        <div class="grp">
          <button class="link" id="skip">Skip</button>
          ${axisDone >= 3 ? '<button class="link" id="reveal">Show my ballot now →</button>' : ''}
        </div>
      </div>
    </div>
  </section>
  <p class="why-asked">${q.kind === 'judges' ? 'Asked because it decides every judge on the back of the ballot.' : q.kind === 'party' ? 'Asked because a few partisan races are still close on the issues.' : esc(whyAsked(q, E))}</p>`;
  app.querySelectorAll('.opt').forEach((b) => b.onclick = (e) => answer(q, b.dataset.opt, b, e));
  $('#skip').onclick = () => { S.skipped.push(q.id); S.hist.push(q.id); S.report = null; leave(() => render()); };
  if ($('#back')) $('#back').onclick = back;
  if ($('#swap')) $('#swap').onclick = () => { S.variants[q.id] = (S.variants[q.id] + 1) % q.variants.length; delete S.shuffles[q.id]; render(); };
  if ($('#reveal')) $('#reveal').onclick = () => { S.lightningDone = true; S.phase = 'done'; render({ celebrate: true }); };
  if (window.scrollY > 60) window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  const rh = $('#rpHead'); if (rh) rh.onclick = () => { const d = rh.nextElementSibling; d.hidden = !d.hidden; rh.setAttribute('aria-expanded', String(!d.hidden)); };
}

function whyAsked(q, E) {
  const hits = RACES.filter((r) => r.kind !== 'retention' && r.kind !== 'judge' && uncertainty(E[r.id]) > 0.3 &&
    (r.kind === 'measure' ? r.yes && r.yes[q.axes[0]] : (r.weights || {})[q.axes[0]]));
  if (!hits.length) return '';
  const names = hits.slice(0, 3).map((r) => r.short || r.title);
  return `This one sorts out ${names.join(', ')}${hits.length > 3 ? ` and ${hits.length - 3} more` : ''}.`;
}

function leave(then) {
  const card = app.querySelector('.qcard');
  if (!card || reduced) return then();
  card.classList.add('leaving'); setTimeout(then, 260);
}

function answer(q, optId, btn, e) {
  const before = evaluate().E;
  S.skipped = S.skipped.filter((id) => id !== q.id);
  if (!S.answers[q.id]) S.order.push(q.id);
  S.hist = S.hist.filter((id) => id !== q.id).concat(q.id);
  S.answers[q.id] = { opt: optId, variant: S.variants[q.id] };
  const after = evaluate().E;
  const moved = RACES.filter((r) => pickLabel(before[r.id]) !== pickLabel(after[r.id]) && pickLabel(after[r.id]) !== '—')
    .map((r) => ({ id: r.id, from: pickLabel(before[r.id]), to: pickLabel(after[r.id]) }));
  S.report = { q: q.id, opt: optId, moved };
  // a beat of feedback before the next card: the choice locks, stars fly
  btn.classList.add('chosen'); btn.parentElement.classList.add('locked');
  burst(e && e.clientX ? e.clientX : btn.getBoundingClientRect().left + 30, e && e.clientY ? e.clientY : btn.getBoundingClientRect().top + 20);
  if (moved.length) { const bb = $('#ballotBtn'); bb.classList.remove('pulse'); void bb.offsetWidth; bb.classList.add('pulse'); }
  setTimeout(() => leave(() => render({ flash: moved.map((m) => m.id) })), reduced ? 0 : 320);
}

function back() {
  if (S.phase === 'done') S.phase = 'q';
  const lastQ = S.hist.pop();
  S.lightningDone = false; S.report = null;
  if (lastQ) {
    S.order = S.order.filter((id) => id !== lastQ);
    S.skipped = S.skipped.filter((id) => id !== lastQ);
    delete S.answers[lastQ];
  }
  render();
}

function renderLightning(list) {
  const { E } = evaluate();
  app.innerHTML = `
  ${track(S.hist.length + 1, 1)}
  <div class="qmeta"><span>Lightning round</span><span>last stop</span></div>
  ${ovalField(E, 'mini')}
  ${reportCard()}
  <section class="qcard card-pop" style="--line:var(--pink)">
    <div class="qsign"><span class="bullet">⚡</span><span class="stn"><small>Express</small>Public questions</span><span class="qn">${list.length}</span></div>
    <div class="qbar"></div>
    <div class="qbody">
      <h2>${esc(LIGHTNING_PROMPT)}</h2>
      <div class="lightning">
        ${list.map((r) => `<div class="lrow">
          <div class="ltext"><b>${esc(r.short || r.title)}</b><span>${esc(r.lightningAsk || r.wording)}</span></div>
          <div class="seg" role="group" aria-label="${esc(r.title)}">
            <button data-m="${r.id}" data-v="yes" class="${S.direct[r.id] === 'yes' ? 'on' : ''}">Yes</button>
            <button data-m="${r.id}" data-v="no" class="${S.direct[r.id] === 'no' ? 'on' : ''}">No</button>
            <button data-m="${r.id}" data-v="" class="${!S.direct[r.id] ? 'on' : ''}">Not sure</button>
          </div></div>`).join('')}
      </div>
      <div class="qfoot"><button class="link" id="back">↶ Undo last</button><button class="btn btn-primary" id="ldone">See my ballot ${STAR}</button></div>
    </div>
  </section>`;
  app.querySelectorAll('.seg button').forEach((b) => b.onclick = (e) => {
    if (b.dataset.v) { S.direct[b.dataset.m] = b.dataset.v; burst(e.clientX, e.clientY, 6); } else delete S.direct[b.dataset.m];
    b.parentElement.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    save(); renderBallot([b.dataset.m]);
    app.querySelector('.ovalfield.mini').outerHTML = ovalField(evaluate().E, 'mini');
  });
  $('#ldone').onclick = () => { S.lightningDone = true; S.phase = 'done'; render({ celebrate: true }); };
  $('#back').onclick = back;
}

// ---------------------------------------------------------------- the ballot panel
function groups() {
  const g = []; for (const r of RACES) { let x = g.find((y) => y.name === r.group); if (!x) g.push(x = { name: r.group, races: [] }); x.races.push(r); }
  return g;
}

function renderBallot(flash = []) {
  const { E } = evaluate();
  const all = RACES.length; const done = RACES.filter((r) => E[r.id].decided).length;
  $('#ballotCount').textContent = `${done}/${all}`;
  const ov = ovals(E); const filled = ov.filter((o) => o.on || o.no).length;
  ballotPane.innerHTML = `
  <div class="bp-head"><div><div class="kicker">Ballot so far</div><b>${done} of ${all} races filled in</b></div>
    <button class="icon-btn bp-close" aria-label="Close" data-close>✕</button></div>
  ${ovalField(E)}
  <div class="of-caption">${filled} of ${ov.length} ovals marked. Tap any race for every candidate, the sources and the why.</div>
  <div class="bp-body">
  ${groups().map((g) => `<div class="bp-group" style="--line:${LINE[g.name]}"><div class="bp-gname"><i></i>${esc(g.name)}</div>
    ${g.races.map((r) => { const ev = E[r.id]; const [cl, tone] = CONF_LABEL[ev.conf] || ['', 'mute'];
      return `<button class="bp-row${flash.includes(r.id) ? ' flash' : ''}" data-race="${r.id}">
        <span class="bp-office">${esc(r.short || r.title)}</span>
        <span class="bp-pick${pickLabel(ev) === '—' ? ' empty' : ''}">${esc(pickLabel(ev))}</span>
        <span class="chip ${tone}">${esc(cl)}</span></button>`; }).join('')}
  </div>`).join('')}</div>`;
  ballotPane.querySelectorAll('[data-race]').forEach((b) => b.onclick = () => openRace(b.dataset.race));
  const c = ballotPane.querySelector('[data-close]'); if (c) c.onclick = closeBallotSheet;
  // the flag's four stars: one per quarter of the ballot filled in
  const lit = Math.floor(4 * done / all + 1e-9);
  document.querySelectorAll('.fstar').forEach((s, i) => {
    const on = i < lit; if (on && !s.classList.contains('lit') && !reduced && lastFilled) burstAt(s, 8);
    s.classList.toggle('lit', on);
  });
  lastFilled = new Set(ov.filter((o) => o.on || o.no).map((o) => o.key));
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
  dlg.style.setProperty('--line', LINE[r.group]);
  dlg.innerHTML = `
    <div class="dlg-sign"><div><div class="kicker">${esc(LINE_NAME[r.group] || '')} · ${esc(r.group)}</div><h3>${esc(r.title)}</h3>${r.es ? `<div class="es">${esc(r.es)}</div>` : ''}</div>
      <button class="icon-btn" data-x aria-label="Close">✕</button></div>
    <div class="dlg-in">
    ${r.context ? `<p class="ctx">${esc(r.context)}</p>` : ''}
    <div class="rec"><div class="rec-top"><span>Your ballot</span><span class="chip ${tone}">${esc(cl)}</span></div>
      <div class="rec-pick">${esc(pickLabel(ev))}</div>
      ${reasons.length ? `<ul class="reasons">${reasons.map((x) => `<li>${x}</li>`).join('')}</ul>` : ev.conf === 'nodata' ? '<p class="mute-t">Answer a few more questions and this fills in, or choose below.</p>' : ''}
      ${S.picks[id] ? '<button class="link" data-unlock>↶ Undo my choice and let my answers decide</button>' : ''}
    </div>
    ${body}
  </div>`;
  dlg.querySelector('[data-x]').onclick = () => dlg.close();
  const ul = dlg.querySelector('[data-unlock]'); if (ul) ul.onclick = () => { delete S.picks[id]; render(); openRace(id); };
  dlg.querySelectorAll('[data-choose]').forEach((b) => b.onclick = (e) => { burst(e.clientX, e.clientY, 6); choose(r, b.dataset.choose); });
  dlg.querySelectorAll('[data-jv]').forEach((b) => b.onclick = () => {
    const [jid, v] = b.dataset.jv.split('|');
    if (v === 'auto') delete S.judgePicks[jid]; else S.judgePicks[jid] = v;
    render(); openRace(id);
    const el = dlg.querySelector(`[data-jid="${jid}"]`); if (el) { el.open = true; el.scrollIntoView({ block: 'nearest' }); }
  });
  dlg.querySelectorAll('[data-filter]').forEach((b) => b.onclick = () => {
    dlg.querySelectorAll('[data-filter]').forEach((x) => x.classList.toggle('on', x === b));
    dlg.querySelectorAll('.judge').forEach((el) => { el.hidden = b.dataset.filter === 'flag' && !el.classList.contains('flagged'); });
  });
  if (!dlg.open) { dlg.showModal(); dlg.scrollTop = 0; }
}

function choose(r, val) {
  if (r.kind === 'measure') S.picks[r.id] = val;
  else if ((r.voteFor || 1) > 1) {
    const { E } = evaluate(); let cur = S.picks[r.id] || E[r.id].picks.slice();
    cur = cur.includes(val) ? cur.filter((x) => x !== val) : [...cur, val].slice(-(r.voteFor));
    S.picks[r.id] = cur;
  } else S.picks[r.id] = val;
  render({ flash: [r.id] }); openRace(r.id);
}

const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return u; } };
function srcList(sources) {
  if (!sources || !sources.length) return '';
  return `<div class="srcs"><span>Sources</span>${sources.map((s, i) => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${i + 1}. ${esc(s.title || hostOf(s.url))}</a>`).join('')}</div>`;
}

function candidatesBody(r, ev) {
  const rows = ev.scored.slice().sort((a, b) => (b.max ? b.s : -9) - (a.max ? a.s : -9) || a.c.ballot - b.c.ballot);
  const multi = (r.voteFor || 1) > 1;
  return `<div class="cands">${rows.map((x) => { const c = x.c; const on = ev.picks.includes(c.id);
    return `<details class="cand${on ? ' on' : ''}"${on && r.candidates.length < 4 ? ' open' : ''}>
      <summary>
        <span class="num">${c.ballot}</span>
        <span class="cname"><b>${esc(c.name)}</b>${c.runningMate ? `<i>& ${esc(c.runningMate)}</i>` : ''}<em>${esc(c.partyName || 'Nonpartisan')}${c.incumbent ? ' · incumbent' : ''}${c.withdrawn ? ' · withdrew, still on the ballot' : ''}</em></span>
        <span class="match">${x.pct == null ? '' : `<b>${x.pct}%</b><span>match</span><div class="mbar"><span style="width:${x.pct}%"></span></div>`}</span>
      </summary>
      <div class="cbody">
        ${c.withdrawn ? `<p class="flagline flag-caution">${esc(c.withdrawn)}</p>` : ''}
        ${c.bio ? `<p>${esc(c.bio)}</p>` : ''}
        ${c.quals ? `<h4>Qualifications</h4><p>${esc(c.quals)}</p>` : ''}
        ${c.positions && Object.keys(c.positions).length ? `<h4>Positions</h4><dl>${Object.entries(c.positions).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>` : ''}
        ${c.endorse && c.endorse.length ? `<h4>Endorsements</h4><p>${c.endorse.map(esc).join(' · ')}</p>` : ''}
        ${c.gaps && c.gaps.length ? `<h4>Gaps & concerns</h4><ul class="gaps">${c.gaps.map((g) => `<li>${esc(g)}</li>`).join('')}</ul>` : ''}
        ${x.parts.filter((p) => p.ax !== 'party').length ? `<h4>How you line up</h4><ul class="align">${x.parts.filter((p) => p.ax !== 'party').map((p) => `<li class="${p.sim > 0.25 ? 'agree' : p.sim < -0.25 ? 'disagree' : 'meh'}"><b>${esc(axisName(p.ax))}:</b> ${esc(p.why || '')}</li>`).join('')}</ul>` : ''}
        ${srcList(c.sources)}
        ${c.withdrawn ? '' : `<button class="btn ${on ? 'btn-ghost' : 'btn-primary'} btn-sm" data-choose="${c.id}">${on ? (multi ? 'Remove from my three' : '✓ My pick') : (multi ? 'Add to my three' : 'Vote for this candidate instead')}</button>`}
      </div></details>`; }).join('')}</div>
    ${r.writeIn ? '<p class="mute-t" style="margin-top:10px">This race also has a write-in line.</p>' : ''}`;
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
    <div class="seg big">${['yes', 'no', 'blank'].map((v) => `<button data-choose="${v}" class="${ev.pick === v ? 'on' : ''}">${{ yes: 'Yes', no: 'No', blank: 'Leave blank' }[v]}</button>`).join('')}</div>
  </div>`;
}

const FLAG = { concern: '⚠ Not recommended by a major bar association', caution: '◐ A red flag from a smaller bar group or the record', clean: '✓ Recommended across the bar groups', unknown: '? No ratings found' };
const BAR = { cba: 'Chicago Bar Association', ccl: 'Chicago Council of Lawyers', isba: 'Illinois State Bar Association', alliance: 'Alliance of Bar Associations', other: 'Other' };

function judgesBody(r, ev, P) {
  const flagged = ev.votes.filter((v) => v.j.flag === 'concern' || v.j.flag === 'caution').length;
  const pol = P.policy ? `Your rule: <b>${esc(P.src.policy.short)}</b>.` : 'Answer the judges question, or set each judge by hand.';
  return `${r.note ? `<p class="ctx">${esc(r.note)}</p>` : ''}
  <p class="ctx">${pol} ${flagged ? `${flagged} ${flagged === 1 ? 'has' : 'have'} a flag.` : ''}</p>
  ${ev.votes.length > 3 ? `<div class="seg filt"><button data-filter="all" class="on">All ${ev.votes.length}</button><button data-filter="flag">Flagged only (${flagged})</button></div>` : ''}
  <div class="judges">${ev.votes.map(({ j, vote, locked }) => `
    <details class="judge${j.flag === 'concern' || j.flag === 'caution' ? ' flagged' : ''}" data-jid="${j.id}">
      <summary>
        <span class="num">${j.yes || j.ballot}</span>
        <span class="cname"><b>${esc(j.name)}</b><em>${esc(j.seat || j.assignment || '')}</em></span>
        <span class="jv ${vote || 'none'}">${vote ? ({ yes: r.kind === 'judge' ? 'Vote' : 'Yes', no: 'No', blank: 'Blank' }[vote]) : '—'}${locked ? ' ✎' : ''}</span>
      </summary>
      <div class="cbody">
        <p class="flagline flag-${esc(j.flag)}">${esc(FLAG[j.flag] || j.flag)}</p>
        ${j.why ? `<p>${esc(j.why)}</p>` : ''}
        ${j.bio ? `<p>${esc(j.bio)}</p>` : ''}
        ${j.ratings && Object.keys(j.ratings).length ? `<h4>Ratings</h4><dl>${Object.entries(j.ratings).map(([k, v]) => `<dt>${esc(BAR[k] || k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>` : ''}
        ${j.iw ? `<h4>Injustice Watch</h4><p>${esc(j.iw)}</p>` : ''}
        ${srcList(j.sources)}
        <div class="seg" style="margin-top:12px">${(r.kind === 'judge' ? ['yes', 'blank', 'auto'] : ['yes', 'no', 'blank', 'auto']).map((v) => `<button data-jv="${j.id}|${v}" class="${(v === 'auto' && !locked) || (locked && vote === v) ? 'on' : ''}">${{ auto: 'Use my rule', blank: 'Blank', yes: r.kind === 'judge' ? 'Vote' : 'Yes', no: 'No' }[v]}</button>`).join('')}</div>
      </div></details>`).join('')}</div>`;
}

// ---------------------------------------------------------------- results
function archetype(P) {
  const u = P.u; const e = u.econ ?? 0, s = u.safety ?? 0, ch = u.change ?? 0, f = u.federal ?? 0;
  if (e <= -0.8 && ch >= 0.8) return ['🔥', 'The Reform Insurgent', 'Progressive on the money and impatient with the old guard. You want the system shaken up, not just steered.'];
  if (e <= -0.8 && s >= 0.8) return ['🧱', 'The Pragmatic Progressive', 'Tax the top and fund the basics, but you want the streets safe now, not after the next study.'];
  if (e <= -0.8) return ['🌊', 'The Lakefront Progressive', 'Public money for public goods, a Chicago that stands up to Washington, and rights written into law.'];
  if (e >= 0.8 && ch >= 0.8) return ['🧨', 'The Outsider Fiscal Hawk', 'Lower taxes, fewer insiders, and somebody finally reading the bills before they pass.'];
  if (e >= 0.8 || (s >= 1 && f >= 1)) return ['🏡', 'The Bungalow Belt Conservative', 'Taxes down, police up, and a government that sticks to the basics and does them well.'];
  if (ch >= 0.8) return ['🦟', 'The Independent Gadfly', 'No party owns you. You vote the person, and you like a little disruption.'];
  if (ch <= -0.8) return ['⚓', 'The Steady Hand', 'Experience matters, and so do results. You’d rather fix the machine than smash it.'];
  return ['⚖️', 'The Split-Ticket Pragmatist', 'Somewhere in the middle, on purpose. You weigh each race on its own.'];
}

function renderDone(celebrate) {
  const { P, E } = evaluate();
  const [emo, name, line] = archetype(P);
  const more = QUESTIONS.filter((q) => !S.answers[q.id] && !S.skipped.includes(q.id));
  const undecided = RACES.filter((r) => !E[r.id].decided);
  const ov = ovals(E);
  const judgeVotes = RACES.filter((r) => r.kind === 'retention').flatMap((r) => E[r.id].votes);
  const strong = RACES.filter((r) => E[r.id].conf === 'strong').length;
  let row = 0;
  app.innerHTML = `
  <section class="done">
    <div class="arch"><span class="arch-emo">${emo}</span><div><div class="kicker">Your Chicago voter type</div><h2>${esc(name)}</h2><p>${esc(line)}</p></div></div>
    <div class="tally">
      <div><b>${ov.filter((o) => o.on || o.no).length}</b><span>ovals marked</span></div>
      <div><b>${S.order.length}</b><span>questions answered</span></div>
      <div><b>${strong}</b><span>strong matches</span></div>
      <div><b>${judgeVotes.filter((v) => v.vote === 'no').length}</b><span>judges you’d vote No on</span></div>
    </div>
    <div class="cta-row">
      <button class="btn btn-primary" id="print">🖨 Print my cheat sheet</button>
      <button class="btn btn-ghost" id="share">🔗 Copy a link to my answers</button>
      ${more.length ? `<button class="btn btn-ghost" id="more">✨ Sharpen it (${more.length} more)</button>` : ''}
      <button class="btn btn-ghost" id="undo">↶ Undo last</button>
      <button class="btn btn-ghost" id="again">Start over</button>
    </div>
    ${undecided.length ? `<p class="fine">${undecided.length} ${undecided.length > 1 ? 'races are' : 'race is'} still open: ${undecided.map((r) => esc(r.short || r.title)).join(', ')}. Tap ${undecided.length > 1 ? 'one' : 'it'} below to choose.</p>` : ''}
    <p class="fine">Illinois lets you bring notes into the booth. Tap any race to see every candidate, the sources, and why it landed where it did.</p>
  </section>
  <section class="sheet" id="sheet">
    <div class="sheet-head"><b>★ My ballot · ${esc(ELECTION.precinct)}</b><span>${esc(ELECTION.dateLabel)} · ${esc(ELECTION.ballotStyle)}</span></div>
    ${groups().map((g) => `<div class="sg" style="--line:${LINE[g.name]}"><h3><i></i>${esc(g.name)}</h3>${g.races.map((r) => sheetRow(r, E[r.id], row++)).join('')}</div>`).join('')}
    <p class="fine">Made with Chicago Voter · Ballot Match. The numbers are the line numbers printed beside each oval on ballot style 124.</p>
  </section>`;
  $('#print').onclick = () => window.print();
  $('#share').onclick = share;
  $('#undo').onclick = back;
  $('#again').onclick = () => { if (confirm('Clear your answers and start over?')) { S = fresh(); render(); } };
  if ($('#more')) $('#more').onclick = () => { S.skipped = S.skipped.filter((id) => Q[id] && Q[id].kind); S.sharpen = true; S.phase = 'q'; render(); };
  app.querySelectorAll('[data-race]').forEach((b) => b.onclick = () => openRace(b.dataset.race));
  if (celebrate) { window.scrollTo({ top: 0 }); confetti(); }
}

function sheetRow(r, ev, i) {
  const d = `style="animation-delay:${Math.min(i, 30) * 22}ms"`;
  if (r.kind === 'retention') {
    return `<div class="srow judgesrow" data-race="${r.id}" ${d}><div class="soff">${esc(r.title)}</div>
      <div class="jgrid">${ev.votes.map(({ j, vote }) => `<span class="jcell ${vote || 'none'}${j.flag === 'concern' || j.flag === 'caution' ? ' fl' : ''}"><i>${vote === 'yes' ? j.yes : vote === 'no' ? j.no : '–'}</i>${esc(j.name)}<b>${vote === 'yes' ? 'Yes' : vote === 'no' ? 'No' : '—'}</b></span>`).join('')}</div></div>`;
  }
  if (r.kind === 'judge') {
    return ev.votes.map(({ j, vote }) => `<div class="srow" data-race="${r.id}" ${d}><div class="soff">${esc(j.seat || r.title)}</div>
      <div class="spick">${vote === 'yes' ? `<span class="oval">${j.ballot}</span>${esc(j.name)}` : '<span class="mute-t">Leave blank</span>'}</div></div>`).join('');
  }
  if (r.kind === 'measure') {
    return `<div class="srow" data-race="${r.id}" ${d}><div class="soff">${esc(r.short || r.title)}</div>
      <div class="spick">${ev.pick === 'yes' || ev.pick === 'no' ? `<span class="oval">${ev.pick === 'yes' ? 'Yes' : 'No'}</span>` : '<span class="mute-t">Blank</span>'}</div></div>`;
  }
  const picks = ev.picks.map((id) => r.candidates.find((c) => c.id === id));
  return `<div class="srow" data-race="${r.id}" ${d}><div class="soff">${esc(r.short || r.title)}${(r.voteFor || 1) > 1 ? ` <em>(vote for ${r.voteFor})</em>` : ''}</div>
    <div class="spick">${picks.length ? picks.map((c) => `<span class="oval">${c.ballot}</span>${esc(c.name)}${c.runningMate ? ` & ${esc(c.runningMate)}` : ''}`).join('<br>') : '<span class="mute-t">Blank</span>'}</div></div>`;
}

function share() {
  const a = S.order.map((id) => `${id}.${S.answers[id].opt}`).join(',');
  const d = Object.entries(S.direct).map(([k, v]) => `${k}.${v[0]}`).join(',');
  const url = `${location.origin}${location.pathname}#a=${a}${d ? `&d=${d}` : ''}`;
  const ok = () => toastText('Link copied. It carries your answers, not your name.');
  if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, () => prompt('Copy this link:', url));
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

// ---------------------------------------------------------------- delight
function burst(x, y, n = 9) {
  if (reduced) return;
  const b = document.createElement('div'); b.className = 'burst'; b.style.left = `${x}px`; b.style.top = `${y}px`;
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + Math.random() * 0.5, d = 34 + Math.random() * 40;
    b.insertAdjacentHTML('beforeend', `<svg style="--dx:${Math.cos(a) * d}px;--dy:${Math.sin(a) * d}px"><use href="#star"/></svg>`);
  }
  document.body.append(b); setTimeout(() => b.remove(), 800);
}
function burstAt(el, n) { const r = el.getBoundingClientRect(); burst(r.left + r.width / 2, r.top + r.height / 2, n); }

// six-pointed stars in flag red and lake blue, raining down once at the reveal
function confetti() {
  if (reduced) return;
  const cv = $('#confetti'); const ctx = cv.getContext('2d'); const dpr = Math.min(2, devicePixelRatio || 1);
  const W = cv.width = innerWidth * dpr, H = cv.height = innerHeight * dpr;
  const cols = ['#e4002b', '#41b6e6', '#e4002b', '#b3ddf2', '#ffffff'];
  const ps = Array.from({ length: 90 }, () => ({ x: Math.random() * W, y: -Math.random() * H * 0.6, r: (6 + Math.random() * 9) * dpr,
    vy: (2 + Math.random() * 3) * dpr, vx: (Math.random() - 0.5) * 2 * dpr, a: Math.random() * 6, va: (Math.random() - 0.5) * 0.2, c: cols[Math.floor(Math.random() * cols.length)] }));
  const star = (p) => {
    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.beginPath();
    for (let i = 0; i < 12; i++) { const rad = i % 2 ? p.r * 0.42 : p.r; const t = -Math.PI / 2 + i * Math.PI / 6; ctx.lineTo(rad * Math.cos(t), rad * Math.sin(t)); }
    ctx.closePath(); ctx.fillStyle = p.c; ctx.fill(); if (p.c === '#ffffff') { ctx.strokeStyle = '#41b6e6'; ctx.lineWidth = dpr; ctx.stroke(); } ctx.restore();
  };
  let t0 = performance.now();
  (function frame(t) {
    ctx.clearRect(0, 0, W, H);
    for (const p of ps) { p.x += p.vx; p.y += p.vy; p.a += p.va; star(p); }
    if (t - t0 < 3800) requestAnimationFrame(frame); else ctx.clearRect(0, 0, W, H);
  })(t0);
}

let toastTimer;
function toastText(t) {
  const el = $('#toast'); el.textContent = t; el.classList.add('show');
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
  if (S.phase === 'q' && !dlg.open && /^[a-d1-4]$/i.test(e.key) && !e.metaKey && !e.ctrlKey && !e.altKey) {
    const i = 'abcd1234'.indexOf(e.key.toLowerCase()) % 4; const b = app.querySelectorAll('.opt')[i]; if (b) b.click();
  }
});
dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });

initTheme();
fromHash();
render();

// for the smoke test
window.__voter = { evaluate, nextStep, RACES, QUESTIONS, get state() { return S; } };
