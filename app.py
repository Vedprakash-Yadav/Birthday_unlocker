from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated database
users = {
    'john': {'password': '123', 'birthday': '1995-07-31', 'instagram': 'john_doe'},
    'emma': {'password': 'abc', 'birthday': '2000-01-01', 'instagram': 'emma_cute'}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        birthday = request.form['birthday']
        instagram = request.form['instagram']
        if username not in users:
            users[username] = {
                'password': password,
                'birthday': birthday,
                'instagram': instagram
            }
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = ''
    matched_instagram = None

    if request.method == 'POST':
        guessed_birthday = request.form['guessed_birthday']
        target_user = request.form['target_user']
        if target_user in users:
            if guessed_birthday == users[target_user]['birthday']:
                matched_instagram = users[target_user]['instagram']
                return redirect(url_for('success', instagram=matched_instagram))
            else:
                message = 'Incorrect guess. Try again!'

    return render_template('dashboard.html', users=users, message=message)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = users[session['username']]

    if request.method == 'POST':
        user['birthday'] = request.form['birthday']
        user['instagram'] = request.form['instagram']
        return redirect(url_for('dashboard'))

    return render_template('edit_profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/success/<instagram>')
def success(instagram):
    return render_template('result.html', instagram=instagram)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
