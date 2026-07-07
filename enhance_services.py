import re, os, json

md_path = '/data/data/com.termux/files/home/portfolio/content/services-content.md'
html_path = '/data/data/com.termux/files/home/portfolio/services.html'

with open(md_path) as f:
    md = f.read()

# Parse services from markdown - each service starts with "### " heading
service_blocks = md.split('### ')[1:]  # Skip the intro heading
services_detail = []

for block in service_blocks:
    lines = block.strip().split('\n')
    name = lines[0].strip()
    
    # Extract sections
    sections = {}
    current_section = None
    current_lines = []
    
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith('**') and stripped.endswith('**'):
            section_name = stripped.strip('*')
            if current_section:
                sections[current_section] = '\n'.join(current_lines).strip()
            current_section = section_name
            current_lines = []
        elif stripped.startswith('- ') or stripped.startswith('1.') or stripped.startswith('2.') or stripped.startswith('3.') or stripped.startswith('4.') or stripped.startswith('5.') or stripped.startswith('6.') or stripped.startswith('7.') or stripped.startswith('8.'):
            current_lines.append(line)
        elif stripped:
            current_lines.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_lines).strip()
    
    services_detail.append({'name': name, 'sections': sections})

print(f"Parsed {len(services_detail)} services from markdown")

# Generate HTML accordion sections
accordion_html = ''
for i, svc in enumerate(services_detail):
    s = svc['sections']
    desc = s.get('Description', '')
    benefits = s.get('Benefits', '')
    who = s.get("Who It's For", '')
    workflow = s.get('Workflow', '')
    deliverables = s.get('Deliverables', '')
    results = s.get('Expected Results', '')
    faq = s.get('FAQ', '')
    cta = s.get('CTA line', '')
    
    accordion_html += f'''
  <div class="service-detail reveal">
    <button class="detail-toggle" onclick="toggleDetail(this)">
      <span><i class="fas fa-chevron-right" style="transition:transform 0.3s"></i></span>
      <span style="font-size:16px;font-weight:600">{svc['name']}</span>
      <span style="font-size:12px;color:var(--text3)">Click to expand</span>
    </button>
    <div class="detail-content" style="display:none">'''
    
    # Description
    if desc:
        paragraphs = [p.strip() for p in desc.split('\n\n') if p.strip()]
        for p in paragraphs:
            accordion_html += f'<p>{p}</p>'
    
    # Benefits
    if benefits:
        accordion_html += '<h4 style="margin-top:20px;color:var(--accent1)">✅ Benefits</h4><ul>'
        for line in benefits.split('\n'):
            if line.strip().startswith('- '):
                accordion_html += f'<li style="margin-bottom:6px">{line.strip()[2:]}</li>'
        accordion_html += '</ul>'
    
    # Who It's For
    if who:
        accordion_html += '<h4 style="margin-top:16px;color:var(--accent1)">🎯 Who ' + "It's" + ' For</h4><p>' + who + '</p>'
    
    # Workflow
    if workflow:
        accordion_html += '<h4 style="margin-top:16px;color:var(--accent1)">⚙️ Workflow</h4><ol>'
        for line in workflow.split('\n'):
            if line.strip() and re.match(r'\d+\.', line.strip()):
                text = re.sub(r'\d+\.\s*', '', line.strip())
                accordion_html += f'<li style="margin-bottom:6px">{text}</li>'
        accordion_html += '</ol>'
    
    # Deliverables
    if deliverables:
        accordion_html += '<h4 style="margin-top:16px;color:var(--accent1)">📦 Deliverables</h4><ul>'
        for line in deliverables.split('\n'):
            if line.strip().startswith('- '):
                accordion_html += f'<li style="margin-bottom:6px">{line.strip()[2:]}</li>'
        accordion_html += '</ul>'
    
    # Expected Results
    if results:
        accordion_html += '<h4 style="margin-top:16px;color:var(--accent1)">📈 Expected Results</h4><ul>'
        for line in results.split('\n'):
            if line.strip().startswith('- '):
                accordion_html += f'<li style="margin-bottom:6px">{line.strip()[2:]}</li>'
        accordion_html += '</ul>'
    
    # FAQ
    if faq:
        accordion_html += '<h4 style="margin-top:16px;color:var(--accent1)">❓ FAQ</h4>'
        faq_items = faq.split('\n\n')
        for item in faq_items:
            if not item.strip():
                continue
            parts = item.split('\n', 1)
            q = parts[0].strip() if parts else ''
            a = parts[1].strip() if len(parts) > 1 else ''
            if q.startswith('- '):
                q = q[2:]
            if a.startswith('- '):
                a = a[2:]
            if q and a:
                accordion_html += f'<p><strong>Q: {q}</strong></p><p>{a}</p>'
    
    accordion_html += f'''
      <div style="margin-top:20px;padding:16px;background:var(--accent1);color:var(--bg);border-radius:12px;text-align:center;font-weight:600;font-size:14px">{cta}</div>
    </div>
  </div>'''

