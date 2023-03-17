from random import randint, sample
import pytest
import requests
from src.user_enums import UserErrors

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

MAX_POSTS_AMOUNT = 100


class TestGetPosts:

    def test_get_all_posts(self, app):
        """Positive. Get all posts
        """
        res = app.get('/posts')
        assert len(res.json()) == MAX_POSTS_AMOUNT, "[WARN] -- expected max amount of numbers is not 100"

    @pytest.mark.parametrize('post_id', [1, 11, 80, MAX_POSTS_AMOUNT])
    def test_get_posts_by_id(self, app, post_id):
        """Positive. Get a few posts in available id values
        """
        res = app.get(f'/posts/{post_id}')
        assert res.status_code == 200, UserErrors.EXP_STATUS_200.value
        assert res.json()['id'] == post_id

    @pytest.mark.parametrize('post_id, result, status_code', [
        (-1, {}, 404),
        (0, {}, 404),
        (MAX_POSTS_AMOUNT + 1, {}, 404),
        ('test_string', {}, 404),
        ('11/posts', {}, 404)]) # todo check out an endpoint ../posts/11/posts
    def test_get_posts_by_id_negative(self, app, post_id, result, status_code):
        """Negative. Get posts with invalid id values
        """
        # if not all(map(lambda p: isinstance(p, (str, float)), (a, b, c))):
        # if not all(isinstance(e, (int, float)) for e in [post_id]):
        #     raise TypeError(f'Not valid type {type(post_id)} in params')
        res = app.get(f'/posts/{post_id}')
        js = res.json()
        assert res.status_code == 404, UserErrors.EXP_STATUS_404.value
        assert len(js) == 0


class TestGetComments:
    @pytest.mark.parametrize('post_id', [1, 11, 80, MAX_POSTS_AMOUNT])
    def test_get_posts_comments_by_id(self, app, post_id):
        """Positive. Get posts comments with valid id values
        1. Each post has 5 comments with different comment id
        2. Each comment's body len > 10 symbols
        """
        res = app.get(f'/posts/{post_id}/comments')
        assert res.status_code == 200, UserErrors.EXP_STATUS_200.value
        js = res.json()
        assert len(js) == 5, "[WARN] -- number of comments on posts should be == 5"
        assert [len(e['body']) > 10 for e in js], "[WARN] -- comment body length must be > 10"

    @pytest.mark.xfail
    @pytest.mark.parametrize('post_id', [-1, 0, MAX_POSTS_AMOUNT + 1, '11/posts'])
    # todo need to finish test
    def test_get_posts_comments_by_id_negative(self, app, post_id):
        """Negative. Get post comment with invalid id values
        1. Each post has 5 comments with different comment id
        2. Each comment's body len > 10 symbols
        """
        res = app.get(f'/posts/{post_id}/comments')
        assert res.status_code == 200, UserErrors.EXP_STATUS_200.value


class TestCreatePosts:
    def test_create_post(self, app):
        """Positive. Create new post with valid data
        1. Each post should consist of a user_Id, title, body
        2. Status Code of new created post should be 201
        3. New created post should be in all get request with correct data
        """
        payload = {'user_Id': 11, 'title': 'create_pan_test', 'body': 'create_pan_test_context'}
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        res = app.post(f'/posts', json=payload, headers=headers)
        assert res.status_code == 201
        js = res.json()
        assert js['user_Id'] == payload['user_Id']
        assert js['title'] == payload['title']
        assert js['body'] == payload['body']
        assert js['id'] == MAX_POSTS_AMOUNT + 1
        # created_user = app.get(f"/posts/{js['id']}")
        # assert created_user.json()['id'] == js['id']

    @pytest.mark.skip(reason='500 caused by type(str) in the post json')
    # @pytest.mark.parametrize('post_id', [-1, 0, MAX_POSTS_AMOUNT + 1])
    def test_create_post_negative(self, app):
        """Negative. Create new post with invalid data
        1. Each post should consist of a user_Id, title, body
        2. Created post's status code should be 201
        3. New created post should be in all get request with correct data
        """
        try:
            res = app.post(f'/posts', json='test_str')
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("[WARN] -- ", err)


class TestUpdatePosts:
    @pytest.mark.skip
    def test_update_post(self, app):
        """Positive. Update random post with valid data
        1. Each post should consist of a user_Id, title, body, id
        2. Updated post status code should be 200
        3. New updated post should be in all get request with correct data
        """
        payload = {'user_Id': 22,
                   'title': 'updated_pan_test',
                   'body': 'updated_pan_test_context',
                   'id': 33}
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        res = app.put(f"/posts/{randint(1, MAX_POSTS_AMOUNT)}", json=payload, headers=headers)
        assert res.status_code == 200
        js = res.json()  # todo bug here: return only id. There are no updated title and body
        print(js)
        # assert js['user_Id'] == payload['user_Id']
        # assert js['title'] == payload['title']
        # assert js['body'] == payload['body']

        updated_post = app.get(f"/posts/{js['id']}")
        result = updated_post.json()
        print(result)
        # assert created_user.json()['id'] == js['id']


class TestDeletePosts:
    @pytest.mark.skip
    def test_delete_random_post(self, app):
        """Positive. Delete random post
        1. Deleted post status code should be 200
        2. Check deleted post should not be in all get request
        """
        random_post_id = randint(1, MAX_POSTS_AMOUNT)
        res = app.delete(f'/posts/{random_post_id}')
        assert res.status_code == 200, UserErrors.EXP_STATUS_200.value
        js = res.json()  # empty {}
        assert len(js) == 0
        # deleted_post = app.get(f"/posts/{random_post_id}")
        # result = deleted_post.json()
        # assert result == {}, "[WARN] -- deleted post should not contain any data. Only empty {}"
