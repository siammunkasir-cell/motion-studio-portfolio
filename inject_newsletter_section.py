import os

portfolio = '/data/data/com.termux/files/home/portfolio'

# Newsletter HTML block to inject (from index.html)
newsletter_block = '''      <!-- Newsletter Signup -->
      <div style="max-width:480px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:36px">
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px">📬 Stay Ahead</h3>
        <p style="font-size:13px;color:var(--text2);margin-bottom:20px">Get UGC tips, AI content strategies, and insider workflows delivered to your inbox every week.</p>
        <form id="newsletterForm" action="https://formsubmit.co/siammunkasir@gmail.com" method="POST" style="display:flex;gap:8px">
          <input type="hidden" name="_next" value="https://motionstudiocreative.surge.sh/">
          <input type="hidden" name="_subject" value="Newsletter Signup - Motion Studio">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" style="display:none !important" tabindex="-1" autocomplete="off">
          <input type="email" name="email" id="newsletterEmail" required placeholder="your@email.com" style="flex:1;padding:12px 16px;background:var(--bg);border:1px solid var(--border);border-radius:100px;color:var(--text);font-size:14px;outline:none;font-family:var(--font)">
          <button type="submit" id="newsletterSubmit" style="padding:12px 24px;border-radius:100px;border:none;background:linear-gradient(135deg,var(--accent1),var(--accent2));color:var(--bg);font-weight:600;font-size:13px;cursor:pointer;white-space:nowrap;font-family:var(--font)">Subscribe</button>
        </form>
        <div id="newsletterMsg" style="font-size:13px;margin-top:8px;display:none"></div>
      </div>
    </div>
  </div>
</section>

<!-- ─── FOOTER ─── -->
'''

pages = ['services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Check if newsletter already exists
    if 'newsletterForm' in html and 'form id="newsletterForm"' in html:
        print(f'{fname}: already has newsletter form, skipping')
        continue
    
    # Find the footer marker and inject before it
    footer_marker = '<!-- ─── FOOTER ─── -->'
    footer_pos = html.find(footer_marker)
    
    if footer_pos >= 0:
        html = html[:footer_pos] + newsletter_block + html[footer_pos:]
        with open(path, 'w') as f:
            f.write(html)
        print(f'✅ {fname}: newsletter injected before footer')
    else:
        # Fallback: inject before <footer>
        footer_tag = html.find('<footer>')
        if footer_tag >= 0:
            # Go back to find a good injection point
            html = html[:footer_tag] + newsletter_block + html[footer_tag:]
            with open(path, 'w') as f:
                f.write(html)
            print(f'✅ {fname}: newsletter injected before <footer>')
        else:
            print(f'❌ {fname}: no footer found')

# Also remove the JS handler for newsletter since we're using redirect-based form
for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # The newsletter JS handler is still there but it's fine - 
    # it checks `if (newsletterForm)` which will be null, so it won't attach
    
    print(f'{fname}: done ({len(html)} bytes)')
