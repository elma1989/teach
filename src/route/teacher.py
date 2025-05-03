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

@teacher_bp.route('/<int:id>')
def teacher(id):
    school = School()
    teacher = school.getTeacher(id)

    if not teacher: return {'message':'Teacher not found'}, 404
    return teacher.to_dict()

@teacher_bp.route('/<int:id>/subjects', methods=['GET','POST'])
def subjects(id):
    school = School()
    teacher = school.getTeacher(id)

    if not teacher: return {'message':'Teacher not found'}, 404

    if request.method == 'POST':
        data = json.loads(request.data.decode())

        if not data.get('abr'):
            return {'message':'Data incomplete'}, 400
        
        res = teacher.add_subject(Subject(data['abr']))

        if res == 1: return {'message':'Subject not found'}, 404
        if res == 2: return {'message':'Teacher allready teaches this subject'}, 409
        location = '/teachers/' + str(teacher.id) + '/subjects/' + data['abr']
        return {'message':'Subject successfully added to Teacher'}, 201, {'Location':location}

    subjects = teacher.subjects
    if len(subjects) == 0: return {'message':'No Subjects'}, 204
    return [subject.to_dict() for subject in subjects]