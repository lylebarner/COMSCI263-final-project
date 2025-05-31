from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)

db.create_all()

upload_page = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a File with Description</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file required>
  <br><br>
  <textarea name=description placeholder="Enter description" required></textarea>
  <br><br>
  <input type=submit value=Upload>
</form>
<a href="{{ url_for('list_files') }}">View Uploaded Files</a>
'''

list_page = '''
<!doctype html>
<title>Uploaded Files</title>
<h1>Uploaded Files</h1>
<table border=1>
    <tr>
        <th>Filename</th>
        <th>Description</th>
        <th>Download</th>
    </tr>
    {% for file in files %}
    <tr>
        <td>{{ file.filename }}</td>
        <td>{{ file.description }}</td>
        <td><a href="{{ url_for('download_file', file_id=file.id) }}">Download</a></td>
    </tr>
    {% endfor %}
</table>
<br>
<a href="{{ url_for('upload_file') }}">Upload Another File</a>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        description = request.form.get('description', '')
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_file = UploadedFile(filename=filename, description=description)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('list_files'))
    return render_template_string(upload_page)

@app.route('/files')
def list_files():
    files = UploadedFile.query.all()
    return render_template_string(list_page, files=files)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)