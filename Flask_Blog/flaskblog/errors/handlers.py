from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', error=error), 404  # default is 200 success.


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', error=error), 403


@errors.app_errorhandler(500)
def error_500(error):
    # report email
    return render_template('errors/500.html', error=error), 500
