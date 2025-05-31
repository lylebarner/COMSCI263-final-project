# app.py
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content:
            comment = Comment(content=content)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('index'))
    comments = Comment.query.all()
    return render_template('index.html', comments=comments, markdown=markdown)

@app.route('/like/<int:comment_id>', methods=['POST'])
def like(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Comments App</title>
</head>
<body>
    <h1>Post a Comment</h1>
    <form method="POST">
        <textarea name="content" rows="4" cols="50" required></textarea><br>
        <button type="submit">Submit</button>
    </form>
    <h2>Comments</h2>
    {% for comment in comments %}
        <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
            <div>{{ markdown(comment.content)|safe }}</div>
            <form action="{{ url_for('like', comment_id=comment.id) }}" method="POST" style="display:inline;">
                <button type="submit">Like</button> {{ comment.likes }}
            </form>
        </div>
    {% endfor %}
</body>
</html>