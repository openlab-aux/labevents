from datetime import date

from flask import g
from flask import render_template, abort

from labevents import app
from labevents.models import Event

@app.route('/')
def show_events():
    events = []
    for e in g.db.query(Event).filter(Event.start_date > date.today()).\
        order_by(Event.start_date).all():
        events.extend(e.resolve_repetitions())
    return render_template("web_show_events.html",
                           events=sorted(events, key=lambda e: e.start_date))
    
@app.route('/events/<int:id>')
def show_event_details(id):
    event = g.db.query(Event).filter(Event.id == id).one()
    return render_template("web_show_event_detail.html",
                           event=event)
