(() => {
  'use strict';
  const form = document.getElementById('outcome-filters');
  if (!form) return;
  const fields = Object.fromEntries(['kind','status','year','q','issues'].map(name => [name, form.elements.namedItem(name)]));
  const records = Array.from(document.querySelectorAll('.outcome-record'));
  const texts = new Map(records.map(r => [r,r.textContent.toLocaleLowerCase()]));
  const count = document.getElementById('outcome-count');
  const empty = document.getElementById('outcome-empty');
  let selectedId = '';
  function readURL() {
    const params = new URLSearchParams(location.search);
    ['kind','status','year','q'].forEach(k => { fields[k].value = params.get(k) || ''; });
    fields.issues.checked = params.get('issues') === '1';
    selectedId = params.get('id') || '';
    if (!records.some(r => r.id === selectedId)) selectedId = '';
  }
  function apply() {
    const terms = fields.q.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let n = 0;
    records.forEach(r => {
      const visible = (!selectedId || r.id === selectedId)
        && (!fields.kind.value || r.dataset.kind === fields.kind.value)
        && (!fields.status.value || r.dataset.status === fields.status.value)
        && (!fields.year.value || r.dataset.years.split(' ').includes(fields.year.value))
        && (!fields.issues.checked || Number(r.dataset.issues) > 0)
        && terms.every(t => texts.get(r).includes(t));
      r.hidden = !visible;
      if (visible) n++;
      if (visible && selectedId) r.open = true;
    });
    count.textContent = `${n}개 성과 · 제목을 열면 검증 근거와 출처별 기록이 나타납니다.`;
    empty.hidden = n !== 0;
  }
  function writeURL() {
    const u = new URL(location.href);
    ['kind','status','year','q','issues','id'].forEach(k => u.searchParams.delete(k));
    ['kind','status','year','q'].forEach(k => { if (fields[k].value.trim()) u.searchParams.set(k,fields[k].value.trim()); });
    if (fields.issues.checked) u.searchParams.set('issues','1');
    if (selectedId) u.searchParams.set('id',selectedId);
    u.hash = 'outcome-results';
    history.replaceState(null,'',u);
  }
  function reveal() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (target && target.matches('.outcome-record') && !target.hidden) {
      target.open = true;
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    }
  }
  form.addEventListener('submit',e=>e.preventDefault());
  form.addEventListener('input',()=>{selectedId='';apply();writeURL();});
  form.addEventListener('reset',()=>{
    selectedId='';['kind','status','year','q'].forEach(k=>{fields[k].value='';});fields.issues.checked=false;
    records.forEach(r=>{r.open=false;});apply();writeURL();
  });
  window.addEventListener('popstate',()=>{readURL();apply();reveal();});
  window.addEventListener('hashchange',reveal);
  readURL();apply();reveal();
})();
