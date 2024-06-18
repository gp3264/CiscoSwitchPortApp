
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
