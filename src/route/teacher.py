from flask import Blueprint, request
from database import School, Teacher, Subject, Course, Lesson

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

@teacher_bp.route('/<int:teach_id>/subjects', methods=['GET','POST'])
def teacher_subject(teach_id):
    school = School ()
    teacher = school.getTeacher(teach_id)

    if not teacher: return {'message':'Teacher not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        abr = data.get('subAbr')
        if not abr: return {'message':"JSON-Field 'subAbr' does not exist"}, 400
        subject = Subject(abr)
        res = teacher.add_subject(subject)

        if res == 1: return {'message':'Subject not found'}, 404
        if res == 2: return {'message':'This teacher allready teaches that Subject'}, 409
        location = f'/subjects/{subject.abr}'
        return {'message':'Subject added to teacher'}, 201, {'Location':location}

    subjects = teacher.subjects
    if len(subjects) == 0: return '', 204
    return [subject.to_dict() for subject in subjects]

@teacher_bp.route('/<int:teach_id>/courses', methods=['GET','POST'])
def course(teach_id):
    school = School()
    teacher = school.getTeacher(teach_id)

    if not teacher: return {'messsage':'Teacher not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        crs_name = data.get('courseName')
        sub_abr = data.get('subAbr')
        if not crs_name or not sub_abr: return {'message':"'courseName' or 'subAbr' not in JSON"}, 400
        subject = Subject(sub_abr)

        if not subject.exists(): return {'message':'Subject not found'}, 404
        if not subject in teacher.subjects: return {'message':'Subject in Teacher Subjects not found'}, 404

        course = Course(crs_name, teacher, subject)
        res = course.add()

        if res == 3: return {'message':'Course allready exists'}, 409
        location = f'/teachers/{teacher.id}/courses/{course.name.replace(' ','%20')}'
        return course.to_dict(), 201, {'Location':location}

    courses = school.courses_of(teacher)
    if len(courses) == 0: return '', 204
    return [course.to_dict() for course in courses]

@teacher_bp.route('/<int:teach_id>/courses/<course_name>', methods=['GET','PATCH'])
def single_course(teach_id, course_name):
    school = School()
    teacher = school.getTeacher(teach_id)
    course = Course(course_name)

    if not teacher: return {'messsage':'Teacher not found'}, 404
    if not course.exists(): return {'message':'Course not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'PATCH':
        data = request.json
        if data.get('newLeaderId'):
            teacher = school.getTeacher(data['newLeaderId'])
            if not teacher: return {'message':'New teacher not found'}, 404
            course.leader = teacher
        return '', 204

    if not course in school.courses_of(teacher): return {'message':'Course in Teachers Courses not found'}, 404

    return course.to_dict()

@teacher_bp.route('/<int:teach_id>/courses/<course_name>/members', methods=['GET','POST'])
def course_members(teach_id, course_name):
    school = School()
    teacher = school.getTeacher(teach_id)
    course = Course(course_name)

    if not teacher: return {'messsage':'Teacher not found'}, 404
    if not course.exists(): return {'message':'Course not found'}, 404
    if not course in school.courses_of(teacher): return {'message':'Course in Teachers Courses not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        if not data.get('newMemberId'): return {'message':"'newMemberId' missing"}, 400
        student = school.getStudent(data['newMemberId'])
        if not student: return {'message':'Student not found'}, 404
        res = course.add_student(student)

        if res == 3: return {'message':'Student in this course allready exists'}, 409
        location = f'/grades/{student.grade.name}/students/{student.id}'
        return student.to_dict(), 201, {'Location':location}

    students = course.students
    if len(students) == 0: return '', 204
    return [student.to_dict() for student in students]

@teacher_bp.route('/<int:teach_id>/courses/<course_name>/lessons', methods=['GET','POST'])
def course_lessons(teach_id, course_name):
    school = School()
    teacher = school.getTeacher(teach_id)
    course = Course(course_name)

    if not teacher: return {'messsage':'Teacher not found'}, 404
    if not course.exists(): return {'message':'Course not found'}, 404
    if not course in school.courses_of(teacher): return {'message':'Course in Teachers Courses not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'POST':
        data = request.json
        if not data.get('time'): return {'message':"'time' missing"}, 400
        time = data['time'].replace('T',' ')
        lesson = Lesson(course, time)
        res = lesson.add()

        if res == 1: return {'message':'Time-Format ist not correct'}, 400
        if res == 3: return {'message':'Lesson allready exists'}, 409
        location = f'/teachers/{teacher.id}/courses/{course.name.replace(' ','%20')}/lessons/{lesson.db_time.replace(' ', '%20')}'
        return lesson.to_dict(), 201, {'Location':location}

    lessons = school.lessons(course)
    if len(lessons) == 0: return '', 204
    return [lesson.to_dict() for lesson in lessons]

@teacher_bp.route('/<int:teach_id>/courses/<course_name>/lessons/<les_time>', methods=['GET','PATCH'])
def course_single_lesson(teach_id, course_name, les_time):
    school = School()
    teacher = school.getTeacher(teach_id)
    course = Course(course_name)

    if not teacher: return {'messsage':'Teacher not found'}, 404
    if not course.exists(): return {'message':'Course not found'}, 404
    if not course in school.courses_of(teacher): return {'message':'Course in Teachers Courses not found'}, 404

    lesson = Lesson(course, les_time)
    if not lesson.exists(): return {'message':'Lesson not found'}, 404

    if request.headers.get('Content-Type') == 'application/json' and request.method == 'PATCH':
        data = request.json
        if data.get('topic'): lesson.topic = data['topic']
        if data.get('newTime'):
            time = data['newTime'].replace('T',' ')
            lesson.time = time
            if lesson.db_time != time: return {'message':'Time format is not Correct'}, 400
        return '', 204

    if not lesson in school.lessons(course): return {'message':'Lesson in this course not found'}, 404

    return lesson.to_dict()