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
    
    assert school.grades == []
    assert school.grades_of(maxm) == []
    assert grd09a.add() == 0
    assert grd09a.add() == 3
    assert school.grades_of(maxm) == [grd09a]
    assert school.grades == [grd09a]

    assert school.grades_of(john) == []
    assert grd10a.add() == 0
    assert school.grades_of(john) == [grd10a]
    assert school.grades == [grd09a, grd10a]