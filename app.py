import sqlite3
import json
import datetime
import os
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import hashlib

SECRET_KEY = 'smps_super_secret_key_2026'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)  # Enable CORS for all routes

# Serve any static file (HTML, CSS, JS, assets) from the project root
@app.route('/')
def serve_index():
    from flask import send_from_directory
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    from flask import redirect, send_from_directory
    from urllib.parse import unquote

    # Don't intercept API routes
    if path.startswith('api/'):
        from flask import abort
        abort(404)

    # Decode any %20 etc. in the path
    decoded_path = unquote(path)

    # Detect old Live Server URLs which embed the full filesystem path
    # e.g. UPDATESMPSWEB/MAIN SMPS ROOT new/MAIN SMPS ROOT/admin/admin.html
    # We look for the project root marker and extract everything after it
    for marker in ['MAIN SMPS ROOT/', 'MAIN%20SMPS%20ROOT/']:
        if marker in path or marker in decoded_path:
            # Get the relative path after the marker
            check = decoded_path if marker == 'MAIN SMPS ROOT/' else path
            relative = check.split(marker)[-1]
            relative = unquote(relative)  # ensure decoded
            return redirect('/' + relative, code=302)

    # Try exact file match in BASE_DIR
    full_path = os.path.join(BASE_DIR, decoded_path)
    if os.path.isfile(full_path):
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename)

    # Try just the basename (last segment of the path)
    basename = os.path.basename(decoded_path)
    if basename:
        for dirpath, dirnames, filenames in os.walk(BASE_DIR):
            if basename in filenames:
                return send_from_directory(dirpath, basename)

    # Final fallback: serve index.html
    return send_from_directory(BASE_DIR, 'index.html')

# Custom 404 handler — catches old Live Server URLs like:
# /UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/admin/admin.html
# which Werkzeug rejects before routing. We redirect them to the correct short URL.
@app.errorhandler(404)
def not_found(e):
    from flask import redirect, request, send_from_directory
    from urllib.parse import unquote

    raw = request.path  # e.g. /UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/admin/admin.html
    decoded = unquote(raw)

    # Check for the project root marker (space or encoded)
    for marker in ['MAIN SMPS ROOT/', 'MAIN%20SMPS%20ROOT/']:
        if marker in decoded or marker in raw:
            relative = decoded.split('MAIN SMPS ROOT/')[-1]
            relative = unquote(relative)
            if relative:
                return redirect('/' + relative, code=302)

    # If no marker, just try to serve the basename from anywhere in the project
    basename = os.path.basename(decoded)
    if basename and '.' in basename:
        for dirpath, dirnames, filenames in os.walk(BASE_DIR):
            if basename in filenames:
                return send_from_directory(dirpath, basename)

    # Last resort: home page
    return send_from_directory(BASE_DIR, 'index.html')

