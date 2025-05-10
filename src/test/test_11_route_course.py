import requests,json

def test_teacher_course(teachurl):
    fail_url = teachurl + '3/courses'
    john_url = teachurl + '1/courses'
    maxm_url = teachurl + '2/courses'
    header = {'Content-Type':'application/json'}

    pl_eng = {
        'courseName':'ENG 1',
        'subAbr':'eng'
    }
    pl_mat = {
        'courseName':'MAT 1',
        'subAbr':'mat'
    }
    pl_deu = {
        'courseName':'DEU 1',
        'subAbr':'deu'
    }

    rmat1 = {
        'name':'MAT 1',
        'subject':{
            'abr':'MAT',
            'name':'Mathematik'
        }
    }
    rdeu1 = {
        'name':'DEU 1',
        'subject':{
            'abr':'DEU',
            'name':'Deutsch'
        }
    }

    rg_fail = requests.get(fail_url)
    rg_john1 = requests.get(john_url)
    rg_maxm1 = requests.get(maxm_url)
    rp_john_eng = requests.post(john_url, json.dumps(pl_eng), headers=header)
    rp_maxm_mat = requests.post(maxm_url, json.dumps(pl_mat), headers=header)
    rp_john_mat1 = requests.post(john_url, json.dumps(pl_mat), headers=header)
    rp_john_mat2 = requests.post(john_url, json.dumps(pl_mat), headers=header)
    rp_maxm_deu = requests.post(maxm_url, json.dumps(pl_deu), headers=header)
    rg_john2 = requests.get(john_url)
    rg_maxm2 = requests.get(maxm_url)

    assert rg_fail.status_code == 404
    assert rg_john1.status_code == 204
    assert rg_maxm1.status_code == 204
    assert rp_john_eng.status_code == 404
    assert rp_maxm_mat.status_code == 404
    assert rp_john_mat1.status_code == 201
    assert rp_john_mat2.status_code == 409
    assert rp_maxm_deu.status_code == 201

    assert rg_john2.status_code == 200
    assert rg_maxm2.status_code == 200
    john_courses = rg_john2.json()
    maxm_courses = rg_maxm2.json()
    assert john_courses == [rmat1]
    assert maxm_courses == [rdeu1]