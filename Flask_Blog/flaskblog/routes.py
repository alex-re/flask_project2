from flaskblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post  # it has to be AFTER creating "db"
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
# from hashlib import sha256
from PIL import Image
# from PIL import ImageFilter


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
    if current_user.is_authenticated:
        flash(f'You have already loged in as {current_user.username}', 'info')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))  # note: `url_for` gets the FUNCTION NAME
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash(f'You have already loged in as {current_user.username}', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # remember=[True-False]
            next_page = request.args.get('next')  # (args is dict class) if no parameter named "next" it will pass None
            # flash("You have been loged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logout.', 'dark')
    return redirect(url_for('home'))


def save_picture(form_picture):
    ''' we wantrandom file name '''
    random_hex = secrets.token_hex(8)
    # random_hex = os.urandom(64).decode('latin1')
    f_name, f_ext = os.path.splitext(form_picture.filename)  # f_ext -> file extetion
    # del f_name  # for memmory saving
    picture_fn = random_hex + f_ext  # picture file name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    resized_img = Image.open(form_picture)
    resized_img.thumbnail(output_size)
    # resized_img.rotate(90)  # 90 degrees
    # resized_img.filter(ImageFilter.GaussianBlur(15))

    resized_img.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

            last_img = os.path.join(app.root_path, 'static/profile_pics/', current_user.image_file)
            if os.path.exists(last_img) and not last_img.endswith('default.png'):
                os.remove(last_img)
            # else:
                # raise NameError(last_img)

            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':  # about browser message: "are you shure you want submit again?"
        form.username.data == current_user.username
        form.email.data == current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title=f'Account {current_user.username}', image_file=image_file, form=form)
