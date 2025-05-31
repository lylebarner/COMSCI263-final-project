from flask import Flask, render_template, request, send_file
import hashlib
import os

app = Flask(__name__)

def calculate_checksum(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_sha256.update(byte_block)
    return hash_sha256.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_checksum', methods=['POST'])
def generate_checksum():
    filenames = request.form.getlist('filenames')
    checksums = {}
    
    for filename in filenames:
        try:
            checksum = calculate_checksum(filename)
            checksums[filename] = checksum
        except FileNotFoundError:
            checksums[filename] = "File not found"
    
    return render_template('results.html', checksums=checksums)

if __name__ == '__main__':
    app.run(debug=True)
