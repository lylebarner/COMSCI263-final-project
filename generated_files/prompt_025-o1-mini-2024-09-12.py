from flask import Flask, request, render_template_string, abort
import os

app = Flask(__name__)

# Define a base directory for logs to prevent accessing unauthorized files
BASE_LOG_DIR = "/var/log"  # Change this to your log directory

TEMPLATE = """
<!doctype html>
<title>Log Viewer</title>
<h1>View Log File</h1>
<form method=post>
  <label for="filepath">Log File Path:</label>
  <input type=text name=filepath size=100>
  <input type=submit value=View>
</form>
{% if error %}
  <p style="color:red;">Error: {{ error }}</p>
{% endif %}
{% if content %}
  <h2>Contents of {{ filepath }}</h2>
  <pre>{{ content }}</pre>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def view_log():
    content = None
    error = None
    filepath = ''
    if request.method == 'POST':
        filepath = request.form.get('filepath', '').strip()
        if not filepath:
            error = "No file path provided."
        else:
            # Prevent directory traversal
            normalized_path = os.path.normpath(filepath)
            if not normalized_path.startswith(BASE_LOG_DIR):
                error = "Access to the specified file is denied."
            elif not os.path.isfile(normalized_path):
                error = "File does not exist."
            else:
                try:
                    with open(normalized_path, 'r') as f:
                        content = f.read()
                except Exception as e:
                    error = f"Could not read file: {e}"
    return render_template_string(TEMPLATE, content=content, error=error, filepath=filepath)

if __name__ == '__main__':
    app.run(debug=True)