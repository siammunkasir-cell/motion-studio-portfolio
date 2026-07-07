import json

with open('/data/data/com.termux/files/home/portfolio/.page_parts.json', 'r') as f:
    parts = json.load(f)

head = parts['head']; nav = parts['nav']; hamburger = parts['hamburger']
mobile = parts['mobile']; footer = parts['footer']; scripts = parts['scripts']

def make_page(title, hero_html, content_html):
    page_head = head.replace('<title>Motion Studio Creative', f'<title>{title} | Motion Studio Creative')
    return f'''<!DOCTYPE html>\n<html lang="en" data-theme="dark">\n{page_head}\n<body>\n\n{nav}\n\n{hamburger}\n\n{mobile}\n\n{hero_html}\n\n{content_html}\n\n{footer}\n\n{scripts}\n</body>\n</html>'''

about_hero = '''<section class="page-hero" style="min-height:50vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 20px 60px;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-tag">About Us</div>
      <h1>Creative Vision, <span class="gradient-text">Global Impact</span></h1>
      <p style="max-width:700px;margin:0 auto;font-size:18px;line-height:1.7">Motion Studio Creative is a boutique creative agency founded by Md. Munkasir Prodhan Siam. We help brands tell their stories through world-class motion graphics, video production, and AI-powered content creation.</p>
    </div>
  </div>
</section>'''

