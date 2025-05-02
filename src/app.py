from flask import Flask
from route import site, subject

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(subject)