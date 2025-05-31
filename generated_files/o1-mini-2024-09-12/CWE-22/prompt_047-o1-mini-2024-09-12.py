from flask import Flask, abort, Response
import os
from pathlib import Path

app = Flask(__name__)

# Define the directory where files are located
BASE_DIR = Path(__file__).parent / 'files'

@app.route('/preview/<path:filename>')
def preview_file(filename):
    # Resolve the full path
    file_path = (BASE_DIR / filename).resolve()
    
    # Prevent directory traversal
    if not file_path.is_file() or not str(file_path).startswith(str(BASE_DIR.resolve())):
        abort(404)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except Exception:
        abort(500)

if __name__ == '__main__':
    # Ensure the BASE_DIR exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    app.run(debug=True)