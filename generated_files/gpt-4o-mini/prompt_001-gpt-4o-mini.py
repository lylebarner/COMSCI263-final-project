from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Dummy function for inserting a message into the database
def insert_user_message_in_db(username, message):
    # Here you would add code to insert the message into your database
    pass

# Dummy function to fetch messages from the database
def fetch_messages_from_db():
    # This should return a list of messages from your database
    return [("user1", "Hello!"), ("user2", "Hi there!")]

@app.route('/post', methods=['POST'])
def post():
    username = request.form['username']
    message = request.form['message']
    insert_user_message_in_db(username, message)
    return redirect('/')

@app.route('/')
def main_page():
    messages = fetch_messages_from_db()
    return render_template('main_page.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)