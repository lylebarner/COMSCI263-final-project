from flask import Flask, request, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return 'File uploaded successfully.', 200
    return 'No file uploaded.', 400

@app.route('/view', methods=['GET'])
def view_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Filename is required as a query parameter.', 400
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_file(file_path)
    return 'File does not exist.', 404

if __name__ == '__main__':
    app.run(debug=True)