from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)
IMAGES_FOLDER = 'images'

@app.route('/image/<filename>')
def serve_image(filename):
    file_path = os.path.join(IMAGES_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_from_directory(IMAGES_FOLDER, filename)
    else:
        abort(404)

# if __name__ == '__main__':
#     app.run(debug=True)
