from database import School, Grade, Teacher

def test_grade_add():
    school = School()
    isaac = Teacher('Isaac','Newton', '1643-01-04')
    john = school.getTeacher(1)
    maxm = school.getTeacher(2)

    grd08a = Grade('08a', isaac)
    grd09a = Grade('09a', maxm)
    grd10a = Grade('10a', john)

    assert grd08a.add() == 2
    assert not grd08a.exists()
    
    assert school.grades == []
    assert school.grades_of(maxm) == []
    assert not grd09a.exists()
    assert grd09a.add() == 0
    assert grd09a.add() == 3
    assert grd09a.exists()
    assert school.grades_of(maxm) == [grd09a]
    assert school.grades == [grd09a]

    assert school.grades_of(john) == []
    assert not grd10a.exists()
    assert grd10a.add() == 0
    assert grd10a.exists()
    assert school.grades_of(john) == [grd10a]
    assert school.grades == [grd09a, grd10a]

def test_grade_setter():
    school = School()
    grd09a = Grade('09a')
    john = school.getTeacher(1)
    maxm = school.getTeacher(2)
    isaac = Teacher('Isaac','Newton', '1643-01-04')

    assert grd09a.leader == maxm
    
    grd09a.name = '10a'
    assert grd09a.name == '09a'
    grd09a.name = '08a'
    assert grd09a.name == '08a'

    grd09a.leader = isaac
    print(grd09a.leader)
    assert grd09a.leader == maxm
    grd09a.leader = john
    assert grd09a.leader == john

def test_grade_to_dict():
    grd10a = Grade('10a')
    
    assert grd10a.to_dict() == {'name':'10a'}