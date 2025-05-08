import requests,json

def test_teacher_index(teachurl):
    fail = {}
    fail_name = {
        'fname':'john',
        'lname':'doe',
        'birth-date':'1990-01-01' 
    }
    fail_birth = {
        'fname':'John',
        'lname':'Doe',
        'birth-date':'01.01.1990'
    }
    john = {
        'fname':'John',
        'lname':'Doe',
        'birth-date':'1990-01-01'
    }
    maxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birth-date':'1991-12-31'
    }
    rjohn = {
        'fname':'John',
        'lname':'Doe',
        'birthDate':'1990-01-01',
        'id': 1
    }
    rmaxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birthDate':'1991-12-31',
        'id': 2
    }

    rg_teachers1 = requests.get(teachurl)
    rp_fail = requests.post(teachurl, fail)
    rp_fail_name = requests.post(teachurl, fail_name)
    rp_fail_birth = requests.post(teachurl, fail_birth)
    rp_john1 = requests.post(teachurl, john)
    rp_john2 = requests.post(teachurl, john)
    rp_maxm = requests.post(teachurl, maxm)
    rg_teachers2 = requests.get(teachurl)

    assert rg_teachers1.status_code == 204
    assert rp_fail.status_code == 400
    assert rp_fail_name.status_code == 400
    assert rp_fail_birth.status_code == 400
    assert rp_john1.status_code == 201
    assert rp_john2.status_code == 409
    assert rp_maxm.status_code == 201
    assert rg_teachers2.status_code == 200
    data = rg_teachers2.json()
    assert data == [rjohn, rmaxm]

def test_teacher_info(teachurl):
    fail_teacher_url = teachurl + '3'
    john_url = teachurl + '1'
    maxm_url = teachurl + '2'
    
    john = {
        'fname':'John',
        'lname':'Doe',
        'birth-date':'1990-01-01'
    }
    maxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birth-date':'1991-12-31'
    }
    rjohn = {
        'fname':'John',
        'lname':'Doe',
        'birthDate':'1990-01-01',
        'id': 1
    }
    rmaxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birthDate':'1991-12-31',
        'id': 2
    }

    rg_fail_teacher = requests.get(fail_teacher_url)
    rg_john = requests.get(john_url)
    rg_maxm = requests.get(maxm_url)

    assert rg_fail_teacher.status_code == 404
    assert rg_john.status_code == 200
    assert rg_maxm.status_code == 200

    johndata = rg_john.json()
    maxmdata = rg_maxm.json()
    assert johndata == rjohn
    assert maxmdata == rmaxm

def test_teacher_subject(teachurl):
    fail_teacher_url = teachurl + '3/subjects'
    john_url = teachurl + '1/subjects'
    header = {'Content-Type':'application/json'}

    mat = {'subAbr':'mat'}
    deu = {'subAbr':'deu'}
    eng = {'subAbr':'eng'}
    rmat = {
        'abr':'MAT',
        'name':'Mathematik'
    }
    rdeu = {
        'abr':'DEU',
        'name':'Deutsch'
    }

    rg_fail_teacher = requests.get(fail_teacher_url)
    rg_john1 = requests.get(john_url)
    rp_john_eng = requests.post(john_url,json.dumps(eng), headers=header)
    rp_john_mat1 = requests.post(john_url,json.dumps(mat), headers=header)
    rp_john_mat2 = requests.post(john_url,json.dumps(mat), headers=header)
    rp_john_deu = requests.post(john_url,json.dumps(deu), headers=header)
    rg_john2 = requests.get(john_url)

    assert rg_fail_teacher.status_code == 404
    assert rg_john1.status_code == 204
    assert rp_john_eng.status_code == 404
    assert rp_john_mat1.status_code == 201
    assert rp_john_mat2.status_code == 409
    assert rp_john_deu.status_code == 201
    assert rg_john2.status_code == 200

    data = rg_john2.json()
    assert data == [rdeu, rmat]