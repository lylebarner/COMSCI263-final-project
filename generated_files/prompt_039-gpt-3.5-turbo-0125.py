def check_mod():
    username = 'user123'
    password = 'pass456'
    
    # Get username and password from form
    user_input_username = 'user123'  # For example
    user_input_password = 'pass456'  # For example
    
    # Check if username and password are correct
    if user_input_username == username and user_input_password == password:
        return 'true'
    else:
        return 'false'