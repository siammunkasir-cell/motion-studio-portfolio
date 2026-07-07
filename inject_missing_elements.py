import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['services.html', 'testimonials.html', 'process.html', 'about.html']

# Elements to inject before </body> (hidden ones for JS, plus visible sections)
injection = '''
<!-- Missing elements for JS to work -->
<div id="loader" style="display:none"></div>
<div class="hero-particles" id="particles" style="display:none"></div>
<div id="cursor-dot" style="display:none"></div>
<div id="cursor-ring" style="display:none"></div>
<div id="scroll-progress" style="display:none"></div>
<button id="back-to-top" style="display:none"></button>

<div id="portfolioModal" class="modal-overlay" style="display:none">
  <div class="modal-content">
    <button class="modal-close" onclick="closeModal()"><i class="fas fa-times"></i></button>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<div id="servicesGrid" style="display:none"></div>
<div id="portfolioGrid" style="display:none"></div>
<div class="portfolio-filters reveal" id="portfolioFilters" style="display:none"></div>
<div id="testimonialsGrid" style="display:none"></div>
'''

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Inject before </body>
    if injection.strip() not in html:
        html = html.replace('</body>', injection + '\n</body>')
        with open(path, 'w') as f:
            f.write(html)
        print(f'{fname}: missing elements injected')
    else:
        print(f'{fname}: already has elements')
