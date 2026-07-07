import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

overrides = '''
/* FORCED VISIBILITY OVERRIDES — white text, lighter cards */
.service-card, 
.service-card[style] { 
  background: #1a1a2e !important;
  border-color: rgba(255,255,255,.1) !important;
}
.service-card h3 { color: #ffffff !important; }
.service-card h4 { color: #ffffff !important; }
.service-card p { color: #ffffff !important; }
.service-card li { color: #ffffff !important; }
.service-card-header p { color: #ffffff !important; }
.service-card-header h3 { color: #ffffff !important; }
.service-details p { color: #ffffff !important; }
.service-details li { color: #ffffff !important; }
.service-details ul li { color: #ffffff !important; }
section p { color: #ffffff !important; }
.testimonial-card { background: #1a1a2e !important; }
.testimonial-card .quote { color: #ffffff !important; }
.testimonial-card .author { color: #ffffff !important; }
.testimonial-card .role { color: #ffffff !important; }
'''

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    css_end = html.find('</style>')
    if css_end >= 0:
        html = html[:css_end] + overrides + html[css_end:]
        with open(path, 'w') as f:
            f.write(html)
        print(f'{fname}: overrides added')