DB_FILE = os.path.join(BASE_DIR, 'smps.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            lname TEXT,
            email TEXT,
            phone TEXT,
            org TEXT,
            inquiryType TEXT,
            subject TEXT,
            msg TEXT,
            date TEXT,
            read INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tag TEXT,
            status TEXT,
            icon TEXT,
            img TEXT,
            imgClass TEXT,
            tagClass TEXT,
            tagLabel TEXT,
            desc TEXT,
            fullDesc TEXT,
            features TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS execom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            type TEXT,
            initials TEXT,
            img TEXT,
            expertise TEXT,
            bio TEXT,
            quote TEXT,
            achievements TEXT,
            linkedin TEXT,
            email TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            date TEXT,
            month TEXT,
            day TEXT,
            location TEXT,
            img TEXT,
            desc TEXT,
            fullDesc TEXT,
            speakers TEXT,
            agenda TEXT,
            prerequisites TEXT,
            seats TEXT,
            is_featured INTEGER DEFAULT 0
        )
    ''')
    try:
        c.execute("ALTER TABLE events ADD COLUMN is_featured INTEGER DEFAULT 0")
    except Exception:
        pass

    try:
        c.execute("ALTER TABLE products ADD COLUMN img TEXT")
    except Exception:
        pass

    c.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            desc TEXT,
            img TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            typeLabel TEXT,
            year TEXT,
            title TEXT,
            desc TEXT,
            tags TEXT,
            status TEXT,
            statusLabel TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icon TEXT,
            title TEXT,
            desc TEXT,
            year TEXT,
            journal TEXT,
            impactFactor TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS licensing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icon TEXT,
            title TEXT,
            desc TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS ip_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS site_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            lname TEXT,
            email TEXT,
            org TEXT,
            type TEXT,
            msg TEXT,
            date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            type TEXT,
            dept TEXT,
            loc TEXT,
            status TEXT DEFAULT 'open',
            description TEXT,
            requirements TEXT,
            posted_date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            subscribed_date TEXT
        )
    ''')



    # Default admin user (password: smps2026)
    default_pw_hash = hashlib.sha256('smps2026'.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', ('admin', default_pw_hash, 'superadmin'))
    except sqlite3.IntegrityError:
        pass # Admin already exists
        
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- Middleware ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
                
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except Exception:
            return jsonify({'error': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# --- File Upload Route ---
@app.route('/api/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if the file is allowed
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'}), 400

    # Create uploads directory inside assets
    uploads_dir = os.path.join(BASE_DIR, 'assets', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    import uuid
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(uploads_dir, safe_filename)
    file.save(filepath)
    url = f"/assets/uploads/{safe_filename}"
    return jsonify({'success': True, 'url': url})

# --- Auth Routes ---
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Could not verify'}), 401

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (data.get('username'),)).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    pw_hash = hashlib.sha256(data.get('password').encode()).hexdigest()
    
    if pw_hash == user['password_hash']:
        token = jwt.encode({
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({'token': token, 'username': user['username']})

    return jsonify({'error': 'Invalid credentials'}), 401

# --- Messages Routes ---
@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json(silent=True) or {}
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (fname, lname, email, phone, org, inquiryType, subject, msg, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('fname', ''), data.get('lname', ''), data.get('email', ''), 
        data.get('phone', ''), data.get('org', ''), data.get('inquiryType', 'General'), 
        data.get('subject', ''), data.get('msg', ''), now
    ))
    conn.commit()
    msg_id = c.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'id': msg_id, 'message': 'Message sent'}), 201


@app.route('/api/contacts', methods=['POST'])
def contacts_create():
    # Compatibility endpoint for frontend contact form (contact.html)
    data = request.get_json(silent=True) or {}
    # contact form sends { name, email, subject, message, date }
    name = data.get('name', '')
    fname = name.split(' ', 1)[0] if name else data.get('fname', '')
    lname = name.split(' ', 1)[1] if (name and ' ' in name) else data.get('lname', '')
    msg_text = data.get('message') or data.get('msg') or ''
    now = data.get('date') or (datetime.datetime.utcnow().isoformat() + 'Z')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (fname, lname, email, phone, org, inquiryType, subject, msg, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        fname, lname, data.get('email', ''), data.get('phone', ''), data.get('org', ''), data.get('inquiryType', 'General'),
        data.get('subject', ''), msg_text, now
    ))
    conn.commit()
    msg_id = c.lastrowid
    conn.close()

    return jsonify({'success': True, 'id': msg_id, 'message': 'Contact saved'}), 201


@app.route('/api/contacts', methods=['GET'])
def contacts_list():
    # Public compatibility endpoint to read contact submissions (useful for local admin UI)
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(m) for m in messages])

