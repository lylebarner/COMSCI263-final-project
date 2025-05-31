from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/img')
def img():
    file_path = request.args.get('file')
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return Response(file_data, mimetype='image/jpeg')
    except FileNotFoundError:
        return "File not found.", 404

if __name__ == '__main__':
    app.run(debug=True)