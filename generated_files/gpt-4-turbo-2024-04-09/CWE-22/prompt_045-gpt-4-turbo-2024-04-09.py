from flask import Flask, send_from_directory, abort, request

app = Flask(__name__)
DOCUMENT_FOLDER = '/path/to/documents'  # specify your actual folder path here

@app.route('/')
def index():
    return '<h1>Welcome to the Document Download Service</h1>'

@app.route('/download', methods=['GET'])
def download_document():
    filename = request.args.get('filename')
    if not filename:
        return "Missing filename parameter!", 400
    try:
        return send_from_directory(DOCUMENT_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)