from flask import Flask, request, render_template_string, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = 'forum.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, content TEXT, created TIMESTAMP)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        content = request.form['content']
        if content:
            conn.execute('INSERT INTO posts (content, created) VALUES (?, ?)', (content, datetime.now()))
            conn.commit()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template_string('''
        <!doctype html>
        <title>Forum</title>
        <h1>Simple Forum</h1>
        <form method="post">
            <textarea name="content"></textarea>
            <input type="submit" value="Add Post">
        </form>
        <ul>
        {% for post in posts %}
            <li>{{ post['created'] }} - {{ post['content'] }}</li>
        {% else %}
            <li>No posts yet!</li>
        {% endfor %}
        </ul>
    ''', posts=posts)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts WHERE content LIKE ?', ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template_string('''
        <!doctype html>
        <title>Search Results</title>
        <h1>Search Results</h1>
        <form method="get" action="{{ url_for('search') }}">
            <input type="text" name="query" value="{{ request.args.get('query') }}">
            <input type="submit" value="Search">
        </form>
        <ul>
        {% for post in posts %}
            <li>{{ post['created'] }} - {{ post['content'] }}</li>
        {% else %}
            <li>No posts found.</li>
        {% endfor %}
        </ul>
        <a href="{{ url_for('index') }}">Back to Home</a>
    ''', posts=posts, request=request)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)