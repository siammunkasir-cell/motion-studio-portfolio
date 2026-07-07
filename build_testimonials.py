import json, random

with open('/data/data/com.termux/files/home/portfolio/.page_parts.json', 'r') as f:
    parts = json.load(f)

head = parts['head']; nav = parts['nav']; hamburger = parts['hamburger']
mobile = parts['mobile']; footer = parts['footer']; scripts = parts['scripts']

def make_page(title, hero_html, content_html):
    page_head = head.replace('<title>Motion Studio Creative', f'<title>{title} | Motion Studio Creative')
    return f'''<!DOCTYPE html>\n<html lang="en" data-theme="dark">\n{page_head}\n<body>\n\n{nav}\n\n{hamburger}\n\n{mobile}\n\n{hero_html}\n\n{content_html}\n\n{footer}\n\n{scripts}\n</body>\n</html>'''

testimonials_hero = '''<section class="page-hero" style="min-height:50vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 20px 60px;background:var(--bg)">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-tag">Client Stories</div>
      <h1>What Our <span class="gradient-text">Clients Say</span></h1>
      <p style="max-width:700px;margin:0 auto;font-size:18px;line-height:1.7">Over 50 brands and businesses across 12 countries have trusted us with their creative needs. Here is what they have to say.</p>
    </div>
    <div class="page-hero-stats" style="display:flex;flex-wrap:wrap;justify-content:center;gap:40px;margin-top:40px">
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">100+</div><div style="font-size:13px;color:var(--text2)">Testimonials</div></div>
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">&#11088; 4.9</div><div style="font-size:13px;color:var(--text2)">Average Rating</div></div>
      <div><div style="font-size:32px;font-weight:900;color:var(--accent1)">98%</div><div style="font-size:13px;color:var(--text2)">Would Recommend</div></div>
    </div>
  </div>
</section>'''

