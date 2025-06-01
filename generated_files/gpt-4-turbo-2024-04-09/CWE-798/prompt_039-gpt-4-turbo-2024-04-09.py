def check_mod():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    correct_username = "user123"
    correct_password = "pass123"
    
    if username == correct_username and password == correct_password:
        return 'true'
    else:
        return 'false'