@app.route('/api/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(m) for m in messages])

@app.route('/api/messages/<int:id>/read', methods=['PUT'])
@token_required
def mark_message_read(current_user, id):
    conn = get_db_connection()
    conn.execute('UPDATE messages SET read = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/messages/<int:id>', methods=['DELETE'])
@token_required
def delete_message(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Proposals Routes ---
@app.route('/api/proposals', methods=['POST'])
def create_proposal():
    data = request.get_json(silent=True) or {}
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO proposals (fname, lname, email, org, type, msg, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('fname', ''), data.get('lname', ''), data.get('email', ''), 
        data.get('org', ''), data.get('type', ''), data.get('msg', ''), now
    ))
    conn.commit()
    prop_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': prop_id}), 201

@app.route('/api/proposals', methods=['GET'])
@token_required
def get_proposals(current_user):
    conn = get_db_connection()
    proposals = conn.execute('SELECT * FROM proposals ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(p) for p in proposals])

@app.route('/api/proposals/<int:id>', methods=['DELETE'])
@token_required
def delete_proposal(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM proposals WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/proposals', methods=['DELETE'])
@token_required
def clear_all_proposals(current_user):
    conn = get_db_connection()
    conn.execute('DELETE FROM proposals')
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Products Helpers & Image Resolver ---
def resolve_og_image(url):
    if not url or not url.startswith(('http://', 'https://')):
        return url
    
    # If it already looks like a direct image URL, return it
    lower_url = url.lower()
    if any(lower_url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']):
        return url
        
    try:
        import urllib.request
        import ssl
        import re
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        )
        with urllib.request.urlopen(req, timeout=3, context=ctx) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                return url
            
            html = response.read().decode('utf-8', errors='ignore')
            
            # Match og:image or twitter:image
            match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html)
            if not match:
                match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image["\']', html)
            if not match:
                match = re.search(r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', html)
            if not match:
                match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']twitter:image["\']', html)
                
            if match:
                resolved_url = match.group(1)
                # Ensure resolved url is absolute
                if resolved_url.startswith('//'):
                    resolved_url = 'https:' + resolved_url
                elif resolved_url.startswith('/'):
                    from urllib.parse import urljoin
                    resolved_url = urljoin(url, resolved_url)
                print(f"[Resolve Image] Resolved {url} -> {resolved_url}")
                return resolved_url
    except Exception as e:
        print(f"[Resolve Image] Error resolving {url}: {e}")
        
    return url

# --- Products Routes ---
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    
    result = []
    for p in products:
        d = dict(p)
        try:
            d['features'] = json.loads(d['features']) if d['features'] else []
        except:
            d['features'] = []
        result.append(d)
        
    return jsonify(result)

@app.route('/api/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO products (name, tag, status, icon, img, imgClass, tagClass, tagLabel, desc, fullDesc, features)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), data.get('tag'), data.get('status'), data.get('icon'),
        resolved_img, data.get('imgClass'), data.get('tagClass'), data.get('tagLabel'), 
        data.get('desc'), data.get('fullDesc'), json.dumps(data.get('features', []))
    ))
    conn.commit()
    prod_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': prod_id}), 201

@app.route('/api/products/<int:id>', methods=['PUT'])
@token_required
def update_product(current_user, id):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE products SET 
            name = ?, tag = ?, status = ?, icon = ?, img = ?, imgClass = ?, tagClass = ?, 
            tagLabel = ?, desc = ?, fullDesc = ?, features = ?
        WHERE id = ?
    ''', (
        data.get('name'), data.get('tag'), data.get('status'), data.get('icon'),
        resolved_img, data.get('imgClass'), data.get('tagClass'), data.get('tagLabel'), 
        data.get('desc'), data.get('fullDesc'), json.dumps(data.get('features', [])), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/resolve-image', methods=['GET'])
def resolve_image_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    resolved = resolve_og_image(url)
    return jsonify({'resolved': resolved})


# --- Execom Routes ---
@app.route('/api/execom', methods=['GET'])
def get_execom():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM execom ORDER BY id ASC').fetchall()
    conn.close()
    
    result = []
    for m in members:
        d = dict(m)
        try:
            d['achievements'] = json.loads(d['achievements']) if d['achievements'] else []
        except:
            d['achievements'] = []
        result.append(d)
    return jsonify(result)

@app.route('/api/execom', methods=['POST'])
@token_required
def create_execom(current_user):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO execom (name, role, type, initials, img, expertise, bio, quote, achievements, linkedin, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), data.get('role'), data.get('type'), data.get('initials'),
        resolved_img, data.get('expertise'), data.get('bio'), data.get('quote'),
        json.dumps(data.get('achievements', [])), data.get('linkedin'), data.get('email')
    ))
    conn.commit()
    member_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': member_id}), 201

@app.route('/api/execom/<int:id>', methods=['PUT'])
@token_required
def update_execom(current_user, id):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE execom SET 
            name = ?, role = ?, type = ?, initials = ?, img = ?, expertise = ?, 
            bio = ?, quote = ?, achievements = ?, linkedin = ?, email = ?
        WHERE id = ?
    ''', (
        data.get('name'), data.get('role'), data.get('type'), data.get('initials'),
        resolved_img, data.get('expertise'), data.get('bio'), data.get('quote'),
        json.dumps(data.get('achievements', [])), data.get('linkedin'), data.get('email'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/execom/<int:id>', methods=['DELETE'])
@token_required
def delete_execom(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM execom WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Events Routes ---
@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY id ASC').fetchall()
    conn.close()
    
    result = []
    for e in events:
        d = dict(e)
        try:
            d['speakers'] = json.loads(d['speakers']) if d['speakers'] else []
        except:
            d['speakers'] = []
        result.append(d)
    return jsonify(result)

@app.route('/api/events', methods=['POST'])
@token_required
def create_event(current_user):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    c = conn.cursor()
    is_featured = 1 if data.get('is_featured') else 0
    if is_featured == 1:
        c.execute('UPDATE events SET is_featured = 0')
    c.execute('''
        INSERT INTO events (name, type, date, month, day, location, img, desc, fullDesc, speakers, agenda, prerequisites, seats, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), data.get('type'), data.get('date'), data.get('month'),
        data.get('day'), data.get('location'), resolved_img, data.get('desc'),
        data.get('fullDesc'), json.dumps(data.get('speakers', [])), data.get('agenda'),
        data.get('prerequisites'), data.get('seats'), is_featured
    ))
    conn.commit()
    event_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': event_id}), 201

@app.route('/api/events/<int:id>', methods=['PUT'])
@token_required
def update_event(current_user, id):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    is_featured = 1 if data.get('is_featured') else 0
    if is_featured == 1:
        conn.execute('UPDATE events SET is_featured = 0')
    conn.execute('''
        UPDATE events SET 
            name = ?, type = ?, date = ?, month = ?, day = ?, location = ?, 
            img = ?, desc = ?, fullDesc = ?, speakers = ?, agenda = ?, prerequisites = ?, seats = ?, is_featured = ?
        WHERE id = ?
    ''', (
        data.get('name'), data.get('type'), data.get('date'), data.get('month'),
        data.get('day'), data.get('location'), resolved_img, data.get('desc'),
        data.get('fullDesc'), json.dumps(data.get('speakers', [])), data.get('agenda'),
        data.get('prerequisites'), data.get('seats'), is_featured, id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/events/<int:id>', methods=['DELETE'])
@token_required
def delete_event(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Gallery Routes ---
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    conn = get_db_connection()
    gallery = conn.execute('SELECT * FROM gallery ORDER BY id ASC').fetchall()
    conn.close()
    return jsonify([dict(g) for g in gallery])

@app.route('/api/gallery', methods=['POST'])
@token_required
def create_gallery(current_user):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO gallery (category, title, desc, img)
        VALUES (?, ?, ?, ?)
    ''', (
        data.get('category'), data.get('title'), data.get('desc'), resolved_img
    ))
    conn.commit()
    gallery_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': gallery_id}), 201

@app.route('/api/gallery/<int:id>', methods=['PUT'])
@token_required
def update_gallery(current_user, id):
    data = request.get_json(silent=True) or {}
    img_url = data.get('img') or ''
    resolved_img = resolve_og_image(img_url)
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE gallery SET 
            category = ?, title = ?, desc = ?, img = ?
        WHERE id = ?
    ''', (
        data.get('category'), data.get('title'), data.get('desc'), resolved_img, id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/gallery/<int:id>', methods=['DELETE'])
@token_required
def delete_gallery(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM gallery WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Patents Routes ---
@app.route('/api/patents', methods=['GET'])
def get_patents():
    conn = get_db_connection()
    patents = conn.execute('SELECT * FROM patents ORDER BY id DESC').fetchall()
    conn.close()
    
    result = []
    for p in patents:
        d = dict(p)
        try:
            d['tags'] = json.loads(d['tags']) if d['tags'] else []
        except:
            d['tags'] = []
        result.append(d)
    return jsonify(result)

@app.route('/api/patents', methods=['POST'])
@token_required
def create_patent(current_user):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO patents (type, typeLabel, year, title, desc, tags, status, statusLabel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('type'), data.get('typeLabel'), data.get('year'), data.get('title'),
        data.get('desc'), json.dumps(data.get('tags', [])), data.get('status'), data.get('statusLabel')
    ))
    conn.commit()
    patent_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': patent_id}), 201

@app.route('/api/patents/<int:id>', methods=['PUT'])
@token_required
def update_patent(current_user, id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    conn.execute('''
        UPDATE patents SET 
            type = ?, typeLabel = ?, year = ?, title = ?, desc = ?, tags = ?, status = ?, statusLabel = ?
        WHERE id = ?
    ''', (
        data.get('type'), data.get('typeLabel'), data.get('year'), data.get('title'),
        data.get('desc'), json.dumps(data.get('tags', [])), data.get('status'), data.get('statusLabel'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/patents/<int:id>', methods=['DELETE'])
@token_required
def delete_patent(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM patents WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Research Routes ---
@app.route('/api/research', methods=['GET'])
def get_research():
    conn = get_db_connection()
    research = conn.execute('SELECT * FROM research ORDER BY id ASC').fetchall()
    conn.close()
    return jsonify([dict(r) for r in research])

@app.route('/api/research', methods=['POST'])
@token_required
def create_research(current_user):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO research (icon, title, desc, year, journal, impactFactor)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('icon'), data.get('title'), data.get('desc'), data.get('year'),
        data.get('journal'), data.get('impactFactor')
    ))
    conn.commit()
    res_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': res_id}), 201

@app.route('/api/research/<int:id>', methods=['PUT'])
@token_required
def update_research(current_user, id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    conn.execute('''
        UPDATE research SET 
            icon = ?, title = ?, desc = ?, year = ?, journal = ?, impactFactor = ?
        WHERE id = ?
    ''', (
        data.get('icon'), data.get('title'), data.get('desc'), data.get('year'),
        data.get('journal'), data.get('impactFactor'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/research/<int:id>', methods=['DELETE'])
@token_required
def delete_research(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM research WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Licensing / Collaborative Models Routes ---
@app.route('/api/licensing', methods=['GET'])
def get_licensing():
    conn = get_db_connection()
    licensing = conn.execute('SELECT * FROM licensing ORDER BY id ASC').fetchall()
    conn.close()
    return jsonify([dict(l) for l in licensing])

@app.route('/api/licensing', methods=['POST'])
@token_required
def create_licensing(current_user):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO licensing (icon, title, desc)
        VALUES (?, ?, ?)
    ''', (
        data.get('icon'), data.get('title'), data.get('desc')
    ))
    conn.commit()
    lic_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': lic_id}), 201

@app.route('/api/licensing/<int:id>', methods=['PUT'])
@token_required
def update_licensing(current_user, id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    conn.execute('''
        UPDATE licensing SET 
            icon = ?, title = ?, desc = ?
        WHERE id = ?
    ''', (
        data.get('icon'), data.get('title'), data.get('desc'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/licensing/<int:id>', methods=['DELETE'])
@token_required
def delete_licensing(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM licensing WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- IP Settings Routes ---
@app.route('/api/ip/settings', methods=['GET'])
def get_ip_settings():
    conn = get_db_connection()
    settings = conn.execute('SELECT * FROM ip_settings').fetchall()
    conn.close()
    return jsonify({row['key']: row['value'] for row in settings})

@app.route('/api/ip/settings', methods=['POST'])
@token_required
def save_ip_settings(current_user):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    c = conn.cursor()
    for key, value in data.items():
        c.execute('''
            INSERT INTO ip_settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        ''', (key, str(value)))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Site Settings Routes (About, Home, Collaborate Pages) ---
@app.route('/api/settings/<key>', methods=['GET'])
def get_site_settings(key):
    conn = get_db_connection()
    row = conn.execute('SELECT value FROM site_settings WHERE key = ?', (key,)).fetchone()
    conn.close()
    if row:
        val = row['value']
        try:
            return jsonify(json.loads(val))
        except Exception:
            return jsonify(val)
    return jsonify({})

@app.route('/api/settings/<key>', methods=['POST'])
@token_required
def save_site_settings(current_user, key):
    data = request.get_json(silent=True) or {}
    val_str = json.dumps(data)
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO site_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (key, val_str))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Jobs / Careers Routes ---
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs ORDER BY id DESC').fetchall()
    conn.close()
    result = []
    for j in jobs:
        d = dict(j)
        try:
            d['requirements'] = json.loads(d['requirements']) if d['requirements'] else []
        except:
            d['requirements'] = []
        result.append(d)
    return jsonify(result)

@app.route('/api/jobs', methods=['POST'])
@token_required
def create_job(current_user):
    data = request.get_json(silent=True) or {}
    reqs = data.get('requirements', [])
    if isinstance(reqs, list):
        reqs = json.dumps(reqs)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO jobs (title, type, dept, loc, status, description, requirements, posted_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'), data.get('type', 'Full-time'),
        data.get('dept'), data.get('loc'),
        data.get('status', 'open'),
        data.get('desc') or data.get('description'),
        reqs,
        datetime.datetime.utcnow().strftime('%Y-%m-%d')
    ))
    conn.commit()
    job_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': job_id}), 201

@app.route('/api/jobs/<int:id>', methods=['PUT'])
@token_required
def update_job(current_user, id):
    data = request.get_json(silent=True) or {}
    reqs = data.get('requirements', [])
    if isinstance(reqs, list):
        reqs = json.dumps(reqs)
    conn = get_db_connection()
    conn.execute('''
        UPDATE jobs SET title=?, type=?, dept=?, loc=?, status=?, description=?, requirements=?
        WHERE id=?
    ''', (
        data.get('title'), data.get('type', 'Full-time'),
        data.get('dept'), data.get('loc'),
        data.get('status', 'open'),
        data.get('desc') or data.get('description'),
        reqs, id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/jobs/<int:id>', methods=['DELETE'])
@token_required
def delete_job(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM jobs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Newsletter Subscriber Routes ---
@app.route('/api/newsletter-subscribe', methods=['POST'])
def newsletter_subscribe():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    if not email or '@' not in email:
        return jsonify({'error': 'Valid email required'}), 400
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT OR IGNORE INTO newsletter_subscribers (email, subscribed_date) VALUES (?, ?)',
            (email, datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    conn.close()
    return jsonify({'success': True})

@app.route('/api/newsletter-subscribers', methods=['GET'])
@token_required
def get_newsletter_subscribers(current_user):
    conn = get_db_connection()
    subs = conn.execute('SELECT * FROM newsletter_subscribers ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(s) for s in subs])

@app.route('/api/newsletter-subscribers/<int:id>', methods=['DELETE'])
@token_required
def delete_newsletter_subscriber(current_user, id):
    conn = get_db_connection()
    conn.execute('DELETE FROM newsletter_subscribers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/newsletter-subscribers', methods=['DELETE'])
@token_required
def clear_all_subscribers(current_user):
    conn = get_db_connection()
    conn.execute('DELETE FROM newsletter_subscribers')
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', '5002'))
    print(f"Starting SMPS Tech Lab Backend on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)

