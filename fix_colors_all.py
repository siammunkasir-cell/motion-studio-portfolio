import os, re

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

# The CSS changes to apply across all pages
replacements = [
    # Service card description - from text2 to text (lighter)
    ('.service-card p{color:var(--text2);font-size:14px;line-height:1.6;margin-bottom:16px}',
     '.service-card p{color:var(--text);font-size:14px;line-height:1.7;margin-bottom:16px;opacity:0.92}'),
    
    # Service features list - from text2 to text (lighter)
    ('.service-features li{font-size:13px;color:var(--text2);padding:6px 0;display:flex;align-items:center;gap:8px}',
     '.service-features li{font-size:13px;color:var(--text);padding:7px 0;display:flex;align-items:center;gap:8px;opacity:0.9}'),
    
    # Testimonial quote - from text2 to text (lighter)
    ('.testimonial-card .quote{font-size:15px;color:var(--text2);line-height:1.7;margin-bottom:16px;font-style:italic}',
     '.testimonial-card .quote{font-size:15px;color:var(--text);line-height:1.7;margin-bottom:16px;font-style:italic;opacity:0.92}'),
    
    # Testimonial role - from text3 to text2 (lighter)
    ('.testimonial-card .role{font-size:12px;color:var(--text3);margin-top:2px}',
     '.testimonial-card .role{font-size:12px;color:var(--text2);margin-top:2px}'),
    
    # Service card hover shadow
    ('.service-card:hover{transform:translateY(-4px);border-color:rgba(255,107,107,.12);box-shadow:0 8px 30px rgba(0,0,0,.3)}',
     '.service-card:hover{transform:translateY(-6px);border-color:rgba(255,107,107,.2);box-shadow:0 12px 40px rgba(255,107,107,.08)}'),
]

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    changed = 0
    for old, new in replacements:
        if old in html:
            html = html.replace(old, new)
            changed += 1
    
    if changed > 0:
        with open(path, 'w') as f:
            f.write(html)
        print(f'✅ {fname}: {changed} color fix(es) applied')
    else:
        print(f'   {fname}: already fixed or no matches')
