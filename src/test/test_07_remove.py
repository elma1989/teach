from database import School, Course, Lesson, Teacher, Grade

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
    deu1 = Course('DEU 1')
    deu2 = Course('DEU 2')
    eng1 = Course('ENG 1')

    assert eng1.remove() == 1
    assert mat1.remove() == 0
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