import requests
from database import indb

def test_remove_with_reference(url):
    john_url = url + '/teachers/1'
    maxm_url = url + '/teachers/2'
    mat_url = url + '/subjects/MAT'
    deu_url = url + '/subjects/DEU'

    rd_john = requests.delete(john_url)
    rd_maxm = requests.delete(maxm_url)
    rd_mat = requests.delete(mat_url)
    rd_deu = requests.delete(deu_url)

    assert rd_john.status_code == 409
    assert rd_maxm.status_code == 409
    assert rd_mat.status_code == 409
    assert rd_deu.status_code == 409

def test_delete_lesson(teachurl):
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30'
    rd_les = requests.delete(les_url)
    assert rd_les.status_code == 204

def test_delete_course(teachurl):
    mat1_url = teachurl + '1/courses/MAT%201'
    deu1_url = teachurl + '1/courses/DEU%201'
    rd_mat1 = requests.delete(mat1_url)
    rd_deu1 = requests.delete(deu1_url)
    assert rd_mat1.status_code == 204
    assert rd_deu1.status_code == 204


def test_delete_student(url):
    carl_url =  url + '/grades/10a/students/1'
    lotte_url = url + '/grades/10a/students/2'
    rd_carl = requests.delete(carl_url)
    rd_lotte = requests.delete(lotte_url)
    assert rd_carl.status_code == 204
    assert rd_lotte.status_code == 204

def test_delete_grade(url):
    cls08a_url = url + '/grades/08a'
    cls10a_url = url + '/grades/10a'
    rd_cls08a = requests.delete(cls08a_url)
    rd_cls10a = requests.delete(cls10a_url)
    assert rd_cls08a.status_code == 204
    assert rd_cls10a.status_code == 204

def test_delete_teacher(teachurl):
    john_url = teachurl + '1'
    maxm_url = teachurl + '2'
    rd_john = requests.delete(john_url)
    rd_maxm = requests.delete(maxm_url)
    assert rd_john.status_code == 204
    assert rd_maxm.status_code == 204

def test_delet_subject(url):
    mat_url = url + '/subjects/MAT'
    deu_url = url + '/subjects/DEU'

    rd_mat = requests.delete(mat_url)
    rd_deu = requests.delete(deu_url)

    assert rd_mat.status_code == 204
    assert rd_deu.status_code == 204

    indb()