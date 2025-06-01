from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import markdown
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_should_be_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# -- Models --
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content_md = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# -- Authentication --
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"  # For demo; change in production

def is_logged_in():
    return session.get('logged_in', False)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template_string('''
    <h2>Admin Login</h2>
    <form method="post">
        <input name="username" type="text" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    ''')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

# -- Admin Dashboard --
@app.route('/admin')
def admin_dashboard():
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template_string('''
    <h1>Admin Dashboard</h1>
    <a href="{{ url_for('admin_new_post') }}">&#x2795; New Post</a> | 
    <a href="{{ url_for('admin_logout') }}">Logout</a>
    <hr>
    <h2>Post History</h2>
    <ul>
      {% for post in posts %}
        <li>
          <strong>{{ post.title }}</strong> 
          <em>({{ post.timestamp.strftime("%Y-%m-%d %H:%M") }})</em>
          [<a href="{{ url_for('view_post', post_id=post.id) }}" target="_blank">View</a>]
        </li>
      {% else %}
        <li>No posts yet.</li>
      {% endfor %}
    </ul>
    ''', posts=posts)

# -- Create New Post (Markdown with live preview) --
@app.route('/admin/new', methods=['GET', 'POST'])
def admin_new_post():
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title'].strip()
        content_md = request.form['content_md']
        content_html = markdown.markdown(content_md, extensions=['fenced_code', 'codehilite'])
        post = Post(title=title, content_md=content_md, content_html=content_html)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template_string('''
    <h2>New Post</h2>
    <a href="{{ url_for('admin_dashboard') }}">&#x25C0; Back to Dashboard</a><hr>
    <form method="post" oninput="updatePreview()">
        <input name="title" type="text" placeholder="Title" style="width:98%;" required><br><br>
        <div style="display:flex;">
            <div style="width:50%;">
                <strong>Markdown:</strong><br>
                <textarea id="md_input" name="content_md" rows="20" style="width:98%;" required oninput="updatePreview()"></textarea>
            </div>
            <div style="width:50%;padding-left:20px;">
                <strong>Live Preview:</strong>
                <div id="preview" style="border:1px solid #ddd;background:#fafafa;min-height:320px;padding:10px;"></div>
            </div>
        </div>
        <br>
        <button type="submit">Publish Post</button>
    </form>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
    function updatePreview() {
        var md = document.getElementById('md_input').value;
        document.getElementById('preview').innerHTML = marked.parse(md);
    }
    document.addEventListener('DOMContentLoaded', updatePreview);
    </script>
    ''')

# -- Public Post View --
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template_string('''
    <h1>{{ post.title }}</h1>
    <em>Posted: {{ post.timestamp.strftime("%Y-%m-%d %H:%M") }}</em>
    <hr>
    <div>{{ post.content_html | safe }}</div>
    <hr>
    <a href="{{ url_for('index') }}">&#x25C0; All Posts</a>
    ''', post=post)

# -- Public Index --
@app.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template_string('''
    <h1>Blog</h1>
    <ul>
      {% for post in posts %}
        <li>
          <a href="{{ url_for('view_post', post_id=post.id) }}">{{ post.title }}</a>
          <em>({{ post.timestamp.strftime("%Y-%m-%d %H:%M") }})</em>
        </li>
      {% else %}
        <li>No posts yet.</li>
      {% endfor %}
    </ul>
    <hr>
    <a href="{{ url_for('admin_login') }}">Admin Login</a>
    ''' , posts=posts)

# -- DB Initialize Helper --
@app.cli.command('initdb')
def initdb():
    db.create_all()
    print('Database initialized.')

if __name__ == "__main__":
    if not os.path.exists('blog.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)