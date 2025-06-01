from flask import Flask, render_template_string, abort, safe_join, send_file
import os

app = Flask(__name__)

# Directory where files are stored
FILE_DIRECTORY = os.path.abspath("files")  # you may change to your desired path

@app.route('/preview/<path:filename>')
def preview(filename):
    # Only allow previewing files in the FILE_DIRECTORY for security
    file_path = safe_join(FILE_DIRECTORY, filename)
    if not file_path or not os.path.isfile(file_path):
        abort(404, description="File not found.")

    # Attempt to guess file type for basic preview
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # For images, display inline
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']:
        return render_template_string(
            '''<h2>Preview: {{ filename }}</h2>
            <img src="{{ url_for('get_file', filename=filename) }}" style="max-width:90vw; max-height:90vh;">
            <br><a href="/">Back</a>
            ''',
            filename=filename
        )

    # For text files, show in <pre>
    elif ext in ['.txt', '.py', '.md', '.log', '.csv', '.json', '.html', '.css', '.js']:
        with open(file_path, encoding="utf-8", errors='replace') as f:
            content = f.read(10240)  # Limit to 10KB preview
        return render_template_string(
            '''<h2>Preview: {{ filename }}</h2>
            <pre style="white-space: pre-wrap;">{{ content }}</pre>
            <br><a href="/">Back</a>
            ''',
            filename=filename, content=content
        )
    else:
        return render_template_string(
            '''<h2>Preview: {{ filename }}</h2>
            <p>File type not supported for preview. <a href="{{ url_for('get_file', filename=filename) }}">Download file</a></p>
            <br><a href="/">Back</a>
            ''',
            filename=filename
        )

@app.route('/files/<path:filename>')
def get_file(filename):
    file_path = safe_join(FILE_DIRECTORY, filename)
    if not file_path or not os.path.isfile(file_path):
        abort(404)
    return send_file(file_path)

@app.route('/')
def index():
    # Show a list of files available for preview
    try:
        files = []
        for root, dirs, filenames in os.walk(FILE_DIRECTORY):
            for fname in filenames:
                rel_dir = os.path.relpath(root, FILE_DIRECTORY)
                rel_file = os.path.join(rel_dir, fname) if rel_dir != '.' else fname
                files.append(rel_file.replace("\\", "/"))
    except Exception:
        files = []

    return render_template_string(
        '''
        <h1>File Previewer</h1>
        <form action="/preview" method="get">
        <input type="text" name="filename" placeholder="Enter filename e.g. test.txt">
        <button type="submit">Preview</button>
        </form>
        <h3>Available Files:</h3>
        <ul>
        {% for file in files %}
          <li><a href="{{ url_for('preview', filename=file) }}">{{ file }}</a></li>
        {% endfor %}
        </ul>
        ''',
        files=files
    )

# Allow query-form input
@app.route('/preview')
def preview_query():
    from flask import request, redirect, url_for
    filename = request.args.get('filename')
    if filename:
        return redirect(url_for('preview', filename=filename))
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(FILE_DIRECTORY, exist_ok=True)
    app.run(debug=True)