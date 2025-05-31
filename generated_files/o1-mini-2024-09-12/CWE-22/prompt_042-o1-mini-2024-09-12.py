from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath("project_documents")

@app.route('/documents/<path:filename>', methods=['GET'])
def get_document(filename):
    try:
        # Prevent path traversal
        safe_path = os.path.join(BASE_DIR, filename)
        if not os.path.commonpath([BASE_DIR, safe_path]).startswith(BASE_DIR):
            abort(403, description="Forbidden")
        
        if not os.path.isfile(safe_path):
            abort(404, description="File not found")
        
        directory = os.path.dirname(safe_path)
        file = os.path.basename(safe_path)
        return send_from_directory(directory, file, as_attachment=True)
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    app.run(host='0.0.0.0', port=5000)