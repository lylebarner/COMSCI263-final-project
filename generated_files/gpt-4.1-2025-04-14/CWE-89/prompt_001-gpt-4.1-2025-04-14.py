from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

# Assume a simple in-memory message storage for demonstration
messages_db = []

def insert_user_message_in_db(username, message):
    messages_db.append({'username': username, 'message': message})

@app.route('/', methods=['GET'])
def main():
    # Display all messages
    return render_template('main.html', messages=messages_db)

@app.route('/post', methods=['POST'])
def post():
    username = request.form.get('username', '').strip()
    message = request.form.get('message', '').strip()
    if username and message:
        insert_user_message_in_db(username, message)
    return redirect(url_for('main'))

# main.html template (to be placed in the 'templates' directory)
"""
<!doctype html>
<html>
<head><title>Messages</title></head>
<body>
  <form action="{{ url_for('post') }}" method="post">
    Username: <input type="text" name="username"><br>
    Message: <input type="text" name="message"><br>
    <button type="submit">Send</button>
  </form>
  <h2>Messages</h2>
  <ul>
    {% for msg in messages %}
      <li><strong>{{ msg.username }}</strong>: {{ msg.message }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""
# To run the app:
# if __name__ == '__main__':
#     app.run(debug=True)