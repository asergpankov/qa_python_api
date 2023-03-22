import requests


class ApiClient:
    def __init__(self, url):
        self.url = url

    def post(self, endpoint=None, **kwargs):
        url = f"{self.url}{endpoint}"
        resp = requests.post(url=url, **kwargs)
        return resp.status_code, resp.json()

    def get(self, endpoint=None, **kwargs):
        url = f"{self.url}{endpoint}"
        resp = requests.get(url=url, **kwargs)
        return resp.status_code, resp.json()

    def options(self, endpoint=None, **kwargs):
        url = f"{self.url}{endpoint}"
        return requests.options(url=url, **kwargs)

    def put(self, endpoint=None, **kwargs):
        url = f"{self.url}{endpoint}"
        resp = requests.put(url=url, **kwargs)
        return resp.status_code, resp.json()

    def delete(self, endpoint=None, **kwargs):
        url = f"{self.url}{endpoint}"
        resp = requests.delete(url=url, **kwargs)
        return resp.status_code, resp.json()