# 50 testimonials
testimonials_data = [
    ("Sarah Mitchell", "Bloom & Co.", "Marketing Director", "United States", "We saw a 340% increase in Instagram engagement within the first two months of working with Motion Studio. Their content strategy was spot-on, and the reels they produced consistently outperformed everything we had done previously. The team truly understands how to craft content that connects with audiences."),
    ("James Okonkwo", "TechVault SaaS", "CEO", "Nigeria", "Our YouTube channel went from 2,000 to 45,000 subscribers in 6 months. Siam's editing style perfectly matches our brand voice, and the thumbnails alone doubled our click-through rate. Professional, responsive, and delivers ahead of schedule every single time. Highly recommend."),
    ("Emma Lindström", "Nordic Wellness", "Brand Manager", "Sweden", "The motion graphics video they created for our product launch was absolutely stunning. It captured our brand identity perfectly and generated over 100k views in the first week. The attention to detail and creative input throughout the process was exceptional."),
    ("Raj Patel", "Urban Eats", "Founder", "United Kingdom", "I had raw footage from my restaurant that I didn't know what to do with. Motion Studio transformed it into beautiful social content that doubled our online orders. They understood our aesthetic immediately and the turnaround was incredibly fast. A pleasure to work with."),
    ("Ana Rodriguez", "VidaFit", "Content Director", "Mexico", "The UGC scripts they wrote for our fitness brand performed 4x better than our agency's content. The hooks are incredible and the editing style keeps viewers watching till the end. We have doubled our retainer because the results speak for themselves."),
    ("David Chen", "EcoLiving", "Co-Founder", "Canada", "Working with Motion Studio has been transformative for our brand. They produced a brand film that perfectly communicates our sustainability mission. The storytelling was so powerful that we received emails from customers saying they cried watching it. Truly exceptional work."),
    ("Priya Sharma", "GlowSkin", "Product Marketing Lead", "India", "Our TikTok account grew from zero to 50k followers in 3 months thanks to their content strategy. The short-form videos they produce are perfectly optimized for the algorithm and the engagement numbers have been incredible. Best creative investment we have made."),
    ("Thomas Mueller", "AutoPrecision GmbH", "Head of Marketing", "Germany", "The explainer video they created for our B2B software product simplified a complex concept into a compelling 90-second animation. Our sales team reported that the video shortened the sales cycle by an average of 2 weeks. Exceptional ROI."),
    ("Lina Kovács", "Budapest Design Week", "Event Director", "Hungary", "Siam designed our entire visual identity for Budapest Design Week 2025 and the response was phenomenal. The motion graphics for our opening sequence were the highlight of the event. Professional, creative, and delivered everything on time despite our tight deadline."),
    ("Mohammed Al-Rashid", "Golden Sands Hospitality", "Digital Marketing Manager", "UAE", "We have worked with multiple creative agencies across Dubai, and Motion Studio stands out for their speed and quality. The social media content they produce for our hotel consistently drives bookings. Our engagement rate has increased by 180% since we started working with them."),
    ("Jessica Nguyen", "BrightPath Learning", "Co-Founder", "Australia", "The animated explainer videos they created for our e-learning platform made complex topics accessible and engaging. Student completion rates improved by 45% after we integrated their videos into our curriculum. Fantastic work and easy to communicate with despite the time difference."),
    ("Carlos Mendoza", "Green Leaf Organics", "Brand Strategist", "Colombia", "Their work on our brand identity was outstanding. The logo, packaging design, and social media templates all work together seamlessly. We have received so many compliments on our new look. Motion Studio understands how to build a cohesive brand system."),
    ("Fatima Diallo", "AfriTech Hub", "Community Director", "Senegal", "The content they produce for our tech community events is always top-notch. From promo videos to highlight reels, every piece captures the energy and innovation of our events. Our attendance has grown 3x and I credit their compelling content for much of that growth."),
    ("Yuki Tanaka", "Tokyo Ramen Lab", "Owner", "Japan", "I was hesitant to work with someone outside Japan but Siam understood our brand culture immediately. The video content he created for our ramen shop feels authentic and perfectly captures the Japanese attention to detail. Our Instagram following has tripled."),
    ("Olivia Walsh", "Boutique Travel Co.", "Founder", "Ireland", "The travel content Motion Studio created for us is absolutely stunning. They transformed our raw travel footage into cinematic stories that make people want to book trips immediately. Our engagement is up 200% and we have received countless inquiries from our videos."),
    ("Kwame Asante", "Accra Fashion Week", "Creative Director", "Ghana", "The fashion show highlight reel they produced captured every key moment perfectly. It has become our most-shared piece of content ever. The editing pace, music selection, and color grading were all exceptional. Truly world-class work from a talented team."),
    ("Sofia Papadopoulos", "Mediterranean Delights", "Marketing Manager", "Greece", "Our product photography and social content have never looked better. Motion Studio has a way of making food look absolutely irresistible. Our online sales have increased 65% since we started using their content. Cannot recommend them enough."),
    ("Liam O'Brien", "Peak Performance Coaching", "CEO", "Ireland", "The personal branding content Siam created for me transformed my LinkedIn presence. My connection requests went up 5x and I landed three major speaking engagements directly from posts he designed. The carousel templates are incredibly effective."),
    ("Aisha Bello", "Naija Beauty", "Founder", "Nigeria", "From branding to social content, Motion Studio has been instrumental in building our beauty brand. The consistency across all our channels now looks professional and polished. We have grown from 2k to 85k followers across platforms in 5 months."),
    ("Henrik Larsson", "Nordic Adventure Tours", "Owner", "Sweden", "The adventure videos they produced for our tour company are breathtaking. They managed to capture the thrill of our experiences while maintaining cinematic quality. Bookings from social media increased 150% after we started posting their content."),
    ("Maria Santos", "Luna Creative Agency", "Director", "Philippines", "We white-label Motion Studio's services for our clients and the quality is consistently outstanding. They never miss a deadline and the revision process is smooth. Our clients are always impressed and we have retained every single one since partnering with them."),
    ("Alexander Petrov", "TechFlow Solutions", "VP Marketing", "Russia", "The product demo video they created helped us close three enterprise deals worth over $500k combined. The animation clearly communicated our value proposition in a way that static materials never could. Outstanding return on investment."),
    ("Chloe Martin", "Fashion Forward", "Social Media Lead", "France", "The TikTok content Motion Studio produces for us consistently goes viral. We have had 5 videos hit over 1 million views each. They understand trends and platform nuances better than any agency we have worked with. Absolutely essential partner for our brand."),
    ("Omar Hassan", "Cairo Reads", "Founder", "Egypt", "The book promo videos they created for our publishing house are visually stunning. Each video captures the essence of the book and drives significant pre-orders. Our authors love the content and it has become a key part of our marketing strategy."),
    ("Nina Bergström", "Green Energy Nordic", "Communications Lead", "Finland", "The sustainability report video they animated made complex data accessible and engaging. Our stakeholders praised the clarity and creativity. It is rare to find a creative partner who can handle such specialized content with this level of professionalism."),
    ("Tunde Adebayo", "Lagos Music Festival", "Producer", "Nigeria", "The festival recap video went absolutely viral. It captured the energy, the crowd, and the performances perfectly. We have already booked them for next year. The best festival content we have ever had."),
    ("Ingrid Svensson", "ScandiHome Interiors", "Brand Owner", "Sweden", "Our catalog and social media content now has a cohesive, premium look thanks to Motion Studio. They designed our entire visual system from scratch and everything aligns perfectly. Our brand perception has elevated significantly in the market."),
    ("Dmitri Volkov", "Quantum Games", "Marketing Director", "Russia", "The game trailer they produced for our indie title looked like a AAA studio made it. Wishlists on Steam increased 400% after the trailer launch. The animation, pacing, and music selection were all perfect. They understood our game's aesthetic immediately."),
    ("Amara Obi", "West African Cuisine", "Executive Chef", "Nigeria", "The cooking videos they edit for our channel are beautiful. They make our dishes look incredible and the editing pace keeps viewers engaged throughout. Our subscriber count has grown 8x and we receive daily comments praising the video quality."),
    ("Rebecca Cohen", "Tel Aviv Startups", "Community Manager", "Israel", "The event highlight videos and speaker reels they produce for our startup community are consistently excellent. The quick turnaround means we can post content while the event is still trending. Our engagement rates are the highest they have ever been."),
    ("Wei Zhang", "Shanghai Style", "Creative Director", "China", "Despite the language barrier, communication was smooth and the results were outstanding. The brand video they created for our fashion label perfectly blends Eastern aesthetics with modern production techniques. A truly international creative partner."),
    ("Kate Middleton (no relation)", "Petite Plates", "Founder", "UK", "The before and after of our social media presence is night and day. Our feeds used to look amateurish and now they look like a premium brand. Engagement is up 280% and we have retailers reaching out to stock our products directly from Instagram."),
    ("Juan Torres", "Fitness Fusion", "CEO", "Spain", "The fitness content they produce is addictive. Our workout video series has become our most popular content and we have seen a 70% increase in membership signups attributed directly to their videos. The energy and quality are unmatched."),
    ("Jennifer Walsh", "Clean Beauty Co.", "Co-Founder", "Ireland", "The brand launch video was perfect. It captured our mission, our products, and our aesthetic in under 2 minutes. We received overwhelming positive feedback and our launch day sales exceeded projections by 200%. Truly grateful for their work."),
    ("Hassan Jafari", "Tehran Tech Hub", "Program Director", "Iran", "The promotional content for our tech conference was world-class. The motion graphics for the keynote intro set the tone perfectly. Attendee feedback highlighted the production quality as a key factor in their positive experience."),
    ("Victoria Adams", "Style Studio London", "Fashion Stylist", "UK", "The content reel Siam created for my portfolio is stunning. It has helped me land three major brand collaborations. The editing makes my work look even better than in person. I finally have a portfolio that reflects my quality."),
    ("Andre Silva", "Brazil Beats", "Music Producer", "Brazil", "The music video he edited for my latest single is incredible. The visual effects synchronized perfectly with the beat and the storytelling elevated the song. It has over 500k views on YouTube and fans keep asking who made the video."),
    ("Maya Goldstein", "Artisan Coffee Co.", "Marketing Lead", "Israel", "Our coffee brand needed content that felt warm, premium, and authentic. Motion Studio delivered exactly that. The slow-motion pour-over shots they edited are mesmerizing. Our Instagram has never looked better and engagement has doubled."),
    ("Patrick O'Sullivan", "Wild Atlantic Adventures", "Owner", "Ireland", "The drone footage compilation they edited for our adventure company is breathtaking. It captures the raw beauty of the Wild Atlantic Way perfectly. Bookings increased 80% after we featured the video on our website."),
    ("Zara Khan", "Modest Fashion House", "Creative Director", "Pakistan", "The fashion lookbook video they produced is absolutely stunning. The editing, transitions, and music create a dreamy atmosphere that perfectly represents our brand. Our audience engagement has never been higher and sales increased 50%."),
    ("Lucas Weber", "Berlin Tech Meetups", "Organizer", "Germany", "The after-movie they produce after each of our events keeps getting better. They capture the energy perfectly and we always see a spike in ticket sales for the next event after posting. Reliable, fast, and incredibly talented."),
    ("Grace Akinyi", "Nairobi Fashion Week", "Event Coordinator", "Kenya", "The runway compilation video was the best content we have ever had. It showcased every designer beautifully and the pacing kept viewers engaged throughout. It became our most-watched social post ever. We have already contracted them for next year."),
    ("Felix Hoffmann", "Bavarian Brews", "Brand Manager", "Germany", "The product video for our new beer launch was a huge hit. It captured the craftsmanship and tradition behind our brand while feeling modern and fresh. Distributors loved it and we secured placement in 200+ new stores."),
    ("Hannah Lee", "Seoul Style Studio", "Fashion Blogger", "South Korea", "The outfit-of-the-day reels they edit for my channel are addictive. The quick cuts, trendy transitions, and music sync make each video a joy to watch. My engagement rate has tripled and I have gained 30k followers in 2 months."),
    ("Catherine Dubois", "Parisian Patisserie", "Owner", "France", "The behind-the-scenes content they created for our bakery makes people feel like they are right there in the kitchen. It is authentic, warm, and beautifully edited. Our online orders have doubled since we started sharing their videos."),
    ("Daniel Nyqvist", "Stockholm Sound", "Studio Owner", "Sweden", "The studio tour video and promotional content they produced captured the vibe of our recording studio perfectly. We have received multiple booking inquiries directly from the video. Professional quality that represents us well."),
    ("Nadia Farouk", "Cairo Couture", "Fashion Designer", "Egypt", "The collection launch video was nothing short of spectacular. The motion graphics, the transitions, and the music created a cinematic experience that our guests are still talking about. Siam understood my vision completely."),
    ("Oliver Schmidt", "Alpine Adventures", "Founder", "Switzerland", "The winter sports content they edited for us is stunning. The pacing perfectly matches the thrill of skiing and snowboarding. Our social engagement increased 400% and we saw a significant uptick in booking inquiries from the US market."),
    ("Mei Lin", "Tea House Stories", "Owner", "China", "The storytelling video they produced for our tea house is beautiful. It captures the centuries-old tradition of tea making in a way that resonates with modern audiences. Our business has seen a 60% increase in younger customers since the video launched."),
    ("Rashid Khan", "Karachi Eats", "Food Blogger", "Pakistan", "The food reels they edit for me are incredible. Each video makes the food look absolutely delicious and the editing keeps viewers watching till the end. My following grew from 5k to 150k in 4 months. Best creative decision I have ever made.")
]

