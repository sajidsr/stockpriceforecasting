   
from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
import sqlalchemy
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

from models import db,Query

contact = Blueprint('contact', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(contact)

@contact.route('/contact', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        if name and email and phone and message:
            
                try:
                    new_user = Query(
                        name=name,
                        email=email,
                        phone=phone,
                        message=message
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('contact.show') + '?error=enter-valid-input')

                return redirect(url_for('contact.show') + '?success=message-sent')
        else:
            return redirect(url_for('contact.show') + '?error=missing-fields')
    else:
        return render_template('contact.html')