/* Module 05: Grover 2-3 Qubit Half-Step Amplitude Amplification & Overshoot Sandbox */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initGrover = function initGrover(ctx) {
    const { byId, f3, pct } = ctx;
    let gState = M.groverInit(3, [5]); // 3 qubits (N=8), target |101>

    const binStr = (idx, n) => idx.toString(2).padStart(n, '0');

    function renderGroverSvgs(gm) {
      // 1. Signed amplitude bar chart + dashed mean line (bars clickable to toggle marked target!)
      const gx0 = 52, gx1 = 618, yZero = 152, scaleY = 104;
      const stepW = (gx1 - gx0) / gm.N;
      const barW = Math.min(48, stepW * 0.62);
      const targetSet = new Set(gm.targets);
      const meanY = yZero - gm.mean * scaleY;

      const barsHtml = gm.amps.map((amp, idx) => {
        const cx = gx0 + (idx + 0.5) * stepW;
        const bx = cx - barW / 2;
        const isTarget = targetSet.has(idx);
        const h = Math.max(2, Math.abs(amp) * scaleY);
        const y = amp >= 0 ? yZero - h : yZero;
        const fill = isTarget ? (amp < 0 ? 'var(--red)' : 'var(--teal)') : 'var(--blue)';
        const lblY = amp >= 0 ? y - 6 : y + h + 13;
        return `<g class="grover-bar-hit" data-grover-toggle="${idx}" style="cursor:pointer">
          <rect x="${(cx - stepW * 0.44).toFixed(1)}" y="34" width="${(stepW * 0.88).toFixed(1)}" height="222" fill="transparent"/>
          <rect x="${bx.toFixed(1)}" y="${y.toFixed(1)}" width="${barW.toFixed(1)}" height="${h.toFixed(1)}" rx="4" fill="${fill}" fill-opacity="${isTarget ? '0.92' : '0.68'}"/>
          <text x="${cx.toFixed(1)}" y="${lblY.toFixed(1)}" text-anchor="middle" fill="${fill}" font-family="var(--mono)" font-size="10.5" font-weight="700">${M.fmtFixed(amp, 2)}</text>
          <text x="${cx.toFixed(1)}" y="248" text-anchor="middle" fill="${isTarget ? 'var(--teal)' : 'var(--muted)'}" font-family="var(--mono)" font-size="10.5" font-weight="${isTarget ? '800' : '600'}">|${binStr(idx, gm.n)}⟩${isTarget ? '★' : ''}</text>
        </g>`;
      }).join('');

      byId('grover-bars-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="264" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="22" fill="var(--heading)" font-size="12" font-weight="700">带符号复振幅柱与均值反射线 μ（点击任意基态柱可增删目标 ★）</text>
        <line x1="${gx0}" y1="${yZero - scaleY}" x2="${gx1}" y2="${yZero - scaleY}" stroke="var(--svg-grid)" stroke-dasharray="3 3"/>
        <line x1="${gx0}" y1="${yZero + scaleY * 0.65}" x2="${gx1}" y2="${yZero + scaleY * 0.65}" stroke="var(--svg-grid)" stroke-dasharray="3 3"/>
        <line x1="${gx0}" y1="${yZero}" x2="${gx1}" y2="${yZero}" stroke="var(--svg-axis)" stroke-width="1.3"/>
        <text x="${gx0 - 6}" y="${yZero - scaleY + 4}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10">+1.0</text>
        <text x="${gx0 - 6}" y="${yZero + 4}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10">0.0</text>
        <text x="${gx0 - 6}" y="${yZero + scaleY * 0.65 + 4}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10">−0.65</text>
        ${barsHtml}
        <!-- Mean line -->
        <line x1="${gx0}" y1="${meanY.toFixed(1)}" x2="${gx1}" y2="${meanY.toFixed(1)}" stroke="var(--amber)" stroke-width="2" stroke-dasharray="6 4"/>
        <rect x="${gx1 - 118}" y="${(meanY - 19).toFixed(1)}" width="114" height="17" rx="4" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1"/>
        <text x="${gx1 - 61}" y="${(meanY - 7).toFixed(1)}" text-anchor="middle" fill="var(--amber)" font-family="var(--mono)" font-size="10.2" font-weight="700">均值 μ = ${M.fmtFixed(gm.mean, 3)}</text>
      `;

      // 2. Synchronized 2D {|B>, |G>} Geometric Plane SVG
      const cx = 136, cy = 140, R = 74;
      const sX = cx + R * Math.cos(gm.theta0);
      const sY = cy - R * Math.sin(gm.theta0);
      const curX = cx + R * gm.bProj;
      const curY = cy - R * gm.gProj;
      const deg = (gm.angle * 180) / Math.PI;
      const th0Deg = (gm.theta0 * 180) / Math.PI;

      byId('grover-plane-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="236" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="21" fill="var(--heading)" font-size="12" font-weight="700">{|B⟩, |G⟩} 二维几何旋转平面（每完整一步净转 +2θ₀ = ${(2 * th0Deg).toFixed(1)}°）</text>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="var(--svg-card)" stroke="var(--line-strong)" stroke-width="1.3"/>
        <line x1="${cx - R - 10}" y1="${cy}" x2="${cx + R + 12}" y2="${cy}" stroke="var(--svg-axis)" stroke-width="1.3"/>
        <line x1="${cx}" y1="${cy - R - 8}" x2="${cx}" y2="${cy + R + 8}" stroke="var(--svg-axis)" stroke-width="1.3"/>
        <text x="${cx + R + 16}" y="${cy + 4}" fill="var(--blue)" font-family="var(--mono)" font-size="11" font-weight="700">|B⟩ 非目标子空间</text>
        <text x="${cx}" y="${cy - R - 16}" text-anchor="middle" fill="var(--teal)" font-family="var(--mono)" font-size="11" font-weight="700">|G⟩ 目标子空间</text>

        <!-- Uniform state |s> reflection axis -->
        <line x1="${cx}" y1="${cy}" x2="${sX.toFixed(1)}" y2="${sY.toFixed(1)}" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="5 3"/>
        <text x="${(sX + 8).toFixed(1)}" y="${(sY - 5).toFixed(1)}" fill="var(--amber)" font-family="var(--mono)" font-size="10.5" font-weight="700">|s⟩ (θ₀=${th0Deg.toFixed(1)}°)</text>

        <!-- Current state vector -->
        <line x1="${cx}" y1="${cy}" x2="${curX.toFixed(1)}" y2="${curY.toFixed(1)}" stroke="${gm.isOvershot ? 'var(--red)' : 'var(--teal)'}" stroke-width="3.2" stroke-linecap="round"/>
        <circle cx="${curX.toFixed(1)}" cy="${curY.toFixed(1)}" r="5.5" fill="${gm.isOvershot ? 'var(--red)' : 'var(--teal)'}" stroke="var(--panel)" stroke-width="2"/>

        <!-- Right side geometry scorecard -->
        <rect x="366" y="42" width="260" height="178" rx="8" fill="var(--svg-card)" stroke="var(--line)" stroke-width="1.2"/>
        <text x="380" y="66" fill="var(--heading)" font-size="12" font-weight="700">当前几何坐标与成功概率</text>
        <text x="380" y="92" fill="var(--muted)" font-family="var(--mono)" font-size="11">当前极角 α = ${deg.toFixed(1)}°（目标 90°）</text>
        <text x="380" y="114" fill="var(--teal)" font-family="var(--mono)" font-size="11.5" font-weight="800">P(命中目标) = sin²α = ${(gm.pGood * 100).toFixed(2)}%</text>
        <text x="380" y="136" fill="var(--blue)" font-family="var(--mono)" font-size="11">P(非目标)   = cos²α = ${(gm.pBad * 100).toFixed(2)}%</text>
        <text x="380" y="160" fill="var(--muted)" font-family="var(--mono)" font-size="11">最优步数 k* = ${gm.kOpt}（峰值 ${(gm.pOpt * 100).toFixed(2)}%）</text>
        <text x="380" y="182" fill="${gm.isOvershot ? 'var(--red)' : 'var(--amber)'}" font-size="11" font-weight="700">${gm.halfPhase === 'after_oracle' ? '半拍：已完成 Oracle 翻负，请点 ② 扩散 D！' : gm.isOvershot ? '⚠ 已过旋转（过冲）：继续迭代反而转过头！' : `已完成 ${gm.fullSteps} 步完整 Grover 迭代`}</text>
        <text x="380" y="204" fill="var(--muted)" font-size="10.5">n=${gm.n} (N=${gm.N}), 目标数 M=${gm.M}</text>
      `;

      // Bind bar clicks for interactive target toggling
      byId('grover-bars-svg').querySelectorAll('[data-grover-toggle]').forEach(g => {
        g.addEventListener('click', () => {
          const idx = Number(g.getAttribute('data-grover-toggle'));
          const cur = new Set(gState.targets);
          if (cur.has(idx)) {
            if (cur.size > 1) cur.delete(idx);
          } else {
            if (cur.size < Math.min(2, gState.N - 1)) cur.add(idx);
            else {
              const first = [...cur][0];
              cur.delete(first);
              cur.add(idx);
            }
          }
          gState = M.groverInit(gState.n, [...cur]);
          updateGroverUi();
        });
      });
    }

    function updateGroverUi() {
      const gm = M.groverMetrics(gState);
      byId('grover-step-val').textContent = gm.halfPhase === 'after_oracle'
        ? `第 ${gm.fullSteps + 1} 步 · 半拍 (Oracle 后)`
        : `第 ${gm.fullSteps} 步（最优 k* = ${gm.kOpt}）`;
      byId('grover-pgood-val').textContent = `${(gm.pGood * 100).toFixed(2)}%`;
      byId('grover-mean-val').textContent = M.fmtFixed(gm.mean, 4);
      byId('grover-angle-val').textContent = `${((gm.angle * 180) / Math.PI).toFixed(1)}° (2θ₀ = ${((2 * gm.theta0 * 180) / Math.PI).toFixed(1)}°)`;
      byId('grover-bar-good').style.width = (100 * gm.pGood).toFixed(2) + '%';
      byId('grover-bar-good-out').textContent = (100 * gm.pGood).toFixed(2) + '%';

      const oracleBtn = byId('grover-oracle-btn');
      const diffBtn = byId('grover-diff-btn');
      oracleBtn.disabled = gm.halfPhase === 'after_oracle';
      diffBtn.disabled = gm.halfPhase !== 'after_oracle';

      const noteEl = byId('grover-note');
      noteEl.className = 'note-box';
      if (gm.halfPhase === 'after_oracle') {
        noteEl.classList.add('amber');
        noteEl.textContent = `半拍观察：Oracle 仅把目标态振幅翻负，此时测得目标的概率尚未变化（仍为 ${(gm.pGood * 100).toFixed(2)}%），但全场均值 μ 被拉低到 ${M.fmtFixed(gm.mean, 3)}——现在点击「② 扩散 D」看目标柱怎样被高高撬起！`;
      } else if (gm.isOvershot) {
        noteEl.classList.add('warn');
        noteEl.textContent = `⚠ 过旋转陷阱（Overshoot）：第 ${gm.fullSteps} 步已转过 |G⟩ 轴（α = ${((gm.angle * 180) / Math.PI).toFixed(1)}° > 90°），命中概率从最优 ${(gm.pOpt * 100).toFixed(2)}% 骤跌至 ${(gm.pGood * 100).toFixed(2)}%！Grover 不是“步数越多越准”。`;
      } else if (gm.fullSteps === gm.kOpt) {
        noteEl.textContent = `✓ 到达最优迭代步 k* = ${gm.kOpt}：命中概率达到峰值 ${(gm.pGood * 100).toFixed(2)}%！再多点一步试试观察“过冲跌落”。`;
      } else {
        noteEl.textContent = `均匀叠加态（或未到峰值）：推荐用「① Oracle 反相」→「② 扩散 D」两步拆解，30 秒看懂振幅放大的几何本质。`;
      }

      document.querySelectorAll('[data-grover-preset]').forEach(b => {
        const key = b.dataset.groverPreset;
        const active = (key === 'n2m1' && gm.n === 2 && gm.M === 1)
          || (key === 'n3m1' && gm.n === 3 && gm.M === 1)
          || (key === 'n3m2' && gm.n === 3 && gm.M === 2);
        b.setAttribute('aria-pressed', String(active));
      });

      renderGroverSvgs(gm);
    }

    document.querySelectorAll('[data-grover-preset]').forEach(btn => {
      btn.addEventListener('click', () => {
        const k = btn.dataset.groverPreset;
        if (k === 'n2m1') gState = M.groverInit(2, [3]);
        else if (k === 'n3m1') gState = M.groverInit(3, [5]);
        else if (k === 'n3m2') gState = M.groverInit(3, [5, 6]);
        updateGroverUi();
      });
    });

    byId('grover-oracle-btn').addEventListener('click', () => {
      gState = M.groverOracle(gState);
      updateGroverUi();
    });
    byId('grover-diff-btn').addEventListener('click', () => {
      gState = M.groverDiffusion(gState);
      updateGroverUi();
    });
    byId('grover-step-btn').addEventListener('click', () => {
      gState = M.groverStep(gState);
      updateGroverUi();
    });
    byId('grover-reset-btn').addEventListener('click', () => {
      gState = M.groverInit(gState.n, gState.targets);
      updateGroverUi();
    });

    updateGroverUi();
  };
})(window);
