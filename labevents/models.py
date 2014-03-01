from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    passwordhash = Column(String)
    
    def __repr__(self):
        return "<User '%s'>" % self.name
        
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.passwordhash = generate_password_hash(password)


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    REPETITION_NONE = 0
    REPETITION_WEEKLY = 1
    REPETITION_BIWEEKLY = 2
    REPETITION_FIRST_WEEKDAY_MONTH = 3
    REPETITION_LAST_WEEKDAY_MONTH = 4
    repetition_pattern = Column(Integer)
    
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User')
    
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location')
    
    cancelations = relationship('Cancelation')
    
    def __repr__(self):
        return "<Event '%s' on '%s'>" % (self.title, 
            self.start_date.strftime('%d-%m-%Y %H:%M'))
        
    def __init__(self, title, description, start_date, owner, location, 
                 end_date=None, repetition_pattern=0):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.owner = owner
        self.repetiton_pattern = repetition_pattern
        self.location = location

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address = Column(String(100))
    
    def __repr__(self):
        return "<Location '%s'>" % self.name
        
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
class Cancelation(Base):
    __tablename__ = 'cancelation'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    reason = Column(String(100))
    
    event_id = Column(Integer, ForeignKey('event.id'))
    
    def __repr__(self):
        return "<Cancelation for '%s'>" % self.date.strftime('%m-%d-%Y')
