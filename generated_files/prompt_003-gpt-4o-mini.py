def check_and_unsubscribe(email, database, unsubscribe_script):
    if email not in database:
        return 0
    
    # Call the unsubscribe script with the email
    result = unsubscribe_script(email)
    if result == 0:
        return 1
    return 0

# Example usage
def mock_unsubscribe_script(email):
    # Simulate unsubscribing logic, return 0 on success
    return 0  # Change this as needed to simulate different outcomes

database = ["example1@gmail.com", "example2@gmail.com"]
email_to_check = "example1@gmail.com"

result = check_and_unsubscribe(email_to_check, database, mock_unsubscribe_script)
print(result)  # Output will be 1 if unsubscribed successfully, 0 otherwise