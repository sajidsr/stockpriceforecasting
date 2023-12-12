from flask import Blueprint, url_for, render_template, redirect, request,session
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from models import db, Admin

adminlogin = Blueprint('adminlogin', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(adminlogin)

@adminlogin.route('/adminlogin', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()

        if admin:
            if check_password_hash(admin.password, password):
                login_user(admin)
                session['username'] = username  # Store the username in Flask session
                return redirect(url_for('adminindex.show',username=username))
            else:
                return redirect(url_for('adminlogin.show') + '?error=incorrect-password')
        else:
            return redirect(url_for('adminlogin.show') + '?error=user-not-found')
    else:
        return render_template('adminlogin.html')
