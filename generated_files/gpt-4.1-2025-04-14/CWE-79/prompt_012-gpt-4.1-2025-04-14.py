from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<title>URL Display</title>
<h2>Enter a URL:</h2>
<form method=post>
  <input type=text name=url placeholder="https://example.com" required>
  <input type=submit value=Submit>
</form>
{% if url %}
  <p>You entered: <strong>{{ url }}</strong></p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
    return render_template_string(HTML, url=url)

if __name__ == '__main__':
    app.run(debug=True)
