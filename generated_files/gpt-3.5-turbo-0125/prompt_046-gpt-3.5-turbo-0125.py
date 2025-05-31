from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_checksum():
    if request.method == 'POST':
        file_name = request.form['file_name']
        with open(file_name, 'rb') as file:
            file_content = file.read()
            checksum = hashlib.md5(file_content).hexdigest()
        return f'Checksum for {file_name}: {checksum}'

    return '''
    <form method="post">
        <label for="file_name">Enter file name:</label><br>
        <input type="text" id="file_name" name="file_name"><br>
        <input type="submit" value="Generate Checksum">
    </form>
    '''

if __name__ == '__main__':
    app.run()