from flask import Flask, request, render_template

app = Flask(__name__)
user_bio = {}

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user_bio['bio'] = request.form['bio']
    
    return render_template('profile.html', bio=user_bio.get('bio'))

if __name__ == '__main__':
    app.run()