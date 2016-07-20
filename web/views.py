# Import the Flask app itself
from web import app
# Imports from Flask
from flask import Flask, render_template, request, redirect, url_for, abort, session

#### Index elements

@app.route('/')
@app.route('/home')
def home():
    return render_template('index-template.html')

@app.route('/students')
def students():
    return render_template('students-template.html')

@app.route('/providers')
def providers():
    return render_template('providers-template.html')

#### Session + User Login elements

@app.route('/login')
def render_login():
    return render_template('login-template.html')

#### Screening elements

@app.route('/screen')
def screen():
    return render_template('screening-template.html')

#### Resource elements

"""
<!--
<h1>Say something</h1>
<form method="post" action="{{ url_for('signup') }}">
    <p><label>Username:</label> <input type="text" name="username" required></p>
    <p><label>Message:</label> <textarea name="message"></textarea></p>
    <p><button type="submit">Send</button></p>
</form>
-->

@app.route('/signup', methods=['POST'])
def signup():
    session['username'] = request.form['username']
    session['message'] = request.form['message']
    return redirect(url_for('message'))

@app.route('/message')
def message():
    if not 'username' in session:
        return abort(403)
    return render_template('message-template.html', username=session['username'], 
                                           message=session['message'])
"""

app.run(debug=True) 