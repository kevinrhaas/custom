// The Gangway Hosta Garden — app frame on the Polecat shell.
// Left rail + topbar + one-view-at-a-time. Garden palette (dark default).
import { configure as configureTheme, applyTheme, toggleMode } from '../vendor/polecat-shell/theme.js';
import { initShell } from '../vendor/polecat-shell/shell.js';
import { icon } from '../vendor/polecat-shell/icons.js';
import { el, escapeHtml } from '../vendor/polecat-shell/ui.js';
import { filterPills, multiselectDropdown } from '../vendor/polecat-shell/views.js';

const DESIGNS = JSON.parse(document.getElementById('designsData').textContent);
const FINAL = JSON.parse(document.getElementById('finalData').textContent);
const CATNAME = {1:'Giant Blue',2:'Giant/Large Gold',3:'Upright / Vase',4:'Large Blue Mound',
  5:'Large Green / Fragrant',6:'Green + White Margin',7:'Gold/Yellow Margin',8:'Gold-Centered Two-Tone',
  9:'Medium Blue Mound',10:'Frosted / Misted',11:'Small Gold Accent',12:'Small Green Edger',13:'Miniature / Mouse-Ear'};
const CAT = {1:['#1f3a6e','#15284d'],2:['#c8961c','#8c6913'],3:['#7a5aa8','#553e75'],4:['#3d6fb5','#2a4d7e'],
  5:['#1f7a45','#155530'],6:['#63b394','#457d67'],7:['#8f9c2b','#646d1e'],8:['#d2691e','#934915'],
  9:['#74a8de','#51759b'],10:['#94a9cf','#677690'],11:['#e0bf2f','#9c8520'],12:['#4f9a56','#376b3c'],13:['#b06a8f','#7b4a64']};

const SECTIONS = [
  { group:'The plan' },
  { key:'final',     label:'Final plan',    icon:'star' },
  { key:'site',      label:'Site & soil',   icon:'layers' },
  { key:'build',     label:'Build & budget',icon:'compass' },
  { key:'finder',    label:'Plant finder',  icon:'search' },
  { group:'Explore' },
  { key:'designs',   label:'Explorations',  icon:'grid' },
  { key:'reference', label:'Plant library', icon:'book' },
  { key:'renderkit', label:'Render kit',    icon:'wand' },
];
const TITLE = { final:'Final plan — Blue & White Gangway', designs:'Explorations', finder:'Plant finder',
  site:'Site & soil', build:'Build & budget', reference:'Plant library', renderkit:'Render kit' };
const KEYS = SECTIONS.filter(s=>s.key).map(s=>s.key);

configureTheme({ storageKey:'hosta.theme', defaultTheme:'garden:dark',
  palettes:[{ key:'garden', label:'Garden', hint:'Shade-garden greens, light & dark' }] });
applyTheme();

let shell, main, titleEl, themeBtn, current='final';
const isLight = ()=>document.documentElement.getAttribute('data-theme')==='light';

function boot(){
  titleEl = el('h1',{ text:TITLE.final, style:'font-size:16px;font-weight:700;margin:0' });
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

  renderFinal();
  routeFromHash();
  window.addEventListener('hashchange', routeFromHash);
}

