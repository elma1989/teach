import requests,json

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

def test_grade_students(url):
    fail_grade_url = url + '/grades/09a/students'
    cls10a_url = url + '/grades/10a/students'
    header = {'Content-Type':'application/json'}

    fail_student = {}
    fail_birth_date = {
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'30.04.1777'
    }
    carl = {
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'1777-04-30'
    }
    lotte = {
        'fname':'Lotte',
        'lname':'Rie',
        'birthDate':'2010-05-05'
    }
    rcarl = {
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'1777-04-30',
        'id': 1
    }
    rlotte = {
        'fname':'Lotte',
        'lname':'Rie',
        'birthDate':'2010-05-05',
        'id': 2
    }

    rg_fail = requests.get(fail_grade_url)
    rg_cls10a1 = requests.get(cls10a_url)
    rp_carl1 = requests.post(cls10a_url, json.dumps(carl), headers=header)
    rp_carl2 = requests.post(cls10a_url, json.dumps(carl), headers=header)
    rp_lotte = requests.post(cls10a_url, json.dumps(lotte), headers=header)
    rg_cls10a2 = requests.get(cls10a_url)

    assert rg_fail.status_code == 404
    assert rg_cls10a1.status_code == 204
    assert rp_carl1.status_code == 201
    assert rp_carl2.status_code == 409
    assert rp_lotte.status_code == 201
    assert rg_cls10a2.status_code == 200