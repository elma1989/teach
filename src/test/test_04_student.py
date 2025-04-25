from database import Student, Grade, School

def test_student_add():
    fail = Student('carl', 'friedrich','01.01.2010')
    carl = Student('Carl Friedrich', 'Gauß', '1777-04-30')
    lotte = Student('Lotte','Rie','2010-05-05')

    assert fail.add() == 1
    assert not carl.exists()
    assert carl.add() == 0
    assert carl.add() == 3
    assert carl.exists()

    assert not lotte.exists()
    assert lotte.add() == 0
    assert lotte.add() == 3
    assert lotte.exists()
