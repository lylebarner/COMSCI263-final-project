from flask import Flask, request, send_file, abort
import os

app = Flask(__name__)

@app.route('/img')
def img():
    name = request.args.get('name')
    if not name:
        abort(400, "Missing 'name' parameter")
    filepath = os.path.join('images', name)
    if not os.path.isfile(filepath):
        abort(404, "Image not found")
    return send_file(filepath)

# Uncomment the below block to run the app directly
# if __name__ == '__main__':
#     app.run(debug=True)
