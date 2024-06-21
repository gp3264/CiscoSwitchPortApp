import os
from .database import Database

db = Database.db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Interface(db.Model):
    __tablename__ = 'interface'
    interface_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    ip_address = db.Column(db.String(64))
    status = db.Column(db.String(64))
    protocol = db.Column(db.String(64))

    device = db.relationship('Device', backref=db.backref('interfaces', lazy=True))

class VersionInfo(db.Model):
    __tablename__ = 'version_info'
    version_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)
    software = db.Column(db.String(256))
    uptime = db.Column(db.String(256))
    system_image = db.Column(db.String(256))
    processor_board_id = db.Column(db.String(64))

    device = db.relationship('Device', backref=db.backref('version_info', lazy=True))
