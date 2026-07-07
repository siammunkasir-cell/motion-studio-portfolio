import os

files = ['index.html', 'services.html', 'process.html', 'testimonials.html', 'about.html']
gsap_block = '\n  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>'

for fname in files:
    path = f'/data/data/com.termux/files/home/portfolio/{fname}'
    with open(path, 'r') as f:
        html = f.read()
    
    count = 0
    if 'gsap' not in html.lower():
        # Add GSAP before </head>
        html = html.replace('</head>', f'{gsap_block}\n</head>', 1)
        count = 1
    else:
        # Already has GSAP
        pass
    
    with open(path, 'w') as f:
        f.write(html)
    print(f"{fname}: {'✅ GSAP added' if count else '✅ Already had GSAP'}")
