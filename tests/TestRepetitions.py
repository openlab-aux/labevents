from unittest import TestCase
from datetime import datetime, timedelta

from labevents.models import Event, User, Location, Cancelation

class TestRepetitions(TestCase):
    def setUp(self):
        u = User(name='test',
                 email='test@example.com',
                 password='test')
        l = Location(name='Test',
                     address='Testweg 1, 12345 Musterstadt')
 
        self.event = Event(title="Testevent",
                           description='Lorem ipsum dolor sit amet',
                           start_date=datetime.now(),
                           end_date=datetime.now()+timedelta(minutes=90),
                           owner = u,
                           location = l)
        
    def test_repetition_none(self):
        self.event.repetition_pattern = Event.REPETITION_NONE
        events = self.event.resolve_repetitions(future=timedelta(days=3))
        self.assertEqual(len(events), 1)
        
    def test_repetition_weekly(self):
        self.event.repetition_pattern = Event.REPETITION_WEEKLY
        events = self.event.resolve_repetitions(future=timedelta(weeks=5))
        self.assertGreater(len(events), 1)
        
    def test_repetition_biweekly(self):
        self.event.repetition_pattern = Event.REPETITION_BIWEEKLY
        events = self.event.resolve_repetitions(future=timedelta(weeks=5))
        self.assertEqual(len(events), 3)
        
    def test_cancelation(self):
        self.event.repetition_pattern = Event.REPETITION_WEEKLY
        self.event.cancelations = [ Cancelation(
            (self.event.start_date+timedelta(weeks=1)).date(), "lel")
        ]
        events = self.event.resolve_repetitions(future=timedelta(weeks=5))
        self.assertEqual(len(events), 5)
