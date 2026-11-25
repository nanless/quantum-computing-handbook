/* Quantum Lab App Shell: Theme Sync, WAI-ARIA Tabs (Arrow/Home/End), Audio Lifecycle & 6 Module Bootstrap */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = global.QuantumLabModules || {};
  const byId = id => document.getElementById(id);

  const f2 = x => M.fmtFixed(x, 2);
  const f3 = x => M.fmtFixed(x, 3);
  const f4 = x => M.fmtFixed(x, 4);
  const pct = x => (100 * Math.max(0, Math.min(1, x))).toFixed(1) + '%';
  const fmtComplex = (re, im) => {
    const r = Math.abs(re) < 5e-5 ? 0 : re;
    const i = Math.abs(im) < 5e-5 ? 0 : im;
    const sign = i >= 0 ? '+' : '−';
    return `${(r === 0 ? 0 : r).toFixed(4)} ${sign} ${Math.abs(i).toFixed(4)}i`;
  };

  // 1. Bidirectional Theme Sync (qch-theme <-> qch-lab-theme)
  const themeBtn = byId('theme-toggle');
  const themeIcon = byId('theme-icon');
  const themeLabel = byId('theme-label');

  function effectiveTheme() {
    const attr = document.documentElement.getAttribute('data-theme');
    if (attr === 'light' || attr === 'dark') return attr;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function syncThemeButton() {
    const isDark = effectiveTheme() === 'dark';
    themeBtn.setAttribute('aria-pressed', String(isDark));
    themeIcon.textContent = isDark ? '☀' : '☾';
    themeLabel.textContent = isDark ? '亮色' : '暗色';
  }

  themeBtn.addEventListener('click', () => {
    const next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try {
      localStorage.setItem('qch-theme', next);
      localStorage.setItem('qch-lab-theme', next);
    } catch {}
    syncThemeButton();
  });
  syncThemeButton();

  // 2. Blob URL Lifecycle & Exclusive Audio Playback
  const blobUrls = { mzi: null, ramseyIdeal: null, ramseyDecay: null };
  const allAudios = [byId('mzi-audio'), byId('ramsey-audio-ideal'), byId('ramsey-audio-decay')].filter(Boolean);

  function pauseAllAudio(exceptEl = null) {
    for (const a of allAudios) {
      if (a !== exceptEl && !a.paused) a.pause();
    }
  }
  for (const audio of allAudios) {
    audio.addEventListener('play', () => pauseAllAudio(audio));
  }

  function setAudioWav(audioEl, key, wavBytes) {
    audioEl.pause();
    if (blobUrls[key]) {
      URL.revokeObjectURL(blobUrls[key]);
      blobUrls[key] = null;
    }
    const url = URL.createObjectURL(new Blob([wavBytes], { type: 'audio/wav' }));
    blobUrls[key] = url;
    audioEl.src = url;
    audioEl.load();
  }

  window.addEventListener('beforeunload', () => {
    for (const key of Object.keys(blobUrls)) {
      if (blobUrls[key]) {
        URL.revokeObjectURL(blobUrls[key]);
        blobUrls[key] = null;
      }
    }
  });

  // 3. Initialize all 6 modules
  const ctx = { byId, f2, f3, f4, pct, fmtComplex, setAudioWav, pauseAllAudio };
  const hooks = {};
  if (Mods.initMzi) hooks.mzi = Mods.initMzi(ctx);
  if (Mods.initBloch) hooks.bloch = Mods.initBloch(ctx);
  if (Mods.initRamsey) hooks.ramsey = Mods.initRamsey(ctx);
  if (Mods.initChsh) hooks.chsh = Mods.initChsh(ctx);
  if (Mods.initGrover) hooks.grover = Mods.initGrover(ctx);
  if (Mods.initSurface) hooks.surface = Mods.initSurface(ctx);

  // 4. WAI-ARIA Tabs (ArrowLeft/ArrowRight/Home/End + roving tabindex + hash deep-linking)
  const tabButtons = [...document.querySelectorAll('[role="tab"]')];
  const tabPanels = {};
  for (const btn of tabButtons) {
    const key = btn.dataset.tab;
    tabPanels[key] = byId(`panel-${key}`);
  }

  function activateTab(tabKey, moveFocus = false) {
    if (!tabPanels[tabKey]) return;
    pauseAllAudio();
    for (const btn of tabButtons) {
      const active = btn.dataset.tab === tabKey;
      btn.setAttribute('aria-selected', String(active));
      btn.setAttribute('tabindex', active ? '0' : '-1');
      if (active && moveFocus) btn.focus();
    }
    for (const [key, panel] of Object.entries(tabPanels)) {
      panel.hidden = key !== tabKey;
    }
    if (hooks[tabKey] && typeof hooks[tabKey].onActivate === 'function') {
      hooks[tabKey].onActivate();
    }
  }

  for (let i = 0; i < tabButtons.length; i++) {
    const btn = tabButtons[i];
    btn.addEventListener('click', () => activateTab(btn.dataset.tab, false));
    btn.addEventListener('keydown', e => {
      let targetIdx = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') targetIdx = (i + 1) % tabButtons.length;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') targetIdx = (i - 1 + tabButtons.length) % tabButtons.length;
      else if (e.key === 'Home') targetIdx = 0;
      else if (e.key === 'End') targetIdx = tabButtons.length - 1;
      if (targetIdx !== null) {
        e.preventDefault();
        activateTab(tabButtons[targetIdx].dataset.tab, true);
      }
    });
  }

  function syncFromHash() {
    const raw = location.hash.replace(/^#/, '').replace(/^tab-/, '').replace(/^panel-/, '').toLowerCase();
    if (tabPanels[raw]) activateTab(raw, false);
  }
  window.addEventListener('hashchange', syncFromHash);
  syncFromHash();
})(window);
