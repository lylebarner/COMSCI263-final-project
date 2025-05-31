# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_content = ''
    if request.method == 'POST':
        html_content = request.form.get('email_content', '')
    return render_template('index.html', html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Email Editor with Live Preview</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            display: flex;
            gap: 20px;
        }
        .form-container, .preview-container {
            width: 50%;
        }
        textarea {
            width: 100%;
            height: 300px;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
        }
        .preview {
            border: 1px solid #ccc;
            padding: 10px;
            min-height: 300px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <h1>Email Editor with Live Preview</h1>
    <form method="POST">
        <label for="email_content">Write your email in HTML:</label><br>
        <textarea id="email_content" name="email_content" placeholder="Enter HTML content here...">{{ html_content }}</textarea><br><br>
        <button type="submit">Preview Email</button>
    </form>

    {% if html_content %}
    <h2>Live Preview:</h2>
    <div class="preview">
        {{ html_content | safe }}
    </div>
    {% endif %}
</body>
</html>