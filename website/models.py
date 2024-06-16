from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    in_game_name = Column(String(150))
    password = Column(String(150))
    admin = Column(Boolean, default=False)
    mechs = relationship('Mechlist', backref='user', lazy=True)

class Mech(db.Model):
    __tablename__ = 'mechs'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, index=True)
    chassis = Column(String(10))
    tonnage = Column(Integer)
    weight_class = Column(String(10))
    chassis_type = Column(String(10))
    omni_mech = Column(Boolean, default=False)
    side = Column(String(10))

class Mechlist(db.Model):
    __tablename__ = 'mechlists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    mech_name = Column(Integer, ForeignKey('mechs.name'))
    data = relationship('Mech', backref='mechlist', lazy=True)

class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    name = Column(String(50), unique=True)
    full_name = Column(String(150))
    team_size = Column(Integer)
    events = relationship('Event', backref='tournament', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    name = Column(String(100))
    date = Column(Date)
    details = Column(String(1000))
    dropdecks = relationship('Dropdeck', backref='event', lazy=True)
    attendees = relationship('Attendance', backref='event', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

class Dropdeck(db.Model):
    __tablename__ = 'dropdecks'

    id = Column(Integer, primary_key=True)
    is_finalized = Column(Boolean, default=False)
    name = Column(String(100))
    event_id = Column(Integer, ForeignKey('events.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    map_id = Column(Integer, ForeignKey('maps.id'), nullable=True)
    starting_side = Column(Integer)
    items = relationship('DropdeckLine', backref='dropdeck', lazy=True)

class Map(db.Model):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class DropdeckLine(db.Model):
    __tablename__ = 'dropdeck_lines'

    id = Column(Integer, primary_key=True)
    dropdeck_id = Column(Integer, ForeignKey('dropdecks.id'))
    pilot_id = Column(Integer, ForeignKey('users.id'))
    mech_id = Column(Integer, ForeignKey('mechs.id'))
    loadout = Column(String)
    notes = Column(String)

class Build(db.Model):
    __tablename__ = 'builds'

    id = Column(Integer, primary_key=True)
    mech_id = Column(Integer, ForeignKey('mechs.id'))
    name = Column(String(100))
    loadout = Column(String(100))
    engine = Column(String(10))
    code = Column(String(200))
    notes = Column(String)
    updated = Column(DateTime(timezone=True), default=func.now())
    data = relationship('Mech', backref='build', lazy=True)

class LogMessage(db.Model):
    __tablename__ = 'log_messages'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    message = Column(String(1000))
