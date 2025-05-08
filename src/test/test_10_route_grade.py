import requests

def test_grade_index(url):
    grades = url + '/grades/'

    fail = {}
    fail_leader = {
        'name': '10a',
        'teach-id': 3
    }
    cls10 = {
        'name': '10a',
        'teach-id': 1
    }
    rcls10 = {'name': '10a'}

    rg_grades1 = requests.get(grades)
    rp_fail = requests.post(grades, fail)
    rp_fail_leader = requests.post(grades, fail_leader)
    rp_cls10 = requests.post(grades, cls10)
    rg_grades2 = requests.get(grades)

    assert rg_grades1.status_code == 204
    assert rp_fail.status_code == 400
    assert rp_fail_leader.status_code == 404
    assert rp_cls10.status_code == 201
    assert rg_grades2.status_code == 200
    data = rg_grades2.json()
    assert data == [rcls10]