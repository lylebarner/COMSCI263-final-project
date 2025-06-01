from flask import Flask, render_template_string, request
import hashlib
import os

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
    <title>File Checksum Generator</title>
</head>
<body>
    <h2>File Checksum Generator</h2>
    <form method="POST">
        <label>Enter filenames (one per line):</label><br>
        <textarea name="filenames" rows="10" cols="50">{{ request.form.filenames or '' }}</textarea><br><br>
        <label>Hash Algorithm:</label>
        <select name="algorithm">
            {% for algo in algos %}
                <option value="{{ algo }}" {% if algo == algorithm %}selected{% endif %}>{{ algo }}</option>
            {% endfor %}
        </select>
        <br><br>
        <input type="submit" value="Generate Checksums">
    </form>
    {% if checksums %}
        <h3>Results</h3>
        <table border="1">
            <tr>
                <th>Filename</th>
                <th>Checksum</th>
                <th>Status</th>
            </tr>
            {% for fname, result in checksums.items() %}
            <tr>
                <td>{{ fname }}</td>
                <td>{% if result.checksum %}{{ result.checksum }}{% else %}-{% endif %}</td>
                <td>{{ result.status }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

def compute_checksum(filename, algorithm='sha256', block_size=65536):
    try:
        hasher = hashlib.new(algorithm)
    except Exception as e:
        return None, f'Invalid algorithm: {algorithm}'
    if not os.path.isfile(filename):
        return None, 'File not found'
    try:
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest(), 'OK'
    except Exception as e:
        return None, f'Error: {str(e)}'

@app.route('/', methods=['GET', 'POST'])
def index():
    checksums = {}
    algos = sorted(hashlib.algorithms_guaranteed)
    algorithm = 'sha256'
    if request.method == 'POST':
        filenames = request.form.get('filenames', '')
        algorithm = request.form.get('algorithm', 'sha256')
        for fname in filter(None, map(str.strip, filenames.splitlines())):
            checksum, status = compute_checksum(fname, algorithm)
            checksums[fname] = {'checksum': checksum, 'status': status}
    return render_template_string(HTML, checksums=checksums, algos=algos, algorithm=algorithm, request=request)

if __name__ == '__main__':
    app.run(debug=True)