from database import Teacher, School, Subject

def test_teacher_add():
    fail1 = Teacher('john','Doe','1990-01-01')
    fail2 = Teacher('John','doe','1990-01-01')
    fail3 = Teacher('John','Doe','01.01.1990')

    john = Teacher('John','Doe','1990-01-01')
    maxm = Teacher('Max','Mustermann','1991-12-31')
    school = School()

    assert fail1.add() == 1
    assert fail2.add() == 1
    assert fail3.add() == 1

    assert school.teachers == []
    assert not john.exists()
    assert john.add() == 0
    assert john.id == 1
    assert john.exists()
    assert john.add() == 3
    assert school.teachers == [john]
    assert school.getTeacher(1) == john

    assert not maxm.exists()
    assert maxm.add() == 0
    assert maxm.exists()
    assert school.teachers == [john, maxm]
    assert school.getTeacher(2) == maxm

    assert not school.getTeacher(3)

def test_teacher_add_subject():
    school = School()
    john = school.getTeacher(1)
    print(john)
    print(john.subjects)
    eng = Subject('eng')
    mat = Subject('mat')
    deu = Subject('deu')

    assert john.subjects == []
    assert john.add_subject(eng) == 1
    assert john.add_subject(mat) == 0
    assert john.subjects == [mat]
    assert john.add_subject(mat) == 2
    assert john.subjects == [mat]
    assert john.add_subject(deu) == 0
    assert john.subjects == [deu, mat]