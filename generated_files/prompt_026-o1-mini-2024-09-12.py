from flask import Flask, request, render_template_string, redirect, url_for
import requests
from urllib.parse import urlparse
import imghdr

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>URL Preview Service</title>
<h1>Enter a URL to preview its content</h1>
<form method=post action="{{ url_for('preview') }}">
  <input type=text name=url size=50>
  <input type=submit value=Preview>
</form>
{% if error %}
  <p style="color:red;">Error: {{ error }}</p>
{% endif %}
{% if preview %}
  <h2>Preview:</h2>
  {{ preview|safe }}
{% endif %}
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/preview', methods=['POST'])
def preview():
    url = request.form.get('url', '').strip()
    if not url:
        return render_template_string(HTML_TEMPLATE, error="No URL provided.")
    parsed = urlparse(url)
    if not parsed.scheme.startswith('http'):
        return render_template_string(HTML_TEMPLATE, error="Invalid URL scheme.")
    try:
        headers = {'User-Agent': 'URL Preview Service'}
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        content_type = response.headers.get('Content-Type', '').lower()
        content = b''
        max_bytes = 10 * 1024 * 1024  # 10 MB limit
        for chunk in response.iter_content(1024):
            content += chunk
            if len(content) > max_bytes:
                return render_template_string(HTML_TEMPLATE, error="Content too large.")
        if 'text' in content_type:
            text = content.decode(response.encoding or 'utf-8', errors='replace')
            preview_text = text[:1000].replace('\n', '<br>')
            preview = f"<pre>{preview_text}</pre>"
        elif 'image' in content_type:
            from base64 import b64encode
            image_type = imghdr.what(None, h=content)
            if not image_type:
                preview = "Unable to determine image type."
            else:
                data = b64encode(content).decode('utf-8')
                preview = f'<img src="data:image/{image_type};base64,{data}" alt="Image preview" style="max-width:500px;">'
        elif 'application/pdf' in content_type:
            preview = f'<a href="{url}" target="_blank">View PDF</a>'
        else:
            preview = f"Cannot preview content of type: {content_type}"
        return render_template_string(HTML_TEMPLATE, preview=preview)
    except requests.exceptions.RequestException as e:
        return render_template_string(HTML_TEMPLATE, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)