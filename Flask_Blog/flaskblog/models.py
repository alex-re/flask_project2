from flaskblog import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    # we write it manually to show login_manager how can it get user    
    return User.query.get(int(user_id))  # we must pass to get method the user "id" 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)  # we will hash passwords
    posts = db.relationship('Post', backref='author', lazy=True)  # upper case because it hints to a "class"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.secret_key, expires_sec)
        # s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id' : self.id}).decode('utf-8')  # generats token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token)['user_id']  # `s.loads` returns a dict
        except:
            return None
        return User.query.get(user_id)

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
