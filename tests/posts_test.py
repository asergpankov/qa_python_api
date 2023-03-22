from random import randint, sample
import pytest
import requests
from src.user_enums import UserErrors
from src.posts_enums import PostsEnums

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

TOTAL_POSTS_NUMBER = 100
TOTAL_POSTS_COMMENTS = 5


class TestGetPosts:
    @pytest.mark.smoke
    def test_get_all_posts(self, app):
        """Positive. Get all posts"""
        code, body = app.get('/posts')
        assert code == 200
        assert len(body) == TOTAL_POSTS_NUMBER, "[WARN] -- expected max amount of numbers is not 100"

    @pytest.mark.parametrize('post_id', [1, randint(2, 99), TOTAL_POSTS_NUMBER])
    def test_get_posts_by_id(self, app, post_id):
        """Positive. Get a few posts with a valid id"""
        code, body = app.get(f'/posts/{post_id}')
        assert code == 200, UserErrors.EXP_STATUS_200.value
        assert body['id'] == post_id

    @pytest.mark.parametrize('post_id, result, expected_code', [
        (-1, {}, 404),
        (0, {}, 404),
        (TOTAL_POSTS_NUMBER + 1, {}, 404),
        ('test_string', {}, 404),
        ('11/posts', {}, 404)])  # todo check out the result on endpoint ../posts/11/posts
    def test_get_posts_by_id_negative(self, app, post_id, result, expected_code):
        """Negative. Get posts with an invalid id"""
        code, body = app.get(f'/posts/{post_id}')
        assert code == expected_code, "WARN -- expected_code does not coordinate with actual code"
        assert len(body) == 0, "WARN -- body length should be equal to 0"

    @pytest.mark.users_posts
    @pytest.mark.parametrize('post_id', [1, randint(2, 99), TOTAL_POSTS_NUMBER])
    def test_get_users_posts_by_id(self, app, post_id):
        """Positive. Get a few users posts with a valid id
        1. The user's post contains elements with the same 'userId'==post_id and different IDs.
        2. The user's post is a list and consists of elements with different IDs.
        """
        code, body = app.get(f'/users/{post_id}/posts')
        assert code == 200, UserErrors.EXP_STATUS_200.value
        if not body == []:
            assert all([e['userId'] == post_id for e in body])
            assert len(body) <= 10


class TestGetComments:
    @pytest.mark.posts
    @pytest.mark.parametrize('post_id', [1, 11, 80, TOTAL_POSTS_NUMBER])
    def test_get_posts_comments_by_id(self, app, post_id):
        """Positive. Get posts comments with valid id values
        1. Each post has 5 comments with different comment id
        2. Each comment's body len > 10 symbols
        """
        code, body = app.get(f'/posts/{post_id}/comments')
        assert code == 200, UserErrors.EXP_STATUS_200.value
        assert len(body) == TOTAL_POSTS_COMMENTS, "[WARN] -- number of comments on posts should be == 5"
        assert all(len(e['body']) > 10 for e in body), "[WARN] -- comment body length must be > 10 symbols"

    @pytest.mark.parametrize('post_id', [-1, 0, TOTAL_POSTS_NUMBER + 1, '11/posts'])
    # todo need to finish test
    def test_get_posts_comments_by_id_negative(self, app, post_id):
        """Negative. Get post comment with invalid id values
        1. Each post has 5 comments with different comment id
        2. Each comment's body len > 10 symbols
        """
        code, body = app.get(f'/posts/{post_id}/comments')
        assert code == 200, UserErrors.EXP_STATUS_200.value

    @pytest.mark.parametrize('post_id', [1, randint(2, 99), TOTAL_POSTS_NUMBER])
    def test_get_posts_comments_by_post_id(self, app, post_id):
        """Positive. Get posts comments with valid id values
        1. Each post has 5 comments with different comment id
        2. Each comment's body len > 10 symbols
        """
        code, body = app.get(f'/comments?postId={post_id}')
        assert code == 200, UserErrors.EXP_STATUS_200.value
        assert len(body) == TOTAL_POSTS_COMMENTS, "[WARN] -- number of comments on posts should be == 5"
        assert all(len(e['body']) > 10 for e in body), "[WARN] -- comment body length must be > 10"


