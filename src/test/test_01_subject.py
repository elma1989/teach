from database import indb, School, Subject

def test_subject_add():
    fail1 = Subject('eng')
    fail2 = Subject('e2n')
    fail3 = Subject('englisch', 'Englisch')
    fail4 = Subject('eng', 'englisch')

    mat = Subject('mat', 'Mathematik')
    deu = Subject('deu', 'Deutsch')
    school = School()

    indb()

    assert fail1.add() == 1
    assert fail2.add() == 1
    assert fail3.add() == 1
    assert fail4.add() == 1

    assert school.subjects == []
    assert not mat.exists()
    assert mat.add() == 0
    assert mat.add() == 3
    assert mat.exists()
    assert school.subjects == [mat]

    assert not deu.exists()
    assert deu.add() == 0
    assert deu.exists()
    assert school.subjects == [deu, mat]
