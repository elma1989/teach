from database import School, Course, Lesson, Teacher, Grade, Student, Subject

def  test_remove_reference():
    school = School()
    maxm = school.getTeacher(2)
    deu = Subject('deu')

    assert maxm.remove() == 2
    assert deu.remove() == 2

def test_remove_lesson():
    school = School()
    mat1 = Course('MAT 1')
    les1 = Lesson(mat1, '2025-04-01 08:00')
    les2 = Lesson(mat1, '2025-04-01 09:30')
    les3 = Lesson(mat1, '2025-04-01 10:00')
    les4 = Lesson(Course('ENG 1'), '2025-04-01 08:00')

    assert les3.remove() == 1
    assert les4.remove() == 1

    assert les1.remove() == 0
    assert school.lessons(mat1) == [les2]

def test_remove_course():
    school = School()
    john = school.getTeacher(1)
    mat1 = Course('MAT 1')
    mat2 = Course('MAT 2')
    deu1 = Course('DEU 1')
    deu2 = Course('DEU 2')
    eng1 = Course('ENG 1')

    assert eng1.remove() == 1
    assert mat1.remove() == 0
    assert mat2.remove() == 0
    assert school.courses_of(john) == [deu1, deu2]

def test_remove_grade():
    school = School()
    carl = school.getStudent(1)
    lotte = school.getStudent(2)
    cls09a = Grade('09a')
    cls08a = Grade('08a')
    cls10a = Grade('10a')

    assert cls09a.remove() == 1
    assert cls10a.remove() == 0
    assert school.grades == [cls08a]
    assert not carl.grade
    assert not lotte.grade

def test_remove_student():
    school = School()
    carl = school.getStudent(1)
    lotte = school.getStudent(2)
    ernst = Student('Ernst','des Lebens', '2010-05-05')

    assert ernst.remove() == 1
    assert lotte.remove() == 0
    assert school.students(None) == [carl]

def test_remove_teacher():
    school = School()
    john = school.getTeacher(1)
    maxm = school.getTeacher(2)
    isaac = Teacher('Isaac', 'Newton', '1643-01-04', 5)

    assert isaac.remove() == 1
    assert maxm.remove() == 0
    assert school.teachers == [john]

def test_remove_teacher_subject():
    school = School()
    eng = Subject('eng')
    mat = Subject('mat')
    deu = Subject('deu')
    john = school.getTeacher(1)
    isaac = Teacher('Isaac', 'Newton', '1643-01-04', 5)
    deu1 = Course('DEU 1')
    deu2 = Course('DEU 2')

    assert isaac.del_subject(deu) == 1
    assert john.del_subject(eng) == 1
    assert john.del_subject(deu) == 2

    assert deu1.remove() == 0
    assert deu2.remove() == 0
    assert john.del_subject(deu) == 0
    assert john.subjects == [mat]

def test_remove_subject():
    eng = Subject('eng')
    deu = Subject('deu')

    assert eng.remove() == 1
    assert deu.remove() == 0