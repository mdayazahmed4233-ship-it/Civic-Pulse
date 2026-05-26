"""
CivicPulse v2.0 — Smart Civic Complaint Management System
Combined Flask Server: Serves the frontend AND provides the REST API.

Run:  python app.py
Open: http://localhost:5000
"""

import os
import uuid
import random
import string
import threading
import webbrowser
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ── App Setup ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

app.config['SECRET_KEY']              = os.environ.get('SECRET_KEY', 'civic-pulse-secret-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///civicpulse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']          = os.environ.get('JWT_SECRET', 'jwt-civic-secret-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES']= timedelta(hours=24)
app.config['UPLOAD_FOLDER']           = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH']      = 16 * 1024 * 1024  # 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

CORS(app)
db  = SQLAlchemy(app)
jwt = JWTManager(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ── Serve Frontend ───────────────────────────────────────────────────
@app.route('/')
def index():
    """Serve the main React SPA."""
    return send_file(os.path.join(BASE_DIR, 'index.html'))

@app.route('/locations.js')
def serve_locations():
    """Serve the Telangana location data JS file."""
    return send_file(os.path.join(BASE_DIR, 'locations.js'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ── Models ───────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    phone      = db.Column(db.String(20))
    role       = db.Column(db.String(20), default='citizen')   # citizen | admin
    district   = db.Column(db.String(100))
    mandal     = db.Column(db.String(100))
    state      = db.Column(db.String(100))
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    complaints = db.relationship('Complaint', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email,
            'phone': self.phone, 'role': self.role,
            'district': self.district, 'mandal': self.mandal,
            'state': self.state, 'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }


class Department(db.Model):
    __tablename__ = 'departments'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50))
    district = db.Column(db.String(100))
    state    = db.Column(db.String(100))
    head     = db.Column(db.String(120))
    email    = db.Column(db.String(200))
    phone    = db.Column(db.String(20))

    def to_dict(self):
        return {k: getattr(self, k) for k in
                ('id', 'name', 'category', 'district', 'state', 'head', 'email', 'phone')}


class Officer(db.Model):
    __tablename__ = 'officers'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department    = db.relationship('Department', backref='officers')
    email         = db.Column(db.String(200))
    phone         = db.Column(db.String(20))
    district      = db.Column(db.String(100))
    mandal        = db.Column(db.String(100))
    is_active     = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name,
            'department': self.department.name if self.department else None,
            'department_id': self.department_id,
            'email': self.email, 'phone': self.phone,
            'district': self.district, 'mandal': self.mandal,
            'is_active': self.is_active,
        }


class Complaint(db.Model):
    __tablename__ = 'complaints'
    id               = db.Column(db.String(20), primary_key=True)
    title            = db.Column(db.String(250), nullable=False)
    description      = db.Column(db.Text, nullable=False)
    category         = db.Column(db.String(50), nullable=False)
    state            = db.Column(db.String(100), nullable=False)
    district         = db.Column(db.String(100), nullable=False)
    mandal           = db.Column(db.String(150))
    area             = db.Column(db.String(150))
    latitude         = db.Column(db.Float)
    longitude        = db.Column(db.Float)
    status           = db.Column(db.String(30), default='Pending')
    priority         = db.Column(db.String(20), default='medium')
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_dept    = db.Column(db.String(150))
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('officers.id'), nullable=True)
    assigned_officer    = db.relationship('Officer', backref='complaints')
    images           = db.Column(db.Text)   # JSON list
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    remarks          = db.relationship('Remark', backref='complaint', cascade='all, delete-orphan')

    def to_dict(self):
        import json
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'category': self.category, 'state': self.state,
            'district': self.district, 'mandal': self.mandal, 'area': self.area,
            'latitude': self.latitude, 'longitude': self.longitude,
            'status': self.status, 'priority': self.priority,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_phone': self.user.phone if self.user else None,
            'assigned_dept': self.assigned_dept,
            'assigned_officer': self.assigned_officer.to_dict() if self.assigned_officer else None,
            'images': json.loads(self.images) if self.images else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'remarks': [r.to_dict() for r in self.remarks],
        }


class Remark(db.Model):
    __tablename__ = 'remarks'
    id           = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(20), db.ForeignKey('complaints.id'))
    text         = db.Column(db.Text, nullable=False)
    author_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    author       = db.relationship('User')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'text': self.text,
            'author': self.author.name if self.author else 'Unknown',
            'created_at': self.created_at.isoformat(),
        }


# ── Helpers ──────────────────────────────────────────────────────────
CATEGORY_DEPT_MAP = {
    'roads':       'PWD Department',
    'sanitation':  'GHMC / Municipal Corp',
    'water':       'HMWSSB (Water Board)',
    'electricity': 'TSSPDCL (Electricity)',
    'drainage':    'Drainage Department',
    'parks':       'Parks & Recreation',
    'noise':       'Pollution Control Board',
    'buildings':   'GHMC Buildings Wing',
    'transport':   'TSRTC / Transport Dept',
    'other':       'Municipal Corporation',
}

URGENT_KEYWORDS = ['accident','dangerous','emergency','severe','critical',
                   'fire','flood','collapse','injury','urgent','fatal','death']


def generate_complaint_id():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'CMP-{suffix}'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request()
        uid  = int(get_jwt_identity())
        user = db.session.get(User, uid)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


