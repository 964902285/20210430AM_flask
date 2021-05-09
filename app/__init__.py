# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         __init__.py
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/5/9 21:45
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import settings

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(settings.DevelopmentConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You must login to use this page!"
login_manager.login_message_category = 'info'

from app.routes import *

# print('DEBUG:', app.config.get('DEBUG'))
#
# print('TESTING:', app.config.get('TESTING'))
#
# print('DATABASE_URI:', app.config.get('DATABASE_URI'))
