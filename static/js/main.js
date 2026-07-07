// ─── MAIN.JS - Enhanced Functionality ───
// Inline JS in index.html handles: cursor, loader, scroll, particles, counters, skills, portfolio filter, testimonials, reviews, FAQ, pricing

// ─── CONTACT FORM API SUBMISSION ───
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
        div.textContent = `${file.name} (${(file.size / 1024 / 1024).toFixed(1)}MB)`;
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

  contactForm.addEventListener('submit', (e) => {
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
console.log('%c Siam Munkasir %c AI Content Strategist & UGC Specialist ',
  'background:#3B82F6;color:#09090B;padding:4px 8px;border-radius:4px 0 0 4px;font-weight:bold;font-size:14px;',
  'background:#0F172A;color:#94A3B8;padding:4px 8px;border-radius:0 4px 4px 0;font-size:14px;');

// ─── BACK TO TOP ───
const backToTop = document.getElementById('backToTop');
if (backToTop) {
  window.addEventListener('scroll', () => {
    backToTop.style.display = window.scrollY > 400 ? 'flex' : 'none';
  });
}
