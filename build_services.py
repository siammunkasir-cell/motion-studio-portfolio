import json

with open('/data/data/com.termux/files/home/portfolio/.page_parts.json', 'r') as f:
    parts = json.load(f)

head = parts['head']
nav = parts['nav']
hamburger = parts['hamburger']
mobile = parts['mobile']
footer = parts['footer']
scripts = parts['scripts']

def make_page(title, hero_html, content_html, body_extra=''):
    page_head = head.replace('<title>Motion Studio Creative', f'<title>{title} | Motion Studio Creative')
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
{page_head}
<body{body_extra}>

{nav}

{hamburger}

{mobile}

{hero_html}

{content_html}

{footer}

{scripts}
</body>
</html>'''
    return html

def service_card(name, icon, desc, benefits, who_for, workflow, deliverables, results, faq_q, faq_a):
    ben_list = ''.join(f'<li style="padding:6px 0;font-size:14px;color:var(--text2)">&#10003; {b.strip()}</li>' for b in benefits.split(';') if b.strip())
    sid = name.lower().replace(' ','-').replace('&','and').replace('--','-')
    return f'''<div class="service-card" id="service-{sid}" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:40px 32px;margin-bottom:30px;scroll-margin-top:100px">
      <div class="service-card-header" style="display:flex;align-items:flex-start;gap:20px;margin-bottom:24px">
        <div style="font-size:40px;line-height:1">{icon}</div>
        <div>
          <h3 style="font-size:22px;font-weight:800;margin:0 0 8px">{name}</h3>
          <p style="color:var(--text2);font-size:15px;line-height:1.7">{desc}</p>
        </div>
      </div>
      <div class="service-details" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px">
        <div>
          <h4 style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin-bottom:12px">Benefits</h4>
          <ul style="list-style:none;padding:0;margin:0">
            {ben_list}
          </ul>
        </div>
        <div>
          <h4 style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin-bottom:12px">Who It Is For</h4>
          <p style="font-size:14px;color:var(--text2);line-height:1.6">{who_for}</p>
          <h4 style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:16px 0 12px">Workflow</h4>
          <p style="font-size:14px;color:var(--text2);line-height:1.6">{workflow}</p>
        </div>
        <div>
          <h4 style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin-bottom:12px">Deliverables</h4>
          <p style="font-size:14px;color:var(--text2);line-height:1.6">{deliverables}</p>
          <h4 style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent1);margin:16px 0 12px">Expected Results</h4>
          <p style="font-size:14px;color:var(--text2);line-height:1.6">{results}</p>
        </div>
      </div>
      <div class="service-faq" style="margin-top:24px;padding-top:20px;border-top:1px solid var(--border)">
        <details>
          <summary style="font-size:14px;font-weight:600;cursor:pointer;color:var(--text1)"><strong>FAQ:</strong> {faq_q}</summary>
          <p style="font-size:14px;color:var(--text2);line-height:1.6;margin-top:10px">{faq_a}</p>
        </details>
      </div>
      <div style="text-align:center;margin-top:24px">
        <a href="index.html#contact" class="nav-cta" style="display:inline-block;padding:12px 32px;font-size:14px">Request This Service</a>
      </div>
    </div>'''

services_hero = '''<!-- SERVICES HERO -->
<section class="page-hero" style="min-height:50vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 20px 60px;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-tag">What We Do</div>
      <h1>Comprehensive <span class="gradient-text">Creative Services</span></h1>
      <p style="max-width:700px;margin:0 auto;font-size:18px;line-height:1.7">From motion graphics to AI-powered content creation — we provide end-to-end production services that help brands stand out, connect with audiences, and drive measurable growth.</p>
    </div>
    <div class="page-hero-stats" style="display:flex;flex-wrap:wrap;justify-content:center;gap:40px;margin-top:40px">
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">19</div><div style="font-size:13px;color:var(--text2)">Services</div></div>
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">500+</div><div style="font-size:13px;color:var(--text2)">Projects Delivered</div></div>
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">48h</div><div style="font-size:13px;color:var(--text2)">Fast Turnaround</div></div>
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">&#11088; 5.0</div><div style="font-size:13px;color:var(--text2)">Client Rating</div></div>
    </div>
  </div>
