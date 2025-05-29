from flask import Flask, send_file

app = Flask(__name__)

@app.route('/download/<document_name>')
def download(document_name):
    folder_path = 'path/to/documents'
    document_path = f'{folder_path}/{document_name}'
    return send_file(document_path, as_attachment=True)

if __name__ == '__main__':
    app.run()