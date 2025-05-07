import pytest

url = 'http://localhost:5000'

@pytest.fixture
def url(): 
    global url
    return url

@pytest.fixture
def teachurl(): 
    global url
    return url + '/teachers/'