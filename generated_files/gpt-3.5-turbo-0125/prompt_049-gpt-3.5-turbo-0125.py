from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/image/<filename>')
def get_image(filename):
    image_path = os.path.join('images', filename)
    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        return "Image not found", 404

if __name__ == '__main__':
    app.run()