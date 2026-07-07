import os

portfolio = '/data/data/com.termux/files/home/portfolio'
email = 'siammunkasir@gmail.com'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    original = html
    
    # ─── INQUIRY FORM ───
    # Replace the entire form with formsubmit.co version
    if 'id="inquiryForm"' in html:
        # Find the form bounds
        form_start = html.find('<form id="inquiryForm"')
        form_end = html.find('</form>', form_start) + len('</form>')
        
        old_form = html[form_start:form_end]
        
        new_form_html = '''<form id="inquiryForm" action="https://formsubmit.co/''' + email + '''" method="POST">
          <input type="hidden" name="_next" value="https://motionstudiocreative.surge.sh/#form-success">
          <input type="hidden" name="_subject" value="New Inquiry - Motion Studio Portfolio">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" style="display:none !important" tabindex="-1" autocomplete="off">
        
          <div class="form-row">
            <div class="form-group">
              <label>Full Name *</label>
              <input type="text" name="name" required placeholder="John Doe">
              <div class="error">Please enter your name</div>
            </div>
            <div class="form-group">
              <label>Company Name</label>
              <input type="text" name="company" placeholder="Brand Inc.">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Email Address *</label>
              <input type="email" name="email" required placeholder="john@company.com">
              <div class="error">Please enter a valid email</div>
            </div>
            <div class="form-group">
              <label>Phone Number</label>
              <input type="tel" name="phone" placeholder="+880 1XXX XXX XXX">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Country</label>
              <select name="country"><option value="">Select country</option><option value="Bangladesh">Bangladesh</option><option value="USA">United States</option><option value="UK">United Kingdom</option><option value="Canada">Canada</option><option value="Australia">Australia</option><option value="Germany">Germany</option><option value="France">France</option><option value="Other">Other</option></select>
            </div>
            <div class="form-group">
              <label>Website</label>
              <input type="url" name="website" placeholder="https://yourbrand.com">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Instagram</label>
              <input type="url" name="instagram" placeholder="https://instagram.com/yourbrand">
            </div>
            <div class="form-group">
              <label>LinkedIn</label>
              <input type="url" name="linkedin" placeholder="https://linkedin.com/company/yourbrand">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Project Type *</label>
              <select name="project_type" required><option value="">Select type</option><option value="Motion Graphics">Motion Graphics</option><option value="UGC Content">UGC Content</option><option value="Video Editing">Video Editing</option><option value="AI Visuals">AI Visuals</option><option value="Brand Design">Brand Design</option><option value="Social Media Content">Social Media Content</option><option value="Other">Other</option></select>
            </div>
            <div class="form-group">
              <label>Business Name</label>
              <input type="text" name="business_name" placeholder="Your Business">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Industry</label>
              <select name="industry"><option value="">Select industry</option><option value="Beauty">Beauty & Cosmetics</option><option value="Fashion">Fashion & Apparel</option><option value="Tech">Technology</option><option value="Food">Food & Beverage</option><option value="E-commerce">E-commerce</option><option value="Other">Other</option></select>
            </div>
            <div class="form-group">
              <label>Budget Range</label>
              <select name="budget"><option value="">Select budget</option><option value="100-500">$100 - $500</option><option value="500-1000">$500 - $1,000</option><option value="1000-3000">$1,000 - $3,000</option><option value="3000-5000">$3,000 - $5,000</option><option value="5000+">$5,000+</option></select>
            </div>
          </div>
          <div class="form-group">
            <label>Project Description</label>
            <textarea name="message" placeholder="Tell us about your project..." rows="3" required></textarea>
          </div>
          <div class="form-group">
            <label>Additional Notes</label>
            <textarea name="notes" placeholder="Anything else we should know..." rows="2"></textarea>
          </div>
          <button type="submit" class="submit-btn" id="formSubmit">
            <span class="btn-text">Send Inquiry <i class="fas fa-paper-plane" style="font-size:14px"></i></span>
            <span class="spinner"></span>
          </button>
        </form>'''
        
        html = html.replace(old_form, new_form_html)
        print(f'✅ {fname}: inquiry form replaced (Formsubmit)')
    
    # ─── NEWSLETTER FORM ───
    if 'id="newsletterForm"' in html:
        # Build new newsletter form
        new_nl_form = '''<form id="newsletterForm" action="https://formsubmit.co/''' + email + '''" method="POST" style="display:flex;gap:8px">
          <input type="hidden" name="_next" value="https://motionstudiocreative.surge.sh/">
          <input type="hidden" name="_subject" value="Newsletter Signup - Motion Studio">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" style="display:none !important" tabindex="-1" autocomplete="off">
          <input type="email" name="email" id="newsletterEmail" required placeholder="your@email.com" style="flex:1;padding:12px 16px;background:var(--bg);border:1px solid var(--border);border-radius:100px;color:var(--text);font-size:14px;outline:none;font-family:var(--font)">
          <button type="submit" id="newsletterSubmit" style="padding:12px 24px;border-radius:100px;border:none;background:linear-gradient(135deg,var(--accent1),var(--accent2));color:var(--bg);font-weight:600;font-size:13px;cursor:pointer;white-space:nowrap;font-family:var(--font)">Subscribe</button>
        </form>'''
        
        # Find old newsletter form and replace
        nl_start = html.find('<form id="newsletterForm"')
        nl_end = html.find('</form>', nl_start) + len('</form>')
        old_nl = html[nl_start:nl_end]
        html = html.replace(old_nl, new_nl_form)
        print(f'✅ {fname}: newsletter form replaced')
    
    if html != original:
        with open(path, 'w') as f:
            f.write(html)
        print(f'   Saved {fname}')
    else:
        print(f'   {fname}: no changes')
