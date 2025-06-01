from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

comments = []

template = '''
<!doctype html>
<title>Comment Page</title>
<h1>Leave a Comment</h1>
<form method="post">
  <input type="text" name="comment" required>
  <input type="submit" value="Submit">
</form>
<h2>Comments:</h2>
<ul>
  {% for c in comments %}
    <li>{{ c }}</li>
  {% endfor %}
</ul>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment', '').strip()
        if comment:
            comments.append(comment)
        return redirect(url_for('index'))
    return render_template_string(template, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)