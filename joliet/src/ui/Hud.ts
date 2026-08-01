/**
 * Minimal HUD + loader.
 *
 * The full HUD (objectives, journal, subtitles, interaction prompts) is the UI
 * agent's territory under src/ui/. This module is the core-owned bootstrap
 * shell it builds on: loader, fatal error, and the subtitle region, which
 * exists from frame one because subtitles are a ship requirement.
 */

let root: HTMLElement | null = null;
let loader: HTMLElement | null = null;
let bar: HTMLElement | null = null;
let label: HTMLElement | null = null;

export function mountHud(): void {
  root = document.getElementById('ui');
  if (!root) return;
  root.innerHTML = `
    <div id="loader" class="loader" role="status" aria-live="polite">
      <div class="loader-inner">
        <div class="mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </div>
        <h1>Joliet</h1>
        <p class="sub">Midnight Infiltration</p>
        <div class="bar"><i id="loadbar"></i></div>
        <p class="status" id="loadlabel">Waking the building</p>
      </div>
    </div>
    <div id="subtitles" class="subtitles" aria-live="polite"></div>
    <div id="prompt" class="prompt" hidden></div>
    <div id="reticle" class="reticle" hidden></div>
  `;
  loader = document.getElementById('loader');
  bar = document.getElementById('loadbar');
  label = document.getElementById('loadlabel');
}

export function setLoadProgress(t: number, text?: string): void {
  if (bar) bar.style.width = `${Math.round(Math.max(0, Math.min(1, t)) * 100)}%`;
  if (text && label) label.textContent = text;
}

export function showLoader(text?: string): void {
  loader?.removeAttribute('hidden');
  loader?.classList.remove('gone');
  if (text && label) label.textContent = text;
}

export function hideLoader(): void {
  loader?.classList.add('gone');
  const reticle = document.getElementById('reticle');
  reticle?.removeAttribute('hidden');
  setTimeout(() => loader?.setAttribute('hidden', ''), 700);
}

/**
 * An honest notice instead of a black screen, for the cases that really are
 * unplayable.
 *
 * This used to be the touch bail-out; touch is handled now (see
 * `core/TouchControls.ts`). What is left is genuine incapability — a browser
 * with no WebGL2 and no WebGPU has nothing to render into, and telling
 * someone that is better than letting them download 5 MB and stare at an
 * unresponsive canvas.
 */
export function showUnsupportedNotice(
  heading = 'This browser cannot render it.',
  body = 'Joliet needs WebGL2 (or WebGPU). Your browser reports neither, which is usually an old version, a disabled setting, or hardware acceleration turned off.',
): void {
  const ui = document.getElementById('ui');
  if (!ui) return;
  const el = document.createElement('div');
  el.className = 'fatal';
  el.innerHTML = `
    <h1>${escapeHtml(heading)}</h1>
    <p>${escapeHtml(body)}</p>
    <p class="hint">Try a current Chrome, Edge, Firefox or Safari 17+.</p>
    <p class="hint" style="margin-top:1.2rem"><a href="../" style="color:#c9ad74">← back to the site</a></p>`;
  ui.appendChild(el);
}

/** Speaker-attributed subtitle line. Cleared after `ms`. */
export function subtitle(speaker: string, line: string, ms = 3800): void {
  const el = document.getElementById('subtitles');
  if (!el) return;
  el.innerHTML = `<p><b>${escapeHtml(speaker)}</b> ${escapeHtml(line)}</p>`;
  el.classList.add('on');
  window.setTimeout(() => el.classList.remove('on'), ms);
}

function escapeHtml(s: string): string {
  return s.replace(
    /[&<>"']/g,
    (c) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c] ?? c,
  );
}
