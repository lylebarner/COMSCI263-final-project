from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route('/img')
def img():
    filename = request.args.get('file')
    if not filename:
        abort(400, 'Filename must be specified.')
    
    try:
        with open(filename, 'rb') as f:
            return send_file(f, mimetype='image/jpeg')  # Adjust mimetype as needed
    except FileNotFoundError:
        abort(404, 'File not found.')

if __name__ == '__main__':
    app.run(debug=True)