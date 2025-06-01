from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<html>
    <head>
        <title>URL Display</title>
    </head>
    <body>
        <h1>Enter a URL</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter your URL here" required>
            <button type="submit">Submit</button>
        </form>
        {% if url %}
            <h2>You entered: {{ url }}</h2>
        {% endif %}
    </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    url = None
    if request.method == 'POST':
        url = request.form['url']
    return render_template_string(TEMPLATE, url=url)

if __name__ == '__main__':
    app.run(debug=True)