import json
from flask import Blueprint, request
from database import School, Subject, Teacher

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teachers')

@teacher_bp.route('/', methods=['GET','POST'])
def index():
    school = School()

    if request.method == 'POST':
        data = json.loads(request.data.decode())
        if not data.get('fname') or not data.get('lname') or not data.get('birthDate'):
            return {'message':'Data incomplete'}, 400
        
        teacher = Teacher(data['fname'], data['lname'], data['birthDate'])
        res = teacher.add()

        if res == 1: return {'message':'Birth date fromat is not correct'}, 400
        if res == 3: return {'message':'Teacher already exists'}, 409

        location = '/teachers/' + str(teacher.id)
        return {'message':'Teacher successfully created'}, 201, {'Location':location}

    teachers = school.teachers
    if len(teachers) == 0: return {'message':'No Teachers exist'}, 404
    return [teacher.to_dict() for teacher in teachers]