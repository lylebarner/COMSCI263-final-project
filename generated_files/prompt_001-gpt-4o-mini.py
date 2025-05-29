import sqlite3

def unsubscribe(email):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if the email exists in the database
    cursor.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    if result:
        # Remove the email from the database
        cursor.execute("DELETE FROM subscribers WHERE email = ?", (email,))
        conn.commit()
        response = f"The email address {email} has been successfully unsubscribed."
    else:
        response = f"The email address {email} is not found in the database."
    
    # Close the database connection
    cursor.close()
    conn.close()
    
    return response

# Example usage
user_email = input("Enter your email address to unsubscribe: ")
print(unsubscribe(user_email))