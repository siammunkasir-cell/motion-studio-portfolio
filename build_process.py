import json

with open('/data/data/com.termux/files/home/portfolio/.page_parts.json', 'r') as f:
    parts = json.load(f)

head = parts['head']; nav = parts['nav']; hamburger = parts['hamburger']
mobile = parts['mobile']; footer = parts['footer']; scripts = parts['scripts']

def make_page(title, hero_html, content_html):
    page_head = head.replace('<title>Motion Studio Creative', f'<title>{title} | Motion Studio Creative')
    return f'''<!DOCTYPE html>\n<html lang="en" data-theme="dark">\n{page_head}\n<body>\n\n{nav}\n\n{hamburger}\n\n{mobile}\n\n{hero_html}\n\n{content_html}\n\n{footer}\n\n{scripts}\n</body>\n</html>'''

# ──────────────────── PROCESS PAGE ────────────────────
process_hero = '''<section class="page-hero" style="min-height:50vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 20px 60px;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-tag">How We Work</div>
      <h1>Our Creative <span class="gradient-text">Process</span></h1>
      <p style="max-width:700px;margin:0 auto;font-size:18px;line-height:1.7">From the first conversation to final delivery — every project follows a proven 14-stage workflow designed to ensure quality, clarity, and exceptional results.</p>
    </div>
  </div>
</section>'''

