import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

nuclear_override = '''
/* ⚠️ NUCLEAR VISIBILITY OVERRIDE - Forces ALL text white */
body, body * { color: #ffffff !important; }
body, body * { border-color: rgba(255,255,255,0.15) !important; }
'''

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    if 'NUCLEAR VISIBILITY OVERRIDE' not in html:
        # Add right before </style>
        html = html.replace('</style>', nuclear_override + '\n</style>')
        with open(path, 'w') as f:
            f.write(html)
        print(f'{fname}: nuclear override added')
    else:
        print(f'{fname}: already has nuclear override')