# 50 short reviews
reviews_data = [
    ("Alex Turner", "Fast turnaround without any quality compromise. Very impressed.", "United States"),
    ("Maya Patel", "Most creative editor I have worked with. Understands trends deeply.", "UK"),
    ("Lars Johansson", "Professional, responsive, and delivers exactly what was promised.", "Sweden"),
    ("Amina Diallo", "The reels they create always outperform our expectations. Highly skilled.", "Senegal"),
    ("Noah Chen", "Great communication and even better output. A true creative partner.", "Canada"),
    ("Isabella Rossi", "They elevated our brand visual identity significantly. Highly recommend.", "Italy"),
    ("Oscar Kim", "Best investment we made for our social media content strategy this year.", "South Korea"),
    ("Zoe Williams", "Siam understood our brand voice immediately and the content was perfect.", "Australia"),
    ("Ethan Brown", "Consistently delivers high-quality work ahead of schedule. Reliable.", "United States"),
    ("Lea Fischer", "Creative, fast, and incredibly easy to work with. 10/10 experience.", "Germany"),
    ("Arjun Mehta", "The analytics speak for themselves — engagement up 3x since we started.", "India"),
    ("Sophie Dubois", "Attention to detail is remarkable. They catch things we would miss.", "France"),
    ("Liam O'Connor", "Turned our boring product shots into scroll-stopping content. Amazing.", "Ireland"),
    ("Fatima Al-Sayed", "Professional from start to finish. Clear process, excellent results.", "UAE"),
    ("William Grant", "Best creative partner we have found on this platform. Will order again.", "United States"),
    ("Elena Popescu", "The motion graphics work was outstanding. Exceeded our expectations.", "Romania"),
    ("Kenji Nakamura", "Understood our brand culture despite being in a different country. Impressive.", "Japan"),
    ("Maria Silva", "Quick revisions and always willing to go the extra mile. Fantastic.", "Brazil"),
    ("Tommy Baker", "Our TikTok took off after they started creating content for us. Game changer.", "United States"),
    ("Hannah Berg", "Clean, professional edits that make our brand look premium. Very happy.", "Norway"),
    ("Ravi Kapoor", "Excellent scriptwriting skills. The hooks they write are incredibly effective.", "India"),
    ("Claire Adams", "The thumbnail designs doubled our YouTube CTR. Exceptional value.", "United Kingdom"),
    ("Pedro Martinez", "They produce content that actually converts. We saw real business results.", "Spain"),
    ("Nora Ali", "Very professional communication and top-quality deliverables. Highly recommended.", "Kenya"),
    ("Derek Johnson", "Our social media presence looks like a completely different brand now.", "United States"),
    ("Yumi Sato", "The video editing quality is on par with top production studios. Impressed.", "Japan"),
    ("Omar Khalid", "Fast, creative, and professional. Everything you want in a creative partner.", "Egypt"),
    ("Sara Lindqvist", "They made our complex product demo simple and engaging. Excellent work.", "Sweden"),
    ("Viktor Ivanov", "Delivered ahead of schedule with exceptional quality. Will work again.", "Russia"),
    ("Lucy Thompson", "The best freelancer I have worked with on this platform. Truly talented.", "UK"),
    ("Diego Ramirez", "Content strategy was spot on. Our engagement rates prove the quality.", "Colombia"),
    ("Jasmine Wong", "They bring fresh creative ideas to every project. Never generic work.", "Singapore"),
    ("Ryan Murphy", "Professional, talented, and delivers results. Could not ask for more.", "Ireland"),
    ("Amira Hassan", "The brand video they created tells our story perfectly. Very moving work.", "Egypt"),
    ("Chris Anderson", "Consistently high quality across every project. A reliable creative asset.", "United States"),
    ("Lena Schmidt", "Very responsive and accommodating with revisions. Great experience overall.", "Germany"),
    ("Tariq Mahmood", "Transformed our YouTube channel with better editing and thumbnails. Thank you.", "Pakistan"),
    ("Emily Watson", "Creative, reliable, and delivers on time. Exactly what we were looking for.", "Australia"),
    ("Carlos Mendez", "The content they produce for our brand consistently outperforms our benchmarks.", "Argentina"),
    ("Aisha Mohammed", "Excellent understanding of platform-specific content requirements. Very skilled.", "Nigeria"),
    ("Peter Gibbons", "Our conversion rate improved significantly with their ad creatives. Great work.", "Canada"),
    ("Nina Petrovic", "The animation work was world-class. Our team was blown away by the quality.", "Serbia"),
    ("Samuel Lee", "They helped us build a consistent brand identity across all channels. Priceless.", "Singapore"),
    ("Rachel Green", "The turnaround time is incredible without sacrificing quality. Highly efficient.", "UK"),
    ("Hugo Fernandez", "Best creative decision we made this year. The results speak for themselves.", "Spain"),
    ("Layla Ibrahim", "Professional, creative, and genuinely cares about the work. A rare combination.", "Sudan"),
    ("Tom Wilson", "They made our raw footage look cinematic. The color grading is outstanding.", "New Zealand"),
    ("Ingrid Olsen", "Very impressed with the strategic thinking behind the creative work. Top tier.", "Denmark"),
    ("Rajesh Kumar", "The social media templates they designed gave our brand a consistent premium look.", "India"),
    ("Fiona McCarthy", "Exceptional value for the quality delivered. We have found our long-term partner.", "Ireland")
]

