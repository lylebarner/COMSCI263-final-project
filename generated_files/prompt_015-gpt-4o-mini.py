from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)

db.create_all()

@app.route('/')
def index():
    comments = Comment.query.all()
    return render_template('index.html', comments=comments)

@app.route('/post_comment', methods=['POST'])
def post_comment():
    content = request.form['content']
    new_comment = Comment(content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown(text)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Comments</title>
</head>
<body>
    <h1>Comments</h1>
    <form action="/post_comment" method="POST">
        <textarea name="content" rows="4" cols="50" placeholder="Write your comment here..." required></textarea><br>
        <button type="submit">Post Comment</button>
    </form>
    <hr>
    {% for comment in comments %}
        <div>
            <div>{{ comment.content|markdown }}</div>
            <button formmethod="POST" formaction="/like_comment/{{ comment.id }}">Like</button> 
            <span>{{ comment.likes }} likes</span>
        </div>
        <hr>
    {% endfor %}
</body>
</html>