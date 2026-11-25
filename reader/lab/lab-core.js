/* Quantum Computing Handbook · Deterministic Pure Math Kernel (6 Modules) */
(function (global) {
  'use strict';

  const INV_SQRT2 = Math.SQRT1_2;
  const BLOCH_ELEV = 19 * Math.PI / 180;
  const BLOCH_AZIM = 34 * Math.PI / 180;

  function cleanZero(x, eps = 1e-10) {
    const n = Number(x);
    if (!Number.isFinite(n) || Math.abs(n) < eps) return 0;
    return n;
  }

  function fmtFixed(x, digits = 3) {
    const v = cleanZero(x, Math.pow(10, -(digits + 1)) * 5);
    return (v === 0 ? 0 : v).toFixed(digits);
  }

  function wilsonCI(k, n, z = 1.959963984540054) {
    if (n <= 0) return { p: 0, lo: 0, hi: 0 };
    const p = k / n;
    const z2 = z * z;
    const denom = 1 + z2 / n;
    const center = (p + z2 / (2 * n)) / denom;
    const half = (z * Math.sqrt((p * (1 - p) + z2 / (4 * n)) / n)) / denom;
    return {
      p,
      lo: Math.max(0, center - half),
      hi: Math.min(1, center + half),
    };
  }

  function mulberry32(seed) {
    let a = (seed >>> 0) || 1;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ==================== 1. MZI MODEL ====================
  function mziMetrics(phiRad, visibility) {
    const V = Math.max(0, Math.min(1, visibility));
    const p0 = Math.max(0, Math.min(1, (1 + V * Math.cos(phiRad)) / 2));
    const p1 = Math.max(0, Math.min(1, (1 - V * Math.cos(phiRad)) / 2));
    const dMax = Math.sqrt(Math.max(0, 1 - V * V));
    const amp0Re = cleanZero((1 + Math.cos(phiRad)) / 2);
    const amp0Im = cleanZero(Math.sin(phiRad) / 2);
    const amp1Re = cleanZero((1 - Math.cos(phiRad)) / 2);
    const amp1Im = cleanZero(-Math.sin(phiRad) / 2);
    // Density matrix before BS2: rho_arm = [[1/2, (V/2)e^{-i phi}], [(V/2)e^{i phi}, 1/2]]
    // After BS2 = H: rho_out has diagonal (p0, p1) and off-diagonal (-i V sin(phi)/2)
    const rho00 = p0;
    const rho11 = p1;
    const rho01ArmAbs = V / 2;
    const rho01OutIm = cleanZero(-0.5 * V * Math.sin(phiRad));
    const purity = 0.5 * (1 + V * V);
    return {
      p0, p1, dMax, coh: V / 2,
      amp0Re, amp0Im, amp1Re, amp1Im,
      rho00, rho11, rho01ArmAbs, rho01OutIm, purity,
      isMixed: V < 0.995,
      visibility: V, phiRad,
    };
  }

  // ==================== 2. BLOCH SPHERE & SINGLE-QUBIT GATES ====================
  function cMul(ar, ai, br, bi) {
    return [ar * br - ai * bi, ar * bi + ai * br];
  }

  const GATES = {
    H: [
      [[INV_SQRT2, 0], [INV_SQRT2, 0]],
      [[INV_SQRT2, 0], [-INV_SQRT2, 0]],
    ],
    X: [
      [[0, 0], [1, 0]],
      [[1, 0], [0, 0]],
    ],
    Y: [
      [[0, 0], [0, -1]],
      [[0, 1], [0, 0]],
    ],
    Z: [
      [[1, 0], [0, 0]],
      [[0, 0], [-1, 0]],
    ],
    S: [
      [[1, 0], [0, 0]],
      [[0, 0], [0, 1]],
    ],
    Sdg: [
      [[1, 0], [0, 0]],
      [[0, 0], [0, -1]],
    ],
    T: [
      [[1, 0], [0, 0]],
      [[0, 0], [INV_SQRT2, INV_SQRT2]],
    ],
    Tdg: [
      [[1, 0], [0, 0]],
      [[0, 0], [INV_SQRT2, -INV_SQRT2]],
    ],
  };

  // Exact SO(3) rotation axis (unit vector) and angle (rad) for spherical surface arcs
  const GATE_ROTATIONS = {
    H: { axis: [INV_SQRT2, 0, INV_SQRT2], angle: Math.PI, label: '绕 (X+Z)/√2 轴转 π' },
    X: { axis: [1, 0, 0], angle: Math.PI, label: '绕 X 轴转 π' },
    Y: { axis: [0, 1, 0], angle: Math.PI, label: '绕 Y 轴转 π' },
    Z: { axis: [0, 0, 1], angle: Math.PI, label: '绕 Z 轴转 π' },
    S: { axis: [0, 0, 1], angle: Math.PI / 2, label: '绕 Z 轴转 +π/2' },
    Sdg: { axis: [0, 0, 1], angle: -Math.PI / 2, label: '绕 Z 轴转 −π/2' },
    T: { axis: [0, 0, 1], angle: Math.PI / 4, label: '绕 Z 轴转 +π/4' },
    Tdg: { axis: [0, 0, 1], angle: -Math.PI / 4, label: '绕 Z 轴转 −π/4' },
    Rx45: { axis: [1, 0, 0], angle: Math.PI / 4, label: '绕 X 轴转 +π/4' },
    Ry45: { axis: [0, 1, 0], angle: Math.PI / 4, label: '绕 Y 轴转 +π/4' },
    Rz45: { axis: [0, 0, 1], angle: Math.PI / 4, label: '绕 Z 轴转 +π/4' },
  };

  function rotationGateMatrix(axisName, angleRad) {
    const c = Math.cos(angleRad / 2);
    const s = Math.sin(angleRad / 2);
    if (axisName === 'X') {
      return [
        [[c, 0], [0, -s]],
        [[0, -s], [c, 0]],
      ];
    }
    if (axisName === 'Y') {
      return [
        [[c, 0], [-s, 0]],
        [[s, 0], [c, 0]],
      ];
    }
    return [
      [[Math.cos(-angleRad / 2), Math.sin(-angleRad / 2)], [0, 0]],
      [[0, 0], [Math.cos(angleRad / 2), Math.sin(angleRad / 2)]],
    ];
  }

  function rodriguesRotate(vec, axis, angleRad) {
    const [vx, vy, vz] = vec;
    const len = Math.hypot(axis[0], axis[1], axis[2]) || 1;
    const kx = axis[0] / len, ky = axis[1] / len, kz = axis[2] / len;
    const c = Math.cos(angleRad), s = Math.sin(angleRad);
    const dot = kx * vx + ky * vy + kz * vz;
    const cx = ky * vz - kz * vy;
    const cy = kz * vx - kx * vz;
    const cz = kx * vy - ky * vx;
    return [
      cleanZero(vx * c + cx * s + kx * dot * (1 - c)),
      cleanZero(vy * c + cy * s + ky * dot * (1 - c)),
      cleanZero(vz * c + cz * s + kz * dot * (1 - c)),
    ];
  }

  function sphericalArcPoints(startVec, axis, angleRad, steps = 32) {
    const pts = [];
    for (let i = 0; i <= steps; i++) {
      pts.push(rodriguesRotate(startVec, axis, (angleRad * i) / steps));
    }
    return pts;
  }

  function canonicalizeState(aRe, aIm, bRe, bIm, fallbackPhi = 0) {
    const norm = Math.hypot(aRe, aIm, bRe, bIm) || 1;
    aRe /= norm; aIm /= norm; bRe /= norm; bIm /= norm;
    const absA = Math.hypot(aRe, aIm);
    const absB = Math.hypot(bRe, bIm);
    if (absA > 1e-11) {
      const phase = Math.atan2(aIm, aRe);
      const cp = Math.cos(-phase), sp = Math.sin(-phase);
      const [naRe, naIm] = cMul(aRe, aIm, cp, sp);
      const [nbRe, nbIm] = cMul(bRe, bIm, cp, sp);
      aRe = cleanZero(Math.max(0, naRe));
      aIm = cleanZero(naIm);
      bRe = cleanZero(nbRe);
      bIm = cleanZero(nbIm);
    } else {
      aRe = 0; aIm = 0;
      const phaseB = Math.atan2(bIm, bRe);
      const cp = Math.cos(-phaseB), sp = Math.sin(-phaseB);
      const [nbRe] = cMul(bRe, bIm, cp, sp);
      bRe = cleanZero(Math.max(0, nbRe));
      bIm = 0;
    }
    const theta = 2 * Math.acos(Math.max(0, Math.min(1, aRe)));
    let phi = fallbackPhi;
    if (absA > 1e-9 && absB > 1e-9) {
      phi = Math.atan2(bIm, bRe);
      if (phi < 0) phi += 2 * Math.PI;
    }
    return { aRe, aIm, bRe, bIm, theta, phi };
  }

  function stateFromAngles(thetaRad, phiRad) {
    const c = Math.cos(thetaRad / 2);
    const s = Math.sin(thetaRad / 2);
    return canonicalizeState(c, 0, s * Math.cos(phiRad), s * Math.sin(phiRad), phiRad);
  }

  function applyMatrix(st, M) {
    const [t00r, t00i] = cMul(M[0][0][0], M[0][0][1], st.aRe, st.aIm);
    const [t01r, t01i] = cMul(M[0][1][0], M[0][1][1], st.bRe, st.bIm);
    const [t10r, t10i] = cMul(M[1][0][0], M[1][0][1], st.aRe, st.aIm);
    const [t11r, t11i] = cMul(M[1][1][0], M[1][1][1], st.bRe, st.bIm);
    return canonicalizeState(t00r + t01r, t00i + t01i, t10r + t11r, t10i + t11i, st.phi);
  }

  function applyGate(st, gateName) {
    if (gateName === 'Rx45') return applyMatrix(st, rotationGateMatrix('X', Math.PI / 4));
    if (gateName === 'Ry45') return applyMatrix(st, rotationGateMatrix('Y', Math.PI / 4));
    if (gateName === 'Rz45') return applyMatrix(st, rotationGateMatrix('Z', Math.PI / 4));
    const M = GATES[gateName];
    if (!M) return stateFromAngles(0, 0);
    return applyMatrix(st, M);
  }

  function blochVector(st) {
    const rx = cleanZero(2 * (st.aRe * st.bRe + st.aIm * st.bIm));
    const ry = cleanZero(2 * (st.aRe * st.bIm - st.aIm * st.bRe));
    const rz = cleanZero((st.aRe * st.aRe + st.aIm * st.aIm) - (st.bRe * st.bRe + st.bIm * st.bIm));
    const norm = Math.hypot(rx, ry, rz);
    return {
      rx, ry, rz, norm,
      pZ0: Math.max(0, Math.min(1, (1 + rz) / 2)),
      pZ1: Math.max(0, Math.min(1, (1 - rz) / 2)),
      pX0: Math.max(0, Math.min(1, (1 + rx) / 2)),
      pX1: Math.max(0, Math.min(1, (1 - rx) / 2)),
      pY0: Math.max(0, Math.min(1, (1 + ry) / 2)),
      pY1: Math.max(0, Math.min(1, (1 - ry) / 2)),
    };
  }

  function projectBloch(x, y, z, cx, cy, R, elev = BLOCH_ELEV, azim = BLOCH_AZIM) {
    const sa = Math.sin(elev), ca = Math.cos(elev);
    const sb = Math.sin(azim), cb = Math.cos(azim);
    const u = -sb * x + cb * y;
    const v = -sa * cb * x - sa * sb * y + ca * z;
    const depth = ca * cb * x + ca * sb * y + sa * z;
    return { sx: cx + R * u, sy: cy - R * v, depth };
  }

  function sampleMeasurement(p0, shots = 1, seed = null) {
    const rng = seed === null ? Math.random : mulberry32(seed);
    let c0 = 0;
    for (let i = 0; i < shots; i++) {
      if (rng() < p0) c0++;
    }
    const ci = wilsonCI(c0, shots);
    return { shots, c0, c1: shots - c0, freq0: c0 / shots, ci };
  }

  // ==================== 3. RAMSEY DECOHERENCE & FISHER SENSING MODEL ====================
  function ramseyPoint(t, fDet, T2) {
    const vis = Math.exp(-t / T2);
    const phase = 2 * Math.PI * fDet * t;
    const c = Math.cos(phase);
    const s = Math.sin(phase);
    const pIdeal = (1 + c) / 2;
    const pDecay = (1 + vis * c) / 2;
    // Common misconception: multiplying ideal probability by V(t) so it decays to 0 instead of 0.5
    const pWrong = vis * pIdeal;
    // Classical Fisher information F_C(phi; V) = V^2 sin^2(phi) / (1 - V^2 cos^2(phi));
    // at V = 1 (t = 0) the limit is identically 1.
    const denom = 1 - vis * vis * c * c;
    const fisherC = vis >= 1 - 1e-12
      ? 1
      : cleanZero((vis * vis * s * s) / Math.max(1e-12, denom));
    return { t, vis, phase, pIdeal, pDecay, pWrong, fisherC };
  }

  // ==================== 4. BELL STATE, PARTIAL TRACE & CHSH MODEL ====================
  function binaryEntropy(p) {
    if (p <= 1e-15 || p >= 1 - 1e-15) return 0;
    return -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p));
  }

  function bellWernerMetrics(thetaRad, pNoise) {
    const p = Math.max(0, Math.min(1, pNoise));
    const c = Math.cos(thetaRad);
    const s = Math.sin(thetaRad);
    const rz = cleanZero(p * Math.cos(2 * thetaRad));
    const rLen = Math.abs(rz);
    const lam0 = Math.max(0, Math.min(1, p * c * c + (1 - p) / 2));
    const lam1 = Math.max(0, Math.min(1, 1 - lam0));
    const entropyA = cleanZero(binaryEntropy(lam0));
    const purityA = lam0 * lam0 + lam1 * lam1;
    // Exact concurrence for rho = p |psi_theta><psi_theta| + (1-p) I/4
    const concurrence = cleanZero(Math.max(0, p * Math.abs(Math.sin(2 * thetaRad)) - (1 - p) / 2));
    // Max achievable CHSH S for this state: 2 * p * sqrt(1 + sin^2(2*theta))
    const sMax = 2 * p * Math.sqrt(1 + Math.pow(Math.sin(2 * thetaRad), 2));
    return {
      thetaRad, p,
      c, s,
      rA: { rx: 0, ry: 0, rz, r: rLen },
      rB: { rx: 0, ry: 0, rz, r: rLen },
      lam0, lam1,
      entropyA, purityA, concurrence, sMax,
    };
  }

  function chshCorrelations(thetaRad, pNoise, a0Deg, a1Deg, b0Deg, b1Deg) {
    const p = Math.max(0, Math.min(1, pNoise));
    const sin2t = Math.sin(2 * thetaRad);
    const rad = d => d * Math.PI / 180;
    const E = (ad, bd) => {
      const a = rad(ad), b = rad(bd);
      return p * (Math.cos(a) * Math.cos(b) + sin2t * Math.sin(a) * Math.sin(b));
    };
    const e00 = E(a0Deg, b0Deg);
    const e01 = E(a0Deg, b1Deg);
    const e10 = E(a1Deg, b0Deg);
    const e11 = E(a1Deg, b1Deg);
    const S = e00 + e01 + e10 - e11;
    const absS = Math.abs(S);
    const pWin00 = (1 + e00) / 2;
    const pWin01 = (1 + e01) / 2;
    const pWin10 = (1 + e10) / 2;
    const pWin11 = (1 - e11) / 2;
    const pWin = (pWin00 + pWin01 + pWin10 + pWin11) / 4; // === 0.5 + S/8
    return {
      e00, e01, e10, e11,
      S: cleanZero(S),
      absS: cleanZero(absS),
      pWin,
      pWinByPair: [pWin00, pWin01, pWin10, pWin11],
      violatesBell: S > 2 + 1e-12,
      tsirelson: 2 * Math.SQRT2,
      quantumWinBound: 0.5 + Math.SQRT2 / 4,
    };
  }

  function simulateChshRounds(thetaRad, pNoise, a0Deg, a1Deg, b0Deg, b1Deg, rounds = 1000, seed = 20261125) {
    const corr = chshCorrelations(thetaRad, pNoise, a0Deg, a1Deg, b0Deg, b1Deg);
    const rng = mulberry32(seed);
    const pairs = [
      { key: '00', pWin: corr.pWinByPair[0], n: 0, wins: 0 },
      { key: '01', pWin: corr.pWinByPair[1], n: 0, wins: 0 },
      { key: '10', pWin: corr.pWinByPair[2], n: 0, wins: 0 },
      { key: '11', pWin: corr.pWinByPair[3], n: 0, wins: 0 },
    ];
    let totalWins = 0;
    for (let i = 0; i < rounds; i++) {
      const idx = Math.floor(rng() * 4);
      const pair = pairs[idx];
      pair.n++;
      if (rng() < pair.pWin) {
        pair.wins++;
        totalWins++;
      }
    }
    const eHat = pairs.map((pr, idx) => {
      const wRate = pr.n ? pr.wins / pr.n : 0.5;
      return idx === 3 ? 1 - 2 * wRate : 2 * wRate - 1;
    });
    const sHat = eHat[0] + eHat[1] + eHat[2] - eHat[3];
    const ci = wilsonCI(totalWins, rounds);
    return {
      rounds,
      wins: totalWins,
      winRate: totalWins / rounds,
      sHat,
      ci,
      beatsClassicCI: ci.lo > 0.75,
      pairs,
    };
  }

  // ==================== 5. GROVER AMPLITUDE AMPLIFICATION MODEL ====================
  function groverInit(nQubits = 3, targets = [5]) {
    const n = nQubits === 2 ? 2 : 3;
    const N = 1 << n;
    const uniq = [...new Set(targets.map(x => ((x % N) + N) % N))].sort((a, b) => a - b);
    const validTargets = uniq.length ? uniq.slice(0, Math.max(1, N - 1)) : [N - 1];
    const amps = new Array(N).fill(1 / Math.sqrt(N));
    return {
      n,
      N,
      targets: validTargets,
      amps,
      fullSteps: 0,
      halfPhase: 'ready', // 'ready' | 'after_oracle'
    };
  }

  function groverOracle(state) {
    const targetSet = new Set(state.targets);
    const amps = state.amps.map((a, idx) => (targetSet.has(idx) ? -a : a));
    return { ...state, amps, halfPhase: 'after_oracle' };
  }

  function groverDiffusion(state) {
    const N = state.N;
    const mean = state.amps.reduce((acc, a) => acc + a, 0) / N;
    const amps = state.amps.map(a => 2 * mean - a);
    return {
      ...state,
      amps,
      fullSteps: state.fullSteps + 1,
      halfPhase: 'ready',
    };
  }

  function groverStep(state) {
    const afterO = state.halfPhase === 'after_oracle' ? state : groverOracle(state);
    return groverDiffusion(afterO);
  }

  function groverMetrics(state) {
    const { n, N, targets, amps, fullSteps, halfPhase } = state;
    const targetSet = new Set(targets);
    const M = targets.length;
    const mean = cleanZero(amps.reduce((acc, a) => acc + a, 0) / N);
    const probs = amps.map(a => a * a);
    let pGood = 0;
    let pBad = 0;
    let gProj = 0;
    let bProj = 0;
    for (let i = 0; i < N; i++) {
      if (targetSet.has(i)) {
        pGood += probs[i];
        gProj += amps[i] / Math.sqrt(M);
      } else {
        pBad += probs[i];
        bProj += amps[i] / Math.sqrt(N - M);
      }
    }
    const theta0 = Math.asin(Math.sqrt(M / N));
    const angle = Math.atan2(gProj, bProj);
    const kOpt = Math.max(1, Math.round(Math.PI / (4 * theta0) - 0.5));
    const nextAngle = (2 * (fullSteps + 1) + 1) * theta0;
    const pOpt = Math.pow(Math.sin((2 * kOpt + 1) * theta0), 2);
    const isOvershot = fullSteps > kOpt && pGood < pOpt - 0.05;
    return {
      n, N, M, targets, amps, probs,
      mean, pGood, pBad,
      gProj: cleanZero(gProj),
      bProj: cleanZero(bProj),
      theta0, angle, kOpt, pOpt, nextAngle,
      fullSteps, halfPhase, isOvershot,
    };
  }

  // ==================== 6. d=3 ROTATED SURFACE CODE [[9,1,3]] MODEL ====================
  // Exact topology matching handbook/assets/v2-10-surface-lattice-surgery.svg:
  // Data qubits 1..9 (0-indexed 0..8) in 3x3 grid:
  //   0(1)  1(2)  2(3)
  //   3(4)  4(5)  5(6)
  //   6(7)  7(8)  8(9)
  const SURFACE_D3 = {
    nData: 9,
    // Z stabilizers detect X (and Y) errors
    zStabs: [
      { id: 'Z1', label: 'Z₁', qubits: [0, 1, 3, 4], type: 'bulk' },
      { id: 'Z2', label: 'Z₂', qubits: [4, 5, 7, 8], type: 'bulk' },
      { id: 'Z3', label: 'Z₃', qubits: [1, 2], type: 'cap-top' },
      { id: 'Z4', label: 'Z₄', qubits: [6, 7], type: 'cap-bot' },
    ],
    // X stabilizers detect Z (and Y) errors
    xStabs: [
      { id: 'X1', label: 'X₁', qubits: [1, 2, 4, 5], type: 'bulk' },
      { id: 'X2', label: 'X₂', qubits: [3, 4, 6, 7], type: 'bulk' },
      { id: 'X3', label: 'X₃', qubits: [0, 3], type: 'cap-left' },
      { id: 'X4', label: 'X₄', qubits: [5, 8], type: 'cap-right' },
    ],
    logicalX: [0, 1, 2], // X_1 X_2 X_3
    logicalZ: [2, 5, 8], // Z_3 Z_6 Z_9
  };

  function maskWeight(mask) {
    let w = 0;
    let m = mask;
    while (m) {
      w += m & 1;
      m >>>= 1;
    }
    return w;
  }

  function parityOfMask(mask, qubits) {
    let p = 0;
    for (let i = 0; i < qubits.length; i++) {
      if ((mask >>> qubits[i]) & 1) p ^= 1;
    }
    return p;
  }

  function surfaceSyndromesFromMasks(errXMask, errZMask) {
    let zSyn = 0;
    const zLit = [];
    for (let i = 0; i < SURFACE_D3.zStabs.length; i++) {
      const bit = parityOfMask(errXMask, SURFACE_D3.zStabs[i].qubits);
      if (bit) {
        zSyn |= 1 << i;
        zLit.push(SURFACE_D3.zStabs[i].id);
      }
    }
    let xSyn = 0;
    const xLit = [];
    for (let i = 0; i < SURFACE_D3.xStabs.length; i++) {
      const bit = parityOfMask(errZMask, SURFACE_D3.xStabs[i].qubits);
      if (bit) {
        xSyn |= 1 << i;
        xLit.push(SURFACE_D3.xStabs[i].id);
      }
    }
    return { zSyn, xSyn, zLit, xLit };
  }

  // Precompute exact minimum-weight lookup tables for 4-bit Z-syndrome (X-correction) and X-syndrome (Z-correction)
  const MIN_WEIGHT_X_CORR = new Int32Array(16).fill(-1);
  const MIN_WEIGHT_Z_CORR = new Int32Array(16).fill(-1);
  (function buildDecoderTables() {
    const masksByWeight = [];
    for (let m = 0; m < 512; m++) masksByWeight.push(m);
    masksByWeight.sort((a, b) => maskWeight(a) - maskWeight(b) || a - b);
    for (const m of masksByWeight) {
      const { zSyn } = surfaceSyndromesFromMasks(m, 0);
      if (MIN_WEIGHT_X_CORR[zSyn] === -1) MIN_WEIGHT_X_CORR[zSyn] = m;
      const { xSyn } = surfaceSyndromesFromMasks(0, m);
      if (MIN_WEIGHT_Z_CORR[xSyn] === -1) MIN_WEIGHT_Z_CORR[xSyn] = m;
    }
  })();

  function maskToQubits(mask) {
    const list = [];
    for (let i = 0; i < 9; i++) if ((mask >>> i) & 1) list.push(i);
    return list;
  }

  function surfaceAnalyze(paulis) {
    // paulis: array of 9 strings in {'I','X','Z','Y'}
    let errX = 0;
    let errZ = 0;
    let totalWeight = 0;
    for (let i = 0; i < 9; i++) {
      const p = (paulis[i] || 'I').toUpperCase();
      if (p === 'X' || p === 'Y') errX |= 1 << i;
      if (p === 'Z' || p === 'Y') errZ |= 1 << i;
      if (p !== 'I') totalWeight++;
    }
    const { zSyn, xSyn, zLit, xLit } = surfaceSyndromesFromMasks(errX, errZ);
    const corrX = MIN_WEIGHT_X_CORR[zSyn];
    const corrZ = MIN_WEIGHT_Z_CORR[xSyn];
    const resX = errX ^ corrX;
    const resZ = errZ ^ corrZ;
    // Residual X error flips logical Z_bar iff it anti-commutes with logical Z_bar = Z3 Z6 Z9 (odd overlap)
    const logicalXFlip = parityOfMask(resX, SURFACE_D3.logicalZ) === 1;
    // Residual Z error flips logical X_bar iff it anti-commutes with logical X_bar = X1 X2 X3 (odd overlap)
    const logicalZFlip = parityOfMask(resZ, SURFACE_D3.logicalX) === 1;
    const residualSyn = surfaceSyndromesFromMasks(resX, resZ);

    let verdict = 'clean';
    if (totalWeight === 0) {
      verdict = 'clean';
    } else if (logicalXFlip || logicalZFlip) {
      verdict = 'logical_error';
    } else if (resX === 0 && resZ === 0) {
      verdict = 'corrected';
    } else {
      verdict = 'degenerate'; // residual is non-trivial stabilizer product -> harmless!
    }

    const corrPaulis = [];
    for (let i = 0; i < 9; i++) {
      const cx = (corrX >>> i) & 1;
      const cz = (corrZ >>> i) & 1;
      corrPaulis.push(cx && cz ? 'Y' : cx ? 'X' : cz ? 'Z' : 'I');
    }

    return {
      errX, errZ, totalWeight,
      zSyn, xSyn, zLit, xLit,
      corrX, corrZ, corrPaulis,
      corrXQubits: maskToQubits(corrX),
      corrZQubits: maskToQubits(corrZ),
      resX, resZ,
      residualXQubits: maskToQubits(resX),
      residualZQubits: maskToQubits(resZ),
      residualZeroSyndrome: residualSyn.zSyn === 0 && residualSyn.xSyn === 0,
      logicalXFlip,
      logicalZFlip,
      verdict,
    };
  }

  const QuantumLabModel = {
    BLOCH_ELEV, BLOCH_AZIM,
    cleanZero, fmtFixed, wilsonCI, mulberry32,
    mziMetrics,
    GATES, GATE_ROTATIONS, rotationGateMatrix, rodriguesRotate, sphericalArcPoints,
    stateFromAngles, applyGate, blochVector, projectBloch, sampleMeasurement,
    ramseyPoint,
    binaryEntropy, bellWernerMetrics, chshCorrelations, simulateChshRounds,
    groverInit, groverOracle, groverDiffusion, groverStep, groverMetrics,
    SURFACE_D3, surfaceSyndromesFromMasks, surfaceAnalyze,
  };

  global.QuantumLabModel = QuantumLabModel;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumLabModel;
  }
})(typeof window !== 'undefined' ? window : globalThis);
