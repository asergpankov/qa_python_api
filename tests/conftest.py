import pytest
import requests

from api_client import ApiClient


@pytest.fixture
def app():
    return ApiClient(url="https://jsonplaceholder.typicode.com")


def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     default='https://jsonplaceholder.typicode.com',
                     # cmd: pytest -v --env=https://jsonplaceholder-rc.typicode.com
                     help='available environments: dev, stage, prod',
                     choices=('https://jsonplaceholder.typicode.com', 'https://test_jsonplaceholder.typicode.com'),
                     )


@pytest.fixture(scope='function')
def base_url(request):
    return request.config.getoption('--env')


@pytest.fixture(scope='module')
def session():
    return requests.Session()
