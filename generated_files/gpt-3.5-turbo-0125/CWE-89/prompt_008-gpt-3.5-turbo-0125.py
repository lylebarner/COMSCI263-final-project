from flask import Flask, request

app = Flask(__name__)

users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return 'Login Successful'
    else:
        return 'Login Failed'

if __name__ == '__main__':
    app.run()