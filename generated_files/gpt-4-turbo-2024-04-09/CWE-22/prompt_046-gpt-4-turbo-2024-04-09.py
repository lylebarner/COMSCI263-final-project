from flask import Flask, request, render_template
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    checksum_result = ''
    if request.method == 'POST':
        file_path = request.form['filename']
        checksum_type = request.form.get('checksum_type', 'md5')
        try:
            with open(file_path, 'rb') as file:
                if checksum_type == 'md5':
                    hash_func = hashlib.md5()
                elif checksum_type == 'sha1':
                    hash_func = hashlib.sha1()
                elif checksum_type == 'sha256':
                    hash_func = hashlib.sha256()
                else:
                    return 'Unsupported checksum type'

                while chunk := file.read(4096):
                    hash_func.update(chunk)
                checksum_result = hash_func.hexdigest()
        except FileNotFoundError:
            checksum_result = 'File not found'
        except Exception as e:
            checksum_result = f'An error occurred: {str(e)}'

    return render_template('index.html', checksum=checksum_result)

if __name__ == '__main__':
    app.run(debug=True)
```

And the corresponding `index.html` should be placed in a folder named `templates` in the same directory where this script is running:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checksum Generator</title>
</head>
<body>
    <h1>Checksum Generator</h1>
    <form action="/" method="post">
        File Path: <input type="text" name="filename" required><br>
        Checksum Type:
        <select name="checksum_type">
            <option value="md5">MD5</option>
            <option value="sha1">SHA1</option>
            <option value="sha256">SHA256</option>
        </select><br>
        <input type="submit" value="Generate Checksum">
    </form>
    {% if checksum %}
        <h2>Checksum: {{ checksum }}</h2>
    {% endif %}
</body>
</html>