from flask import Flask, send_from_directory, jsonify, abort
import os

app = Flask(__name__)

# Directory where project documents are stored
DOCUMENTS_DIR = os.path.abspath('project_documents')

@app.route('/documents', methods=['GET'])
def list_documents():
    """
    List all available project documents.
    """
    if not os.path.exists(DOCUMENTS_DIR):
        return jsonify({"error": "Documents directory not found."}), 404
    files = [f for f in os.listdir(DOCUMENTS_DIR)
             if os.path.isfile(os.path.join(DOCUMENTS_DIR, f))]
    return jsonify({"documents": files})

@app.route('/documents/<path:filename>', methods=['GET'])
def get_document(filename):
    """
    Fetch a specific document by filename.
    """
    safe_path = os.path.join(DOCUMENTS_DIR, filename)
    if not os.path.commonprefix((os.path.abspath(safe_path), DOCUMENTS_DIR)) == DOCUMENTS_DIR:
        abort(403, description="Access denied.")
    if not os.path.isfile(safe_path):
        abort(404, description="File not found.")
    return send_from_directory(DOCUMENTS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)
    app.run(debug=True)