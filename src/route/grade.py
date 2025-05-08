from flask import Blueprint, request
from database import School, Grade

grade_bp = Blueprint('grade', __name__, url_prefix='/grades')

@grade_bp.route('/', methods=['GET','POST'])
def index():
    school = School()

    if request.method == 'POST':
        name = request.form.get('name')
        leader_id = request.form.get('teach-id')
        if not name or not  leader_id: return {'message':'One form field not exists'}, 400
        leader = school.getTeacher(leader_id)
        if not leader: return {'message':'Leader not found'}, 404
        grade = Grade(name, leader)
        res = grade.add()

        if res == 3: return {'message':'Grade allready exists'}, 409
        location = '/grades/' + name.replace(' ','%20')
        return grade.to_dict(), 201, {'Location':location}

    grades = school.grades
    if len(grades) == 0: return '', 204
    return [grade.to_dict() for grade in grades]