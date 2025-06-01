from flask import Flask, request, redirect, render_template_string, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key in production

# In-memory URL store
url_store = {}
alias_store = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in url_store:
            return code

HTML = '''
<!doctype html>
<title>URL Shortener</title>
<h2>URL Shortener</h2>
<form method=post>
  <label>Long URL:</label><br>
  <input type=text name=long_url required size=50><br><br>
  <label>Custom Alias (optional):</label><br>
  <input type=text name=custom_alias size=20><br><br>
  <input type=submit value=Shorten>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul style="color:red;">
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
{% if short_url %}
    <p>Shortened URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url'].strip()
        custom_alias = request.form['custom_alias'].strip()

        # Simple URL validation
        if not (long_url.startswith('http://') or long_url.startswith('https://')):
            flash('Please enter a valid URL (http:// or https://)')
            return render_template_string(HTML, short_url=None)

        if custom_alias:
            if not custom_alias.isalnum():
                flash('Custom alias must be alphanumeric.')
                return render_template_string(HTML, short_url=None)
            if custom_alias in url_store:
                flash('Alias already in use. Choose another one.')
                return render_template_string(HTML, short_url=None)
            code = custom_alias
        else:
            code = generate_short_code()
            # Guarantee no collision with custom aliases
            while code in url_store:
                code = generate_short_code()

        url_store[code] = long_url
        alias_store[long_url] = code  # For demonstration; not used for deduplication
        short_url = url_for('shorten_redirect', code=code, _external=True)
    return render_template_string(HTML, short_url=short_url)

@app.route('/<code>')
def shorten_redirect(code):
    long_url = url_store.get(code)
    if long_url:
        return redirect(long_url)
    return '<h3>Invalid or expired short link.</h3>', 404

if __name__ == '__main__':
    app.run(debug=True)