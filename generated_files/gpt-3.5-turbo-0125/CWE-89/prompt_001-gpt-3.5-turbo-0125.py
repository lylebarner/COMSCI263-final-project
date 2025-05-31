def post(request):
    username = request.POST.get('username')
    message = request.POST.get('message')
    
    insert_user_message_in_db(username, message)
    
    return redirect('main_page')

# Add code to display messages