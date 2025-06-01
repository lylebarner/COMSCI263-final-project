from flask import Flask, request, render_template_string, abort
import os

app = Flask(__name__)

LOG_VIEW_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Log Viewer</title>
    <style>
        body { font-family: monospace; background: #2b2b2b; color: #e0e0e0;}
        textarea { width: 100%; height: 500px; background: #222; color: #dcdcdc; border: none; }
        .input-container { margin-bottom: 20px; }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <h1>Log File Viewer</h1>
    <form method="POST">
        <div class="input-container">
            <label for="log_path">Log File Path:</label>
            <input type="text" name="log_path" id="log_path" size="80" value="{{ log_path|default('') }}">
            <button type="submit">Read Log</button>
        </div>
    </form>
    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
    {% if log_contents is defined %}
        <h2>Contents of: {{ log_path }}</h2>
        <textarea readonly>{{ log_contents }}</textarea>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def view_log():
    log_contents = ''
    error = None
    log_path = ''

    if request.method == 'POST':
        log_path = request.form.get('log_path', '').strip()
        if not log_path:
            error = 'Please specify a log file path.'
        else:
            # Basic security: don't allow directory traversal to /etc/passwd, etc
            if os.path.isabs(log_path) and not os.path.isfile(log_path):
                error = 'Log file does not exist.'
            elif ".." in os.path.normpath(log_path):
                error = 'Directory traversal is not allowed.'
            else:
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
                        log_contents = f.read()
                except Exception as e:
                    error = f'Error reading log file: {e}'

    return render_template_string(
        LOG_VIEW_TEMPLATE,
        log_path=log_path,
        log_contents=log_contents if log_contents else None,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
