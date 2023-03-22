import pytest
from validation_schemas.pydantic_schemas import GetPosts


class TestEndpointsSchemas:
    def test_all_posts_pydantic_schema_validation(self, app):
        """Check all posts with Pydantic schema validator
        1. Each post's structure corresponds to accurate pydantic schema
        """
        code, body = app.get('/posts')
        assert [GetPosts(**item) for item in body], "[WARN] -- post data does not correspond to schema validator"
    # todo add schema check for another endpoints
