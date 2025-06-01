from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_cms.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default="user")
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='posts')

# Utils
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            return "Not authorized", 403
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route("/init-db")
def init_db():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin_user = User(username="admin", email="admin@example.com", role="admin")
        admin_user.set_password("admin")
        db.session.add(admin_user)
        db.session.commit()
    return "DB Initialized and admin created."

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('admin_panel'))
        return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route("/admin", methods=["GET"])
@admin_required
def admin_panel():
    return render_template_string(ADMIN_TEMPLATE)

@app.route("/admin/users", methods=["GET","POST"])
@admin_required
def admin_users():
    filters = {}
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        role = request.form.get("role")
        query = User.query
        if username:
            query = query.filter(User.username.contains(username))
        if email:
            query = query.filter(User.email.contains(email))
        if role:
            query = query.filter(User.role == role)
        users = query.all()
    else:
        users = User.query.all()
    return render_template_string(USERS_TEMPLATE, users=users)

@app.route("/admin/posts", methods=["GET","POST"])
@admin_required
def admin_posts():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        date_from = request.form.get("date_from")
        date_to = request.form.get("date_to")
        query = Post.query
        if title:
            query = query.filter(Post.title.contains(title))
        if author:
            query = query.join(User).filter(User.username.contains(author))
        if date_from:
            try:
                dt = datetime.strptime(date_from, "%Y-%m-%d")
                query = query.filter(Post.timestamp >= dt)
            except:
                pass
        if date_to:
            try:
                dt = datetime.strptime(date_to, "%Y-%m-%d")
                query = query.filter(Post.timestamp <= dt)
            except:
                pass
        posts = query.all()
    else:
        posts = Post.query.all()
    return render_template_string(POSTS_TEMPLATE, posts=posts)

# --- Templates ---

LOGIN_TEMPLATE = """
<!DOCTYPE html><html>
<head><title>Login</title></head>
<body>
<h2>Login</h2>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<form method="post">
Username: <input type="text" name="username" /><br>
Password: <input type="password" name="password" /><br>
<input type="submit" value="Login" />
</form>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html><html>
<head><title>Admin Panel</title></head>
<body>
<h1>Admin Panel</h1>
<ul>
    <li><a href="{{ url_for('admin_users') }}">User Search</a></li>
    <li><a href="{{ url_for('admin_posts') }}">Post Search</a></li>
    <li><a href="{{ url_for('logout') }}">Logout</a></li>
</ul>
</body>
</html>
"""

USERS_TEMPLATE = """
<!DOCTYPE html><html>
<head><title>User Search</title></head>
<body>
<h2>User Search</h2>
<form method="post">
    Username: <input type="text" name="username">
    Email: <input type="text" name="email">
    Role: <select name="role">
      <option value="">Any</option>
      <option value="admin">Admin</option>
      <option value="user">User</option>
    </select>
    <input type="submit" value="Search">
</form>
<table border="1">
<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>
{% for user in users %}
<tr>
<td>{{user.id}}</td><td>{{user.username}}</td><td>{{user.email}}</td><td>{{user.role}}</td>
</tr>
{% endfor %}
</table>
<a href="{{url_for('admin_panel')}}">Back to admin</a>
</body>
</html>
"""

POSTS_TEMPLATE = """
<!DOCTYPE html><html>
<head><title>Post Search</title></head>
<body>
<h2>Post Search</h2>
<form method="post">
    Title: <input type="text" name="title">
    Author: <input type="text" name="author">
    Date from: <input type="date" name="date_from">
    Date to: <input type="date" name="date_to">
    <input type="submit" value="Search">
</form>
<table border="1">
<tr><th>ID</th><th>Title</th><th>Author</th><th>Date</th></tr>
{% for post in posts %}
<tr>
<td>{{post.id}}</td>
<td>{{post.title}}</td>
<td>{{post.author.username}}</td>
<td>{{post.timestamp.strftime('%Y-%m-%d')}}</td>
</tr>
{% endfor %}
</table>
<a href="{{url_for('admin_panel')}}">Back to admin</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)