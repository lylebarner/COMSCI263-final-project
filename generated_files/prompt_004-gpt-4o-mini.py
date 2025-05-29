from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Post {self.id} by {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        new_post = Post(username=username, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/filter', methods=['GET'])
def filter_posts():
    username = request.args.get('username', '')
    posts = Post.query.filter(Post.username.contains(username)).all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Forum</title>
</head>
<body>
    <h1>Web Forum</h1>
    <form method="POST">
        <input type="text" name="username" placeholder="Your Name" required>
        <textarea name="content" placeholder="Your Post" required></textarea>
        <button type="submit">Post</button>
    </form>
    <hr>
    <h2>Filter Posts</h2>
    <form method="GET" action="{{ url_for('filter_posts') }}">
        <input type="text" name="username" placeholder="Filter by Username">
        <button type="submit">Filter</button>
    </form>
    <hr>
    <h2>Posts</h2>
    <ul>
        {% for post in posts %}
            <li><strong>{{ post.username }}:</strong> {{ post.content }}</li>
        {% endfor %}
    </ul>
</body>
</html>