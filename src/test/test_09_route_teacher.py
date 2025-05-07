import requests

def test_teacher_index(teachurl):
    fail = {}
    fail_name = {
        'fname':'john',
        'lname':'doe',
        'birth_date':'1990-01-01' 
    }
    fail_birth = {
        'fname':'John',
        'lname':'Doe',
        'birth_date':'01.01.1990'
    }
    john = {
        'fname':'John',
        'lname':'Deo',
        'birth_date':'1990-01-01',
        'id': 1
    }
    maxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birth_date':'1991-12-31',
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
    assert data == [john, maxm]