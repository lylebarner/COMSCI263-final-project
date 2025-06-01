from flask import Flask, send_file, abort, request
import os

app = Flask(__name__)
documents_folder = '/path/to/documents'  # configure the path to your documents folder

@app.route('/documents/<filename>', methods=['GET'])
def get_document(filename):
    if '..' in filename or filename.startswith('/'):
        # Prevent directory traversal attack
        abort(400, description="Invalid filename")
        
    file_path = os.path.join(documents_folder, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404, description="File not found")

if __name__ == "__main__":
    app.run(debug=True)