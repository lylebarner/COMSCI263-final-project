from flask import Flask, redirect, request, abort

app = Flask(__name__)

@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_invalid_url(url):
    if url.startswith('http://example.com/') or url.startswith('https://example.com/'):
        return redirect(url)
    else:
        return abort(404, description="Invalid URL. Must be from example.com")

if __name__ == '__main__':
    app.run(debug=True)