# ── Telangana Location Data ───────────────────────────────────────────
TELANGANA = {
    "Adilabad": {
        "mandals": ["Adilabad Rural","Adilabad Urban","Bazarhatnoor","Bela","Bhainsa","Boath","Dilawarpur","Gudihatnoor","Ichoda","Indervelli","Jainath","Kaddam","Laxmanchanda","Manjrath","Mavala","Narnoor","Neradigonda","Tamsi","Utnoor"],
        "streets": {"Adilabad Urban":["Main Road","Collector Office Road","Gandhi Chowk","Railway Station Road","Bus Stand Area","Ashok Nagar","Ambedkar Colony"],"Bhainsa":["Bhainsa Main Road","Market Road","Old Town"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Bhadradri Kothagudem": {
        "mandals": ["Aswapuram","Bayyaram","Bhadrachalam","Burgampahad","Cherla","Dammapeta","Gundala","Julurpad","Kothagudem","Laxmidevipally","Manuguru","Mulkalapally","Palvancha","Pinapaka","Sujathanagar","Tekulapally","Thirumalayapalem","Yellandu"],
        "streets": {"Bhadrachalam":["Temple Road","Godavari Ghat Road","RTC Bus Stand Road","Old Town","Sitarampuram"],"Kothagudem":["Main Road","Singareni Colony","Power House Road","Civil Lines"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Hanamkonda": {
        "mandals": ["Elkathurthy","Geesugonda","Hanamkonda","Hasanparthy","Kamalapur","Parkal","Rayaparthy","Sangem","Shayampet","Velair","Wardhannapet"],
        "streets": {"Hanamkonda":["Hanamkonda Main Road","Mulugu Road","Nakkalagutta","Subedari","Chaitanyapuri","Vidyanagar","Station Road"],"Hasanparthy":["Hasanparthy Main Road","NH163","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Hyderabad": {
        "mandals": ["Amberpet","Asifnagar","Bandlaguda Jagir","Charminar","Golconda","Khairatabad","Musheerabad","Nampally","Secunderabad","Shaikpet","Tirumalgiri","Yakutpura"],
        "streets": {"Khairatabad":["Banjara Hills Rd No.1","Banjara Hills Rd No.12","Jubilee Hills Rd No.36","Panjagutta","Raj Bhavan Road","Somajiguda","Ameerpet"],"Secunderabad":["MG Road","SD Road","Paradise Circle","SP Road","James Street","Bowenpally","Maredpally"],"Charminar":["Charminar Road","Laad Bazaar","Pathar Gatti","Sultan Shahi","Shalibanda","Mir Alam Mandi"],"Golconda":["Golconda Fort Road","Toli Chowki","Karwan","Rethibowli","Falaknuma"],"Musheerabad":["Musheerabad Main Road","Kavadiguda","Narayanguda","Himayatnagar","Basheerbagh"],"Nampally":["Nampally Station Road","Abids","Gunfoundry","Liberty","Mozamjahi Market"],"default":["Main Road","Colony Road","Nagar","Hills Road"]}
    },
    "Jagtial": {
        "mandals": ["Buggaram","Dharmapuri","Gollapelly","Jagtial","Kathalapur","Kodimial","Koratla","Mallapur","Metpally","Pegadapally","Raikal","Sarangapur","Velgatoor"],
        "streets": {"Jagtial":["Main Road","Collector Office Road","Bus Stand Road","Civil Lines","Ambedkar Colony"],"Koratla":["Koratla Main Road","Market Road","NH163"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Jangaon": {
        "mandals": ["Bachannapet","Devaruppula","Ghanpur Station","Jangaon","Kodakandla","Lingalaghanpur","Narmetta","Palakurthi","Raghunathpally","Rayavaram","Regonda","Tarigoppula","Zaffergadh"],
        "streets": {"Jangaon":["Main Road","Bus Stand Area","RTC Colony","Bhuvanagiri Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Jayashankar Bhupalpally": {
        "mandals": ["Bhupalpally","Chityal","Eturunagaram","Ghanpur","Kataram","Mahadevpur","Malharrao","Mogullapally","Mulugu","Palimela","Regunta","Tadvai","Tekumatla","Venkatapur"],
        "streets": {"Bhupalpally":["Main Road","Bus Stand Road","Revenue Colony","Ambedkar Colony"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Jogulamba Gadwal": {
        "mandals": ["Alampur","Attoor","Dharur","Gadwal","Gattu","Goliyadoddi","Ieeja","Itikyal","Krishna","Lingal","Maldakal","Manopad","Waddepally"],
        "streets": {"Gadwal":["Gadwal Main Road","Market Road","Bus Stand Road","Old Town"],"Alampur":["Alampur Main Road","Temple Road","Colony Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Kamareddy": {
        "mandals": ["Banswada","Bheemgal","Bhiknoor","Domakonda","Ellareddy","Gandhari","Jakranpally","Kamareddy","Lingampet","Machareddy","Madnoor","Naspur","Pitlam","Ramareddy","Sadashivnagar","Sarangapur","Yellareddy"],
        "streets": {"Kamareddy":["Main Road","Bus Stand Road","Collector Office Road","Ambedkar Colony"],"Banswada":["Banswada Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Karimnagar": {
        "mandals": ["Choppadandi","Chigurumamidi","Elkathurthy","Gangadhara","Huzurabad","Jammikunta","Karimnagar Rural","Karimnagar Urban","Koheda","Manakondur","Manthani","Ramagundam","Saidapur","Shankarapatnam","Thimmapur","Veenavanka"],
        "streets": {"Karimnagar Urban":["Main Road","Collectorate Road","Jyothinagar","Godavarikhani Road","Ramagundam Road","SP Road","Civil Lines","Kakatiya Circle"],"Ramagundam":["Ramagundam Main Road","Power House Road","NTPC Colony","Old Town"],"Huzurabad":["Huzurabad Main Road","Market Road","Station Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Khammam": {
        "mandals": ["Aswaraopeta","Balapanur","Bonakal","Enkoor","Kamepalli","Khammam Rural","Khammam Urban","Konijerla","Kusumanchi","Madhira","Mudigonda","Nelakondapally","Sattupally","Singareni","Thallada","Wyra"],
        "streets": {"Khammam Urban":["Main Road","Wyra Road","Kothagudem Road","Balaji Nagar","Nehru Nagar","Bus Stand Area","Collectorate Road"],"Madhira":["Madhira Main Road","Market Road","NH163"],"Sattupally":["Sattupally Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Komaram Bheem Asifabad": {
        "mandals": ["Asifabad","Bejjur","Dahegaon","Jainath","Kaghaznagar","Kerameri","Koutala","Rebbena","Sirpur (T)","Sirpur (U)","Tiryani","Wankidi"],
        "streets": {"Asifabad":["Main Road","Bus Stand Road","Revenue Colony"],"Kaghaznagar":["Kaghaznagar Main Road","Paper Mill Road","Colony Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Mahabubabad": {
        "mandals": ["Bayyaram","Chintakani","Curruppagallu","Dornakal","Gudur","Kesamudram","Khanapur","Mahabubabad","Maripeda","Nellipaka","Nellikuduru","Narsimhulapet","Thorrur"],
        "streets": {"Mahabubabad":["Main Road","Bus Stand Road","Collector Office Road","Revenue Colony"],"Dornakal":["Dornakal Main Road","Station Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Mahabubnagar": {
        "mandals": ["Addakal","Balanagar","Bhoothpur","Devarkadra","Farooqnagar","Jadcherla","Koilkonda","Kosgi","Mahabubnagar Rural","Mahabubnagar Urban","Makthal","Midjil","Peddamandadi","Shadadnagar"],
        "streets": {"Mahabubnagar Urban":["Main Road","Collectorate Road","Bus Stand Road","Civil Lines","New Town","Jadcherla Road"],"Jadcherla":["Jadcherla Main Road","NH44","Industrial Area"],"Farooqnagar":["Farooqnagar Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Mancherial": {
        "mandals": ["Bellampalli","Bheemini","Chandrapur","Chennur","Dandepally","Hajipur","Jaipur","Luxettipet","Mancherial","Mandamarri","Naspur","Ramakrishnapur","Vemulawada"],
        "streets": {"Mancherial":["Main Road","Bus Stand Road","Bellarpur Road","Civil Lines"],"Bellampalli":["Bellampalli Main Road","Coal Mine Road","Revenue Colony"],"Mandamarri":["Mandamarri Main Road","Colony Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Medak": {
        "mandals": ["Alladurg","Andole","Chegunta","Dubbak","Gajwel","Havelighanpur","Jogipet","Kondapur","Medak","Narayankhed","Narsapur","Papannapet","Ramayampet","Shankarampet (A)","Shankarampet (R)","Tekmal","Toopran","Yeldurthy"],
        "streets": {"Medak":["Main Road","Cathedral Road","Bus Stand Area","Old Town","Revenue Colony"],"Gajwel":["Gajwel Main Road","NH161","Market Road"],"Toopran":["Toopran Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Medchal-Malkajgiri": {
        "mandals": ["Alwal","Balanagar","Bachupally","Bollaram","Dundigal-Gandimaisamma","Ghatkesar","Keesara","Kompally","Malkajgiri","Medchal","Quthbullapur","Suraram","Uppal"],
        "streets": {"Malkajgiri":["Malkajgiri Main Road","ECIL Road","Neredmet","Safilguda","Kushaiguda","Lothkunta"],"Kompally":["Kompally Main Road","Suchitra Circle","Pragati Nagar","JNTU Road"],"Uppal":["Uppal Main Road","Nagole Road","Habsiguda","Tarnaka","Mallapur"],"Ghatkesar":["Ghatkesar Main Road","LB Nagar Road","Boduppal","Pocharam"],"Alwal":["Alwal Main Road","Secunderabad Road","CRPF Colony"],"Bachupally":["Bachupally Main Road","Miyapur Road","Chandanagar"],"default":["Main Road","Colony Road","Nagar","Circle"]}
    },
    "Mulugu": {
        "mandals": ["Eturnagaram","Govindaraopet","Kannaigudem","Mangapet","Mulugu","Tadvai","Venkatapur","Wazeedu"],
        "streets": {"Mulugu":["Main Road","Bus Stand Road","Revenue Colony"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Nagarkurnool": {
        "mandals": ["Achampet","Amrabad","Bijnapally","Bijinapalle","Bhoothpur","Charakonda","Dhanwada","Kollapur","Kodair","Lingal","Maddur","Nagarkurnool","Peddakothapally","Tadoor","Telkapally","Uppununthala","Veldanda","Waddepally"],
        "streets": {"Nagarkurnool":["Main Road","Bus Stand Road","Collectorate Road","Revenue Colony"],"Achampet":["Achampet Main Road","Market Road"],"Kollapur":["Kollapur Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Nalgonda": {
        "mandals": ["Alair","Aler","Bhuvanagiri","Chandampet","Choutuppal","Devarakonda","Gattu","Huzurnagar","Miryalaguda","Munugodu","Nalgonda","Narayanapur","Nidamanur","Nereducharla","Ramannapet","Thipparthi","Tirumalagiri","Tungaturthy"],
        "streets": {"Nalgonda":["Main Road","Collectorate Road","Bus Stand Road","Civil Lines","Miryalaguda Road","Hyderabad Road"],"Miryalaguda":["Miryalaguda Main Road","Market Road","Station Road"],"Huzurnagar":["Huzurnagar Main Road","Suryapet Road","Market Area"],"Devarakonda":["Devarakonda Main Road","Fort Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Narayanpet": {
        "mandals": ["Kosgi","Maddur","Maganoor","Marikal","Narayanpet","Narva"],
        "streets": {"Narayanpet":["Main Road","Bus Stand Road","Revenue Colony","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Nirmal": {
        "mandals": ["Bhainsa","Dilawarpur","Gudihatnoor","Khanapur","Kubeer","Laxmanchanda","Lokeswaram","Mamada","Mudhole","Narsapur","Nirmal","Sarangapur","Tanoor","Utnoor"],
        "streets": {"Nirmal":["Main Road","Collectorate Road","Bus Stand Area","Revenue Colony"],"Bhainsa":["Bhainsa Main Road","Market Road","Old Town"],"Mudhole":["Mudhole Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Nizamabad": {
        "mandals": ["Armoor","Balkonda","Banswada","Bheemgal","Bodhan","Dichpally","Domakonda","Edapally","Enkoor","Jakranpally","Kotgiri","Lingampet","Madnoor","Mortad","Navipet","Nizamabad Rural","Nizamabad Urban","Pitlam","Yedpally","Yellareddy"],
        "streets": {"Nizamabad Urban":["Main Road","Collectorate Road","Station Road","Bodhan Road","Armoor Road","Civil Lines","Kumarpally"],"Bodhan":["Bodhan Main Road","Market Road","Sugar Factory Road"],"Armoor":["Armoor Main Road","Market Road","NH44"],"Dichpally":["Dichpally Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Peddapalli": {
        "mandals": ["Anthargaon","Dharmaram","Gorrepadu","Julapally","Kalwacherthyal","Kathlapur","Korutla","Manthani","Odela","Peddapalli","Ramagundam","Srirampur","Sultanabad"],
        "streets": {"Peddapalli":["Main Road","Bus Stand Road","Revenue Colony"],"Ramagundam":["Ramagundam Main Road","NTPC Colony","Power House Road","Station Road"],"Korutla":["Korutla Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Rajanna Sircilla": {
        "mandals": ["Boinpally","Chandurthi","Chinnakodur","Eddula","Elkathurthy","Gambhiraopet","Illanthakunta","Koheda","Konaraopet","Mustabad","Rudrangi","Sircilla","Thangallapally","Vemulawada"],
        "streets": {"Sircilla":["Main Road","Bus Stand Road","Textile Mill Road","Revenue Colony","Market Road"],"Vemulawada":["Vemulawada Main Road","Temple Road","Market Road"],"Gambhiraopet":["Gambhiraopet Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Rangareddy": {
        "mandals": ["Bandlaguda Jagir","Chevella","Farooqnagar","Ghatkesar","Hayathnagar","Ibrahimpatnam","Kandukur","Kothur","Kulkacharla","Marpally","Maheswaram","Manchal","Nandigama","Narsingi","Rajendranagar","Saroornagar","Shamshabad","Shabad","Tandur","Yacharam"],
        "streets": {"Rajendranagar":["Rajendranagar Main Road","Srinagar Colony","Attapur","Kishanbagh","Mehdipatnam"],"Shamshabad":["Shamshabad Main Road","Airport Road","Rajapur","Kothur Road"],"Saroornagar":["Saroornagar Main Road","LB Nagar","Vanasthalipuram","Dilsukhnagar Road"],"Hayathnagar":["Hayathnagar Main Road","Nagole Road","Boduppal Road"],"Ibrahimpatnam":["Ibrahimpatnam Main Road","Pochampally Road","Market Road"],"Narsingi":["Narsingi Main Road","Financial District","Gachibowli Road"],"Chevella":["Chevella Main Road","Market Road"],"Tandur":["Tandur Main Road","Industrial Area"],"default":["Main Road","Colony Road","Nagar","Road"]}
    },
    "Sangareddy": {
        "mandals": ["Andole","Chegunta","Hasnabad","Isnapur","Jogipet","Kohir","Kondapur","Manoor","Mulugu","Narayankhed","Narsapur","Nyalkal","Papannapet","Patancheru","Pulkal","Ramachandrapuram","Sangareddy","Sadasivpet","Ameenpur"],
        "streets": {"Sangareddy":["Main Road","Bus Stand Road","Collectorate Road","Civil Lines","Patancheru Road"],"Patancheru":["Patancheru Main Road","APIIC Road","Industrial Area","Bollarum Road"],"Sadasivpet":["Sadasivpet Main Road","Market Road","NH65"],"Ameenpur":["Ameenpur Main Road","Patancheru Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Siddipet": {
        "mandals": ["Cheriyal","Chinnapotharam","Doultabad","Dubbak","Gajwel","Husnabad","Komuravelly","Maddur","Markook","Nangnoor","Raipole","Siddipet","Thoguta","Wargal"],
        "streets": {"Siddipet":["Main Road","Bus Stand Road","Collectorate Road","Revenue Colony","Gajwel Road"],"Gajwel":["Gajwel Main Road","Market Road","Hyderabad Road"],"Cheriyal":["Cheriyal Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Suryapet": {
        "mandals": ["Atmakur","Chivvemla","Deverkonda","Garidepally","Huzurnagar","Kodad","Munagala","Neredcherla","Ramannapet","Suryapet","Thipparthi","Tirumalapur"],
        "streets": {"Suryapet":["Main Road","Collectorate Road","Bus Stand Road","Market Road","Hyderabad Road"],"Kodad":["Kodad Main Road","Market Road","NH65"],"Huzurnagar":["Huzurnagar Main Road","Market Area"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Vikarabad": {
        "mandals": ["Bantwaram","Basheerabad","Bomraspet","Dharur","Doulatabad","Kulkacherla","Marpally","Nawabpet","Pargi","Pudur","Tandur","Vikarabad","Yalal"],
        "streets": {"Vikarabad":["Main Road","Bus Stand Road","Market Road","Revenue Colony"],"Tandur":["Tandur Main Road","Industrial Area","Market Road"],"Pargi":["Pargi Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Wanaparthy": {
        "mandals": ["Amarchinta","Atmakur","Bhoothpur","Ghanpur","Gopalpet","Kothakota","Madanapur","Peddamandadi","Pebbair","Rever","Srirangapur","Wanaparthy","Weepangandla"],
        "streets": {"Wanaparthy":["Main Road","Bus Stand Road","Market Road","Revenue Colony"],"Gopalpet":["Gopalpet Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Warangal": {
        "mandals": ["Atmakur","Chennaraopet","Dharmasagar","Duggondi","Geesugonda","Hasanparthy","Khanapur","Nallabelly","Parvathagiri","Shayampet","Warangal"],
        "streets": {"Warangal":["Hanamkonda Road","Kazipet Road","Mulugu Road","Station Road","Subedari","Nakkalagutta","Ramji Junction","Hunter Road"],"Hasanparthy":["Hasanparthy Main Road","Market Road","NH163"],"Nallabelly":["Nallabelly Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
    "Yadadri Bhuvanagiri": {
        "mandals": ["Alair","Bhuvanagiri","Bibinagar","Choutuppal","Damarcherla","Gundlapochampally","Motakondur","Mothkur","Munagala","Narketpally","Nereducharla","Ramannapeta","Rajapet","Turkapally","Yadagirigutta"],
        "streets": {"Yadagirigutta":["Temple Road","Yadadri Main Road","Pilgrim Road","Market Road","Bus Stand Road"],"Bhuvanagiri":["Bhuvanagiri Main Road","Market Road","Station Road"],"Bibinagar":["Bibinagar Main Road","AIIMS Road","Market Area"],"Narketpally":["Narketpally Main Road","Market Road"],"default":["Main Road","Colony Road","Market Area"]}
    },
}

STATES_DATA = {
    "Telangana": list(TELANGANA.keys()),
    "Maharashtra": ["Mumbai","Pune","Nagpur","Nashik","Aurangabad"],
    "Karnataka": ["Bengaluru","Mysuru","Hubballi","Mangaluru","Belagavi"],
    "Andhra Pradesh": ["Visakhapatnam","Vijayawada","Guntur","Tirupati","Kurnool","Rajahmundry"],
    "Tamil Nadu": ["Chennai","Coimbatore","Madurai","Salem","Tiruchirappalli"],
}


# ── Auth Routes ───────────────────────────────────────────────────────
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        name=data['name'], email=data['email'],
        password=generate_password_hash(data['password']),
        phone=data.get('phone', ''), role='citizen',
        district=data.get('district', ''),
        mandal=data.get('mandal', ''),
        state=data.get('state', 'Telangana'),
    )
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'user': user.to_dict()}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password, data.get('password', '')):
        return jsonify({'error': 'Invalid email or password'}), 401
    if not user.is_active:
        return jsonify({'error': 'Account deactivated. Contact admin.'}), 403
    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'user': user.to_dict()})


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def me():
    return jsonify(db.get_or_404(User, int(get_jwt_identity())).to_dict())


@app.route('/api/auth/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    user = db.get_or_404(User, int(get_jwt_identity()))
    data = request.get_json()
    for f in ['name', 'phone', 'district', 'mandal', 'state']:
        if f in data:
            setattr(user, f, data[f])
    db.session.commit()
    return jsonify(user.to_dict())


# ── Complaint Routes ──────────────────────────────────────────────────
@app.route('/api/complaints', methods=['GET'])
@jwt_required()
def get_complaints():
    uid  = int(get_jwt_identity())
    user = db.session.get(User, uid)
    q    = Complaint.query
    if user.role == 'citizen':
        q = q.filter_by(user_id=uid)

    for field, value in [('status', request.args.get('status')),
                         ('category', request.args.get('category')),
                         ('district', request.args.get('district')),
                         ('mandal',   request.args.get('mandal')),
                         ('priority', request.args.get('priority'))]:
        if value:
            q = q.filter(getattr(Complaint, field) == value)

    search = request.args.get('search', '')
    if search:
        like = f'%{search}%'
        q = q.filter(db.or_(Complaint.title.ilike(like),
                             Complaint.id.ilike(like),
                             Complaint.description.ilike(like)))

    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    pag      = q.order_by(Complaint.created_at.desc()).paginate(
                    page=page, per_page=per_page, error_out=False)
    return jsonify({'complaints': [c.to_dict() for c in pag.items],
                    'total': pag.total, 'pages': pag.pages, 'page': page})


@app.route('/api/complaints/<cid>', methods=['GET'])
@jwt_required()
def get_complaint(cid):
    c    = db.get_or_404(Complaint, cid)
    uid  = int(get_jwt_identity())
    user = db.session.get(User, uid)
    if user.role == 'citizen' and c.user_id != uid:
        return jsonify({'error': 'Access denied'}), 403
    return jsonify(c.to_dict())


@app.route('/api/complaints/track/<cid>', methods=['GET'])
def track_complaint(cid):
    c = db.session.get(Complaint, cid)
    if not c:
        return jsonify({'error': 'Complaint not found'}), 404
    return jsonify({
        'id': c.id, 'title': c.title, 'category': c.category,
        'district': c.district, 'mandal': c.mandal, 'area': c.area,
        'status': c.status, 'priority': c.priority,
        'assigned_dept': c.assigned_dept,
        'created_at': c.created_at.isoformat(),
        'updated_at': c.updated_at.isoformat(),
        'remarks': [r.to_dict() for r in c.remarks],
    })


@app.route('/api/complaints', methods=['POST'])
@jwt_required()
def create_complaint():
    uid  = int(get_jwt_identity())
    data = request.get_json()
    if not all(k in data for k in ['title', 'description', 'category', 'state', 'district']):
        return jsonify({'error': 'Missing required fields'}), 400

    desc_lower = data['description'].lower()
    priority   = data.get('priority', 'medium')
    if any(kw in desc_lower for kw in URGENT_KEYWORDS):
        priority = 'urgent'

    cid = generate_complaint_id()
    while db.session.get(Complaint, cid):
        cid = generate_complaint_id()

    c = Complaint(
        id=cid, title=data['title'], description=data['description'],
        category=data['category'], state=data['state'],
        district=data['district'], mandal=data.get('mandal', ''),
        area=data.get('area', ''), latitude=data.get('latitude'),
        longitude=data.get('longitude'), priority=priority,
        user_id=uid,
        assigned_dept=CATEGORY_DEPT_MAP.get(data['category'], 'Municipal Corporation'),
        images='[]',
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route('/api/complaints/<cid>', methods=['PATCH'])
@jwt_required()
def update_complaint(cid):
    uid  = int(get_jwt_identity())
    user = db.session.get(User, uid)
    c    = db.get_or_404(Complaint, cid)
    if user.role == 'citizen' and c.user_id != uid:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()
    if user.role == 'admin':
        for f in ['status', 'assigned_officer_id', 'priority', 'assigned_dept']:
            if f in data:
                setattr(c, f, data[f])
        if data.get('remark', '').strip():
            db.session.add(Remark(complaint_id=cid, text=data['remark'].strip(), author_id=uid))
    else:
        if c.status == 'Pending':
            for f in ['description', 'area', 'mandal']:
                if f in data:
                    setattr(c, f, data[f])

    c.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(c.to_dict())


@app.route('/api/complaints/<cid>', methods=['DELETE'])
@admin_required
def delete_complaint(cid):
    c = db.get_or_404(Complaint, cid)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'Deleted'})


@app.route('/api/complaints/<cid>/images', methods=['POST'])
@jwt_required()
def upload_image(cid):
    import json
    uid = int(get_jwt_identity())
    c   = db.get_or_404(Complaint, cid)
    if c.user_id != uid:
        return jsonify({'error': 'Access denied'}), 403
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    images = json.loads(c.images or '[]')
    images.append(filename)
    c.images = json.dumps(images)
    db.session.commit()
    return jsonify({'filename': filename, 'images': images}), 201


# ── Admin Routes ──────────────────────────────────────────────────────
@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    total    = Complaint.query.count()
    resolved = Complaint.query.filter_by(status='Resolved').count()
    cat_counts, dist_counts = {}, {}
    for c in Complaint.query.all():
        cat_counts[c.category]  = cat_counts.get(c.category, 0) + 1
        if c.state == 'Telangana':
            dist_counts[c.district] = dist_counts.get(c.district, 0) + 1
    return jsonify({
        'total':    total,
        'pending':  Complaint.query.filter_by(status='Pending').count(),
        'in_progress': Complaint.query.filter_by(status='In Progress').count(),
        'resolved': resolved,
        'urgent':   Complaint.query.filter(Complaint.priority=='urgent', Complaint.status!='Resolved').count(),
        'citizens': User.query.filter_by(role='citizen').count(),
        'resolution_rate': round(resolved / total * 100, 1) if total else 0,
        'category_breakdown': cat_counts,
        'district_breakdown': dist_counts,
    })


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def list_users():
    return jsonify([u.to_dict() for u in User.query.order_by(User.created_at.desc()).all()])


@app.route('/api/admin/users/<int:uid>/toggle', methods=['PATCH'])
@admin_required
def toggle_user(uid):
    u = db.get_or_404(User, uid)
    u.is_active = not u.is_active
    db.session.commit()
    return jsonify(u.to_dict())


@app.route('/api/admin/users/<int:uid>', methods=['DELETE'])
@admin_required
def delete_user(uid):
    u = db.get_or_404(User, uid)
    if u.role == 'admin':
        return jsonify({'error': 'Cannot delete admin'}), 403
    db.session.delete(u)
    db.session.commit()
    return jsonify({'message': 'Deleted'})


# ── Officers Routes ───────────────────────────────────────────────────
@app.route('/api/officers', methods=['GET'])
@jwt_required()
def list_officers():
    q = Officer.query.filter_by(is_active=True)
    if request.args.get('district'):
        q = q.filter_by(district=request.args.get('district'))
    return jsonify([o.to_dict() for o in q.all()])


@app.route('/api/officers', methods=['POST'])
@admin_required
def create_officer():
    data = request.get_json()
    o = Officer(name=data['name'], department_id=data.get('department_id'),
                email=data.get('email'), phone=data.get('phone'),
                district=data.get('district'), mandal=data.get('mandal'))
    db.session.add(o)
    db.session.commit()
    return jsonify(o.to_dict()), 201


@app.route('/api/officers/<int:oid>', methods=['PATCH', 'DELETE'])
@admin_required
def manage_officer(oid):
    o = db.get_or_404(Officer, oid)
    if request.method == 'DELETE':
        o.is_active = False
        db.session.commit()
        return jsonify({'message': 'Deactivated'})
    data = request.get_json()
    for f in ['name', 'email', 'phone', 'district', 'mandal', 'department_id', 'is_active']:
        if f in data:
            setattr(o, f, data[f])
    db.session.commit()
    return jsonify(o.to_dict())


# ── Departments Routes ────────────────────────────────────────────────
@app.route('/api/departments', methods=['GET'])
@jwt_required()
def list_departments():
    return jsonify([d.to_dict() for d in Department.query.all()])


@app.route('/api/departments', methods=['POST'])
@admin_required
def create_department():
    data = request.get_json()
    d = Department(name=data['name'], category=data.get('category'),
                   district=data.get('district'), state=data.get('state', 'Telangana'),
                   head=data.get('head'), email=data.get('email'), phone=data.get('phone'))
    db.session.add(d)
    db.session.commit()
    return jsonify(d.to_dict()), 201


# ── Analytics ─────────────────────────────────────────────────────────
@app.route('/api/analytics/monthly', methods=['GET'])
@admin_required
def monthly_analytics():
    from sqlalchemy import extract, func
    results = db.session.query(
        extract('year',  Complaint.created_at).label('year'),
        extract('month', Complaint.created_at).label('month'),
        func.count(Complaint.id).label('total'),
        func.sum(db.case((Complaint.status == 'Resolved', 1), else_=0)).label('resolved'),
    ).group_by('year', 'month').order_by('year', 'month').all()
    return jsonify([{'year': int(r.year), 'month': int(r.month),
                     'total': r.total, 'resolved': int(r.resolved or 0)} for r in results])


@app.route('/api/analytics/districts', methods=['GET'])
@admin_required
def district_analytics():
    from sqlalchemy import func
    results = db.session.query(
        Complaint.district,
        func.count(Complaint.id).label('total'),
        func.sum(db.case((Complaint.status == 'Resolved', 1), else_=0)).label('resolved'),
    ).filter_by(state='Telangana').group_by(Complaint.district).all()
    return jsonify([{'district': r.district, 'total': r.total,
                     'resolved': int(r.resolved or 0)} for r in results])


# ── Location Routes ───────────────────────────────────────────────────
@app.route('/api/locations/states', methods=['GET'])
def get_states():
    return jsonify(list(STATES_DATA.keys()))


@app.route('/api/locations/districts/<state>', methods=['GET'])
def get_districts(state):
    return jsonify(STATES_DATA.get(state, []))


@app.route('/api/locations/mandals/<district>', methods=['GET'])
def get_mandals(district):
    return jsonify(TELANGANA.get(district, {}).get('mandals', []))


@app.route('/api/locations/streets/<district>/<mandal>', methods=['GET'])
def get_streets(district, mandal):
    streets_map = TELANGANA.get(district, {}).get('streets', {})
    return jsonify(streets_map.get(mandal, streets_map.get('default', ['Main Road', 'Colony Road'])))


@app.route('/api/locations/all-districts', methods=['GET'])
def all_districts():
    return jsonify([{'name': d, 'mandal_count': len(v['mandals']), 'mandals': v['mandals']}
                    for d, v in TELANGANA.items()])


# ── Health Check ──────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'version': '2.0.0',
                    'districts': len(TELANGANA), 'url': 'http://localhost:5000'})


# ── Error Handlers ────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    # For API routes return JSON; for everything else serve the SPA
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_file(os.path.join(BASE_DIR, 'index.html'))

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# ── Seed Data ─────────────────────────────────────────────────────────
def seed_db():
    if User.query.count() == 0:
        db.session.add_all([
            User(name='Admin Officer', email='admin@civic.gov',
                 password=generate_password_hash('admin123'),
                 role='admin', district='Hyderabad', state='Telangana'),
            User(name='Ravi Shankar', email='ravi@gmail.com',
                 password=generate_password_hash('ravi123'),
                 role='citizen', phone='9000000002',
                 district='Hyderabad', mandal='Secunderabad', state='Telangana'),
            User(name='Priya Reddy', email='priya@gmail.com',
                 password=generate_password_hash('priya123'),
                 role='citizen', phone='9000000003',
                 district='Rangareddy', mandal='Shamshabad', state='Telangana'),
        ])
        db.session.commit()

    if Department.query.count() == 0:
        db.session.add_all([
            Department(name='PWD Department',       category='roads',       district='Hyderabad', state='Telangana', head='Er. Krishnarao',    email='pwd.hyd@gov.in',          phone='040-23456789'),
            Department(name='GHMC - Sanitation',    category='sanitation',  district='Hyderabad', state='Telangana', head='Commissioner GHMC', email='sanitation@ghmc.gov.in',  phone='040-23228777'),
            Department(name='HMWSSB - Water Board', category='water',       district='Hyderabad', state='Telangana', head='MD HMWSSB',         email='info@hmwssb.gov.in',      phone='040-23299999'),
            Department(name='TSSPDCL - Electricity',category='electricity', district='Hyderabad', state='Telangana', head='CMD TSSPDCL',       email='cmd@tsspdcl.gov.in',      phone='040-23435555'),
            Department(name='Drainage Department',  category='drainage',    district='Hyderabad', state='Telangana', head='Chief Engineer',    email='drainage@ghmc.gov.in',    phone='040-23228700'),
            Department(name='Parks & Recreation',   category='parks',       district='Hyderabad', state='Telangana', head='Director Parks',    email='parks@ghmc.gov.in',       phone='040-23228100'),
            Department(name='Pollution Control',    category='noise',       district='Hyderabad', state='Telangana', head='Member Secretary',  email='tspcb@gov.in',            phone='040-23898000'),
            Department(name='Municipal Corporation',category='other',       district='Hyderabad', state='Telangana', head='Commissioner',      email='mc@ghmc.gov.in',          phone='040-23228999'),
        ])
        db.session.commit()

    if Officer.query.count() == 0:
        db.session.add_all([
            Officer(name='Rajesh Kumar',  department_id=1, district='Hyderabad',          mandal='Khairatabad', email='rajesh@pwd.gov.in',    phone='9100000001'),
            Officer(name='Sunita Sharma', department_id=2, district='Hyderabad',          mandal='Secunderabad',email='sunita@ghmc.gov.in',   phone='9100000002'),
            Officer(name='Pradeep Nair',  department_id=3, district='Hyderabad',          mandal='Musheerabad', email='pradeep@hmwssb.gov.in', phone='9100000003'),
            Officer(name='Anita Rao',     department_id=4, district='Hyderabad',          mandal='Golconda',    email='anita@tsspdcl.gov.in', phone='9100000004'),
            Officer(name='Venkat Reddy',  department_id=2, district='Rangareddy',         mandal='Saroornagar', email='venkat@ghmc.gov.in',   phone='9100000005'),
            Officer(name='Mahesh Babu',   department_id=1, district='Rangareddy',         mandal='Shamshabad',  email='mahesh@pwd.gov.in',    phone='9100000006'),
            Officer(name='Kavitha Devi',  department_id=5, district='Medchal-Malkajgiri', mandal='Kompally',    email='kavitha@drain.gov.in', phone='9100000007'),
            Officer(name='Suresh Goud',   department_id=6, district='Hyderabad',          mandal='Charminar',   email='suresh@parks.gov.in',  phone='9100000008'),
        ])
        db.session.commit()

    if Complaint.query.count() == 0:
        db.session.add_all([
            Complaint(id='CMP-HYD001', title='Large pothole on MG Road', category='roads',
                      state='Telangana', district='Hyderabad', mandal='Secunderabad', area='MG Road',
                      description='Dangerous pothole near Paradise circle causing accidents and traffic jams',
                      status='In Progress', priority='urgent', user_id=2,
                      assigned_dept='PWD Department', assigned_officer_id=1, images='[]'),
            Complaint(id='CMP-HYD002', title='Garbage overflow at Kukatpally', category='sanitation',
                      state='Telangana', district='Medchal-Malkajgiri', mandal='Kompally', area='Kukatpally Main Road',
                      description='Garbage bins overflowing for 3 days near the main market',
                      status='Pending', priority='high', user_id=2,
                      assigned_dept='GHMC - Sanitation', images='[]'),
            Complaint(id='CMP-RR001', title='Street lights not working - Airport Road', category='electricity',
                      state='Telangana', district='Rangareddy', mandal='Shamshabad', area='Airport Road',
                      description='3 consecutive street lights not working since a week',
                      status='Resolved', priority='medium', user_id=3,
                      assigned_dept='TSSPDCL - Electricity', assigned_officer_id=4, images='[]'),
            Complaint(id='CMP-KMR001', title='Water supply disruption - Karimnagar Urban', category='water',
                      state='Telangana', district='Karimnagar', mandal='Karimnagar Urban', area='Main Road',
                      description='Water supply not available for 3 days in the colony',
                      status='Pending', priority='urgent', user_id=2,
                      assigned_dept='HMWSSB - Water Board', images='[]'),
            Complaint(id='CMP-WGL001', title='Broken park benches - Warangal', category='parks',
                      state='Telangana', district='Warangal', mandal='Warangal', area='Station Road',
                      description='Multiple benches in the central park are broken',
                      status='Pending', priority='low', user_id=3,
                      assigned_dept='Parks & Recreation', images='[]'),
            Complaint(id='CMP-RR002', title='Open drain near Rajendranagar', category='drainage',
                      state='Telangana', district='Rangareddy', mandal='Rajendranagar', area='Rajendranagar Main Road',
                      description='Open drainage canal causing mosquito breeding and bad smell',
                      status='In Progress', priority='high', user_id=3,
                      assigned_dept='Drainage Department', assigned_officer_id=7, images='[]'),
        ])
        db.session.commit()

        db.session.add_all([
            Remark(complaint_id='CMP-HYD001', text='Officer dispatched to site', author_id=1),
            Remark(complaint_id='CMP-HYD001', text='Repair work scheduled for tomorrow', author_id=1),
            Remark(complaint_id='CMP-RR001',  text='Issue resolved, new LED lights installed', author_id=1),
            Remark(complaint_id='CMP-RR002',  text='Site inspection done, work order raised', author_id=1),
        ])
        db.session.commit()


# ── Entry Point ───────────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_db()

    # Auto-open browser (only on first start, not on reload)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        def open_browser():
            webbrowser.open('http://localhost:5000')
        threading.Timer(1.5, open_browser).start()

    print("=" * 55)
    print("  CivicPulse v2.0 - Telangana Civic Management")
    print("=" * 55)
    print("  Frontend : http://localhost:5000")
    print("  API      : http://localhost:5000/api/health")
    print("  Districts: 33 Telangana districts loaded")
    print("=" * 55)
    print("  Admin    : admin@civic.gov / admin123")
    print("  Citizen  : ravi@gmail.com  / ravi123")
    print("=" * 55)
    print("  Press CTRL+C to stop the server")
    print("=" * 55)

    app.run(debug=False, host='0.0.0.0', port=5000)
