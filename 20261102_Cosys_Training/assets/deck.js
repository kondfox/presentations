/* Shared slide-deck engine.
   Markup: .viewport > .stage#stage > section.slide[data-title] …
   Each slide receives a `slideenter` / `slideleave` event when it becomes active / inactive.
   Build steps: <section class="slide" data-steps="3"> reveals in parts — the slide gets classes
   step-1 … step-N cumulatively; next/prev walk the steps before changing slide.
   Keys: →/Space/PageDown next · ←/PageUp back · Home/End · f fullscreen · Esc back to the session map. */
(function () {
  const slides = [...document.querySelectorAll('.slide')];
  const stage = document.getElementById('stage');

  const nav = document.createElement('nav');
  nav.className = 'chrome';
  nav.innerHTML = `
    <a href="../">← All sessions</a>
    <div class="dots"></div>
    <div class="right">
      <button data-go="-1" aria-label="Previous slide">←</button>
      <span class="count"></span>
      <button data-go="1" aria-label="Next slide">→</button>
    </div>`;
  document.body.appendChild(nav);
  const dots = nav.querySelector('.dots');
  const count = nav.querySelector('.count');
  slides.forEach((s, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', s.dataset.title || `Slide ${i + 1}`);
    b.onclick = () => go(i);
    dots.appendChild(b);
  });
  nav.querySelectorAll('[data-go]').forEach(b => b.onclick = () => Number(b.dataset.go) > 0 ? next() : prev());

  let cur = -1, step = 0;
  const stepsOf = s => Number(s.dataset.steps) || 0;
  function setStep(n) {
    const s = slides[cur], max = stepsOf(s);
    step = n;
    for (let k = 1; k <= max; k++) s.classList.toggle('step-' + k, k <= n);
    count.textContent = `${cur + 1} / ${slides.length}` + (max ? ` · part ${n}/${max}` : '');
    s.dispatchEvent(new CustomEvent('slidestep', { detail: n }));
  }
  function next() {
    const max = stepsOf(slides[cur]);
    if (max && step < max) setStep(step + 1); else go(cur + 1);
  }
  function prev() {
    if (stepsOf(slides[cur]) && step > 1) setStep(step - 1); else go(cur - 1, true);
  }
  function go(i, fromEnd = false) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === cur) return;
    slides.forEach((s, k) => {
      const on = k === i, was = k === cur;
      s.classList.toggle('active', on);
      s.querySelectorAll('video').forEach(v => { if (on) { v.currentTime = 0; v.play().catch(() => {}); } else v.pause(); });
      if (was && !on) s.dispatchEvent(new CustomEvent('slideleave'));
    });
    [...dots.children].forEach((d, k) => d.classList.toggle('on', k === i));
    count.textContent = `${i + 1} / ${slides.length}`;
    cur = i;
    history.replaceState(null, '', '#' + (i + 1));
    if (stepsOf(slides[i])) setStep(fromEnd ? stepsOf(slides[i]) : 1);
    slides[i].dispatchEvent(new CustomEvent('slideenter'));
  }

  document.addEventListener('keydown', e => {
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') go(0);
    else if (e.key === 'End') go(slides.length - 1);
    else if (e.key === 'Escape') location.href = '../';
    else if (e.key === 'f') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  });

  let tx = null;
  addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', e => { if (tx === null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) (dx < 0 ? next : prev)(); tx = null; });

  function fit() { stage.style.transform = `scale(${Math.min(innerWidth / 1600, innerHeight / 900)})`; }
  addEventListener('resize', fit); fit();

  let idleT;
  function wake() { document.body.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(() => document.body.classList.add('idle'), 2500); }
  addEventListener('mousemove', wake); wake();

  window.deck = { go, next, prev, get current() { return cur; } };
  // start after the page's own scripts have attached their slideenter listeners
  const start = () => go((parseInt(location.hash.slice(1), 10) || 1) - 1);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else setTimeout(start);
})();
