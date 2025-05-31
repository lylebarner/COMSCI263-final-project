from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logs', methods=['GET', 'POST'])
def display_logs():
    if request.method == 'POST':
        log_file_path = request.form['log_file_path']
        try:
            with open(log_file_path, 'r') as log_file:
                logs = log_file.readlines()
        except FileNotFoundError:
            logs = ['Log file not found.']
        return render_template('logs.html', logs=logs)
    else:
        return render_template('logs.html', logs=[])

if __name__ == '__main__':
    app.run(debug=True)