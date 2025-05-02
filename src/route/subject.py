from flask import Blueprint, request, Response, jsonify
import json
from database import School, Subject

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')

@subject_bp.route('/', methods=['GET','POST'])
def index():
    school = School()

    if request.method == 'POST':
        data = json.loads(request.data.decode())

        if not data.get('abr') or not data.get('name'): return {'message':'Nesseary Fields not given'}, 400
        
        subject = Subject(data['abr'], data['name'])
        res = subject.add()

        if res == 1: return {'message':'Data not correct'}, 400
        if res == 3: return {'message':'Subject already exists'}, 409

        location = '/subject/' + subject.abr.lower()
        return {'message':'Subject successfully created'}, 201, {'Content-Type':'application/json', 'Location':location}

    if len(school.subjects) == 0: return {'message':'No Subjects exists'}, 404
    return [subject.to_dict() for subject in school.subjects]

@subject_bp.route('/<abr>')
def subject(abr):
    subject = Subject(abr)

    if not subject.exists(): return {'message':'Subject does not exist'}, 404

    return subject.to_dict()