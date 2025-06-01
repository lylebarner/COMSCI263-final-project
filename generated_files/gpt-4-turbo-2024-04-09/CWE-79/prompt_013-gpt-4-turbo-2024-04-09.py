from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Assuming an in-memory list to store comments
comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)
        return redirect(url_for('index'))
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comment Page</title>
</head>
<body>
    <h1>Submit a comment</h1>
    <form method="post">
        <textarea name="comment" placeholder="Enter your comment"></textarea>
        <button type="submit">Submit Comment</button>
    </form>
    <h2>Comments</h2>
    <ul>
        {% for comment in comments %}
        <li>{{ comment }}</li>
        {% endfor %}
    </ul>
</body>
</html>