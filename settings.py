# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         settings
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/4/30 0:48
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/20210430AM_flask'  # 数据库信息
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # flask 谷歌邮件配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    # MAIL_USE_TLS: False
    # MAIL_USE_SSL = True
    MAIL_USERNAME = 'xxhlovingcoding@gmail.com'
    MAIL_PASSWORD = 'iayiay111'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
