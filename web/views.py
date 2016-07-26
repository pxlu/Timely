# Import the Flask app itself
from web import app, _cwd
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

#### Session + User Login/Signup elements

@app.route('/login')
def render_login():
    return render_template('login-template.html')

@app.route('/signup')
def render_signup():
    return render_template('signup-template.html')

#### Screening elements

@app.route('/screen')
def screen():
    return render_template('screening-template.html')

@app.route('/screening-form')
def screening_form():
    return render_template('screening-form.html')

#### Resource elements