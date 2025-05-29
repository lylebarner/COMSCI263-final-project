from flask import Flask, request

app = Flask(__name__)

@app.route('/preview/<filename>')
def preview_file(filename):
    with open(filename, 'r') as file:
        contents = file.read()
    return contents

if __name__ == '__main__':
    app.run(debug=True)