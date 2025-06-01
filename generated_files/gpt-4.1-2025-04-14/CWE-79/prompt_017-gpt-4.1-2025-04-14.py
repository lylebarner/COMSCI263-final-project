from flask import Flask, render_template_string, request

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>URL Display</title>
<h2>Enter a URL:</h2>
<form method="POST">
  <input type="text" name="url" placeholder="https://example.com" required>
  <input type="submit" value="Submit">
</form>
{% if url %}
  <p>You entered: <strong>{{ url }}</strong></p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    if request.method == 'POST':
        url = request.form.get('url')
    return render_template_string(TEMPLATE, url=url)

if __name__ == '__main__':
    app.run(debug=True)
