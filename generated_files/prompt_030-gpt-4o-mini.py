import os
from flask import Flask, request, jsonify, send_file, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Enter URL" required>
            <button type="submit">Download</button>
        </form>
    ''')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Save content to a file
        filename = 'downloaded_content.txt'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Preview
        preview = response.text[:500]  # Preview first 500 characters

        return jsonify({'message': 'Content downloaded successfully!', 'preview': preview})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```