from flask import Flask
from route import site, subject, teacher, grade

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(subject)
app.register_blueprint(teacher)
app.register_blueprint(grade)