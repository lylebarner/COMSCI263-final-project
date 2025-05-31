from flask import Flask, jsonify, send_from_directory, abort
import os

app = Flask(__name__)

# Specify the directory where project-related documents are stored
DOCUMENTS_DIRECTORY = 'path/to/documents'

@app.route('/documents/<filename>', methods=['GET'])
def get_document(filename):
    try:
        return send_from_directory(DOCUMENTS_DIRECTORY, filename)
    except FileNotFoundError:
        abort(404, description="File not found")

@app.route('/documents', methods=['GET'])
def list_documents():
    try:
        files = os.listdir(DOCUMENTS_DIRECTORY)
        return jsonify(files)
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)