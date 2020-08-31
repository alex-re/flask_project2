from flaskblog import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)  # we will hash passwords
    posts = db.relationship('Post', backref='author', lazy=True)  # upper case because it hints to a "class"

    def __repr__(self):  # like __str__
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # lower case because it hints to a "table name and a column name"

    def __repr__(self):  # like __str__
        return f"Post('{self.title}', '{self.date_posted}')"
#  from flaskblog import db  # (with a lot output :)
#  db.create_all()  # db.drop_all()
