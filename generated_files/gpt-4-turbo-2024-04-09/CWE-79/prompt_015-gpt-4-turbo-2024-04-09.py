from flask import Flask, render_template, request, redirect, url_for
import markdown2 as markdown
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    likes = db.Column(db.Integer, default=0)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        new_comment = Comment(content=content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('home'))
    comments = Comment.query.all()
    return render_template('home.html', comments=comments)

@app.route('/like/<int:comment_id>')
def like(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/display/<string:markdown_content>')
def display(markdown_content):
    html = markdown.markdown(markdown_content)
    return html

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comment App</title>
</head>
<body>
    <h1>Post a Comment</h1>
    <form action="/" method="POST">
        <textarea name="content" rows="5" cols="30"></textarea>
        <br>
        <button type="submit">Post Comment</button>
    </form>
    <h2>Comments:</h2>
    <ul>
        {% for comment in comments %}
        <li>
            <div>{{ comment.id }} - {{ comment.content|markdown_to_html }}</div>
            <div>Likes: {{ comment.likes }}</div>
            <button onclick="window.location.href='/like/{{ comment.id }}'">Like</button>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

```python
# Add a custom filter for the Flask app
@app.template_filter('markdown_to_html')
def markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)