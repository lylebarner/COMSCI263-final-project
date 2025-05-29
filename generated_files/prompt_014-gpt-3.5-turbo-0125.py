from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        description = request.form['description']
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions.txt'), 'a') as f:
                f.write(f"{file.filename}: {description}\n")
    
    files = []
    descriptions = {}
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions.txt'), 'r') as f:
        for line in f:
            parts = line.strip().split(': ')
            files.append(parts[0])
            descriptions[parts[0]] = parts[1]

    return render_template('index.html', files=files, descriptions=descriptions)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)