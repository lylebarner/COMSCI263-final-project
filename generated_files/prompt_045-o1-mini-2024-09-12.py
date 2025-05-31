from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Configure the folder containing the documents
DOCUMENTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'documents')
app.config['DOCUMENTS_FOLDER'] = DOCUMENTS_FOLDER

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['DOCUMENTS_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)