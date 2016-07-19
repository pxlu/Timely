from flask import Flask

app = Flask('timely')
app.config.from_pyfile('config.py')

from web import views