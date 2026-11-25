(() => {
  'use strict';

  const root = document.getElementById('course-home');
  if (!root) return;

  // 1. Dynamic "Continue Last Reading" resume banner
  const resumeBar = document.getElementById('course-resume-bar');
  const resumeLink = document.getElementById('course-resume-link');
  const resumePct = document.getElementById('course-resume-pct');
  const resumeClose = document.getElementById('course-resume-close');
  if (resumeBar && resumeLink) {
    try {
      const raw = localStorage.getItem('qch-last-read');
      if (raw) {
        const rec = JSON.parse(raw);
        if (rec && rec.url && rec.url !== 'index.html' && rec.title) {
          resumeLink.href = rec.url;
          resumeLink.textContent = `${rec.title} →`;
          if (resumePct) {
            const p = Math.max(0, Math.min(100, Math.round(Number(rec.pct) || 0)));
            resumePct.textContent = p > 0 ? `已读 ${p}%` : '上次停留';
          }
          resumeBar.hidden = false;
        }
      }
    } catch {}
    if (resumeClose) {
      resumeClose.addEventListener('click', () => {
        resumeBar.hidden = true;
      });
    }
  }

  // 2. Hero 4-mode interactive Quantum Interference Workbench
  const scene = document.getElementById('qch-hero-sim');
  if (scene) {
    const modeButtons = [...scene.querySelectorAll('[data-course-mode]')];
    const replayBtn = scene.querySelector('[data-course-replay]');
    const reduced = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };

    const eqEl = document.getElementById('course-demo-eq');
    const lowerLbl = document.getElementById('course-lower-label');
    const phasePill = document.getElementById('course-phase-pill');
    const outWire0 = document.getElementById('course-out-wire0');
    const outWire1 = document.getElementById('course-out-wire1');
    const blochArc = document.getElementById('course-bloch-arc');
    const blochVec = document.getElementById('course-bloch-vec');
    const blochDot = document.getElementById('course-bloch-dot');
    const blochR = document.getElementById('course-bloch-r');
    const sumLeg2 = document.getElementById('course-sum-leg2');
    const sumRes = document.getElementById('course-sum-res');
    const sumDot = document.getElementById('course-sum-dot');
    const sumCap = document.getElementById('course-sum-caption');
    const barD0 = document.getElementById('course-bar-d0');
    const barD1 = document.getElementById('course-bar-d1');
    const barVal0 = document.getElementById('course-bar-val0');
    const barVal1 = document.getElementById('course-bar-val1');
    const box1 = document.getElementById('course-box-line1');
    const box2 = document.getElementById('course-box-line2');
    const box3 = document.getElementById('course-box-line3');
    const p0Out = document.getElementById('qch-hero-p0');
    const p1Out = document.getElementById('qch-hero-p1');
    const noteEl = document.getElementById('qch-hero-note');

    const MODES = {
      phi0: {
        eq: '|ψ_out⟩ = |0⟩ · V = 1.00',
        pill: 'P(0°)',
        lower: '下支路 |1⟩ · 相位 e^(i·0) = +1',
        p0: 100,
        p1: 0,
        blochX: 188,
        blochY: 362,
        blochArc: 'M 158 362 A 22 22 0 0 0 158 362',
        blochR: '|r_xy| = 1.00',
        leg2X: 436,
        leg2Y: 362,
        resX: 436,
        resY: 362,
        sumCap: '(1 + e^(i·0))/2 = 1.00',
        box1: '● D₀ 同相相长：1/2 + 1/2 = 1',
        box2: '● D₁ 反相相消：1/2 − 1/2 = 0',
        box3: '纯态干涉：两路径相位差 0°，全部概率进入 D₀',
        note: '当前模式：φ = 0° 相长干涉，两路径同相汇合，全部概率进入 D₀，D₁ 严格相消为零。',
      },
      phi90: {
        eq: '|ψ_out⟩ = (1+i)/2|0⟩ + (1−i)/2|1⟩ · V = 1.00',
        pill: 'P(90°)',
        lower: '下支路 |1⟩ · 相位 e^(iπ/2) = +i',
        p0: 50,
        p1: 50,
        blochX: 136,
        blochY: 310,
        blochArc: 'M 158 362 A 22 22 0 0 0 136 340',
        blochR: '|r_xy| = 1.00',
        leg2X: 410,
        leg2Y: 336,
        resX: 410,
        resY: 336,
        sumCap: '|(1 + i)/2| = 1/√2 → P(0)=50%',
        box1: '● D₀ 正交叠加：|(1+i)/2|² = 0.50',
        box2: '● D₁ 正交叠加：|(1−i)/2|² = 0.50',
        box3: '仍是纯态！Bloch 向量指向 +Y (|+i⟩)，相干度 V = 1',
        note: '当前模式：φ = 90°（π/2）正交叠加，两臂夹角 90°，D₀ 与 D₁ 概率严格均分 50% / 50%。',
      },
      phi180: {
        eq: '|ψ_out⟩ = |1⟩ · H·Z·H|0⟩ = |1⟩',
        pill: 'P(180°)',
        lower: '下支路 |1⟩ · 相位 e^(iπ) = −1',
        p0: 0,
        p1: 100,
        blochX: 84,
        blochY: 362,
        blochArc: 'M 158 362 A 22 22 0 1 0 114 362',
        blochR: '|r_xy| = 1.00',
        leg2X: 384,
        leg2Y: 362,
        resX: 384,
        resY: 362,
        sumCap: '(1 − 1)/2 = 0 → D₀ 彻底相消',
        box1: '● D₀ 反相相消：1/2 − 1/2 = 0',
        box2: '● D₁ 同相相长：1/2 + 1/2 = 1',
        box3: '量子算法核心引擎：仅改相对相位就把输出翻转到 |1⟩',
        note: '当前模式：φ = 180°（π）相消干涉，D₀ 振幅精确归零，全部概率转向 D₁（即 H·Z·H|0⟩ = |1⟩）。',
      },
      decohere: {
        eq: 'ρ_out = I/2 · V = 0.00（完全混态）',
        pill: 'P(φ) 失效',
        lower: '路径被环境记录 · 非对角元 ρ₀₁ = 0',
        p0: 50,
        p1: 50,
        blochX: 136,
        blochY: 362,
        blochArc: 'M 136 362 L 136 362',
        blochR: '|r_xy| = 0.00（缩至球心）',
        leg2X: 410,
        leg2Y: 362,
        resX: 384,
        resY: 362,
        sumCap: 'ρ₀₀ = 0.50 · |ρ₀₁| = 0（无交叉项）',
        box1: '● 密度矩阵 ρ = diag(0.5, 0.5)',
        box2: '● Englert 互补：D = 1 ⇒ V = 0',
        box3: '即便没人读取探测器，条纹也消失，与 φ 无关！',
        note: '当前模式：加路径测量（退相干），路径信息泄露至环境使非对角相干项 ρ₀₁ 归零，干涉彻底消失，D₀ / D₁ 锁定在经典 50% / 50%。',
      },
    };

    function playWave() {
      scene.classList.remove('course-playing');
      if (reduced.matches) return;
      void scene.offsetWidth;
      scene.classList.add('course-playing');
    }

    function applyMode(key) {
      const m = MODES[key] || MODES.phi0;
      scene.dataset.mode = key;
      for (const btn of modeButtons) {
        btn.setAttribute('aria-pressed', String(btn.dataset.courseMode === key));
      }
      if (eqEl) eqEl.textContent = m.eq;
      if (lowerLbl) lowerLbl.textContent = m.lower;
      if (phasePill) phasePill.textContent = m.pill;
      if (outWire0) {
        outWire0.setAttribute('stroke-width', m.p0 === 0 ? '1.2' : m.p0 === 100 ? '3.8' : '2.6');
        outWire0.setAttribute('stroke-dasharray', m.p0 === 0 ? '4 4' : '');
      }
      if (outWire1) {
        outWire1.setAttribute('stroke-width', m.p1 === 0 ? '1.2' : m.p1 === 100 ? '3.8' : '2.6');
        outWire1.setAttribute('stroke-dasharray', m.p1 === 0 ? '4 4' : '');
      }
      if (blochArc) blochArc.setAttribute('d', m.blochArc);
      if (blochVec) {
        blochVec.setAttribute('x2', String(m.blochX));
        blochVec.setAttribute('y2', String(m.blochY));
      }
      if (blochDot) {
        blochDot.setAttribute('cx', String(m.blochX));
        blochDot.setAttribute('cy', String(m.blochY));
      }
      if (blochR) blochR.textContent = m.blochR;
      if (sumLeg2) {
        sumLeg2.setAttribute('x2', String(m.leg2X));
        sumLeg2.setAttribute('y2', String(m.leg2Y));
        sumLeg2.style.opacity = key === 'decohere' ? '0.18' : '1';
      }
      if (sumRes) {
        sumRes.setAttribute('x2', String(m.resX));
        sumRes.setAttribute('y2', String(m.resY));
        sumRes.style.opacity = key === 'decohere' ? '0.2' : '1';
      }
      if (sumDot) {
        sumDot.setAttribute('cx', String(m.resX));
        sumDot.setAttribute('cy', String(m.resY));
      }
      if (sumCap) sumCap.textContent = m.sumCap;

      const h0 = Math.max(2, Math.round((m.p0 / 100) * 136));
      const h1 = Math.max(2, Math.round((m.p1 / 100) * 136));
      if (barD0) {
        barD0.setAttribute('y', String(264 - h0));
        barD0.setAttribute('height', String(h0));
      }
      if (barD1) {
        barD1.setAttribute('y', String(264 - h1));
        barD1.setAttribute('height', String(h1));
      }
      if (barVal0) {
        barVal0.setAttribute('y', String(264 - h0 - 7));
        barVal0.textContent = `${m.p0}%`;
      }
      if (barVal1) {
        barVal1.setAttribute('y', String(264 - h1 - 7));
        barVal1.textContent = `${m.p1}%`;
      }
      if (box1) box1.textContent = m.box1;
      if (box2) box2.textContent = m.box2;
      if (box3) box3.textContent = m.box3;
      if (p0Out) p0Out.textContent = `${m.p0}%`;
      if (p1Out) p1Out.textContent = `${m.p1}%`;
      if (noteEl) noteEl.textContent = m.note;
      playWave();
    }

    for (const btn of modeButtons) {
      btn.addEventListener('click', () => applyMode(btn.dataset.courseMode));
    }
    if (replayBtn) {
      replayBtn.hidden = reduced.matches;
      replayBtn.addEventListener('click', playWave);
    }
    if (reduced.addEventListener) {
      reduced.addEventListener('change', () => {
        if (replayBtn) replayBtn.hidden = reduced.matches;
      });
    }
    applyMode('phi0');
  }

  // 3. Bell / CHSH interactive preview toggle
  const chshWidget = root.querySelector('.course-chsh-widget');
  if (chshWidget) {
    const btns = [...chshWidget.querySelectorAll('[data-course-chsh]')];
    const status = chshWidget.querySelector('.course-chsh-result');
    const labels = {
      classic: '经典局域策略：S ≤ 2，至多赢 3/4 = 75.00%，(1,1) 局必然冲突。',
      quantum: '量子最优角：S = 2√2 ≈ 2.828，胜率 85.36%，严格击穿经典 75% 上界。',
    };
    for (const btn of btns) {
      btn.addEventListener('click', () => {
        const mode = btn.dataset.courseChsh;
        chshWidget.dataset.chsh = mode;
        for (const other of btns) other.setAttribute('aria-pressed', String(other === btn));
        if (status) status.textContent = labels[mode] || labels.quantum;
      });
    }
  }

  // 4. d=3 Surface Code interactive preview toggle
  const qecWidget = root.querySelector('.course-qec-widget');
  if (qecWidget) {
    const btns = [...qecWidget.querySelectorAll('[data-course-qec]')];
    const status = qecWidget.querySelector('.course-qec-result');
    const labels = {
      single: '单错 X₅：双 Z 面亮灯，权 1 解码精准复原（残余 I）。',
      double: '双错 X₄X₅：Z₁ 抵消仅 Z₂ 亮灯，最小权重解码误加 X₆，拼成逻辑 X̄ 翻转！',
    };
    for (const btn of btns) {
      btn.addEventListener('click', () => {
        const mode = btn.dataset.courseQec;
        qecWidget.dataset.qec = mode;
        for (const other of btns) other.setAttribute('aria-pressed', String(other === btn));
        if (status) status.textContent = labels[mode] || labels.single;
      });
    }
  }

  // 5. Synchronized multi-track quantum sonification board (MASP readiness queue pattern)
  const audioBoard = document.getElementById('course-audio-board');
  if (audioBoard) {
    const primaryClips = [...audioBoard.querySelectorAll('.course-audio-grid audio')];
    const allClips = [...audioBoard.querySelectorAll('audio')];
    for (const clip of allClips) {
      clip.addEventListener('play', () => {
        for (const other of allClips) {
          if (other !== clip && !other.paused) other.pause();
        }
      });
    }

    const jumps = audioBoard.querySelector('.course-audio-jumps');
    const seekStatus = jumps?.querySelector('.course-seek-status');
    const jumpBtns = jumps ? [...jumps.querySelectorAll('[data-course-seek]')] : [];
    const pending = new Set();
    let seekSeconds = null;

    function seekWhenReady(clip) {
      if (!pending.has(clip) || seekSeconds === null) return;
      const target = Number(seekSeconds);
      if (clip.readyState >= 1) {
        try {
          clip.currentTime = target;
        } catch {}
        pending.delete(clip);
        if (pending.size === 0 && seekStatus) {
          seekStatus.textContent = `已同步定位到 ${seekSeconds}s，请依次单轨播放对比响度与波动。`;
        }
      }
    }

    for (const clip of primaryClips) {
      for (const evt of ['loadedmetadata', 'progress', 'canplay', 'canplaythrough']) {
        clip.addEventListener(evt, () => seekWhenReady(clip));
      }
    }

    if (jumps) {
      jumps.hidden = false;
      for (const btn of jumpBtns) {
        btn.addEventListener('click', () => {
          seekSeconds = btn.dataset.courseSeek;
          for (const b of jumpBtns) b.classList.toggle('is-active', b === btn);
          if (seekStatus) seekStatus.textContent = `正在同步三轨到 ${seekSeconds}s…`;
          for (const clip of allClips) if (!clip.paused) clip.pause();
          pending.clear();
          for (const clip of primaryClips) {
            pending.add(clip);
            if (clip.readyState === 0 && clip.networkState !== HTMLMediaElement.NETWORK_LOADING) {
              clip.preload = 'auto';
              clip.load();
            }
            seekWhenReady(clip);
          }
        });
      }
    }
  }
})();
