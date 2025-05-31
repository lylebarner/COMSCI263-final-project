import os
from flask import Flask, request, jsonify, send_file
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_content():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Validate URL
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return jsonify({'error': 'Invalid URL'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Save content to a temporary file
        temp_file_path = 'temp_content.txt'
        with open(temp_file_path, 'wb') as f:
            f.write(response.content)

        # Preview (get first 100 characters)
        preview = response.content.decode('utf-8', errors='ignore')[:100]

        return jsonify({
            'message': 'Content downloaded successfully',
            'preview': preview,
            'download_link': request.host_url + 'download_file/' + os.path.basename(temp_file_path)
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)