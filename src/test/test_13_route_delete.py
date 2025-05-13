import requests

def test_delete_lesson(teachurl):
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30'
    rd_les = requests.delete(les_url)
    assert rd_les.status_code == 204

def test_delete_course(teachurl):
    mat1_url = teachurl + '1/courses/MAT%201'
    rd_mat1 = requests.delete(mat1_url)
    assert rd_mat1.status_code == 204