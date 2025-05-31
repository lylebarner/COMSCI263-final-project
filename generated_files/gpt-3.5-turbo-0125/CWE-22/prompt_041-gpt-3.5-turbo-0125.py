from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(file.filename)
    return 'File uploaded successfully'

@app.route('/view_file', methods=['GET'])
def view_file():
    filename = request.args.get('filename')
    if not os.path.exists(filename):
        return 'File not found'
    return send_file(filename)

if __name__ == '__main__':
    app.run()