import requests, json

def test_grade_index(url):
    suburl = url + '/grades/'
    cls09a = {'name':'09a'}
    cls10a = {'name':'10a'}

    rgrades = requests.get(suburl)
    data = rgrades.json()

    assert rgrades.status_code == 200
    assert data == [cls09a, cls10a]

def test_grade_students(url):
    urlfail = url + '/grades/08a/students'
    url10a = url + '/grades/10a/students'
    fail1 = {}
    fail2 = {
        'fname':'Carl Friedrich',
        'lname':'Gauß',
        'birthDate':'30.04.1777'
    }
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

    rfail = requests.get(urlfail)
    rget1 = requests.get(url10a)
    r10afail1 = requests.post(url10a, json.dumps(fail1))
    r10afail2 = requests.post(url10a, json.dumps(fail2))
    r10acarl1 = requests.post(url10a, json.dumps(carl))
    r10acarl2 = requests.post(url10a, json.dumps(carl))
    r10alotte = requests.post(url10a, json.dumps(lotte))
    rget2 = requests.get(url10a)
    data = rget2.json()

    assert rfail.status_code == 404
    assert rget1.status_code == 204
    assert r10afail1.status_code == 400
    assert r10afail2.status_code == 400
    assert r10acarl1.status_code == 201
    assert r10acarl2.status_code == 409
    assert r10alotte.status_code == 201
    assert rget2.status_code == 200
    assert data == [carl, lotte]