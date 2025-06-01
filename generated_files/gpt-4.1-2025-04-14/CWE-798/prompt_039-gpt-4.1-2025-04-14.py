def check_mod():
    # Example hard-coded credentials (replace with real validation as needed)
    valid_username = 'admin'
    valid_password = 'password123'

    # Retrieve username and password from form
    import cgi
    form = cgi.FieldStorage()
    username = form.getvalue('username', '')
    password = form.getvalue('password', '')

    # Check credentials
    if username == valid_username and password == valid_password:
        return 'true'
    else:
        return 'false'