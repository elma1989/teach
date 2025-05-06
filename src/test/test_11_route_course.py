import requests, json

def test_teacher_course(url):
    suburl = url + '/teachers/'
    fail = suburl + '3/courses'
    johnurl = suburl + '1/courses'
    maxmurl = suburl + '2/courses'
    crsfail = {}
    eng1 = {
        'name':'ENG 1',
        'subject':'eng'
    }
    mat1 = {
        'name':'MAT 1',
        'subject':'mat'
    }
    deu1 = {
        'name':'DEU 1',
        'subject':'deu'
    }
    mat1out = {
        'name':'MAT 1',
        'subject': {
            'abr':'MAT',
            'name':'Mathematik'
        }
    }
    deu1out = {
        'name':'DEU 1',
        'subject': {
            'abr':'DEU',
            'name':'Deutsch'
        }
    }

    rfail = requests.get(fail)
    rjohncrs1 = requests.get(johnurl)
    rmaxmcrs1 = requests.get(maxmurl)
    rjohnfail = requests.post(johnurl,json.dumps(crsfail), headers={'Content-Type':'application/json'})
    rjohneng = requests.post(johnurl,json.dumps(eng1), headers={'Content-Type':'application/json'})
    rjohnmat1 = requests.post(johnurl,json.dumps(mat1), headers={'Content-Type':'application/json'})
    rjohnmat2 = requests.post(johnurl,json.dumps(mat1), headers={'Content-Type':'application/json'})
    rmaxmdeu = requests.post(maxmurl,json.dumps(deu1), headers={'Content-Type':'application/json'})
    rjohncrs2 = requests.get(johnurl)
    rmaxmcrs2 = requests.get(maxmurl)

    assert rfail.status_code == 404
    assert rjohncrs1.status_code == 204
    assert rmaxmcrs1.status_code == 204
    assert rjohnfail.status_code == 400
    assert rjohneng.status_code == 404
    assert rjohnmat1.status_code == 201
    assert rjohnmat2.status_code == 409
    assert rmaxmdeu.status_code == 201
    assert rjohncrs2.status_code == 200
    assert rmaxmcrs2.status_code == 200

    johndata = rjohncrs2.json()
    maxmdata = rmaxmcrs2.json()
    assert johndata == [mat1out]
    assert maxmdata == [deu1out]

def test_teacher_single_course(url):
    suburl = url + '/teachers/'
    header = {'Content-Type':'application/json'}
    failteachurl = suburl + '4/courses/MAT%201'
    failcourseurl = suburl + '1/courses/ENG%201'
    johnmaturl = suburl + '1/courses/MAT%201'
    johndeuurl = suburl + '1/courses/DEU%201'
    isaacurl = suburl + '3/courses/DEU%201' 

    isaac = {
        'fname':'Isaac',
        'lname':'Newton',
        'birthDate':'1643-01-04'
    }
    mat = {'abr':'mat'}
    phy = {
        'abr':'phy',
        'name':'Physik'
    }
    mat1 = {
        'name':'MAT 1',
        'subject': {
            'abr':'MAT',
            'name':'Mathematik'
        }
    }

    risaacadd = requests.post(suburl,json.dumps(isaac),headers=header)
    assert risaacadd.status_code == 201
    risaacadd = requests.post(url + '/subjects/',json.dumps(phy),headers=header)
    assert risaacadd.status_code == 201
    risaacadd = requests.post(suburl + '3/subjects',json.dumps(mat),headers=header)
    assert risaacadd.status_code == 201
    risaacadd = requests.post(suburl + '3/subjects',json.dumps(phy),headers=header)
    assert risaacadd.status_code == 201

    rfailteach = requests.get(failteachurl)
    rfailcourse = requests.get(failcourseurl)
    rgjohndeu = requests.get(johndeuurl)
    rgjohnmat = requests.get(johnmaturl)
    rpisaacdeu = requests.put(isaacurl)
    rpjohndeu = requests.put(johndeuurl)

    assert rfailteach.status_code == 404
    assert rfailcourse.status_code == 404
    assert rgjohndeu.status_code == 404
    assert rgjohnmat.status_code == 200
    assert rpisaacdeu.status_code == 409
    assert rpjohndeu.status_code == 200
    johnmatdata = rgjohnmat.json()
    assert johnmatdata == mat1

def test_mgm_students(url):
    suburl = url + '/teachers/'
    member_mat1 = suburl + '1/courses/MAT%201/students'
    fail_teach_url = suburl + '4/courses/MAT%201/students/1'
    fail_course_url = suburl + '1/courses/ENG%201/students/1'
    fail_student_url = suburl + '1/courses/MAT%201/students/3'
    john_mat1_url = suburl + '1/courses/MAT%201/students/1'
    lotte_mat1_url = suburl + '1/courses/MAT%201/students/2'

    carl = {
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'1777-04-30',
        'id':1
    }
    lotte = {
        'fname':'Lotte',
        'lname':'Rie',
        'birthDate':'2010-05-05',
        'id':2
    }

    rg_member1_mat1 = requests.get(member_mat1)
    rp_fail_teach = requests.put(fail_teach_url)
    rp_fail_course = requests.put(fail_course_url)
    rp_fail_student = requests.put(fail_student_url)
    rp_john1_mat1 = requests.put(john_mat1_url)
    rp_john2_mat1 = requests.put(john_mat1_url)
    rp_lotte_mat1 = requests.put(lotte_mat1_url)
    rg_member2_mat1 = requests.get(member_mat1)

    assert rg_member1_mat1.status_code == 204
    assert rp_fail_teach.status_code == 404
    assert rp_fail_course.status_code == 404
    assert rp_fail_student.status_code == 404
    assert rp_john1_mat1.status_code == 200
    assert rp_john2_mat1.status_code == 409
    assert rp_lotte_mat1.status_code == 200
    assert rg_member2_mat1.status_code == 200
    data = rg_member2_mat1.json()
    assert data == [carl, lotte]