from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    random_user_list = generate_random_names(random.randint(1, 10))
    return jsonify(random_user_list)

def generate_random_names(amount):
    names = ['Ivan', 'Jana', 'Andrii', 'Alisa', 'Volodymyr', 'Emilia', 'Oksana', 'Olena', 'Danylo', 'Maryana']
    random_names = random.sample(names, amount)
    return random_names

@app.route('/books', methods=['GET'])
def get_books():
    random_books_list = generate_random_books(random.randint(1, 4))
    return '<ul>' + random_books_list + '</ul>'

def generate_random_books(amount):
    books = ['Harry Potter', 'Silence of the Lambs', 'Ivanhoe', '100 Recipes of Borscht']
    random_books = random.sample(books, amount)
    book_list_html = ''
    for book in random_books:
        book_list_html += '<li>' + book + '</li>'
    return book_list_html

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    if id % 2 == 0:
        return f'User was found: {id}'
    else:
        return 'Not Found', 404

@app.route('/books/<string:title>', methods=['GET'])
def get_book_by_title(title):
    transformed_title = title.capitalize()
    return transformed_title

if __name__ == '__main__':
    app.run()

## NOT FINISHED
