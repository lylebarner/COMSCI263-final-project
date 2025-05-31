from flask import Flask, request, render_template_string

app = Flask(__name__)
comments = []

template = '''
<!doctype html>
<html lang="en">
<head>
    <title>Comment Page</title>
</head>
<body>
    <h1>Submit a Comment</h1>
    <form method="post">
        <textarea name="comment" rows="4" cols="50" required></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
    <h2>Comments:</h2>
    {% if comments %}
        <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No comments yet.</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)
    return render_template_string(template, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)