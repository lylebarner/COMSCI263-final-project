import sqlite3
from datetime import datetime

class DatabaseMaintenance:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def lookup_records(self, table, **filters):
        query = f"SELECT * FROM {table}"
        if filters:
            filter_str = " AND ".join([f"{k} = ?" for k in filters])
            query += " WHERE " + filter_str
            self.cursor.execute(query, tuple(filters.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def archive_records(self, table, archive_table, **filters):
        records = self.lookup_records(table, **filters)
        if not records:
            print("No records to archive.")
            return

        self.cursor.executemany(f"INSERT INTO {archive_table} VALUES ({','.join(['?' for _ in range(len(records[0]))])})", records)
        delete_str = " AND ".join([f"{k} = ?" for k in filters])
        self.cursor.execute(f"DELETE FROM {table} WHERE " + delete_str, tuple(filters.values()))
        self.conn.commit()
        print(f"Archived {len(records)} records.")

    def close(self):
        self.conn.close()


def main():
    db_maintenance = DatabaseMaintenance("example.db")
    try:
        while True:
            print("\nDatabase Maintenance Menu")
            print("1. Lookup records")
            print("2. Archive records")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                table = input("Enter table name for lookup: ")
                filters = {}
                while True:
                    key = input("Enter filter column (blank to finish): ")
                    if not key:
                        break
                    value = input(f"Enter value for {key}: ")
                    filters[key] = value
                records = db_maintenance.lookup_records(table, **filters)
                for record in records:
                    print(record)

            elif choice == '2':
                table = input("Enter table name for archiving from: ")
                archive_table = input("Enter table name for archiving into: ")
                filters = {}
                while True:
                    key = input("Enter filter column (blank to finish): ")
                    if not key:
                        break
                    value = input(f"Enter value for {key}: ")
                    filters[key] = value
                db_maintenance.archive_records(table, archive_table, **filters)

            elif choice == '3':
                break
            else:
                print("Invalid option.")
    finally:
        db_maintenance.close()

if __name__ == "__main__":
    main()