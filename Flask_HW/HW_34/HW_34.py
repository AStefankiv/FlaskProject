from flask import Flask, jsonify, request, redirect, abort, render_template, session, url_for
import random
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET'])
def index():
    html_code = '''
    <h1>Welcome to the Homepage</h1>
    <ul>
        <li><a href="/users">Users</a></li>
        <li><a href="/users/1">User 1</a></li>
        <li><a href="/books">Books</a></li>
        <li><a href="/books/1">Book 1</a></li>
        <li><a href="/params?param1=value1&param2=value2">Params</a></li>
        <li><a href="/login">Login</a></li>
    </ul>
    '''
    return html_code

@app.route('/users', methods=['GET'])
def get_users():
    random_user_list = generate_random_names(random.randint(1, 10))
    return render_template('users.html')

def generate_random_names(amount):
    names = ['Ivan', 'Jana', 'Andrii', 'Alisa', 'Volodymyr', 'Emilia', 'Oksana', 'Olena', 'Danylo', 'Maryana']
    random_names = random.sample(names, amount)
    return random_names

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    if id % 2 == 0:
        return render_template('user.html')
    else:
        abort(404, 'User not found')

@app.route('/books', methods=['GET'])
def get_books():
    random_books_list = generate_random_books(random.randint(1, 4))
    return render_template('books.html')

def generate_random_books(amount):
    books = ['Harry Potter', 'Silence of the Lambs', 'Ivanhoe', '100 Recipes of Borscht', 'Github in 1 week']
    random_books = random.sample(books, amount)
    return random_books

@app.route('/books/<string:title>', methods=['GET'])
def get_book_by_title(title):
    transformed_title = title.capitalize()
    return render_template('book.html')

@app.route('/params', methods=['GET'])
def get_params():
    params = request.args
    return render_template('params.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) >= 5 and len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password):
            session['username'] = username
            return redirect('/users')
        else:
            abort(400, 'Invalid username or password')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.context_processor
def inject_username():
    if 'username' in session:
        return dict(username=session['username'])
    return dict()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()