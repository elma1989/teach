from flask import Flask
from route import subject, teacher, grade

app = Flask(__name__)

app.register_blueprint(subject)
app.register_blueprint(teacher)
app.register_blueprint(grade)