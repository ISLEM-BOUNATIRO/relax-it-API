from email.policy import default
from app import db,ma
from sqlalchemy import *
from datetime import *

groups = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'), primary_key=True)
)


class Group(db.Model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name=Column(String, unique=True)
    members=Column(Text,default="")
    description=Column(Text)

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(Integer, primary_key=True)
    ip = db.Column(String, unique=True, nullable=False)
    type = db.Column(String)
    vendor = db.Column(String)
    model = db.Column(String)
    serial_number = db.Column(String)
    firmware_version = db.Column(String)
    creation_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow())
    groups = db.relationship('Group', secondary=groups,lazy='subquery' 
        ,backref=db.backref('devices',lazy=True))


class Script(db.Model):
    __tablename__ = 'script'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, unique=True, nullable=False)
    content = db.Column(Text)
    description = db.Column(Text)
    creation_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow())

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username=Column(String, unique=True)
    email=Column(Text,default="")
    password=Column(Text)


class Office(db.Model):
    __tablename__ = 'office'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    office_class = db.Column(String)
    postal_code = db.Column(String)


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        load_instance = True

class ScriptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Script
        load_instance = True

class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class OfficeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Office
        load_instance = True