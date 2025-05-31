from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<title>Checksum Generator</title>
<h1>Upload Files to Generate Checksums</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=files multiple>
  <input type=submit value=Upload>
</form>
{% if checksums %}
    <h2>Checksums:</h2>
    <ul>
    {% for filename, checksum in checksums %}
        <li><strong>{{ filename }}</strong>: {{ checksum }}</li>
    {% endfor %}
    </ul>
{% endif %}
'''

def calculate_checksum(file_stream, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    for chunk in iter(lambda: file_stream.read(4096), b""):
        hash_func.update(chunk)
    file_stream.seek(0)
    return hash_func.hexdigest()

@app.route('/', methods=['GET', 'POST'])
def index():
    checksums = []
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        for file in uploaded_files:
            if file.filename:
                checksum = calculate_checksum(file.stream)
                checksums.append((file.filename, checksum))
    return render_template_string(HTML_FORM, checksums=checksums)

if __name__ == '__main__':
    app.run(debug=True)