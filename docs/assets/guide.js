(() => {
  'use strict';

  function setupCopyButtons() {
    document.querySelectorAll('.copy-code').forEach(btn => {
      btn.addEventListener('click', async () => {
        const pre = btn.closest('.code-block').querySelector('pre');
        if (!pre) return;
        const text = pre.innerText.replace(/^\$\s+/gm, '').trim();
        try {
          await navigator.clipboard.writeText(text);
          const original = btn.textContent;
          btn.textContent = 'Copiado ✓';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.textContent = original;
            btn.classList.remove('copied');
          }, 2000);
        } catch (err) {
          // Fallback para contextos sin portapapeles async
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.left = '-9999px';
          document.body.appendChild(ta);
          ta.select();
          try {
            document.execCommand('copy');
            btn.textContent = 'Copiado ✓';
            btn.classList.add('copied');
            setTimeout(() => {
              btn.textContent = 'Copiar';
              btn.classList.remove('copied');
            }, 2000);
          } finally {
            document.body.removeChild(ta);
          }
        }
      });
    });
  }

  function setupActiveNav() {
    const links = document.querySelectorAll('.guide-nav a');
    const sections = document.querySelectorAll('.guide-content section');
    if (!links.length || !sections.length) return;

    function onScroll() {
      let currentSection = sections[0].id;
      const scrollY = window.scrollY + 120;
      sections.forEach(sec => {
        if (sec.offsetTop <= scrollY) {
          currentSection = sec.id;
        }
      });
      links.forEach(a => {
        if (a.getAttribute('href') === '#' + currentSection) {
          a.classList.add('active');
        } else {
          a.classList.remove('active');
        }
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function init() {
    setupCopyButtons();
    setupActiveNav();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
