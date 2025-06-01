from flask import Flask, request, render_template_string, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<title>URL Preview Service</title>
<h2>Enter a URL to preview content</h2>
<form method=post>
  <input type=text name=url size=50 required>
  <input type=submit value=Preview>
</form>
{% if error %}
  <p style="color: red;">{{ error }}</p>
{% endif %}
{% if preview %}
  <h3>Preview</h3>
  <p><strong>Title:</strong> {{ preview.title }}</p>
  <p><strong>Description:</strong> {{ preview.description }}</p>
  {% if preview.image %}
    <img src="{{ preview.image }}" alt="Preview Image" style="max-width:300px;">
  {% endif %}
  <p><a href="{{ preview.url }}" target="_blank">Visit Page</a></p>
{% endif %}
'''

def fetch_preview(url):
    try:
        # Accept only http(s) URLs to prevent file:/// etc.
        if not url.lower().startswith(('http://', 'https://')):
            return None, "Only http(s) URLs allowed."

        resp = requests.get(url, timeout=5, headers={'User-Agent': 'PreviewBot/1.0'})
        if resp.status_code != 200:
            return None, "Failed to fetch URL (status code {}).".format(resp.status_code)

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Try to find OpenGraph title & description & image, else fallback.
        title = soup.find('meta', property='og:title')
        if not title:
            title = soup.title
            title = title.string if title else ''
        else:
            title = title.get('content', '')

        description = soup.find('meta', property='og:description')
        if not description:
            description = soup.find('meta', attrs={'name': 'description'})
            description = description.get('content', '') if description else ''
        else:
            description = description.get('content', '')

        image = soup.find('meta', property='og:image')
        if image:
            image = image.get('content', '')
        else:
            image = None

        return {
            'url': url,
            'title': title.strip(),
            'description': description.strip(),
            'image': image
        }, None

    except Exception as exc:
        return None, "Error: " + str(exc)

@app.route('/', methods=['GET', 'POST'])
def index():
    preview = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        preview, error = fetch_preview(url)
    return render_template_string(HTML_FORM, preview=preview, error=error)

if __name__ == '__main__':
    app.run(debug=True)