from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>File Viewer</title>
</head>
<body>
    <h2>Contents of {{ filename }}:</h2>
    {% if content %}
    <pre>{{ content }}</pre>
    {% else %}
    <p>File could not be found or is empty.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/preview/<filename>')
def file_preview(filename):
    content = None
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        content = None

    return render_template_string(HTML_TEMPLATE, filename=filename, content=content)

if __name__ == '__main__':
    app.run(debug=True)