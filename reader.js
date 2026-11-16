// The source links still work when the article is opened from disk.
const dialog = document.querySelector('.doc-reader');
const body = dialog.querySelector('.reader-body');
const pane = dialog.querySelector('.reader-scroll');
const download = dialog.querySelector('.reader-download');
const close = dialog.querySelector('.reader-close');
const root = new URL('./', location.href);
const documents = new Map();
const sources = new Map();
for (const link of document.querySelectorAll('.doc-index [data-doc-source]')) {
  const canonical = link.dataset.docSource;
  documents.set(canonical, link.href);
  sources.set(new URL(canonical, root).href, canonical);
  sources.set(link.href, canonical);
}
const english = document.documentElement.lang === 'en';
const articleTitle = document.title;
let parser;
let pending;
let lastSource;
let opener;
let tableObservers = [];
guideTableScroll(document.querySelector('#cost .scroll'));

// Only show the instruction when the table actually overflows its container.
function guideTableScroll(region) {
  const hint = document.createElement('div');
  hint.className = 'table-hint';
  hint.lang = document.documentElement.lang;
  hint.textContent = hint.lang === 'ro'
    ? 'Derulează orizontal pentru toate coloanele.'
    : 'Scroll horizontally to see all columns.';
  region.before(hint);
  region.addEventListener('keydown', event => {
    if (event.target !== region || hint.hidden || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    region.scrollLeft += event.key === 'ArrowLeft' ? -64 : 64;
  });
  function update() {
    const overflow = region.scrollWidth > region.clientWidth + 1;
    hint.hidden = !overflow;
    region.tabIndex = overflow ? 0 : -1;
  }
  update();
  const observer = new ResizeObserver(update);
  observer.observe(region);
  return () => observer.disconnect();
}

function releaseTables() {
  for (const disconnect of tableObservers) disconnect();
  tableObservers = [];
}

function readerURL(file, anchor = '') {
  const url = new URL(location.href);
  url.searchParams.set('doc', file + anchor);
  return url;
}

function wireLink(link, source) {
  const url = new URL(link.getAttribute('href'), source);
  const anchor = url.hash;
  url.hash = '';
  const file = sources.get(url.href);
  if (file) {
    link.href = readerURL(file, anchor);
    link.dataset.doc = file + anchor;
    link.setAttribute('aria-haspopup', 'dialog');
  } else {
    link.href = url.href + anchor;
  }
}

function formatDocument(markdown, file) {
  body.innerHTML = parser.render(markdown);
  const source = new URL(file, root);
  for (const link of body.querySelectorAll('a[href]')) {
    wireLink(link, source);
    if (!link.dataset.doc) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    }
  }
  for (const img of body.querySelectorAll('img')) img.src = new URL(img.getAttribute('src'), source);
  const ids = new Set();
  for (const heading of body.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
    const slug = heading.textContent.trim().toLowerCase().replace(/[^\p{Letter}\p{Number}\s_-]/gu, '').replace(/\s+/g, '-');
    let id = slug;
    for (let i = 1; ids.has(id); i++) id = slug + '-' + i;
    ids.add(id);
    heading.id = 'doc-' + id;
  }
  for (const table of body.querySelectorAll('table')) {
    const wrapper = document.createElement('div');
    wrapper.className = 'reader-table';
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', [...table.querySelectorAll('thead th')].map(th => th.textContent).join(', '));
    table.before(wrapper);
    wrapper.append(table);
    tableObservers.push(guideTableScroll(wrapper));
  }
}

async function showDocument() {
  pending?.abort();
  const request = new AbortController();
  pending = request;
  const doc = new URL(location.href).searchParams.get('doc');
  if (!doc) {
    if (dialog.open) {
      dialog.close();
      document.title = articleTitle;
      releaseTables();
      opener?.focus({preventScroll: true});
    }
    lastSource = undefined;
    return;
  }
  if (!dialog.open) dialog.showModal();
  const [file, anchor] = doc.split('#');
  const source = documents.get(file);
  const language = dialog.querySelector('.reader-language');
  const alternate = new URL(language.getAttribute('hreflang') === 'ro' ? 'ro.html' : 'index.html', root);
  alternate.search = location.search;
  alternate.hash = location.hash;
  language.href = alternate;
  download.hidden = !source;
  if (!download.hidden) download.href = source;
  body.lang = document.documentElement.lang;
  try {
    if (download.hidden) throw Error();
    if (lastSource !== file) {
      releaseTables();
      body.setAttribute('aria-busy', 'true');
      body.textContent = english ? 'Loading document…' : 'Se încarcă documentul…';
      lastSource = undefined;
      pane.scrollTop = 0;
      const [module, response] = await Promise.all([
        import('./vendor/markdown-it.mjs'), fetch(source, {signal: request.signal})
      ]);
      if (!response.ok) throw Error();
      const markdown = await response.text();
      if (request.signal.aborted) return;
      parser ??= module.default({html: false});
      formatDocument(markdown, file);
      const heading = body.querySelector('h1');
      document.title = (heading?.textContent || file) + ' · Acceleratu';
      if (heading) {
        heading.tabIndex = -1;
        heading.focus({preventScroll: true});
      }
      lastSource = file;
    }
    pane.scrollTop = history.state?.readerScroll ?? 0;
    if (anchor && !history.state?.readerScroll) body.querySelector('#' + CSS.escape('doc-' + decodeURIComponent(anchor)))?.scrollIntoView({block:'start'});
  } catch {
    if (request.signal.aborted) return;
    lastSource = undefined;
    body.lang = document.documentElement.lang;
    body.textContent = english ? 'This document could not be opened.' : 'Documentul nu a putut fi deschis.';
  } finally {
    if (!request.signal.aborted) body.removeAttribute('aria-busy');
  }
}

function closeDocument() {
  const depth = history.state?.readerDepth;
  if (depth) { history.go(-depth); return; }
  const url = new URL(location.href);
  url.searchParams.delete('doc');
  history.replaceState(null, '', url);
  showDocument();
}

if (location.protocol !== 'file:' && typeof dialog.showModal === 'function') {
  for (const link of document.querySelectorAll('article a[href]')) {
    if (sources.has(link.href)) wireLink(link, location.href);
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-doc]');
    if (!link || event.defaultPrevented || event.button || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    if (!dialog.open) opener = link;
    else history.replaceState({...history.state, readerScroll:pane.scrollTop}, '');
    const url = readerURL(link.dataset.doc);
    if (!dialog.open) url.hash = link.closest('section')?.id || location.hash;
    history.pushState({readerDepth: (history.state?.readerDepth || 0) + 1}, '', url);
    showDocument();
  });
  close.addEventListener('click', closeDocument);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeDocument(); });
  dialog.addEventListener('click', event => { if (event.target === dialog) closeDocument(); });
  window.addEventListener('popstate', showDocument);
  showDocument();
}
