from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/readfile', methods=['POST'])
def read_file():
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'error': 'Missing filename'}), 400
    filename = data['filename']
    if not os.path.isfile(filename):
        return jsonify({'error': 'File not found'}), 404
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)