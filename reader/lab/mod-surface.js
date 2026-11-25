/* Module 06: d=3 Rotated Surface Code [[9,1,3]] Interactive Error Injection & Exact MW Decoder */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initSurface = function initSurface(ctx) {
    const { byId } = ctx;
    const CYCLE = ['I', 'X', 'Z', 'Y'];
    let errors = new Array(9).fill('I');
    let showDecode = false;

    // 3x3 coordinates strictly matching handbook/assets/v2-10-surface-lattice-surgery.svg
    const coords = [
      [152, 108], [272, 108], [392, 108],
      [152, 228], [272, 228], [392, 228],
      [152, 348], [272, 348], [392, 348],
    ];

    function fmtPauliList(arr, filterFn) {
      const items = [];
      for (let i = 0; i < 9; i++) {
        if (filterFn(arr[i], i)) items.push(`${arr[i]}_${i + 1}`);
      }
      return items.length ? items.join(' · ') : 'I（无）';
    }

    function renderSurfaceSvg(an) {
      const zLitSet = new Set(an.zLit);
      const xLitSet = new Set(an.xLit);

      const zFill = id => zLitSet.has(id) ? 'var(--red)' : 'var(--blue-soft)';
      const zFillOp = id => zLitSet.has(id) ? '0.32' : '0.9';
      const zStroke = id => zLitSet.has(id) ? 'var(--red)' : 'var(--blue)';
      const zSw = id => zLitSet.has(id) ? '3' : '1.5';

      const xFill = id => xLitSet.has(id) ? 'var(--amber)' : 'var(--red-soft)';
      const xFillOp = id => xLitSet.has(id) ? '0.36' : '0.72';
      const xStroke = id => xLitSet.has(id) ? 'var(--amber)' : 'var(--red)';
      const xSw = id => xLitSet.has(id) ? '3' : '1.5';

      const beacon = (cx, cy, lit, label, kind) => {
        const col = kind === 'Z' ? (lit ? 'var(--red)' : 'var(--blue)') : (lit ? 'var(--amber)' : 'var(--red)');
        return `<g>
          ${lit ? `<circle cx="${cx}" cy="${cy}" r="18" fill="${col}" fill-opacity="0.24" stroke="${col}" stroke-width="2.2"/>` : ''}
          <text x="${cx}" y="${cy + 5}" text-anchor="middle" fill="${col}" font-family="var(--mono)" font-size="14" font-weight="800">${label}${lit ? '!' : ''}</text>
        </g>`;
      };

      // Correction overlay rings when decoded
      let corrHtml = '';
      if (showDecode) {
        for (let i = 0; i < 9; i++) {
          const cp = an.corrPaulis[i];
          if (cp === 'I') continue;
          const [qx, qy] = coords[i];
          corrHtml += `<g>
            <circle cx="${qx}" cy="${qy}" r="24" fill="none" stroke="var(--teal)" stroke-width="3.2" stroke-dasharray="5 3"/>
            <rect x="${qx + 14}" y="${qy - 28}" width="32" height="17" rx="4" fill="var(--teal)"/>
            <text x="${qx + 30}" y="${qy - 16}" text-anchor="middle" fill="var(--svg-badge-ink)" font-family="var(--mono)" font-size="10.5" font-weight="800">纠${cp}</text>
          </g>`;
        }
      }

      // Data qubits (clickable + keyboard friendly buttons below too)
      const nodesHtml = coords.map(([qx, qy], i) => {
        const err = errors[i];
        const fill = err === 'I' ? 'var(--svg-card)' : err === 'X' ? 'var(--red)' : err === 'Z' ? 'var(--blue)' : 'var(--amber)';
        const stroke = err === 'I' ? 'var(--heading)' : fill;
        const txtCol = err === 'I' ? 'var(--heading)' : 'var(--svg-badge-ink)';
        return `<g data-surface-q="${i}" style="cursor:pointer" role="button" aria-label="数据比特 ${i + 1}，当前状态 ${err}，点击循环注错">
          <circle cx="${qx}" cy="${qy}" r="17" fill="${fill}" stroke="${stroke}" stroke-width="2.2"/>
          <text x="${qx}" y="${qy + 5}" text-anchor="middle" fill="${txtCol}" font-family="var(--mono)" font-size="13" font-weight="800">${err === 'I' ? String(i + 1) : `${err}${i + 1}`}</text>
        </g>`;
      }).join('');

      byId('surface-svg').innerHTML = `
        <rect x="2" y="2" width="540" height="440" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="24" fill="var(--heading)" font-size="12.5" font-weight="700">[[9, 1, 3]] 旋转表面码棋盘格（点击任意数据比特循环 I → X → Z → Y）</text>

        <!-- Z stabilizers (detect X / Y errors) -->
        <rect x="152" y="108" width="120" height="120" fill="${zFill('Z1')}" fill-opacity="${zFillOp('Z1')}" stroke="${zStroke('Z1')}" stroke-width="${zSw('Z1')}"/>
        <rect x="272" y="228" width="120" height="120" fill="${zFill('Z2')}" fill-opacity="${zFillOp('Z2')}" stroke="${zStroke('Z2')}" stroke-width="${zSw('Z2')}"/>
        <path d="M 272 108 A 60 40 0 0 1 392 108 Z" fill="${zFill('Z3')}" fill-opacity="${zFillOp('Z3')}" stroke="${zStroke('Z3')}" stroke-width="${zSw('Z3')}"/>
        <path d="M 152 348 A 60 40 0 0 0 272 348 Z" fill="${zFill('Z4')}" fill-opacity="${zFillOp('Z4')}" stroke="${zStroke('Z4')}" stroke-width="${zSw('Z4')}"/>

        <!-- X stabilizers (detect Z / Y errors) -->
        <rect x="272" y="108" width="120" height="120" fill="${xFill('X1')}" fill-opacity="${xFillOp('X1')}" stroke="${xStroke('X1')}" stroke-width="${xSw('X1')}"/>
        <rect x="152" y="228" width="120" height="120" fill="${xFill('X2')}" fill-opacity="${xFillOp('X2')}" stroke="${xStroke('X2')}" stroke-width="${xSw('X2')}"/>
        <path d="M 152 108 A 40 60 0 0 0 152 228 Z" fill="${xFill('X3')}" fill-opacity="${xFillOp('X3')}" stroke="${xStroke('X3')}" stroke-width="${xSw('X3')}"/>
        <path d="M 392 228 A 40 60 0 0 1 392 348 Z" fill="${xFill('X4')}" fill-opacity="${xFillOp('X4')}" stroke="${xStroke('X4')}" stroke-width="${xSw('X4')}"/>

        <!-- Logical Operator Guides -->
        <line x1="152" y1="108" x2="392" y2="108" stroke="var(--red)" stroke-width="4" stroke-dasharray="10 6" opacity="0.72"/>
        <line x1="392" y1="108" x2="392" y2="348" stroke="var(--blue)" stroke-width="4" opacity="0.72"/>
        <text x="152" y="54" fill="var(--red)" font-family="var(--mono)" font-size="11.5" font-weight="700">逻辑 X̄ = X₁X₂X₃（虚线）</text>
        <text x="456" y="182" text-anchor="middle" fill="var(--blue)" font-family="var(--mono)" font-size="11.5" font-weight="700">逻辑 Z̄</text>
        <text x="456" y="198" text-anchor="middle" fill="var(--blue)" font-family="var(--mono)" font-size="11">Z₃Z₆Z₉</text>

        <!-- Stabilizer Beacons -->
        ${beacon(212, 168, zLitSet.has('Z1'), 'Z₁', 'Z')}
        ${beacon(332, 288, zLitSet.has('Z2'), 'Z₂', 'Z')}
        ${beacon(332, 88, zLitSet.has('Z3'), 'Z₃', 'Z')}
        ${beacon(212, 372, zLitSet.has('Z4'), 'Z₄', 'Z')}
        ${beacon(332, 168, xLitSet.has('X1'), 'X₁', 'X')}
        ${beacon(212, 288, xLitSet.has('X2'), 'X₂', 'X')}
        ${beacon(128, 168, xLitSet.has('X3'), 'X₃', 'X')}
        ${beacon(416, 288, xLitSet.has('X4'), 'X₄', 'X')}

        ${corrHtml}
        ${nodesHtml}

        <text x="16" y="424" fill="var(--muted)" font-size="11">蓝面 Z₁–Z₄ 检 X/Y 错 · 红面 X₁–X₄ 检 Z/Y 错 · 绿色虚圈为分别最小化 X/Z 分量所得修正链</text>
      `;

      byId('surface-svg').querySelectorAll('[data-surface-q]').forEach(g => {
        g.addEventListener('click', () => {
          const idx = Number(g.getAttribute('data-surface-q'));
          const next = CYCLE[(CYCLE.indexOf(errors[idx]) + 1) % CYCLE.length];
          errors[idx] = next;
          showDecode = false;
          updateSurfaceUi();
        });
      });
    }

    function updateSurfaceUi() {
      const an = M.surfaceAnalyze(errors);
      byId('surface-err-val').textContent = fmtPauliList(errors, p => p !== 'I');
      byId('surface-syn-val').textContent =
        `Z 症状: ${an.zLit.length ? an.zLit.join(', ') : '全 +1'} ｜ X 症状: ${an.xLit.length ? an.xLit.join(', ') : '全 +1'}`;
      byId('surface-corr-val').textContent = showDecode
        ? fmtPauliList(an.corrPaulis, p => p !== 'I')
        : '（点击“⚡ 分量解码”计算修正链）';

      const verdictEl = byId('surface-verdict-val');
      const noteEl = byId('surface-note');
      noteEl.className = 'note-box';
      if (!showDecode) {
        verdictEl.textContent = an.totalWeight === 0 ? '无错待检' : `已注入 ${an.totalWeight} 比特错 · 待解码`;
        noteEl.textContent = an.totalWeight === 0
          ? '码空间洁净：8 个稳定子全为 +1。点击左侧任意数据比特（或下方预设）注入 X / Z / Y 错误，观察症状红灯如何亮起！'
          : `已点亮 ${an.zLit.length + an.xLit.length} 盏稳定子症状灯（Z 型测 X/Y 错，X 型测 Z/Y 错）。点击「⚡ 分量解码」核查码距 d=3 能否成功救回！`;
      } else if (an.verdict === 'clean') {
        verdictEl.textContent = '✓ 无错误';
        noteEl.textContent = '无错误注入，无需修正，逻辑态保持原样。';
      } else if (an.verdict === 'corrected') {
        verdictEl.textContent = '✓ 精准纠回（残余 I）';
        noteEl.textContent = `分量解码器给出的修正 ${fmtPauliList(an.corrPaulis, p => p !== 'I')} 与物理错完全抵消（C·E = I），逻辑 X̄ 与 Z̄ 均保持不变！`;
      } else if (an.verdict === 'degenerate') {
        verdictEl.textContent = '✓ 简并纠回（差稳定子）';
        noteEl.classList.add('amber');
        noteEl.textContent = `物理纠错精妙现象——简并性（Degeneracy）！解码修正与原错不同，但二者乘积 C·E 恰好属于稳定子群 S（与 X̄、Z̄ 全对易），因此逻辑量子态仍 100% 完整无损！`;
      } else {
        const flips = [an.logicalXFlip ? '逻辑 X̄ 翻转' : '', an.logicalZFlip ? '逻辑 Z̄ 翻转' : ''].filter(Boolean).join(' + ');
        verdictEl.textContent = `✕ 解码错配：${flips}！`;
        noteEl.classList.add('warn');
        noteEl.textContent = `✕ 超出码距 d=3 纠错上限（t = ⌊(d−1)/2⌋ = 1）！残余算符 C·E 与稳定子全对易（症状已归零），却与逻辑算符反对易——触发了不可察觉的「${flips}」！`;
      }

      // Sync keyboard-accessible quick qubit buttons
      document.querySelectorAll('[data-surface-btn]').forEach(btn => {
        const idx = Number(btn.dataset.surfaceBtn);
        btn.textContent = `q${idx + 1}:${errors[idx]}`;
        btn.setAttribute('aria-pressed', String(errors[idx] !== 'I'));
      });

      renderSurfaceSvg(an);
    }

    document.querySelectorAll('[data-surface-btn]').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.dataset.surfaceBtn);
        errors[idx] = CYCLE[(CYCLE.indexOf(errors[idx]) + 1) % CYCLE.length];
        showDecode = false;
        updateSurfaceUi();
      });
    });

    document.querySelectorAll('[data-surface-preset]').forEach(btn => {
      btn.addEventListener('click', () => {
        errors = new Array(9).fill('I');
        const k = btn.dataset.surfacePreset;
        if (k === 'x5') { errors[4] = 'X'; showDecode = true; }
        else if (k === 'x4') { errors[3] = 'X'; showDecode = true; }
        else if (k === 'y5') { errors[4] = 'Y'; showDecode = true; }
        else if (k === 'x4x5') { errors[3] = 'X'; errors[4] = 'X'; showDecode = true; }
        else if (k === 'z3z6') { errors[2] = 'Z'; errors[5] = 'Z'; showDecode = true; }
        else { showDecode = false; }
        updateSurfaceUi();
      });
    });

    byId('surface-decode-btn').addEventListener('click', () => {
      showDecode = true;
      updateSurfaceUi();
    });
    byId('surface-clear-btn').addEventListener('click', () => {
      errors = new Array(9).fill('I');
      showDecode = false;
      updateSurfaceUi();
    });

    updateSurfaceUi();
  };
})(window);
