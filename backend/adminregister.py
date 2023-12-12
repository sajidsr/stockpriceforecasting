from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
import sqlalchemy
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

from models import db,Admin

adminregister = Blueprint('adminregister', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(adminregister)

@adminregister.route('/adminregister', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if fname and lname and username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Admin(
                        firstName=fname,
                        lastName=lname,
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('adminregister.show') + '?error=user-or-email-exists')

                return redirect(url_for('adminlogin.show') + '?success=account-created')
        else:
            return redirect(url_for('adminregister.show') + '?error=missing-fields')
    else:
        return render_template('adminregister.html')
