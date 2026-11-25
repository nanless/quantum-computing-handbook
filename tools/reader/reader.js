(() => {
  'use strict';

  const root = document.documentElement;

  // 1. Theme toggle (manual override + localStorage persistence synced with quantum-lab)
  const themeBtn = document.getElementById('theme-toggle');
  const darkQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function effectiveTheme() {
    const attr = root.getAttribute('data-theme');
    if (attr === 'dark' || attr === 'light') return attr;
    return darkQuery && darkQuery.matches ? 'dark' : 'light';
  }

  function syncThemeButton() {
    if (!themeBtn) return;
    const isDark = effectiveTheme() === 'dark';
    themeBtn.setAttribute('aria-pressed', String(isDark));
    themeBtn.setAttribute('aria-label', isDark ? '切换为亮色模式' : '切换为暗色模式');
    themeBtn.setAttribute('title', isDark ? '切换为亮色模式' : '切换为暗色模式');
    const icon = themeBtn.querySelector('.theme-icon');
    const label = themeBtn.querySelector('.theme-label');
    if (icon) icon.textContent = isDark ? '☀' : '☾';
    if (label) label.textContent = isDark ? '亮色' : '暗色';
  }

  if (themeBtn) {
    syncThemeButton();
    themeBtn.addEventListener('click', () => {
      const next = effectiveTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try {
        localStorage.setItem('qch-theme', next);
        localStorage.setItem('qch-lab-theme', next);
      } catch {}
      syncThemeButton();
    });
    if (darkQuery && darkQuery.addEventListener) {
      darkQuery.addEventListener('change', () => {
        if (!root.getAttribute('data-theme')) syncThemeButton();
      });
    }
  }

  // 2. Chapter search filter + '/' shortcut + Esc clear
  const searchInput = document.getElementById('nav-search');
  if (searchInput) {
    const navLinks = () => document.querySelectorAll('.chapters nav a');
    const applyFilter = () => {
      const q = searchInput.value.trim().toLowerCase();
      navLinks().forEach(a => {
        a.hidden = q ? !a.textContent.toLowerCase().includes(q) : false;
      });
    };
    searchInput.addEventListener('input', applyFilter);
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        if (searchInput.value) {
          searchInput.value = '';
          applyFilter();
        }
        searchInput.blur();
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || document.activeElement?.isContentEditable) return;
      e.preventDefault();
      const details = searchInput.closest('details');
      if (details) details.open = true;
      searchInput.focus();
      searchInput.select();
    });
  }

  // 3. Mobile inline TOC auto-collapse
  const inlineContents = document.querySelector('.inline-contents');
  if (inlineContents) {
    inlineContents.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        inlineContents.open = false;
      });
    });
  }

  // 4. Top 2px reading progress bar
  const progressBar = document.getElementById('qch-read-progress');
  if (progressBar) {
    let ticking = false;
    const updateProgress = () => {
      ticking = false;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = docHeight > 0 ? Math.min(1, Math.max(0, window.scrollY / docHeight)) : 0;
      progressBar.style.width = `${(ratio * 100).toFixed(2)}%`;
    };
    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updateProgress);
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    updateProgress();
  }

  // 5. Right-column TOC ScrollSpy
  const tocLinks = [...document.querySelectorAll('.contents nav a[href^="#"]')];
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const linkById = new Map();
    const targets = [];
    for (const a of tocLinks) {
      const id = decodeURIComponent(a.getAttribute('href').slice(1));
      const el = document.getElementById(id);
      if (el) {
        linkById.set(id, a);
        targets.push(el);
      }
    }
    let activeId = null;
    const setActive = id => {
      if (!id || id === activeId) return;
      activeId = id;
      for (const [k, link] of linkById) {
        const active = k === id;
        link.classList.toggle('is-active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      }
    };
    if (targets.length) {
      const visible = new Set();
      const observer = new IntersectionObserver(
        entries => {
          for (const entry of entries) {
            if (entry.isIntersecting) visible.add(entry.target);
            else visible.delete(entry.target);
          }
          if (visible.size) {
            const topMost = targets.find(t => visible.has(t));
            if (topMost) setActive(topMost.id);
          } else {
            let lastAbove = targets[0];
            for (const t of targets) {
              if (t.getBoundingClientRect().top <= 120) lastAbove = t;
              else break;
            }
            setActive(lastAbove.id);
          }
        },
        { rootMargin: '-80px 0px -65% 0px', threshold: 0 },
      );
      targets.forEach(t => observer.observe(t));
      setActive(targets[0].id);
    }
  }

  // 6. Native <dialog class="figure-lightbox"> image preview
  let lightbox = null;
  function ensureLightbox() {
    if (lightbox) return lightbox;
    const dlg = document.createElement('dialog');
    dlg.id = 'qch-lightbox';
    dlg.className = 'figure-lightbox';
    dlg.setAttribute('aria-label', '图像放大预览');
    dlg.innerHTML =
      '<div class="lightbox-shell">' +
      '<div class="lightbox-bar">' +
      '<span class="lightbox-caption"></span>' +
      '<div class="lightbox-tools">' +
      '<button type="button" class="lightbox-btn" data-lb-zoom>1:1 原始尺寸</button>' +
      '<a class="lightbox-btn lightbox-open-raw" target="_blank" rel="noopener">新标签打开原图 ↗</a>' +
      '<button type="button" class="lightbox-btn lightbox-close" data-lb-close aria-label="关闭预览">关闭 ✕</button>' +
      '</div></div>' +
      '<div class="lightbox-stage"><img alt=""></div>' +
      '</div>';
    document.body.appendChild(dlg);
    const zoomBtn = dlg.querySelector('[data-lb-zoom]');
    const closeBtn = dlg.querySelector('[data-lb-close]');
    const stage = dlg.querySelector('.lightbox-stage');
    zoomBtn.addEventListener('click', () => {
      const zoomed = stage.classList.toggle('is-zoomed');
      zoomBtn.textContent = zoomed ? '适应窗口' : '1:1 原始尺寸';
    });
    closeBtn.addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', e => {
      if (e.target === dlg) dlg.close();
    });
    lightbox = dlg;
    return dlg;
  }

  document.addEventListener('click', e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const anchor = e.target.closest?.('a.image-open');
    if (!anchor) return;
    const img = anchor.querySelector('img');
    if (!img || typeof HTMLDialogElement === 'undefined') return;
    e.preventDefault();
    const dlg = ensureLightbox();
    const stage = dlg.querySelector('.lightbox-stage');
    const preview = stage.querySelector('img');
    const cap = dlg.querySelector('.lightbox-caption');
    const rawLink = dlg.querySelector('.lightbox-open-raw');
    const zoomBtn = dlg.querySelector('[data-lb-zoom]');
    stage.classList.remove('is-zoomed');
    zoomBtn.textContent = '1:1 原始尺寸';
    preview.src = anchor.href;
    preview.alt = img.alt || '';
    cap.textContent = img.alt || '原尺寸矢量图';
    rawLink.href = anchor.href;
    if (!dlg.open) dlg.showModal();
  });

  // 7. One-click copy for code blocks and display math (raw LaTeX from annotation)
  async function copyText(str) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(str);
        return true;
      } catch {}
    }
    try {
      const ta = document.createElement('textarea');
      ta.value = str;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch {
      return false;
    }
  }

  function attachCopyButton(targetEl, label, ariaLabel, getText) {
    if (!targetEl.parentElement || targetEl.parentElement.classList.contains('copy-host')) return;
    const host = document.createElement('span');
    host.className = 'copy-host';
    targetEl.parentNode.insertBefore(host, targetEl);
    host.appendChild(targetEl);
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = label;
    btn.setAttribute('aria-label', ariaLabel);
    let timer = null;
    btn.addEventListener('click', async () => {
      const text = getText();
      if (!text) return;
      const ok = await copyText(text);
      btn.textContent = ok ? '已复制 ✓' : '复制失败';
      btn.classList.toggle('is-copied', ok);
      clearTimeout(timer);
      timer = setTimeout(() => {
        btn.textContent = label;
        btn.classList.remove('is-copied');
      }, 1600);
    });
    host.appendChild(btn);
  }

  document.querySelectorAll('article pre, .solution-body pre').forEach(pre => {
    const code = pre.querySelector('code');
    if (!code) return;
    attachCopyButton(pre, '复制', '复制代码块', () => code.textContent || '');
  });

  document.querySelectorAll('article .katex-display, .solution-body .katex-display').forEach(kd => {
    const ann = kd.querySelector('annotation[encoding="application/x-tex"]');
    if (!ann || !ann.textContent.trim()) return;
    attachCopyButton(kd, '复制 TeX', '复制 LaTeX 源码', () => ann.textContent.trim());
  });

  // 8. Chapter solutions Expand/Collapse All + auto-open on print
  const solSection = document.querySelector('.chapter-solutions');
  if (solSection) {
    const toggleBtn = solSection.querySelector('[data-solutions-toggle]');
    const items = [...solSection.querySelectorAll('details.solution-item')];
    const syncSolBtn = () => {
      if (!toggleBtn || !items.length) return;
      const allOpen = items.every(d => d.open);
      toggleBtn.textContent = allOpen ? '折叠全部解答' : '展开全部解答';
      toggleBtn.setAttribute('aria-expanded', String(allOpen));
    };
    if (toggleBtn && items.length) {
      toggleBtn.addEventListener('click', () => {
        const nextOpen = !items.every(d => d.open);
        items.forEach(d => { d.open = nextOpen; });
        syncSolBtn();
      });
      items.forEach(d => d.addEventListener('toggle', syncSolBtn));
      syncSolBtn();
    }
    window.addEventListener('beforeprint', () => {
      items.forEach(d => {
        if (!d.open) {
          d.setAttribute('data-print-opened', '1');
          d.open = true;
        }
      });
    });
    window.addEventListener('afterprint', () => {
      items.forEach(d => {
        if (d.getAttribute('data-print-opened') === '1') {
          d.open = false;
          d.removeAttribute('data-print-opened');
        }
      });
      syncSolBtn();
    });
  }

  // 9. Audio exclusive playback + Ramsey cue jump bar on labs/audio.html
  document.addEventListener(
    'play',
    e => {
      const current = e.target;
      if (!current || current.tagName !== 'AUDIO') return;
      document.querySelectorAll('audio').forEach(other => {
        if (other !== current && !other.paused) other.pause();
      });
    },
    true,
  );

  const ramseyCues = [
    { t: 0.0, label: '0.0s', tip: '初始最大峰（P0 = 1.000）' },
    { t: 0.5, label: '0.5s', tip: '首谷对照（理想 0 vs 退相干 0.142）' },
    { t: 1.5, label: '1.5s', tip: '核心例题点（理想 0 vs 退相干 0.316）' },
    { t: 3.5, label: '3.5s', tip: '尾段稳态（退相干趋近 0.5 而非静音）' },
  ];

  function seekAndPlay(audio, targetTime) {
    document.querySelectorAll('audio').forEach(other => {
      if (other !== audio && !other.paused) other.pause();
    });
    const finish = () => {
      try {
        audio.currentTime = targetTime;
      } catch {}
      audio.play().catch(() => {});
    };
    if (audio.readyState >= 1) {
      finish();
      return;
    }
    audio.preload = 'auto';
    const onReady = () => {
      audio.removeEventListener('loadedmetadata', onReady);
      audio.removeEventListener('canplay', onReady);
      finish();
    };
    audio.addEventListener('loadedmetadata', onReady, { once: true });
    audio.addEventListener('canplay', onReady, { once: true });
    audio.load();
  }

  document.querySelectorAll('audio').forEach(audio => {
    const src = audio.getAttribute('src') || '';
    if (!/ramsey-(?:ideal|decay)\.wav$/i.test(src)) return;
    const bar = document.createElement('div');
    bar.className = 'ramsey-cue-bar';
    bar.setAttribute('role', 'group');
    bar.setAttribute('aria-label', 'Ramsey 关键时刻跳转');
    const prefixLabel = document.createElement('span');
    prefixLabel.className = 'ramsey-cue-label';
    prefixLabel.textContent = '快跳：';
    bar.appendChild(prefixLabel);
    ramseyCues.forEach(cue => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ramsey-cue-btn';
      btn.textContent = cue.label;
      btn.title = cue.tip;
      btn.setAttribute('aria-label', `跳到 ${cue.label}（${cue.tip}）`);
      btn.addEventListener('click', () => {
        bar.querySelectorAll('.ramsey-cue-btn').forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        seekAndPlay(audio, cue.t);
      });
      bar.appendChild(btn);
    });
    audio.insertAdjacentElement('afterend', bar);
  });

  // 10. Landing Hero 3-state quantum interference controller
  const heroSim = document.getElementById('qch-hero-sim');
  if (heroSim) {
    const states = {
      0: {
        phaseText: 'φ = 0',
        p0: 100,
        p1: 0,
        arcD: 'M 210 132 L 222 132',
        lowerOpacity: '0.95',
        note: '两支路同相相加（1 + 1），全部概率汇入 D0，D1 严格相消归零。',
      },
      90: {
        phaseText: 'φ = π/2',
        p0: 50,
        p1: 50,
        arcD: 'M 222 132 A 12 12 0 0 0 210 120',
        lowerOpacity: '0.95',
        note: '两支路正交相差 90°（1 + i），探测器 D0 与 D1 概率严格均分 50% / 50%。',
      },
      180: {
        phaseText: 'φ = π',
        p0: 0,
        p1: 100,
        arcD: 'M 222 132 A 12 12 0 1 0 198 132',
        lowerOpacity: '0.95',
        note: '下支路反相翻转（1 − 1 = 0），D0 严格相消，全部概率转向 D1。',
      },
    };
    const buttons = [...heroSim.querySelectorAll('[data-phase]')];
    const bar0 = document.getElementById('qch-svg-bar0');
    const bar1 = document.getElementById('qch-svg-bar1');
    const val0 = document.getElementById('qch-svg-val0');
    const val1 = document.getElementById('qch-svg-val1');
    const phaseTxt = document.getElementById('qch-svg-phase-text');
    const phaseArc = document.getElementById('qch-svg-phase-arc');
    const outP0 = document.getElementById('qch-hero-p0');
    const outP1 = document.getElementById('qch-hero-p1');
    const outNote = document.getElementById('qch-hero-note');

    const applyPhase = key => {
      const st = states[key];
      if (!st) return;
      buttons.forEach(btn => {
        const active = btn.getAttribute('data-phase') === String(key);
        btn.classList.toggle('is-active', active);
        btn.setAttribute('aria-pressed', String(active));
      });
      if (bar0) bar0.setAttribute('width', String(Math.max(2, Math.round(st.p0 * 0.72))));
      if (bar1) bar1.setAttribute('width', String(Math.max(2, Math.round(st.p1 * 0.72))));
      if (val0) val0.textContent = `${st.p0}%`;
      if (val1) val1.textContent = `${st.p1}%`;
      if (phaseTxt) phaseTxt.textContent = st.phaseText;
      if (phaseArc) phaseArc.setAttribute('d', st.arcD);
      if (outP0) outP0.textContent = `${st.p0}%`;
      if (outP1) outP1.textContent = `${st.p1}%`;
      if (outNote) outNote.textContent = st.note;
    };

    buttons.forEach(btn => {
      btn.addEventListener('click', () => applyPhase(btn.getAttribute('data-phase')));
    });
    applyPhase('0');
  }
})();
