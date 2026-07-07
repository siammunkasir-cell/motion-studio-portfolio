import os, re

md_path = '/data/data/com.termux/files/home/portfolio/content/testimonials-content.md'
html_path = '/data/data/com.termux/files/home/portfolio/testimonials.html'

with open(md_path) as f:
    md = f.read()

# Parse the 50 short reviews (from "## Reviews" section)
lines = md.split('\n')
in_reviews = False
reviews_data = []
name_pattern = re.compile(r'^### \d+\.\s*(.+?)\s*\|\s*(.+?)$')
review_text_pattern = re.compile(r'^>\s*"(.*)"\s*$')
strength_pattern = re.compile(r'\*\*Strength:\*\*\s*(.+?)$')

for line in lines:
    stripped = line.strip()
    
    if stripped == '## Reviews':
        in_reviews = True
        continue
    
    if in_reviews and stripped.startswith('### '):
        # Parse name | industry
        m = name_pattern.match(stripped)
        if m:
            name = m.group(1).strip()
            industry = m.group(2).strip()
            review_text = ''
            strength = ''
            reviews_data.append({
                'name': name,
                'industry': industry,
                'text': '',
                'strength': ''
            })
    
    if in_reviews and reviews_data and stripped.startswith('> "'):
        m = review_text_pattern.match(stripped)
        if m:
            reviews_data[-1]['text'] = m.group(1)
    
    if in_reviews and reviews_data and '**Strength:**' in stripped:
        m = strength_pattern.search(stripped)
        if m:
            reviews_data[-1]['strength'] = m.group(1).strip()

print(f"Parsed {len(reviews_data)} short reviews")
if len(reviews_data) > 3:
    print(f"Sample: {reviews_data[0]['name']} ({reviews_data[0]['industry']}) - {reviews_data[0]['text'][:50]}... [{reviews_data[0]['strength']}]")

# Generate HTML
reviews_html = ''
for r in reviews_data:
    reviews_html += f'''
    <div class="review-card reveal">
      <div class="review-strength">{r['strength']}</div>
      <div class="review-text">"{r['text']}"</div>
      <div class="review-meta">
        <span class="review-name">{r['name']}</span>
        <span class="review-industry">{r['industry']}</span>
        <span class="review-stars">★★★★★</span>
      </div>
    </div>'''

if not reviews_html:
    print("ERROR: No reviews parsed!")
    exit(1)

with open(html_path) as f:
    html = f.read()

styles = '''
<style>
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 32px;
}
.review-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  position: relative;
  transition: 0.3s;
}
.review-card:hover { transform: translateY(-3px); border-color: rgba(255,107,107,0.2); }
.review-strength {
  position: absolute;
  top: -8px;
  right: 16px;
  background: linear-gradient(135deg, var(--accent1), var(--accent2));
  color: var(--bg);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 3px 12px;
  border-radius: 20px;
}
.review-text {
  font-size: 14px;
  color: var(--text2);
  line-height: 1.7;
  margin-bottom: 12px;
  font-style: italic;
}
.review-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}
.review-name { font-weight: 600; color: var(--text); }
.review-industry { color: var(--text3); }
.review-stars { color: #ffd93d; margin-left: auto; letter-spacing: 2px; }
</style>
'''

reviews_section = f'''
</section>

<!-- ─── QUICK REVIEWS ─── -->
<section id="quickReviews" style="padding:60px 0;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <span class="section-tag">5-Star Ratings</span>
      <h2>What People Are Saying</h2>
      <p>{len(reviews_data)} quick reviews from clients across industries worldwide.</p>
    </div>
    <div class="reviews-grid">
{reviews_html}
    </div>
  </div>
</section>'''

# Insert before scripts
script_idx = html.find('<script>')
if script_idx >= 0:
    insert_before = html[script_idx:]
    html_part = html[:script_idx]
    html_part += reviews_section
    html = html_part + '\n' + styles + '\n' + insert_before
    
    with open(html_path, 'w') as f:
        f.write(html)
    
    sz = os.path.getsize(html_path) / 1024
    print(f"✅ testimonials.html updated: {sz:.0f}KB")
else:
    print("ERROR: Script tag not found")
