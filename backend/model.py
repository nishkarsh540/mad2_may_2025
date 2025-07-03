from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)        
    role = db.Column(db.String(20), nullable=False, default='user')
    # 'user','admin'

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))


with app.app_context():

    db.create_all()

    if User.query.filter_by(username='admin').first() is None:
        admin_password = generate_password_hash('admin123')
        admin = User(username='admin',email='admin@grocery.com',password=admin_password,role='admin')

        db.session.add(admin)
        db.session.commit()

    else:
        print("Admin user already exists.")