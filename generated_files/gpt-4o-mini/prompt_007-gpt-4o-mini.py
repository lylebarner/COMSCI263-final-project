import sqlite3

def connect_db(db_name):
    return sqlite3.connect(db_name)

def create_table(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS records (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def lookup_records(conn, filter_value, filter_column='name'):
    cursor = conn.cursor()
    query = f'SELECT * FROM records WHERE {filter_column} = ?'
    cursor.execute(query, (filter_value,))
    return cursor.fetchall()

def archive_records(conn, age_limit):
    with conn:
        conn.execute('DELETE FROM records WHERE age > ?', (age_limit,))

def main():
    db_name = input("Enter the database name: ")
    conn = connect_db(db_name)
    create_table(conn)

    while True:
        print("\nDatabase Maintenance Utility")
        print("1. Lookup Records")
        print("2. Archive Records")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            filter_value = input("Enter the value to filter by (name): ")
            records = lookup_records(conn, filter_value)
            print("Found Records:", records)

        elif choice == '2':
            age_limit = int(input("Enter age limit for archival: "))
            archive_records(conn, age_limit)
            print(f"Archived records older than {age_limit}.")

        elif choice == '3':
            break
        
        else:
            print("Invalid option. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()