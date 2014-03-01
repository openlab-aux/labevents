from unittest import TestCase
from datetime import date, datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from labevents.models import Base, User, Event, Location, Cancelation

class TestModels(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        self.Session = sessionmaker(bind=engine)
        
        s = self.Session()
        u = User(name='test',
                 email='test@example.com',
                 password='test')
        s.add(u)
        
        l = Location(name='Test',
                     address='Testweg 1, 12345 Musterstadt')
        s.add(l)
        
        e =  Event(title='Test',
                   description='Lorem ipsum dolor sit amet',
                   start_date=datetime.now(),
                   end_date=datetime.now()+timedelta(minutes=90),
                   owner = u,
                   location = l)

        c = Cancelation(date(e.start_date.year,
                             e.start_date.month,
                             e.start_date.day),
                        "Test")
        s.add(c)
        e.cancelations.append(c)

        s.add(e)
        
        s.commit()
        
    def test_event_has_owner(self):
        s = self.Session()
        e = s.query(Event).all()[0]

        self.assertIsInstance(e.owner, User)
        
    def test_event_has_location(self):
        s = self.Session()
        e = s.query(Event).all()[0]
        
        self.assertIsInstance(e.location, Location)

    def test_event_has_cancelation(self):
        s = self.Session()
        e = s.query(Event).all()[0]
        
        self.assertGreater(len(e.cancelations), 0)
        for c in e.cancelations:
            self.assertIsInstance(c, Cancelation)
