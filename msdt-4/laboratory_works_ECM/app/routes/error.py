from flask import Blueprint, render_template

ERROR = Blueprint('error', __name__)

@ERROR.route('/error')
def index():
    return render_template('errors/base_error.html')