</section>'''

# Service definitions
services = [
    ("Motion Graphics Design", "\U0001F3AC",
     "Professional motion graphics that bring your brand story to life. We create dynamic animated content from kinetic typography and logo reveals to explainer videos and broadcast graphics designed to capture attention and communicate complex ideas visually.",
     "Increased viewer retention by up to 60%;Enhanced brand recognition through consistent visual identity;Complex messages explained in seconds;Premium look that builds trust;Shareable content that boosts social engagement",
     "Brands launching new products or campaigns;Marketing teams needing explainer videos;Event organizers wanting promotional content;Corporate teams requiring internal communications;YouTube creators needing channel branding",
     "Brief, Script and storyboard, Style frames, Animation, Sound design, Review, Final delivery. Average project: 5-10 business days.",
     "Animated explainer video (30-90s);Branded social media templates;Broadcast graphics package;Product demo animations;Kinetic typography videos;Logo animation and stingers",
     "40-60% increase in viewer engagement;30% higher conversion on landing pages;Stronger brand recall;Professional brand perception",
     "How long does a motion graphics project take?",
     "A typical 60-second explainer animation takes 5-10 business days from concept to delivery. Rush delivery (48h) available for select projects."),

    ("Video Editing", "\u2702\uFE0F",
     "End-to-end video editing that transforms raw footage into polished, engaging content. Our editing workflow covers everything from rough cuts and color grading to sound design, transitions, and final export optimization for any platform.",
     "Professional polish that elevates brand perception;Time savings for creators and businesses;Consistent quality across all video content;Optimized exports for every platform;Faster turnaround than in-house editing",
     "Content creators needing regular uploads;Businesses repurposing event or meeting recordings;Agencies requiring clean published content;Podcasters wanting highlight reels;Anyone with raw footage who needs a polished final product",
     "Footage review, Rough cut, Client feedback, Fine cut, Color grading, Audio mix, Graphics, Final export, Delivery. Standard: 3-7 days per video.",
     "Fully edited video (any length);Color graded and sound mixed;Graphics and text overlays;Intro/outro sequences;Multiple format exports (MP4, MOV);Optimized versions for different platforms",
     "Higher audience retention rates;Professional quality that builds credibility;Consistent publishing schedule;Increased social shares and engagement",
     "Can you work with my existing raw footage?",
     "Yes. We accept footage from any camera, phone, or screen recording. Upload via Google Drive, Dropbox, or WeTransfer."),

    ("Social Media Content Creation", "\U0001F4F1",
     "Scroll-stopping social media content designed for maximum engagement. We create platform-optimized posts, stories, reels, and ads that align with your brand voice and drive real interaction.",
     "Consistent high-quality posting schedule;Platform-specific optimization;Higher engagement rates;Brand consistency across channels;More followers and community growth",
     "Brands wanting to grow their social presence;Influencers needing regular content;E-commerce stores showcasing products;Agencies managing multiple client accounts;Startups building brand awareness",
     "Audit, Content calendar, Asset creation, Caption writing, Scheduling, Engagement monitoring, Reporting. Ongoing retainer available.",
     "5-15 posts per week (platform-dependent);Custom graphic templates;Captions and hashtag research;Story templates and highlight covers;Monthly performance report",
     "2-5x increase in engagement rate;Consistent follower growth;Higher click-through to website;Improved brand sentiment and community",
     "How many posts should I publish per week?",
     "We recommend 5-7 posts plus daily Stories for Instagram, 3-5 posts for TikTok, and 3-4 for LinkedIn. Each platform has unique best practices we follow."),

    ("Short Form Video Editing", "\u26A1",
     "High-energy short-form videos optimized for TikTok, Instagram Reels, and YouTube Shorts. Our editing includes fast cuts, trending effects, text overlays, captions, and audio sync designed to hook viewers in the first 2 seconds.",
     "Higher completion rates (60-80% for short form);Faster content production (3-5 reels per day);Viral potential through trend-driven editing;Better algorithm performance;More affordable than long-form",
     "Brands needing daily short-form content;Influencers growing their following;Agencies producing UGC-style ads;Businesses hopping on trends;Podcasters creating clip content",
     "Trend research, Footage selection, Rough cut, Effects and captions, Audio sync, Export. Turnaround: 24-48h per batch.",
     "3-5 edited reels/shorts per batch;Captioned and subtitled;Music and sound effects;Trend-based transitions;Platform-optimized export;Source files included",
     "50-80% improvement in watch time;Higher share and save rates;Algorithm-friendly content;Increased profile visits and follows",
     "Can you edit from just a product and script?",
     "Absolutely. If you only have a product and brief, we can script, source footage, and edit using stock assets and motion graphics."),

    ("Long Form Video Editing", "\U0001F3A5",
     "Professional long-form editing for YouTube videos, documentaries, tutorials, podcasts, and corporate films. We handle complex timelines, multi-camera setups, color grading, sound mixing, and storytelling pacing.",
     "Professional cinematic quality;Better audience retention;Consistent upload schedule;Time savings (10+ hours per video);SEO-optimized descriptions and chapters",
     "YouTubers growing their channel;Educators creating course content;Podcasters publishing episodes;Corporate training videos;Documentary filmmakers",
     "Footage organization, Assembly edit, Story edit, Client review, Fine cut, Color grade, Audio mix, Graphics, Chapters and description, Export. 7-14 days for 15-30 min videos.",
     "Fully edited video (10-60 min);Color graded and mixed audio;Chapters and timestamps;SEO description and tags;Multiple export formats;Thumbnail (add-on option)",
     "Higher watch time and retention;Better YouTube algorithm ranking;Increased subscriber conversion;Professional production value",
     "How do I send you my footage?",
     "We accept footage via Google Drive, Dropbox, or direct upload. For large projects we can coordinate a shared drive."),

    ("Brand Identity Design", "\U0001F3A8",
     "Complete brand identity design that captures your essence and differentiates you in the market. From logo concepts to full brand guidelines, we create cohesive visual systems that communicate your brand story across every touchpoint.",
     "Clear consistent brand recognition;Professional first impression;Higher perceived value;Easier marketing and content creation;Better customer trust and loyalty",
     "Startups launching their brand;Businesses rebranding or refreshing;Founders wanting professional presence;Product companies needing packaging;Service businesses establishing credibility",
     "Discovery, Research, Moodboards, Logo concepts, Refinement, Brand guidelines, Asset delivery. 10-15 business days for full identity.",
     "Logo (primary, secondary, icon);Color palette;Typography system;Brand guidelines PDF;Business card design;Social media kit;Stationery templates",
     "Stronger brand recognition;Professional credibility;Consistent marketing materials;Clearer brand communication",
     "What is included in brand guidelines?",
     "Our brand guidelines document includes logo usage rules, color codes (HEX/RGB/CMYK), typography specifications, tone of voice guidelines, and application examples."),

    ("Social Media Management", "\U0001F4CA",
     "Complete social media management from strategy and content creation to publishing, community engagement, and performance analytics. We handle the day-to-day so you can focus on running your business.",
     "Consistent active presence;Time savings (10+ hours/week);Strategic content aligned with goals;Real-time engagement with audience;Data-driven optimization",
     "Small business owners with no time;Brands scaling their social presence;Agencies needing white-label management;E-commerce stores driving sales;Founders building personal brands",
     "Strategy, Content planning, Creation, Scheduling, Community management, Reporting, Optimization. Monthly retainer.",
     "Content calendar (30 days);Daily posts and stories;Community engagement;Monthly analytics report;Competitor analysis;Strategy adjustments",
     "30-50% increase in engagement;Consistent follower growth;Higher website traffic;Improved customer response times",
     "How many platforms do you manage?",
     "We recommend starting with 2-3 platforms maximum to maintain quality. Each additional platform requires 5+ hours per week of dedicated effort."),

    ("Content Strategy", "\U0001F4DD",
     "Data-driven content strategies that align your content production with business objectives. We develop content pillars, audience personas, distribution plans, and measurement frameworks to ensure every piece of content serves a purpose.",
     "Clear direction for all content;Better ROI on content investment;Reduced wasted production;Audience-focused approach;Measurable results tracking",
     "Marketing teams needing direction;Brands launching content programs;Agencies structuring client strategies;Businesses scaling content production;Founders building content engines",
     "Audit, Research, Persona development, Pillar definition, Channel strategy, Content calendar, Measurement framework, Documentation. 7-10 days.",
     "Content strategy document;Audience personas (2-3);Content pillars (4-5);30-day content calendar;Distribution and promotion plan;KPI framework",
     "Clear content direction;Reduced wasted content;Better audience alignment;Measurable content performance",
     "How often should strategy be updated?",
     "We recommend a full strategy review quarterly, with monthly performance check-ins to adjust tactics based on what is working."),

    ("YouTube Video Editing", "\u25B6\uFE0F",
     "Specialized YouTube editing that keeps viewers watching from the hook to the CTA. We optimize retention, add channel-branded elements, and ensure your videos perform well with YouTube's algorithm.",
     "Higher retention and watch time;Better search ranking;Professional production value;Faster turnaround;Algorithm-friendly formatting",
     "YouTubers of all sizes;Brands with YouTube channels;Educators and course creators;Review and tutorial creators;Vloggers and lifestyle channels",
     "Script review, Hook assembly, Main edit, Graphics, Color grade, Audio, Thumbnail, SEO. 3-7 days for standard videos.",
     "Edited video with retention optimization;Custom thumbnails;SEO title and description;End screens and cards;Chapters and timestamps;Transcript file",
     "Higher retention rates (40%+);Increased search visibility;Better CTR from thumbnails;More subscribers per video",
     "Do you do SEO for YouTube as well?",
     "Yes. We optimize video titles, descriptions, tags, and captions for search. We also create strategically designed thumbnails that drive clicks."),

    ("Instagram Reels Editing", "\U0001F4F9",
     "Reels crafted specifically for Instagram's algorithm. We create trend-aware, hook-driven content optimized for the 9:16 format that stops the scroll and drives profile visits.",
     "Algorithm-friendly content;Higher reach to non-followers;Consistent content pipeline;Trend-aware editing;Engagement-optimized hooks",
     "Brands growing on Instagram;Influencers and creators;E-commerce stores;Service businesses;Events and launches",
     "Trend research, Script, Footage, Fast-cut edit, Captions, Music, Export. 24-48h per batch of 3-5 Reels.",
     "3-5 edited Reels per batch;On-trend transitions;Text overlays and captions;Music sync;Hashtag research;Thumbnail cover",
     "2-5x increase in Reach;Higher profile engagement;More saves and shares;Faster follower growth",
     "How do you stay on top of trends?",
     "We monitor Instagram daily for emerging trends, sounds, and formats. Our team has a dedicated trend-watching process to ensure your content is always current."),

    ("TikTok Video Editing", "\U0001F4F3",
     "Native TikTok editing that understands the platform's unique culture, pacing, and trends. We create content that feels native using TikTok's signature fast cuts, text overlays, and viral sound integration.",
     "Platform-native feel;Trend-driven for algorithm boost;High completion rates;Viral potential;Affordable bulk production",
     "Brands entering TikTok;Creators growing their presence;Agencies managing TikTok accounts;Products targeting Gen Z;Businesses jumping on trends",
     "Trend analysis, Script, Production, Fast edit, Effects, Captions, Export. 12-24h per video.",
     "TikTok-optimized video (15-60s);Captions and text overlay;Trending sound integration;Green screen and effects;Hashtag strategy;Batch delivery available",
     "Higher completion and share rates;Algorithm-friendly performance;Increased profile visits;Authentic brand presence on TikTok",
     "What makes TikTok editing different?",
     "TikTok editing is faster-paced, trend-driven, and less polished than other platforms. It prioritizes authenticity and relatability over production value."),

    ("LinkedIn Content Design", "\U0001F4BC",
     "Professional LinkedIn content that builds thought leadership and generates B2B leads. We design carousels, documents, infographics, and posts that establish authority and drive professional engagement.",
     "Thought leadership positioning;B2B lead generation;Professional network growth;Higher post reach and engagement;Credibility and trust building",
     "B2B companies and founders;Executives building personal brands;Consultants and coaches;Recruiters and agencies;Sales professionals",
     "Topic research, Outline, Design, Copywriting, Carousel assembly, Scheduling, Engagement tracking. 2-4 days per batch.",
     "Carousel posts (5-10 slides);Text posts with design elements;Infographics;Document posts;Engagement-optimized copy;Hashtag research",
     "Higher post visibility;More profile views and connections;B2B lead generation;Professional authority building",
     "How often should I post on LinkedIn?",
     "We recommend 3-5 posts per week for consistent growth. Carousels perform best with 2-3x higher engagement than text posts."),

    ("Advertising Creatives", "\U0001F4E2",
     "High-converting ad creatives designed for Meta Ads, Google Ads, TikTok Ads, and LinkedIn Ads. We combine persuasive copywriting with compelling visuals to maximize ROAS.",
     "Higher click-through and conversion rates;Platform-compliant formats;A/B test-ready variations;Faster creative testing;Data-driven design decisions",
     "E-commerce brands scaling ads;SaaS companies running PPC;Agencies managing ad accounts;Local businesses advertising;Launch campaigns and promotions",
     "Brief, Audience review, Concept, Design, Copy, Variations, Export, Performance review. 3-5 days for a campaign set.",
     "3-5 ad creative variations;Headline and copy options;Multiple format exports;Platform-specific sizes;Campaign setup guide;Performance tracking links",
     "20-40% lower CPA;Higher click-through rates;More effective A/B testing;Scalable creative system",
     "Do you also manage ad campaigns?",
     "We focus on creative production. For campaign management and optimization, we recommend partnering with a media buyer."),

    ("Thumbnail Design", "\U0001F5BC\uFE0F",
     "Click-worthy thumbnails designed to maximize CTR on YouTube, blog posts, and social media. We use visual psychology, contrast, facial expressions, and clear messaging to make your content stand out.",
     "40-80% higher CTR;More views from existing reach;Professional first impression;Brand consistency;Competitive advantage",
     "YouTubers and video creators;Bloggers and publishers;Course creators;Podcasters;Anyone publishing visual content",
     "Brief, Concept, Design (2-3 options), Client selection, Final polish, Export. 24-48h per thumbnail.",
     "Custom thumbnail (2-3 concepts);High-res export (1280x720);Text overlay;Facial expression optimization;Brand-consistent styling;A/B test variants",
     "40-80% improvement in CTR;More views from impressions;Higher subscriber conversion;Professional content appearance",
     "What makes a good thumbnail?",
     "The best thumbnails have three elements: a clear focal point (face/object), high contrast, and a curiosity gap that makes people want to click."),

    ("AI Content Creation", "\U0001F916",
     "AI-powered content production that combines human creativity with machine efficiency. We use cutting-edge AI tools for scriptwriting, image generation, video creation, voiceovers, and ideation.",
     "10x faster content production;Lower costs than traditional methods;Consistent quality at scale;Innovative creative approaches;24/7 content generation capability",
     "Brands needing high-volume content;Agencies scaling production;Creators exploring AI workflows;Businesses wanting to stay ahead;Anyone curious about AI content",
     "Brief, AI tool selection, Prompt engineering, Generation, Human review and polish, Final delivery. 24-48h for most projects.",
     "AI-generated scripts and copy;AI video content;AI image generation;Voiceovers (AI or human);AI-assisted editing;Creative AI strategy",
     "Significantly faster turnaround;Cost-effective scaling;Consistent quality;Access to cutting-edge creative tools",
     "Does AI replace human creativity?",
     "No. AI is a tool that enhances human creativity. We use it to accelerate production and explore ideas faster, but every output is reviewed and refined by our creative team."),

    ("Animation", "\U0001F39E\uFE0F",
     "Custom 2D and 3D animation for brands, products, and stories. From character animation and explainer videos to product demos and abstract visualizations, we bring ideas to life with fluid motion and compelling narratives.",
     "Explains complex ideas visually;High shareability and engagement;Premium brand perception;Timeless content that stays relevant;Different from typical video content",
     "Brands explaining complex products;Educators and trainers;Marketing campaigns needing differentiation;Product launches;Internal communications",
     "Script, Storyboard, Style frames, Animation, Sound design, Review, Delivery. 10-20 business days for standard projects.",
     "Animated video (30-120s);Character animation;Product visualization;Motion graphics;Audio and music;Multiple format exports",
     "Higher shareability than live-action;Explains complex concepts easily;Premium brand positioning;Long shelf life (2-3 years)",
     "How is animation different from motion graphics?",
     "Animation typically involves characters, stories, and complex movement (rigging, keyframes) while motion graphics focuses on text, shapes, and data visualization. We do both."),

    ("Visual Storytelling", "\U0001F4D6",
     "Strategic visual storytelling that connects emotionally with your audience. We craft narratives through visuals — brand films, customer journeys, product stories — that resonate and drive action.",
     "Emotional connection with audience;Higher message retention;Stronger brand loyalty;Differentiation in crowded markets;Compelling shareable content",
     "Brands wanting emotional connection;Non-profits sharing their impact;Product launches with a story;Companies building brand love;Campaigns needing differentiation",
     "Discovery, Narrative development, Visual treatment, Production, Post-production, Review, Delivery. 7-14 days.",
     "Brand film (2-5 min);Customer story video;Product narrative;Visual treatment document;Storyboard;Distribution-ready formats",
     "Deeper audience connection;Higher brand recall;Increased shareability;Stronger emotional engagement",
     "Can you work with existing brand assets?",
     "Yes. We can build visual stories around existing footage, photos, and brand materials. A fresh edit and narrative structure can transform your existing assets."),

    ("Marketing Creative Design", "\U0001F4CB",
     "Marketing collateral design for both digital and print — from social ads and email banners to brochures, flyers, and presentation decks. Every asset is designed with conversion in mind.",
     "Consistent brand experience;Higher conversion from marketing assets;Time savings with on-demand design;Professional polish;Platform-specific optimization",
     "Marketing teams needing on-demand design;Businesses with consistent promotional needs;Event organizers needing collateral;Sales teams needing presentations;Agencies requiring white-label design",
     "Brief, Research, Concepts, Design, Review, Final, Export. 2-5 days per asset type.",
     "Social media ads (all formats);Email banners and headers;Brochures and flyers;Presentation decks;Media kit;E-book/PDF design",
     "Higher conversion rates;Consistent brand presentation;Professional marketing materials;Faster campaign launches",
     "Can you create designs for print?",
     "Yes. We design for both digital and print with proper CMYK color profiles, bleed, and resolution specifications. Print proofs are provided before final production."),

    ("Custom Creative Solutions", "\u2728",
     "Have a unique creative challenge? We offer custom creative solutions tailored to your specific needs. Whether it is a mixed-media project, experiential content, or something completely new.",
     "Tailored solution for unique needs;Innovative approach;One-on-one creative partnership;Flexible process and pricing;No cookie-cutter templates",
     "Brands with unique creative needs;Special projects beyond standard services;Experimental campaigns;Mixed-media projects;Any creative challenge",
     "Discovery call, Needs assessment, Custom proposal, Creative development, Iterative feedback, Final delivery. Timeline varies by project.",
     "Custom deliverables based on project;Full creative documentation;Source files;Usage rights;Support and maintenance options",
     "Unique solution to your specific challenge;Innovative competitive advantage;Personalized creative partnership",
     "What kind of custom projects have you done?",
     "Custom projects include interactive brand experiences, AI-powered content systems, full visual identity overhauls, and multi-platform campaign ecosystems. Tell us what you need.")
]

# Build services content
services_content = '''<section class="services-page" style="padding:60px 0;background:var(--bg2)"><div class="container">
    <div class="section-header reveal">
      <h2>Explore Our <span class="gradient-text">Services</span></h2>
      <p>Each service is backed by a proven workflow, clear deliverables, and measurable outcomes. Click any service to jump to its details.</p>
    </div>
    <div class="services-nav" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:40px;justify-content:center">'''

