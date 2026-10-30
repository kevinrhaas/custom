/* Custom — landing motion. Classic script, no deps.
   Everything here is enhancement: the page reads complete without it. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function css(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }

  /* ---- theme ----------------------------------------------------------- */
  var themeListeners = [];
  var toggle = document.getElementById('themeToggle');
  if (toggle) toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('custom.theme', next); } catch (e) {}
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', next === 'light' ? '#f6f4ef' : '#08090c');
    themeListeners.forEach(function (fn) { fn(); });
  });

  /* ---- nav state + page progress ---------------------------------------- */
  var nav = document.getElementById('nav');
  var bar = document.querySelector('.progress');
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var y = window.scrollY || 0, vh = window.innerHeight;
      var max = Math.max(1, document.documentElement.scrollHeight - vh);
      if (nav) nav.classList.toggle('scrolled', y > 24);
      if (bar) bar.style.setProperty('--sp', (y / max).toFixed(4));
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---- reveal on scroll + counters ------------------------------------- */
  function countUp(el) {
    var to = +el.getAttribute('data-count'), small = el.querySelector('small');
    var label = small ? small.outerHTML : '';
    if (reduce || !to) return;
    var t0 = null, dur = 1400;
    function step(t) {
      if (t0 === null) t0 = t;
      var k = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 4);
      el.innerHTML = Math.round(to * e) + label;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var reveals = [].slice.call(document.querySelectorAll('.reveal'));
  if (!('IntersectionObserver' in window)) {
    reveals.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        [].forEach.call(en.target.querySelectorAll('[data-count]'), countUp);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (e) { io.observe(e); });
  }

  /* ---- card spotlight + tilt ------------------------------------------- */
  [].forEach.call(document.querySelectorAll('.card'), function (card) {
    card.addEventListener('pointermove', function (ev) {
      var r = card.getBoundingClientRect();
      var x = ev.clientX - r.left, y = ev.clientY - r.top;
      card.style.setProperty('--mx', x + 'px');
      card.style.setProperty('--my', y + 'px');
      if (finePointer && !reduce) {
        card.style.setProperty('--ry', ((x / r.width - 0.5) * 5).toFixed(2) + 'deg');
        card.style.setProperty('--rx', ((0.5 - y / r.height) * 5).toFixed(2) + 'deg');
      }
    });
    card.addEventListener('pointerleave', function () {
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
    });
  });

  /* ---- object filters ---------------------------------------------------- */
  var filters = document.getElementById('filters');
  if (filters) {
    var pill = filters.querySelector('.pill');
    var btns = [].slice.call(filters.querySelectorAll('button'));
    var objs = [].slice.call(document.querySelectorAll('#objGrid .obj'));
    var placePill = function () {
      var on = filters.querySelector('[aria-pressed="true"]');
      if (!on || !pill) return;
      pill.style.width = on.offsetWidth + 'px';
      pill.style.transform = 'translateX(' + on.offsetLeft + 'px)';
    };
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-f');
        btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        placePill();
        objs.forEach(function (o) { o.classList.add('fading'); });
        setTimeout(function () {
          objs.forEach(function (o) {
            var show = f === 'all' || o.getAttribute('data-k') === f;
            o.classList.toggle('hide', !show);
          });
          requestAnimationFrame(function () {
            objs.forEach(function (o) { o.classList.remove('fading'); o.classList.add('in'); });
          });
        }, reduce ? 0 : 220);
      });
    });
    placePill();
    window.addEventListener('resize', placePill);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(placePill);
  }

  /* ---- shared canvas helpers ------------------------------------------- */
  function fitCanvas(cv) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) {
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    }
    var ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }
  function hexToRgb(hex) {
    hex = hex.replace('#', '');
    if (hex.length === 3) hex = hex.replace(/./g, '$&$&');
    var n = parseInt(hex, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  // Runs draw(t) every frame while the canvas is on screen and the tab is visible.
  function animate(cv, draw) {
    var visible = true, raf = 0;
    function loop(t) { raf = 0; draw(t); if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(loop); }
    function kick() { if (!raf) raf = requestAnimationFrame(loop); }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) kick(); }).observe(cv);
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
    window.addEventListener('resize', kick);
    themeListeners.push(kick);
    kick();
  }

  /* ---- hero: drifting strata ------------------------------------------ */
  (function () {
    var cv = document.getElementById('strata');
    if (!cv || !cv.getContext) return;
    var mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };
    var hero = cv.parentNode;
    hero.addEventListener('pointermove', function (e) {
      var r = cv.getBoundingClientRect(); mouse.tx = e.clientX - r.left; mouse.ty = e.clientY - r.top;
      if (mouse.x < -999) { mouse.x = mouse.tx; mouse.y = mouse.ty; }
    });
    hero.addEventListener('pointerleave', function () { mouse.tx = -9999; mouse.ty = -9999; });
    var palette = [], light = false;
    function readTheme() {
      light = root.getAttribute('data-theme') === 'light';
      palette = [hexToRgb(css('--accent')), hexToRgb(css('--red')), hexToRgb(css('--sky'))];
    }
    readTheme(); themeListeners.push(readTheme);
    function mix(a, b, k) { return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]; }

    animate(cv, function (t) {
      var f = fitCanvas(cv), ctx = f.ctx, W = f.w, H = f.h;
      t = reduce ? 4000 : t;
      ctx.clearRect(0, 0, W, H);
      mouse.x += (mouse.tx - mouse.x) * 0.08; mouse.y += (mouse.ty - mouse.y) * 0.08;
      if (mouse.tx < -999 && Math.abs(mouse.x) > 5000) mouse.x = mouse.y = -9999;
      var gap = W < 640 ? 15 : 19, L = Math.ceil(H / gap) + 6, step = W < 640 ? 10 : 14;
      ctx.lineWidth = 1;
      for (var k = 0; k < L; k++) {
        var base = -gap * 3 + k * gap, u = k / L;
        var amp = 8 + 30 * Math.sin(u * Math.PI);
        var c = u < 0.5 ? mix(palette[0], palette[1], u * 2) : mix(palette[1], palette[2], (u - 0.5) * 2);
        var a = (light ? 0.10 : 0.07) + (light ? 0.22 : 0.26) * Math.pow(Math.sin(u * Math.PI), 2);
        ctx.strokeStyle = 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + a.toFixed(3) + ')';
        ctx.beginPath();
        for (var x = -step; x <= W + step; x += step) {
          var y = base + amp * (0.55 * Math.sin(x * 0.0021 + t * 0.00022 + k * 0.32) +
                                0.30 * Math.sin(x * 0.0049 - t * 0.00016 + k * 0.17) +
                                0.45 * Math.sin(x * 0.0008 + k * 0.05 + t * 0.00009));
          var dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy;
          if (d2 < 90000) y += (dy >= 0 ? 1 : -1) * 42 * Math.exp(-d2 / 14000);
          if (x === -step) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    });
  })();

  /* ---- 4D Chicago: an isometric town that builds itself through time ---- */
  (function () {
    var cv = document.getElementById('iso');
    if (!cv || !cv.getContext) return;
    var yearEl = document.getElementById('isoYear');
    var N = 12;

    // Seeded random so the town is the same every visit.
    var seed = 1835;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

    // Water: the main stem runs east from the Wolf Point fork to the lake; branches run north and south.
    function water(i, j) {
      if (i >= N - 1) return 'lake';
      if (j === 5 && i >= 5) return 'river';
      if (i === 5 && j <= 5) return 'river';
      if ((i === 4 && j <= 2)) return 'river';
      if (i === 5 && j >= 5 && j <= 8) return 'river';
      if (i === 6 && j >= 9) return 'river';
      return null;
    }
    function conf() { var r = rnd(); return r < 0.5 ? 'doc' : r < 0.82 ? 'inf' : 'gue'; }

    // Each lot is a list of epochs: [from, to, height, confidence]. 1871 burns the centre.
    var lots = [];
    for (var j = 0; j < N; j++) for (var i = 0; i < N; i++) {
      if (water(i, j)) continue;
      var ep = [], d = Math.abs(i - 7) + Math.abs(j - 5);
      if ((i === 9 || i === 10) && j === 6) ep.push([1803, 0, 0.9, 'doc']);              // Fort Dearborn
      else if ((i === 8 && j === 4) || (i === 6 && j === 4)) ep.push([1804, 1871, 0.6, 'doc']); // cabins across the river
      else if (d <= 5 && rnd() < 0.62) ep.push([1828 + Math.floor(rnd() * 7), 1871, 0.4 + rnd() * 0.8, conf()]);
      var south = j >= 8 && i >= 7;
      if (south && rnd() < 0.7) ep.push([1880 + Math.floor(rnd() * 20), 0, 1.1 + rnd() * 0.8, conf()]); // Prairie Avenue
      else if (!south && rnd() < 0.78) ep.push([1873 + Math.floor(rnd() * 25), 0, 1 + rnd() * (d < 4 ? 4.5 : 2), conf()]);
      lots.push({ i: i, j: j, ep: ep });
    }

    function ease(k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
    function heightAt(lot, Y) {
      var h = 0;
      for (var n = 0; n < lot.ep.length; n++) {
        var e = lot.ep[n], g = clamp((Y - e[0]) / 4, 0, 1);
        if (e[1] && Y > e[1]) g *= clamp(1 - (Y - e[1]) / 1.2, 0, 1);
        h = Math.max(h, e[2] * ease(g));
        if (g > 0) lot.c = e[3];
      }
      return h;
    }

    // Timeline: hold at each destination, travel between them, rewind at the end.
    var stops = [1812, 1835, 1904], HOLD = 2600, TRAVEL = 2600;
    var cycle = stops.length * (HOLD + TRAVEL);
    function yearAt(t) {
      var p = t % cycle, s = Math.floor(p / (HOLD + TRAVEL)), q = p - s * (HOLD + TRAVEL);
      var a = stops[s], b = stops[(s + 1) % stops.length];
      if (q < HOLD) return { y: a, stop: a, fwd: true };
      return { y: a + (b - a) * ease((q - HOLD) / TRAVEL), stop: null, fwd: b > a };
    }

    var shade = {
      doc: ['#f3eee2', '#d3c9b4', '#a89d86'],
      inf: ['rgba(126,200,227,.92)', 'rgba(65,182,230,.62)', 'rgba(41,128,170,.62)'],
      gue: ['rgba(255,255,255,.07)', 'rgba(255,255,255,.04)', 'rgba(255,255,255,.02)']
    };
    var px = 0, py = 0, tpx = 0, tpy = 0;
    cv.addEventListener('pointermove', function (e) {
      var r = cv.getBoundingClientRect();
      tpx = (e.clientX - r.left) / r.width - 0.5; tpy = (e.clientY - r.top) / r.height - 0.5;
    });
    cv.addEventListener('pointerleave', function () { tpx = tpy = 0; });

    function poly(ctx, pts, fill, stroke, dash) {
      ctx.beginPath(); ctx.moveTo(pts[0], pts[1]);
      for (var n = 2; n < pts.length; n += 2) ctx.lineTo(pts[n], pts[n + 1]);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.setLineDash(dash || []); ctx.strokeStyle = stroke; ctx.stroke(); ctx.setLineDash([]); }
    }

    animate(cv, function (t) {
      var f = fitCanvas(cv), ctx = f.ctx, W = f.w, H = f.h;
      var st = reduce ? { y: 1835, stop: 1835 } : yearAt(t);
      var Y = st.y;
      px += (tpx - px) * 0.06; py += (tpy - py) * 0.06;
      var hw = Math.min(W * 0.84 / (2 * N), H * 0.9 / (N + 4)), hh = hw * 0.5, unit = hh * 1.5;
      var ox = W / 2 + px * 14, oy = H / 2 - N * hh + hh * 2.2 + py * 10;
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1;

      function P(i, j, z) { return [ox + (i - j) * hw, oy + (i + j) * hh - z * unit]; }

      // ground + water
      for (var j = 0; j < N; j++) for (var i = 0; i < N; i++) {
        var a = P(i, j, 0), b = P(i + 1, j, 0), c = P(i + 1, j + 1, 0), d = P(i, j + 1, 0);
        var w = water(i, j);
        if (w) {
          var sh = 0.16 + 0.08 * Math.sin(t * 0.002 + (i + j) * 0.7);
          poly(ctx, [a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1]], 'rgba(65,182,230,' + (w === 'lake' ? sh + 0.06 : sh + 0.12).toFixed(3) + ')', null);
        } else {
          poly(ctx, [a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1]], null, 'rgba(255,255,255,.06)');
        }
      }

      // buildings, back to front
      for (var n = 0; n < lots.length; n++) {
        var L = lots[n], h = heightAt(L, Y);
        if (h < 0.02) continue;
        var m = 0.16, i0 = L.i + m, j0 = L.j + m, i1 = L.i + 1 - m, j1 = L.j + 1 - m;
        var s = shade[L.c || 'doc'];
        var t0 = P(i0, j0, h), t1 = P(i1, j0, h), t2 = P(i1, j1, h), t3 = P(i0, j1, h);
        var g1 = P(i1, j0, 0), g2 = P(i1, j1, 0), g3 = P(i0, j1, 0);
        var line = L.c === 'gue' ? 'rgba(255,255,255,.55)' : L.c === 'inf' ? 'rgba(160,220,240,.5)' : 'rgba(0,0,0,.18)';
        var dash = L.c === 'gue' ? [3, 3] : null;
        poly(ctx, [t3[0], t3[1], t2[0], t2[1], g2[0], g2[1], g3[0], g3[1]], s[1], line, dash);   // left face
        poly(ctx, [t1[0], t1[1], t2[0], t2[1], g2[0], g2[1], g1[0], g1[1]], s[2], line, dash);   // right face
        poly(ctx, [t0[0], t0[1], t1[0], t1[1], t2[0], t2[1], t3[0], t3[1]], s[0], line, dash);   // roof
      }

      // the fire: a glow that passes as the year crosses October 1871
      var fire = st.fwd ? clamp(1 - Math.abs(Y - 1871.5) / 2.2, 0, 1) : 0;
      if (fire > 0) {
        var c0 = P(7, 4, 0), gr = ctx.createRadialGradient(c0[0], c0[1], 0, c0[0], c0[1], W * 0.55);
        gr.addColorStop(0, 'rgba(255,122,61,' + (0.55 * fire).toFixed(3) + ')');
        gr.addColorStop(1, 'rgba(255,59,79,0)');
        ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
      }

      if (yearEl) yearEl.textContent = Math.round(Y);
    });
  })();
})();