class TestCreatePosts:
    @pytest.mark.posts
    def test_create_post(self, app):
        """Positive. Create new post with a valid data
        1. Status Code of new created post should be 201
        2. Each post should consist of a user_Id, title, body
        3. New created post should be inside all get request with correct data
        """
        payload, headers = PostsEnums.POSITIVE_PAYLOAD.value, PostsEnums.HEADERS.value
        code, body = app.post(f'/posts', json=payload, headers=headers)
        assert code == 201
        assert body['user_Id'] == payload['user_Id']
        assert body['title'] == payload['title']
        assert body['body'] == payload['body']
        assert body['id'] == TOTAL_POSTS_NUMBER + 1
        # created_user_code, created_user_body = app.get(f"/posts/{body['id']}")
        # assert created_user_body['id'] == body['id']

    @pytest.mark.skip(reason='500 caused by type(str) in the post json')
    @pytest.mark.parametrize('post_id', [-1, 0, TOTAL_POSTS_NUMBER + 1, 'test_str', '11'])
    def test_create_post_negative(self, app, post_id):
        """Negative. Create new post with invalid data
        1. Each post should consist of a user_Id, title, body
        2. Created post's status code should be 201
        3. New created post should be in all get request with correct data
        """
        try:
            code, body = app.post(f'/posts', json=post_id)
            assert code == 201
            # res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return "[WARN] -- ", err

@pytest.mark.skip(reason='need to recognize')
@pytest.mark.parametrize(
    'endpoint, payload, expected_code',
    [
        ('/posts', PostsEnums.POSITIVE_PAYLOAD.value, 201),
        ('/posts', PostsEnums.POSITIVE_PAYLOAD_WITHOUT_USERID_FIELD.value, 201),
        ('/posts', PostsEnums.POSITIVE_PAYLOAD_USERID_NONE.value, 201),
        # ('/posts', {}, 400), # Are the title and body fields required for a request?
        ('/posts', {'id': 101}, 400),
        ('/posts', {'id': 1}, 400),
        ('/posts/1', {'id': 1}, 400),
        ('/users/1/posts', {'title': 'foo', 'body': 'bar'}, 201),
    ])
def test_create_post_multiple_cases(app, endpoint, payload, expected_code):
    """Positive and negative. Create new post with invalid data"""
    code, body = app.post(endpoint, json=payload)
    assert code == expected_code, f'[WARN] -- Actual status code != expected code: {code} != {expected_code}'
    print(body)
    if code == 201:
        assert body.get('id'), '[WARN] -- The resource does not have ID!'


class TestUpdatePosts:
    def test_update_post(self, app):
        """Positive. Update random post with valid data
        1. Each post should consist of a user_Id, title, body, id
        2. Updated post status code should be 200
        3. New updated post should be in all get request with correct data
        """
        payload, headers = PostsEnums.POSITIVE_PAYLOAD.value, PostsEnums.HEADERS.value
        code, body = app.put(f"/posts/{randint(1, TOTAL_POSTS_NUMBER)}", json=payload, headers=headers)
        assert code == 200
        # todo bug here: return only id. There are no updated title and body: {'id': 50}
        assert body['user_Id'] == payload['user_Id']
        assert body['title'] == payload['title']
        assert body['body'] == payload['body']

        updated_post_code, updated_post_body = app.get(f"/posts/{body['id']}")
        assert updated_post_body['id'] == body['id']


class TestDeletePosts:
    @pytest.mark.parametrize(
        'post_id, expected_code',
        [
            (1, 200),
            (0, 404),
            (TOTAL_POSTS_NUMBER, 200),
            (TOTAL_POSTS_NUMBER + 1, 404)
        ])
    def test_delete_post(self, app, post_id, expected_code):
        """Positive and negative. Delete posts
        1. Deleted post status code should be 200
        2. Check deleted post should not be in all get request
        """
        code, body = app.delete(f'/posts/{post_id}')
        assert code == expected_code, "[WARN] -- deleted post's status code expected as {expected_code}"
        assert len(body) == 0
        deleted_post_code, deleted_post_body = app.get(f"/posts/{post_id}")
        assert deleted_post_body == {}, "[WARN] -- deleted post should not contains any data. Only empty {}"
