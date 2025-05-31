from flask import Flask, redirect, abort

app = Flask(__name__)

@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_invalid_url(url):
    valid_domain = "example.com"
    
    if valid_domain in url:
        return redirect(f"http://{url}", code=302)
    else:
        return abort(400, description="Invalid URL: Only example.com is allowed.")

if __name__ == '__main__':
    app.run(debug=True)