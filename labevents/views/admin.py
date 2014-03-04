# -*- coding: utf-8 -*-
import labevents
from labevents import app
from labevents.models import Event, Location, Cancelation
from labevents.util import random_string, crop_square_image

from os.path import join as opj

from flask import g, render_template, redirect
from flask.ext.login import login_required, current_user

from flask_wtf import Form
from wtforms import TextField, TextAreaField, DateTimeField, SelectField, \
    FileField
from wtforms import validators


@app.route('/admin')
@login_required
def admin_overview():
    locations = g.db.query(Location).all()
    events = g.db.query(Event).all()
    return render_template("admin.html",
                           user=current_user,
                           events=events,
                           locations=locations)
    
class EventForm(Form):
    title = TextField(validators=[validators.Required()])
    location = SelectField(validators=[validators.Required()])
    description = TextAreaField(validators=[validators.Required()])
    start_date = DateTimeField(format="%d.%m.%Y, %H:%M", validators=[validators.Required()])
    end_date = DateTimeField(format="%d.%m.%Y, %H:%M")
    image = FileField()
    repetition_pattern = SelectField(choices=[(u"0", "Keine"), (u"1", u"Wöchentlich"), 
                                              (u"2", u"Zweiwöchentlich")], 
                                     validators=[validators.Required()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.location.choices = [ (str(l.id), l.name) for l in labevents.database.Session().query(Location).all() ]

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

        if form.image.data is not None:
            filename = random_string(32)+'.'+\
                       form.image.data.mimetype.split("/")[1]
            path = opj(app.config['IMAGE_UPLOAD_PATH'], filename)
            image_squared = crop_square_image(form.image.data)
            image_squared.save(path)
            e.image_path=app.config['IMAGE_UPLOAD_PREFIX']+filename

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
        l = g.db.query(Location).\
            filter(Location.id == int(form.location.data)).one()

        e.title = form.title.data
        e.description = form.description.data
        e.start_date = form.start_date.data
        e.end_date = form.end_date.data
        e.repetition_pattern = int(form.repetition_pattern.data)
        e.location = l
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
    
class LocationForm(Form):
    name = TextField(validators=[validators.Required()])
    address = TextField(validators=[validators.Required()])

@app.route('/admin/locations/add', methods=['GET', 'POST'])
@login_required
def create_location():
    form = LocationForm()

    if form.validate_on_submit():
        l = Location(name=form.name.data,
                     address=form.address.data)
        g.db.add(l)
        g.db.commit()
        return redirect('/admin')

    return render_template("create_location.html",
                           form=form)
    
@app.route('/admin/locations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_location(id):
    l = g.db.query(Location).filter(Location.id == id).one()
    form = LocationForm(obj=l)

    if form.validate_on_submit():
        l.name = form.name.data
        l.address = form.address.data
        g.db.commit()
        return redirect('/admin')

    return render_template("edit_location.html",
                           form=form)

@app.route('/admin/locations/delete/<int:id>')
@login_required
def delete_location(id):
    l = g.db.query(Location).filter(Location.id == id).one()
    g.db.delete(l)
    g.db.commit()
    return redirect('/admin')
