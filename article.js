const languageLink = document.querySelector('[data-lang]');
function carrySection() {
  const path = languageLink.getAttribute('href').split('#')[0];
  languageLink.href = path.split('?')[0] + window.location.search + window.location.hash;
}
window.addEventListener('hashchange', carrySection);
languageLink.addEventListener('click', carrySection);
carrySection();

const rail = document.querySelector('.rail');
const narrowLayout = window.matchMedia('(max-width: 720px)');
function setContentsLayout() {
  rail.open = !narrowLayout.matches;
}
setContentsLayout();
narrowLayout.addEventListener('change', setContentsLayout);

const sectionLinks = Array.from(rail.querySelectorAll('nav a'));
rail.querySelector('nav').addEventListener('click', event => {
  const link = event.target.closest('a');
  if (link && narrowLayout.matches && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
    rail.open = false;
  }
});
const sections = sectionLinks.map(link => document.querySelector(link.hash));
function updateContents() {
  const readingLine = window.innerHeight * 0.25;
  let current = null;
  sections.forEach((section, index) => {
    if (section.getBoundingClientRect().top <= readingLine) current = sectionLinks[index];
  });
  if (sections[sections.length - 1].getBoundingClientRect().bottom < 0) current = null;
  for (const link of sectionLinks) {
    if (link === current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}
let scheduled = false;
function queueUpdate() {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => {
    scheduled = false;
    updateContents();
  });
}
window.addEventListener('scroll', queueUpdate, { passive: true });
window.addEventListener('resize', queueUpdate);
window.addEventListener('load', updateContents);
updateContents();

for (const button of document.querySelectorAll('.prompt-language')) {
  const original = document.getElementById(button.getAttribute('aria-controls'));
  const translation = button.parentElement.querySelector('[lang="en"].verbatim');
  button.hidden = false;
  button.addEventListener('click', () => {
    const showOriginal = original.hidden;
    original.hidden = !showOriginal;
    translation.hidden = showOriginal;
    button.setAttribute('aria-expanded', String(showOriginal));
    button.textContent = showOriginal ? 'See translation' : 'See original';
  });
}
