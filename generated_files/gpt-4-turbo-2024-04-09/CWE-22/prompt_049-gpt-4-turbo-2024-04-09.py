from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

def route(url):
    def decorator(func):
        @app.route(url)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

@route("/images/<filename>")
def get_image(filename):
    img_path = os.path.join("images", filename)
    if os.path.exists(img_path):
        return send_from_directory("images", filename)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)