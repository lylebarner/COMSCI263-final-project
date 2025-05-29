def check_and_unsubscribe(email):
    if email in database:
        if unsubscribe_script(email) == 0:
            return 1
        else:
            return 0
    else:
        return 0