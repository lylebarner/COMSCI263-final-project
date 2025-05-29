from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/admin')
def admin():
    posts = Post.query.all()
    return render_template('admin.html', posts=posts)

@app.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('admin'))
    return render_template('new_post.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('admin'))
    return render_template('edit_post.html', post=post)

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('admin'))

@app.route('/preview', methods=['POST'])
def preview():
    content = request.form['content']
    html_content = markdown.markdown(content)
    return render_template('preview.html', html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
```

**Templates Required:**

1. `templates/index.html`
2. `templates/admin.html`
3. `templates/new_post.html`
4. `templates/edit_post.html`
5. `templates/post.html`
6. `templates/preview.html`

### `templates/index.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
</head>
<body>
    <h1>Blog Posts</h1>
    {% for post in posts %}
        <h2><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
    {% endfor %}
    <a href="{{ url_for('admin') }}">Admin Dashboard</a>
</body>
</html>
```

### `templates/admin.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
</head>
<body>
    <h1>Admin Dashboard</h1>
    <a href="{{ url_for('new_post') }}">Create New Post</a>
    <h2>Post History</h2>
    {% for post in posts %}
        <h3>{{ post.title }}</h3>
        <a href="{{ url_for('edit_post', post_id=post.id) }}">Edit</a>
        <form action="{{ url_for('delete_post', post_id=post.id) }}" method="post" style="display:inline;">
            <button type="submit">Delete</button>
        </form>
    {% endfor %}
</body>
</html>
```

### `templates/new_post.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Post</title>
</head>
<body>
    <h1>Create New Post</h1>
    <form method="post">
        <input type="text" name="title" placeholder="Post Title" required>
        <textarea name="content" id="markdown" rows="10" placeholder="Write your post in Markdown" required></textarea>
        <button type="submit">Submit</button>
    </form>
    <h2>Preview</h2>
    <div id="preview"></div>
    <script>
        document.getElementById('markdown').addEventListener('input', function() {
            fetch('/preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({'content': this.value}),
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('preview').innerHTML = html;
            });
        });
    </script>
</body>
</html>
```

### `templates/edit_post.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Post</title>
</head>
<body>
    <h1>Edit Post</h1>
    <form method="post">
        <input type="text" name="title" value="{{ post.title }}" required>
        <textarea name="content" id="markdown" rows="10" required>{{ post.content }}</textarea>
        <button type="submit">Update</button>
    </form>
    <h2>Preview</h2>
    <div id="preview"></div>
    <script>
        document.getElementById('markdown').addEventListener('input', function() {
            fetch('/preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({'content': this.value}),
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('preview').innerHTML = html;
            });
        });
    </script>
</body>
</html>
```

### `templates/post.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <div>{{ post.content|safe }}</div>
    <a href="{{ url_for('admin') }}">Back to Admin Dashboard</a>
</body>
</html>
```

### `templates/preview.html`
```html
<div>{{ html_content|safe }}</div>