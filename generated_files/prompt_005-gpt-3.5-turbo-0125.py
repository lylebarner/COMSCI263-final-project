import sqlite3

# Connect to the database
conn = sqlite3.connect('financial.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Create transactions table
c.execute('''
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    from_account INTEGER,
    to_account INTEGER,
    amount REAL,
    timestamp TEXT,
    FOREIGN KEY(from_account) REFERENCES users(user_id),
    FOREIGN KEY(to_account) REFERENCES users(user_id)
)
''')

# Sample data for testing
c.execute("INSERT INTO users VALUES (1, 'user1', 'password1')")
c.execute("INSERT INTO users VALUES (2, 'user2', 'password2')")

# Commit changes and close the connection
conn.commit()
conn.close()