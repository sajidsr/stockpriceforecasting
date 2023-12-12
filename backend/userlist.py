from flask import Blueprint, render_template,session
from flask_login import LoginManager, login_required, current_user

from models import db,Users

userlist = Blueprint('userlist', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(userlist)

@userlist.route('/userlist', methods=['GET'])
@login_required
def show():
    table = Users.query.all()
    username = session.get('username')
    return render_template('userlist.html',username=username,table=table)