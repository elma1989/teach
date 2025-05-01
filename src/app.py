from flask import Flask
from route import site

app = Flask(__name__)
app.register_blueprint(site)