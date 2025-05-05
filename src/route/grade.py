import json
from database import School, Grade, Student
from flask import Blueprint, request

grade_bp = Blueprint('grade',__name__,url_prefix='/grades')

@grade_bp.route('/')
def index():
    school = School()
    grades = school.grades

    if len(grades) == 0: return {'message':'Grades not found'}, 404
    return [grade.to_dict() for grade in grades]

@grade_bp.route('/<gradename>', methods=['PATCH'])
def grade(gradename):
    grade = Grade(gradename)

    if not grade.exists(): return {'message':'Grade not found'}, 404

    data = json.loads(request.data.decode())

    if not data.get('name'): return {'message':"JSON-Field 'name' not exists"}, 400
    grade.name = data['name']

    if grade.name == gradename: return {'message':'Gradename allready exists'}, 409
    return {'message':'Grade name successfully changed'}

@grade_bp.route('/<gradename>/students', methods=['GET','POST'])
def students(gradename):
    school = School()

    if gradename == 'none':
        students = school.students(None)
        if len(students) == 0: return {'message':'No students without grade'}, 204
        return [student.to_dict() for student in students]

    grade = Grade(gradename)

    if not grade.exists(): return {'message':'Grade not found'}, 404

    if request.method == 'POST':
        data = json.loads(request.data.decode())

        if not data.get('fname') or not data.get('lname') or not data.get('birthDate'):
            return {'message':'One or more missing JSON-Field'}, 400
        
        student = Student(data['fname'], data['lname'], data['birthDate'])
        res = student.add()
        student.grade = grade

        if res == 1: return {'message':'Birthdate format is not correct'}, 400
        if res == 3: return {'message':'Student allready exists'}, 409
        location = '/grades/' + grade.name + '/students/' + str(student.id)
        return {'message':'Student successfully created'}, 201, {'Location':location}

    students = school.students(grade)
    if len(students) == 0: return {'message':'No students in grade'}, 204
    return [student.to_dict() for student in students]