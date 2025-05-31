from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    logs = ''
    if request.method == 'POST':
        log_file_path = request.form.get('log_file_path')
        if log_file_path and os.path.isfile(log_file_path):
            with open(log_file_path, 'r') as file:
                logs = file.read()
        else:
            logs = "Invalid file path or file does not exist."
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)