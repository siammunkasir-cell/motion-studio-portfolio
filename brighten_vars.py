import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Replace the CSS variables to be dramatically brighter
    html = html.replace('--text: #e0e0e8;', '--text: #ffffff;')
    html = html.replace('--text2: #a0a0b8;', '--text2: #e0e0e8;')
    html = html.replace('--text3: #666688;', '--text3: #b0b0c8;')
    html = html.replace('--card: #12121f;', '--card: #1a1a2e;')
    html = html.replace('--border: #2a2a3e;', '--border: #3a3a4e;')
    
    with open(path, 'w') as f:
        f.write(html)
    
    print(f'{fname}: CSS variables brightened')
