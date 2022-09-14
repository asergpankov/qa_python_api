import pytest

import requests

def pytest_addoption(parser):
    parser.addoption(
        '--env',
        action='store',
        default='https://jsonplaceholder.typicode.com', #cmd: pytest -v --env=https://jsonplaceholder-rc.typicode.com
        help='available environments: dev, stage, prod',
        choices=('https://jsonplaceholder.typicode.com', 'https://jsonplaceholder-rc.typicode.com'),
    )


@pytest.fixture(scope='module')
def base_url(request):
    return request.config.getoption('--env')


@pytest.fixture(scope='module')
def session():
    return requests.Session()
