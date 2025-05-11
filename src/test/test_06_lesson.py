from database import School, Lesson, Course, Student

def test_lesson_add():
    school = School()
    mat1 = Course('MAT 1')
    eng1 = Course('ENG 1')
    fail1 = Lesson(eng1, '2025-04-01 08:00')
    fail2 = Lesson(mat1, '01.04.2025 08:00')
    les1 = Lesson(mat1, '2025-04-01 08:00')
    les2 = Lesson(mat1, '2025-04-01 09:30')

    assert school.lessons(mat1) == []
    assert not school.lessons(eng1)
    assert fail1.add() == 2
    assert fail2.add() == 1

    assert not les1.exists()
    assert les1.add() == 0
    assert les1.add() == 3
    assert les1.exists()
    assert school.lessons(mat1) == [les1]

    assert not les2.exists()
    assert les2.add() == 0
    assert les2.exists()
    assert school.lessons(mat1) == [les1, les2]

def test_lesson_topic():
    les1 = Lesson(Course('MAT 1'),'2025-04-01 08:00')

    les1.topic = 'Gaußscher Algorithmus'
    assert les1.topic == 'Gaußscher Algorithmus'

def test_lesson_to_dict():
    les1 = Lesson(Course('MAT 1'),'2025-04-01 08:00')
    test = {
        'course':'MAT 1',
        'time':'2025-04-01 08:00',
        'topic':'Gaußscher Algorithmus'
    }

    assert les1.to_dict() == test

def test_lessson_add_homework():
    task1 = 'LGS Lösen'
    task2 = 'LB. S. 250'
    mat1 = Course('MAT 1')
    fail1 = Lesson(Course('ENG 1'), '2025-04-01 08:00')
    fail2 = Lesson(mat1, '2025-04-01 10:00')
    les1 = Lesson(mat1, '2025-04-01 08:00')

    assert fail1.add_homework(task1) == 1
    assert fail2.add_homework(task1) == 1

    assert les1.add_homework(task1) == 0
    assert les1.add_homework(task1) == 2
    assert les1.homeworks == [task1]
    assert les1.add_homework(task2) == 0
    assert les1.homeworks == [task2, task1]

def test_set_present_status():
    school = School()
    carl = school.getStudent(1)
    lotte = school.getStudent(2)
    les1 = Lesson(Course('MAT 1'),'2025-04-01 08:00')
    les2 = Lesson(Course('MAT 1'),'2025-04-01 10:00')

    assert les1.set_present_status([True]) == 1
    assert les1.set_present_status([1.2,3]) == 1
    assert les2.set_present_status([True, False]) == 2

    assert les1.set_present_status([True, False]) == 0
    assert les1.students == [(carl, True), (lotte, False)]
    assert les1.set_present_status([False, True]) == 0
    assert les1.students == [(carl, False), (lotte, True)]
    assert les1.set_present_status([True, True]) == 0
    assert les1.students == [(carl, True), (lotte, True)]