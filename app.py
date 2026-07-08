import os, json, uuid, re, hashlib, smtplib, csv, io, time, threading, math, random
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory, abort, flash, Response
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'portfolio.db')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'mp4', 'mov', 'avi', 'zip', 'rar'}

# ─── SMTP Config (customize these) ───
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = ''  # set via admin or env
SMTP_PASS = ''
ADMIN_EMAIL = ''

# ─── Rate limiting ───
_rate_limit_store = {}
def rate_limit(max_per_minute=5):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr or 'unknown'
            now = time.time()
            if ip not in _rate_limit_store:
                _rate_limit_store[ip] = []
            _rate_limit_store[ip] = [t for t in _rate_limit_store[ip] if now - t < 60]
            if len(_rate_limit_store[ip]) >= max_per_minute:
                return jsonify({'error': 'Too many requests. Please wait.'}), 429
            _rate_limit_store[ip].append(now)
            return f(*args, **kwargs)
        return wrapper
    return decorator

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            company_name TEXT,
            email TEXT NOT NULL,
            phone TEXT,
            country TEXT,
            website TEXT,
            instagram TEXT,
            linkedin TEXT,
            facebook TEXT,
            youtube TEXT,
            project_type TEXT,
            business_name TEXT,
            industry TEXT,
            budget TEXT,
            timeline TEXT,
            project_description TEXT,
            main_problem TEXT,
            goals TEXT,
            additional_notes TEXT,
            uploaded_files TEXT,
            ip_address TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            description TEXT,
            client TEXT,
            date TEXT,
            image_url TEXT,
            video_url TEXT,
            tags TEXT,
            live_url TEXT,
            featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            company TEXT,
            role TEXT,
            content TEXT NOT NULL,
            rating INTEGER DEFAULT 5,
            avatar_url TEXT,
            featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            price TEXT,
            features TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS site_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS email_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inquiry_id INTEGER,
            recipient TEXT,
            subject TEXT,
            body TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            country TEXT DEFAULT '',
            rating INTEGER DEFAULT 5,
            service TEXT DEFAULT '',
            review_text TEXT NOT NULL,
            review_date TEXT DEFAULT '',
            is_verified INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(client_name, review_text)
        );
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL UNIQUE,
            answer TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            sort_order INTEGER DEFAULT 0,
            is_published INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            percentage INTEGER DEFAULT 50,
            category TEXT DEFAULT 'Design',
            icon TEXT DEFAULT 'fas fa-star',
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            visit_count INTEGER DEFAULT 1,
            country TEXT DEFAULT '',
            city TEXT DEFAULT '',
            region TEXT DEFAULT '',
            timezone TEXT DEFAULT '',
            language TEXT DEFAULT '',
            device_type TEXT DEFAULT '',
            os TEXT DEFAULT '',
            browser TEXT DEFAULT '',
            browser_version TEXT DEFAULT '',
            screen_resolution TEXT DEFAULT '',
            total_page_views INTEGER DEFAULT 0,
            total_clicks INTEGER DEFAULT 0,
            total_session_duration INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id INTEGER NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            referrer TEXT DEFAULT '',
            landing_page TEXT DEFAULT '',
            exit_page TEXT DEFAULT '',
            traffic_source TEXT DEFAULT 'Direct',
            utm_source TEXT DEFAULT '',
            utm_medium TEXT DEFAULT '',
            utm_campaign TEXT DEFAULT '',
            utm_term TEXT DEFAULT '',
            utm_content TEXT DEFAULT '',
            device_type TEXT DEFAULT '',
            os TEXT DEFAULT '',
            browser TEXT DEFAULT '',
            browser_version TEXT DEFAULT '',
            screen_resolution TEXT DEFAULT '',
            country TEXT DEFAULT '',
            city TEXT DEFAULT '',
            region TEXT DEFAULT '',
            timezone TEXT DEFAULT '',
            language TEXT DEFAULT '',
            page_views INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            scroll_depth INTEGER DEFAULT 0,
            session_duration INTEGER DEFAULT 0,
            is_bounce INTEGER DEFAULT 1,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            FOREIGN KEY (visitor_id) REFERENCES visitors(id)
        );
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_id INTEGER NOT NULL,
            visitor_id INTEGER NOT NULL,
            page_url TEXT NOT NULL,
            page_title TEXT DEFAULT '',
            time_spent INTEGER DEFAULT 0,
            scroll_depth INTEGER DEFAULT 0,
            referrer TEXT DEFAULT '',
            view_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (visit_id) REFERENCES visits(id),
            FOREIGN KEY (visitor_id) REFERENCES visitors(id)
        );
        CREATE TABLE IF NOT EXISTS live_visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            current_page TEXT DEFAULT '',
            page_title TEXT DEFAULT '',
            country TEXT DEFAULT '',
            device_type TEXT DEFAULT '',
            browser TEXT DEFAULT '',
            ip_address TEXT DEFAULT '',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (visitor_id) REFERENCES visitors(id)
        );
        CREATE INDEX IF NOT EXISTS idx_visits_visitor ON visits(visitor_id);
        CREATE INDEX IF NOT EXISTS idx_visits_started ON visits(started_at);
        CREATE INDEX IF NOT EXISTS idx_page_views_visit ON page_views(visit_id);
        CREATE INDEX IF NOT EXISTS idx_page_views_time ON page_views(view_time);
        CREATE INDEX IF NOT EXISTS idx_live_heartbeat ON live_visitors(last_heartbeat);

        -- CMS tables
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT DEFAULT '',
            excerpt TEXT DEFAULT '',
            category TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            featured_image TEXT DEFAULT '',
            author TEXT DEFAULT 'Siam Munkasir',
            status TEXT DEFAULT 'draft',
            seo_title TEXT DEFAULT '',
            seo_description TEXT DEFAULT '',
            seo_keywords TEXT DEFAULT '',
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS pricing_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL DEFAULT '0',
            currency TEXT DEFAULT '$',
            period TEXT DEFAULT '/mo',
            description TEXT DEFAULT '',
            features TEXT DEFAULT '', -- JSON array
            icon TEXT DEFAULT 'fas fa-star',
            button_text TEXT DEFAULT 'Get Started',
            button_link TEXT DEFAULT '#contact',
            highlighted INTEGER DEFAULT 0,
            popular_badge TEXT DEFAULT '',
            tier TEXT DEFAULT 'bundle',
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS navigation_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            link TEXT NOT NULL DEFAULT '#',
            parent_id INTEGER DEFAULT 0,
            icon TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            is_visible INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            filepath TEXT NOT NULL,
            filetype TEXT DEFAULT '',
            filesize INTEGER DEFAULT 0,
            alt_text TEXT DEFAULT '',
            folder TEXT DEFAULT '/',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS homepage_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_key TEXT UNIQUE NOT NULL,
            content TEXT DEFAULT '{}',
            is_active INTEGER DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT DEFAULT '',
            action TEXT NOT NULL,
            details TEXT DEFAULT '',
            ip_address TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        # Create default admin if not exists
        existing = db.execute("SELECT id FROM admin WHERE username='admin'").fetchone()
        if not existing:
            pw = hashlib.sha256('admin123'.encode()).hexdigest()
            db.execute("INSERT INTO admin (username, password_hash) VALUES (?, ?)", ('admin', pw))
        # Default settings
        defaults = {'site_name': 'Siam Munkasir', 'site_tagline': 'AI Content Strategist & UGC Specialist — crafting high-impact digital content that drives real business results.', 'admin_email': ''}
        for k, v in defaults.items():
            db.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES (?, ?)", (k, v))

        # ─── SEED DATA (only if tables are empty) ───
        empty = db.execute("SELECT COUNT(*) FROM portfolio").fetchone()[0] == 0
        if not empty:
            return

        # Portfolio
        portfolio_items = [
            ('Luxury Brand Reel', 'Motion Graphics', 'Cinematic brand film for a luxury fashion label — smooth transitions, dynamic typography, and a premium color palette that elevated brand perception.', 'Chanel Style Co.', '2026-06', 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=600&h=375&fit=crop', '', 'cinematic,brand,luxury', '', 1),
            ('AI UGC Campaign', 'UGC Strategy', 'AI-powered UGC campaign combining authentic user content with intelligent strategy — driving 3x engagement across social platforms.', 'TechBrand Inc.', '2026-05', 'https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=600&h=375&fit=crop', '', 'ugc,ai,campaign', '', 1),
            ('Product Launch Teaser', 'Video Production', 'High-energy product launch teaser with cinematic editing, motion graphics overlays, and a pulse-pounding sound design.', 'StartupX', '2026-04', 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=600&h=375&fit=crop', '', 'product,launch,editing', '', 1),
            ('YouTube Rebrand Package', 'Brand Identity', 'Complete channel identity with intro/outro animations, lower thirds, transition pack, and custom thumbnail templates.', 'Creator Hub', '2026-03', 'https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?w=600&h=375&fit=crop', '', 'youtube,rebrand,motion', '', 1),
            ('SaaS Explainer Video', 'AI/Automation', 'Animated explainer for an AI SaaS product — simplifying complex features into an engaging 90-second story.', 'CloudSoft', '2026-02', 'https://images.unsplash.com/photo-1559028012-481c04fa702d?w=600&h=375&fit=crop', '', 'explainer,2d,saas', '', 1),
            ('Viral Reel Series', 'Social Media Ads', '30-day viral short-form content package optimized for TikTok, Reels, and Shorts — trend-jacking with data-driven hooks.', 'Influence Pro', '2026-01', 'https://images.unsplash.com/photo-1611605698335-8b1569810432?w=600&h=375&fit=crop', '', 'social,shortform,package', '', 1),
        ]
        for p in portfolio_items:
            db.execute('''INSERT OR IGNORE INTO portfolio (title, category, description, client, date, image_url, video_url, tags, live_url, featured) VALUES (?,?,?,?,?,?,?,?,?,?)''', p)

        # Services
        services = [
            ('AI Content Strategy', 'Data-driven content strategy powered by AI analytics and market research. I help brands identify high-impact content opportunities and create roadmaps that drive measurable results.', 'fa-robot', '$500+', '["Audit","Strategy","Calendar","AI Tools"]'),
            ('UGC Production', 'Authentic user-generated content that builds trust and drives conversions. From concept to final edit, I produce scroll-stopping UGC that feels real and performs.', 'fa-users', '$300+', '["Scripting","Filming","Editing","Optimization"]'),
            ('Motion Design', 'Professional motion graphics and animation for brands that want to stand out. Smooth transitions, cinematic effects, and pixel-perfect execution.', 'fa-film', '$800+', '["Storyboard","Animation","VFX","Sound Design"]'),
            ('Short-Form Video', 'High-retention short-form content optimized for TikTok, Reels, and YouTube Shorts. Hook-driven editing that keeps viewers watching.', 'fa-bolt', '$200+', '["Trend Research","Editing","Captions","Thumbnails"]'),
        ]
        for s in services:
            db.execute('''INSERT OR IGNORE INTO services (title, description, icon, price, features) VALUES (?,?,?,?,?)''', s)

        # Testimonials (sample)
        testimonials = [
            ('Yuki Tanaka', 'Tokyo Studio One', 'Creative Lead', 'The attention to detail in every frame is remarkable. Truly world-class motion graphics.', 5, 'Japan', '2026-04-05'),
            ('Hannah Bauer', 'Alpine Media', 'Marketing Lead', 'Our YouTube channel has never looked better. Video editing and motion graphics improved viewer retention significantly.', 5, 'Switzerland', '2026-03-28'),
            ('Ahmed Hassan', 'Desert Rose Media', 'CEO', 'Professional, creative, and reliable. Outstanding content that resonated perfectly with our audience.', 5, 'UAE', '2026-03-20'),
            ('Emma Wilson', 'Pacific Creative', 'Brand Director', 'The best decision we made this year. Our brand videos now look world-class.', 5, 'Australia', '2026-03-15'),
            ('Lucas Andersen', 'Nordic Media House', 'Creative Director', 'Incredible talent and exceptional service. They go above and beyond every time.', 5, 'Denmark', '2026-03-10'),
            ('Maria Santos', 'Brazil Media Group', 'Content Director', 'The social media content strategy was genius. Every video performs exceptionally well.', 5, 'Brazil', '2026-03-05'),
        ]
        for t in testimonials:
            db.execute('''INSERT OR IGNORE INTO testimonials (client_name, company, role, content, rating, avatar_url, featured, created_at) VALUES (?,?,?,?,?,'',1,?)''', (t[0], t[1], t[2], t[3], t[4], t[6]))

        # Reviews
        reviews_data = [
            ('Alex Johnson', 'United States', 5, 'Motion Graphics', 'The motion graphics work was absolutely phenomenal. They took our rough concept and turned it into a visually stunning animation.', '2026-06-01'),
            ('Maria Garcia', 'Spain', 5, 'Video Editing', 'Incredible video editing skills. They transformed raw footage into a polished, professional video.', '2026-05-28'),
            ('David Brown', 'United Kingdom', 5, 'Explainer Video', 'Our explainer video came out better than we imagined. Clear, engaging, and visually appealing.', '2026-05-25'),
            ('Lisa Wang', 'Singapore', 5, 'Instagram Reels', 'The Instagram Reels content has been a game-changer. Engagement rates have tripled.', '2026-05-22'),
            ('Mohammed Ali', 'UAE', 5, 'Brand Video', 'The brand video captured our essence perfectly. Cinematic, emotional, and professionally executed.', '2026-05-20'),
            ('Sarah Johnson', 'Canada', 4, 'YouTube Editing', 'Great YouTube editing services. Well-paced, engaging, and excellent thumbnail designs.', '2026-05-18'),
        ]
        for r in reviews_data:
            db.execute('''INSERT OR IGNORE INTO reviews (client_name, country, rating, service, review_text, review_date, is_verified) VALUES (?,?,?,?,?,?,1)''', r)

        # FAQs
        faqs = [
            ('How long does a typical project take?', 'Timeline depends on scope. Short-form edits typically take 1-3 days, motion graphics projects 5-10 days, and full brand videos 2-4 weeks. I will provide a detailed timeline during our consultation.', 'General', 1),
            ('What is your pricing structure?', 'Pricing varies based on project complexity, length, and usage rights. I offer both per-project and retainer packages. Contact me with your requirements for a customized quote.', 'Pricing', 2),
            ('Do you offer revisions?', 'Yes! Each project includes up to 2 rounds of revisions to ensure the final product meets your expectations. Additional revisions can be arranged at a nominal fee.', 'General', 3),
            ('What information do you need to get started?', 'Share your brand guidelines, reference materials, script/voiceover if available, and any specific requirements. The more context, the better I can tailor the output to your needs.', 'Process', 4),
            ('Can you work with my existing team?', 'Absolutely. I collaborate seamlessly with marketing teams, agencies, and production houses. I can work within your existing workflow and brand guidelines.', 'Collaboration', 5),
            ('What formats do you deliver in?', 'I deliver in all standard formats (MP4, MOV, GIF) optimized for your target platform. I also provide source files upon request for an additional fee.', 'Technical', 6),
        ]
        for f in faqs:
            db.execute('''INSERT OR IGNORE INTO faqs (question, answer, category, sort_order, is_published) VALUES (?,?,?,?,1)''', f)

        # Skills
        skills = [
            ('AI Content Strategy', 95, 'Strategy', 'fa-brain', 1),
            ('UGC Production', 92, 'Content', 'fa-camera', 2),
            ('Motion Design', 90, 'Design', 'fa-film', 3),
            ('Video Editing', 95, 'Production', 'fa-cut', 4),
            ('ChatGPT & Gemini', 90, 'AI', 'fa-comment', 5),
            ('Scriptwriting', 88, 'Strategy', 'fa-pen', 6),
            ('Brand Strategy', 85, 'Strategy', 'fa-bullseye', 7),
            ('Social Media', 90, 'Marketing', 'fa-share-alt', 8),
        ]
        for sk in skills:
            db.execute('''INSERT OR IGNORE INTO skills (name, percentage, category, icon, sort_order) VALUES (?,?,?,?,?)''', sk)

        # ─── CMS DEFAULTS ───
        # Navigation
        nav_items = [
            ('Home', '/', 0, '', 1, 1),
            ('Services', '/#services', 0, '', 2, 1),
            ('Portfolio', '/#portfolio', 0, '', 3, 1),
            ('Testimonials', '/#testimonials', 0, '', 4, 1),
            ('Reviews', '/#reviews', 0, '', 5, 1),
            ('Pricing', '/#pricing', 0, '', 6, 1),
            ('Contact', '/#contact', 0, '', 7, 1),
        ]
        for n in nav_items:
            db.execute('''INSERT OR IGNORE INTO navigation_items (label, link, parent_id, icon, sort_order, is_visible) VALUES (?,?,?,?,?,?)''', n)

        # Pricing plans (bundle packages)
        bundles = [
            ('Launch', '$799', '$', '/mo', 'Perfect for startups testing the waters', '["1x Short-Form Edit","2x Revisions","3-Day Delivery","Basic Captions","Social Media Export"]', 'fa-rocket', 'Get Started', '#contact', 0, 'Most Popular', 'bundle', 1),
            ('Growth', '$1,299', '$', '/mo', 'For growing brands ready to scale', '["2x Short-Form Edits","3x Revisions","2-Day Delivery","Advanced Captions","Social Media Export","1x Motion Graphics Clip","Source Files"]', 'fa-chart-line', 'Get Started', '#contact', 1, 'Best Value', 'bundle', 2),
            ('Empire', '$1,999', '$', '/mo', 'Full-service content domination', '["4x Short-Form Edits","Unlimited Revisions","1-Day Delivery","Premium Captions","Social Media Export","3x Motion Graphics Clips","Source Files","Strategy Call","Priority Support"]', 'fa-crown', 'Get Started', '#contact', 0, '', 'bundle', 3),
        ]
        for b in bundles:
            db.execute('''INSERT OR IGNORE INTO pricing_plans (name, price, currency, period, description, features, icon, button_text, button_link, highlighted, popular_badge, tier, sort_order) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', b)

        # Homepage sections (defaults)
        default_sections = {
            'hero': json.dumps({
                'badge_text': 'Available for Projects',
                'title': 'AI-Powered Content That Captivates & Converts',
                'roles': ['AI Content Strategist','UGC Specialist','Creative Director','Motion Designer','Brand Storyteller'],
                'subtitle': "Crafting high-impact digital content and AI-powered solutions that drive real business results for brands worldwide.",
                'cta_primary': {'text': 'View Portfolio', 'href': '#portfolio'},
                'cta_secondary': {'text': 'Hire Me', 'href': '#contact'},
                'cta_tertiary': {'text': 'Book a Call', 'href': 'https://wa.me/8801989430474'},
                'stats': [{'label':'Projects Completed','value':200,'suffix':'+'},{'label':'Clients Served','value':50,'suffix':'+'},{'label':'Years Experience','value':3,'suffix':'+'},{'label':'Client Satisfaction','value':98,'suffix':'%'}]
            }),
            'about': json.dumps({
                'tag': 'About Me',
                'title': 'Creative Content Strategist & AI UGC Specialist',
                'subtitle': 'Bridging creative storytelling with cutting-edge AI technology to deliver content that drives real business results.',
                'name': 'Siam Munkasir',
                'initials': 'SM',
                'bio_1': "I'm a Creative Content Strategist and AI UGC Specialist based in Dhaka, Bangladesh.",
                'bio_2': 'My expertise spans UGC strategy, short-form video production, and AI-driven marketing automation.',
                'mission': 'Bridging creative storytelling with cutting-edge AI technology.',
                'process_steps': [
                    {'title':'Discovery & Strategy','desc':'Understanding your brand, goals, and audience.'},
                    {'title':'AI-Powered Research','desc':'Researching trends and generating data-backed concepts.'},
                    {'title':'Script & Storyboard','desc':'Crafting viral hooks for each platform.'},
                    {'title':'Production & Filming','desc':'Creating authentic UGC content.'},
                    {'title':'AI-Enhanced Editing','desc':'Editing with AI tools for algorithm optimization.'},
                    {'title':'Review & Optimization','desc':'Data-driven refinements for maximum performance.'},
                    {'title':'Delivery & Analytics','desc':'Performance tracking to measure real business impact.'}
                ]
            }),
            'marquee': json.dumps({
                'items_top': ['AI Content Strategy','UGC Production','Motion Design','Brand Storytelling','AI Automation'],
                'items_bottom': ['ChatGPT & Gemini Expert','Short-Form Video Editor','Content Strategist','SaaS Builder','Creative Director'],
                'separator_top': '✦',
                'separator_bottom': '◆'
            }),
            'stats': json.dumps([
                {'label': 'Projects Completed', 'value': '200+', 'icon': 'fa-check-circle'},
                {'label': 'Happy Clients', 'value': '50+', 'icon': 'fa-smile'},
                {'label': 'Years Experience', 'value': '3+', 'icon': 'fa-clock'},
                {'label': 'Content Pieces', 'value': '500+', 'icon': 'fa-file-alt'}
            ]),
            'services_heading': json.dumps({
                'title': 'Services',
                'subtitle': 'What I Can Do For You',
                'description': 'From AI-powered content strategy to cinematic motion design — I offer end-to-end content solutions.'
            })
        }
        for key in ['hero', 'about', 'marquee', 'stats', 'services_heading']:
            if key in default_sections:
                db.execute("INSERT OR IGNORE INTO homepage_sections (section_key, content) VALUES (?,?)", (key, default_sections[key]))

        # Additional settings defaults
        extra_settings = {
            'site_logo': '',
            'site_favicon': '',
            'footer_logo': '',
            'footer_copyright': '© 2026 Siam Munkasir. All rights reserved.',
            'footer_address': '',
            'footer_email': 'hello@siammunkasir.com',
            'footer_phone': '',
            'social_instagram': '#',
            'social_linkedin': '#',
            'social_youtube': '#',
            'social_twitter': '#',
            'social_github': '#',
            'seo_home_title': 'Siam Munkasir — AI Content Strategist & UGC Specialist',
            'seo_home_description': 'AI Content Strategist & UGC Specialist crafting high-impact digital content that drives real business results.',
            'seo_home_keywords': 'content strategy, UGC, motion graphics, video editing, AI content',
            'og_image': '',
            'primary_color': '#ff6b6b',
            'secondary_color': '#ffd93d',
            'accent_color': '#6c5ce7',
            'font_heading': 'Inter',
            'font_body': 'Inter',
            'border_radius': '12px',
            'shadow_intensity': '20',
            'button_style': 'gradient',
            'theme_mode': 'dark',
            'smtp_user': '',
            'smtp_pass': '',
            'admin_email': '',
            'blog_enabled': '1',
            'contact_email_to': '',
            'form_captcha_enabled': '1',
            'ga_tracking_id': '',
        }
        for k, v in extra_settings.items():
            db.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES (?,?)", (k, v))

@app.context_processor
def inject_admin_globals():
    """Inject new_inquiries count into all admin templates."""
    if session.get('admin_logged_in'):
        try:
            with get_db() as db:
                count = db.execute("SELECT COUNT(*) as c FROM inquiries WHERE status='new'").fetchone()['c']
            return {'new_inquiries': count}
        except:
            pass
    return {'new_inquiries': 0}

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            if request.is_json:
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email_async(to, subject, html_body):
    """Send email in a background thread so the request isn't blocked."""
    th = threading.Thread(target=send_email, args=(to, subject, html_body), daemon=True)
    th.start()

def send_email(to, subject, html_body):
    smtp_user = ''
    smtp_pass = ''
    admin_email = ''
    try:
        with get_db() as db:
            row = db.execute("SELECT value FROM site_settings WHERE key='smtp_user'").fetchone()
            if row: smtp_user = row['value']
            row = db.execute("SELECT value FROM site_settings WHERE key='smtp_pass'").fetchone()
            if row: smtp_pass = row['value']
            row = db.execute("SELECT value FROM site_settings WHERE key='admin_email'").fetchone()
            if row: admin_email = row['value']
    except:
        smtp_user = ''
        smtp_pass = ''
        admin_email = ''
    
    if not smtp_user or not smtp_pass:
        print(f"[EMAIL SKIPPED] No SMTP config. Would send to {to}: {subject}")
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as srv:
            srv.starttls()
            srv.login(smtp_user, smtp_pass)
            srv.send_message(msg)
        # Log
        with get_db() as db:
            db.execute("INSERT INTO email_log (recipient, subject, body) VALUES (?, ?, ?)",
                      (to, subject, html_body[:500]))
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False

# ─── PUBLIC ROUTES ───

@app.route('/')
def index():
    with get_db() as db:
        portfolio_items = db.execute("SELECT * FROM portfolio ORDER BY featured DESC, created_at DESC LIMIT 12").fetchall()
        testimonials = db.execute("SELECT * FROM testimonials WHERE featured=1 ORDER BY created_at DESC LIMIT 6").fetchall()
        services = db.execute("SELECT * FROM services ORDER BY id ASC").fetchall()
        settings = {row['key']: row['value'] for row in db.execute("SELECT * FROM site_settings").fetchall()}
        sections_raw = db.execute("SELECT section_key, content FROM homepage_sections WHERE is_active=1").fetchall()
    sections = {row['section_key']: json.loads(row['content']) for row in sections_raw}
    return render_template('index.html',
                         portfolio=portfolio_items,
                         testimonials=testimonials,
                         services=services,
                         settings=settings,
                         sections=sections)

@app.route('/api/submit-inquiry', methods=['POST'])
@rate_limit(max_per_minute=3)
def submit_inquiry():
    try:
        data = request.form.to_dict()
        files = request.files.getlist('uploaded_files[]')
        
        # CAPTCHA check (simple math)
        captcha_answer = data.get('captcha_answer', '')
        captcha_expected = data.get('captcha_expected', '')
        if captcha_answer != captcha_expected:
            return jsonify({'error': 'Invalid CAPTCHA answer.'}), 400
        
        # Validate required
        required = ['full_name', 'email']
        for field in required:
            if not data.get(field, '').strip():
                return jsonify({'error': f'{field.replace("_", " ").title()} is required.'}), 400
        
        # Sanitize
        def sanitize(val):
            if not val: return ''
            return re.sub(r'<[^>]*>', '', str(val).strip())
        
        # Save uploaded files
        saved_files = []
        if files:
            for f in files:
                if f and f.filename and allowed_file(f.filename):
                    safe = secure_filename(f.filename)
                    unique = f"{uuid.uuid4().hex[:8]}_{safe}"
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], unique))
                    saved_files.append(unique)
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
        
        with get_db() as db:
            cursor = db.execute('''INSERT INTO inquiries (
                full_name, company_name, email, phone, country, website,
                instagram, linkedin, facebook, youtube, project_type,
                business_name, industry, budget, timeline, project_description,
                main_problem, goals, additional_notes, uploaded_files, ip_address
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                sanitize(data.get('full_name','')),
                sanitize(data.get('company_name','')),
                sanitize(data.get('email','')),
                sanitize(data.get('phone','')),
                sanitize(data.get('country','')),
                sanitize(data.get('website','')),
                sanitize(data.get('instagram','')),
                sanitize(data.get('linkedin','')),
                sanitize(data.get('facebook','')),
                sanitize(data.get('youtube','')),
                sanitize(data.get('project_type','')),
                sanitize(data.get('business_name','')),
                sanitize(data.get('industry','')),
                sanitize(data.get('budget','')),
                sanitize(data.get('timeline','')),
                sanitize(data.get('project_description','')),
                sanitize(data.get('main_problem','')),
                sanitize(data.get('goals','')),
                sanitize(data.get('additional_notes','')),
                ','.join(saved_files) if saved_files else '',
                ip
            ))
            inquiry_id = cursor.lastrowid
        
        # Send confirmation to visitor
        confirm_html = f"""
        <div style="font-family:'Inter',sans-serif;max-width:600px;margin:0 auto;padding:40px;background:linear-gradient(135deg,#0f0f1a,#1a1a2e);border-radius:16px;color:#fff;">
            <h1 style="font-size:28px;margin-bottom:8px;background:linear-gradient(135deg,#ff6b6b,#ffd93d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Thank You, {sanitize(data.get('full_name',''))}!</h1>
            <p style="color:#a0a0b8;font-size:16px;line-height:1.6;">We've received your inquiry and will review it shortly. Our team typically responds within <strong style="color:#ffd93d;">24 hours</strong>.</p>
            <hr style="border-color:#2a2a3e;margin:24px 0;">
            <p style="color:#a0a0b8;font-size:14px;"><strong style="color:#fff;">Project:</strong> {sanitize(data.get('project_type','N/A'))}</p>
            <p style="color:#a0a0b8;font-size:14px;"><strong style="color:#fff;">Reference:</strong> #{inquiry_id}</p>
            <hr style="border-color:#2a2a3e;margin:24px 0;">
            <p style="color:#666688;font-size:12px;">This is an automated confirmation. We'll reach out to you at <strong style="color:#a0a0b8;">{sanitize(data.get('email',''))}</strong>.</p>
        </div>"""
        send_email_async(data.get('email'), f'Thank you for reaching out — Siam Munkasir', confirm_html)

        # Send notification to admin (async)
        notif_admin_email = ''
        try:
            with get_db() as db:
                r = db.execute("SELECT value FROM site_settings WHERE key='admin_email'").fetchone()
                if r: notif_admin_email = r['value']
        except: pass
        
        if notif_admin_email:
            notif_html = f"""
            <div style="font-family:'Inter',sans-serif;max-width:600px;margin:0 auto;padding:40px;background:#fff;border-radius:16px;border:1px solid #e0e0e0;">
                <h2 style="color:#1a1a2e;">🔔 New Inquiry #{inquiry_id}</h2>
                <table style="width:100%;border-collapse:collapse;">
                    <tr><td style="padding:8px 0;color:#666;"><strong>Name:</strong></td><td>{sanitize(data.get('full_name',''))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Email:</strong></td><td>{sanitize(data.get('email',''))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Phone:</strong></td><td>{sanitize(data.get('phone','N/A'))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Company:</strong></td><td>{sanitize(data.get('company_name','N/A'))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Project:</strong></td><td>{sanitize(data.get('project_type','N/A'))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Budget:</strong></td><td>{sanitize(data.get('budget','N/A'))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Timeline:</strong></td><td>{sanitize(data.get('timeline','N/A'))}</td></tr>
                    <tr><td style="padding:8px 0;color:#666;"><strong>Industry:</strong></td><td>{sanitize(data.get('industry','N/A'))}</td></tr>
                    <tr><td colspan="2" style="padding-top:16px;"><strong>Problem:</strong><br>{sanitize(data.get('main_problem','N/A'))}</td></tr>
                    <tr><td colspan="2" style="padding-top:8px;"><strong>Goals:</strong><br>{sanitize(data.get('goals','N/A'))}</td></tr>
                </table>
                <hr style="border-color:#eee;margin:16px 0;">
                <p style="color:#999;font-size:12px;">IP: {ip} | {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
                <a href="{request.host_url}admin/inquiries" style="display:inline-block;padding:12px 24px;background:#ff6b6b;color:#fff;text-decoration:none;border-radius:8px;margin-top:16px;">View in Dashboard</a>
            </div>"""
            send_email_async(notif_admin_email, f'New Inquiry #{inquiry_id} — {sanitize(data.get("full_name",""))}', notif_html)
        
        return jsonify({'success': True, 'message': 'Your inquiry has been submitted successfully! We will get back to you soon.'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ─── ADMIN ROUTES ───

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username', '')
        password = data.get('password', '')
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        with get_db() as db:
            user = db.execute("SELECT * FROM admin WHERE username=? AND password_hash=?", (username, pw_hash)).fetchone()
            if user:
                session['admin_logged_in'] = True
                session['admin_username'] = username
                return jsonify({'success': True})
        return jsonify({'error': 'Invalid credentials'}), 401
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    with get_db() as db:
        new_inquiries = db.execute("SELECT COUNT(*) as c FROM inquiries WHERE status='new'").fetchone()['c']
        total_inquiries = db.execute("SELECT COUNT(*) as c FROM inquiries").fetchone()['c']
        total_portfolio = db.execute("SELECT COUNT(*) as c FROM portfolio").fetchone()['c']
        total_testimonials = db.execute("SELECT COUNT(*) as c FROM testimonials").fetchone()['c']
        total_reviews = db.execute("SELECT COUNT(*) as c FROM reviews").fetchone()['c']
        total_faqs = db.execute("SELECT COUNT(*) as c FROM faqs").fetchone()['c']
        total_skills = db.execute("SELECT COUNT(*) as c FROM skills").fetchone()['c']
        total_services = db.execute("SELECT COUNT(*) as c FROM services").fetchone()['c']
        total_pricing = db.execute("SELECT COUNT(*) as c FROM pricing_plans").fetchone()['c']
        total_blog = db.execute("SELECT COUNT(*) as c FROM blog_posts").fetchone()['c']
        total_nav = db.execute("SELECT COUNT(*) as c FROM navigation_items").fetchone()['c']
        total_media = db.execute("SELECT COUNT(*) as c FROM media_files").fetchone()['c']
        recent = db.execute("SELECT id, full_name, email, project_type, status, created_at FROM inquiries ORDER BY created_at DESC LIMIT 10").fetchall()
    return render_template('admin/dashboard.html', new_inquiries=new_inquiries, total_inquiries=total_inquiries,
                         total_portfolio=total_portfolio, total_testimonials=total_testimonials,
                         total_reviews=total_reviews, total_faqs=total_faqs, total_skills=total_skills,
                         total_services=total_services, total_pricing=total_pricing, total_blog=total_blog,
                         total_nav=total_nav, total_media=total_media, recent=recent)

@app.route('/admin/inquiries')
@admin_required
def admin_inquiries():
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    with get_db() as db:
        query = "SELECT * FROM inquiries"
        count_query = "SELECT COUNT(*) as c FROM inquiries"
        conditions = []
        params = []
        
        if status_filter:
            conditions.append("status=?")
            params.append(status_filter)
        if search:
            conditions.append("(full_name LIKE ? OR email LIKE ? OR company_name LIKE ? OR project_type LIKE ?)")
            params.extend([f'%{search}%']*4)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            count_query += " WHERE " + " AND ".join(conditions)
        
        total = db.execute(count_query, params).fetchone()['c']
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        inquiries = db.execute(query, params).fetchall()
    
    return render_template('admin/inquiries.html', inquiries=inquiries, total=total, page=page, per_page=per_page,
                         status_filter=status_filter, search=search)

@app.route('/admin/inquiry/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_inquiry_detail(id):
    with get_db() as db:
        inquiry = db.execute("SELECT * FROM inquiries WHERE id=?", (id,)).fetchone()
        if not inquiry:
            abort(404)
        if request.method == 'POST':
            data = request.json if request.is_json else request.form
            new_status = data.get('status', inquiry['status'])
            admin_reply = data.get('reply', '')
            db.execute("UPDATE inquiries SET status=? WHERE id=?", (new_status, id))
            if admin_reply:
                # Email reply to visitor
                reply_html = f"""
                <div style="font-family:'Inter',sans-serif;max-width:600px;margin:0 auto;padding:40px;background:linear-gradient(135deg,#0f0f1a,#1a1a2e);border-radius:16px;color:#fff;">
                    <h2 style="font-size:24px;background:linear-gradient(135deg,#ff6b6b,#ffd93d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Response from Siam Munkasir</h2>
                    <p style="color:#a0a0b8;font-size:16px;line-height:1.6;">{admin_reply}</p>
                    <hr style="border-color:#2a2a3e;margin:24px 0;">
                    <p style="color:#666688;font-size:12px;">Regarding inquiry #{inquiry['id']}</p>
                </div>"""
                send_email(inquiry['email'], 'Response from Siam Munkasir', reply_html)
                db.execute("INSERT INTO email_log (inquiry_id, recipient, subject, body) VALUES (?,?,?,?)",
                          (id, inquiry['email'], 'Admin Reply', admin_reply[:500]))
            if request.is_json:
                return jsonify({'success': True})
            flash('Updated successfully')
            return redirect(url_for('admin_inquiry_detail', id=id))
    return render_template('admin/inquiry_detail.html', inquiry=inquiry)

@app.route('/admin/inquiry/<int:id>/delete', methods=['POST'])
@admin_required
def admin_delete_inquiry(id):
    with get_db() as db:
        db.execute("DELETE FROM inquiries WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/inquiries/export')
@admin_required
def admin_export_inquiries():
    status_filter = request.args.get('status', '')
    with get_db() as db:
        query = "SELECT * FROM inquiries"
        params = []
        if status_filter:
            query += " WHERE status=?"
            params.append(status_filter)
        query += " ORDER BY created_at DESC"
        inquiries = db.execute(query, params).fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    headers = ['ID', 'Name', 'Company', 'Email', 'Phone', 'Country', 'Project Type', 'Budget', 'Timeline',
               'Industry', 'Status', 'Created At']
    writer.writerow(headers)
    for i in inquiries:
        writer.writerow([i['id'], i['full_name'], i['company_name'], i['email'], i['phone'],
                        i['country'], i['project_type'], i['budget'], i['timeline'],
                        i['industry'], i['status'], i['created_at']])
    
    response = app.response_class(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=inquiries.csv'
    return response

# ─── ADMIN PORTFOLIO CRUD ───

@app.route('/admin/portfolio')
@admin_required
def admin_portfolio():
    with get_db() as db:
        items = db.execute("SELECT * FROM portfolio ORDER BY created_at DESC").fetchall()
    return render_template('admin/portfolio.html', items=items)

@app.route('/admin/portfolio/add', methods=['POST'])
@admin_required
def admin_portfolio_add():
    data = request.form
    image_file = request.files.get('image')
    image_url = ''
    if image_file and image_file.filename and allowed_file(image_file.filename):
        safe = secure_filename(image_file.filename)
        unique = f"{uuid.uuid4().hex[:8]}_{safe}"
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique))
        image_url = f"/uploads/{unique}"
    
    with get_db() as db:
        db.execute('''INSERT INTO portfolio (title, category, description, client, date, image_url, video_url, tags, live_url, featured)
                    VALUES (?,?,?,?,?,?,?,?,?,?)''', (
            data.get('title',''), data.get('category',''), data.get('description',''),
            data.get('client',''), data.get('date',''), image_url, data.get('video_url',''),
            data.get('tags',''), data.get('live_url',''), 1 if data.get('featured') else 0
        ))
    return redirect(url_for('admin_portfolio'))

@app.route('/admin/portfolio/<int:id>/edit', methods=['POST'])
@admin_required
def admin_portfolio_edit(id):
    data = request.form
    image_file = request.files.get('image')
    with get_db() as db:
        item = db.execute("SELECT * FROM portfolio WHERE id=?", (id,)).fetchone()
        if not item: abort(404)
        image_url = item['image_url']
        if image_file and image_file.filename and allowed_file(image_file.filename):
            safe = secure_filename(image_file.filename)
            unique = f"{uuid.uuid4().hex[:8]}_{safe}"
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique))
            image_url = f"/uploads/{unique}"
        
        db.execute('''UPDATE portfolio SET title=?, category=?, description=?, client=?, date=?,
                    image_url=?, video_url=?, tags=?, live_url=?, featured=? WHERE id=?''', (
            data.get('title',''), data.get('category',''), data.get('description',''),
            data.get('client',''), data.get('date',''), image_url, data.get('video_url',''),
            data.get('tags',''), data.get('live_url',''), 1 if data.get('featured') else 0, id
        ))
    return redirect(url_for('admin_portfolio'))

@app.route('/admin/portfolio/<int:id>/delete', methods=['POST'])
@admin_required
def admin_portfolio_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM portfolio WHERE id=?", (id,))
    return jsonify({'success': True})

# ─── ADMIN TESTIMONIALS CRUD ───

@app.route('/admin/testimonials')
@admin_required
def admin_testimonials():
    with get_db() as db:
        items = db.execute("SELECT * FROM testimonials ORDER BY created_at DESC").fetchall()
    return render_template('admin/testimonials.html', items=items)

@app.route('/admin/testimonials/add', methods=['POST'])
@admin_required
def admin_testimonials_add():
    data = request.form
    with get_db() as db:
        db.execute('''INSERT INTO testimonials (client_name, company, role, content, rating, featured)
                    VALUES (?,?,?,?,?,?)''', (
            data.get('client_name',''), data.get('company',''), data.get('role',''),
            data.get('content',''), int(data.get('rating', 5)), 1 if data.get('featured') else 0
        ))
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/testimonials/<int:id>/delete', methods=['POST'])
@admin_required
def admin_testimonials_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM testimonials WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/testimonials/<int:id>/edit', methods=['POST'])
@admin_required
def admin_testimonials_edit(id):
    data = request.form
    with get_db() as db:
        db.execute('''UPDATE testimonials SET client_name=?, company=?, role=?, content=?, rating=?, featured=? WHERE id=?''', (
            data.get('client_name',''), data.get('company',''), data.get('role',''),
            data.get('content',''), int(data.get('rating', 5)), 1 if data.get('featured') else 0, id
        ))
    return redirect(url_for('admin_testimonials'))

# ─── ADMIN SERVICES CRUD ───

@app.route('/admin/services')
@admin_required
def admin_services():
    with get_db() as db:
        items = db.execute("SELECT * FROM services ORDER BY id ASC").fetchall()
    return render_template('admin/services.html', items=items)

@app.route('/admin/services/add', methods=['POST'])
@admin_required
def admin_services_add():
    data = request.form
    with get_db() as db:
        db.execute('''INSERT INTO services (title, description, icon, price, features, sort_order)
                    VALUES (?,?,?,?,?,?)''', (
            data.get('title',''), data.get('description',''), data.get('icon',''),
            data.get('price',''), data.get('features',''), int(data.get('sort_order', 0))
        ))
    return redirect(url_for('admin_services'))

@app.route('/admin/services/<int:id>/delete', methods=['POST'])
@admin_required
def admin_services_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM services WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/services/<int:id>/edit', methods=['POST'])
@admin_required
def admin_services_edit(id):
    data = request.form
    with get_db() as db:
        db.execute('''UPDATE services SET title=?, description=?, icon=?, price=?, features=?, sort_order=? WHERE id=?''', (
            data.get('title',''), data.get('description',''), data.get('icon',''),
            data.get('price',''), data.get('features',''), int(data.get('sort_order', 0)), id
        ))
    return redirect(url_for('admin_services'))

# ─── ADMIN SETTINGS ───

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        data = request.form
        with get_db() as db:
            for key, value in data.items():
                db.execute("INSERT OR REPLACE INTO site_settings (key, value) VALUES (?, ?)", (key, value))
        flash('Settings saved.')
        return redirect(url_for('admin_settings'))
    with get_db() as db:
        settings = {row['key']: row['value'] for row in db.execute("SELECT * FROM site_settings").fetchall()}
    return render_template('admin/settings.html', settings=settings)

# ─── ADMIN REVIEWS CRUD ───

@app.route('/admin/reviews')
@admin_required
def admin_reviews():
    search = request.args.get('search', '')
    rating = request.args.get('rating', '')
    with get_db() as db:
        query = "SELECT * FROM reviews"
        params = []
        conditions = []
        if search:
            conditions.append("(client_name LIKE ? OR review_text LIKE ?)")
            params.extend([f'%{search}%']*2)
        if rating:
            conditions.append("rating=?")
            params.append(int(rating))
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at DESC"
        items = db.execute(query, params).fetchall()
    return render_template('admin/reviews.html', items=items, search=search, rating=rating)

@app.route('/admin/reviews/add', methods=['POST'])
@admin_required
def admin_reviews_add():
    data = request.form
    with get_db() as db:
        db.execute('''INSERT INTO reviews (client_name, country, rating, service, review_text, is_verified)
                    VALUES (?,?,?,?,?,?)''', (
            data.get('client_name',''), data.get('country',''), int(data.get('rating', 5)),
            data.get('service',''), data.get('review_text',''), 1 if data.get('is_verified') else 0
        ))
    return redirect(url_for('admin_reviews'))

@app.route('/admin/reviews/<int:id>/delete', methods=['POST'])
@admin_required
def admin_reviews_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM reviews WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/reviews/<int:id>/edit', methods=['POST'])
@admin_required
def admin_reviews_edit(id):
    data = request.form
    with get_db() as db:
        db.execute('''UPDATE reviews SET client_name=?, country=?, rating=?, service=?, review_text=?, is_verified=? WHERE id=?''', (
            data.get('client_name',''), data.get('country',''), int(data.get('rating', 5)),
            data.get('service',''), data.get('review_text',''), 1 if data.get('is_verified') else 0, id
        ))
    return redirect(url_for('admin_reviews'))

# ─── ADMIN FAQS CRUD ───

@app.route('/admin/faqs')
@admin_required
def admin_faqs():
    with get_db() as db:
        items = db.execute("SELECT * FROM faqs ORDER BY sort_order ASC, id ASC").fetchall()
    return render_template('admin/faqs.html', items=items)

@app.route('/admin/faqs/add', methods=['POST'])
@admin_required
def admin_faqs_add():
    data = request.form
    with get_db() as db:
        db.execute('''INSERT INTO faqs (question, answer, category, sort_order, is_published)
                    VALUES (?,?,?,?,?)''', (
            data.get('question',''), data.get('answer',''), data.get('category','General'),
            int(data.get('sort_order', 0)), 1 if data.get('is_published') else 0
        ))
    return redirect(url_for('admin_faqs'))

@app.route('/admin/faqs/<int:id>/delete', methods=['POST'])
@admin_required
def admin_faqs_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM faqs WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/faqs/<int:id>/edit', methods=['POST'])
@admin_required
def admin_faqs_edit(id):
    data = request.form
    with get_db() as db:
        db.execute('''UPDATE faqs SET question=?, answer=?, category=?, sort_order=?, is_published=? WHERE id=?''', (
            data.get('question',''), data.get('answer',''), data.get('category','General'),
            int(data.get('sort_order', 0)), 1 if data.get('is_published') else 0, id
        ))
    return redirect(url_for('admin_faqs'))

# ─── ADMIN SKILLS CRUD ───

@app.route('/admin/skills')
@admin_required
def admin_skills():
    with get_db() as db:
        items = db.execute("SELECT * FROM skills ORDER BY sort_order ASC, id ASC").fetchall()
    return render_template('admin/skills.html', items=items)

@app.route('/admin/skills/add', methods=['POST'])
@admin_required
def admin_skills_add():
    data = request.form
    with get_db() as db:
        db.execute('''INSERT INTO skills (name, percentage, category, icon, sort_order)
                    VALUES (?,?,?,?,?)''', (
            data.get('name',''), int(data.get('percentage', 50)), data.get('category','Design'),
            data.get('icon','fas fa-star'), int(data.get('sort_order', 0))
        ))
    return redirect(url_for('admin_skills'))

@app.route('/admin/skills/<int:id>/delete', methods=['POST'])
@admin_required
def admin_skills_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM skills WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/skills/<int:id>/edit', methods=['POST'])
@admin_required
def admin_skills_edit(id):
    data = request.form
    with get_db() as db:
        db.execute('''UPDATE skills SET name=?, percentage=?, category=?, icon=?, sort_order=? WHERE id=?''', (
            data.get('name',''), int(data.get('percentage', 50)), data.get('category','Design'),
            data.get('icon','fas fa-star'), int(data.get('sort_order', 0)), id
        ))
    return redirect(url_for('admin_skills'))

# ─── API ENDPOINTS (for frontend) ───

@app.route('/api/portfolio')
def api_portfolio():
    with get_db() as db:
        items = db.execute("SELECT * FROM portfolio WHERE featured=1 OR 1=1 ORDER BY created_at DESC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/testimonials')
def api_testimonials():
    with get_db() as db:
        items = db.execute("SELECT * FROM testimonials ORDER BY created_at DESC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/services')
def api_services():
    with get_db() as db:
        items = db.execute("SELECT * FROM services ORDER BY id ASC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/reviews')
def api_reviews():
    search = request.args.get('search', '')
    rating = request.args.get('rating', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page
    with get_db() as db:
        params = []
        conditions = []
        if search:
            conditions.append("(client_name LIKE ? OR review_text LIKE ?)")
            params.extend([f'%{search}%']*2)
        if rating:
            conditions.append("rating=?")
            params.append(int(rating))
        where = ""
        if conditions:
            where = " WHERE " + " AND ".join(conditions)
        total = db.execute(f"SELECT COUNT(*) as c FROM reviews{where}", params).fetchone()['c']
        items = db.execute(f"SELECT * FROM reviews{where} ORDER BY created_at DESC LIMIT ? OFFSET ?", params + [per_page, offset]).fetchall()
    return jsonify({'items': [dict(i) for i in items], 'total': total, 'page': page, 'per_page': per_page})

@app.route('/api/reviews/stats')
def api_reviews_stats():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) as c FROM reviews").fetchone()['c']
        avg = db.execute("SELECT ROUND(AVG(rating), 1) as a FROM reviews").fetchone()['a'] or 0
        five_star = db.execute("SELECT COUNT(*) as c FROM reviews WHERE rating=5").fetchone()['c']
        five_star_pct = round((five_star / total * 100) if total > 0 else 0, 1)
    return jsonify({'total': total, 'avg_rating': avg, 'five_star_pct': five_star_pct, 'five_star_count': five_star})

@app.route('/api/faqs')
def api_faqs():
    with get_db() as db:
        items = db.execute("SELECT * FROM faqs WHERE is_published=1 ORDER BY sort_order ASC, id ASC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/skills')
def api_skills():
    with get_db() as db:
        items = db.execute("SELECT * FROM skills ORDER BY sort_order ASC, id ASC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/captcha')
def api_captcha():
    import random
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    ops = ['+', '-', '*']
    op = random.choice(ops[:2])  # keep it simple: + or -
    if op == '+': answer = a + b
    elif op == '-': answer = a - b
    else: answer = a * b
    return jsonify({'question': f'{a} {op} {b} = ?', 'answer': str(answer)})

# ─── VISITOR TRACKING ───

@app.route('/api/track', methods=['POST'])
def api_track():
    try:
        data = request.get_json(silent=True) or {}
        event = data.get('event', 'page_view')
        fingerprint = data.get('fingerprint', '')
        session_id = data.get('session_id', '')
        page_url = data.get('page_url', '')
        page_title = data.get('page_title', '')
        referrer = data.get('referrer', '')

        if not fingerprint or not session_id:
            return jsonify({'error': 'Missing tracking identifiers'}), 400

        ua = request.headers.get('User-Agent', '')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()
        current_time = datetime.utcnow()

        with get_db() as db:
            # Upsert visitor
            visitor = db.execute("SELECT * FROM visitors WHERE fingerprint=?", (fingerprint,)).fetchone()
            if visitor:
                visitor_id = visitor['id']
                db.execute("UPDATE visitors SET last_visit=?, visit_count=visit_count+1, ip_address=? WHERE id=?",
                          (current_time, ip, visitor_id))
            else:
                cursor = db.execute('''INSERT INTO visitors (fingerprint, ip_address, device_type, os, browser,
                    browser_version, screen_resolution, language, country, city, region, timezone)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (
                    fingerprint, ip,
                    data.get('device_type', ''),
                    data.get('os', ''),
                    data.get('browser', ''),
                    data.get('browser_version', ''),
                    data.get('screen_resolution', ''),
                    data.get('language', ''),
                    data.get('country', ''),
                    data.get('city', ''),
                    data.get('region', ''),
                    data.get('timezone', '')
                ))
                visitor_id = cursor.lastrowid

            # Get or create visit
            visit = db.execute("SELECT * FROM visits WHERE session_id=?", (session_id,)).fetchone()
            if event == 'session_start' or not visit:
                # Determine traffic source
                traffic_source = 'Direct'
                utm_source = data.get('utm_source', '')
                utm_medium = data.get('utm_medium', '')
                utm_campaign = data.get('utm_campaign', '')

                if utm_source:
                    traffic_source = 'Campaign'
                elif referrer:
                    ref_lower = referrer.lower()
                    if 'google' in ref_lower:
                        traffic_source = 'Google Search'
                    elif 'bing' in ref_lower:
                        traffic_source = 'Bing'
                    elif 'facebook' in ref_lower:
                        traffic_source = 'Facebook'
                    elif 'instagram' in ref_lower:
                        traffic_source = 'Instagram'
                    elif 'linkedin' in ref_lower:
                        traffic_source = 'LinkedIn'
                    elif 'x.com' in ref_lower or 'twitter' in ref_lower:
                        traffic_source = 'X (Twitter)'
                    elif 'youtube' in ref_lower:
                        traffic_source = 'YouTube'
                    elif 'mail' in ref_lower or 'email' in ref_lower:
                        traffic_source = 'Email'
                    elif 'qrcode' in ref_lower or 'qr' in ref_lower:
                        traffic_source = 'QR Code'
                    else:
                        traffic_source = 'Referral'

                if visit:
                    # Update existing
                    db.execute('''UPDATE visits SET landing_page=?, referrer=?, traffic_source=?,
                        utm_source=?, utm_medium=?, utm_campaign=?, device_type=?, os=?, browser=?,
                        browser_version=?, screen_resolution=?, country=?, city=?, region=?,
                        timezone=?, language=? WHERE session_id=?''', (
                        page_url, referrer, traffic_source, utm_source, utm_medium, utm_campaign,
                        data.get('device_type', ''), data.get('os', ''), data.get('browser', ''),
                        data.get('browser_version', ''), data.get('screen_resolution', ''),
                        data.get('country', ''), data.get('city', ''), data.get('region', ''),
                        data.get('timezone', ''), data.get('language', ''), session_id
                    ))
                else:
                    cursor = db.execute('''INSERT INTO visits (visitor_id, session_id, ip_address, user_agent,
                        referrer, landing_page, traffic_source, utm_source, utm_medium, utm_campaign,
                        utm_term, utm_content, device_type, os, browser, browser_version,
                        screen_resolution, country, city, region, timezone, language)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                        visitor_id, session_id, ip, ua, referrer, page_url, traffic_source,
                        utm_source, utm_medium, utm_campaign,
                        data.get('utm_term', ''), data.get('utm_content', ''),
                        data.get('device_type', ''), data.get('os', ''), data.get('browser', ''),
                        data.get('browser_version', ''), data.get('screen_resolution', ''),
                        data.get('country', ''), data.get('city', ''), data.get('region', ''),
                        data.get('timezone', ''), data.get('language', '')
                    ))
                    visit_id = cursor.lastrowid
                    visit = db.execute("SELECT * FROM visits WHERE id=?", (visit_id,)).fetchone()

                # Add to live visitors
                db.execute('''INSERT OR REPLACE INTO live_visitors (visitor_id, session_id, current_page,
                    page_title, country, device_type, browser, ip_address, last_heartbeat)
                    VALUES (?,?,?,?,?,?,?,?,?)''', (
                    visitor_id, session_id, page_url, page_title,
                    data.get('country', ''), data.get('device_type', ''),
                    data.get('browser', ''), ip, current_time
                ))

            visit_id = visit['id'] if visit else None

            if event == 'page_view' and visit_id:
                # Record page view
                db.execute('''INSERT INTO page_views (visit_id, visitor_id, page_url, page_title, referrer)
                    VALUES (?,?,?,?,?)''', (visit_id, visitor_id, page_url, page_title, referrer))
                db.execute("UPDATE visits SET page_views=page_views+1, exit_page=? WHERE id=?", (page_url, visit_id))
                db.execute("UPDATE visitors SET total_page_views=total_page_views+1 WHERE id=?", (visitor_id,))

                # Update live visitor
                db.execute('''UPDATE live_visitors SET current_page=?, page_title=?, last_heartbeat=?
                    WHERE session_id=?''', (page_url, page_title, current_time, session_id))

            elif event == 'heartbeat' and visit_id:
                db.execute('''UPDATE live_visitors SET last_heartbeat=? WHERE session_id=?''',
                          (current_time, session_id))
                duration = int(data.get('duration', 0))
                if duration > 0:
                    db.execute("UPDATE visits SET session_duration=? WHERE id=? AND session_duration<?",
                              (duration, visit_id, duration))

            elif event == 'click' and visit_id:
                db.execute("UPDATE visits SET clicks=clicks+1 WHERE id=?", (visit_id,))
                db.execute("UPDATE visitors SET total_clicks=total_clicks+1 WHERE id=?", (visitor_id,))

            elif event == 'scroll' and visit_id:
                depth = int(data.get('scroll_depth', 0))
                db.execute("UPDATE visits SET scroll_depth=MAX(scroll_depth,?) WHERE id=?", (depth, visit_id))

            elif event == 'session_end' and visit_id:
                duration = int(data.get('duration', 0))
                db.execute('''UPDATE visits SET session_duration=?, ended_at=?, is_bounce=0
                    WHERE id=? AND ended_at IS NULL''', (duration, current_time, visit_id))
                db.execute("DELETE FROM live_visitors WHERE session_id=?", (session_id,))
                if duration > 0:
                    db.execute("UPDATE visitors SET total_session_duration=total_session_duration+? WHERE id=?",
                              (duration, visitor_id))

            # Clean up stale live visitors (30+ seconds old)
            db.execute("DELETE FROM live_visitors WHERE last_heartbeat < ?",
                      (current_time - timedelta(seconds=30),))

            return jsonify({'success': True, 'visitor_id': visitor_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── ADMIN ANALYTICS ───

def log_activity(action, details=''):
    try:
        with get_db() as db:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
            db.execute("INSERT INTO activity_logs (admin_username, action, details, ip_address) VALUES (?,?,?,?)",
                      (session.get('admin_username',''), action, details[:500], ip))
    except: pass

# ─── MEDIA LIBRARY ───

@app.route('/admin/media')
@admin_required
def admin_media():
    folder = request.args.get('folder', '/')
    with get_db() as db:
        files = db.execute("SELECT * FROM media_files WHERE folder=? ORDER BY uploaded_at DESC", (folder,)).fetchall()
        folders = db.execute("SELECT DISTINCT folder FROM media_files ORDER BY folder").fetchall()
    return render_template('admin/media.html', files=files, folders=[r['folder'] for r in folders], current_folder=folder)

@app.route('/admin/media/upload', methods=['POST'])
@admin_required
def admin_media_upload():
    folder = request.form.get('folder', '/')
    uploaded = []
    for f in request.files.getlist('files[]'):
        if f and f.filename and allowed_file(f.filename):
            safe = secure_filename(f.filename)
            unique = f"{uuid.uuid4().hex[:8]}_{safe}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            f.save(filepath)
            fsize = os.path.getsize(filepath)
            ext = safe.rsplit('.', 1)[1].lower() if '.' in safe else ''
            ftype = {'png':'image','jpg':'image','jpeg':'image','gif':'image','webp':'image','mp4':'video','mov':'video','avi':'video','pdf':'document'}.get(ext, 'other')
            with get_db() as db:
                db.execute("INSERT INTO media_files (filename, original_name, filepath, filetype, filesize, folder) VALUES (?,?,?,?,?,?)",
                          (unique, safe, f'/uploads/{unique}', ftype, fsize, folder))
            uploaded.append(unique)
    log_activity('Media Upload', f'Uploaded {len(uploaded)} files to {folder}')
    return jsonify({'success': True, 'uploaded': len(uploaded)})

@app.route('/admin/media/<int:id>/delete', methods=['POST'])
@admin_required
def admin_media_delete(id):
    with get_db() as db:
        f = db.execute("SELECT * FROM media_files WHERE id=?", (id,)).fetchone()
        if f:
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], f['filename'])
            if os.path.exists(fpath): os.remove(fpath)
            db.execute("DELETE FROM media_files WHERE id=?", (id,))
            log_activity('Media Delete', f'Deleted {f["original_name"]}')
    return jsonify({'success': True})

@app.route('/admin/media/update-alt', methods=['POST'])
@admin_required
def admin_media_update_alt():
    data = request.json
    with get_db() as db:
        db.execute("UPDATE media_files SET alt_text=? WHERE id=?", (data.get('alt_text',''), data.get('id')))
    return jsonify({'success': True})

@app.route('/api/media')
def api_media():
    with get_db() as db:
        files = db.execute("SELECT * FROM media_files ORDER BY uploaded_at DESC LIMIT 50").fetchall()
    return jsonify([dict(f) for f in files])

# ─── NAVIGATION MANAGER ───

@app.route('/admin/navigation')
@admin_required
def admin_navigation():
    with get_db() as db:
        items = db.execute("SELECT * FROM navigation_items ORDER BY sort_order ASC, id ASC").fetchall()
    return render_template('admin/navigation.html', items=items)

@app.route('/admin/navigation/add', methods=['POST'])
@admin_required
def admin_navigation_add():
    data = request.form
    with get_db() as db:
        db.execute("INSERT INTO navigation_items (label, link, parent_id, icon, sort_order, is_visible) VALUES (?,?,?,?,?,?)",
                  (data.get('label',''), data.get('link','#'), int(data.get('parent_id',0)),
                   data.get('icon',''), int(data.get('sort_order',0)), 1 if data.get('is_visible') else 0))
    log_activity('Navigation Add', f'Added nav: {data.get("label")}')
    return redirect(url_for('admin_navigation'))

@app.route('/admin/navigation/<int:id>/edit', methods=['POST'])
@admin_required
def admin_navigation_edit(id):
    data = request.form
    with get_db() as db:
        db.execute("UPDATE navigation_items SET label=?, link=?, parent_id=?, icon=?, sort_order=?, is_visible=? WHERE id=?",
                  (data.get('label',''), data.get('link','#'), int(data.get('parent_id',0)),
                   data.get('icon',''), int(data.get('sort_order',0)), 1 if data.get('is_visible') else 0, id))
    log_activity('Navigation Edit', f'Edited nav: {data.get("label")}')
    return redirect(url_for('admin_navigation'))

@app.route('/admin/navigation/<int:id>/delete', methods=['POST'])
@admin_required
def admin_navigation_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM navigation_items WHERE id=?", (id,))
    return jsonify({'success': True})

@app.route('/admin/navigation/reorder', methods=['POST'])
@admin_required
def admin_navigation_reorder():
    data = request.json
    with get_db() as db:
        for item in data.get('order', []):
            db.execute("UPDATE navigation_items SET sort_order=? WHERE id=?", (item.get('order',0), item.get('id')))
    return jsonify({'success': True})

# ─── PRICING PLANS ───

@app.route('/admin/pricing')
@admin_required
def admin_pricing():
    with get_db() as db:
        plans = db.execute("SELECT * FROM pricing_plans ORDER BY sort_order ASC, id ASC").fetchall()
    return render_template('admin/pricing.html', plans=plans)

@app.route('/admin/pricing/add', methods=['POST'])
@admin_required
def admin_pricing_add():
    data = request.form
    features = json.dumps([f.strip() for f in data.get('features','').split('\n') if f.strip()])
    with get_db() as db:
        db.execute('''INSERT INTO pricing_plans (name, price, currency, period, description, features, icon, button_text, button_link, highlighted, popular_badge, tier, sort_order)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            data.get('name',''), data.get('price','0'), data.get('currency','$'), data.get('period','/mo'),
            data.get('description',''), features, data.get('icon','fas fa-star'),
            data.get('button_text','Get Started'), data.get('button_link','#contact'),
            1 if data.get('highlighted') else 0, data.get('popular_badge',''),
            data.get('tier','bundle'), int(data.get('sort_order',0))
        ))
    log_activity('Pricing Add', f'Added plan: {data.get("name")}')
    return redirect(url_for('admin_pricing'))

@app.route('/admin/pricing/<int:id>/edit', methods=['POST'])
@admin_required
def admin_pricing_edit(id):
    data = request.form
    features = json.dumps([f.strip() for f in data.get('features','').split('\n') if f.strip()])
    with get_db() as db:
        db.execute('''UPDATE pricing_plans SET name=?, price=?, currency=?, period=?, description=?, features=?, icon=?,
            button_text=?, button_link=?, highlighted=?, popular_badge=?, tier=?, sort_order=? WHERE id=?''', (
            data.get('name',''), data.get('price','0'), data.get('currency','$'), data.get('period','/mo'),
            data.get('description',''), features, data.get('icon','fas fa-star'),
            data.get('button_text','Get Started'), data.get('button_link','#contact'),
            1 if data.get('highlighted') else 0, data.get('popular_badge',''),
            data.get('tier','bundle'), int(data.get('sort_order',0)), id
        ))
    log_activity('Pricing Edit', f'Edited plan: {data.get("name")}')
    return redirect(url_for('admin_pricing'))

@app.route('/admin/pricing/<int:id>/delete', methods=['POST'])
@admin_required
def admin_pricing_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM pricing_plans WHERE id=?", (id,))
    return jsonify({'success': True})

# ─── BLOG / CMS ───

@app.route('/admin/blog')
@admin_required
def admin_blog():
    status = request.args.get('status', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    with get_db() as db:
        conditions = []
        params = []
        if status:
            conditions.append("status=?")
            params.append(status)
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        total = db.execute(f"SELECT COUNT(*) as c FROM blog_posts{where}", params).fetchone()['c']
        posts = db.execute(f"SELECT * FROM blog_posts{where} ORDER BY created_at DESC LIMIT ? OFFSET ?", params + [per_page, offset]).fetchall()
    return render_template('admin/blog.html', posts=posts, total=total, page=page, per_page=per_page, status_filter=status)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@admin_required
def admin_blog_new():
    if request.method == 'POST':
        data = request.form
        slug = re.sub(r'[^a-z0-9-]', '', data.get('slug','') or data.get('title','').lower().replace(' ','-')[:60])
        with get_db() as db:
            db.execute('''INSERT INTO blog_posts (title, slug, content, excerpt, category, tags, featured_image, author, status, seo_title, seo_description, seo_keywords)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (
                data.get('title',''), slug, data.get('content',''), data.get('excerpt',''),
                data.get('category',''), data.get('tags',''), data.get('featured_image',''),
                data.get('author','Siam Munkasir'), data.get('status','draft'),
                data.get('seo_title',''), data.get('seo_description',''), data.get('seo_keywords','')
            ))
        log_activity('Blog Created', f'Created post: {data.get("title")}')
        return redirect(url_for('admin_blog'))
    return render_template('admin/blog_edit.html', post=None)

@app.route('/admin/blog/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_blog_edit(id):
    with get_db() as db:
        post = db.execute("SELECT * FROM blog_posts WHERE id=?", (id,)).fetchone()
        if not post: abort(404)
        if request.method == 'POST':
            data = request.form
            slug = re.sub(r'[^a-z0-9-]', '', data.get('slug','') or post['slug'])
            db.execute('''UPDATE blog_posts SET title=?, slug=?, content=?, excerpt=?, category=?, tags=?,
                featured_image=?, author=?, status=?, seo_title=?, seo_description=?, seo_keywords=? WHERE id=?''', (
                data.get('title',''), slug, data.get('content',''), data.get('excerpt',''),
                data.get('category',''), data.get('tags',''), data.get('featured_image',''),
                data.get('author','Siam Munkasir'), data.get('status','draft'),
                data.get('seo_title',''), data.get('seo_description',''), data.get('seo_keywords',''), id
            ))
            log_activity('Blog Updated', f'Updated post: {data.get("title")}')
            return redirect(url_for('admin_blog'))
    return render_template('admin/blog_edit.html', post=post)

@app.route('/admin/blog/<int:id>/delete', methods=['POST'])
@admin_required
def admin_blog_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM blog_posts WHERE id=?", (id,))
    return jsonify({'success': True})

# ─── ACTIVITY LOG ───

@app.route('/admin/activity-log')
@admin_required
def admin_activity_log():
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = (page - 1) * per_page
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) as c FROM activity_logs").fetchone()['c']
        logs = db.execute("SELECT * FROM activity_logs ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    return render_template('admin/activity_log.html', logs=logs, total=total, page=page, per_page=per_page)

# ─── CMS SETTINGS API ───

@app.route('/admin/settings/update', methods=['POST'])
@admin_required
def admin_settings_update():
    data = request.form
    with get_db() as db:
        for key, value in data.items():
            db.execute("INSERT OR REPLACE INTO site_settings (key, value) VALUES (?, ?)", (key, value))
    log_activity('Settings Update', f'Updated {len(data)} settings')
    return jsonify({'success': True})

@app.route('/admin/homepage')
@admin_required
def admin_homepage():
    with get_db() as db:
        sections = {}
        for r in db.execute("SELECT * FROM homepage_sections").fetchall():
            try: sections[r['section_key']] = json.loads(r['content'])
            except: sections[r['section_key']] = r['content']
        settings = {r['key']: r['value'] for r in db.execute("SELECT * FROM site_settings").fetchall()}
    return render_template('admin/homepage.html', sections=sections, settings=settings)

@app.route('/admin/homepage/update', methods=['POST'])
@admin_required
def admin_homepage_update():
    data = request.json
    with get_db() as db:
        for key, value in data.items():
            db.execute("INSERT OR REPLACE INTO homepage_sections (section_key, content) VALUES (?,?)",
                      (key, json.dumps(value) if isinstance(value, (dict, list)) else value))
    log_activity('Homepage Update', f'Updated {len(data)} sections')
    return jsonify({'success': True})

@app.route('/api/settings')
def api_settings():
    with get_db() as db:
        settings = {r['key']: r['value'] for r in db.execute("SELECT * FROM site_settings").fetchall()}
    return jsonify(settings)

@app.route('/api/pricing-plans')
def api_pricing_plans():
    with get_db() as db:
        plans = db.execute("SELECT * FROM pricing_plans ORDER BY sort_order ASC, id ASC").fetchall()
    result = []
    for p in plans:
        d = dict(p)
        try: d['features'] = json.loads(d['features'])
        except: d['features'] = []
        result.append(d)
    return jsonify(result)

@app.route('/api/navigation')
def api_navigation():
    with get_db() as db:
        items = db.execute("SELECT * FROM navigation_items WHERE is_visible=1 ORDER BY sort_order ASC, id ASC").fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/api/blog-posts')
def api_blog_posts():
    with get_db() as db:
        posts = db.execute("SELECT * FROM blog_posts WHERE status='published' ORDER BY published_at DESC LIMIT 10").fetchall()
    return jsonify([dict(p) for p in posts])

@app.route('/api/homepage-sections')
def api_homepage_sections():
    with get_db() as db:
        sections = {r['section_key']: r['content'] for r in db.execute("SELECT * FROM homepage_sections WHERE is_active=1").fetchall()}
    result = {}
    for k, v in sections.items():
        try: result[k] = json.loads(v)
        except: result[k] = v
    return jsonify(result)

# ─── BACKUP ───

@app.route('/admin/backup')
@admin_required
def admin_backup():
    return render_template('admin/backup.html')

@app.route('/admin/backup/create', methods=['POST'])
@admin_required
def admin_backup_create():
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.db')
    try:
        import shutil
        shutil.copy2(app.config['DATABASE'], backup_file)
        log_activity('Backup Created', f'Backup saved: backup_{timestamp}.db')
        return jsonify({'success': True, 'file': f'backup_{timestamp}.db', 'size': os.path.getsize(backup_file)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/backup/list')
@admin_required
def admin_backup_list():
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    backups = []
    for f in sorted(os.listdir(backup_dir), reverse=True):
        fpath = os.path.join(backup_dir, f)
        if os.path.isfile(fpath) and f.endswith('.db'):
            backups.append({'file': f, 'size': os.path.getsize(fpath), 'date': datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')})
    return jsonify(backups)

@app.route('/admin/backup/restore', methods=['POST'])
@admin_required
def admin_backup_restore():
    file = request.json.get('file', '')
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    fpath = os.path.join(backup_dir, file)
    if not os.path.exists(fpath) or not file.endswith('.db'):
        return jsonify({'error': 'Invalid backup file'}), 400
    try:
        import shutil
        shutil.copy2(fpath, app.config['DATABASE'])
        log_activity('Backup Restored', f'Restored from: {file}')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/backup/download/<filename>')
@admin_required
def admin_backup_download(filename):
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    return send_from_directory(backup_dir, filename, as_attachment=True)

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    return render_template('admin/analytics.html')

@app.route('/api/admin/analytics/stats')
@admin_required
def api_analytics_stats():
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    with get_db() as db:
        # Total visitors
        total_visitors = db.execute("SELECT COUNT(*) as c FROM visitors").fetchone()['c']

        # Today's visitors
        today_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)=?",
                                   (today,)).fetchone()['c']
        yesterday_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)=?",
                                       (yesterday,)).fetchone()['c']

        # This week
        week_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)>=?",
                                  (week_start,)).fetchone()['c']

        # This month
        month_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)>=?",
                                   (month_start,)).fetchone()['c']

        # This year
        year_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)>=?",
                                  (year_start,)).fetchone()['c']

        # Live visitors
        cutoff = datetime.utcnow() - timedelta(seconds=15)
        live_visitors = db.execute("SELECT COUNT(*) as c FROM live_visitors WHERE last_heartbeat>=?",
                                  (cutoff,)).fetchone()['c']

        # Unique vs returning
        unique_visitors = db.execute("SELECT COUNT(*) as c FROM visitors WHERE visit_count=1").fetchone()['c']
        returning_visitors = db.execute("SELECT COUNT(*) as c FROM visitors WHERE visit_count>1").fetchone()['c']

        # Total page views
        total_page_views = db.execute("SELECT COUNT(*) as c FROM page_views").fetchone()['c']

        # Average session duration
        avg_duration = db.execute("SELECT COALESCE(ROUND(AVG(session_duration)),0) as a FROM visits WHERE session_duration>0").fetchone()['a']

        # Bounce rate
        total_sessions = db.execute("SELECT COUNT(*) as c FROM visits").fetchone()['c']
        bounces = db.execute("SELECT COUNT(*) as c FROM visits WHERE is_bounce=1 AND page_views=1").fetchone()['c']
        bounce_rate = round((bounces / total_sessions * 100), 1) if total_sessions > 0 else 0

        # Previous period comparisons
        prev_month_start = (month_start - timedelta(days=1)).replace(day=1)
        prev_month_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)>=? AND date(started_at)<?",
                                        (prev_month_start, month_start)).fetchone()['c']
        prev_week_start = week_start - timedelta(days=7)
        prev_week_visitors = db.execute("SELECT COUNT(DISTINCT visitor_id) as c FROM visits WHERE date(started_at)>=? AND date(started_at)<?",
                                       (prev_week_start, week_start)).fetchone()['c']

    month_change = round(((month_visitors - prev_month_visitors) / prev_month_visitors * 100), 1) if prev_month_visitors > 0 else 0
    week_change = round(((week_visitors - prev_week_visitors) / prev_week_visitors * 100), 1) if prev_week_visitors > 0 else 0

    return jsonify({
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
        'yesterday_visitors': yesterday_visitors,
        'week_visitors': week_visitors,
        'month_visitors': month_visitors,
        'year_visitors': year_visitors,
        'live_visitors': live_visitors,
        'unique_visitors': unique_visitors,
        'returning_visitors': returning_visitors,
        'total_page_views': total_page_views,
        'avg_session_duration': avg_duration,
        'bounce_rate': bounce_rate,
        'month_change': month_change,
        'week_change': week_change
    })

