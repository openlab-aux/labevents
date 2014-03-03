from labevents import app, login_manager
from labevents.models import User

import sqlalchemy
from flask import render_template, redirect, g
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@login_manager.user_loader
def get_user(id):
    try:
        user = g.db.query(User).filter(User.id == int(id)).one()
        return user
    except:
        return None


@app.route('/login', methods=['GET', 'POST'])
def web_login():
    class LoginForm(Form):
        username = TextField('username', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = g.db.query(User).filter(User.name == form.username.data).one()
            if check_password_hash(user.passwordhash, form.password.data):
                login_user(user)
                return redirect('/lel')
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    return render_template("login.html", form=form)
    
@app.route('/logout')
@login_required
def web_logout():
    logout_user()
    return redirect('/')
