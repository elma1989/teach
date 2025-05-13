from flask import Blueprint, request
from database import School, Grade, Student

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

@grade_bp.route('/<grade_name>', methods=['GET','PATCH','DELETE'])
def grade(grade_name):
    school = School()
    grade = Grade(grade_name)
    
    if not grade.exists(): return {'message':'Grade not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'PATCH':
        data = request.json
        if data.get('name'):
            grade.name = data['name']
            if grade.name != data['name']: return {'message':'Grade name is not available'}, 409
        if data.get('leaderId'):
            leader = school.getTeacher(data['leaderId'])
            if not leader: return {'message':'Leader not found'}, 404
        return '', 204
    
    if request.method == 'DELETE':
        grade.remove()
        return '', 204

    return grade.to_dict()

@grade_bp.route('/<grade_name>/students', methods=['GET','POST'])
def students(grade_name):
    school = School()
    students = []

    if grade_name == 'none':
        students = school.students(None)
        if len(students) == 0: return '', 204
        return [student.to_dict() for student in students]

    grade = Grade(grade_name)
    if not grade.exists(): return {'message':'Grade not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        fname = data.get('fname')
        lname = data.get('lname')
        birth_date = data.get('birthDate')
        if not fname or not lname or not birth_date: return {'message':'One of the JSON-Fields does not exist'}, 400
        student = Student(fname, lname, birth_date)
        res = student.add()

        if res == 1: return {'message':'birthDate is not correct'}, 400
        if res == 3: return {'message':'Student allready exists'}, 409

        student.grade = grade
        location = f'/grades/{grade.name.replace(' ','%20')}/students/{student.id}'
        return student.to_dict(), 201, {'Location':location}

    students = school.students(grade)
    if len(students) == 0: return '', 204
    return [student.to_dict() for student in students]

@grade_bp.route('/<grade_name>/students/<int:student_id>', methods=['GET','PATCH','DELETE'])
def single_student(grade_name, student_id):
    school = School()
    grade = Grade(grade_name)
    student = school.getStudent(student_id)

    if not grade: return {'message':'Grade not found'}, 404
    if not student: return {'message':'Student not found'}, 404

    if request.headers.get('COntent-Type') == 'application/json' and request.method == 'PATCH':
        data = request.json
        if data.get('gradeName'):
            new_grade = Grade(data['gradeName'])
            if not new_grade.exists(): return {'message':'New grade not found'}, 404
            student.grade = new_grade
        return '', 204

    if not student in school.students(grade): return {'message':'Student in Grade not found'}, 404

    if request.method == 'DELETE':
        student.remove()
        return '', 204

    return student.to_dict()