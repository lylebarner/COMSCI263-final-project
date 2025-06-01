from flask import Flask, request, redirect, render_template

app = Flask(__name__)

def insert_user_message_in_db(username, message):
    # Placeholder function for database interaction
    pass

@app.route('/', methods=['GET'])
def index():
    # Placeholder function to display messages
    messages = []  # Fetch messages from database
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
def post():
    username = request.form['username']
    message = request.form['message']
    insert_user_message_in_db(username, message)
    return redirect('/')