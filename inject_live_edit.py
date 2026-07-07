import os, json

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html']

# The loadFromStorage function to inject
load_fn = """// ─── LIVE EDIT: Load from admin localStorage ───
function loadFromStorage(key, defaultVal) {
  try {
    const saved = localStorage.getItem('motion_studio_data');
    if (saved) {
      const data = JSON.parse(saved);
      if (data[key] && Array.isArray(data[key]) && data[key].length > 0) {
        return data[key];
      }
    }
  } catch(e) {}
  return defaultVal;
}
"""

# Data declarations to wrap
declarations = {
    'services.html': [('const services = [', 'const services = loadFromStorage(\'services\', [')],
    'testimonials.html': [('const testimonials = [', 'const testimonials = loadFromStorage(\'testimonials\', [')],
    'index.html': [
        ('const services = [', 'const services = loadFromStorage(\'services\', ['),
        ('const portfolioItems = [', 'const portfolioItems = loadFromStorage(\'portfolio\', ['),
    ],
}

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # 1. Inject loadFromStorage after <script> tag
    script_start = html.find('<script>\n// ─── DATA ───')
    if script_start < 0:
        script_start = html.find('<script>\n// ─── DATA')
    if script_start < 0:
        script_start = html.find('<script>')
    
    if script_start >= 0:
        # Find the end of <script> tag line
        eol = html.find('\n', script_start)
        before = html[:eol+1]
        after = html[eol+1:]
        replaced = 0
        
        # Apply data declaration wraps
        if fname in declarations:
            for old_start, new_start in declarations[fname]:
                if old_start in after:
                    after = after.replace(old_start, new_start, 1)
                    replaced += 1
        
        if replaced > 0:
            html = before + '\n' + load_fn + after
            with open(path, 'w') as f:
                f.write(html)
            print(f'✅ {fname} — injected loadFromStorage, wrapped {replaced} arrays')
        else:
            print(f'✗ {fname} — data arrays not found')
    else:
        print(f'✗ {fname} — no script tag found')

# Also update admin.html to save to localStorage properly
admin_path = os.path.join(portfolio, 'admin.html')
with open(admin_path) as f:
    admin = f.read()

# Update saveToServer to save individual keys too
old_save = """function saveToServer() {
  // Save to localStorage
  localStorage.setItem('motion_studio_data', JSON.stringify(data));
}"""

new_save = """function saveToServer() {
  localStorage.setItem('motion_studio_data', JSON.stringify(data));
  // Also save individual keys for live site pages
  try { localStorage.setItem('motion_services', JSON.stringify(data.services)); } catch(e) {}
  try { localStorage.setItem('motion_portfolio', JSON.stringify(data.portfolio)); } catch(e) {}
  try { localStorage.setItem('motion_testimonials', JSON.stringify(data.testimonials)); } catch(e) {}
}"""

if old_save in admin:
    admin = admin.replace(old_save, new_save)
    with open(admin_path, 'w') as f:
        f.write(admin)
    print('✅ admin.html — updated saveToServer')
else:
    print('✗ admin.html — saveToServer not found')

# Copy pages
deploy = '/data/data/com.termux/files/home/portfolio-deploy'
for f in pages + ['admin.html']:
    src = os.path.join(portfolio, f)
    dst = os.path.join(deploy, f)
    content = open(src).read()
    with open(dst, 'w') as fh:
        fh.write(content)
    print(f'📋 Copied {f} ({len(content)} bytes) to deploy')

print('\n✅ Done! All pages updated for live editing from admin.')
