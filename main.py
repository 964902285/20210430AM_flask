# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         settings
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/4/30 0:20
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from app import app

if __name__ == "__main__":
    app.env = 'Development'
    app.run()
