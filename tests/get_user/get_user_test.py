import sys

import pytest

from base_classes.base_classes import Response
from validation_schemas.pydantic_schemas import UserSchema


# r = requests.get(url=SERVICE_URL)
# # print(r.__getstate__())
# print(r.json().get("data"))


@pytest.mark.skipif(sys.version_info < (3, 5), reason="requires python3.5 or higher")
def test_getting_data_from_get(get_users):
    Response(get_users).assert_status_code(200).validate(UserSchema)
    assert len(get_users.json()) == 2, "[WARN] -- json_len isn't correct"


