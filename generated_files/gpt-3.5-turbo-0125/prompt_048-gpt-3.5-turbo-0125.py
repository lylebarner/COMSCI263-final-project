def img(func):
    def wrapper(*args, **kwargs):
        name = kwargs.get('name', '')
        with open(f'images/{name}', 'rb') as file:
            return file.read()
    return wrapper

@img
def img():
    pass