from flask import Flask, send_file

app = Flask(__name__)

@app.route('/documents/<filename>', methods=['GET'])
def get_document(filename):
    try:
        return send_file(f'path_to_documents/{filename}', as_attachment=True)
    except FileNotFoundError:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)