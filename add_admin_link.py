import os

portfolio = '/data/data/com.termux/files/home/portfolio'
files = ['index.html', 'services.html', 'process.html', 'testimonials.html', 'about.html']

for fname in files:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    old = '<a href="#contact">Dhaka, Bangladesh</a></div>'
    new = '<a href="#contact">Dhaka, Bangladesh</a><a href="admin.html" style="opacity:0.4;font-size:12px;color:var(--text3)">🔐 Admin</a></div>'
    
    if old in html:
        html = html.replace(old, new)
        with open(path, 'w') as f:
            f.write(html)
        print(f'✅ {fname} — admin link added')
    else:
        # Try alternative footer structure
        alt_old = '<a href="#contact">Dhaka, Bangladesh</a></div>\n    </div>\n    <div class="footer-bottom">'
        alt_new = '<a href="#contact">Dhaka, Bangladesh</a><a href="admin.html" style="opacity:0.4;font-size:12px;color:var(--text3)">🔐 Admin</a></div>\n    </div>\n    <div class="footer-bottom">'
        if alt_old in html:
            html = html.replace(alt_old, alt_new)
            with open(path, 'w') as f:
                f.write(html)
            print(f'✅ {fname} — admin link added (alt)')
        else:
            print(f'✗ {fname} — NO MATCH')
            # Debug: find "Dhaka" in the file
            idx = html.find('Dhaka')
            if idx >= 0:
                print(f'  Found Dhaka at offset {idx}: ...{html[idx-20:idx+60]}...')
