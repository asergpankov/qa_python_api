import requests


class ApiClient:
    def __init__(self, url):
        self.url = url

    def post(self, endpoint=None, params=None, data=None, json=None, headers=None):
        url = f"{self.url}{endpoint}"
        return requests.post(url=url, params=params, data=data, json=json, headers=headers)

    def get(self, endpoint=None, params=None, headers=None):
        url = f"{self.url}{endpoint}"
        return requests.get(url=url, params=params, headers=headers)

    def options(self, endpoint=None, params=None, headers=None):
        url = f"{self.url}{endpoint}"
        return requests.options(url=url, params=params, headers=headers)

    def put(self, endpoint=None, params=None, data=None, json=None, headers=None):
        url = f"{self.url}{endpoint}"
        return requests.put(url=url, json=None, headers=headers)

    def delete(self, endpoint=None, params=None, headers=None):
        url = f"{self.url}{endpoint}"
        return requests.delete(url=url, params=params, headers=headers)