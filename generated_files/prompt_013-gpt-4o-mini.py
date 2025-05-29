from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store comments in a list
comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)  # Add comment to the list
            return redirect(url_for('index'))  # Redirect to the same page
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comment Form</title>
</head>
<body>
    <h1>Submit a Comment</h1>
    <form method="POST">
        <textarea name="comment" required></textarea><br>
        <button type="submit">Submit</button>
    </form>
    <h2>Comments:</h2>
    <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% endfor %}
    </ul>
</body>
</html>