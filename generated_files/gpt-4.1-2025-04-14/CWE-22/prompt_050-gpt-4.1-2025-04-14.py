from flask import Flask, request, Response, abort

app = Flask(__name__)

@app.route('/img')
def img():
    filename = request.args.get('file')
    if not filename:
        abort(400, 'No file parameter provided.')
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        # Optionally, set a generic image MIME type
        return Response(data, mimetype='image/*')
    except FileNotFoundError:
        abort(404, 'File not found.')
    except Exception as e:
        abort(500, str(e))

if __name__ == '__main__':
    app.run(debug=True)
