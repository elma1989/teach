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