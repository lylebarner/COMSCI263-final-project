from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Viewer</title>
</head>
<body>
    <h1>Log Viewer</h1>
    <form method="GET" action="/view-log">
        <input type="text" name="path" placeholder="Enter log file path" style="width: 300px;" required>
        <button type="submit">View Log</button>
    </form>
    {% if log_contents %}
    <h2>Contents of {{ log_path }}:</h2>
    <pre>{{ log_contents }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/view-log')
def view_log():
    log_path = request.args.get('path', '')
    log_contents = ''
    if log_path and os.path.isfile(log_path):
        with open(log_path, 'r') as file:
            log_contents = file.read()
    return render_template_string(HTML_TEMPLATE, log_contents=log_contents, log_path=log_path)

if __name__ == "__main__":
    app.run(debug=True)