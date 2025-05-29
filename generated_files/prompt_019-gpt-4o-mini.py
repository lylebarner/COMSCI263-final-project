from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class EmailForm(FlaskForm):
    html_email = TextAreaField('HTML Email', validators=[DataRequired()])
    submit = SubmitField('Preview')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    email_preview = ''
    if form.validate_on_submit():
        email_preview = form.html_email.data
    return render_template('index.html', form=form, email_preview=email_preview)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Preview</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container mt-5">
    <h1>HTML Email Previewer</h1>
    <form method="POST" novalidate>
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.html_email.label(class="form-label") }}
            {{ form.html_email(class="form-control", rows=10) }}
        </div>
        <div class="form-group">
            {{ form.submit(class="btn btn-primary") }}
        </div>
    </form>
    <h2>Email Preview</h2>
    <div class="border p-3" style="background-color:#f8f9fa;">
        {{ email_preview|safe }}
    </div>
</div>
</body>
</html>