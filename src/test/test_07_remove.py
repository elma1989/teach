from database import School, Course, Lesson

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