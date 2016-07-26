from flask import Flask
import os

_cwd = os.path.dirname(os.path.realpath(__file__))

app = Flask('Timely', template_folder='../web/templates')
app.config.from_pyfile(_cwd + '/config.py')

from web import views