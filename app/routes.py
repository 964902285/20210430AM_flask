# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         routes
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/5/9 21:47
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm
from app.models import User
from app.emails import send_reset_password_mail

import os
import time
import cv2

from app import app, bcrypt, db

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()  # 把格式转为字符串。
    return img_stream


@app.route('/')
@login_required
def index():
    img_index = [1, 2]
    img_lis = []
    title = "Flask&Mysql collect web"
    for i in os.listdir("app/static/imgs/"):

        img_path = f"app/static/imgs/{i}"
        img_stream = return_img_stream(img_path)

        img_lis.append(img_stream)

    return render_template("index.html", title=title, data=img_index, img_stream=img_lis)


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
        flash("user not exit or password not match!!try again.", category="danger")
    return render_template("login.html", title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'app/static/imgs',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'app/static/imgs', 'test.jpg'), img)

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    title = "send reset password request."
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('password reset request is sent to your mail, please check yout mailbox.', category='info')
    return render_template('send_password_reset_request.html', form=form, title=title)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    title = "reset password."
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            password = bcrypt.generate_password_hash(form.password.data)
            user.password = password
            db.session.commit()
            flash('your password reset success!!please login with new password now!!', category='info')
            return redirect(url_for('login'))
        else:
            flash('the user is not exist.', category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form, title=title)
