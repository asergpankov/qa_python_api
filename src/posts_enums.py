from enum import Enum


class PostsEnums(Enum):
    HEADERS = {'Content-type': 'application/json; charset=UTF-8'}
    POSITIVE_PAYLOAD = {
        'user_Id': 11,
        'title': 'create_pan_test',
        'body': 'create_pan_test_context'
    }
    POSITIVE_PAYLOAD_FOR_USERS = {
        'title': 'create_pan_test',
        'body': 'create_pan_test_context'
    }
    POSITIVE_PAYLOAD_WITHOUT_USERID_FIELD = {
        'title': 'create_pan_test',
        'body': 'create_pan_test_context'
    }
    NEGATIVE_PAYLOAD_USERID_STR = {
        'user_Id': '11',
        'title': 'create_pan_test',
        'body': 'create_pan_test_context'
    }
    POSITIVE_PAYLOAD_USERID_NONE = {
        'user_Id': None,
        'title': 'create_pan_test',
        'body': 'create_pan_test_context'
    }