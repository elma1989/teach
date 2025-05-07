import pytest

@pytest.fixture
def url(): 
    return 'http://localhost:5000'

@pytest.fixture
def teachurl(): 
    return 'http://localhost:5000/teachers/'