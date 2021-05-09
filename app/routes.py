# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         routes
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/5/9 21:47
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from forms import RegisterForm, LoginForm
from models import User

import settings
from app import app, bcrypt, db


@app.route('/')
@login_required
def index():
    lis = [
        'A1',
        'A2',
        'A3'
    ]
    title = "flask web app home."
    return render_template("index.html", title=title, data=lis)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "register page."
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)  # 哈希加密密码
        email = form.email.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("register success!", category="success")
        return redirect(url_for('login'))
    return render_template("register.html", title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "login page."
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # check password
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash("login success!", category="info")
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash("user not exit or password not match!!", category="danger")
    return render_template("login.html", title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
