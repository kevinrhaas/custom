// The Gangway Hosta Garden — app frame on the Polecat shell.
// Left rail + topbar + one-view-at-a-time. Garden palette (dark default).
import { configure as configureTheme, applyTheme, toggleMode } from '../vendor/polecat-shell/theme.js';
import { initShell } from '../vendor/polecat-shell/shell.js';
import { icon } from '../vendor/polecat-shell/icons.js';
import { el, escapeHtml } from '../vendor/polecat-shell/ui.js';
import { filterPills, multiselectDropdown } from '../vendor/polecat-shell/views.js';

const DESIGNS = JSON.parse(document.getElementById('designsData').textContent);
const CATNAME = {1:'Giant Blue',2:'Giant/Large Gold',3:'Upright / Vase',4:'Large Blue Mound',
  5:'Large Green / Fragrant',6:'Green + White Margin',7:'Gold/Yellow Margin',8:'Gold-Centered Two-Tone',
  9:'Medium Blue Mound',10:'Frosted / Misted',11:'Small Gold Accent',12:'Small Green Edger',13:'Miniature / Mouse-Ear'};
const CAT = {1:['#1f3a6e','#15284d'],2:['#c8961c','#8c6913'],3:['#7a5aa8','#553e75'],4:['#3d6fb5','#2a4d7e'],
  5:['#1f7a45','#155530'],6:['#63b394','#457d67'],7:['#8f9c2b','#646d1e'],8:['#d2691e','#934915'],
  9:['#74a8de','#51759b'],10:['#94a9cf','#677690'],11:['#e0bf2f','#9c8520'],12:['#4f9a56','#376b3c'],13:['#b06a8f','#7b4a64']};

const SECTIONS = [
  { group:'Guide' },
  { key:'overview',  label:'Overview',      icon:'home' },
  { key:'designs',   label:'Designs',       icon:'grid' },
  { key:'finder',    label:'Plant finder',  icon:'search' },
  { group:'Reference' },
  { key:'site',      label:'Site & soil',   icon:'layers' },
  { key:'build',     label:'Build & budget',icon:'compass' },
  { key:'reference', label:'Plant library', icon:'book' },
  { key:'renderkit', label:'Render kit',    icon:'wand' },
];
const TITLE = { overview:'The Gangway Hosta Garden', designs:'Designs', finder:'Plant finder',
  site:'Site & soil', build:'Build & budget', reference:'Plant library', renderkit:'Render kit' };
const KEYS = SECTIONS.filter(s=>s.key).map(s=>s.key);

configureTheme({ storageKey:'hosta.theme', defaultTheme:'garden:dark',
  palettes:[{ key:'garden', label:'Garden', hint:'Shade-garden greens, light & dark' }] });
applyTheme();

let shell, main, titleEl, themeBtn, current='overview';
const isLight = ()=>document.documentElement.getAttribute('data-theme')==='light';

function boot(){
  titleEl = el('h1',{ text:TITLE.overview, style:'font-size:16px;font-weight:700;margin:0' });
  themeBtn = el('button',{ class:'btn icon ghost', title:'Toggle light / dark', 'aria-label':'Toggle theme',
    html:icon(isLight()?'moon':'sun'), onclick:()=>{ toggleMode(); themeBtn.innerHTML=icon(isLight()?'moon':'sun'); } });
  const home = el('a',{ class:'btn sm ghost', href:'../', title:'Custom home', html:`${icon('external',15)} <span class="hide-sm">Custom</span>` });

  // mount on <body> (the shell's flex layout lives on body.ps-shell)
  shell = initShell({
    app:{ id:'hosta', name:'Gangway Hosta', wordmark:'🌿' },
    sections: SECTIONS.map(s=> s.group ? s : { ...s, icon:icon(s.icon) }),
    onNav:(k)=>go(k),
    rail:{ storageKey:'hosta.rail' },
    topbar:{ left:[titleEl], right:[home, themeBtn] },
  });
  main = shell.els.main;

  // move the pre-rendered view sections into the shell's main region
  const views = document.getElementById('views');
  [...views.querySelectorAll('section[data-view]')].forEach(sec=>{
    const inner = el('div',{ class:'view-inner' });
    while(sec.firstChild) inner.appendChild(sec.firstChild);
    sec.appendChild(inner); sec.hidden = true; main.appendChild(sec);
  });
  views.remove();

  renderOverview();
  routeFromHash();
  window.addEventListener('hashchange', routeFromHash);
}

