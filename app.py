import os
from flask import Flask, render_template

# 'templates' klasörünü Flask'a manuel olarak tanıtıyoruz
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Bu komut, 'templates/index.html' dosyasını arar
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ANA SAYFAYI GÖSTEREN KISIM
@app.route('/')
def index():
    return render_template('index.html')

# API ROTALARI (Sitenin verileri buradan çekecek)
@app.route('/api/user')
def get_user():
    return jsonify({
        "username": "Geliştirici",
        "credits": 0,
        "avatar": "https://ui-avatars.com/api/?name=User",
        "role": "Kullanıcı",
        "bio": "Yeni başlayan",
        "uploaded_projects": [],
        "purchased_projects": []
    })

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codetrade.db'
db = SQLAlchemy(app)

# Kullanıcı veritabanı yapısı
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    credits = db.Column(db.Integer, default=10)

# Dosya veritabanı yapısı
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    owner_name = db.Column(db.String(80))
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    
    # Gelişmiş Kurumsal Kullanıcı Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT, real_name TEXT, email TEXT, 
        credits INTEGER, avatar TEXT, role TEXT, bio TEXT, join_date TEXT)''')
    
    # Detaylandırılmış Endüstriyel Dosya Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY, title TEXT, description TEXT, category TEXT, 
        subcategory TEXT, file_type TEXT, uploader_id INTEGER, cost INTEGER, 
        downloads INTEGER, simulated_structure TEXT)''')
    
    # Satın Alma Geçmişi
    c.execute('''CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY, user_id INTEGER, file_id INTEGER, purchase_date TEXT)''')
    
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        # Varsayılan Master Profil (Senin Profilin)
        c.execute('''INSERT INTO users (username, real_name, email, credits, avatar, role, bio, join_date) 
            VALUES ("Bilal", "Bilal Geliştirici", "bilal@codeswap.io", 30, 
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80", 
            "Platform Architect", "Sistem mimarı ve Full-Stack geliştirici. Temiz kod hayranı.", "Haziran 2026")''')
        
        # Diğer simüle kullanıcıları ekleyelim ki kredi akışı test edilebilsin
        c.execute('''INSERT INTO users (username, real_name, email, credits, avatar, role, bio, join_date) 
            VALUES ("AhmetEren", "Ahmet Eren", "ahmet@codeswap.io", 10, "https://ui-avatars.com/api/?name=AE", "Developer", "CodeTrade üyesi", "2026")''')

        # Başlangıç Premium Projeleri (Farklı Kullanıcılardan)
        c.execute('''INSERT INTO files (title, description, category, subcategory, file_type, uploader_id, cost, downloads, simulated_structure) 
            VALUES ("Gelişmiş Ağ Topolojisi Sunumu", "Cisco Packet Tracer ortamında tasarlanmış, tüm router konfigürasyonlarını içeren 9. Sınıf dönem projesi.", "Sunum", "Ağ Teknolojileri", "PPTX", 2, 5, 14, "sunum.pptx")''')
        c.execute('''INSERT INTO files (title, description, category, subcategory, file_type, uploader_id, cost, downloads, simulated_structure) 
            VALUES ("Python Hata Yakalama Kütüphanesi", "BTT ve Programlama Temelleri dersi için hazırlanmış, özel hata loglama mekanizması.", "Yazılım Geliştirme", "Veri Bilimi & AI", "PY", 2, 4, 8, "logger.py")''')
            
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Kullanıcı Verisi Getirme (İlişkisel Veritabanı Sorguları İle)
@app.route('/api/user')
def get_user():
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    c.execute('SELECT username, real_name, email, credits, avatar, role, bio, join_date FROM users WHERE id=1')
    u = c.fetchone()
    
    # Kullanıcının paylaştığı ve başkalarının indirdiği dosyalar
    c.execute('SELECT id, title, cost, downloads FROM files WHERE uploader_id=1')
    uploaded = [{"id": r[0], "title": r[1], "cost": r[2], "downloads": r[3]} for r in c.fetchall()]
    
    # Satın alınan kütüphane
    c.execute('''SELECT f.id, f.title, f.file_type FROM purchases p 
                 JOIN files f ON p.file_id = f.id WHERE p.user_id=1''')
    purchased = [{"id": r[0], "title": r[1], "file_type": r[2]} for r in c.fetchall()]
    
    conn.close()
    return jsonify({
        "username": u[0], "real_name": u[1], "email": u[2], "credits": u[3], "avatar": u[4], 
        "role": u[5], "bio": u[6], "join_date": u[7], "uploaded_projects": uploaded, "purchased_projects": purchased
    })

