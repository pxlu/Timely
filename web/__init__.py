from flask import Flask
import os

_cwd = os.path.dirname(os.path.realpath(__file__))

app = Flask('Timely', template_folder= _cwd + '/templates', static_folder= _cwd + '/static')
app.config.from_pyfile(_cwd + '/config.py')

from Timely.web import views