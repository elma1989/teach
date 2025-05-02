import pytest

@pytest.fixture
def url():
    value = 'http://localhost:5000'
    return value