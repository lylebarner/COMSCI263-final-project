from flask import Flask, request, redirect
import string
import random

app = Flask(__name__)
url_database = {}

def generate_short_url(length=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=length))

@app.route('/')
def index():
    return "Welcome to URL Shortener"

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    custom_alias = request.form.get('alias')
    
    if custom_alias:
        if custom_alias in url_database:
            return f"Error: Alias already exists for {url_database[custom_alias]}"
        short_url = custom_alias
    else:
        short_url = generate_short_url()
        
    url_database[short_url] = long_url
    return f"Short URL: {'<Your_Domain>/' + short_url}"

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    if short_url in url_database:
        return redirect(url_database[short_url])
    else:
        return "Short URL not found"

if __name__ == '__main__':
    app.run()