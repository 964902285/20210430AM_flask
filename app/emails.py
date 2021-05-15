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
from threading import Thread

from app import mail, app


def send_async_mail(app, msg):  # 开启线程加速邮件发送，目的是让前端页面不要等待邮件发送完毕而一直在刷新
    with app.app_context():
        mail.send(msg)


def send_reset_password_mail(user, token):
    msg = Message('reset your password',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email],
                  html=render_template(
                      'reset_password_mail.html',
                      token=token, user=user
                  ))
    # mail.send(msg)
    Thread(target=send_async_mail, args=(app, msg)).start()
