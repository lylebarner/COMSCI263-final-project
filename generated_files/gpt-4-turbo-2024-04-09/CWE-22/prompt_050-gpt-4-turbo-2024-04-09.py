from flask import Flask, request

app = Flask(__name__)

@app.route('/img')
def img():
    file_name = request.args.get('file')
    with open(file_name, 'rb') as file:
        content = file.read()
    return content