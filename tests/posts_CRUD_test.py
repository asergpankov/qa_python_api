from random import randint
import pytest
import requests
from src.user_enums import UserErrors
from validation_schemas.pydantic_schemas import PostsGet
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

MAX_POSTS_AMOUNT = 100
rand = randint(1, 100)


def test_random_get_pydantic_schema_validation(app):
    res = app.get('/posts')
    validated_res = [PostsGet(**item) for item in res.json()]
    assert str(res.json()[rand]) == str(validated_res[rand].json()).replace('"', "'")


def test_get_all_posts(app):
    res = app.get('/posts')
    assert len(res.json()) == MAX_POSTS_AMOUNT, "[WARN] -- expected max amount of numbers is not 100"


@pytest.mark.parametrize('post_id', [1, 50, MAX_POSTS_AMOUNT])
def test_get_random_positive_posts(app, post_id):
    res = app.get(f'/posts/{post_id}')
    assert res.status_code == 200, UserErrors.EXP_STATUS_200.value
    assert res.json()['id'] == post_id

@pytest.mark.xfail
@pytest.mark.parametrize('post_id', [-1, 0, MAX_POSTS_AMOUNT + 1])
def test_get_corner_values_posts(app, post_id):
    # if not all(map(lambda p: isinstance(p, (str, float)), (a, b, c))):
    if not all(isinstance(e, (int, float)) for e in [post_id]):
        raise TypeError(f'Not valid type {type(post_id)} in params')
    res = app.get(f'/posts/{post_id}')
    assert res.status_code == 404, UserErrors.EXP_STATUS_404.value
    assert len(res.json()) == 0


def test_create_post_positive(app):
    payload = {'user_Id': 1, 'title': 'foo', 'body': 'bars'}
    res = app.post(f'/posts', json=payload)
    assert res.status_code == 201
    j = res.json()
    assert j['user_Id'] == payload['user_Id']
    assert j['title'] == payload['title']
    assert j['body'] == payload['body']
    assert j['id'] == MAX_POSTS_AMOUNT + 1


@pytest.mark.skip(reason='500 caused by type(str) in the post json')
@pytest.mark.parametrize('post_id', [-1, 0, MAX_POSTS_AMOUNT + 1])
def test_create_post_invalid_body(app):
    try:
        res = app.post(f'/posts', json='test_str')
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("[WARN] -- ", err)


def test_update_post_positive(app):
    payload = {'user_Id': 1,
               'title': 'foo_after_put',
               'body': 'bars_after_put',
               'id': 1}
    res = app.put(f"/posts/{payload['id']}", json=payload)
    assert res.status_code == 200
    res_json = res.json()
    assert res_json['user_Id'] == payload['user_Id']
    assert res_json['title'] == payload['title']
    assert res_json['body'] == payload['body']


def test_delete_item(session, base_url):
    res = session.delete(url=f'{base_url}/posts/{rand}')
    assert res.status_code == 200, UserErrors.EXP_STATUS_200.value
    assert len(res.json()) == 0
