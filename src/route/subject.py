from flask import Blueprint, request
from database import School, Subject

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')

@subject_bp.route('/', methods=['GET','POST'])
def index():
    school = School()

    if request.method == 'POST':
        abr = request.form.get('abr')
        name = request.form.get('name')
        if not abr or not name: return {'message':"Formdata 'abr' odr 'name' not exists"}, 400
        subject = Subject(abr, name)
        res = subject.add()

        if res == 1: return {'message':'Data not correct'}, 400
        if res == 3: return {'message':'Subject allready exists'}, 409
        location = '/subjects/' + subject.abr
        return subject.to_dict(), 201, {'Location':location}

    subjects = school.subjects
    if len(subjects) == 0: return '', 204
    return [subject.to_dict() for subject in subjects]

@subject_bp.route('/<sub_abr>')
def subject(sub_abr):
    subject = Subject(sub_abr)

    if not subject.exists(): return {'message':'Subject not found'}, 404

    return subject.to_dict()