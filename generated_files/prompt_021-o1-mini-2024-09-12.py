from flask import Flask, redirect, abort
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect/<path:url>')
def redirect_invalid_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'example.com':
        return redirect(url)
    else:
        return "Error: Invalid URL. Only example.com URLs are allowed.", 400

if __name__ == '__main__':
    app.run(debug=True)