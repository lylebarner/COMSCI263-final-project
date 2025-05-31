from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_UPLOAD_FORM = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a file</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('view_file', filename=filename))
    return render_template_string(HTML_UPLOAD_FORM)

@app.route('/view')
def view_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Filename not provided', 400
    filename = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)