@app.route('/api/admin/analytics/visitor-growth')
@admin_required
def api_analytics_visitor_growth():
    period = request.args.get('period', 'daily')
    with get_db() as db:
        if period == 'daily':
            rows = db.execute('''SELECT date(started_at) as d, COUNT(DISTINCT visitor_id) as c
                FROM visits WHERE started_at >= date('now', '-30 days')
                GROUP BY d ORDER BY d''').fetchall()
        elif period == 'weekly':
            rows = db.execute('''SELECT strftime('%Y-W%W', started_at) as d, COUNT(DISTINCT visitor_id) as c
                FROM visits WHERE started_at >= date('now', '-6 months')
                GROUP BY d ORDER BY d''').fetchall()
        elif period == 'monthly':
            rows = db.execute('''SELECT strftime('%Y-%m', started_at) as d, COUNT(DISTINCT visitor_id) as c
                FROM visits WHERE started_at >= date('now', '-12 months')
                GROUP BY d ORDER BY d''').fetchall()
        else:
            rows = db.execute('''SELECT strftime('%Y', started_at) as d, COUNT(DISTINCT visitor_id) as c
                FROM visits GROUP BY d ORDER BY d''').fetchall()
    return jsonify([{'date': r['d'], 'count': r['c']} for r in rows])

