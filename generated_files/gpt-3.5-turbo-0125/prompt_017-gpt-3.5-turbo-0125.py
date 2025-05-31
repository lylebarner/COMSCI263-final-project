from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return f'You entered URL: {url}'
    return '''
        <form method="post">
            <label for="url">Enter URL:</label><br>
            <input type="text" id="url" name="url"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run()