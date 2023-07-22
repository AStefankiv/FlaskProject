from flask import Flask, request, redirect, abort, render_template, session, url_for, jsonify
import random
from flask_sqlalchemy import SQLAlchemy
import re
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HW_35/instance/db.sqlite'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('purchases', lazy=True))
    book = db.relationship('Book', backref=db.backref('purchases', lazy=True))

    def __repr__(self):
        return f"<Purchase {self.id}>"


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_data)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "email": user.email})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    books_data = [{"id": book.id, "title": book.title, "author": book.author, "price": book.price} for book in books]
    return jsonify(books_data)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({"id": book.id, "title": book.title, "author": book.author, "price": book.price})
    else:
        return jsonify({"message": "Book not found"}), 404

@app.route('/purchases', methods=['GET'])
def get_all_purchases():
    purchases = Purchase.query.all()
    purchases_data = [{"id": purchase.id, "user_id": purchase.user_id, "book_id": purchase.book_id, "purchase_date": purchase.purchase_date} for purchase in purchases]
    return jsonify(purchases_data)

@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase_by_id(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        return jsonify({"id": purchase.id, "user_id": purchase.user_id, "book_id": purchase.book_id, "purchase_date": purchase.purchase_date})
    else:
        return jsonify({"message": "Purchase not found"}), 404
