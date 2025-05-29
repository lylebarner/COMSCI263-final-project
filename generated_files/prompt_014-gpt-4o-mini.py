from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

uploads = []

@app.route('/')
def index():
    return render_template('index.html', uploads=uploads)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    description = request.form.get('description', '')

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        uploads.append({'filename': file.filename, 'description': description})
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'Download link for {filename}'

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Files</title>
</head>
<body>
    <h1>Upload File</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file" required>
        <input type="text" name="description" placeholder="Enter a description" required>
        <button type="submit">Upload</button>
    </form>
    
    <h2>Uploaded Files</h2>
    <ul>
        {% for upload in uploads %}
            <li>
                <a href="{{ url_for('uploaded_file', filename=upload.filename) }}">{{ upload.filename }}</a> - {{ upload.description }}
            </li>
        {% endfor %}
    </ul>
</body>
</html>