# Profil Güncelleme API'si (Sıfır Hata Güvencesi)
@app.route('/api/user/update', methods=['POST'])
def update_user():
    data = request.json
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET username=?, real_name=?, bio=?, avatar=? WHERE id=1''',
              (data['username'], data['real_name'], data['bio'], data['avatar']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Profil matrixi başarıyla güncellendi."})

# Pazar Yeri Filtreleme Motoru
@app.route('/api/files')
def get_files():
    category = request.args.get('category', '')
    subcategory = request.args.get('subcategory', '')
    search = request.args.get('search', '').lower()
    
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    query = 'SELECT id, title, description, category, subcategory, file_type, cost, downloads FROM files WHERE 1=1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    if subcategory:
        query += ' AND subcategory = ?'
        params.append(subcategory)
    if search:
        query += ' AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)'
        params.append(f'%{search}%')
        params.append(f'%{search}%')
        
    query += ' ORDER BY id DESC'
    c.execute(query, params)
    files = [{"id": r[0], "title": r[1], "description": r[2], "category": r[3], 
              "subcategory": r[4], "file_type": r[5], "cost": r[6], "downloads": r[7]} for r in c.fetchall()]
    conn.close()
    return jsonify(files)

# Gelişmiş Proje Yayınlama Sistemi
@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    # Kredi eklemiyoruz! Sadece havuzda yayınlıyoruz.
    c.execute('''INSERT INTO files (title, description, category, subcategory, file_type, uploader_id, cost, downloads, simulated_structure) 
        VALUES (?, ?, ?, ?, ?, 1, ?, 0, ?)''', 
        (data['title'], data['description'], data['category'], data['subcategory'], data['file_type'], int(data['cost']), data['structure']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Projeniz global havuzda listelendi. Biri indirdiğinde kredi kazanacaksınız!"})

# P2P Kredi Akışlı İndirme Sistemi (Muazzam Güvenli)
@app.route('/api/download', methods=['POST'])
def download():
    file_id = request.json.get('file_id')
    conn = sqlite3.connect('codeswap.db')
    c = conn.cursor()
    
    # Alıcının kredisini al
    c.execute('SELECT credits FROM users WHERE id=1')
    buyer_credits = c.fetchone()[0]
    
    # Dosya bilgilerini ve yükleyicisini al
    c.execute('SELECT cost, uploader_id, title FROM files WHERE id=?', (file_id,))
    file_data = c.fetchone()
    
    if not file_data:
        conn.close()
        return jsonify({"success": False, "message": "Kaynak matriste bulunamadı."})
        
    cost, uploader_id, title = file_data
    
    if uploader_id == 1:
        conn.close()
        return jsonify({"success": False, "message": "Kendi yüklediğiniz projeden lisans alamazsınız."})
        
    if buyer_credits >= cost:
        # Alıcıdan kredi düş
        c.execute('UPDATE users SET credits = credits - ? WHERE id=1', (cost,))
        # Yükleyiciye (Satıcıya) kredi aktar (İstediğin P2P Sistem!)
        c.execute('UPDATE users SET credits = credits + ? WHERE id=?', (cost, uploader_id))
        # İndirme sayısını artır
        c.execute('UPDATE files SET downloads = downloads + 1 WHERE id=?', (file_id,))
        # Geçmişe ekle
        c.execute('INSERT INTO purchases (user_id, file_id, purchase_date) VALUES (1, ?, "Bugün")', (file_id,))
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"'{title}' başarıyla lisanslandı. {cost} CR aktarıldı."})
        
    conn.close()
    return jsonify({"success": False, "message": "Yetersiz kredi düzeyi. Havuza proje kazandırarak kredi biriktirin."})

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask, render_template

app = Flask(__name__)

# Bu kısım sitenin ana sayfası (kapısı)
@app.route('/')
def ana_sayfa():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
@app.route('/api/user')
def get_user():
    return jsonify({
        "username": "Bilal", 
        "credits": 50, 
        "avatar": "https://i.pravatar.cc/150",
        "role": "Admin",
        "bio": "Kod mimarı",
        "uploaded_projects": [{"title": "Test Projesi", "downloads": 5}],
        "purchased_projects": []
    })