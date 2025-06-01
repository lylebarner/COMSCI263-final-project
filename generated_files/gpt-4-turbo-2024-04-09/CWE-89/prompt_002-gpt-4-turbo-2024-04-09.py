from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def check_email_in_database(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def unsubscribe_user(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is missing'}), 400
    
    if check_email_in_database(email):
        unsubscribe_user(email)
        return jsonify({'message': 'You have been successfully unsubscribed'}), 200
    else:
        return jsonify({'message': 'User with this email is not subscribed'}), 404

if __name__ == '__main__':
    app.run(debug=True)