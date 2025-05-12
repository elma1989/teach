import requests, json

def test_course_lessons(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201/lessons'
    fail_course_url = teachurl + '1/courses/ENG%201/lessons'
    fail_teach_course_url = teachurl + '2/courses/DEU%201/lessons'
    mat1_url = teachurl + '1/courses/MAT%201/lessons'
    header = {'Content-Type':'application/json'}

    pl_les_fail = {'time':'01.04.2025 08:00'}
    pl_les = {'time':'2025-04-01T08:00'}
    rles1 = {
        'course':'MAT 1',
        'time':'2025-04-01 08:00',
        'topic':''
    }

    rg_fail_teach = requests.get(fail_teach_url)
    rg_fail_course = requests.get(fail_course_url)
    rg_fail_teach_course = requests.get(fail_teach_course_url)
    rg_mat1 = requests.get(mat1_url)
    rp_les_fail = requests.post(mat1_url, json.dumps(pl_les_fail), headers=header)
    rp_les1 = requests.post(mat1_url, json.dumps(pl_les), headers=header)
    rp_les2 = requests.post(mat1_url, json.dumps(pl_les), headers=header)
    rg_mat1_2 = requests.get(mat1_url)

    assert rg_fail_teach.status_code == 404
    assert rg_fail_course.status_code == 404
    assert rg_fail_teach_course.status_code == 404
    assert rg_mat1.status_code == 204
    assert rp_les_fail.status_code == 400
    assert rp_les1.status_code == 201
    assert rp_les2.status_code == 409
    assert rg_mat1_2.status_code == 200
    data = rg_mat1_2.json()
    assert data == [rles1]

def test_single_lesson(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201/lessons/2025-04-01%2008:00'
    fail_course_url = teachurl + '1/courses/ENG%201/lessons/2025-04-01%2008:00'
    fail_teach_course_url = teachurl + '2/courses/DEU%201/lessons/2025-04-01%2008:00'
    fail_time_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:00'
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2008:00'
    les2_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30'
    header = {'Content-Type':'application/json'}

    pl_fail_time = {'newTime':'01.04.2025 09:30'}
    pl_les1 = {
        'newTime':'2025-04-01T09:30',
        'topic':'Gaußscher Algorithmus'
    }

    rles1 = {
        'course':'MAT 1',
        'time':'2025-04-01 08:00',
        'topic':''
    }
    rles2 = {
        'course':'MAT 1',
        'time':'2025-04-01 09:30',
        'topic':'Gaußscher Algorithmus'
    }

    rg_fail_teach = requests.get(fail_teach_url)
    rg_fail_course = requests.get(fail_course_url)
    rg_fail_teach_course = requests.get(fail_teach_course_url)
    rg_fail_time = requests.get(fail_time_url)
    rg_les = requests.get(les_url)
    rp_fail_time = requests.patch(les_url, json.dumps(pl_fail_time), headers=header)
    rg_les_1 = requests.get(les_url)
    rp_les1 = requests.patch(les_url, json.dumps(pl_les1), headers=header)
    rg_les2 = requests.get(les2_url)

    assert rg_fail_teach.status_code == 404
    assert rg_fail_course.status_code == 404
    assert rg_fail_teach_course.status_code == 404
    assert rg_fail_time.status_code == 404
    assert rg_les.status_code == 200
    data = rg_les.json()
    assert data == rles1

    assert rp_fail_time.status_code == 400
    assert rg_les_1.status_code == 200
    data = rg_les_1.json()
    assert data == rles1
    assert rp_les1.status_code == 204
    assert rg_les2.status_code == 200
    data = rg_les2.json()
    assert data == rles2

def test_lesson_homeworks(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201/lessons/2025-04-01%2008:00/homeworks'
    fail_course_url = teachurl + '1/courses/ENG%201/lessons/2025-04-01%2008:00/homeworks'
    fail_teach_course_url = teachurl + '2/courses/DEU%201/lessons/2025-04-01%2008:00/homeworks'
    fail_time_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:00/homeworks'
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30/homeworks'
    header = {'Content-Type':'application/json'}

    pl_fail = {}
    pl_les = {'task':'LGS lösen'}
    les_hw = ['LGS lösen']

    rg_fail_teach = requests.get(fail_teach_url)
    rg_fail_course = requests.get(fail_course_url)
    rg_fail_teach_course = requests.get(fail_teach_course_url)
    rg_fail_time = requests.get(fail_time_url)
    rg_les = requests.get(les_url)
    rp_les_fail = requests.post(les_url, json.dumps(pl_fail), headers=header)
    rp_les = requests.post(les_url, json.dumps(pl_les), headers=header)
    rp_les_2 = requests.post(les_url, json.dumps(pl_les), headers=header)
    rg_les2 = requests.get(les_url)
    
    assert rg_fail_teach.status_code == 404
    assert rg_fail_course.status_code == 404
    assert rg_fail_teach_course.status_code == 404
    assert rg_fail_time.status_code == 404
    assert rg_les.status_code == 204
    assert rp_les_fail.status_code == 400
    assert rp_les.status_code == 201
    assert rp_les_2.status_code == 409
    assert rg_les2.status_code == 200
    data = rg_les2.json()
    assert data == les_hw

def test_lesson_presents_get(teachurl):
    fail_teach_url = teachurl + '3/courses/MAT%201/lessons/2025-04-01%2008:00/presents'
    fail_course_url = teachurl + '1/courses/ENG%201/lessons/2025-04-01%2008:00/presents'
    fail_teach_course_url = teachurl + '2/courses/DEU%201/lessons/2025-04-01%2008:00/presents'
    fail_time_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:00/presents'
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30/presents'

    expect_res = [
        {
            'id':1,
            'fname':'Carl Friedrich',
            'lname':'Gauß',
            'birthDate':'1777-04-30',
            'present': False
        }, {
            'id':2,
            'fname':'Lotte',
            'lname':'Rie',
            'birthDate':'2010-05-05',
            'present': False
        }
    ]

    rg_fail_teach = requests.get(fail_teach_url)
    rg_fail_course = requests.get(fail_course_url)
    rg_fail_teacher_course = requests.get(fail_teach_course_url)
    rg_fail_time = requests.get(fail_time_url)
    rg_les = requests.get(les_url)

    assert rg_fail_teach.status_code == 404
    assert rg_fail_course.status_code == 404
    assert rg_fail_teacher_course.status_code == 404
    assert rg_fail_time.status_code == 404
    assert rg_les.status_code == 200
    data = rg_les.json()
    assert data == expect_res

def test_lesson_presents_put(teachurl):
    les_url = teachurl + '1/courses/MAT%201/lessons/2025-04-01%2009:30/presents'
    headers = {'Content-Type':'application/json'}

    pl_fail = {}
    pl_students = [True, True]
        
    rput_fail = requests.put(les_url, json.dumps(pl_fail), headers=headers)
    rput_students = requests.put(les_url, json.dumps(pl_students), headers=headers)

    assert rput_fail.status_code == 400
    assert rput_students.status_code == 204