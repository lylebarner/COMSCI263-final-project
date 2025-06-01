from flask import Flask, request, redirect, abort

app = Flask(__name__)

@app.route('/go')
def redirect_invalid_url():
    url = request.args.get('url', '')
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.netloc.endswith('example.com'):
            return redirect(url)
        else:
            return 'Invalid URL: not an example.com domain.', 400
    except Exception:
        return 'Invalid URL.', 400

if __name__ == '__main__':
    app.run(debug=True)