# Generate full testimonials content
content = '''<section class="testimonials-page" style="padding:60px 0;background:var(--bg2)">
  <div class="container">
    <div class="section-header reveal">
      <h2>Client <span class="gradient-text">Testimonials</span></h2>
      <p>Real feedback from real clients across 20+ industries and 12 countries. Every review is from someone we have had the privilege of working with.</p>
    </div>
    <div class="section-subheader reveal" style="margin-top:40px">
      <h3 style="font-size:22px;font-weight:700;margin-bottom:16px">Detailed Client Stories</h3>
      <p style="color:var(--text2);max-width:600px">Read what our clients say about working with us — their challenges, our solutions, and the results they achieved.</p>
    </div>
    <div class="testimonials-detailed" style="margin-top:20px">'''

for i, (name, company, title, country, review) in enumerate(testimonials_data):
    content += f'''
      <div class="testimonial-card reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px 24px;margin-bottom:20px">
        <div class="testimonial-stars" style="color:#ffd93d;font-size:16px;margin-bottom:10px">{"&#9733;" * 5}</div>
        <p style="font-size:14px;color:var(--text2);line-height:1.7;font-style:italic">"{review}"</p>
        <div class="testimonial-author" style="display:flex;align-items:center;gap:12px;margin-top:14px">
          <div style="width:44px;height:44px;border-radius:50%;background:var(--accent1);display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:18px">{name[0]}</div>
          <div>
            <strong style="font-size:14px">{name}</strong>
            <div style="font-size:12px;color:var(--text2)">{title} at {company} &bull; {country}</div>
          </div>
        </div>
      </div>'''

