from labevents import app
from labevents.models import User

import sqlalchemy
from flask import render_template, redirect, g, request
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def web_login():
    class LoginForm(Form):
        username = TextField('username', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        
    if request.method == 'POST':
        form = LoginForm(request.form)
    else:
        form = LoginForm()
    try:
        if form.validate_on_submit():
            user = g.db.query(User).filter(User.name == form.username.data).one()
            if check_password_hash(user.passwordhash, form.password.data):
                session = request.environ['beaker.session']
                session['username'] = user.name
                session.save()
                return redirect('/admin')
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    return render_template("login.html", form=form)
    
@app.route('/logout')
def web_logout():
    session = request.environ['beaker.session']
    try:
        del session['username']
    except KeyError:
        pass
    session.save()
    return redirect('/')