function routeFromHash(){
  const [k, sub] = location.hash.replace(/^#\/?/,'').split('/');
  go(KEYS.includes(k) ? k : 'overview', sub, true);
}
function go(key, sub, fromHash){
  if(!KEYS.includes(key)) key='overview';
  current = key;
  main.querySelectorAll('section[data-view]').forEach(s=> s.hidden = s.dataset.view !== key);
  titleEl.textContent = TITLE[key];
  shell.setActive(key);
  const hash = sub ? `${key}/${sub}` : key;
  if(!fromHash) location.hash = hash;
  if(key==='designs') renderDesigns(sub);
  if(key==='finder') renderFinder();
  if(key==='renderkit') wireRenderKit();
  main.scrollTo?.(0,0);
  if(window.matchMedia('(max-width:860px)').matches) shell.setOpen(false);
}

// ---------------------------------------------------------------- overview
function renderOverview(){
  const sec = main.querySelector('[data-view="overview"] .view-inner');
  const cards = [
    ['designs','grid','The designs','6 plans + variations, side by side'],
    ['finder','search','Plant finder','Search all 74 varieties, tile or list'],
    ['site','layers','Site & soil','Light zones, the soil fix, slugs'],
    ['build','compass','Build & budget','Order of work, timing, the money'],
    ['reference','book','Plant library','Every variety, with substitutions'],
    ['renderkit','wand','Render kit','The GPT prompt for accurate images'],
  ].map(([k,ic,t,s])=>`<button class="ov-card" data-goto="${k}"><span class="ic">${icon(ic,22)}</span><b>${t}</b><span>${s}</span></button>`).join('');
  sec.innerHTML = `
    <div class="ov-hero">
      <p class="eyebrow">Portage Park · Chicago bungalow · USDA 6a</p>
      <h1>The Gangway Hosta Garden</h1>
      <p>Six designed plans — plus two finalization variations for each of the three core picks —
      for ninety-five feet of deep shade between two brick bungalows. Photoreal renders, measured
      plans, real Lurvey prices, and the whole build from soil to slugs.</p>
      <div class="ov-facts">
        <div><b>95 ft</b>total run</div><div><b>3 ft</b>wide bed</div>
        <div><b>6 + 6</b>plans &amp; variations</div><div><b>74</b>varieties costed</div>
        <div><b>$500–732</b>in plants</div>
      </div>
    </div>
    <div class="ov-cards">${cards}</div>`;
  sec.querySelectorAll('[data-goto]').forEach(b=> b.onclick=()=>go(b.dataset.goto));
}

// ---------------------------------------------------------------- designs
function designByN(n){ return DESIGNS.find(d=>String(d.n)===String(n)); }
function renderDesigns(sub){
  const sec = main.querySelector('[data-view="designs"] .view-inner');
  const gallery = sec.querySelector('#dvGallery'), detail = sec.querySelector('#dvDetail');
  const d = sub && designByN(sub);
  if(d){ gallery.hidden = true; detail.hidden = false; renderDetail(detail, d); }
  else {
    detail.hidden = true; gallery.hidden = false;
    if(gallery.dataset.done) return;
    gallery.innerHTML = `<div class="view-lede" style="grid-column:1/-1"><h2 style="margin:0 0 4px">The designs</h2>
      Six reference designs. The three core picks (★) each carry two finalization variations — twelve options in all.
      Open any to see its render, plan, shopping list and — for the cores — the variation comparison.</div>` +
      DESIGNS.map(x=>`<button class="dv-card${x.core?' core':''}" data-open="${x.n}">
        <img loading="lazy" src="${x.plate}" alt="${escapeHtml(x.name)}">
        <div class="dv-cb"><span class="dv-num">${x.n}</span>
          <span><span class="dv-nm">${escapeHtml(x.name)}</span><span class="dv-sub">${escapeHtml(x.tag)}</span></span>
          ${x.core?'<span class="dv-badge">★ core</span>':''}</div></button>`).join('');
    gallery.dataset.done = '1';
    gallery.querySelectorAll('[data-open]').forEach(b=> b.onclick=()=>go('designs', b.dataset.open));
  }
}
function renderDetail(host, d){
  const tabs = [{ key:'core', title:d.name, tag:d.tag, plate:d.plate }]
    .concat(d.variations.map(v=>({ key:v.key, title:v.title, tag:v.kicker, plate:v.plate, v })));
  const idx = 0;
  host.innerHTML = `
    <div class="dd-top">
      <button class="dd-back">← All designs</button>
      <div class="dd-nav">${prevNext(d.n)}</div>
    </div>
    <div id="ddBody"></div>`;
  host.querySelector('.dd-back').onclick = ()=>go('designs');
  host.querySelectorAll('[data-nav]').forEach(b=> b.onclick=()=>go('designs', b.dataset.nav));
  const body = host.querySelector('#ddBody');
  paintTab(body, d, tabs, idx);
}
function prevNext(n){
  n = +n; const prev = n>1?n-1:6, next = n<6?n+1:1;
  return `<button data-nav="${prev}">← ${prev}</button><button data-nav="${next}">${next} →</button>`;
}
function paintTab(body, d, tabs, i){
  const t = tabs[i];
  const tabStrip = tabs.length>1 ? `<div class="dd-tabs">${tabs.map((x,j)=>
     `<button class="dd-tab${j===i?' on':''}${d.core?' core':''}" data-t="${j}">${j===0?'Core plan':escapeHtml(x.title)}</button>`).join('')
     + `<button class="dd-tab" data-cmp="1">⇄ Compare all three</button>`}</div>` : '';
  const isCore = t.key==='core';
  const shop = isCore ? d.shop : t.v.shop;
  const meta = isCore ? '' : `<p class="dd-meta">${t.v.varieties} varieties · ${t.v.plants} plants · $${t.v.cost.toFixed(2)} in plants · installed $${t.v.total.toFixed(2)}</p>`;
  const changes = isCore ? (d.idea?`<div class="dd-changes">${d.idea}</div>`:'') : `<div class="dd-changes"><b>What changes vs the core:</b> ${t.v.changes}</div>`;
  const plan = isCore ? d.plan : `<div class="dd-h">Schematic top-down — proportional mix &amp; placement</div><div class="g-svg">${t.v.schematic}</div>`;
  const why = isCore ? (d.why?`<div class="dd-h">Why this works</div><div class="guide">${d.why}</div>`:'') : '';
  body.innerHTML = `
    <span class="dv-num" style="display:none"></span>
    <p class="dd-tag" style="text-transform:uppercase;letter-spacing:.12em;font-size:11px;color:var(--text-3);margin:0 0 4px">
      ${d.core?'★ Core pick · ':''}Plan ${d.n}${isCore?'':' variation'}</p>
    <h2 class="dd-title">${escapeHtml(t.title)}</h2>
    <p class="dd-tag">${escapeHtml(t.tag)}</p>
    <div class="guide"><img class="dd-plate" src="${t.plate}" alt="${escapeHtml(t.title)}"></div>
    ${tabStrip}
    ${changes}${meta}
    <div class="dd-cols">
      <div class="guide"><div class="dd-h">${isCore?'Plan — looking down at the bed':''}</div>${plan}</div>
      <div class="guide"><div class="dd-h">Shopping list</div>${shop}${why}</div>
    </div>`;
  body.querySelectorAll('[data-t]').forEach(b=> b.onclick=()=>paintTab(body, d, tabs, +b.dataset.t));
  const cmp = body.querySelector('[data-cmp]'); if(cmp) cmp.onclick=()=>paintCompare(body, d, tabs);
}
function paintCompare(body, d, tabs){
  const coreNames = new Set((d.plants||[]).map(p=>p.name));
  const cols = tabs.map((t,j)=>{
    const rows = j===0 ? (d.plants||[]) : (t.v.plantList||[]);
    const head = j===0 ? `Core — ${escapeHtml(d.name)}` : escapeHtml(t.title);
    const sub  = j===0 ? escapeHtml(d.tag) : escapeHtml(t.v.kicker);
    return `<div class="cmp-col${j===0?' is-core':''}"><h4>${head}</h4><p class="cmp-k">${sub}</p>
      <ul>${rows.map(r=>{ const swap = j>0 && !coreNames.has(r.name);
        return `<li class="${swap?'swap':''}"><b>${escapeHtml(r.name)}</b> × ${escapeHtml(String(r.qty))}${swap?' <span class="swap-tag">swapped in</span>':''}</li>`;
      }).join('')}</ul></div>`;
  }).join('');
  body.innerHTML = `
    <div class="dd-tabs"><button class="dd-tab" data-back="1">← Back to ${escapeHtml(d.name)}</button></div>
    <h2 class="dd-title">Compare — core &amp; its two variations</h2>
    <p class="dd-tag">Same footprint, different plant choices. Bold names show what each variation swaps in.</p>
    <div class="cmp-grid">${cols}</div>`;
  body.querySelector('[data-back]').onclick = ()=>paintTab(body, d, tabs, 0);
}

// ---------------------------------------------------------------- finder
const FKEY='hosta.lurvey.override';
let finderReady=false, F={ q:'', cats:[], toggles:[], sort:'cat', view:'tile', data:null };
function activeData(){
  if(F.data) return F.data;
  let d=null; try{ const o=localStorage.getItem(FKEY); if(o) d=JSON.parse(o); }catch(e){}
  F.data = (d&&Array.isArray(d.records)) ? d : JSON.parse(document.getElementById('lurveyData').textContent);
  F._override = !!(d&&Array.isArray(d.records));
  return F.data;
}
function renderFinder(){
  const sec = main.querySelector('[data-view="finder"] .view-inner');
  if(!finderReady){
    finderReady = true;
    const data = activeData();
    const counts = {}; data.records.forEach(r=> counts[r.category]=(counts[r.category]||0)+1);
    // category multiselect
    const catDd = multiselectDropdown({ label:'Category',
      options: Object.keys(CATNAME).map(k=>({ value:k, label:`${k}. ${CATNAME[k]}` })),
      selected: F.cats, counts,
      onChange:(sel)=>{ F.cats=sel; drawResults(sec); } });
    sec.querySelector('#fcatMount').replaceChildren(catDd);
    // toggle pills
    const pills = filterPills({ options:[
        { key:'stock', label:'In stock' }, { key:'fits', label:'Fits the bed' }, { key:'plans', label:'Used in a plan' }],
      selected: F.toggles, onChange:(sel)=>{ F.toggles=sel; drawResults(sec); } });
    sec.querySelector('#pillMount').replaceChildren(pills);
    sec.querySelector('#q').addEventListener('input', e=>{ F.q=e.target.value.trim().toLowerCase(); drawResults(sec); });
    sec.querySelector('#sort').addEventListener('change', e=>{ F.sort=e.target.value; drawResults(sec); });
    sec.querySelectorAll('#viewSeg button').forEach(b=> b.onclick=()=>{
      F.view=b.dataset.v; sec.querySelectorAll('#viewSeg button').forEach(x=>x.classList.toggle('on', x===b)); drawResults(sec); });
    // data panel
    const st = sec.querySelector('#dataStatus');
    st.textContent = F._override
      ? `Imported set: ${data.count||data.records.length} varieties, pulled ${data.pulledAt||'?'}.`
      : `Shipped base data: ${data.count||data.records.length} varieties, pulled ${data.pulledAt||'?'}.`;
    sec.querySelector('#dataExport').onclick = ()=>download('lurvey-hostas.json', JSON.stringify(activeData(),null,2));
    sec.querySelector('#dataReset').onclick = ()=>{ try{ localStorage.removeItem(FKEY); }catch(e){} location.reload(); };
    sec.querySelector('#dataFile').addEventListener('change', function(){
      const f=this.files[0]; if(!f) return; const rd=new FileReader();
      rd.onload=()=>{ try{ const p=JSON.parse(rd.result); if(!p||!Array.isArray(p.records)||!p.records.length) throw new Error('no records[]');
        localStorage.setItem(FKEY, JSON.stringify(p)); location.reload(); }
        catch(err){ alert('Import failed: '+err.message+'\n\nExpected the lurvey-hostas/v1 shape — see the spec.'); } this.value=''; };
      rd.readAsText(f);
    });
  }
  drawResults(sec);
}
const CMP = {
  cat:(a,b)=> (a.category-b.category) || a.name.localeCompare(b.name),
  name:(a,b)=> a.name.localeCompare(b.name),
  plo:(a,b)=> a.price-b.price || a.name.localeCompare(b.name),
  phi:(a,b)=> b.price-a.price || a.name.localeCompare(b.name),
  wlo:(a,b)=> a.spreadFt-b.spreadFt, whi:(a,b)=> b.spreadFt-a.spreadFt,
};
function drawResults(sec){
  const data = activeData();
  let rows = data.records.filter(r=>
    (!F.q || String(r.search||'').includes(F.q)) &&
    (!F.cats.length || F.cats.includes(String(r.category))) &&
    (!F.toggles.includes('stock') || r.inStock) &&
    (!F.toggles.includes('fits') || r.fit!=='no') &&
    (!F.toggles.includes('plans') || (r.plansUsed||0)>0));
  rows = rows.slice().sort(CMP[F.sort]||CMP.cat);
  sec.querySelector('#cnt').textContent = `Showing ${rows.length} of ${data.records.length}`;
  sec.querySelector('#nores').hidden = rows.length>0;
  const out = sec.querySelector('#finderResults');
  out.innerHTML = rows.length ? (F.view==='tile' ? tileHTML(rows) : listHTML(rows)) : '';
}
function fitBadge(r){
  if(!r.inStock) return `<span class="badge oos">Sold out</span>`;
  return `<span class="badge fit-${r.fitClass||'y'}">${escapeHtml(r.fitLabel||'Fits')}</span>`;
}
function sw(cat){ const c=CAT[cat]||['#888','#555']; return `<span class="sw" style="background:${c[0]};border-color:${c[1]}"></span>`; }
function tileHTML(rows){
  return `<div class="tiles">${rows.map(r=>`
    <div class="tile${r.inStock?'':' oos'}">
      <div class="th${r.image?'':' noimg'}">${r.image?`<img loading="lazy" src="${escapeHtml(r.image)}" alt="">`:'🌿'}</div>
      <div class="tb">
        <div class="tnm">${sw(r.category)}<a href="${escapeHtml(r.url)}" target="_blank" rel="noopener">${escapeHtml(r.name)}</a>${r.star?'<span class="star">★</span>':''}</div>
        <div class="tcat">${r.category}. ${escapeHtml(CATNAME[r.category]||'')} · ${escapeHtml(r.color||'')}</div>
        <div class="tnote">${escapeHtml(r.note||'')}</div>
        <div class="trow"><span class="tprice">$${Number(r.price||0).toFixed(2)}</span>${fitBadge(r)}</div>
      </div></div>`).join('')}</div>`;
}
function listHTML(rows){
  return `<div class="ltw"><table class="ltbl"><thead><tr>
    <th></th><th>Variety</th><th>Category</th><th>Colour</th><th>Spread</th><th>Light</th><th>Fits</th><th class="r">Price</th></tr></thead><tbody>${
    rows.map(r=>`<tr>
      <td>${sw(r.category)}</td>
      <td class="lnm"><a href="${escapeHtml(r.url)}" target="_blank" rel="noopener">${escapeHtml(r.name)}</a>${r.star?' <span style="color:var(--honey)">★</span>':''}
        <div style="font-size:11.5px;color:var(--text-3);font-weight:400">${escapeHtml(r.note||'')}</div></td>
      <td>${r.category}. ${escapeHtml(CATNAME[r.category]||'')}</td>
      <td>${escapeHtml(r.color||'')}</td><td>${escapeHtml(r.leafSize||'')}</td><td>${escapeHtml(r.light||'')}</td>
      <td>${fitBadge(r)}</td><td class="r">$${Number(r.price||0).toFixed(2)}</td></tr>`).join('')}</tbody></table></div>`;
}

// ---------------------------------------------------------------- render kit
function wireRenderKit(){
  const btn = main.querySelector('[data-view="renderkit"] .rk-copy');
  if(btn && !btn.dataset.wired){ btn.dataset.wired='1';
    btn.onclick = ()=>{ const pre=document.getElementById('rkPrompt'); if(!pre) return;
      navigator.clipboard?.writeText(pre.textContent).then(()=>{ btn.textContent='Copied ✓'; setTimeout(()=>btn.textContent='Copy',1500); }); };
  }
}

// ---------------------------------------------------------------- util
function download(name, text){
  const b=new Blob([text],{type:'application/json'}), u=URL.createObjectURL(b), a=document.createElement('a');
  a.href=u; a.download=name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(u),1000);
}

boot();
