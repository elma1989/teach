import requests
from database import indb

def test_subject(url):
    suburl = url + '/subjects/'
    fail = {}
    failabr = {
        'abr':'math',
        'name':'Mathematik'
    }
    failname = {
        'abr':'MAT',
        'name':'mathematik'
    }
    mat = {
        'abr':'MAT',
        'name':'Mathematik'
    }
    deu = {
        'abr':'DEU',
        'name':'Deutsch'
    }

    indb()

    rg_subjects1 = requests.get(suburl)
    rp_fail = requests.post(suburl, fail)
    rp_failabr = requests.post(suburl, failabr)
    rp_failname = requests.post(suburl, failname)
    rp_mat1 = requests.post(suburl, mat)
    rp_mat2 = requests.post(suburl, mat)
    rp_deu = requests.post(suburl, deu)
    rg_subjects2 = requests.get(suburl)

    assert rg_subjects1.status_code == 204
    assert rp_fail.status_code == 400
    assert rp_failabr.status_code == 400
    assert rp_failname.status_code == 400
    assert rp_mat1.status_code == 201
    assert rp_mat2.status_code == 409
    assert rp_deu.status_code == 201
    assert rg_subjects2.status_code == 200
    data = rg_subjects2.json()
    assert data == [deu, mat]