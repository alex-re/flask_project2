from flask import render_template, request, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)


# posts = [{'author': 'ali', 'title': 'Blog Post 1', 'content': 'First post content', 'date_posted': 'April 20, 2018'},
    # {'author': 'gholi','title': 'Blog Post 2','content': 'Second post content','date_posted': 'April 20, 2020'}]


@main.route("/")
@main.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get('page', 1, type=int)  # default value is 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)  # order_by for reversing.
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
