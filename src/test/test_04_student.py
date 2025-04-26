from database import Student, Grade, School

def test_student_add():
    school = School()
    fail = Student('carl', 'friedrich','01.01.2010')
    carl = Student('Carl Friedrich', 'Gauß', '1777-04-30')
    lotte = Student('Lotte','Rie','2010-05-05')

    assert fail.add() == 1
    assert not carl.exists()
    assert carl.add() == 0
    assert carl.add() == 3
    assert carl.exists()
    assert school.getStudent(1) == carl

    assert not lotte.exists()
    assert lotte.add() == 0
    assert lotte.add() == 3
    assert lotte.exists()
    assert school.getStudent(2) == lotte

def test_student_grade():
    school = School()
    carl = school.getStudent(1)
    lotte = school.getStudent(2)
    fail = Grade('09a')
    cls10a = Grade('10a')

    carl.grade = fail
    assert not carl.grade
    assert not school.students(fail)

    assert school.students(cls10a) == []
    carl.grade = cls10a
    assert carl.grade == cls10a
    assert school.students(cls10a) == [carl]

    lotte.grade = cls10a
    assert lotte.grade == cls10a
    assert school.students(cls10a) == [carl, lotte]

def test_student_to_dict():
    school = School()
    carl = school.getStudent(1)
    test = {
        'id':1,
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate': '1777-04-30'
    }

    assert carl.to_dict() == test