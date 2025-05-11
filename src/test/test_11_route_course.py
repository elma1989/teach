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

def  test_single_course_get(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201'
    fail_course_url = teachurl + '1/courses/ENG%201'
    john_deu1_url = teachurl + '1/courses/DEU%201'
    mat1_url = teachurl + '1/courses/MAT%201'
    deu1_url = teachurl + '2/courses/DEU%201'
    
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

    rg_teach_fail = requests.get(fail_teach_url)
    rg_course_fail = requests.get(fail_course_url)
    rg_john_deu1 = requests.get(john_deu1_url)
    rg_mat1 = requests.get(mat1_url)
    rg_deu1 = requests.get(deu1_url)

    assert rg_teach_fail.status_code == 404
    assert rg_course_fail.status_code == 404
    assert rg_john_deu1.status_code == 404
    assert rg_mat1.status_code == 200
    assert rg_deu1.status_code == 200
    mat1_dat = rg_mat1.json()
    deu1_dat = rg_deu1.json()
    assert mat1_dat == rmat1
    assert deu1_dat == rdeu1

def test_course_change_leader(teachurl):
    john_deu1_url = teachurl + '1/courses/DEU%201'
    maxm_deu1_url = teachurl + '2/courses/DEU%201'
    header = {'Content-Type':'application/json'}

    pl_fail_teacher = {'newLeaderId':3}
    pl_john = {'newLeaderId':1}
    rdeu1 = {
        'name':'DEU 1',
        'subject':{
            'abr':'DEU',
            'name':'Deutsch'
        }
    }

    rg_john_deu1 = requests.get(john_deu1_url)
    rg_maxm_deu1 = requests.get(maxm_deu1_url)
    rpat_fail_teacher = requests.patch(maxm_deu1_url, json.dumps(pl_fail_teacher), headers=header)
    rpat_john = requests.patch(maxm_deu1_url, json.dumps(pl_john), headers=header)
    rg_john_deu2 = requests.get(john_deu1_url)
    rg_maxm_deu2 = requests.get(maxm_deu1_url)

    assert rg_john_deu1.status_code == 404
    assert rg_maxm_deu1.status_code == 200
    assert rpat_fail_teacher.status_code == 404
    assert rpat_john.status_code == 204
    assert rg_john_deu2.status_code == 200
    assert rg_maxm_deu2.status_code == 404
    data = rg_john_deu2.json()
    assert data == rdeu1