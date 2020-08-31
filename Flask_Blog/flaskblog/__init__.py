from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# import secrets; secret.token_hex(16)  # argiuments (16) is optional.
app.config["SECRET_KEY"] = '8e6880f71e7fb8ad8e502554b1e8a244'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)


from flaskblog import routes  # here because preventional of circular import.
