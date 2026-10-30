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

  /* ---- 4D Chicago: the reel plays while it is on screen; the film opens in a dialog ---- */
  (function () {
    var reel = document.getElementById('reel');
    var saveData = navigator.connection && navigator.connection.saveData;
    if (reel && !reduce && !saveData) {
      var tryPlay = function () { var p = reel.play(); if (p && p.catch) p.catch(function () {}); };
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (e) { if (e[0].isIntersecting) tryPlay(); else reel.pause(); }, { threshold: 0.25 }).observe(reel);
      } else tryPlay();
      document.addEventListener('visibilitychange', function () { if (document.hidden) reel.pause(); });
    }
    var dlg = document.getElementById('film'), film = document.getElementById('filmVideo');
    var close = document.getElementById('closeFilm'), title = document.getElementById('filmTitle');
    var openers = [].slice.call(document.querySelectorAll('[data-film]'));
    if (!dlg || !film || !openers.length) return;
    var current = '', V = '?v=4';
    function load(name) {
      if (name === current && film.currentSrc) return;
      current = name;
      film.pause();
      film.innerHTML = '<source src="media/' + name + '.webm' + V + '" type="video/webm"><source src="media/' + name + '.mp4' + V + '" type="video/mp4">';
      film.poster = 'media/' + name + '.jpg' + V;
      film.load();
    }
    openers.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var name = btn.getAttribute('data-film');
        if (typeof dlg.showModal !== 'function') { location.href = 'media/' + name + '.mp4'; return; }   // very old browsers
        load(name);
        if (title) title.textContent = btn.getAttribute('data-title') || '';
        dlg.showModal();
        if (reel) reel.pause();
        var p = film.play(); if (p && p.catch) p.catch(function () {});
      });
    });
    close.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () {
      film.pause();
      if (reel && !reduce && !saveData) { var p = reel.play(); if (p && p.catch) p.catch(function () {}); }
    });
  })();
})();
