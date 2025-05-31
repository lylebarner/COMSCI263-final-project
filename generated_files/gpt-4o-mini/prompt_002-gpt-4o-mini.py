from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('users.db')

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'message': 'Email parameter is required.'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Successfully unsubscribed.'}), 200
    else:
        conn.close()
        return jsonify({'message': 'User is not subscribed.'}), 404

if __name__ == '__main__':
    app.run(debug=True)