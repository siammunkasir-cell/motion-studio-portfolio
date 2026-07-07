import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['process.html', 'about.html']

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

declarations = {
    'process.html': [
        ('const services = [', 'const services = loadFromStorage(\'services\', ['),
        ('const portfolioItems = [', 'const portfolioItems = loadFromStorage(\'portfolio\', ['),
        ('const testimonials = [', 'const testimonials = loadFromStorage(\'testimonials\', ['),
    ],
    'about.html': [
        ('const services = [', 'const services = loadFromStorage(\'services\', ['),
        ('const portfolioItems = [', 'const portfolioItems = loadFromStorage(\'portfolio\', ['),
        ('const testimonials = [', 'const testimonials = loadFromStorage(\'testimonials\', ['),
    ],
}

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    script_start = html.find('<script>')
    if script_start >= 0:
        eol = html.find('\n', script_start)
        before = html[:eol+1]
        after = html[eol+1:]
        replaced = 0
        
        for old_start, new_start in declarations[fname]:
            if old_start in after:
                after = after.replace(old_start, new_start, 1)
                replaced += 1
        
        if replaced > 0:
            html = before + '\n' + load_fn + after
            with open(path, 'w') as f:
                f.write(html)
            print(f'✅ {fname} — injected, wrapped {replaced} arrays')
        else:
            print(f'✗ {fname} — no matches')
    else:
        print(f'✗ {fname} — no script tag')

# Copy to deploy
deploy = '/data/data/com.termux/files/home/portfolio-deploy'
for fname in pages:
    src = os.path.join(portfolio, fname)
    dst = os.path.join(deploy, fname)
    content = open(src).read()
    with open(dst, 'w') as fh:
        fh.write(content)
    print(f'📋 Copied {fname} ({len(content)} bytes)')
