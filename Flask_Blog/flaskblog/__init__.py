# note: in each pakage `__init__.py` file says to python that it is a pakage.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'  # FUNCTION NAME
login_manager.login_message = "please first login"
login_manager.login_message_category = 'warning'


# from flaskblog import routes  # here because preventional of circular import.
from flaskblog.main.routes import main  # Blueprint
from flaskblog.users.routes import users  # Blueprint
from flaskblog.posts.routes import posts  # Blueprint

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
