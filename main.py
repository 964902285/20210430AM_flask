# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         settings
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/4/30 0:20
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask import Flask

import settings

app = Flask(__name__)

app.config.from_object(settings.ProductionConfig)

print('DEBUG:', app.config.get('DEBUG'))

print('TESTING:', app.config.get('TESTING'))

print('DATABASE_URI:', app.config.get('DATABASE_URI'))