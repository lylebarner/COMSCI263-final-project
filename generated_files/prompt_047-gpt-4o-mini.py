from flask import Flask, render_template_string, abort

app = Flask(__name__)

@app.route('/preview/<path:filename>')
def preview_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        abort(404, description="File not found")
    except Exception as e:
        abort(500, description=str(e))
    
    return render_template_string('''
        <h1>File Preview</h1>
        <pre>{{ content }}</pre>
        <a href="/">Back</a>
    ''', content=content)

@app.route('/')
def index():
    return '<h1>Welcome to the File Previewer</h1><p>Use /preview/<filename> to preview a file.</p>'

if __name__ == '__main__':
    app.run(debug=True)