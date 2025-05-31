from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>URL Display</title>
</head>
<body>
    <h1>Enter a URL</h1>
    <form method="post">
        <input type="url" name="url" required>
        <button type="submit">Submit</button>
    </form>
    {% if url %}
        <p>You entered: <a href="{{ url }}" target="_blank">{{ url }}</a></p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    url = None
    if request.method == 'POST':
        url = request.form.get('url')
    return render_template_string(HTML_TEMPLATE, url=url)

if __name__ == '__main__':
    app.run(debug=True)