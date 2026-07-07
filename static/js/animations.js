// ─── GSAP ANIMATIONS — Motion Studio ───
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined') return;
  if (typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);

  // ─── SPLIT TEXT INTO SPANS ───
  function splitText(el) {
    const text = el.textContent.trim();
    const words = text.split(/\s+/);
    el.innerHTML = words
      .map(w => `<span class="word" style="display:inline-block;overflow:hidden;vertical-align:top">
        <span class="word-inner" style="display:inline-block">${w}</span>
      </span>`)
      .join(' ');
    return el.querySelectorAll('.word-inner');
  }

  // ─── HERO STAGGER ───
  const heroContent = document.querySelector('.hero-content');
  if (heroContent) {
    const tl = gsap.timeline({ delay: 2.6 });

    // Hero badge
    tl.from('.hero-badge', { opacity: 0, y: 40, scale: 0.9, duration: 0.9, ease: 'power4.out' });

    // Hero title with split words
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
      const words = heroTitle.querySelectorAll('.word-inner');
      if (words.length) {
        tl.from(words, {
          opacity: 0,
          y: 80,
          rotateX: -40,
          stagger: 0.04,
          duration: 0.8,
          ease: 'power3.out'
        }, '-=0.5');
      } else {
        tl.from('.hero-title', { opacity: 0, y: 50, duration: 0.8, ease: 'power3.out' }, '-=0.5');
      }
    }

    // Role text typewriter is handled by main.js
    tl.from('.hero-role-wrapper', { opacity: 0, y: 20, duration: 0.5, ease: 'power2.out' }, '-=0.3');

    // Subtitle
    tl.from('.hero-subtitle', { opacity: 0, y: 30, duration: 0.7, ease: 'power3.out' }, '-=0.2');

    // Actions stagger
    tl.from('.hero-actions .btn-primary', { opacity: 0, y: 20, scale: 0.95, duration: 0.5, ease: 'back.out(1.7)' }, '-=0.2');
    tl.from('.hero-actions .btn-secondary', { opacity: 0, y: 20, scale: 0.95, stagger: 0.08, duration: 0.5, ease: 'back.out(1.7)' }, '-=0.35');

    // Stats
    tl.from('.hero-stats .stat', { opacity: 0, y: 40, stagger: 0.1, duration: 0.6, ease: 'power3.out' }, '-=0.1');
  }

  // ─── SCROLL-TRIGGERED WORD REVEAL ───
  document.querySelectorAll('.split-reveal').forEach(el => {
    const words = splitText(el);
    ScrollTrigger.create({
      trigger: el,
      start: 'top 88%',
      onEnter: () => {
        gsap.to(words, {
          opacity: 1,
          y: 0,
          stagger: 0.03,
          duration: 0.6,
          ease: 'power2.out'
        });
      },
      once: true
    });
  });

  // ─── SECTION STAGGER REVEALS ───
  const sectionConfigs = [
    { selector: '.services-section .service-card', stagger: 0.08, y: 40 },
    { selector: '.portfolio-item', stagger: 0.06, y: 30, scale: 0.97 },
    { selector: '.pricing-card', stagger: 0.12, y: 40 },
    { selector: '.why-card', stagger: 0.08, y: 30 },
    { selector: '.workflow-step', stagger: 0.1, y: 30 },
    { selector: '.strength-item', stagger: 0.05, y: 20 }
  ];

  sectionConfigs.forEach(({ selector, stagger, y, scale }) => {
    const items = gsap.utils.toArray(selector);
    if (!items.length) return;
    gsap.from(items, {
      opacity: 0,
      y,
      ...(scale ? { scale } : {}),
      stagger,
      duration: 0.5,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: items[0].parentElement || items[0],
        start: 'top 92%',
        toggleActions: 'play none none none',
        once: true
      }
    });
  });

  // ─── TESTIMONIAL CARDS STAGGER ───
  gsap.from('.testimonial-card', {
    opacity: 0,
    x: 40,
    stagger: 0.08,
    duration: 0.5,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: '.testimonials-track',
      start: 'top 90%',
      once: true
    }
  });

  // ─── SKILL BARS ANIMATE ON SCROLL ───
  document.querySelectorAll('.skill-fill').forEach(bar => {
    ScrollTrigger.create({
      trigger: bar.closest('.skill-item') || bar,
      start: 'top 90%',
      onEnter: () => {
        const w = bar.getAttribute('data-width');
        if (w && !bar.dataset.animated) {
          bar.dataset.animated = 'true';
          gsap.to(bar, { width: w + '%', duration: 1.2, ease: 'power3.out', delay: 0.2 });
        }
      },
      once: true
    });
  });

  // ─── COUNTER ANIMATION (GSAP enhanced) ───
  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'));
    if (isNaN(target) || el.dataset.counted) return;
    el.dataset.counted = 'true';
    const obj = { val: 0 };
    gsap.to(obj, {
      val: target,
      duration: 2,
      ease: 'power3.out',
      onUpdate: () => { el.textContent = Math.floor(obj.val); }
    });
  }

  const heroStatsEl = document.querySelector('.hero-stats');
  if (heroStatsEl) {
    ScrollTrigger.create({
      trigger: heroStatsEl,
      start: 'top 90%',
      onEnter: () => {
        document.querySelectorAll('.stat-num').forEach(animateCounter);
      },
      once: true
    });
  }

  // ─── PARALLAX EFFECTS ───
  if (typeof ScrollTrigger !== 'undefined') {
    // Hero gradient
    gsap.to('.hero-gradient', {
      yPercent: 25,
      ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1.5 }
    });

    // Hero grid
    gsap.to('.hero-grid', {
      yPercent: 15,
      ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1.5 }
    });

    // Floating elements slow parallax
    document.querySelectorAll('.float-el').forEach((el, i) => {
      gsap.to(el, {
        y: () => window.innerHeight * (0.08 + i * 0.025),
        ease: 'none',
        scrollTrigger: {
          trigger: 'body',
          start: 'top top',
          end: 'bottom bottom',
          scrub: 2
        }
      });
    });

    // Section reveal — fade up entire sections
    gsap.utils.toArray('.section:not(.hero)').forEach(section => {
      const header = section.querySelector('.section-header');
      if (header) {
        gsap.from(header, {
          opacity: 0,
          y: 40,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: section,
            start: 'top 85%',
            toggleActions: 'play none none none',
            once: true
          }
        });
      }
    });
  }

  // ─── MOUSE PARALLAX ON HERO ───
  const hero = document.querySelector('.hero');
  if (hero && window.matchMedia('(pointer: fine)').matches) {
    hero.addEventListener('mousemove', e => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;
      gsap.to('.hero-gradient', { x: x * 15, y: y * 10, duration: 1, ease: 'power2.out' });
    });
  }

  // ─── SMOOTH ANCHOR SCROLL ───
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      gsap.to(window, {
        duration: 1.2,
        scrollTo: { y: target, offsetY: 80 },
        ease: 'power3.inOut'
      });
    });
  });

  // ─── BACK TO TOP ───
  const backBtn = document.getElementById('backToTop');
  if (backBtn) {
    backBtn.addEventListener('click', () => {
      gsap.to(window, { duration: 1, scrollTo: 0, ease: 'power3.inOut' });
    });
  }

  // ─── SPOTLIGHT CARDS (mousemove) ───
  document.querySelectorAll('.spotlight-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--mx', ((e.clientX - rect.left) / rect.width * 100) + '%');
      card.style.setProperty('--my', ((e.clientY - rect.top) / rect.height * 100) + '%');
    });
  });

  // ─── STAT RING ANIMATION ───
  document.querySelectorAll('.stat-ring.animate-on-scroll').forEach(ring => {
    ScrollTrigger.create({
      trigger: ring,
      start: 'top 90%',
      onEnter: () => ring.classList.add('animated'),
      once: true
    });
  });

  // ─── STAGGER LIST ITEMS ───
  document.querySelectorAll('.stagger-list').forEach(list => {
    gsap.from(list.children, {
      opacity: 0, y: 24, stagger: 0.06, duration: 0.5, ease: 'power2.out',
      scrollTrigger: { trigger: list, start: 'top 92%', toggleActions: 'play none none none', once: true }
    });
  });

  // ─── SECTION DIVIDER WAVE ANIMATION ───
  gsap.utils.toArray('.section-divider').forEach(div => {
    const wave = div.querySelector('path');
    if (!wave) return;
    const path = wave.getAttribute('d');
    let progress = { val: 0 };
    ScrollTrigger.create({
      trigger: div.parentElement || div,
      start: 'top center',
      onEnter: () => {
        gsap.to(progress, {
          val: 1, duration: 1.2, ease: 'power1.inOut',
          onUpdate: () => {
            // Subtle wave shift (morph not applied for perf — visibility is enough)
          }
        });
      },
      once: true
    });
  });

  // ─── SCROLL REFRESH ───
  if (typeof ScrollTrigger !== 'undefined') ScrollTrigger.refresh();
});
