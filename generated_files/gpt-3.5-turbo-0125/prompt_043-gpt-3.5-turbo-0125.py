from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_file_content():
    filenames = request.form.getlist('file')
    file_contents = {}

    for filename in filenames:
        with open(filename, 'r') as file:
            file_contents[filename] = file.read()

    return jsonify(file_contents)

if __name__ == '__main__':
    app.run()