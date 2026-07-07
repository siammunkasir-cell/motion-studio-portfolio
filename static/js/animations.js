// ─── GSAP ANIMATIONS ───
// Inline JS in index.html handles: scroll reveals, counters, skill bars, testimonials slider
// animations.js adds GSAP-enhanced animations that inline JS can't provide

document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined') return;

  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // ─── HERO STAGGER ANIMATION ───
  const heroContainer = document.querySelector('.hero-content');
  if (heroContainer) {
    const tl = gsap.timeline({ delay: 2.4 });
    tl.from('.hero-badge', { opacity: 0, y: 40, duration: 0.8, ease: 'power3.out' })
      .from('.hero-title', { opacity: 0, y: 50, duration: 0.8, ease: 'power3.out' }, '-=0.4')
      .from('.hero-subtitle', { opacity: 0, y: 30, duration: 0.7, ease: 'power3.out' }, '-=0.3')
      .from('.hero-actions', { opacity: 0, y: 20, duration: 0.6, ease: 'power3.out' }, '-=0.2')
      .from('.hero-stats .stat', { opacity: 0, y: 30, stagger: 0.12, duration: 0.6, ease: 'power3.out' }, '-=0.1');
  }

  // ─── PARALLAX EFFECTS ───
  if (typeof ScrollTrigger !== 'undefined') {
    // Hero gradient parallax
    const heroGrad = document.querySelector('.hero-gradient');
    if (heroGrad) {
      gsap.to(heroGrad, {
        yPercent: 20,
        ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
      });
    }
    // Floating elements parallax
    const heroGrid = document.querySelector('.hero-grid');
    if (heroGrid) {
      gsap.to(heroGrid, {
        yPercent: 10,
        ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
      });
    }
    // Floating background elements slow parallax
    document.querySelectorAll('.floating-elements .float-el').forEach((el, i) => {
      const spd = 0.08 + (i * 0.02);
      gsap.to(el, {
        y: () => window.innerHeight * spd,
        ease: 'none',
        scrollTrigger: {
          trigger: 'body',
          start: 'top top',
          end: 'bottom bottom',
          scrub: 2
        }
      });
    });

    // Service cards stagger reveal
    gsap.utils.toArray('.services-section .service-card').forEach((card, i) => {
      gsap.from(card, {
        opacity: 0,
        y: 40,
        duration: 0.6,
        delay: i * 0.08,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 90%',
          toggleActions: 'play none none none'
        }
      });
    });

    // Portfolio items stagger
    gsap.utils.toArray('.portfolio-item').forEach((item, i) => {
      gsap.from(item, {
        opacity: 0,
        y: 30,
        scale: 0.98,
        duration: 0.5,
        delay: i * 0.06,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: item,
          start: 'top 92%',
          toggleActions: 'play none none none'
        }
      });
    });

    // Pricing cards stagger
    gsap.from('.pricing-card', {
      opacity: 0,
      y: 40,
      stagger: 0.15,
      duration: 0.6,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.pricing-grid',
        start: 'top 85%',
        toggleActions: 'play none none none'
      }
    });
  }
});
