# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         test
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/5/15 16:59
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from app.models import User
from app import app


user = User.query.all()[0]
print(user)
with app.app_context():
    token = user.generate_reset_password_token()
    print(token)

with app.app_context():
    print(user.check_reset_password_token(token))
