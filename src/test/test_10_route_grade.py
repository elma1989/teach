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
    cls09 = {
        'name': '09a',
        'teach-id': 2
    }
    rcls10 = {'name': '10a'}
    rcls09 = {'name': '09a'}

    rg_grades1 = requests.get(grades)
    rp_fail = requests.post(grades, fail)
    rp_fail_leader = requests.post(grades, fail_leader)
    rp_cls101 = requests.post(grades, cls10)
    rp_cls102 = requests.post(grades, cls10)
    rp_cls09 = requests.post(grades, cls09)
    rg_grades2 = requests.get(grades)

    assert rg_grades1.status_code == 204
    assert rp_fail.status_code == 400
    assert rp_fail_leader.status_code == 404
    assert rp_cls101.status_code == 201
    assert rp_cls102.status_code == 409
    assert rp_cls09.status_code == 201
    assert rg_grades2.status_code == 200
    data = rg_grades2.json()
    assert data == [rcls09, rcls10]

def test_grade_students(url):
    fail_grade_url = url + '/grades/08a/students'
    cls10a_url = url + '/grades/10a/students'
    cls09a_url = url + '/grades/09a/students'
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
    rp_fail_student = requests.post(cls10a_url, json.dumps(fail_student), headers=header)
    rp_fail_birth = requests.post(cls10a_url, json.dumps(fail_birth_date), headers=header)
    rp_carl1 = requests.post(cls10a_url, json.dumps(carl), headers=header)
    rp_carl2 = requests.post(cls10a_url, json.dumps(carl), headers=header)
    rp_lotte = requests.post(cls09a_url, json.dumps(lotte), headers=header)
    rg_cls10a2 = requests.get(cls10a_url)
    rg_cls09 = requests.get(cls09a_url)

    assert rg_fail.status_code == 404
    assert rp_fail_student.status_code == 400
    assert rp_fail_birth.status_code == 400
    assert rg_cls10a1.status_code == 204
    assert rp_carl1.status_code == 201
    assert rp_carl2.status_code == 409
    assert rp_lotte.status_code == 201
    assert rg_cls10a2.status_code == 200
    assert rg_cls10a2.status_code == 200
    assert rg_cls09.status_code == 200

def test_grade_info(url):
    fail_url = url + '/grades/07a'
    cls08a_url = url + '/grades/08a'
    cls09a_url = url + '/grades/09a'
    cls10a_url = url + '/grades/10a'
    header = {'Content-Type':'application/json'}

    pl_cls10a = {'name':'10a'}
    pl_cls08a = {'name':'08a'}
    pl_fail_leader = {'lederId':3}
    pl_john = {'leaderId':1}

    rg_fail = requests.get(fail_url)
    rg_cls09a = requests.get(cls09a_url)
    rg_cls10a = requests.get(cls10a_url)
    rpat_cls10a = requests.patch(cls09a_url, json.dumps(pl_cls10a), headers=header)
    rpat_cls08a = requests.patch(cls09a_url, json.dumps(pl_cls08a), headers=header)
    rpat_fail_leader = requests.patch(cls09a_url, json.dumps(pl_fail_leader), headers=header)
    rpat_john = requests.patch(cls08a_url, json.dumps(pl_john), headers=header)

    assert rg_fail.status_code == 404
    assert rg_cls09a.status_code == 200
    assert rg_cls10a.status_code == 200
    assert rpat_cls10a.status_code == 409
    assert rpat_cls08a.status_code == 204
    assert rpat_fail_leader.status_code == 404
    assert rpat_john.status_code == 204