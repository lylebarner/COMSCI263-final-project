# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.title}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search', '')
        posts = Post.query.filter(
            Post.title.contains(search_query) | Post.content.contains(search_query)
        ).order_by(Post.created_at.desc()).all()
    else:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Forum</title>
</head>
<body>
    <h1>Forum Posts</h1>
    <form method="POST">
        <input type="text" name="search" placeholder="Search posts">
        <button type="submit">Search</button>
        <a href="{{ url_for('create') }}">Create New Post</a>
    </form>
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post.title }}</h2>
                <p>{{ post.content }}</p>
                <small>Posted on {{ post.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
            </li>
        {% else %}
            <li>No posts found.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

```html
<!-- templates/create.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Create New Post</title>
</head>
<body>
    <h1>Create a New Post</h1>
    <form method="POST">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" required><br><br>
        <label for="content">Content:</label><br>
        <textarea id="content" name="content" rows="5" cols="40" required></textarea><br><br>
        <button type="submit">Submit</button>
        <a href="{{ url_for('index') }}">Back to Posts</a>
    </form>
</body>
</html>