@app.route('/api/admin/analytics/traffic-sources')
@admin_required
def api_analytics_traffic():
    with get_db() as db:
        rows = db.execute('''SELECT traffic_source, COUNT(*) as c FROM visits
            GROUP BY traffic_source ORDER BY c DESC''').fetchall()
    return jsonify([{'source': r['traffic_source'], 'count': r['c']} for r in rows])

@app.route('/api/admin/analytics/devices')
@admin_required
def api_analytics_devices():
    with get_db() as db:
        rows = db.execute('''SELECT device_type, COUNT(*) as c FROM visits
            WHERE device_type != '' GROUP BY device_type ORDER BY c DESC''').fetchall()
    return jsonify([{'device': r['device_type'] or 'Unknown', 'count': r['c']} for r in rows])

@app.route('/api/admin/analytics/browsers')
@admin_required
def api_analytics_browsers():
    with get_db() as db:
        rows = db.execute('''SELECT browser, COUNT(*) as c FROM visits
            WHERE browser != '' GROUP BY browser ORDER BY c DESC''').fetchall()
    return jsonify([{'browser': r['browser'] or 'Unknown', 'count': r['c']} for r in rows])

@app.route('/api/admin/analytics/countries')
@admin_required
def api_analytics_countries():
    with get_db() as db:
        rows = db.execute('''SELECT country, COUNT(*) as c FROM visitors
            WHERE country != '' GROUP BY country ORDER BY c DESC LIMIT 20''').fetchall()
    total = sum(r['c'] for r in rows)
    return jsonify([{'country': r['country'], 'count': r['c'], 'percentage': round(r['c']/total*100,1) if total else 0} for r in rows])

