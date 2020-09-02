from flaskblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post  # it has to be AFTER creating "db"
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
# from hashlib import sha256
from PIL import Image
# from PIL import ImageFilter


# posts = [{'author': 'ali', 'title': 'Blog Post 1', 'content': 'First post content', 'date_posted': 'April 20, 2018'},
    # {'author': 'gholi','title': 'Blog Post 2','content': 'Second post content','date_posted': 'April 20, 2020'}]


@app.route("/")
@app.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get('page', 1, type=int)  # default value is 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)  # order_by for reversing.
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


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form, title='New Post', legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title=post.title, post=post, form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()    
    
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    
    return render_template('user_posts.html', posts=posts, user=user, title=user.username)
