from flask import Flask, request, send_file, abort
import os

app = Flask(__name__)

@app.route('/img')
def img():
    name = request.args.get('name')
    if not name:
        abort(400, 'Name parameter is missing.')
    file_path = os.path.join('images', name)
    if not os.path.isfile(file_path):
        abort(404, 'Image not found.')
    return send_file(file_path, mimetype='image/*')

if __name__ == '__main__':
    app.run()