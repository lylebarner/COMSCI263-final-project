from flask import Flask, send_file
import os

app = Flask(__name__)

def img_decorator(f):
    def wrapper(name):
        file_path = os.path.join('images', name)
        if os.path.exists(file_path):
            return f(file_path)
        else:
            return "File not found", 404
    return wrapper

@app.route('/img/<name>')
@img_decorator
def img(file_path):
    return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=True)