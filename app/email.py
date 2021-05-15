"""
@File    : email.py
@Time    : 2021/5/15 9:27
@Author  : shroud.xu
@Description: 一个 ctrl c + v 工程师
@Email   : shroud.xu@cygia.com
@Software: PyCharm
"""
from flask_mail import Message
from flask import current_app, render_template

from app import mail


def send_reset_password_mail(user, token):
    msg = Message('reset your password', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email], html=render_template(
        'reset_password_mail.html', token=token, user=user
    ))
    mail.send(msg)
