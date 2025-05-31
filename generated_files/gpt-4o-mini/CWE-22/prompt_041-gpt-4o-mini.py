from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template_string('''
        <h1>Upload a File</h1>
        <form method="post" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
        <h2>View Uploaded File</h2>
        <form method="get" action="/view">
            <input type="text" name="filename" required placeholder="Enter filename">
            <input type="submit" value="View">
        </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return f'File uploaded successfully: {file.filename}'

@app.route('/view')
def view_file():
    filename = request.args.get('filename')
    if filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
    return 'Filename not provided', 400

if __name__ == '__main__':
    app.run(debug=True)