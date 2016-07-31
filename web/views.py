# Import the Flask app itself
from Timely.web import app, _cwd
# Imports from Flask
from flask import Flask, render_template, request, redirect, url_for, abort, session
from Timely.scripts.screen import _get_profile

#### Index elements

@app.route('/')
@app.route('/home')
def home():
    return render_template('index-template.html')

@app.route('/students')
def students():
    return render_template('/students/students-template.html')

@app.route('/providers')
def providers():
    return render_template('/providers/providers-template.html')

#### Session + User Login/Signup elements

@app.route('/login')
def render_login():
    return render_template('/uauth/login-template.html')

@app.route('/signup')
def render_signup():
    return render_template('/uauth/signup-template.html')

#### Screening elements

@app.route('/screening')
def screening_template():
    return render_template('/students/screening-template.html')

@app.route('/screening-form')
def screening_form():
    return render_template('/students/screening-form.html')

@app.route('/screening-results', methods=['POST', 'GET'])
def screening_results():
    if request.method == 'POST':
        result = request.form
        return render_template('/students/screening-results.html', result= _get_profile(in_file="no_file",profile_name=result['name'], no_file=True, text_input=result['bio']))

#### Resource elements