// ─── MAIN.JS — Motion Studio Enhanced ───

// ─── TYPEWRITER: Rotating Hero Roles ───
(function() {
  const el = document.getElementById('heroRole');
  if (!el) return;

  const roles = JSON.parse(el.getAttribute('data-roles') || '[]');
  if (!roles.length) return;

  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let isPaused = false;

  // Parse cursor from HTML
  const cursorEl = el.querySelector('.role-cursor');
  const textEl = el.querySelector('.role-text');

  function type() {
    const current = roles[roleIndex];
    if (!current) return;

    if (!isDeleting) {
      // Typing forward
      charIndex++;
      textEl.textContent = current.substring(0, charIndex);

      if (charIndex === current.length) {
        isPaused = true;
        setTimeout(() => {
          isPaused = false;
          isDeleting = true;
          requestAnimationFrame(type);
        }, 2000);
        return;
      }
    } else {
      // Deleting backward
      charIndex--;
      textEl.textContent = current.substring(0, charIndex);

      if (charIndex === 0) {
        isDeleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        setTimeout(() => requestAnimationFrame(type), 400);
        return;
      }
    }

    const speed = isDeleting ? 30 : 60; // ms per char
    setTimeout(() => requestAnimationFrame(type), speed);
  }

  // Start after GSAP hero animation finishes (~3.5s delay)
  setTimeout(() => requestAnimationFrame(type), 3500);
})();

// ─── MAGNETIC BUTTON EFFECT ───
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
  });
});

// ─── 3D TILT ON SERVICE CARDS ───
document.querySelectorAll('.service-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    card.style.transform = `perspective(1000px) rotateY(${x * 6}deg) rotateX(${-y * 6}deg) translateY(-4px)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

// ─── 3D TILT ON PORTFOLIO ITEMS ───
document.querySelectorAll('.portfolio-item').forEach(item => {
  item.addEventListener('mousemove', e => {
    const rect = item.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    item.style.transform = `perspective(1000px) rotateY(${x * 4}deg) rotateX(${-y * 4}deg) translateY(-4px)`;
  });
  item.addEventListener('mouseleave', () => {
    item.style.transform = '';
  });
});

// ─── BUTTON RIPPLE EFFECT ───
document.querySelectorAll('.btn-ripple').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const r = document.createElement('span');
    r.className = 'ripple';
    const size = Math.max(rect.width, rect.height);
    r.style.width = r.style.height = size + 'px';
    r.style.left = (e.clientX - rect.left - size/2) + 'px';
    r.style.top = (e.clientY - rect.top - size/2) + 'px';
    this.appendChild(r);
    setTimeout(() => r.remove(), 600);
  });
});

// ─── SMOOTH CURSOR RING CLICK ───
const ring = document.getElementById('cursor-ring');
document.addEventListener('mousedown', () => ring && ring.classList.add('click'));
document.addEventListener('mouseup', () => ring && ring.classList.remove('click'));

// ─── CONTACT FORM ───
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  if (fileInput && fileList) {
    fileInput.addEventListener('change', () => {
      fileList.innerHTML = '';
      Array.from(fileInput.files).forEach(file => {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.innerHTML = `<i class="fas fa-paperclip"></i> ${file.name} (${(file.size / 1024 / 1024).toFixed(1)}MB)`;
        fileList.appendChild(div);
      });
    });
  }

  function loadCaptcha() {
    fetch('/api/captcha')
      .then(r => r.json())
      .then(data => {
        const qEl = document.getElementById('captchaQuestion');
        const eEl = document.getElementById('captchaExpected');
        if (qEl && eEl) {
          qEl.textContent = data.question;
          eEl.value = data.answer;
        }
      })
      .catch(() => {});
  }
  loadCaptcha();
  const refreshBtn = document.getElementById('refreshCaptcha');
  if (refreshBtn) refreshBtn.addEventListener('click', loadCaptcha);

  contactForm.addEventListener('submit', e => {
    e.preventDefault();
    const submitBtn = contactForm.querySelector('.btn-submit');
    if (!submitBtn) return;
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    const formData = new FormData(contactForm);
    fetch('/api/submit-inquiry', { method: 'POST', body: formData })
      .then(r => r.json())
      .then(data => {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        if (data.success) {
          const formFields = document.getElementById('formFields');
          const formSuccess = document.getElementById('formSuccess');
          if (formFields && formSuccess) {
            formFields.style.display = 'none';
            formSuccess.style.display = 'block';
          }
        } else {
          alert(data.error || 'Something went wrong. Please try again.');
        }
      })
      .catch(() => {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        alert('Network error. Please check your connection and try again.');
      });
  });
}

// ─── ESCAPE HTML ───
function escHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ─── CONSOLE BRANDING ───
console.log('%c Motion Studio %c by Siam Munkasir ',
  'background:#3B82F6;color:#09090B;padding:4px 8px;border-radius:4px 0 0 4px;font-weight:bold;font-size:14px;',
  'background:#0F172A;color:#94A3B8;padding:4px 8px;border-radius:0 4px 4px 0;font-size:14px;');