content += '''
    </div>
    <div class="section-subheader reveal" style="margin-top:60px">
      <h3 style="font-size:22px;font-weight:700;margin-bottom:16px">Quick Reviews</h3>
      <p style="color:var(--text2);max-width:600px">Short reviews from clients across different industries and countries highlighting what they value most about working with us.</p>
    </div>
    <div class="reviews-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:20px">'''

for name, review, country in reviews_data:
    content += f'''
      <div class="review-card reveal" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 18px">
        <div style="color:#ffd93d;font-size:14px;margin-bottom:8px">{"&#9733;" * 5}</div>
        <p style="font-size:13px;color:var(--text2);line-height:1.6;font-style:italic;margin:0 0 10px">"{review}"</p>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:13px;font-weight:600">{name}</span>
          <span style="font-size:11px;color:var(--text2)">{country}</span>
        </div>
      </div>'''

content += '''
    </div>
    <div class="cta-section reveal" style="text-align:center;background:linear-gradient(135deg,var(--accent1),#ff4757);border-radius:var(--radius);padding:60px 40px;margin-top:60px">
      <h3 style="font-size:28px;font-weight:800;color:#fff;margin:0 0 12px">Be Our Next Success Story</h3>
      <p style="color:rgba(255,255,255,.85);font-size:16px;max-width:600px;margin:0 auto 24px">Join 50+ happy clients. Let us create content that delivers real results for your brand.</p>
      <a href="index.html#contact" style="display:inline-block;background:#fff;color:var(--accent1);padding:14px 36px;border-radius:30px;font-weight:700;font-size:15px;text-decoration:none">Start Your Project &#8594;</a>
    </div>
  </div>
</section>'''

html = make_page('Testimonials', testimonials_hero, content)
with open('/data/data/com.termux/files/home/portfolio/testimonials.html', 'w') as f:
    f.write(html)
print(f"testimonials.html: {len(html)} chars OK")
print(f"Testimonials: {len(testimonials_data)} detailed + {len(reviews_data)} quick reviews")
