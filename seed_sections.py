"""Seed homepage_sections table with default content matching the frontend."""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')

SECTIONS = {
    'hero': {
        'badge_text': 'Available for Projects',
        'title': 'AI-Powered Content That Captivates & Converts',
        'roles': ['AI Content Strategist', 'UGC Specialist', 'Creative Director', 'Motion Designer', 'Brand Storyteller'],
        'subtitle': "Crafting high-impact digital content and AI-powered solutions that drive real business results for brands worldwide — from UGC strategy to full AI automation systems.",
        'cta_primary': {'text': 'View Portfolio', 'href': '#portfolio'},
        'cta_secondary': {'text': 'Hire Me', 'href': '#contact'},
        'cta_tertiary': {'text': 'Book a Call', 'href': 'https://wa.me/8801989430474', 'icon': 'fab fa-whatsapp'},
        'stats': [
            {'label': 'Projects Completed', 'value': 200, 'suffix': '+'},
            {'label': 'Clients Served', 'value': 50, 'suffix': '+'},
            {'label': 'Years Experience', 'value': 3, 'suffix': '+'},
            {'label': 'Client Satisfaction', 'value': 98, 'suffix': '%'},
        ]
    },
    'about': {
        'tag': 'About Me',
        'title': 'Creative Content Strategist & AI UGC Specialist',
        'subtitle': 'Bridging creative storytelling with cutting-edge AI technology to deliver content that drives real business results.',
        'name': 'BrandFit Media',
        'initials': 'SM',
        'bio_1': "I'm a Creative Content Strategist and AI UGC Specialist based in Dhaka, Bangladesh. With 3+ years of experience, I help brands craft high-impact digital content and AI-powered solutions — from UGC strategy for e-commerce brands to short-form video production and full AI automation systems.",
        'bio_2': 'My expertise spans User Generated Content (UGC) strategy for beauty and lifestyle brands, short-form video production across TikTok, Instagram, and YouTube, and AI-driven marketing automation. I combine creative storytelling with cutting-edge AI tools to deliver content that drives real business results.',
        'mission': 'My mission is to bridge creative storytelling with cutting-edge AI technology — delivering content that not only looks authentic but also converts viewers into loyal customers.',
        'process_steps': [
            {'icon': 'fas fa-lightbulb', 'title': 'Discovery & Strategy', 'desc': 'We start by understanding your brand, goals, and target audience to craft a data-driven content strategy.'},
            {'icon': 'fas fa-pen-fancy', 'title': 'Creative Production', 'desc': 'From scripting to storyboarding, we create compelling content tailored to each platform and audience segment.'},
            {'icon': 'fas fa-robot', 'title': 'AI Optimization', 'desc': 'Leveraging AI tools for content optimization, A/B testing, and performance prediction to maximize ROI.'},
            {'icon': 'fas fa-chart-line', 'title': 'Delivery & Analytics', 'desc': 'Final delivery with performance tracking and analytics to measure real business impact.'},
        ]
    },
    'marquee': {
        'items_top': ['AI Content Strategy', 'UGC Production', 'Motion Design', 'Brand Storytelling', 'AI Automation'],
        'items_bottom': ['ChatGPT & Gemini Expert', 'Short-Form Video Editor', 'Content Strategist', 'SaaS Builder', 'Creative Director'],
        'separator_top': '✦',
        'separator_bottom': '◆',
    },
}

def seed():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    for key, data in SECTIONS.items():
        existing = db.execute("SELECT id FROM homepage_sections WHERE section_key=?", (key,)).fetchone()
        content_json = json.dumps(data)
        if existing:
            db.execute("UPDATE homepage_sections SET content=?, is_active=1, updated_at=CURRENT_TIMESTAMP WHERE section_key=?", (content_json, key))
            print(f'Updated section: {key}')
        else:
            db.execute("INSERT INTO homepage_sections (section_key, content, is_active) VALUES (?, ?, 1)", (key, content_json))
            print(f'Created section: {key}')
    db.commit()
    # Verify
    rows = db.execute("SELECT section_key, is_active, length(content) as clen FROM homepage_sections").fetchall()
    for r in rows:
        print(f'  ✅ {r["section_key"]} (active: {r["is_active"]}, {r["clen"]} chars)')
    db.close()
    print(f'\nSeeded {len(SECTIONS)} homepage sections')

if __name__ == '__main__':
    seed()