for i, (name, icon, *_) in enumerate(services):
    sid = name.lower().replace(' ','-').replace('&','and').replace('--','-')
    services_content += f'<a href="#service-{sid}" style="background:var(--card);border:1px solid var(--border);border-radius:20px;padding:8px 16px;font-size:13px;font-weight:500;color:var(--text1);text-decoration:none">{icon} {name}</a>'

services_content += '</div>'

for svc in services:
    services_content += service_card(*svc)

# CTA at bottom
services_content += '''
    <div class="cta-section reveal" style="text-align:center;background:linear-gradient(135deg,var(--accent1),#ff4757);border-radius:var(--radius);padding:60px 40px;margin-top:60px">
      <h3 style="font-size:28px;font-weight:800;color:#fff;margin:0 0 12px">Not Sure Which Service You Need?</h3>
      <p style="color:rgba(255,255,255,.85);font-size:16px;max-width:600px;margin:0 auto 24px">Book a free 15-minute discovery call. We will listen to your goals, recommend the right services, and give you a custom quote with no obligation.</p>
      <a href="index.html#contact" style="display:inline-block;background:#fff;color:var(--accent1);padding:14px 36px;border-radius:30px;font-weight:700;font-size:15px;text-decoration:none">Book Your Free Discovery Call &#8594;</a>
    </div>
  </div>
</section>'''

services_html = make_page('Services', services_hero, services_content)

with open('/data/data/com.termux/files/home/portfolio/services.html', 'w') as f:
    f.write(services_html)
print(f"services.html: {len(services_html)} chars OK")
