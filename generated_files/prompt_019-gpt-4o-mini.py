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
