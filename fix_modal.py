import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

modal_overrides = '''
/* FORCED MODAL VISIBILITY */
.modal-content { background: #1a1a2e !important; }
.modal-body h2 { color: #ffffff !important; }
.modal-body .meta { color: #ffffff !important; }
.modal-body .meta span { color: #ffffff !important; }
.modal-body .section h4 { color: #ffd93d !important; }
.modal-body .section p { color: #ffffff !important; }
.modal-body .section ul { color: #ffffff !important; }
.modal-body .section ul li { color: #ffffff !important; }
.modal-close { color: #ffffff !important; }
'''

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Add modal overrides right before the closing </style>
    if modal_overrides.strip() not in html:
        css_end = html.find('</style>')
        if css_end >= 0:
            html = html[:css_end] + modal_overrides + html[css_end:]
            with open(path, 'w') as f:
                f.write(html)
            print(f'{fname}: modal overrides added')
        else:
            print(f'{fname}: no </style> found')
    else:
        print(f'{fname}: already has modal overrides')
