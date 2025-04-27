from database import School, Course, Teacher, Subject

def test_course_add():
    school = School()
    john = school.getTeacher(1)
    maxm = school.getTeacher(2)
    isaac = Teacher('Isasc', 'Newton', '1643-01-04')
    mat = Subject('mat')
    deu = Subject('deu')
    eng = Subject('eng')

    mat1 = Course('MAT 1', john, mat)
    mat2 = Course('MAT 2', maxm, mat)
    mat3 = Course('MAT 3', isaac, mat)
    deu1 = Course('DEU 1', john, deu)
    deu2 = Course('DEU 2', maxm, deu)
    eng1 = Course('ENG 1', john, eng)

    assert school.courses == []
    assert school.courses_of(john) == []
    assert school.courses_of(maxm) == []
    assert not school.courses_of(isaac)
    assert mat3.add() == 2
    assert eng1.add() == 2

    assert not mat1.exists()
    assert mat1.add() == 0
    assert mat1.add() == 3
    assert mat1.exists()
    assert school.courses_of(john) == [mat1]
    assert school.courses == [mat1]

    assert not mat2.exists()
    assert mat2.add() == 0
    assert mat2.exists()
    assert school.courses_of(maxm) == [mat2]
    assert school.courses == [mat1, mat2]

    assert not deu1.exists()
    assert deu1.add() == 0
    assert deu1.exists()
    assert school.courses_of(john) == [deu1, mat1]
    assert school.courses == [deu1, mat1, mat2]

    assert not deu2.exists()
    assert deu2.add() == 0
    assert deu2.exists()
    assert school.courses_of(maxm) == [deu2, mat2]
    assert school.courses == [deu1, deu2, mat1, mat2]

def test_course_leader():
    school = School()
    john = school.getTeacher(1)
    maxm = school.getTeacher(2)
    isaac = Teacher('Isasc', 'Newton', '1643-01-04')
    deu2 = Course('DEU 2')

    deu2.leader = isaac
    assert deu2.leader == maxm

    deu2.leader = john
    assert deu2.leader == john

def test_course_to_dict():
    mat1 = Course('MAT 1')
    test = {
        'name':'MAT 1',
        'subject':{
            'abr':'MAT',
            'name':'Mathematik'
        }
    }
    assert mat1.to_dict() == test