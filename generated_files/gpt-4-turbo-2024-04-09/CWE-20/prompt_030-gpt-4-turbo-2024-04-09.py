import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_url():
    content_url = request.json.get('url')
    if not content_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        response = requests.get(content_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    soup = BeautifulSoup(response.content, 'html.parser')
    preview_text = soup.get_text()[:500]  # first 500 characters as preview
    return jsonify({'url': content_url, 'preview': preview_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)