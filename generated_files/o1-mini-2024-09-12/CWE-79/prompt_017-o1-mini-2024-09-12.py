from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
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
      <p>You entered: <a href="{{ url }}">{{ url }}</a></p>
    {% endif %}
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    if request.method == 'POST':
        url = request.form.get('url')
    return render_template_string(HTML, url=url)

if __name__ == '__main__':
    app.run(debug=True)