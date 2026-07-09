import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

# The default service data from the JS
services = [
    {'icon':'fa-film', 'title':'Motion Graphics', 'desc':'Animated explainers, kinetic typography, logo reveals, and brand animations that bring your story to life.', 'price':'From $500', 'features':['2D/3D Animation','Kinetic Typography','Logo Animation','Title Sequences']},
    {'icon':'fa-video', 'title':'UGC Content', 'desc':'Authentic user-generated content strategies that build trust and drive engagement across all platforms.', 'price':'From $300', 'features':['Content Strategy','UGC Production','Influencer Collabs','Performance Analytics']},
    {'icon':'fa-robot', 'title':'AI Visuals', 'desc':'Cutting-edge AI-generated visuals, from concept art to photorealistic renders, tailored to your brand identity.', 'price':'From $200', 'features':['AI Image Generation','AI Video Creation','Style Transfer','Custom Training']},
    {'icon':'fa-paint-brush', 'title':'Brand Design', 'desc':'Complete brand identity packages including logos, color palettes, typography, and brand guidelines.', 'price':'From $800', 'features':['Logo Design','Brand Guidelines','Visual Identity','Brand Strategy']},
    {'icon':'fa-scroll', 'title':'Script Writing', 'desc':'Compelling scripts for videos, ads, podcasts, and social media that resonate with your target audience.', 'price':'From $150', 'features':['Video Scripts','Ad Copy','Storyboarding','Voiceover Scripts']},
    {'icon':'fa-music', 'title':'Audio Production', 'desc':'Professional sound design, music production, voiceovers, and audio post-production for your content.', 'price':'From $250', 'features':['Sound Design','Music Production','Voiceover Recording','Audio Mixing']},
]

def build_service_card(s):
    features = '\n'.join(f'<li><i class="fas fa-check"></i> {f}</li>' for f in s['features'])
    return f'''<div class="service-card reveal">
  <div class="service-icon"><i class="fas {s["icon"]}"></i></div>
  <h3>{s["title"]}</h3>
  <p>{s["desc"]}</p>
  <span class="service-price">{s["price"]}</span>
  <ul class="service-features">{features}</ul>
</div>'''

# Default testimonials
testimonials = [
    {'name':'Sarah Johnson', 'role':'Marketing Director', 'company':'TechFlow Inc.', 'text':'"Working with BrandFit Media transformed our brand presence. The animations they created captured exactly what we wanted to communicate — and the results speak for themselves."', 'rating':5},
    {'name':'David Chen', 'role':'CEO', 'company':'Creative Labs', 'text':'"The AI-generated visuals blew us away. We saved months of production time and got even better results than traditional methods. Absolutely game-changing."', 'rating':5},
    {'name':'Emily Rodriguez', 'role':'Content Strategist', 'company':'MediaPulse', 'text':'"Our social media engagement doubled after we started using their UGC content strategy. They truly understand what authentic content looks like."', 'rating':5},
    {'name':'Marcus Williams', 'role':'Founder', 'company':'StartupBoost', 'text':'"Professional, creative, and incredibly responsive. The script writing service alone was worth it — they nailed our brand voice from the first draft."', 'rating':5},
    {'name':'Priya Patel', 'role':'Brand Manager', 'company':'Luxe Cosmetics', 'text':'"The brand identity package was comprehensive and thoughtful. Every detail, from the logo to the color palette, perfectly represents our premium positioning."', 'rating':4},
    {'name':'James Thompson', 'role':'Creative Director', 'company':'PixelWorks Studio', 'text':'"They don\'t just produce content — they partner with you to achieve your vision. The audio production quality exceeded our expectations."', 'rating':5},
]

def build_testimonial_card(t):
    stars = '★' * t['rating'] + '☆' * (5 - t['rating'])
    company_str = f', {t["company"]}' if t['company'] else ''
    return f'''<div class="testimonial-card reveal">
  <div class="testimonial-stars">{stars}</div>
  <div class="quote">{t["text"]}</div>
  <div class="author">{t["name"]}</div>
  <div class="role">{t["role"]}{company_str}</div>
</div>'''

# Build the full grid HTML
services_html = '\n'.join(build_service_card(s) for s in services)
testimonials_html = '\n'.join(build_testimonial_card(t) for t in testimonials)

print("Static service cards generated ✓")
print(f"Services HTML: {len(services_html)} chars")
print(f"Testimonials HTML: {len(testimonials_html)} chars")

# Now inject into pages
for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Replace empty grids with static content
    old_services = '<div class="services-grid" id="servicesGrid"></div>'
    new_services = f'<div class="services-grid" id="servicesGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px">\n{services_html}\n</div>'
    
    old_testimonials = '<div class="testimonials-grid" id="testimonialsGrid"></div>'
    new_testimonials = f'<div class="testimonials-grid" id="testimonialsGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px">\n{testimonials_html}\n</div>'
    
    changes = []
    if old_services in html:
        html = html.replace(old_services, new_services)
        changes.append('services')
    else:
        print(f'{fname}: servicesGrid not found or already has content')
    
    if old_testimonials in html:
        html = html.replace(old_testimonials, new_testimonials)
        changes.append('testimonials')
    else:
        print(f'{fname}: testimonialsGrid not found or already has content')
    
    with open(path, 'w') as f:
        f.write(html)
    
    if changes:
        print(f'{fname}: injected static {" and ".join(changes)}')
