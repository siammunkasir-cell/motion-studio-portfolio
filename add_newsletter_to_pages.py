import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['services.html', 'testimonials.html', 'process.html', 'about.html']

# Read index.html to extract newsletter section + JS handler
with open(os.path.join(portfolio, 'index.html')) as f:
    idx = f.read()

# Extract newsletter HTML section (the section between the </p> and end of newsletter div)
news_start = idx.find('id="newsletterForm"')
if news_start < 0:
    print("❌ newsletterForm not found in index")
    exit(1)

# Go back to find the enclosing div
news_div_start = idx.rfind('<div', 0, news_start)
news_div_end = idx.find('</div>', news_start)
# Find the END of this newsletter section (closing div of the container)
# Count div nesting
depth = 1
pos = news_div_start + 5
while depth > 0 and pos < len(idx):
    open_div = idx.find('<div', pos)
    close_div = idx.find('</div>', pos)
    if close_div < 0:
        break
    if open_div >= 0 and open_div < close_div:
        depth += 1
        pos = open_div + 5
    else:
        depth -= 1
        pos = close_div + 6

newsletter_html = idx[news_div_start:pos]
print(f"✅ Newsletter HTML: {len(newsletter_html)} chars")

# Extract newsletter JS handler
js_start = idx.find('// ─── NEWSLETTER ───')
js_end = idx.find('\n\n', idx.find('}\n\n', js_start) + 2)
newsletter_js = idx[js_start:js_end]
print(f"✅ Newsletter JS: {len(newsletter_js)} chars")

# Now inject into each page
for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Check if newsletter already exists
    if 'newsletterForm' in html:
        print(f"  {fname}: already has newsletter, skipping")
        continue
    
    # Find where to inject: before the footer section
    footer_pos = html.find('<footer')
    if footer_pos < 0:
        print(f"  {fname}: no footer found, skipping")
        continue
    
    # Find the newsletter placeholder in the footer area
    # Look for a section before the footer that says "Stay Ahead" or similar
    # Or just inject right before <footer>
    html = html[:footer_pos] + '\n' + newsletter_html + '\n' + html[footer_pos:]
    
    # Now inject the JS handler - find the inquiryForm handler and add newsletter after it
    # Find the second-to-last </script>, which is the main script block
    script_end = html.rfind('</script>')
    if script_end >= 0:
        # Find the form handler section  
        form_section_end = html.rfind('\n// ─── INIT', 0, script_end)
        if form_section_end >= 0:
            html = html[:form_section_end] + '\n\n' + newsletter_js + html[form_section_end:]
            print(f"  {fname}: JS injected at init start")
        else:
            # Fallback: inject before </script>
            html = html[:script_end] + '\n\n' + newsletter_js + '\n' + html[script_end:]
            print(f"  {fname}: JS injected before </script>")
    else:
        print(f"  {fname}: no script tag found, JS NOT injected")
    
    with open(path, 'w') as f:
        f.write(html)
    print(f"  ✅ {fname}: done ({len(html)} bytes)")
