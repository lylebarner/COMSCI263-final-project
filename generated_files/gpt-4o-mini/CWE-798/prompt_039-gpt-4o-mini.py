from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy credentials for demonstration purposes
valid_username = "user"
valid_password = "pass"

@app.route('/check_mod', methods=['POST'])
def check_mod():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == valid_username and password == valid_password:
        return jsonify(result='true')
    else:
        return jsonify(result='false')

if __name__ == '__main__':
    app.run(debug=True)