@app.route('/api/admin/analytics/pages')
@admin_required
def api_analytics_pages():
    with get_db() as db:
        rows = db.execute('''SELECT page_url, COUNT(*) as views,
            COALESCE(ROUND(AVG(time_spent)),0) as avg_time
            FROM page_views GROUP BY page_url
            ORDER BY views DESC LIMIT 20''').fetchall()
    return jsonify([{'page': r['page_url'], 'views': r['views'], 'avg_time': r['avg_time']} for r in rows])

@app.route('/api/admin/analytics/live')
@admin_required
def api_analytics_live():
    cutoff = datetime.utcnow() - timedelta(seconds=15)
    with get_db() as db:
        rows = db.execute('''SELECT lv.*, v.browser, v.os, v.device_type, v.country, v.city
            FROM live_visitors lv
            LEFT JOIN visitors v ON lv.visitor_id = v.id
            WHERE lv.last_heartbeat >= ?
            ORDER BY lv.last_heartbeat DESC''', (cutoff,)).fetchall()
    result = []
    for r in rows:
        dur = (datetime.utcnow() - datetime.strptime(r['started_at'][:19], '%Y-%m-%d %H:%M:%S')).total_seconds() if r['started_at'] else 0
        result.append({
            'visitor_id': r['visitor_id'],
            'session_id': r['session_id'],
            'current_page': r['current_page'],
            'page_title': r['page_title'],
            'country': r['country'] or '',
            'city': r['city'] or '',
            'device_type': r['device_type'] or '',
            'browser': r['browser'] or '',
            'duration': int(dur)
        })
    return jsonify(result)

