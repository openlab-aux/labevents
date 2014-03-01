from flask import g
from flask import render_template, abort

from labevents import app
from labevents.models import Event

@app.route('/')
def show_events():
    events = []
    for e in g.db.query(Event).all():
        events.extend(e.resolve_repetitions())
    return render_template("web_show_events.html",
                           events=events)
    
@app.route('/events/<int:id>')
def show_event_details(id):
    event = g.db.query(Event).filter(Event.id == id).one()
    return render_template("web_show_event_detail.html",
                           event=event)
