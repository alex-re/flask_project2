from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
# import secrets; secret.token_hex(16)  # argiuments (16) is optional.
app.config["SECRET_KEY"] = '8e6880f71e7fb8ad8e502554b1e8a244'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # FUNCTION NAME
login_manager.login_message = "please first login"
login_manager.login_message_category = 'warning'

from flaskblog import routes  # here because preventional of circular import.
