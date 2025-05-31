from flask import Flask, request

app = Flask(__name__)

database = ['user1@example.com', 'user2@example.com']

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')

    if email in database:
        database.remove(email)
        return 'You have been unsubscribed'
    else:
        return 'User is not subscribed'

if __name__ == '__main__':
    app.run()