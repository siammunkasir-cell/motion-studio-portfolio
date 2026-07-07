import os, json, uuid, urllib.request

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'process.html', 'testimonials.html', 'about.html']

def fix_page(path):
    with open(path) as f:
        html = f.read()
    c = 0
    
    # 1. Fix redirect URL
    if 'motion-studio.surge.sh/#contact' in html:
        html = html.replace('motion-studio.surge.sh/#contact', 'motionstudiocreative.surge.sh/#contact')
        c += 1
    
    # 2. Remove Web3Forms client script
    for variant in [
        '<script src="https://web3forms.com/client/script.js" async defer></script>',
        '<script src="https://web3forms.com/client/script.js"></script>',
        '<script src="https://web3forms.com/client/script.js">',
    ]:
        if variant in html:
            html = html.replace(variant, '')
            c += 1
    
    # 3. Upgrade form handler
    old_handler = "document.getElementById('inquiryForm').addEventListener('submit', function(e) {"
    new_handler = """document.getElementById('inquiryForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn = document.getElementById('formSubmit');
  const btnText = btn.querySelector('.btn-text');
  const successDiv = document.getElementById('formSuccess');
  const form = this;
  if (!document.getElementById('consent').checked) {
    showToast('Please agree to the privacy policy', 'error');
    return;
  }
  btn.classList.add('loading');
  btn.disabled = true;
  btnText.textContent = 'Sending...';
  try {
    const formData = new FormData(form);
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST', body: formData
    });
    const data = await response.json();
    if (data.success) {
      form.reset();
      successDiv.style.display = 'block';
      form.querySelector('.submit-btn').style.display = 'none';
      showToast('Message sent! We will respond within 24h.', 'success');
    } else {
      showToast(data.message || 'Submission failed. Try again.', 'error');
    }
  } catch (err) {
    showToast('Network error. Check connection.', 'error');
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
    btnText.innerHTML = 'Send Inquiry <i class="fas fa-paper-plane" style="font-size:14px"></i>';
  }
});"""
    if old_handler in html:
        html = html.replace(old_handler, new_handler)
        c += 1
    
    # 4. Remove hCaptcha, add honeypot
    old_hcaptcha = '          <div class="h-captcha" data-sitekey="937a6f50-5cc4-4028-ac1e-1bd1ebfbfa6f"></div>'
    honeypot = '          <!-- Honeypot -->\n          <input type="checkbox" name="botcheck" style="display:none!important">'
    if old_hcaptcha in html:
        html = html.replace(old_hcaptcha, honeypot)
        c += 1
    
    # 5. Remove redirect hidden input
    old_redirect = '<input type="hidden" name="redirect" value="https://motionstudiocreative.surge.sh/#contact">'
    html = html.replace(old_redirect, '')
    
    # 6. Remove action/enctype from form tags
    html = html.replace(' action="https://api.web3forms.com/submit" method="POST" enctype="multipart/form-data"', '')
    
    # 7. Add newsletter handler if missing
    if 'newsletterForm' not in html and 'function showToast' in html and 'Stay Ahead' in html:
        news_handler = """// --- NEWSLETTER ---
const newsletterForm = document.getElementById('newsletterForm');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = document.getElementById('newsletterSubmit');
    const email = document.getElementById('newsletterEmail');
    const msg = document.getElementById('newsletterMsg');
    const originalText = btn.textContent;
    btn.textContent = 'Subscribing...';
    btn.disabled = true;
    msg.style.display = 'none';
    try {
      const fd = new FormData();
      fd.append('access_key', 'c1e6d832-f9f5-4021-9ada-23523b2f99ca');
      fd.append('email', email.value);
      fd.append('subject', 'Newsletter Signup');
      fd.append('from_name', 'Newsletter');
      const r = await fetch('https://api.web3forms.com/submit', {method:'POST',body:fd});
      const d = await r.json();
      if (d.success) { msg.textContent = 'Subscribed!'; msg.style.color = '#4ade80'; email.value = ''; }
      else { msg.textContent = d.message || 'Failed.'; msg.style.color = '#ff6b6b'; }
    } catch(e) { msg.textContent = 'Network error.'; msg.style.color = '#ff6b6b'; }
    msg.style.display = 'block';
    btn.textContent = originalText;
    btn.disabled = false;
  });
}
function showToast"""
        html = html.replace('function showToast', news_handler)
        c += 1
    
    with open(path, 'w') as f:
        f.write(html)
    return c

for p in pages:
    path = os.path.join(portfolio, p)
    if os.path.exists(path):
        ch = fix_page(path)
        sz = os.path.getsize(path) / 1024
        print(f'  {p}: {ch} fixes, {sz:.0f}KB')

# Test Web3Forms API
print()
print('--- Testing Web3Forms API ---')
boundary = uuid.uuid4().hex
body = f'--{boundary}\r\nContent-Disposition: form-data; name="access_key"\r\n\r\nc1e6d832-f9f5-4021-9ada-23523b2f99ca\r\n--{boundary}\r\nContent-Disposition: form-data; name="email"\r\n\r\ntest@studio.xyz\r\n--{boundary}\r\nContent-Disposition: form-data; name="subject"\r\n\r\nAPI Test\r\n--{boundary}--\r\n'.encode()
req = urllib.request.Request(
    'https://api.web3forms.com/submit',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)
try:
    r = urllib.request.urlopen(req, timeout=10)
    d = json.loads(r.read())
    print(f'  Response: success={d.get("success")}, msg={d.get("message","")}')
except Exception as e:
    print(f'  Error: {e}')
    if hasattr(e, 'read'):
        print(f'  Body: {e.read().decode()[:200]}')
