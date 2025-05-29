from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    url = ''
    if request.method == 'POST':
        url = request.form['url']
    return render_template('index.html', url=url)

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
    <title>URL Input</title>
</head>
<body>
    <h1>Enter a URL</h1>
    <form method="post">
        <input type="text" name="url" required>
        <button type="submit">Submit</button>
    </form>
    {% if url %}
        <p>You entered: {{ url }}</p>
    {% endif %}
</body>
</html>