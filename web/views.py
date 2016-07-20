# Import the Flask app itself
from web import app
# Imports from Flask
from flask import Flask, render_template, request, redirect, url_for, abort, session

#### Routing for the index elements

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

####

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

app.run(debug=True) 