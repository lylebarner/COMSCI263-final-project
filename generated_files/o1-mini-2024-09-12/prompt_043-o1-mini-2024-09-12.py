from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/get_files', methods=['POST'])
def get_files():
    data = request.get_json()
    if not data or 'filenames' not in data:
        return jsonify({'error': 'No filenames provided'}), 400

    filenames = data['filenames']
    files_content = {}

    for filename in filenames:
        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as f:
                    files_content[filename] = f.read()
            except Exception as e:
                files_content[filename] = f'Error reading file: {str(e)}'
        else:
            files_content[filename] = 'File not found'

    return jsonify(files_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)