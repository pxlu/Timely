# Import the Flask app itself
from web import app
# Imports from Flask
from flask import render_template, request

# Routing for the index
@app.route('/')
@app.route('/index')
def index():
	return render_template('index-template.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

app.run(debug=True)