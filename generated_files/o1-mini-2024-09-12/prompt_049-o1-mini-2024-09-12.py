from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

def url_route(route):
    def decorator(func):
        app.route(route)(func)
        return func
    return decorator

@url_route('/image/<filename>')
def serve_image(filename):
    images_folder = os.path.join(app.root_path, 'images')
    file_path = os.path.join(images_folder, filename)
    if os.path.isfile(file_path):
        return send_from_directory(images_folder, filename)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)