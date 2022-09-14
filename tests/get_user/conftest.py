import pytest
import requests
from configurations import SERVICE_URL


@pytest.fixture(scope='module')
def get_users():
    r = requests.get(url=SERVICE_URL)
    return r