steps = [
    ("Discovery Call", "01", "fas fa-phone", 
     "What Happens", "We start every project with a conversation. We listen to your goals, understand your brand, identify your target audience, and discuss your vision. This is a no-pressure discovery session where we ask questions and you share your expectations.",
     "Why It Matters", "Alignment is the foundation of great creative work. This call ensures we pursue the right direction from day one, saving time, money, and frustration later.",
     "Client Receives", "A written summary of our discussion with key takeaways, initial thoughts, and a proposed next step.",
     "Timeline", "30-45 minutes. Usually completed within 24 hours of initial inquiry.",
     "We discuss your brand, goals, target audience, competition, budget, timeline, and desired outcomes. We also answer any questions you have about our process."),

    ("Research", "02", "fas fa-search",
     "What Happens", "We dive deep into your industry, competitors, audience behavior, and content trends. This phase includes market analysis, competitor content audit, audience persona development, and platform-specific research to identify what works in your niche.",
     "Why It Matters", "Data-driven creative outperforms guesswork every time. Research ensures your content is strategically positioned to stand out and connect with the right audience.",
     "Client Receives", "A research brief summarizing key findings, competitor insights, audience data, and content opportunities.",
     "Timeline", "1-3 business days depending on project scope.",
     "We analyze competitor content strategies, identify content gaps in your niche, study platform algorithms, research trending formats and sounds, and develop audience personas based on your target demographic."),

    ("Strategy Planning", "03", "fas fa-chess",
     "What Happens", "We translate research into a clear creative strategy. This includes defining content pillars, selecting the right platforms, setting KPIs, creating a content calendar, and outlining the creative direction for each piece of content.",
     "Why It Matters", "A strategy without a plan is just a wish. Strategic planning ensures every piece of content serves a defined purpose and moves your business closer to its goals.",
     "Client Receives", "A comprehensive strategy document including content pillars, channel strategy, posting schedule, KPI framework, and creative direction brief.",
     "Timeline", "2-4 business days.",
     "We define 4-5 content pillars aligned with your brand values, create a 30-day content calendar, establish success metrics (engagement rate, reach, CTR, conversion), and select optimal posting times for each platform."),

    ("Creative Direction", "04", "fas fa-paint-brush",
     "What Happens", "We establish the visual and tonal direction for your project. This includes mood boards, color palettes, typography selection, visual references, tone of voice guidelines, and sample style frames to ensure we're aligned on creative vision before production begins.",
     "Why It Matters", "Clear creative direction eliminates subjective feedback loops during production. When everyone agrees on the visual language upfront, the execution phase becomes faster and more focused.",
     "Client Receives", "A creative direction deck with mood boards, visual references, color palette, typography samples, tone of voice examples, and 2-3 style frames.",
     "Timeline", "2-3 business days.",
     "We create 2-3 distinct visual directions for your project, source reference images and video samples, define color codes (HEX/RGB), select fonts, and document the desired mood and tone."),

    ("Script Planning", "05", "fas fa-file-alt",
     "What Happens", "Our creative team develops engaging scripts tailored to your platform, audience, and goals. We write hook-first scripts designed to capture attention in the critical first 2-3 seconds, with clear narrative arcs and strong calls to action.",
     "Why It Matters", "Great content starts with great writing. A well-structured script is the blueprint for every successful video, post, or campaign.",
     "Client Receives", "2-3 script options per piece of content with hook analysis, visual direction notes, and suggested runtime.",
     "Timeline", "1-2 business days per script batch.",
     "Each script includes a powerful hook, engaging body with visual cues [in brackets], clear value proposition, and compelling CTA. We optimize for retention, shareability, and conversion."),

    ("Storyboarding", "06", "fas fa-images",
     "What Happens", "We create visual storyboards that map out every scene, transition, and visual element. Each storyboard frame includes camera angles, motion notes, text overlays, timing, and audio cues — giving you a frame-by-frame preview of the final content.",
     "Why It Matters", "Storyboarding catches creative issues before production begins. It is far cheaper and faster to adjust a storyboard than to re-shoot or re-edit footage.",
     "Client Receives", "A detailed storyboard document or animatic (animated storyboard) for your review and approval.",
     "Timeline", "1-3 business days depending on project complexity.",
     "We create frame-by-frame visual plans with timing annotations, camera movement notes, text overlay placement, transition descriptions, and audio sync references."),

    ("Design", "07", "fas fa-pencil-ruler",
     "What Happens", "Our design team brings the storyboard to life. We create all visual assets including graphics, illustrations, text overlays, backgrounds, and branded elements. Every design asset follows the creative direction established earlier and is optimized for its target platform.",
     "Why It Matters", "Professional design is what separates amateur content from premium brand communication. Consistent, high-quality design builds trust and credibility with your audience.",
     "Client Receives", "Design assets in appropriate formats (PNG, AI, PSD, EPS) with brand-consistent styling and platform optimization.",
     "Timeline", "2-5 business days depending on asset volume.",
     "We design using industry-standard tools (Adobe Creative Suite, Figma) and follow platform-specific best practices for dimensions, resolution, and file formats."),

    ("Motion Graphics", "08", "fas fa-film",
     "What Happens", "Our animators bring static designs to life with fluid motion, smooth transitions, kinetic typography, and dynamic visual effects. This phase transforms raw designs into engaging animated content that captures and holds viewer attention.",
     "Why It Matters", "Motion increases retention. Animated content holds viewer attention 2-3x longer than static images and drives significantly higher engagement.",
     "Client Receives", "Animated sequences with smooth transitions, branded motion design, sound effects, and music integration.",
     "Timeline", "3-7 business days depending on complexity.",
     "We use After Effects, Cinema 4D, and Premiere Pro for motion design. Every animation includes ease-in/out curves, branded color application, and sound design."),

    ("Video Editing", "09", "fas fa-cut",
     "What Happens", "Raw footage and animated sequences are assembled into a cohesive final video. Our editors focus on pacing, timing, audio mixing, color grading, and visual continuity to create a polished, professional final product.",
     "Why It Matters", "The difference between raw footage and compelling content is editing. Skilled editing controls pacing, builds emotion, and ensures your message lands effectively.",
     "Client Receives", "A first draft edit for review, followed by a color-graded and sound-mixed final version.",
     "Timeline", "2-7 days depending on video length and complexity.",
     "Our editing workflow includes: assembly edit, fine cut, color grading (DaVinci Resolve/Premiere Pro), audio mixing, sound design, graphics integration, and platform-optimized export."),

    ("Revisions", "10", "fas fa-sync-alt",
     "What Happens", "We present the initial output for your feedback and provide up to 3 rounds of revisions. Our revision process is structured and efficient — we address specific feedback, make targeted adjustments, and present updated versions within 24-48 hours.",
     "Why It Matters", "Collaboration produces the best work. The revision process ensures the final output perfectly matches your vision while keeping the project on schedule.",
     "Client Receives", "Updated versions addressing your feedback within 24-48 hours per revision round.",
     "Timeline", "24-48 hours per revision round. Up to 3 rounds included.",
     "We use frame-accurate feedback tools for video reviews. Clients can leave timestamped comments directly on the video for precise, efficient feedback."),

    ("Quality Assurance", "11", "fas fa-check-double",
     "What Happens", "Every deliverable undergoes rigorous quality checks before delivery. We review video and audio quality, verify brand compliance, check file formats and specifications, test on target platforms, and ensure all links and integrations work correctly.",
     "Why It Matters", "Quality assurance prevents embarrassing mistakes and ensures your content performs perfectly when published. We catch issues you might miss.",
     "Client Receives", "A QA report confirming all checks passed, along with delivery-ready files.",
     "Timeline", "4-8 hours before final delivery.",
     "Our QA checklist includes: resolution check, audio sync, color accuracy, brand compliance, format optimization, spelling and grammar, call-to-action functionality, and platform-specific testing."),

    ("Final Delivery", "12", "fas fa-rocket",
     "What Happens", "We deliver all final assets in your preferred format and location. This includes organized file structures, multiple format exports, source files (optional), and a delivery note summarizing what was produced and next steps.",
     "Why It Matters", "Clean organized delivery saves you time and confusion. You get everything you need, in the right format, ready to publish.",
     "Client Receives", "Final deliverables via Google Drive, Dropbox, or direct transfer. Includes all formats, source files (on request), and usage guidelines.",
     "Timeline", "Delivery within 24 hours of final approval.",
     "We provide organized folders with clear naming conventions, multiple format exports (MP4, MOV, GIF for social), and a delivery checklist summarizing all assets."),

    ("Performance Review", "13", "fas fa-chart-line",
     "What Happens", "After your content is published, we track its performance and provide a detailed report. We analyze engagement metrics, audience response, conversion data, and compare results against the KPIs established in the strategy phase.",
     "Why It Matters", "Measuring results is how we improve. Performance data informs future content decisions and ensures continuous improvement in your content strategy.",
     "Client Receives", "A performance report with key metrics, insights, and recommendations for future content.",
     "Timeline", "7-14 days after publication.",
     "We track views, reach, engagement rate, click-through rate, conversion rate, follower growth, and audience sentiment. Reports include actionable recommendations."),

    ("Ongoing Support", "14", "fas fa-handshake",
     "What Happens", "Our relationship doesn't end at delivery. We offer ongoing support including content maintenance, performance optimization, strategy updates, and priority access for new projects. Retainer clients get dedicated support slots and faster turnaround.",
     "Why It Matters", "Consistent ongoing support ensures your content stays fresh, your strategy evolves with trends, and you always have a creative partner ready when you need one.",
     "Client Receives", "Priority support, strategy check-ins, trend updates, and faster turnaround on new projects.",
     "Timeline", "Ongoing — monthly check-ins for retainer clients.",
     "Retainer clients receive dedicated support hours, monthly strategy reviews, trend alerts, and priority scheduling. One-off project clients get 30 days of post-delivery support.")
]

