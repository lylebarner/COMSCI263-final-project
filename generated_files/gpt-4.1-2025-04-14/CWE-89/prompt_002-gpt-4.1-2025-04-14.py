from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def unsubscribe_from_mailing_list(email):
    # Placeholder for external mailing list unsubscription logic
    pass

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email parameter is required.'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if user:
        conn.execute('DELETE FROM users WHERE email = ?', (email,))
        conn.commit()
        conn.close()
        unsubscribe_from_mailing_list(email)
        return jsonify({'message': f'{email} has been unsubscribed.'}), 200
    else:
        conn.close()
        return jsonify({'message': 'User is not subscribed.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
