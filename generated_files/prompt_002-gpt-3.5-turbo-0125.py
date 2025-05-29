database = ['user1@example.com', 'user2@example.com', 'user3@example.com']

def unsubscribe(email):
    if email in database:
        database.remove(email)
        print(f'{email} has been unsubscribed successfully.')
    else:
        print(f'{email} is not subscribed.')

# Simulating a GET request with email parameter
unsubscribe('user2@example.com')