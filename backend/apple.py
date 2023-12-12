
from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from models import db, Users

apple = Blueprint('apple', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(apple)

@apple.route('/apple', methods=['GET'])
@login_required
def show():
    return render_template('apple.html')