import pytest


class TestEndpointsMethods:

    @pytest.mark.parametrize('endpoint', [
        '/posts',
        '/comments',
        '/albums',
        '/photos',
        '/todos',
        '/users',
    ])
    def test_get_all_endpoints(self, app, endpoint):
        """Check all endpoints with a get method works fine
        1. Status code of all get requests must be == 200
        """
        code, body = app.get(endpoint)
        assert code == 200, f'[WARN] -- Endpoint {endpoint} response code {code} != 200'

    @pytest.mark.parametrize('endpoint', [
        '/posts',
        '/comments',
        '/albums',
        '/photos',
        '/todos',
        '/users',
    ])
    def test_allowed_methods(self, app, endpoint):
        """
        1. Check status code is 204 - no content
        2. Check all endpoints maintain allowed methods
        """
        allowed_methods = ['GET', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE']
        methods = app.options(endpoint)
        assert methods.status_code == 204
        supported_methods = methods.headers['Access-Control-Allow-Methods'].split(',')
        assert all(e in allowed_methods for e in supported_methods), \
            f"[WARN] -- The endpoint {endpoint} should support the following methods: {allowed_methods}, \
            currently supports only - {methods}"
