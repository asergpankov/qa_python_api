import pytest

import requests


class ApiClient:
    def __init__(self, url):
        self.url = url

    def post(self, path=None, params=None, data=None, json=None, headers=None):
        url = f"{self.url}{path}"
        return requests.post(url=url, params=params, data=data, json=json, headers=headers)

    def get(self, path=None, params=None, headers=None):
        url = f"{self.url}{path}"
        return requests.get(url=url, params=params, headers=headers)

    def put(self, path=None, params=None, data=None, json=None, headers=None):
        url = f"{self.url}{path}"
        return requests.put(url=url, json=None, headers=headers)


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
