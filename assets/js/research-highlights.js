/* Independent year navigation; every highlight remains readable without JS. */
(() => {
  'use strict';
  const section = document.getElementById('research-highlights');
  if (!section) return;
  const controls = section.querySelector('.highlights-controls');
  const buttons = [...section.querySelectorAll('[data-highlight-year]')];
  const panels = [...section.querySelectorAll('[data-highlight-panel]')];
  const status = document.getElementById('highlights-status');
  function show(year) {
    let total = 0;
    panels.forEach(panel => {
      panel.hidden = year !== 'all' && panel.dataset.highlightPanel !== year;
      if (!panel.hidden) total += panel.querySelectorAll('.highlight-card').length;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.highlightYear === year)));
    status.textContent = `${year === 'all' ? '전체 연도' : year + '년'} 대표성과 ${total}개`;
  }
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return false; }
    const target = document.getElementById(id);
    const panel = target && target.closest('[data-highlight-panel]');
    if (!panel) return false;
    show(panel.dataset.highlightPanel);
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
    return true;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    const year = button.dataset.highlightYear;
    show(year);
    const url = new URL(location.href);
    url.hash = year === 'all' ? 'research-highlights' : 'highlights-year-' + year;
    history.replaceState(null, '', url);
  }));
  section.querySelectorAll('[data-highlight-jump]').forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    show(link.dataset.highlightJump);
  }));
  controls.hidden = false;
  if (!revealHash()) show(panels[panels.length - 1].dataset.highlightPanel);
  window.addEventListener('hashchange', revealHash);
  window.addEventListener('popstate', revealHash);
})();
