import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

old = '.reveal{opacity:0;transform:translateY(40px);transition:opacity 0.8s cubic-bezier(.25,.46,.45,.94),transform 0.8s cubic-bezier(.25,.46,.45,.94)}'
new = '.reveal{opacity:1;transform:translateY(0px);transition:opacity 0.6s ease,transform 0.6s ease}'

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        with open(path, 'w') as f:
            f.write(html)
        print(f'{fname}: replaced {count} occurrence(s)')
    else:
        print(f'{fname}: no match (might already be fixed)')
