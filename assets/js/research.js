/* Progressive enhancement: all research content is readable without JavaScript. */
(() => {
  'use strict';
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let parent = target.parentElement;
    while (parent) {
      if (parent.tagName === 'DETAILS') parent.open = true;
      parent = parent.parentElement;
    }
    if (target.tagName === 'DETAILS') target.open = true;
    requestAnimationFrame(() => (target.closest('.deliverables-card') || target).scrollIntoView({block: 'start'}));
  }
  const form = document.getElementById('research-filters');
  if (!form) {
    revealHash();
    window.addEventListener('hashchange', revealHash);
    return;
  }
  const fields = Object.fromEntries(['vertical', 'horizontal', 'year', 'q'].map(name => [name, form.elements.namedItem(name)]));
  const topics = Array.from(document.querySelectorAll('.research-topic'));
  const cells = Array.from(document.querySelectorAll('[data-map-vertical]'));
  const searchText = new Map(topics.map(topic => [topic, topic.textContent.toLocaleLowerCase()]));
  const count = document.getElementById('research-result-count');
  const empty = document.getElementById('research-empty');
  let selectedTech = '';
  function readURL() {
    const params = new URLSearchParams(location.search);
    Object.entries(fields).forEach(([name, field]) => { field.value = params.get(name) || ''; });
    const tech = params.get('tech') || '';
    selectedTech = topics.some(topic => topic.dataset.technology === tech) ? tech : '';
  }
  function writeURL(hash) {
    const url = new URL(location.href);
    ['vertical', 'horizontal', 'year', 'q', 'tech'].forEach(name => url.searchParams.delete(name));
    Object.entries(fields).forEach(([name, field]) => { if (field.value.trim()) url.searchParams.set(name, field.value.trim()); });
    if (selectedTech) url.searchParams.set('tech', selectedTech);
    if (hash !== undefined) url.hash = hash;
    history.replaceState(null, '', url);
  }
  function apply() {
    const vertical = fields.vertical.value;
    const horizontal = fields.horizontal.value;
    const year = fields.year.value;
    const words = fields.q.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let total = 0;
    topics.forEach(topic => {
      const milestones = Array.from(topic.querySelectorAll('.research-milestone'));
      milestones.forEach(item => { item.hidden = Boolean(year && item.dataset.year !== year); });
      const verticals = topic.dataset.vertical.split(' ').filter(Boolean);
      const visible = (!selectedTech || topic.dataset.technology === selectedTech)
        && (!vertical || (vertical === 'common' ? !verticals.length : verticals.includes(vertical)))
        && (!horizontal || topic.dataset.horizontal.split(' ').includes(horizontal))
        && (!year || milestones.some(item => item.dataset.year === year))
        && words.every(word => searchText.get(topic).includes(word));
      topic.hidden = !visible;
      if (visible) {
        total += 1;
        if (selectedTech || vertical || horizontal || year || words.length) topic.open = true;
      }
    });
    count.textContent = `${total}개 연구 주제 · 제목을 열면 연차별 연구내용과 대표 성과를 볼 수 있습니다.`;
    empty.hidden = total !== 0;
    cells.forEach(cell => {
      if (cell.dataset.mapVertical === vertical && cell.dataset.mapHorizontal === horizontal) cell.setAttribute('aria-current', 'true');
      else cell.removeAttribute('aria-current');
    });
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', () => { selectedTech = ''; apply(); writeURL('research-results'); });
  form.addEventListener('reset', () => {
    selectedTech = '';
    Object.values(fields).forEach(field => { field.value = ''; });
    topics.forEach(topic => { topic.open = false; });
    apply();
    writeURL('research-results');
  });
  cells.forEach(cell => cell.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    selectedTech = '';
    fields.vertical.value = cell.dataset.mapVertical;
    fields.horizontal.value = cell.dataset.mapHorizontal;
    fields.year.value = '';
    fields.q.value = '';
    apply();
    writeURL('research-results');
    document.getElementById('research-results').scrollIntoView({block: 'start'});
  }));
  window.addEventListener('popstate', () => { readURL(); apply(); revealHash(); });
  window.addEventListener('hashchange', revealHash);
  readURL();
  apply();
  if (location.hash) revealHash();
})();
