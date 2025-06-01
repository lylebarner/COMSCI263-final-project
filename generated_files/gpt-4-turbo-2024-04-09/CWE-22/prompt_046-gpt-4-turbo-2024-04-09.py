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
