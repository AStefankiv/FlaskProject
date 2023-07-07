from flask import Flask, jsonify, request, redirect, abort, render_template
import random
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    html_code = '''
    <h1>Welcome to the Homepage</h1>
    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/users">Users</a></li>
        <li><a href="/books">Books</a></li>
        <li><a href="/params">Params</a></li>
    </ul>
    '''
    return html_code

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
    books = ['Harry Potter', 'Silence of the Lambs', 'Ivanhoe', '100 Recipes of Borscht', 'Github in 1 week']
    random_books = random.sample(books, amount)
    book_list_html = ''
    for book in random_books:
        book_list_html += '<li>' + book + '</li>'
    return book_list_html

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    if id % 2 == 0:
        return f'User {id} was found.'
    else:
        abort(404, 'User not found')

@app.route('/books/<string:title>', methods=['GET'])
def get_book_by_title(title):
    transformed_title = title.capitalize()
    return transformed_title

@app.route('/params', methods=['GET'])
def get_params():
    params = request.args
    html_table = '<table><tr><th>parameter</th><th>value</th></tr>'
    for key, value in params.items():
        html_table += f'<tr><td>{key}</td><td>{value}</td></tr>'
    html_table += '</table>'
    return html_table

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        login_form = '''
        <form method="POST" action="/login">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <input type="submit" value="Submit">
        </form>
        '''
        return login_form
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) >= 5 and len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password):
            return redirect('/users')
        else:
            abort(400, 'Invalid username or password')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
