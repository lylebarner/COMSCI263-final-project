import requests
from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>URL Preview Service</title>
</head>
<body>
    <h1>URL Preview Service</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter URL" size="60" required>
        <button type="submit">Preview</button>
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    {% if preview %}
        <hr>
        <h2>Preview:</h2>
        <p><strong>Title:</strong> {{ preview.title }}</p>
        <p><strong>Description:</strong> {{ preview.description }}</p>
        {% if preview.image %}
            <img src="{{ preview.image }}" alt="Preview Image" width="300">
        {% endif %}
        <p><a href="{{ preview.url }}" target="_blank">{{ preview.url }}</a></p>
    {% endif %}
</body>
</html>
"""

def validate_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def fetch_preview(url):
    resp = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(resp.text, 'html.parser')

    title = soup.title.string if soup.title else ''
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    description = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else ''

    img_tag = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
    image = img_tag['content'] if img_tag and 'content' in img_tag.attrs else ''
    # Fallback to first <img> tag if nothing found
    if not image:
        img_tag = soup.find('img')
        image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''

    return {
        'title': title or '(No Title)',
        'description': description or '(No Description)',
        'image': image,
        'url': url
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    preview = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url', '')
        if not validate_url(url):
            error = "Invalid URL."
        else:
            try:
                preview = fetch_preview(url)
            except Exception as e:
                error = f"Error fetching URL: {e}"
    return render_template_string(HTML_TEMPLATE, preview=preview, error=error)

if __name__ == '__main__':
    app.run(debug=True)