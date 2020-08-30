from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# import secrets; secret.token_hex(16)  # argiuments (16) is optional.
app.config["SECRET_KEY"] = '8e6880f71e7fb8ad8e502554b1e8a244'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # lower case because it hints to a "table name and a column name"

    def __repr__(self):  # like __str__
        return f"Post('{self.title}', '{self.date_posted}')"
#  from flaskblog import db  # (with a lot output :)
#  db.create_all()  # db.drop_all()
posts = [
    {
        'author': 'ali',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'gholi',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 20, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accont created for {form.username.data} !', 'success')
        return redirect(url_for('home'))  # note: `url_for` gets the FUNCTION NAME
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'abc123':
            flash("You have been loged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'danger')
    return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':
    app.run(debug=True) # port=int, host=...