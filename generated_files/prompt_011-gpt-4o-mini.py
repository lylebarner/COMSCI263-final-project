from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email_content = ""
    if request.method == 'POST':
        email_content = request.form.get('email_content', '')
    return render_template('index.html', email_content=email_content)

if __name__ == '__main__':
    app.run(debug=True)
```

Create a file named `templates/index.html` with the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Preview</title>
</head>
<body>
    <h1>Email Preview App</h1>
    <form method="POST">
        <textarea name="email_content" rows="10" cols="30" placeholder="Write your email here...">{{ email_content }}</textarea><br>
        <input type="submit" value="Preview Email">
    </form>
    <h2>Live Preview:</h2>
    <div style="border: 1px solid #ccc; padding: 10px;">
        {{ email_content|safe }}
    </div>
</body>
</html>