def unsubscribe(email):
    if email in database:
        database.remove(email)
    else:
        print("You are not in the database")