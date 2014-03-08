from datetime import date

from flask import g
from flask import render_template, abort
from flask import Response
from html2text import html2text
from sqlalchemy.orm import contains_eager
import icalendar

from labevents import app
from labevents.models import Event

def __get_events(conn):
    events = []
    for e in conn.query(Event).options(contains_eager('location'), 
                                       contains_eager('owner')).\
             filter((Event.start_date > date.today()) | 
                    (Event.repetition_pattern != Event.REPETITION_NONE)).\
             order_by(Event.start_date).all():
        for r in e.resolve_repetitions():
            if r.start_date.date() >= date.today():
                events.append(r)
    return sorted(
        events,
        key=lambda e: e.start_date
    )


@app.route('/')
def show_events():
    return render_template("web_show_events.html",
                           events=__get_events(g.db))
    
@app.route('/events/<int:id>')
def show_event_details(id):
    event = g.db.query(Event).filter(Event.id == id).one()
    return render_template("web_show_event_detail.html",
                           event=event)
    
@app.route('/events/ical')
def show_events_ical():
    events = __get_events(g.db)

    cal = icalendar.Calendar()
    cal.add('prodid', '-//Weltraumpflege.org///NONSGML LabEvents//EN')
    cal.add('version', '2.0')

    for event in events:
        ical_event = icalendar.Event()
        ical_event.add('summary', event.title)
        ical_event.add('dtstart', event.start_date)
        if event.end_date:
            ical_event.add('dtend', event.end_date)
        if event.description:
            ical_event.add('description', html2text(event.description))
        # ical_event.add('dtstamp', event.lastchanged_date)
        ical_event['uid'] = event.start_date.strftime("%s") + str(event.id) \
            + "@events.openlab-augsburg.de"
        cal.add_component(ical_event)

    return Response(cal.to_ical(), mimetype='text/calendar')