@app.route('/api/admin/analytics/visitor-log')
@admin_required
def api_analytics_visitor_log():
    search = request.args.get('search', '')
    source = request.args.get('source', '')
    device = request.args.get('device', '')
    country = request.args.get('country', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page

    with get_db() as db:
        conditions = []
        params = []
        if search:
            conditions.append("(v.ip_address LIKE ? OR v.country LIKE ? OR v.city LIKE ? OR v.browser LIKE ?)")
            params.extend([f'%{search}%']*4)
        if source:
            conditions.append("v.traffic_source=?")
            params.append(source)
        if device:
            conditions.append("v.device_type=?")
            params.append(device)
        if country:
            conditions.append("v.country=?")
            params.append(country)

        where = ""
        if conditions:
            where = " WHERE " + " AND ".join(conditions)

        total = db.execute(f"SELECT COUNT(*) as c FROM visits v{where}", params).fetchone()['c']
        rows = db.execute(f'''SELECT v.*, vi.fingerprint, vi.total_page_views, vi.total_clicks
            FROM visits v LEFT JOIN visitors vi ON v.visitor_id = vi.id
            {where} ORDER BY v.started_at DESC LIMIT ? OFFSET ?''',
            params + [per_page, offset]).fetchall()

    return jsonify({
        'items': [dict(r) for r in rows],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/admin/analytics/export')
@admin_required
def api_analytics_export():
    fmt = request.args.get('format', 'csv')
    with get_db() as db:
        rows = db.execute('''SELECT v.id, v.session_id, v.ip_address, v.country, v.city,
            v.device_type, v.browser, v.os, v.landing_page, v.exit_page,
            v.page_views, v.session_duration, v.traffic_source, v.is_bounce, v.started_at
            FROM visits v ORDER BY v.started_at DESC''').fetchall()

    if fmt == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Session ID', 'IP', 'Country', 'City', 'Device', 'Browser', 'OS',
                        'Landing Page', 'Exit Page', 'Page Views', 'Duration (s)', 'Traffic Source',
                        'Bounced', 'Date'])
        for r in rows:
            writer.writerow([r['id'], r['session_id'], r['ip_address'], r['country'], r['city'],
                           r['device_type'], r['browser'], r['os'], r['landing_page'], r['exit_page'],
                           r['page_views'], r['session_duration'], r['traffic_source'],
                           'Yes' if r['is_bounce'] else 'No', r['started_at']])
        response = app.response_class(output.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=analytics_visitor_log.csv'
        return response
    else:
        # Excel via CSV (simple fallback)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Session ID', 'IP', 'Country', 'City', 'Device', 'Browser', 'OS',
                        'Landing Page', 'Exit Page', 'Page Views', 'Duration (s)', 'Traffic Source', 'Date'])
        for r in rows:
            writer.writerow([r['id'], r['session_id'], r['ip_address'], r['country'], r['city'],
                           r['device_type'], r['browser'], r['os'], r['landing_page'], r['exit_page'],
                           r['page_views'], r['session_duration'], r['traffic_source'], r['started_at']])
        response = app.response_class(output.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=analytics_visitor_log.csv'
        return response

def seed_default_sections():
    """Seed homepage_sections if empty OR old format (migration helper)."""
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), 'portfolio.db')
    try:
        conn = sqlite3.connect(db_path)
        # Check if old-format sections exist (has 'headline' instead of 'title')
        hero = conn.execute("SELECT content FROM homepage_sections WHERE section_key='hero'").fetchone()
        needs_migration = hero and '"headline"' in hero[0]
        if needs_migration:
            print('Migrating homepage_sections to new format...')
        exists = conn.execute("SELECT COUNT(*) FROM homepage_sections").fetchone()[0]
        if exists == 0 or needs_migration:
            SECTIONS = {
                'hero': {
                    'badge_text': 'Available for Projects',
                    'title': 'AI-Powered Content That Captivates & Converts',
                    'roles': ['AI Content Strategist','UGC Specialist','Creative Director','Motion Designer','Brand Storyteller'],
                    'subtitle': "Crafting high-impact digital content and AI-powered solutions that drive real business results for brands worldwide — from UGC strategy to full AI automation systems.",
                    'cta_primary': {'text': 'View Portfolio', 'href': '#portfolio'},
                    'cta_secondary': {'text': 'Hire Me', 'href': '#contact'},
                    'cta_tertiary': {'text': 'Book a Call', 'href': 'https://wa.me/8801989430474'},
                    'stats': [{'label':'Projects Completed','value':200,'suffix':'+'},{'label':'Clients Served','value':50,'suffix':'+'},{'label':'Years Experience','value':3,'suffix':'+'},{'label':'Client Satisfaction','value':98,'suffix':'%'}]
                },
                'about': {
                    'tag': 'About Me',
                    'title': 'Creative Content Strategist & AI UGC Specialist',
                    'subtitle': 'Bridging creative storytelling with cutting-edge AI technology to deliver content that drives real business results.',
                    'name': 'Siam Munkasir',
                    'initials': 'SM',
                    'bio_1': "I'm a Creative Content Strategist and AI UGC Specialist based in Dhaka, Bangladesh. With 3+ years of experience, I help brands craft high-impact digital content and AI-powered solutions — from UGC strategy for e-commerce brands to short-form video production and full AI automation systems.",
                    'bio_2': 'My expertise spans User Generated Content (UGC) strategy for beauty and lifestyle brands, short-form video production across TikTok, Instagram, and YouTube, and AI-driven marketing automation. I combine creative storytelling with cutting-edge AI tools to deliver content that drives real business results.',
                    'mission': 'My mission is to bridge creative storytelling with cutting-edge AI technology — delivering content that not only looks authentic but also converts viewers into loyal customers.',
                    'process_steps': [{'title':'Discovery & Strategy','desc':'Understanding your brand, goals, and audience.'},{'title':'AI-Powered Research','desc':'Researching trends and generating data-backed concepts.'},{'title':'Script & Storyboard','desc':'Crafting viral hooks for each platform.'},{'title':'Production & Filming','desc':'Creating authentic UGC content.'},{'title':'AI-Enhanced Editing','desc':'Editing with AI tools for algorithm optimization.'},{'title':'Review & Optimization','desc':'Data-driven refinements for maximum performance.'},{'title':'Delivery & Analytics','desc':'Performance tracking to measure real business impact.'}]
                },
                'marquee': {
                    'items_top': ['AI Content Strategy','UGC Production','Motion Design','Brand Storytelling','AI Automation'],
                    'items_bottom': ['ChatGPT & Gemini Expert','Short-Form Video Editor','Content Strategist','SaaS Builder','Creative Director'],
                    'separator_top': '✦',
                    'separator_bottom': '◆'
                }
            }
            for key, data in SECTIONS.items():
                if needs_migration:
                    conn.execute("INSERT OR REPLACE INTO homepage_sections (section_key, content, is_active) VALUES (?, ?, 1)", (key, json.dumps(data)))
                else:
                    conn.execute("INSERT INTO homepage_sections (section_key, content, is_active) VALUES (?, ?, 1)", (key, json.dumps(data)))
            conn.commit()
            action = 'Migrated' if needs_migration else 'Seeded'
            print(f'{action} {len(SECTIONS)} homepage sections')
        conn.close()
    except Exception as e:
        print(f'Seed sections: {e}')

if __name__ == '__main__':
    init_db()
    seed_default_sections()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