process_content = '''<section class="process-page" style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Our 14-Step <span class="gradient-text">Creative Process</span></h2>
      <p>Every project follows this proven workflow — designed to ensure quality, clarity, and exceptional results at every stage.</p>
    </div>
    <div class="process-timeline" style="position:relative;margin-top:60px">'''

for i, (title, num, icon, label1, desc1, label2, why_text, label3, client_receives, label4, timeline, detail_desc) in enumerate(steps):
    side = "left" if i % 2 == 0 else "right"
    process_content += f'''
      <div class="process-timeline-item reveal" style="position:relative;padding:20px 0;padding-left:{'0' if side=='left' else '50%'};padding-right:{'50%' if side=='left' else '0'};margin-bottom:20px">
        <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 24px">
          <div class="step-indicator" style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <span style="background:var(--accent1);color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px">{num}</span>
            <h3 style="margin:0;font-size:18px;font-weight:700">{title}</h3>
          </div>
          <div class="step-details" style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
            <div>
              <h4 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:0 0 6px">{label1}</h4>
              <p style="font-size:14px;color:var(--text2);line-height:1.6;margin:0">{desc1}</p>
            </div>
            <div>
              <h4 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:0 0 6px">{label2}</h4>
              <p style="font-size:14px;color:var(--text2);line-height:1.6;margin:0">{why_text}</p>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px">
            <div>
              <h4 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:0 0 6px">{label3}</h4>
              <p style="font-size:14px;color:var(--text2);line-height:1.6;margin:0">{client_receives}</p>
            </div>
            <div>
              <h4 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:0 0 6px">{label4}</h4>
              <p style="font-size:14px;color:var(--accent1);font-weight:600;margin:0">{timeline}</p>
            </div>
          </div>
          <details style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border)">
            <summary style="font-size:13px;font-weight:600;cursor:pointer;color:var(--text1)">Tools and Workflow Details</summary>
            <p style="font-size:14px;color:var(--text2);line-height:1.6;margin-top:8px">{detail_desc}</p>
          </details>
        </div>
      </div>'''

process_content += '''
    </div>
    <div class="process-cta reveal" style="text-align:center;background:linear-gradient(135deg,var(--accent1),#ff4757);border-radius:var(--radius);padding:60px 40px;margin-top:40px">
      <h3 style="font-size:28px;font-weight:800;color:#fff;margin:0 0 12px">Ready to Start Your Project?</h3>
      <p style="color:rgba(255,255,255,.85);font-size:16px;max-width:600px;margin:0 auto 24px">Our process is proven, transparent, and designed for results. Let us begin with a free discovery call.</p>
      <a href="index.html#contact" style="display:inline-block;background:#fff;color:var(--accent1);padding:14px 36px;border-radius:30px;font-weight:700;font-size:15px;text-decoration:none">Start Your Discovery Call &#8594;</a>
    </div>
  </div>
</section>'''

process_html = make_page('Our Process', process_hero, process_content)

with open('/data/data/com.termux/files/home/portfolio/process.html', 'w') as f:
    f.write(process_html)
print(f"process.html: {len(process_html)} chars OK")
