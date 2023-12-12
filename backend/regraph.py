from flask import Blueprint, render_template
from flask_login import LoginManager, login_required


regraph = Blueprint('regraph', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(regraph)

@regraph.route('/regraph', methods=['GET'])
@login_required
def show():
    return render_template('regraph.html')