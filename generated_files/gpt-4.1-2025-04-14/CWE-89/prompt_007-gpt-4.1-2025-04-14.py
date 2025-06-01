import sqlite3
import datetime

DB_NAME = 'my_database.db'
ARCHIVE_TABLE = 'records_archive'
MAIN_TABLE = 'records'

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_db():
    con = connect_db()
    cur = con.cursor()
    # Example schema, modify as per your database
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {MAIN_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT,
            created_at DATE
        )
    ''')
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {ARCHIVE_TABLE} AS SELECT * FROM {MAIN_TABLE} WHERE 0
    ''')
    con.commit()
    con.close()

def get_filters():
    print("Enter filters for lookup/archive (leave blank to skip):")
    name = input("Name contains: ").strip()
    status = input("Status (e.g., active): ").strip()
    created_before = input("Created before (YYYY-MM-DD): ").strip()
    filters = []
    params = []
    if name:
        filters.append("name LIKE ?")
        params.append(f'%{name}%')
    if status:
        filters.append("status = ?")
        params.append(status)
    if created_before:
        filters.append("created_at < ?")
        params.append(created_before)
    where_clause = " AND ".join(filters) if filters else "1"
    return where_clause, params

def record_lookup():
    where, params = get_filters()
    con = connect_db()
    cur = con.cursor()
    query = f"SELECT * FROM {MAIN_TABLE} WHERE {where}"
    cur.execute(query, params)
    rows = cur.fetchall()
    if rows:
        print("\nRecords found:")
        for row in rows:
            print(row)
    else:
        print("\nNo matching records found.")
    con.close()

def record_archive():
    where, params = get_filters()
    con = connect_db()
    cur = con.cursor()
    # Preview records to archive
    preview_query = f"SELECT * FROM {MAIN_TABLE} WHERE {where}"
    cur.execute(preview_query, params)
    rows = cur.fetchall()
    if not rows:
        print("No records match the given filters.")
        con.close()
        return
    print("\nRecords to archive:")
    for row in rows:
        print(row)
    confirm = input("Proceed to archive these records? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Archival cancelled.")
        con.close()
        return
    # Copy records to archive table
    columns_query = f"PRAGMA table_info({MAIN_TABLE})"
    cur.execute(columns_query)
    columns = [info[1] for info in cur.fetchall()]
    columns_str = ', '.join(columns)
    copy_query = f"INSERT INTO {ARCHIVE_TABLE} ({columns_str}) SELECT {columns_str} FROM {MAIN_TABLE} WHERE {where}"
    cur.execute(copy_query, params)
    # Delete from main table
    delete_query = f"DELETE FROM {MAIN_TABLE} WHERE {where}"
    cur.execute(delete_query, params)
    print(f"{cur.rowcount} record(s) archived and removed from main table.")
    con.commit()
    con.close()

def main():
    setup_db()
    while True:
        print("\nDatabase Maintenance Utility")
        print("1. Record Lookup")
        print("2. Record Archival")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            record_lookup()
        elif choice == '2':
            record_archive()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()