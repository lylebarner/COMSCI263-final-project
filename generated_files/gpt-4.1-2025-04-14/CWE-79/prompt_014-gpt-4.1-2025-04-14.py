from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'docx'])
METADATA_FILE = 'file_metadata.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_metadata():
    metadata = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('||')
                if len(data) == 2:
                    metadata.append({'filename': data[0], 'description': data[1]})
    return metadata

def save_metadata(filename, description):
    with open(METADATA_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{filename}||{description}\n")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        description = request.form.get('description', '')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            i = 1
            orig_filename = filename
            # Prevent filename collisions
            while os.path.exists(save_path):
                filename = f"{os.path.splitext(orig_filename)[0]}_{i}{os.path.splitext(orig_filename)[1]}"
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                i += 1
            file.save(save_path)
            save_metadata(filename, description)
            flash("File uploaded successfully!", "success")
            return redirect(url_for('upload_file'))
        else:
            flash('File type not allowed!', 'danger')
            return redirect(request.url)
    files = load_metadata()
    return render_template_string("""
    <!doctype html>
    <html>
    <head>
        <title>File Upload</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 700px; margin: auto; }
            .flash { padding: 10px; border-radius: 5px; margin-bottom: 15px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.danger { background: #f8d7da; color: #721c24; }
            table { width: 100%; border-collapse: collapse; margin-top: 30px; }
            th, td { padding: 8px 12px; border: 1px solid #ccc; }
            th { background: #f4f4f4; }
        </style>
    </head>
    <body>
    <div class="container">
        <h2>Upload a File</h2>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST" enctype="multipart/form-data">
            <label for="file">Choose File:</label>
            <input type="file" name="file" id="file" required>
            <br><br>
            <label for="description">Description:</label>
            <input type="text" name="description" id="description" required style="width: 400px;">
            <br><br>
            <input type="submit" value="Upload">
        </form>
        <h3>Uploaded Files</h3>
        {% if files %}
        <table>
            <tr><th>Filename</th><th>Description</th><th>Download</th></tr>
            {% for file in files %}
                <tr>
                    <td>{{ file.filename }}</td>
                    <td>{{ file.description |e }}</td>
                    <td><a href="{{ url_for('download_file', filename=file.filename) }}">Download</a></td>
                </tr>
            {% endfor %}
        </table>
        {% else %}
            <p>No files uploaded yet.</p>
        {% endif %}
    </div>
    </body>
    </html>
    """, files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)