
from .database import Database

db = Database.db

class MdtaRegion(db.Model):
    __tablename__ = 'mdta_region'
    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(64), nullable=False, unique=True)

class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(64), nullable=False, unique=True)
    host_name = db.Column(db.String(64), nullable=False, unique=True)
    region_id = db.Column(db.Integer, db.ForeignKey('mdta_region.region_id'), nullable=False)

    region = db.relationship('MdtaRegion', backref=db.backref('devices', lazy=True))

class Switchport(db.Model):
    __tablename__ = 'switchport'
    switchport_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)
    ip_address = db.Column(db.String(64), nullable=False)
    host_name = db.Column(db.String(64), nullable=False)

    device = db.relationship('Device', backref=db.backref('switchports', lazy=True))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AD_SERVER = 'ldap://your_ad_server'
    AD_DOMAIN = 'your_domain'
    LANSWEEPER_SERVER = r'(localdb)\.\LSInstance'
    LANSWEEPER_DATABASE = 'lansweeperdb'
    LANSWEEPER_USERNAME = os.environ.get('LANSWEEPER_USERNAME') or 'your_username'
    LANSWEEPER_PASSWORD = os.environ.get('LANSWEEPER_PASSWORD') or 'your_password'
