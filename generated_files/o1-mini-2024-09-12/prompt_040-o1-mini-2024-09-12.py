from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace these with your actual username and password
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/check_mod')
def check_mod():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return 'true'
    return 'false'

if __name__ == '__main__':
    app.run(debug=True)