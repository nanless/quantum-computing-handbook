/* Module 03: Ramsey Detuning & Decoherence Sonification (Zero aria-live Spam, rAF Playhead, Lazy WAV) */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initRamsey = function initRamsey(ctx) {
    const { byId, f2, f4, setAudioWav, pauseAllAudio } = ctx;
    let ramseyFdet = 1.0;
    let ramseyT2 = 1.5;
    let ramseyMap = 'correct';
    let ramseyCursorT = 1.5;
    let audioReady = false;
    let rafId = null;

    const idealAudio = byId('ramsey-audio-ideal');
    const decayAudio = byId('ramsey-audio-decay');

    // Plot geometry with safe top clearance (gy1=58, ymax=0.46) so badge, asymptote pill & curves NEVER collide
    const GX0 = 56, GX1 = 616, GY0 = 246, GY1 = 58, DUR = 4.0;
    const xOf = t => GX0 + (Math.max(0, Math.min(DUR, t)) / DUR) * (GX1 - GX0);
    const yOf = env => GY0 - (env / 0.46) * (GY0 - GY1);

    function updatePlayheadOnly() {
      const curX = xOf(ramseyCursorT);
      const pt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      const isPitfall = ramseyMap === 'pitfall';
      const curY = yOf(isPitfall ? pt.envPitfall : pt.envCorrect);

      const line = byId('ramsey-playhead');
      const dot = byId('ramsey-playhead-dot');
      const box = byId('ramsey-playhead-box');
      const txt = byId('ramsey-playhead-txt');
      if (line) {
        line.setAttribute('x1', curX.toFixed(1));
        line.setAttribute('x2', curX.toFixed(1));
      }
      if (dot) {
        dot.setAttribute('cx', curX.toFixed(1));
        dot.setAttribute('cy', curY.toFixed(1));
      }
      const boxX = Math.min(GX1 - 74, Math.max(GX0 + 2, curX - 35));
      if (box) box.setAttribute('x', boxX.toFixed(1));
      if (txt) {
        txt.setAttribute('x', (boxX + 36).toFixed(1));
        txt.textContent = `t = ${f2(ramseyCursorT)}s`;
      }

      // Live numeric readout OUTSIDE aria-live so screen readers are never spammed at 4-60Hz
      byId('ramsey-t-val').textContent = `${f2(ramseyCursorT)} s`;
      byId('ramsey-v-val').textContent = f4(pt.vis);
      byId('ramsey-p0-val').textContent = f4(pt.pDecay);
      byId('ramsey-env-val').textContent = `${f4(pt.envCorrect)} vs ${f4(pt.envPitfall)}`;
    }

    function renderRamseySvg() {
      const ptsIdeal = [], ptsCorrect = [], ptsPitfall = [];
      const N = 220;
      for (let i = 0; i <= N; i++) {
        const t = (DUR * i) / N;
        const pt = M.ramseyPoint(t, ramseyFdet, ramseyT2);
        const x = xOf(t).toFixed(1);
        const cmd = i === 0 ? 'M' : 'L';
        ptsIdeal.push(`${cmd}${x} ${yOf(pt.envIdeal).toFixed(1)}`);
        ptsCorrect.push(`${cmd}${x} ${yOf(pt.envCorrect).toFixed(1)}`);
        ptsPitfall.push(`${cmd}${x} ${yOf(pt.envPitfall).toFixed(1)}`);
      }
      const asymY = yOf(0.4 * Math.SQRT1_2);
      const curX = xOf(ramseyCursorT);
      const curPt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      const isPitfall = ramseyMap === 'pitfall';
      const curY = yOf(isPitfall ? curPt.envPitfall : curPt.envCorrect);

      const cueBands = [0.0, 0.5, 1.5, 3.5].map(t => {
        const cx = xOf(t).toFixed(1);
        return `<line x1="${cx}" y1="${GY1}" x2="${cx}" y2="${GY0}" stroke="var(--svg-grid)" stroke-width="1.2" stroke-dasharray="3 3"/>`
          + `<text x="${cx}" y="${GY0 + 18}" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">${t.toFixed(1)}s</text>`;
      }).join('');

      const yTickHtml = [[0, '0.00'], [0.2, '0.20'], [0.4 * Math.SQRT1_2, '0.283'], [0.4, '0.40']].map(([v, lbl]) => {
        const yy = yOf(v).toFixed(1);
        return `<line x1="${GX0}" y1="${yy}" x2="${GX1}" y2="${yy}" stroke="var(--svg-grid)" stroke-width="1"/>`
          + `<text x="${GX0 - 7}" y="${(Number(yy) + 4).toFixed(1)}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10">${lbl}</text>`;
      }).join('');

      const boxX = Math.min(GX1 - 74, Math.max(GX0 + 2, curX - 35));

      byId('ramsey-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="292" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="21" fill="var(--heading)" font-size="12" font-weight="700">声化包络对比（点击/拖动图面定位 t）</text>
        <line x1="296" y1="17" x2="314" y2="17" stroke="var(--blue)" stroke-width="1.6" stroke-dasharray="4 3"/>
        <text x="319" y="21" fill="var(--blue)" font-family="var(--mono)" font-size="10">理想 V=1</text>
        <line x1="386" y1="17" x2="404" y2="17" stroke="var(--teal)" stroke-width="2.5"/>
        <text x="409" y="21" fill="var(--teal)" font-family="var(--mono)" font-size="10" font-weight="700">正确 0.4√P₀</text>
        <line x1="496" y1="17" x2="514" y2="17" stroke="var(--red)" stroke-width="2.2" stroke-dasharray="6 3"/>
        <text x="519" y="21" fill="var(--red)" font-family="var(--mono)" font-size="10" font-weight="700">误区 0.4V(t)</text>
        ${yTickHtml}
        ${cueBands}

        <!-- Asymptote 0.4/sqrt(2) dashed guide -->
        <line x1="${GX0}" y1="${asymY.toFixed(1)}" x2="${GX1}" y2="${asymY.toFixed(1)}" stroke="var(--teal)" stroke-width="1.3" stroke-dasharray="5 4" opacity="0.72"/>

        <line x1="${GX0}" y1="${GY0}" x2="${GX1}" y2="${GY0}" stroke="var(--svg-axis)" stroke-width="1.3"/>
        <line x1="${GX0}" y1="${GY1}" x2="${GX0}" y2="${GY0}" stroke="var(--svg-axis)" stroke-width="1.3"/>

        <path d="${ptsIdeal.join('')}" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.65"/>
        <path d="${ptsCorrect.join('')}" fill="none" stroke="var(--teal)" stroke-width="${isPitfall ? '1.8' : '2.7'}" opacity="${isPitfall ? '0.52' : '1'}"/>
        <path d="${ptsPitfall.join('')}" fill="none" stroke="var(--red)" stroke-width="${isPitfall ? '2.7' : '1.7'}" stroke-dasharray="7 4" opacity="${isPitfall ? '1' : '0.68'}"/>

        <!-- Asymptote label placed above all curves (y = 60..78 vs curve peak y = 82.5) so curves NEVER cross it -->
        <rect x="${GX1 - 186}" y="${GY1 + 2}" width="182" height="18" rx="9" fill="var(--teal-soft)" stroke="var(--teal)" stroke-width="1.1"/>
        <line x1="${GX1 - 177}" y1="${GY1 + 11}" x2="${GX1 - 163}" y2="${GY1 + 11}" stroke="var(--teal)" stroke-width="1.6" stroke-dasharray="4 2"/>
        <text x="${GX1 - 158}" y="${GY1 + 14.5}" fill="var(--teal)" font-family="var(--mono)" font-size="9.8" font-weight="700">稳态极限 0.4/√2 (P₀→1/2)</text>

        <!-- Lightweight Playhead Elements (updated by rAF without rebuilding SVG) -->
        <line id="ramsey-playhead" x1="${curX.toFixed(1)}" y1="${GY1}" x2="${curX.toFixed(1)}" y2="${GY0}" stroke="var(--amber)" stroke-width="2.0"/>
        <circle id="ramsey-playhead-dot" cx="${curX.toFixed(1)}" cy="${curY.toFixed(1)}" r="5.5" fill="${isPitfall ? 'var(--red)' : 'var(--teal)'}" stroke="var(--panel)" stroke-width="2"/>
        <rect id="ramsey-playhead-box" x="${boxX.toFixed(1)}" y="${GY1 - 24}" width="72" height="19" rx="4" fill="var(--heading)"/>
        <text id="ramsey-playhead-txt" x="${(boxX + 36).toFixed(1)}" y="${GY1 - 11}" text-anchor="middle" fill="var(--bg)" font-family="var(--mono)" font-size="10" font-weight="700">t = ${f2(ramseyCursorT)}s</text>

        <text x="16" y="282" fill="var(--muted)" font-size="11">横轴：教学时间 t (0–4.0 s) · 纵轴：合成声波瞬时振幅包络</text>
      `;
    }

    function updateRamseyStaticUi() {
      byId('ramsey-fdet-out').textContent = `${f2(ramseyFdet)} Hz`;
      byId('ramsey-t2-out').textContent = `${f2(ramseyT2)} s`;
      const isPitfall = ramseyMap === 'pitfall';
      byId('ramsey-map-correct').setAttribute('aria-pressed', String(!isPitfall));
      byId('ramsey-map-pitfall').setAttribute('aria-pressed', String(isPitfall));
      byId('ramsey-decay-title').textContent = isPitfall
        ? '退相干 Ramsey（✕ 常见误区：线性衰减 V(t)）'
        : '退相干 Ramsey（✓ 正确映射：√P₀(t)）';

      const noteEl = byId('ramsey-note');
      noteEl.className = isPitfall ? 'note-box warn' : 'note-box';
      if (isPitfall) {
        noteEl.textContent = `已切至常见误区 0.4·V(t) sin(ωt)：在 t = 3.5 s 处 V = ${f4(Math.exp(-3.5 / ramseyT2))}，声音几乎衰减到静音——这会误导读者以为退相干让量子比特“归零静音”，而实际概率是趋向 1/2 稳态混合！`;
      } else {
        noteEl.textContent = '正确映射 0.4√P₀(t) sin(ωt)（均方声能 ∝ P₀）：随退相干推进，条纹起伏缩小，但声音趋向 0.4/√2 ≈ 0.2828 的平稳常音而非静音。';
      }
      renderRamseySvg();
      updatePlayheadOnly();
    }

    let pendingSeekTarget = null;
    const pendingClips = new Set();

    function applyPendingSeek(clip) {
      if (pendingSeekTarget === null || !pendingClips.has(clip)) return;
      if (clip.readyState >= 1) {
        try { clip.currentTime = pendingSeekTarget; } catch {}
        pendingClips.delete(clip);
      }
    }

    function synthRamseyAudio(both = true, preserveCue = false) {
      audioReady = true;
      if (both) {
        const ideal = M.synthesizeRamsey(ramseyFdet, ramseyT2, 'ideal');
        setAudioWav(idealAudio, 'ramseyIdeal', ideal.bytes);
        byId('ramsey-ideal-meta').textContent = `4.00s · 22050 Hz 16-bit · Peak ${f4(ideal.peak)} · RMS ${f4(ideal.rms)}`;
        if (preserveCue && ramseyCursorT > 0) {
          pendingSeekTarget = ramseyCursorT;
          pendingClips.add(idealAudio);
          applyPendingSeek(idealAudio);
        }
      }
      const decay = M.synthesizeRamsey(ramseyFdet, ramseyT2, ramseyMap);
      setAudioWav(decayAudio, 'ramseyDecay', decay.bytes);
      byId('ramsey-decay-meta').textContent = `4.00s · 22050 Hz 16-bit · Peak ${f4(decay.peak)} · RMS ${f4(decay.rms)}`;
      if (preserveCue && ramseyCursorT > 0) {
        pendingSeekTarget = ramseyCursorT;
        pendingClips.add(decayAudio);
        applyPendingSeek(decayAudio);
      }
    }

    function startPlayheadLoop(clip) {
      if (rafId) cancelAnimationFrame(rafId);
      function tick() {
        if (clip.paused || clip.ended) {
          rafId = null;
          return;
        }
        ramseyCursorT = Math.min(DUR, Math.max(0, clip.currentTime));
        updatePlayheadOnly();
        rafId = requestAnimationFrame(tick);
      }
      rafId = requestAnimationFrame(tick);
    }

    for (const clip of [idealAudio, decayAudio]) {
      for (const evt of ['loadedmetadata', 'canplay', 'canplaythrough']) {
        clip.addEventListener(evt, () => applyPendingSeek(clip));
      }
      clip.addEventListener('play', () => startPlayheadLoop(clip));
      clip.addEventListener('pause', () => {
        if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
      });
    }

    function jumpRamseyTo(targetSec) {
      if (!audioReady) synthRamseyAudio(true, false);
      pauseAllAudio();
      ramseyCursorT = Math.max(0, Math.min(DUR, targetSec));
      pendingSeekTarget = ramseyCursorT;
      pendingClips.clear();
      for (const clip of [idealAudio, decayAudio]) {
        pendingClips.add(clip);
        applyPendingSeek(clip);
      }
      const pt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      byId('ramsey-seek-status').textContent =
        `已同步定位到 t = ${f2(ramseyCursorT)} s：理想 P₀ = ${f4(pt.pIdeal)}，退相干 P₀ = ${f4(pt.pDecay)}，包络（正确 ${f4(pt.envCorrect)} vs 误区 ${f4(pt.envPitfall)}）。`;
      updatePlayheadOnly();
    }

    // Click / drag on Ramsey SVG to scrub time cursor directly
    const rSvg = byId('ramsey-svg');
    let rScrub = false;
    function scrubT(e) {
      const rect = rSvg.getBoundingClientRect();
      if (!rect.width) return;
      const svgX = ((e.clientX - rect.left) / rect.width) * 640;
      const t = ((svgX - GX0) / (GX1 - GX0)) * DUR;
      ramseyCursorT = Math.max(0, Math.min(DUR, Math.round(t * 20) / 20));
      updatePlayheadOnly();
    }
    rSvg.style.cursor = 'ew-resize';
    rSvg.addEventListener('pointerdown', e => {
      rScrub = true;
      rSvg.setPointerCapture?.(e.pointerId);
      scrubT(e);
    });
    rSvg.addEventListener('pointermove', e => { if (rScrub) scrubT(e); });
    rSvg.addEventListener('pointerup', () => {
      if (rScrub) {
        rScrub = false;
        jumpRamseyTo(ramseyCursorT);
      }
    });

    byId('ramsey-fdet').addEventListener('input', e => {
      ramseyFdet = Number(e.target.value);
      updateRamseyStaticUi();
    });
    byId('ramsey-fdet').addEventListener('change', () => synthRamseyAudio(true));

    byId('ramsey-t2').addEventListener('input', e => {
      ramseyT2 = Number(e.target.value);
      updateRamseyStaticUi();
    });
    byId('ramsey-t2').addEventListener('change', () => synthRamseyAudio(false));

    document.querySelectorAll('[data-ramsey-map]').forEach(btn => {
      btn.addEventListener('click', () => {
        ramseyMap = btn.dataset.ramseyMap;
        updateRamseyStaticUi();
        synthRamseyAudio(false, true);
      });
    });
    document.querySelectorAll('[data-ramsey-jump]').forEach(btn => {
      btn.addEventListener('click', () => jumpRamseyTo(Number(btn.dataset.ramseyJump)));
    });
    byId('ramsey-reset').addEventListener('click', () => {
      ramseyFdet = 1.0;
      ramseyT2 = 1.5;
      ramseyMap = 'correct';
      ramseyCursorT = 1.5;
      byId('ramsey-fdet').value = '1.0';
      byId('ramsey-t2').value = '1.5';
      updateRamseyStaticUi();
      synthRamseyAudio(true);
      byId('ramsey-seek-status').textContent = '已恢复手册 A02 默认参数（f_det = 1.00 Hz, T₂ = 1.50 s, 正确映射 √P₀(t)）。';
    });

    updateRamseyStaticUi();
    byId('ramsey-seek-status').textContent = '就绪：点击时间点或直接拖动曲线游标即可同步定位两路播放器。';

    // Return lazy-init hook so hidden tab does NOT burn CPU synthesizing 2×4s PCM at page load
    return {
      onActivate() {
        if (!audioReady) synthRamseyAudio(true, false);
      },
    };
  };
})(window);
