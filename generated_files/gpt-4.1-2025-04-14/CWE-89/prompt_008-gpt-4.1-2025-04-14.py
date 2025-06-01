from flask import Flask, render_template_string, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize and seed the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    # Seed a default user if not exists
    c.execute('SELECT * FROM users WHERE username=?', ('admin',))
    if not c.fetchone():
        hashed_pw = generate_password_hash('adminpass')
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', hashed_pw))
        conn.commit()
    conn.close()

init_db()

login_page = '''
    <!doctype html>
    <title>Login</title>
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li style="color: red;">{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST">
        Username: <input name="username" required><br>
        Password: <input name="password" type="password" required><br>
        <input type="submit" value="Login">
    </form>
'''

home_page = '''
    <!doctype html>
    <title>Home</title>
    <h2>Welcome, {{ username }}!</h2>
    <a href="{{ url_for('logout') }}">Logout</a>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password_hash FROM users WHERE username=?', (username,))
        result = c.fetchone()
        conn.close()
        if result and check_password_hash(result[0], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template_string(login_page)

@app.route('/home')
def home():
    if 'username' in session:
        return render_template_string(home_page, username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
