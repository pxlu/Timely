# Import the Flask app itself
from web import app
# Imports from Flask
from flask import render_template, request

# Routing for the index
@app.route('/')
@app.route('/index')
def index():
	return render_template('index-template.html')

app.run(debug=True) 