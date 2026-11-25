/* Module 04: Bell State, Dual Bloch Sphere Partial-Trace Collapse & CHSH 1,000-Game Arena */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initChsh = function initChsh(ctx) {
    const { byId, f2, f3, f4, pct } = ctx;
    const formatConcurrence = value => value > 0 && value < 0.001 ? value.toExponential(3) : f4(value);
    let thetaDeg = 45;
    let pNoise = 1.0;
    let a0 = 0, a1 = 90, b0 = 45, b1 = -45;
    let simSeed = 20261125;

    function drawMiniBloch(cx, cy, R, rz, title, accentVar) {
      const tipY = cy - R * rz;
      const rLen = Math.abs(rz);
      const shrunk = rLen < 0.08;
      return `<g>
        <text x="${cx}" y="${cy - R - 18}" text-anchor="middle" fill="var(--heading)" font-size="12" font-weight="700">${title}</text>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="var(--svg-card)" stroke="var(--svg-sphere-stroke)" stroke-width="1.8"/>
        <ellipse cx="${cx}" cy="${cy}" rx="${R}" ry="${(R * 0.28).toFixed(1)}" fill="none" stroke="var(--svg-grid)" stroke-width="1.3" stroke-dasharray="4 3"/>
        <line x1="${cx}" y1="${cy - R - 8}" x2="${cx}" y2="${cy + R + 8}" stroke="var(--svg-grid)" stroke-width="1.2"/>
        <text x="${cx + 8}" y="${cy - R - 3}" fill="var(--muted)" font-family="var(--mono)" font-size="10">|0⟩</text>
        <text x="${cx + 8}" y="${cy + R + 10}" fill="var(--muted)" font-family="var(--mono)" font-size="10">|1⟩</text>
        <circle cx="${cx}" cy="${cy}" r="3.2" fill="var(--svg-axis)"/>
        ${shrunk
          ? `<circle cx="${cx}" cy="${cy}" r="9" fill="${accentVar}" fill-opacity="0.22" stroke="${accentVar}" stroke-width="2.2"/>
             <circle cx="${cx}" cy="${cy}" r="4.2" fill="${accentVar}"/>`
          : `<line x1="${cx}" y1="${cy}" x2="${cx}" y2="${tipY.toFixed(1)}" stroke="${accentVar}" stroke-width="3.2" stroke-linecap="round"/>
             <circle cx="${cx}" cy="${tipY.toFixed(1)}" r="5.5" fill="${accentVar}" stroke="var(--panel)" stroke-width="1.8"/>`}
        <text x="${cx}" y="${cy + R + 28}" text-anchor="middle" fill="${accentVar}" font-family="var(--mono)" font-size="11" font-weight="700">|r| = ${f3(rLen)} (r_z = ${M.fmtFixed(rz, 2)})</text>
      </g>`;
    }

    function renderDualBloch(bm) {
      const entPct = Math.round(bm.entropyA * 100);
      byId('chsh-bloch-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="248" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="22" fill="var(--heading)" font-size="12" font-weight="700">约化态偏迹坍缩：随纠缠增强，单比特 Bloch 矢从球面缩向球心（I/2）</text>
        ${drawMiniBloch(136, 128, 66, bm.rA.rz, 'Alice 约化态 ρ_A = Tr_B(ρ)', 'var(--teal)')}
        ${drawMiniBloch(504, 128, 66, bm.rB.rz, 'Bob 约化态 ρ_B = Tr_A(ρ)', 'var(--blue)')}
        <!-- Center entanglement bridge -->
        <rect x="234" y="62" width="172" height="132" rx="8" fill="var(--svg-card)" stroke="var(--line-strong)" stroke-width="1.2"/>
        <text x="320" y="84" text-anchor="middle" fill="var(--heading)" font-size="11.5" font-weight="700">约化态的冯·诺依曼熵 S(ρ_A)</text>
        <text x="320" y="114" text-anchor="middle" fill="var(--red)" font-family="var(--mono)" font-size="22" font-weight="800">${f3(bm.entropyA)} bit</text>
        <rect x="252" y="128" width="136" height="10" rx="5" fill="var(--stone)"/>
        <rect x="252" y="128" width="${Math.round(1.36 * entPct)}" height="10" rx="5" fill="var(--red)"/>
        <text x="320" y="158" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">纯度 Tr(ρ_A²) = ${f3(bm.purityA)}</text>
        <text x="320" y="177" text-anchor="middle" fill="${bm.concurrence > 0 ? 'var(--teal)' : 'var(--muted)'}" font-family="var(--mono)" font-size="10.8" font-weight="700">并发度 C(ρ) = ${formatConcurrence(bm.concurrence)}</text>
      `;
    }

    function renderAngleWheel(corr) {
      const cx = 134, cy = 114, R = 74;
      const ray = (deg, len, color, label, off) => {
        const rad = (deg * Math.PI) / 180;
        const x = cx + len * Math.sin(rad);
        const y = cy - len * Math.cos(rad);
        const lx = cx + (len + off) * Math.sin(rad);
        const ly = cy - (len + off) * Math.cos(rad);
        return `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${color}" stroke-width="2.6" stroke-linecap="round"/>`
          + `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="${color}"/>`
          + `<text x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" text-anchor="middle" fill="${color}" font-family="var(--mono)" font-size="10.5" font-weight="700">${label}</text>`;
      };

      const pairs = ['(0,0)', '(0,1)', '(1,0)', '(1,1)'];
      const vals = corr.pWinByPair;
      const baseY = 182;
      const maxBarH = 110;
      const barHtml = pairs.map((lbl, i) => {
        const bx = 274 + i * 80;
        const h = Math.max(2, Math.round(vals[i] * maxBarH));
        const col = vals[i] > 0.75 ? 'var(--teal)' : 'var(--blue)';
        return `<rect x="${bx}" y="${baseY - h}" width="46" height="${h}" rx="4" fill="${col}"/>`
          + `<text x="${bx + 23}" y="${baseY - h - 7}" text-anchor="middle" fill="${col}" font-family="var(--mono)" font-size="10.5" font-weight="700">${pct(vals[i])}</text>`
          + `<text x="${bx + 23}" y="${baseY + 17}" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">${lbl}</text>`;
      }).join('');
      const classicY = (baseY - 0.75 * maxBarH).toFixed(1);

      byId('chsh-game-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="218" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="21" fill="var(--heading)" font-size="12" font-weight="700">测量轴夹角（X–Z 平面）与四类提问 (x,y) 理论胜率</text>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="var(--svg-card)" stroke="var(--line-strong)" stroke-width="1.2"/>
        <line x1="${cx - R}" y1="${cy}" x2="${cx + R}" y2="${cy}" stroke="var(--svg-grid)"/>
        <line x1="${cx}" y1="${cy - R}" x2="${cx}" y2="${cy + R}" stroke="var(--svg-grid)"/>
        ${ray(a0, 62, 'var(--teal)', `a₀ ${a0}°`, 16)}
        ${ray(a1, 62, 'var(--teal)', `a₁ ${a1}°`, 16)}
        ${ray(b0, 50, 'var(--red)', `b₀ ${b0}°`, 15)}
        ${ray(b1, 50, 'var(--red)', `b₁ ${b1}°`, 15)}

        <line x1="264" y1="${baseY}" x2="622" y2="${baseY}" stroke="var(--svg-axis)" stroke-width="1.2"/>
        ${barHtml}
        <line x1="264" y1="${classicY}" x2="570" y2="${classicY}" stroke="var(--amber)" stroke-width="1.6" stroke-dasharray="5 3"/>
        <rect x="572" y="${(Number(classicY) - 9).toFixed(1)}" width="48" height="18" rx="9" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.2"/>
        <text x="596" y="${(Number(classicY) + 3.5).toFixed(1)}" text-anchor="middle" fill="var(--amber)" font-family="var(--mono)" font-size="9.5" font-weight="700">75.0%</text>
        <rect x="476" y="30" width="146" height="19" rx="9.5" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.2"/>
        <line x1="485" y1="39.5" x2="500" y2="39.5" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="4 2"/>
        <text x="505" y="43" fill="var(--amber)" font-family="var(--mono)" font-size="10" font-weight="700">经典均界 75.0%</text>
      `;
    }

    function updateChsh(clearSim = false) {
      const thetaRad = (thetaDeg * Math.PI) / 180;
      const bm = M.bellWernerMetrics(thetaRad, pNoise);
      const corr = M.chshCorrelations(thetaRad, pNoise, a0, a1, b0, b1);

      byId('chsh-theta').value = String(thetaDeg);
      byId('chsh-p').value = String(pNoise);
      byId('chsh-a0').value = String(a0);
      byId('chsh-a1').value = String(a1);
      byId('chsh-b0').value = String(b0);
      byId('chsh-b1').value = String(b1);

      byId('chsh-theta-out').textContent = `${thetaDeg}° (cos=${f3(bm.c)}, sin=${f3(bm.s)})`;
      byId('chsh-p-out').textContent = `p = ${f2(pNoise)}`;
      byId('chsh-a0-out').textContent = `${a0}°`;
      byId('chsh-a1-out').textContent = `${a1}°`;
      byId('chsh-b0-out').textContent = `${b0}°`;
      byId('chsh-b1-out').textContent = `${b1}°`;

      byId('chsh-s-val').textContent = `${f4(corr.S)}（局域界 |S| ≤ 2）`;
      byId('chsh-win-val').textContent = `${pct(corr.pWin)} (经典 ≤ 75.0%)`;
      byId('chsh-ent-val').textContent = `${f4(bm.entropyA)} bit · |r_A|=${f3(bm.rA.r)}`;
      byId('chsh-conc-val').textContent = `${formatConcurrence(bm.concurrence)} ${bm.concurrence > 0 ? '(纠缠态)' : '(可分态)'}`;

      byId('chsh-bar-win').style.width = (100 * corr.pWin).toFixed(2) + '%';
      byId('chsh-bar-win-out').textContent = pct(corr.pWin);

      const noteEl = byId('chsh-note');
      noteEl.className = 'note-box';
      if (corr.violatesBell) {
        noteEl.textContent = `理论 |S| = ${f4(corr.absS)} > 2，违背 Bell–CHSH 局域界。固定游戏规则的胜率为 ${pct(corr.pWin)}。当 S 为负时，翻转 Alice 的两个输出标签可得到高胜率的一侧。`;
      } else if (bm.concurrence > 0) {
        noteEl.classList.add('amber');
        noteEl.textContent = `当前态仍存在纠缠（C = ${formatConcurrence(bm.concurrence)} > 0），但该噪声/测量角组合的 |S| = ${f3(corr.absS)} ≤ 2，尚未击穿 CHSH 不等式（提示：Werner 态需 p > 1/√2 ≈ 0.707 且取最优角）。`;
      } else {
        noteEl.classList.add('warn');
        noteEl.textContent = `当前为可分态（C = 0）：无法违背任何 Bell 不等式，最高胜率被死死限制在 75% 以内。`;
      }

      if (clearSim) {
        byId('chsh-sim-out').textContent = '参数已变更：点击“🎲 模拟 1,000 局”重新抽样检验 95% Wilson 置信区间。';
      }
      renderDualBloch(bm);
      renderAngleWheel(corr);
    }

    function runSim1000() {
      simSeed = (simSeed + 7919) >>> 0;
      const thetaRad = (thetaDeg * Math.PI) / 180;
      const sim = M.simulateChshRounds(thetaRad, pNoise, a0, a1, b0, b1, 1000, simSeed);
      const verdict = sim.beatsClassicCI
        ? '该模型的模拟样本给出的 95% Wilson 下界高于固定规则的局域胜率上限。'
        : sim.ci.hi < 0.25
          ? '该模型的模拟样本给出的 95% Wilson 上界低于固定规则的局域胜率下限。'
          : '该模拟样本的 95% Wilson 区间与固定规则的局域胜率范围有重合。';
      byId('chsh-sim-out').textContent =
        `1,000 局模拟：胜 ${sim.wins}/1000 = ${pct(sim.winRate)} · 95% Wilson 区间 [${pct(sim.ci.lo)}, ${pct(sim.ci.hi)}] · 经验 Ŝ = ${f3(sim.sHat)}。${verdict}`;
    }

    byId('chsh-theta').addEventListener('input', e => { thetaDeg = Number(e.target.value); updateChsh(true); });
    byId('chsh-p').addEventListener('input', e => { pNoise = Number(e.target.value); updateChsh(true); });
    byId('chsh-a0').addEventListener('input', e => { a0 = Number(e.target.value); updateChsh(true); });
    byId('chsh-a1').addEventListener('input', e => { a1 = Number(e.target.value); updateChsh(true); });
    byId('chsh-b0').addEventListener('input', e => { b0 = Number(e.target.value); updateChsh(true); });
    byId('chsh-b1').addEventListener('input', e => { b1 = Number(e.target.value); updateChsh(true); });

    document.querySelectorAll('[data-chsh-preset]').forEach(btn => {
      btn.addEventListener('click', () => {
        const k = btn.dataset.chshPreset;
        if (k === 'bell') { thetaDeg = 45; pNoise = 1.0; a0 = 0; a1 = 90; b0 = 45; b1 = -45; }
        else if (k === 'product') { thetaDeg = 0; pNoise = 1.0; a0 = 0; a1 = 90; b0 = 45; b1 = -45; }
        else if (k === 'threshold') { thetaDeg = 45; pNoise = 0.71; a0 = 0; a1 = 90; b0 = 45; b1 = -45; }
        else if (k === 'separable') { thetaDeg = 45; pNoise = 0.33; a0 = 0; a1 = 90; b0 = 45; b1 = -45; }
        else if (k === 'classic-angles') { a0 = 0; a1 = 0; b0 = 0; b1 = 0; }
        updateChsh(true);
      });
    });

    byId('chsh-sim-btn').addEventListener('click', runSim1000);

    updateChsh(false);
    runSim1000();
  };
})(window);
