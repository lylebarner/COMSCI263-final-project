from flask import Flask, request, redirect, url_for, render_template
import string
import random

app = Flask(__name__)

# In-memory storage for URLs
url_mapping = {}

def generate_short_link(length=6):
    """Generate a random short link."""
    characters = string.ascii_letters + string.digits
    while True:
        short_link = ''.join(random.choice(characters) for _ in range(length))
        if short_link not in url_mapping:
            return short_link

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        custom_alias = request.form.get('custom_alias', '').strip()

        if custom_alias:
            if custom_alias in url_mapping:
                return "Custom alias already exists.", 400
            short_link = custom_alias
        else:
            short_link = generate_short_link()

        url_mapping[short_link] = long_url
        return f"Shortened URL: <a href='/{short_link}'>{request.host_url}{short_link}</a>"

    return render_template('index.html')

@app.route('/<short_link>')
def redirect_to_long_url(short_link):
    long_url = url_mapping.get(short_link)
    if long_url:
        return redirect(long_url)
    return "URL not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
