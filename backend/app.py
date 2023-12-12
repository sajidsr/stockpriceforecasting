from flask import Flask
import sqlalchemy
from flask_login import LoginManager

from models import db, Users

from index import index
from adminindex import adminindex
from about import about
from post import post
from contact import contact
from login import login
from logout import logout
from adminlogin import adminlogin
from adminlogout import adminlogout
from register import register
from adminregister import adminregister
from userlist import userlist
from regraph import regraph
from refresh import refresh
from home import home
from apple import apple

app = Flask(__name__, static_folder='../frontend/static')

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'

#app.config['SQLALCHEMY_BINDS'] = {'admin':'sqlite:///../admin.db'}

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(adminlogin)
app.register_blueprint(adminlogout)
app.register_blueprint(register)
app.register_blueprint(adminregister)
app.register_blueprint(userlist)
app.register_blueprint(refresh)
app.register_blueprint(regraph)
app.register_blueprint(home)
app.register_blueprint(adminindex)
app.register_blueprint(about)
app.register_blueprint(contact)
app.register_blueprint(post)
app.register_blueprint(apple)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




if __name__ == '__main__':
    from models import db
    with app.app_context():
     db.create_all()

    app.run()
