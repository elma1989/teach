import requests

def test_grade_index(url):
    suburl = url + '/grades/'
    cls09a = {'name':'09a'}
    cls10a = {'name':'10a'}

    rgrades = requests.get(suburl)
    data = rgrades.json()

    assert rgrades.status_code == 200
    assert data == [cls09a, cls10a]