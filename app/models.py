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
from datetime import datetime

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


followers = db.Table(
    "followers",
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    extend_existing=True
)


# class Followers(db.Model):
#     __table_args__ = {'extend_existing': True}
#     db.Column('follower_id', db.Integer, db.ForeignKey('user_id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user_id'))


class User(db.Model, UserMixin):
    # __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    avatar_img = db.Column(db.String(120), default='/static/imgs/default-avatar.png', nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    post = db.relationship('Post', backref=db.backref('author', lazy=True))
    followed = db.relationship(
        "User", secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy=True), lazy=True
    )

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.count(user) > 0


class Post(db.Model):
    # __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(180), nullable=False)
    pub_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # return '<Post %r>' % self.body
        return '<Post {}>'.format(self.body)


if __name__ == "__main__":
    print("******** starting create database... ********")
    db.create_all()
    print("database created!!")
