from flask import Flask, redirect, request, abort

app = Flask(__name__)

@app.route('/redirect/')
def redirect_invalid_url():
    url = request.args.get('url')
    if url and "example.com" in url:
        return redirect(url)
    else:
        abort(404, description="Invalid URL. Domain is not example.com")

if __name__ == '__main__':
    app.run(debug=True)