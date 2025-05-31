# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email = {}
    if request.method == 'POST':
        email['to'] = request.form.get('to', '')
        email['subject'] = request.form.get('subject', '')
        email['body'] = request.form.get('body', '')
    return render_template('index.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Composer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        form { margin-bottom: 20px; }
        .preview { border: 1px solid #ccc; padding: 10px; }
    </style>
</head>
<body>
    <h1>Compose Email</h1>
    <form method="post">
        <label for="to">To:</label><br>
        <input type="email" id="to" name="to" required><br><br>
        
        <label for="subject">Subject:</label><br>
        <input type="text" id="subject" name="subject" required><br><br>
        
        <label for="body">Body:</label><br>
        <textarea id="body" name="body" rows="10" cols="50" required></textarea><br><br>
        
        <input type="submit" value="Preview">
    </form>
    
    {% if email.to %}
    <h2>Preview:</h2>
    <div class="preview">
        <p><strong>To:</strong> {{ email.to }}</p>
        <p><strong>Subject:</strong> {{ email.subject }}</p>
        <p><strong>Body:</strong></p>
        <p>{{ email.body | nl2br }}</p>
    </div>
    {% endif %}
</body>
</html>
```

```python
# To handle the nl2br filter, add the following to app.py

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

def nl2br(value):
    return Markup("<br>".join(value.split('\n')))

app.jinja_env.filters['nl2br'] = nl2br