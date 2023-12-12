from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)
    
class Query(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(12))
    message = db.Column(db.String(500))