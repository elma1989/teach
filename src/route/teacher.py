import json
from flask import Blueprint, request
from database import School, Subject, Teacher, Grade, Course

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
    if len(subjects) == 0: return {'message':'Teacher has no subjects'}, 204
    return [subject.to_dict() for subject in subjects]

@teacher_bp.route('/<int:id>/grades', methods=['GET','POST'])
def grades(id):
    school = School()
    teacher = school.getTeacher(id)

    if not teacher: return {'message':'Teacher not found'}, 404

    if request.method == 'POST':
        data = json.loads(request.data.decode())
        
        if not data.get('name'): return {'message':"JSON-field 'name' does not exist"}, 400

        grade = Grade(data['name'], teacher)
        res = grade.add()

        if res == 3: return {'message':'Grade allready exists'}, 409
        location = '/grades/' + grade.name
        return {'message':'Grade successfully created'}, 201, {'Location':location}

    grades = school.grades_of(teacher)
    if len(grades) == 0: return {'message':'Teacher leads no Grades'}, 204
    return [grade.to_dict() for grade in grades]

@teacher_bp.route('/<int:id>/grades/<name>', methods=['PUT'])
def change_leader(id, name):
    school = School()
    teacher = school.getTeacher(id)
    grade = Grade(name)

    if not teacher or not grade.exists(): return {'message':'Teacher oder grade not found'}, 404

    grade.leader = teacher
    return {'message':'Leader successfully changed'}

@teacher_bp.route('/<int:id>/courses', methods=['GET','POST'])
def course(id):
    school = School()
    leader = school.getTeacher(id)

    if not leader: return {'message':'Course-Leader not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        name = data.get('name')
        sub = data.get('subject')

        if not name or not sub: return {'message':'One or many of JSON-Fields not exists'}, 400

        course = Course(name, leader, Subject(sub))
        res = course.add()

        if res == 2: return {'message':'Subject does not exists'}, 404
        if res == 3: return {'message':'Course allready exists'}, 409
        location = '/' + str(leader.id) + '/courses/' + course.name
        return {'message':'Course successfully created'}, 201, {'Location':location}

    
    courses = school.courses_of(leader)
    if len(courses) == 0: return {'message':'Leader does not have any courses'}, 204
    return [course.to_dict() for course in courses]

@teacher_bp.route('/<int:id>/courses/<name>', methods=['GET','PUT'])
def single_course(id, name):
    school = School()
    leader = school.getTeacher(id)
    course = Course(name)

    if not leader: return {'message':'Leader not found'}, 404
    if not course.exists(): return {'message': 'Course not found'}, 404

    if request.method == 'PUT':
        course.leader = leader
        if course.leader != leader: return {'message':'This teacher does not teasch this subject'}, 409
        return {'message':'Leader successfully changed'}

    if not course in school.courses_of(leader): return {'message':'Course in Leader-Courses not found'}, 404
    
    return course.to_dict()