from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory store for the bio
profiles = {
    'username': {'bio': 'Your initial bio goes here.'}
}

@app.route('/')
def profile():
    # Retrieve the user's bio and display it
    user_bio = profiles['username']['bio']
    return render_template('profile.html', bio=user_bio)

@app.route('/edit', methods=['GET', 'POST'])
def edit_bio():
    if request.method == 'POST':
        # Update the bio information
        new_bio = request.form.get('bio')
        profiles['username']['bio'] = new_bio
        return redirect(url_for('profile'))
    else:
        # Show the form for editing the bio
        current_bio = profiles['username']['bio']
        return render_template('edit_bio.html', bio=current_bio)

if __name__ == '__main__':
    app.run(debug=True)