function routeFromHash(){
  const [k, sub] = location.hash.replace(/^#\/?/,'').split('/');
  go(KEYS.includes(k) ? k : 'final', sub, true);
}
function go(key, sub, fromHash){
  if(!KEYS.includes(key)) key='final';
  current = key;
  main.querySelectorAll('section[data-view]').forEach(s=> s.hidden = s.dataset.view !== key);
  titleEl.textContent = TITLE[key];
  shell.setActive(key);
  const hash = sub ? `${key}/${sub}` : key;
  if(!fromHash) location.hash = hash;
  if(key==='final') renderFinal();
  if(key==='designs') renderDesigns(sub);
  if(key==='finder') renderFinder();
  if(key==='renderkit') wireRenderKit();
  main.scrollTo?.(0,0);
  if(window.matchMedia('(max-width:860px)').matches) shell.setOpen(false);
}

// ---------------------------------------------------------------- final plan
function renderFinal(){
  const sec = main.querySelector('[data-view="final"] .view-inner');
  if(sec.dataset.done) return;
  sec.dataset.done = '1';
  const h = FINAL.hero;
  let html = `
    <div class="ov-hero">
      <p class="eyebrow">${escapeHtml(h.kicker)}</p>
      <h1>${escapeHtml(h.title)}</h1>
      <p>${escapeHtml(h.blurb)}</p>
      <div class="ov-facts">${h.facts.map(f=>`<div><b>${escapeHtml(f[0])}</b>${escapeHtml(f[1])}</div>`).join('')}</div>
    </div>
    <div class="dd-h">The three zones, street → yard</div>
    <div class="guide fp-ov"><div class="g-svg">${h.overview}</div></div>`;
  FINAL.zones.forEach((z, zi)=>{
    html += `<section class="fp-zone"><h2>${escapeHtml(z.name)}</h2><p class="view-lede">${escapeHtml(z.intro)}</p>`;
    if(z.options){
      html += `<div class="dd-tabs">${z.options.map((o,i)=>
        `<button class="dd-tab${i===0?' on':''}${o.chosen?' fp-chosen':''}" data-zopt="${zi}:${i}">${o.chosen?'★ ':''}${escapeHtml(o.label)}${o.chosen?' · chosen':''}</button>`).join('')}</div>
        <div class="fp-opt" id="fpopt-${zi}"></div>`;
    }
    if(z.steps){
      html += `<ol class="fp-steps">${z.steps.map(s=>
        `<li><b>${escapeHtml(s[0])}</b><span>${escapeHtml(s[1])}</span></li>`).join('')}</ol>`;
      if(z.note) html += `<div class="dd-changes">${escapeHtml(z.note)}</div>`;
    }
    if(z.groundcover){
      html += `<div class="dd-h">${escapeHtml(z.groundcover.intro)}</div>
        <div class="fp-gc">${z.groundcover.choices.map(c=>
          `<div class="fp-gc-card"><b>${escapeHtml(c[0])}</b><span>${escapeHtml(c[1])}</span></div>`).join('')}</div>`;
    }
    html += `</section>`;
  });
  sec.innerHTML = html;
  FINAL.zones.forEach((z, zi)=>{ if(z.options) paintOpt(zi, 0); });
  sec.querySelectorAll('[data-zopt]').forEach(b=> b.onclick=()=>{
    const [zi, i] = b.dataset.zopt.split(':').map(Number);
    b.parentElement.querySelectorAll('.dd-tab').forEach(x=>x.classList.toggle('on', x===b));
    paintOpt(zi, i);
  });
}
function paintOpt(zi, i){
  const o = FINAL.zones[zi].options[i];
  const host = main.querySelector('#fpopt-'+zi);
  const rows = o.plants.map(p=>{
    const sw = p.sw ? p.sw : ['#cdd68c','#8a9a4e'];
    const cost = p.each ? `$${p.each.toFixed(2)} ea · $${p.line.toFixed(2)}` : '<span class="fp-comp">companion</span>';
    return `<tr><td><span class="sw" style="background:${sw[0]};border-color:${sw[1]}"></span></td>
      <td class="lnm">${escapeHtml(p.name)}${p.tag?` <span class="fp-tag">${escapeHtml(p.tag)}</span>`:''}</td>
      <td class="r">×${p.qty}</td><td class="r">${cost}</td></tr>`;
  }).join('');
  const topLabel = FINAL.zones[zi].id === 'bed' ? 'Top-down — staggered drift' : 'Top-down — fence corner';
  const rends = o.renders || [];
  let renderBlock = '';
  if(rends.length){
    const toggle = rends.length > 1
      ? `<div class="fp-rtoggle">${rends.map((r, ri)=>`<button class="fp-rbtn${ri===0?' on':''}" type="button" data-r="${ri}">${escapeHtml(r.label)}</button>`).join('')}</div>`
      : `<div class="fp-rcap">${escapeHtml(rends[0].label)}</div>`;
    renderBlock = `<div class="dd-h">Final render — how it looks</div>${toggle}
      <img class="fp-renderimg" id="fprender-${zi}" src="${rends[0].img}" alt="final render — ${escapeHtml(rends[0].label)}" loading="lazy">`;
  }
  // the GPT prompt / reference: front-and-centre when there's no render yet, tucked into a
  // collapsible once a render exists.
  const gen = `<div class="fp-render">
      <img class="fp-sample" src="${o.sample}" alt="style reference" loading="lazy">
      <p class="fp-hint">Attach this plate as the style/site reference, paste the prompt, generate — then send it back.</p>
      <button class="chip fp-copy" type="button">⧉ Copy render prompt</button>
      <pre class="fp-prompt">${escapeHtml(o.prompt)}</pre>
    </div>`;
  const genPanel = rends.length
    ? `<details class="fp-gen"><summary>Regenerate / prompt &amp; reference</summary>${gen}</details>`
    : `<div class="dd-h">Generate the image in GPT</div>${gen}`;
  host.innerHTML = `
    <div class="dd-changes">${escapeHtml(o.note)}</div>
    ${renderBlock}
    <div class="dd-h">${topLabel}</div>
    <div class="guide"><div class="g-svg">${o.schematic}</div></div>
    <div class="fp-cols">
      <div><div class="dd-h">Plant list</div>
        <table class="ltbl fp-plants"><tbody>${rows}</tbody>
        <tfoot><tr><td></td><td><b>Hostas subtotal</b></td><td></td><td class="r"><b>$${o.cost.toFixed(2)}</b></td></tr></tfoot></table></div>
      <div>${genPanel}</div>
    </div>`;
  host.querySelectorAll('.fp-rbtn').forEach(b=> b.onclick=()=>{
    const ri = +b.dataset.r; const img = host.querySelector('#fprender-'+zi);
    img.src = rends[ri].img; img.alt = 'final render — ' + rends[ri].label;
    host.querySelectorAll('.fp-rbtn').forEach(x=>x.classList.toggle('on', x===b));
  });
  host.querySelector('.fp-copy').onclick = (e)=>{
    const btn = e.currentTarget;
    navigator.clipboard?.writeText(o.prompt).then(()=>{ btn.textContent='Copied ✓'; setTimeout(()=>btn.textContent='⧉ Copy render prompt', 1500); });
  };
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
