from flask import Blueprint, render_template,session
from flask_login import LoginManager, login_required, current_user

from models import db, Admin,Query

adminindex = Blueprint('adminindex', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(adminindex)

@adminindex.route('/adminindex', methods=['GET'])
@login_required
def show():
    table = Query.query.all()
    username = session.get('username')
    return render_template('adminindex.html',username=username,table=table)