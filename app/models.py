# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         models
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/5/9 16:28
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask_login import UserMixin
from flask import current_app
import jwt

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_reset_password_token(self):
        return jwt.encode({'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_reset_password_token(token):  # 套上静态方法，就不用传入self参数（外部函数可以直接跳过该类的实例化对其进行调用）
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except:
            return


if __name__ == "__main__":
    print("******** starting create database... ********")
    db.create_all()
    print("database created!!")
