// Mobile menu
const toggle = document.querySelector('.menu-toggle');
const setMenu = open => {
  document.body.classList.toggle('menu-open', open);
  toggle?.setAttribute('aria-expanded', String(open));
  if (toggle) toggle.textContent = open ? 'Sluiten' : 'Menu';
};
toggle?.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

// Header: saffron while the hero is under it, hairline once the page has scrolled
const header = document.querySelector('.site-header');
const hero = document.querySelector('.hero');
if (header && hero) {
  header.classList.add('is-over-hero');
  new IntersectionObserver(([e]) => header.classList.toggle('is-over-hero', e.isIntersecting), {
    rootMargin: '-72px 0px 0px 0px',
  }).observe(hero);
}
const sentinel = document.querySelector('.scroll-sentinel');
if (header && sentinel) {
  new IntersectionObserver(([e]) => header.classList.toggle('is-stuck', !e.isIntersecting)).observe(sentinel);
}

// Opened from disk (file://): folder links don't open index.html automatically, so point them at it
if (location.protocol === 'file:') {
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    if (/^(\.\.?\/|[\w-]+\/)([\w-]+\/)?(#.*)?$/.test(h) || h === './' || h === '../') {
      a.setAttribute('href', h.replace(/\/(#.*)?$/, '/index.html$1'));
    }
  });
}
