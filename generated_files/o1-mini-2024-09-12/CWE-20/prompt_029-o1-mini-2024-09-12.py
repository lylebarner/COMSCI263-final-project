from flask import Flask, request, redirect, render_template_string, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

BASE = string.ascii_letters + string.digits
BASE_LENGTH = 6

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, long_url, short_code):
        self.long_url = long_url
        self.short_code = short_code

def generate_short_code(length=BASE_LENGTH):
    return ''.join(random.choices(BASE, k=length))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        custom_alias = request.form.get('custom_alias')

        if not long_url:
            flash('Please provide a URL.', 'danger')
            return redirect(url_for('home'))

        if custom_alias:
            existing = URL.query.filter_by(short_code=custom_alias).first()
            if existing:
                flash('Custom alias already exists. Choose another one.', 'danger')
                return redirect(url_for('home'))
            short_code = custom_alias
        else:
            short_code = generate_short_code()
            while URL.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code()

        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        short_url = request.host_url + short_code
        return render_template_string(TEMPLATE, short_url=short_url)

    return render_template_string(TEMPLATE)

@app.route('/<short_code>')
def redirect_short_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url_entry.long_url)

TEMPLATE = '''
<!doctype html>
<title>URL Shortener</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<div class="container">
    <h1 class="mt-5">URL Shortener</h1>
    <form method="POST" class="mt-3">
        <div class="form-group">
            <label for="long_url">Long URL</label>
            <input type="url" class="form-control" id="long_url" name="long_url" placeholder="Enter your URL" required>
        </div>
        <div class="form-group">
            <label for="custom_alias">Custom Alias (optional)</label>
            <input type="text" class="form-control" id="custom_alias" name="custom_alias" placeholder="Custom alias">
        </div>
        <button type="submit" class="btn btn-primary">Shorten</button>
    </form>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <div class="mt-3">
          {% for category, message in messages %}
            <div class="alert alert-{{category}}">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    {% if short_url %}
    <div class="alert alert-success mt-3">
        Short URL: <a href="{{ short_url }}">{{ short_url }}</a>
    </div>
    {% endif %}
</div>
'''

if __name__ == '__main__':
    app.run(debug=True)