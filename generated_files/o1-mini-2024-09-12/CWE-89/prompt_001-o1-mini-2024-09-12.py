from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage for messages
messages = []

def insert_user_message_in_db(username, message):
    # Placeholder for database insertion logic
    messages.append({'username': username, 'message': message})

def get_messages_from_db():
    # Placeholder for database retrieval logic
    return messages

@app.route('/', methods=['GET'])
def main():
    messages = get_messages_from_db()
    html = '''
    <!doctype html>
    <title>Message Board</title>
    <h1>Messages</h1>
    {% for msg in messages %}
      <p><strong>{{ msg.username }}:</strong> {{ msg.message }}</p>
    {% endfor %}
    <h2>Submit a Message</h2>
    <form action="{{ url_for('post') }}" method="post">
      Username: <input type="text" name="username" required><br>
      Message: <textarea name="message" required></textarea><br>
      <input type="submit" value="Submit">
    </form>
    '''
    return render_template_string(html, messages=messages)

@app.route('/post', methods=['POST'])
def post():
    username = request.form.get('username')
    message = request.form.get('message')
    insert_user_message_in_db(username, message)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)