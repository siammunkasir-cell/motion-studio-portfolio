"""
Seed data script for Siam Munkasir Portfolio
Inserts 30 testimonials, 50 reviews, 20 FAQs, and 17 skills into the database.
Run: python seed_data.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def seed_testimonials():
    testimonials = [
        ('Sarah Mitchell', 'TechVista Inc.', 'Marketing Director', 'Absolutely incredible work. The motion graphics exceeded our expectations and perfectly captured our brand identity. Our engagement metrics have never been better.', 5, 'United States', '2026-06-15'),
        ('James Chen', 'Luminary Studios', 'CEO', 'Working with this team was a game-changer for our content strategy. The level of creativity and attention to detail is unmatched in the industry.', 5, 'Canada', '2026-06-10'),
        ('Priya Patel', 'Digital Horizon', 'Head of Content', 'The best investment we have made for our social media presence. The animations are stunning and have dramatically improved our conversion rates.', 5, 'India', '2026-06-05'),
        ('Marcus Thompson', 'Elevate Brand Co.', 'Brand Manager', 'Exceptional quality and professionalism. Every project was delivered on time with outstanding results. Our clients constantly compliment the videos.', 5, 'United Kingdom', '2026-05-28'),
        ('Elena Rodriguez', 'Viva Media Group', 'Creative Director', 'I have worked with many motion designers, but none have delivered the level of creativity and technical skill that this team brought to our projects.', 5, 'Spain', '2026-05-20'),
        ('Kenji Nakamura', 'Sakura Digital', 'VP Marketing', 'The explainer video they created for our product launch was perfect. Clear, engaging, and beautifully animated. Our sales team loves it.', 5, 'Japan', '2026-05-15'),
        ('Amara Okafor', 'AfriTech Solutions', 'CEO', 'Outstanding work! They understood our vision immediately and brought it to life in ways we could not have imagined. Highly recommended.', 5, 'Nigeria', '2026-05-10'),
        ('Oliver Schmidt', 'Bavaria Media', 'Content Strategist', 'The Instagram Reels content has transformed our social media presence. Engagement is up 300% since we started working together.', 5, 'Germany', '2026-05-05'),
        ('Sophie Laurent', 'Maison Creative', 'Art Director', 'Elegant, professional, and incredibly creative. The corporate video they produced for our brand launch was a masterpiece.', 5, 'France', '2026-04-28'),
        ('Liam O\'Brien', 'Celtic Media Group', 'Director of Operations', 'From concept to delivery, every step was handled with utmost professionalism. The final product was beyond what we envisioned.', 5, 'Ireland', '2026-04-20'),
        ('Aisha Rahman', 'Nusantara Creative', 'Founder', 'I was blown away by the quality of work. The motion graphics for our campaign were visually stunning and highly effective.', 5, 'Indonesia', '2026-04-15'),
        ('Carlos Mendez', 'Fuego Media', 'Head of Production', 'Fast turnaround without compromising quality. They managed our tight deadline perfectly and delivered exceptional work.', 5, 'Mexico', '2026-04-10'),
        ('Yuki Tanaka', 'Tokyo Studio One', 'Creative Lead', 'The attention to detail in every frame is remarkable. These are truly world-class motion graphics professionals.', 5, 'Japan', '2026-04-05'),
        ('Hannah Bauer', 'Alpine Media', 'Marketing Lead', 'Our YouTube channel has never looked better. The video editing and motion graphics have significantly improved our viewer retention.', 5, 'Switzerland', '2026-03-28'),
        ('Ahmed Hassan', 'Desert Rose Media', 'CEO', 'Professional, creative, and reliable. They delivered outstanding content for our advertising campaign that resonated perfectly with our audience.', 5, 'UAE', '2026-03-20'),
        ('Emma Wilson', 'Pacific Creative', 'Brand Director', 'The best decision we made this year. Our brand videos now look world-class and our clients are consistently impressed.', 5, 'Australia', '2026-03-15'),
        ('Lucas Andersen', 'Nordic Media House', 'Creative Director', 'Incredible talent and exceptional service. They go above and beyond to ensure the final product exceeds expectations.', 5, 'Denmark', '2026-03-10'),
        ('Maria Santos', 'Brazil Media Group', 'Content Director', 'The social media content strategy they developed for us was genius. Every video performs exceptionally well.', 5, 'Brazil', '2026-03-05'),
        ('David Kim', 'Seoul Creative Lab', 'Art Director', 'Outstanding motion design skills. The commercial they produced for our brand was cinematic and highly engaging.', 5, 'South Korea', '2026-02-28'),
        ('Natasha Volkov', 'Baltic Media', 'Marketing Director', 'Professionalism and creativity at the highest level. They understood our brand voice perfectly and delivered exceptional content.', 5, 'Russia', '2026-02-20'),
        ('Ryan O\'Connor', 'Shamrock Media', 'CEO', 'Transformed our video content completely. The quality is consistently excellent and our audience engagement has skyrocketed.', 5, 'Ireland', '2026-02-15'),
        ('Zara Al-Farsi', 'Oasis Creative', 'Brand Strategist', 'The explainer video they created simplified our complex product perfectly. Our customer understanding has improved dramatically.', 5, 'Saudi Arabia', '2026-02-10'),
        ('Felix Wagner', 'Rhine Media', 'Content Manager', 'I am consistently impressed by the creativity and technical skill. They are true masters of their craft.', 5, 'Austria', '2026-02-05'),
        ('Isabella Rossi', 'Mediterranean Studio', 'Creative Lead', 'The corporate videos they produced elevated our brand image significantly. Every detail was carefully considered and executed.', 5, 'Italy', '2026-01-28'),
        ('Thomas Berg', 'Scandinavian Media', 'Head of Video', 'Reliable, creative, and incredibly talented. The motion graphics work they delivered was nothing short of extraordinary.', 5, 'Sweden', '2026-01-20'),
        ('Mei Lin', 'Dragon Media Group', 'Marketing VP', 'Exceptional work on our product launch campaign. The videos were visually stunning and highly effective at driving conversions.', 5, 'Singapore', '2026-01-15'),
        ('Pieter van der Berg', 'Dutch Creative', 'Creative Director', 'They brought our brand story to life in ways we never imagined. The animation quality is world-class.', 5, 'Netherlands', '2026-01-10'),
        ('Nadia Petrov', 'Eastern Media', 'Content Strategist', 'The Instagram content they create for us consistently outperforms everything else we post. Truly exceptional work.', 5, 'Poland', '2026-01-05'),
        ('Ahmet Yilmaz', 'Bosphorus Media', 'CEO', 'From initial consultation to final delivery, the experience was flawless. The results speak for themselves - outstanding work.', 4, 'Turkey', '2025-12-28'),
        ('Grace Osei', 'Golden Media', 'Brand Manager', 'I appreciate how they took the time to understand our brand before creating the content. The result was perfectly aligned with our vision.', 5, 'Ghana', '2025-12-20'),
    ]

    conn = get_db()
    count = 0
    for t in testimonials:
        conn.execute('''INSERT OR IGNORE INTO testimonials (client_name, company, role, content, rating, avatar_url, featured, created_at)
                      VALUES (?,?,?,?,?,?,1,?)''',
                     (t[0], t[1], t[2], t[3], t[4], '', t[6] if len(t) > 6 else '2026-01-01'))
        count += 1
    conn.commit()
    conn.close()
    print(f"✓ Inserted {count} testimonials")

def seed_reviews():
    reviews = [
        ('Alex Johnson', 'United States', 5, 'Motion Graphics', 'The motion graphics work was absolutely phenomenal. They took our rough concept and turned it into a visually stunning animation that perfectly communicated our message. The attention to detail and creative flair was beyond impressive.', '2026-06-01'),
        ('Maria Garcia', 'Spain', 5, 'Video Editing', 'Incredible video editing skills. They transformed our raw footage into a polished, professional video that tells a compelling story. The pacing, transitions, and color grading were all perfect.', '2026-05-28'),
        ('David Brown', 'United Kingdom', 5, 'Explainer Video', 'Our explainer video came out better than we could have imagined. They managed to take complex concepts and make them simple, engaging, and visually appealing. Highly recommend their services.', '2026-05-25'),
        ('Lisa Wang', 'Singapore', 5, 'Instagram Reels', 'The Instagram Reels content they created for us has been a game-changer. Our engagement rates have tripled and we are getting so many compliments on the quality of our content.', '2026-05-22'),
        ('Mohammed Ali', 'UAE', 5, 'Brand Video', 'The brand video they produced captured our essence perfectly. It was cinematic, emotional, and professionally executed. This is the best investment we have made in our marketing.', '2026-05-20'),
        ('Sarah Johnson', 'Canada', 4, 'YouTube Editing', 'Great YouTube editing services. The videos are well-paced, engaging, and the thumbnail designs are excellent. Communication could be slightly faster but the quality makes up for it.', '2026-05-18'),
        ('Tom Williams', 'Australia', 5, 'Motion Graphics', 'Exceptional motion graphics work! They created an animated intro for our channel that looks incredibly professional. Our subscribers love it and it has really elevated our brand.', '2026-05-15'),
        ('Emily Chen', 'China', 5, 'Social Media Videos', 'Outstanding social media content! Every video they create for us is perfectly optimized for each platform. The creativity and production quality is consistently excellent.', '2026-05-12'),
        ('Robert Taylor', 'United States', 5, 'Corporate Video', 'The corporate video they produced for our annual report was stunning. It made complex data engaging and accessible. Our stakeholders were incredibly impressed.', '2026-05-10'),
        ('Anna Kowalski', 'Poland', 5, '2D Animation', 'Beautiful 2D animation work. The character design and motion were fluid and engaging. They brought our story to life in a way that connected deeply with our audience.', '2026-05-08'),
        ('James Wilson', 'New Zealand', 5, 'Motion Design', 'World-class motion design. Every element was thoughtfully designed and animated. The final product exceeded our expectations and has significantly improved our brand perception.', '2026-05-05'),
        ('Sophie Martin', 'France', 4, 'Video Editing', 'Professional video editing services. They polished our raw footage beautifully and the final product was clean and engaging. Would appreciate faster turnaround but quality is top-notch.', '2026-05-03'),
        ('Daniel Lee', 'South Korea', 5, 'Advertisement Video', 'The advertisement video they created was cinematic and highly effective. It has generated tremendous response for our campaign. Truly exceptional work.', '2026-05-01'),
        ('Rachel Green', 'United States', 5, 'Motion Graphics', 'Absolutely love the motion graphics work! They made our presentation come alive with stunning animations. Our clients were blown away by the visual quality.', '2026-04-28'),
        ('Omar Hassan', 'Egypt', 5, 'Explainer Video', 'The best explainer video we have ever had. They simplified our complex product features into an engaging, easy-to-understand animation. Highly recommended for any business.', '2026-04-25'),
        ('Nina Petersen', 'Denmark', 5, 'Brand Video', 'Exceptional brand video production. They captured our company culture and values perfectly. The storytelling was powerful and the production quality was outstanding.', '2026-04-22'),
        ('Chris Anderson', 'United Kingdom', 5, 'YouTube Editing', 'Transformed our YouTube channel completely. The editing style is engaging and keeps viewers watching till the end. Our retention rates have improved significantly.', '2026-04-20'),
        ('Yuki Sato', 'Japan', 5, 'Motion Graphics', 'Precision and artistry combined perfectly. The motion graphics work was technically flawless and artistically stunning. They truly understand the craft at the highest level.', '2026-04-18'),
        ('Laura Hernandez', 'Mexico', 4, 'Instagram Reels', 'Great Instagram Reels content that resonates well with our audience. The creativity is excellent and the production quality is consistently high. Minor delays sometimes but worth the wait.', '2026-04-15'),
        ('Kevin O\'Brien', 'Ireland', 5, 'Social Media Videos', 'Our social media presence has transformed since we started working together. The video content is engaging, on-brand, and performs exceptionally well on every platform.', '2026-04-12'),
        ('Isabella Costa', 'Italy', 5, 'Motion Design', 'Beautiful motion design that perfectly represents our brand aesthetic. The animations are smooth, elegant, and highly professional. A true artist at work.', '2026-04-10'),
        ('Raj Patel', 'India', 5, 'Corporate Video', 'The corporate video was a masterpiece. They managed to make our company story engaging and emotionally resonant. Our team was incredibly moved by the final result.', '2026-04-08'),
        ('Hannah Muller', 'Switzerland', 5, 'Explainer Video', 'Clear, concise, and visually stunning explainer video. They took our technical product and made it accessible and engaging. Excellent work from start to finish.', '2026-04-05'),
        ('Viktor Ivanov', 'Russia', 5, 'Motion Graphics', 'Incredible attention to detail in every frame. The motion graphics work was technically sophisticated and visually impressive. True professionals at the top of their game.', '2026-04-03'),
        ('Amanda Foster', 'Canada', 5, 'Video Editing', 'Outstanding video editing that transformed our raw footage into a compelling narrative. The pacing, music selection, and transitions were all perfectly executed.', '2026-04-01'),
        ('Carlos Silva', 'Brazil', 5, 'Advertisement Video', 'The advertisement they created for our campaign was incredibly effective. It captured attention immediately and drove great results. Creative genius at work.', '2026-03-28'),
        ('Elena Popescu', 'Romania', 4, 'Social Media Videos', 'Good social media video content that performs well. The quality is consistently good and the turnaround time is reasonable. Some minor improvements in creativity would be welcome.', '2026-03-25'),
        ('Faisal Ahmed', 'Bangladesh', 5, 'Motion Graphics', 'Absolutely brilliant motion graphics work. They understood exactly what we needed and delivered beyond expectations. Our brand looks world-class thanks to their work.', '2026-03-22'),
        ('Grace Kim', 'United States', 5, '2D Animation', 'Charming and professional 2D animation that perfectly captured our brand personality. The characters were lovable and the animation was smooth and engaging.', '2026-03-20'),
        ('Thabo Nkosi', 'South Africa', 5, 'Brand Video', 'A powerful brand video that tells our story beautifully. They captured the essence of our company and presented it in the most compelling way possible.', '2026-03-18'),
        ('Ingrid Svensson', 'Sweden', 5, 'Motion Design', 'Elegant and sophisticated motion design. Every animation choice was intentional and impactful. Working with them was an absolute pleasure.', '2026-03-15'),
        ('Pedro Santos', 'Portugal', 5, 'Instagram Reels', 'Our Instagram has never looked better. The Reels content is creative, on-trend, and perfectly tailored to our audience. Engagement has soared since we started.', '2026-03-12'),
        ('Naomi Wanjiku', 'Kenya', 5, 'Video Editing', 'Professional video editing that elevated our content significantly. The color grading was beautiful and the overall production quality was outstanding.', '2026-03-10'),
        ('Hans Gruber', 'Germany', 4, 'Corporate Video', 'Solid corporate video production. The quality was very good and they followed our brand guidelines carefully. Some room for more creative input but overall satisfied.', '2026-03-08'),
        ('Mia Torres', 'Philippines', 5, 'Motion Graphics', 'Incredible motion graphics that made our marketing campaign stand out. The animations were creative, polished, and highly effective at communicating our message.', '2026-03-05'),
        ('Lars Johansson', 'Norway', 5, 'Explainer Video', 'The explainer video was perfectly executed. They took our complex SaaS product and made it simple, visual, and engaging. Our conversion rates have improved noticeably.', '2026-03-02'),
        ('Fatima Al-Rashid', 'Qatar', 5, 'Brand Video', 'A stunning brand video that perfectly represents our premium positioning. Every frame was beautifully composed and the storytelling was powerful.', '2026-02-28'),
        ('William Chen', 'Taiwan', 5, 'YouTube Editing', 'Excellent YouTube video editing. The content is well-structured, engaging, and professionally polished. Viewers consistently compliment the production quality.', '2026-02-25'),
        ('Sofia Andersson', 'Finland', 5, 'Motion Design', 'Minimal yet powerful motion design. They understood our Nordic aesthetic perfectly and delivered work that was both beautiful and functional.', '2026-02-22'),
        ('Diego Morales', 'Argentina', 5, 'Social Media Videos', 'Transformative social media video content. Our engagement rates have doubled and the brand perception has improved dramatically. Exceptional work.', '2026-02-20'),
        ('Aya Tanaka', 'Japan', 4, 'Motion Graphics', 'Very good motion graphics work with great attention to detail. The animations are clean and professional. Sometimes the creative process took longer than expected but results were worth it.', '2026-02-18'),
        ('Ryan Murphy', 'Australia', 5, 'Advertisement Video', 'The advertisement they produced was a hit with our target audience. The creative concept was strong and the execution was flawless. Highly effective campaign.', '2026-02-15'),
        ('Lea Moreau', 'Belgium', 5, '2D Animation', 'Delightful 2D animation work that brought our childrens educational content to life. The characters were charming and the animation style was perfect for our audience.', '2026-02-12'),
        ('Oleg Volkov', 'Ukraine', 5, 'Video Editing', 'Professional video editing with excellent pacing and narrative flow. They transformed hours of footage into an engaging 5-minute story. Exceptional work.', '2026-02-10'),
        ('Carmen Diaz', 'Colombia', 5, 'Motion Graphics', 'Vibrant and dynamic motion graphics that perfectly match our brand energy. Every project is delivered with creativity and technical excellence.', '2026-02-08'),
        ('Abdullah Khan', 'Pakistan', 5, 'Instagram Reels', 'The Instagram Reels content they create is always fresh, engaging, and on-trend. Our follower growth has accelerated since we started working together.', '2026-02-05'),
        ('Helena Berg', 'Czech Republic', 5, 'Brand Video', 'A beautifully crafted brand video that tells our story with authenticity and emotion. The production quality was outstanding and the team was a pleasure to work with.', '2026-02-02'),
        ('George Constantinou', 'Greece', 5, 'Explainer Video', 'Excellent explainer video that clearly communicates our value proposition. The animation quality is top-notch and the script was well-written and engaging.', '2026-01-28'),
        ('Kate Nguyen', 'Vietnam', 5, 'Social Media Videos', 'Our social media content has never been better. Each video is tailored perfectly to the platform and audience. The creativity and quality are consistently outstanding.', '2026-01-25'),
        ('Jan Novak', 'Slovakia', 4, 'Motion Graphics', 'Good quality motion graphics work. The animations are professional and clean. Some projects had longer turnaround times but the final results were satisfactory.', '2026-01-22'),
    ]

    conn = get_db()
    count = 0
    for r in reviews:
        conn.execute('''INSERT OR IGNORE INTO reviews (client_name, country, rating, service, review_text, review_date, is_verified)
                      VALUES (?,?,?,?,?,?,1)''', r)
        count += 1
    conn.commit()
    conn.close()
    print(f"✓ Inserted {count} reviews")

def seed_faqs():
    faqs = [
        ('What is your typical project turnaround time?', 'Most projects take 3-7 business days depending on complexity. A simple social media edit might take 2-3 days, while a full brand video or commercial can take 1-2 weeks. I always provide a clear timeline before starting any project.', 'Timeline', 1),
        ('How much do your services cost?', 'My pricing varies based on project scope, complexity, and timeline. Basic edits start from $200, while premium projects with full creative direction range from $500-$1200+. I offer custom quotes for larger projects.', 'Pricing', 2),
        ('Do you offer revisions?', 'Yes! Every package includes revisions. The Starter package includes 2 rounds, Professional includes 5 rounds, and Premium includes unlimited revisions until you are completely satisfied.', 'Revisions', 3),
        ('What file formats do you deliver?', 'I deliver in multiple formats including MP4, MOV, and GIF. For social media, I optimize for each platform. I also provide source files (After Effects, Premiere) upon request for Premium clients.', 'Delivery', 4),
        ('How do you handle communication?', 'I maintain clear communication throughout the project. You will receive regular updates, progress previews, and I am available via email, WhatsApp, or video calls to discuss any questions.', 'Communication', 5),
        ('Do you require a deposit?', 'Yes, I require a 50% deposit to begin work, with the remaining 50% due upon final delivery. Payment is processed securely through our booking system.', 'Payment', 6),
        ('What if I need urgent delivery?', 'I offer rush delivery options for an additional fee. Express 24-hour delivery is available for select projects at 1.5x the standard rate. Contact me to discuss your timeline.', 'Timeline', 7),
        ('Who owns the rights to my content?', 'You retain full commercial rights to all delivered content. I do not claim ownership of your final videos. I may request permission to feature completed work in my portfolio.', 'Rights', 8),
        ('What software do you primarily use?', 'My primary tools are After Effects for motion graphics, Premiere Pro for video editing, and DaVinci Resolve for color grading. I also use Cinema 4D and Blender for 3D work when needed.', 'General', 9),
        ('Can you work with existing brand guidelines?', 'Absolutely! I follow your brand guidelines meticulously including colors, fonts, logos, and style preferences. This ensures all content aligns perfectly with your brand identity.', 'Workflow', 10),
        ('What industries do you specialize in?', 'I work across diverse industries including tech, e-commerce, education, entertainment, healthcare, real estate, and more. Each industry gets a tailored approach to visual storytelling.', 'General', 11),
        ('How do you handle feedback and changes?', 'I use a structured feedback system where you can provide comments on specific timestamps. Changes are tracked and implemented systematically to ensure nothing is missed.', 'Revisions', 12),
        ('Do you offer subscription packages?', 'Yes! I offer monthly retainer packages for businesses needing consistent content. This includes a set number of videos per month at a discounted rate. Contact me for custom pricing.', 'Pricing', 13),
        ('What information do you need to start?', 'I need your project brief, brand assets (logo, colors, fonts), any reference materials or examples, your target audience info, and the key message you want to convey.', 'Workflow', 14),
        ('Is there a satisfaction guarantee?', 'Absolutely. Your satisfaction is my top priority. I work with you until the results meet your expectations. If you are not happy, I will make it right.', 'Support', 15),
        ('How do you ensure confidentiality?', 'All client information and project details are kept strictly confidential. I offer NDA agreements for sensitive projects and store all files on encrypted servers.', 'Support', 16),
        ('Can you handle multiple projects at once?', 'Yes, I manage multiple projects with dedicated timelines for each. My workflow is designed to handle concurrent projects without compromising quality.', 'Workflow', 17),
        ('What payment methods do you accept?', 'I accept bank transfers, PayPal, and major credit cards. Payment terms are clearly outlined in the project agreement before work begins.', 'Payment', 18),
        ('Do you provide captions/subtitles?', 'Yes, I can include professional captions and subtitles in multiple languages. This is included in the Premium package and available as an add-on for other packages.', 'Delivery', 19),
        ('What happens after project completion?', 'After delivery, I provide 30 days of support for any adjustments or technical issues. I also offer ongoing maintenance packages to keep your content fresh and updated.', 'Support', 20),
    ]

    conn = get_db()
    count = 0
    for f in faqs:
        conn.execute('''INSERT OR IGNORE INTO faqs (question, answer, category, sort_order, is_published)
                      VALUES (?,?,?,?,1)''', f)
        count += 1
    conn.commit()
    conn.close()
    print(f"✓ Inserted {count} FAQs")

def seed_skills():
    skills = [
        ('After Effects', 95, 'Tools', 'fab fa-adobe', 1),
        ('Premiere Pro', 92, 'Tools', 'fab fa-adobe', 2),
        ('Photoshop', 88, 'Tools', 'fab fa-adobe', 3),
        ('Illustrator', 85, 'Tools', 'fab fa-adobe', 4),
        ('Figma', 90, 'Design', 'fab fa-figma', 5),
        ('DaVinci Resolve', 80, 'Tools', 'fas fa-video', 6),
        ('Blender', 75, '3D & Animation', 'fas fa-cube', 7),
        ('Cinema 4D', 78, '3D & Animation', 'fas fa-cube', 8),
        ('CapCut', 95, 'Tools', 'fas fa-cut', 9),
        ('Canva', 90, 'Design', 'fas fa-paint-brush', 10),
        ('Motion Design', 95, 'Creative', 'fas fa-film', 11),
        ('Color Grading', 85, 'Creative', 'fas fa-palette', 12),
        ('Sound Design', 80, 'Creative', 'fas fa-music', 13),
        ('Video Production', 90, 'Creative', 'fas fa-camera', 14),
        ('Visual Effects', 85, 'Creative', 'fas fa-magic', 15),
        ('Storyboarding', 82, 'Creative', 'fas fa-pencil-alt', 16),
        ('Creative Strategy', 88, 'Creative', 'fas fa-lightbulb', 17),
    ]

    conn = get_db()
    count = 0
    for s in skills:
        conn.execute('''INSERT OR IGNORE INTO skills (name, percentage, category, icon, sort_order)
                      VALUES (?,?,?,?,?)''', s)
        count += 1
    conn.commit()
    conn.close()
    print(f"✓ Inserted {count} skills")

def main():
    print("🌱 Seeding Siam Munkasir Portfolio Database...")
    print(f"Database: {DB_PATH}")
    seed_testimonials()
    seed_reviews()
    seed_faqs()
    seed_skills()
    print("\n✨ Database seeding complete!")

if __name__ == '__main__':
    main()
