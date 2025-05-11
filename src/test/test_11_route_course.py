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

def test_course_members(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201/members'
    fail_course_url = teachurl + '1/courses/ENG%201/members'
    fail_teach_course_url = teachurl + '2/courses/DEU%201/members'
    mat1_url = teachurl + '1/courses/MAT%201/members'
    header = {'Content-Type':'application/json'}

    pl_fail_data = {}
    pl_fail_student = {'newMemberId': 3}
    pl_carl = {'newMemberId': 1}
    pl_lotte = {'newMemberId': 2}

    rcarl = {
        'id':1,
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'1777-04-30'
    }
    rlotte = {
        'id':2,
        'fname':'Lotte',
        'lname':'Rie',
        'birthDate':'2010-05-05'
    }

    rg_fail_teach = requests.get(fail_teach_url)
    rg_fail_course = requests.get(fail_course_url)
    rg_fail_teach_course = requests.get(fail_teach_course_url)
    rg_mat1 = requests.get(mat1_url)
    rp_mat1_fail_data = requests.post(mat1_url, json.dumps(pl_fail_data), headers=header)
    rp_mat1_fail_student = requests.post(mat1_url, json.dumps(pl_fail_student), headers=header)
    rp_mat1_carl1 = requests.post(mat1_url, json.dumps(pl_carl), headers=header)
    rp_mat1_carl2 = requests.post(mat1_url, json.dumps(pl_carl), headers=header)
    rp_mat1_lotte = requests.post(mat1_url, json.dumps(pl_lotte), headers=header)
    rg_mat1_2 = requests.get(mat1_url)

    assert rg_fail_teach.status_code == 404
    assert rg_fail_course.status_code == 404
    assert rg_fail_teach_course.status_code == 404
    assert rg_mat1.status_code == 204
    assert rp_mat1_fail_data.status_code == 400
    assert rp_mat1_fail_student.status_code == 404
    assert rp_mat1_carl1.status_code == 201
    assert rp_mat1_carl2.status_code == 409
    assert rp_mat1_lotte.status_code == 201
    assert rg_mat1_2.status_code == 200
    data = rg_mat1_2.json()
    assert data == [rcarl, rlotte]