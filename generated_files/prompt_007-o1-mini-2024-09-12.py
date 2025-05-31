import sys
from sqlalchemy import create_engine, Column, Integer, String, Date, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    date_created = Column(Date)

class Archive(Base):
    __tablename__ = 'archive'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    date_created = Column(Date)
    archived_on = Column(Date)

def get_filters():
    print("Enter filter criteria (leave blank to skip):")
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    date_from = input("Date From (YYYY-MM-DD): ").strip()
    date_to = input("Date To (YYYY-MM-DD): ").strip()
    filters = []
    if name:
        filters.append(Record.name.like(f"%{name}%"))
    if category:
        filters.append(Record.category == category)
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
            filters.append(Record.date_created >= date_from_obj)
        except ValueError:
            print("Invalid Date From format. Ignoring this filter.")
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
            filters.append(Record.date_created <= date_to_obj)
        except ValueError:
            print("Invalid Date To format. Ignoring this filter.")
    return filters

def lookup_records(session, filters):
    query = session.query(Record)
    if filters:
        query = query.filter(and_(*filters))
    records = query.all()
    if records:
        print(f"Found {len(records)} record(s):")
        for record in records:
            print(f"ID: {record.id}, Name: {record.name}, Category: {record.category}, Date Created: {record.date_created}")
    else:
        print("No records found.")
    return records

def archive_records(session, records):
    if not records:
        return
    for record in records:
        archived = Archive(
            id=record.id,
            name=record.name,
            category=record.category,
            date_created=record.date_created,
            archived_on=datetime.today().date()
        )
        session.add(archived)
        session.delete(record)
    session.commit()
    print(f"Archived {len(records)} record(s).")

def main():
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\nDatabase Maintenance Utility")
        print("1. Lookup Records")
        print("2. Archive Records")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            filters = get_filters()
            lookup_records(session, filters)
        elif choice == '2':
            filters = get_filters()
            records = lookup_records(session, filters)
            if records:
                confirm = input("Do you want to archive these records? (y/n): ").strip().lower()
                if confirm == 'y':
                    archive_records(session, records)
        elif choice == '3':
            print("Exiting.")
            session.close()
            sys.exit()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()