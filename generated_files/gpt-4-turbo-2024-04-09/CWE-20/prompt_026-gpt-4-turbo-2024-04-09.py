from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_url():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "Invalid URL or no URL provided"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Assuming that we are dealing with HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        preview = soup.prettify()[:1000]  # Getting a small part of the content for preview

        return jsonify({"url": url, "preview": preview}), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)