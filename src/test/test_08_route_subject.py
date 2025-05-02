import requests, json
from database import indb

def test_subjects(url):
    suburl = url + '/subjects/'
    fail1 = {'abr':'eng'}
    fail2 = {
        'abr':'eng',
        'name':'englisch'
    }
    mat = {
        'abr':'MAT',
        'name':'Mathematik'
    }
    deu = {
        'abr':'DEU',
        'name':'Deutsch'
    }
    subjects = [deu,mat]

    indb()

    rsub1 = requests.get(suburl)
    rfail1 = requests.post(suburl, json.dumps(fail1))
    rfail2 = requests.post(suburl, json.dumps(fail2))
    rmat1 = requests.post(suburl, json.dumps(mat))
    rmat2 = requests.post(suburl, json.dumps(mat))
    rdeu = requests.post(suburl, json.dumps(deu))
    rsub2 = requests.get(suburl)
    data = rsub2.json()

    assert rsub1.status_code == 404
    assert rfail1.status_code == 400
    assert rfail2.status_code == 400
    assert rmat1.status_code == 201
    assert rmat2.status_code == 409
    assert rdeu.status_code == 201
    assert rsub2.status_code == 200
    assert data == subjects

def test_single_subject(url):
    suburl = url + '/subjects/'
    mat = {
        'abr':'MAT',
        'name':'Mathematik'
    }
    deu = {
        'abr':'DEU',
        'name':'Deutsch'
    }

    rfail = requests.get(suburl + 'eng')
    rmat = requests.get(suburl + 'mat')
    rdeu = requests.get(suburl + 'deu')
    matdat = rmat.json()
    deudat = rdeu.json()

    assert rfail.status_code == 404
    assert rmat.status_code == 200
    assert rdeu.status_code == 200
    assert matdat == mat
    assert deudat == deu