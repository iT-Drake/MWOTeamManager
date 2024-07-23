from flask_login import UserMixin

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from .utility import Duration, LocalDate, SetUTC, Now
from . import db

class Model(db.Model):
    __abstract__ = True

    @classmethod
    def Total(self):
        return self.query.count()
    
    @classmethod
    def All(self):
        return self.query.all()

    def Add(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)
        return self

    def Update(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)

class User(Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    in_game_name = Column(String(150))
    timezone = Column(String(100))
    password = Column(String(150))
    admin = Column(Boolean, default=False)
    mechs = relationship('Mechlist', backref='user', lazy=True)

    @classmethod
    def Total(self):
        count = self.query.filter_by(admin=False).count()
        return count
    
    @classmethod
    def All(self):
        return self.query.filter_by(admin=False).all()

class Mech(Model):
    __tablename__ = 'mechs'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, index=True)
    chassis = Column(String(10))
    tonnage = Column(Integer)
    weight_class = Column(String(10))
    chassis_type = Column(String(10))
    omni_mech = Column(Boolean, default=False)
    side = Column(String(10))

class Mechlist(Model):
    __tablename__ = 'mechlists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    mech_name = Column(Integer, ForeignKey('mechs.name'))
    data = relationship('Mech', backref='mechlist', lazy=True)

    @classmethod
    def TeamTotal(self):
        u = db.session.query(Mechlist, func.count(Mechlist.id)).group_by(Mechlist.mech_name).all()
        team_total = {}
        for item in u:
            mechlist = item[0]
            count = item[1]
            team_total[mechlist.mech_name] = count
        
        return team_total

class Tournament(Model):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    name = Column(String(50), unique=True)
    full_name = Column(String(150))
    team_size = Column(Integer)
    events = relationship('Event', backref='tournament', lazy=True)

class Event(Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    name = Column(String(100))
    date = Column(DateTime(timezone=True), default=func.now())
    duration = Column(Integer)
    details = Column(String(1000))
    map_planner_link = Column(String(100))
    is_canceled = Column(Boolean, default=False)
    dropdecks = relationship('Dropdeck', backref='event', lazy=True)
    attendees = relationship('Attendance', backref='event', lazy=True)

    @classmethod
    def ActiveEvents(self):
        active_events = self.query.join(Tournament).filter(Tournament.is_active == True, Event.is_canceled == False).all()
        items = []
        current_date = Now()
        for event in active_events:
            if event.EndDate() > current_date:
                event.date = LocalDate(event.date)
                items.append(event)
        return items

    @classmethod
    def ActiveTotal(self):
        return self.query.join(Tournament).filter(Tournament.is_active == True, Event.is_canceled == False).count()
    
    @classmethod
    def PassedEvents(self):
        passed_events = self.query.join(Tournament).filter(Tournament.is_active == True).all()
        items = []
        current_date = Now()
        for event in passed_events:
            if event.EndDate() <= current_date or event.is_canceled:
                event.date = LocalDate(event.date)
                items.append(event)
        return items
    
    def EndDate(self):
        return SetUTC(self.date + Duration(self.duration)) if self.duration else SetUTC(self.date)
    
    def Attendees(self):
        pilots = {}
        # for item in self.attendees:
        #     pilots[item.user_id] = item.user.in_game_name
        # if len(pilots) == 0:
        #     items = User.All()
        #     for item in items:
        #         pilots[item.id] = item.in_game_name
        items = User.All()
        for item in items:
            pilots[item.id] = item.in_game_name
        return pilots

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='attendance', lazy=True)

class Map(db.Model):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class Build(Model):
    __tablename__ = 'builds'

    id = Column(Integer, primary_key=True)
    mech_id = Column(Integer, ForeignKey('mechs.id'))
    name = Column(String(100))
    loadout = Column(String(100))
    code = Column(String(200))
    notes = Column(String)
    for_omni_mechs = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    armor = Column(String(10))
    engine = Column(String(10))
    speed = Column(String(20))
    firepower = Column(String(10))
    dps = Column(String(10))
    heatsinks = Column(String(10))
    dissipation = Column(String(10))
    updated = Column(DateTime(timezone=True), default=func.now())
    data = relationship('Mech', backref='build', lazy=True)

class Dropdeck(Model):
    __tablename__ = 'dropdecks'

    id = Column(Integer, primary_key=True)
    is_finalized = Column(Boolean, default=False)
    name = Column(String(100))
    drop_number = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    map_id = Column(Integer, ForeignKey('maps.id'), nullable=True)
    starting_side = Column(Integer)
    rows = relationship('DropdeckLine', backref='dropdeck', lazy=True)
    map = relationship('Map', backref='dropdeck', lazy=True)
    author = relationship('User', backref='dropdeck', lazy=True)

    @classmethod
    def ActiveDropdecks(self):
        return self.query.join(Event).join(Tournament).filter(Tournament.is_active == True).all()

class DropdeckLine(db.Model):
    __tablename__ = 'dropdeck_lines'

    id = Column(Integer, primary_key=True)
    dropdeck_id = Column(Integer, ForeignKey('dropdecks.id'))
    pilot_id = Column(Integer, ForeignKey('users.id'))
    spawn = Column(String(10))
    mech_id = Column(Integer, ForeignKey('mechs.id'))
    build_id = Column(Integer, ForeignKey('builds.id'))
    notes = Column(String)
    build = relationship('Build', backref='dropdeck_line', lazy=True)

class LogMessage(db.Model):
    __tablename__ = 'log_messages'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), default=func.now())
    message = Column(String(1000))
