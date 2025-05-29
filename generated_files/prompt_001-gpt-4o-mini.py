import sqlite3

def unsubscribe(email):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if the email exists in the database
    cursor.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    if result:
        # Email found, proceed to unsubscribe
        cursor.execute("DELETE FROM subscribers WHERE email = ?", (email,))
        conn.commit()
        print("You have been successfully unsubscribed.")
    else:
        # Email not found
        print("You are not in the database.")
    
    # Close the database connection
    conn.close()

# Example usage
user_email = input("Enter your email address to unsubscribe: ")
unsubscribe(user_email)