print(f"Generated {len(services_detail)} accordion sections ({len(accordion_html)} chars)")

# Insert into services.html
with open(html_path) as f:
    html = f.read()

# Find insertion point - after the services grid and before the JS
insert_marker = '</div>\n</section>\n'  # End of services section
idx = html.find(insert_marker)
if idx >= 0:
    idx = idx + len(insert_marker)
    # Find the next section
    
    styles = '''
<style>
.service-detail {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin-bottom: 12px;
  overflow: hidden;
}
.detail-toggle {
  width: 100%;
  padding: 18px 24px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: var(--font);
  color: var(--text);
  font-size: 14px;
  text-align: left;
}
.detail-toggle:hover { background: rgba(255,255,255,0.03); }
.detail-content { padding: 0 24px 24px; line-height: 1.8; font-size: 14px; color: var(--text2); }
.detail-content h4 { margin-top: 20px; margin-bottom: 8px; font-size: 15px; }
.detail-content ul, .detail-content ol { padding-left: 20px; }
.detail-content li { margin-bottom: 6px; }
.detail-content p { margin-bottom: 10px; }
</style>
'''
    
    detail_section = f'''
</section>

<!-- ─── SERVICE DETAILS ─── -->
<section id="serviceDetails" style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="section-header reveal">
      <span class="section-tag">Deep Dive</span>
      <h2>Full Service Breakdown</h2>
      <p>Detailed descriptions, workflows, deliverables, and FAQs for every service we offer.</p>
    </div>
    <div style="max-width:900px;margin:0 auto">
{accordion_html}
    </div>
  </div>
</section>'''
    
    # Insert before footer JS
    html = html.replace(styles, '')  # Remove if already exists
    js_idx = html.find('// ─── DATA ───')
    
    if 'SERVICE DETAILS' not in html:
        # Find the end of the pricing/cta section before the scripts
        script_idx = html.find('<script>')
        if script_idx >= 0:
            # Insert before script
            insert_before = html[script_idx:]
            html_part = html[:script_idx]
            html_part += detail_section
            html = html_part + '\n' + styles + '\n' + insert_before
            
            # Add toggle function to the script block
            toggle_fn = '''
// ─── DETAIL TOGGLE ───
function toggleDetail(btn) {
  const content = btn.nextElementSibling;
  const chevron = btn.querySelector('.fa-chevron-right');
  const isOpen = content.style.display === 'block';
  content.style.display = isOpen ? 'none' : 'block';
  chevron.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(90deg)';
  btn.querySelector('span:last-child').textContent = isOpen ? 'Click to expand' : 'Click to collapse';
}
'''
            html = html.replace('// ─── RENDER FUNCTIONS ───', toggle_fn + '\n// ─── RENDER FUNCTIONS ───')
        else:
            print("ERROR: Could not find script insertion point")
    
    with open(html_path, 'w') as f:
        f.write(html)
    
    sz = os.path.getsize(html_path) / 1024
    print(f"✅ services.html updated: {sz:.0f}KB")
else:
    print("ERROR: Could not find insertion point")
