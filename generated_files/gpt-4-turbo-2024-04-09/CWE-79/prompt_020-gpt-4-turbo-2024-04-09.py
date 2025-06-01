from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markdown2 import markdown
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Post {self.id}'

@app.route("/")
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("index.html", posts=posts)

@app.route("/dashboard")
def dashboard():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("dashboard.html", posts=posts)

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("create_post.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, content=markdown(post.content))

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_post.html', post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <title>Blog</title>
</head>
<body>
    <h1>Blog Posts</h1>
    <div>
        {% for post in posts %}
            <div class="post">
                <h2><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
                <p>Posted on: {{ post.date_posted.strftime('%Y-%m-%d') }}</p>
            </div>
        {% endfor %}
    </div>
</body>
</html>

<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <h1>Admin Dashboard</h1>
    <a href="{{ url_for('new_post') }}">Create New Post</a>
    <div>
        {% for post in posts %}
            <div class="post">
                <h3>{{ post.title }}</h3>
                <p>
                    <a href="{{ url_for('edit_post', post_id=post.id) }}">Edit</a> |
                    <form action="{{ url_for('delete_post', post_id=post.id) }}" method="post">
                        <button type="submit">Delete</button>
                    </form>
                </p>
            </div>
        {% endfor %}
    </div>
</body>
</html>

<!-- templates/create_post.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Create Post</title>
</head>
<body>
    <h1>Create a New Post</h1>
    <form action="{{ url_for('new_post') }}" method="post">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" required><br><br>
        <label for="content">Content (Markdown):</label>
        <textarea id="content" name="content" required></textarea><br><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>

<!-- templates/edit_post.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Post</title>
</head>
<body>
    <h1>Edit Post</h1>
    <form action="{{ url_for('edit_post', post_id=post.id) }}" method="post">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" value="{{ post.title }}" required><br><br>
        <label for="content">Content (Markdown):</label>
        <textarea id="content" name="content" required>{{ post.content }}</textarea><br><br>
        <button type="submit">Update</button>
    </form>
</body>
</html>

<!-- templates/post.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>{{ content|safe }}</p>
    <p>Posted on: {{ post.date_posted.strftime('%Y-%m-%d') }}</p>
</body>
</html>