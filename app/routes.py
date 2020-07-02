from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from flask_login import  login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        user=User.query.filter_by(username=name).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid Username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password=generate_password_hash(form.password.data)
        email=form.email.data
        fname, lname = form.fname.data, form.lname.data
        user=User(username=username,
                password=password,
                email=email,
                fname=fname,
                lname=lname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    username=current_user.username
    return render_template('profile.html')