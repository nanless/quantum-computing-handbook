(() => {
  'use strict';

  const root = document.documentElement;
  const readerScript = document.querySelector('script[src$="assets/reader.js"]');
  const rootPrefix = readerScript ? readerScript.getAttribute('src').replace(/assets\/reader\.js$/, '') : '';
  const isEditableFocus = () => {
    const el = document.activeElement;
    if (!el) return false;
    const tag = el.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable;
  };

  // 1. Theme toggle + bidirectional dual-variant SVG & Lightbox synchronization
  const themeBtn = document.getElementById('theme-toggle');
  const darkQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  let lightbox = null;

  function effectiveTheme() {
    const attr = root.getAttribute('data-theme');
    if (attr === 'dark' || attr === 'light') return attr;
    return darkQuery && darkQuery.matches ? 'dark' : 'light';
  }

  function syncThemedMedia() {
    const isDark = effectiveTheme() === 'dark';
    document.querySelectorAll('img[data-dark-src][data-light-src]').forEach(img => {
      const target = isDark ? img.getAttribute('data-dark-src') : img.getAttribute('data-light-src');
      if (target && img.getAttribute('src') !== target) img.setAttribute('src', target);
    });
    document.querySelectorAll('a[data-dark-href][data-light-href]').forEach(a => {
      const target = isDark ? a.getAttribute('data-dark-href') : a.getAttribute('data-light-href');
      if (target && a.getAttribute('href') !== target) a.setAttribute('href', target);
    });
    if (lightbox && lightbox.open) {
      const target = isDark ? lightbox.dataset.darkSrc : lightbox.dataset.lightSrc;
      if (target) {
        const preview = lightbox.querySelector('.lightbox-stage img');
        const rawLink = lightbox.querySelector('.lightbox-open-raw');
        if (preview) preview.src = target;
        if (rawLink) rawLink.href = target;
      }
    }
  }

  function syncThemeButton() {
    const isDark = effectiveTheme() === 'dark';
    if (themeBtn) {
      themeBtn.setAttribute('aria-pressed', String(isDark));
      themeBtn.setAttribute('aria-label', isDark ? '切换为亮色模式' : '切换为暗色模式');
      themeBtn.setAttribute('title', isDark ? '切换为亮色模式 (t)' : '切换为暗色模式 (t)');
      const icon = themeBtn.querySelector('.theme-icon');
      const label = themeBtn.querySelector('.theme-label');
      if (icon) icon.textContent = isDark ? '☀' : '☾';
      if (label) label.textContent = isDark ? '亮色' : '暗色';
    }
    syncThemedMedia();
  }

  function toggleTheme() {
    const next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try {
      localStorage.setItem('qch-theme', next);
      localStorage.setItem('qch-lab-theme', next);
    } catch {}
    syncThemeButton();
  }

  syncThemeButton();
  if (themeBtn) themeBtn.addEventListener('click', toggleTheme);
  if (darkQuery && darkQuery.addEventListener) {
    darkQuery.addEventListener('change', () => {
      if (!root.getAttribute('data-theme')) syncThemeButton();
    });
  }

  // 2. Sidebar chapter filter (hides empty .nav-label groups + offers full-book search fallback)
  const searchInput = document.getElementById('nav-search');
  const chapterDetails = document.querySelector('.chapters > details');
  if (chapterDetails) {
    if (window.matchMedia && window.matchMedia('(max-width: 760px)').matches) {
      chapterDetails.open = false;
    } else {
      const aside = chapterDetails.closest('.chapters');
      const currentNav = chapterDetails.querySelector('nav a[aria-current="page"]');
      if (aside && currentNav && aside.scrollHeight > aside.clientHeight + 4) {
        const asideRect = aside.getBoundingClientRect();
        const navRect = currentNav.getBoundingClientRect();
        const targetTop = aside.scrollTop + (navRect.top - asideRect.top) - (aside.clientHeight - navRect.height) / 2;
        aside.scrollTop = Math.max(0, Math.min(aside.scrollHeight - aside.clientHeight, targetTop));
      }
    }
  }

  if (searchInput) {
    const navEl = document.querySelector('.chapters nav');
    const emptyBox = document.createElement('div');
    emptyBox.className = 'nav-empty-state';
    emptyBox.hidden = true;
    if (navEl) navEl.appendChild(emptyBox);

    const applyFilter = () => {
      if (!navEl) return;
      const q = searchInput.value.trim().toLowerCase();
      let visibleTotal = 0;
      const children = [...navEl.children];
      let currentLabel = null;
      let groupVisible = 0;
      const flushLabel = () => {
        if (currentLabel) currentLabel.hidden = Boolean(q) && groupVisible === 0;
      };
      for (const el of children) {
        if (el === emptyBox) continue;
        if (el.classList.contains('nav-label')) {
          flushLabel();
          currentLabel = el;
          groupVisible = 0;
        } else if (el.tagName === 'A') {
          const match = !q || el.textContent.toLowerCase().includes(q);
          el.hidden = !match;
          if (match) {
            groupVisible++;
            visibleTotal++;
          }
        }
      }
      flushLabel();
      if (q && visibleTotal === 0) {
        emptyBox.hidden = false;
        emptyBox.innerHTML = '';
        const p = document.createElement('p');
        p.textContent = `目录中无「${searchInput.value.trim()}」`;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'nav-empty-search-btn';
        btn.textContent = '🔍 打开全书检索 (⌘K)';
        btn.addEventListener('click', () => openGlobalSearch(searchInput.value.trim()));
        emptyBox.append(p, btn);
      } else {
        emptyBox.hidden = true;
      }
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

  // 5. Right-column TOC ScrollSpy (auto-scrolls active item within .contents; ignores hidden targets)
  const tocContainer = document.querySelector('.contents');
  const tocLinks = [...document.querySelectorAll('.contents nav a[href^="#"]')];
  let refreshScrollSpy = () => {};
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
    const isTargetHidden = t => Boolean(t.closest('[hidden]')) || t.getClientRects().length === 0;
    let activeId = null;
    const setActive = id => {
      if (!id || id === activeId) return;
      activeId = id;
      for (const [k, link] of linkById) {
        const active = k === id;
        link.classList.toggle('is-active', active);
        if (active) {
          link.setAttribute('aria-current', 'location');
          if (tocContainer && tocContainer.scrollHeight > tocContainer.clientHeight + 4) {
            const cRect = tocContainer.getBoundingClientRect();
            const lRect = link.getBoundingClientRect();
            if (lRect.top < cRect.top + 32 || lRect.bottom > cRect.bottom - 32) {
              tocContainer.scrollTop += (lRect.top - cRect.top) - tocContainer.clientHeight * 0.35;
            }
          }
        } else {
          link.removeAttribute('aria-current');
        }
      }
    };
    if (targets.length) {
      const visible = new Set();
      const pickActive = () => {
        for (const t of targets) {
          if (isTargetHidden(t)) continue;
          if (visible.has(t)) {
            setActive(t.id);
            return;
          }
        }
        let firstShown = null;
        let lastAbove = null;
        for (const t of targets) {
          if (isTargetHidden(t)) continue;
          if (!firstShown) firstShown = t;
          if (t.getBoundingClientRect().top <= 140) lastAbove = t;
          else break;
        }
        const chosen = lastAbove || firstShown;
        if (chosen) setActive(chosen.id);
      };
      refreshScrollSpy = pickActive;
      const observer = new IntersectionObserver(
        entries => {
          for (const entry of entries) {
            if (entry.isIntersecting && !isTargetHidden(entry.target)) visible.add(entry.target);
            else visible.delete(entry.target);
          }
          pickActive();
        },
        { rootMargin: '-80px 0px -65% 0px', threshold: 0 },
      );
      targets.forEach(t => observer.observe(t));
      pickActive();
    }
  }

  // 6. Native <dialog class="figure-lightbox"> image preview (theme-aware)
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
    const originalWidth = Number(img.dataset.originalWidth) || img.naturalWidth;
    stage.style.setProperty('--figure-original-width', originalWidth > 0 ? `${originalWidth}px` : 'auto');
    stage.scrollLeft = 0;
    zoomBtn.textContent = '1:1 原始尺寸';
    const isDark = effectiveTheme() === 'dark';
    const lightSrc = img.getAttribute('data-light-src') || anchor.getAttribute('href');
    const darkSrc = img.getAttribute('data-dark-src') || lightSrc;
    const activeSrc = isDark ? darkSrc : lightSrc;
    dlg.dataset.lightSrc = lightSrc;
    dlg.dataset.darkSrc = darkSrc;
    preview.src = activeSrc;
    preview.alt = img.alt || '';
    cap.textContent = img.alt || '原尺寸矢量图';
    rawLink.href = activeSrc;
    if (!dlg.open) dlg.showModal();
  });

  // 7. Lazy-mounted one-click copy for code blocks and display math (data-tex) via IntersectionObserver
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
    if (!targetEl || targetEl.dataset.copyAttached === '1') return;
    if (!targetEl.parentElement || targetEl.parentElement.classList.contains('copy-host')) return;
    targetEl.dataset.copyAttached = '1';
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

  function mountCopyTarget(el) {
    if (el.tagName === 'PRE') {
      const code = el.querySelector('code');
      if (code) attachCopyButton(el, '复制', '复制代码块', () => code.textContent || '');
    } else if (el.classList.contains('katex-display')) {
      const getTex = () => (
        el.getAttribute('data-tex') ||
        el.querySelector('annotation[encoding="application/x-tex"]')?.textContent ||
        ''
      ).trim();
      if (getTex()) attachCopyButton(el, '复制 TeX', '复制 LaTeX 源码', getTex);
    }
  }

  const copyCandidates = [
    ...document.querySelectorAll('main > article pre, .solution-body pre, .ex-answer-body pre, .ex-hint-body pre'),
    ...document.querySelectorAll('main > article .katex-display[data-tex], .solution-body .katex-display[data-tex], .ex-answer-body .katex-display[data-tex], .ex-hint-body .katex-display[data-tex]'),
  ];
  if (copyCandidates.length) {
    if ('IntersectionObserver' in window) {
      const copyObs = new IntersectionObserver(
        entries => {
          for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            copyObs.unobserve(entry.target);
            mountCopyTarget(entry.target);
          }
        },
        { rootMargin: '260px 0px' },
      );
      copyCandidates.forEach(el => copyObs.observe(el));
    } else {
      copyCandidates.forEach(mountCopyTarget);
    }
  }

  // 8. Chapter solutions Expand/Collapse All (supports both 1-level and 2-level hint+answer cards)
  const solSection = document.querySelector('.chapter-solutions');
  if (solSection) {
    const toggleBtn = solSection.querySelector('[data-solutions-toggle]');
    const items = [...solSection.querySelectorAll('details.solution-item, details.ex-hint-box, details.ex-answer-box')];
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
  }

  // Auto-open all collapsible solutions & exercises during print, restoring afterwards.
  window.addEventListener('beforeprint', () => {
    document.querySelectorAll('details.solution-item, details.ex-chapter, details.ex-hint-box, details.ex-answer-box').forEach(d => {
      if (!d.open) {
        d.setAttribute('data-print-opened', '1');
        d.open = true;
      }
    });
  });
  window.addEventListener('afterprint', () => {
    document.querySelectorAll('details[data-print-opened="1"]').forEach(d => {
      d.open = false;
      d.removeAttribute('data-print-opened');
    });
  });

  // 9. Zero-dependency Offline Full-Book Search Modal (Cmd/Ctrl+K, '/', and [data-open-search])
  let searchDialog = null;
  let searchCategory = 'all';
  let searchResults = [];
  let searchSelected = 0;

  const KIND_LABELS = { ch: '章节', sec: '小节', term: '术语', lab: '实验' };

  function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function appendHighlighted(parent, text, tokens) {
    if (!tokens.length || !text) {
      parent.textContent = text || '';
      return;
    }
    const re = new RegExp(`(${tokens.map(escapeRegExp).join('|')})`, 'gi');
    const parts = text.split(re);
    for (let i = 0; i < parts.length; i++) {
      if (!parts[i]) continue;
      if (i % 2 === 1) {
        const mark = document.createElement('mark');
        mark.textContent = parts[i];
        parent.appendChild(mark);
      } else {
        parent.appendChild(document.createTextNode(parts[i]));
      }
    }
  }

  function ensureSearchDialog() {
    if (searchDialog) return searchDialog;
    const dlg = document.createElement('dialog');
    dlg.id = 'qch-search-dialog';
    dlg.className = 'search-modal';
    dlg.setAttribute('aria-label', '全书离线检索');
    dlg.innerHTML =
      '<div class="search-modal-shell">' +
        '<div class="search-modal-head">' +
          '<span class="search-modal-icon" aria-hidden="true">🔍</span>' +
          '<input type="search" id="qch-global-search-input" class="search-modal-input" role="combobox" aria-label="搜索全书" aria-controls="qch-search-results" aria-autocomplete="list" aria-expanded="false" autocomplete="off" placeholder="搜索全书 26 章、1,300+ 小节、术语与实验（如：表面码、Barren Plateau、Weyl 室、CHSH）…">' +
          '<button type="button" class="search-modal-close" data-search-close aria-label="关闭检索">Esc</button>' +
        '</div>' +
        '<div class="search-cat-bar" role="group" aria-label="按内容类型筛选">' +
          '<button type="button" class="search-cat-btn is-active" data-search-cat="all" aria-pressed="true">全部</button>' +
          '<button type="button" class="search-cat-btn" data-search-cat="ch" aria-pressed="false">章节</button>' +
          '<button type="button" class="search-cat-btn" data-search-cat="sec" aria-pressed="false">小节</button>' +
          '<button type="button" class="search-cat-btn" data-search-cat="term" aria-pressed="false">术语</button>' +
          '<button type="button" class="search-cat-btn" data-search-cat="lab" aria-pressed="false">实验</button>' +
          '<span class="search-count" id="qch-search-count" role="status"></span>' +
        '</div>' +
        '<div class="search-results" id="qch-search-results" role="listbox" aria-label="检索结果"></div>' +
        '<div class="search-modal-foot"><span><kbd>↑</kbd><kbd>↓</kbd> 选择 · <kbd>Enter</kbd> 跳转 · <kbd>Esc</kbd> 关闭</span><span>100% 离线本地索引 · 零网络请求</span></div>' +
      '</div>';
    document.body.appendChild(dlg);

    const input = dlg.querySelector('#qch-global-search-input');
    const resultsEl = dlg.querySelector('#qch-search-results');
    const countEl = dlg.querySelector('#qch-search-count');
    const catBtns = [...dlg.querySelectorAll('[data-search-cat]')];

    const renderList = () => {
      const qRaw = input.value.trim();
      const tokens = qRaw.toLowerCase().split(/\s+/).filter(Boolean);
      const idx = Array.isArray(window.__QCH_SEARCH_INDEX__) ? window.__QCH_SEARCH_INDEX__ : [];
      const scored = [];
      for (const item of idx) {
        if (searchCategory !== 'all' && item.k !== searchCategory) continue;
        if (!tokens.length) {
          if (item.k === 'ch' || item.k === 'lab') scored.push({ item, score: item.k === 'lab' ? 5 : 10 });
          continue;
        }
        const tLow = (item.t || '').toLowerCase();
        const pLow = (item.p || '').toLowerCase();
        const sLow = (item.s || '').toLowerCase();
        const combined = tLow + ' ' + pLow + ' ' + sLow;
        let ok = true;
        let score = 0;
        for (const tok of tokens) {
          if (!combined.includes(tok)) { ok = false; break; }
          if (tLow === tok) score += 120;
          else if (tLow.startsWith(tok)) score += 60;
          else if (tLow.includes(tok)) score += 36;
          else if (pLow.includes(tok)) score += 14;
          else score += 6;
        }
        if (!ok) continue;
        if (item.k === 'term') score += 14;
        if (item.k === 'ch') score += 10;
        if (item.k === 'lab') score += 8;
        scored.push({ item, score });
      }
      scored.sort((a, b) => b.score - a.score);
      searchResults = scored.slice(0, 48).map(x => x.item);
      searchSelected = 0;
      countEl.textContent = tokens.length
        ? `命中 ${scored.length} 条${scored.length > 48 ? '（显示前 48 条）' : ''}`
        : `共索引 ${idx.length} 条（输入中英文关键词即可检索）`;

      resultsEl.innerHTML = '';
      input.removeAttribute('aria-activedescendant');
      input.setAttribute('aria-expanded', String(searchResults.length > 0));
      if (!searchResults.length) {
        const empty = document.createElement('div');
        empty.className = 'search-empty';
        empty.textContent = tokens.length ? `未找到包含「${qRaw}」的条目，可尝试换词或切换“全部”分类。` : '输入关键词开始搜索，如：表面码、Barren Plateau、Weyl 室、Grover、CHSH。';
        resultsEl.appendChild(empty);
        return;
      }

      searchResults.forEach((item, i) => {
        const a = document.createElement('a');
        a.className = 'search-item' + (i === 0 ? ' is-selected' : '');
        a.id = `qch-search-option-${i}`;
        a.tabIndex = -1;
        a.setAttribute('role', 'option');
        a.setAttribute('aria-selected', String(i === 0));
        a.href = rootPrefix + item.u;
        const top = document.createElement('div');
        top.className = 'search-item-top';
        const badge = document.createElement('span');
        badge.className = `search-badge search-badge-${item.k}`;
        badge.textContent = KIND_LABELS[item.k] || '正文';
        const titleEl = document.createElement('strong');
        titleEl.className = 'search-item-title';
        appendHighlighted(titleEl, item.t, tokens);
        const pageEl = document.createElement('span');
        pageEl.className = 'search-item-page';
        pageEl.textContent = item.p;
        top.append(badge, titleEl, pageEl);
        a.appendChild(top);
        if (item.s) {
          const snip = document.createElement('p');
          snip.className = 'search-item-snip';
          appendHighlighted(snip, item.s, tokens);
          a.appendChild(snip);
        }
        a.addEventListener('click', () => dlg.close());
        resultsEl.appendChild(a);
      });
      input.setAttribute('aria-activedescendant', resultsEl.firstElementChild.id);
    };

    const updateSelection = nextIdx => {
      const rows = [...resultsEl.querySelectorAll('.search-item')];
      if (!rows.length) return;
      searchSelected = (nextIdx + rows.length) % rows.length;
      rows.forEach((r, idx) => {
        const active = idx === searchSelected;
        r.classList.toggle('is-selected', active);
        r.setAttribute('aria-selected', String(active));
        if (active) {
          input.setAttribute('aria-activedescendant', r.id);
          r.scrollIntoView({ block: 'nearest' });
        }
      });
    };

    input.addEventListener('input', renderList);
    input.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); updateSelection(searchSelected + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); updateSelection(searchSelected - 1); }
      else if (e.key === 'Enter') {
        const active = resultsEl.querySelector('.search-item.is-selected');
        if (active) {
          e.preventDefault();
          dlg.close();
          window.location.href = active.href;
        }
      }
    });
    catBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        searchCategory = btn.dataset.searchCat || 'all';
        catBtns.forEach(b => {
          const on = b === btn;
          b.classList.toggle('is-active', on);
          b.setAttribute('aria-pressed', String(on));
        });
        renderList();
        input.focus();
      });
    });
    dlg.querySelector('[data-search-close]').addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', () => {
      input.setAttribute('aria-expanded', 'false');
      input.removeAttribute('aria-activedescendant');
    });
    dlg._renderList = renderList;
    searchDialog = dlg;
    return dlg;
  }

  function openGlobalSearch(prefill = '') {
    if (typeof HTMLDialogElement === 'undefined') return;
    const dlg = ensureSearchDialog();
    const input = dlg.querySelector('#qch-global-search-input');
    if (prefill) input.value = prefill;
    dlg._renderList();
    if (!dlg.open) dlg.showModal();
    input.focus();
    input.select();
  }

  document.addEventListener('click', e => {
    const trigger = e.target.closest?.('[data-open-search]');
    if (!trigger) return;
    e.preventDefault();
    openGlobalSearch('');
  });

  // 11. Beginner Core-Track Mode (toggle collapsible data-advanced="true" sections)
  const beginnerBtn = document.getElementById('beginner-toggle');
  const advancedSections = [...document.querySelectorAll('section.advanced-section[data-advanced="true"]')];
  advancedSections.forEach(sec => {
    const heading = sec.querySelector(':scope > h2, :scope > h3, :scope > h4');
    if (!heading || sec.querySelector(':scope > .advanced-banner')) return;
    const banner = document.createElement('div');
    banner.className = 'advanced-banner';
    const label = document.createElement('span');
    label.textContent = '☆ 进阶选读小节（初学主线模式已折叠，二刷可随时展开）';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'advanced-banner-btn';
    btn.textContent = '展开本节';
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', () => setAdvancedExpanded(sec, !sec.classList.contains('is-expanded')));
    banner.append(label, btn);
    heading.insertAdjacentElement('afterend', banner);
  });

  function setAdvancedExpanded(section, open) {
    section.classList.toggle('is-expanded', open);
    const button = section.querySelector(':scope > .advanced-banner .advanced-banner-btn');
    if (button) {
      button.textContent = open ? '收起本节' : '展开本节';
      button.setAttribute('aria-expanded', String(open));
    }
  }

  function syncBeginnerButton() {
    const on = root.getAttribute('data-beginner-mode') === 'on';
    if (!beginnerBtn) return;
    beginnerBtn.setAttribute('aria-pressed', String(on));
    const lbl = beginnerBtn.querySelector('.beginner-label');
    if (lbl) lbl.textContent = on ? '主线中' : '主线';
    beginnerBtn.title = on
      ? '初学主线模式已开启（点击恢复全部进阶选读）'
      : '初学主线模式：一键折叠进阶选读小节';
  }
  syncBeginnerButton();
  if (beginnerBtn) {
    beginnerBtn.addEventListener('click', () => {
      const nextOn = root.getAttribute('data-beginner-mode') !== 'on';
      if (nextOn) root.setAttribute('data-beginner-mode', 'on');
      else root.removeAttribute('data-beginner-mode');
      try { localStorage.setItem('qch-beginner-mode', nextOn ? 'on' : 'off'); } catch {}
      syncBeginnerButton();
    });
  }

  // 12. Local reading progress (qch-last-read) & mastered chapter check-in (qch-mastered)
  const pageUrl = document.body.getAttribute('data-page-url') || '';
  const pageTitle = document.body.getAttribute('data-page-title') || document.title;
  if (pageUrl && pageUrl !== 'index.html') {
    let lastSaveTs = 0;
    const saveLastRead = force => {
      const now = Date.now();
      if (!force && now - lastSaveTs < 1200) return;
      lastSaveTs = now;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? Math.round(Math.min(100, Math.max(0, (window.scrollY / docHeight) * 100))) : 0;
      try {
        localStorage.setItem('qch-last-read', JSON.stringify({ url: pageUrl, title: pageTitle, pct, updatedAt: now }));
      } catch {}
    };
    saveLastRead(true);
    window.addEventListener('scroll', () => saveLastRead(false), { passive: true });
    window.addEventListener('pagehide', () => saveLastRead(true));
  }

  function loadMastered() {
    try {
      const arr = JSON.parse(localStorage.getItem('qch-mastered') || '[]');
      return new Set(Array.isArray(arr) ? arr : []);
    } catch {
      return new Set();
    }
  }
  function saveMastered(set) {
    try { localStorage.setItem('qch-mastered', JSON.stringify([...set])); } catch {}
  }

  const TOTAL_CHAPTERS = 26;
  const checkinBox = document.querySelector('.chapter-checkin');
  const checkinBtn = document.getElementById('qch-checkin-btn');
  const checkinStatus = document.getElementById('qch-checkin-status');
  const sidebarProg = document.getElementById('qch-sidebar-progress');
  const progCount = document.getElementById('qch-progress-count');
  const progFill = document.getElementById('qch-progress-fill');

  function syncMasteredUI() {
    const mastered = loadMastered();
    document.querySelectorAll('.chapters nav a[data-ch-id]').forEach(a => {
      a.classList.toggle('is-mastered', mastered.has(a.getAttribute('data-ch-id')));
    });
    if (sidebarProg && progCount && progFill) {
      const n = mastered.size;
      sidebarProg.hidden = n === 0;
      progCount.textContent = `${n} / ${TOTAL_CHAPTERS} 章`;
      progFill.style.width = `${Math.min(100, Math.round((n / TOTAL_CHAPTERS) * 100))}%`;
    }
    if (checkinBox && checkinBtn) {
      const cid = checkinBox.getAttribute('data-chapter-id');
      const done = mastered.has(cid);
      checkinBtn.classList.toggle('is-done', done);
      checkinBtn.setAttribute('aria-pressed', String(done));
      checkinBtn.textContent = done ? '✓ 本章已掌握（点击取消）' : '✓ 标记本章已掌握';
      if (checkinStatus) {
        checkinStatus.textContent = done
          ? `已记录本章完成（当前累计 ${mastered.size} / ${TOTAL_CHAPTERS} 章，仅保存在本机浏览器）。`
          : '学完本章并核对自检题后，可标记为已掌握。';
      }
    }
  }
  syncMasteredUI();
  if (checkinBox && checkinBtn) {
    checkinBtn.addEventListener('click', () => {
      const cid = checkinBox.getAttribute('data-chapter-id');
      if (!cid) return;
      const mastered = loadMastered();
      if (mastered.has(cid)) mastered.delete(cid);
      else mastered.add(cid);
      saveMastered(mastered);
      syncMasteredUI();
    });
  }

  // 13. exercises.html sticky chapter chip bar + search + hash auto-open inside <details>
  const exToolbar = document.getElementById('ex-toolbar');
  if (exToolbar) {
    const exChapters = [...document.querySelectorAll('details.ex-chapter')];
    const exChips = [...exToolbar.querySelectorAll('[data-ex-filter]')];
    const exSearch = document.getElementById('ex-search');
    const exStatus = document.getElementById('ex-toolbar-status');
    const exToggleChapters = exToolbar.querySelector('[data-ex-toggle-chapters]');
    const exToggleAnswers = exToolbar.querySelector('[data-ex-toggle-answers]');
    let activeChapterFilter = 'all';

    const applyExFilter = () => {
      const q = (exSearch?.value || '').trim().toLowerCase();
      let shownCh = 0;
      let shownQ = 0;
      for (const ch of exChapters) {
        const key = ch.getAttribute('data-ex-ch');
        const chipMatch = activeChapterFilter === 'all' || key === activeChapterFilter;
        if (!chipMatch) {
          ch.hidden = true;
          continue;
        }
        const cards = [...ch.querySelectorAll('.ex-question-card')];
        if (!q) {
          ch.hidden = false;
          cards.forEach(c => { c.hidden = false; });
          shownCh++;
          shownQ += cards.length;
          if (activeChapterFilter !== 'all') ch.open = true;
        } else {
          let hits = 0;
          for (const card of cards) {
            const hay = (card.getAttribute('data-ex-search') || '') + ' ' + card.textContent.toLowerCase();
            const ok = hay.includes(q);
            card.hidden = !ok;
            if (ok) hits++;
          }
          ch.hidden = hits === 0;
          if (hits > 0) {
            ch.open = true;
            shownCh++;
            shownQ += hits;
          }
        }
      }
      if (exStatus) {
        exStatus.textContent = q
          ? `筛选「${exSearch.value.trim()}」：命中 ${shownCh} 章共 ${shownQ} 题`
          : activeChapterFilter === 'all'
            ? `当前显示全部 ${shownCh} 章共 ${shownQ} 题（点击芯片可聚焦任意单章）`
            : `已聚焦第 ${activeChapterFilter} 章（共 ${shownQ} 题，点“全部”恢复总览）`;
      }
      refreshScrollSpy();
    };

    const scrollToTargetBelowSticky = target => {
      if (!target) return;
      const headerEl = document.querySelector('header.reader-header, header:not(.course-header)');
      const headerHeight = headerEl ? headerEl.getBoundingClientRect().height : 0;
      const toolbarStyle = getComputedStyle(exToolbar);
      const toolbarHeight = (toolbarStyle.position === 'sticky' || toolbarStyle.position === 'fixed')
        ? exToolbar.getBoundingClientRect().height
        : 0;
      const offset = headerHeight + toolbarHeight + 12;
      const y = Math.max(0, window.scrollY + target.getBoundingClientRect().top - offset);
      const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: y, behavior: reduceMotion ? 'auto' : 'smooth' });
    };

    exChips.forEach(chip => {
      chip.addEventListener('click', () => {
        activeChapterFilter = chip.getAttribute('data-ex-filter') || 'all';
        exChips.forEach(c => {
          const on = c === chip;
          c.classList.toggle('is-active', on);
          c.setAttribute('aria-pressed', String(on));
        });
        applyExFilter();
        if (activeChapterFilter !== 'all') {
          const target = exChapters.find(ch => ch.getAttribute('data-ex-ch') === activeChapterFilter);
          scrollToTargetBelowSticky(target);
        }
      });
    });

    if (exSearch) exSearch.addEventListener('input', applyExFilter);
    if (exToggleChapters) {
      exToggleChapters.addEventListener('click', () => {
        const visibleCh = exChapters.filter(c => !c.hidden);
        const nextOpen = !visibleCh.every(c => c.open);
        visibleCh.forEach(c => { c.open = nextOpen; });
        exToggleChapters.textContent = nextOpen ? '折叠全部章' : '展开全部章';
        exToggleChapters.setAttribute('aria-expanded', String(nextOpen));
      });
    }
    if (exToggleAnswers) {
      exToggleAnswers.addEventListener('click', () => {
        const visibleDetails = [];
        for (const ch of exChapters) {
          if (ch.hidden) continue;
          if (!ch.open) ch.open = true;
          ch.querySelectorAll('.ex-question-card:not([hidden]) details').forEach(d => visibleDetails.push(d));
        }
        const nextOpen = !visibleDetails.every(d => d.open);
        visibleDetails.forEach(d => { d.open = nextOpen; });
        exToggleAnswers.textContent = nextOpen ? '折叠当前解答' : '展开当前解答';
        exToggleAnswers.setAttribute('aria-expanded', String(nextOpen));
      });
    }
  }

  function revealHashTarget() {
    if (!location.hash || location.hash.length < 2) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = location.hash.slice(1); }
    const target = document.getElementById(id);
    if (!target) return;
    let p = target.closest('details');
    while (p) {
      p.open = true;
      p.hidden = false;
      p = p.parentElement?.closest('details');
    }
    const adv = target.closest('.advanced-section');
    if (adv) setAdvancedExpanded(adv, true);
    if (exToolbar) {
      const headerEl = document.querySelector('header.reader-header, header:not(.course-header)');
      const headerHeight = headerEl ? headerEl.getBoundingClientRect().height : 0;
      const toolbarStyle = getComputedStyle(exToolbar);
      const toolbarHeight = (toolbarStyle.position === 'sticky' || toolbarStyle.position === 'fixed')
        ? exToolbar.getBoundingClientRect().height
        : 0;
      const y = Math.max(0, window.scrollY + target.getBoundingClientRect().top - (headerHeight + toolbarHeight + 12));
      window.scrollTo({ top: y, behavior: 'auto' });
    } else {
      target.scrollIntoView({ block: 'start' });
    }
    refreshScrollSpy();
  }
  window.addEventListener('hashchange', revealHashTarget);
  revealHashTarget();

  // 14. Horizontal scroll overflow shadow indicators + distraction-free keyboard shortcuts
  const scrollBoxes = [...document.querySelectorAll('.table-scroll, .flowchart-scroll')];
  if (scrollBoxes.length) {
    const syncScrollHint = el => {
      const canRight = el.scrollWidth - el.clientWidth - el.scrollLeft > 4;
      const canLeft = el.scrollLeft > 4;
      el.classList.toggle('can-scroll-right', canRight);
      el.classList.toggle('can-scroll-left', canLeft);
    };
    scrollBoxes.forEach(el => {
      syncScrollHint(el);
      el.addEventListener('scroll', () => syncScrollHint(el), { passive: true });
    });
    window.addEventListener('resize', () => scrollBoxes.forEach(syncScrollHint), { passive: true });
  }

  let shortcutDialog = null;
  function openShortcutDialog() {
    if (typeof HTMLDialogElement === 'undefined') return;
    if (!shortcutDialog) {
      const dlg = document.createElement('dialog');
      dlg.id = 'qch-shortcut-dialog';
      dlg.className = 'shortcut-modal';
      dlg.setAttribute('aria-label', '键盘快捷键速查');
      dlg.innerHTML =
        '<div class="shortcut-shell">' +
          '<div class="shortcut-head"><strong>键盘快捷键速查</strong><button type="button" class="lightbox-btn" data-sc-close>关闭 ✕</button></div>' +
          '<dl class="shortcut-list">' +
            '<div><dt><kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd> / <kbd>/</kbd></dt><dd>打开全书离线检索弹窗</dd></div>' +
            '<div><dt><kbd>[</kbd> 或 <kbd>Alt+←</kbd></dt><dd>跳转到上一章</dd></div>' +
            '<div><dt><kbd>]</kbd> 或 <kbd>Alt+→</kbd></dt><dd>跳转到下一章</dd></div>' +
            '<div><dt><kbd>t</kbd></dt><dd>切换亮色 / 暗色主题</dd></div>' +
            '<div><dt><kbd>?</kbd></dt><dd>打开本快捷键速查表</dd></div>' +
            '<div><dt><kbd>Esc</kbd></dt><dd>关闭当前弹窗或清空筛选</dd></div>' +
          '</dl>' +
        '</div>';
      document.body.appendChild(dlg);
      dlg.querySelector('[data-sc-close]').addEventListener('click', () => dlg.close());
      dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
      shortcutDialog = dlg;
    }
    if (!shortcutDialog.open) shortcutDialog.showModal();
  }

  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openGlobalSearch('');
      return;
    }
    if (isEditableFocus()) return;
    const anyModalOpen = Boolean(document.querySelector('dialog[open]'));
    if (anyModalOpen) return;

    if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      openGlobalSearch('');
    } else if (e.key === 't' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      toggleTheme();
    } else if (e.key === '?' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      openShortcutDialog();
    } else if ((e.key === '[' && !e.ctrlKey && !e.metaKey && !e.altKey) || (e.altKey && e.key === 'ArrowLeft')) {
      const prev = document.querySelector('.page-turn a[data-nav-prev]');
      if (prev) { e.preventDefault(); window.location.href = prev.href; }
    } else if ((e.key === ']' && !e.ctrlKey && !e.metaKey && !e.altKey) || (e.altKey && e.key === 'ArrowRight')) {
      const next = document.querySelector('.page-turn a[data-nav-next]');
      if (next) { e.preventDefault(); window.location.href = next.href; }
    }
  });
})();
