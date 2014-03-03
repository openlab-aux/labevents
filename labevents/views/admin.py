# -*- coding: utf-8 -*-
import labevents
from labevents import app
from labevents.models import Event, Location, Cancelation

from flask import g, render_template, redirect
from flask.ext.login import login_required, current_user

from flask_wtf import Form
from wtforms import TextField, TextAreaField, DateTimeField, FileField, SelectField
from wtforms import validators

@app.route('/admin')
@login_required
def admin_overview():
    locations = g.db.query(Location).all()
    events = g.db.query(Event).all()
    return render_template("admin.html", events=events, locations=locations)
    
class EventForm(Form):
    title = TextField(validators=[validators.Required()])
    location = SelectField(validators=[validators.Required()],
                           choices=[ (str(l.id), l.name) for l in labevents.database.Session().query(Location).all() ])
    description = TextAreaField(validators=[validators.Required()])
    start_date = DateTimeField(format="%d.%m.%Y, %H:%M", validators=[validators.Required()])
    end_date = DateTimeField(format="%d.%m.%Y, %H:%M")
    image = FileField()
    repetition_pattern = SelectField(choices=[(u"0", "Keine"), (u"1", u"Wöchentlich"), 
                                              (u"2", u"Zweiwöchentlich")], 
                                     validators=[validators.Required()])
@app.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        l = g.db.query(Location).filter(
            Location.id==int(form.location.data
        )).one()
        u = current_user
        e = Event(title=form.title.data,
                  description=form.description.data,
                  start_date=form.start_date.data,
                  end_date=form.end_date.data,
                  location=l,
                  owner=u,
                  repetition_pattern=int(form.repetition_pattern.data)
        )
        g.db.add(e)
        g.db.commit()
        return redirect('/admin')

    return render_template("create_event.html", form=form) 
    
@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    e = g.db.query(Event).filter(Event.id == id).one()
    form = EventForm(obj=e)
    
    if form.validate_on_submit():
        e.title = form.title.data
        e.description = form.description.data
        e.start_date = form.start_date.data
        e.end_date = form.end_date.data
        e.repetition_pattern = int(form.repetition_pattern.data)
        g.db.commit()
        return redirect('/admin')

    return render_template("edit_event.html",
                           form=form)
    
@app.route('/admin/events/delete/<int:id>', methods=['GET'])
@login_required
def delete_event(id):
    e = g.db.query(Event).filter(Event.id == id).one()
    g.db.delete(e)
    g.db.commit()
    return redirect('/admin')
