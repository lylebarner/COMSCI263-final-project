from flask import Flask, redirect

app = Flask(__name__)

@app.route('/redirect/<path:url>')
def redirect_invalid_url(url):
    if 'example.com' in url:
        return redirect(url)
    return 'Error: Invalid URL'

if __name__ == '__main__':
    app.run()