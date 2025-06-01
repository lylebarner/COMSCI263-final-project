from flask import Flask, redirect, abort, request
from urllib.parse import urlparse, unquote

app = Flask(__name__)

def redirect_invalid_url(url):
    decoded_url = unquote(url)
    parsed = urlparse(decoded_url)
    if parsed.netloc.lower().endswith("example.com"):
        return redirect(decoded_url)
    else:
        return "Invalid URL: Only redirects to example.com are allowed.", 400

@app.route('/redirect/<path:url>')
def redirect_route(url):
    return redirect_invalid_url(url)

if __name__ == '__main__':
    app.run(debug=True)
