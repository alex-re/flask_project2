from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

# import secrets; secret.token_hex(16)  # argiuments (16) is optional.
app.config["SECRET_KEY"] = '8e6880f71e7fb8ad8e502554b1e8a244'

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