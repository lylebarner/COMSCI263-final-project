from flask import Flask, send_from_directory, request, abort
import os

app = Flask(__name__)

# Configuration
DOCUMENTS_FOLDER = 'path/to/documents'  # Change this to the folder path containing your documents
app.config['DOCUMENTS_FOLDER'] = DOCUMENTS_FOLDER

@app.route('/download', methods=['GET'])
def download_document():
    # Get the filename from the query parameters
    filename = request.args.get('name')

    if not filename:
        abort(400, description="Filename not provided")

    # Sanitize the filename to prevent path traversal attacks
    safe_filename = os.path.basename(filename)

    # Check if the file exists
    if not os.path.isfile(os.path.join(app.config['DOCUMENTS_FOLDER'], safe_filename)):
        abort(404, description="File not found")

    # Send the file to the user
    return send_from_directory(app.config['DOCUMENTS_FOLDER'], safe_filename)

if __name__ == '__main__':
    app.run(debug=True)