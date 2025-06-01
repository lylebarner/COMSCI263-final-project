from flask import Flask, redirect, request, abort

app = Flask(__name__)

@app.route('/redirect/<path:url>')
def redirect_invalid_url(url):
    if "example.com" in url:
        return redirect(f"http://{url}")
    else:
        abort(404, description="Error: Invalid URL. Only URLs from example.com are allowed.")

if __name__ == "__main__":
    app.run(debug=True)