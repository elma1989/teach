import json, requests

def test_teachers(url):
    suburl = url + '/teachers/'
    fail1 = {'fname':'John'}
    fail2 = {
        'fname':'John',
        'lname':'Doe',
        'birthDate':'01.01.1990'
    }
    john = {
        'fname':'John',
        'lname':'Doe',
        'birthDate':'1990-01-01'
    }
    maxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birthDate':'1991-12-31'
    }

    rteach1 = requests.get(suburl)
    rfail1 = requests.post(suburl, json.dumps(fail1))
    rfail2 = requests.post(suburl, json.dumps(fail2))
    rjohn1 = requests.post(suburl, json.dumps(john))
    rjohn2 = requests.post(suburl, json.dumps(john))
    rmaxm = requests.post(suburl, json.dumps(maxm))
    rteach2 = requests.get(suburl)
    data = rteach2.json()
    john['id'] = 1
    maxm['id'] = 2

    assert rteach1.status_code == 404
    assert rfail1.status_code == 400
    assert rfail2.status_code == 400
    assert rjohn1.status_code == 201
    assert rjohn2.status_code == 409
    assert rmaxm.status_code == 201
    assert rteach2.status_code == 200
    assert data == [john,maxm]

def test_single_teacher(url):
    suburl = url + '/teachers/'
    john = {
        'fname':'John',
        'lname':'Doe',
        'birthDate':'1990-01-01',
        'id':1
    }
    maxm = {
        'fname':'Max',
        'lname':'Mustermann',
        'birthDate':'1991-12-31',
        'id':2
    }

    rfail = requests.get(suburl + '3')
    rjohn = requests.get(suburl + '1')
    rmaxm = requests.get(suburl + '2')
    johndat = rjohn.json()
    maxmdat = rmaxm.json()

    assert rfail.status_code == 404
    assert rjohn.status_code == 200
    assert rmaxm.status_code == 200
    assert johndat == john
    assert maxmdat == maxm

def test_teacher_subject(url):
    suburl = url + '/teachers/'
    failurl = suburl + '3/subjects'
    johnurl = suburl + '1/subjects'
    maxmurl = suburl + '2/subjects'
    fail = {}
    mat = {
        'abr':'MAT',
        'name':'Mathematik'
    }
    deu = {
        'abr':'DEU',
        'name':'Deutsch'
    }
    eng = {
        'abr':'ENG',
        'name':'Englisch'
    }
    
    rfail = requests.get(failurl)
    rjohnsub1 = requests.get(johnurl)
    rmaxmsub1 = requests.get(maxmurl)
    rjohnfail = requests.post(johnurl, json.dumps(fail))
    rjohnmat1 = requests.post(johnurl, json.dumps(mat))
    rjohnmat2 = requests.post(johnurl, json.dumps(mat))
    rjohndeu = requests.post(johnurl, json.dumps(deu))
    rjohneng = requests.post(johnurl, json.dumps(eng))
    rmaxmmat = requests.post(maxmurl, json.dumps(mat))
    rmaxmdeu = requests.post(maxmurl, json.dumps(deu))
    rjohnsub2 = requests.get(johnurl)
    rmaxmsub2 = requests.get(maxmurl)
    johnsubdata = rjohnsub2.json()
    maxmsubdata = rmaxmsub2.json()

    assert rfail.status_code == 404
    assert rjohnsub1.status_code == 204
    assert rmaxmsub1.status_code == 204
    assert rjohnfail.status_code == 400
    assert rjohnmat1.status_code == 201
    assert rjohnmat2.status_code == 409
    assert rjohndeu.status_code == 201
    assert rjohneng.status_code == 404
    assert rmaxmmat.status_code == 201
    assert rmaxmdeu.status_code == 201
    assert rjohnsub2.status_code == 200
    assert rmaxmsub2.status_code == 200
    assert johnsubdata == [deu, mat]
    assert maxmsubdata == [deu, mat]

def test_teacher_grade(url):
    suburl = url + '/teachers/'
    failurl = suburl + '3/grades'
    johnurl = suburl + '1/grades'
    maxmurl = suburl + '2/grades'
    fail = {}
    cls10a = {'name':'10a'}
    cls09a = {'name':'09a'}

    rfail = requests.get(failurl)
    rjohngrade1 = requests.get(johnurl)
    rmaxmgrade1 = requests.get(maxmurl)
    rjohnfail = requests.post(johnurl, json.dumps(fail))
    rjohn10a1 = requests.post(johnurl, json.dumps(cls10a))
    rjohn10a2 = requests.post(johnurl, json.dumps(cls10a))
    rmaxm09a = requests.post(maxmurl, json.dumps(cls09a))
    rjohngrade2 = requests.get(johnurl)
    rmaxmgrade2 = requests.get(maxmurl)
    cls10adat = rjohngrade2.json()
    cls09adat = rmaxmgrade2.json()

    assert rfail.status_code == 404
    assert rjohngrade1.status_code == 204
    assert rmaxmgrade1.status_code == 204
    assert rjohnfail.status_code == 400
    assert rjohn10a1.status_code == 201
    assert rjohn10a2.status_code == 409
    assert rmaxm09a.status_code == 201
    assert rjohngrade2.status_code == 200
    assert rmaxmgrade2.status_code == 200
    assert cls10adat == [cls10a]
    assert cls09adat == [cls09a]

def test_grade_change_leader(url):
    suburl = url + '/teachers/'
    failurl = suburl + '3/grades/10a'
    johnfailurl = suburl + '1/grades/08a'
    john09aurl = suburl + '1/grades/09a'

    rfail = requests.put(failurl)
    rjohnfail = requests.put(johnfailurl)
    rjohn09a = requests.put(john09aurl)

    assert rfail.status_code == 404
    assert rjohnfail.status_code == 404
    assert rjohn09a.status_code == 200