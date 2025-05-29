from flask import Flask, redirect

app = Flask(__name__)

@app.route('/<path:url>')
def redirect_invalid_url(url):
    if 'example.com' in url:
        return redirect(url)
    else:
        return 'Error: Invalid URL'

if __name__ == '__main__':
    app.run()