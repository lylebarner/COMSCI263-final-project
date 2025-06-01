from flask import Flask, send_from_directory, abort, request
import os

app = Flask(__name__)
DOCUMENT_FOLDER = os.path.join(os.path.dirname(__file__), 'documents')

@app.route('/download')
def download_file():
    filename = request.args.get('name')
    if not filename:
        abort(400, description="Missing 'name' parameter.")
    # Prevent path traversal attacks
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        abort(400, description="Invalid filename.")
    file_path = os.path.join(DOCUMENT_FOLDER, filename)
    if not os.path.isfile(file_path):
        abort(404, description="File not found.")
    return send_from_directory(DOCUMENT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(DOCUMENT_FOLDER, exist_ok=True)
    app.run(debug=True)
