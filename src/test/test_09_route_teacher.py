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