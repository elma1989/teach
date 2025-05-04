from database import School, Grade
from flask import Blueprint

grade_bp = Blueprint('grade',__name__,url_prefix='/grades')

@grade_bp.route('/')
def index():
    school = School()
    grades = school.grades

    if len(grades) == 0: return {'message':'Grades not found'}, 404
    return [grade.to_dict() for grade in grades]