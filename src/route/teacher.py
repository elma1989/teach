from flask import Blueprint, request
from database import School, Teacher

teacher_bp = Blueprint('teacher',__name__, url_prefix='/teachers')

@teacher_bp.route('/', methods=['GET','POST'])
def index():
    school = School()

    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        birth_date = request.form.get('birth-date')
        if not fname or not lname or not birth_date: return {'message':'Form Data missing'}, 400
        teacher = Teacher(fname,lname,birth_date)
        res = teacher.add()

        if res == 1: return {'message':'Format Birth date is not correct'}, 400
        if res == 3: return {'message':'Teacher allready exists'}, 409
        location = '/teachers/' + str(teacher.id)
        return teacher.to_dict(), 201, {'Location':location}

    teachers = school.teachers
    if len(teachers) == 0: return '', 204
    return [teacher.to_dict() for teacher in teachers]

@teacher_bp.route('/<int:teach_id>')
def teacher(teach_id):
    school = School ()
    teacher = school.getTeacher(teach_id)

    if not teacher: return {'message':'Teacher not found'}, 404

    return teacher.to_dict()