content = '''
<!-- ABOUT INTRO -->
<section style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="reveal" style="text-align:center;max-width:800px;margin:0 auto">
      <h2 style="font-size:28px;font-weight:800;margin-bottom:20px">Who We <span class="gradient-text">Are</span></h2>
      <p style="color:var(--text2);font-size:16px;line-height:1.8;margin-bottom:24px">
        Motion Studio Creative started with a simple belief: great creative work should be accessible to every brand, regardless of size or budget. Founded by <strong>Md. Munkasir Prodhan Siam</strong> in Dhaka, Bangladesh, we have grown from a solo operation to a globally trusted creative partner serving clients across 12+ countries.
      </p>
      <p style="color:var(--text2);font-size:16px;line-height:1.8">
        With <strong>3+ years of experience</strong> working with agencies like Brandfit Media and ABC Agency, we bring a unique blend of hands-on production expertise and strategic thinking. We combine traditional creative craftsmanship with cutting-edge AI tools to deliver work that is faster, better, and more affordable than traditional agencies.
      </p>
    </div>
    <div class="founder-section reveal" style="display:grid;grid-template-columns:300px 1fr;gap:40px;margin-top:60px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:40px;align-items:start">
      <div style="text-align:center">
        <div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,var(--accent1),var(--accent2));margin:0 auto 16px;display:flex;align-items:center;justify-content:center;font-size:80px">M</div>
        <h3 style="font-size:18px;font-weight:800;margin-bottom:4px;">Md. Munkasir Prodhan Siam</h3>
        <div style="font-size:13px;color:var(--accent1);font-weight:600;margin-bottom:12px">Founder &amp; AI UGC Specialist</div>
        <div style="display:flex;gap:8px;justify-content:center;font-size:20px">
          <span style="cursor:default">&#9993;</span>
          <span style="cursor:default">&#127760;</span>
        </div>
      </div>
      <div>
        <h4 style="font-size:16px;font-weight:700;margin-bottom:12px">A Note From the Founder</h4>
        <p style="color:var(--text2);font-size:14px;line-height:1.8;margin-bottom:16px">
          "I started Motion Studio because I believe that high-quality creative content should not be a luxury reserved for big-budget brands. Every business, from a startup in Lagos to a boutique in Tokyo, deserves content that makes them look amazing and helps them grow.
        </p>
        <p style="color:var(--text2);font-size:14px;line-height:1.8;margin-bottom:16px">
          Over the past 3 years, I have had the privilege of working with incredible brands across industries and continents. Each project has taught me something new and helped me refine my craft. Today, I combine everything I have learned with the latest AI tools to deliver work that rivals top agencies at a fraction of the cost.
        </p>
        <p style="color:var(--text2);font-size:14px;line-height:1.8">
          When you work with Motion Studio, you work directly with me. No account managers, no middlemen, no inflated fees. Just great creative work, clear communication, and a genuine commitment to your success."
        </p>
      </div>
    </div>
  </div>
</section>

<!-- MISSION VISION VALUES -->
<section style="padding:60px 0;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Our <span class="gradient-text">Core</span> Values</h2>
      <p>The principles that guide every project, every decision, and every interaction with our clients.</p>
    </div>
    <div class="values-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-top:40px">
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#127775;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Excellence</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">We never compromise on quality. Every project receives our full creative energy regardless of size or budget.</p>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#128107;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Integrity</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">We are honest about timelines, transparent about pricing, and upfront about what is possible. No surprises.</p>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#9889;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Speed</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">We respect your time. 48-hour turnaround available on most projects without sacrificing quality.</p>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#128200;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Results</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">Every project starts with clear KPIs and ends with measurable outcomes. We optimize for business results.</p>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#127758;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Global Mindset</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">We work across cultures, time zones, and languages. Your audience is global and so is our perspective.</p>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center">
        <div style="font-size:36px;margin-bottom:12px">&#128300;</div>
        <h4 style="font-size:15px;font-weight:700;margin-bottom:8px">Innovation</h4>
        <p style="color:var(--text2);font-size:13px;line-height:1.6">We stay at the cutting edge of AI tools, platform trends, and creative techniques to deliver modern content.</p>
      </div>
    </div>
  </div>
</section>

<!-- EXPERIENCE -->
<section style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Our <span class="gradient-text">Journey</span></h2>
      <p>Key milestones that shaped Motion Studio Creative.</p>
    </div>
    <div class="timeline" style="margin-top:40px;max-width:700px;margin-left:auto;margin-right:auto">
      <div class="timeline-item reveal" style="display:grid;grid-template-columns:80px 1fr;gap:20px;margin-bottom:30px">
        <div style="text-align:right">
          <div style="font-weight:900;color:var(--accent1);font-size:20px">2022</div>
        </div>
        <div style="border-left:2px solid var(--border);padding-left:20px;padding-bottom:10px">
          <h4 style="font-size:15px;font-weight:700;margin:0 0 4px">Started at Brandfit Media</h4>
          <p style="font-size:13px;color:var(--text2);margin:0">Began professional journey creating motion graphics and brand content for multiple client campaigns. Developed core skills in animation, video editing, and creative direction.</p>
        </div>
      </div>
      <div class="timeline-item reveal" style="display:grid;grid-template-columns:80px 1fr;gap:20px;margin-bottom:30px">
        <div style="text-align:right">
          <div style="font-weight:900;color:var(--accent1);font-size:20px">2023</div>
        </div>
        <div style="border-left:2px solid var(--border);padding-left:20px;padding-bottom:10px">
          <h4 style="font-size:15px;font-weight:700;margin:0 0 4px">Joined ABC Agency + Freelance Launch</h4>
          <p style="font-size:13px;color:var(--text2);margin:0">Expanded expertise in UGC content, social media strategy, and AI-powered content workflows. Started independent freelance work on Fiverr and Upwork, serving international clients.</p>
        </div>
      </div>
      <div class="timeline-item reveal" style="display:grid;grid-template-columns:80px 1fr;gap:20px;margin-bottom:30px">
        <div style="text-align:right">
          <div style="font-weight:900;color:var(--accent1);font-size:20px">2025</div>
        </div>
        <div style="border-left:2px solid var(--border);padding-left:20px;padding-bottom:10px">
          <h4 style="font-size:15px;font-weight:700;margin:0 0 4px">Built ViralForge AI + Motion Studio</h4>
          <p style="font-size:13px;color:var(--text2);margin:0">Launched proprietary AI-powered SaaS platform for UGC content creation. Founded Motion Studio Creative as a premium creative agency serving global clients across 12+ countries.</p>
        </div>
      </div>
      <div class="timeline-item reveal" style="display:grid;grid-template-columns:80px 1fr;gap:20px;margin-bottom:30px">
        <div style="text-align:right">
          <div style="font-weight:900;color:var(--accent1);font-size:20px">2026</div>
        </div>
        <div style="border-left:2px solid var(--border);padding-left:20px;padding-bottom:10px">
          <h4 style="font-size:15px;font-weight:700;margin:0 0 4px">500+ Projects Milestone</h4>
          <p style="font-size:13px;color:var(--text2);margin:0">Reached 500+ projects delivered across 20+ industries. Launched UGC Script Studio tool. Expanded services to include comprehensive AI content creation and custom creative solutions.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SKILLS AND EXPERTISE -->
<section style="padding:60px 0;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Areas of <span class="gradient-text">Expertise</span></h2>
      <p>Skills and capabilities we bring to every project.</p>
    </div>
    <div class="skills-grid reveal" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-top:32px">
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <div style="font-size:13px;font-weight:600;color:var(--accent1);margin-bottom:4px">&#9733;</div>
        <span style="font-size:13px;font-weight:600">AI UGC Creation</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Motion Graphics</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Video Editing</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Script Writing</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Brand Identity</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Social Media Strategy</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">AI Image/Video Generation</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Content Strategy</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Animation</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Graphic Design</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">AI Receptionist Systems</span>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 16px;text-align:center">
        <span style="font-size:13px;font-weight:600">Content Marketing</span>
      </div>
    </div>
  </div>
</section>

<!-- ACHIEVEMENTS -->
<section style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Achievements &amp; <span class="gradient-text">Recognition</span></h2>
    </div>
    <div class="achievements-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-top:32px">
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px 20px;text-align:center">
        <div style="font-size:32px;font-weight:900;color:var(--accent1)">500+</div>
        <div style="font-size:14px;font-weight:600;margin:8px 0 4px">Projects Completed</div>
        <div style="font-size:12px;color:var(--text2)">Across 20+ industries worldwide</div>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px 20px;text-align:center">
        <div style="font-size:32px;font-weight:900;color:var(--accent1)">12+</div>
        <div style="font-size:14px;font-weight:600;margin:8px 0 4px">Countries Served</div>
        <div style="font-size:12px;color:var(--text2)">From USA to Japan to Nigeria</div>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px 20px;text-align:center">
        <div style="font-size:32px;font-weight:900;color:var(--accent1)">&#11088; 4.9</div>
        <div style="font-size:14px;font-weight:600;margin:8px 0 4px">Average Client Rating</div>
        <div style="font-size:12px;color:var(--text2)">Across 100+ verified reviews</div>
      </div>
      <div class="reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px 20px;text-align:center">
        <div style="font-size:32px;font-weight:900;color:var(--accent1)">3+ Yrs</div>
        <div style="font-size:14px;font-weight:600;margin:8px 0 4px">Industry Experience</div>
        <div style="font-size:12px;color:var(--text2)">Brandfit Media &amp; ABC Agency</div>
      </div>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section style="padding:60px 0;background:var(--bg)">
  <div class="container">
    <div class="cta-section reveal" style="text-align:center;background:linear-gradient(135deg,var(--accent1),#ff4757);border-radius:var(--radius);padding:60px 40px">
      <h3 style="font-size:28px;font-weight:800;color:#fff;margin:0 0 12px">Let Us Create Something Amazing Together</h3>
      <p style="color:rgba(255,255,255,.85);font-size:16px;max-width:600px;margin:0 auto 24px">One conversation is all it takes to get started. Tell us about your project and we will craft a custom solution.</p>
      <a href="index.html#contact" style="display:inline-block;background:#fff;color:var(--accent1);padding:14px 36px;border-radius:30px;font-weight:700;font-size:15px;text-decoration:none">Start Your Project Today &#8594;</a>
    </div>
  </div>
</section>'''

html = make_page('About', about_hero, content)
with open('/data/data/com.termux/files/home/portfolio/about.html', 'w') as f:
    f.write(html)
print(f"about.html: {len(html)} chars OK")
