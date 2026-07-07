import os, re

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Replace all inline color:var(--text2) with color:var(--text)
    # Only replace INSIDE style="..." attributes, not inside <style> CSS
    count_text2 = 0
    count_text3 = 0
    
    # Use regex to find style="..." attributes and replace inside
    def replace_inline(match):
        global count_text2, count_text3
        content = match.group(0)
        # Replace text2 -> text in inline styles
        new = content.replace('color:var(--text2)', 'color:var(--text)')
        new = new.replace('color:var(--text3)', 'color:var(--text)')
        if new != content:
            if 'color:var(--text2)' in content:
                count_text2 += content.count('color:var(--text2)')
            if 'color:var(--text3)' in content:
                count_text3 += content.count('color:var(--text3)')
        return new
    
    # Match style="..." attributes
    html = re.sub(r'style="[^"]*"', replace_inline, html)
    
    with open(path, 'w') as f:
        f.write(html)
    
    print(f'{fname}: replaced text2={count_text2} text3={count_text3}')
