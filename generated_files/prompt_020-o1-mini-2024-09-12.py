# app.py

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import markdown
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content_markdown = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PostHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content_markdown = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

@app.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('admin_dashboard.html', posts=posts)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content_markdown = request.form['content']
        content_html = markdown.markdown(content_markdown, extensions=['fenced_code'])
        new_post = Post(title=title, content_markdown=content_markdown, content_html=content_html)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('new_post.html')

@app.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        # Save current state to history
        history = PostHistory(
            post_id=post.id,
            title=post.title,
            content_markdown=post.content_markdown,
            content_html=post.content_html
        )
        db.session.add(history)
        
        # Update post
        post.title = request.form['title']
        post.content_markdown = request.form['content']
        post.content_html = markdown.markdown(post.content_markdown, extensions=['fenced_code'])
        post.timestamp = datetime.utcnow()
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_post.html', post=post)

@app.route('/admin/history/<int:post_id>')
@login_required
def post_history(post_id):
    histories = PostHistory.query.filter_by(post_id=post_id).order_by(PostHistory.timestamp.desc()).all()
    return render_template('post_history.html', histories=histories, post_id=post_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Initialize Admin User
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        new_user = User(username='admin', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blogging Platform</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
        {% endif %}
    </nav>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

```html
<!-- templates/index.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Blog Posts</h1>
    {% for post in posts %}
        <div class="post">
            <h2><a href="{{ url_for('post_view', post_id=post.id) }}">{{ post.title }}</a></h2>
            <p>Published on {{ post.timestamp.strftime('%Y-%m-%d %H:%M') }}</p>
            <div>{{ post.content_html|safe }}</div>
        </div>
        <hr>
    {% else %}
        <p>No posts available.</p>
    {% endfor %}
{% endblock %}
```

```html
<!-- templates/post.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>{{ post.title }}</h1>
    <p>Published on {{ post.timestamp.strftime('%Y-%m-%d %H:%M') }}</p>
    <div>{{ post.content_html|safe }}</div>
{% endblock %}
```

```html
<!-- templates/admin_dashboard.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Admin Dashboard</h1>
    <a href="{{ url_for('new_post') }}">Create New Post</a>
    <h2>All Posts</h2>
    <ul>
        {% for post in posts %}
            <li>
                <a href="{{ url_for('post_view', post_id=post.id) }}">{{ post.title }}</a>
                - <a href="{{ url_for('edit_post', post_id=post.id) }}">Edit</a>
                - <a href="{{ url_for('post_history', post_id=post.id) }}">History</a>
                - Published on {{ post.timestamp.strftime('%Y-%m-%d %H:%M') }}
            </li>
        {% else %}
            <li>No posts available.</li>
        {% endfor %}
    </ul>
{% endblock %}
```

```html
<!-- templates/new_post.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Create New Post</h1>
    <form method="POST">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" required><br><br>
        
        <label for="content">Content (Markdown):</label><br>
        <textarea id="content" name="content" rows="10" cols="50" required></textarea><br><br>
        
        <input type="submit" value="Create Post">
    </form>
    <h2>Live Preview</h2>
    <div id="preview"></div>
    <script>
        const textarea = document.getElementById('content');
        const preview = document.getElementById('preview');

        textarea.addEventListener('input', function() {
            preview.innerHTML = marked.parse(textarea.value);
        });

        // Initialize preview
        preview.innerHTML = marked.parse(textarea.value);
    </script>
{% endblock %}
```

```html
<!-- templates/edit_post.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Edit Post</h1>
    <form method="POST">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" value="{{ post.title }}" required><br><br>
        
        <label for="content">Content (Markdown):</label><br>
        <textarea id="content" name="content" rows="10" cols="50" required>{{ post.content_markdown }}</textarea><br><br>
        
        <input type="submit" value="Update Post">
    </form>
    <h2>Live Preview</h2>
    <div id="preview"></div>
    <script>
        const textarea = document.getElementById('content');
        const preview = document.getElementById('preview');

        textarea.addEventListener('input', function() {
            preview.innerHTML = marked.parse(textarea.value);
        });

        // Initialize preview
        preview.innerHTML = marked.parse(textarea.value);
    </script>
{% endblock %}
```

```html
<!-- templates/post_history.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Post History for Post ID: {{ post_id }}</h1>
    <ul>
        {% for history in histories %}
            <li>
                <strong>{{ history.title }}</strong>
                - {{ history.timestamp.strftime('%Y-%m-%d %H:%M') }}
                <div>{{ history.content_html|safe }}</div>
            </li>
            <hr>
        {% else %}
            <li>No history available.</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('admin_dashboard') }}">Back to Dashboard</a>
{% endblock %}
```

```html
<!-- templates/login.html -->

{% extends 'base.html' %}
{% block content %}
    <h1>Admin Login</h1>
    <form method="POST">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        
        <input type="submit" value="Login">
    </form>
{% endblock %}
```

```css
/* static/styles.css */

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

nav {
    background-color: #333;
    padding: 1em;
}

nav a {
    color: #fff;
    margin-right: 1em;
    text-decoration: none;
}

.container {
    padding: 2em;
}

.flash {
    padding: 1em;
    margin-bottom: 1em;
}

.flash.success {
    background-color: #d4edda;
    color: #155724;
}

.flash.danger {
    background-color: #f8d7da;
    color: #721c24;
}

textarea {
    width: 100%;
    font-family: monospace;
}
```

```bash
# requirements.txt

Flask
Flask-Login
Flask-Bcrypt
Flask-SQLAlchemy
markdown
```

**Instructions to Run the Application:**

1. **Create a Project Directory:**
   ```bash
   mkdir blogging_platform
   cd blogging_platform
   ```

2. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Create `requirements.txt` and Install Dependencies:**
   Save the `requirements.txt` content provided above into a file named `requirements.txt`, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the Directory Structure:**
   ```bash
   mkdir templates static
   ```

5. **Add Files:**
   - Save the respective HTML templates into the `templates` folder.
   - Save the CSS into `static/styles.css`.
   - Save `app.py` in the root directory.

6. **Run the Application:**
   ```bash
   python app.py
   ```

7. **Access the Application:**
   Open your browser and navigate to `http://127.0.0.1:5000`.

**Default Admin Credentials:**
- **Username:** admin
- **Password:** admin
