from . import auth
from flask import redirect, render_template, url_for, flash, request
from .forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, login_required
from .. import db
from ..models import User



@auth.route('/signup', methods=['POST','GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login')) 
    return render_template('auth/signup.html', form = form)


@auth.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main.home'))
        flash('Invalid username or Password', "danger")
                
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))