from flask import Flask
from route import subject

app = Flask(__name__)

app.register_blueprint(subject)