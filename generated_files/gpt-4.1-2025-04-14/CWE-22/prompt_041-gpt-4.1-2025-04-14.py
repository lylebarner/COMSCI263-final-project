from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecret'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            savepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(savepath)
            return redirect(url_for('view_file', filename=filename))
        else:
            flash('File type not allowed.')
            return redirect(request.url)
    return render_template_string('''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <h2>Uploaded Files:</h2>
    <ul>
      {% for f in files %}
        <li><a href="{{ url_for('view_file') }}?filename={{ f }}">{{ f }}</a></li>
      {% endfor %}
    </ul>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for msg in messages %}
          <li>{{ msg }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    ''', files=os.listdir(UPLOAD_FOLDER))

@app.route('/view')
def view_file():
    filename = request.args.get('filename')
    if not filename or not allowed_file(filename):
        return "Invalid or missing filename.", 400
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if not os.path.isfile(file_path):
        return "File not found.", 404
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']:
        return render_template_string('''
            <h1>Viewing {{ filename }}</h1>
            <img src="{{ url_for('uploaded_file', filename=filename) }}" style="max-width:600px;">
            <br><a href="{{ url_for('upload') }}">Back</a>
        ''', filename=filename)
    elif ext in ['txt', 'md']:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
        return render_template_string('''
            <h1>Viewing {{ filename }}</h1>
            <pre style="background:#eee; padding:10px;">{{ content }}</pre>
            <br><a href="{{ url_for('upload') }}">Back</a>
        ''', filename=filename, content=content)
    elif ext == 'pdf':
        return render_template_string('''
            <h1>Viewing {{ filename }}</h1>
            <embed src="{{ url_for('uploaded_file', filename=filename) }}" width="800" height="600" type="application/pdf">
            <br><a href="{{ url_for('upload') }}">Back</a>
        ''', filename=filename)
    else:
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)