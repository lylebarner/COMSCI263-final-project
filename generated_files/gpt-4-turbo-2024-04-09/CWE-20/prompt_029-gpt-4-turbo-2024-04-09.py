from flask import Flask, request, redirect, jsonify
import hashlib
import re

app = Flask(__name__)
url_map = {}
base_url = "http://localhost:5000/"

def generate_short_link(long_url, custom_alias=None):
    if custom_alias:
        if custom_alias in url_map:
            return None
        short_url = custom_alias
    else:
        # Use MD5 hash generator to create a short link
        hash_object = hashlib.md5(long_url.encode())
        short_url = hash_object.hexdigest()[:6]
    if short_url in url_map and url_map[short_url] != long_url:
        return None
    url_map[short_url] = long_url
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    custom_alias = data.get('alias', None)
    response = {}
    if long_url:
        short_url = generate_short_link(long_url, custom_alias)
        if short_url:
            response["short_url"] = base_url + short_url
            response["status"] = "success"
        else:
            response["status"] = "error"
            response["message"] = "Alias already in use or short URL collision."
    else:
        response["status"] = "error"
        response["message"] = "No URL provided."
    return jsonify(response)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    long_url = url_map.get(short_url, None)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"status": "error", "message": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)