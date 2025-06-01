from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store uploads with descriptions
uploads_info = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files or 'description' not in request.form:
            return "No file or description part", 400
        file = request.files['file']
        description = request.form['description']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploads_info.append((filename, description, filepath))
    return render_template('index.html', uploads=uploads_info)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!doctype html>
<html>
<head>
    <title>File Upload with Description</title>
</head>
<body>
    <h2>Upload new File</h2>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=text name=description placeholder='Enter description'>
        <input type=submit value=Upload>
    </form>
    <h2>Uploaded Files</h2>
    <ul>
        {% for filename, description, filepath in uploads %}
        <li>
            <a href="{{ url_for('uploaded_file', filename=filename) }}">{{ filename }}</a>
            - {{ description }}
        </li>
        {% endfor %}
    </ul>
</body>
</html>