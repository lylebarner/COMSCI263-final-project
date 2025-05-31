@app.route('/img')
def img():
    file_name = request.args.get('file')
    with open(file_name, 'rb') as file:
        file_data = file.read()
    
    return file_data