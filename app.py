import os, json, uuid, re, hashlib, smtplib, csv, io, time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory, abort, flash
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
    return render_template('index.html',
                         portfolio=portfolio_items,
                         testimonials=testimonials,
                         services=services,
                         settings=settings)

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
        send_email(data.get('email'), f'Thank you for reaching out — Siam Munkasir', confirm_html)
        
        # Send notification to admin
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
            send_email(notif_admin_email, f'New Inquiry #{inquiry_id} — {sanitize(data.get("full_name",""))}', notif_html)
        
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
        recent = db.execute("SELECT id, full_name, email, project_type, status, created_at FROM inquiries ORDER BY created_at DESC LIMIT 10").fetchall()
    return render_template('admin/dashboard.html', new_inquiries=new_inquiries, total_inquiries=total_inquiries,
                         total_portfolio=total_portfolio, total_testimonials=total_testimonials,
                         total_reviews=total_reviews, total_faqs=total_faqs, total_skills=total_skills, recent=recent)

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
        db.execute('''INSERT INTO services (title, description, icon, price, features)
                    VALUES (?,?,?,?,?)''', (
            data.get('title',''), data.get('description',''), data.get('icon',''),
            data.get('price',''), data.get('features','')
        ))
    return redirect(url_for('admin_services'))

@app.route('/admin/services/<int:id>/delete', methods=['POST'])
@admin_required
def admin_services_delete(id):
    with get_db() as db:
        db.execute("DELETE FROM services WHERE id=?", (id,))
    return jsonify({'success': True})

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

# ─── Initialize database on import ───
with app.app_context():
    init_db()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
