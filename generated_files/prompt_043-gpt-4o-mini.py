from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/getfile', methods=['POST'])
def get_file_contents():
    data = request.get_json()
    if 'filename' not in data:
        return jsonify({'error': 'Filename not provided'}), 400

    filename = data['filename']
    
    if not os.path.isfile(filename):
        return jsonify({'error': 'File not found'}), 404

    with open(filename, 'r') as file:
        contents = file.read()

    return jsonify({'filename': filename, 'contents': contents})

if __name__ == '__main__':
    app.run(debug=True)